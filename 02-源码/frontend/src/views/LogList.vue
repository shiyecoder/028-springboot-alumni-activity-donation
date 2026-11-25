<template>
  <div>
    <div class="page-head">
      <div>
        <h1>操作日志</h1>
        <p>关键业务操作留痕：认证审核、捐赠核对、状态流转、评分计算等，可按模块检索</p>
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
  title: '操作日志',
  url: '/api/sys-log',
  kwPlaceholder: '模块名称',
  readonly: true,
  noDelete: true,
  rowWidth: 110,
  columns: [
    { prop: 'userName', label: '操作人', width: 110 },
    { prop: 'module', label: '模块', width: 130, type: 'link' },
    { prop: 'action', label: '操作', width: 130 },
    { prop: 'method', label: '请求方法', width: 110 },
    { prop: 'params', label: '请求参数', minWidth: 300 },
    { prop: 'ip', label: 'IP', width: 130 },
    { prop: 'costMs', label: '耗时(ms)', width: 100, type: 'num' },
    { prop: 'createTime', label: '操作时间', width: 160, type: 'time' }
  ],
  fields: [
    { prop: 'userName', label: '操作人' },
    { prop: 'module', label: '模块' },
    { prop: 'action', label: '操作' },
    { prop: 'method', label: '请求方法' },
    { prop: 'params', label: '请求参数', type: 'textarea' },
    { prop: 'ip', label: 'IP' },
    { prop: 'costMs', label: '耗时(ms)' },
    { prop: 'createTime', label: '操作时间', type: 'datetime' }
  ]
}
</script>
