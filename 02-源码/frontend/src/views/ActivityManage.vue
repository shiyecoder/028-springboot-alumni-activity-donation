<template>
  <div>
    <div class="page-head">
      <div>
        <h1>活动管理</h1>
        <p>活动立项后提交审核，审核通过进入报名中；满员自动转入候补，取消报名自动递补</p>
      </div>
      <el-button plain @click="$router.push('/activity-audit')">待审核活动</el-button>
    </div>
    <CrudPage ref="pageRef" :cfg="cfg" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import CrudPage from '@/components/CrudPage.vue'

const pageRef = ref()
const cfg = {
  title: '活动',
  url: '/api/activity',
  kwPlaceholder: '活动标题',
  statusOptions: ['待审核', '报名中', '进行中', '已归档', '已驳回', '已取消'],
  rowWidth: 150,
  columns: [
    { prop: 'poster', label: '海报', width: 84, type: 'image' },
    { prop: 'title', label: '活动标题', minWidth: 220, type: 'link' },
    { prop: 'activityType', label: '类型', width: 110 },
    { prop: 'orgName', label: '主办组织', minWidth: 160 },
    { prop: 'location', label: '地点', minWidth: 150 },
    { prop: 'startTime', label: '开始时间', width: 160, type: 'time' },
    { prop: 'capacity', label: '名额', width: 80, type: 'num' },
    { prop: 'signupCount', label: '已报名', width: 90, type: 'num' },
    { prop: 'waitCount', label: '候补', width: 80, type: 'num' },
    { prop: 'checkinCount', label: '签到', width: 80, type: 'num' },
    { prop: 'status', label: '状态', width: 100, type: 'status' }
  ],
  fields: [
    { prop: 'title', label: '活动标题', required: true },
    { prop: 'activityType', label: '活动类型', type: 'select', options: ['校友返校', '行业沙龙', '公益徒步', '讲座论坛', '文体赛事', '年级聚会'] },
    { prop: 'orgName', label: '主办组织' },
    { prop: 'college', label: '所属学院' },
    { prop: 'location', label: '活动地点' },
    { prop: 'startTime', label: '开始时间', type: 'datetime' },
    { prop: 'endTime', label: '结束时间', type: 'datetime' },
    { prop: 'capacity', label: '名额', type: 'number', default: 50 },
    { prop: 'chargePerson', label: '负责人' },
    { prop: 'auditMode', label: '报名方式', type: 'select', options: ['自动通过', '人工审核'] },
    { prop: 'poster', label: '活动海报', type: 'image' },
    { prop: 'agenda', label: '活动议程', type: 'textarea' },
    { prop: 'status', label: '状态', type: 'select', options: ['待审核', '报名中', '进行中', '已归档'] }
  ]
}
</script>
