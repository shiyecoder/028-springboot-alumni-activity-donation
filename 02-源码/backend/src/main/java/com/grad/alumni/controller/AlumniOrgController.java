package com.grad.alumni.controller;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.grad.alumni.common.BizException;
import com.grad.alumni.common.R;
import com.grad.alumni.entity.AlumniOrganization;
import com.grad.alumni.entity.OrganizationMember;
import com.grad.alumni.mapper.AlumniOrganizationMapper;
import com.grad.alumni.mapper.OrganizationMemberMapper;
import org.springframework.web.bind.annotation.*;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/** 校友组织（地方校友会 / 行业俱乐部 / 院系校友会）：组织档案与成员明细 */
@RestController
@RequestMapping("/api/alumni-org")
public class AlumniOrgController extends BaseController<AlumniOrganization> {

    private final AlumniOrganizationMapper mapper;
    private final OrganizationMemberMapper memberMapper;

    public AlumniOrgController(AlumniOrganizationMapper mapper, OrganizationMemberMapper memberMapper) {
        this.mapper = mapper;
        this.memberMapper = memberMapper;
    }

    @Override
    protected BaseMapper<AlumniOrganization> mapper() { return mapper; }

    @Override
    protected String kwColumn() { return "org_name"; }

    @Override
    protected String statusColumn() { return "status"; }

    @Override
    protected Map<String, String> extraFilters() {
        return Map.of("orgType", "org_type", "college", "college", "regionName", "region_name");
    }

    /** 组织详情：档案 + 成员构成（按角色/状态分组） */
    @GetMapping("/{id}/detail")
    public R<Map<String, Object>> detailAll(@PathVariable Long id) {
        AlumniOrganization org = mapper.selectById(id);
        if (org == null) throw new BizException("组织不存在");
        List<OrganizationMember> members = memberMapper.selectList(new QueryWrapper<OrganizationMember>()
                .eq("org_id", id).orderByAsc("create_time"));
        Map<String, Integer> byStatus = new LinkedHashMap<>();
        for (OrganizationMember m : members) {
            byStatus.merge(m.getJoinStatus(), 1, Integer::sum);
        }
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("org", org);
        out.put("members", members);
        out.put("memberStats", byStatus);
        return R.ok(out);
    }
}
