<template>
  <div>
    <div class="page-head">
      <div>
        <h1>变更审核</h1>
        <p>校友申请修改工作单位、地区、联系方式等字段，通过后自动写回档案，退回需说明原因</p>
      </div>
    </div>
    <CrudPage ref="pageRef" :cfg="cfg">
      <template #row-actions="{ row }">
        <template v-if="row.auditStatus === '待审核'">
          <el-button link type="success" @click="onPass(row)">通过</el-button>
          <el-button link type="danger" @click="onReject(row)">退回</el-button>
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
  title: '变更申请',
  url: '/api/change',
  kwPlaceholder: '校友姓名',
  statusOptions: ['待审核', '已通过', '已退回'],
  rowWidth: 200,
  readonly: true,
  noDelete: true,
  columns: [
    { prop: 'alumniName', label: '校友', width: 90, type: 'link' },
    { prop: 'changeType', label: '变更类型', width: 110 },
    { prop: 'fieldName', label: '变更字段', width: 110 },
    { prop: 'oldValue', label: '变更前', minWidth: 180 },
    { prop: 'newValue', label: '变更后', minWidth: 180 },
    { prop: 'reason', label: '申请说明', minWidth: 200 },
    { prop: 'auditStatus', label: '审核状态', width: 100, type: 'status' },
    { prop: 'auditRemark', label: '审核意见', minWidth: 160 },
    { prop: 'auditTime', label: '审核时间', width: 160, type: 'time' }
  ],
  fields: [
    { prop: 'alumniName', label: '校友' },
    { prop: 'changeType', label: '变更类型' },
    { prop: 'fieldName', label: '变更字段' },
    { prop: 'oldValue', label: '变更前' },
    { prop: 'newValue', label: '变更后' },
    { prop: 'reason', label: '申请说明', type: 'textarea' },
    { prop: 'auditStatus', label: '审核状态' },
    { prop: 'auditRemark', label: '审核意见', type: 'textarea' },
    { prop: 'createTime', label: '申请时间', type: 'datetime' }
  ]
}

const onPass = (row) => audit({ url: `/api/change/${row.id}/audit`, status: '已通过', name: row.alumniName, label: '审核通过', body: { remark: '信息核实无误，予以变更' } })
  .then(() => pageRef.value.reload()).catch(() => {})
const onReject = (row) => audit({ url: `/api/change/${row.id}/audit`, status: '已退回', name: row.alumniName, label: '退回', reason: true })
  .then(() => pageRef.value.reload()).catch(() => {})
</script>
