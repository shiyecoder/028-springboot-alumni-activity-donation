package com.grad.alumni.controller;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.grad.alumni.entity.SysRoleMenu;
import com.grad.alumni.mapper.SysRoleMenuMapper;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/** SysRoleMenu 通用增删改查接口（分页/详情/新建/更新/删除） */
@RestController
@RequestMapping("/api/sys-rolemenu")
public class SysRoleMenuController extends BaseController<SysRoleMenu> {

    private final SysRoleMenuMapper mapper;

    public SysRoleMenuController(SysRoleMenuMapper mapper) {
        this.mapper = mapper;
    }

    @Override
    protected BaseMapper<SysRoleMenu> mapper() {
        return mapper;
    }

}
