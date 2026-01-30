import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '@/views/Login'
import store from '@/store' 
import Layout from '@/views/layout/AdminLayout'
import StudentLayout from '@/views/student/layout/StudentLayout' // 🟢 确保引入了学生布局

Vue.use(VueRouter)

// 解决 "Redirected when going from..." 报错
const originalPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(location) {
  return originalPush.call(this, location).catch(err => err)
}

/**
 * constantRoutes
 * 静态路由：所有角色均可见
 */
export const constantRoutes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    hidden: true
  },
  {
    path: '/404',
    component: () => import('@/views/error-page/404'), 
    hidden: true
  },
  
  // 🟢 [核心] 学生端静态路由配置
  {
    path: '/student',
    component: StudentLayout,
    redirect: '/student/home',
    hidden: true,
    children: [
      {
        path: 'home',
        name: 'StudentHome',
        component: () => import('@/views/student/Home'),
        meta: { title: '学习首页' }
      },
// 🟢 [新增] 公告列表页
      {
        path: 'notices',
        name: 'StudentNoticeList',
        component: () => import('@/views/student/notice/List'),
        meta: { title: '公告列表' }
      },
      // 🟢 [新增] 公告详情页
      {
        path: 'notice/:id',
        name: 'StudentNoticeDetail',
        component: () => import('@/views/student/notice/Detail'),
        meta: { title: '公告详情' }
      },
      {
        path: 'courses',
        name: 'StudentCourseList',
        component: () => import('@/views/student/course/List'),
        meta: { title: '课程中心' }
      },
      {
        path: 'course/:id',
        name: 'StudentCourseDetail',
        component: () => import('@/views/student/course/Detail'),
        meta: { title: '课程详情' }
      },
	  {
      path: 'problems',
      name: 'StudentProblemList',
      component: () => import('@/views/student/competitions/ProblemList'),
      meta: { title: '编程题库' }
    },
    {
      path: 'problem/:id', // 详情页路由
      name: 'StudentProblemDetail',
      component: () => import('@/views/student/competitions/ProblemDetail'),
      meta: { title: '做题页面', hideFooter: true } // hideFooter可选，用于全屏沉浸式
    },
    {
      path: 'competitions',
      name: 'StudentCompetitionList',
      component: () => import('@/views/student/competitions/CompetitionList'),
      meta: { title: '竞赛活动' }
    },
      {
        path: 'profile',
        name: 'StudentProfile',
        component: () => import('@/views/student/profile/Index'),
        meta: { title: '个人中心' }
      }
    ]
  },

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
          meta: { title: '字典数据', activeMenu: '/system/dict' }
        }
      ]
    },
]

const createRouter = () => new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher
}

// ----------------------------------------------------------------------
// 🟢 全局路由守卫 (核心修复逻辑)
// ----------------------------------------------------------------------
router.beforeEach(async (to, from, next) => {
  document.title = to.meta.title ? `${to.meta.title} - 在线编程题库` : "基于Django+Vue的在线编程题库"
  
  const token = localStorage.getItem('token')

  if (token) {
    if (to.path === '/login') {
      next({ path: '/' })
    } else {
      if (store.state.isRoutesLoaded) {
        next()
      } else {
        try {
          // 1. 获取后端动态路由
          // 注意：accessRoutes 此时可能包含 { path: '*', ... } 这个隐藏路由
          const accessRoutes = await store.dispatch('GenerateRoutes')
          
          let rootRedirect = ''
          
          // 🟢 [核心修复] 查找第一个“可见”的菜单 (exclusion hidden)
          const firstVisibleRoute = accessRoutes.find(r => !r.hidden && r.path !== '*')

          if (firstVisibleRoute) {
             // --- 情况A: 管理员/教师 (有可见菜单) ---
             rootRedirect = firstVisibleRoute.path
             
             // 如果是目录，尝试取第一个子菜单
             if (firstVisibleRoute.children && firstVisibleRoute.children.length > 0) {
                 const firstChild = firstVisibleRoute.children.find(c => !c.hidden)
                 if (firstChild) {
                     const basePath = firstVisibleRoute.path.endsWith('/') ? firstVisibleRoute.path : firstVisibleRoute.path + '/'
                     const childPath = firstChild.path.startsWith('/') ? firstChild.path.slice(1) : firstChild.path
                     rootRedirect = basePath + childPath
                 }
             }
          } else {
             // --- 情况B: 学生 (没有可见菜单，只有隐藏的 404 路由) ---
             // 强制跳转到学生首页
             rootRedirect = '/student/home'
          }

          // 兜底：防止 rootRedirect 依然为空
          if (!rootRedirect) rootRedirect = '/404'

          // 动态添加根路由重定向
          router.addRoute({
            path: '/',
            redirect: rootRedirect,
            hidden: true
          })
          
          // 添加后端返回的动态路由
          accessRoutes.forEach(route => {
            router.addRoute(route)
          })
          
          store.commit('SET_LOADED', true)
          next({ ...to, replace: true })

        } catch (error) {
          console.error('路由加载失败', error)
          localStorage.clear()
          next(`/login?redirect=${to.path}`)
        }
      }
    }
  } else {
    const whiteList = ['/login', '/404']
    if (whiteList.indexOf(to.path) !== -1) {
      next()
    } else {
      next(`/login?redirect=${to.path}`)
    }
  }
})

export default router