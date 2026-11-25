package com.grad.alumni.entity;

import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import java.math.BigDecimal;
import java.time.LocalDateTime;

/** activity_archive 实体（字段与数据库列一一对应） */
@TableName("activity_archive")
public class ActivityArchive {

    @TableId
    /** id */
    private Long id;

    /** activity_id */
    private Long activityId;

    /** activity_title */
    private String activityTitle;

    /** plan_count */
    private Integer planCount;

    /** actual_count */
    private Integer actualCount;

    /** photo_path */
    private String photoPath;

    /** news_title */
    private String newsTitle;

    /** news_content */
    private String newsContent;

    /** cost_summary */
    private String costSummary;

    /** cost_total */
    private BigDecimal costTotal;

    /** feedback_summary */
    private String feedbackSummary;

    /** summary */
    private String summary;

    /** archive_user */
    private String archiveUser;

    /** archive_time */
    private LocalDateTime archiveTime;

    /** create_time */
    private LocalDateTime createTime;

    public Long getId() { return id; }
    public void setId(Long v) { this.id = v; }
    public Long getActivityId() { return activityId; }
    public void setActivityId(Long v) { this.activityId = v; }
    public String getActivityTitle() { return activityTitle; }
    public void setActivityTitle(String v) { this.activityTitle = v; }
    public Integer getPlanCount() { return planCount; }
    public void setPlanCount(Integer v) { this.planCount = v; }
    public Integer getActualCount() { return actualCount; }
    public void setActualCount(Integer v) { this.actualCount = v; }
    public String getPhotoPath() { return photoPath; }
    public void setPhotoPath(String v) { this.photoPath = v; }
    public String getNewsTitle() { return newsTitle; }
    public void setNewsTitle(String v) { this.newsTitle = v; }
    public String getNewsContent() { return newsContent; }
    public void setNewsContent(String v) { this.newsContent = v; }
    public String getCostSummary() { return costSummary; }
    public void setCostSummary(String v) { this.costSummary = v; }
    public BigDecimal getCostTotal() { return costTotal; }
    public void setCostTotal(BigDecimal v) { this.costTotal = v; }
    public String getFeedbackSummary() { return feedbackSummary; }
    public void setFeedbackSummary(String v) { this.feedbackSummary = v; }
    public String getSummary() { return summary; }
    public void setSummary(String v) { this.summary = v; }
    public String getArchiveUser() { return archiveUser; }
    public void setArchiveUser(String v) { this.archiveUser = v; }
    public LocalDateTime getArchiveTime() { return archiveTime; }
    public void setArchiveTime(LocalDateTime v) { this.archiveTime = v; }
    public LocalDateTime getCreateTime() { return createTime; }
    public void setCreateTime(LocalDateTime v) { this.createTime = v; }
}
