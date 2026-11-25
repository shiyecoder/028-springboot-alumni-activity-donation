<template>
  <div>
    <div class="page-head">
      <div>
        <h1>活动审核</h1>
        <p>仅「待审核」的活动可审核；通过后进入报名中并开放报名入口，驳回必须填写原因</p>
      </div>
    </div>
    <CrudPage ref="pageRef" :cfg="cfg">
      <template #row-actions="{ row }">
        <template v-if="row.status === '待审核'">
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
const cfg = {
  title: '活动审核',
  url: '/api/activity',
  kwPlaceholder: '活动标题',
  rowWidth: 190,
  readonly: true,
  noDelete: true,
  params: { status: '待审核' },
  columns: [
    { prop: 'poster', label: '海报', width: 84, type: 'image' },
    { prop: 'title', label: '活动标题', minWidth: 220, type: 'link' },
    { prop: 'activityType', label: '类型', width: 110 },
    { prop: 'orgName', label: '主办组织', minWidth: 160 },
    { prop: 'location', label: '地点', minWidth: 140 },
    { prop: 'startTime', label: '开始时间', width: 160, type: 'time' },
    { prop: 'capacity', label: '名额', width: 80, type: 'num' },
    { prop: 'chargePerson', label: '负责人', width: 100 },
    { prop: 'status', label: '状态', width: 100, type: 'status' },
    { prop: 'createTime', label: '提交时间', width: 160, type: 'time' }
  ],
  fields: [
    { prop: 'title', label: '活动标题' },
    { prop: 'activityType', label: '活动类型' },
    { prop: 'orgName', label: '主办组织' },
    { prop: 'location', label: '活动地点' },
    { prop: 'startTime', label: '开始时间', type: 'datetime' },
    { prop: 'endTime', label: '结束时间', type: 'datetime' },
    { prop: 'capacity', label: '名额' },
    { prop: 'chargePerson', label: '负责人' },
    { prop: 'agenda', label: '活动议程', type: 'textarea' },
    { prop: 'status', label: '状态' }
  ]
}

const onPass = (row) => audit({ url: `/api/activity/${row.id}/audit`, status: '报名中', name: row.title, label: '审核通过并开放报名' })
  .then(() => pageRef.value.reload()).catch(() => {})
const onReject = (row) => audit({ url: `/api/activity/${row.id}/audit`, status: '已驳回', name: row.title, label: '驳回', reason: true, reasonKey: 'reason' })
  .then(() => pageRef.value.reload()).catch(() => {})
</script>
