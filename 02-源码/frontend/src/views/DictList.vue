<template>
  <div>
    <div class="page-head">
      <div>
        <h1>数据字典</h1>
        <p>活动类型、捐赠类型、组织类型等枚举项统一维护，页面下拉项与报表分组保持一致口径</p>
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
  title: '字典项',
  url: '/api/sys-dict',
  kwPlaceholder: '字典标签',
  statusOptions: ['启用', '停用'],
  rowWidth: 150,
  columns: [
    { prop: 'dictType', label: '字典类型', width: 160, type: 'link' },
    { prop: 'dictCode', label: '字典编码', width: 160 },
    { prop: 'dictLabel', label: '字典标签', minWidth: 180 },
    { prop: 'sortNo', label: '排序', width: 80, type: 'num' },
    { prop: 'status', label: '状态', width: 90, type: 'status' },
    { prop: 'createTime', label: '创建时间', width: 160, type: 'time' }
  ],
  fields: [
    { prop: 'dictType', label: '字典类型', required: true },
    { prop: 'dictCode', label: '字典编码', required: true },
    { prop: 'dictLabel', label: '字典标签', required: true },
    { prop: 'sortNo', label: '排序', type: 'number', default: 10 },
    { prop: 'status', label: '状态', type: 'select', options: ['启用', '停用'], default: '启用' }
  ]
}
</script>
