package com.grad.alumni.entity;

import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import java.time.LocalDateTime;

/** organization_notice 实体（字段与数据库列一一对应） */
@TableName("organization_notice")
public class OrganizationNotice {

    @TableId
    /** id */
    private Long id;

    /** org_id */
    private Long orgId;

    /** org_name */
    private String orgName;

    /** title */
    private String title;

    /** content */
    private String content;

    /** publisher */
    private String publisher;

    /** publish_time */
    private LocalDateTime publishTime;

    /** top_flag */
    private Integer topFlag;

    /** create_time */
    private LocalDateTime createTime;

    public Long getId() { return id; }
    public void setId(Long v) { this.id = v; }
    public Long getOrgId() { return orgId; }
    public void setOrgId(Long v) { this.orgId = v; }
    public String getOrgName() { return orgName; }
    public void setOrgName(String v) { this.orgName = v; }
    public String getTitle() { return title; }
    public void setTitle(String v) { this.title = v; }
    public String getContent() { return content; }
    public void setContent(String v) { this.content = v; }
    public String getPublisher() { return publisher; }
    public void setPublisher(String v) { this.publisher = v; }
    public LocalDateTime getPublishTime() { return publishTime; }
    public void setPublishTime(LocalDateTime v) { this.publishTime = v; }
    public Integer getTopFlag() { return topFlag; }
    public void setTopFlag(Integer v) { this.topFlag = v; }
    public LocalDateTime getCreateTime() { return createTime; }
    public void setCreateTime(LocalDateTime v) { this.createTime = v; }
}
