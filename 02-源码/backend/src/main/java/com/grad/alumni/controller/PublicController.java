package com.grad.alumni.controller;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.grad.alumni.common.*;
import com.grad.alumni.entity.DonationProject;
import com.grad.alumni.entity.ProjectMilestone;
import com.grad.alumni.entity.ProjectProgress;
import com.grad.alumni.mapper.DonationProjectMapper;
import com.grad.alumni.mapper.ProjectMilestoneMapper;
import com.grad.alumni.mapper.ProjectProgressMapper;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.*;

import java.util.*;

/**
 * 公开端接口（无需登录）：只返回经审核公开的信息。
 * 匿名捐赠在公开端隐藏姓名，仅显示「匿名校友」；未核对捐赠不计入实收。
 */
@RestController
@RequestMapping("/api/public")
public class PublicController {

    private final DonationProjectMapper projectMapper;
    private final ProjectProgressMapper progressMapper;
    private final ProjectMilestoneMapper milestoneMapper;
    private final JdbcTemplate jdbc;

    public PublicController(DonationProjectMapper projectMapper, ProjectProgressMapper progressMapper,
                            ProjectMilestoneMapper milestoneMapper, JdbcTemplate jdbc) {
        this.projectMapper = projectMapper;
        this.progressMapper = progressMapper;
        this.milestoneMapper = milestoneMapper;
        this.jdbc = jdbc;
    }

    @GetMapping("/projects")
    public R<PageResult<DonationProject>> projects(@RequestParam(defaultValue = "1") long page,
                                                   @RequestParam(defaultValue = "9") long size,
                                                   @RequestParam(required = false) String kw) {
        QueryWrapper<DonationProject> q = new QueryWrapper<DonationProject>()
                .eq("public_status", "已通过").eq("public_flag", 1).ne("status", "已取消");
        if (kw != null && !kw.isBlank()) q.like("project_name", kw.trim());
        q.orderByDesc("update_time");
        return R.ok(PageResult.of(projectMapper.selectPage(new Page<>(page, size), q)));
    }

    @GetMapping("/projects/{id}")
    public R<Map<String, Object>> detail(@PathVariable Long id) {
        DonationProject p = projectMapper.selectById(id);
        if (p == null || !"已通过".equals(p.getPublicStatus())) throw new BizException("项目不存在或未公开");
        List<ProjectProgress> progress = progressMapper.selectList(new QueryWrapper<ProjectProgress>()
                .eq("project_id", id).eq("audit_status", "已发布").orderByDesc("publish_time"));
        // 公开端捐赠明细：匿名记录不返回姓名
        List<Map<String, Object>> donors = jdbc.queryForList(
                "SELECT record_no, IF(anonymous_flag=1,'匿名校友',donor_name) AS donorName, donor_type AS donorType, " +
                "amount, donate_date AS donateDate FROM donation_record WHERE project_id=? AND verify_status='已核对' " +
                "AND anonymous_flag=0 ORDER BY donate_date DESC LIMIT 10", id);
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("project", p);
        out.put("progress", progress);
        // 创新模块：执行里程碑对公众开放，展示计划/完成时间与交付物，供捐赠人核对执行进度
        out.put("milestones", milestoneMapper.selectList(new QueryWrapper<ProjectMilestone>()
                .eq("project_id", id).orderByAsc("seq_no")));
        out.put("donors", donors);
        return R.ok(out);
    }

    @GetMapping("/stats")
    public R<Map<String, Object>> stats() {
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("projectCount", jdbc.queryForObject(
                "SELECT COUNT(*) FROM donation_project WHERE public_status='已通过' AND public_flag=1", Long.class));
        out.put("raisedAmount", jdbc.queryForObject(
                "SELECT IFNULL(SUM(raised_amount),0) FROM donation_project WHERE public_status='已通过'", Long.class));
        out.put("donorCount", jdbc.queryForObject(
                "SELECT COUNT(*) FROM donation_record WHERE verify_status='已核对'", Long.class));
        out.put("beneficiary", jdbc.queryForObject(
                "SELECT IFNULL(SUM(beneficiary_count),0) FROM donation_project WHERE public_status='已通过'", Long.class));
        return R.ok(out);
    }
}
