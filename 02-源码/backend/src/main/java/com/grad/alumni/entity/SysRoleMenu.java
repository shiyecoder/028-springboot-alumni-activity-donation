package com.grad.alumni.entity;

import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;

/** sys_role_menu 实体（字段与数据库列一一对应） */
@TableName("sys_role_menu")
public class SysRoleMenu {

    @TableId
    /** id */
    private Long id;

    /** role_id */
    private Long roleId;

    /** menu_id */
    private Long menuId;

    public Long getId() { return id; }
    public void setId(Long v) { this.id = v; }
    public Long getRoleId() { return roleId; }
    public void setRoleId(Long v) { this.roleId = v; }
    public Long getMenuId() { return menuId; }
    public void setMenuId(Long v) { this.menuId = v; }
}
