<template>
  <div class="student-course-list" style="width: 1200px; margin: 0 auto; padding: 20px;">
    <el-card shadow="never">
      <div slot="header" class="clearfix">
        <span style="font-size: 18px; font-weight: bold; line-height: 32px;">全部课程</span>
        
        <div style="float: right; width: 350px;">
          <el-input 
            placeholder="请输入课程名称 / 授课教师" 
            v-model="search" 
            size="small" 
            clearable 
            @clear="handleSearch"
            @keyup.enter.native="handleSearch">
            <el-button slot="append" icon="el-icon-search" @click="handleSearch"></el-button>
          </el-input>
        </div>
      </div>

      <el-row :gutter="20" v-loading="loading">
        <el-empty v-if="courseList.length === 0" description="未找到相关课程"></el-empty>

        <el-col :span="6" v-for="item in courseList" :key="item.id" style="margin-bottom: 20px;">
          <el-card :body-style="{ padding: '0px' }" shadow="hover" @click.native="$router.push(`/student/course/${item.id}`)" style="cursor: pointer; border-radius: 8px; overflow: hidden;">
            
            <div style="height: 160px; background: #f9f9f9; display: flex; align-items: center; justify-content: center; overflow: hidden;">
                <img :src="item.cover_img" style="width: 100%; height: 100%; object-fit: contain;">
            </div>

            <div style="padding: 14px;">
              <div style="font-weight: bold; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; margin-bottom: 8px;">{{ item.title }}</div>
              
              <div style="color: #999; font-size: 12px; display: flex; justify-content: space-between; align-items: center;">
                <span><i class="el-icon-user"></i> {{ item.teacher_name || '讲师' }}</span>
                <span><i class="el-icon-view"></i> {{ item.view_count }}</span>
              </div>
              
              <div style="margin-top: 10px; display: flex; justify-content: space-between; align-items: center;">
                 <el-tag size="mini" type="info" effect="plain">{{ item.category }}</el-tag>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script>
export default {
  name: "StudentCourseList",
  data() {
    return { 
      courseList: [],
      search: '', // 🟢 搜索关键词
      loading: false
    }
  },
  created() {
    this.getCourseList();
  },
  methods: {
    // 获取课程列表
    async getCourseList() {
      this.loading = true;
      try {
        // 🟢 [核心] 将 search 参数传递给后端
        // 后端配置了 search_fields = ['title', 'teacher__nickname']，会自动处理模糊搜索
        const res = await this.$axios.get('courses/', { 
          params: { 
            search: this.search,
            ordering: '-created_at' // 默认按创建时间倒序
          } 
        });
        this.courseList = res.data.results || res.data;
      } catch (e) {
        console.error(e);
        this.$message.error("获取课程列表失败");
      } finally {
        this.loading = false;
      }
    },
    
    // 🟢 搜索事件
    handleSearch() {
      this.getCourseList();
    }
  }
}
</script>

<style scoped>
/* 修复浮动塌陷 */
.clearfix:before,
.clearfix:after {
  display: table;
  content: "";
}
.clearfix:after {
  clear: both
}
</style>