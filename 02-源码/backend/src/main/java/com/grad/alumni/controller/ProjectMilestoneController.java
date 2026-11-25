package com.grad.alumni.controller;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.grad.alumni.entity.ProjectMilestone;
import com.grad.alumni.mapper.ProjectMilestoneMapper;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/** ProjectMilestone 通用增删改查接口（分页/详情/新建/更新/删除） */
@RestController
@RequestMapping("/api/milestone")
public class ProjectMilestoneController extends BaseController<ProjectMilestone> {

    private final ProjectMilestoneMapper mapper;

    public ProjectMilestoneController(ProjectMilestoneMapper mapper) {
        this.mapper = mapper;
    }

    @Override
    protected BaseMapper<ProjectMilestone> mapper() {
        return mapper;
    }

    @Override
    protected String kwColumn() { return "milestone_name"; }
    @Override
    protected String statusColumn() { return "status"; }
}
