<template>
  <div class="login-wrap">
    <!-- 左侧品牌区：使用按主题生成的本地背景图，断网也能显示 -->
    <div class="login-bg">
      <div class="brand-top"><span class="seal">校友</span></div>
      <div class="brand-copy">
        <h1>校友活动与捐赠<br />项目管理平台</h1>
        <p>连接校友、组织活动、公开捐赠进展。所有线下捐赠经财务核对后计入项目实收，匿名捐赠在公开端自动隐藏姓名。</p>
        <div class="stats">
          <div><b class="num">1,284</b><span>已认证校友</span></div>
          <div><b class="num">32</b><span>捐赠项目</span></div>
          <div><b class="num">¥ 784.8 万</b><span>累计登记</span></div>
        </div>
      </div>
      <div class="brand-foot">高校校友工作办公室 · 仅限授权人员使用</div>
    </div>

    <div class="login-form">
      <div class="login-box">
        <h2>登录</h2>
        <div class="sub">请使用校友办分配的账号登录，校友账号可用学号申请认证后使用</div>
        <el-form @submit.prevent="doLogin">
          <el-form-item>
            <el-input v-model="username" size="large" placeholder="账号 / 学号" :prefix-icon="User" />
          </el-form-item>
          <el-form-item>
            <el-input v-model="password" size="large" type="password" show-password placeholder="密码"
                      :prefix-icon="Lock" @keyup.enter="doLogin" />
          </el-form-item>
          <div class="row">
            <el-checkbox v-model="remember">记住账号</el-checkbox>
            <a class="link">忘记密码？</a>
          </div>
          <el-button type="primary" size="large" class="btn" :loading="loading" @click="doLogin">登 录</el-button>
        </el-form>
        <div class="tips">
          <div>演示账号（点击填入）：</div>
          <div class="chips">
            <span v-for="a in accounts" :key="a.u" class="chip" @click="fill(a)">{{ a.label }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'
import request from '@/utils/request'
import { store } from '@/store/user'

const router = useRouter()
const route = useRoute()
const username = ref('')
const password = ref('')
const remember = ref(true)
const loading = ref(false)
const accounts = [
  { label: '校友办管理员', u: 'admin', p: 'admin123' },
  { label: '校友联络员', u: 'liaison01', p: '123456' },
  { label: '财务登记员', u: 'finance01', p: '123456' },
  { label: '校友', u: 'alumni01', p: '123456' }
]

function fill(a) {
  username.value = a.u
  password.value = a.p
}

async function doLogin() {
  if (!username.value || !password.value) {
    ElMessage.warning('请输入账号和密码')
    return
  }
  loading.value = true
  try {
    const d = await request.post('/api/auth/login', { username: username.value, password: password.value })
    localStorage.setItem('alumni_token', d.token)
    store.setLogin(d.user, d.menus)
    ElMessage.success('登录成功')
    const target = route.query.redirect || (d.user.roleCode === 'ALUMNI' ? '/activity-square' : '/dashboard')
    router.push(target)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  const saved = localStorage.getItem('alumni_last_user')
  if (saved) username.value = saved
})
</script>

<style scoped>
.login-wrap { min-height: 100vh; display: grid; grid-template-columns: 1.05fr .95fr; }
.login-bg {
  position: relative; padding: 56px; color: #fff; display: flex; flex-direction: column; justify-content: space-between;
  background: linear-gradient(150deg, rgba(58,22,32,.82), rgba(91,37,51,.72) 55%, rgba(122,57,71,.68)),
              url('/login-bg.jpg') center/cover no-repeat;
  background-color: #431B26;
}
.seal { width: 64px; height: 64px; border: 2px solid rgba(255,255,255,.45); border-radius: 10px;
  display: inline-flex; align-items: center; justify-content: center; font-size: 20px; letter-spacing: 3px; }
.brand-copy h1 { font-size: 32px; line-height: 46px; font-weight: 600; letter-spacing: 1px; margin: 0; }
.brand-copy p { color: rgba(255,255,255,.76); margin-top: 14px; font-size: 14px; max-width: 440px; line-height: 24px; }
.stats { display: flex; gap: 40px; margin-top: 34px; }
.stats b { display: block; font-size: 24px; font-weight: 600; }
.stats span { font-size: 12px; color: rgba(255,255,255,.62); }
.brand-foot { font-size: 12px; color: rgba(255,255,255,.55); }
.login-form { display: flex; align-items: center; justify-content: center; background: #fff; }
.login-box { width: 380px; }
.login-box h2 { font-size: 24px; margin: 0; font-weight: 600; }
.login-box .sub { font-size: 13px; color: var(--text3); margin: 8px 0 26px; line-height: 20px; }
.row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px; font-size: 12px; }
.link { color: var(--accent); cursor: pointer; }
.btn { width: 100%; height: 44px; font-size: 15px; letter-spacing: 4px; }
.tips { margin-top: 22px; font-size: 12px; color: var(--text3); line-height: 22px; }
.chips { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 6px; }
.chip { padding: 3px 10px; border: 1px solid var(--border); border-radius: 14px; cursor: pointer; color: var(--text2); }
.chip:hover { border-color: var(--primary); color: var(--primary); }
</style>
