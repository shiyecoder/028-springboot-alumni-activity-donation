package com.grad.alumni.entity;

import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import java.time.LocalDateTime;

/** organization_member 实体（字段与数据库列一一对应） */
@TableName("organization_member")
public class OrganizationMember {

    @TableId
    /** id */
    private Long id;

    /** org_id */
    private Long orgId;

    /** alumni_id */
    private Long alumniId;

    /** alumni_name */
    private String alumniName;

    /** member_role */
    private String memberRole;

    /** join_status */
    private String joinStatus;

    /** apply_reason */
    private String applyReason;

    /** audit_user */
    private String auditUser;

    /** audit_time */
    private LocalDateTime auditTime;

    /** create_time */
    private LocalDateTime createTime;

    public Long getId() { return id; }
    public void setId(Long v) { this.id = v; }
    public Long getOrgId() { return orgId; }
    public void setOrgId(Long v) { this.orgId = v; }
    public Long getAlumniId() { return alumniId; }
    public void setAlumniId(Long v) { this.alumniId = v; }
    public String getAlumniName() { return alumniName; }
    public void setAlumniName(String v) { this.alumniName = v; }
    public String getMemberRole() { return memberRole; }
    public void setMemberRole(String v) { this.memberRole = v; }
    public String getJoinStatus() { return joinStatus; }
    public void setJoinStatus(String v) { this.joinStatus = v; }
    public String getApplyReason() { return applyReason; }
    public void setApplyReason(String v) { this.applyReason = v; }
    public String getAuditUser() { return auditUser; }
    public void setAuditUser(String v) { this.auditUser = v; }
    public LocalDateTime getAuditTime() { return auditTime; }
    public void setAuditTime(LocalDateTime v) { this.auditTime = v; }
    public LocalDateTime getCreateTime() { return createTime; }
    public void setCreateTime(LocalDateTime v) { this.createTime = v; }
}
