<template>
  <div>
    <div class="page-head">
      <div>
        <h1>校友档案</h1>
        <p>维护全院校友基础信息，认证状态由「认证审核」环节变更，此处不直接改写</p>
      </div>
      <el-button plain @click="$router.push('/cert-audit')">去认证审核</el-button>
    </div>
    <CrudPage ref="pageRef" :cfg="cfg">
      <template #row-actions="{ row }">
        <template v-if="row.certStatus === '待审核'">
          <el-button link type="success" @click="onPass(row)">认证</el-button>
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
  title: '校友档案',
  url: '/api/alumni',
  kwPlaceholder: '姓名',
  statusOptions: ['待审核', '已认证', '已驳回'],
  rowWidth: 220,
  columns: [
    { prop: 'alumniNo', label: '档案编号', width: 118 },
    { prop: 'realName', label: '姓名', width: 84, type: 'link' },
    { prop: 'certStatus', label: '认证状态', width: 96, type: 'status' },
    { prop: 'gender', label: '性别', width: 62 },
    { prop: 'college', label: '学院', minWidth: 130 },
    { prop: 'major', label: '专业', minWidth: 130 },
    { prop: 'graduateYear', label: '毕业年份', width: 92, type: 'num' },
    { prop: 'phone', label: '手机', width: 116 },
    { prop: 'workUnit', label: '工作单位', minWidth: 150 },
    { prop: 'regionName', label: '所在地区', width: 104 },
    { prop: 'auditTime', label: '认证时间', width: 150, type: 'time' }
  ],
  fields: [
    { prop: 'realName', label: '姓名', required: true },
    { prop: 'gender', label: '性别', type: 'select', options: ['男', '女'] },
    { prop: 'college', label: '学院' },
    { prop: 'major', label: '专业' },
    { prop: 'className', label: '班级' },
    { prop: 'graduateYear', label: '毕业年份', type: 'number' },
    { prop: 'phone', label: '手机' },
    { prop: 'email', label: '邮箱' },
    { prop: 'workUnit', label: '工作单位' },
    { prop: 'workTitle', label: '职务' },
    { prop: 'regionName', label: '所在地区' },
    { prop: 'industry', label: '所属行业' },
    { prop: 'avatar', label: '头像', type: 'image' }
  ]
}

const onPass = (row) => audit({ url: `/api/alumni/${row.id}/audit`, status: '已认证', name: row.realName, label: '认证通过' })
  .then(() => pageRef.value.reload()).catch(() => {})
const onReject = (row) => audit({ url: `/api/alumni/${row.id}/audit`, status: '已驳回', name: row.realName, label: '驳回', reason: true })
  .then(() => pageRef.value.reload()).catch(() => {})
</script>
