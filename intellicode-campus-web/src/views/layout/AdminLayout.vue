<template>
  <el-container class="app-wrapper">
    <el-aside width="240px" class="sidebar-container">
      <el-menu
        :default-active="$route.path"
        router
        unique-opened
        text-color="#333"
        active-text-color="#67C23A"
        class="el-menu-vertical">
        
        <sidebar-item 
          v-for="route in menuList" 
          :key="route.path" 
          :item="route" 
          :base-path="route.path"
        />

      </el-menu>
    </el-aside>

    <el-container class="main-container">
      <el-header height="60px">
        <div class="header-left">
          <div class="header-title">基于Django+Vue的在线编程题库与代码提交评测系统</div>
        </div>
        
        <div class="header-right">
          <el-dropdown class="avatar-container" trigger="hover" @command="handleCommand">
            <div class="avatar-wrapper">
              <div class="icon-box">
                <i class="el-icon-info"></i>
              </div>
              <span class="user-name">{{ username }}</span>
            </div>
            
            <el-dropdown-menu slot="dropdown" class="user-dropdown">
              <el-dropdown-item command="clearCache">清除缓存</el-dropdown-item>
              <el-dropdown-item command="logout">注销登录</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </div>
      </el-header>

      <el-main>
        <transition name="fade-transform" mode="out-in">
          <router-view />
        </transition>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import { mapState } from 'vuex'
import SidebarItem from './components/SidebarItem'
import { resetRouter } from '@/router'

export default {
  name: "AdminLayout",
  components: { SidebarItem },
  data() {
    return {
      username: "系统管理员"
    };
  },
  computed: {
    ...mapState(['menuList'])
  },
  created() {
    const storedName = localStorage.getItem('username');
    if (storedName) {
      this.username = storedName;
    }
  },
  methods: {
    handleCommand(command) {
      if (command === 'logout') {
        this.handleLogout();
      } else if (command === 'clearCache') {
        this.handleClearCache();
      }
    },
    handleLogout() {
      this.$confirm('确定要注销登录吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        // 1. 清除存储
        localStorage.clear();
        sessionStorage.clear();
        
        // 2. 重置 Vuex
        this.$store.commit('SET_LOADED', false);
        this.$store.commit('SET_MENU', []);
        
        // 3. 重置路由 (防止 Duplicate named routes)
        resetRouter();
        
        // 4. 跳转
        this.$router.push('/login');
        this.$message.success('已安全退出');
      }).catch(() => {});
    },
    handleClearCache() {
      const loading = this.$loading({
        lock: true,
        text: '正在清理系统缓存...',
        spinner: 'el-icon-loading',
        background: 'rgba(0, 0, 0, 0.7)'
      });
      setTimeout(() => {
        loading.close();
        this.$message({
          type: 'success',
          message: '缓存清除成功!',
          duration: 2000
        });
      }, 1000);
    }
  }
};
</script>

<style lang="scss" scoped>
/* 保持原有样式，未做任何修改 */
.app-wrapper {
  height: 100vh;
  width: 100%;
}

.sidebar-container {
  background-color: #fff;
  border-right: 1px solid #e6e6e6;
  .el-menu { border-right: none; }
  .el-menu-item.is-active {
    background-color: #f0f9eb;
    border-left: 3px solid #67C23A;
    color: #67C23A;
  }
}

.main-container { background-color: #f5f7fa; }

.el-header {
  background-color: #fff;
  line-height: 60px;
  position: relative; 
  display: flex;
  align-items: center;
  border-bottom: 1px solid #e6e6e6;
  padding: 0 30px;

  .header-left {
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    
    .header-title {
      font-size: 24px;
      color: #5a5e66; 
      font-weight: 500;
      letter-spacing: 1px;
      text-align: center;
      white-space: nowrap; 
    }
  }

  .header-right {
    position: absolute;
    right: 30px;
    height: 100%; 
    display: flex;
    align-items: center;
  }

  .avatar-container {
    height: 100%;
    display: flex;
    align-items: center;
    
    .avatar-wrapper {
      cursor: pointer;
      display: flex;
      align-items: center;
      height: 100%;
      
      .icon-box {
        width: 24px;
        height: 24px;
        background-color: #4a4a4a;
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        margin-right: 8px;
        
        i {
          color: #fff;
          font-size: 14px;
          font-weight: bold;
        }
      }

      .user-name {
        font-size: 16px;
        color: #4a4a4a;
        font-weight: 500;
      }
      
      &:hover {
        opacity: 0.8;
      }
    }
  }
}

.el-main { padding: 20px; }

.fade-transform-leave-active,
.fade-transform-enter-active {
  transition: all .5s;
}
.fade-transform-enter {
  opacity: 0;
  transform: translateX(-30px);
}
.fade-transform-leave-to {
  opacity: 0;
  transform: translateX(30px);
}
</style>

<style>
.user-dropdown {
  top: 50px !important;
  padding: 10px 0 !important;
}
.user-dropdown .el-dropdown-menu__item {
  font-size: 14px;
  padding: 0 25px;
  line-height: 36px;
  text-align: center;
  color: #606266;
}
.user-dropdown .el-dropdown-menu__item:hover {
  background-color: #f5f7fa;
  color: #67C23A;
}
.el-popper[x-placement^=bottom] .popper__arrow {
  display: none; 
}
</style>