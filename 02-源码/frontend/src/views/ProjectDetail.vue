<template>
  <div v-loading="loading">
    <div class="detail-head card">
      <img class="cover" :src="p.coverImage" :alt="p.projectName" />
      <div class="info">
        <div class="title-row">
          <h1>{{ p.projectName }}</h1>
          <el-tag :type="statusType(p.status)" effect="light">{{ p.status }}</el-tag>
          <el-tag v-if="p.publicStatus === '已通过'" type="success" effect="plain">进展已公开</el-tag>
          <el-tag v-else type="warning" effect="plain">公开{{ p.publicStatus }}</el-tag>
        </div>
        <p class="muted">{{ p.purpose }}</p>
        <div class="kv">
          <span>项目编号 <b>{{ p.projectNo }}</b></span>
          <span>发起方 <b>{{ p.initiator }}</b></span>
          <span>负责部门 <b>{{ p.deptName }}</b></span>
          <span>负责人 <b>{{ p.chargePerson }}</b></span>
          <span>周期 <b>{{ formatDate(p.startDate) }} ~ {{ formatDate(p.endDate) }}</b></span>
          <span>受益人数 <b>{{ p.beneficiaryCount }} 人</b></span>
        </div>
        <div class="ops">
          <el-button v-for="t in nextStatus" :key="t" :type="t === '已取消' ? 'danger' : 'primary'"
                     :plain="t === '已取消'" size="small" @click="transition(t)">流转为{{ t }}</el-button>
          <el-button size="small" plain @click="evaluate">重新计算公开评分</el-button>
          <el-button size="small" @click="$router.back()">返回</el-button>
        </div>
      </div>
      <div class="money">
        <div class="m-item"><span>目标金额</span><b>{{ wan(p.targetAmount) }}</b></div>
        <div class="m-item"><span>已募集（已核对）</span><b class="up">{{ wan(p.raisedAmount) }}</b></div>
        <div class="m-item"><span>已支出</span><b>{{ wan(p.spentAmount) }}</b></div>
        <el-progress type="dashboard" :percentage="Math.min(100, Math.round(p.progressRate || 0))"
                     :width="112" color="#5B2533">
          <template #default="{ percentage }"><div class="pct">{{ percentage }}%</div><div class="pct-l">资金完成度</div></template>
        </el-progress>
      </div>
    </div>

    <div class="card tabs-card">
      <el-tabs v-model="tab">
        <el-tab-pane label="执行里程碑" name="ms">
          <el-timeline class="tl">
            <el-timeline-item v-for="m in milestones" :key="m.id"
                              :type="m.status === '已完成' ? 'success' : 'primary'"
                              :hollow="m.status !== '已完成'"
                              :timestamp="`计划 ${formatDate(m.planDate)}${m.finishDate ? ' · 完成 ' + formatDate(m.finishDate) : ''}`">
              <div class="tl-row">
                <b>{{ m.seqNo }}. {{ m.milestoneName }}</b>
                <el-tag size="small" :type="m.status === '已完成' ? 'success' : 'info'">{{ m.status }}</el-tag>
                <span class="muted">权重 {{ m.weight }}</span>
              </div>
              <div class="muted small">{{ m.deliverable }}</div>
            </el-timeline-item>
          </el-timeline>
          <el-empty v-if="!milestones.length" description="尚未登记里程碑" />
        </el-tab-pane>

        <el-tab-pane label="进展公示" name="progress">
          <el-timeline class="tl">
            <el-timeline-item v-for="g in progress" :key="g.id" :timestamp="formatTime(g.publishTime)"
                              :type="g.auditStatus === '已发布' ? 'success' : 'warning'">
              <div class="tl-row">
                <b>{{ g.stageName }}</b>
                <el-tag size="small" :type="g.auditStatus === '已发布' ? 'success' : 'warning'">{{ g.auditStatus }}</el-tag>
                <span class="muted">进度 {{ g.progressRate }}%</span>
              </div>
              <div class="small">{{ g.content }}</div>
              <div class="muted small">资金说明：{{ g.fundSummary }}</div>
              <img v-if="g.photoPath" class="ph" :src="g.photoPath" alt="" />
            </el-timeline-item>
          </el-timeline>
          <el-empty v-if="!progress.length" description="暂无进展公示" />
        </el-tab-pane>

        <el-tab-pane :label="`捐赠明细（${records.length}）`" name="records">
          <el-table :data="records" border size="small">
            <el-table-column prop="recordNo" label="登记编号" width="150" />
            <el-table-column prop="donorName" label="捐赠人" width="110" />
            <el-table-column prop="donorType" label="类型" width="90" />
            <el-table-column prop="amount" label="金额" width="120" align="right">
              <template #default="{ row }"><span class="num">{{ money(row.amount) }}</span></template>
            </el-table-column>
            <el-table-column prop="donateDate" label="捐赠日期" width="110">
              <template #default="{ row }">{{ formatDate(row.donateDate) }}</template>
            </el-table-column>
            <el-table-column prop="verifyStatus" label="核对状态" width="100">
              <template #default="{ row }">
                <el-tag size="small" :type="statusType(row.verifyStatus)">{{ row.verifyStatus }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="intention" label="捐赠意向" min-width="200" />
            <el-table-column label="凭证" width="90">
              <template #default="{ row }">
                <el-image v-if="row.voucherPath" :src="row.voucherPath" :preview-src-list="[row.voucherPath]"
                          fit="cover" style="width:44px;height:32px;border-radius:4px" />
                <span v-else class="muted">无</span>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <el-tab-pane :label="`附件凭证（${attachments.length}）`" name="att">
          <div class="atts">
            <div v-for="a in attachments" :key="a.id" class="att">
              <el-image :src="a.filePath" :preview-src-list="[a.filePath]" fit="cover" class="att-img" />
              <div class="att-name">{{ a.fileName }}</div>
              <div class="muted small">{{ a.bizType }} · {{ (a.fileSize / 1024).toFixed(0) }} KB</div>
            </div>
            <el-empty v-if="!attachments.length" description="暂无附件" />
          </div>
        </el-tab-pane>

        <el-tab-pane label="公开评分留痕" name="score">
          <div v-if="score" class="score">
            <div class="score-top">
              <div class="total">
                <b>{{ score.totalScore }}</b>
                <span>综合得分</span>
              </div>
              <div class="level" :style="{ color: levelColor(score.resultLevel), borderColor: levelColor(score.resultLevel) }">
                {{ score.resultLevel }}
              </div>
              <div class="score-meta">
                <div>规则版本 {{ score.ruleVersion }} · 计算人 {{ score.calcUser }}</div>
                <div class="muted">计算时间 {{ formatTime(score.calcTime) }}</div>
              </div>
            </div>
            <div class="factors">
              <div v-for="f in factors" :key="f.name" class="f-item">
                <div class="f-name">{{ f.name }}<span class="muted">（权重 {{ f.weight }}%）</span></div>
                <el-progress :percentage="Math.round(f.score)" :stroke-width="8" :color="levelColor(score.resultLevel)" />
                <div class="muted small">输入 {{ f.input }} · 加权 {{ f.weighted }} 分</div>
              </div>
            </div>
            <div class="explain">
              <p><b>结果解释：</b>{{ score.explanation }}</p>
              <p><b>未满足条件：</b>{{ score.unmetConditions }}</p>
              <p><b>改进建议：</b>{{ score.improveItems }}</p>
              <p v-if="score.manualLevel"><b>人工修正：</b>{{ score.manualLevel }}（{{ score.manualReason }}，{{ score.manualUser }}）</p>
              <p class="muted small">输入快照：{{ score.inputSnapshot }}</p>
            </div>
          </div>
          <el-empty v-else description="该项目尚未执行公开评分计算，可点击上方「重新计算公开评分」" />
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '@/utils/request'
import { formatTime, formatDate, money, wan, statusType, levelColor } from '@/utils/format'

const route = useRoute()
const id = route.params.id
const loading = ref(false)
const tab = ref('ms')
const p = ref({})
const milestones = ref([])
const progress = ref([])
const records = ref([])
const attachments = ref([])
const score = ref(null)
const factors = ref([])

/** 状态机与后端 NEXT 保持一致，前端只展示合法去向 */
const NEXT = {
  '项目立项': ['募集中', '已取消'],
  '募集中': ['执行中', '已取消'],
  '执行中': ['待验收', '已取消'],
  '待验收': ['已结项', '执行中'],
  '已结项': []
}
const nextStatus = computed(() => NEXT[p.value.status] || [])

async function load() {
  loading.value = true
  try {
    const d = await request.get(`/api/project/${id}/detail`)
    p.value = d.project || {}
    milestones.value = d.milestones || []
    progress.value = d.progress || []
    records.value = d.records || []
    attachments.value = d.attachments || []
    score.value = d.score || null
    if (score.value) await loadFactors()
  } finally { loading.value = false }
}

/** 明细分项：读取留痕的原始分项得分，配合当前规则权重展示加权过程（只读，不重复写库） */
async function loadFactors() {
  try {
    const rule = await request.get('/api/rule/active')
    const s = score.value
    const snap = JSON.parse(s.inputSnapshot || '{}')
    const w = [
      ['目标金额', s.targetScore, rule.targetWeight, `${fmtNum(snap.target)} 元`],
      ['已登记金额', s.amountScore, rule.amountWeight, `${fmtNum(snap.raised)} 元`],
      ['里程碑完成度', s.milestoneScore, rule.milestoneWeight, `${Math.round(snap.milestoneRate || 0)}%`],
      ['支出凭证', s.voucherScore, rule.voucherWeight, `${snap.voucherCount || 0} 份`],
      ['受益人数', s.beneficiaryScore, rule.beneficiaryWeight, `${snap.beneficiary || 0} 人`],
      ['公开审核状态', s.auditScore, rule.auditWeight, snap.publicStatus || '-']
    ]
    factors.value = w.map(([name, sc, weight, input]) => ({
      name, score: Number(sc || 0), weight: weight || 0, input,
      weighted: Math.round(Number(sc || 0) * (weight || 0)) / 100
    }))
  } catch (e) { factors.value = [] }
}
function fmtNum(v) {
  return v === null || v === undefined ? '-' : Number(v).toLocaleString('zh-CN')
}

async function transition(t) {
  let reason = ''
  if (t === '已取消') {
    const { value } = await ElMessageBox.prompt('取消项目必须填写原因（不少于 5 个字）', '取消项目', {
      inputType: 'textarea', inputValidator: (v) => ((v || '').trim().length >= 5 ? true : '原因不少于 5 个字')
    })
    reason = (value || '').trim()
  } else {
    await ElMessageBox.confirm(`确认将项目状态流转为「${t}」？`, '状态流转', { type: 'warning' })
  }
  await request.post(`/api/project/${id}/transition`, { status: t, reason })
  ElMessage.success('状态已更新')
  load()
}

async function evaluate() {
  await ElMessageBox.confirm('将按当前启用规则重新计算一次公开评分，并保存本次输入快照用于留痕。确认执行？', '重新计算', { type: 'warning' })
  const d = await request.post(`/api/score/project/${id}/evaluate`)
  factors.value = d.factors || []
  score.value = d.score
  ElMessage.success(`计算完成：${d.level}（${d.score.totalScore} 分）`)
}

onMounted(load)
</script>

<style scoped>
.detail-head { display: flex; gap: 20px; padding: 18px; margin-bottom: 16px; }
.cover { width: 220px; height: 148px; object-fit: cover; border-radius: 10px; flex: none; background: #EFE6E3; }
.info { flex: 1; min-width: 0; }
.title-row { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }
.title-row h1 { font-size: 20px; margin: 0; color: var(--text); }
.info p { font-size: 13px; margin: 0 0 10px; line-height: 1.6; }
.kv { display: flex; flex-wrap: wrap; gap: 8px 22px; font-size: 12px; color: var(--text3); margin-bottom: 12px; }
.kv b { color: var(--text); font-weight: 500; }
.ops { display: flex; gap: 8px; flex-wrap: wrap; }
.money { width: 200px; flex: none; display: flex; flex-direction: column; gap: 8px; align-items: flex-end; }
.m-item { text-align: right; }
.m-item span { display: block; font-size: 11px; color: var(--text3); }
.m-item b { font-size: 15px; color: var(--text); }
.up { color: #A61B29; }
.pct { font-size: 20px; font-weight: 600; color: #5B2533; }
.pct-l { font-size: 11px; color: var(--text3); }
.tabs-card { padding: 4px 20px 20px; }
.tl { padding-left: 4px; margin-top: 12px; }
.tl-row { display: flex; align-items: center; gap: 10px; margin-bottom: 4px; }
.small { font-size: 12px; }
.ph { width: 180px; height: 110px; object-fit: cover; border-radius: 8px; margin-top: 8px; }
.atts { display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 14px; padding-top: 8px; }
.att-img { width: 100%; height: 108px; border-radius: 8px; }
.att-name { font-size: 12px; margin-top: 6px; color: var(--text); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.score-top { display: flex; align-items: center; gap: 24px; padding: 8px 0 16px; }
.total b { font-size: 34px; color: #5B2533; }
.total span { display: block; font-size: 12px; color: var(--text3); }
.level { border: 1px solid; border-radius: 8px; padding: 6px 16px; font-size: 15px; font-weight: 600; }
.score-meta { font-size: 12px; color: var(--text2); }
.factors { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; }
.f-item { border: 1px solid var(--border); border-radius: 8px; padding: 10px 12px; }
.f-name { font-size: 13px; color: var(--text); margin-bottom: 6px; }
.explain { margin-top: 16px; background: #FAF7F5; border-radius: 8px; padding: 12px 16px; font-size: 13px; line-height: 1.8; color: var(--text2); }
.explain p { margin: 0; }
</style>
