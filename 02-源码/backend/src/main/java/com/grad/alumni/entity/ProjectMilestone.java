package com.grad.alumni.entity;

import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import java.time.LocalDate;
import java.time.LocalDateTime;

/** project_milestone 实体（字段与数据库列一一对应） */
@TableName("project_milestone")
public class ProjectMilestone {

    @TableId
    /** id */
    private Long id;

    /** project_id */
    private Long projectId;

    /** milestone_name */
    private String milestoneName;

    /** seq_no */
    private Integer seqNo;

    /** plan_date */
    private LocalDate planDate;

    /** finish_date */
    private LocalDate finishDate;

    /** weight */
    private Integer weight;

    /** status */
    private String status;

    /** deliverable */
    private String deliverable;

    /** create_time */
    private LocalDateTime createTime;

    public Long getId() { return id; }
    public void setId(Long v) { this.id = v; }
    public Long getProjectId() { return projectId; }
    public void setProjectId(Long v) { this.projectId = v; }
    public String getMilestoneName() { return milestoneName; }
    public void setMilestoneName(String v) { this.milestoneName = v; }
    public Integer getSeqNo() { return seqNo; }
    public void setSeqNo(Integer v) { this.seqNo = v; }
    public LocalDate getPlanDate() { return planDate; }
    public void setPlanDate(LocalDate v) { this.planDate = v; }
    public LocalDate getFinishDate() { return finishDate; }
    public void setFinishDate(LocalDate v) { this.finishDate = v; }
    public Integer getWeight() { return weight; }
    public void setWeight(Integer v) { this.weight = v; }
    public String getStatus() { return status; }
    public void setStatus(String v) { this.status = v; }
    public String getDeliverable() { return deliverable; }
    public void setDeliverable(String v) { this.deliverable = v; }
    public LocalDateTime getCreateTime() { return createTime; }
    public void setCreateTime(LocalDateTime v) { this.createTime = v; }
}
