<template>
  <div class="square" v-loading="loading">
    <div class="sq-head">
      <div>
        <h1>活动广场</h1>
        <p>报名中的校友活动一览，先到先得，满员自动进入候补队列</p>
      </div>
      <div class="sq-filter">
        <el-select v-model="type" placeholder="全部类型" clearable style="width:160px" @change="reload">
          <el-option v-for="t in types" :key="t" :label="t" :value="t" />
        </el-select>
        <el-input v-model="kw" placeholder="搜索活动" clearable style="width:220px" @keyup.enter="reload" @clear="reload" />
        <el-button type="primary" @click="reload">搜索</el-button>
      </div>
    </div>

    <div class="grid">
      <div v-for="a in rows" :key="a.id" class="card act">
        <div class="cover">
          <img :src="a.poster" :alt="a.title" />
          <span class="tag" :class="a.status === '报名中' ? 'on' : 'off'">{{ a.status }}</span>
        </div>
        <div class="body">
          <h3>{{ a.title }}</h3>
          <div class="meta"><el-icon><Calendar /></el-icon>{{ formatTime(a.startTime) }}</div>
          <div class="meta"><el-icon><Location /></el-icon>{{ a.location || '待定' }}</div>
          <div class="meta"><el-icon><OfficeBuilding /></el-icon>{{ a.orgName || a.college }}</div>
          <div class="bar-row">
            <span class="num">{{ a.signupCount || 0 }} / {{ a.capacity || 0 }}</span>
            <span class="muted">候补 {{ a.waitCount || 0 }}</span>
          </div>
          <el-progress :percentage="Math.min(100, Math.round(((a.signupCount || 0) * 100) / (a.capacity || 1)))"
                       :stroke-width="6" :show-text="false" color="#2F6F6A" />
          <el-button class="join" type="primary" :disabled="a.status !== '报名中' || signedIds.includes(a.id)"
                     @click="signup(a)">
            {{ signedIds.includes(a.id) ? '已报名' : a.status === '报名中' ? '立即报名' : '暂不可报名' }}
          </el-button>
        </div>
      </div>
      <el-empty v-if="!loading && !rows.length" description="暂无符合条件的活动" style="grid-column:1/-1" />
    </div>

    <el-pagination background layout="prev, pager, next" :total="total" v-model:current-page="page"
                   :page-size="9" @current-change="load" style="justify-content:center;margin-top:20px" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '@/utils/request'
import { store } from '@/store/user'
import { formatTime } from '@/utils/format'

const rows = ref([])
const total = ref(0)
const page = ref(1)
const kw = ref('')
const type = ref('')
const loading = ref(false)
const signedIds = ref([])
const types = ['校友返校', '行业沙龙', '公益徒步', '讲座论坛', '文体赛事', '年级聚会']

async function load() {
  loading.value = true
  try {
    const d = await request.get('/api/activity/page', {
      params: { page: page.value, size: 9, kw: kw.value, status: '报名中', activityType: type.value }
    })
    rows.value = d.list || []
    total.value = d.total || 0
  } finally { loading.value = false }
}
function reload() { page.value = 1; load() }

async function loadMine() {
  try {
    const d = await request.get('/api/signup/my')
    signedIds.value = (d || []).filter((s) => s.status !== '已取消').map((s) => s.activityId)
  } catch (e) { signedIds.value = [] }
}

async function signup(a) {
  const full = (a.signupCount || 0) >= (a.capacity || 0)
  await ElMessageBox.confirm(
    full ? '该活动名额已满，报名后将进入候补队列，有人取消时按报名时间自动递补。确认继续？' : `确认报名「${a.title}」？`,
    '报名确认', { type: 'warning' })
  const d = await request.post('/api/signup/apply', {
    activityId: a.id, alumniId: store.user.id, alumniName: store.user.realName, companionCount: 0
  })
  ElMessage.success(d.status === '候补' ? `名额已满，您已进入候补（序号 ${d.waitNo || '-'}）` : '报名成功，请按时到场')
  load(); loadMine()
}

onMounted(() => { load(); loadMine() })
</script>

<style scoped>
.square { max-width: 1180px; margin: 0 auto; padding: 24px 0 40px; }
.sq-head { display: flex; align-items: flex-end; justify-content: space-between; margin-bottom: 18px; }
.sq-head h1 { font-size: 22px; color: var(--text); margin: 0 0 6px; }
.sq-head p { font-size: 13px; color: var(--text3); margin: 0; }
.sq-filter { display: flex; gap: 10px; }
.grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; }
@media (max-width: 1100px) { .grid { grid-template-columns: repeat(2, 1fr); } }
.act { padding: 0; overflow: hidden; display: flex; flex-direction: column; }
.cover { position: relative; height: 152px; background: #EFE6E3; }
.cover img { width: 100%; height: 100%; object-fit: cover; display: block; }
.tag { position: absolute; top: 10px; left: 10px; padding: 2px 9px; border-radius: 10px; font-size: 11px; color: #fff; }
.tag.on { background: #2D765C; }
.tag.off { background: rgba(0,0,0,.45); }
.body { padding: 14px 16px 16px; display: flex; flex-direction: column; gap: 6px; flex: 1; }
.body h3 { font-size: 15px; margin: 0 0 2px; color: var(--text); line-height: 1.4; }
.meta { display: flex; align-items: center; gap: 6px; font-size: 12px; color: var(--text3); }
.bar-row { display: flex; justify-content: space-between; font-size: 12px; color: var(--text2); margin-top: 6px; }
.join { margin-top: 10px; width: 100%; }
</style>
