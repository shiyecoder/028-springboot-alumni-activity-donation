package com.grad.alumni.controller;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.grad.alumni.common.*;
import com.grad.alumni.entity.AlumniOrganization;
import com.grad.alumni.entity.OrganizationMember;
import com.grad.alumni.mapper.AlumniOrganizationMapper;
import com.grad.alumni.mapper.OrganizationMemberMapper;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.Map;

/** 组织成员：通过入会申请后累加组织成员数 */
@RestController
@RequestMapping("/api/member")
public class MemberController extends BaseController<OrganizationMember> {

    private final OrganizationMemberMapper mapper;
    private final AlumniOrganizationMapper orgMapper;

    public MemberController(OrganizationMemberMapper mapper, AlumniOrganizationMapper orgMapper) {
        this.mapper = mapper;
        this.orgMapper = orgMapper;
    }

    @Override
    protected BaseMapper<OrganizationMember> mapper() { return mapper; }

    @Override
    protected String kwColumn() { return "alumni_name"; }

    @Override
    protected String statusColumn() { return "join_status"; }

    @PostMapping("/{id}/audit")
    public R<Void> audit(@PathVariable Long id, @RequestBody Map<String, String> body) {
        String status = body.getOrDefault("status", "");
        if (!"已通过".equals(status) && !"已退出".equals(status)) throw new BizException("审核结果不合法");
        OrganizationMember m = mapper.selectById(id);
        if (m == null) throw new BizException("申请不存在");
        if (!"待审核".equals(m.getJoinStatus())) throw new BizException("该申请已处理");
        m.setJoinStatus(status);
        m.setAuditUser(UserContext.name());
        m.setAuditTime(LocalDateTime.now());
        mapper.updateById(m);
        if ("已通过".equals(status)) {
            AlumniOrganization org = orgMapper.selectById(m.getOrgId());
            if (org != null) {
                AlumniOrganization up = new AlumniOrganization();
                up.setId(org.getId());
                up.setMemberCount((org.getMemberCount() == null ? 0 : org.getMemberCount()) + 1);
                up.setUpdateTime(LocalDateTime.now());
                orgMapper.updateById(up);
            }
        }
        return R.ok();
    }
}
