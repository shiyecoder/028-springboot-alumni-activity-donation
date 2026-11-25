package com.grad.alumni.entity;

import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import java.time.LocalDateTime;

/** alumni_change_request 实体（字段与数据库列一一对应） */
@TableName("alumni_change_request")
public class AlumniChangeRequest {

    @TableId
    /** id */
    private Long id;

    /** alumni_id */
    private Long alumniId;

    /** alumni_name */
    private String alumniName;

    /** change_type */
    private String changeType;

    /** field_name */
    private String fieldName;

    /** old_value */
    private String oldValue;

    /** new_value */
    private String newValue;

    /** reason */
    private String reason;

    /** audit_status */
    private String auditStatus;

    /** audit_user */
    private String auditUser;

    /** audit_time */
    private LocalDateTime auditTime;

    /** audit_remark */
    private String auditRemark;

    /** create_time */
    private LocalDateTime createTime;

    public Long getId() { return id; }
    public void setId(Long v) { this.id = v; }
    public Long getAlumniId() { return alumniId; }
    public void setAlumniId(Long v) { this.alumniId = v; }
    public String getAlumniName() { return alumniName; }
    public void setAlumniName(String v) { this.alumniName = v; }
    public String getChangeType() { return changeType; }
    public void setChangeType(String v) { this.changeType = v; }
    public String getFieldName() { return fieldName; }
    public void setFieldName(String v) { this.fieldName = v; }
    public String getOldValue() { return oldValue; }
    public void setOldValue(String v) { this.oldValue = v; }
    public String getNewValue() { return newValue; }
    public void setNewValue(String v) { this.newValue = v; }
    public String getReason() { return reason; }
    public void setReason(String v) { this.reason = v; }
    public String getAuditStatus() { return auditStatus; }
    public void setAuditStatus(String v) { this.auditStatus = v; }
    public String getAuditUser() { return auditUser; }
    public void setAuditUser(String v) { this.auditUser = v; }
    public LocalDateTime getAuditTime() { return auditTime; }
    public void setAuditTime(LocalDateTime v) { this.auditTime = v; }
    public String getAuditRemark() { return auditRemark; }
    public void setAuditRemark(String v) { this.auditRemark = v; }
    public LocalDateTime getCreateTime() { return createTime; }
    public void setCreateTime(LocalDateTime v) { this.createTime = v; }
}
