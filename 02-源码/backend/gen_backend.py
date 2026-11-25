#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""后端生成器：按数据库结构生成 26 个实体、26 个 Mapper 与控制器。
运行：python3 backend/gen_backend.py
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent
JAVA = ROOT / "src/main/java/com/grad/alumni"
PKG = "com.grad.alumni"

# (表名, 类名, 路由, 关键字列, 状态列, [字段...])  字段：col:Type
SCHEMA = [
    ("sys_org", "SysOrg", None, "org_name", None,
     "id:L org_name:S org_code:S org_type:S parent_id:L sort_no:I status:I create_time:T"),
    ("sys_role", "SysRole", None, "role_name", None,
     "id:L role_code:S role_name:S data_scope:S remark:S status:I create_time:T"),
    ("sys_user", "SysUser", None, "real_name", None,
     "id:L username:S password:S real_name:S phone:S email:S avatar:S org_id:L role_id:L status:I login_fail_count:I lock_until:T last_login_time:T create_time:T update_time:T deleted:I"),
    ("sys_menu", "SysMenu", None, "menu_name", None,
     "id:L parent_id:L menu_name:S menu_type:S path:S perm:S icon:S sort_no:I visible:I create_time:T"),
    ("sys_role_menu", "SysRoleMenu", None, None, None, "id:L role_id:L menu_id:L"),
    ("sys_message", "SysMessage", None, "title", None,
     "id:L user_id:L title:S content:S msg_type:S biz_no:S biz_url:S read_flag:I create_time:T"),
    ("sys_dict", "SysDict", None, "dict_label", None,
     "id:L dict_type:S dict_code:S dict_label:S sort_no:I status:I create_time:T"),
    ("sys_file", "SysFile", None, "file_name", None,
     "id:L file_name:S file_path:S file_size:L file_type:S biz_type:S uploader_id:L uploader_name:S create_time:T"),
    ("sys_log", "SysLog", None, "module", None,
     "id:L user_id:L user_name:S module:S action:S method:S params:S ip:S cost_ms:I create_time:T"),
    ("alumni_profile", "AlumniProfile", "/api/alumni", "real_name", "cert_status",
     "id:L alumni_no:S student_no:S real_name:S gender:S birth_date:D enroll_year:I graduate_year:I college:S major:S class_name:S phone:S email:S work_unit:S work_title:S region_name:S industry:S avatar:S cert_status:S cert_material:S cert_remark:S audit_user:S audit_time:T privacy_level:S show_phone:I show_email:I show_unit:I show_region:I user_id:L create_time:T update_time:T deleted:I"),
    ("alumni_change_request", "AlumniChangeRequest", "/api/change", "alumni_name", "audit_status",
     "id:L alumni_id:L alumni_name:S change_type:S field_name:S old_value:S new_value:S reason:S audit_status:S audit_user:S audit_time:T audit_remark:S create_time:T"),
    ("alumni_organization", "AlumniOrganization", "/api/alumni-org", "org_name", "status",
     "id:L org_name:S org_code:S org_type:S college:S region_name:S grade_year:I leader_name:S leader_phone:S member_count:I intro:S cover_image:S status:S create_time:T update_time:T deleted:I"),
    ("organization_member", "OrganizationMember", "/api/member", "alumni_name", "join_status",
     "id:L org_id:L alumni_id:L alumni_name:S member_role:S join_status:S apply_reason:S audit_user:S audit_time:T create_time:T"),
    ("organization_notice", "OrganizationNotice", "/api/notice", "title", None,
     "id:L org_id:L org_name:S title:S content:S publisher:S publish_time:T top_flag:I create_time:T"),
    ("alumni_activity", "AlumniActivity", "/api/activity", "title", "status",
     "id:L activity_no:S title:S activity_type:S org_id:L org_name:S college:S location:S start_time:T end_time:T capacity:I signup_count:I wait_count:I checkin_count:I poster:S agenda:S signup_form:S audit_mode:S status:S charge_person:S reject_reason:S create_time:T update_time:T deleted:I"),
    ("activity_signup", "ActivitySignup", "/api/signup", "alumni_name", "status",
     "id:L signup_no:S activity_id:L activity_title:S alumni_id:L alumni_name:S companion_count:I companion_names:S status:S wait_no:I checkin_code:S checkin_time:T audit_user:S audit_time:T remark:S create_time:T update_time:T"),
    ("activity_checkin", "ActivityCheckin", "/api/checkin", "alumni_name", None,
     "id:L activity_id:L signup_id:L alumni_id:L alumni_name:S checkin_code:S checkin_time:T checkin_by:S checkin_type:S remark:S create_time:T"),
    ("activity_archive", "ActivityArchive", "/api/archive", "activity_title", None,
     "id:L activity_id:L activity_title:S plan_count:I actual_count:I photo_path:S news_title:S news_content:S cost_summary:S cost_total:M feedback_summary:S summary:S archive_user:S archive_time:T create_time:T"),
    ("donation_project", "DonationProject", "/api/project", "project_name", "status",
     "id:L project_no:S project_name:S initiator:S purpose:S target_amount:M raised_amount:M spent_amount:M beneficiary_count:I start_date:D end_date:D charge_person:S dept_name:S budget_amount:M public_flag:I public_status:S status:S cover_image:S public_desc:S milestone_rate:M progress_rate:M rule_version:S create_time:T update_time:T deleted:I"),
    ("donation_record", "DonationRecord", "/api/donation", "donor_name", "verify_status",
     "id:L record_no:S project_id:L project_name:S donor_name:S donor_alumni_id:L donor_type:S amount:M goods_desc:S goods_value:M donate_date:D intention:S voucher_path:S anonymous_flag:I cert_flag:I verify_status:S verify_user:S verify_time:T verify_remark:S fund_usage:S receipt_status:S create_time:T update_time:T"),
    ("project_milestone", "ProjectMilestone", "/api/milestone", "milestone_name", "status",
     "id:L project_id:L milestone_name:S seq_no:I plan_date:D finish_date:D weight:I status:S deliverable:S create_time:T"),
    ("project_progress", "ProjectProgress", "/api/progress", "stage_name", "audit_status",
     "id:L project_id:L project_name:S stage_name:S progress_rate:M content:S fund_summary:S photo_path:S publish_user:S publish_time:T audit_status:S audit_user:S audit_time:T create_time:T"),
    ("thank_certificate", "ThankCertificate", "/api/cert", "donor_name", "send_status",
     "id:L cert_no:S record_id:L record_no:S project_id:L project_name:S donor_name:S donor_alumni_id:L amount:M issue_date:D cert_path:S issue_user:S send_status:S send_time:T send_way:S remark:S create_time:T"),
    ("alumni_project_rule", "AlumniProjectRule", "/api/rule", "rule_name", "status",
     "id:L rule_name:S version:S target_weight:I amount_weight:I milestone_weight:I voucher_weight:I beneficiary_weight:I audit_weight:I pass_score:I good_score:I status:S effect_time:T create_user:S create_time:T"),
    ("alumni_project_score", "AlumniProjectScore", "/api/score", "project_name", "result_level",
     "id:L project_id:L project_name:S rule_id:L rule_version:S input_snapshot:S target_score:M amount_score:M milestone_score:M voucher_score:M beneficiary_score:M audit_score:M total_score:M result_level:S explanation:S unmet_conditions:S improve_items:S calc_time:T calc_user:S manual_level:S manual_reason:S manual_user:S manual_time:T create_time:T"),
    ("project_attachment", "ProjectAttachment", "/api/attachment", "file_name", None,
     "id:L project_id:L biz_type:S file_name:S file_path:S file_size:L uploader:S create_time:T"),
]

TYPE = {"L": "Long", "S": "String", "I": "Integer", "M": "java.math.BigDecimal",
        "T": "java.time.LocalDateTime", "D": "java.time.LocalDate"}

GENERIC = ["SysOrg", "SysDict", "SysLog", "OrganizationNotice", "ActivityCheckin",
           "ActivityArchive", "ProjectMilestone", "ProjectAttachment", "SysRoleMenu"]


def camel(col):
    parts = col.split("_")
    return parts[0] + "".join(p.capitalize() for p in parts[1:])


def gen_entities():
    for table, cls, _, _, _, fields in SCHEMA:
        decls = []
        imports = set()
        for f in fields.split():
            col, t = f.split(":")
            jt = TYPE[t]
            if jt.startswith("java."):
                imports.add(jt)
            decls.append(f"    /** {col} */\n    private {jt.split('.')[-1]} {camel(col)};")
        imps = "".join(f"import {i};\n" for i in sorted(imports))
        body = "\n\n".join(decls)
        # getter/setter
        acc = []
        for f in fields.split():
            col, t = f.split(":")
            jt = TYPE[t].split(".")[-1]
            fn = camel(col)
            cap = fn[0].upper() + fn[1:]
            acc.append(f"    public {jt} get{cap}() {{ return {fn}; }}\n"
                       f"    public void set{cap}({jt} v) {{ this.{fn} = v; }}")
        src = f"""package {PKG}.entity;

import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
{imps}
/** {table} 实体（字段与数据库列一一对应） */
@TableName("{table}")
public class {cls} {{

    @TableId
{body}

{chr(10).join(acc)}
}}
"""
        (JAVA / "entity" / f"{cls}.java").write_text(src, encoding="utf-8")

        mapper = f"""package {PKG}.mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import {PKG}.entity.{cls};
import org.apache.ibatis.annotations.Mapper;

/** {cls} 数据访问 */
@Mapper
public interface {cls}Mapper extends BaseMapper<{cls}> {{
}}
"""
        (JAVA / "mapper" / f"{cls}Mapper.java").write_text(mapper, encoding="utf-8")


def gen_generic():
    for table, cls, route, kw, status, _ in SCHEMA:
        if cls not in GENERIC:
            continue
        route = route or ("/api/" + cls.replace("Sys", "sys-").replace("Organization", "org-").lower())
        kwm = f'    @Override\n    protected String kwColumn() {{ return "{kw}"; }}\n' if kw else ""
        stm = f'    @Override\n    protected String statusColumn() {{ return "{status}"; }}\n' if status else ""
        src = f"""package {PKG}.controller;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;
import {PKG}.entity.{cls};
import {PKG}.mapper.{cls}Mapper;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/** {cls} 通用增删改查接口（分页/详情/新建/更新/删除） */
@RestController
@RequestMapping("{route}")
public class {cls}Controller extends BaseController<{cls}> {{

    private final {cls}Mapper mapper;

    public {cls}Controller({cls}Mapper mapper) {{
        this.mapper = mapper;
    }}

    @Override
    protected BaseMapper<{cls}> mapper() {{
        return mapper;
    }}

{kwm}{stm}}}
"""
        (JAVA / "controller" / f"{cls}Controller.java").write_text(src, encoding="utf-8")


if __name__ == "__main__":
    gen_entities()
    gen_generic()
    print("entities:", len(SCHEMA), "generic controllers:", len(GENERIC))
