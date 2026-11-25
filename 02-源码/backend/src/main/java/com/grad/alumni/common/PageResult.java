package com.grad.alumni.common;

import java.util.List;

/** 分页返回：总条数、页码、每页条数、数据列表 */
public class PageResult<T> {
    private long total;
    private long page;
    private long size;
    private List<T> list;

    public PageResult(long total, long page, long size, List<T> list) {
        this.total = total;
        this.page = page;
        this.size = size;
        this.list = list;
    }

    public static <T> PageResult<T> of(com.baomidou.mybatisplus.extension.plugins.pagination.Page<T> p) {
        return new PageResult<>(p.getTotal(), p.getCurrent(), p.getSize(), p.getRecords());
    }

    public long getTotal() { return total; }
    public void setTotal(long total) { this.total = total; }
    public long getPage() { return page; }
    public void setPage(long page) { this.page = page; }
    public long getSize() { return size; }
    public void setSize(long size) { this.size = size; }
    public List<T> getList() { return list; }
    public void setList(List<T> list) { this.list = list; }
}
