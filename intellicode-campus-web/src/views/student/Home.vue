<template>
  <div class="student-home">
    <div class="container-1200">
      <el-row :gutter="20">
        <el-col :span="18">
          <el-carousel trigger="click" height="300px" style="border-radius: 8px; overflow: hidden; margin-bottom: 30px; box-shadow: 0 4px 12px rgba(0,0,0,0.08);">
            <el-carousel-item v-for="item in banners" :key="item.id">
              <img :src="item.image" style="width:100%; height:100%; object-fit: cover; cursor: pointer;" @click="goLink(item.url)">
            </el-carousel-item>
          </el-carousel>
          
          <div class="section-header">
            <h3 class="section-title">🔥 热门课程</h3>
            <span class="more-link" @click="$router.push('/student/courses')">全部课程 <i class="el-icon-arrow-right"></i></span>
          </div>

          <div class="course-grid">
            <el-card 
              v-for="course in hotCourses" 
              :key="course.id" 
              shadow="hover" 
              :body-style="{ padding: '0px' }" 
              class="course-card" 
              @click.native="goCourse(course.id)"
            >
              <div class="img-box">
                <img :src="course.cover_img" class="course-img">
                <span class="course-tag" v-if="course.category">{{ course.category }}</span>
              </div>
              
              <div class="course-info">
                <div class="title" :title="course.title">{{ course.title }}</div>
                
                <div class="meta">
                  <span>共{{ 12 }}节</span>
                  <span class="dot">·</span>
                  <span>{{ course.view_count }}人学习</span>
                  <span class="dot">·</span>
                  <span>{{ course.teacher_name }}</span>
                </div>
              </div>
            </el-card>
          </div>
        </el-col>
        
        <el-col :span="6">
          <el-card shadow="never" class="user-card">
            <div class="avatar-box">
              <el-avatar :size="60" :src="userInfo && userInfo.avatar ? userInfo.avatar : 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'"></el-avatar>
              <h4>{{ (userInfo && userInfo.nickname) || '同学' }}</h4>
              <p>{{ (userInfo && userInfo.display_class_name) || '暂无班级' }}</p>
            </div>
            <div class="stats-row">
              <div class="stat-item">
                <div class="num">{{ stats.done_problems }}</div>
                <div class="label">已刷题</div>
              </div>
              <div class="stat-item">
                <div class="num">{{ stats.rank }}</div>
                <div class="label">排名</div>
              </div>
            </div>
          </el-card>
          
          <el-card shadow="never" class="notice-card" style="margin-top: 20px;">
            <div slot="header" class="clearfix">
              <span>🔔 最新公告</span>
              <el-button style="float: right; padding: 3px 0" type="text" @click="$router.push('/student/notices')">更多</el-button>
            </div>
            <ul class="notice-list">
              <li v-for="n in notices" :key="n.id" @click="goNoticeDetail(n.id)">
                <el-tag v-if="n.is_top" size="mini" type="danger" effect="dark" style="margin-right: 5px;">置顶</el-tag>
                
                <el-tag size="mini" effect="plain" :type="getDictTagType(n.type)">
                  {{ getDictLabel(n.type) }}
                </el-tag>
                
                <span class="text" :title="n.title">{{ n.title }}</span>
                <span class="date">{{ formatDate(n.created_at) }}</span>
              </li>
              <li v-if="notices.length === 0" style="color: #999; text-align: center; padding: 10px;">暂无公告</li>
            </ul>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'StudentHome',
  data() {
    return {
      banners: [],
      hotCourses: [],
      notices: [],
      // 🟢 字典数据
      noticeDicts: [],
      stats: { done_problems: 0, rank: '-' },
    }
  },
  computed: {
    ...mapState(['user']),
    userInfo() {
      return this.user || {}
    }
  },
  created() {
    this.fetchHomeData();
    // 🟢 加载字典
    this.getDicts();
  },
  methods: {
    async fetchHomeData() {
      try {
        const [resBanner, resCourse, resNotice] = await Promise.all([
          this.$axios.get('banners/'),
          this.$axios.get('courses/', { params: { ordering: '-view_count', page_size: 8 } }),
          // 获取公告，后端已按置顶排序
          this.$axios.get('notices/', { params: { page_size: 10 } }) 
        ]);

        this.banners = resBanner.data.results || resBanner.data;
        this.hotCourses = resCourse.data.results || resCourse.data;
        
        const rawNotices = resNotice.data.results || resNotice.data;
        this.notices = rawNotices ? rawNotices.slice(0, 10) : [];

      } catch (error) {
        console.error("首页数据加载失败", error);
      }
    },

    // 🟢 获取字典数据
    async getDicts() {
      try {
        const res = await this.$axios.get('dict-data/', { params: { dict_type__type: 'notice_type' } });
        this.noticeDicts = res.data.results || res.data;
      } catch (e) {
        console.error("加载字典失败", e);
      }
    },

    // 🟢 翻译字典文本
    getDictLabel(value) {
      if (!this.noticeDicts.length) return '...';
      const found = this.noticeDicts.find(item => item.value == value);
      return found ? found.label : '公告';
    },

    // 🟢 翻译字典颜色
    getDictTagType(value) {
      if (!this.noticeDicts.length) return '';
      const found = this.noticeDicts.find(item => item.value == value);
      return found && found.list_class ? found.list_class : ''; 
    },

    formatDate(dateStr) {
      if (!dateStr) return '';
      const date = new Date(dateStr);
      return `${date.getMonth() + 1}-${date.getDate()}`;
    },
    goLink(url) {
      if(url) window.open(url, '_blank');
    },
    goCourse(id) {
      this.$router.push(`/student/course/${id}`);
    },
    goNoticeDetail(id) {
      this.$router.push(`/student/notice/${id}`);
    }
  }
}
</script>

<style scoped lang="scss">
.container-1200 { width: 1200px; margin: 0 auto; padding-top: 20px;}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  .section-title { margin: 0; font-size: 20px; font-weight: 600; color: #333; }
  .more-link { cursor: pointer; color: #999; font-size: 14px; &:hover { color: #409EFF; } }
}

/* 课程网格样式 */
.course-grid { 
  display: grid; 
  grid-template-columns: repeat(4, 1fr); /* 4列 */
  gap: 16px; 
}

.course-card {
  cursor: pointer;
  transition: all 0.3s;
  border-radius: 8px;
  border: none;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  overflow: hidden;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 16px rgba(0,0,0,0.12);
  }

  .img-box {
    position: relative;
    width: 100%;
    height: 160px;
    overflow: hidden;
    background-color: #f9f9f9; 
    display: flex;
    justify-content: center;
    align-items: center;
    
    .course-img {
      width: 100%;
      height: 100%;
      object-fit: contain; 
      transition: transform 0.3s;
    }
    
    .course-tag {
      position: absolute;
      bottom: 6px;
      right: 6px;
      background: rgba(0,0,0,0.6);
      color: #fff;
      font-size: 12px;
      padding: 2px 6px;
      border-radius: 4px;
    }
  }
  
  &:hover .course-img {
    transform: scale(1.05);
  }

  .course-info {
    padding: 12px;
    
    .title {
      font-weight: 600;
      font-size: 14px;
      color: #333;
      margin-bottom: 8px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap; 
    }
    
    .meta {
      font-size: 12px;
      color: #999;
      margin-bottom: 4px; 
      display: flex;
      align-items: center;
      .dot { margin: 0 4px; }
    }
  }
}

/* 右侧边栏样式 */
.user-card .avatar-box { text-align: center; margin-bottom: 15px; }
.stats-row { display: flex; justify-content: space-around; text-align: center; border-top: 1px solid #f5f5f5; padding-top: 15px; }
.stats-row .num { font-weight: bold; font-size: 18px; color: #333; }
.stats-row .label { font-size: 12px; color: #999; margin-top: 5px; }

.notice-list { padding: 0; margin: 0; list-style: none; }
.notice-list li { 
  display: flex; 
  align-items: center; 
  margin-bottom: 12px; 
  cursor: pointer; 
  padding: 4px 0;
  border-bottom: 1px dashed #f0f0f0;
}
.notice-list li:last-child { border-bottom: none; }
.notice-list li:hover .text { color: #409EFF; }
.notice-list .text { 
  margin-left: 8px; 
  flex: 1; 
  overflow: hidden; 
  text-overflow: ellipsis; 
  white-space: nowrap; 
  font-size: 13px; 
  color: #606266;
}
.notice-list .date {
  font-size: 12px;
  color: #c0c4cc;
  margin-left: 10px;
  white-space: nowrap;
}
</style>