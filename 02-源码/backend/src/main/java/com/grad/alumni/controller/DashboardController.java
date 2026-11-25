package com.grad.alumni.controller;

import com.grad.alumni.common.R;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.*;

/**
 * 校友运营看板：6 项核心指标 + 6 个图表数据，全部由数据库聚合，不在前端二次聚合全表。
 * 点击图表跳转的列表总数与这里返回的统计值一致。
 */
@RestController
@RequestMapping("/api/dashboard")
public class DashboardController {

    private final JdbcTemplate jdbc;

    public DashboardController(JdbcTemplate jdbc) { this.jdbc = jdbc; }

    @GetMapping("/overview")
    public R<Map<String, Object>> overview() {
        Map<String, Object> out = new LinkedHashMap<>();

        Map<String, Object> kpi = new LinkedHashMap<>();
        kpi.put("participants", num("SELECT IFNULL(SUM(signup_count),0) FROM alumni_activity"));
        kpi.put("activityCount", num("SELECT COUNT(*) FROM alumni_activity WHERE status <> '已取消'"));
        kpi.put("projectCount", num("SELECT COUNT(*) FROM donation_project WHERE status <> '已取消'"));
        kpi.put("raisedAmount", num("SELECT IFNULL(SUM(raised_amount),0) FROM donation_project"));
        kpi.put("milestoneRate", num("SELECT IFNULL(ROUND(AVG(milestone_rate),1),0) FROM donation_project WHERE status <> '项目立项'"));
        kpi.put("alumniCount", num("SELECT COUNT(*) FROM alumni_profile WHERE cert_status='已认证' AND deleted=0"));
        kpi.put("activeRate", num("SELECT IFNULL(ROUND(COUNT(DISTINCT s.alumni_id)*100.0/NULLIF((SELECT COUNT(*) FROM alumni_profile WHERE deleted=0),0),1),0) FROM activity_signup s"));
        out.put("kpi", kpi);

        // 捐赠趋势（近 6 个月，按月）
        out.put("trend", jdbc.queryForList(
                "SELECT DATE_FORMAT(create_time,'%Y-%m') AS month, ROUND(SUM(amount)/10000,1) AS amount, COUNT(*) AS cnt " +
                "FROM donation_record WHERE verify_status='已核对' AND create_time >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH) " +
                "GROUP BY month ORDER BY month"));

        // 项目状态分布
        out.put("projectStatus", jdbc.queryForList(
                "SELECT status AS name, COUNT(*) AS value FROM donation_project GROUP BY status ORDER BY value DESC"));

        // 学院贡献分布（按已核对金额）
        out.put("collegeRank", jdbc.queryForList(
                "SELECT p.dept_name AS name, ROUND(SUM(r.amount),2) AS value FROM donation_record r " +
                "JOIN donation_project p ON p.id=r.project_id WHERE r.verify_status='已核对' " +
                "GROUP BY p.dept_name ORDER BY value DESC LIMIT 6"));

        // 活动报名与到场率
        out.put("activityFunnel", jdbc.queryForList(
                "SELECT '报名' AS name, IFNULL(SUM(signup_count),0) AS value FROM alumni_activity " +
                "UNION ALL SELECT '候补', IFNULL(SUM(wait_count),0) FROM alumni_activity " +
                "UNION ALL SELECT '签到', IFNULL(SUM(checkin_count),0) FROM alumni_activity"));

        // 组织活跃度（按成员数）
        out.put("orgRank", jdbc.queryForList(
                "SELECT org_name AS name, member_count AS value FROM alumni_organization " +
                "WHERE deleted=0 ORDER BY member_count DESC LIMIT 6"));

        // 创新模块结果分布
        out.put("scoreDist", jdbc.queryForList(
                "SELECT result_level AS name, COUNT(*) AS value FROM alumni_project_score GROUP BY result_level"));

        // 待办汇总
        Map<String, Object> todo = new LinkedHashMap<>();
        todo.put("certPending", num("SELECT COUNT(*) FROM alumni_profile WHERE cert_status='待审核'"));
        todo.put("changePending", num("SELECT COUNT(*) FROM alumni_change_request WHERE audit_status='待审核'"));
        todo.put("activityPending", num("SELECT COUNT(*) FROM alumni_activity WHERE status='待审核'"));
        todo.put("donationPending", num("SELECT COUNT(*) FROM donation_record WHERE verify_status='待核对'"));
        todo.put("progressPending", num("SELECT COUNT(*) FROM project_progress WHERE audit_status='待审核'"));
        out.put("todo", todo);
        return R.ok(out);
    }

    private long num(String sql) {
        Long v = jdbc.queryForObject(sql, Long.class);
        return v == null ? 0 : v;
    }
}
