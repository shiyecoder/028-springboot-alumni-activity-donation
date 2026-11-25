package com.grad.alumni.controller;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.grad.alumni.entity.SysDict;
import com.grad.alumni.mapper.SysDictMapper;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/** SysDict 通用增删改查接口（分页/详情/新建/更新/删除） */
@RestController
@RequestMapping("/api/sys-dict")
public class SysDictController extends BaseController<SysDict> {

    private final SysDictMapper mapper;

    public SysDictController(SysDictMapper mapper) {
        this.mapper = mapper;
    }

    @Override
    protected BaseMapper<SysDict> mapper() {
        return mapper;
    }

    @Override
    protected String kwColumn() { return "dict_label"; }
}
