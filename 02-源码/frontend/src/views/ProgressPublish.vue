<template>
  <div>
    <div class="page-head">
      <div>
        <h1>进展公示</h1>
        <p>项目阶段进展与资金使用说明提交后需审核，通过即在公开端展示，是创新模块「执行里程碑公开」的数据来源</p>
      </div>
      <el-button plain @click="openPublic">查看公开端</el-button>
    </div>
    <CrudPage ref="pageRef" :cfg="cfg">
      <template #row-actions="{ row }">
        <template v-if="row.auditStatus === '待审核'">
          <el-button link type="success" @click="onPass(row)">发布</el-button>
          <el-button link type="danger" @click="onReject(row)">驳回</el-button>
        </template>
      </template>
    </CrudPage>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import CrudPage from '@/components/CrudPage.vue'
import { audit } from '@/utils/audit'

const pageRef = ref()
const cfg = {
  title: '进展公示',
  url: '/api/progress',
  kwPlaceholder: '阶段名称',
  statusOptions: ['待审核', '已发布', '已驳回'],
  rowWidth: 180,
  columns: [
    { prop: 'photoPath', label: '现场图', width: 84, type: 'image' },
    { prop: 'stageName', label: '阶段名称', minWidth: 160, type: 'link' },
    { prop: 'projectName', label: '所属项目', minWidth: 200 },
    { prop: 'progressRate', label: '项目进度', width: 120, type: 'progress' },
    { prop: 'content', label: '进展说明', minWidth: 240 },
    { prop: 'fundSummary', label: '资金使用', minWidth: 180 },
    { prop: 'auditStatus', label: '审核状态', width: 100, type: 'status' },
    { prop: 'publishUser', label: '提交人', width: 100 },
    { prop: 'publishTime', label: '提交时间', width: 160, type: 'time' }
  ],
  fields: [
    { prop: 'projectId', label: '所属项目', type: 'project', required: true },
    { prop: 'stageName', label: '阶段名称', required: true },
    { prop: 'progressRate', label: '项目进度(%)', type: 'number' },
    { prop: 'content', label: '进展说明', type: 'textarea', required: true },
    { prop: 'fundSummary', label: '资金使用说明', type: 'textarea' },
    { prop: 'photoPath', label: '现场照片', type: 'image' }
  ]
}

const onPass = (row) => audit({ url: `/api/progress/${row.id}/audit`, status: '已发布', name: row.stageName, label: '审核发布' })
  .then(() => pageRef.value.reload()).catch(() => {})
const onReject = (row) => audit({ url: `/api/progress/${row.id}/audit`, status: '已驳回', name: row.stageName, label: '驳回' })
  .then(() => pageRef.value.reload()).catch(() => {})
/** 公开端为独立页面，新窗口打开便于对照 */
function openPublic() {
  window.open('/public/projects', '_blank')
}
</script>
