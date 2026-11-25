package com.grad.alumni.entity;

import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import java.time.LocalDateTime;

/** activity_checkin 实体（字段与数据库列一一对应） */
@TableName("activity_checkin")
public class ActivityCheckin {

    @TableId
    /** id */
    private Long id;

    /** activity_id */
    private Long activityId;

    /** signup_id */
    private Long signupId;

    /** alumni_id */
    private Long alumniId;

    /** alumni_name */
    private String alumniName;

    /** checkin_code */
    private String checkinCode;

    /** checkin_time */
    private LocalDateTime checkinTime;

    /** checkin_by */
    private String checkinBy;

    /** checkin_type */
    private String checkinType;

    /** remark */
    private String remark;

    /** create_time */
    private LocalDateTime createTime;

    public Long getId() { return id; }
    public void setId(Long v) { this.id = v; }
    public Long getActivityId() { return activityId; }
    public void setActivityId(Long v) { this.activityId = v; }
    public Long getSignupId() { return signupId; }
    public void setSignupId(Long v) { this.signupId = v; }
    public Long getAlumniId() { return alumniId; }
    public void setAlumniId(Long v) { this.alumniId = v; }
    public String getAlumniName() { return alumniName; }
    public void setAlumniName(String v) { this.alumniName = v; }
    public String getCheckinCode() { return checkinCode; }
    public void setCheckinCode(String v) { this.checkinCode = v; }
    public LocalDateTime getCheckinTime() { return checkinTime; }
    public void setCheckinTime(LocalDateTime v) { this.checkinTime = v; }
    public String getCheckinBy() { return checkinBy; }
    public void setCheckinBy(String v) { this.checkinBy = v; }
    public String getCheckinType() { return checkinType; }
    public void setCheckinType(String v) { this.checkinType = v; }
    public String getRemark() { return remark; }
    public void setRemark(String v) { this.remark = v; }
    public LocalDateTime getCreateTime() { return createTime; }
    public void setCreateTime(LocalDateTime v) { this.createTime = v; }
}
