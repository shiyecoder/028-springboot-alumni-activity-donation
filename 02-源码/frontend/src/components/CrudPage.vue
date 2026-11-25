<template>
  <div>
    <!-- 筛选区：服务端分页，切换筛选条件后回到第 1 页 -->
    <div class="card">
      <div class="card-b">
        <div class="filter-bar">
          <el-input v-if="cfg.kwPlaceholder" v-model="kw" :placeholder="cfg.kwPlaceholder" clearable
                    @keyup.enter="reload" @clear="reload" />
          <el-select v-if="cfg.statusOptions" v-model="status" placeholder="全部状态" clearable @change="reload">
            <el-option v-for="o in cfg.statusOptions" :key="o" :label="o" :value="o" />
          </el-select>
          <slot name="filters" :reload="reload" />
          <el-button type="primary" @click="reload">查询</el-button>
          <el-button @click="reset">重置</el-button>
          <div style="margin-left:auto;display:flex;gap:8px">
            <slot name="toolbar" />
            <el-button v-if="!cfg.readonly" type="primary" plain @click="openAdd">
              <el-icon><Plus /></el-icon>新建
            </el-button>
          </div>
        </div>
      </div>
    </div>

    <div class="card">
      <div class="card-h">
        <h2>{{ cfg.title }}</h2>
        <div class="r">共 {{ total }} 条</div>
      </div>
      <el-table :data="rows" v-loading="loading" border style="width:100%" row-key="id">
        <el-table-column v-for="c in cfg.columns" :key="c.prop" :prop="c.prop" :label="c.label"
                         :min-width="c.minWidth || 110" :width="c.width" :align="c.align || 'left'"
                         :fixed="c.fixed" show-overflow-tooltip>
          <template #default="{ row }">
            <img v-if="c.type === 'image'" class="thumb" :src="row[c.prop]" alt="" />
            <el-tag v-else-if="c.type === 'status'" :type="statusType(row[c.prop])" effect="light">
              {{ statusText(row[c.prop]) }}
            </el-tag>
            <el-progress v-else-if="c.type === 'progress'" :percentage="Math.min(100, Number(row[c.prop] || 0))"
                         :stroke-width="8" :color="'#2F6F6A'" />
            <span v-else-if="c.type === 'time'" class="num">{{ formatTime(row[c.prop]) }}</span>
            <span v-else-if="c.type === 'date'" class="num">{{ formatDate(row[c.prop]) }}</span>
            <span v-else-if="c.type === 'money'" class="num">{{ money(row[c.prop]) }}</span>
            <span v-else-if="c.type === 'num'" class="num">{{ row[c.prop] ?? '-' }}</span>
            <a v-else-if="c.type === 'link'" class="link" @click="$emit('row-click', row)">{{ row[c.prop] }}</a>
            <span v-else>{{ row[c.prop] ?? '-' }}</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" :width="cfg.rowWidth || 180" fixed="right" class-name="op-col">
          <template #default="{ row }">
            <el-button link type="primary" @click="openView(row)">查看</el-button>
            <el-button v-if="!cfg.readonly" link type="primary" @click="openEdit(row)">编辑</el-button>
            <el-button v-if="!cfg.readonly && !cfg.noDelete" link type="danger" @click="remove(row)">删除</el-button>
            <slot name="row-actions" :row="row" :reload="load" />
          </template>
        </el-table-column>
        <template #empty>
          <el-empty :description="cfg.emptyText || '当前筛选条件下无记录，清空筛选或新建'" />
        </template>
      </el-table>
      <el-pagination background layout="total, sizes, prev, pager, next" :total="total"
                     v-model:current-page="page" v-model:page-size="size" :page-sizes="[10, 20, 50]"
                     @current-change="load" @size-change="reload" />
    </div>

    <!-- 新建/编辑使用右侧抽屉，关闭前检测未保存内容 -->
    <el-drawer v-model="visible" :title="(viewMode ? '查看' : form.id ? '编辑' : '新建') + cfg.title" size="560px"
               :before-close="beforeClose">
      <el-form :model="form" label-width="110px" :disabled="viewMode">
        <el-form-item v-for="f in cfg.fields" :key="f.prop" :label="f.label" :required="f.required">
          <el-select v-if="f.type === 'select'" v-model="form[f.prop]" style="width:220px" clearable>
            <el-option v-for="o in f.options" :key="o" :label="o" :value="o" />
          </el-select>
          <el-select v-else-if="f.type === 'project'" v-model="form[f.prop]" filterable style="width:100%">
            <el-option v-for="p in projects" :key="p.id" :label="p.projectName" :value="p.id" />
          </el-select>
          <el-input v-else-if="f.type === 'textarea'" v-model="form[f.prop]" type="textarea" :rows="3" />
          <el-date-picker v-else-if="f.type === 'date'" v-model="form[f.prop]" type="date"
                          value-format="YYYY-MM-DD" style="width:200px" />
          <el-date-picker v-else-if="f.type === 'datetime'" v-model="form[f.prop]" type="datetime"
                          value-format="YYYY-MM-DD HH:mm:ss" style="width:220px" />
          <el-input-number v-else-if="f.type === 'number'" v-model="form[f.prop]" :precision="f.precision || 0"
                           :min="0" style="width:200px" />
          <el-switch v-else-if="f.type === 'switch'" v-model="form[f.prop]" :active-value="1" :inactive-value="0" />
          <img v-else-if="f.type === 'image' && viewMode && form[f.prop]" class="thumb" style="width:96px;height:72px"
               :src="form[f.prop]" alt="" />
          <el-upload v-else-if="f.type === 'image'" :show-file-list="false" :http-request="(o) => doUpload(o, f.prop)">
            <img v-if="form[f.prop]" class="thumb" style="width:96px;height:72px" :src="form[f.prop]" alt="" />
            <el-button v-else size="small">上传图片</el-button>
          </el-upload>
          <el-input v-else v-model="form[f.prop]" style="width:320px" />
          <div v-if="f.hint" class="hint" style="width:100%">{{ f.hint }}</div>
        </el-form-item>
        <slot name="form-extra" :form="form" :view-mode="viewMode" />
      </el-form>
      <template #footer>
        <el-button @click="visible = false">{{ viewMode ? '关闭' : '取消' }}</el-button>
        <el-button v-if="!viewMode" type="primary" :loading="saving" @click="save">保存</el-button>
      </template>
    </el-drawer>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import request from '@/utils/request'
import { formatTime, formatDate, statusText, statusType, money } from '@/utils/format'

const props = defineProps({ cfg: { type: Object, required: true } })
const emit = defineEmits(['row-click', 'saved'])
const cfg = props.cfg
const rows = ref([])
const total = ref(0)
const page = ref(1)
const size = ref(10)
const kw = ref('')
const status = ref('')
const loading = ref(false)
const saving = ref(false)
const visible = ref(false)
const viewMode = ref(false)
const dirty = ref(false)
const form = reactive({})
const projects = ref([])

async function load() {
  loading.value = true
  try {
    const d = await request.get(cfg.url + '/page', {
      params: { page: page.value, size: size.value, kw: kw.value, status: status.value, ...(cfg.params || {}) }
    })
    rows.value = d.list || []
    total.value = d.total || 0
  } finally { loading.value = false }
}
function reload() { page.value = 1; load() }
function reset() { kw.value = ''; status.value = ''; reload() }

function openAdd() {
  Object.keys(form).forEach((k) => delete form[k])
  ;(cfg.fields || []).forEach((f) => { form[f.prop] = f.default ?? null })
  viewMode.value = false
  dirty.value = false
  visible.value = true
}
function openEdit(row) {
  Object.keys(form).forEach((k) => delete form[k])
  Object.assign(form, JSON.parse(JSON.stringify(row)))
  viewMode.value = false
  dirty.value = false
  visible.value = true
}
/** 查看：同抽屉只读呈现，字段与编辑一致，避免另建一套详情页造成口径不一致 */
function openView(row) {
  openEdit(row)
  viewMode.value = true
  dirty.value = false
  emit('row-click', row)
}
watch(form, () => { dirty.value = true }, { deep: true })

async function beforeClose(done) {
  if (!dirty.value) return done()
  try {
    await ElMessageBox.confirm('表单内容尚未保存，确认放弃修改？', '未保存提示', { type: 'warning' })
    done()
  } catch (e) { /* 继续编辑 */ }
}

async function save() {
  saving.value = true
  try {
    if (form.id) await request.put(cfg.url + '/' + form.id, form)
    else await request.post(cfg.url, form)
    ElMessage.success('保存成功')
    dirty.value = false
    visible.value = false
    load()
    emit('saved')
  } finally { saving.value = false }
}

async function remove(row) {
  await ElMessageBox.confirm('删除后不可恢复，确认删除该记录？', '删除确认', { type: 'warning' })
  await request.delete(cfg.url + '/' + row.id)
  ElMessage.success('已删除')
  load()
}

async function doUpload(opt, prop) {
  const fd = new FormData()
  fd.append('file', opt.file)
  const d = await request.post('/api/file/upload', fd, { headers: { 'Content-Type': 'multipart/form-data' } })
  form[prop] = d.path
  ElMessage.success('上传成功')
}

async function loadProjects() {
  try {
    const d = await request.get('/api/project/page', { params: { page: 1, size: 100 } })
    projects.value = d.list || []
  } catch (e) { /* 非项目相关页面无需项目列表 */ }
}

onMounted(() => { load(); loadProjects() })
defineExpose({ reload, load, openEdit, openView, openAdd })
</script>

<style scoped>
/* 操作列不换行，按钮间距统一，避免「编辑/删除」被拆成两行 */
:deep(.op-col .cell) { display: flex; align-items: center; justify-content: flex-start; gap: 8px; white-space: nowrap; }
:deep(.op-col .el-button + .el-button) { margin-left: 0; }
</style>
