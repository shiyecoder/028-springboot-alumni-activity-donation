import { ElMessageBox, ElMessage } from 'element-plus'
import request from '@/utils/request'

/**
 * 统一审核交互：通过需二次确认；驳回/退回必须填写不少于 5 个字的原因（与后端校验保持一致）。
 * 用户取消时抛出 cancel，调用方统一 .catch(() => {}) 忽略即可。
 * @param {{url:string,id:number,status:string,body?:object,name?:string,label?:string,reason?:boolean,reasonKey?:string}} o
 */
export async function audit(o) {
  const body = { ...(o.body || {}), status: o.status }
  if (o.reason) {
    const { value } = await ElMessageBox.prompt(`请填写${o.label || '处理'}原因（不少于 5 个字）`, o.label || '填写原因', {
      inputType: 'textarea',
      inputValidator: (v) => ((v || '').trim().length >= 5 ? true : '原因不少于 5 个字')
    })
    body[o.reasonKey || 'remark'] = (value || '').trim()
  } else {
    await ElMessageBox.confirm(
      `确认将${o.name ? '「' + o.name + '」' : '该记录'}${o.label || '审核通过'}？`, '操作确认', { type: 'warning' })
  }
  await request.post(o.url, body)
  ElMessage.success('操作成功')
  return true
}
