<template>
  <div>
    <div class="page-head">
      <div>
        <h1>组织管理</h1>
        <p>地方校友会、行业俱乐部、院系校友会的组织档案、负责人与成员规模</p>
      </div>
      <el-button plain @click="$router.push('/member-audit')">成员审核</el-button>
    </div>
    <CrudPage ref="pageRef" :cfg="cfg" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import CrudPage from '@/components/CrudPage.vue'

const pageRef = ref()
const cfg = {
  title: '校友组织',
  url: '/api/alumni-org',
  kwPlaceholder: '组织名称',
  statusOptions: ['启用', '停用'],
  rowWidth: 150,
  columns: [
    { prop: 'orgName', label: '组织名称', minWidth: 200, type: 'link' },
    { prop: 'orgType', label: '组织类型', width: 120 },
    { prop: 'regionName', label: '所在地区', width: 110 },
    { prop: 'college', label: '挂靠学院', minWidth: 150 },
    { prop: 'gradeYear', label: '届别', width: 80, type: 'num' },
    { prop: 'leaderName', label: '负责人', width: 110 },
    { prop: 'leaderPhone', label: '联系电话', width: 130 },
    { prop: 'memberCount', label: '成员数', width: 90, type: 'num' },
    { prop: 'status', label: '状态', width: 90, type: 'status' },
    { prop: 'createTime', label: '创建时间', width: 160, type: 'time' }
  ],
  fields: [
    { prop: 'orgName', label: '组织名称', required: true },
    { prop: 'orgCode', label: '组织编码' },
    { prop: 'orgType', label: '组织类型', type: 'select', options: ['地方校友会', '行业俱乐部', '院系校友会', '年级理事会'] },
    { prop: 'college', label: '挂靠学院' },
    { prop: 'regionName', label: '所在地区' },
    { prop: 'gradeYear', label: '届别', type: 'number' },
    { prop: 'leaderName', label: '负责人' },
    { prop: 'leaderPhone', label: '负责人电话' },
    { prop: 'memberCount', label: '成员数', type: 'number' },
    { prop: 'intro', label: '组织简介', type: 'textarea' },
    { prop: 'coverImage', label: '封面图', type: 'image' },
    { prop: 'status', label: '状态', type: 'select', options: ['启用', '停用'], default: '启用' }
  ]
}
</script>
