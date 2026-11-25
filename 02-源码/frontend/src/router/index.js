import { createRouter, createWebHistory } from 'vue-router'

/** 路由表：公开端（无需登录）与系统内页面分开 */
const routes = [
  { path: '/login', component: () => import('@/views/Login.vue'), meta: { public: true, title: '登录' } },
  { path: '/public/projects', component: () => import('@/views/PublicProjects.vue'), meta: { public: true, title: '捐赠项目公开' } },
  { path: '/public/projects/:id', component: () => import('@/views/PublicProjectDetail.vue'), meta: { public: true, title: '项目进展' } },
  {
    path: '/',
    component: () => import('@/layout/MainLayout.vue'),
    redirect: '/dashboard',
    children: [
      { path: 'dashboard', component: () => import('@/views/Dashboard.vue'), meta: { title: '校友运营看板' } },
      { path: 'alumni-list', component: () => import('@/views/AlumniList.vue'), meta: { title: '校友档案' } },
      { path: 'cert-audit', component: () => import('@/views/CertAudit.vue'), meta: { title: '认证审核' } },
      { path: 'change-audit', component: () => import('@/views/ChangeAudit.vue'), meta: { title: '变更审核' } },
      { path: 'org-list', component: () => import('@/views/OrgList.vue'), meta: { title: '组织管理' } },
      { path: 'member-audit', component: () => import('@/views/MemberAudit.vue'), meta: { title: '成员审核' } },
      { path: 'notice', component: () => import('@/views/NoticeList.vue'), meta: { title: '组织公告' } },
      { path: 'activity-manage', component: () => import('@/views/ActivityManage.vue'), meta: { title: '活动管理' } },
      { path: 'activity-audit', component: () => import('@/views/ActivityAudit.vue'), meta: { title: '活动审核' } },
      { path: 'signup-manage', component: () => import('@/views/SignupManage.vue'), meta: { title: '报名与签到' } },
      { path: 'activity-archive', component: () => import('@/views/ActivityArchive.vue'), meta: { title: '活动归档' } },
      { path: 'activity-square', component: () => import('@/views/ActivitySquare.vue'), meta: { title: '活动广场' } },
      { path: 'project-list', component: () => import('@/views/ProjectList.vue'), meta: { title: '捐赠项目' } },
      { path: 'project/:id', component: () => import('@/views/ProjectDetail.vue'), meta: { title: '项目详情' } },
      { path: 'donation-record', component: () => import('@/views/DonationRecord.vue'), meta: { title: '线下捐赠登记' } },
      { path: 'donation-verify', component: () => import('@/views/DonationVerify.vue'), meta: { title: '捐赠核对' } },
      { path: 'progress-publish', component: () => import('@/views/ProgressPublish.vue'), meta: { title: '进展公示' } },
      { path: 'certificate', component: () => import('@/views/Certificate.vue'), meta: { title: '感谢证书' } },
      { path: 'rule', component: () => import('@/views/RuleConfig.vue'), meta: { title: '捐赠公开规则' } },
      { path: 'score', component: () => import('@/views/ScoreList.vue'), meta: { title: '计算留痕' } },
      { path: 'effect', component: () => import('@/views/EffectStat.vue'), meta: { title: '效果统计' } },
      { path: 'user', component: () => import('@/views/UserList.vue'), meta: { title: '用户管理' } },
      { path: 'role', component: () => import('@/views/RoleList.vue'), meta: { title: '角色管理' } },
      { path: 'menu', component: () => import('@/views/MenuList.vue'), meta: { title: '菜单管理' } },
      { path: 'log', component: () => import('@/views/LogList.vue'), meta: { title: '操作日志' } },
      { path: 'dict', component: () => import('@/views/DictList.vue'), meta: { title: '数据字典' } },
      { path: 'profile', component: () => import('@/views/Profile.vue'), meta: { title: '个人中心' } },
      { path: 'my-profile', component: () => import('@/views/MyProfile.vue'), meta: { title: '我的档案' } },
      { path: 'my-signup', component: () => import('@/views/MySignup.vue'), meta: { title: '我的报名' } },
      { path: 'my-cert', component: () => import('@/views/MyCert.vue'), meta: { title: '我的证书' } }
    ]
  }
]

const router = createRouter({ history: createWebHistory(), routes })

router.beforeEach((to) => {
  if (to.meta && to.meta.public) return true
  const token = localStorage.getItem('alumni_token')
  if (!token) return { path: '/login', query: { redirect: to.fullPath } }
  return true
})

export default router
