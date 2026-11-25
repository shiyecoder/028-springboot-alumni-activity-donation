<template>
  <div class="pub" v-loading="loading">
    <header class="top">
      <div class="brand"><span class="logo">校</span>校友捐赠公开平台</div>
      <div class="nav">
        <a class="on">项目公开</a>
        <a @click="$router.push('/login')">工作台登录</a>
      </div>
    </header>

    <section class="hero">
      <div class="hero-in">
        <h1>每一笔捐赠，都看得见去向</h1>
        <p>公开项目目标、筹资进度、执行里程碑与支出凭证，捐赠明细经财务核对后计入实收</p>
        <div class="nums">
          <div><b>{{ stat.projectCount || 0 }}</b><span>公开项目</span></div>
          <div><b>{{ wan(stat.raisedAmount) }}</b><span>累计募集</span></div>
          <div><b>{{ stat.donorCount || 0 }}</b><span>有效捐赠笔数</span></div>
          <div><b>{{ stat.beneficiary || 0 }}</b><span>累计受益人数</span></div>
        </div>
      </div>
    </section>

    <section class="body">
      <div class="filter">
        <el-input v-model="kw" placeholder="搜索项目名称" clearable style="width:300px"
                  @keyup.enter="reload" @clear="reload" />
        <el-button type="primary" @click="reload">搜索</el-button>
        <span class="muted">共 {{ total }} 个项目已通过公开审核</span>
      </div>

      <div class="grid">
        <div v-for="p in rows" :key="p.id" class="card proj" @click="$router.push('/public/projects/' + p.id)">
          <div class="cover"><img :src="p.coverImage" :alt="p.projectName" /></div>
          <div class="c-body">
            <h3>{{ p.projectName }}</h3>
            <p class="desc">{{ p.publicDesc || p.purpose }}</p>
            <div class="bar">
              <el-progress :percentage="Math.min(100, Math.round(p.progressRate || 0))" :stroke-width="8"
                           :show-text="false" color="#5B2533" />
              <div class="bar-t"><span>{{ Math.round(p.progressRate || 0) }}%</span>
                <span class="muted">{{ wan(p.raisedAmount) }} / {{ wan(p.targetAmount) }}</span></div>
            </div>
            <div class="foot">
              <span>里程碑 {{ Math.round(p.milestoneRate || 0) }}%</span>
              <span>受益 {{ p.beneficiaryCount || 0 }} 人</span>
              <span>{{ p.deptName }}</span>
            </div>
          </div>
        </div>
        <el-empty v-if="!loading && !rows.length" description="暂无公开项目" style="grid-column:1/-1" />
      </div>

      <el-pagination background layout="prev, pager, next" :total="total" v-model:current-page="page"
                     :page-size="9" @current-change="load" style="justify-content:center;margin-top:26px" />
    </section>

    <footer class="foot-bar">数据来源于校友会捐赠管理系统 · 仅展示经审核公开的信息</footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import request from '@/utils/request'
import { wan } from '@/utils/format'

const rows = ref([])
const total = ref(0)
const page = ref(1)
const kw = ref('')
const loading = ref(false)
const stat = ref({})

async function load() {
  loading.value = true
  try {
    const d = await request.get('/api/public/projects', { params: { page: page.value, size: 9, kw: kw.value } })
    rows.value = d.list || []
    total.value = d.total || 0
  } finally { loading.value = false }
}
function reload() { page.value = 1; load() }

onMounted(async () => {
  load()
  stat.value = await request.get('/api/public/stats')
})
</script>

<style scoped>
.pub { min-height: 100vh; background: #FAF7F5; }
.top { height: 60px; background: #fff; border-bottom: 1px solid #E7DFDC; display: flex; align-items: center;
  justify-content: space-between; padding: 0 48px; }
.brand { display: flex; align-items: center; gap: 10px; font-size: 15px; font-weight: 600; color: #5B2533; }
.logo { width: 24px; height: 24px; border-radius: 6px; background: #5B2533; color: #fff; display: inline-flex;
  align-items: center; justify-content: center; font-size: 12px; }
.nav { display: flex; gap: 22px; font-size: 14px; color: #6B5F5C; }
.nav a { cursor: pointer; }
.nav a.on { color: #5B2533; font-weight: 500; }
.hero { background: linear-gradient(120deg, #431B26, #5B2533 55%, #7A3947); color: #fff; padding: 46px 48px 40px; }
.hero-in { max-width: 1180px; margin: 0 auto; }
.hero h1 { font-size: 30px; margin: 0 0 10px; font-weight: 600; }
.hero p { font-size: 14px; color: rgba(255,255,255,.78); margin: 0 0 26px; }
.nums { display: grid; grid-template-columns: repeat(4, 1fr); gap: 18px; max-width: 760px; }
.nums b { font-size: 26px; display: block; }
.nums span { font-size: 12px; color: rgba(255,255,255,.7); }
.body { max-width: 1180px; margin: 0 auto; padding: 26px 24px 40px; }
.filter { display: flex; align-items: center; gap: 12px; margin-bottom: 20px; }
.grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; }
@media (max-width: 1100px) { .grid { grid-template-columns: repeat(2, 1fr); } }
.proj { padding: 0; overflow: hidden; cursor: pointer; transition: box-shadow .2s, transform .2s; }
.proj:hover { box-shadow: 0 10px 26px rgba(91,37,51,.13); transform: translateY(-2px); }
.cover { height: 148px; background: #EFE6E3; }
.cover img { width: 100%; height: 100%; object-fit: cover; display: block; }
.c-body { padding: 14px 16px 16px; }
.c-body h3 { margin: 0 0 6px; font-size: 15px; color: #2E2422; }
.desc { font-size: 12px; color: #8C8279; margin: 0 0 12px; height: 34px; overflow: hidden;
  display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; }
.bar-t { display: flex; justify-content: space-between; font-size: 12px; margin-top: 4px; color: #5B2533; }
.foot { display: flex; gap: 14px; font-size: 12px; color: #8C8279; margin-top: 10px;
  border-top: 1px dashed #E7DFDC; padding-top: 10px; }
.foot-bar { text-align: center; font-size: 12px; color: #A79C97; padding: 22px 0 30px; }
</style>
