package com.grad.alumni.entity;

import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import java.time.LocalDateTime;

/** sys_org 实体（字段与数据库列一一对应） */
@TableName("sys_org")
public class SysOrg {

    @TableId
    /** id */
    private Long id;

    /** org_name */
    private String orgName;

    /** org_code */
    private String orgCode;

    /** org_type */
    private String orgType;

    /** parent_id */
    private Long parentId;

    /** sort_no */
    private Integer sortNo;

    /** status */
    private Integer status;

    /** create_time */
    private LocalDateTime createTime;

    public Long getId() { return id; }
    public void setId(Long v) { this.id = v; }
    public String getOrgName() { return orgName; }
    public void setOrgName(String v) { this.orgName = v; }
    public String getOrgCode() { return orgCode; }
    public void setOrgCode(String v) { this.orgCode = v; }
    public String getOrgType() { return orgType; }
    public void setOrgType(String v) { this.orgType = v; }
    public Long getParentId() { return parentId; }
    public void setParentId(Long v) { this.parentId = v; }
    public Integer getSortNo() { return sortNo; }
    public void setSortNo(Integer v) { this.sortNo = v; }
    public Integer getStatus() { return status; }
    public void setStatus(Integer v) { this.status = v; }
    public LocalDateTime getCreateTime() { return createTime; }
    public void setCreateTime(LocalDateTime v) { this.createTime = v; }
}
