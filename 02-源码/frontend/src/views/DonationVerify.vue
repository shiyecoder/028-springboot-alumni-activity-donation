<template>
  <div>
    <div class="page-head">
      <div>
        <h1>捐赠核对</h1>
        <p>财务核对到账凭证后确认，系统按已核对明细重算项目实收与资金完成度；无凭证不可通过</p>
      </div>
      <el-radio-group v-model="tab" @change="switchTab">
        <el-radio-button label="待核对" />
        <el-radio-button label="已核对" />
        <el-radio-button label="已退回" />
      </el-radio-group>
    </div>
    <CrudPage ref="pageRef" :cfg="cfg">
      <template #row-actions="{ row }">
        <template v-if="row.verifyStatus === '待核对'">
          <el-button link type="success" @click="onPass(row)">核对通过</el-button>
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
const tab = ref('待核对')
const cfg = {
  title: '捐赠核对',
  url: '/api/donation',
  kwPlaceholder: '捐赠人姓名',
  rowWidth: 190,
  readonly: true,
  noDelete: true,
  params: { status: '待核对' },
  columns: [
    { prop: 'recordNo', label: '登记编号', width: 150 },
    { prop: 'donorName', label: '捐赠人', width: 110, type: 'link' },
    { prop: 'projectName', label: '捐赠项目', minWidth: 200 },
    { prop: 'amount', label: '金额', width: 120, type: 'money' },
    { prop: 'donateDate', label: '捐赠日期', width: 110, type: 'date' },
    { prop: 'voucherPath', label: '凭证', width: 84, type: 'image' },
    { prop: 'verifyStatus', label: '核对状态', width: 100, type: 'status' },
    { prop: 'verifyUser', label: '核对人', width: 100 },
    { prop: 'verifyTime', label: '核对时间', width: 160, type: 'time' },
    { prop: 'verifyRemark', label: '核对意见', minWidth: 160 }
  ],
  fields: [
    { prop: 'recordNo', label: '登记编号' },
    { prop: 'donorName', label: '捐赠人' },
    { prop: 'projectName', label: '捐赠项目' },
    { prop: 'amount', label: '金额' },
    { prop: 'donateDate', label: '捐赠日期' },
    { prop: 'voucherPath', label: '凭证', type: 'image' },
    { prop: 'intention', label: '捐赠意向', type: 'textarea' },
    { prop: 'verifyStatus', label: '核对状态' },
    { prop: 'verifyRemark', label: '核对意见', type: 'textarea' }
  ]
}

function switchTab(v) {
  cfg.params.status = v
  if (pageRef.value) pageRef.value.reload()
}
const onPass = (row) => audit({ url: `/api/donation/${row.id}/verify`, status: '已核对', name: row.donorName, label: '核对通过', body: { remark: '凭证与到账记录一致' } })
  .then(() => pageRef.value.reload()).catch(() => {})
const onReject = (row) => audit({ url: `/api/donation/${row.id}/verify`, status: '已退回', name: row.donorName, label: '退回', reason: true })
  .then(() => pageRef.value.reload()).catch(() => {})
</script>
