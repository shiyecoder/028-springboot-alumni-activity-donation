package com.grad.alumni.entity;

import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import java.time.LocalDateTime;

/** activity_signup 实体（字段与数据库列一一对应） */
@TableName("activity_signup")
public class ActivitySignup {

    @TableId
    /** id */
    private Long id;

    /** signup_no */
    private String signupNo;

    /** activity_id */
    private Long activityId;

    /** activity_title */
    private String activityTitle;

    /** alumni_id */
    private Long alumniId;

    /** alumni_name */
    private String alumniName;

    /** companion_count */
    private Integer companionCount;

    /** companion_names */
    private String companionNames;

    /** status */
    private String status;

    /** wait_no */
    private Integer waitNo;

    /** checkin_code */
    private String checkinCode;

    /** checkin_time */
    private LocalDateTime checkinTime;

    /** audit_user */
    private String auditUser;

    /** audit_time */
    private LocalDateTime auditTime;

    /** remark */
    private String remark;

    /** create_time */
    private LocalDateTime createTime;

    /** update_time */
    private LocalDateTime updateTime;

    public Long getId() { return id; }
    public void setId(Long v) { this.id = v; }
    public String getSignupNo() { return signupNo; }
    public void setSignupNo(String v) { this.signupNo = v; }
    public Long getActivityId() { return activityId; }
    public void setActivityId(Long v) { this.activityId = v; }
    public String getActivityTitle() { return activityTitle; }
    public void setActivityTitle(String v) { this.activityTitle = v; }
    public Long getAlumniId() { return alumniId; }
    public void setAlumniId(Long v) { this.alumniId = v; }
    public String getAlumniName() { return alumniName; }
    public void setAlumniName(String v) { this.alumniName = v; }
    public Integer getCompanionCount() { return companionCount; }
    public void setCompanionCount(Integer v) { this.companionCount = v; }
    public String getCompanionNames() { return companionNames; }
    public void setCompanionNames(String v) { this.companionNames = v; }
    public String getStatus() { return status; }
    public void setStatus(String v) { this.status = v; }
    public Integer getWaitNo() { return waitNo; }
    public void setWaitNo(Integer v) { this.waitNo = v; }
    public String getCheckinCode() { return checkinCode; }
    public void setCheckinCode(String v) { this.checkinCode = v; }
    public LocalDateTime getCheckinTime() { return checkinTime; }
    public void setCheckinTime(LocalDateTime v) { this.checkinTime = v; }
    public String getAuditUser() { return auditUser; }
    public void setAuditUser(String v) { this.auditUser = v; }
    public LocalDateTime getAuditTime() { return auditTime; }
    public void setAuditTime(LocalDateTime v) { this.auditTime = v; }
    public String getRemark() { return remark; }
    public void setRemark(String v) { this.remark = v; }
    public LocalDateTime getCreateTime() { return createTime; }
    public void setCreateTime(LocalDateTime v) { this.createTime = v; }
    public LocalDateTime getUpdateTime() { return updateTime; }
    public void setUpdateTime(LocalDateTime v) { this.updateTime = v; }
}
