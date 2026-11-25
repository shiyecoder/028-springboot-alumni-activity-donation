<template>
  <div>
    <div class="page-head">
      <div>
        <h1>计算留痕</h1>
        <p>每次公开评分都保存输入快照、规则版本与明细分项；人工修正只写修正字段，原始结果保持不变</p>
      </div>
      <div class="ops">
        <el-select v-model="projectId" filterable placeholder="选择项目执行计算" style="width:300px">
          <el-option v-for="p in projects" :key="p.id" :label="p.projectName" :value="p.id" />
        </el-select>
        <el-button type="primary" :loading="calculating" @click="evaluate">执行计算</el-button>
        <el-button plain @click="$router.push('/rule')">规则配置</el-button>
      </div>
    </div>

    <CrudPage ref="pageRef" :cfg="cfg">
      <template #row-actions="{ row }">
        <el-button link type="primary" @click="openDetail(row)">明细</el-button>
        <el-button link type="warning" @click="openManual(row)">人工修正</el-button>
      </template>
    </CrudPage>

    <el-drawer v-model="detailVisible" title="计算明细与结果解释" size="620px">
      <div v-if="cur" class="d">
        <div class="d-top">
          <div><b>{{ cur.projectName }}</b><div class="muted small">规则 {{ cur.ruleVersion }} · {{ formatTime(cur.calcTime) }} · {{ cur.calcUser }}</div></div>
          <div class="d-score">
            <b>{{ cur.totalScore }}</b>
            <span :style="{ color: levelColor(cur.resultLevel) }">{{ cur.resultLevel }}</span>
          </div>
        </div>
        <el-divider />
        <div v-for="f in cur.factors" :key="f.name" class="f">
          <div class="f-h"><span>{{ f.name }}</span><b class="num">{{ f.score }} × {{ f.weight }}% = {{ f.weighted }}</b></div>
          <el-progress :percentage="Math.round(f.score)" :stroke-width="7" :show-text="false"
                       :color="levelColor(cur.resultLevel)" />
          <div class="muted small">输入：{{ f.input }}（{{ f.note }}）</div>
        </div>
        <el-divider />
        <p><b>结果解释：</b>{{ cur.explanation }}</p>
        <p><b>未满足条件：</b>{{ cur.unmetConditions }}</p>
        <p><b>改进建议：</b>{{ cur.improveItems }}</p>
        <p class="snap">输入快照：{{ cur.inputSnapshot }}</p>
        <el-alert v-if="cur.manualLevel" type="warning" :closable="false"
                  :title="`人工修正为「${cur.manualLevel}」，原因：${cur.manualReason}（${cur.manualUser}）`" />
      </div>
    </el-drawer>

    <el-dialog v-model="manualVisible" title="人工修正结果等级" width="480px">
      <el-form label-width="90px">
        <el-form-item label="原始结果">
          <el-tag :type="'info'">{{ cur?.resultLevel }}（{{ cur?.totalScore }} 分）</el-tag>
        </el-form-item>
        <el-form-item label="修正为">
          <el-select v-model="manual.level" style="width:160px">
            <el-option v-for="l in ['推荐', '观察', '不推荐']" :key="l" :label="l" :value="l" />
          </el-select>
        </el-form-item>
        <el-form-item label="修正原因">
          <el-input v-model="manual.reason" type="textarea" :rows="3" placeholder="不少于 5 个字，将随修正一起留痕" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="manualVisible = false">取消</el-button>
        <el-button type="primary" @click="submitManual">提交修正</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import CrudPage from '@/components/CrudPage.vue'
import request from '@/utils/request'
import { formatTime, levelColor } from '@/utils/format'

const pageRef = ref()
const projects = ref([])
const projectId = ref(null)
const calculating = ref(false)
const detailVisible = ref(false)
const manualVisible = ref(false)
const cur = ref(null)
const manual = reactive({ level: '观察', reason: '' })

const cfg = {
  title: '计算记录',
  url: '/api/score',
  kwPlaceholder: '项目名称',
  statusOptions: ['推荐', '观察', '不推荐'],
  rowWidth: 210,
  readonly: true,
  noDelete: true,
  columns: [
    { prop: 'projectName', label: '项目', minWidth: 220, type: 'link' },
    { prop: 'ruleVersion', label: '规则版本', width: 100 },
    { prop: 'targetScore', label: '目标', width: 76, align: 'right' },
    { prop: 'amountScore', label: '已登记', width: 84, align: 'right' },
    { prop: 'milestoneScore', label: '里程碑', width: 84, align: 'right' },
    { prop: 'voucherScore', label: '凭证', width: 76, align: 'right' },
    { prop: 'beneficiaryScore', label: '受益', width: 76, align: 'right' },
    { prop: 'auditScore', label: '审核', width: 76, align: 'right' },
    { prop: 'totalScore', label: '总分', width: 84, align: 'right' },
    { prop: 'resultLevel', label: '结果', width: 100, type: 'status' },
    { prop: 'manualLevel', label: '人工修正', width: 100 },
    { prop: 'calcTime', label: '计算时间', width: 160, type: 'time' },
    { prop: 'calcUser', label: '计算人', width: 100 }
  ],
  fields: [
    { prop: 'projectName', label: '项目' },
    { prop: 'ruleVersion', label: '规则版本' },
    { prop: 'totalScore', label: '综合得分' },
    { prop: 'resultLevel', label: '结果等级' },
    { prop: 'explanation', label: '结果解释', type: 'textarea' },
    { prop: 'unmetConditions', label: '未满足条件', type: 'textarea' },
    { prop: 'improveItems', label: '改进建议', type: 'textarea' },
    { prop: 'inputSnapshot', label: '输入快照', type: 'textarea' },
    { prop: 'manualLevel', label: '人工修正等级' },
    { prop: 'manualReason', label: '修正原因', type: 'textarea' }
  ]
}

/** 由快照与分项得分还原明细分，避免再次调用计算接口产生重复留痕 */
async function buildFactors(row) {
  const rule = await request.get('/api/rule/active')
  const s = JSON.parse(row.inputSnapshot || '{}')
  const fmt = (v) => (v === undefined ? '-' : Number(v).toLocaleString('zh-CN'))
  return [
    { name: '目标金额', score: Number(row.targetScore || 0), weight: rule.targetWeight, input: `${fmt(s.target)} 元`, note: '目标金额越大，公开示范价值越高' },
    { name: '已登记金额', score: Number(row.amountScore || 0), weight: rule.amountWeight, input: `${fmt(s.raised)} 元`, note: '已核对金额 / 目标金额' },
    { name: '里程碑完成度', score: Number(row.milestoneScore || 0), weight: rule.milestoneWeight, input: `${Math.round(s.milestoneRate || 0)}%`, note: '已完成里程碑权重占比' },
    { name: '支出凭证', score: Number(row.voucherScore || 0), weight: rule.voucherWeight, input: `${s.voucherCount || 0} 份`, note: '凭证份数反映执行透明度' },
    { name: '受益人数', score: Number(row.beneficiaryScore || 0), weight: rule.beneficiaryWeight, input: `${s.beneficiary || 0} 人`, note: '受益人数体现社会效益' },
    { name: '公开审核状态', score: Number(row.auditScore || 0), weight: rule.auditWeight, input: s.publicStatus || '-', note: '进展公示需通过审核' }
  ].map((f) => ({ ...f, weighted: Math.round(f.score * f.weight) / 100 }))
}

async function openDetail(row) {
  const factors = await buildFactors(row)
  cur.value = { ...row, factors }
  detailVisible.value = true
}

function openManual(row) {
  cur.value = row
  manual.level = row.manualLevel || row.resultLevel
  manual.reason = row.manualReason || ''
  manualVisible.value = true
}

async function submitManual() {
  if ((manual.reason || '').trim().length < 5) { ElMessage.warning('修正原因不少于 5 个字'); return }
  await request.post(`/api/score/${cur.value.id}/manual`, { level: manual.level, reason: manual.reason.trim() })
  ElMessage.success('人工修正已保存，原始结果保持不变')
  manualVisible.value = false
  pageRef.value.reload()
}

async function evaluate() {
  if (!projectId.value) { ElMessage.warning('请先选择项目'); return }
  calculating.value = true
  try {
    const d = await request.post(`/api/score/project/${projectId.value}/evaluate`)
    ElMessage.success(`计算完成：${d.level}（${d.score.totalScore} 分）`)
    pageRef.value.reload()
  } finally { calculating.value = false }
}

async function loadProjects() {
  const d = await request.get('/api/project/page', { params: { page: 1, size: 200 } })
  projects.value = d.list || []
  if (projects.value.length) projectId.value = projects.value[0].id
}
onMounted(loadProjects)
</script>

<style scoped>
.page-head { display: flex; align-items: flex-end; justify-content: space-between; margin-bottom: 18px; }
.page-head h1 { font-size: 22px; margin: 0 0 6px; color: var(--text); }
.page-head p { font-size: 13px; color: var(--text3); margin: 0; }
.ops { display: flex; gap: 10px; }
.d-top { display: flex; justify-content: space-between; align-items: flex-start; }
.d-score { text-align: right; }
.d-score b { font-size: 28px; color: #5B2533; display: block; }
.f { margin-bottom: 12px; }
.f-h { display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 4px; color: var(--text); }
.d p { font-size: 13px; line-height: 1.8; color: var(--text2); margin: 6px 0; }
.snap { word-break: break-all; font-size: 12px; color: var(--text3); background: #FAF7F5; padding: 8px 10px; border-radius: 6px; }
.small { font-size: 12px; }
</style>
