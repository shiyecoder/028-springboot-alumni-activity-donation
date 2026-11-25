<template>
  <div>
    <div class="page-head">
      <div>
        <h1>感谢证书</h1>
        <p>已核对捐赠可生成感谢证书，支持发放登记与重发，发送方式与时间全程留痕</p>
      </div>
    </div>
    <CrudPage ref="pageRef" :cfg="cfg">
      <template #row-actions="{ row }">
        <el-button v-if="row.sendStatus === '待发放'" link type="primary" @click="onSend(row)">发放</el-button>
        <el-button v-else link type="primary" @click="onResend(row)">重发</el-button>
      </template>
    </CrudPage>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import CrudPage from '@/components/CrudPage.vue'
import request from '@/utils/request'

const pageRef = ref()
const cfg = {
  title: '感谢证书',
  url: '/api/cert',
  kwPlaceholder: '捐赠人姓名',
  statusOptions: ['待发放', '已发放'],
  rowWidth: 150,
  readonly: true,
  noDelete: true,
  columns: [
    { prop: 'certNo', label: '证书编号', width: 160, type: 'link' },
    { prop: 'donorName', label: '捐赠人', width: 110 },
    { prop: 'projectName', label: '捐赠项目', minWidth: 200 },
    { prop: 'amount', label: '金额', width: 120, type: 'money' },
    { prop: 'issueDate', label: '开具日期', width: 110, type: 'date' },
    { prop: 'issueUser', label: '开具人', width: 100 },
    { prop: 'sendStatus', label: '发放状态', width: 100, type: 'status' },
    { prop: 'sendWay', label: '发放方式', width: 110 },
    { prop: 'sendTime', label: '发放时间', width: 160, type: 'time' }
  ],
  fields: [
    { prop: 'certNo', label: '证书编号' },
    { prop: 'donorName', label: '捐赠人' },
    { prop: 'projectName', label: '捐赠项目' },
    { prop: 'amount', label: '金额' },
    { prop: 'issueDate', label: '开具日期' },
    { prop: 'sendStatus', label: '发放状态' },
    { prop: 'sendWay', label: '发放方式' },
    { prop: 'remark', label: '备注', type: 'textarea' }
  ]
}

async function onSend(row) {
  const { value } = await ElMessageBox.prompt('选择发放方式', '证书发放', {
    inputValue: '电子邮件', inputPlaceholder: '电子邮件 / 邮寄 / 现场领取'
  })
  await request.post(`/api/cert/${row.id}/send`, { sendWay: (value || '电子邮件').trim() })
  ElMessage.success('已登记发放')
  pageRef.value.reload()
}
async function onResend(row) {
  await ElMessageBox.confirm(`确认重新发放「${row.donorName}」的感谢证书？`, '重发确认', { type: 'warning' })
  await request.post(`/api/cert/${row.id}/resend`)
  ElMessage.success('已重发')
  pageRef.value.reload()
}
</script>
