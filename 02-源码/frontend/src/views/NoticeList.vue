<template>
  <div>
    <div class="page-head">
      <div>
        <h1>组织公告</h1>
        <p>各校友组织发布的通知公告，置顶公告排在列表最前</p>
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
  title: '公告',
  url: '/api/notice',
  kwPlaceholder: '公告标题',
  rowWidth: 150,
  columns: [
    { prop: 'title', label: '公告标题', minWidth: 240, type: 'link' },
    { prop: 'orgName', label: '发布组织', minWidth: 160 },
    { prop: 'content', label: '公告内容', minWidth: 280 },
    { prop: 'publisher', label: '发布人', width: 110 },
    { prop: 'topFlag', label: '置顶', width: 80, type: 'num' },
    { prop: 'publishTime', label: '发布时间', width: 160, type: 'time' }
  ],
  fields: [
    { prop: 'orgId', label: '组织ID', type: 'number' },
    { prop: 'orgName', label: '组织名称' },
    { prop: 'title', label: '公告标题', required: true },
    { prop: 'content', label: '公告内容', type: 'textarea', required: true },
    { prop: 'publisher', label: '发布人' },
    { prop: 'publishTime', label: '发布时间', type: 'datetime' },
    { prop: 'topFlag', label: '是否置顶', type: 'switch', default: 0 }
  ]
}
</script>
