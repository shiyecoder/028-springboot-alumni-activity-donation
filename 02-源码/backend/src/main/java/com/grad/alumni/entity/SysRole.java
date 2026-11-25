package com.grad.alumni.entity;

import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import java.time.LocalDateTime;

/** sys_role 实体（字段与数据库列一一对应） */
@TableName("sys_role")
public class SysRole {

    @TableId
    /** id */
    private Long id;

    /** role_code */
    private String roleCode;

    /** role_name */
    private String roleName;

    /** data_scope */
    private String dataScope;

    /** remark */
    private String remark;

    /** status */
    private Integer status;

    /** create_time */
    private LocalDateTime createTime;

    public Long getId() { return id; }
    public void setId(Long v) { this.id = v; }
    public String getRoleCode() { return roleCode; }
    public void setRoleCode(String v) { this.roleCode = v; }
    public String getRoleName() { return roleName; }
    public void setRoleName(String v) { this.roleName = v; }
    public String getDataScope() { return dataScope; }
    public void setDataScope(String v) { this.dataScope = v; }
    public String getRemark() { return remark; }
    public void setRemark(String v) { this.remark = v; }
    public Integer getStatus() { return status; }
    public void setStatus(Integer v) { this.status = v; }
    public LocalDateTime getCreateTime() { return createTime; }
    public void setCreateTime(LocalDateTime v) { this.createTime = v; }
}
