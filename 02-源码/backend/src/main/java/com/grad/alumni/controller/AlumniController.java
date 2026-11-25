package com.grad.alumni.controller;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.grad.alumni.common.*;
import com.grad.alumni.entity.AlumniProfile;
import com.grad.alumni.mapper.AlumniProfileMapper;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.*;

/** 校友档案：认证申请与审核、隐私选项、本人档案查询 */
@RestController
@RequestMapping("/api/alumni")
public class AlumniController extends BaseController<AlumniProfile> {

    private final AlumniProfileMapper mapper;

    public AlumniController(AlumniProfileMapper mapper) { this.mapper = mapper; }

    @Override
    protected BaseMapper<AlumniProfile> mapper() { return mapper; }

    @Override
    protected String kwColumn() { return "real_name"; }

    @Override
    protected String statusColumn() { return "cert_status"; }

    @Override
    protected Map<String, String> extraFilters() {
        return Map.of("college", "college", "graduateYear", "graduate_year", "regionName", "region_name");
    }

    /** 校友提交认证申请：同一学号不可重复提交 */
    @PostMapping("/apply")
    public R<AlumniProfile> apply(@RequestBody AlumniProfile body) {
        if (body.getStudentNo() == null || body.getStudentNo().isBlank()) throw new BizException("学号不能为空");
        if (body.getRealName() == null || body.getRealName().isBlank()) throw new BizException("姓名不能为空");
        Long dup = mapper.selectCount(new QueryWrapper<AlumniProfile>()
                .eq("student_no", body.getStudentNo().trim()).ne("cert_status", "已驳回"));
        if (dup != null && dup > 0) throw new BizException("该学号已提交过认证申请，请等待审核");
        body.setAlumniNo(nextNo("A" + (body.getEnrollYear() == null ? "" : body.getEnrollYear())));
        body.setStudentNo(body.getStudentNo().trim());
        body.setRealName(body.getRealName().trim());
        body.setCertStatus("待审核");
        body.setUserId(UserContext.userId());
        body.setPrivacyLevel("PUBLIC");
        body.setShowPhone(1);
        body.setShowEmail(1);
        body.setShowUnit(1);
        body.setShowRegion(1);
        body.setDeleted(0);
        body.setCreateTime(LocalDateTime.now());
        body.setUpdateTime(LocalDateTime.now());
        mapper.insert(body);
        return R.ok(body);
    }

    /** 认证审核：待审核 -> 已认证 / 已驳回；驳回必须填写原因（≥5 字） */
    @PostMapping("/{id}/audit")
    public R<Void> audit(@PathVariable Long id, @RequestBody Map<String, String> body) {
        if (!UserContext.isAdmin()) throw new BizException(403, "只有校友办管理员可以审核认证");
        String status = body.getOrDefault("status", "");
        String remark = body.getOrDefault("remark", "").trim();
        if (!"已认证".equals(status) && !"已驳回".equals(status)) throw new BizException("审核结果不合法");
        if ("已驳回".equals(status) && remark.length() < 5) throw new BizException("驳回原因不少于 5 个字");
        AlumniProfile p = new AlumniProfile();
        p.setId(id);
        p.setCertStatus(status);
        p.setCertRemark(remark.isEmpty() ? "材料齐全，审核通过" : remark);
        p.setAuditUser(UserContext.name());
        p.setAuditTime(LocalDateTime.now());
        p.setUpdateTime(LocalDateTime.now());
        mapper.updateById(p);
        return R.ok();
    }

    /** 本人档案：未提交认证时返回 null，前端引导去申请 */
    @GetMapping("/me")
    public R<AlumniProfile> me() {
        AlumniProfile p = mapper.selectOne(new QueryWrapper<AlumniProfile>()
                .eq("user_id", UserContext.userId()).orderByDesc("id").last("limit 1"));
        return R.ok(p);
    }

    /** 隐私选项：关闭后公开端不展示对应字段 */
    @PostMapping("/{id}/privacy")
    public R<Void> privacy(@PathVariable Long id, @RequestBody Map<String, Integer> body) {
        AlumniProfile p = new AlumniProfile();
        p.setId(id);
        p.setShowPhone(body.getOrDefault("showPhone", 1));
        p.setShowEmail(body.getOrDefault("showEmail", 1));
        p.setShowUnit(body.getOrDefault("showUnit", 1));
        p.setShowRegion(body.getOrDefault("showRegion", 1));
        p.setUpdateTime(LocalDateTime.now());
        mapper.updateById(p);
        return R.ok();
    }

    /** 按院系统计（看板用）：已认证人数 */
    @GetMapping("/stats/college")
    public R<List<Map<String, Object>>> collegeStats() {
        List<Map<String, Object>> out = new ArrayList<>();
        List<AlumniProfile> all = mapper.selectList(new QueryWrapper<AlumniProfile>().eq("cert_status", "已认证"));
        Map<String, Integer> cnt = new LinkedHashMap<>();
        all.forEach(a -> cnt.merge(a.getCollege() == null ? "未填写" : a.getCollege(), 1, Integer::sum));
        cnt.forEach((k, v) -> {
            Map<String, Object> m = new LinkedHashMap<>();
            m.put("name", k);
            m.put("value", v);
            out.add(m);
        });
        return R.ok(out);
    }
}
