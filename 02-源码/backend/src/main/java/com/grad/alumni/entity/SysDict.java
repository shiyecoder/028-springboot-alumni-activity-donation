package com.grad.alumni.entity;

import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import java.time.LocalDateTime;

/** sys_dict 实体（字段与数据库列一一对应） */
@TableName("sys_dict")
public class SysDict {

    @TableId
    /** id */
    private Long id;

    /** dict_type */
    private String dictType;

    /** dict_code */
    private String dictCode;

    /** dict_label */
    private String dictLabel;

    /** sort_no */
    private Integer sortNo;

    /** status */
    private Integer status;

    /** create_time */
    private LocalDateTime createTime;

    public Long getId() { return id; }
    public void setId(Long v) { this.id = v; }
    public String getDictType() { return dictType; }
    public void setDictType(String v) { this.dictType = v; }
    public String getDictCode() { return dictCode; }
    public void setDictCode(String v) { this.dictCode = v; }
    public String getDictLabel() { return dictLabel; }
    public void setDictLabel(String v) { this.dictLabel = v; }
    public Integer getSortNo() { return sortNo; }
    public void setSortNo(Integer v) { this.sortNo = v; }
    public Integer getStatus() { return status; }
    public void setStatus(Integer v) { this.status = v; }
    public LocalDateTime getCreateTime() { return createTime; }
    public void setCreateTime(LocalDateTime v) { this.createTime = v; }
}
