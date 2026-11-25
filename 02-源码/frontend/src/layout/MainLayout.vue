<template>
  <!-- 校友走门户式布局（顶部导航 + 内容流），其余角色走后台布局（侧边栏 + 顶栏） -->
  <div v-if="isAlumni" class="portal">
    <header class="p-top">
      <div class="p-brand"><span class="logo">校</span>校友之家</div>
      <nav class="p-nav">
        <a v-for="m in alumniNav" :key="m.path" :class="{ on: route.path === m.path }" @click="go(m.path)">{{ m.name }}</a>
      </nav>
      <div class="p-right">
        <el-badge :value="unread" :hidden="unread === 0">
          <el-icon class="bell" @click="msgVisible = true"><Bell /></el-icon>
        </el-badge>
        <el-dropdown @command="onCommand">
          <span class="who">
            <img class="avatar" :src="avatarUrl" alt="" />
            <span><b>{{ store.user?.realName }}</b><i>{{ store.user?.roleName }}</i></span>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="profile">个人中心</el-dropdown-item>
              <el-dropdown-item command="logout" divided>退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </header>
    <main class="portal-page"><router-view /></main>
    <el-drawer v-model="msgVisible" title="站内消息" size="420px">
      <div v-for="m in messages" :key="m.id" class="msg" @click="readMsg(m)">
        <div class="msg-t"><b>{{ m.title }}</b><span class="muted num">{{ formatTime(m.createTime) }}</span></div>
        <div class="msg-c">{{ m.content }}</div>
      </div>
      <el-empty v-if="!messages.length" description="暂无消息" />
    </el-drawer>
  </div>

  <div v-else class="layout">
    <aside class="side" :class="{ fold }">
      <div class="brand"><span class="logo">校</span><span v-show="!fold">校友工作平台</span></div>
      <el-menu :default-active="route.path" :collapse="fold" :collapse-transition="false"
               background-color="#431B26" text-color="rgba(255,255,255,.78)"
               active-text-color="#fff" router class="menu">
        <template v-for="g in groups" :key="g.name">
          <div class="grp" v-show="!fold">{{ g.name }}</div>
          <el-menu-item v-for="m in g.items" :key="m.id" :index="m.path">
            <el-icon><component :is="iconOf(m.icon)" /></el-icon>
            <template #title>{{ m.name }}</template>
          </el-menu-item>
        </template>
      </el-menu>
    </aside>

    <div class="main">
      <header class="top">
        <el-icon class="fold-btn" @click="fold = !fold"><Fold v-if="!fold" /><Expand v-else /></el-icon>
        <el-breadcrumb separator="/">
          <el-breadcrumb-item>{{ roleName }}</el-breadcrumb-item>
          <el-breadcrumb-item>{{ route.meta.title || '工作台' }}</el-breadcrumb-item>
        </el-breadcrumb>
        <div class="right">
          <span class="muted num">{{ today }}</span>
          <el-badge :value="unread" :hidden="unread === 0">
            <el-icon class="bell" @click="msgVisible = true"><Bell /></el-icon>
          </el-badge>
          <el-dropdown @command="onCommand">
            <span class="who">
              <img class="avatar" :src="avatarUrl" alt="" />
              <span><b>{{ store.user?.realName }}</b><i>{{ store.user?.roleName }}</i></span>
              <el-icon><ArrowDown /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">个人中心</el-dropdown-item>
                <el-dropdown-item command="logout" divided>退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </header>
      <main class="content"><router-view /></main>
    </div>

    <el-drawer v-model="msgVisible" title="站内消息" size="420px">
      <div v-for="m in messages" :key="m.id" class="msg" @click="readMsg(m)">
        <div class="msg-t"><b>{{ m.title }}</b><span class="muted num">{{ formatTime(m.createTime) }}</span></div>
        <div class="msg-c">{{ m.content }}</div>
      </div>
      <el-empty v-if="!messages.length" description="暂无消息" />
    </el-drawer>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { store } from '@/store/user'
import request from '@/utils/request'
import { formatTime } from '@/utils/format'

const route = useRoute()
const router = useRouter()
const fold = ref(false)
const messages = ref([])
const unread = ref(0)
const msgVisible = ref(false)

const isAlumni = computed(() => store.user?.roleCode === 'ALUMNI')
const roleName = computed(() => store.user?.roleName || '工作台')
const today = new Date().toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' })
const avatarUrl = computed(() => store.user?.avatar || '')

/** 校友门户导航：只放本人相关入口 */
const alumniNav = [
  { path: '/activity-square', name: '活动广场' },
  { path: '/my-profile', name: '我的档案' },
  { path: '/my-signup', name: '我的报名' },
  { path: '/my-cert', name: '我的证书' },
  { path: '/project-list', name: '捐赠项目' }
]

/** 侧边栏按业务域分组，顺序固定；未列出的菜单落到「其他」 */
const SECTIONS = [
  ['工作台', ['校友运营看板']],
  ['档案管理', ['校友档案', '认证审核', '变更审核']],
  ['校友组织', ['组织管理', '成员审核', '组织公告']],
  ['活动运营', ['活动管理', '活动审核', '报名与签到', '活动归档', '活动广场']],
  ['捐赠管理', ['捐赠项目', '线下捐赠登记', '捐赠核对', '进展公示', '感谢证书', '项目公开端', '捐赠项目公开']],
  ['创新模块', ['捐赠公开规则', '计算留痕', '效果统计']],
  ['系统', ['用户管理', '角色管理', '菜单管理', '操作日志', '数据字典']]
]
const groups = computed(() => {
  // 只保留有路由的叶子菜单；目录型菜单（type=M）由分组标题承担，不单独渲染
  const menus = (store.menus || []).filter((m) => m.path && m.type !== 'M')
  const used = new Set()
  const out = []
  for (const [name, names] of SECTIONS) {
    const items = menus.filter((m) => names.includes(m.name))
    items.forEach((m) => used.add(m.id))
    if (items.length) out.push({ name, items })
  }
  const rest = menus.filter((m) => !used.has(m.id) && m.path !== '/profile')
  if (rest.length) out.push({ name: '其他', items: rest })
  return out
})

const ICONS = {
  'data-board': 'DataBoard', user: 'User', users: 'UserFilled', 'circle-check': 'CircleCheck',
  document: 'Document', 'office-building': 'OfficeBuilding', 'user-filled': 'UserFilled',
  calendar: 'Calendar', stamp: 'Stamp', checked: 'Checked', folder: 'Folder', sunny: 'Sunny',
  money: 'Money', wallet: 'Wallet', 'trend-charts': 'TrendCharts', medal: 'Medal', view: 'View',
  'set-up': 'SetUp', operation: 'Operation', 'data-line': 'DataLine', histogram: 'Histogram',
  setting: 'Setting', avatar: 'Avatar', menu: 'Menu', collection: 'Collection', bell: 'Bell',
  tickets: 'Tickets'
}
function iconOf(name) { return ICONS[name] || 'Menu' }

function go(path) { if (path) router.push(path) }

async function loadMessages() {
  try {
    const d = await request.get('/api/message/page', { params: { page: 1, size: 20 } })
    messages.value = d.list || []
    unread.value = messages.value.filter((m) => m.readFlag === 0).length
  } catch (e) { /* 消息失败不影响主流程 */ }
}
async function readMsg(m) {
  if (m.readFlag === 0) {
    await request.post('/api/message/' + m.id + '/read')
    m.readFlag = 1
    unread.value = messages.value.filter((x) => x.readFlag === 0).length
  }
  if (m.bizUrl) router.push(m.bizUrl)
}
function onCommand(c) {
  if (c === 'profile') router.push('/profile')
  else { store.logout(); router.push('/login') }
}
onMounted(loadMessages)
</script>

<style scoped>
.layout { display: flex; height: 100vh; overflow: hidden; }
.side { width: 220px; background: #431B26; display: flex; flex-direction: column; transition: width .2s; flex: none; }
.side.fold { width: 64px; }
.brand { height: 56px; display: flex; align-items: center; gap: 10px; padding: 0 18px; color: #fff;
  font-weight: 600; font-size: 15px; border-bottom: 1px solid rgba(255,255,255,.1); white-space: nowrap; }
.logo { width: 22px; height: 22px; border-radius: 5px; background: #7A3947; display: inline-flex;
  align-items: center; justify-content: center; font-size: 12px; flex: none; }
.menu { border: none; flex: 1; overflow-y: auto; }
.grp { padding: 13px 18px 5px; font-size: 11px; color: rgba(255,255,255,.45); letter-spacing: 1px; }
.main { flex: 1; display: flex; flex-direction: column; min-width: 0; }
.top { height: 56px; background: #fff; border-bottom: 1px solid var(--border); display: flex;
  align-items: center; gap: 16px; padding: 0 24px; flex: none; }
.fold-btn { cursor: pointer; font-size: 18px; color: var(--text2); }
.right { margin-left: auto; display: flex; align-items: center; gap: 18px; }
.bell { font-size: 18px; color: var(--text2); cursor: pointer; }
.who { display: flex; align-items: center; gap: 8px; cursor: pointer; font-size: 12px; color: var(--text3); }
.who b { display: block; font-size: 13px; color: var(--text); font-weight: 500; }
.who i { font-style: normal; font-size: 11px; }
.avatar { width: 32px; height: 32px; border-radius: 50%; object-fit: cover; border: 1px solid var(--border); background: #EADCDE; }
.content { flex: 1; overflow-y: auto; padding: 24px; }
.msg { padding: 12px 0; border-bottom: 1px solid var(--border); cursor: pointer; }
.msg-t { display: flex; justify-content: space-between; font-size: 14px; gap: 10px; }
.msg-c { font-size: 13px; color: var(--text2); margin-top: 4px; }

/* 校友门户 */
.portal { min-height: 100vh; background: var(--bg); }
.p-top { height: 60px; background: #fff; border-bottom: 1px solid var(--border); display: flex;
  align-items: center; gap: 28px; padding: 0 40px; position: sticky; top: 0; z-index: 10; }
.p-brand { font-size: 15px; font-weight: 600; color: var(--primary); display: flex; align-items: center; gap: 10px; }
.p-nav { display: flex; gap: 4px; }
.p-nav a { padding: 6px 14px; border-radius: 6px; font-size: 14px; color: var(--text2); cursor: pointer; }
.p-nav a:hover { background: var(--primary-light); color: var(--primary); }
.p-nav a.on { background: var(--primary-light); color: var(--primary); font-weight: 500; }
.p-right { margin-left: auto; display: flex; align-items: center; gap: 18px; }
</style>
