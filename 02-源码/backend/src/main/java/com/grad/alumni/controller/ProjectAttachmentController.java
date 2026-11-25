package com.grad.alumni.controller;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.grad.alumni.entity.ProjectAttachment;
import com.grad.alumni.mapper.ProjectAttachmentMapper;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/** ProjectAttachment 通用增删改查接口（分页/详情/新建/更新/删除） */
@RestController
@RequestMapping("/api/attachment")
public class ProjectAttachmentController extends BaseController<ProjectAttachment> {

    private final ProjectAttachmentMapper mapper;

    public ProjectAttachmentController(ProjectAttachmentMapper mapper) {
        this.mapper = mapper;
    }

    @Override
    protected BaseMapper<ProjectAttachment> mapper() {
        return mapper;
    }

    @Override
    protected String kwColumn() { return "file_name"; }
}
