import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css';
import axios from 'axios'

Vue.config.productionTip = false

// 使用 ElementUI
Vue.use(ElementUI)

// 配置全局 Axios
Vue.prototype.$axios = axios
axios.defaults.baseURL = 'http://127.0.0.1:8000/api/' // 指向你的 Django 后端

// 🔴 [核心修复] 请求拦截器：自动携带 Token
axios.interceptors.request.use(config => {
  // 从 localStorage 获取 Token
  const token = localStorage.getItem('token');
  
  if (token) {
    // 这里的 'Token' 是 Django REST Framework 的标准前缀，注意后面有个空格
    config.headers.Authorization = `Token ${token}`; 
  }
  return config;
}, error => {
  return Promise.reject(error);
});

// [可选] 响应拦截器：处理 Token 过期或 403/401 错误
axios.interceptors.response.use(response => {
  return response;
}, error => {
  if (error.response) {
    // 如果后端返回 401 (未认证) 或 403 (禁止)，说明 Token 可能失效
    if (error.response.status === 401 || error.response.status === 403) {
      // 避免在登录页重复跳转
      if (router.currentRoute.path !== '/login') {
        localStorage.clear(); // 清除无效 Token
        router.replace('/login'); // 强制跳转回登录页
        // ElementUI.Message.error('登录已过期，请重新登录');
      }
    }
  }
  return Promise.reject(error);
});

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')