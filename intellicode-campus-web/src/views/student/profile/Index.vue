<template>
  <div class="profile-page" style="width: 1200px; margin: 0 auto; padding: 20px;">
    <el-card shadow="never" style="min-height: 600px;">
      <el-tabs tab-position="left" style="height: 100%;">
        
        <el-tab-pane label="基本资料">
          <div style="padding-left: 40px; padding-top: 20px;">
            <h3 style="margin-bottom: 30px;">个人信息</h3>
            
            <el-form label-width="80px" style="max-width: 500px;">
              <el-form-item label="头像">
                <el-upload
                  class="avatar-uploader"
                  action="" 
                  :show-file-list="false"
                  :http-request="uploadAvatar"
                  :before-upload="beforeAvatarUpload">
                  
                  <el-avatar 
                    v-if="form.avatar" 
                    :size="80" 
                    :src="form.avatar">
                  </el-avatar>
                  <i v-else class="el-icon-plus avatar-uploader-icon"></i>
                  
                  <div class="el-upload__tip" slot="tip">点击头像可进行修改</div>
                </el-upload>
              </el-form-item>

              <el-form-item label="账号">
                <el-input v-model="form.username" disabled></el-input>
              </el-form-item>
              
              <el-form-item label="姓名">
                <el-input v-model="form.nickname" disabled placeholder="暂无姓名"></el-input>
              </el-form-item>
              
              <el-form-item label="手机号">
                <el-input v-model="form.phone" disabled placeholder="暂无手机号"></el-input>
              </el-form-item>

              <el-form-item label="班级">
                <el-input v-model="form.display_class_name" disabled placeholder="暂无班级"></el-input>
              </el-form-item>
            </el-form>
          </div>
        </el-tab-pane>
        
        <el-tab-pane label="我的错题本">
          <el-empty description="错题本功能即将上线"></el-empty>
        </el-tab-pane>
        
        <el-tab-pane label="考试记录">
          <el-empty description="暂无考试记录"></el-empty>
        </el-tab-pane>

      </el-tabs>
    </el-card>
  </div>
</template>

<script>
export default {
  name: "StudentProfile",
  data() {
    return {
      // 🟢 [核心修复] 初始化 form 对象，防止 undefined 报错
      form: {
        id: null,
        username: '',
        nickname: '',
        avatar: '',
        phone: '',
        display_class_name: ''
      }
    };
  },
  created() {
    this.fetchUserInfo();
  },
  methods: {
    // 获取当前用户信息
    async fetchUserInfo() {
          try {
            // 直接调用后端新增的 info 接口，后端会根据 Token 识别是谁
            const res = await this.$axios.get('users/info/');
            
            // 赋值给表单
            this.form = res.data;
            
            // 如果后端返回了完整的图片路径(带http)，则直接使用；否则可能需要拼接
            // (通常 Django ImageField 返回的是相对路径或完整路径，视配置而定)
            
          } catch (error) {
            console.error("获取用户信息失败", error);
            this.$message.error("获取用户信息失败，请检查登录状态");
          }
        },
    
        // 自定义上传头像
        async uploadAvatar(param) {
          // 这里 form.id 绝对不会为空了，因为 fetchUserInfo 是根据 Token 拿到的 ID
          if (!this.form.id) {
            this.$message.warning("正在加载用户信息，请稍候...");
            return;
          }
    
          const formData = new FormData();
          formData.append('avatar', param.file);
    
          try {
            // 调用后端 PATCH 接口更新头像
            const res = await this.$axios.patch(`users/${this.form.id}/`, formData);
            this.$message.success('头像修改成功');
			
            // 更新页面显示
            this.form.avatar = res.data.avatar;
	// 🟢 [新增] 核心代码：通知 Vuex 更新全局头像
	        // 这样顶部导航栏就会立刻变过来
	        this.$store.commit('SET_AVATAR', res.data.avatar);
			
          } catch (error) {
            console.error(error);
            this.$message.error('头像上传失败');
          }
        },

    // 上传前校验
        beforeAvatarUpload(file) {
          const isJPGOrPNG = file.type === 'image/jpeg' || file.type === 'image/png';
          const isLt2M = file.size / 1024 / 1024 < 2;
    
          if (!isJPGOrPNG) {
            this.$message.error('上传头像图片只能是 JPG/PNG 格式!');
          }
          if (!isLt2M) {
            this.$message.error('上传头像图片大小不能超过 2MB!');
          }
          return isJPGOrPNG && isLt2M;
        },
    
    // 占位方法，防止报错（虽然上面用了 http-request 覆盖了 success 回调，但保留以防万一）
    refreshUser() {
      this.fetchUserInfo();
    }
  }
};
</script>

<style scoped>
.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}
.avatar-uploader .el-upload:hover {
  border-color: #409EFF;
}
.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 80px;
  height: 80px;
  line-height: 80px;
  text-align: center;
  border: 1px dashed #d9d9d9;
  border-radius: 4px;
}
.el-upload__tip {
  margin-top: 10px;
  color: #909399;
}
</style>