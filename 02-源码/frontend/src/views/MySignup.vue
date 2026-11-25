<template>
  <div class="my" v-loading="loading">
    <div class="page-head">
      <div>
        <h1>我的报名</h1>
        <p>报名后会生成唯一签到码，现场出示即可签到；满员时自动进入候补，有人取消按顺序递补</p>
      </div>
      <el-button plain @click="$router.push('/activity-square')">去活动广场</el-button>
    </div>

    <div class="stats">
      <div class="s"><b>{{ rows.length }}</b><span>累计报名</span></div>
      <div class="s"><b>{{ count('已签到') }}</b><span>已参加</span></div>
      <div class="s"><b>{{ count('候补') }}</b><span>候补中</span></div>
      <div class="s"><b>{{ count('已报名') }}</b><span>待到场</span></div>
    </div>

    <div class="list">
      <div v-for="r in rows" :key="r.id" class="card item">
        <div class="l">
          <h3>{{ r.activityTitle }}</h3>
          <div class="meta"><span class="num">报名号 {{ r.signupNo }}</span><span>同行 {{ r.companionCount }} 人</span>
            <span>报名于 {{ formatTime(r.createTime) }}</span></div>
        </div>
        <div class="m">
          <div v-if="r.status === '已签到'" class="code done">已签到 {{ formatTime(r.checkinTime) }}</div>
          <div v-else class="code">签到码 <b>{{ r.checkinCode }}</b></div>
          <div v-if="r.waitNo" class="muted small">候补序号 {{ r.waitNo }}</div>
        </div>
        <div class="r">
          <el-tag :type="statusType(r.status)" effect="light">{{ r.status }}</el-tag>
          <el-button v-if="['已报名', '候补'].includes(r.status)" link type="danger" @click="cancel(r)">取消报名</el-button>
        </div>
      </div>
      <el-empty v-if="!loading && !rows.length" description="还没有报名记录，去活动广场看看">
        <el-button type="primary" @click="$router.push('/activity-square')">去报名</el-button>
      </el-empty>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '@/utils/request'
import { formatTime, statusType } from '@/utils/format'

const rows = ref([])
const loading = ref(false)
const count = (s) => rows.value.filter((r) => r.status === s).length

async function load() {
  loading.value = true
  try {
    const d = await request.get('/api/signup/my')
    rows.value = d || []
  } finally { loading.value = false }
}

async function cancel(r) {
  await ElMessageBox.confirm('取消后如为候补首位将自动递补他人，确认取消报名？', '取消报名', { type: 'warning' })
  const d = await request.post(`/api/signup/${r.id}/cancel`)
  ElMessage.success(d && d.promoted ? `已取消，候补校友「${d.promoted}」已自动递补` : '已取消报名')
  load()
}

onMounted(load)
</script>

<style scoped>
.my { max-width: 1040px; margin: 0 auto; padding: 24px 0 40px; }
.page-head { display: flex; align-items: flex-end; justify-content: space-between; margin-bottom: 18px; }
.page-head h1 { font-size: 22px; margin: 0 0 6px; color: var(--text); }
.page-head p { font-size: 13px; color: var(--text3); margin: 0; }
.stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 18px; }
.s { background: #fff; border: 1px solid var(--border); border-radius: 10px; padding: 14px 18px; }
.s b { font-size: 22px; color: #5B2533; display: block; }
.s span { font-size: 12px; color: var(--text3); }
.list { display: flex; flex-direction: column; gap: 12px; }
.item { display: flex; align-items: center; gap: 18px; padding: 16px 20px; }
.l { flex: 1; min-width: 0; }
.l h3 { margin: 0 0 6px; font-size: 15px; color: var(--text); }
.meta { display: flex; gap: 18px; font-size: 12px; color: var(--text3); }
.m { text-align: center; }
.code { font-size: 12px; color: var(--text3); }
.code b { font-size: 18px; color: #5B2533; letter-spacing: 2px; }
.code.done { color: #2D765C; }
.r { display: flex; flex-direction: column; align-items: flex-end; gap: 6px; width: 120px; }
.small { font-size: 11px; }
</style>
