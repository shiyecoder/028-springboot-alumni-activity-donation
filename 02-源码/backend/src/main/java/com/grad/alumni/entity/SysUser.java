package com.grad.alumni.entity;

import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import java.time.LocalDateTime;

/** sys_user 实体（字段与数据库列一一对应） */
@TableName("sys_user")
public class SysUser {

    @TableId
    /** id */
    private Long id;

    /** username */
    private String username;

    /** password */
    private String password;

    /** real_name */
    private String realName;

    /** phone */
    private String phone;

    /** email */
    private String email;

    /** avatar */
    private String avatar;

    /** org_id */
    private Long orgId;

    /** role_id */
    private Long roleId;

    /** status */
    private Integer status;

    /** login_fail_count */
    private Integer loginFailCount;

    /** lock_until */
    private LocalDateTime lockUntil;

    /** last_login_time */
    private LocalDateTime lastLoginTime;

    /** create_time */
    private LocalDateTime createTime;

    /** update_time */
    private LocalDateTime updateTime;

    /** deleted */
    private Integer deleted;

    public Long getId() { return id; }
    public void setId(Long v) { this.id = v; }
    public String getUsername() { return username; }
    public void setUsername(String v) { this.username = v; }
    public String getPassword() { return password; }
    public void setPassword(String v) { this.password = v; }
    public String getRealName() { return realName; }
    public void setRealName(String v) { this.realName = v; }
    public String getPhone() { return phone; }
    public void setPhone(String v) { this.phone = v; }
    public String getEmail() { return email; }
    public void setEmail(String v) { this.email = v; }
    public String getAvatar() { return avatar; }
    public void setAvatar(String v) { this.avatar = v; }
    public Long getOrgId() { return orgId; }
    public void setOrgId(Long v) { this.orgId = v; }
    public Long getRoleId() { return roleId; }
    public void setRoleId(Long v) { this.roleId = v; }
    public Integer getStatus() { return status; }
    public void setStatus(Integer v) { this.status = v; }
    public Integer getLoginFailCount() { return loginFailCount; }
    public void setLoginFailCount(Integer v) { this.loginFailCount = v; }
    public LocalDateTime getLockUntil() { return lockUntil; }
    public void setLockUntil(LocalDateTime v) { this.lockUntil = v; }
    public LocalDateTime getLastLoginTime() { return lastLoginTime; }
    public void setLastLoginTime(LocalDateTime v) { this.lastLoginTime = v; }
    public LocalDateTime getCreateTime() { return createTime; }
    public void setCreateTime(LocalDateTime v) { this.createTime = v; }
    public LocalDateTime getUpdateTime() { return updateTime; }
    public void setUpdateTime(LocalDateTime v) { this.updateTime = v; }
    public Integer getDeleted() { return deleted; }
    public void setDeleted(Integer v) { this.deleted = v; }
}
