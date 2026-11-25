<template>
  <div class="eff" v-loading="loading">
    <div class="page-head">
      <div>
        <h1>效果统计</h1>
        <p>验证创新模块是否有效：推荐采纳率、人工调整率、等级分布与分项平均分对比</p>
      </div>
      <el-button plain @click="$router.push('/score')">查看计算留痕</el-button>
    </div>

    <div class="kpis">
      <div class="kpi"><h4>累计计算次数</h4><b>{{ e.total || 0 }}</b><span>覆盖全部捐赠项目</span></div>
      <div class="kpi"><h4>推荐结果数</h4><b>{{ e.recommendCount || 0 }}</b><span>总分达推荐线</span></div>
      <div class="kpi"><h4>平均综合得分</h4><b>{{ e.avgScore || 0 }}</b><span>满分 100</span></div>
      <div class="kpi"><h4>推荐采纳率</h4><b>{{ e.adoptionRate || 0 }}%</b><span>未被人工修正的比例</span></div>
      <div class="kpi"><h4>人工调整率</h4><b>{{ e.manualRate || 0 }}%</b><span>需人工修正的比例</span></div>
    </div>

    <div class="charts">
      <div class="card">
        <div class="card-h"><h2>结果等级分布</h2><div class="r">按计算结果</div></div>
        <div class="chart-body" ref="distEl"></div>
      </div>
      <div class="card">
        <div class="card-h"><h2>分项平均得分</h2><div class="r">六因素对比</div></div>
        <div class="chart-body" ref="radarEl"></div>
      </div>
      <div class="card">
        <div class="card-h"><h2>项目综合得分排名</h2><div class="r">Top 8</div></div>
        <div class="chart-body" ref="rankEl"></div>
      </div>
      <div class="card">
        <div class="card-h"><h2>计算与人工修正对比</h2><div class="r">评审有效性</div></div>
        <div class="chart-body" ref="manualEl"></div>
      </div>
    </div>

    <div class="card">
      <div class="card-h"><h2>修正明细</h2><div class="r">人工修正不影响原始结果</div></div>
      <el-table :data="manualRows" border size="small">
        <el-table-column prop="projectName" label="项目" min-width="220" />
        <el-table-column prop="totalScore" label="原始得分" width="100" align="right" />
        <el-table-column prop="resultLevel" label="原始结果" width="100" />
        <el-table-column prop="manualLevel" label="修正结果" width="100" />
        <el-table-column prop="manualReason" label="修正原因" min-width="240" />
        <el-table-column prop="manualUser" label="修正人" width="110" />
        <el-table-column prop="manualTime" label="修正时间" width="160">
          <template #default="{ row }">{{ formatTime(row.manualTime) }}</template>
        </el-table-column>
      </el-table>
      <el-empty v-if="!manualRows.length" description="暂无人工修正记录，说明计算结果与实际判断一致性较好" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue'
import * as echarts from 'echarts'
import request from '@/utils/request'
import { formatTime, levelColor } from '@/utils/format'

const loading = ref(false)
const e = ref({})
const all = ref([])
const manualRows = ref([])
const distEl = ref(null)
const radarEl = ref(null)
const rankEl = ref(null)
const manualEl = ref(null)
const charts = []
const COLORS = ['#5B2533', '#2F6F6A', '#7A3947', '#B4761F', '#2D765C', '#8C8279']

function init(el) {
  if (!el) return null
  const c = echarts.init(el)
  charts.push(c)
  return c
}

function render() {
  const dist = e.value.distribution || {}
  const c1 = init(distEl.value)
  c1 && c1.setOption({
    tooltip: { trigger: 'item' },
    legend: { bottom: 0, itemWidth: 10, itemHeight: 10, textStyle: { fontSize: 11 } },
    series: [{
      type: 'pie', radius: ['46%', '68%'], center: ['50%', '44%'],
      itemStyle: { borderColor: '#fff', borderWidth: 2 },
      label: { formatter: '{b}\n{c} 个', fontSize: 11 },
      data: Object.keys(dist).map((k) => ({ name: k, value: dist[k], itemStyle: { color: levelColor(k) } }))
    }]
  })

  const avg = (k) => {
    const list = all.value
    if (!list.length) return 0
    return Math.round((list.reduce((s, x) => s + Number(x[k] || 0), 0) / list.length) * 10) / 10
  }
  const c2 = init(radarEl.value)
  c2 && c2.setOption({
    tooltip: {},
    radar: {
      indicator: [
        { name: '目标金额', max: 100 }, { name: '已登记', max: 100 }, { name: '里程碑', max: 100 },
        { name: '支出凭证', max: 100 }, { name: '受益人数', max: 100 }, { name: '公开审核', max: 100 }
      ],
      radius: '62%', center: ['50%', '52%'],
      axisName: { fontSize: 11, color: '#6B5F5C' },
      splitLine: { lineStyle: { color: '#E7DFDC' } },
      axisLine: { lineStyle: { color: '#E7DFDC' } }
    },
    series: [{
      type: 'radar', symbolSize: 5,
      areaStyle: { opacity: 0.18, color: '#5B2533' },
      lineStyle: { color: '#5B2533' }, itemStyle: { color: '#5B2533' },
      data: [{
        value: [avg('targetScore'), avg('amountScore'), avg('milestoneScore'),
          avg('voucherScore'), avg('beneficiaryScore'), avg('auditScore')],
        name: '分项平均分'
      }]
    }]
  })

  const top = [...all.value].sort((a, b) => Number(b.totalScore) - Number(a.totalScore)).slice(0, 8).reverse()
  const c3 = init(rankEl.value)
  c3 && c3.setOption({
    grid: { left: 8, right: 46, top: 12, bottom: 6, containLabel: true },
    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
    xAxis: { type: 'value', max: 100, splitLine: { lineStyle: { color: '#F0EAE7' } }, axisLabel: { fontSize: 10 } },
    yAxis: {
      type: 'category', axisTick: { show: false }, axisLine: { show: false },
      axisLabel: { fontSize: 11, width: 96, overflow: 'truncate' },
      data: top.map((x) => x.projectName)
    },
    series: [{
      type: 'bar', barWidth: 12, label: { show: true, position: 'right', fontSize: 10 },
      itemStyle: { borderRadius: [0, 6, 6, 0] },
      data: top.map((x) => ({
        value: Number(x.totalScore),
        itemStyle: { color: levelColor(x.resultLevel) }
      }))
    }]
  })

  const c4 = init(manualEl.value)
  c4 && c4.setOption({
    grid: { left: 8, right: 16, top: 24, bottom: 6, containLabel: true },
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: ['计算总数', '推荐结果', '人工修正', '采纳结果'], axisLabel: { fontSize: 11 } },
    yAxis: { type: 'value', splitLine: { lineStyle: { color: '#F0EAE7' } }, axisLabel: { fontSize: 10 } },
    series: [{
      type: 'bar', barWidth: 26, itemStyle: { borderRadius: [6, 6, 0, 0] },
      data: [
        { value: e.value.total || 0, itemStyle: { color: COLORS[0] } },
        { value: e.value.recommendCount || 0, itemStyle: { color: COLORS[1] } },
        { value: e.value.manualCount || 0, itemStyle: { color: COLORS[3] } },
        { value: (e.value.total || 0) - (e.value.manualCount || 0), itemStyle: { color: COLORS[4] } }
      ]
    }]
  })
}

async function load() {
  loading.value = true
  try {
    const [ef, page] = await Promise.all([
      request.get('/api/score/effect'),
      request.get('/api/score/page', { params: { page: 1, size: 200 } })
    ])
    e.value = ef
    all.value = page.list || []
    manualRows.value = all.value.filter((x) => x.manualLevel)
    await nextTick()
    render()
  } finally { loading.value = false }
}

function onResize() { charts.forEach((c) => c.resize()) }
onMounted(() => { load(); window.addEventListener('resize', onResize) })
onBeforeUnmount(() => { window.removeEventListener('resize', onResize); charts.forEach((c) => c.dispose()) })
</script>

<style scoped>
.page-head { display: flex; align-items: flex-end; justify-content: space-between; margin-bottom: 18px; }
.page-head h1 { font-size: 22px; margin: 0 0 6px; color: var(--text); }
.page-head p { font-size: 13px; color: var(--text3); margin: 0; }
.kpis { display: grid; grid-template-columns: repeat(5, 1fr); gap: 14px; margin-bottom: 18px; }
.kpi { background: #fff; border: 1px solid var(--border); border-radius: 10px; padding: 14px 16px; }
.kpi h4 { font-size: 12px; color: var(--text3); font-weight: 400; margin: 0 0 6px; }
.kpi b { font-size: 22px; color: var(--text); display: block; }
.kpi span { font-size: 11px; color: var(--text3); }
.charts { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; margin-bottom: 16px; }
.chart-body { height: 230px; }
</style>
