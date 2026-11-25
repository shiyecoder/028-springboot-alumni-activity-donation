package com.grad.alumni.entity;

import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import java.math.BigDecimal;
import java.time.LocalDateTime;

/** project_progress 实体（字段与数据库列一一对应） */
@TableName("project_progress")
public class ProjectProgress {

    @TableId
    /** id */
    private Long id;

    /** project_id */
    private Long projectId;

    /** project_name */
    private String projectName;

    /** stage_name */
    private String stageName;

    /** progress_rate */
    private BigDecimal progressRate;

    /** content */
    private String content;

    /** fund_summary */
    private String fundSummary;

    /** photo_path */
    private String photoPath;

    /** publish_user */
    private String publishUser;

    /** publish_time */
    private LocalDateTime publishTime;

    /** audit_status */
    private String auditStatus;

    /** audit_user */
    private String auditUser;

    /** audit_time */
    private LocalDateTime auditTime;

    /** create_time */
    private LocalDateTime createTime;

    public Long getId() { return id; }
    public void setId(Long v) { this.id = v; }
    public Long getProjectId() { return projectId; }
    public void setProjectId(Long v) { this.projectId = v; }
    public String getProjectName() { return projectName; }
    public void setProjectName(String v) { this.projectName = v; }
    public String getStageName() { return stageName; }
    public void setStageName(String v) { this.stageName = v; }
    public BigDecimal getProgressRate() { return progressRate; }
    public void setProgressRate(BigDecimal v) { this.progressRate = v; }
    public String getContent() { return content; }
    public void setContent(String v) { this.content = v; }
    public String getFundSummary() { return fundSummary; }
    public void setFundSummary(String v) { this.fundSummary = v; }
    public String getPhotoPath() { return photoPath; }
    public void setPhotoPath(String v) { this.photoPath = v; }
    public String getPublishUser() { return publishUser; }
    public void setPublishUser(String v) { this.publishUser = v; }
    public LocalDateTime getPublishTime() { return publishTime; }
    public void setPublishTime(LocalDateTime v) { this.publishTime = v; }
    public String getAuditStatus() { return auditStatus; }
    public void setAuditStatus(String v) { this.auditStatus = v; }
    public String getAuditUser() { return auditUser; }
    public void setAuditUser(String v) { this.auditUser = v; }
    public LocalDateTime getAuditTime() { return auditTime; }
    public void setAuditTime(LocalDateTime v) { this.auditTime = v; }
    public LocalDateTime getCreateTime() { return createTime; }
    public void setCreateTime(LocalDateTime v) { this.createTime = v; }
}
