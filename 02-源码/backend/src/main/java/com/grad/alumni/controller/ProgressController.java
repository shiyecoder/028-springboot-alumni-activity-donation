package com.grad.alumni.controller;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.grad.alumni.common.*;
import com.grad.alumni.entity.DonationProject;
import com.grad.alumni.entity.ProjectProgress;
import com.grad.alumni.mapper.DonationProjectMapper;
import com.grad.alumni.mapper.ProjectProgressMapper;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;

/** 进展公示：发布后需审核，审核通过才对公开端可见 */
@RestController
@RequestMapping("/api/progress")
public class ProgressController extends BaseController<ProjectProgress> {

    private final ProjectProgressMapper mapper;
    private final DonationProjectMapper projectMapper;

    public ProgressController(ProjectProgressMapper mapper, DonationProjectMapper projectMapper) {
        this.mapper = mapper;
        this.projectMapper = projectMapper;
    }

    @Override
    protected BaseMapper<ProjectProgress> mapper() { return mapper; }

    @Override
    protected String kwColumn() { return "stage_name"; }

    @Override
    protected String statusColumn() { return "audit_status"; }

    @Override
    protected Map<String, String> extraFilters() { return Map.of("projectId", "project_id"); }

    @Override
    protected void beforeSave(ProjectProgress body, boolean create) {
        if (create) {
            DonationProject p = projectMapper.selectById(body.getProjectId());
            if (p == null) throw new BizException("项目不存在");
            if (body.getStageName() == null || body.getStageName().isBlank()) throw new BizException("进展阶段不能为空");
            body.setProjectName(p.getProjectName());
            body.setAuditStatus("待审核");
            body.setPublishUser(UserContext.name());
            body.setPublishTime(LocalDateTime.now());
            body.setCreateTime(LocalDateTime.now());
        }
    }

    @PostMapping("/{id}/audit")
    public R<Void> audit(@PathVariable Long id, @RequestBody Map<String, String> body) {
        if (!UserContext.isAdmin()) throw new BizException(403, "只有校友办管理员可以审核进展公示");
        String status = body.getOrDefault("status", "");
        if (!"已发布".equals(status) && !"已驳回".equals(status)) throw new BizException("审核结果不合法");
        ProjectProgress up = new ProjectProgress();
        up.setId(id);
        up.setAuditStatus(status);
        up.setAuditUser(UserContext.name());
        up.setAuditTime(LocalDateTime.now());
        mapper.updateById(up);
        return R.ok();
    }

    /** 时间轴：按发布时间正序，供详情页展示 */
    @GetMapping("/timeline/{projectId}")
    public R<List<ProjectProgress>> timeline(@PathVariable Long projectId) {
        return R.ok(mapper.selectList(new QueryWrapper<ProjectProgress>()
                .eq("project_id", projectId).orderByAsc("publish_time")));
    }
}
