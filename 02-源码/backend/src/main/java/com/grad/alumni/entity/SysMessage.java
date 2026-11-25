package com.grad.alumni.entity;

import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import java.time.LocalDateTime;

/** sys_message 实体（字段与数据库列一一对应） */
@TableName("sys_message")
public class SysMessage {

    @TableId
    /** id */
    private Long id;

    /** user_id */
    private Long userId;

    /** title */
    private String title;

    /** content */
    private String content;

    /** msg_type */
    private String msgType;

    /** biz_no */
    private String bizNo;

    /** biz_url */
    private String bizUrl;

    /** read_flag */
    private Integer readFlag;

    /** create_time */
    private LocalDateTime createTime;

    public Long getId() { return id; }
    public void setId(Long v) { this.id = v; }
    public Long getUserId() { return userId; }
    public void setUserId(Long v) { this.userId = v; }
    public String getTitle() { return title; }
    public void setTitle(String v) { this.title = v; }
    public String getContent() { return content; }
    public void setContent(String v) { this.content = v; }
    public String getMsgType() { return msgType; }
    public void setMsgType(String v) { this.msgType = v; }
    public String getBizNo() { return bizNo; }
    public void setBizNo(String v) { this.bizNo = v; }
    public String getBizUrl() { return bizUrl; }
    public void setBizUrl(String v) { this.bizUrl = v; }
    public Integer getReadFlag() { return readFlag; }
    public void setReadFlag(Integer v) { this.readFlag = v; }
    public LocalDateTime getCreateTime() { return createTime; }
    public void setCreateTime(LocalDateTime v) { this.createTime = v; }
}
