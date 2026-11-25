package com.grad.alumni.entity;

import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import java.time.LocalDateTime;

/** sys_file 实体（字段与数据库列一一对应） */
@TableName("sys_file")
public class SysFile {

    @TableId
    /** id */
    private Long id;

    /** file_name */
    private String fileName;

    /** file_path */
    private String filePath;

    /** file_size */
    private Long fileSize;

    /** file_type */
    private String fileType;

    /** biz_type */
    private String bizType;

    /** uploader_id */
    private Long uploaderId;

    /** uploader_name */
    private String uploaderName;

    /** create_time */
    private LocalDateTime createTime;

    public Long getId() { return id; }
    public void setId(Long v) { this.id = v; }
    public String getFileName() { return fileName; }
    public void setFileName(String v) { this.fileName = v; }
    public String getFilePath() { return filePath; }
    public void setFilePath(String v) { this.filePath = v; }
    public Long getFileSize() { return fileSize; }
    public void setFileSize(Long v) { this.fileSize = v; }
    public String getFileType() { return fileType; }
    public void setFileType(String v) { this.fileType = v; }
    public String getBizType() { return bizType; }
    public void setBizType(String v) { this.bizType = v; }
    public Long getUploaderId() { return uploaderId; }
    public void setUploaderId(Long v) { this.uploaderId = v; }
    public String getUploaderName() { return uploaderName; }
    public void setUploaderName(String v) { this.uploaderName = v; }
    public LocalDateTime getCreateTime() { return createTime; }
    public void setCreateTime(LocalDateTime v) { this.createTime = v; }
}
