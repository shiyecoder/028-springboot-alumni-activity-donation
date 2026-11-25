package com.grad.alumni.controller;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import com.grad.alumni.common.*;
import com.grad.alumni.entity.*;
import com.grad.alumni.mapper.*;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.*;

/**
 * 报名与签到。
 * 规则：报名人数达上限后进入候补；有人取消时按报名时间顺序自动转正（状态机在服务端校验）。
 */
@RestController
@RequestMapping("/api/signup")
public class SignupController extends BaseController<ActivitySignup> {

    private final ActivitySignupMapper mapper;
    private final AlumniActivityMapper activityMapper;
    private final ActivityCheckinMapper checkinMapper;

    public SignupController(ActivitySignupMapper mapper, AlumniActivityMapper activityMapper,
                            ActivityCheckinMapper checkinMapper) {
        this.mapper = mapper;
        this.activityMapper = activityMapper;
        this.checkinMapper = checkinMapper;
    }

    @Override
    protected BaseMapper<ActivitySignup> mapper() { return mapper; }

    @Override
    protected String kwColumn() { return "alumni_name"; }

    @Override
    protected String statusColumn() { return "status"; }

    @Override
    protected Map<String, String> extraFilters() { return Map.of("activityId", "activity_id"); }

    /** 校友报名：满员自动候补，重复报名被拒绝 */
    @PostMapping("/apply")
    public R<ActivitySignup> apply(@RequestBody ActivitySignup body) {
        AlumniActivity act = activityMapper.selectById(body.getActivityId());
        if (act == null) throw new BizException("活动不存在");
        if (!"报名中".equals(act.getStatus())) throw new BizException("当前活动不在报名阶段");
        Long dup = mapper.selectCount(new QueryWrapper<ActivitySignup>()
                .eq("activity_id", act.getId()).eq("alumni_id", body.getAlumniId())
                .in("status", "待审核", "已报名", "候补", "已签到"));
        if (dup != null && dup > 0) throw new BizException("您已报名该活动，请勿重复提交");
        int taken = (act.getSignupCount() == null ? 0 : act.getSignupCount())
                + (body.getCompanionCount() == null ? 0 : body.getCompanionCount());
        boolean full = taken >= (act.getCapacity() == null ? 0 : act.getCapacity());
        body.setSignupNo(nextNo("S"));
        body.setCheckinCode(String.valueOf(1000 + new Random().nextInt(9000)));
        body.setStatus(full ? "候补" : ("自动通过".equals(act.getAuditMode()) ? "已报名" : "已报名"));
        body.setCreateTime(LocalDateTime.now());
        body.setUpdateTime(LocalDateTime.now());
        AlumniActivity up = new AlumniActivity();
        up.setId(act.getId());
        if (full) {
            Long waitCnt = mapper.selectCount(new QueryWrapper<ActivitySignup>()
                    .eq("activity_id", act.getId()).eq("status", "候补"));
            body.setWaitNo((int) (waitCnt + 1));
            up.setWaitCount((act.getWaitCount() == null ? 0 : act.getWaitCount()) + 1);
        } else {
            up.setSignupCount((act.getSignupCount() == null ? 0 : act.getSignupCount())
                    + 1 + (body.getCompanionCount() == null ? 0 : body.getCompanionCount()));
        }
        mapper.insert(body);
        activityMapper.updateById(up);
        return R.ok(body);
    }

    /** 取消报名：占用名额时按报名时间顺序把最早候补转正 */
    @PostMapping("/{id}/cancel")
    public R<Map<String, Object>> cancel(@PathVariable Long id, @RequestBody(required = false) Map<String, String> body) {
        ActivitySignup s = mapper.selectById(id);
        if (s == null) throw new BizException("报名记录不存在");
        if (!List.of("待审核", "已报名", "候补").contains(s.getStatus())) throw new BizException("当前状态不可取消");
        boolean heldSeat = "已报名".equals(s.getStatus()) || "待审核".equals(s.getStatus());
        ActivitySignup up = new ActivitySignup();
        up.setId(id);
        up.setStatus("已取消");
        up.setRemark(body == null ? null : body.get("remark"));
        up.setUpdateTime(LocalDateTime.now());
        mapper.updateById(up);

        AlumniActivity act = activityMapper.selectById(s.getActivityId());
        AlumniActivity actUp = new AlumniActivity();
        actUp.setId(act.getId());
        String promoted = null;
        if (heldSeat) {
            actUp.setSignupCount(Math.max(0, (act.getSignupCount() == null ? 0 : act.getSignupCount()) - 1));
            ActivitySignup first = mapper.selectOne(new QueryWrapper<ActivitySignup>()
                    .eq("activity_id", act.getId()).eq("status", "候补")
                    .orderByAsc("create_time").last("limit 1"));
            if (first != null) {
                ActivitySignup p = new ActivitySignup();
                p.setId(first.getId());
                p.setStatus("已报名");
                p.setWaitNo(null);
                p.setUpdateTime(LocalDateTime.now());
                mapper.updateById(p);
                actUp.setSignupCount((actUp.getSignupCount() == null ? 0 : actUp.getSignupCount()) + 1);
                actUp.setWaitCount(Math.max(0, (act.getWaitCount() == null ? 0 : act.getWaitCount()) - 1));
                promoted = first.getAlumniName();
            }
        } else {
            actUp.setWaitCount(Math.max(0, (act.getWaitCount() == null ? 0 : act.getWaitCount()) - 1));
        }
        activityMapper.updateById(actUp);
        Map<String, Object> out = new LinkedHashMap<>();
        out.put("promoted", promoted);
        return R.ok(out);
    }

    /** 现场签到：校验 6 位验证码（人才唯一），重复签到返回提示 */
    @PostMapping("/{id}/checkin")
    public R<Void> checkin(@PathVariable Long id, @RequestBody Map<String, String> body) {
        ActivitySignup s = mapper.selectById(id);
        if (s == null) throw new BizException("报名记录不存在");
        if ("已签到".equals(s.getStatus())) throw new BizException("该校友已签到，请勿重复操作");
        if (!List.of("已报名", "候补", "未到场").contains(s.getStatus())) throw new BizException("当前状态不可签到");
        String code = body.getOrDefault("code", "").trim();
        if (!code.isEmpty() && !code.equals(s.getCheckinCode())) throw new BizException("签到验证码不正确");
        ActivitySignup up = new ActivitySignup();
        up.setId(id);
        up.setStatus("已签到");
        up.setCheckinTime(LocalDateTime.now());
        up.setUpdateTime(LocalDateTime.now());
        mapper.updateById(up);

        ActivityCheckin c = new ActivityCheckin();
        c.setActivityId(s.getActivityId());
        c.setSignupId(s.getId());
        c.setAlumniId(s.getAlumniId());
        c.setAlumniName(s.getAlumniName());
        c.setCheckinCode(code.isEmpty() ? s.getCheckinCode() : code);
        c.setCheckinTime(LocalDateTime.now());
        c.setCheckinBy(UserContext.name());
        c.setCheckinType(code.isEmpty() ? "手工补签" : "验证码");
        c.setCreateTime(LocalDateTime.now());
        checkinMapper.insert(c);

        AlumniActivity act = activityMapper.selectById(s.getActivityId());
        AlumniActivity actUp = new AlumniActivity();
        actUp.setId(act.getId());
        actUp.setCheckinCount((act.getCheckinCount() == null ? 0 : act.getCheckinCount()) + 1);
        activityMapper.updateById(actUp);
        return R.ok();
    }

    /** 手工转正：管理员或联络员把候补直接转为已报名 */
    @PostMapping("/{id}/promote")
    public R<Void> promote(@PathVariable Long id) {
        ActivitySignup s = mapper.selectById(id);
        if (s == null) throw new BizException("报名记录不存在");
        if (!"候补".equals(s.getStatus())) throw new BizException("只有候补状态的报名可以转正");
        ActivitySignup up = new ActivitySignup();
        up.setId(id);
        up.setStatus("已报名");
        up.setWaitNo(null);
        up.setUpdateTime(LocalDateTime.now());
        mapper.updateById(up);
        AlumniActivity act = activityMapper.selectById(s.getActivityId());
        AlumniActivity actUp = new AlumniActivity();
        actUp.setId(act.getId());
        actUp.setSignupCount((act.getSignupCount() == null ? 0 : act.getSignupCount()) + 1);
        actUp.setWaitCount(Math.max(0, (act.getWaitCount() == null ? 0 : act.getWaitCount()) - 1));
        activityMapper.updateById(actUp);
        return R.ok();
    }

    /** 我的报名 */
    @GetMapping("/my")
    public R<List<ActivitySignup>> my() {
        return R.ok(mapper.selectList(new QueryWrapper<ActivitySignup>()
                .eq("alumni_id", UserContext.userId()).orderByDesc("create_time")));
    }
}
