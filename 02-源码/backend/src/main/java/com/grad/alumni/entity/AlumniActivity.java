package com.grad.alumni.entity;

import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import java.time.LocalDateTime;

/** alumni_activity 实体（字段与数据库列一一对应） */
@TableName("alumni_activity")
public class AlumniActivity {

    @TableId
    /** id */
    private Long id;

    /** activity_no */
    private String activityNo;

    /** title */
    private String title;

    /** activity_type */
    private String activityType;

    /** org_id */
    private Long orgId;

    /** org_name */
    private String orgName;

    /** college */
    private String college;

    /** location */
    private String location;

    /** start_time */
    private LocalDateTime startTime;

    /** end_time */
    private LocalDateTime endTime;

    /** capacity */
    private Integer capacity;

    /** signup_count */
    private Integer signupCount;

    /** wait_count */
    private Integer waitCount;

    /** checkin_count */
    private Integer checkinCount;

    /** poster */
    private String poster;

    /** agenda */
    private String agenda;

    /** signup_form */
    private String signupForm;

    /** audit_mode */
    private String auditMode;

    /** status */
    private String status;

    /** charge_person */
    private String chargePerson;

    /** reject_reason */
    private String rejectReason;

    /** create_time */
    private LocalDateTime createTime;

    /** update_time */
    private LocalDateTime updateTime;

    /** deleted */
    private Integer deleted;

    public Long getId() { return id; }
    public void setId(Long v) { this.id = v; }
    public String getActivityNo() { return activityNo; }
    public void setActivityNo(String v) { this.activityNo = v; }
    public String getTitle() { return title; }
    public void setTitle(String v) { this.title = v; }
    public String getActivityType() { return activityType; }
    public void setActivityType(String v) { this.activityType = v; }
    public Long getOrgId() { return orgId; }
    public void setOrgId(Long v) { this.orgId = v; }
    public String getOrgName() { return orgName; }
    public void setOrgName(String v) { this.orgName = v; }
    public String getCollege() { return college; }
    public void setCollege(String v) { this.college = v; }
    public String getLocation() { return location; }
    public void setLocation(String v) { this.location = v; }
    public LocalDateTime getStartTime() { return startTime; }
    public void setStartTime(LocalDateTime v) { this.startTime = v; }
    public LocalDateTime getEndTime() { return endTime; }
    public void setEndTime(LocalDateTime v) { this.endTime = v; }
    public Integer getCapacity() { return capacity; }
    public void setCapacity(Integer v) { this.capacity = v; }
    public Integer getSignupCount() { return signupCount; }
    public void setSignupCount(Integer v) { this.signupCount = v; }
    public Integer getWaitCount() { return waitCount; }
    public void setWaitCount(Integer v) { this.waitCount = v; }
    public Integer getCheckinCount() { return checkinCount; }
    public void setCheckinCount(Integer v) { this.checkinCount = v; }
    public String getPoster() { return poster; }
    public void setPoster(String v) { this.poster = v; }
    public String getAgenda() { return agenda; }
    public void setAgenda(String v) { this.agenda = v; }
    public String getSignupForm() { return signupForm; }
    public void setSignupForm(String v) { this.signupForm = v; }
    public String getAuditMode() { return auditMode; }
    public void setAuditMode(String v) { this.auditMode = v; }
    public String getStatus() { return status; }
    public void setStatus(String v) { this.status = v; }
    public String getChargePerson() { return chargePerson; }
    public void setChargePerson(String v) { this.chargePerson = v; }
    public String getRejectReason() { return rejectReason; }
    public void setRejectReason(String v) { this.rejectReason = v; }
    public LocalDateTime getCreateTime() { return createTime; }
    public void setCreateTime(LocalDateTime v) { this.createTime = v; }
    public LocalDateTime getUpdateTime() { return updateTime; }
    public void setUpdateTime(LocalDateTime v) { this.updateTime = v; }
    public Integer getDeleted() { return deleted; }
    public void setDeleted(Integer v) { this.deleted = v; }
}
