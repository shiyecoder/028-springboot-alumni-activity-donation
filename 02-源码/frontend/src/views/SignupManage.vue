<template>
  <div>
    <div class="page-head">
      <div>
        <h1>报名与签到</h1>
        <p>按活动查看报名名单；满员自动进入候补，有人取消后按报名时间自动递补，也可手工转正</p>
      </div>
      <el-select v-model="activityId" filterable placeholder="选择活动查看名单" style="width:340px" @change="onActivity">
        <el-option v-for="a in activities" :key="a.id" :label="`${a.title}（${a.status}）`" :value="a.id" />
      </el-select>
    </div>

    <div class="stat-row">
      <div class="stat"><b>{{ stat.signup }}</b><span>已报名</span></div>
      <div class="stat"><b>{{ stat.wait }}</b><span>候补中</span></div>
      <div class="stat"><b>{{ stat.checkin }}</b><span>已签到</span></div>
      <div class="stat"><b>{{ stat.rate }}%</b><span>到场率</span></div>
    </div>

    <CrudPage ref="pageRef" :cfg="cfg">
      <template #row-actions="{ row }">
        <el-button v-if="['已报名', '候补', '未到场'].includes(row.status)" link type="success"
                   @click="onCheckin(row)">签到</el-button>
        <el-button v-if="row.status === '候补'" link type="primary" @click="onPromote(row)">转正</el-button>
      </template>
    </CrudPage>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import CrudPage from '@/components/CrudPage.vue'
import request from '@/utils/request'

const pageRef = ref()
const activities = ref([])
const activityId = ref(null)
const stat = reactive({ signup: 0, wait: 0, checkin: 0, rate: 0 })

const cfg = {
  title: '报名记录',
  url: '/api/signup',
  kwPlaceholder: '校友姓名',
  statusOptions: ['已报名', '候补', '已签到', '未到场', '已取消'],
  rowWidth: 170,
  readonly: true,
  noDelete: true,
  params: {},
  columns: [
    { prop: 'signupNo', label: '报名编号', width: 150 },
    { prop: 'alumniName', label: '校友', width: 100, type: 'link' },
    { prop: 'activityTitle', label: '活动', minWidth: 220 },
    { prop: 'companionCount', label: '同行', width: 70, type: 'num' },
    { prop: 'waitNo', label: '候补序号', width: 90, type: 'num' },
    { prop: 'checkinCode', label: '签到码', width: 90 },
    { prop: 'status', label: '状态', width: 100, type: 'status' },
    { prop: 'checkinTime', label: '签到时间', width: 160, type: 'time' },
    { prop: 'createTime', label: '报名时间', width: 160, type: 'time' }
  ],
  fields: [
    { prop: 'signupNo', label: '报名编号' },
    { prop: 'alumniName', label: '校友' },
    { prop: 'activityTitle', label: '活动' },
    { prop: 'companionCount', label: '同行人数' },
    { prop: 'waitNo', label: '候补序号' },
    { prop: 'checkinCode', label: '签到验证码' },
    { prop: 'status', label: '状态' },
    { prop: 'remark', label: '备注', type: 'textarea' }
  ]
}

async function loadActivities() {
  const d = await request.get('/api/activity/page', { params: { page: 1, size: 100 } })
  activities.value = d.list || []
  // 默认选中最近一场可报名的活动，避免一进页面就是空名单
  const first = activities.value.find((a) => a.status === '报名中')
    || activities.value.find((a) => a.status === '进行中')
    || activities.value[0]
  if (first) {
    activityId.value = first.id
    onActivity()
  }
}
function onActivity() {
  cfg.params.activityId = activityId.value
  stat.signup = stat.wait = stat.checkin = 0
  stat.rate = 0
  const a = activities.value.find((x) => x.id === activityId.value)
  if (a) {
    stat.signup = a.signupCount || 0
    stat.wait = a.waitCount || 0
    stat.checkin = a.checkinCount || 0
    stat.rate = stat.signup ? Math.round((stat.checkin * 100) / stat.signup) : 0
  }
  if (pageRef.value) pageRef.value.reload()
}

async function onCheckin(row) {
  let code = ''
  try {
    const { value } = await ElMessageBox.prompt(`为「${row.alumniName}」登记签到（留空表示工作人员手工补签）`,
      '现场签到', { inputPlaceholder: `默认签到码 ${row.checkinCode || ''}`, inputValidator: () => true })
    code = (value || '').trim()
  } catch (e) { return }
  await request.post(`/api/signup/${row.id}/checkin`, { code })
  ElMessage.success('签到成功')
  pageRef.value.reload()
  const a = activities.value.find((x) => x.id === activityId.value)
  if (a) a.checkinCount = (a.checkinCount || 0) + 1
  onActivity()
}

async function onPromote(row) {
  await ElMessageBox.confirm(`确认将候补的「${row.alumniName}」转为正式报名？`, '候补转正', { type: 'warning' })
  await request.post(`/api/signup/${row.id}/promote`)
  ElMessage.success('已转为正式报名')
  onActivity()
}

onMounted(loadActivities)
</script>

<style scoped>
.page-head { display: flex; align-items: flex-end; justify-content: space-between; margin-bottom: 16px; }
.page-head h1 { font-size: 22px; margin: 0 0 6px; color: var(--text); }
.page-head p { font-size: 13px; color: var(--text3); margin: 0; }
.stat-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 16px; }
.stat { background: #fff; border: 1px solid var(--border); border-radius: 10px; padding: 12px 18px;
  display: flex; align-items: baseline; gap: 10px; }
.stat b { font-size: 22px; color: #5B2533; font-variant-numeric: tabular-nums; }
.stat span { font-size: 12px; color: var(--text3); }
</style>
