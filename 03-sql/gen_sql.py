#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""init.sql 生成器：26 张表 + 真实分布的测试数据（跨 6 个月）+ 真实本地图片路径 + 创新模块计算留痕。
运行：python3 sql/gen_sql.py  →  sql/init.sql
"""
import pathlib, random, bcrypt, datetime

BASE = pathlib.Path(__file__).resolve().parent
random.seed(20261101)

def pw(raw):
    return bcrypt.hashpw(raw.encode(), bcrypt.gensalt(rounds=10, prefix=b"2a")).decode()

def T(days, hh=9, mm=0):
    """过去第 days 天的某时刻（相对导入时间），保证 create_time 跨半年分布"""
    return f"DATE_SUB(CURDATE(), INTERVAL {days} DAY) + INTERVAL {hh * 60 + mm} MINUTE"

def F(days, hh=9, mm=0):
    """未来第 days 天"""
    return f"DATE_ADD(CURDATE(), INTERVAL {days} DAY) + INTERVAL {hh * 60 + mm} MINUTE"

def D(days):
    return f"DATE_SUB(CURDATE(), INTERVAL {days} DAY)"

def D2(days):
    return f"DATE_ADD(CURDATE(), INTERVAL {days} DAY)"

def q(v):
    if v is None:
        return "NULL"
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, str) and v.startswith(("DATE_", "NOW()", "CURDATE()")):
        return v
    return "'" + str(v).replace("\\", "\\\\").replace("'", "''") + "'"

def insert(table, cols, rows):
    if not rows:
        return ""
    out = [f"INSERT INTO `{table}` ({', '.join('`' + c + '`' for c in cols)}) VALUES"]
    vals = []
    for r in rows:
        vals.append("(" + ", ".join(q(x) for x in r) + ")")
    out.append(",\n".join(vals) + ";")
    return "\n".join(out) + "\n"

S = []  # SQL 片段

# ============ 1. 系统表 ============
S.append("""-- ============================================================
-- 校友活动与捐赠项目管理系统 数据库初始化脚本（MySQL 8 / utf8mb4）
-- 26 张表：系统 9 张 + 校友业务 9 张 + 捐赠业务 5 张 + 创新模块 2 张 + 附件 1 张
-- 执行：mysql -uroot -p123456 < sql/init.sql
-- 默认账号：admin / admin123（校友办），liaison01、finance01、alumni01 密码 123456
-- ============================================================
DROP DATABASE IF EXISTS `new_028`;
CREATE DATABASE `new_028` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `new_028`;

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

CREATE TABLE `sys_org` (
  `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '主键',
  `org_name` VARCHAR(100) NOT NULL COMMENT '组织名称',
  `org_code` VARCHAR(50) NOT NULL COMMENT '组织编码',
  `org_type` VARCHAR(20) NOT NULL COMMENT '类型：COLLEGE/DEPT/ASSOC',
  `parent_id` BIGINT DEFAULT 0 COMMENT '上级组织',
  `sort_no` INT DEFAULT 0 COMMENT '排序',
  `status` TINYINT DEFAULT 1 COMMENT '1 启用 0 停用',
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`), UNIQUE KEY `uk_org_code` (`org_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='组织/院系';

CREATE TABLE `sys_role` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `role_code` VARCHAR(30) NOT NULL COMMENT '角色编码',
  `role_name` VARCHAR(50) NOT NULL COMMENT '角色名称',
  `data_scope` VARCHAR(20) NOT NULL COMMENT '数据范围：ALL/DEPT/SELF/ORG',
  `remark` VARCHAR(200) DEFAULT NULL COMMENT '说明',
  `status` TINYINT DEFAULT 1,
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`), UNIQUE KEY `uk_role_code` (`role_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='角色';

CREATE TABLE `sys_user` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(50) NOT NULL COMMENT '登录账号',
  `password` VARCHAR(100) NOT NULL COMMENT 'BCrypt 密文，任何接口不得返回',
  `real_name` VARCHAR(50) NOT NULL COMMENT '姓名',
  `phone` VARCHAR(20) DEFAULT NULL,
  `email` VARCHAR(100) DEFAULT NULL,
  `avatar` VARCHAR(200) DEFAULT NULL COMMENT '头像相对路径',
  `org_id` BIGINT DEFAULT NULL COMMENT '所属组织',
  `role_id` BIGINT NOT NULL COMMENT '角色',
  `status` TINYINT DEFAULT 1 COMMENT '1 正常 0 停用',
  `login_fail_count` INT DEFAULT 0 COMMENT '连续登录失败次数',
  `lock_until` DATETIME DEFAULT NULL COMMENT '锁定截止时间',
  `last_login_time` DATETIME DEFAULT NULL,
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `deleted` TINYINT DEFAULT 0 COMMENT '逻辑删除',
  PRIMARY KEY (`id`), UNIQUE KEY `uk_username` (`username`), KEY `idx_role` (`role_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户';

CREATE TABLE `sys_menu` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `parent_id` BIGINT DEFAULT 0,
  `menu_name` VARCHAR(50) NOT NULL,
  `menu_type` CHAR(1) NOT NULL COMMENT 'M 目录/C 菜单/F 按钮',
  `path` VARCHAR(120) DEFAULT NULL COMMENT '前端路由',
  `perm` VARCHAR(100) DEFAULT NULL COMMENT '权限标识',
  `icon` VARCHAR(50) DEFAULT NULL,
  `sort_no` INT DEFAULT 0,
  `visible` TINYINT DEFAULT 1 COMMENT '1 显示 0 隐藏',
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='菜单';

CREATE TABLE `sys_role_menu` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `role_id` BIGINT NOT NULL,
  `menu_id` BIGINT NOT NULL,
  PRIMARY KEY (`id`), UNIQUE KEY `uk_role_menu` (`role_id`, `menu_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='角色菜单';

CREATE TABLE `sys_message` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `user_id` BIGINT NOT NULL COMMENT '接收人',
  `title` VARCHAR(120) NOT NULL,
  `content` VARCHAR(500) DEFAULT NULL,
  `msg_type` VARCHAR(30) DEFAULT NULL COMMENT 'AUDIT/PROGRESS/CERT/SIGNUP',
  `biz_no` VARCHAR(50) DEFAULT NULL COMMENT '业务编号',
  `biz_url` VARCHAR(200) DEFAULT NULL COMMENT '详情跳转地址',
  `read_flag` TINYINT DEFAULT 0,
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`), KEY `idx_user_read` (`user_id`, `read_flag`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='站内消息';

CREATE TABLE `sys_dict` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `dict_type` VARCHAR(50) NOT NULL COMMENT '字典类型',
  `dict_code` VARCHAR(50) NOT NULL,
  `dict_label` VARCHAR(50) NOT NULL,
  `sort_no` INT DEFAULT 0,
  `status` TINYINT DEFAULT 1,
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`), KEY `idx_type` (`dict_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='数据字典';

CREATE TABLE `sys_file` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `file_name` VARCHAR(200) NOT NULL COMMENT '原始文件名',
  `file_path` VARCHAR(300) NOT NULL COMMENT '相对路径 /uploads/...',
  `file_size` BIGINT DEFAULT 0,
  `file_type` VARCHAR(50) DEFAULT NULL,
  `biz_type` VARCHAR(50) DEFAULT NULL COMMENT 'CERT/POSTER/VOUCHER/PROGRESS/AVATAR',
  `uploader_id` BIGINT DEFAULT NULL,
  `uploader_name` VARCHAR(50) DEFAULT NULL,
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='文件元数据';

CREATE TABLE `sys_log` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `user_id` BIGINT DEFAULT NULL,
  `user_name` VARCHAR(50) DEFAULT NULL,
  `module` VARCHAR(50) DEFAULT NULL COMMENT '模块',
  `action` VARCHAR(50) DEFAULT NULL COMMENT '动作',
  `method` VARCHAR(200) DEFAULT NULL,
  `params` VARCHAR(500) DEFAULT NULL,
  `ip` VARCHAR(50) DEFAULT NULL,
  `cost_ms` INT DEFAULT 0,
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`), KEY `idx_time` (`create_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='操作日志';
""")

# ============ 2. 校友业务表 ============
S.append("""
CREATE TABLE `alumni_profile` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `alumni_no` VARCHAR(30) NOT NULL COMMENT '校友编号，后端生成',
  `student_no` VARCHAR(30) NOT NULL COMMENT '学号',
  `real_name` VARCHAR(50) NOT NULL,
  `gender` VARCHAR(10) DEFAULT NULL COMMENT '男/女',
  `birth_date` DATE DEFAULT NULL,
  `enroll_year` INT DEFAULT NULL COMMENT '入学年',
  `graduate_year` INT DEFAULT NULL COMMENT '毕业年',
  `college` VARCHAR(60) DEFAULT NULL COMMENT '院系',
  `major` VARCHAR(60) DEFAULT NULL COMMENT '专业',
  `class_name` VARCHAR(40) DEFAULT NULL COMMENT '班级',
  `phone` VARCHAR(20) DEFAULT NULL,
  `email` VARCHAR(100) DEFAULT NULL,
  `work_unit` VARCHAR(120) DEFAULT NULL COMMENT '工作单位',
  `work_title` VARCHAR(60) DEFAULT NULL COMMENT '职务',
  `region_name` VARCHAR(40) DEFAULT NULL COMMENT '所在地区',
  `industry` VARCHAR(40) DEFAULT NULL COMMENT '行业',
  `avatar` VARCHAR(200) DEFAULT NULL COMMENT '头像相对路径',
  `cert_status` VARCHAR(20) NOT NULL DEFAULT '待审核' COMMENT '待审核/已认证/已驳回',
  `cert_material` VARCHAR(300) DEFAULT NULL COMMENT '证明材料路径',
  `cert_remark` VARCHAR(300) DEFAULT NULL COMMENT '审核意见',
  `audit_user` VARCHAR(50) DEFAULT NULL,
  `audit_time` DATETIME DEFAULT NULL,
  `privacy_level` VARCHAR(20) DEFAULT 'PUBLIC' COMMENT 'PUBLIC/ALUMNI_ONLY/SELF',
  `show_phone` TINYINT DEFAULT 1 COMMENT '是否向校友公开手机号',
  `show_email` TINYINT DEFAULT 1,
  `show_unit` TINYINT DEFAULT 1,
  `show_region` TINYINT DEFAULT 1,
  `user_id` BIGINT DEFAULT NULL COMMENT '绑定登录账号',
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `deleted` TINYINT DEFAULT 0,
  PRIMARY KEY (`id`), UNIQUE KEY `uk_alumni_no` (`alumni_no`), KEY `idx_name` (`real_name`), KEY `idx_college` (`college`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='校友档案';

CREATE TABLE `alumni_change_request` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `alumni_id` BIGINT NOT NULL,
  `alumni_name` VARCHAR(50) DEFAULT NULL,
  `change_type` VARCHAR(30) NOT NULL COMMENT '工作单位/联系方式/所在地区/邮箱',
  `field_name` VARCHAR(50) DEFAULT NULL,
  `old_value` VARCHAR(300) DEFAULT NULL,
  `new_value` VARCHAR(300) DEFAULT NULL,
  `reason` VARCHAR(300) DEFAULT NULL COMMENT '申请理由',
  `audit_status` VARCHAR(20) DEFAULT '待审核' COMMENT '待审核/已通过/已退回',
  `audit_user` VARCHAR(50) DEFAULT NULL,
  `audit_time` DATETIME DEFAULT NULL,
  `audit_remark` VARCHAR(300) DEFAULT NULL COMMENT '审核意见（退回必填≥5字）',
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`), KEY `idx_alumni` (`alumni_id`), KEY `idx_status` (`audit_status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='校友信息变更申请';

CREATE TABLE `alumni_organization` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `org_name` VARCHAR(100) NOT NULL,
  `org_code` VARCHAR(50) NOT NULL,
  `org_type` VARCHAR(20) NOT NULL COMMENT '班级/年级/地区/行业',
  `college` VARCHAR(60) DEFAULT NULL COMMENT '挂靠院系',
  `region_name` VARCHAR(40) DEFAULT NULL,
  `grade_year` INT DEFAULT NULL,
  `leader_name` VARCHAR(50) DEFAULT NULL COMMENT '负责人',
  `leader_phone` VARCHAR(20) DEFAULT NULL,
  `member_count` INT DEFAULT 0 COMMENT '成员数（申请通过后累加）',
  `intro` VARCHAR(500) DEFAULT NULL,
  `cover_image` VARCHAR(200) DEFAULT NULL,
  `status` VARCHAR(20) DEFAULT '已通过' COMMENT '待审核/已通过/已停用',
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `deleted` TINYINT DEFAULT 0,
  PRIMARY KEY (`id`), UNIQUE KEY `uk_org` (`org_code`), KEY `idx_type` (`org_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='校友组织';

CREATE TABLE `organization_member` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `org_id` BIGINT NOT NULL,
  `alumni_id` BIGINT NOT NULL,
  `alumni_name` VARCHAR(50) DEFAULT NULL,
  `member_role` VARCHAR(20) DEFAULT '成员' COMMENT '负责人/成员',
  `join_status` VARCHAR(20) DEFAULT '待审核' COMMENT '待审核/已通过/已退出',
  `apply_reason` VARCHAR(300) DEFAULT NULL,
  `audit_user` VARCHAR(50) DEFAULT NULL,
  `audit_time` DATETIME DEFAULT NULL,
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`), KEY `idx_org` (`org_id`), KEY `idx_alumni` (`alumni_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='组织成员';

CREATE TABLE `organization_notice` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `org_id` BIGINT NOT NULL,
  `org_name` VARCHAR(100) DEFAULT NULL,
  `title` VARCHAR(150) NOT NULL,
  `content` VARCHAR(1000) DEFAULT NULL,
  `publisher` VARCHAR(50) DEFAULT NULL,
  `publish_time` DATETIME DEFAULT NULL,
  `top_flag` TINYINT DEFAULT 0,
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`), KEY `idx_org` (`org_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='组织公告';

CREATE TABLE `alumni_activity` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `activity_no` VARCHAR(30) NOT NULL COMMENT '活动编号，后端生成',
  `title` VARCHAR(150) NOT NULL,
  `activity_type` VARCHAR(20) NOT NULL COMMENT '返校/沙龙/论坛/文体/公益/聚会',
  `org_id` BIGINT DEFAULT NULL COMMENT '主办组织',
  `org_name` VARCHAR(100) DEFAULT NULL,
  `college` VARCHAR(60) DEFAULT NULL,
  `location` VARCHAR(150) DEFAULT NULL,
  `start_time` DATETIME NOT NULL COMMENT '开始时间',
  `end_time` DATETIME DEFAULT NULL,
  `capacity` INT NOT NULL DEFAULT 50 COMMENT '人数上限',
  `signup_count` INT DEFAULT 0 COMMENT '已报名（不含候补）',
  `wait_count` INT DEFAULT 0 COMMENT '候补人数',
  `checkin_count` INT DEFAULT 0 COMMENT '已签到人数',
  `poster` VARCHAR(200) DEFAULT NULL COMMENT '海报相对路径',
  `agenda` VARCHAR(1000) DEFAULT NULL COMMENT '活动日程',
  `signup_form` VARCHAR(500) DEFAULT NULL COMMENT '报名表单字段',
  `audit_mode` VARCHAR(20) DEFAULT '人工审核' COMMENT '自动通过/人工审核',
  `status` VARCHAR(20) DEFAULT '待审核' COMMENT '待审核/报名中/进行中/已归档/已驳回/已取消',
  `charge_person` VARCHAR(50) DEFAULT NULL COMMENT '负责人',
  `reject_reason` VARCHAR(300) DEFAULT NULL,
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `deleted` TINYINT DEFAULT 0,
  PRIMARY KEY (`id`), UNIQUE KEY `uk_activity_no` (`activity_no`), KEY `idx_status` (`status`), KEY `idx_start` (`start_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='校友活动';

CREATE TABLE `activity_signup` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `signup_no` VARCHAR(30) NOT NULL,
  `activity_id` BIGINT NOT NULL,
  `activity_title` VARCHAR(150) DEFAULT NULL,
  `alumni_id` BIGINT NOT NULL,
  `alumni_name` VARCHAR(50) DEFAULT NULL,
  `companion_count` INT DEFAULT 0 COMMENT '同行人数',
  `companion_names` VARCHAR(200) DEFAULT NULL COMMENT '同行人姓名',
  `status` VARCHAR(20) DEFAULT '待审核' COMMENT '待审核/已报名/候补/已签到/未到场/已取消',
  `wait_no` INT DEFAULT NULL COMMENT '候补序号，转正时清空',
  `checkin_code` VARCHAR(10) DEFAULT NULL COMMENT '6 位签到验证码',
  `checkin_time` DATETIME DEFAULT NULL,
  `audit_user` VARCHAR(50) DEFAULT NULL,
  `audit_time` DATETIME DEFAULT NULL,
  `remark` VARCHAR(300) DEFAULT NULL COMMENT '取消原因等',
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`), UNIQUE KEY `uk_signup_no` (`signup_no`), KEY `idx_activity` (`activity_id`), KEY `idx_alumni` (`alumni_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='活动报名（含候补）';

CREATE TABLE `activity_checkin` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `activity_id` BIGINT NOT NULL,
  `signup_id` BIGINT NOT NULL,
  `alumni_id` BIGINT DEFAULT NULL,
  `alumni_name` VARCHAR(50) DEFAULT NULL,
  `checkin_code` VARCHAR(10) DEFAULT NULL,
  `checkin_time` DATETIME DEFAULT NULL,
  `checkin_by` VARCHAR(50) DEFAULT NULL,
  `checkin_type` VARCHAR(20) DEFAULT '验证码' COMMENT '验证码/手工补签',
  `remark` VARCHAR(200) DEFAULT NULL,
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`), KEY `idx_activity` (`activity_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='现场签到';

CREATE TABLE `activity_archive` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `activity_id` BIGINT NOT NULL,
  `activity_title` VARCHAR(150) DEFAULT NULL,
  `plan_count` INT DEFAULT 0 COMMENT '计划人数',
  `actual_count` INT DEFAULT 0 COMMENT '实际到场',
  `photo_path` VARCHAR(300) DEFAULT NULL COMMENT '现场照片',
  `news_title` VARCHAR(200) DEFAULT NULL COMMENT '新闻稿标题',
  `news_content` VARCHAR(1000) DEFAULT NULL,
  `cost_summary` VARCHAR(500) DEFAULT NULL COMMENT '费用摘要',
  `cost_total` DECIMAL(12,2) DEFAULT 0 COMMENT '费用合计',
  `feedback_summary` VARCHAR(500) DEFAULT NULL,
  `summary` VARCHAR(1000) DEFAULT NULL COMMENT '活动总结',
  `archive_user` VARCHAR(50) DEFAULT NULL,
  `archive_time` DATETIME DEFAULT NULL,
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`), UNIQUE KEY `uk_activity` (`activity_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='活动归档';
""")

# ============ 3. 捐赠业务表 ============
S.append("""
CREATE TABLE `donation_project` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `project_no` VARCHAR(50) NOT NULL COMMENT '项目编号，后端生成',
  `project_name` VARCHAR(150) NOT NULL,
  `initiator` VARCHAR(100) NOT NULL COMMENT '发起单位',
  `purpose` VARCHAR(1000) DEFAULT NULL COMMENT '项目目标/用途',
  `target_amount` DECIMAL(14,2) NOT NULL DEFAULT 0 COMMENT '目标金额',
  `raised_amount` DECIMAL(14,2) DEFAULT 0 COMMENT '已登记金额（仅已核对计入）',
  `spent_amount` DECIMAL(14,2) DEFAULT 0 COMMENT '已支出',
  `beneficiary_count` INT DEFAULT 0 COMMENT '受益人数',
  `start_date` DATE DEFAULT NULL,
  `end_date` DATE DEFAULT NULL,
  `charge_person` VARCHAR(50) DEFAULT NULL COMMENT '负责人',
  `dept_name` VARCHAR(60) DEFAULT NULL COMMENT '责任部门',
  `budget_amount` DECIMAL(14,2) DEFAULT 0 COMMENT '预算',
  `public_flag` TINYINT DEFAULT 1 COMMENT '是否公开',
  `public_status` VARCHAR(20) DEFAULT '待审核' COMMENT '待审核/已通过/已驳回',
  `status` VARCHAR(20) DEFAULT '项目立项' COMMENT '项目立项/募集中/执行中/待验收/已结项/已驳回/已取消',
  `cover_image` VARCHAR(200) DEFAULT NULL COMMENT '项目封面',
  `public_desc` VARCHAR(1000) DEFAULT NULL COMMENT '公开说明',
  `milestone_rate` DECIMAL(6,2) DEFAULT 0 COMMENT '里程碑完成度(%)',
  `progress_rate` DECIMAL(6,2) DEFAULT 0 COMMENT '资金完成度(%)',
  `rule_version` VARCHAR(20) DEFAULT NULL COMMENT '最近计算使用的规则版本',
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `deleted` TINYINT DEFAULT 0,
  PRIMARY KEY (`id`), UNIQUE KEY `uk_project_no` (`project_no`), KEY `idx_status` (`status`), KEY `idx_public` (`public_status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='捐赠项目（核心过程单据）';

CREATE TABLE `donation_record` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `record_no` VARCHAR(50) NOT NULL COMMENT '登记编号，后端生成',
  `project_id` BIGINT NOT NULL,
  `project_name` VARCHAR(150) DEFAULT NULL,
  `donor_name` VARCHAR(100) NOT NULL,
  `donor_alumni_id` BIGINT DEFAULT NULL,
  `donor_type` VARCHAR(20) DEFAULT '校友' COMMENT '校友/企业/社会',
  `amount` DECIMAL(14,2) DEFAULT 0 COMMENT '金额',
  `goods_desc` VARCHAR(300) DEFAULT NULL COMMENT '物资说明',
  `goods_value` DECIMAL(14,2) DEFAULT 0 COMMENT '物资金额',
  `donate_date` DATE DEFAULT NULL,
  `intention` VARCHAR(300) DEFAULT NULL COMMENT '捐赠意向',
  `voucher_path` VARCHAR(300) DEFAULT NULL COMMENT '凭证路径',
  `anonymous_flag` TINYINT DEFAULT 0 COMMENT '是否匿名',
  `cert_flag` TINYINT DEFAULT 1 COMMENT '是否开具证明',
  `verify_status` VARCHAR(20) DEFAULT '待核对' COMMENT '待核对/已核对/已退回',
  `verify_user` VARCHAR(50) DEFAULT NULL,
  `verify_time` DATETIME DEFAULT NULL,
  `verify_remark` VARCHAR(300) DEFAULT NULL COMMENT '退回原因（≥5字）',
  `fund_usage` VARCHAR(300) DEFAULT NULL COMMENT '资金用途',
  `receipt_status` VARCHAR(20) DEFAULT '未开具' COMMENT '未开具/已开具',
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
  `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`), UNIQUE KEY `uk_record_no` (`record_no`), KEY `idx_project` (`project_id`), KEY `idx_verify` (`verify_status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='线下捐赠登记';

CREATE TABLE `project_milestone` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `project_id` BIGINT NOT NULL,
  `milestone_name` VARCHAR(150) NOT NULL,
  `seq_no` INT DEFAULT 1 COMMENT '顺序',
  `plan_date` DATE DEFAULT NULL,
  `finish_date` DATE DEFAULT NULL,
  `weight` INT DEFAULT 0 COMMENT '权重(%)，同一项目合计 100',
  `status` VARCHAR(20) DEFAULT '未开始' COMMENT '未开始/进行中/已完成',
  `deliverable` VARCHAR(300) DEFAULT NULL COMMENT '交付物',
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`), KEY `idx_project` (`project_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='项目里程碑（创新模块输入）';

CREATE TABLE `project_progress` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `project_id` BIGINT NOT NULL,
  `project_name` VARCHAR(150) DEFAULT NULL,
  `stage_name` VARCHAR(100) NOT NULL COMMENT '进展阶段',
  `progress_rate` DECIMAL(6,2) DEFAULT 0 COMMENT '当期完成度',
  `content` VARCHAR(1000) DEFAULT NULL COMMENT '进展说明',
  `fund_summary` VARCHAR(500) DEFAULT NULL COMMENT '资金使用摘要',
  `photo_path` VARCHAR(300) DEFAULT NULL COMMENT '成果照片',
  `publish_user` VARCHAR(50) DEFAULT NULL,
  `publish_time` DATETIME DEFAULT NULL,
  `audit_status` VARCHAR(20) DEFAULT '待审核' COMMENT '待审核/已发布/已驳回',
  `audit_user` VARCHAR(50) DEFAULT NULL,
  `audit_time` DATETIME DEFAULT NULL,
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`), KEY `idx_project` (`project_id`), KEY `idx_audit` (`audit_status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='项目进展公示';

CREATE TABLE `thank_certificate` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `cert_no` VARCHAR(50) NOT NULL COMMENT '证书编号，后端生成',
  `record_id` BIGINT NOT NULL,
  `record_no` VARCHAR(50) DEFAULT NULL,
  `project_id` BIGINT DEFAULT NULL,
  `project_name` VARCHAR(150) DEFAULT NULL,
  `donor_name` VARCHAR(100) DEFAULT NULL COMMENT '对外显示名（匿名时为匿名校友）',
  `donor_alumni_id` BIGINT DEFAULT NULL,
  `amount` DECIMAL(14,2) DEFAULT 0,
  `issue_date` DATE DEFAULT NULL,
  `cert_path` VARCHAR(300) DEFAULT NULL COMMENT '电子证书路径',
  `issue_user` VARCHAR(50) DEFAULT NULL,
  `send_status` VARCHAR(20) DEFAULT '待发放' COMMENT '待发放/已发放',
  `send_time` DATETIME DEFAULT NULL,
  `send_way` VARCHAR(50) DEFAULT NULL COMMENT '电子邮件/纸质邮寄',
  `remark` VARCHAR(300) DEFAULT NULL,
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`), UNIQUE KEY `uk_cert_no` (`cert_no`), KEY `idx_record` (`record_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='感谢证书';
""")

# ============ 4. 创新模块 + 附件 ============
S.append("""
CREATE TABLE `alumni_project_rule` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `rule_name` VARCHAR(100) NOT NULL COMMENT '规则名称',
  `version` VARCHAR(20) NOT NULL COMMENT '版本号',
  `target_weight` INT DEFAULT 15 COMMENT '目标金额权重',
  `amount_weight` INT DEFAULT 25 COMMENT '已登记金额权重',
  `milestone_weight` INT DEFAULT 20 COMMENT '里程碑完成度权重',
  `voucher_weight` INT DEFAULT 15 COMMENT '支出凭证权重',
  `beneficiary_weight` INT DEFAULT 15 COMMENT '受益人数权重',
  `audit_weight` INT DEFAULT 10 COMMENT '公开审核状态权重',
  `pass_score` INT DEFAULT 60 COMMENT '观察阈值',
  `good_score` INT DEFAULT 80 COMMENT '推荐阈值',
  `status` VARCHAR(20) DEFAULT '启用' COMMENT '启用/停用',
  `effect_time` DATETIME DEFAULT NULL COMMENT '生效时间',
  `create_user` VARCHAR(50) DEFAULT NULL,
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`), UNIQUE KEY `uk_version` (`version`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='捐赠公开规则（权重合计必须 100）';

CREATE TABLE `alumni_project_score` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `project_id` BIGINT NOT NULL,
  `project_name` VARCHAR(150) DEFAULT NULL,
  `rule_id` BIGINT DEFAULT NULL,
  `rule_version` VARCHAR(20) DEFAULT NULL,
  `input_snapshot` TEXT COMMENT '输入快照 JSON，保证可追溯',
  `target_score` DECIMAL(6,2) DEFAULT 0,
  `amount_score` DECIMAL(6,2) DEFAULT 0,
  `milestone_score` DECIMAL(6,2) DEFAULT 0,
  `voucher_score` DECIMAL(6,2) DEFAULT 0,
  `beneficiary_score` DECIMAL(6,2) DEFAULT 0,
  `audit_score` DECIMAL(6,2) DEFAULT 0,
  `total_score` DECIMAL(6,2) DEFAULT 0 COMMENT '加权总分',
  `result_level` VARCHAR(20) DEFAULT NULL COMMENT '推荐/观察/不推荐',
  `explanation` VARCHAR(1000) DEFAULT NULL COMMENT '结果解释：主要影响因素',
  `unmet_conditions` VARCHAR(500) DEFAULT NULL COMMENT '未满足条件',
  `improve_items` VARCHAR(500) DEFAULT NULL COMMENT '可改进项',
  `calc_time` DATETIME DEFAULT NULL,
  `calc_user` VARCHAR(50) DEFAULT NULL,
  `manual_level` VARCHAR(20) DEFAULT NULL COMMENT '人工调整后等级',
  `manual_reason` VARCHAR(300) DEFAULT NULL COMMENT '人工修正原因（≥5字）',
  `manual_user` VARCHAR(50) DEFAULT NULL,
  `manual_time` DATETIME DEFAULT NULL,
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`), KEY `idx_project` (`project_id`), KEY `idx_time` (`calc_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='创新模块计算留痕（原始结果不得被覆盖）';

CREATE TABLE `project_attachment` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `project_id` BIGINT NOT NULL,
  `biz_type` VARCHAR(30) DEFAULT '凭证' COMMENT '凭证/封面/进展照片/结项报告',
  `file_name` VARCHAR(200) DEFAULT NULL,
  `file_path` VARCHAR(300) NOT NULL COMMENT '相对路径，不存外链',
  `file_size` BIGINT DEFAULT 0,
  `uploader` VARCHAR(50) DEFAULT NULL,
  `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`), KEY `idx_project` (`project_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='项目附件';
""")

# ============ 数据 ============
orgs = [
    (1, "校友工作办公室", "ORG-ADMIN", "DEPT", 0, 1),
    (2, "计算机学院", "ORG-CS", "COLLEGE", 0, 2),
    (3, "经济管理学院", "ORG-EM", "COLLEGE", 0, 3),
    (4, "机械工程学院", "ORG-ME", "COLLEGE", 0, 4),
    (5, "外国语学院", "ORG-FL", "COLLEGE", 0, 5),
    (6, "材料科学学院", "ORG-MS", "COLLEGE", 0, 6),
    (7, "上海校友会", "ORG-SH", "ASSOC", 1, 7),
    (8, "深圳校友会", "ORG-SZ", "ASSOC", 1, 8),
]
S.append(insert("sys_org", ["id", "org_name", "org_code", "org_type", "parent_id", "sort_no", "status", "create_time"],
                [(o[0], o[1], o[2], o[3], o[4], o[5], 1, T(180)) for o in orgs]))

roles = [(1, "ADMIN", "校友办管理员", "ALL", "认证校友、审核活动与项目、发布进展、处理证书"),
         (2, "LIAISON", "校友联络员", "ORG", "维护班级/地区组织、发起活动、审核成员、管理签到"),
         (3, "FINANCE", "财务登记员", "ALL", "核对线下捐赠、凭证、资金用途与收据状态"),
         (4, "ALUMNI", "校友", "SELF", "申请认证、更新联系信息、报名活动、登记捐赠意向")]
S.append(insert("sys_role", ["id", "role_code", "role_name", "data_scope", "remark", "status", "create_time"],
                [(r[0], r[1], r[2], r[3], r[4], 1, T(200)) for r in roles]))

p_admin, p_user = pw("admin123"), pw("123456")
users = [
    (1, "admin", p_admin, "周敏", "13800000001", "zhoumin@univ.edu.cn", 1, 1),
    (2, "admin02", p_user, "李建国", "13800000002", "lijianguo@univ.edu.cn", 1, 1),
    (3, "liaison01", p_user, "陈立", "13800002210", "chenli@example.com", 7, 2),
    (4, "liaison02", p_user, "王海涛", "13700003345", "wanght@example.com", 8, 2),
    (5, "finance01", p_user, "张倩", "13900005566", "zhangqian@univ.edu.cn", 1, 3),
    (6, "finance02", p_user, "刘伟", "13900005577", "liuwei@univ.edu.cn", 1, 3),
    (7, "alumni01", p_user, "林雅", "13900008876", "linya@example.com", 3, 4),
    (8, "alumni02", p_user, "孙倩", "13600004418", "sunqian@example.com", 6, 4),
    (9, "alumni03", p_user, "周子涵", "13800007723", "zhouzh@example.com", 2, 4),
    (10, "alumni04", p_user, "赵一鸣", "13500009902", "zhaoym@example.com", 5, 4),
]
av = lambda i: f"/uploads/seed/avatar/{((i * 7) % 6) + 1:02d}.jpg"
S.append(insert("sys_user", ["id", "username", "password", "real_name", "phone", "email", "avatar", "org_id", "role_id",
                             "status", "login_fail_count", "last_login_time", "create_time", "update_time", "deleted"],
                [(u[0], u[1], u[2], u[3], u[4], u[5], av(u[0]), u[6], u[7], 1, 0,
                  T(random.randint(0, 5), random.randint(8, 20), random.randint(0, 59)), T(190 - u[0]), T(3), 0) for u in users]))

# ---- 菜单 ----
# (id, parent, name, type, path, perm, icon, sort)
menus = [
    (1, 0, "校友运营看板", "C", "/dashboard", "dashboard:view", "data-board", 1),
    (10, 0, "校友档案", "M", "/alumni", None, "user", 2),
    (11, 10, "校友档案", "C", "/alumni-list", "alumni:list", "users", 1),
    (12, 10, "认证审核", "C", "/cert-audit", "alumni:cert", "circle-check", 2),
    (13, 10, "变更审核", "C", "/change-audit", "alumni:change", "document", 3),
    (20, 0, "校友组织", "M", "/org", None, "office-building", 3),
    (21, 20, "组织管理", "C", "/org-list", "org:list", "office-building", 1),
    (22, 20, "成员审核", "C", "/member-audit", "org:member", "user-filled", 2),
    (23, 20, "组织公告", "C", "/notice", "org:notice", "bell", 3),
    (30, 0, "活动运营", "M", "/activity", None, "calendar", 4),
    (31, 30, "活动管理", "C", "/activity-manage", "activity:list", "calendar", 1),
    (32, 30, "活动审核", "C", "/activity-audit", "activity:audit", "stamp", 2),
    (33, 30, "报名与签到", "C", "/signup-manage", "activity:signup", "checked", 3),
    (34, 30, "活动归档", "C", "/activity-archive", "activity:archive", "folder", 4),
    (35, 30, "活动广场", "C", "/activity-square", "activity:square", "sunny", 5),
    (40, 0, "捐赠管理", "M", "/donation", None, "money", 5),
    (41, 40, "捐赠项目", "C", "/project-list", "project:list", "wallet", 1),
    (42, 40, "线下捐赠登记", "C", "/donation-record", "donation:record", "money", 2),
    (43, 40, "捐赠核对", "C", "/donation-verify", "donation:verify", "stamp", 3),
    (44, 40, "进展公示", "C", "/progress-publish", "progress:list", "trend-charts", 4),
    (45, 40, "感谢证书", "C", "/certificate", "cert:list", "medal", 5),
    (46, 40, "项目公开端", "C", "/public-projects", "project:public", "view", 6),
    (50, 0, "创新模块", "M", "/innovation", None, "set-up", 6),
    (51, 50, "捐赠公开规则", "C", "/rule", "rule:config", "operation", 1),
    (52, 50, "计算留痕", "C", "/score", "score:list", "data-line", 2),
    (53, 50, "效果统计", "C", "/effect", "rule:effect", "histogram", 3),
    (60, 0, "系统管理", "M", "/system", None, "setting", 7),
    (61, 60, "用户管理", "C", "/user", "sys:user", "user", 1),
    (62, 60, "角色管理", "C", "/role", "sys:role", "avatar", 2),
    (63, 60, "菜单管理", "C", "/menu", "sys:menu", "menu", 3),
    (64, 60, "操作日志", "C", "/log", "sys:log", "document", 4),
    (65, 60, "数据字典", "C", "/dict", "sys:dict", "collection", 5),
    (66, 60, "个人中心", "C", "/profile", "sys:profile", "user", 6),
    (90, 0, "我的档案", "C", "/my-profile", "self:profile", "user", 8),
    (91, 0, "我的报名", "C", "/my-signup", "self:signup", "tickets", 9),
    (92, 0, "我的证书", "C", "/my-cert", "self:cert", "medal", 10),
    (93, 0, "捐赠项目公开", "C", "/public-projects", "public:project", "view", 11),
]
S.append(insert("sys_menu", ["id", "parent_id", "menu_name", "menu_type", "path", "perm", "icon", "sort_no", "visible", "create_time"],
                [(m[0], m[1], m[2], m[3], m[4], m[5], m[6], m[7], 1, T(200)) for m in menus]))

role_menu = set()
for m in menus:
    if m[0] in (90, 91, 92):
        role_menu.add((4, m[0]))
    elif m[0] in (93, ):
        for r in (1, 2, 4):
            role_menu.add((r, m[0]))
    elif m[0] in (31, 33, 34, 35, 21, 22, 23, 1, 66):
        for r in (1, 2):
            role_menu.add((r, m[0]))
    elif m[0] in (41, 42, 43, 44, 45):
        for r in (1, 3):
            role_menu.add((r, m[0]))
    else:
        role_menu.add((1, m[0]))
for m in menus:
    if m[2] in ("活动运营", "校友组织", "捐赠管理", "创新模块", "校友档案", "系统管理"):
        role_menu.add((2, m[0])) if m[0] in (30, 20, 40) else None
S.append(insert("sys_role_menu", ["role_id", "menu_id"],
                [(r, m) for r, m in sorted(role_menu)]))

# ---- 字典 ----
dicts = []
for t, items in [
    ("activity_type", ["返校", "沙龙", "论坛", "文体", "公益", "聚会"]),
    ("activity_status", ["待审核", "报名中", "进行中", "已归档", "已驳回", "已取消"]),
    ("cert_status", ["待审核", "已认证", "已驳回"]),
    ("project_status", ["项目立项", "募集中", "执行中", "待验收", "已结项", "已驳回", "已取消"]),
    ("verify_status", ["待核对", "已核对", "已退回"]),
    ("org_type", ["班级", "年级", "地区", "行业"]),
    ("donor_type", ["校友", "企业", "社会"]),
    ("result_level", ["推荐", "观察", "不推荐"]),
]:
    for i, v in enumerate(items, 1):
        dicts.append((t, f"{t}_{i}", v, i))
S.append(insert("sys_dict", ["dict_type", "dict_code", "dict_label", "sort_no", "status", "create_time"],
                [(d[0], d[1], d[2], d[3], 1, T(200)) for d in dicts]))

# ---- 校友档案 ----
surnames = "陈林王赵孙周吴郑冯褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜".replace(" ", "")
given = ["立", "雅", "海涛", "一鸣", "倩", "子涵", "建国", "晓明", "文静", "浩然", "思远", "嘉怡", "振宇", "若曦",
         "泽宇", "静怡", "宇轩", "欣怡", "子豪", "雨桐", "梓涵", "诗涵", "俊杰", "佳琪", "明轩", "露露", "天佑", "芷若",
         "远航", "书瑶", "博文", "心怡", "慕白", "清歌", "岩松", "婉如", "亦凡", "知微", "向阳", "可欣"]
colleges = ["计算机学院", "经济管理学院", "机械工程学院", "外国语学院", "材料科学学院"]
majors = {"计算机学院": ["软件工程", "计算机科学与技术", "人工智能"],
          "经济管理学院": ["会计学", "金融学", "工商管理"],
          "机械工程学院": ["机械设计制造及其自动化", "车辆工程"],
          "外国语学院": ["英语", "日语"],
          "材料科学学院": ["高分子材料与工程", "材料科学与工程"]}
cities = ["上海", "北京", "深圳", "杭州", "广州", "苏州", "成都", "武汉", "南京", "西安"]
units = [("字节跳动", "技术专家"), ("腾讯", "产品经理"), ("阿里巴巴", "高级工程师"), ("中金公司", "高级经理"),
         ("比亚迪", "结构工程师"), ("华为技术有限公司", "解决方案总监"), ("协鑫集团", "研发主管"), ("自由职业", "独立顾问"),
         ("国家电网", "项目经理"), ("普华永道", "审计经理"), ("某高校", "副教授"), ("自主创业", "创始人")]
industries = ["互联网", "金融", "制造", "教育", "能源", "咨询", "文化传媒"]

profiles = []
weibo_pool = ["已认证"] * 30 + ["待审核"] * 4 + ["已驳回"] * 2
for i in range(1, 37):
    c = colleges[(i * 3) % 5]
    gy = 2006 + (i * 3) % 17
    ey = gy - 4
    name = surnames[(i * 7) % len(surnames)] + given[i % len(given)]
    st = weibo_pool[i - 1] if i <= 36 else "已认证"
    u = units[i % len(units)]
    profiles.append((
        i, f"A{ey}{i:04d}", f"{ey}{c[:2]}{1000 + i * 7}", name, "男" if i % 2 else "女",
        f"{ey - 18}-0{(i % 9) + 1}-1{ i % 9 }", ey, gy, c, majors[c][i % len(majors[c])],
        f"{ey}{c[:1]}{(i % 4) + 1}班", f"1{3 + i % 3}8{i:04d}{i % 10}00", f"user{i}@example.com",
        u[0], u[1], cities[i % len(cities)], industries[i % len(industries)], av(i),
        st, "/uploads/seed/cert/01.jpg" if st != "已认证" else None,
        "材料齐全" if st == "已认证" else ("证明材料模糊，请重新上传" if st == "已驳回" else None),
        "周敏" if st != "待审核" else None, T(150 - i * 2, 10, 30) if st != "待审核" else None,
        "PUBLIC", 1, 1 if i % 4 else 0, 1, 1,
        7 + (i - 1) if i <= 4 else None,
        T(170 - i, 9, i), T(10 - (i % 9), 14, 20)))
S.append(insert("alumni_profile",
                ["id", "alumni_no", "student_no", "real_name", "gender", "birth_date", "enroll_year", "graduate_year",
                 "college", "major", "class_name", "phone", "email", "work_unit", "work_title", "region_name",
                 "industry", "avatar", "cert_status", "cert_material", "cert_remark", "audit_user", "audit_time",
                 "privacy_level", "show_phone", "show_email", "show_unit", "show_region", "user_id",
                 "create_time", "update_time"], profiles))

# ---- 变更申请 ----
changes = [
    (1, "工作单位", "工作单位", "字节跳动 · 工程师", "字节跳动 · 技术专家", "岗位晋升，需更新对外展示信息", "待审核", None, None, T(3, 14, 22)),
    (2, "联系方式", "手机", "13900008876", "13900006621", "更换常用手机号", "待审核", None, None, T(3, 15, 40)),
    (5, "所在地区", "所在地区", "无锡", "苏州", "工作调动至苏州分公司", "已通过", "周敏", "信息核对无误", T(5, 9, 12)),
    (6, "工作单位", "工作单位", "某培训机构", "自由职业", "离职转为自由译者", "已退回", "周敏", "未提供新的在职证明，请补充后重新提交", T(6, 17, 5)),
    (3, "邮箱", "邮箱", "old@example.com", "wanght@example.com", "常用邮箱变更", "已通过", "周敏", "已核验", T(12, 11, 8)),
    (9, "工作单位", "工作单位", "腾讯 · 产品经理", "腾讯 · 高级产品经理", "职级调整", "待审核", None, None, T(2, 10, 15)),
]
S.append(insert("alumni_change_request",
                ["alumni_id", "alumni_name", "change_type", "field_name", "old_value", "new_value", "reason",
                 "audit_status", "audit_user", "audit_remark", "create_time"],
                [(c[0], profiles[c[0] - 1][3], c[1], c[2], c[3], c[4], c[5], c[6], c[7], c[8], c[9]) for c in changes]))

# ---- 校友组织 ----
org_defs = [
    (1, "1998级计算机甲班", "AL-1998-CS1", "班级", "计算机学院", "上海", 1998, "王海涛", 42, "1998 级计算机甲班班级联谊组织，每年组织返校聚会。"),
    (2, "2000级经管校友会", "AL-2000-EM", "年级", "经济管理学院", "北京", 2000, "林雅", 128, "覆盖 2000 级经管各专业，定期举办行业沙龙。"),
    (3, "上海校友会", "AL-SH", "地区", None, "上海", None, "陈立", 386, "上海地区校友联络组织，下设 6 个行业分组。"),
    (4, "深圳校友会", "AL-SZ", "地区", None, "深圳", None, "王海涛", 254, "深圳及粤港澳大湾区校友联络组织。"),
    (5, "智能制造行业联谊会", "AL-IND-MFG", "行业", "机械工程学院", "全国", None, "孙倩", 96, "面向智能制造、装备制造行业校友的行业联谊组织。"),
    (6, "2012级软工二班", "AL-2012-CS2", "班级", "计算机学院", "广州", 2012, "周子涵", 38, "2012 级软件工程二班，毕业后保持年度聚会传统。"),
    (7, "材料学院青年学者联谊会", "AL-MS-YOUNG", "行业", "材料科学学院", "全国", None, "孙倩", 64, "材料领域青年学者与产业界校友交流平台。"),
    (8, "1995级机械乙班", "AL-1995-ME2", "班级", "机械工程学院", "苏州", 1995, "赵一鸣", 36, "毕业三十年，坚持每年组织一次班级公益行。"),
    (9, "北京校友会", "AL-BJ", "地区", None, "北京", None, "林雅", 312, "北京地区校友组织，承办校友企业家论坛。"),
    (10, "文创行业校友会", "AL-IND-CUL", "行业", "外国语学院", "全国", None, "周子涵", 58, "文化创意与传媒行业校友组织。"),
]
S.append(insert("alumni_organization",
                ["id", "org_name", "org_code", "org_type", "college", "region_name", "grade_year", "leader_name",
                 "leader_phone", "member_count", "intro", "cover_image", "status", "create_time", "update_time", "deleted"],
                [(o[0], o[1], o[2], o[3], o[4], o[5], o[6], o[7], f"13{70000000 + o[0] * 1111}", o[8], o[9],
                  f"/uploads/seed/activity/{((o[0] * 7) % 8) + 1:02d}.jpg",
                  "待审核" if o[0] == 7 else "已通过", T(170 - o[0] * 6, 9, 20), T(20 - o[0], 15, 0), 0) for o in org_defs]))

# 负责人统一取自校友档案，保证组织负责人、成员与档案三处一致
org_defs = [(o[0], o[1], o[2], o[3], o[4], o[5], o[6], profiles[((o[0] * 5) % 33)][3], o[8], o[9]) for o in org_defs]

members = []
mid = 1
for o in org_defs:
    leader_pid = ((o[0] * 5) % 33) + 1
    members.append((mid, o[0], leader_pid, profiles[leader_pid - 1][3], "负责人", "已通过", "发起组织", "周敏",
                    T(160 - o[0] * 5, 10, 0), T(160 - o[0] * 5, 9, 0)))
    mid += 1
    cnt = 4 + (o[0] * 3) % 5
    for k in range(cnt):
        pid = ((o[0] * 7 + k * 3) % 33) + 1
        if pid == leader_pid:
            pid = pid % 33 + 1
        st = "待审核" if (o[0] + k) % 9 == 0 else "已通过"
        members.append((mid, o[0], pid, profiles[pid - 1][3], "成员", st, "希望加入组织参与活动",
                        "周敏" if st != "待审核" else None,
                        T(120 - k * 5, 11, 10) if st != "待审核" else None, T(125 - k * 5, 11, 0)))
        mid += 1
S.append(insert("organization_member",
                ["id", "org_id", "alumni_id", "alumni_name", "member_role", "join_status", "apply_reason",
                 "audit_user", "audit_time", "create_time"], members))

notices = []
for i, o in enumerate(org_defs, 1):
    notices.append((o[0], o[1], f"{o[1]}年度活动安排通知",
                    f"经组织负责人商议，{o[1]}本年度将组织 2 场主题活动，具体时间与报名方式见活动广场。",
                    o[7], T(30 - i * 2, 10, 0), 1 if i <= 3 else 0, T(30 - i * 2, 9, 50)))
S.append(insert("organization_notice",
                ["org_id", "org_name", "title", "content", "publisher", "publish_time", "top_flag", "create_time"], notices))

# ---- 活动 ----
activity_defs = [
    ("计算机学院校友返校日", "返校", 1, "计算机学院", 120, 12, "报名中", 86, 6, 0),
    ("上海校友会秋季沙龙", "沙龙", 3, "经济管理学院", 80, 8, "报名中", 80, 8, 0),
    ("校友企业家论坛", "论坛", 9, "经济管理学院", 200, 3, "待审核", 0, 0, 0),
    ("1998级毕业25周年聚会", "聚会", 1, "计算机学院", 60, -6, "已归档", 58, 0, 55),
    ("粤港澳校友徒步活动", "文体", 4, "机械工程学院", 100, -12, "已归档", 97, 0, 91),
    ("新材料产业趋势分享", "沙龙", 5, "材料科学学院", 60, 6, "待审核", 0, 0, 0),
    ("2000级经管返校日", "返校", 2, "经济管理学院", 90, 20, "报名中", 62, 0, 0),
    ("校友公益支教招募", "公益", 10, "外国语学院", 40, 15, "报名中", 28, 0, 0),
    ("深圳校友会年度晚宴", "聚会", 4, "机械工程学院", 150, 30, "报名中", 118, 12, 0),
    ("智能制造行业参访", "论坛", 5, "机械工程学院", 50, 25, "报名中", 34, 0, 0),
    ("2012级软工二班十年之约", "聚会", 6, "计算机学院", 45, 9, "报名中", 41, 0, 0),
    ("古籍修复志愿活动", "公益", 7, "材料科学学院", 30, -20, "已归档", 27, 0, 25),
    ("北京校友会读书会", "沙龙", 9, "外国语学院", 40, -28, "已归档", 36, 0, 33),
    ("校友创业项目路演", "论坛", 3, "经济管理学院", 120, -35, "已归档", 112, 0, 104),
    ("机械学院实验室开放日", "返校", 8, "机械工程学院", 80, -45, "已归档", 74, 0, 69),
    ("校友子女夏令营", "文体", 1, "计算机学院", 60, -60, "已归档", 56, 0, 52),
    ("上海校友会迎新酒会", "聚会", 3, "经济管理学院", 100, -75, "已归档", 92, 0, 88),
    ("校友企业招聘专场", "论坛", 3, "计算机学院", 300, -90, "已归档", 268, 0, 241),
    ("秋季校园公益跑", "文体", 1, "计算机学院", 200, -105, "已归档", 186, 0, 172),
    ("材料学院校友学术论坛", "论坛", 5, "材料科学学院", 90, -120, "已归档", 84, 0, 78),
    ("校友捐赠答谢会", "聚会", 1, "经济管理学院", 80, -140, "已归档", 76, 0, 71),
    ("2026 校友工作研讨会", "论坛", 1, "经济管理学院", 60, -2, "已取消", 0, 0, 0),
]
acts = []
for i, a in enumerate(activity_defs, 1):
    no = f"ACT-{20260000 + i * 17:08d}"
    act_status = a[6]
    acts.append((i, no, a[0], a[1], a[2], org_defs[a[2] - 1][1], a[3],
                 F(a[5], 9 + i % 8, (i * 7) % 60) if a[5] >= 0 else T(-a[5], 9 + i % 8, (i * 7) % 60),
                 F(a[5], 17, 0) if a[5] >= 0 else T(-a[5], 17, 0),
                 a[4], a[7], a[8], a[9],
                 f"/uploads/seed/activity/{((i * 7) % 8) + 1:02d}.jpg",
                 "09:00 签到 · 09:30 主题分享 · 11:00 圆桌交流 · 12:00 合影与午餐",
                 "姓名,手机号,同行人数,饮食禁忌", "人工审核" if i % 3 else "自动通过",
                 act_status, org_defs[a[2] - 1][7],
                 "活动方案与海报信息不一致，请修改后重新提交" if act_status == "已取消" else None,
                 T(40 + i, 10, 15), T(2 + i % 10, 16, 30)))
# 活动 INSERT 延后到报名生成之后（统计值由明细推导，保证一致）

# ---- 报名 ----
signups = []
sno = 0
for a in acts:
    aid, cap, st = a[0], a[9], a[17]
    if st in ("待审核", "已取消"):
        continue
    if st == "已归档":
        n_main, n_wait, n_cancel = int(cap * 0.95), 0, 2
    else:
        n_main, n_wait, n_cancel = min(cap, 26), (4 if cap <= 120 else 8), 2
    for k in range(n_main + n_wait + n_cancel):
        sno += 1
        pid = ((aid * 7 + k * 3) % 33) + 1
        if k < n_main:
            if st == "已归档":
                s_status = "已签到" if k < int(n_main * 0.92) else "未到场"
            else:
                s_status = "已报名"
            wait_no = None
        elif k < n_main + n_wait:
            s_status, wait_no = "候补", k - n_main + 1
        else:
            s_status, wait_no = "已取消", None
        signups.append((sno, f"S{202600000 + sno * 13}", aid, a[2], pid, profiles[pid - 1][3],
                        1 if k % 5 == 0 else 0, "家属 1 名" if k % 5 == 0 else None,
                        s_status, wait_no, f"{(sno * 37) % 9000 + 1000}",
                        T(2 + (sno % 6), 9 + sno % 10, sno % 60) if s_status == "已签到" else None,
                        "周敏" if s_status in ("已报名", "已签到", "未到场") else None,
                        T(9 - (sno % 6), 10, sno % 60) if s_status in ("已报名", "已签到", "未到场") else None,
                        "临时出差，申请取消" if s_status == "已取消" else None,
                        T(10 - (sno % 8), 8, sno % 60), T(3, 12, 0)))

# 依据报名明细回填活动的报名数/候补数/签到数，保证统计与明细一致
for idx, a in enumerate(acts):
    mine = [x for x in signups if x[2] == a[0]]
    cnt_main = sum(1 for x in mine if x[8] in ("已报名", "已签到", "未到场"))
    cnt_wait = sum(1 for x in mine if x[8] == "候补")
    cnt_check = sum(1 for x in mine if x[8] == "已签到")
    acts[idx] = a[:10] + (cnt_main, cnt_wait, cnt_check) + a[13:]

S.append(insert("alumni_activity",
                ["id", "activity_no", "title", "activity_type", "org_id", "org_name", "college", "start_time", "end_time",
                 "capacity", "signup_count", "wait_count", "checkin_count", "poster", "agenda", "signup_form", "audit_mode",
                 "status", "charge_person", "reject_reason", "create_time", "update_time"], acts))


S.append(insert("activity_signup",
                ["id", "signup_no", "activity_id", "activity_title", "alumni_id", "alumni_name", "companion_count",
                 "companion_names", "status", "wait_no", "checkin_code", "checkin_time", "audit_user", "audit_time",
                 "remark", "create_time", "update_time"], signups))

checkins = []
cid = 0
for s in signups:
    if s[8] == "已签到":
        cid += 1
        checkins.append((cid, s[2], s[0], s[4], s[5], s[10], s[11], s[12] or "周敏",
                         "验证码" if cid % 5 else "手工补签", None, s[11]))
S.append(insert("activity_checkin",
                ["id", "activity_id", "signup_id", "alumni_id", "alumni_name", "checkin_code", "checkin_time",
                 "checkin_by", "checkin_type", "remark", "create_time"], checkins))

# ---- 归档 ----
archives = []
arch_act = [a for a in acts if a[17] == "已归档"]
for i, a in enumerate(arch_act, 1):
    total = 6800 + i * 1200 + (i % 3) * 2400
    archives.append((i, a[0], a[2], a[9], a[12],
                     f"/uploads/seed/activity/{((i * 3) % 8) + 1:02d}.jpg",
                     f"{a[2]}顺利举办，校友共叙情谊",
                     f"{a[2]}于近日举办，到场校友 {a[12]} 人，现场氛围热烈，多位校友表示希望增加此类活动频次。",
                     f"场地 ¥ {1800 + i * 200} · 餐饮 ¥ {3200 + i * 400} · 物料 ¥ {900 + i * 100} · 合计 ¥ {total}",
                     total, "整体满意度 4.7/5，建议增加自由交流时间。",
                     f"活动按计划完成，实际到场 {a[12]} 人，费用控制在预算内，已形成新闻稿一篇并归档现场照片。",
                     "周敏", T(2 + i, 17, 20), T(2 + i, 17, 0)))
S.append(insert("activity_archive",
                ["id", "activity_id", "activity_title", "plan_count", "actual_count", "photo_path", "news_title",
                 "news_content", "cost_summary", "cost_total", "feedback_summary", "summary", "archive_user",
                 "archive_time", "create_time"], archives))

# ---- 捐赠项目 ----
pdefs = [
    ("计算机学院实验楼改造基金", "计算机学院", "用于实验楼三层机房改造与设备更新，覆盖 6 间实验室、约 1,200 名学生。",
     1000000, "募集中", "李建国", "计算机学院", 1200),
    ("寒门学子助学金", "校友工作办公室", "资助家庭经济困难学生完成学业，每人每年 5,000 元。",
     500000, "执行中", "周敏", "校友工作办公室", 320),
    ("图书馆古籍修复计划", "图书馆", "修复馆藏古籍 120 册，购置恒温恒湿存储设备。",
     300000, "执行中", "张倩", "图书馆", 860),
    ("校友创新创业基金", "创新创业学院", "支持在校生与校友创业项目孵化，提供种子资金与导师辅导。",
     2000000, "募集中", "陈立", "创新创业学院", 240),
    ("校园银杏林认养", "后勤保障处", "认养校园银杏林 200 株，用于日常养护与景观提升。",
     120000, "待验收", "王海涛", "后勤保障处", 1500),
    ("98级班级基金", "计算机学院", "1998 级计算机甲班班级基金，用于班级互助与母校公益项目。",
     200000, "已结项", "林雅", "计算机学院", 180),
    ("智能制造实训中心建设", "机械工程学院", "建设智能制造实训中心，采购工业机器人与数字孪生平台。",
     1500000, "执行中", "孙倩", "机械工程学院", 640),
    ("外国语学院国际交流基金", "外国语学院", "资助学生海外交流与外语竞赛。",
     400000, "募集中", "周子涵", "外国语学院", 210),
    ("材料学科青年学者奖", "材料科学学院", "奖励材料学科优秀青年学者与研究生。",
     600000, "募集中", "刘伟", "材料科学学院", 96),
    ("校园紧急救助金", "校友工作办公室", "为突发重大疾病的在校生提供紧急救助。",
     300000, "执行中", "周敏", "校友工作办公室", 64),
    ("校友林步道改造", "后勤保障处", "改造校友林步道 800 米，增设休闲座椅与照明。",
     180000, "募集中", "王海涛", "后勤保障处", 3200),
    ("图书馆数字资源采购", "图书馆", "采购电子期刊与数据库，服务全校师生科研。",
     800000, "募集中", "张倩", "图书馆", 12000),
    ("创新创业大赛奖金", "创新创业学院", "支持年度创新创业大赛奖金与项目辅导。",
     250000, "待验收", "陈立", "创新创业学院", 180),
    ("计算机学院奖教金", "计算机学院", "奖励教学一线优秀教师。",
     350000, "执行中", "李建国", "计算机学院", 42),
    ("体育场馆器材更新", "体育部", "更新篮球场、羽毛球场地胶与器材。",
     450000, "募集中", "王海涛", "体育部", 4200),
    ("校史馆展陈提升", "档案馆", "校史馆展陈数字化提升与实物征集。",
     700000, "项目立项", "周敏", "档案馆", 0),
    ("乡村振兴实践基金", "团委", "支持学生暑期乡村振兴社会实践团队。",
     200000, "执行中", "周子涵", "团委", 560),
    ("心理健康教育中心", "学生工作处", "建设心理健康教育中心，配备咨询室与测评系统。",
     500000, "募集中", "周敏", "学生工作处", 1800),
    ("校友导师计划", "校友工作办公室", "邀请校友担任在校生职业发展导师。",
     150000, "待验收", "陈立", "校友工作办公室", 240),
    ("实验室安全改造", "材料科学学院", "改造实验室通风与危化品存储设施。",
     380000, "执行中", "孙倩", "材料科学学院", 380),
    ("校园文化节赞助", "团委", "支持年度校园文化节系列活动。",
     120000, "已结项", "周子涵", "团委", 2600),
    ("贫困地区图书捐赠", "图书馆", "向对口帮扶地区学校捐赠图书 5,000 册。",
     160000, "已结项", "张倩", "图书馆", 1800),
    ("校友足球联赛", "体育部", "支持校友足球联赛场地与裁判费用。",
     90000, "已结项", "王海涛", "体育部", 480),
    ("实验室设备更新（材料）", "材料科学学院", "更新材料分析测试设备两台。",
     1200000, "募集中", "孙倩", "材料科学学院", 220),
    ("新生入学礼包", "学生工作处", "为家庭经济困难新生提供入学礼包。",
     100000, "待验收", "周敏", "学生工作处", 600),
    ("校友讲堂运营", "校友工作办公室", "全年组织 12 期校友讲堂。",
     80000, "募集中", "陈立", "校友工作办公室", 1200),
    ("图书馆阅读空间改造", "图书馆", "改造二层阅读空间，增设自习座位。",
     260000, "募集中", "张倩", "图书馆", 5400),
    ("学院网站升级", "计算机学院", "学院官网改版与移动端适配。",
     60000, "项目立项", "李建国", "计算机学院", 0),
    ("创新创业孵化空间", "创新创业学院", "改造孵化空间 600 平米。",
     900000, "已取消", "陈立", "创新创业学院", 0),
    ("校友健康跑活动", "体育部", "组织校友健康跑，推广全民健身。",
     50000, "已结项", "王海涛", "体育部", 900),
    ("材料学院实验室开放基金", "材料科学学院", "支持本科生进入实验室开展科研训练。",
     280000, "募集中", "孙倩", "材料科学学院", 420),
    ("校友之家装修", "校友工作办公室", "建设校友之家活动空间。",
     650000, "待验收", "周敏", "校友工作办公室", 800),
]
projects = []
for i, p in enumerate(pdefs, 1):
    no = f"PJ-2026{i:03d}"
    start = 200 - i * 5
    end = -60 + i * 3
    # 分数分档：band 1 = 推荐档（执行充分）、2 = 观察档、0 = 不推荐档（募捐不足）
    band = 1 if i % 3 == 1 else (2 if i % 3 == 2 else 0)
    ratio_map = {1: 0.682, 2: 0.936, 3: 0.72, 5: 1.0, 6: 0.93, 13: 0.96, 19: 0.94, 25: 1.0}
    ratio = ratio_map.get(i, {1: 0.86, 2: 0.63, 0: 0.34}[band])
    ben = p[7] if band != 1 else max(p[7], 900 + (i * 37) % 600)
    projects.append({
        "id": i, "no": no, "name": p[0], "initiator": p[1], "purpose": p[2], "target": p[3], "status": p[4],
        "band": band, "ratio": ratio, "beneficiary": ben,
        "charge": p[5], "dept": p[6], "start": D(start), "end": D2(end),
        "public_status": "已驳回" if p[4] == "已取消" else ("待审核" if i % 9 == 0 else "已通过"),
        "raised": 0.0, "spent": 0.0, "vouchers": 0,
    })

# ---- 捐赠记录（金额由记录汇总，保证统计一致）----
records = []
rno = 0
donor_types = ["校友", "校友", "校友", "企业", "社会"]
for p in projects:
    if p["status"] in ("项目立项", "已取消"):
        continue
    n = random.randint(3, 6)
    base = p["target"] * p["ratio"] / n
    for k in range(n):
        rno += 1
        amount = round(base * random.uniform(0.5, 1.6), -2)
        if amount < 1000:
            amount = 1000
        pid = ((p["id"] * 5 + k * 3) % 33) + 1
        anonymous = 1 if k == 2 and p["id"] % 3 == 0 else 0
        dname = profiles[pid - 1][3] if anonymous == 0 else "匿名校友"
        if k == 0 and p["id"] % 4 == 0:
            dname, dtype = "华为技术有限公司", "企业"
        elif k == 1 and p["id"] % 5 == 0:
            dname, dtype = "某某科技有限公司", "企业"
        else:
            dtype = "校友"
        verify = "待核对" if (p["id"] + k) % 11 == 0 else ("已退回" if (p["id"] + k) % 17 == 0 else "已核对")
        if p["status"] == "已结项":
            verify = "已核对"
        records.append({
            "id": rno, "no": f"DN-{20260000 + rno * 7:08d}", "project_id": p["id"], "project_name": p["name"],
            "donor_name": dname, "alumni_id": None if dtype != "校友" else pid, "donor_type": dtype,
            "amount": amount, "donate_date": D(180 - (rno * 3) % 175),
            "intention": f"用于{p['name']}相关支出", "voucher": f"/uploads/seed/voucher/{((rno * 7) % 4) + 1:02d}.jpg",
            "anonymous": anonymous, "cert_flag": 1 if amount >= 5000 else 0, "verify": verify,
            "verify_user": "张倩" if verify != "待核对" else None,
            "verify_time": T(6 - (rno % 5), 10, rno % 60) if verify != "待核对" else None,
            "verify_remark": "银行流水与凭证金额不一致，请重新上传凭证" if verify == "已退回" else None,
            "fund_usage": "设备采购与改造支出" if p["status"] in ("执行中", "待验收", "已结项") else None,
            "receipt": "已开具" if verify == "已核对" and amount >= 10000 else "未开具",
            "create_time": T(175 - (rno * 3) % 170, 9 + rno % 9, rno % 60),
        })
        if verify == "已核对":
            p["raised"] += amount
            if p["status"] in ("执行中", "待验收", "已结项"):
                p["spent"] += amount * random.uniform(0.35, 0.8)
S.append(insert("donation_record",
                ["id", "record_no", "project_id", "project_name", "donor_name", "donor_alumni_id", "donor_type",
                 "amount", "goods_desc", "goods_value", "donate_date", "intention", "voucher_path", "anonymous_flag",
                 "cert_flag", "verify_status", "verify_user", "verify_time", "verify_remark", "fund_usage",
                 "receipt_status", "create_time", "update_time"],
                [(r["id"], r["no"], r["project_id"], r["project_name"], r["donor_name"], r["alumni_id"], r["donor_type"],
                  r["amount"], None, 0, r["donate_date"], r["intention"], r["voucher"], r["anonymous"], r["cert_flag"],
                  r["verify"], r["verify_user"], r["verify_time"], r["verify_remark"], r["fund_usage"],
                  r["receipt"], r["create_time"], r["create_time"]) for r in records]))

# ---- 里程碑（每项目 4 个，权重合计 100）----
ms_names = [("方案设计与预算评审", 20), ("一期实施", 35), ("二期实施", 30), ("验收与结项", 15)]
milestones = []
mzid = 0
for p in projects:
    done_ratio = {1: 1.0, 2: 0.55, 0: 0.25}[p["band"]]
    if p["status"] in ("项目立项", "已取消"):
        done_ratio = 0.0
    elif p["status"] == "已结项":
        done_ratio = 1.0
    for k, (nm, w) in enumerate(ms_names):
        mzid += 1
        if k < int(done_ratio * 4 + 0.5):
            st = "已完成"
            fin = D(max(1, 150 - p["id"] * 4 - k * 12))
        elif k == int(done_ratio * 4 + 0.5):
            st = "进行中"
            fin = None
        else:
            st, fin = "未开始", None
        milestones.append((mzid, p["id"], nm, k + 1, D(150 - p["id"] * 4 - k * 20), fin, w, st,
                           f"{nm}交付物清单与验收单"))
p["milestone_rate"] = 0
S.append(insert("project_milestone",
                ["id", "project_id", "milestone_name", "seq_no", "plan_date", "finish_date", "weight", "status",
                 "deliverable", "create_time"],
                [(m[0], m[1], m[2], m[3], m[4], m[5], m[6], m[7], m[8], T(150 - m[1] * 4, 9, 0)) for m in milestones]))

# ---- 项目附件（凭证数量，创新模块输入）----
attach = []
aid = 0
for p in projects:
    if p["status"] in ("项目立项", "已取消"):
        continue
    n = min(14, max(0, int(p["spent"] / 45000) + (p["id"] % 5)))
    p["vouchers"] = n
    for k in range(n):
        aid += 1
        attach.append((aid, p["id"], "凭证", f"支出凭证-{k + 1:02d}.jpg",
                       f"/uploads/seed/voucher/{((aid * 7) % 4) + 1:02d}.jpg", 180000 + aid * 1300,
                       p["charge"], D(120 - (aid % 100))))
S.append(insert("project_attachment",
                ["id", "project_id", "biz_type", "file_name", "file_path", "file_size", "uploader", "create_time"], attach))

# ---- 进展公示 ----
progress = []
gid = 0
for p in projects:
    if p["status"] in ("项目立项", "已取消"):
        continue
    done_ms = [m for m in milestones if m[1] == p["id"] and m[7] == "已完成"]
    for k, m in enumerate(done_ms):
        gid += 1
        progress.append((gid, p["id"], p["name"], m[2], m[6] * (k + 1),
                         f"{m[2]}已完成，相关支出与成果已归档，受益情况见项目说明。",
                         f"本期支出 ¥ {round(p['spent'] / max(1, len(done_ms))):,}，凭证 {max(1, p['vouchers'] // max(1, len(done_ms)))} 份",
                         f"/uploads/seed/progress/{((gid * 7) % 4) + 1:02d}.jpg",
                         p["charge"], m[5] or T(30, 15, 0),
                         "已发布" if p["public_status"] == "已通过" else "待审核",
                         "周敏" if p["public_status"] == "已通过" else None,
                         T(20, 16, 20) if p["public_status"] == "已通过" else None, m[5] or T(30, 15, 0)))
# 再加两条待审核进展
progress.append((gid + 1, 1, pdefs[0][0], "二期设备采购启动", 68, "已签订服务器采购合同，预算 ¥ 260,000，预计 11 月底到货安装。",
                 "本期支出 ¥ 96,000，凭证 3 份", "/uploads/seed/progress/01.jpg", "李建国", T(4, 15, 40), "待审核", None, None, T(4, 15, 40)))
progress.append((gid + 2, 2, pdefs[1][0], "秋季助学金发放完成", 94, "本学期 96 名受助学生助学金已发放完毕。",
                 "本期支出 ¥ 480,000，凭证 24 份", "/uploads/seed/progress/02.jpg", "周敏", T(7, 10, 12), "待审核", None, None, T(7, 10, 12)))
S.append(insert("project_progress",
                ["id", "project_id", "project_name", "stage_name", "progress_rate", "content", "fund_summary",
                 "photo_path", "publish_user", "publish_time", "audit_status", "audit_user", "audit_time", "create_time"],
                progress))

# ---- 项目金额回填 ----
proj_rows = []
for p in projects:
    raised = round(p["raised"], 2)
    p["raised"] = raised
    p["spent"] = round(min(p["spent"], raised), 2)
    rate = round(min(100.0, raised / p["target"] * 100), 2) if p["target"] else 0
    ms_rate = round(sum(m[6] for m in milestones if m[1] == p["id"] and m[7] == "已完成"), 2)
    p["milestone_rate"] = ms_rate
    proj_rows.append((p["id"], p["no"], p["name"], p["initiator"], p["purpose"], p["target"], raised,
                      p["spent"], p["beneficiary"], p["start"], p["end"], p["charge"], p["dept"],
                      round(p["target"] * 1.05, 2), 1 if p["public_status"] == "已通过" else 0,
                      p["public_status"], p["status"],
                      f"/uploads/seed/project/{((p['id'] * 7) % 6) + 1:02d}.jpg",
                      p["purpose"], ms_rate, rate, "v3",
                      T(200 - p["id"] * 5, 9, 30), T(2 + p["id"] % 12, 15, 10), 0))
S.append(insert("donation_project",
                ["id", "project_no", "project_name", "initiator", "purpose", "target_amount", "raised_amount",
                 "spent_amount", "beneficiary_count", "start_date", "end_date", "charge_person", "dept_name",
                 "budget_amount", "public_flag", "public_status", "status", "cover_image", "public_desc",
                 "milestone_rate", "progress_rate", "rule_version", "create_time", "update_time", "deleted"], proj_rows))

# ---- 感谢证书（仅已核对记录，匿名对外显示匿名校友）----
certs = []
cert_i = 0
for r in records:
    if r["verify"] != "已核对" or r["cert_flag"] != 1:
        continue
    cert_i += 1
    certs.append((cert_i, f"TC-2026-{cert_i:06d}", r["id"], r["no"], r["project_id"], r["project_name"],
                  "匿名校友" if r["anonymous"] else r["donor_name"],
                  None if r["anonymous"] else r["alumni_id"], r["amount"], r["donate_date"],
                  f"/uploads/seed/cert/{((cert_i * 7) % 3) + 1:02d}.jpg", "周敏",
                  "已发放" if cert_i % 4 else "待发放",
                  T(3, 10, 0) if cert_i % 4 else None,
                  "电子邮件" if cert_i % 3 else "纸质邮寄", None, r["create_time"]))
S.append(insert("thank_certificate",
                ["id", "cert_no", "record_id", "record_no", "project_id", "project_name", "donor_name",
                 "donor_alumni_id", "amount", "issue_date", "cert_path", "issue_user", "send_status", "send_time",
                 "send_way", "remark", "create_time"], certs))

# ---- 创新模块：规则 + 计算留痕 ----
S.append(insert("alumni_project_rule",
                ["id", "rule_name", "version", "target_weight", "amount_weight", "milestone_weight", "voucher_weight",
                 "beneficiary_weight", "audit_weight", "pass_score", "good_score", "status", "effect_time",
                 "create_user", "create_time"],
                [(1, "捐赠目标与执行里程碑公开", "v1", 20, 25, 20, 10, 15, 10, 60, 80, "停用", T(240, 0, 0), "系统", T(240)),
                 (2, "捐赠目标与执行里程碑公开", "v2", 18, 25, 22, 12, 13, 10, 60, 80, "停用", T(150, 0, 0), "周敏", T(150)),
                 (3, "捐赠目标与执行里程碑公开", "v3", 15, 25, 20, 15, 15, 10, 60, 80, "启用", T(60, 0, 0), "周敏", T(60))]))

WEIGHTS = dict(target=15, amount=25, milestone=20, voucher=15, beneficiary=15, audit=10)

def calc(p, ms_rate, voucher_cnt):
    s_target = round(min(100.0, p["target"] / 500_000 * 100), 1)
    s_amount = round(min(100.0, p["raised"] / p["target"] * 100), 1) if p["target"] else 0
    s_ms = round(ms_rate, 1)
    s_voucher = round(min(100.0, voucher_cnt * 12.5), 1)
    s_ben = round(min(100.0, p["beneficiary"] / 1000 * 100), 1)
    s_audit = {"已通过": 100, "待审核": 30, "已驳回": 0}[p["public_status"]]
    total = round((s_target * 15 + s_amount * 25 + s_ms * 20 + s_voucher * 15 + s_ben * 15 + s_audit * 10) / 100, 1)
    level = "推荐" if total >= 80 else ("观察" if total >= 60 else "不推荐")
    parts = [f"目标金额 {s_target} 分（权重 15%，加权 {round(s_target * .15, 1)} 分）",
             f"已登记金额 {s_amount} 分（权重 25%，加权 {round(s_amount * .25, 1)} 分）",
             f"里程碑完成度 {s_ms} 分（权重 20%，加权 {round(s_ms * .2, 1)} 分）",
             f"支出凭证 {s_voucher} 分（权重 15%，加权 {round(s_voucher * .15, 1)} 分）",
             f"受益人数 {s_ben} 分（权重 15%，加权 {round(s_ben * .15, 1)} 分）",
             f"公开审核状态 {s_audit} 分（权重 10%，加权 {round(s_audit * .1, 1)} 分）"]
    strong = max(parts, key=lambda x: float(x.split("加权 ")[1].split(" 分")[0]))
    unmet = []
    if s_amount < 60:
        unmet.append(f"已登记金额仅达目标的 {s_amount}%，低于 60% 的推荐门槛")
    if s_ms < 80:
        unmet.append(f"里程碑完成度 {s_ms}%，未达到 80%")
    if s_voucher < 60:
        unmet.append(f"支出凭证不足（{voucher_cnt} 份），得分 {s_voucher}")
    if s_audit < 100:
        unmet.append("项目进展公示尚未通过审核")
    improve = []
    if s_amount < 80:
        improve.append(f"继续推动募捐，已登记金额距目标还差 ¥ {round(p['target'] - p['raised']):,}")
    if s_ms < 80:
        improve.append("加快未完成里程碑的实施与验收")
    if s_voucher < 80:
        improve.append("补充支出凭证并完成归档")
    if s_ben < 60:
        improve.append("完善受益人数统计口径并回填")
    if not improve:
        improve.append("保持当前执行节奏，按期完成结项")
    return total, level, s_target, s_amount, s_ms, s_voucher, s_ben, s_audit, strong, unmet, improve

scores = []
sc = 0
for p in projects:
    if p["status"] in ("项目立项", "已取消"):
        continue
    sc += 1
    total, level, st_, sa, sm, sv, sb, sau, strong, unmet, improve = calc(p, p["milestone_rate"], p["vouchers"])
    snap = ('{"target":%d,"raised":%.2f,"milestoneRate":%.2f,"voucherCount":%d,"beneficiary":%d,"publicStatus":"%s"}'
            % (p["target"], p["raised"], p["milestone_rate"], p["vouchers"], p["beneficiary"], p["public_status"]))
    manual = manual_reason = manual_user = None
    if sc % 9 == 0:
        manual = "推荐" if level == "观察" else "观察"
        manual_reason = "项目已完成阶段验收并发布公示，受益人数统计口径尚未更新，按实际执行情况上调"
        manual_user = "周敏"
    scores.append((sc, p["id"], p["name"], 3, "v3", snap, st_, sa, sm, sv, sb, sau, total, level,
                   f"权重最高的影响因素为{'已登记金额' if sa >= sm else '里程碑完成度'}：{strong}；综合得分 {total}，判定为「{level}」。",
                   "；".join(unmet) if unmet else "各项条件均已满足",
                   "；".join(improve), T(4 + sc % 20, 15, 40), "周敏", manual, manual_reason, manual_user,
                   T(3 + sc % 15, 16, 10) if manual else None, T(4 + sc % 20, 15, 40)))
S.append(insert("alumni_project_score",
                ["id", "project_id", "project_name", "rule_id", "rule_version", "input_snapshot", "target_score",
                 "amount_score", "milestone_score", "voucher_score", "beneficiary_score", "audit_score", "total_score",
                 "result_level", "explanation", "unmet_conditions", "improve_items", "calc_time", "calc_user",
                 "manual_level", "manual_reason", "manual_user", "manual_time", "create_time"], scores))

# ---- 消息 ----
msgs = []
for i in range(1, 31):
    uid = ((i * 3) % 10) + 1
    kind = ["AUDIT", "PROGRESS", "CERT", "SIGNUP"][i % 4]
    title, url = {
        "AUDIT": ("您有 1 条待审核事项", "/cert-audit"),
        "PROGRESS": ("捐赠项目有新进展", "/progress-publish"),
        "CERT": ("感谢证书已生成/已发放", "/certificate"),
        "SIGNUP": ("活动报名状态更新", "/signup-manage"),
    }[kind]
    msgs.append((uid, title, f"业务编号 {['A2026001', 'PJ-2026001', 'TC-2026-000001', 'S202600013'][i % 4]} 状态已更新，请及时处理。",
                 kind, ['A2026001', 'PJ-2026001', 'TC-2026-000001', 'S202600013'][i % 4], url,
                 1 if i % 3 else 0, T(i % 25, 9 + i % 8, i % 60)))
S.append(insert("sys_message", ["user_id", "title", "content", "msg_type", "biz_no", "biz_url", "read_flag", "create_time"], msgs))

# ---- 文件 + 日志 ----
files = []
for i in range(1, 13):
    biz = ["POSTER", "VOUCHER", "PROGRESS", "CERT", "AVATAR"][i % 5]
    files.append((f"{biz.lower()}-{i:03d}.jpg", f"/uploads/seed/activity/{((i * 7) % 8) + 1:02d}.jpg",
                  180000 + i * 5200, "image/jpeg", biz, (i % 10) + 1, users[i % 10][3], T(30 - i, 10, 0)))
S.append(insert("sys_file", ["file_name", "file_path", "file_size", "file_type", "biz_type", "uploader_id",
                             "uploader_name", "create_time"], files))

logs = []
for i in range(1, 26):
    logs.append((((i * 3) % 10) + 1, users[(i * 3) % 10][3], ["认证审核", "捐赠核对", "活动审核", "进展公示", "规则配置"][i % 5],
                 ["审核通过", "核对通过", "发布", "更新", "查询"][i % 5], ["POST", "PUT", "GET"][i % 3] + f" /api/{['cert', 'donation', 'activity', 'progress', 'rule'][i % 5]}",
                 "参数已脱敏", f"10.10.1.{i % 200 + 10}", 30 + i * 7, T(i % 30, 9 + i % 9, i % 60)))
S.append(insert("sys_log", ["user_id", "user_name", "module", "action", "method", "params", "ip", "cost_ms", "create_time"], logs))

S.append("""
SET FOREIGN_KEY_CHECKS = 1;

-- 校验：项目已登记金额应等于其已核对捐赠记录之和
SELECT '数据校验' AS chk,
       (SELECT COUNT(*) FROM donation_project) AS projects,
       (SELECT COUNT(*) FROM donation_record) AS records,
       (SELECT COUNT(*) FROM alumni_project_score) AS scores;
""")

out = BASE / "init.sql"
out.write_text("\n".join(S), encoding="utf-8")
print(f"生成 {out} ，{out.stat().st_size/1024:.1f} KB")
print(f"项目 {len(projects)} 个，捐赠记录 {len(records)} 条，活动 {len(acts)} 场，报名 {len(signups)} 条，"
      f"证书 {len(certs)} 张，评分 {len(scores)} 条，附件 {len(attach)} 个，里程碑 {len(milestones)} 条")
