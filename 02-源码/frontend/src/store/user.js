import { reactive } from 'vue'

/** 轻量全局状态：登录人、角色、动态菜单 */
export const store = reactive({
  user: JSON.parse(localStorage.getItem('alumni_user') || 'null'),
  menus: JSON.parse(localStorage.getItem('alumni_menus') || '[]'),
  setLogin(user, menus) {
    this.user = user
    this.menus = menus || []
    localStorage.setItem('alumni_user', JSON.stringify(user || null))
    localStorage.setItem('alumni_menus', JSON.stringify(menus || []))
  },
  setUser(user) {
    this.user = user
    localStorage.setItem('alumni_user', JSON.stringify(user || null))
  },
  logout() {
    this.user = null
    this.menus = []
    localStorage.removeItem('alumni_token')
    localStorage.removeItem('alumni_user')
    localStorage.removeItem('alumni_menus')
  }
})
