<template>
  <div class="pub" v-loading="loading">
    <header class="top">
      <div class="brand" @click="$router.push('/public/projects')"><span class="logo">校</span>校友捐赠公开平台</div>
      <div class="nav"><a @click="$router.push('/public/projects')">返回项目列表</a></div>
    </header>

    <template v-if="p.id">
      <section class="hero">
        <div class="hero-in">
          <div class="h-left">
            <h1>{{ p.projectName }}</h1>
            <p>{{ p.publicDesc || p.purpose }}</p>
            <div class="kv">
              <span>发起方 {{ p.initiator }}</span>
              <span>负责部门 {{ p.deptName }}</span>
              <span>执行周期 {{ formatDate(p.startDate) }} ~ {{ formatDate(p.endDate) }}</span>
              <span>项目状态 {{ p.status }}</span>
            </div>
          </div>
          <div class="h-right">
            <div class="big">{{ wan(p.raisedAmount) }}</div>
            <div class="sub">已募集（已核对） / 目标 {{ wan(p.targetAmount) }}</div>
            <el-progress :percentage="Math.min(100, Math.round(p.progressRate || 0))" :stroke-width="10"
                         :show-text="false" color="#fff" :define-message="''" class="pg" />
            <div class="sub">{{ Math.round(p.progressRate || 0) }}% · 受益 {{ p.beneficiaryCount || 0 }} 人</div>
          </div>
        </div>
      </section>

      <section class="body">
        <div class="cols">
          <div class="card main">
            <div class="card-h"><h2>执行里程碑</h2><span class="muted">完成度按权重计算 {{ Math.round(p.milestoneRate || 0) }}%</span></div>
            <div class="ms">
              <div v-for="m in milestones" :key="m.id" class="m-item" :class="{ done: m.status === '已完成' }">
                <div class="dot"></div>
                <div class="m-body">
                  <div class="m-h">
                    <b>{{ m.seqNo }}. {{ m.milestoneName }}</b>
                    <el-tag size="small" :type="m.status === '已完成' ? 'success' : 'info'">{{ m.status }}</el-tag>
                    <span class="muted small">权重 {{ m.weight }}</span>
                  </div>
                  <div class="muted small">计划 {{ formatDate(m.planDate) }}<template v-if="m.finishDate"> · 完成 {{ formatDate(m.finishDate) }}</template></div>
                  <div class="small">{{ m.deliverable }}</div>
                </div>
              </div>
              <el-empty v-if="!milestones.length" description="里程碑信息待补充" />
            </div>

            <el-divider />
            <div class="card-h"><h2>阶段进展公示</h2><span class="muted">仅展示审核通过的进展</span></div>
            <el-timeline class="tl">
              <el-timeline-item v-for="g in progress" :key="g.id" :timestamp="formatTime(g.publishTime)" type="success">
                <div class="tl-h"><b>{{ g.stageName }}</b><span class="muted">进度 {{ g.progressRate }}%</span></div>
                <div class="small">{{ g.content }}</div>
                <div class="muted small">资金使用：{{ g.fundSummary }}</div>
                <img v-if="g.photoPath" class="ph" :src="g.photoPath" alt="" />
              </el-timeline-item>
            </el-timeline>
            <el-empty v-if="!progress.length" description="暂无进展公示" />
          </div>

          <div class="side">
            <div class="card">
              <div class="card-h"><h2>捐赠鸣谢</h2><span class="muted">匿名捐赠不展示姓名</span></div>
              <div class="donors">
                <div v-for="(d, i) in donors" :key="i" class="donor">
                  <span class="idx">{{ i + 1 }}</span>
                  <span class="name">{{ d.donorName }}</span>
                  <span class="type muted">{{ d.donorType }}</span>
                  <b class="num">{{ money(d.amount) }}</b>
                </div>
                <el-empty v-if="!donors.length" description="暂无展示的捐赠记录" :image-size="70" />
              </div>
            </div>
            <div class="card">
              <div class="card-h"><h2>资金使用</h2></div>
              <div class="card-b">
                <div class="kv2"><span>预算金额</span><b>{{ wan(p.budgetAmount) }}</b></div>
                <div class="kv2"><span>已募集</span><b class="up">{{ wan(p.raisedAmount) }}</b></div>
                <div class="kv2"><span>已支出</span><b>{{ wan(p.spentAmount) }}</b></div>
                <div class="kv2"><span>结余</span><b>{{ wan((p.raisedAmount || 0) - (p.spentAmount || 0)) }}</b></div>
                <el-divider />
                <p class="muted small">公示口径：实收金额仅统计经财务核对通过的捐赠，未核对捐赠不计入。</p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </template>

    <el-empty v-else-if="!loading" description="项目不存在或未公开" style="padding:80px 0" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import request from '@/utils/request'
import { formatTime, formatDate, money, wan } from '@/utils/format'

const route = useRoute()
const loading = ref(false)
const p = ref({})
const milestones = ref([])
const progress = ref([])
const donors = ref([])

async function load() {
  loading.value = true
  try {
    const d = await request.get(`/api/public/projects/${route.params.id}`)
    p.value = d.project || {}
    milestones.value = d.milestones || []
    progress.value = d.progress || []
    donors.value = d.donors || []
  } finally { loading.value = false }
}
onMounted(load)
</script>

<style scoped>
.pub { min-height: 100vh; background: #FAF7F5; }
.top { height: 60px; background: #fff; border-bottom: 1px solid #E7DFDC; display: flex; align-items: center;
  justify-content: space-between; padding: 0 48px; }
.brand { display: flex; align-items: center; gap: 10px; font-size: 15px; font-weight: 600; color: #5B2533; cursor: pointer; }
.logo { width: 24px; height: 24px; border-radius: 6px; background: #5B2533; color: #fff; display: inline-flex;
  align-items: center; justify-content: center; font-size: 12px; }
.nav { font-size: 13px; color: #5B2533; }
.nav a { cursor: pointer; }
.hero { background: linear-gradient(120deg, #431B26, #5B2533 60%, #7A3947); color: #fff; padding: 34px 48px; }
.hero-in { max-width: 1180px; margin: 0 auto; display: flex; justify-content: space-between; gap: 40px; }
.h-left { flex: 1; }
.h-left h1 { font-size: 26px; margin: 0 0 10px; }
.h-left p { font-size: 13px; color: rgba(255,255,255,.8); margin: 0 0 16px; line-height: 1.8; max-width: 640px; }
.kv { display: flex; flex-wrap: wrap; gap: 8px 22px; font-size: 12px; color: rgba(255,255,255,.72); }
.h-right { width: 280px; flex: none; text-align: right; }
.big { font-size: 30px; font-weight: 600; }
.sub { font-size: 12px; color: rgba(255,255,255,.72); margin-top: 4px; }
.pg { margin: 12px 0 6px; }
.body { max-width: 1180px; margin: 0 auto; padding: 22px 24px 44px; }
.cols { display: grid; grid-template-columns: 1fr 330px; gap: 18px; }
@media (max-width: 1000px) { .cols { grid-template-columns: 1fr; } }
.main { padding: 4px 20px 20px; }
.ms { padding-top: 6px; }
.m-item { position: relative; display: flex; gap: 12px; padding: 8px 0 12px 4px; }
.m-item::before { content: ''; position: absolute; left: 8px; top: 22px; bottom: -6px; width: 1px; background: #E7DFDC; }
.m-item:last-child::before { display: none; }
.dot { width: 9px; height: 9px; border-radius: 50%; background: #C9BCB7; margin-top: 6px; flex: none; z-index: 1; }
.m-item.done .dot { background: #2D765C; }
.m-body { flex: 1; }
.m-h { display: flex; align-items: center; gap: 10px; margin-bottom: 3px; }
.small { font-size: 12px; }
.tl { padding-left: 2px; margin-top: 10px; }
.tl-h { display: flex; gap: 12px; align-items: center; margin-bottom: 4px; }
.ph { width: 200px; height: 124px; object-fit: cover; border-radius: 8px; margin-top: 8px; }
.side { display: flex; flex-direction: column; gap: 18px; }
.donors { padding: 6px 16px 16px; }
.donor { display: flex; align-items: center; gap: 8px; font-size: 12px; padding: 7px 0; border-bottom: 1px dashed #E7DFDC; }
.idx { width: 18px; height: 18px; border-radius: 4px; background: #F3EAE7; color: #7A3947;
  display: inline-flex; align-items: center; justify-content: center; font-size: 11px; }
.name { flex: 1; color: #2E2422; }
.type { font-size: 11px; }
.donor b { color: #A61B29; }
.card-b { padding: 0 16px 16px; }
.kv2 { display: flex; justify-content: space-between; font-size: 13px; padding: 6px 0; color: #6B5F5C; }
.kv2 b { color: #2E2422; }
.up { color: #A61B29; }
</style>
