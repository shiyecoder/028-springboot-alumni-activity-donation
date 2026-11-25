package com.grad.alumni.controller;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.grad.alumni.common.BizException;
import com.grad.alumni.common.R;
import com.grad.alumni.entity.SysRole;
import com.grad.alumni.entity.SysRoleMenu;
import com.grad.alumni.mapper.SysRoleMapper;
import com.grad.alumni.mapper.SysRoleMenuMapper;
import org.springframework.web.bind.annotation.*;

import java.util.*;

/** 角色管理：为角色分配菜单，菜单与数据范围分别控制 */
@RestController
@RequestMapping("/api/role")
public class RoleController extends BaseController<SysRole> {

    private final SysRoleMapper mapper;
    private final SysRoleMenuMapper roleMenuMapper;

    public RoleController(SysRoleMapper mapper, SysRoleMenuMapper roleMenuMapper) {
        this.mapper = mapper;
        this.roleMenuMapper = roleMenuMapper;
    }

    @Override
    protected BaseMapper<SysRole> mapper() { return mapper; }

    @Override
    protected String kwColumn() { return "role_name"; }

    @GetMapping("/list")
    public R<List<SysRole>> list() {
        return R.ok(mapper.selectList(new QueryWrapper<SysRole>().orderByAsc("id")));
    }

    @GetMapping("/{id}/menus")
    public R<List<Long>> menus(@PathVariable Long id) {
        List<Long> ids = new ArrayList<>();
        roleMenuMapper.selectList(new QueryWrapper<SysRoleMenu>().eq("role_id", id))
                .forEach(r -> ids.add(r.getMenuId()));
        return R.ok(ids);
    }

    /** 重新分配菜单：先清空再写入，任一失败整批回滚 */
    @PutMapping("/{id}/menus")
    public R<Void> assign(@PathVariable Long id, @RequestBody List<Long> menuIds) {
        SysRole role = mapper.selectById(id);
        if (role == null) throw new BizException("角色不存在");
        if ("ADMIN".equals(role.getRoleCode()) && (menuIds == null || menuIds.isEmpty())) {
            throw new BizException("管理员角色至少保留一个菜单");
        }
        roleMenuMapper.delete(new QueryWrapper<SysRoleMenu>().eq("role_id", id));
        if (menuIds != null) {
            for (Long mid : menuIds) {
                SysRoleMenu rm = new SysRoleMenu();
                rm.setRoleId(id);
                rm.setMenuId(mid);
                roleMenuMapper.insert(rm);
            }
        }
        return R.ok();
    }
}
