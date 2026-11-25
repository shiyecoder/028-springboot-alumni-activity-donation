<template>
  <div v-loading="loading">
    <div class="page-head">
      <div>
        <h1>捐赠公开规则</h1>
        <p>创新模块「捐赠目标与执行里程碑公开」的评分权重配置，保存后自动生成新版本并停用旧版本</p>
      </div>
      <el-tag v-if="active" type="success" effect="light">当前启用 {{ active.version }}</el-tag>
    </div>

    <div class="rule-grid">
      <div class="card panel">
        <div class="card-h"><h2>权重配置</h2><span class="muted">六项权重合计必须等于 100%</span></div>
        <div class="card-b">
          <div v-for="f in factors" :key="f.key" class="row">
            <div class="row-h">
              <span>{{ f.label }}</span>
              <b class="num">{{ form[f.key] }}%</b>
            </div>
            <el-slider v-model="form[f.key]" :max="60" :step="5" show-stops />
            <div class="hint">{{ f.hint }}</div>
          </div>

          <div class="sum" :class="{ bad: sum !== 100 }">
            权重合计 <b>{{ sum }}%</b>
            <span v-if="sum !== 100">（需调整为 100% 才能保存）</span>
            <span v-else>（校验通过）</span>
          </div>

          <div class="level-row">
            <div>
              <span class="lbl">推荐线</span>
              <el-input-number v-model="form.goodScore" :min="50" :max="100" size="small" />
            </div>
            <div>
              <span class="lbl">观察线</span>
              <el-input-number v-model="form.passScore" :min="10" :max="99" size="small" />
            </div>
            <div class="grow">
              <span class="lbl">规则名称</span>
              <el-input v-model="form.ruleName" size="small" />
            </div>
          </div>

          <div class="actions">
            <el-button type="primary" :disabled="sum !== 100" :loading="saving" @click="save">保存为新版本</el-button>
            <el-button @click="reset">恢复当前启用值</el-button>
          </div>
          <p class="muted small">说明：保存后旧版本状态改为「停用」但保留历史，已产生的计算结果不受影响，可追溯当时的规则版本。</p>
        </div>
      </div>

      <div class="card panel">
        <div class="card-h"><h2>评分口径</h2></div>
        <div class="card-b">
          <div v-for="c in calibers" :key="c.name" class="cal">
            <b>{{ c.name }}</b>
            <span>{{ c.desc }}</span>
          </div>
          <el-divider />
          <div class="cal"><b>结果等级</b><span>总分 ≥ 推荐线判「推荐」，≥ 观察线判「观察」，否则「不推荐」</span></div>
          <div class="cal"><b>计算留痕</b><span>每次计算保存输入快照（目标/已登记/里程碑完成度/凭证数/受益人数/审核状态）与规则版本</span></div>
          <div class="cal"><b>人工修正</b><span>允许修正等级并必须填写原因，原始结果字段保留不被覆盖，便于效果统计对比</span></div>
        </div>
      </div>
    </div>

    <div class="card">
      <div class="card-h"><h2>版本历史</h2><div class="r">共 {{ history.length }} 个版本</div></div>
      <el-table :data="history" border size="small">
        <el-table-column prop="version" label="版本" width="80" />
        <el-table-column prop="ruleName" label="规则名称" min-width="180" />
        <el-table-column prop="targetWeight" label="目标" width="70" align="center" />
        <el-table-column prop="amountWeight" label="已登记" width="80" align="center" />
        <el-table-column prop="milestoneWeight" label="里程碑" width="80" align="center" />
        <el-table-column prop="voucherWeight" label="凭证" width="70" align="center" />
        <el-table-column prop="beneficiaryWeight" label="受益" width="70" align="center" />
        <el-table-column prop="auditWeight" label="审核" width="70" align="center" />
        <el-table-column prop="goodScore" label="推荐线" width="80" align="center" />
        <el-table-column prop="passScore" label="观察线" width="80" align="center" />
        <el-table-column prop="status" label="状态" width="90">
          <template #default="{ row }">
            <el-tag size="small" :type="row.status === '启用' ? 'success' : 'info'">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="effectTime" label="生效时间" width="160">
          <template #default="{ row }">{{ formatTime(row.effectTime) }}</template>
        </el-table-column>
        <el-table-column prop="createUser" label="创建人" width="110" />
      </el-table>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '@/utils/request'
import { formatTime } from '@/utils/format'

const loading = ref(false)
const saving = ref(false)
const active = ref(null)
const history = ref([])
const form = reactive({
  ruleName: '捐赠目标与执行里程碑公开',
  targetWeight: 15, amountWeight: 25, milestoneWeight: 20,
  voucherWeight: 15, beneficiaryWeight: 15, auditWeight: 10,
  goodScore: 80, passScore: 60
})

const factors = [
  { key: 'targetWeight', label: '目标金额', hint: '目标越大，公开示范价值越高；按目标 / 50 万折算' },
  { key: 'amountWeight', label: '已登记金额', hint: '已核对金额 / 目标金额，体现募集达成度' },
  { key: 'milestoneWeight', label: '里程碑完成度', hint: '已完成里程碑权重之和 / 全部权重' },
  { key: 'voucherWeight', label: '支出凭证', hint: '凭证份数 × 12.5 封顶 100，反映执行透明度' },
  { key: 'beneficiaryWeight', label: '受益人数', hint: '受益人数 / 1000 折算，体现社会效益' },
  { key: 'auditWeight', label: '公开审核状态', hint: '已通过 100、待审核 30、已驳回 0' }
]
const calibers = [
  { name: '目标金额', desc: '得分 = MIN(目标金额 / 500000 × 100, 100)' },
  { name: '已登记金额', desc: '得分 = MIN(已核对金额 / 目标金额 × 100, 100)' },
  { name: '里程碑完成度', desc: '得分 = 已完成里程碑权重 / 全部里程碑权重 × 100' },
  { name: '支出凭证', desc: '得分 = MIN(凭证份数 × 12.5, 100)' },
  { name: '受益人数', desc: '得分 = MIN(受益人数 / 1000 × 100, 100)' },
  { name: '公开审核状态', desc: '已通过 100 / 待审核 30 / 已驳回 0' }
]

const sum = computed(() => factors.reduce((s, f) => s + Number(form[f.key] || 0), 0))

function fill(r) {
  active.value = r
  Object.keys(form).forEach((k) => { if (r[k] !== undefined && r[k] !== null) form[k] = r[k] })
}

async function load() {
  loading.value = true
  try {
    const [a, h] = await Promise.all([request.get('/api/rule/active'), request.get('/api/rule/list')])
    fill(a)
    history.value = h || []
  } finally { loading.value = false }
}
function reset() { if (active.value) fill(active.value) }

async function save() {
  await ElMessageBox.confirm(`保存后生成新版本，旧版本「${active.value?.version || ''}」将被停用。确认保存？`, '保存规则', { type: 'warning' })
  saving.value = true
  try {
    const d = await request.post('/api/rule/save', { ...form })
    ElMessage.success(`已保存为新版本 ${d.version}`)
    load()
  } finally { saving.value = false }
}

onMounted(load)
</script>

<style scoped>
.page-head { display: flex; align-items: flex-end; justify-content: space-between; margin-bottom: 18px; }
.page-head h1 { font-size: 22px; margin: 0 0 6px; color: var(--text); }
.page-head p { font-size: 13px; color: var(--text3); margin: 0; }
.rule-grid { display: grid; grid-template-columns: 1.35fr 1fr; gap: 18px; margin-bottom: 18px; }
@media (max-width: 1200px) { .rule-grid { grid-template-columns: 1fr; } }
.row { margin-bottom: 10px; }
.row-h { display: flex; justify-content: space-between; font-size: 13px; color: var(--text); margin-bottom: 2px; }
.row-h b { color: #5B2533; }
.hint { font-size: 11px; color: var(--text3); }
.sum { margin: 14px 0; padding: 10px 14px; border-radius: 8px; background: #EDF5F2; color: #2D765C; font-size: 13px; }
.sum.bad { background: #FBECEA; color: #A61B29; }
.level-row { display: flex; gap: 18px; align-items: center; margin-bottom: 14px; }
.level-row .lbl { font-size: 12px; color: var(--text3); margin-right: 6px; }
.grow { flex: 1; }
.actions { display: flex; gap: 10px; }
.cal { margin-bottom: 10px; }
.cal b { display: block; font-size: 13px; color: var(--text); font-weight: 500; margin-bottom: 2px; }
.cal span { font-size: 12px; color: var(--text3); line-height: 1.6; }
.small { font-size: 12px; }
</style>
