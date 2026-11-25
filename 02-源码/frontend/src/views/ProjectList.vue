<template>
  <div v-loading="loading">
    <div class="page-head">
      <div>
        <h1>捐赠项目</h1>
        <p>项目立项 → 募集中 → 执行中 → 待验收 → 已结项；实收金额由已核对捐赠明细汇总推导</p>
      </div>
      <div class="filters">
        <el-select v-model="status" placeholder="全部状态" clearable style="width:150px" @change="reload">
          <el-option v-for="s in statuses" :key="s" :label="s" :value="s" />
        </el-select>
        <el-input v-model="kw" placeholder="项目名称" clearable style="width:220px" @keyup.enter="reload" @clear="reload" />
        <el-button type="primary" @click="reload">查询</el-button>
        <el-button plain @click="$router.push('/donation-record')">登记捐赠</el-button>
      </div>
    </div>

    <div class="summary">
      <div class="s-item"><span>项目总数</span><b>{{ kpi.count }}</b></div>
      <div class="s-item"><span>目标金额合计</span><b>{{ wan(kpi.target) }}</b></div>
      <div class="s-item"><span>已募集金额</span><b class="up">{{ wan(kpi.raised) }}</b></div>
      <div class="s-item"><span>平均完成度</span><b>{{ kpi.rate }}%</b></div>
    </div>

    <div class="grid">
      <div v-for="p in rows" :key="p.id" class="card proj" @click="$router.push('/project/' + p.id)">
        <div class="cover">
          <img :src="p.coverImage" :alt="p.projectName" />
          <span class="status" :class="statusType(p.status)">{{ p.status }}</span>
        </div>
        <div class="body">
          <h3>{{ p.projectName }}</h3>
          <p class="muted line2">{{ p.purpose }}</p>
          <div class="amount">
            <b class="up">{{ wan(p.raisedAmount) }}</b>
            <span class="muted">/ {{ wan(p.targetAmount) }}</span>
          </div>
          <el-progress :percentage="Math.min(100, Math.round(p.progressRate || 0))" :stroke-width="6"
                       :show-text="false" color="#5B2533" />
          <div class="foot">
            <span>里程碑 {{ Math.round(p.milestoneRate || 0) }}%</span>
            <span>{{ p.deptName }}</span>
            <el-tag v-if="p.publicStatus === '已通过'" size="small" type="success" effect="plain">已公开</el-tag>
            <el-tag v-else size="small" type="warning" effect="plain">{{ p.publicStatus }}</el-tag>
          </div>
        </div>
      </div>
      <el-empty v-if="!loading && !rows.length" description="暂无项目" style="grid-column:1/-1" />
    </div>

    <el-pagination background layout="total, prev, pager, next" :total="total" v-model:current-page="page"
                   :page-size="9" @current-change="load" style="justify-content:center;margin-top:20px" />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import request from '@/utils/request'
import { wan, statusType } from '@/utils/format'

const rows = ref([])
const total = ref(0)
const page = ref(1)
const kw = ref('')
const status = ref('')
const loading = ref(false)
const kpi = reactive({ count: 0, target: 0, raised: 0, rate: 0 })
const statuses = ['项目立项', '募集中', '执行中', '待验收', '已结项']

async function load() {
  loading.value = true
  try {
    const d = await request.get('/api/project/page', {
      params: { page: page.value, size: 9, kw: kw.value, status: status.value }
    })
    rows.value = d.list || []
    total.value = d.total || 0
    // 汇总按当前筛选条件重新取全量，避免分页导致 KPI 只统计当页
    const all = await request.get('/api/project/page', {
      params: { page: 1, size: 200, kw: kw.value, status: status.value }
    })
    const list = all.list || []
    kpi.count = all.total || 0
    kpi.target = list.reduce((s, p) => s + Number(p.targetAmount || 0), 0)
    kpi.raised = list.reduce((s, p) => s + Number(p.raisedAmount || 0), 0)
    kpi.rate = kpi.target ? Math.round((kpi.raised * 100) / kpi.target) : 0
  } finally { loading.value = false }
}
function reload() { page.value = 1; load() }
onMounted(load)
</script>

<style scoped>
.page-head { display: flex; align-items: flex-end; justify-content: space-between; margin-bottom: 18px; }
.page-head h1 { font-size: 22px; margin: 0 0 6px; color: var(--text); }
.page-head p { font-size: 13px; color: var(--text3); margin: 0; }
.filters { display: flex; gap: 10px; }
.summary { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 18px; }
.s-item { background: #fff; border: 1px solid var(--border); border-radius: 10px; padding: 14px 18px; }
.s-item span { display: block; font-size: 12px; color: var(--text3); margin-bottom: 6px; }
.s-item b { font-size: 20px; color: var(--text); font-weight: 600; }
.up { color: #A61B29; }
.grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; }
@media (max-width: 1200px) { .grid { grid-template-columns: repeat(2, 1fr); } }
.proj { padding: 0; overflow: hidden; cursor: pointer; transition: box-shadow .2s, transform .2s; }
.proj:hover { box-shadow: 0 8px 22px rgba(91,37,51,.12); transform: translateY(-2px); }
.cover { position: relative; height: 140px; background: #EFE6E3; }
.cover img { width: 100%; height: 100%; object-fit: cover; display: block; }
.status { position: absolute; top: 10px; left: 10px; background: rgba(255,255,255,.94); color: #5B2533;
  font-size: 11px; padding: 2px 9px; border-radius: 10px; }
.body { padding: 14px 16px 16px; }
.body h3 { font-size: 15px; margin: 0 0 6px; color: var(--text); }
.line2 { display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;
  font-size: 12px; min-height: 34px; margin: 0 0 10px; }
.amount { font-size: 12px; color: var(--text3); margin-bottom: 6px; }
.amount b { font-size: 17px; margin-right: 4px; }
.foot { display: flex; align-items: center; gap: 10px; font-size: 12px; color: var(--text3); margin-top: 10px; }
</style>
