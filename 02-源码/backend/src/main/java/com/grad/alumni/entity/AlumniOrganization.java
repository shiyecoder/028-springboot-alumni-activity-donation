package com.grad.alumni.entity;

import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import java.time.LocalDateTime;

/** alumni_organization 实体（字段与数据库列一一对应） */
@TableName("alumni_organization")
public class AlumniOrganization {

    @TableId
    /** id */
    private Long id;

    /** org_name */
    private String orgName;

    /** org_code */
    private String orgCode;

    /** org_type */
    private String orgType;

    /** college */
    private String college;

    /** region_name */
    private String regionName;

    /** grade_year */
    private Integer gradeYear;

    /** leader_name */
    private String leaderName;

    /** leader_phone */
    private String leaderPhone;

    /** member_count */
    private Integer memberCount;

    /** intro */
    private String intro;

    /** cover_image */
    private String coverImage;

    /** status */
    private String status;

    /** create_time */
    private LocalDateTime createTime;

    /** update_time */
    private LocalDateTime updateTime;

    /** deleted */
    private Integer deleted;

    public Long getId() { return id; }
    public void setId(Long v) { this.id = v; }
    public String getOrgName() { return orgName; }
    public void setOrgName(String v) { this.orgName = v; }
    public String getOrgCode() { return orgCode; }
    public void setOrgCode(String v) { this.orgCode = v; }
    public String getOrgType() { return orgType; }
    public void setOrgType(String v) { this.orgType = v; }
    public String getCollege() { return college; }
    public void setCollege(String v) { this.college = v; }
    public String getRegionName() { return regionName; }
    public void setRegionName(String v) { this.regionName = v; }
    public Integer getGradeYear() { return gradeYear; }
    public void setGradeYear(Integer v) { this.gradeYear = v; }
    public String getLeaderName() { return leaderName; }
    public void setLeaderName(String v) { this.leaderName = v; }
    public String getLeaderPhone() { return leaderPhone; }
    public void setLeaderPhone(String v) { this.leaderPhone = v; }
    public Integer getMemberCount() { return memberCount; }
    public void setMemberCount(Integer v) { this.memberCount = v; }
    public String getIntro() { return intro; }
    public void setIntro(String v) { this.intro = v; }
    public String getCoverImage() { return coverImage; }
    public void setCoverImage(String v) { this.coverImage = v; }
    public String getStatus() { return status; }
    public void setStatus(String v) { this.status = v; }
    public LocalDateTime getCreateTime() { return createTime; }
    public void setCreateTime(LocalDateTime v) { this.createTime = v; }
    public LocalDateTime getUpdateTime() { return updateTime; }
    public void setUpdateTime(LocalDateTime v) { this.updateTime = v; }
    public Integer getDeleted() { return deleted; }
    public void setDeleted(Integer v) { this.deleted = v; }
}
