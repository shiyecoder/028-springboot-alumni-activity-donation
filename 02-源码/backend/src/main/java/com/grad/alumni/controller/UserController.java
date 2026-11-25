package com.grad.alumni.controller;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.grad.alumni.common.BizException;
import com.grad.alumni.common.PageResult;
import com.grad.alumni.common.R;
import com.grad.alumni.common.UserContext;
import com.grad.alumni.entity.SysRole;
import com.grad.alumni.entity.SysUser;
import com.grad.alumni.mapper.SysRoleMapper;
import com.grad.alumni.mapper.SysUserMapper;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.*;

/** 用户管理：任何接口都不返回 password 字段 */
@RestController
@RequestMapping("/api/user")
public class UserController extends BaseController<SysUser> {

    private final SysUserMapper mapper;
    private final SysRoleMapper roleMapper;
    private final PasswordEncoder encoder;

    public UserController(SysUserMapper mapper, SysRoleMapper roleMapper, PasswordEncoder encoder) {
        this.mapper = mapper;
        this.roleMapper = roleMapper;
        this.encoder = encoder;
    }

    @Override
    protected BaseMapper<SysUser> mapper() { return mapper; }

    @Override
    protected String kwColumn() { return "real_name"; }

    @Override
    protected Map<String, String> extraFilters() { return Map.of("roleId", "role_id"); }

    /** 覆盖基类分页：返回前清空密码字段，并附加角色名 */
    @Override
    @GetMapping("/page")
    public R<PageResult<SysUser>> page(@RequestParam(defaultValue = "1") long page,
                                       @RequestParam(defaultValue = "10") long size,
                                       @RequestParam(required = false) String kw,
                                       @RequestParam(required = false) String status,
                                       @RequestParam Map<String, String> params) {
        QueryWrapper<SysUser> q = new QueryWrapper<>();
        if (kw != null && !kw.isBlank()) q.and(w -> w.like("real_name", kw).or().like("username", kw));
        if (params.get("roleId") != null && !params.get("roleId").isBlank()) {
            q.eq("role_id", params.get("roleId"));
        }
        q.orderByDesc("create_time");
        Page<SysUser> p = mapper.selectPage(new Page<>(page, size), q);
        p.getRecords().forEach(u -> u.setPassword(null));
        return R.ok(PageResult.of(p));
    }

    @Override
    @GetMapping("/{id}")
    public R<SysUser> detail(@PathVariable Long id) {
        SysUser u = mapper.selectById(id);
        if (u == null) throw new BizException("用户不存在");
        u.setPassword(null);
        return R.ok(u);
    }

    @PostMapping
    public R<SysUser> create(@RequestBody SysUser body) {
        if (body.getUsername() == null || body.getUsername().isBlank()) throw new BizException("账号不能为空");
        Long cnt = mapper.selectCount(new QueryWrapper<SysUser>().eq("username", body.getUsername().trim()));
        if (cnt != null && cnt > 0) throw new BizException("账号已存在");
        String raw = body.getPassword() == null || body.getPassword().isBlank() ? "123456" : body.getPassword();
        body.setPassword(encoder.encode(raw));
        body.setCreateTime(LocalDateTime.now());
        body.setUpdateTime(LocalDateTime.now());
        body.setDeleted(0);
        body.setStatus(body.getStatus() == null ? 1 : body.getStatus());
        mapper.insert(body);
        body.setPassword(null);
        return R.ok(body);
    }

    /** 更新前钩子：密码只能通过重置接口修改，这里强制清空 */
    @Override
    protected void beforeSave(SysUser body, boolean create) {
        if (!create) {
            body.setPassword(null);
        }
    }

    @PostMapping("/{id}/reset-password")
    public R<Void> reset(@PathVariable Long id, @RequestBody(required = false) Map<String, String> body) {
        String raw = body == null ? null : body.get("password");
        if (raw == null || raw.length() < 6) raw = "123456";
        SysUser u = new SysUser();
        u.setId(id);
        u.setPassword(encoder.encode(raw));
        u.setLoginFailCount(0);
        u.setLockUntil(null);
        mapper.updateById(u);
        return R.ok();
    }

    /** 修改自己的密码：校验原密码 */
    @PostMapping("/change-password")
    public R<Void> changePassword(@RequestBody Map<String, String> body) {
        SysUser u = mapper.selectById(UserContext.userId());
        if (!encoder.matches(body.getOrDefault("oldPassword", ""), u.getPassword())) {
            throw new BizException("原密码不正确");
        }
        String np = body.getOrDefault("newPassword", "");
        if (np.length() < 6) throw new BizException("新密码至少 6 位");
        SysUser up = new SysUser();
        up.setId(u.getId());
        up.setPassword(encoder.encode(np));
        mapper.updateById(up);
        return R.ok();
    }

    /** 个人资料：姓名、联系方式、头像，头像上传后右上角同步 */
    @PostMapping("/profile")
    public R<Map<String, Object>> updateProfile(@RequestBody Map<String, String> body) {
        SysUser u = new SysUser();
        u.setId(UserContext.userId());
        u.setRealName(body.get("realName"));
        u.setPhone(body.get("phone"));
        u.setEmail(body.get("email"));
        u.setAvatar(body.get("avatar"));
        u.setUpdateTime(LocalDateTime.now());
        mapper.updateById(u);
        SysUser fresh = mapper.selectById(u.getId());
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("realName", fresh.getRealName());
        out.put("avatar", fresh.getAvatar());
        out.put("phone", fresh.getPhone());
        out.put("email", fresh.getEmail());
        return R.ok(out);
    }

    @GetMapping("/roles")
    public R<List<SysRole>> roles() {
        return R.ok(roleMapper.selectList(null));
    }
}
