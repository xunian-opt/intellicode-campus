<template>
  <div class="course-detail-container">
    <div class="content-wrapper">
      <el-card shadow="never" class="course-header-card">
        <div class="header-content">
          <div class="cover-box">
            <img :src="course.cover_img" class="course-cover" alt="课程封面">
          </div>
          
          <div class="info-box">
            <h1 class="course-title">{{ course.title }}</h1>
            <div class="course-meta">
              <span class="tag"><i class="el-icon-user"></i> {{ course.teacher_name }}</span>
              <span class="tag"><i class="el-icon-folder-opened"></i> {{ course.category }}</span>
              <span class="tag"><i class="el-icon-view"></i> {{ course.view_count }} 次浏览</span>
            </div>
            <p class="course-desc">{{ course.description }}</p>
            
            <div class="action-btn-group">
              <el-button type="primary" size="medium" icon="el-icon-video-play" @click="startLearning">开始学习</el-button>
              <el-button size="medium" icon="el-icon-star-off" circle></el-button>
              <el-button size="medium" icon="el-icon-thumb" circle></el-button>
            </div>
          </div>
        </div>
      </el-card>

      <div class="course-body">
        <el-card shadow="never">
          <el-tabs v-model="activeTab">
            
            <el-tab-pane label="课程大纲" name="outline">
              <div class="markdown-body">
                <div v-if="course.outline" style="white-space: pre-wrap; line-height: 1.8;">{{ course.outline }}</div>
                <el-empty v-else description="暂无课程大纲"></el-empty>
              </div>
            </el-tab-pane>

            <el-tab-pane label="课程资源" name="resources">
              <el-table :data="resources" style="width: 100%">
                <el-table-column prop="name" label="资源名称"></el-table-column>
                <el-table-column prop="resource_type" label="类型" width="100">
                  <template slot-scope="scope">
                    <el-tag v-if="scope.row.resource_type===1">视频</el-tag>
                    <el-tag v-else-if="scope.row.resource_type===2" type="warning">课件</el-tag>
                    <el-tag v-else type="info">其他</el-tag>
                  </template>
                </el-table-column>
                <el-table-column label="操作" width="120">
                  <template slot-scope="scope">
                    <el-button type="text" icon="el-icon-download" @click="download(scope.row.file)">下载</el-button>
                  </template>
                </el-table-column>
              </el-table>
            </el-tab-pane>

            <el-tab-pane label="作业任务" name="assignments">
              <div v-if="assignments.length > 0">
                <div v-for="assign in assignments" :key="assign.id" class="assignment-item">
                  <div class="assign-header">
                    <h4>{{ assign.title }}</h4>
                    <span class="deadline">截止时间：{{ formatDate(assign.deadline) }}</span>
                  </div>
                  <p class="assign-content">{{ assign.content }}</p>
                  
                  <div class="upload-area">
                    <el-upload
                      class="upload-demo"
                      action="#"
                      :http-request="(params) => submitAssignment(params, assign.id)"
                      :show-file-list="false">
                      <el-button size="small" type="primary">提交作业 (上传文档)</el-button>
                      <span slot="tip" class="el-upload__tip" style="margin-left:10px;">支持 Word/PDF/Zip 等格式</span>
                    </el-upload>
                  </div>
                </div>
              </div>
              <el-empty v-else description="该课程暂无作业"></el-empty>
            </el-tab-pane>

          </el-tabs>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "CourseDetail",
  data() {
    return {
      courseId: null,
      course: {},
      resources: [],
      assignments: [],
      activeTab: 'outline'
    };
  },
  created() {
    this.courseId = this.$route.params.id;
    if (this.courseId) {
      this.fetchCourseDetail();
      this.fetchResources();
      this.fetchAssignments();
    }
  },
  methods: {
    async fetchCourseDetail() {
      try {
        const res = await this.$axios.get(`courses/${this.courseId}/`);
        this.course = res.data;
      } catch (error) {
        console.error(error);
        this.$message.error("获取课程详情失败");
      }
    },
    async fetchResources() {
      const res = await this.$axios.get('course_resources/', { params: { course: this.courseId } });
      this.resources = res.data.results || res.data;
    },
    async fetchAssignments() {
      const res = await this.$axios.get('assignments/', { params: { course: this.courseId } });
      this.assignments = res.data.results || res.data;
    },
    
    startLearning() {
      this.activeTab = 'resources';
      this.$message.success("已开始学习，请浏览课程资源");
    },
    download(url) {
      window.open(url, '_blank');
    },
    formatDate(dateStr) {
      if (!dateStr) return '无';
      return new Date(dateStr).toLocaleString();
    },

    async submitAssignment(params, assignmentId) {
      const formData = new FormData();
      formData.append('assignment', assignmentId);
      
      const userId = this.$store.state.user?.id; 
      if(userId) formData.append('student', userId);

      formData.append('file', params.file);

      try {
        await this.$axios.post('submissions/', formData);
        this.$message.success("作业提交成功！");
      } catch (error) {
        console.error(error);
        this.$message.error("提交失败，请重试");
      }
    }
  }
};
</script>

<style lang="scss" scoped>
.course-detail-container {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: calc(100vh - 60px);
}

.content-wrapper {
  width: 1200px;
  margin: 0 auto;
}

.course-header-card {
  margin-bottom: 20px;
  .header-content {
    display: flex;
    gap: 30px;
    
    /* 🟢 [CSS修改] 图片容器样式调整 */
    .cover-box {
      width: 400px;
      height: 250px;
      border-radius: 8px;
      overflow: hidden;
      flex-shrink: 0;
      background-color: #f9f9f9; /* 增加背景色，避免图片留白时太突兀 */
      border: 1px solid #eee;
      display: flex;
      justify-content: center;
      align-items: center;

      .course-cover {
        width: 100%;
        height: 100%;
        object-fit: contain; /* 关键：完整展示图片，不裁切 */
      }
    }
    
    .info-box {
      flex: 1;
      display: flex;
      flex-direction: column;
      
      .course-title {
        font-size: 24px;
        margin: 0 0 15px 0;
        color: #333;
      }
      
      .course-meta {
        margin-bottom: 15px;
        .tag {
          margin-right: 20px;
          color: #666;
          font-size: 14px;
          i { margin-right: 5px; color: #409EFF; }
        }
      }
      
      .course-desc {
        color: #666;
        font-size: 14px;
        line-height: 1.6;
        flex: 1; 
        display: -webkit-box;
        -webkit-line-clamp: 4;
        -webkit-box-orient: vertical;
        overflow: hidden;
      }
      
      .action-btn-group {
        margin-top: 20px;
      }
    }
  }
}

.assignment-item {
  border-bottom: 1px solid #ebeef5;
  padding: 20px 0;
  &:last-child { border-bottom: none; }
  
  .assign-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
    h4 { margin: 0; font-size: 16px; font-weight: 600; }
    .deadline { color: #f56c6c; font-size: 13px; }
  }
  .assign-content {
    color: #606266;
    font-size: 14px;
    margin-bottom: 15px;
  }
}
</style>