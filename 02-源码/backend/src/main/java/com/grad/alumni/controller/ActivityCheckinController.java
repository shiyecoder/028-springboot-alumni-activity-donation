package com.grad.alumni.controller;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.grad.alumni.entity.ActivityCheckin;
import com.grad.alumni.mapper.ActivityCheckinMapper;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/** ActivityCheckin 通用增删改查接口（分页/详情/新建/更新/删除） */
@RestController
@RequestMapping("/api/checkin")
public class ActivityCheckinController extends BaseController<ActivityCheckin> {

    private final ActivityCheckinMapper mapper;

    public ActivityCheckinController(ActivityCheckinMapper mapper) {
        this.mapper = mapper;
    }

    @Override
    protected BaseMapper<ActivityCheckin> mapper() {
        return mapper;
    }

    @Override
    protected String kwColumn() { return "alumni_name"; }
}
