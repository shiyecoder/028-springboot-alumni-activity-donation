package com.grad.alumni.controller;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.grad.alumni.common.*;
import com.grad.alumni.entity.*;
import com.grad.alumni.mapper.*;
import org.springframework.web.bind.annotation.*;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.*;

/**
 * 捐赠项目（核心过程单据）。
 * 主流程：项目立项 → 募集中 → 执行中 → 待验收 → 已结项；任一阶段可取消（须填原因）。
 * 状态流转全部在后端校验，禁止前端越级调用。
 */
@RestController
@RequestMapping("/api/project")
public class ProjectController extends BaseController<DonationProject> {

    private static final Map<String, List<String>> NEXT = Map.of(
            "项目立项", List.of("募集中", "已取消"),
            "募集中", List.of("执行中", "已取消"),
            "执行中", List.of("待验收", "已取消"),
            "待验收", List.of("已结项", "执行中"),
            "已结项", List.of(),
            "已驳回", List.of("项目立项"),
            "已取消", List.of());

    private final DonationProjectMapper mapper;
    private final ProjectMilestoneMapper milestoneMapper;
    private final ProjectProgressMapper progressMapper;
    private final DonationRecordMapper recordMapper;
    private final ProjectAttachmentMapper attachmentMapper;
    private final AlumniProjectScoreMapper scoreMapper;

    public ProjectController(DonationProjectMapper mapper, ProjectMilestoneMapper milestoneMapper,
                             ProjectProgressMapper progressMapper, DonationRecordMapper recordMapper,
                             ProjectAttachmentMapper attachmentMapper, AlumniProjectScoreMapper scoreMapper) {
        this.mapper = mapper;
        this.milestoneMapper = milestoneMapper;
        this.progressMapper = progressMapper;
        this.recordMapper = recordMapper;
        this.attachmentMapper = attachmentMapper;
        this.scoreMapper = scoreMapper;
    }

    @Override
    protected BaseMapper<DonationProject> mapper() { return mapper; }

    @Override
    protected String kwColumn() { return "project_name"; }

    @Override
    protected String statusColumn() { return "status"; }

    @Override
    protected Map<String, String> extraFilters() {
        return Map.of("initiator", "initiator", "publicStatus", "public_status", "chargePerson", "charge_person");
    }

    @Override
    protected void beforeSave(DonationProject body, boolean create) {
        if (create) {
            if (body.getProjectName() == null || body.getProjectName().isBlank()) throw new BizException("项目名称不能为空");
            if (body.getInitiator() == null || body.getInitiator().isBlank()) throw new BizException("发起单位不能为空");
            if (body.getTargetAmount() == null || body.getTargetAmount().signum() < 0)
                throw new BizException("目标金额不能为负数");
            body.setProjectName(body.getProjectName().trim());
            body.setProjectNo(nextNo("PJ"));
            body.setStatus(body.getStatus() == null ? "项目立项" : body.getStatus());
            body.setPublicStatus(body.getPublicStatus() == null ? "待审核" : body.getPublicStatus());
            body.setRaisedAmount(BigDecimal.ZERO);
            body.setSpentAmount(BigDecimal.ZERO);
            body.setMilestoneRate(BigDecimal.ZERO);
            body.setProgressRate(BigDecimal.ZERO);
            body.setDeleted(0);
            body.setCreateTime(LocalDateTime.now());
        }
        if (body.getStartDate() != null && body.getEndDate() != null && body.getEndDate().isBefore(body.getStartDate())) {
            throw new BizException("结束日期不能早于开始日期");
        }
        body.setUpdateTime(LocalDateTime.now());
    }

    /** 状态流转：校验目标状态是否合法，取消/退回必须填写原因（≥5 字） */
    @PostMapping("/{id}/transition")
    public R<Void> transition(@PathVariable Long id, @RequestBody Map<String, String> body) {
        DonationProject p = mapper.selectById(id);
        if (p == null) throw new BizException("项目不存在");
        String target = body.getOrDefault("status", "");
        String reason = body.getOrDefault("reason", "").trim();
        List<String> allowed = NEXT.getOrDefault(p.getStatus(), List.of());
        if (!allowed.contains(target)) {
            throw new BizException("不允许从「" + p.getStatus() + "」流转到「" + target + "」");
        }
        if (("已取消".equals(target) || "项目立项".equals(target)) && reason.length() < 5) {
            throw new BizException("取消或退回必须填写原因，且不少于 5 个字");
        }
        DonationProject up = new DonationProject();
        up.setId(id);
        up.setStatus(target);
        up.setPublicFlag("已取消".equals(target) ? 0 : p.getPublicFlag());
        up.setUpdateTime(LocalDateTime.now());
        mapper.updateById(up);
        return R.ok();
    }

    /** 项目详情：基础信息 + 里程碑 + 进展 + 关联捐赠 + 附件 + 最近一次计算结果 */
    @GetMapping("/{id}/detail")
    public R<Map<String, Object>> detailAll(@PathVariable Long id) {
        DonationProject p = mapper.selectById(id);
        if (p == null) throw new BizException("项目不存在");
        List<ProjectMilestone> ms = milestoneMapper.selectList(new QueryWrapper<ProjectMilestone>()
                .eq("project_id", id).orderByAsc("seq_no"));
        List<ProjectProgress> progress = progressMapper.selectList(new QueryWrapper<ProjectProgress>()
                .eq("project_id", id).orderByDesc("publish_time"));
        List<DonationRecord> records = recordMapper.selectList(new QueryWrapper<DonationRecord>()
                .eq("project_id", id).orderByDesc("donate_date").last("limit 20"));
        List<ProjectAttachment> atts = attachmentMapper.selectList(new QueryWrapper<ProjectAttachment>()
                .eq("project_id", id).orderByDesc("id"));
        AlumniProjectScore score = scoreMapper.selectOne(new QueryWrapper<AlumniProjectScore>()
                .eq("project_id", id).orderByDesc("calc_time").last("limit 1"));
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("project", p);
        out.put("milestones", ms);
        out.put("progress", progress);
        out.put("records", records);
        out.put("attachments", atts);
        out.put("score", score);
        return R.ok(out);
    }

    /** 公开端可见的项目（仅审核通过且公开） */
    @GetMapping("/public-list")
    public R<List<DonationProject>> publicList() {
        return R.ok(mapper.selectList(new QueryWrapper<DonationProject>()
                .eq("public_status", "已通过").eq("public_flag", 1).ne("status", "已取消")
                .orderByDesc("create_time")));
    }
}
