package com.grad.alumni.entity;

import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import java.time.LocalDateTime;

/** sys_menu 实体（字段与数据库列一一对应） */
@TableName("sys_menu")
public class SysMenu {

    @TableId
    /** id */
    private Long id;

    /** parent_id */
    private Long parentId;

    /** menu_name */
    private String menuName;

    /** menu_type */
    private String menuType;

    /** path */
    private String path;

    /** perm */
    private String perm;

    /** icon */
    private String icon;

    /** sort_no */
    private Integer sortNo;

    /** visible */
    private Integer visible;

    /** create_time */
    private LocalDateTime createTime;

    public Long getId() { return id; }
    public void setId(Long v) { this.id = v; }
    public Long getParentId() { return parentId; }
    public void setParentId(Long v) { this.parentId = v; }
    public String getMenuName() { return menuName; }
    public void setMenuName(String v) { this.menuName = v; }
    public String getMenuType() { return menuType; }
    public void setMenuType(String v) { this.menuType = v; }
    public String getPath() { return path; }
    public void setPath(String v) { this.path = v; }
    public String getPerm() { return perm; }
    public void setPerm(String v) { this.perm = v; }
    public String getIcon() { return icon; }
    public void setIcon(String v) { this.icon = v; }
    public Integer getSortNo() { return sortNo; }
    public void setSortNo(Integer v) { this.sortNo = v; }
    public Integer getVisible() { return visible; }
    public void setVisible(Integer v) { this.visible = v; }
    public LocalDateTime getCreateTime() { return createTime; }
    public void setCreateTime(LocalDateTime v) { this.createTime = v; }
}
