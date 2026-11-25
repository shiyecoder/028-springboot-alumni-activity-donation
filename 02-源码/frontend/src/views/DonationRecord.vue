<template>
  <div>
    <div class="page-head">
      <div>
        <h1>线下捐赠登记</h1>
        <p>登记现金/实物/企业捐赠，必须上传凭证；登记后进入「捐赠核对」，未核对不计入项目实收</p>
      </div>
      <el-button plain @click="$router.push('/donation-verify')">去捐赠核对</el-button>
    </div>
    <CrudPage ref="pageRef" :cfg="cfg">
      <template #row-actions="{ row }">
        <el-button v-if="row.verifyStatus === '已核对' && row.certFlag === 1" link type="primary"
                   @click="issueCert(row)">生成证书</el-button>
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
  title: '捐赠登记',
  url: '/api/donation',
  kwPlaceholder: '捐赠人姓名',
  statusOptions: ['待核对', '已核对', '已退回'],
  rowWidth: 180,
  columns: [
    { prop: 'recordNo', label: '登记编号', width: 150 },
    { prop: 'donorName', label: '捐赠人', width: 110, type: 'link' },
    { prop: 'donorType', label: '捐赠类型', width: 100 },
    { prop: 'projectName', label: '捐赠项目', minWidth: 200 },
    { prop: 'amount', label: '金额', width: 120, type: 'money' },
    { prop: 'goodsDesc', label: '实物说明', minWidth: 150 },
    { prop: 'donateDate', label: '捐赠日期', width: 110, type: 'date' },
    { prop: 'anonymousFlag', label: '匿名', width: 70, type: 'num' },
    { prop: 'voucherPath', label: '凭证', width: 84, type: 'image' },
    { prop: 'verifyStatus', label: '核对状态', width: 100, type: 'status' },
    { prop: 'receiptStatus', label: '票据', width: 90 },
    { prop: 'createTime', label: '登记时间', width: 160, type: 'time' }
  ],
  fields: [
    { prop: 'projectId', label: '捐赠项目', type: 'project', required: true },
    { prop: 'donorName', label: '捐赠人', required: true },
    { prop: 'donorType', label: '捐赠类型', type: 'select', options: ['现金', '实物', '企业捐赠', '线上转账'], default: '现金' },
    { prop: 'amount', label: '捐赠金额', type: 'number', precision: 2, required: true },
    { prop: 'goodsDesc', label: '实物资助说明', type: 'textarea' },
    { prop: 'goodsValue', label: '实物估值', type: 'number', precision: 2 },
    { prop: 'donateDate', label: '捐赠日期', type: 'date' },
    { prop: 'intention', label: '捐赠意向', type: 'textarea' },
    { prop: 'anonymousFlag', label: '是否匿名', type: 'switch', default: 0, hint: '匿名记录在公开端不展示姓名' },
    { prop: 'certFlag', label: '是否需要证书', type: 'switch', default: 1 },
    { prop: 'voucherPath', label: '转账/收款凭证', type: 'image', required: true, hint: '无凭证的捐赠无法通过核对' },
    { prop: 'fundUsage', label: '资金用途说明', type: 'textarea' }
  ]
}

async function issueCert(row) {
  await ElMessageBox.confirm(`为「${row.donorName}」的 ${row.amount} 元捐赠生成感谢证书？`, '生成证书', { type: 'warning' })
  const d = await request.post(`/api/donation/${row.id}/certificate`)
  ElMessage.success(`证书已生成：${d.certNo}`)
  pageRef.value.reload()
}
</script>
