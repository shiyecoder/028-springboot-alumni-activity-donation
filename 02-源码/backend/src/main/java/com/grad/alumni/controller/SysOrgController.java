package com.grad.alumni.controller;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.grad.alumni.entity.SysOrg;
import com.grad.alumni.mapper.SysOrgMapper;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/** SysOrg 通用增删改查接口（分页/详情/新建/更新/删除） */
@RestController
@RequestMapping("/api/sys-org")
public class SysOrgController extends BaseController<SysOrg> {

    private final SysOrgMapper mapper;

    public SysOrgController(SysOrgMapper mapper) {
        this.mapper = mapper;
    }

    @Override
    protected BaseMapper<SysOrg> mapper() {
        return mapper;
    }

    @Override
    protected String kwColumn() { return "org_name"; }
}
