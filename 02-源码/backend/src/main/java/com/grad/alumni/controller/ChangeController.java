package com.grad.alumni.controller;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.grad.alumni.common.*;
import com.grad.alumni.entity.AlumniChangeRequest;
import com.grad.alumni.entity.AlumniProfile;
import com.grad.alumni.mapper.AlumniChangeRequestMapper;
import com.grad.alumni.mapper.AlumniProfileMapper;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.Map;

/** 校友信息变更：保留历史值，审核通过后写回档案 */
@RestController
@RequestMapping("/api/change")
public class ChangeController extends BaseController<AlumniChangeRequest> {

    private final AlumniChangeRequestMapper mapper;
    private final AlumniProfileMapper profileMapper;

    public ChangeController(AlumniChangeRequestMapper mapper, AlumniProfileMapper profileMapper) {
        this.mapper = mapper;
        this.profileMapper = profileMapper;
    }

    @Override
    protected BaseMapper<AlumniChangeRequest> mapper() { return mapper; }

    @Override
    protected String kwColumn() { return "alumni_name"; }

    @Override
    protected String statusColumn() { return "audit_status"; }

    /** 校友提交变更申请：记录变更前后值，便于留痕 */
    @PostMapping("/apply")
    public R<AlumniChangeRequest> apply(@RequestBody AlumniChangeRequest body) {
        if (body.getAlumniId() == null) throw new BizException("校友档案不能为空");
        if (body.getNewValue() == null || body.getNewValue().isBlank()) throw new BizException("变更后的值不能为空");
        AlumniProfile p = profileMapper.selectById(body.getAlumniId());
        if (p == null) throw new BizException("校友档案不存在");
        body.setAlumniName(p.getRealName());
        body.setAuditStatus("待审核");
        body.setCreateTime(LocalDateTime.now());
        mapper.insert(body);
        return R.ok(body);
    }

    /** 审核：通过后写回档案；退回必须填写原因（≥5 字） */
    @PostMapping("/{id}/audit")
    public R<Void> audit(@PathVariable Long id, @RequestBody Map<String, String> body) {
        if (!UserContext.isAdmin()) throw new BizException(403, "只有校友办管理员可以审核变更");
        String status = body.getOrDefault("status", "");
        String remark = body.getOrDefault("remark", "").trim();
        if (!"已通过".equals(status) && !"已退回".equals(status)) throw new BizException("审核结果不合法");
        if ("已退回".equals(status) && remark.length() < 5) throw new BizException("退回原因不少于 5 个字");
        AlumniChangeRequest req = mapper.selectById(id);
        if (req == null) throw new BizException("申请不存在");
        if (!"待审核".equals(req.getAuditStatus())) throw new BizException("该申请已处理，不能重复审核");
        req.setAuditStatus(status);
        req.setAuditUser(UserContext.name());
        req.setAuditTime(LocalDateTime.now());
        req.setAuditRemark(remark);
        mapper.updateById(req);
        if ("已通过".equals(status)) {
            AlumniProfile p = new AlumniProfile();
            p.setId(req.getAlumniId());
            p.setUpdateTime(LocalDateTime.now());
            switch (req.getFieldName() == null ? "" : req.getFieldName()) {
                case "工作单位" -> p.setWorkUnit(req.getNewValue());
                case "所在地区" -> p.setRegionName(req.getNewValue());
                case "手机" -> p.setPhone(req.getNewValue());
                case "邮箱" -> p.setEmail(req.getNewValue());
                default -> { }
            }
            profileMapper.updateById(p);
        }
        return R.ok();
    }
}
