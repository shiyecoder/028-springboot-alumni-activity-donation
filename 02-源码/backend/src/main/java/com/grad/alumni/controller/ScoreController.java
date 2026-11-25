package com.grad.alumni.controller;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.grad.alumni.common.*;
import com.grad.alumni.entity.*;
import com.grad.alumni.mapper.*;
import org.springframework.web.bind.annotation.*;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.LocalDateTime;
import java.util.*;

/**
 * 创新模块：捐赠目标与执行里程碑公开 —— 计算留痕与人工修正。
 *
 * 计算口径（每项先折算 0~100 分，再按权重加权求和）：
 *  1 目标金额：目标 / 50 万 × 100，封顶 100
 *  2 已登记金额：已核对金额 / 目标 × 100，封顶 100
 *  3 里程碑完成度：已完成里程碑权重之和 / 全部权重 × 100
 *  4 支出凭证：凭证份数 × 12.5，封顶 100
 *  5 受益人数：受益人数 / 1000 × 100，封顶 100
 *  6 公开审核状态：已通过 100、待审核 30、已驳回 0
 * 结果等级：总分 ≥ 80 推荐；60~79 观察；< 60 不推荐。
 * 每次计算保存输入快照、规则版本与明细分；人工修正只写 manual_* 字段，原始结果不可覆盖。
 */
@RestController
@RequestMapping("/api/score")
public class ScoreController extends BaseController<AlumniProjectScore> {

    private final AlumniProjectScoreMapper mapper;
    private final DonationProjectMapper projectMapper;
    private final ProjectMilestoneMapper milestoneMapper;
    private final ProjectAttachmentMapper attachmentMapper;
    private final AlumniProjectRuleMapper ruleMapper;

    public ScoreController(AlumniProjectScoreMapper mapper, DonationProjectMapper projectMapper,
                           ProjectMilestoneMapper milestoneMapper, ProjectAttachmentMapper attachmentMapper,
                           AlumniProjectRuleMapper ruleMapper) {
        this.mapper = mapper;
        this.projectMapper = projectMapper;
        this.milestoneMapper = milestoneMapper;
        this.attachmentMapper = attachmentMapper;
        this.ruleMapper = ruleMapper;
    }

    @Override
    protected BaseMapper<AlumniProjectScore> mapper() { return mapper; }

    @Override
    protected String kwColumn() { return "project_name"; }

    @Override
    protected String statusColumn() { return "result_level"; }

    /** 对指定项目执行一次计算，返回结果与明细分项（供结果页展示，不只是一个等级） */
    @PostMapping("/project/{projectId}/evaluate")
    public R<Map<String, Object>> evaluate(@PathVariable Long projectId) {
        DonationProject p = projectMapper.selectById(projectId);
        if (p == null) throw new BizException("项目不存在");
        AlumniProjectRule rule = ruleMapper.selectOne(new QueryWrapper<AlumniProjectRule>()
                .eq("status", "启用").orderByDesc("effect_time").last("limit 1"));
        if (rule == null) throw new BizException("尚未配置启用中的规则，请先在规则配置页设置权重");

        List<ProjectMilestone> ms = milestoneMapper.selectList(new QueryWrapper<ProjectMilestone>()
                .eq("project_id", projectId));
        double totalWeight = ms.stream().mapToDouble(m -> m.getWeight() == null ? 0 : m.getWeight()).sum();
        double doneWeight = ms.stream().filter(m -> "已完成".equals(m.getStatus()))
                .mapToDouble(m -> m.getWeight() == null ? 0 : m.getWeight()).sum();
        double msRate = totalWeight <= 0 ? 0 : doneWeight / totalWeight * 100;

        long vouchers = attachmentMapper.selectCount(new QueryWrapper<ProjectAttachment>()
                .eq("project_id", projectId).eq("biz_type", "凭证"));
        double target = p.getTargetAmount() == null ? 0 : p.getTargetAmount().doubleValue();
        double raised = p.getRaisedAmount() == null ? 0 : p.getRaisedAmount().doubleValue();
        int beneficiary = p.getBeneficiaryCount() == null ? 0 : p.getBeneficiaryCount();

        double sTarget = clamp(target / 500_000 * 100);
        double sAmount = target <= 0 ? 0 : clamp(raised / target * 100);
        double sMs = clamp(msRate);
        double sVoucher = clamp(vouchers * 12.5);
        double sBen = clamp(beneficiary / 1000.0 * 100);
        double sAudit = switch (p.getPublicStatus() == null ? "" : p.getPublicStatus()) {
            case "已通过" -> 100;
            case "待审核" -> 30;
            default -> 0;
        };

        List<Map<String, Object>> factors = new ArrayList<>();
        factors.add(factor("目标金额", fmt(target) + " 元", sTarget, rule.getTargetWeight(), "目标金额越大，公开示范价值越高"));
        factors.add(factor("已登记金额", fmt(raised) + " 元", sAmount, rule.getAmountWeight(), "已核对金额 / 目标金额"));
        factors.add(factor("里程碑完成度", String.format("%.0f%%（%d/%d 个）", msRate, ms.stream().filter(m -> "已完成".equals(m.getStatus())).count(), ms.size()),
                sMs, rule.getMilestoneWeight(), "已完成里程碑权重占比"));
        factors.add(factor("支出凭证", vouchers + " 份", sVoucher, rule.getVoucherWeight(), "凭证份数反映执行透明度"));
        factors.add(factor("受益人数", beneficiary + " 人", sBen, rule.getBeneficiaryWeight(), "受益人数体现社会效益"));
        factors.add(factor("公开审核状态", p.getPublicStatus(), sAudit, rule.getAuditWeight(), "进展公示需通过审核"));

        double total = 0;
        for (Map<String, Object> f : factors) {
            total += ((Double) f.get("score")) * ((Integer) f.get("weight")) / 100.0;
        }
        total = round1(total);
        String level = total >= (rule.getGoodScore() == null ? 80 : rule.getGoodScore()) ? "推荐"
                : (total >= (rule.getPassScore() == null ? 60 : rule.getPassScore()) ? "观察" : "不推荐");

        // 主要影响因素 = 加权分最高的一项
        Map<String, Object> top = factors.stream()
                .max(Comparator.comparingDouble(f -> ((Double) f.get("weighted")))).orElse(factors.get(0));
        List<String> unmet = new ArrayList<>();
        if (sAmount < 60) unmet.add("已登记金额仅达目标的 " + round1(sAmount) + "%，低于 60% 的推荐门槛");
        if (sMs < 80) unmet.add("里程碑完成度 " + round1(sMs) + "%，未达到 80%");
        if (sVoucher < 60) unmet.add("支出凭证仅 " + vouchers + " 份，得分 " + round1(sVoucher));
        if (sAudit < 100) unmet.add("项目进展公示尚未通过审核");
        List<String> improve = new ArrayList<>();
        if (sAmount < 80) improve.add("继续推动募捐，距目标还差 " + fmt(Math.max(0, target - raised)) + " 元");
        if (sMs < 80) improve.add("加快未完成里程碑的实施与验收");
        if (sVoucher < 80) improve.add("补充支出凭证并完成归档");
        if (sBen < 60) improve.add("完善受益人数统计口径并回填");
        if (improve.isEmpty()) improve.add("保持当前执行节奏，按期完成结项");

        String snapshot = String.format(Locale.ROOT,
                "{\"target\":%.2f,\"raised\":%.2f,\"milestoneRate\":%.2f,\"voucherCount\":%d,\"beneficiary\":%d,\"publicStatus\":\"%s\"}",
                target, raised, msRate, vouchers, beneficiary, p.getPublicStatus());

        AlumniProjectScore s = new AlumniProjectScore();
        s.setProjectId(projectId);
        s.setProjectName(p.getProjectName());
        s.setRuleId(rule.getId());
        s.setRuleVersion(rule.getVersion());
        s.setInputSnapshot(snapshot);
        s.setTargetScore(bd(sTarget));
        s.setAmountScore(bd(sAmount));
        s.setMilestoneScore(bd(sMs));
        s.setVoucherScore(bd(sVoucher));
        s.setBeneficiaryScore(bd(sBen));
        s.setAuditScore(bd(sAudit));
        s.setTotalScore(bd(total));
        s.setResultLevel(level);
        s.setExplanation("权重最高的影响因素为" + top.get("name") + "（" + top.get("input") + "，得分 "
                + top.get("score") + "，加权 " + top.get("weighted") + " 分）；综合得分 " + total + "，判定为「" + level + "」。");
        s.setUnmetConditions(unmet.isEmpty() ? "各项条件均已满足" : String.join("；", unmet));
        s.setImproveItems(String.join("；", improve));
        s.setCalcTime(LocalDateTime.now());
        s.setCalcUser(UserContext.name());
        s.setCreateTime(LocalDateTime.now());
        mapper.insert(s);

        DonationProject up = new DonationProject();
        up.setId(projectId);
        up.setMilestoneRate(bd(msRate));
        up.setRuleVersion(rule.getVersion());
        up.setUpdateTime(LocalDateTime.now());
        projectMapper.updateById(up);

        Map<String, Object> out = new LinkedHashMap<>();
        out.put("score", s);
        out.put("factors", factors);
        out.put("level", level);
        return R.ok(out);
    }

    private Map<String, Object> factor(String name, String input, double score, Integer weight, String note) {
        Map<String, Object> m = new LinkedHashMap<>();
        m.put("name", name);
        m.put("input", input);
        m.put("score", round1(score));
        m.put("weight", weight == null ? 0 : weight);
        m.put("weighted", round1(score * (weight == null ? 0 : weight) / 100.0));
        m.put("note", note);
        return m;
    }

    private double clamp(double v) { return Math.max(0, Math.min(100, v)); }

    private double round1(double v) { return BigDecimal.valueOf(v).setScale(1, RoundingMode.HALF_UP).doubleValue(); }

    private BigDecimal bd(double v) { return BigDecimal.valueOf(v).setScale(1, RoundingMode.HALF_UP); }

    private String fmt(double v) { return String.format("%,.0f", v); }

    /** 人工修正：必须填写原因（≥5 字），原始计算结果保持不变 */
    @PostMapping("/{id}/manual")
    public R<Void> manual(@PathVariable Long id, @RequestBody Map<String, String> body) {
        AlumniProjectScore s = mapper.selectById(id);
        if (s == null) throw new BizException("计算记录不存在");
        String level = body.getOrDefault("level", "");
        String reason = body.getOrDefault("reason", "").trim();
        if (!List.of("推荐", "观察", "不推荐").contains(level)) throw new BizException("修正等级不合法");
        if (reason.length() < 5) throw new BizException("人工修正必须填写原因，且不少于 5 个字");
        AlumniProjectScore up = new AlumniProjectScore();
        up.setId(id);
        up.setManualLevel(level);
        up.setManualReason(reason);
        up.setManualUser(UserContext.name());
        up.setManualTime(LocalDateTime.now());
        mapper.updateById(up);
        return R.ok();
    }

    /** 效果统计：推荐采纳率、人工调整率、等级分布，用于验证创新模块是否有效 */
    @GetMapping("/effect")
    public R<Map<String, Object>> effect() {
        List<AlumniProjectScore> all = mapper.selectList(new QueryWrapper<>());
        long total = all.size();
        long recommend = all.stream().filter(s -> "推荐".equals(s.getResultLevel())).count();
        long manual = all.stream().filter(s -> s.getManualLevel() != null).count();
        double avg = all.stream().mapToDouble(s -> s.getTotalScore() == null ? 0 : s.getTotalScore().doubleValue())
                .average().orElse(0);
        Map<String, Long> dist = new LinkedHashMap<>();
        for (String k : List.of("推荐", "观察", "不推荐")) {
            dist.put(k, all.stream().filter(s -> k.equals(s.getResultLevel())).count());
        }
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("total", total);
        out.put("recommendCount", recommend);
        out.put("manualCount", manual);
        out.put("avgScore", round1(avg));
        out.put("adoptionRate", total == 0 ? 0 : round1((total - manual) * 100.0 / total));
        out.put("manualRate", total == 0 ? 0 : round1(manual * 100.0 / total));
        out.put("distribution", dist);
        return R.ok(out);
    }
}
