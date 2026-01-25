import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

// 组件映射函数
function loadView(view) {
  if (view === 'Layout') {
    return () => import('@/views/layout/AdminLayout.vue')
  }
  // 动态引入 views 下的组件
  return () => import(`@/views/${view}.vue`)
}

// 递归处理后端菜单数据，转换为 Vue 路由格式
function filterAsyncRoutes(routes, parentPath = '') {
  const res = []
  
  routes.forEach(route => {
    // 🔴 核心修改：过滤掉类型为 'F' (按钮) 的节点
    // 如果后端没有返回 menu_type 字段，默认显示（兼容旧数据）
    if (route.menu_type === 'F') {
      return
    }

    // 构造路由对象
    const tmp = {
      path: route.path,
      component: loadView(route.component), 
      name: route.path, // 用 path 做 name
      meta: { 
        title: route.title, 
        icon: route.icon 
      }
    }

    // 处理子菜单
    if (route.children && route.children.length) {
      // 递归过滤子节点
      tmp.children = filterAsyncRoutes(route.children, tmp.path)
      
      // 如果子节点全部被过滤掉了（比如全是按钮），且当前节点不是目录，
      // 可以考虑是否还要保留当前节点（视需求而定，通常保留空目录也没关系）
    }
    
    res.push(tmp)
  })
  return res
}

export default new Vuex.Store({
  state: {
    menuList: [], // 侧边栏菜单数据
    isRoutesLoaded: false 
  },
  mutations: {
    SET_MENU(state, menuList) {
      state.menuList = menuList
    },
    SET_LOADED(state, status) {
      state.isRoutesLoaded = status
    }
  },
  actions: {
    GenerateRoutes({ commit }) {
      return new Promise((resolve, reject) => {
        axios.get('system/menu/').then(res => {
          const backEndMenus = res.data
          
          // 1. 生成路由表 (这里会自动过滤掉按钮)
          const accessedRoutes = filterAsyncRoutes(backEndMenus)
          
          // 2. 将过滤后的路由表存入 Vuex，用于渲染侧边栏
          // 注意：这里我们存的是 accessedRoutes，而不是原始 backEndMenus
          // 这样侧边栏就只显示过滤后的菜单了
          commit('SET_MENU', accessedRoutes)
          
          // 3. 追加 404
          accessedRoutes.push({ path: '*', redirect: '/404', hidden: true })
          
          resolve(accessedRoutes)
        }).catch(error => {
          reject(error)
        })
      })
    }
  }
})