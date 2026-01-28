<template>
  <div class="login-container">
    <div class="login-box">
      <div class="title-container">
        <h2 class="main-title">基于Django+Vue的在线编程题库与代码提交评测系统</h2>
        <p class="sub-title">SMART EDUCATION PLATFORM</p>
      </div>

      <el-form :model="loginForm" :rules="rules" ref="loginForm" class="login-form">
        <el-form-item prop="username">
          <el-input 
            v-model="loginForm.username" 
            prefix-icon="el-icon-user" 
            placeholder="请输入账号"
            class="glass-input">
          </el-input>
        </el-form-item>

        <el-form-item prop="password">
          <el-input 
            v-model="loginForm.password" 
            prefix-icon="el-icon-lock" 
            type="password" 
            placeholder="请输入密码	"
            show-password
            class="glass-input"
            @keyup.enter.native="handleLogin">
          </el-input>
        </el-form-item>

        <el-button type="primary" :loading="loading" class="login-btn" @click="handleLogin">
          登 录
        </el-button>
      </el-form>
    </div>
  </div>
</template>

<script>
export default {
  name: "Login",
  data() {
    return {
      loading: false,
      loginForm: {
        username: "",
        password: ""
      },
      rules: {
        username: [{ required: true, message: "请输入用户名", trigger: "blur" }],
        password: [{ required: true, message: "请输入密码", trigger: "blur" }]
      }
    };
  },
  methods: {
    handleLogin() {
      this.$refs.loginForm.validate(async (valid) => {
        if (valid) {
          this.loading = true;
          try {
            // 调用后端登录接口
            const res = await this.$axios.post('login/', this.loginForm);
            
            // 假设后端返回结构: { token: '...', role: 1, ... }
            const role = res.data.role; 
            const token = res.data.token;
            
            // 存储 Token (实际项目中建议存 Vuex 或 Cookie)
            localStorage.setItem('token', token);
            localStorage.setItem('role', role);
            localStorage.setItem('username', this.loginForm.username);

            this.$message.success("登录成功");

            // 🔴 [核心修改] 不要用 $router.push
                      // 改用 window.location.href = '/' 进行强制刷新跳转
                      // 这能保证 Vuex 状态被重置，重新触发 router.beforeEach 中的 GenerateRoutes
            setTimeout(() => {
                window.location.href = '/'; 
            }, 500);

          } catch (error) {
            console.error(error);
            this.$message.error("登录失败，请检查账号密码");
          } finally {
            this.loading = false;
          }
        }
      });
    }
  }
};
</script>

<style lang="scss" scoped>
/* 1. 背景容器：深色星空图 */
.login-container {
  height: 100vh;
  width: 100vw;
  background: url('https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=2072&auto=format&fit=crop') no-repeat center center;
  background-size: cover;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}

/* 2. 毛玻璃卡片核心样式 */
.login-box {
  width: 400px;
  padding: 40px;
  border-radius: 15px;
  
  /* 毛玻璃特效 */
  background: rgba(255, 255, 255, 0.1); 
  backdrop-filter: blur(10px); 
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 15px 25px rgba(0, 0, 0, 0.2);
  
  text-align: center;
  color: #fff;
}

/* 3. 标题样式 */
.title-container {
  margin-bottom: 40px;
  
  .main-title {
    font-size: 24px;
    font-weight: 600;
    margin-bottom: 10px;
    letter-spacing: 2px;
    color: #ffffff;
    text-shadow: 0 2px 4px rgba(0,0,0,0.3);
  }
  
  .sub-title {
    font-size: 12px;
    color: rgba(255, 255, 255, 0.7);
    letter-spacing: 3px;
    text-transform: uppercase;
  }
}

/* 4. 深度修改 Element UI 输入框样式以匹配设计图 */
::v-deep .glass-input {
  input {
    background: transparent !important;
    border: none !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.3) !important;
    border-radius: 0 !important;
    color: #fff !important;
    padding-left: 35px;
    
    &::placeholder {
      color: rgba(255, 255, 255, 0.5);
    }
    
    &:focus {
      border-bottom-color: #409EFF !important;
    }
  }
  
  /* 图标颜色 */
  .el-input__prefix {
    color: rgba(255, 255, 255, 0.7);
    left: 0;
  }
}

/* 5. 按钮样式 */
.login-btn {
  width: 100%;
  margin-top: 20px;
  border-radius: 25px; /* 圆角按钮 */
  background: linear-gradient(90deg, #00c6ff, #0072ff); /* 渐变色 */
  border: none;
  font-weight: 600;
  letter-spacing: 2px;
  
  &:hover {
    opacity: 0.9;
    transform: translateY(-1px);
    box-shadow: 0 5px 15px rgba(0, 114, 255, 0.4);
  }
}
</style>