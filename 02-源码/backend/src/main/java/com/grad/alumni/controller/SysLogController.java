package com.grad.alumni.controller;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.grad.alumni.entity.SysLog;
import com.grad.alumni.mapper.SysLogMapper;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/** SysLog 通用增删改查接口（分页/详情/新建/更新/删除） */
@RestController
@RequestMapping("/api/sys-log")
public class SysLogController extends BaseController<SysLog> {

    private final SysLogMapper mapper;

    public SysLogController(SysLogMapper mapper) {
        this.mapper = mapper;
    }

    @Override
    protected BaseMapper<SysLog> mapper() {
        return mapper;
    }

    @Override
    protected String kwColumn() { return "module"; }
}
