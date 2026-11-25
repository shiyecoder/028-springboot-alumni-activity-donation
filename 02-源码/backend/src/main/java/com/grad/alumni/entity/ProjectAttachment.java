package com.grad.alumni.entity;

import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import java.time.LocalDateTime;

/** project_attachment 实体（字段与数据库列一一对应） */
@TableName("project_attachment")
public class ProjectAttachment {

    @TableId
    /** id */
    private Long id;

    /** project_id */
    private Long projectId;

    /** biz_type */
    private String bizType;

    /** file_name */
    private String fileName;

    /** file_path */
    private String filePath;

    /** file_size */
    private Long fileSize;

    /** uploader */
    private String uploader;

    /** create_time */
    private LocalDateTime createTime;

    public Long getId() { return id; }
    public void setId(Long v) { this.id = v; }
    public Long getProjectId() { return projectId; }
    public void setProjectId(Long v) { this.projectId = v; }
    public String getBizType() { return bizType; }
    public void setBizType(String v) { this.bizType = v; }
    public String getFileName() { return fileName; }
    public void setFileName(String v) { this.fileName = v; }
    public String getFilePath() { return filePath; }
    public void setFilePath(String v) { this.filePath = v; }
    public Long getFileSize() { return fileSize; }
    public void setFileSize(Long v) { this.fileSize = v; }
    public String getUploader() { return uploader; }
    public void setUploader(String v) { this.uploader = v; }
    public LocalDateTime getCreateTime() { return createTime; }
    public void setCreateTime(LocalDateTime v) { this.createTime = v; }
}
