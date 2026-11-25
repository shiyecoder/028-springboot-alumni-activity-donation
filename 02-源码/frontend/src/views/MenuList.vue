<template>
  <div>
    <div class="page-head">
      <div>
        <h1>菜单管理</h1>
        <p>系统菜单与权限标识，角色菜单分配时按此树勾选；修改后需重新登录生效</p>
      </div>
    </div>
    <CrudPage ref="pageRef" :cfg="cfg" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import CrudPage from '@/components/CrudPage.vue'

const pageRef = ref()
const cfg = {
  title: '菜单',
  url: '/api/menu',
  kwPlaceholder: '菜单名称',
  rowWidth: 150,
  columns: [
    { prop: 'menuName', label: '菜单名称', minWidth: 180, type: 'link' },
    { prop: 'parentId', label: '上级ID', width: 90, type: 'num' },
    { prop: 'menuType', label: '类型', width: 100 },
    { prop: 'path', label: '路由地址', minWidth: 180 },
    { prop: 'perm', label: '权限标识', minWidth: 180 },
    { prop: 'icon', label: '图标', width: 130 },
    { prop: 'sortNo', label: '排序', width: 80, type: 'num' },
    { prop: 'visible', label: '可见', width: 80, type: 'num' },
    { prop: 'createTime', label: '创建时间', width: 160, type: 'time' }
  ],
  fields: [
    { prop: 'menuName', label: '菜单名称', required: true },
    { prop: 'parentId', label: '上级菜单ID', type: 'number', default: 0, hint: '0 表示一级菜单' },
    { prop: 'menuType', label: '类型', type: 'select', options: ['目录', '菜单', '按钮'], default: '菜单' },
    { prop: 'path', label: '路由地址' },
    { prop: 'perm', label: '权限标识' },
    { prop: 'icon', label: '图标名' },
    { prop: 'sortNo', label: '排序', type: 'number', default: 10 },
    { prop: 'visible', label: '是否可见', type: 'switch', default: 1 }
  ]
}
</script>
