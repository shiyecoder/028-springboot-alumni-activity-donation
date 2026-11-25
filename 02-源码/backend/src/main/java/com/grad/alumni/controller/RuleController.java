package com.grad.alumni.controller;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.grad.alumni.common.*;
import com.grad.alumni.entity.AlumniProjectRule;
import com.grad.alumni.mapper.AlumniProjectRuleMapper;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;

/**
 * 创新模块：捐赠目标与执行里程碑公开 —— 权重规则配置。
 * 硬性约束：六项权重合计必须等于 100；每次修改生成新版本并记录生效时间，旧版本置为停用。
 */
@RestController
@RequestMapping("/api/rule")
public class RuleController extends BaseController<AlumniProjectRule> {

    private final AlumniProjectRuleMapper mapper;

    public RuleController(AlumniProjectRuleMapper mapper) { this.mapper = mapper; }

    @Override
    protected BaseMapper<AlumniProjectRule> mapper() { return mapper; }

    @Override
    protected String kwColumn() { return "rule_name"; }

    @Override
    protected String statusColumn() { return "status"; }

    @GetMapping("/active")
    public R<AlumniProjectRule> active() {
        AlumniProjectRule r = mapper.selectOne(new QueryWrapper<AlumniProjectRule>()
                .eq("status", "启用").orderByDesc("effect_time").last("limit 1"));
        if (r == null) throw new BizException("尚未配置启用中的规则");
        return R.ok(r);
    }

    @GetMapping("/list")
    public R<List<AlumniProjectRule>> list() {
        return R.ok(mapper.selectList(new QueryWrapper<AlumniProjectRule>().orderByDesc("effect_time")));
    }

    /** 保存规则：校验权重合计 100%，生成新版本号并停用旧版本 */
    @PostMapping("/save")
    public R<AlumniProjectRule> save(@RequestBody AlumniProjectRule body) {
        int sum = n(body.getTargetWeight()) + n(body.getAmountWeight()) + n(body.getMilestoneWeight())
                + n(body.getVoucherWeight()) + n(body.getBeneficiaryWeight()) + n(body.getAuditWeight());
        if (sum != 100) throw new BizException("权重合计必须等于 100%，当前为 " + sum + "%");
        for (int w : new int[]{n(body.getTargetWeight()), n(body.getAmountWeight()), n(body.getMilestoneWeight()),
                n(body.getVoucherWeight()), n(body.getBeneficiaryWeight()), n(body.getAuditWeight())}) {
            if (w < 0 || w > 100) throw new BizException("单项权重必须在 0~100 之间");
        }
        List<AlumniProjectRule> olds = mapper.selectList(new QueryWrapper<AlumniProjectRule>().eq("status", "启用"));
        int maxVersion = 0;
        for (AlumniProjectRule r : mapper.selectList(null)) {
            String v = r.getVersion() == null ? "v0" : r.getVersion().replace("v", "");
            try { maxVersion = Math.max(maxVersion, Integer.parseInt(v)); } catch (Exception ignored) { }
        }
        for (AlumniProjectRule old : olds) {
            AlumniProjectRule off = new AlumniProjectRule();
            off.setId(old.getId());
            off.setStatus("停用");
            mapper.updateById(off);
        }
        body.setId(null);
        body.setVersion("v" + (maxVersion + 1));
        body.setStatus("启用");
        body.setEffectTime(LocalDateTime.now());
        body.setCreateUser(UserContext.name());
        body.setCreateTime(LocalDateTime.now());
        body.setRuleName(body.getRuleName() == null ? "捐赠目标与执行里程碑公开" : body.getRuleName());
        body.setPassScore(body.getPassScore() == null ? 60 : body.getPassScore());
        body.setGoodScore(body.getGoodScore() == null ? 80 : body.getGoodScore());
        mapper.insert(body);
        return R.ok(body);
    }

    private int n(Integer v) { return v == null ? 0 : v; }
}
