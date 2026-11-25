<template>
  <div class="my" v-loading="loading">
    <div class="page-head">
      <div>
        <h1>我的证书</h1>
        <p>感谢证书在捐赠核对通过后开具，可下载留作纪念</p>
      </div>
    </div>

    <div class="certs">
      <div v-for="c in rows" :key="c.id" class="cert">
        <div class="c-head">
          <span class="badge">捐赠感谢证书</span>
          <span class="num">{{ c.certNo }}</span>
        </div>
        <div class="c-body">
          <p class="thanks">感谢</p>
          <h2>{{ c.donorName }}</h2>
          <p class="txt">您向「{{ c.projectName }}」捐赠人民币</p>
          <p class="amount">{{ money(c.amount) }}</p>
          <p class="txt">谨此致谢，您的支持将转化为实实在在的公益成果。</p>
        </div>
        <div class="c-foot">
          <span>{{ formatDate(c.issueDate) }}</span>
          <el-tag size="small" :type="c.sendStatus === '已发放' ? 'success' : 'warning'" effect="plain">{{ c.sendStatus }}</el-tag>
        </div>
      </div>
      <el-empty v-if="!loading && !rows.length" description="暂无感谢证书，完成捐赠并核对通过后自动开具" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import request from '@/utils/request'
import { store } from '@/store/user'
import { formatDate, money } from '@/utils/format'

const rows = ref([])
const loading = ref(false)

async function load() {
  loading.value = true
  try {
    const d = await request.get('/api/cert/page', {
      params: { page: 1, size: 50, donorAlumniId: store.user?.id }
    })
    rows.value = d.list || []
  } finally { loading.value = false }
}
onMounted(load)
</script>

<style scoped>
.my { max-width: 1040px; margin: 0 auto; padding: 24px 0 40px; }
.page-head { margin-bottom: 18px; }
.page-head h1 { font-size: 22px; margin: 0 0 6px; color: var(--text); }
.page-head p { font-size: 13px; color: var(--text3); margin: 0; }
.certs { display: grid; grid-template-columns: repeat(2, 1fr); gap: 18px; }
.cert { background: #fff; border: 1px solid var(--border); border-radius: 12px; overflow: hidden;
  box-shadow: 0 6px 18px rgba(91,37,51,.06); }
.c-head { display: flex; justify-content: space-between; align-items: center; padding: 12px 20px;
  background: linear-gradient(90deg, #5B2533, #7A3947); color: #fff; font-size: 12px; }
.badge { letter-spacing: 2px; }
.c-body { padding: 22px 24px 10px; text-align: center; position: relative; }
.c-body::after { content: ''; position: absolute; right: 18px; top: 18px; width: 54px; height: 54px;
  border: 2px solid rgba(166,27,41,.35); border-radius: 50%; }
.thanks { font-size: 12px; color: var(--text3); margin: 0; letter-spacing: 4px; }
.c-body h2 { font-size: 22px; margin: 6px 0 10px; color: #5B2533; }
.txt { font-size: 13px; color: var(--text2); margin: 4px 0; line-height: 1.8; }
.amount { font-size: 24px; color: #A61B29; margin: 8px 0; font-weight: 600; }
.c-foot { display: flex; justify-content: space-between; align-items: center; padding: 12px 20px;
  border-top: 1px dashed var(--border); font-size: 12px; color: var(--text3); }
</style>
