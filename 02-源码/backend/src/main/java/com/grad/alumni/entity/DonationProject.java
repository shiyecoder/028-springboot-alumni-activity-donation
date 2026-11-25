package com.grad.alumni.entity;

import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;

/** donation_project 实体（字段与数据库列一一对应） */
@TableName("donation_project")
public class DonationProject {

    @TableId
    /** id */
    private Long id;

    /** project_no */
    private String projectNo;

    /** project_name */
    private String projectName;

    /** initiator */
    private String initiator;

    /** purpose */
    private String purpose;

    /** target_amount */
    private BigDecimal targetAmount;

    /** raised_amount */
    private BigDecimal raisedAmount;

    /** spent_amount */
    private BigDecimal spentAmount;

    /** beneficiary_count */
    private Integer beneficiaryCount;

    /** start_date */
    private LocalDate startDate;

    /** end_date */
    private LocalDate endDate;

    /** charge_person */
    private String chargePerson;

    /** dept_name */
    private String deptName;

    /** budget_amount */
    private BigDecimal budgetAmount;

    /** public_flag */
    private Integer publicFlag;

    /** public_status */
    private String publicStatus;

    /** status */
    private String status;

    /** cover_image */
    private String coverImage;

    /** public_desc */
    private String publicDesc;

    /** milestone_rate */
    private BigDecimal milestoneRate;

    /** progress_rate */
    private BigDecimal progressRate;

    /** rule_version */
    private String ruleVersion;

    /** create_time */
    private LocalDateTime createTime;

    /** update_time */
    private LocalDateTime updateTime;

    /** deleted */
    private Integer deleted;

    public Long getId() { return id; }
    public void setId(Long v) { this.id = v; }
    public String getProjectNo() { return projectNo; }
    public void setProjectNo(String v) { this.projectNo = v; }
    public String getProjectName() { return projectName; }
    public void setProjectName(String v) { this.projectName = v; }
    public String getInitiator() { return initiator; }
    public void setInitiator(String v) { this.initiator = v; }
    public String getPurpose() { return purpose; }
    public void setPurpose(String v) { this.purpose = v; }
    public BigDecimal getTargetAmount() { return targetAmount; }
    public void setTargetAmount(BigDecimal v) { this.targetAmount = v; }
    public BigDecimal getRaisedAmount() { return raisedAmount; }
    public void setRaisedAmount(BigDecimal v) { this.raisedAmount = v; }
    public BigDecimal getSpentAmount() { return spentAmount; }
    public void setSpentAmount(BigDecimal v) { this.spentAmount = v; }
    public Integer getBeneficiaryCount() { return beneficiaryCount; }
    public void setBeneficiaryCount(Integer v) { this.beneficiaryCount = v; }
    public LocalDate getStartDate() { return startDate; }
    public void setStartDate(LocalDate v) { this.startDate = v; }
    public LocalDate getEndDate() { return endDate; }
    public void setEndDate(LocalDate v) { this.endDate = v; }
    public String getChargePerson() { return chargePerson; }
    public void setChargePerson(String v) { this.chargePerson = v; }
    public String getDeptName() { return deptName; }
    public void setDeptName(String v) { this.deptName = v; }
    public BigDecimal getBudgetAmount() { return budgetAmount; }
    public void setBudgetAmount(BigDecimal v) { this.budgetAmount = v; }
    public Integer getPublicFlag() { return publicFlag; }
    public void setPublicFlag(Integer v) { this.publicFlag = v; }
    public String getPublicStatus() { return publicStatus; }
    public void setPublicStatus(String v) { this.publicStatus = v; }
    public String getStatus() { return status; }
    public void setStatus(String v) { this.status = v; }
    public String getCoverImage() { return coverImage; }
    public void setCoverImage(String v) { this.coverImage = v; }
    public String getPublicDesc() { return publicDesc; }
    public void setPublicDesc(String v) { this.publicDesc = v; }
    public BigDecimal getMilestoneRate() { return milestoneRate; }
    public void setMilestoneRate(BigDecimal v) { this.milestoneRate = v; }
    public BigDecimal getProgressRate() { return progressRate; }
    public void setProgressRate(BigDecimal v) { this.progressRate = v; }
    public String getRuleVersion() { return ruleVersion; }
    public void setRuleVersion(String v) { this.ruleVersion = v; }
    public LocalDateTime getCreateTime() { return createTime; }
    public void setCreateTime(LocalDateTime v) { this.createTime = v; }
    public LocalDateTime getUpdateTime() { return updateTime; }
    public void setUpdateTime(LocalDateTime v) { this.updateTime = v; }
    public Integer getDeleted() { return deleted; }
    public void setDeleted(Integer v) { this.deleted = v; }
}
