package com.grad.alumni.entity;

import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import java.time.LocalDateTime;

/** alumni_project_rule 实体（字段与数据库列一一对应） */
@TableName("alumni_project_rule")
public class AlumniProjectRule {

    @TableId
    /** id */
    private Long id;

    /** rule_name */
    private String ruleName;

    /** version */
    private String version;

    /** target_weight */
    private Integer targetWeight;

    /** amount_weight */
    private Integer amountWeight;

    /** milestone_weight */
    private Integer milestoneWeight;

    /** voucher_weight */
    private Integer voucherWeight;

    /** beneficiary_weight */
    private Integer beneficiaryWeight;

    /** audit_weight */
    private Integer auditWeight;

    /** pass_score */
    private Integer passScore;

    /** good_score */
    private Integer goodScore;

    /** status */
    private String status;

    /** effect_time */
    private LocalDateTime effectTime;

    /** create_user */
    private String createUser;

    /** create_time */
    private LocalDateTime createTime;

    public Long getId() { return id; }
    public void setId(Long v) { this.id = v; }
    public String getRuleName() { return ruleName; }
    public void setRuleName(String v) { this.ruleName = v; }
    public String getVersion() { return version; }
    public void setVersion(String v) { this.version = v; }
    public Integer getTargetWeight() { return targetWeight; }
    public void setTargetWeight(Integer v) { this.targetWeight = v; }
    public Integer getAmountWeight() { return amountWeight; }
    public void setAmountWeight(Integer v) { this.amountWeight = v; }
    public Integer getMilestoneWeight() { return milestoneWeight; }
    public void setMilestoneWeight(Integer v) { this.milestoneWeight = v; }
    public Integer getVoucherWeight() { return voucherWeight; }
    public void setVoucherWeight(Integer v) { this.voucherWeight = v; }
    public Integer getBeneficiaryWeight() { return beneficiaryWeight; }
    public void setBeneficiaryWeight(Integer v) { this.beneficiaryWeight = v; }
    public Integer getAuditWeight() { return auditWeight; }
    public void setAuditWeight(Integer v) { this.auditWeight = v; }
    public Integer getPassScore() { return passScore; }
    public void setPassScore(Integer v) { this.passScore = v; }
    public Integer getGoodScore() { return goodScore; }
    public void setGoodScore(Integer v) { this.goodScore = v; }
    public String getStatus() { return status; }
    public void setStatus(String v) { this.status = v; }
    public LocalDateTime getEffectTime() { return effectTime; }
    public void setEffectTime(LocalDateTime v) { this.effectTime = v; }
    public String getCreateUser() { return createUser; }
    public void setCreateUser(String v) { this.createUser = v; }
    public LocalDateTime getCreateTime() { return createTime; }
    public void setCreateTime(LocalDateTime v) { this.createTime = v; }
}
