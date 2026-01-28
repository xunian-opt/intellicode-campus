import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '@/views/Login'
import store from '@/store' 
import Layout from '@/views/layout/AdminLayout'

Vue.use(VueRouter)

// 1. 解决 "Redirected when going from..." 报错
const originalPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => err)
}

/**
 * constantRoutes
 * 所有权限通用的静态路由 (登录页、404页等)
 */
export const constantRoutes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    hidden: true
  },
  
  // 🟢 [必须存在] 404 路由
  // 防止动态路由匹配失败时陷入死循环
  {
    path: '/404',
    component: () => import('@/views/error-page/404'), 
    hidden: true
  },

  // 🟢 [核心修改] 移除这里原本的 path: '/' 配置
  // 我们将在 beforeEach 中根据用户权限动态添加它，防止学生账号被重定向到管理员页面

  // 字典数据管理 (隐藏路由)
  {
      path: '/dict-manage',
      component: Layout,
      hidden: true,  
      children: [
        {
          path: 'index',
          component: () => import('@/views/admin/system/DictDataList'),
          name: 'DictData',
          meta: { 
            title: '字典数据', 
            activeMenu: '/system/dict' 
          }
        }
      ]
    },
]

const createRouter = () => new VueRouter({
  mode: 'history', // 去掉url中的#
  base: process.env.BASE_URL,
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// 2. 路由重置方法 (用于注销时清空动态路由)
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // 核心：重置 matcher
}

// 3. 全局路由守卫
router.beforeEach(async (to, from, next) => {
	
  // 设置网页标题
  document.title = to.meta.title ? `${to.meta.title} - 在线编程题库` : "基于Django+Vue的在线编程题库与代码提交评测系统"
	
  const token = localStorage.getItem('token')

  if (token) {
    if (to.path === '/login') {
      // 已登录则跳转首页
      next({ path: '/' })
    } else {
      // 判断是否已经加载过动态路由
      if (store.state.isRoutesLoaded) {
        next()
      } else {
        try {
          // 1. 获取后端菜单数据并生成路由表
          const accessRoutes = await store.dispatch('GenerateRoutes')
          
          // -------------------------------------------------------------
          // 🟢 [核心修复] 动态计算“首页”路径
          // -------------------------------------------------------------
          let rootRedirect = '/404' // 默认兜底
          
          // 寻找第一个有效的菜单作为首页
          if (accessRoutes && accessRoutes.length > 0) {
            // 找到第一个非隐藏的路由 (通常是目录或菜单)
            const firstRoute = accessRoutes.find(r => !r.hidden)
            if (firstRoute) {
               rootRedirect = firstRoute.path
               
               // 如果是目录(有子路由)，则取其第一个子菜单
               if (firstRoute.children && firstRoute.children.length > 0) {
                   const firstChild = firstRoute.children.find(c => !c.hidden)
                   if (firstChild) {
                       // 拼接路径，处理可能出现的双斜杠
                       const basePath = firstRoute.path.endsWith('/') ? firstRoute.path : firstRoute.path + '/'
                       const childPath = firstChild.path.startsWith('/') ? firstChild.path.slice(1) : firstChild.path
                       rootRedirect = basePath + childPath
                   }
               }
            }
          }

          // 🟢 动态添加根路由：将 / 重定向到刚才计算出的 rootRedirect
          // 这样管理员会去 /admin/dashboard，学生会去 /course/list (或他们有的第一个菜单)
          router.addRoute({
            path: '/',
            component: Layout,
            redirect: rootRedirect,
            hidden: true
          })
          // -------------------------------------------------------------
          
          // 2. 循环添加其他动态路由
          accessRoutes.forEach(route => {
            router.addRoute(route)
          })
          
          // 3. 标记路由已加载
          store.commit('SET_LOADED', true)
          
          // 4. 确保路由添加完整后跳转 (replace: true 替换当前历史记录，防止回退空白)
          next({ ...to, replace: true })

        } catch (error) {
          console.error('路由加载失败', error)
          // 出错时清除 Token 并重定向回登录页，防止死循环
          localStorage.clear()
          next(`/login?redirect=${to.path}`)
        }
      }
    }
  } else {
    // 免登录白名单
    const whiteList = ['/login', '/404']
    if (whiteList.indexOf(to.path) !== -1) {
      next()
    } else {
      next(`/login?redirect=${to.path}`)
    }
  }
})

export default router