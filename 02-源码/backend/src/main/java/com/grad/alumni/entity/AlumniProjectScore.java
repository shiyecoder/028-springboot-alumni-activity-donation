package com.grad.alumni.entity;

import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import java.math.BigDecimal;
import java.time.LocalDateTime;

/** alumni_project_score 实体（字段与数据库列一一对应） */
@TableName("alumni_project_score")
public class AlumniProjectScore {

    @TableId
    /** id */
    private Long id;

    /** project_id */
    private Long projectId;

    /** project_name */
    private String projectName;

    /** rule_id */
    private Long ruleId;

    /** rule_version */
    private String ruleVersion;

    /** input_snapshot */
    private String inputSnapshot;

    /** target_score */
    private BigDecimal targetScore;

    /** amount_score */
    private BigDecimal amountScore;

    /** milestone_score */
    private BigDecimal milestoneScore;

    /** voucher_score */
    private BigDecimal voucherScore;

    /** beneficiary_score */
    private BigDecimal beneficiaryScore;

    /** audit_score */
    private BigDecimal auditScore;

    /** total_score */
    private BigDecimal totalScore;

    /** result_level */
    private String resultLevel;

    /** explanation */
    private String explanation;

    /** unmet_conditions */
    private String unmetConditions;

    /** improve_items */
    private String improveItems;

    /** calc_time */
    private LocalDateTime calcTime;

    /** calc_user */
    private String calcUser;

    /** manual_level */
    private String manualLevel;

    /** manual_reason */
    private String manualReason;

    /** manual_user */
    private String manualUser;

    /** manual_time */
    private LocalDateTime manualTime;

    /** create_time */
    private LocalDateTime createTime;

    public Long getId() { return id; }
    public void setId(Long v) { this.id = v; }
    public Long getProjectId() { return projectId; }
    public void setProjectId(Long v) { this.projectId = v; }
    public String getProjectName() { return projectName; }
    public void setProjectName(String v) { this.projectName = v; }
    public Long getRuleId() { return ruleId; }
    public void setRuleId(Long v) { this.ruleId = v; }
    public String getRuleVersion() { return ruleVersion; }
    public void setRuleVersion(String v) { this.ruleVersion = v; }
    public String getInputSnapshot() { return inputSnapshot; }
    public void setInputSnapshot(String v) { this.inputSnapshot = v; }
    public BigDecimal getTargetScore() { return targetScore; }
    public void setTargetScore(BigDecimal v) { this.targetScore = v; }
    public BigDecimal getAmountScore() { return amountScore; }
    public void setAmountScore(BigDecimal v) { this.amountScore = v; }
    public BigDecimal getMilestoneScore() { return milestoneScore; }
    public void setMilestoneScore(BigDecimal v) { this.milestoneScore = v; }
    public BigDecimal getVoucherScore() { return voucherScore; }
    public void setVoucherScore(BigDecimal v) { this.voucherScore = v; }
    public BigDecimal getBeneficiaryScore() { return beneficiaryScore; }
    public void setBeneficiaryScore(BigDecimal v) { this.beneficiaryScore = v; }
    public BigDecimal getAuditScore() { return auditScore; }
    public void setAuditScore(BigDecimal v) { this.auditScore = v; }
    public BigDecimal getTotalScore() { return totalScore; }
    public void setTotalScore(BigDecimal v) { this.totalScore = v; }
    public String getResultLevel() { return resultLevel; }
    public void setResultLevel(String v) { this.resultLevel = v; }
    public String getExplanation() { return explanation; }
    public void setExplanation(String v) { this.explanation = v; }
    public String getUnmetConditions() { return unmetConditions; }
    public void setUnmetConditions(String v) { this.unmetConditions = v; }
    public String getImproveItems() { return improveItems; }
    public void setImproveItems(String v) { this.improveItems = v; }
    public LocalDateTime getCalcTime() { return calcTime; }
    public void setCalcTime(LocalDateTime v) { this.calcTime = v; }
    public String getCalcUser() { return calcUser; }
    public void setCalcUser(String v) { this.calcUser = v; }
    public String getManualLevel() { return manualLevel; }
    public void setManualLevel(String v) { this.manualLevel = v; }
    public String getManualReason() { return manualReason; }
    public void setManualReason(String v) { this.manualReason = v; }
    public String getManualUser() { return manualUser; }
    public void setManualUser(String v) { this.manualUser = v; }
    public LocalDateTime getManualTime() { return manualTime; }
    public void setManualTime(LocalDateTime v) { this.manualTime = v; }
    public LocalDateTime getCreateTime() { return createTime; }
    public void setCreateTime(LocalDateTime v) { this.createTime = v; }
}
