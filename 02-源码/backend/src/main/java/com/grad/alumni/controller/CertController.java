package com.grad.alumni.controller;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.grad.alumni.common.*;
import com.grad.alumni.entity.ThankCertificate;
import com.grad.alumni.mapper.ThankCertificateMapper;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.Map;

/** 感谢证书：发放登记与重发 */
@RestController
@RequestMapping("/api/cert")
public class CertController extends BaseController<ThankCertificate> {

    private final ThankCertificateMapper mapper;

    public CertController(ThankCertificateMapper mapper) { this.mapper = mapper; }

    @Override
    protected BaseMapper<ThankCertificate> mapper() { return mapper; }

    @Override
    protected String kwColumn() { return "donor_name"; }

    @Override
    protected String statusColumn() { return "send_status"; }

    @Override
    protected Map<String, String> extraFilters() { return Map.of("donorAlumniId", "donor_alumni_id"); }

    @PostMapping("/{id}/send")
    public R<Void> send(@PathVariable Long id, @RequestBody(required = false) Map<String, String> body) {
        ThankCertificate c = mapper.selectById(id);
        if (c == null) throw new BizException("证书不存在");
        if ("已发放".equals(c.getSendStatus())) throw new BizException("该证书已发放，如需重发请使用重发接口");
        ThankCertificate up = new ThankCertificate();
        up.setId(id);
        up.setSendStatus("已发放");
        up.setSendTime(LocalDateTime.now());
        up.setSendWay(body == null ? "电子邮件" : body.getOrDefault("sendWay", "电子邮件"));
        mapper.updateById(up);
        return R.ok();
    }

    @PostMapping("/{id}/resend")
    public R<Void> resend(@PathVariable Long id) {
        ThankCertificate up = new ThankCertificate();
        up.setId(id);
        up.setSendStatus("已发放");
        up.setSendTime(LocalDateTime.now());
        mapper.updateById(up);
        return R.ok();
    }
}
