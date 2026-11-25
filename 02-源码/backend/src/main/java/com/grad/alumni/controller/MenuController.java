package com.grad.alumni.controller;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.grad.alumni.common.R;
import com.grad.alumni.entity.SysMenu;
import com.grad.alumni.mapper.SysMenuMapper;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.*;

/** 菜单管理：树形返回，前端按角色渲染 */
@RestController
@RequestMapping("/api/menu")
public class MenuController extends BaseController<SysMenu> {

    private final SysMenuMapper mapper;

    public MenuController(SysMenuMapper mapper) { this.mapper = mapper; }

    @Override
    protected BaseMapper<SysMenu> mapper() { return mapper; }

    @Override
    protected String kwColumn() { return "menu_name"; }

    @Override
    protected String orderBy() { return "sort_no"; }

    @Override
    protected boolean desc() { return false; }

    /** 全部菜单树（含按钮），供角色分配菜单使用；「菜单管理」自身不参与分配 */
    @GetMapping("/tree")
    public R<List<Map<String, Object>>> tree() {
        List<SysMenu> all = mapper.selectList(new QueryWrapper<SysMenu>().orderByAsc("sort_no"));
        return R.ok(build(all, 0L));
    }

    private List<Map<String, Object>> build(List<SysMenu> all, Long parent) {
        List<Map<String, Object>> out = new ArrayList<>();
        for (SysMenu m : all) {
            if (!Objects.equals(m.getParentId() == null ? 0L : m.getParentId(), parent)) continue;
            Map<String, Object> one = new LinkedHashMap<>();
            one.put("id", m.getId());
            one.put("menuName", m.getMenuName());
            one.put("menuType", m.getMenuType());
            one.put("path", m.getPath());
            one.put("sortNo", m.getSortNo());
            one.put("visible", m.getVisible());
            one.put("children", build(all, m.getId()));
            out.add(one);
        }
        return out;
    }
}
