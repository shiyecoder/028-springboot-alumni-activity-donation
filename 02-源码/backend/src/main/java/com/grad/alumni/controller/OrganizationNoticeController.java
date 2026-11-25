package com.grad.alumni.controller;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.grad.alumni.entity.OrganizationNotice;
import com.grad.alumni.mapper.OrganizationNoticeMapper;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/** OrganizationNotice 通用增删改查接口（分页/详情/新建/更新/删除） */
@RestController
@RequestMapping("/api/notice")
public class OrganizationNoticeController extends BaseController<OrganizationNotice> {

    private final OrganizationNoticeMapper mapper;

    public OrganizationNoticeController(OrganizationNoticeMapper mapper) {
        this.mapper = mapper;
    }

    @Override
    protected BaseMapper<OrganizationNotice> mapper() {
        return mapper;
    }

    @Override
    protected String kwColumn() { return "title"; }
}
