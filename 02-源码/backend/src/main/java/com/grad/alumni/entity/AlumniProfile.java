package com.grad.alumni.entity;

import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import java.time.LocalDate;
import java.time.LocalDateTime;

/** alumni_profile 实体（字段与数据库列一一对应） */
@TableName("alumni_profile")
public class AlumniProfile {

    @TableId
    /** id */
    private Long id;

    /** alumni_no */
    private String alumniNo;

    /** student_no */
    private String studentNo;

    /** real_name */
    private String realName;

    /** gender */
    private String gender;

    /** birth_date */
    private LocalDate birthDate;

    /** enroll_year */
    private Integer enrollYear;

    /** graduate_year */
    private Integer graduateYear;

    /** college */
    private String college;

    /** major */
    private String major;

    /** class_name */
    private String className;

    /** phone */
    private String phone;

    /** email */
    private String email;

    /** work_unit */
    private String workUnit;

    /** work_title */
    private String workTitle;

    /** region_name */
    private String regionName;

    /** industry */
    private String industry;

    /** avatar */
    private String avatar;

    /** cert_status */
    private String certStatus;

    /** cert_material */
    private String certMaterial;

    /** cert_remark */
    private String certRemark;

    /** audit_user */
    private String auditUser;

    /** audit_time */
    private LocalDateTime auditTime;

    /** privacy_level */
    private String privacyLevel;

    /** show_phone */
    private Integer showPhone;

    /** show_email */
    private Integer showEmail;

    /** show_unit */
    private Integer showUnit;

    /** show_region */
    private Integer showRegion;

    /** user_id */
    private Long userId;

    /** create_time */
    private LocalDateTime createTime;

    /** update_time */
    private LocalDateTime updateTime;

    /** deleted */
    private Integer deleted;

    public Long getId() { return id; }
    public void setId(Long v) { this.id = v; }
    public String getAlumniNo() { return alumniNo; }
    public void setAlumniNo(String v) { this.alumniNo = v; }
    public String getStudentNo() { return studentNo; }
    public void setStudentNo(String v) { this.studentNo = v; }
    public String getRealName() { return realName; }
    public void setRealName(String v) { this.realName = v; }
    public String getGender() { return gender; }
    public void setGender(String v) { this.gender = v; }
    public LocalDate getBirthDate() { return birthDate; }
    public void setBirthDate(LocalDate v) { this.birthDate = v; }
    public Integer getEnrollYear() { return enrollYear; }
    public void setEnrollYear(Integer v) { this.enrollYear = v; }
    public Integer getGraduateYear() { return graduateYear; }
    public void setGraduateYear(Integer v) { this.graduateYear = v; }
    public String getCollege() { return college; }
    public void setCollege(String v) { this.college = v; }
    public String getMajor() { return major; }
    public void setMajor(String v) { this.major = v; }
    public String getClassName() { return className; }
    public void setClassName(String v) { this.className = v; }
    public String getPhone() { return phone; }
    public void setPhone(String v) { this.phone = v; }
    public String getEmail() { return email; }
    public void setEmail(String v) { this.email = v; }
    public String getWorkUnit() { return workUnit; }
    public void setWorkUnit(String v) { this.workUnit = v; }
    public String getWorkTitle() { return workTitle; }
    public void setWorkTitle(String v) { this.workTitle = v; }
    public String getRegionName() { return regionName; }
    public void setRegionName(String v) { this.regionName = v; }
    public String getIndustry() { return industry; }
    public void setIndustry(String v) { this.industry = v; }
    public String getAvatar() { return avatar; }
    public void setAvatar(String v) { this.avatar = v; }
    public String getCertStatus() { return certStatus; }
    public void setCertStatus(String v) { this.certStatus = v; }
    public String getCertMaterial() { return certMaterial; }
    public void setCertMaterial(String v) { this.certMaterial = v; }
    public String getCertRemark() { return certRemark; }
    public void setCertRemark(String v) { this.certRemark = v; }
    public String getAuditUser() { return auditUser; }
    public void setAuditUser(String v) { this.auditUser = v; }
    public LocalDateTime getAuditTime() { return auditTime; }
    public void setAuditTime(LocalDateTime v) { this.auditTime = v; }
    public String getPrivacyLevel() { return privacyLevel; }
    public void setPrivacyLevel(String v) { this.privacyLevel = v; }
    public Integer getShowPhone() { return showPhone; }
    public void setShowPhone(Integer v) { this.showPhone = v; }
    public Integer getShowEmail() { return showEmail; }
    public void setShowEmail(Integer v) { this.showEmail = v; }
    public Integer getShowUnit() { return showUnit; }
    public void setShowUnit(Integer v) { this.showUnit = v; }
    public Integer getShowRegion() { return showRegion; }
    public void setShowRegion(Integer v) { this.showRegion = v; }
    public Long getUserId() { return userId; }
    public void setUserId(Long v) { this.userId = v; }
    public LocalDateTime getCreateTime() { return createTime; }
    public void setCreateTime(LocalDateTime v) { this.createTime = v; }
    public LocalDateTime getUpdateTime() { return updateTime; }
    public void setUpdateTime(LocalDateTime v) { this.updateTime = v; }
    public Integer getDeleted() { return deleted; }
    public void setDeleted(Integer v) { this.deleted = v; }
}
