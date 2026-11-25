package com.grad.alumni.entity;

import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;

/** thank_certificate 实体（字段与数据库列一一对应） */
@TableName("thank_certificate")
public class ThankCertificate {

    @TableId
    /** id */
    private Long id;

    /** cert_no */
    private String certNo;

    /** record_id */
    private Long recordId;

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

    /** amount */
    private BigDecimal amount;

    /** issue_date */
    private LocalDate issueDate;

    /** cert_path */
    private String certPath;

    /** issue_user */
    private String issueUser;

    /** send_status */
    private String sendStatus;

    /** send_time */
    private LocalDateTime sendTime;

    /** send_way */
    private String sendWay;

    /** remark */
    private String remark;

    /** create_time */
    private LocalDateTime createTime;

    public Long getId() { return id; }
    public void setId(Long v) { this.id = v; }
    public String getCertNo() { return certNo; }
    public void setCertNo(String v) { this.certNo = v; }
    public Long getRecordId() { return recordId; }
    public void setRecordId(Long v) { this.recordId = v; }
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
    public BigDecimal getAmount() { return amount; }
    public void setAmount(BigDecimal v) { this.amount = v; }
    public LocalDate getIssueDate() { return issueDate; }
    public void setIssueDate(LocalDate v) { this.issueDate = v; }
    public String getCertPath() { return certPath; }
    public void setCertPath(String v) { this.certPath = v; }
    public String getIssueUser() { return issueUser; }
    public void setIssueUser(String v) { this.issueUser = v; }
    public String getSendStatus() { return sendStatus; }
    public void setSendStatus(String v) { this.sendStatus = v; }
    public LocalDateTime getSendTime() { return sendTime; }
    public void setSendTime(LocalDateTime v) { this.sendTime = v; }
    public String getSendWay() { return sendWay; }
    public void setSendWay(String v) { this.sendWay = v; }
    public String getRemark() { return remark; }
    public void setRemark(String v) { this.remark = v; }
    public LocalDateTime getCreateTime() { return createTime; }
    public void setCreateTime(LocalDateTime v) { this.createTime = v; }
}
