package com.grad.alumni.entity;

import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import java.time.LocalDateTime;

/** sys_log 实体（字段与数据库列一一对应） */
@TableName("sys_log")
public class SysLog {

    @TableId
    /** id */
    private Long id;

    /** user_id */
    private Long userId;

    /** user_name */
    private String userName;

    /** module */
    private String module;

    /** action */
    private String action;

    /** method */
    private String method;

    /** params */
    private String params;

    /** ip */
    private String ip;

    /** cost_ms */
    private Integer costMs;

    /** create_time */
    private LocalDateTime createTime;

    public Long getId() { return id; }
    public void setId(Long v) { this.id = v; }
    public Long getUserId() { return userId; }
    public void setUserId(Long v) { this.userId = v; }
    public String getUserName() { return userName; }
    public void setUserName(String v) { this.userName = v; }
    public String getModule() { return module; }
    public void setModule(String v) { this.module = v; }
    public String getAction() { return action; }
    public void setAction(String v) { this.action = v; }
    public String getMethod() { return method; }
    public void setMethod(String v) { this.method = v; }
    public String getParams() { return params; }
    public void setParams(String v) { this.params = v; }
    public String getIp() { return ip; }
    public void setIp(String v) { this.ip = v; }
    public Integer getCostMs() { return costMs; }
    public void setCostMs(Integer v) { this.costMs = v; }
    public LocalDateTime getCreateTime() { return createTime; }
    public void setCreateTime(LocalDateTime v) { this.createTime = v; }
}
