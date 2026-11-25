package com.grad.alumni.controller;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.grad.alumni.common.*;
import com.grad.alumni.entity.DonationProject;
import com.grad.alumni.entity.DonationRecord;
import com.grad.alumni.entity.ThankCertificate;
import com.grad.alumni.mapper.DonationProjectMapper;
import com.grad.alumni.mapper.DonationRecordMapper;
import com.grad.alumni.mapper.ThankCertificateMapper;
import org.springframework.web.bind.annotation.*;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.*;

/**
 * 线下捐赠登记与财务核对。
 * 关键规则：未经财务核对（verify_status=已核对）的捐赠不计入项目实收、不生成证书；
 * 核对通过后按已核对金额重算项目 raised_amount，保证统计与明细一致。
 */
@RestController
@RequestMapping("/api/donation")
public class DonationController extends BaseController<DonationRecord> {

    private final DonationRecordMapper mapper;
    private final DonationProjectMapper projectMapper;
    private final ThankCertificateMapper certMapper;

    public DonationController(DonationRecordMapper mapper, DonationProjectMapper projectMapper,
                              ThankCertificateMapper certMapper) {
        this.mapper = mapper;
        this.projectMapper = projectMapper;
        this.certMapper = certMapper;
    }

    @Override
    protected BaseMapper<DonationRecord> mapper() { return mapper; }

    @Override
    protected String kwColumn() { return "donor_name"; }

    @Override
    protected String statusColumn() { return "verify_status"; }

    @Override
    protected Map<String, String> extraFilters() {
        return Map.of("projectId", "project_id", "donorType", "donor_type");
    }

    @Override
    protected void beforeSave(DonationRecord body, boolean create) {
        if (create) {
            if (body.getProjectId() == null) throw new BizException("意向项目不能为空");
            if (body.getDonorName() == null || body.getDonorName().isBlank()) throw new BizException("捐赠人不能为空");
            if (body.getAmount() == null || body.getAmount().signum() < 0) throw new BizException("金额不能为负数");
            DonationProject p = projectMapper.selectById(body.getProjectId());
            if (p == null) throw new BizException("意向项目不存在");
            body.setProjectName(p.getProjectName());
            body.setRecordNo(nextNo("DN"));
            body.setVerifyStatus("待核对");
            body.setReceiptStatus("未开具");
            body.setDonateDate(body.getDonateDate() == null ? LocalDate.now() : body.getDonateDate());
            body.setCreateTime(LocalDateTime.now());
        }
        body.setUpdateTime(LocalDateTime.now());
    }

    /** 财务核对：已核对计入实收并重算项目金额；退回必须填写原因（≥5 字） */
    @PostMapping("/{id}/verify")
    public R<Map<String, Object>> verify(@PathVariable Long id, @RequestBody Map<String, String> body) {
        if (!UserContext.isFinance() && !UserContext.isAdmin()) {
            throw new BizException(403, "只有财务登记员可以核对捐赠");
        }
        DonationRecord r = mapper.selectById(id);
        if (r == null) throw new BizException("登记记录不存在");
        if (!"待核对".equals(r.getVerifyStatus())) throw new BizException("该记录已核对，不能重复操作");
        String status = body.getOrDefault("status", "");
        String remark = body.getOrDefault("remark", "").trim();
        if (!"已核对".equals(status) && !"已退回".equals(status)) throw new BizException("核对结果不合法");
        if ("已退回".equals(status) && remark.length() < 5) throw new BizException("退回原因不少于 5 个字");
        if ("已核对".equals(status) && (r.getVoucherPath() == null || r.getVoucherPath().isBlank())) {
            throw new BizException("未上传凭证的捐赠不能通过核对，请退回补充凭证");
        }
        DonationRecord up = new DonationRecord();
        up.setId(id);
        up.setVerifyStatus(status);
        up.setVerifyUser(UserContext.name());
        up.setVerifyTime(LocalDateTime.now());
        up.setVerifyRemark(remark);
        if ("已核对".equals(status)) up.setReceiptStatus(r.getAmount().compareTo(BigDecimal.valueOf(10000)) >= 0 ? "已开具" : "未开具");
        mapper.updateById(up);

        BigDecimal raised = recompute(r.getProjectId());
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("projectRaised", raised);
        return R.ok(out);
    }

    /** 按已核对明细重算项目实收与资金完成度 */
    private BigDecimal recompute(Long projectId) {
        List<DonationRecord> verified = mapper.selectList(new QueryWrapper<DonationRecord>()
                .eq("project_id", projectId).eq("verify_status", "已核对"));
        BigDecimal sum = verified.stream().map(DonationRecord::getAmount)
                .filter(Objects::nonNull).reduce(BigDecimal.ZERO, BigDecimal::add);
        DonationProject p = projectMapper.selectById(projectId);
        DonationProject up = new DonationProject();
        up.setId(projectId);
        up.setRaisedAmount(sum);
        if (p.getTargetAmount() != null && p.getTargetAmount().signum() > 0) {
            up.setProgressRate(sum.multiply(BigDecimal.valueOf(100))
                    .divide(p.getTargetAmount(), 2, java.math.RoundingMode.HALF_UP));
        }
        up.setUpdateTime(LocalDateTime.now());
        projectMapper.updateById(up);
        return sum;
    }

    /** 生成感谢证书：仅已核对且勾选开证明的记录；匿名捐赠对外显示「匿名校友」 */
    @PostMapping("/{id}/certificate")
    public R<ThankCertificate> issueCert(@PathVariable Long id) {
        DonationRecord r = mapper.selectById(id);
        if (r == null) throw new BizException("登记记录不存在");
        if (!"已核对".equals(r.getVerifyStatus())) throw new BizException("未通过财务核对的捐赠不能生成证书");
        if (r.getCertFlag() == null || r.getCertFlag() == 0) throw new BizException("该捐赠未申请开具证明");
        Long exist = certMapper.selectCount(new QueryWrapper<ThankCertificate>().eq("record_id", id));
        if (exist != null && exist > 0) throw new BizException("该捐赠已生成过证书");
        ThankCertificate c = new ThankCertificate();
        c.setCertNo(nextNo("TC"));
        c.setRecordId(r.getId());
        c.setRecordNo(r.getRecordNo());
        c.setProjectId(r.getProjectId());
        c.setProjectName(r.getProjectName());
        c.setDonorName(r.getAnonymousFlag() != null && r.getAnonymousFlag() == 1 ? "匿名校友" : r.getDonorName());
        c.setDonorAlumniId(r.getAnonymousFlag() != null && r.getAnonymousFlag() == 1 ? null : r.getDonorAlumniId());
        c.setAmount(r.getAmount());
        c.setIssueDate(LocalDate.now());
        c.setIssueUser(UserContext.name());
        c.setSendStatus("待发放");
        c.setCreateTime(LocalDateTime.now());
        certMapper.insert(c);
        return R.ok(c);
    }

    /** 项目捐赠汇总：已核对金额、笔数、待核对笔数 */
    @GetMapping("/summary/{projectId}")
    public R<Map<String, Object>> summary(@PathVariable Long projectId) {
        List<DonationRecord> all = mapper.selectList(new QueryWrapper<DonationRecord>().eq("project_id", projectId));
        BigDecimal verified = all.stream().filter(x -> "已核对".equals(x.getVerifyStatus()))
                .map(DonationRecord::getAmount).filter(Objects::nonNull)
                .reduce(BigDecimal.ZERO, BigDecimal::add);
        long pending = all.stream().filter(x -> "待核对".equals(x.getVerifyStatus())).count();
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("total", all.size());
        out.put("verifiedAmount", verified);
        out.put("pendingCount", pending);
        return R.ok(out);
    }
}
