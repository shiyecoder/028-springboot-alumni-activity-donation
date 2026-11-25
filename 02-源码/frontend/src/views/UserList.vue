<template>
  <div>
    <div class="page-head">
      <div>
        <h1>用户管理</h1>
        <p>系统账号与角色绑定，列表不返回密码字段；重置密码由后端统一加盐加密</p>
      </div>
      <el-button plain @click="$router.push('/role')">角色权限</el-button>
    </div>
    <CrudPage ref="pageRef" :cfg="cfg">
      <template #row-actions="{ row }">
        <el-button link type="warning" @click="resetPwd(row)">重置密码</el-button>
      </template>
    </CrudPage>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import CrudPage from '@/components/CrudPage.vue'
import request from '@/utils/request'

const pageRef = ref()
const roles = ref([])
const cfg = {
  title: '用户',
  url: '/api/user',
  kwPlaceholder: '姓名',
  statusOptions: ['正常', '停用'],
  rowWidth: 190,
  columns: [
    { prop: 'username', label: '账号', width: 130, type: 'link' },
    { prop: 'realName', label: '姓名', width: 100 },
    { prop: 'phone', label: '手机', width: 130 },
    { prop: 'email', label: '邮箱', minWidth: 180 },
    { prop: 'roleId', label: '角色', width: 120 },
    { prop: 'orgId', label: '所属组织', width: 100, type: 'num' },
    { prop: 'status', label: '状态', width: 90, type: 'status' },
    { prop: 'lastLoginTime', label: '最近登录', width: 160, type: 'time' },
    { prop: 'createTime', label: '创建时间', width: 160, type: 'time' }
  ],
  fields: [
    { prop: 'username', label: '账号', required: true },
    { prop: 'realName', label: '姓名', required: true },
    { prop: 'phone', label: '手机' },
    { prop: 'email', label: '邮箱' },
    { prop: 'roleId', label: '角色ID', type: 'number', hint: '1 管理员 / 2 联络员 / 3 财务 / 4 校友' },
    { prop: 'orgId', label: '所属组织ID', type: 'number' },
    { prop: 'avatar', label: '头像', type: 'image' },
    { prop: 'status', label: '状态', type: 'select', options: ['正常', '停用'], default: '正常' }
  ]
}

async function resetPwd(row) {
  const { value } = await ElMessageBox.prompt(`为「${row.realName}」设置新密码（至少 6 位）`, '重置密码', {
    inputValue: '123456',
    inputValidator: (v) => ((v || '').length >= 6 ? true : '密码至少 6 位')
  })
  await request.post(`/api/user/${row.id}/reset-password`, { password: value })
  ElMessage.success('密码已重置')
}

async function loadRoles() {
  const d = await request.get('/api/role/list')
  roles.value = d || []
}
onMounted(loadRoles)
</script>
