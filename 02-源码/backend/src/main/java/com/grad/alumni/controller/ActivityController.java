package com.grad.alumni.controller;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.grad.alumni.common.*;
import com.grad.alumni.entity.ActivityArchive;
import com.grad.alumni.entity.ActivitySignup;
import com.grad.alumni.entity.AlumniActivity;
import com.grad.alumni.mapper.ActivityArchiveMapper;
import com.grad.alumni.mapper.ActivitySignupMapper;
import com.grad.alumni.mapper.AlumniActivityMapper;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.*;

/** 活动管理：发起、审核、详情；人数满后报名进候补由报名接口处理 */
@RestController
@RequestMapping("/api/activity")
public class ActivityController extends BaseController<AlumniActivity> {

    private final AlumniActivityMapper mapper;
    private final ActivitySignupMapper signupMapper;
    private final ActivityArchiveMapper archiveMapper;

    public ActivityController(AlumniActivityMapper mapper, ActivitySignupMapper signupMapper,
                              ActivityArchiveMapper archiveMapper) {
        this.mapper = mapper;
        this.signupMapper = signupMapper;
        this.archiveMapper = archiveMapper;
    }

    @Override
    protected BaseMapper<AlumniActivity> mapper() { return mapper; }

    @Override
    protected String kwColumn() { return "title"; }

    @Override
    protected String statusColumn() { return "status"; }

    @Override
    protected Map<String, String> extraFilters() {
        return Map.of("activityType", "activity_type", "college", "college", "orgId", "org_id");
    }

    @Override
    protected void beforeSave(AlumniActivity body, boolean create) {
        if (create) {
            if (body.getTitle() == null || body.getTitle().isBlank()) throw new BizException("活动名称不能为空");
            if (body.getCapacity() == null || body.getCapacity() <= 0) throw new BizException("人数上限必须大于 0");
            body.setActivityNo(nextNo("ACT"));
            body.setStatus("待审核");
            body.setSignupCount(0);
            body.setWaitCount(0);
            body.setCheckinCount(0);
            body.setDeleted(0);
            body.setCreateTime(LocalDateTime.now());
        }
        body.setUpdateTime(LocalDateTime.now());
    }

    /** 活动审核：待审核 -> 报名中 / 已驳回（驳回原因≥5 字） */
    @PostMapping("/{id}/audit")
    public R<Void> audit(@PathVariable Long id, @RequestBody Map<String, String> body) {
        String status = body.getOrDefault("status", "");
        String reason = body.getOrDefault("reason", "").trim();
        if (!"报名中".equals(status) && !"已驳回".equals(status)) throw new BizException("审核结果不合法");
        AlumniActivity a = mapper.selectById(id);
        if (a == null) throw new BizException("活动不存在");
        if (!"待审核".equals(a.getStatus())) throw new BizException("只有待审核的活动可以审核");
        if ("已驳回".equals(status) && reason.length() < 5) throw new BizException("驳回原因不少于 5 个字");
        AlumniActivity up = new AlumniActivity();
        up.setId(id);
        up.setStatus(status);
        up.setRejectReason("已驳回".equals(status) ? reason : null);
        up.setUpdateTime(LocalDateTime.now());
        mapper.updateById(up);
        return R.ok();
    }

    /** 活动详情：基础信息 + 报名统计 + 归档信息 */
    @GetMapping("/{id}/detail")
    public R<Map<String, Object>> detailAll(@PathVariable Long id) {
        AlumniActivity a = mapper.selectById(id);
        if (a == null) throw new BizException("活动不存在");
        List<ActivitySignup> signs = signupMapper.selectList(new QueryWrapper<ActivitySignup>()
                .eq("activity_id", id).orderByAsc("id"));
        Map<String, Integer> byStatus = new LinkedHashMap<>();
        for (ActivitySignup s : signs) {
            byStatus.merge(s.getStatus(), 1, Integer::sum);
        }
        ActivityArchive archive = archiveMapper.selectOne(new QueryWrapper<ActivityArchive>()
                .eq("activity_id", id).last("limit 1"));
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("activity", a);
        out.put("signupStats", byStatus);
        out.put("signupTotal", signs.size());
        out.put("archive", archive);
        return R.ok(out);
    }

    /** 报名名单（含候补序号），按报名时间排序 */
    @GetMapping("/{id}/signups")
    public R<List<ActivitySignup>> signups(@PathVariable Long id) {
        return R.ok(signupMapper.selectList(new QueryWrapper<ActivitySignup>()
                .eq("activity_id", id).orderByAsc("create_time")));
    }
}
