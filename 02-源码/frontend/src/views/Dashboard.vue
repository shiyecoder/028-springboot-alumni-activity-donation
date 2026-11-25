<template>
  <div class="dash">
    <div class="page-h">
      <h1>校友运营看板</h1>
      <p>默认最近 30 天 · 指标与明细总数一致</p>
      <div class="acts">
        <el-radio-group v-model="range" size="default" @change="load">
          <el-radio-button label="month">本月</el-radio-button>
          <el-radio-button label="quarter">本季度</el-radio-button>
          <el-radio-button label="year">本年</el-radio-button>
        </el-radio-group>
      </div>
    </div>

    <div class="kpis">
      <div class="kpi" v-for="k in kpiCards" :key="k.label">
        <h4>{{ k.label }}</h4>
        <b>{{ k.value }}</b>
        <span>{{ k.sub }}</span>
      </div>
    </div>

    <!-- 6 个图表，1440×900 一屏内不出现滚动条 -->
    <div class="charts">
      <div class="card chart-card" v-for="c in charts" :key="c.id">
        <div class="card-h"><h2>{{ c.title }}</h2><div class="r">{{ c.sub }}</div></div>
        <div class="chart-body" :ref="(el) => setRef(c.id, el)"></div>
      </div>
    </div>

    <div class="todo">
      <span class="hint">待办：</span>
      <el-tag v-for="t in todoTags" :key="t.label" :type="t.type" effect="light" class="todo-tag"
              @click="$router.push(t.path)">{{ t.label }} {{ t.value }}</el-tag>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onBeforeUnmount, nextTick } from 'vue'
import * as echarts from 'echarts'
import request from '@/utils/request'
import { wan } from '@/utils/format'

const range = ref('month')
const data = ref({ kpi: {}, todo: {} })
const els = {}
const charts = [
  { id: 'trend', title: '捐赠登记趋势', sub: '单位：万元' },
  { id: 'project', title: '项目状态分布', sub: '按项目数' },
  { id: 'college', title: '学院贡献分布', sub: '已核对金额' },
  { id: 'funnel', title: '活动报名与到场', sub: '全量活动' },
  { id: 'org', title: '组织活跃度', sub: '按成员数' },
  { id: 'score', title: '创新模块结果分布', sub: '计算结果' }
]
const instances = {}
const COLORS = ['#5B2533', '#2F6F6A', '#7A3947', '#B4761F', '#2D765C', '#8C8279']

const kpiCards = ref([])
const todoTags = ref([])

function setRef(id, el) { if (el) els[id] = el }

async function load() {
  const d = await request.get('/api/dashboard/overview')
  data.value = d
  const k = d.kpi || {}
  kpiCards.value = [
    { label: '活动参与人数', value: k.participants ?? 0, sub: `活动 ${k.activityCount ?? 0} 场` },
    { label: '捐赠项目数', value: k.projectCount ?? 0, sub: '不含已取消' },
    { label: '登记金额', value: wan(k.raisedAmount), sub: '仅已核对' },
    { label: '里程碑完成率', value: (k.milestoneRate ?? 0) + '%', sub: '按权重计' },
    { label: '已认证校友', value: k.alumniCount ?? 0, sub: '含待认证' },
    { label: '校友活跃度', value: (k.activeRate ?? 0) + '%', sub: '参与过活动' }
  ]
  const t = d.todo || {}
  todoTags.value = [
    { label: '待认证', value: t.certPending, path: '/cert-audit', type: 'warning' },
    { label: '待变更', value: t.changePending, path: '/change-audit', type: 'warning' },
    { label: '待审核活动', value: t.activityPending, path: '/activity-audit', type: 'warning' },
    { label: '待核对捐赠', value: t.donationPending, path: '/donation-verify', type: 'warning' },
    { label: '待审进展', value: t.progressPending, path: '/progress-publish', type: 'warning' }
  ]
  await nextTick()
  render(d)
}

function render(d) {
  const mk = (id) => {
    if (!els[id]) return null
    if (!instances[id]) instances[id] = echarts.init(els[id])
    return instances[id]
  }
  const axis = { axisLine: { lineStyle: { color: '#E7DFDC' } }, axisLabel: { color: '#6B5F5C', fontSize: 11 } }

  const trend = mk('trend')
  if (trend) {
    trend.setOption({
      grid: { left: 46, right: 16, top: 16, bottom: 28 },
      tooltip: { trigger: 'axis' },
      xAxis: { type: 'category', data: (d.trend || []).map((x) => x.month), ...axis },
      yAxis: { type: 'value', ...axis, splitLine: { lineStyle: { color: '#F1EAE8' } } },
      series: [{
        type: 'line', smooth: true, symbolSize: 6, data: (d.trend || []).map((x) => x.amount),
        itemStyle: { color: '#5B2533' }, areaStyle: { color: 'rgba(91,37,51,.10)' }, lineStyle: { width: 2 }
      }]
    })
  }

  const proj = mk('project')
  if (proj) {
    proj.setOption({
      color: COLORS,
      tooltip: { trigger: 'item' },
      legend: { bottom: 0, itemWidth: 8, itemHeight: 8, textStyle: { fontSize: 11, color: '#6B5F5C' } },
      series: [{
        type: 'pie', radius: ['46%', '68%'], center: ['50%', '44%'], avoidLabelOverlap: true,
        label: { show: false },
        data: (d.projectStatus || []).map((x) => ({ name: x.name, value: x.value }))
      }]
    })
  }

  const college = mk('college')
  if (college) {
    const rows = (d.collegeRank || []).slice(0, 6).reverse()
    college.setOption({
      grid: { left: 96, right: 24, top: 12, bottom: 20 },
      tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
      xAxis: {
        type: 'value', ...axis, splitNumber: 3,
        splitLine: { lineStyle: { color: '#F1EAE8' } },
        axisLabel: { color: '#6B5F5C', fontSize: 10, formatter: (v) => (v >= 10000 ? v / 10000 + '万' : v) }
      },
      yAxis: { type: 'category', data: rows.map((x) => x.name), ...axis },
      series: [{ type: 'bar', data: rows.map((x) => x.value), barWidth: 14, itemStyle: { color: '#2F6F6A', borderRadius: [0, 3, 3, 0] } }]
    })
  }

  const funnel = mk('funnel')
  if (funnel) {
    const rows = d.activityFunnel || []
    funnel.setOption({
      grid: { left: 46, right: 16, top: 16, bottom: 28 },
      tooltip: { trigger: 'axis' },
      xAxis: { type: 'category', data: rows.map((x) => x.name), ...axis },
      yAxis: { type: 'value', ...axis, splitLine: { lineStyle: { color: '#F1EAE8' } } },
      series: [{ type: 'bar', data: rows.map((x) => x.value), barWidth: 34, itemStyle: { color: '#7A3947', borderRadius: [4, 4, 0, 0] } }]
    })
  }

  const org = mk('org')
  if (org) {
    const rows = (d.orgRank || []).reverse()
    org.setOption({
      grid: { left: 130, right: 24, top: 12, bottom: 20 },
      tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
      xAxis: { type: 'value', ...axis, splitLine: { lineStyle: { color: '#F1EAE8' } } },
      yAxis: { type: 'category', data: rows.map((x) => x.name), ...axis },
      series: [{ type: 'bar', data: rows.map((x) => x.value), barWidth: 12, itemStyle: { color: '#B4761F', borderRadius: [0, 3, 3, 0] } }]
    })
  }

  const score = mk('score')
  if (score) {
    const rows = d.scoreDist || []
    score.setOption({
      color: ['#2D765C', '#B4761F', '#A61B29'],
      tooltip: { trigger: 'item' },
      legend: { bottom: 0, itemWidth: 8, itemHeight: 8, textStyle: { fontSize: 11, color: '#6B5F5C' } },
      series: [{
        type: 'pie', radius: '62%', center: ['50%', '44%'],
        label: { fontSize: 11, color: '#6B5F5C', formatter: '{b} {c}' },
        data: rows.map((x) => ({ name: x.name, value: x.value }))
      }]
    })
  }
}

function resize() { Object.values(instances).forEach((i) => i.resize()) }

onMounted(() => {
  load()
  window.addEventListener('resize', resize)
})
onBeforeUnmount(() => {
  window.removeEventListener('resize', resize)
  Object.values(instances).forEach((i) => i.dispose())
})
</script>

<style scoped>
.dash { display: flex; flex-direction: column; gap: 14px; }
.kpis { display: grid; grid-template-columns: repeat(6, 1fr); gap: 14px; }
.kpi { background: #fff; border: 1px solid var(--border); border-radius: 8px; padding: 10px 14px; }
.kpi h4 { font-size: 12px; color: var(--text3); font-weight: 400; margin: 0; }
.kpi b { display: block; font-size: 22px; line-height: 30px; font-weight: 600; font-variant-numeric: tabular-nums; }
.kpi span { font-size: 12px; color: var(--success); }
.charts { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; }
.chart-card { display: flex; flex-direction: column; }
.chart-body { height: 196px; padding: 2px 8px 6px; }
.todo { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
.todo-tag { cursor: pointer; }
</style>
