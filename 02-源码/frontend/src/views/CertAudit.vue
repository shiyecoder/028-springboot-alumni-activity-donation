<template>
  <div>
    <div class="page-head">
      <div>
        <h1>认证审核</h1>
        <p>校友提交的认证材料逐条核对，通过后档案状态变为「已认证」，驳回必须说明原因</p>
      </div>
      <el-radio-group v-model="tab" @change="switchTab">
        <el-radio-button label="待审核" />
        <el-radio-button label="已认证" />
        <el-radio-button label="已驳回" />
      </el-radio-group>
    </div>
    <CrudPage ref="pageRef" :cfg="cfg">
      <template #row-actions="{ row }">
        <template v-if="row.certStatus === '待审核'">
          <el-button link type="success" @click="onPass(row)">通过</el-button>
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
const tab = ref('待审核')
/** 切换页签只改固定筛选参数，不改变列定义，避免整表重渲染 */
const cfg = {
  title: '认证申请',
  url: '/api/alumni',
  kwPlaceholder: '姓名',
  rowWidth: 190,
  readonly: true,
  noDelete: true,
  params: { status: '待审核' },
  columns: [
    { prop: 'alumniNo', label: '档案编号', width: 130 },
    { prop: 'realName', label: '姓名', width: 90, type: 'link' },
    { prop: 'studentNo', label: '学号', width: 130 },
    { prop: 'college', label: '学院', minWidth: 140 },
    { prop: 'major', label: '专业', minWidth: 130 },
    { prop: 'graduateYear', label: '毕业年份', width: 96, type: 'num' },
    { prop: 'certMaterial', label: '认证材料', minWidth: 200 },
    { prop: 'certStatus', label: '状态', width: 100, type: 'status' },
    { prop: 'certRemark', label: '审核意见', minWidth: 170 },
    { prop: 'auditTime', label: '审核时间', width: 160, type: 'time' }
  ],
  fields: [
    { prop: 'realName', label: '姓名' },
    { prop: 'studentNo', label: '学号' },
    { prop: 'college', label: '学院' },
    { prop: 'major', label: '专业' },
    { prop: 'graduateYear', label: '毕业年份' },
    { prop: 'phone', label: '手机' },
    { prop: 'email', label: '邮箱' },
    { prop: 'certMaterial', label: '认证材料', type: 'textarea' },
    { prop: 'certStatus', label: '认证状态' },
    { prop: 'certRemark', label: '审核意见', type: 'textarea' }
  ]
}

function switchTab(v) {
  cfg.params.status = v
  if (pageRef.value) pageRef.value.reload()
}
const onPass = (row) => audit({ url: `/api/alumni/${row.id}/audit`, status: '已认证', name: row.realName, label: '认证通过', body: { remark: '材料齐全，信息与学籍库一致' } })
  .then(() => { pageRef.value.reload(); tab.value = '已认证' }).catch(() => {})
const onReject = (row) => audit({ url: `/api/alumni/${row.id}/audit`, status: '已驳回', name: row.realName, label: '驳回', reason: true })
  .then(() => pageRef.value.reload()).catch(() => {})
</script>
