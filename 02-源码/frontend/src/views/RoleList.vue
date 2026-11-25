<template>
  <div v-loading="loading">
    <div class="page-head">
      <div>
        <h1>角色管理</h1>
        <p>角色决定可见菜单与数据范围；菜单权限按树勾选，保存后该角色下次登录即按新菜单加载</p>
      </div>
    </div>

    <div class="card">
      <el-table :data="roles" border>
        <el-table-column prop="roleCode" label="角色编码" width="140" />
        <el-table-column prop="roleName" label="角色名称" width="160" />
        <el-table-column prop="dataScope" label="数据范围" min-width="200" />
        <el-table-column prop="remark" label="说明" min-width="240" />
        <el-table-column prop="status" label="状态" width="90">
          <template #default="{ row }">
            <el-tag size="small" :type="row.status === '启用' ? 'success' : 'info'">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="160" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="openPerm(row)">分配菜单</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <el-dialog v-model="visible" :title="`分配菜单 · ${cur?.roleName || ''}`" width="520px">
      <div class="tip">
        <el-checkbox v-model="expandAll" @change="toggleExpand">展开/收起全部</el-checkbox>
        <span class="muted">已选 {{ checked.length }} 个菜单</span>
      </div>
      <el-tree ref="treeRef" :data="tree" show-checkbox node-key="id" :props="{ label: 'menuName', children: 'children' }"
               :default-expand-all="expandAll" @check="onCheck" style="max-height:420px;overflow:auto" />
      <template #footer>
        <el-button @click="visible = false">取消</el-button>
        <el-button type="primary" @click="save">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import request from '@/utils/request'

const loading = ref(false)
const roles = ref([])
const tree = ref([])
const visible = ref(false)
const expandAll = ref(true)
const treeRef = ref(null)
const cur = ref(null)
const checked = ref([])

async function load() {
  loading.value = true
  try {
    const [r, t] = await Promise.all([request.get('/api/role/list'), request.get('/api/menu/tree')])
    roles.value = r || []
    tree.value = t || []
  } finally { loading.value = false }
}

async function openPerm(row) {
  cur.value = row
  const ids = await request.get(`/api/role/${row.id}/menus`)
  checked.value = ids || []
  visible.value = true
  await nextTick()
  // 只回填叶子节点，父节点由 el-tree 半选自动推导
  const leaf = []
  const walk = (nodes) => nodes.forEach((n) => {
    if (!n.children || !n.children.length) { if (checked.value.includes(n.id)) leaf.push(n.id) }
    else walk(n.children)
  })
  walk(tree.value)
  treeRef.value.setCheckedKeys(leaf)
}

function onCheck() {
  const t = treeRef.value
  checked.value = [...t.getCheckedKeys(), ...t.getHalfCheckedKeys()]
}
function toggleExpand(v) {
  const nodes = treeRef.value.store._getAllNodes()
  nodes.forEach((n) => { n.expanded = v })
}

async function save() {
  const ids = [...treeRef.value.getCheckedKeys(), ...treeRef.value.getHalfCheckedKeys()]
  if (cur.value.roleCode === 'ADMIN' && !ids.length) { ElMessage.warning('管理员角色至少保留一个菜单'); return }
  await request.put(`/api/role/${cur.value.id}/menus`, ids)
  ElMessage.success('菜单权限已更新')
  visible.value = false
}

onMounted(load)
</script>

<style scoped>
.page-head { margin-bottom: 18px; }
.page-head h1 { font-size: 22px; margin: 0 0 6px; color: var(--text); }
.page-head p { font-size: 13px; color: var(--text3); margin: 0; }
.tip { display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px; }
</style>
