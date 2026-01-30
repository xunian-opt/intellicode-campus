<template>
  <div class="student-layout">
    <div class="navbar">
      <div class="nav-content">
        <div class="logo">
          <i class="el-icon-school"></i> IntelliCode Campus
        </div>
        
        <div class="nav-links">
          <router-link to="/student/home" active-class="active">首页</router-link>
          <router-link to="/student/courses" active-class="active">课程中心</router-link>
          
          <router-link to="/student/problems" active-class="active">编程题库</router-link>
          
          <router-link to="/student/competitions" active-class="active">竞赛活动</router-link>
          
          <router-link to="/student/community" active-class="active">社区讨论</router-link>
        </div>

        <div class="right-menu">
          <el-tooltip content="AI 编程助手" placement="bottom">
            <i class="el-icon-cpu ai-icon" @click="showAI = true"></i>
          </el-tooltip>
          <el-badge :value="unreadCount" :max="99" class="msg-badge">
            <i class="el-icon-bell nav-icon" @click="$router.push('/student/messages')"></i>
          </el-badge>
          <el-dropdown trigger="click" @command="handleCommand">
            <div class="avatar-wrapper">
              <el-avatar :size="32" :src="userInfo && userInfo.avatar ? userInfo.avatar : defaultAvatar"></el-avatar>
              <span class="username">{{ userInfo ? userInfo.nickname : '同学' }}</span>
            </div>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item command="profile">个人中心</el-dropdown-item>
              <el-dropdown-item command="wrongbook">我的错题本</el-dropdown-item>
              <el-dropdown-item command="records">考试记录</el-dropdown-item>
              <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </div>
      </div>
    </div>

    <div class="main-content">
      <router-view />
    </div>

    <el-dialog title="AI 编程助手" :visible.sync="showAI" width="400px" custom-class="ai-dialog" :append-to-body="true">
      <div style="text-align:center; padding: 20px;">
        <i class="el-icon-chat-dot-round" style="font-size: 40px; color: #409EFF;"></i>
        <p>AI 助手功能开发中...</p>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { mapState } from 'vuex';

export default {
  name: 'StudentLayout',
  data() {
    return {
      showAI: false,
      unreadCount: 0,
      defaultAvatar: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'
    }
  },
  computed: {
    ...mapState(['user']),
    
    userInfo() {
      return this.user || {};
    }
  },
  created() {
    this.$store.dispatch('GetUserInfo');
  },
  
  methods: {
    handleCommand(cmd) {
      if (cmd === 'logout') {
        this.$confirm('确定注销并退出系统吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          localStorage.clear();
          sessionStorage.clear();
          this.$router.push('/login');
          location.reload(); 
        }).catch(() => {
        });
      } else if (cmd === 'profile') {
        this.$router.push('/student/profile');
      } else if (cmd === 'wrongbook') {
        this.$router.push('/student/wrong-book');
      } else if (cmd === 'records') {
        this.$router.push('/student/exam-records');
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.navbar {
  height: 60px;
  background: #fff;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  position: fixed;
  top: 0;
  width: 100%;
  z-index: 1000;
  
  .nav-content {
    max-width: 1200px;
    margin: 0 auto;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 20px;
    
    .logo {
      font-size: 20px;
      font-weight: bold;
      color: #333;
      cursor: pointer;
      display: flex;
      align-items: center;
      i { color: #409EFF; margin-right: 8px; font-size: 24px; }
    }
    
    /* 导航链接样式 */
    .nav-links {
      display: flex;
      gap: 30px;
      a {
        text-decoration: none;
        color: #666;
        font-size: 16px;
        transition: color 0.3s;
        /* 悬停或激活时的样式 */
        &.active, &:hover { color: #409EFF; font-weight: 500; }
        /* Vue Router 自动激活样式 */
        &.router-link-active { color: #409EFF; font-weight: 500; border-bottom: 2px solid #409EFF; padding-bottom: 18px; }
      }
    }
    
    .right-menu {
      display: flex;
      align-items: center;
      gap: 20px;
      
      .nav-icon { font-size: 20px; cursor: pointer; color: #666; &:hover { color: #409EFF; } }
      .ai-icon { font-size: 22px; cursor: pointer; color: #67C23A; &:hover { opacity: 0.8; } }
      
      .avatar-wrapper {
        display: flex;
        align-items: center;
        cursor: pointer;
        .username { margin-left: 8px; font-size: 14px; color: #333; font-weight: 500; }
      }
    }
  }
}

.main-content {
  margin-top: 60px; /* 避开 navbar */
  min-height: calc(100vh - 60px);
  background-color: #f7f8fa; /* 浅灰背景，护眼 */
  padding: 20px;
}
</style>