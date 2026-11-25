import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'

const service = axios.create({ baseURL: '', timeout: 30000 })

service.interceptors.request.use((cfg) => {
  const token = localStorage.getItem('alumni_token')
  if (token) cfg.headers.Authorization = 'Bearer ' + token
  return cfg
})

service.interceptors.response.use(
  (res) => {
    const body = res.data
    if (body && typeof body.code !== 'undefined') {
      if (body.code === 0) return body.data
      if (body.code === 401) {
        localStorage.removeItem('alumni_token')
        router.push('/login')
        ElMessage.error(body.msg || '登录已过期，请重新登录')
        return Promise.reject(new Error(body.msg))
      }
      ElMessage.error(body.msg || '请求失败')
      return Promise.reject(new Error(body.msg || '请求失败'))
    }
    return body
  },
  (err) => {
    if (err.response && err.response.status === 401) {
      localStorage.removeItem('alumni_token')
      router.push('/login')
    }
    ElMessage.error(err.message || '网络异常')
    return Promise.reject(err)
  }
)

export default service
