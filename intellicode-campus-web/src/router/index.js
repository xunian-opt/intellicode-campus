import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '../views/Login.vue'
import store from '../store' 

Vue.use(VueRouter)

// 1. 解决 "Redirected when going from..." 报错
const originalPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => err)
}

export const constantRoutes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    hidden: true
  },
  {
    path: '/',
    redirect: '/admin/dashboard',
    hidden: true
  }
]

const createRouter = () => new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: constantRoutes
})

const router = createRouter()

// 2. 路由重置方法 (用于注销时清空动态路由)
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // 核心：重置 matcher
}

router.beforeEach(async (to, from, next) => {
	
	document.title = "基于Django+Vue的在线编程题库与代码提交评测系统"
	
  const token = localStorage.getItem('token')

  if (token) {
    if (to.path === '/login') {
      next({ path: '/' })
    } else {
      // 判断是否已经加载过动态路由
      if (store.state.isRoutesLoaded) {
        next()
      } else {
        try {
          // 获取后端菜单数据并生成路由表
          const accessRoutes = await store.dispatch('GenerateRoutes')
          
          // 🔴 核心修复：使用 addRoute 循环添加，替代已废弃的 addRoutes
          accessRoutes.forEach(route => {
            router.addRoute(route)
          })
          
          store.commit('SET_LOADED', true)
          
          // 确保路由添加完整后跳转
          next({ ...to, replace: true })
        } catch (error) {
          console.error('路由加载失败', error)
          localStorage.clear()
          next(`/login?redirect=${to.path}`)
        }
      }
    }
  } else {
    if (to.path === '/login') {
      next()
    } else {
      next(`/login?redirect=${to.path}`)
    }
  }
})

export default router