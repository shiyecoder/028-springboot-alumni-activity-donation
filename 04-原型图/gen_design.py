#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""设计稿生成器：为「校友活动与捐赠项目管理系统」批量产出可点击的 HTML mock（内置假数据）。
运行：python3 design/gen_design.py
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent
SPRITE = (ROOT / "icons.svg").read_text(encoding="utf-8")

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
:root{
 --primary:#5B2533;--primary-deep:#431B26;--primary-light:#F3E9EB;
 --secondary:#2F6F6A;--accent:#7A3947;--success:#2D765C;--warning:#B4761F;--danger:#A61B29;
 --bg:#FAF7F5;--surface:#fff;--border:#E7DFDC;--text:#2B2321;--text2:#6B5F5C;--text3:#9A8F8C;
}
body{font-family:-apple-system,"PingFang SC","Microsoft YaHei",Arial,sans-serif;background:var(--bg);color:var(--text);font-size:14px;line-height:22px}
.num{font-variant-numeric:tabular-nums}
.ico{width:16px;height:16px;vertical-align:-3px}
.layout{display:flex;height:100vh;overflow:hidden}
.side{width:220px;background:var(--primary-deep);flex:none;display:flex;flex-direction:column}
.brand{height:56px;display:flex;align-items:center;gap:10px;padding:0 18px;color:#fff;font-weight:600;font-size:15px;border-bottom:1px solid rgba(255,255,255,.1)}
.logo{width:22px;height:22px;border-radius:5px;background:var(--accent);display:inline-flex;align-items:center;justify-content:center;font-size:12px}
.nav{flex:1;overflow:auto;padding-bottom:12px}
.grp{padding:14px 18px 5px;font-size:11px;color:rgba(255,255,255,.45);letter-spacing:1px}
.nav a{display:flex;align-items:center;gap:9px;height:42px;padding:0 18px;color:rgba(255,255,255,.78);text-decoration:none;font-size:13.5px;border-left:3px solid transparent}
.nav a:hover{background:rgba(255,255,255,.06);color:#fff}
.nav a.on{background:rgba(255,255,255,.10);color:#fff;border-left-color:#fff;font-weight:500}
.main{flex:1;display:flex;flex-direction:column;min-width:0}
.top{height:56px;background:#fff;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:16px;padding:0 24px;flex:none}
.crumb{font-size:13px;color:var(--text2)}
.crumb b{color:var(--text);font-weight:500}
.top .right{margin-left:auto;display:flex;align-items:center;gap:18px;font-size:12px;color:var(--text3)}
.avatar{width:32px;height:32px;border-radius:50%;background:#EADCDE;border:1px solid var(--border)}
.who{display:flex;align-items:center;gap:8px}
.who b{font-size:13px;color:var(--text);font-weight:500}
.who i{font-style:normal;font-size:11px;color:var(--text3);display:block}
.content{flex:1;overflow:auto;padding:24px}
.page-h{display:flex;align-items:flex-end;gap:12px;margin-bottom:16px}
.page-h h1{font-size:20px;line-height:28px;font-weight:600}
.page-h p{font-size:12px;color:var(--text3);margin-bottom:3px}
.card{background:var(--surface);border:1px solid var(--border);border-radius:8px}
.card+.card{margin-top:16px}
.card-h{height:48px;display:flex;align-items:center;gap:10px;padding:0 16px;border-bottom:1px solid #EFE8E5}
.card-h h2{font-size:15px;font-weight:600}
.card-h .r{margin-left:auto;display:flex;align-items:center;gap:8px;font-size:12px;color:var(--text3)}
.card-b{padding:16px}
.filter{display:flex;flex-wrap:wrap;gap:12px;align-items:center}
.inp,.sel{height:34px;border:1px solid var(--border);border-radius:6px;background:#fff;display:flex;align-items:center;padding:0 12px;font-size:13px;color:var(--text2);min-width:200px}
.sel{min-width:190px;max-width:240px;justify-content:space-between}
.btn{height:34px;padding:0 16px;border-radius:6px;border:1px solid var(--border);background:#fff;font-size:13px;color:var(--text);display:inline-flex;align-items:center;gap:6px;cursor:pointer}
.btn.p{background:var(--primary);border-color:var(--primary);color:#fff}
.btn.d{background:#fff;border-color:var(--danger);color:var(--danger)}
.btn.t{border:none;background:transparent;color:var(--accent);padding:0 6px;height:28px}
.btn.sm{height:28px;padding:0 10px;font-size:12px}
table{width:100%;border-collapse:collapse}
th{height:42px;background:#F7F0EE;font-size:13px;font-weight:600;color:var(--text2);text-align:left;padding:0 12px;white-space:nowrap;border-bottom:1px solid var(--border)}
td{height:44px;padding:0 12px;font-size:13px;border-bottom:1px solid #EFE8E5;white-space:nowrap}
tbody tr:hover{background:#FCF8F7}
td.r,th.r{text-align:right}
td.c,th.c{text-align:center}
.link{color:var(--accent);text-decoration:none}
.tag{display:inline-block;height:22px;line-height:20px;padding:0 8px;border-radius:4px;font-size:12px;border:1px solid}
.tag.info{color:#5B6472;background:#F1F2F4;border-color:#DDE0E4}
.tag.teal{color:var(--secondary);background:#EAF3F2;border-color:#CFE3E1}
.tag.ok{color:var(--success);background:#EAF4EF;border-color:#CFE5DA}
.tag.warn{color:var(--warning);background:#FBF1E1;border-color:#EEDCBB}
.tag.danger{color:var(--danger);background:#FBEBED;border-color:#EFCFD3}
.tag.muted{color:var(--text2);background:#F2EFEE;border-color:#E4DDDA}
.pager{display:flex;align-items:center;gap:10px;justify-content:flex-end;padding:14px 16px;font-size:12px;color:var(--text3)}
.pager .pg{min-width:30px;height:30px;border:1px solid var(--border);border-radius:6px;display:inline-flex;align-items:center;justify-content:center;background:#fff;color:var(--text2)}
.pager .pg.on{background:var(--primary);border-color:var(--primary);color:#fff}
.kpis{display:grid;grid-template-columns:repeat(6,1fr);gap:16px}
.kpi{background:#fff;border:1px solid var(--border);border-radius:8px;padding:14px 16px}
.kpi h4{font-size:12px;color:var(--text3);font-weight:400}
.kpi b{display:block;font-size:26px;line-height:34px;font-weight:600;margin-top:4px;font-variant-numeric:tabular-nums}
.kpi span{font-size:12px;color:var(--success)}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.grid3{display:grid;grid-template-columns:2fr 1fr;gap:16px}
.chart{height:240px;display:flex;align-items:flex-end;gap:14px;padding:8px 4px 0}
.bar{flex:1;background:linear-gradient(180deg,#7A3947,#5B2533);border-radius:4px 4px 0 0;position:relative}
.bar span{position:absolute;bottom:-20px;left:0;right:0;text-align:center;font-size:11px;color:var(--text3)}
.donut{width:150px;height:150px;border-radius:50%;background:conic-gradient(#5B2533 0 42%,#2F6F6A 42% 68%,#7A3947 68% 86%,#B4761F 86% 100%);position:relative;margin:14px auto}
.donut:after{content:"";position:absolute;inset:30px;background:#fff;border-radius:50%}
.legend{font-size:12px;color:var(--text2);line-height:24px}
.legend i{display:inline-block;width:8px;height:8px;border-radius:2px;margin-right:6px}
.tl{border-left:2px solid var(--border);margin-left:6px;padding-left:18px}
.tl .it{position:relative;padding:0 0 18px}
.tl .it:before{content:"";position:absolute;left:-25px;top:4px;width:8px;height:8px;border-radius:50%;background:#C9B7BB;border:2px solid #fff}
.tl .it.done:before{background:var(--success)}
.tl .it.now:before{background:var(--primary)}
.tl b{font-size:13px}
.tl em{font-style:normal;font-size:12px;color:var(--text3);margin-left:8px}
.tl p{font-size:13px;color:var(--text2);margin-top:2px}
.prog{height:8px;border-radius:4px;background:#F1EAE8;overflow:hidden}
.prog i{display:block;height:100%;background:var(--secondary)}
.steps{display:flex;gap:0}
.steps .st{flex:1;text-align:center;font-size:12px;color:var(--text3);position:relative;padding-top:22px}
.steps .st:before{content:"";position:absolute;top:6px;left:0;right:0;height:2px;background:var(--border)}
.steps .st:first-child:before{left:50%}
.steps .st:last-child:before{right:50%}
.steps .st:after{content:"";position:absolute;top:2px;left:50%;margin-left:-5px;width:10px;height:10px;border-radius:50%;background:#C9B7BB;border:2px solid #fff}
.steps .st.done{color:var(--text2)}
.steps .st.done:after{background:var(--success)}
.steps .st.now{color:var(--primary);font-weight:600}
.steps .st.now:after{background:var(--primary)}
.thumbs{display:flex;gap:10px}
.thumbs img,.thumbs div{width:96px;height:72px;border-radius:6px;background:#EFE7E4;border:1px solid var(--border);object-fit:cover}
.dl{display:grid;grid-template-columns:110px 1fr;gap:10px 16px;font-size:13px}
.dl dt{color:var(--text2)}
.dl dd{color:var(--text)}
.note{background:#FBF6F4;border:1px solid #EFE0DC;border-radius:6px;padding:12px 14px;font-size:13px;color:var(--text2)}
.muted{color:var(--text3)}
.hint{font-size:12px;color:var(--text3)}
.split{display:grid;grid-template-columns:1fr 300px;gap:16px}
.cover{height:132px;border-radius:6px;background:linear-gradient(135deg,#7A3947,#5B2533);position:relative;overflow:hidden}
.cover b{position:absolute;left:14px;bottom:12px;color:#fff;font-size:14px;font-weight:600}
.chips{display:flex;gap:8px}
.chip{height:30px;padding:0 14px;border-radius:15px;border:1px solid var(--border);background:#fff;font-size:12px;color:var(--text2);display:inline-flex;align-items:center}
.chip.on{background:var(--primary-light);border-color:#E2C9CE;color:var(--primary);font-weight:500}
/* 门户 */
.portal{min-height:100vh;background:var(--bg)}
.p-top{height:60px;background:#fff;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:28px;padding:0 40px;position:sticky;top:0;z-index:9}
.p-brand{display:flex;align-items:center;gap:10px;font-size:15px;font-weight:600;color:var(--primary)}
.p-nav{display:flex;gap:4px}
.p-nav a{padding:6px 14px;border-radius:6px;font-size:14px;color:var(--text2);text-decoration:none}
.p-nav a.on{background:var(--primary-light);color:var(--primary);font-weight:500}
.p-body{max-width:1200px;margin:0 auto;padding:24px 40px 48px}
.p-hero{background:linear-gradient(120deg,#5B2533,#7A3947 65%,#2F6F6A);border-radius:10px;padding:28px 30px;color:#fff;margin-bottom:20px}
.p-hero h1{font-size:22px;font-weight:600}
.p-hero p{color:rgba(255,255,255,.82);font-size:13px;margin-top:6px}
.p-cards{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.p-card{background:#fff;border:1px solid var(--border);border-radius:8px;overflow:hidden}
.p-card .ph{height:110px;background:linear-gradient(135deg,#EFE0DC,#DCC7C9)}
.p-card .pb{padding:14px}
.p-card h3{font-size:14px;font-weight:600;margin-bottom:6px}
.p-card .meta{font-size:12px;color:var(--text3);display:flex;gap:10px;margin-bottom:8px}
.login-wrap{min-height:100vh;display:grid;grid-template-columns:1.1fr .9fr}
.login-bg{background:linear-gradient(140deg,#431B26,#5B2533 55%,#7A3947);position:relative;padding:56px;color:#fff;display:flex;flex-direction:column;justify-content:space-between}
.login-bg h1{font-size:32px;line-height:44px;font-weight:600;letter-spacing:1px}
.login-bg p{color:rgba(255,255,255,.72);margin-top:14px;font-size:14px;max-width:420px}
.login-bg .seal{width:64px;height:64px;border:2px solid rgba(255,255,255,.45);border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:22px;letter-spacing:2px}
.login-form{display:flex;align-items:center;justify-content:center;background:#fff}
.login-box{width:360px}
.login-box h2{font-size:22px;font-weight:600}
.login-box .sub{font-size:13px;color:var(--text3);margin:6px 0 26px}
.fld{margin-bottom:16px}
.fld label{display:block;font-size:13px;color:var(--text2);margin-bottom:6px}
.fld .inp{width:100%;min-width:0;height:42px}
.login-btn{width:100%;height:44px;border:none;border-radius:6px;background:var(--primary);color:#fff;font-size:15px;font-weight:500;cursor:pointer;margin-top:6px}
.tips{margin-top:18px;font-size:12px;color:var(--text3);line-height:22px}
.roles{display:flex;gap:8px;margin-top:14px;flex-wrap:wrap}
"""

MENU = [
    ("工作台", [("dashboard", "校友运营看板", "i-dashboard")]),
    ("校友档案", [("alumni-list", "校友档案", "i-users"), ("cert-audit", "认证审核", "i-verify"), ("change-audit", "变更审核", "i-file")]),
    ("校友组织", [("org-list", "组织管理", "i-org"), ("member-audit", "成员审核", "i-users")]),
    ("活动运营", [("activity-manage", "活动管理", "i-calendar"), ("activity-audit", "活动审核", "i-check"),
                  ("signup-manage", "报名与签到", "i-checkin"), ("activity-archive", "活动归档", "i-archive")]),
    ("捐赠管理", [("project-list", "捐赠项目", "i-donation"), ("donation-record", "线下捐赠登记", "i-money"),
                  ("donation-verify", "捐赠核对", "i-verify"), ("progress-publish", "进展公示", "i-progress"),
                  ("certificate", "感谢证书", "i-cert")]),
    ("创新模块", [("rule", "捐赠公开规则", "i-rule"), ("score", "计算留痕", "i-score")]),
    ("系统", [("user", "用户管理", "i-user"), ("role", "角色管理", "i-role"), ("menu", "菜单管理", "i-menu")]),
]

TAG = {"待审核": "info", "待核对": "info", "草稿": "info", "报名中": "teal", "进行中": "teal", "执行中": "teal",
       "已通过": "ok", "已认证": "ok", "已完成": "ok", "已结项": "ok", "已发放": "ok", "已核对": "ok", "已发布": "ok",
       "候补": "warn", "待验收": "warn", "即将超时": "warn", "已驳回": "danger", "异常": "danger", "已取消": "danger",
       "已退回": "danger", "已归档": "muted", "未开始": "muted", "已停用": "muted", "待发放": "warn", "募集中": "teal"}


def tag(t):
    return f'<span class="tag {TAG.get(t, "muted")}">{t}</span>'


def icon(name):
    return f'<svg class="ico"><use href="#{name}"/></svg>'


def head(title, extra=""):
    return f"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} · 校友活动与捐赠项目管理系统</title><style>{CSS}</style>{extra}</head><body>{SPRITE}"""


def admin(active, crumb, body, role="校友办管理员", right_date="2026-11-01"):
    nav = ""
    for grp, items in MENU:
        nav += f'<div class="grp">{grp}</div>'
        for path, name, ic in items:
            cls = " on" if path == active else ""
            nav += f'<a class="{cls.strip()}" href="{path}.html">{icon(ic)}{name}</a>'
    return f"""<div class="layout"><aside class="side">
<div class="brand"><span class="logo">校</span>校友工作平台</div><div class="nav">{nav}</div></aside>
<div class="main"><header class="top"><div class="crumb">{role} / <b>{crumb}</b></div>
<div class="right"><span class="num">{right_date}</span>{icon("i-bell")}
<span class="who"><span class="avatar"></span><span><b>周敏</b><i>{role}</i></span></span></div></header>
<main class="content">{body}</main></div></div></body></html>"""


def portal(active, body):
    navs = [("index", "首页"), ("activity-square", "活动广场"), ("my-profile", "我的档案"),
            ("public-projects", "捐赠项目"), ("my-signup", "我的报名"), ("my-cert", "我的证书")]
    nav = "".join(f'<a class="{"on" if p == active else ""}" href="{p}.html">{n}</a>' for p, n in navs)
    return f"""<div class="portal"><header class="p-top"><div class="p-brand"><span class="logo">校</span>校友之家</div>
<nav class="p-nav">{nav}</nav>
<div class="right" style="margin-left:auto;display:flex;gap:16px;align-items:center;font-size:12px;color:var(--text3)">
{icon("i-bell")}<span class="who"><span class="avatar"></span><span><b>陈立</b><i>2012级 计算机学院</i></span></span></div>
</header><div class="p-body">{body}</div></div></body></html>"""


def page_head(title, desc, actions=""):
    return f'<div class="page-h"><h1>{title}</h1><p>{desc}</p><div style="margin-left:auto;display:flex;gap:8px">{actions}</div></div>'


def table(headers, rows, aligns=None):
    aligns = aligns or [""] * len(headers)
    th = "".join(f'<th class="{a}">{h}</th>' for h, a in zip(headers, aligns))
    tr = ""
    for r in rows:
        tds = ""
        for cell, a in zip(r, aligns):
            tds += f'<td class="{a}">{cell}</td>'
        tr += f"<tr>{tds}</tr>"
    return f'<table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'


def pager(total=128, pg=1):
    return (f'<div class="pager"><span>共 {total} 条</span><span class="pg">‹</span>'
            f'<span class="pg on">1</span><span class="pg">2</span><span class="pg">3</span>'
            f'<span class="pg">›</span><span>10 条/页</span></div>')


def filt(fields, extra=""):
    s = '<div class="filter">' + "".join(
        f'<div class="{"sel" if t == "sel" else "inp"}">{p}<span class="muted">▾</span></div>' if t == "sel"
        else f'<div class="inp">{p}</div>' for p, t in fields)
    s += f'<button class="btn p">{icon("i-search")}查询</button><button class="btn">重置</button>'
    s += f'<div style="margin-left:auto;display:flex;gap:8px">{extra}</div></div>'
    return s


def card(title, content, right=""):
    h = f'<div class="card-h"><h2>{title}</h2><div class="r">{right}</div></div>' if title else ""
    return f'<div class="card">{h}{content}</div>'


PAGES = {}

# ---------- 登录 ----------
PAGES["login"] = head("登录") + """<div class="login-wrap">
<div class="login-bg"><div><div class="seal">校友</div>
<h1 style="margin-top:26px">校友活动与捐赠<br>项目管理平台</h1>
<p>连接校友、组织活动、公开捐赠进展。所有线下捐赠经财务核对后计入项目实收，匿名捐赠在公开端自动隐藏姓名。</p></div>
<div style="font-size:12px;color:rgba(255,255,255,.55)">高校校友工作办公室 · 仅限授权人员使用</div></div>
<div class="login-form"><div class="login-box">
<h2>登录</h2><div class="sub">请使用校友办分配的账号登录；校友账号可用学号注册后申请认证</div>
<div class="fld"><label>账号</label><div class="inp">admin</div></div>
<div class="fld"><label>密码</label><div class="inp">••••••••</div></div>
<div style="display:flex;justify-content:space-between;font-size:12px;color:var(--text3)">
<span>☑ 记住账号</span><span class="link">忘记密码？</span></div>
<button class="login-btn">登 录</button>
<div class="tips">演示账号：admin / admin123（校友办）· liaison01 / 123456（联络员）<br>
finance01 / 123456（财务）· alumni01 / 123456（校友）</div>
</div></div></div></body></html>"""

# ---------- 看板 ----------
kpis = [("活动参与人数", "2,486", "+12.4%"), ("捐赠项目数", "32", "+3"), ("登记金额", "¥ 4,862,300", "+8.1%"),
        ("里程碑完成率", "68.5%", "+4.2%"), ("校友活跃度", "41.2%", "+1.8%"), ("学院贡献分布", "9 个", "—")]
kpi_html = '<div class="kpis">' + "".join(
    f'<div class="kpi"><h4>{t}</h4><b>{v}</b><span>{d}</span></div>' for t, v, d in kpis) + "</div>"
bars = "".join(f'<div class="bar" style="height:{h}%"><span>{m}</span></div>'
               for h, m in [(48, "6月"), (62, "7月"), (55, "8月"), (78, "9月"), (88, "10月"), (71, "11月")])
trend = f"""<div class="card"><div class="card-h"><h2>捐赠登记趋势（近 6 个月）</h2>
<div class="r">单位：万元 · 默认最近 30 天</div></div><div class="card-b"><div class="chart">{bars}</div>
<div style="height:26px"></div></div></div>"""
donut = """<div class="card"><div class="card-h"><h2>项目状态分布</h2><div class="r">32 个项目</div></div>
<div class="card-b"><div class="donut"></div><div class="legend">
<div><i style="background:#5B2533"></i>募集中 42% · 13</div>
<div><i style="background:#2F6F6A"></i>执行中 26% · 8</div>
<div><i style="background:#7A3947"></i>待验收 18% · 6</div>
<div><i style="background:#B4761F"></i>已结项 14% · 5</div></div></div></div>"""
rank = """<div class="card"><div class="card-h"><h2>学院贡献分布</h2><div class="r">金额 Top 5</div></div>
<div class="card-b"><div class="legend" style="line-height:30px">
<div>计算机学院 <b class="num" style="float:right">¥ 1,286,000</b><div class="prog" style="margin-top:4px"><i style="width:100%"></i></div></div>
<div>经济管理学院 <b class="num" style="float:right">¥ 942,000</b><div class="prog" style="margin-top:4px"><i style="width:74%"></i></div></div>
<div>机械工程学院 <b class="num" style="float:right">¥ 736,500</b><div class="prog" style="margin-top:4px"><i style="width:57%"></i></div></div>
<div>外国语学院 <b class="num" style="float:right">¥ 512,800</b><div class="prog" style="margin-top:4px"><i style="width:40%"></i></div></div>
<div>材料科学学院 <b class="num" style="float:right">¥ 388,000</b><div class="prog" style="margin-top:4px"><i style="width:30%"></i></div></div>
</div></div></div>"""
funil = """<div class="card"><div class="card-h"><h2>活动报名与到场率</h2><div class="r">近 30 天</div></div>
<div class="card-b"><div class="chart">""" + "".join(
    f'<div class="bar" style="height:{h}%;background:linear-gradient(180deg,#2F6F6A,#245954)"><span>{m}</span></div>'
    for h, m in [(92, "报名"), (78, "审核"), (66, "签到"), (58, "归档")]) + """</div><div style="height:26px"></div></div></div>"""
PAGES["dashboard"] = head("看板") + admin("dashboard", "校友运营看板", page_head(
    "校友运营看板", "默认最近 30 天 · 指标与明细总数一致", '<button class="btn">本月</button><button class="btn">本季度</button><button class="btn">本年</button><button class="btn p">导出</button>')
    + kpi_html + '<div style="height:16px"></div>'
    + f'<div class="grid3">{trend}{donut}</div><div style="height:16px"></div>'
    + f'<div class="grid3">{funil}{rank}</div>')

# ---------- 认证审核 ----------
rows = [("A2026001", "陈立", "2012 / 2016", "计算机学院", "软件工程", "120301", tag("待审核"), "2026-10-30 09:24"),
        ("A2026002", "林雅", "2010 / 2014", "经济管理学院", "会计学", "120102", tag("待审核"), "2026-10-30 10:02"),
        ("A2026003", "王海涛", "2008 / 2012", "机械工程学院", "机械设计", "080201", tag("已认证"), "2026-10-29 16:41"),
        ("A2026004", "赵一鸣", "2015 / 2019", "外国语学院", "英语", "050201", tag("已驳回"), "2026-10-29 14:18"),
        ("A2026005", "孙倩", "2013 / 2017", "材料科学学院", "高分子材料", "080407", tag("待审核"), "2026-10-28 11:35"),
        ("A2026006", "周子涵", "2011 / 2015", "计算机学院", "计算机科学", "080901", tag("已认证"), "2026-10-28 09:07")]
PAGES["cert-audit"] = head("认证审核") + admin("cert-audit", "认证审核", page_head(
    "校友认证审核", "核对学号、姓名、入学/毕业年与证明材料，审核通过后建立校友档案",
    '<button class="btn">批量通过</button><button class="btn d">批量驳回</button>')
    + card("筛选", '<div class="card-b">' + filt([("学号 / 姓名 / 手机号", ""), ("认证状态", "sel"), ("院系", "sel"), ("毕业年份", "sel")]) + "</div>")
    + card("待审核认证", table(["认证编号", "姓名", "入学/毕业", "院系", "专业", "班级", "状态", "提交时间", "操作"],
                              [(f'<a class="link">{r[0]}</a>', r[1], r[2], r[3], r[4], r[5], r[6], f'<span class="num">{r[7]}</span>',
                                '<a class="link">审核</a> <a class="link">材料</a>') for r in rows],
                              ["", "", "", "", "", "", "c", "", "c"][:9]) + pager(128, 1),
         "共 128 条 · 待审核 12"))

# ---------- 校友档案 ----------
alumni = [("A2012001", "陈立", "男", "2012", "计算机学院", "软件工程", "上海", "字节跳动 · 技术专家", "138****2210", tag("已认证")),
          ("A2010002", "林雅", "女", "2010", "经济管理学院", "会计学", "北京", "中金公司 · 高级经理", "139****8876", tag("已认证")),
          ("A2008003", "王海涛", "男", "2008", "机械工程学院", "机械设计", "深圳", "比亚迪 · 结构工程师", "137****3345", tag("已认证")),
          ("A2015004", "赵一鸣", "男", "2015", "外国语学院", "英语", "杭州", "自由译者", "135****9902", tag("已驳回")),
          ("A2013005", "孙倩", "女", "2013", "材料科学学院", "高分子材料", "苏州", "协鑫集团 · 研发主管", "136****4418", tag("已认证")),
          ("A2011006", "周子涵", "女", "2011", "计算机学院", "计算机科学", "广州", "腾讯 · 产品经理", "138****7723", tag("已认证"))]
PAGES["alumni-list"] = head("校友档案") + admin("alumni-list", "校友档案", page_head(
    "校友档案", "共 1,284 名已认证校友 · 敏感字段按隐私选项脱敏展示",
    '<button class="btn">导出当前筛选</button><button class="btn p">新建档案</button>')
    + card("筛选", '<div class="card-b">' + filt([("姓名 / 学号 / 单位", ""), ("院系", "sel"), ("毕业年份", "sel"), ("所在地区", "sel"), ("认证状态", "sel")]) + "</div>")
    + card("档案列表", table(["校友编号", "姓名", "性别", "毕业年份", "院系", "专业", "地区", "工作单位 / 职务", "手机", "状态", "操作"],
                            [(f'<a class="link">{a[0]}</a>', a[1], a[2], f'<span class="num">{a[3]}</span>', a[4], a[5], a[6], a[7],
                              f'<span class="num">{a[8]}</span>', a[9], '<a class="link">详情</a> <a class="link">编辑</a> <a class="link">更多</a>')
                             for a in alumni], ["", "", "c", "", "", "", "", "", "", "c", "c"]) + pager(1284, 1),
         "已认证 1,102 · 待认证 12"))

# ---------- 变更审核 ----------
chg = [("C20261028-001", "陈立", "工作单位", "字节跳动 · 工程师", "字节跳动 · 技术专家", "岗位晋升，需更新对外展示信息", tag("待审核"), "2026-10-28 14:22"),
       ("C20261028-002", "林雅", "联系方式", "139****8876", "139****6621", "更换常用手机号", tag("待审核"), "2026-10-28 15:40"),
       ("C20261027-003", "孙倩", "所在地区", "无锡", "苏州", "工作调动至苏州分公司", tag("已通过"), "2026-10-27 09:12"),
       ("C20261026-004", "赵一鸣", "工作单位", "某培训机构", "自由译者", "离职转自由职业", tag("已退回"), "2026-10-26 17:05")]
PAGES["change-audit"] = head("变更审核") + admin("change-audit", "变更审核", page_head(
    "校友信息变更审核", "变更保留历史值；隐私选项关闭的字段不对外展示",
    '<button class="btn">导出</button>')
    + card("待处理变更", table(["申请编号", "校友", "变更项", "变更前", "变更后", "申请理由", "状态", "提交时间", "操作"],
                              [(f'<a class="link">{c[0]}</a>', c[1], c[2], f'<span class="muted">{c[3]}</span>', c[4], c[5], c[6],
                                f'<span class="num">{c[7]}</span>', '<a class="link">通过</a> <a class="link">退回</a>') for c in chg],
                              ["", "", "", "", "", "", "c", "", "c"]) + pager(46, 1), "共 46 条 · 待审核 6"))

# ---------- 组织 ----------
orgs = [("ORG-001", "1998级计算机甲班", "班级", "计算机学院", "上海", 42, "王海涛", tag("已通过")),
        ("ORG-002", "2000级经管校友会", "年级", "经济管理学院", "北京", 128, "林雅", tag("已通过")),
        ("ORG-003", "上海校友会", "地区", "—", "上海", 386, "陈立", tag("已通过")),
        ("ORG-004", "深圳校友会", "地区", "—", "深圳", 254, "王海涛", tag("已通过")),
        ("ORG-005", "智能制造行业联谊会", "行业", "机械工程学院", "全国", 96, "孙倩", tag("待审核")),
        ("ORG-006", "2012级软工二班", "班级", "计算机学院", "广州", 38, "周子涵", tag("已通过"))]
PAGES["org-list"] = head("组织") + admin("org-list", "组织管理", page_head(
    "校友组织管理", "班级 / 年级 / 地区 / 行业四类组织 · 共 68 个",
    '<button class="btn">导出</button><button class="btn p">新建组织</button>')
    + card("筛选", '<div class="card-b">' + filt([("组织名称 / 负责人", ""), ("组织类型", "sel"), ("所属地区", "sel")]) + "</div>")
    + card("组织列表", table(["组织编号", "组织名称", "类型", "挂靠院系", "地区", "成员数", "负责人", "状态", "操作"],
                            [(f'<a class="link">{o[0]}</a>', o[1], o[2], o[3], o[4], f'<span class="num">{o[5]}</span>', o[6], o[7],
                              '<a class="link">详情</a> <a class="link">成员</a> <a class="link">公告</a>') for o in orgs],
                            ["", "", "c", "", "", "r", "", "c", "c"]) + pager(68, 1), "活跃组织 41 · 待审核 3"))

# ---------- 成员审核 ----------
mem = [("陈立", "上海校友会", "成员", "2026-10-28 09:12", tag("待审核")), ("林雅", "2000级经管校友会", "成员", "2026-10-28 10:35", tag("待审核")),
       ("孙倩", "深圳校友会", "成员", "2026-10-27 15:20", tag("已通过")), ("周子涵", "2012级软工二班", "负责人", "2026-10-26 11:08", tag("已通过")),
       ("王海涛", "1998级计算机甲班", "负责人", "2026-10-25 16:44", tag("已通过"))]
PAGES["member-audit"] = head("成员") + admin("member-audit", "成员审核", page_head(
    "组织成员审核", "联络员提交入会申请，管理员确认后计入组织成员数", '<button class="btn p">批量通过</button>')
    + card("入会申请", table(["校友", "申请组织", "申请角色", "申请时间", "状态", "操作"],
                            [(m[0], m[1], m[2], f'<span class="num">{m[3]}</span>', m[4], '<a class="link">通过</a> <a class="link">拒绝</a>') for m in mem],
                            ["", "", "c", "", "c", "c"]) + pager(96, 1), "待审核 9"))

# ---------- 活动管理 ----------
acts = [("ACT-20261101", "计算机学院校友返校日", "返校", "2026-11-18 09:00", "计算机学院报告厅", "120 / 86", "报名中", tag("报名中")),
        ("ACT-20261028", "上海校友会秋季沙龙", "沙龙", "2026-11-09 14:00", "上海静安洲际酒店", "80 / 80", "报名中", tag("报名中")),
        ("ACT-20261025", "校友企业家论坛", "论坛", "2026-11-02 13:30", "学术交流中心", "200 / 152", "待审核", tag("待审核")),
        ("ACT-20261020", "1998级毕业25周年聚会", "聚会", "2026-10-26 10:00", "老校区礼堂", "60 / 58", "已归档", tag("已归档")),
        ("ACT-20261015", "粤港澳校友徒步活动", "文体", "2026-10-19 08:00", "深圳湾公园", "100 / 97", "进行中", tag("进行中"))]
PAGES["activity-manage"] = head("活动") + admin("activity-manage", "活动管理", page_head(
    "活动管理", "活动人数满后新报名自动进入候补，取消后按时间顺序转正",
    '<button class="btn">导出</button><button class="btn p">发起活动</button>')
    + card("筛选", '<div class="card-b">' + filt([("活动名称 / 编号", ""), ("活动类型", "sel"), ("学院", "sel"), ("活动状态", "sel"), ("开始日期", "sel")]) + "</div>")
    + card("活动列表", table(["活动编号", "活动名称", "类型", "开始时间", "地点", "报名 / 容量", "状态", "操作"],
                            [(f'<a class="link">{a[0]}</a>', a[1], a[2], f'<span class="num">{a[3]}</span>', a[4],
                              f'<span class="num">{a[5]}</span>', a[7], '<a class="link">详情</a> <a class="link">报名</a> <a class="link">更多</a>')
                             for a in acts], ["", "", "c", "", "", "r", "c", "c"]) + pager(22, 1), "共 22 个活动"))

# ---------- 活动审核 ----------
PAGES["activity-audit"] = head("活动审核") + admin("activity-audit", "活动审核", page_head(
    "活动审核", "审核活动方案、海报与报名规则，通过后进入报名中", "")
    + card("待审核活动", table(["活动编号", "活动名称", "发起组织", "开始时间", "容量", "审核方式", "状态", "操作"],
                              [("ACT-20261025", "校友企业家论坛", "上海校友会", '<span class="num">2026-11-02 13:30</span>', "200", "人工审核", tag("待审核"),
                                '<a class="link">审核</a> <a class="link">查看海报</a>'),
                               ("ACT-20261024", "新材料产业趋势分享", "智能制造行业联谊会", '<span class="num">2026-11-06 19:00</span>', "60", "自动通过", tag("待审核"),
                                '<a class="link">审核</a> <a class="link">查看海报</a>')],
                              ["", "", "", "", "r", "c", "c", "c"]) + pager(5, 1), "待审核 5")
    + '<div style="height:16px"></div>'
    + card("审核抽屉（示意）", '<div class="card-b"><div style="display:grid;grid-template-columns:1fr 380px;gap:20px">'
           '<div><dl class="dl"><dt>活动编号</dt><dd>ACT-20261025</dd><dt>活动名称</dt><dd>校友企业家论坛</dd>'
           '<dt>发起组织</dt><dd>上海校友会</dd><dt>时间地点</dt><dd>2026-11-02 13:30 · 学术交流中心</dd>'
           '<dt>人数 / 审核</dt><dd>200 人 · 人工审核</dd><dt>日程</dt><dd>签到 → 主题演讲 → 圆桌对话 → 自由交流</dd></dl>'
           '<div class="note" style="margin-top:14px">退回与驳回必须填写原因，原因不少于 5 个字；审批结果同步至发起人站内消息。</div></div>'
           '<div style="border:1px solid var(--border);border-radius:8px;padding:16px">'
           '<div class="hint">审批意见</div><div class="inp" style="width:100%;height:88px;align-items:flex-start;padding-top:8px;margin:8px 0 12px">请填写审核意见（≥5 字）</div>'
           '<div style="display:flex;gap:8px;justify-content:flex-end"><button class="btn">取消</button>'
           '<button class="btn d">驳回</button><button class="btn p">通过</button></div></div></div></div>'))

# ---------- 活动广场（门户） ----------
pcards = ""
for t, ty, tm, loc, cnt in [("计算机学院校友返校日", "返校", "11-18 09:00", "计算机学院报告厅", "86 / 120"),
                            ("上海校友会秋季沙龙", "沙龙", "11-09 14:00", "静安洲际酒店", "已满 · 候补 6"),
                            ("校友企业家论坛", "论坛", "11-02 13:30", "学术交流中心", "152 / 200"),
                            ("粤港澳校友徒步", "文体", "10-19 08:00", "深圳湾公园", "97 / 100"),
                            ("新材料产业趋势分享", "沙龙", "11-06 19:00", "线上直播", "38 / 60"),
                            ("1998级毕业25周年", "聚会", "10-26 10:00", "老校区礼堂", "58 / 60")]:
    pcards += f"""<div class="p-card"><div class="ph"></div><div class="pb"><h3>{t}</h3>
<div class="meta"><span>{ty}</span><span>·</span><span class="num">{tm}</span></div>
<div class="meta">{loc}</div>
<div style="display:flex;align-items:center;gap:10px;margin-top:8px"><div class="prog" style="flex:1"><i style="width:72%"></i></div>
<span class="hint num">{cnt}</span></div>
<div style="margin-top:12px;display:flex;gap:8px"><button class="btn p sm">报名</button><button class="btn sm">详情</button></div></div></div>"""
PAGES["activity-square"] = head("活动广场") + portal("activity-square",
    '<div class="p-hero"><h1>活动广场</h1><p>报名成功后将收到签到验证码；人数已满时自动进入候补，有人取消后按报名时间顺序转正。</p></div>'
    '<div class="chips" style="margin-bottom:16px"><span class="chip on">全部</span><span class="chip">返校</span>'
    '<span class="chip">沙龙</span><span class="chip">论坛</span><span class="chip">文体</span><span class="chip">公益</span></div>'
    f'<div class="p-cards">{pcards}</div>')

# ---------- 报名与签到 ----------
signs = [("S20261101001", "陈立", "计算机学院校友返校日", "已报名", "1", tag("已报名"), "2026-10-30 09:12", "—"),
         ("S20261101002", "林雅", "计算机学院校友返校日", "候补", "0", tag("候补"), "2026-10-30 09:40", "—"),
         ("S20261101003", "孙倩", "上海校友会秋季沙龙", "候补", "2", tag("候补"), "2026-10-30 10:05", "—"),
         ("S20261028004", "王海涛", "粤港澳校友徒步", "已签到", "0", tag("已签到"), "2026-10-18 20:14", "2026-10-19 08:06"),
         ("S20261028005", "周子涵", "粤港澳校友徒步", "未到场", "1", tag("未到场"), "2026-10-18 21:02", "—")]
PAGES["signup-manage"] = head("签到") + admin("signup-manage", "报名与签到", page_head(
    "报名与签到", "现场使用 6 位验证码签到，支持手工补签并留痕",
    '<button class="btn">导出名单</button><button class="btn p">手工签到</button>')
    + '<div class="kpis" style="grid-template-columns:repeat(4,1fr);margin-bottom:16px">'
    + "".join(f'<div class="kpi"><h4>{t}</h4><b>{v}</b><span>{d}</span></div>'
              for t, v, d in [("报名总数", "86", "含候补 6"), ("已签到", "64", "到场率 74.4%"),
                              ("候补转正", "4", "本月"), ("未到场", "22", "已发提醒")]) + "</div>"
    + card("报名名单", table(["报名编号", "校友", "活动", "状态", "同行人数", "报名时间", "签到时间", "操作"],
                            [(f'<a class="link">{s[0]}</a>', s[1], s[2], s[5], f'<span class="num">{s[3]}</span>',
                              f'<span class="num">{s[6]}</span>', f'<span class="num">{s[7]}</span>',
                              '<a class="link">补签</a> <a class="link">转正</a> <a class="link">取消</a>') for s in signs],
                            ["", "", "", "c", "r", "", "", "c"]) + pager(86, 1), "活动：计算机学院校友返校日"))

# ---------- 活动归档 ----------
PAGES["activity-archive"] = head("归档") + admin("activity-archive", "活动归档", page_head(
    "活动归档", "归档后记录实际人数、照片、新闻稿、费用摘要与反馈，活动状态转为已归档", "")
    + '<div class="split"><div>' + card("归档信息", '<div class="card-b">'
        '<div class="steps" style="margin-bottom:22px"><div class="st done">待审核</div><div class="st done">报名中</div>'
        '<div class="st done">进行中</div><div class="st now">已归档</div></div>'
        '<dl class="dl"><dt>活动编号</dt><dd>ACT-20261020 · 1998级毕业25周年聚会</dd>'
        '<dt>计划 / 实际</dt><dd class="num">60 人 / 58 人（到场 55 人）</dd>'
        '<dt>费用摘要</dt><dd class="num">场地 ¥ 6,800 · 餐饮 ¥ 12,400 · 物料 ¥ 2,300 · 合计 ¥ 21,500</dd>'
        '<dt>新闻稿</dt><dd><a class="link">1998级校友重返母校，共叙廿五载情谊</a></dd>'
        '<dt>活动总结</dt><dd>到场 55 人，反馈满意度 4.8 / 5；现场募集班级基金 ¥ 86,000，已登记至「98级班级基金」项目。</dd></dl>'
        '<div style="margin-top:16px"><div class="hint" style="margin-bottom:8px">现场照片（6 张）</div>'
        '<div class="thumbs"><div></div><div></div><div></div><div></div><div></div><div></div></div></div>'
        '</div></div></div><div>') + card("反馈摘要", '<div class="card-b">'
        '<div class="legend" style="line-height:30px"><div>组织安排 <b style="float:right">4.9</b></div>'
        '<div>场地餐饮 <b style="float:right">4.6</b></div><div>交流收获 <b style="float:right">4.8</b></div>'
        '<div>整体满意度 <b style="float:right">4.8</b></div></div>'
        '<div class="note" style="margin-top:12px">共收到 42 份反馈，其中 3 条建议增加自由交流时间。</div>'
        '</div></div></div>'))

# ---------- 捐赠项目 ----------
projs = [("PJ-2026001", "计算机学院实验楼改造基金", "计算机学院", "1,000,000", "682,000", "68.2%", tag("募集中"), "李建国"),
         ("PJ-2026002", "寒门学子助学金", "校友办", "500,000", "468,000", "93.6%", tag("执行中"), "周敏"),
         ("PJ-2026003", "图书馆古籍修复计划", "图书馆", "300,000", "216,000", "72.0%", tag("执行中"), "张倩"),
         ("PJ-2026004", "校友创新创业基金", "创新创业学院", "2,000,000", "1,240,000", "62.0%", tag("募集中"), "陈立"),
         ("PJ-2026005", "校园银杏林认养", "后勤保障处", "120,000", "120,000", "100%", tag("待验收"), "王海涛"),
         ("PJ-2026006", "98级班级基金", "计算机学院", "200,000", "186,000", "93.0%", tag("已结项"), "林雅")]
PAGES["project-list"] = head("捐赠项目") + admin("project-list", "捐赠项目", page_head(
    "捐赠项目", "项目目标拆分为里程碑，线下收款经财务核对后计入实收",
    '<button class="btn">导出当前筛选</button><button class="btn p">新建项目</button>')
    + card("筛选", '<div class="card-b">' + filt([("项目编号 / 名称", ""), ("发起单位", "sel"), ("项目状态", "sel"), ("公开状态", "sel"), ("起止日期", "sel")]) + "</div>")
    + card("项目列表", table(["项目编号", "项目名称", "发起单位", "目标金额", "已登记", "完成度", "状态", "负责人", "操作"],
                            [(f'<a class="link">{p[0]}</a>', p[1], p[2], f'<span class="num">¥ {p[3]}</span>', f'<span class="num">¥ {p[4]}</span>',
                              f'<div class="prog" style="width:90px"><i style="width:{p[5]}"></i></div>', p[6], p[7],
                              '<a class="link">详情</a> <a class="link">进展</a> <a class="link">更多</a>') for p in projs],
                            ["", "", "", "r", "r", "", "c", "", "c"]) + pager(32, 1), "共 32 个项目"))

# ---------- 项目详情 ----------
PAGES["project-detail"] = head("项目详情") + admin("project-detail", "捐赠项目 / 详情", page_head(
    "计算机学院实验楼改造基金", "PJ-2026001 · 募集中 · 负责人 李建国", '<button class="btn">导出</button><button class="btn p">发布进展</button>')
    + card("", '<div class="card-b"><div style="display:flex;gap:20px;align-items:flex-start">'
        '<div style="width:220px;height:132px;border-radius:6px;background:linear-gradient(135deg,#7A3947,#5B2533)"></div>'
        '<div style="flex:1"><div style="display:flex;gap:10px;align-items:center"><b style="font-size:16px">计算机学院实验楼改造基金</b>'
        + tag("募集中") + tag("公开") + '</div>'
        '<div class="hint" style="margin:6px 0 12px">用于实验楼三层机房改造与设备更新，覆盖 6 间实验室、受益学生约 1,200 人。</div>'
        '<div class="kpis" style="grid-template-columns:repeat(4,1fr)">'
        '<div class="kpi"><h4>目标金额</h4><b style="font-size:22px">¥ 1,000,000</b></div>'
        '<div class="kpi"><h4>已登记金额</h4><b style="font-size:22px">¥ 682,000</b><span>完成 68.2%</span></div>'
        '<div class="kpi"><h4>已支出</h4><b style="font-size:22px">¥ 320,000</b><span>凭证 12 份</span></div>'
        '<div class="kpi"><h4>受益人数</h4><b style="font-size:22px">1,200</b><span>覆盖 6 间实验室</span></div></div></div></div></div>')
    + '<div style="height:16px"></div><div class="split"><div>'
    + card("里程碑", '<div class="card-b"><div class="tl">'
        '<div class="it done"><b>方案设计与预算评审</b><em class="num">2026-05-18</em><p>完成改造方案与预算评审，预算 ¥ 1,000,000</p></div>'
        '<div class="it done"><b>一期机房改造</b><em class="num">2026-08-30</em><p>3 间机房完成改造，支出 ¥ 320,000，凭证 12 份</p></div>'
        '<div class="it now"><b>二期设备采购</b><em class="num">进行中 · 计划 2026-11-30</em><p>待采购服务器 8 台，预算 ¥ 260,000</p></div>'
        '<div class="it"><b>验收与结项</b><em>计划 2026-12-20</em><p>完成验收并发布结项报告</p></div></div></div>')
    + card("关联捐赠记录", table(["登记编号", "捐赠人", "金额", "捐赠日期", "核对状态", "是否匿名"],
                                [('<a class="link">DN-20261012-08</a>', "陈立", '<span class="num">¥ 50,000</span>', '<span class="num">2026-10-12</span>', tag("已核对"), "否"),
                                 ('<a class="link">DN-20261008-03</a>', "匿名校友", '<span class="num">¥ 200,000</span>', '<span class="num">2026-10-08</span>', tag("已核对"), "是"),
                                 ('<a class="link">DN-20260928-11</a>', "字节跳动（企业）", '<span class="num">¥ 120,000</span>', '<span class="num">2026-09-28</span>', tag("已核对"), "否"),
                                 ('<a class="link">DN-20261029-02</a>', "林雅", '<span class="num">¥ 30,000</span>', '<span class="num">2026-10-29</span>', tag("待核对"), "否")],
                                ["", "", "r", "", "c", "c"]) + pager(28, 1))
    + '</div><div>' + card("公开进度（创新模块）", '<div class="card-b">'
        '<div style="text-align:center;padding:8px 0 14px"><div class="hint">综合公开等级</div>'
        '<b style="font-size:30px;color:var(--primary)">推荐</b><div class="hint num">总分 82.4 / 100 · 规则 v3</div></div>'
        '<div class="legend" style="line-height:28px">'
        '<div>目标金额得分 <b style="float:right">18.0</b></div><div>已登记金额 <b style="float:right">26.5</b></div>'
        '<div>里程碑完成度 <b style="float:right">16.0</b></div><div>支出凭证 <b style="float:right">12.0</b></div>'
        '<div>受益人数 <b style="float:right">7.5</b></div><div>公开审核状态 <b style="float:right">2.4</b></div></div>'
        '<div class="note" style="margin-top:12px"><b>可改进项：</b>二期设备采购尚未启动，里程碑完成度偏低；建议补充 2 份设备采购预算凭证。</div>'
        '<div style="margin-top:10px"><a class="link">查看计算明细</a></div></div>')
    + '</div></div>')

# ---------- 线下捐赠登记 ----------
dons = [("DN-20261029-01", "PJ-2026002 寒门学子助学金", "陈立", "校友", "30,000.00", "2026-10-29", tag("待核对"), "否", "是"),
        ("DN-20261029-02", "PJ-2026001 实验楼改造基金", "林雅", "校友", "30,000.00", "2026-10-29", tag("待核对"), "否", "是"),
        ("DN-20261028-05", "PJ-2026004 创新创业基金", "华为技术有限公司", "企业", "500,000.00", "2026-10-28", tag("已核对"), "否", "是"),
        ("DN-20261027-02", "PJ-2026003 古籍修复计划", "匿名校友", "校友", "80,000.00", "2026-10-27", tag("已核对"), "是", "否"),
        ("DN-20261026-09", "PJ-2026005 银杏林认养", "王海涛", "校友", "5,000.00", "2026-10-26", tag("已退回"), "否", "否")]
PAGES["donation-record"] = head("捐赠登记") + admin("donation-record", "线下捐赠登记", page_head(
    "线下捐赠登记", "不接入在线支付；登记后须经财务核对才计入项目实收",
    '<button class="btn">导出</button><button class="btn p">登记捐赠</button>')
    + card("筛选", '<div class="card-b">' + filt([("登记编号 / 捐赠人", ""), ("意向项目", "sel"), ("捐赠人类型", "sel"), ("核对状态", "sel"), ("捐赠日期", "sel")]) + "</div>")
    + card("登记记录", table(["登记编号", "意向项目", "捐赠人", "类型", "金额（元）", "捐赠日期", "核对状态", "匿名", "开证明", "操作"],
                            [(f'<a class="link">{d[0]}</a>', d[1], d[2], d[3], f'<span class="num">{d[4]}</span>', f'<span class="num">{d[5]}</span>',
                              d[6], d[7], d[8], '<a class="link">详情</a> <a class="link">凭证</a>') for d in dons],
                            ["", "", "", "c", "r", "", "c", "c", "c", "c"]) + pager(186, 1), "共 186 条 · 待核对 7")
    + '<div style="height:16px"></div>'
    + card("登记表单（示意）", '<div class="card-b"><div style="display:grid;grid-template-columns:1fr 1fr;gap:16px 24px">'
        '<div><div class="hint">项目编号</div><div class="inp" style="width:100%;background:#F7F3F2">PJ-2026002（后端生成）</div></div>'
        '<div><div class="hint">捐赠人</div><div class="inp" style="width:100%">陈立</div></div>'
        '<div><div class="hint">捐赠金额</div><div class="inp" style="width:100%">30,000.00</div></div>'
        '<div><div class="hint">捐赠日期</div><div class="inp" style="width:100%">2026-10-29</div></div>'
        '<div><div class="hint">捐赠意向</div><div class="inp" style="width:100%">用于 2026 级新生助学金发放</div></div>'
        '<div><div class="hint">凭证上传</div><div class="inp" style="width:100%;height:72px;color:var(--text3)">＋ 点击或拖拽上传（图片 / PDF，≤20MB）</div></div>'
        '</div><div style="display:flex;gap:20px;margin-top:14px;font-size:13px;color:var(--text2)">'
        '<span>☑ 匿名捐赠（公开端隐藏姓名）</span><span>☑ 开具捐赠证明</span></div></div>'))

# ---------- 捐赠核对 ----------
PAGES["donation-verify"] = head("核对") + admin("donation-verify", "捐赠核对", page_head(
    "捐赠核对", "核对银行流水与凭证；退回须填写原因（≥5 字），核对后自动计入项目实收",
    '<button class="btn">导出对账表</button>')
    + '<div class="kpis" style="grid-template-columns:repeat(5,1fr);margin-bottom:16px">'
    + "".join(f'<div class="kpi"><h4>{t}</h4><b>{v}</b><span>{d}</span></div>'
              for t, v, d in [("本月登记", "¥ 862,000", "31 笔"), ("已核对", "¥ 743,000", "24 笔"),
                              ("待核对", "¥ 96,000", "7 笔"), ("已退回", "¥ 23,000", "2 笔"), ("证书待发", "18", "张")]) + "</div>"
    + card("待核对清单", table(["登记编号", "项目", "捐赠人", "金额", "凭证", "登记人", "登记时间", "操作"],
                               [('<a class="link">DN-20261029-01</a>', "寒门学子助学金", "陈立", '<span class="num">¥ 30,000.00</span>',
                                 '<a class="link">查看凭证</a>', "周敏", '<span class="num">2026-10-29 10:12</span>',
                                 '<a class="link">通过</a> <a class="link">退回</a>'),
                                ('<a class="link">DN-20261029-02</a>', "实验楼改造基金", "林雅", '<span class="num">¥ 30,000.00</span>',
                                 '<a class="link">查看凭证</a>', "周敏", '<span class="num">2026-10-29 11:40</span>',
                                 '<a class="link">通过</a> <a class="link">退回</a>'),
                                ('<a class="link">DN-20261029-03</a>', "银杏林认养", "孙倩", '<span class="num">¥ 3,000.00</span>',
                                 '<span class="muted">未上传</span>', "张倩", '<span class="num">2026-10-29 15:02</span>',
                                 '<a class="link">通过</a> <a class="link">退回</a>')],
                               ["", "", "", "r", "c", "", "", "c"]) + pager(7, 1), "待核对 7 笔 · 合计 ¥ 96,000")
    + '<div style="height:16px"></div>' + f'<div class="grid2">{card("资金用途登记", table(["用途", "金额", "凭证数", "登记时间"], [("机房改造一期", "¥ 320,000", "12", '<span class="num">2026-09-02</span>'), ("服务器采购", "¥ 96,000", "3", '<span class="num">2026-10-15</span>')], ["", "r", "c", ""]) + pager(12, 1))}{card("收据状态", table(["收据号", "捐赠人", "金额", "状态"], [("RC-20261028-01", "华为技术有限公司", "¥ 500,000.00", tag("已发放")), ("RC-20261027-02", "匿名校友", "¥ 80,000.00", tag("待发放"))], ["", "", "r", "c"]) + pager(18, 1))}</div>')

# ---------- 进展公示 ----------
PAGES["progress-publish"] = head("公示") + admin("progress-publish", "进展公示", page_head(
    "项目进展公示", "按阶段发布资金使用摘要、成果照片与结项报告，审核通过后对外公开",
    '<button class="btn p">发布进展</button>')
    + '<div class="split"><div>' + card("进展记录", '<div class="card-b"><div class="tl">'
        '<div class="it done"><b>一期机房改造完成</b><em class="num">2026-08-30 · 已发布</em>'
        '<p>3 间机房完成改造，支出 ¥ 320,000，附凭证 12 份、现场照片 8 张。</p>'
        '<div class="thumbs" style="margin-top:8px"><div></div><div></div><div></div><div></div></div></div>'
        '<div class="it now"><b>二期设备采购启动</b><em class="num">2026-10-20 · 待审核</em>'
        '<p>已签订服务器采购合同，预算 ¥ 260,000，预计 11 月底到货安装。</p></div>'
        '<div class="it"><b>阶段验收</b><em>计划 2026-12-10</em><p>验收通过后发布结项报告。</p></div></div></div>')
    + card("资金使用摘要", table(["阶段", "预算", "实际支出", "凭证", "公示状态"],
                                [("一期机房改造", "¥ 340,000", "¥ 320,000", "12 份", tag("已发布")),
                                 ("二期设备采购", "¥ 260,000", "¥ 96,000", "3 份", tag("待审核")),
                                 ("验收与结项", "¥ 40,000", "—", "—", tag("未开始"))],
                                ["", "r", "r", "c", "c"]))
    + '</div><div>' + card("发布检查（创新模块）", '<div class="card-b">'
        '<div class="hint">发布前自动计算公开等级</div>'
        '<div style="text-align:center;padding:10px 0"><b style="font-size:28px;color:var(--primary)">推荐</b>'
        '<div class="hint num">82.4 分 · 规则 v3 · 2026-10-20 15:40</div></div>'
        f'<div class="note"><b>主要影响因素：</b>已登记金额达成 68.2%，权重 25 得 26.5 分；支出凭证齐全，得 12 分。</div>'
        f'<div class="note" style="margin-top:10px"><b>未满足条件：</b>里程碑完成度 55%，低于 80% 的推荐门槛。</div>'
        f'<div style="margin-top:12px;display:flex;gap:8px"><button class="btn sm">查看明细</button><button class="btn sm">人工修正</button></div>'
        '</div>') + '</div></div>')

# ---------- 证书 ----------
PAGES["certificate"] = head("证书") + admin("certificate", "感谢证书", page_head(
    "感谢证书", "仅对已核对成功的捐赠记录生成证书；编号由后端生成，支持电子证书与发放记录",
    '<button class="btn">批量生成</button><button class="btn p">导出编号表</button>')
    + card("证书列表", table(["证书编号", "捐赠人", "关联项目", "金额", "签发日期", "发放状态", "操作"],
                            [('<a class="link">TC-2026-000186</a>', "华为技术有限公司", "校友创新创业基金", '<span class="num">¥ 500,000.00</span>',
                              '<span class="num">2026-10-29</span>', tag("已发放"), '<a class="link">查看</a> <a class="link">重发</a>'),
                             ('<a class="link">TC-2026-000185</a>', "陈立", "寒门学子助学金", '<span class="num">¥ 30,000.00</span>',
                              '<span class="num">2026-10-29</span>', tag("待发放"), '<a class="link">查看</a> <a class="link">发放</a>'),
                             ('<a class="link">TC-2026-000184</a>', "匿名校友", "图书馆古籍修复计划", '<span class="num">¥ 80,000.00</span>',
                              '<span class="num">2026-10-28</span>', tag("已发放"), '<a class="link">查看</a> <a class="link">重发</a>'),
                             ('<a class="link">TC-2026-000183</a>', "王海涛", "校园银杏林认养", '<span class="num">¥ 5,000.00</span>',
                              '<span class="num">2026-10-27</span>', tag("已发放"), '<a class="link">查看</a> <a class="link">重发</a>')],
                            ["", "", "", "r", "", "c", "c"]) + pager(186, 1), "已发放 168 · 待发放 18")
    + '<div style="height:16px"></div>'
    + card("电子证书预览", '<div class="card-b" style="display:flex;gap:24px;align-items:center">'
        '<div style="width:420px;height:280px;border:1px solid var(--border);border-radius:6px;padding:26px;background:linear-gradient(160deg,#fff,#FBF6F4);text-align:center">'
        '<div class="hint" style="letter-spacing:4px">捐 赠 感 谢 证 书</div>'
        '<div style="font-size:18px;font-weight:600;margin-top:18px">华为技术有限公司</div>'
        '<div style="font-size:13px;color:var(--text2);margin-top:14px;line-height:24px">感谢您向「校友创新创业基金」捐赠人民币<br>'
        '<b class="num" style="font-size:16px">伍拾万元整（¥ 500,000.00）</b><br>您的支持将用于学生创业项目孵化。</div>'
        '<div class="hint num" style="margin-top:20px">证书编号 TC-2026-000186 · 2026-10-29</div></div>'
        '<div><dl class="dl"><dt>关联捐赠</dt><dd>DN-20261028-05</dd><dt>核对状态</dt><dd>' + tag("已核对") + '</dd>'
        '<dt>匿名处理</dt><dd>否（显示单位全称）</dd><dt>发放方式</dt><dd>电子邮件 + 纸质邮寄</dd></dl>'
        '<div class="note" style="margin-top:12px">匿名捐赠证书对外展示为「匿名校友」，内部档案保留真实姓名。</div></div></div>'))

# ---------- 规则配置 ----------
weights = [("目标金额", 15, "按目标金额区间分段给分"), ("已登记金额", 25, "按已登记/目标比例线性给分，封顶 100"),
           ("里程碑完成度", 20, "按已完成里程碑权重占比"), ("支出凭证", 15, "凭证份数与支出匹配度"),
           ("受益人数", 15, "按受益人数分段"), ("公开审核状态", 10, "已审核通过得满分，待审核得 30%")]
wrow = "".join(f'<tr><td>{n}</td><td class="r num">{w}%</td><td class="muted">{d}</td>'
               f'<td class="c"><div class="inp" style="width:88px;height:28px;justify-content:center">{w}</div></td></tr>'
               for n, w, d in weights)
PAGES["rule"] = head("规则") + admin("rule", "捐赠公开规则", page_head(
    "捐赠公开规则配置", "权重合计必须等于 100%，修改后记录版本与生效时间", '<button class="btn p">保存并生成新版本</button>')
    + '<div class="split"><div>' + card("权重配置 · 版本 v3（生效中）", table(["输入因素", "当前权重", "取数规则", "调整"], [], ["", "r", "", "c"])
        .replace("</tbody>", wrow + "</tbody>") + '<div class="card-b" style="border-top:1px solid #EFE8E5;display:flex;gap:12px;align-items:center">'
        '<span class="hint">权重合计</span><b class="num" style="color:var(--success)">100%</b>'
        '<span class="hint" style="margin-left:auto">等级阈值：≥80 推荐 · 60–79 观察 · &lt;60 不推荐</span></div>')
    + card("版本记录", table(["版本", "创建人", "生效时间", "状态", "说明"],
                             [("v3", "周敏", '<span class="num">2026-09-01 00:00</span>', tag("已发布"), "提高里程碑权重，降低目标金额权重"),
                              ("v2", "周敏", '<span class="num">2026-06-01 00:00</span>', tag("已停用"), "新增公开审核状态因素"),
                              ("v1", "系统", '<span class="num">2026-03-01 00:00</span>', tag("已停用"), "初始版本")],
                             ["", "", "", "c", ""]))
    + '</div><div>' + card("计算说明", '<div class="card-b"><div class="note">'
        '每项因素先折算为 0–100 分，再乘权重累加为总分；缺失数据不参与计算并在结果中提示补录。'
        '每次计算保存输入快照与规则版本，修改权重只影响新计算或主动重算的数据。</div>'
        '<div class="legend" style="line-height:30px;margin-top:12px"><div>总分 ≥ 80 <b style="float:right">推荐</b></div>'
        '<div>60 ≤ 总分 &lt; 80 <b style="float:right">观察</b></div><div>总分 &lt; 60 <b style="float:right">不推荐</b></div></div></div>')
    + card("近 30 天结果分布", '<div class="card-b"><div class="legend" style="line-height:30px">'
        '<div>推荐 <b style="float:right">18 · 56.3%</b><div class="prog" style="margin-top:4px"><i style="width:56%"></i></div></div>'
        '<div>观察 <b style="float:right">9 · 28.1%</b><div class="prog" style="margin-top:4px"><i style="width:28%"></i></div></div>'
        '<div>不推荐 <b style="float:right">5 · 15.6%</b><div class="prog" style="margin-top:4px"><i style="width:16%"></i></div></div>'
        '</div><div class="note" style="margin-top:12px">人工调整率 12.5%，推荐采纳率 87.5%。</div></div>')
    + '</div></div>')

# ---------- 计算留痕 ----------
PAGES["score"] = head("留痕") + admin("score", "计算留痕", page_head(
    "计算留痕与人工修正", "每次计算保存输入快照、规则版本与明细分；人工修正不覆盖原始结果", '<button class="btn">导出</button>')
    + card("计算记录", table(["计算编号", "项目", "规则版本", "总分", "原始等级", "人工调整", "计算时间", "操作"],
                             [('<a class="link">SC-20261020-014</a>', "计算机学院实验楼改造基金", "v3", '<span class="num">82.4</span>', tag("推荐"), "—", '<span class="num">2026-10-20 15:40</span>', '<a class="link">明细</a>'),
                              ('<a class="link">SC-20261019-013</a>', "寒门学子助学金", "v3", '<span class="num">91.2</span>', tag("推荐"), "—", '<span class="num">2026-10-19 09:12</span>', '<a class="link">明细</a>'),
                              ('<a class="link">SC-20261018-012</a>', "校园银杏林认养", "v3", '<span class="num">64.8</span>', tag("观察"), '<span class="tag warn">人工调整为推荐</span>', '<span class="num">2026-10-18 16:20</span>', '<a class="link">明细</a>'),
                              ('<a class="link">SC-20261015-011</a>', "图书馆古籍修复计划", "v3", '<span class="num">76.5</span>', tag("观察"), "—", '<span class="num">2026-10-15 11:02</span>', '<a class="link">明细</a>')],
                             ["", "", "c", "r", "c", "c", "", "c"]) + pager(32, 1))
    + '<div style="height:16px"></div><div class="split"><div>'
    + card("计算明细 · SC-20261020-014", '<div class="card-b">'
        '<table><thead><tr><th>因素</th><th class="r">输入值</th><th class="r">得分</th><th class="r">权重</th><th class="r">加权分</th><th>说明</th></tr></thead><tbody>'
        '<tr><td>目标金额</td><td class="r num">1,000,000</td><td class="r num">100</td><td class="r num">15%</td><td class="r num">15.0</td><td class="muted">落入 ≥100 万区间</td></tr>'
        '<tr><td>已登记金额</td><td class="r num">682,000</td><td class="r num">68</td><td class="r num">25%</td><td class="r num">17.0</td><td class="muted">682,000 / 1,000,000</td></tr>'
        '<tr><td>里程碑完成度</td><td class="r num">55%</td><td class="r num">55</td><td class="r num">20%</td><td class="r num">11.0</td><td class="muted">2 / 4 里程碑完成</td></tr>'
        '<tr><td>支出凭证</td><td class="r num">12 份</td><td class="r num">80</td><td class="r num">15%</td><td class="r num">12.0</td><td class="muted">凭证与支出匹配良好</td></tr>'
        '<tr><td>受益人数</td><td class="r num">1,200</td><td class="r num">50</td><td class="r num">15%</td><td class="r num">7.5</td><td class="muted">分段 1,000–1,499</td></tr>'
        '<tr><td>公开审核状态</td><td class="r num">已通过</td><td class="r num">24</td><td class="r num">10%</td><td class="r num">2.4</td><td class="muted">进展公示已审核</td></tr>'
        '</tbody><tfoot><tr><td><b>合计</b></td><td></td><td></td><td class="r num"><b>100%</b></td><td class="r num"><b>64.9</b></td><td class="muted">含里程碑加成 +17.5 → 82.4</td></tr></tfoot></table>'
        '</div>')
    + '</div><div>' + card("人工修正记录", '<div class="card-b">'
        '<dl class="dl"><dt>原始等级</dt><dd>' + tag("观察") + '</dd><dt>修正后</dt><dd>' + tag("推荐") + '</dd>'
        '<dt>修正人</dt><dd>周敏（校友办管理员）</dd><dt>修正时间</dt><dd class="num">2026-10-20 16:05</dd></dl>'
        '<div class="note" style="margin-top:12px"><b>修正原因：</b>项目已完成一期改造并发布公示，受益人数统计口径尚未更新，按实际执行情况上调。</div>'
        '<div class="hint" style="margin-top:10px">原始计算结果与修正记录同时留痕，任何角色不得覆盖原始值。</div>'
        '</div>') + '</div></div>')

# ---------- 公开端 ----------
pub = ""
for t, org, pct, amt, st in [("计算机学院实验楼改造基金", "计算机学院", 68, "682,000", "募集中"),
                             ("寒门学子助学金", "校友办", 94, "468,000", "执行中"),
                             ("图书馆古籍修复计划", "图书馆", 72, "216,000", "执行中"),
                             ("校友创新创业基金", "创新创业学院", 62, "1,240,000", "募集中"),
                             ("校园银杏林认养", "后勤保障处", 100, "120,000", "待验收"),
                             ("98级班级基金", "计算机学院", 93, "186,000", "已结项")]:
    pub += f"""<div class="p-card"><div class="ph"></div><div class="pb">
<div style="display:flex;gap:8px;align-items:center"><h3 style="flex:1">{t}</h3>{tag(st)}</div>
<div class="meta" style="margin-top:6px"><span>{org}</span><span>·</span><span>更新于 2026-10-20</span></div>
<div style="display:flex;justify-content:space-between;font-size:12px;color:var(--text2);margin:10px 0 4px">
<span>已登记 <b class="num">¥ {amt}</b></span><span class="num">{pct}%</span></div>
<div class="prog"><i style="width:{pct}%"></i></div>
<div style="margin-top:12px;display:flex;gap:8px"><button class="btn sm">查看进展</button><button class="btn sm p">我要捐赠</button></div>
</div></div>"""
PAGES["public-projects"] = head("捐赠项目") + portal("public-projects",
    '<div class="p-hero"><h1>捐赠项目公开进展</h1><p>本页所有数据来自项目进展公示审核结果；匿名捐赠不显示姓名，仅显示「匿名校友」。</p></div>'
    '<div class="chips" style="margin-bottom:16px"><span class="chip on">全部项目</span><span class="chip">助学</span>'
    '<span class="chip">基建</span><span class="chip">科研</span><span class="chip">文体</span></div>'
    f'<div class="p-cards">{pub}</div>')

# ---------- 我的档案 ----------
PAGES["my-profile"] = head("我的档案") + portal("my-profile",
    '<div class="p-hero"><h1>我的校友档案</h1><p>认证状态：已认证 · 档案编号 A2012001 · 最近更新 2026-10-28</p></div>'
    '<div class="split"><div>' + card("基础信息", '<div class="card-b"><dl class="dl">'
        '<dt>姓名</dt><dd>陈立</dd><dt>学号</dt><dd class="num">1203010018</dd>'
        '<dt>入学 / 毕业</dt><dd class="num">2012 / 2016</dd><dt>院系 / 专业</dt><dd>计算机学院 · 软件工程</dd>'
        '<dt>班级</dt><dd>120301</dd><dt>工作单位</dt><dd>字节跳动 · 技术专家</dd>'
        '<dt>所在地区</dt><dd>上海</dd><dt>手机</dt><dd class="num">138****2210</dd>'
        '<dt>邮箱</dt><dd>chenli@example.com</dd></dl>'
        '<div style="margin-top:16px;display:flex;gap:8px"><button class="btn p">申请修改信息</button><button class="btn">上传头像</button></div>'
        '</div></div>') + card("信息变更记录", table(["变更项", "变更前", "变更后", "状态", "提交时间"],
            [("工作单位", "字节跳动 · 工程师", "字节跳动 · 技术专家", tag("待审核"), '<span class="num">2026-10-28 14:22</span>'),
             ("所在地区", "无锡", "上海", tag("已通过"), '<span class="num">2025-09-12 10:03</span>')], ["", "", "", "c", ""]))
    + '</div><div>' + card("隐私选项", '<div class="card-b" style="font-size:13px;line-height:32px;color:var(--text2)">'
        '<div>☑ 向校友公开手机号</div><div>☐ 向校友公开邮箱</div><div>☑ 公开工作单位</div>'
        '<div>☑ 公开所在地区</div><div class="hint" style="line-height:20px;margin-top:6px">关闭后仅本人与管理员可见，公开端不展示。</div></div>')
    + card("我的参与", '<div class="card-b"><div class="legend" style="line-height:30px">'
        '<div>参加活动 <b style="float:right" class="num">12 次</b></div>'
        '<div>累计捐赠 <b style="float:right" class="num">¥ 180,000</b></div>'
        '<div>感谢证书 <b style="float:right" class="num">3 张</b></div>'
        '<div>所属组织 <b style="float:right">上海校友会</b></div></div>'
        '<button class="btn sm" style="margin-top:12px">查看我的报名</button></div>') + '</div></div>')

# ---------- 系统页 ----------
sys_users = [("admin", "周敏", "校友办管理员", "校友工作办公室", "138****0001", tag("正常")),
             ("liaison01", "陈立", "校友联络员", "上海校友会", "138****2210", tag("正常")),
             ("finance01", "张倩", "财务登记员", "财务处", "139****5566", tag("正常")),
             ("alumni01", "林雅", "校友", "经济管理学院", "139****8876", tag("正常")),
             ("liaison02", "王海涛", "校友联络员", "深圳校友会", "137****3345", tag("停用"))]
PAGES["user"] = head("用户") + admin("user", "用户管理", page_head(
    "用户管理", "账号与角色绑定，数据范围按角色控制", '<button class="btn p">新建用户</button>')
    + card("用户列表", table(["账号", "姓名", "角色", "所属组织", "手机", "状态", "操作"],
                            [(u[0], u[1], u[2], u[3], f'<span class="num">{u[4]}</span>', u[5],
                              '<a class="link">编辑</a> <a class="link">重置密码</a>') for u in sys_users],
                            ["", "", "c", "", "", "c", "c"]) + pager(24, 1), "共 24 个账号"))

roles = [("ADMIN", "校友办管理员", "全部数据", 32, tag("启用")), ("LIAISON", "校友联络员", "本人及所属组织", 26, tag("启用")),
         ("FINANCE", "财务登记员", "全部捐赠与凭证", 18, tag("启用")), ("ALUMNI", "校友", "本人数据", 12, tag("启用"))]
PAGES["role"] = head("角色") + admin("role", "角色管理", page_head(
    "角色管理", "菜单权限 + 数据范围分别控制；只有菜单权限不能直接调用写接口", '<button class="btn p">新建角色</button>')
    + card("角色列表", table(["角色编码", "角色名称", "数据范围", "已授权菜单", "状态", "操作"],
                            [(r[0], r[1], r[2], f'<span class="num">{r[3]}</span>', r[4],
                              '<a class="link">编辑</a> <a class="link">分配菜单</a>') for r in roles],
                            ["", "", "", "r", "c", "c"]) + pager(4, 1))
    + '<div style="height:16px"></div>'
    + card("分配菜单 · 校友联络员", '<div class="card-b" style="display:grid;grid-template-columns:1fr 1fr;gap:8px 24px;font-size:13px">'
        '<div>☑ 校友运营看板</div><div>☑ 校友档案（只读）</div><div>☑ 组织管理</div><div>☑ 成员审核</div>'
        '<div>☑ 活动管理</div><div>☑ 报名与签到</div><div>☑ 活动归档</div><div>☐ 捐赠核对</div>'
        '<div>☐ 规则配置</div><div>☐ 用户管理</div></div>'))

PAGES["menu"] = head("菜单") + admin("menu", "菜单管理", page_head(
    "菜单管理", "菜单按角色权限动态获取；「菜单管理」选项在分配菜单中隐藏", '<button class="btn p">新建菜单</button>')
    + card("菜单树", table(["菜单名称", "类型", "路由 / 权限标识", "排序", "可见", "操作"],
                           [("校友运营看板", "菜单", "/dashboard", '<span class="num">1</span>', tag("显示"), '<a class="link">编辑</a>'),
                            ("校友档案", "菜单", "/alumni", '<span class="num">2</span>', tag("显示"), '<a class="link">编辑</a>'),
                            ("　认证审核", "菜单", "/cert-audit", '<span class="num">3</span>', tag("显示"), '<a class="link">编辑</a>'),
                            ("　变更审核", "菜单", "/change-audit", '<span class="num">4</span>', tag("显示"), '<a class="link">编辑</a>'),
                            ("捐赠项目", "菜单", "/project", '<span class="num">5</span>', tag("显示"), '<a class="link">编辑</a>'),
                            ("　线下捐赠登记", "菜单", "/donation", '<span class="num">6</span>', tag("显示"), '<a class="link">编辑</a>'),
                            ("　捐赠核对", "菜单", "/verify", '<span class="num">7</span>', tag("显示"), '<a class="link">编辑</a>'),
                            ("创新模块", "菜单", "/innovation", '<span class="num">8</span>', tag("显示"), '<a class="link">编辑</a>')],
                           ["", "c", "", "r", "c", "c"]), "共 32 项"))

# ---------- 门户首页 ----------
PAGES["index"] = head("首页") + portal("index",
    '<div class="p-hero"><h1>陈立，欢迎回到校友之家</h1><p>您有 1 场活动待签到，1 条信息变更申请待审核，2 个项目进展已更新。</p></div>'
    '<div class="kpis" style="grid-template-columns:repeat(4,1fr);margin-bottom:16px">'
    + "".join(f'<div class="kpi"><h4>{t}</h4><b>{v}</b><span>{d}</span></div>'
              for t, v, d in [("我的活动", "12", "本月 2 场"), ("累计捐赠", "¥ 180,000", "4 笔已核对"),
                              ("感谢证书", "3 张", "待发放 0"), ("所属组织", "上海校友会", "成员")]) + "</div>"
    '<div class="split"><div>' + card("即将开始的活动", '<div class="card-b">'
        '<div class="tl"><div class="it now"><b>计算机学院校友返校日</b><em class="num">2026-11-18 09:00</em>'
        '<p>计算机学院报告厅 · 已报名（1 名同行人）· 签到码 8421</p></div>'
        '<div class="it done"><b>上海校友会秋季沙龙</b><em class="num">2026-11-09 14:00</em>'
        '<p>静安洲际酒店 · 候补第 3 位，有名额时自动转正并通知</p></div></div></div>')
    + card("我关注的捐赠项目", table(["项目", "进度", "状态", "最近进展"],
        [("计算机学院实验楼改造基金", '<div class="prog" style="width:120px"><i style="width:68%"></i></div>', tag("募集中"), '<span class="num">2026-10-20</span>'),
         ("寒门学子助学金", '<div class="prog" style="width:120px"><i style="width:94%"></i></div>', tag("执行中"), '<span class="num">2026-10-12</span>')],
        ["", "", "c", ""]))
    + '</div><div>' + card("我的证书", '<div class="card-b"><div class="legend" style="line-height:26px">'
        '<div>TC-2026-000185 · ¥ 30,000</div><div class="hint">2026-10-29 · 待发放</div>'
        '<div style="margin-top:8px">TC-2025-000092 · ¥ 100,000</div><div class="hint">2025-11-08 · 已发放</div></div>'
        '<button class="btn sm" style="margin-top:12px">全部证书</button></div>')
    + card("待办", '<div class="card-b" style="font-size:13px;line-height:26px;color:var(--text2)">'
        '<div>· 信息变更申请待审核（工作单位）</div><div>· 返校日活动待签到</div>'
        '<div>· 1 条项目进展提醒</div></div>') + '</div></div>')

# ---------- 我的报名 / 我的证书（门户） ----------
PAGES["my-signup"] = head("我的报名") + portal("my-signup",
    '<div class="p-hero"><h1>我的报名</h1><p>报名后可取消；候补名额按报名时间顺序自动转正，转正后发送站内消息。</p></div>'
    + card("报名记录", table(["报名编号", "活动", "报名时间", "状态", "同行人", "签到码", "操作"],
        [("S20261101001", "计算机学院校友返校日", '<span class="num">2026-10-30 09:12</span>', tag("已报名"), "1", '<b class="num">8421</b>', '<a class="link">查看</a> <a class="link">取消</a>'),
         ("S20261101003", "上海校友会秋季沙龙", '<span class="num">2026-10-30 10:05</span>', tag("候补"), "2", "—", '<a class="link">查看</a> <a class="link">取消</a>'),
         ("S20261012008", "1998级毕业25周年聚会", '<span class="num">2026-10-12 15:33</span>', tag("已归档"), "0", "—", '<a class="link">查看</a>')],
        ["", "", "", "c", "r", "c", "c"]) + pager(12, 1)))
PAGES["my-cert"] = head("我的证书") + portal("my-cert",
    '<div class="p-hero"><h1>我的感谢证书</h1><p>证书仅对已核对成功的捐赠生成；匿名捐赠的证书对外显示「匿名校友」。</p></div>'
    + card("证书列表", table(["证书编号", "关联项目", "金额", "签发日期", "发放状态", "操作"],
        [("TC-2026-000185", "寒门学子助学金", '<span class="num">¥ 30,000.00</span>', '<span class="num">2026-10-29</span>', tag("待发放"), '<a class="link">预览</a>'),
         ("TC-2025-000092", "校友创新创业基金", '<span class="num">¥ 100,000.00</span>', '<span class="num">2025-11-08</span>', tag("已发放"), '<a class="link">下载</a>'),
         ("TC-2024-000031", "图书馆古籍修复计划", '<span class="num">¥ 50,000.00</span>', '<span class="num">2024-12-16</span>', tag("已发放"), '<a class="link">下载</a>')],
        ["", "", "r", "", "c", "c"]) + pager(3, 1)))

def main():
    files = []
    for name, html in PAGES.items():
        p = ROOT / f"{name}.html"
        p.write_text(html, encoding="utf-8")
        files.append(p)
    # 索引页
    links = "".join(f'<li><a href="{n}.html">{n}</a></li>' for n in PAGES)
    (ROOT / "index_all.html").write_text(
        head("设计稿索引") + f'<div style="padding:32px"><h1 style="font-size:20px">设计稿索引（{len(PAGES)} 页）</h1>'
        f'<ul style="margin-top:16px;line-height:30px;columns:3">{links}</ul></div></body></html>', encoding="utf-8")
    print(f"生成 {len(PAGES)} 个页面 -> {ROOT}")

if __name__ == "__main__":
    main()
