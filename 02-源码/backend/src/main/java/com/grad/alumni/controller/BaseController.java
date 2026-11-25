package com.grad.alumni.controller;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.grad.alumni.common.BizException;
import com.grad.alumni.common.PageResult;
import com.grad.alumni.common.R;
import com.grad.alumni.common.UserContext;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

/**
 * 通用 CRUD 控制器基类：分页、详情、新建、更新、删除。
 * 子类只需给出 Mapper 与可搜索列，业务校验放在具体业务接口里，不在此处堆叠。
 */
public abstract class BaseController<T> {

    protected abstract BaseMapper<T> mapper();

    /** 关键字模糊搜索列（可空表示不支持） */
    protected String kwColumn() { return null; }

    /** 精确匹配状态列（可空表示不支持） */
    protected String statusColumn() { return null; }

    /** 默认排序，保证列表稳定 */
    protected String orderBy() { return "create_time"; }

    protected boolean desc() { return true; }

    protected QueryWrapper<T> buildQuery(String kw, String status, Map<String, String> params) {
        QueryWrapper<T> q = new QueryWrapper<>();
        if (kw != null && !kw.isBlank() && kwColumn() != null) {
            q.like(kwColumn(), kw.trim());
        }
        if (status != null && !status.isBlank() && statusColumn() != null) {
            q.eq(statusColumn(), status);
        }
        // 额外等值筛选：只接受子类声明的列，避免 SQL 注入
        Map<String, String> allowed = extraFilters();
        for (Map.Entry<String, String> e : allowed.entrySet()) {
            String v = params.get(e.getKey());
            if (v != null && !v.isBlank()) {
                q.eq(e.getValue(), v.trim());
            }
        }
        q.orderBy(true, desc(), orderBy());
        return q;
    }

    /** 允许通过查询参数等值筛选的字段：参数名 -> 数据库列 */
    protected Map<String, String> extraFilters() { return Map.of(); }

    @GetMapping("/page")
    public R<PageResult<T>> page(@RequestParam(defaultValue = "1") long page,
                                 @RequestParam(defaultValue = "10") long size,
                                 @RequestParam(required = false) String kw,
                                 @RequestParam(required = false) String status,
                                 @RequestParam Map<String, String> params) {
        if (page < 1) page = 1;
        if (size < 1 || size > 200) size = 10;
        Page<T> p = mapper().selectPage(new Page<>(page, size), buildQuery(kw, status, params));
        return R.ok(PageResult.of(p));
    }

    @GetMapping("/{id}")
    public R<T> detail(@PathVariable Long id) {
        T t = mapper().selectById(id);
        if (t == null) throw new BizException("记录不存在或已删除");
        return R.ok(t);
    }

    @PostMapping
    public R<T> create(@RequestBody T body) {
        beforeSave(body, true);
        mapper().insert(body);
        return R.ok(body);
    }

    @PutMapping("/{id}")
    public R<T> update(@PathVariable Long id, @RequestBody T body) {
        beforeSave(body, false);
        mapper().updateById(body);
        return R.ok(body);
    }

    @DeleteMapping("/{id}")
    public R<Void> delete(@PathVariable Long id) {
        mapper().deleteById(id);
        return R.ok();
    }

    /** 保存前钩子：子类可校验必填、去空格、补默认值 */
    protected void beforeSave(T body, boolean create) { }

    /** 生成业务编号：前缀 + 年份 + 6 位序列，前端只读 */
    protected String nextNo(String prefix) {
        return prefix + "-" + java.time.LocalDate.now().getYear()
                + String.format("%06d", (System.currentTimeMillis() / 1000) % 1000000);
    }

    protected String operator() {
        return UserContext.name();
    }
}
