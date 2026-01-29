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
    // 过滤掉类型为 'F' (按钮) 的节点
    if (route.menu_type === 'F') {
      return
    }

    // 构造路由对象
    const tmp = {
      path: route.path,
      component: loadView(route.component), 
      name: route.path, // 用 path 做 name
      
      // 🟢 [核心修改] 强制显示目录
      // 如果是目录(M)，设置为 alwaysShow: true
      // 这样即使该目录下只有一个子菜单，也会显示父级折叠框
      alwaysShow: route.menu_type === 'M',
      
      meta: { 
        title: route.title, 
        icon: route.icon 
      }
    }

    // 处理子菜单
    if (route.children && route.children.length) {
      // 递归过滤子节点
      tmp.children = filterAsyncRoutes(route.children, tmp.path)
    }
    
    res.push(tmp)
  })
  return res
}

export default new Vuex.Store({
  state: {
    menuList: [], // 侧边栏菜单数据
    isRoutesLoaded: false,
	user: {}   //用户信息状态
  },
  mutations: {
    SET_MENU(state, menuList) {
      state.menuList = menuList
    },
    SET_LOADED(state, status) {
      state.isRoutesLoaded = status
    },
	// 🟢 [新增] 更新用户信息的方法
	SET_USER(state, userInfo) {
	  state.user = userInfo
	},
	    // 🟢 [新增] 单独更新头像的方法
	SET_AVATAR(state, avatarUrl) {
	  if (state.user) {
	        // 使用 Vue.set 确保响应式更新
	    Vue.set(state.user, 'avatar', avatarUrl)
	 }
	}
  },
  actions: {
// 🟢 [新增] 获取用户信息的 Action (供 Layout 调用)
    GetUserInfo({ commit }) {
      return new Promise((resolve, reject) => {
        axios.get('users/info/').then(res => {
          commit('SET_USER', res.data)
          resolve(res.data)
        }).catch(error => {
          reject(error)
        })
      })
    },
    GenerateRoutes({ commit }) {
      return new Promise((resolve, reject) => {
        
        // 1. 获取 Token
        const token = localStorage.getItem('token');
        
        // 2. 构造请求头
        const config = {
            headers: { 
                'Authorization': token ? `Token ${token}` : '' 
            }
        };
        
        // 3. 发送请求获取路由
        axios.get('system/menu/user_routers/', config).then(res => {
            const backEndMenus = res.data
          
            // 4. 生成路由表
            const accessedRoutes = filterAsyncRoutes(backEndMenus)
          
            commit('SET_MENU', accessedRoutes)
            
            // 添加 404 兜底路由
            accessedRoutes.push({ path: '*', redirect: '/404', hidden: true })
            
            resolve(accessedRoutes)
        }).catch(error => {
            reject(error)
        })
      })
    }
  }
})