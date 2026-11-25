package com.grad.alumni.controller;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.grad.alumni.common.BizException;
import com.grad.alumni.common.JwtUtil;
import com.grad.alumni.common.R;
import com.grad.alumni.common.UserContext;
import com.grad.alumni.entity.*;
import com.grad.alumni.mapper.*;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.*;

/** 登录认证：连续失败 5 次锁定 10 分钟；返回 token、登录人信息与动态菜单 */
@RestController
@RequestMapping("/api/auth")
public class AuthController {

    private final SysUserMapper userMapper;
    private final SysRoleMapper roleMapper;
    private final SysMenuMapper menuMapper;
    private final SysRoleMenuMapper roleMenuMapper;
    private final SysOrgMapper orgMapper;
    private final AlumniProfileMapper profileMapper;
    private final PasswordEncoder encoder;
    private final JwtUtil jwtUtil;

    @Value("${app.login-fail-limit:5}")
    private int failLimit;

    @Value("${app.login-lock-minutes:10}")
    private int lockMinutes;

    public AuthController(SysUserMapper userMapper, SysRoleMapper roleMapper, SysMenuMapper menuMapper,
                          SysRoleMenuMapper roleMenuMapper, SysOrgMapper orgMapper,
                          AlumniProfileMapper profileMapper, PasswordEncoder encoder, JwtUtil jwtUtil) {
        this.userMapper = userMapper;
        this.roleMapper = roleMapper;
        this.menuMapper = menuMapper;
        this.roleMenuMapper = roleMenuMapper;
        this.orgMapper = orgMapper;
        this.profileMapper = profileMapper;
        this.encoder = encoder;
        this.jwtUtil = jwtUtil;
    }

    @PostMapping("/login")
    public R<Map<String, Object>> login(@RequestBody Map<String, String> body) {
        String username = body.getOrDefault("username", "").trim();
        String password = body.getOrDefault("password", "");
        if (username.isEmpty() || password.isEmpty()) {
            throw new BizException("账号和密码不能为空");
        }
        SysUser user = userMapper.selectOne(new QueryWrapper<SysUser>().eq("username", username).last("limit 1"));
        if (user == null) {
            throw new BizException("账号或密码错误");
        }
        if (user.getStatus() != null && user.getStatus() == 0) {
            throw new BizException("账号已停用，请联系管理员");
        }
        if (user.getLockUntil() != null && user.getLockUntil().isAfter(LocalDateTime.now())) {
            throw new BizException("登录失败次数过多，账号锁定至 " + user.getLockUntil());
        }
        if (!encoder.matches(password, user.getPassword())) {
            int fail = (user.getLoginFailCount() == null ? 0 : user.getLoginFailCount()) + 1;
            user.setLoginFailCount(fail);
            if (fail >= failLimit) {
                user.setLockUntil(LocalDateTime.now().plusMinutes(lockMinutes));
                user.setLoginFailCount(0);
            }
            userMapper.updateById(user);
            throw new BizException(fail >= failLimit ? "连续失败 " + failLimit + " 次，账号已锁定 " + lockMinutes + " 分钟"
                    : "账号或密码错误，还可尝试 " + (failLimit - fail) + " 次");
        }
        SysRole role = roleMapper.selectById(user.getRoleId());
        user.setLoginFailCount(0);
        user.setLockUntil(null);
        user.setLastLoginTime(LocalDateTime.now());
        userMapper.updateById(user);

        Map<String, Object> claims = new HashMap<>();
        claims.put("name", user.getRealName());
        claims.put("role", role == null ? "ALUMNI" : role.getRoleCode());
        claims.put("orgId", user.getOrgId());
        claims.put("scope", role == null ? "SELF" : role.getDataScope());
        String token = jwtUtil.create(claims, user.getId());

        Map<String, Object> info = new HashMap<>();
        info.put("id", user.getId());
        info.put("username", user.getUsername());
        info.put("realName", user.getRealName());
        info.put("avatar", user.getAvatar());
        info.put("phone", user.getPhone());
        info.put("email", user.getEmail());
        info.put("roleCode", role == null ? "ALUMNI" : role.getRoleCode());
        info.put("roleName", role == null ? "校友" : role.getRoleName());
        info.put("dataScope", role == null ? "SELF" : role.getDataScope());
        info.put("orgId", user.getOrgId());
        SysOrg org = user.getOrgId() == null ? null : orgMapper.selectById(user.getOrgId());
        info.put("orgName", org == null ? "" : org.getOrgName());

        Map<String, Object> out = new HashMap<>();
        out.put("token", token);
        out.put("user", info);
        out.put("menus", menusOf(user.getRoleId()));
        return R.ok(out);
    }

    /** 按角色动态获取菜单：只返回类型为 M/C 且可见的项 */
    private List<Map<String, Object>> menusOf(Long roleId) {
        List<SysRoleMenu> rels = roleMenuMapper.selectList(new QueryWrapper<SysRoleMenu>().eq("role_id", roleId));
        Set<Long> ids = new HashSet<>();
        rels.forEach(r -> ids.add(r.getMenuId()));
        List<SysMenu> all = menuMapper.selectList(new QueryWrapper<SysMenu>().in("menu_type", "M", "C")
                .eq("visible", 1).orderByAsc("sort_no"));
        List<Map<String, Object>> out = new ArrayList<>();
        for (SysMenu m : all) {
            if (!ids.contains(m.getId())) continue;
            Map<String, Object> one = new LinkedHashMap<>();
            one.put("id", m.getId());
            one.put("parentId", m.getParentId());
            one.put("name", m.getMenuName());
            one.put("path", m.getPath());
            one.put("icon", m.getIcon());
            one.put("type", m.getMenuType());
            out.add(one);
        }
        return out;
    }

    @GetMapping("/me")
    public R<Map<String, Object>> me() {
        Long uid = UserContext.userId();
        if (uid == null) throw new BizException(401, "登录已过期");
        SysUser user = userMapper.selectById(uid);
        SysRole role = roleMapper.selectById(user.getRoleId());
        Map<String, Object> info = new HashMap<>();
        info.put("id", user.getId());
        info.put("username", user.getUsername());
        info.put("realName", user.getRealName());
        info.put("avatar", user.getAvatar());
        info.put("phone", user.getPhone());
        info.put("email", user.getEmail());
        info.put("roleCode", role.getRoleCode());
        info.put("roleName", role.getRoleName());
        info.put("dataScope", role.getDataScope());
        info.put("orgId", user.getOrgId());
        AlumniProfile p = profileMapper.selectOne(new QueryWrapper<AlumniProfile>().eq("user_id", uid).last("limit 1"));
        info.put("alumniNo", p == null ? "" : p.getAlumniNo());
        info.put("menus", menusOf(user.getRoleId()));
        return R.ok(info);
    }

    @PostMapping("/logout")
    public R<Void> logout() {
        return R.ok();
    }
}
