<template>
  <div v-loading="loading" class="profile">
    <div class="page-head">
      <div>
        <h1>个人中心</h1>
        <p>维护本人账号信息与头像，头像保存后右上角立即同步</p>
      </div>
    </div>

    <div class="cols">
      <div class="card left">
        <div class="avatar-box">
          <el-upload ref="upRef" class="up" :show-file-list="false" :http-request="uploadAvatar" accept="image/*">
            <img v-if="form.avatar" :src="form.avatar" class="avatar" alt="头像" />
            <div v-else class="avatar ph">{{ (form.realName || '?').slice(0, 1) }}</div>
          </el-upload>
          <div class="up-link" @click="pickAvatar">更换头像</div>
          <h3>{{ form.realName }}</h3>
          <p class="muted">{{ me.roleName }} · {{ me.username }}</p>
          <el-tag size="small" effect="plain">{{ me.roleName || '系统用户' }}</el-tag>
        </div>
        <el-divider />
        <div class="mini"><span>校友编号</span><b>{{ me.alumniNo || '未生成' }}</b></div>
        <div class="mini"><span>所属组织</span><b>{{ me.orgId || '—' }}</b></div>
        <div class="mini"><span>可访问菜单</span><b>{{ (me.menus || []).length }} 项</b></div>
      </div>

      <div class="card right">
        <div class="card-h"><h2>基本信息</h2></div>
        <div class="card-b">
          <el-form :model="form" label-width="100px" style="max-width:520px">
            <el-form-item label="姓名"><el-input v-model="form.realName" /></el-form-item>
            <el-form-item label="手机"><el-input v-model="form.phone" /></el-form-item>
            <el-form-item label="邮箱"><el-input v-model="form.email" /></el-form-item>
            <el-form-item>
              <el-button type="primary" :loading="saving" @click="save">保存资料</el-button>
            </el-form-item>
          </el-form>
        </div>
        <el-divider />
        <div class="card-h"><h2>修改密码</h2><span class="muted">修改成功后需重新登录</span></div>
        <div class="card-b">
          <el-form :model="pwd" label-width="100px" style="max-width:520px">
            <el-form-item label="原密码"><el-input v-model="pwd.oldPassword" type="password" show-password /></el-form-item>
            <el-form-item label="新密码"><el-input v-model="pwd.newPassword" type="password" show-password placeholder="至少 6 位" /></el-form-item>
            <el-form-item label="确认新密码"><el-input v-model="pwd.confirm" type="password" show-password /></el-form-item>
            <el-form-item>
              <el-button type="primary" plain :loading="changing" @click="changePwd">修改密码</el-button>
            </el-form-item>
          </el-form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import request from '@/utils/request'
import { store } from '@/store/user'

const router = useRouter()
const loading = ref(false)
const saving = ref(false)
const changing = ref(false)
const upRef = ref()
const me = ref({})
const form = reactive({ realName: '', phone: '', email: '', avatar: '' })
const pwd = reactive({ oldPassword: '', newPassword: '', confirm: '' })

async function load() {
  loading.value = true
  try {
    const d = await request.get('/api/auth/me')
    me.value = d || {}
    form.realName = d.realName || ''
    form.phone = d.phone || ''
    form.email = d.email || ''
    form.avatar = d.avatar || ''
  } finally { loading.value = false }
}

/** 点击「更换头像」直接触发上传组件内部的文件选择 */
function pickAvatar() {
  const input = upRef.value && upRef.value.$el.querySelector('input[type=file]')
  if (input) input.click()
}

async function uploadAvatar(opt) {  const fd = new FormData()
  fd.append('file', opt.file)
  const d = await request.post('/api/file/upload', fd, { headers: { 'Content-Type': 'multipart/form-data' } })
  form.avatar = d.path
  await save(true)
}

async function save(silent = false) {
  saving.value = true
  try {
    const d = await request.post('/api/user/profile', { ...form })
    // 同步全局登录态，顶栏头像与姓名即时刷新
    store.setUser({ ...store.user, ...d })
    if (!silent) ElMessage.success('资料已保存')
  } finally { saving.value = false }
}

async function changePwd() {
  if (pwd.newPassword !== pwd.confirm) { ElMessage.warning('两次输入的新密码不一致'); return }
  changing.value = true
  try {
    await request.post('/api/user/change-password', { oldPassword: pwd.oldPassword, newPassword: pwd.newPassword })
    ElMessage.success('密码已修改，请重新登录')
    store.logout()
    router.push('/login')
  } finally { changing.value = false }
}

onMounted(load)
</script>

<style scoped>
.page-head { margin-bottom: 18px; }
.page-head h1 { font-size: 22px; margin: 0 0 6px; color: var(--text); }
.page-head p { font-size: 13px; color: var(--text3); margin: 0; }
.cols { display: grid; grid-template-columns: 320px 1fr; gap: 18px; }
.left { padding: 24px 20px; }
.avatar-box { text-align: center; }
.up { position: relative; display: inline-block; cursor: pointer; }
.avatar { width: 92px; height: 92px; border-radius: 50%; object-fit: cover; display: block; }
.avatar.ph { display: flex; align-items: center; justify-content: center; background: #EADCDE; color: #5B2533; font-size: 32px; margin: 0 auto; }
.up-link { margin-top: 8px; font-size: 12px; color: var(--primary); cursor: pointer; }
.up-link:hover { text-decoration: underline; }
.avatar-box h3 { margin: 12px 0 4px; font-size: 16px; color: var(--text); }
.avatar-box p { font-size: 12px; margin: 0 0 10px; }
.mini { display: flex; justify-content: space-between; font-size: 13px; padding: 7px 0; color: var(--text3); }
.mini b { color: var(--text); font-weight: 500; }
.right { padding: 4px 20px 20px; }
</style>
