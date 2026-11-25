<template>
  <div>
    <div class="page-head">
      <div>
        <h1>活动归档</h1>
        <p>活动结束后登记实际到场、经费与图文总结，归档记录作为校友活动年度考核依据</p>
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
  title: '归档记录',
  url: '/api/archive',
  kwPlaceholder: '活动标题',
  rowWidth: 150,
  columns: [
    { prop: 'photoPath', label: '现场照片', width: 96, type: 'image' },
    { prop: 'activityTitle', label: '活动标题', minWidth: 220, type: 'link' },
    { prop: 'planCount', label: '计划人数', width: 96, type: 'num' },
    { prop: 'actualCount', label: '实际到场', width: 96, type: 'num' },
    { prop: 'costTotal', label: '经费合计', width: 120, type: 'money' },
    { prop: 'newsTitle', label: '新闻标题', minWidth: 200 },
    { prop: 'summary', label: '活动总结', minWidth: 240 },
    { prop: 'archiveUser', label: '归档人', width: 100 },
    { prop: 'archiveTime', label: '归档时间', width: 160, type: 'time' }
  ],
  fields: [
    { prop: 'activityId', label: '活动ID', type: 'number', required: true },
    { prop: 'activityTitle', label: '活动标题' },
    { prop: 'planCount', label: '计划人数', type: 'number' },
    { prop: 'actualCount', label: '实际到场', type: 'number' },
    { prop: 'costTotal', label: '经费合计', type: 'number', precision: 2 },
    { prop: 'costSummary', label: '经费说明', type: 'textarea' },
    { prop: 'newsTitle', label: '新闻标题' },
    { prop: 'newsContent', label: '新闻正文', type: 'textarea' },
    { prop: 'feedbackSummary', label: '反馈摘要', type: 'textarea' },
    { prop: 'summary', label: '活动总结', type: 'textarea' },
    { prop: 'photoPath', label: '现场照片', type: 'image' }
  ]
}
</script>
