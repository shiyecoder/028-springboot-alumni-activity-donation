/**
 * 全局时间格式化：全系统统一调用，禁止各页面自行拼接
 * @param {string|Date} v 时间值
 * @param {boolean} dateOnly 是否只显示日期
 */
export function formatTime(v, dateOnly = false) {
  if (!v) return '-'
  const s = String(v).replace('T', ' ')
  const m = s.match(/^(\d{4})-(\d{2})-(\d{2})[ ]?(\d{2}):(\d{2}):(\d{2})/)
  if (m) {
    return dateOnly ? `${m[1]}-${m[2]}-${m[3]}` : `${m[1]}-${m[2]}-${m[3]} ${m[4]}:${m[5]}:${m[6]}`
  }
  return s
}

export function formatDate(v) {
  return formatTime(v, true)
}

/** 金额：两位小数 + 千分位 */
export function money(v) {
  if (v === null || v === undefined || v === '') return '-'
  const n = Number(v)
  if (Number.isNaN(n)) return '-'
  return '¥ ' + n.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

/** 大额金额（万元） */
export function wan(v) {
  const n = Number(v || 0)
  return (n / 10000).toFixed(1) + ' 万'
}

/** 状态字典 → 中文标签（覆盖系统全部状态） */
export const STATUS_TEXT = {
  // 认证
  '待审核': '待审核', '已认证': '已认证', '已驳回': '已驳回', '已退回': '已退回',
  // 活动
  '报名中': '报名中', '进行中': '进行中', '已归档': '已归档', '已取消': '已取消',
  // 报名
  '已报名': '已报名', '候补': '候补', '已签到': '已签到', '未到场': '未到场',
  // 项目
  '项目立项': '项目立项', '募集中': '募集中', '执行中': '执行中', '待验收': '待验收', '已结项': '已结项',
  // 核对
  '待核对': '待核对', '已核对': '已核对',
  // 证书
  '待发放': '待发放', '已发放': '已发放',
  // 里程碑
  '未开始': '未开始', '已完成': '已完成',
  // 审核
  '已通过': '已通过', '已发布': '已发布',
  // 创新结果
  '推荐': '推荐', '观察': '观察', '不推荐': '不推荐',
  // 其他
  '启用': '启用', '停用': '停用', '正常': '正常', '已退出': '已退出'
}

export function statusText(s) {
  return STATUS_TEXT[s] || s || '-'
}

/** 状态 → Element Plus tag 类型；状态必须同时显示文字，不只用颜色 */
export function statusType(s) {
  if (['已认证', '已通过', '已完成', '已结项', '已签到', '已核对', '已发放', '已发布', '推荐', '正常', '启用'].includes(s)) return 'success'
  if (['报名中', '进行中', '执行中', '募集中', '已报名'].includes(s)) return 'primary'
  if (['待审核', '待核对', '待发放', '待验收', '候补', '未开始', '观察'].includes(s)) return 'warning'
  if (['已驳回', '已退回', '已取消', '未到场', '不推荐'].includes(s)) return 'danger'
  return 'info'
}

/** 结果等级 → 颜色（创新模块专用） */
export function levelColor(level) {
  return { '推荐': '#2D765C', '观察': '#B4761F', '不推荐': '#A61B29' }[level] || '#6B5F5C'
}
