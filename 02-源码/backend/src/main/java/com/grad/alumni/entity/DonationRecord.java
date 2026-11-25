package com.grad.alumni.entity;

import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;

/** donation_record 实体（字段与数据库列一一对应） */
@TableName("donation_record")
public class DonationRecord {

    @TableId
    /** id */
    private Long id;

    /** record_no */
    private String recordNo;

    /** project_id */
    private Long projectId;

    /** project_name */
    private String projectName;

    /** donor_name */
    private String donorName;

    /** donor_alumni_id */
    private Long donorAlumniId;

    /** donor_type */
    private String donorType;

    /** amount */
    private BigDecimal amount;

    /** goods_desc */
    private String goodsDesc;

    /** goods_value */
    private BigDecimal goodsValue;

    /** donate_date */
    private LocalDate donateDate;

    /** intention */
    private String intention;

    /** voucher_path */
    private String voucherPath;

    /** anonymous_flag */
    private Integer anonymousFlag;

    /** cert_flag */
    private Integer certFlag;

    /** verify_status */
    private String verifyStatus;

    /** verify_user */
    private String verifyUser;

    /** verify_time */
    private LocalDateTime verifyTime;

    /** verify_remark */
    private String verifyRemark;

    /** fund_usage */
    private String fundUsage;

    /** receipt_status */
    private String receiptStatus;

    /** create_time */
    private LocalDateTime createTime;

    /** update_time */
    private LocalDateTime updateTime;

    public Long getId() { return id; }
    public void setId(Long v) { this.id = v; }
    public String getRecordNo() { return recordNo; }
    public void setRecordNo(String v) { this.recordNo = v; }
    public Long getProjectId() { return projectId; }
    public void setProjectId(Long v) { this.projectId = v; }
    public String getProjectName() { return projectName; }
    public void setProjectName(String v) { this.projectName = v; }
    public String getDonorName() { return donorName; }
    public void setDonorName(String v) { this.donorName = v; }
    public Long getDonorAlumniId() { return donorAlumniId; }
    public void setDonorAlumniId(Long v) { this.donorAlumniId = v; }
    public String getDonorType() { return donorType; }
    public void setDonorType(String v) { this.donorType = v; }
    public BigDecimal getAmount() { return amount; }
    public void setAmount(BigDecimal v) { this.amount = v; }
    public String getGoodsDesc() { return goodsDesc; }
    public void setGoodsDesc(String v) { this.goodsDesc = v; }
    public BigDecimal getGoodsValue() { return goodsValue; }
    public void setGoodsValue(BigDecimal v) { this.goodsValue = v; }
    public LocalDate getDonateDate() { return donateDate; }
    public void setDonateDate(LocalDate v) { this.donateDate = v; }
    public String getIntention() { return intention; }
    public void setIntention(String v) { this.intention = v; }
    public String getVoucherPath() { return voucherPath; }
    public void setVoucherPath(String v) { this.voucherPath = v; }
    public Integer getAnonymousFlag() { return anonymousFlag; }
    public void setAnonymousFlag(Integer v) { this.anonymousFlag = v; }
    public Integer getCertFlag() { return certFlag; }
    public void setCertFlag(Integer v) { this.certFlag = v; }
    public String getVerifyStatus() { return verifyStatus; }
    public void setVerifyStatus(String v) { this.verifyStatus = v; }
    public String getVerifyUser() { return verifyUser; }
    public void setVerifyUser(String v) { this.verifyUser = v; }
    public LocalDateTime getVerifyTime() { return verifyTime; }
    public void setVerifyTime(LocalDateTime v) { this.verifyTime = v; }
    public String getVerifyRemark() { return verifyRemark; }
    public void setVerifyRemark(String v) { this.verifyRemark = v; }
    public String getFundUsage() { return fundUsage; }
    public void setFundUsage(String v) { this.fundUsage = v; }
    public String getReceiptStatus() { return receiptStatus; }
    public void setReceiptStatus(String v) { this.receiptStatus = v; }
    public LocalDateTime getCreateTime() { return createTime; }
    public void setCreateTime(LocalDateTime v) { this.createTime = v; }
    public LocalDateTime getUpdateTime() { return updateTime; }
    public void setUpdateTime(LocalDateTime v) { this.updateTime = v; }
}
