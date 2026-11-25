package com.grad.alumni.controller;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.grad.alumni.entity.ActivityArchive;
import com.grad.alumni.mapper.ActivityArchiveMapper;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/** ActivityArchive 通用增删改查接口（分页/详情/新建/更新/删除） */
@RestController
@RequestMapping("/api/archive")
public class ActivityArchiveController extends BaseController<ActivityArchive> {

    private final ActivityArchiveMapper mapper;

    public ActivityArchiveController(ActivityArchiveMapper mapper) {
        this.mapper = mapper;
    }

    @Override
    protected BaseMapper<ActivityArchive> mapper() {
        return mapper;
    }

    @Override
    protected String kwColumn() { return "activity_title"; }
}
