<template>
  <div>
    <div class="page-head">
      <div>
        <h1>成员审核</h1>
        <p>校友申请加入地方校友会/俱乐部，通过后组织成员数自动累加</p>
      </div>
    </div>
    <CrudPage ref="pageRef" :cfg="cfg">
      <template #row-actions="{ row }">
        <template v-if="row.joinStatus === '待审核'">
          <el-button link type="success" @click="onPass(row)">通过</el-button>
          <el-button link type="danger" @click="onReject(row)">拒绝</el-button>
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
  title: '入会申请',
  url: '/api/member',
  kwPlaceholder: '校友姓名',
  statusOptions: ['待审核', '已通过', '已退出'],
  rowWidth: 180,
  readonly: true,
  noDelete: true,
  columns: [
    { prop: 'alumniName', label: '校友', width: 100, type: 'link' },
    { prop: 'orgId', label: '组织ID', width: 90, type: 'num' },
    { prop: 'memberRole', label: '申请角色', width: 110 },
    { prop: 'applyReason', label: '申请理由', minWidth: 240 },
    { prop: 'joinStatus', label: '审核状态', width: 100, type: 'status' },
    { prop: 'auditUser', label: '审核人', width: 110 },
    { prop: 'auditTime', label: '审核时间', width: 160, type: 'time' },
    { prop: 'createTime', label: '申请时间', width: 160, type: 'time' }
  ],
  fields: [
    { prop: 'alumniName', label: '校友' },
    { prop: 'orgId', label: '组织ID' },
    { prop: 'memberRole', label: '申请角色' },
    { prop: 'applyReason', label: '申请理由', type: 'textarea' },
    { prop: 'joinStatus', label: '审核状态' },
    { prop: 'createTime', label: '申请时间', type: 'datetime' }
  ]
}

const onPass = (row) => audit({ url: `/api/member/${row.id}/audit`, status: '已通过', name: row.alumniName, label: '入会通过' })
  .then(() => pageRef.value.reload()).catch(() => {})
const onReject = (row) => audit({ url: `/api/member/${row.id}/audit`, status: '已退出', name: row.alumniName, label: '拒绝入会' })
  .then(() => pageRef.value.reload()).catch(() => {})
</script>
