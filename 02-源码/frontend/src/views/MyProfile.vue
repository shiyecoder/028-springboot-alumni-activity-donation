<template>
  <div class="my" v-loading="loading">
    <div class="page-head">
      <div>
        <h1>我的档案</h1>
        <p>档案信息由本人提交认证后生成，修改请提交变更申请，审核通过后生效</p>
      </div>
      <div>
        <el-tag v-if="!profile" type="warning" effect="light">尚未提交认证</el-tag>
        <el-tag v-else :type="statusType(profile.certStatus)" effect="light">{{ profile.certStatus }}</el-tag>
      </div>
    </div>

    <div v-if="!profile" class="card empty-card">
      <el-empty description="您还没有提交校友认证，提交后由校友办审核">
        <el-button type="primary" @click="applyVisible = true">提交认证申请</el-button>
      </el-empty>
    </div>

    <template v-else>
      <div class="cols">
        <div class="card hero">
          <img class="avatar" :src="profile.avatar" alt="" />
          <div class="who">
            <h3>{{ profile.realName }}<span class="muted">（{{ profile.gender }}）</span></h3>
            <p class="muted">{{ profile.college }} · {{ profile.major }} · {{ profile.className }}</p>
            <p class="muted">{{ profile.graduateYear }} 届 · 学号 {{ profile.studentNo }}</p>
            <div class="tags">
              <el-tag size="small" effect="plain">{{ profile.alumniNo }}</el-tag>
              <el-tag size="small" effect="plain" type="info">{{ profile.certStatus }}</el-tag>
            </div>
          </div>
        </div>

        <div class="card info">
          <div class="card-h"><h2>联系与职业信息</h2><el-button link type="primary" @click="changeVisible = true">申请变更</el-button></div>
          <div class="grid2">
            <div class="kv"><span>手机</span><b>{{ profile.phone || '未填写' }}</b></div>
            <div class="kv"><span>邮箱</span><b>{{ profile.email || '未填写' }}</b></div>
            <div class="kv"><span>工作单位</span><b>{{ profile.workUnit || '未填写' }}</b></div>
            <div class="kv"><span>职务</span><b>{{ profile.workTitle || '未填写' }}</b></div>
            <div class="kv"><span>所在地区</span><b>{{ profile.regionName || '未填写' }}</b></div>
            <div class="kv"><span>所属行业</span><b>{{ profile.industry || '未填写' }}</b></div>
          </div>
        </div>

        <div class="card privacy">
          <div class="card-h"><h2>隐私设置</h2><span class="muted">关闭后公开端不展示</span></div>
          <div class="card-b">
            <div class="sw"><span>展示手机号</span><el-switch v-model="pv.showPhone" :active-value="1" :inactive-value="0" @change="savePrivacy" /></div>
            <div class="sw"><span>展示邮箱</span><el-switch v-model="pv.showEmail" :active-value="1" :inactive-value="0" @change="savePrivacy" /></div>
            <div class="sw"><span>展示工作单位</span><el-switch v-model="pv.showUnit" :active-value="1" :inactive-value="0" @change="savePrivacy" /></div>
            <div class="sw"><span>展示所在地区</span><el-switch v-model="pv.showRegion" :active-value="1" :inactive-value="0" @change="savePrivacy" /></div>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="card-h"><h2>我的变更申请</h2><div class="r">共 {{ changes.length }} 条</div></div>
        <el-table :data="changes" border size="small">
          <el-table-column prop="changeType" label="类型" width="120" />
          <el-table-column prop="fieldName" label="字段" width="120" />
          <el-table-column prop="oldValue" label="变更前" min-width="160" />
          <el-table-column prop="newValue" label="变更后" min-width="160" />
          <el-table-column prop="auditStatus" label="状态" width="100">
            <template #default="{ row }">
              <el-tag size="small" :type="statusType(row.auditStatus)">{{ row.auditStatus }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="auditRemark" label="审核意见" min-width="180" />
          <el-table-column prop="createTime" label="申请时间" width="160">
            <template #default="{ row }">{{ formatTime(row.createTime) }}</template>
          </el-table-column>
        </el-table>
        <el-empty v-if="!changes.length" description="暂无变更申请" />
      </div>
    </template>

    <el-dialog v-model="applyVisible" title="提交校友认证" width="560px">
      <el-form :model="form" label-width="90px">
        <el-form-item label="姓名"><el-input v-model="form.realName" /></el-form-item>
        <el-form-item label="学号"><el-input v-model="form.studentNo" /></el-form-item>
        <el-form-item label="学院"><el-input v-model="form.college" /></el-form-item>
        <el-form-item label="专业"><el-input v-model="form.major" /></el-form-item>
        <el-form-item label="毕业年份"><el-input-number v-model="form.graduateYear" :min="1980" :max="2035" /></el-form-item>
        <el-form-item label="手机"><el-input v-model="form.phone" /></el-form-item>
        <el-form-item label="认证材料"><el-input v-model="form.certMaterial" type="textarea" :rows="2" placeholder="毕业证/学位证编号或说明" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="applyVisible = false">取消</el-button>
        <el-button type="primary" @click="submitApply">提交</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="changeVisible" title="提交变更申请" width="520px">
      <el-form :model="chg" label-width="90px">
        <el-form-item label="变更字段">
          <el-select v-model="chg.fieldName" style="width:200px">
            <el-option v-for="f in changeFields" :key="f" :label="f" :value="f" />
          </el-select>
        </el-form-item>
        <el-form-item label="变更后"><el-input v-model="chg.newValue" /></el-form-item>
        <el-form-item label="申请说明"><el-input v-model="chg.reason" type="textarea" :rows="3" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="changeVisible = false">取消</el-button>
        <el-button type="primary" @click="submitChange">提交</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import request from '@/utils/request'
import { store } from '@/store/user'
import { formatTime, statusType } from '@/utils/format'

const loading = ref(false)
const profile = ref(null)
const changes = ref([])
const applyVisible = ref(false)
const changeVisible = ref(false)
const pv = reactive({ showPhone: 1, showEmail: 1, showUnit: 1, showRegion: 1 })
const form = reactive({ realName: '', studentNo: '', college: '', major: '', graduateYear: 2018, phone: '', certMaterial: '' })
const chg = reactive({ fieldName: '工作单位', newValue: '', reason: '' })
const changeFields = ['工作单位', '所在地区', '手机', '邮箱']

const OLD = { 工作单位: 'workUnit', 所在地区: 'regionName', 手机: 'phone', 邮箱: 'email' }

async function load() {
  loading.value = true
  try {
    const d = await request.get('/api/alumni/me')
    profile.value = d || null
    if (d) {
      pv.showPhone = d.showPhone ?? 1
      pv.showEmail = d.showEmail ?? 1
      pv.showUnit = d.showUnit ?? 1
      pv.showRegion = d.showRegion ?? 1
      const c = await request.get('/api/change/page', { params: { page: 1, size: 50, kw: d.realName } })
      changes.value = (c.list || []).filter((x) => x.alumniId === d.id)
    }
  } finally { loading.value = false }
}

async function submitApply() {
  if (!form.realName || !form.studentNo) { ElMessage.warning('姓名与学号为必填'); return }
  await request.post('/api/alumni/apply', { ...form })
  ElMessage.success('认证申请已提交，等待校友办审核')
  applyVisible.value = false
  load()
}

async function submitChange() {
  if (!chg.newValue || (chg.reason || '').trim().length < 5) { ElMessage.warning('请填写变更后内容，申请说明不少于 5 个字'); return }
  await request.post('/api/change/apply', {
    alumniId: profile.value.id,
    alumniName: profile.value.realName,
    changeType: '信息变更',
    fieldName: chg.fieldName,
    oldValue: profile.value[OLD[chg.fieldName]] || '',
    newValue: chg.newValue,
    reason: chg.reason
  })
  ElMessage.success('变更申请已提交')
  changeVisible.value = false
  load()
}

async function savePrivacy() {
  await request.post(`/api/alumni/${profile.value.id}/privacy`, { ...pv })
  ElMessage.success('隐私设置已保存')
}

onMounted(() => {
  if (!store.user) { ElMessage.warning('登录已失效'); return }
  load()
})
</script>

<style scoped>
.my { max-width: 1120px; margin: 0 auto; padding: 24px 0 40px; }
.page-head { display: flex; align-items: flex-end; justify-content: space-between; margin-bottom: 18px; }
.page-head h1 { font-size: 22px; margin: 0 0 6px; color: var(--text); }
.page-head p { font-size: 13px; color: var(--text3); margin: 0; }
.empty-card { padding: 30px; }
.cols { display: grid; grid-template-columns: 1.1fr 1fr; gap: 18px; margin-bottom: 18px; }
.hero { display: flex; gap: 18px; padding: 20px; }
.avatar { width: 84px; height: 84px; border-radius: 12px; object-fit: cover; background: #EFE6E3; }
.who h3 { margin: 0 0 6px; font-size: 18px; color: var(--text); }
.who p { margin: 0 0 4px; font-size: 13px; }
.tags { display: flex; gap: 8px; margin-top: 8px; }
.info { padding: 4px 20px 18px; }
.grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: 10px 18px; }
.kv { display: flex; justify-content: space-between; font-size: 13px; border-bottom: 1px dashed var(--border); padding-bottom: 6px; }
.kv span { color: var(--text3); }
.kv b { color: var(--text); font-weight: 500; }
.privacy { padding: 4px 20px 16px; }
.sw { display: flex; justify-content: space-between; align-items: center; font-size: 13px; padding: 8px 0; color: var(--text2); }
</style>
