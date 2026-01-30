<template>
  <div class="competition-home">
    <div class="container-1200">
      
      <div class="comp-banner">
        <div class="banner-content">
          <h1>🏆 编程竞赛</h1>
          <p>Challenge yourself, compete with peers!</p>
        </div>
        <i class="el-icon-trophy" style="font-size: 100px; color: #FFD700; opacity: 0.9;"></i>
      </div>

      <div class="section-box">
        <h3 class="section-title">🔥 热门赛事</h3>
        
        <el-row :gutter="24"> <el-col :span="12" v-for="(comp, index) in activeCompetitions" :key="comp.id" style="margin-bottom: 20px;">
            <div class="comp-card large-card" @click="enterCompetition(comp)">
              <div class="card-bg" :style="getCardBgStyle(comp, index)"></div>
              <div class="card-mask"></div>

              <div class="card-content">
                <div class="top-row">
                  <span class="status-badge" :class="getStatusClass(comp)">
                    <i class="el-icon-timer"></i> {{ getStatusText(comp) }}
                  </span>
                  <span v-if="!hasStarted(comp)" class="countdown">
                    <i class="el-icon-alarm-clock"></i> 距开始: {{ getCountdown(comp.start_time) }}
                  </span>
                </div>

                <div class="main-info">
                  <h2 class="comp-title">{{ comp.title }}</h2>
                  <div class="comp-time">
                    {{ formatTime(comp.start_time) }} ({{ getDuration(comp) }})
                  </div>
                </div>

                <div class="action-btn-wrapper">
                  <el-button 
                    v-if="!comp.is_enrolled" 
                    type="warning" 
                    round 
                    @click.stop="handleEnroll(comp)"
                    class="glass-btn"
                  >立即报名</el-button>
                  <el-button 
                    v-else 
                    type="primary" 
                    round 
                    class="glass-btn primary"
                  >进入比赛</el-button>
                </div>
              </div>
            </div>
          </el-col>
          
          <el-col :span="24" v-if="activeCompetitions.length === 0">
            <div class="empty-state">暂无正在进行的赛事</div>
          </el-col>
        </el-row>
      </div>

      <div class="section-box history-section">
        <div class="tab-header">
          <div class="tab-item" :class="{active: activeTab==='past'}" @click="switchTab('past')">往届竞赛</div>
          <div class="tab-item" :class="{active: activeTab==='my'}" @click="switchTab('my')">我的竞赛</div>
          
          <div class="tab-indicator" :style="{ left: activeTab==='past' ? '0' : '110px' }"></div>
        </div>

        <el-card shadow="never" class="history-list" v-loading="loading">
          <div v-for="comp in displayList" :key="comp.id" class="history-item">
            <div class="cover">
              <img v-if="comp.cover_img" :src="comp.cover_img" class="thumb-img">
              <div v-else class="thumb-placeholder"><i class="el-icon-data-board"></i></div>
            </div>
            <div class="info">
              <div class="title">{{ comp.title }}</div>
              <div class="time">{{ formatTime(comp.start_time) }}</div>
            </div>
            <div class="action">
              <el-tag v-if="activeTab==='my'" size="small" type="success" style="margin-right:10px;">已报名</el-tag>
              <el-button size="small" plain round @click="enterCompetition(comp)">
                {{ activeTab==='my' ? '查看详情' : '虚拟参赛' }}
              </el-button>
            </div>
          </div>
          <div v-if="displayList.length === 0" class="empty-text">暂无数据</div>
        </el-card>
      </div>

    </div>
  </div>
</template>

<script>
export default {
  name: 'StudentCompetitionList',
  data() {
    return {
      activeCompetitions: [], // 进行中/未开始
      pastCompetitions: [],   // 往届
      myCompetitions: [],     // 我的
      activeTab: 'past',      // 当前Tab
      loading: false
    }
  },
  computed: {
    displayList() {
      return this.activeTab === 'past' ? this.pastCompetitions : this.myCompetitions;
    }
  },
  created() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      this.loading = true;
      try {
        const res = await this.$axios.get('competitions/');
        const all = res.data.results || res.data;
        const now = new Date();
        
        // 分类
        this.activeCompetitions = all.filter(c => new Date(c.end_time) > now);
        this.pastCompetitions = all.filter(c => new Date(c.end_time) <= now);
      } finally {
        this.loading = false;
      }
    },
    
    // 切换 Tab 时加载“我的竞赛”
    async switchTab(tab) {
      this.activeTab = tab;
      if (tab === 'my' && this.myCompetitions.length === 0) {
        this.loading = true;
        try {
          const res = await this.$axios.get('competitions/my_competitions/');
          this.myCompetitions = res.data.results || res.data;
        } finally {
          this.loading = false;
        }
      }
    },

    async handleEnroll(comp) {
      try {
        await this.$axios.post('enrollments/', {
          competition: comp.id,
          student: this.$store.state.user.id,
          status: 1 
        });
        this.$message.success("报名成功！");
        this.fetchData(); // 刷新
      } catch(e) {
        this.$message.error("报名失败");
      }
    },
    enterCompetition(comp) {
      this.$message.success(`进入竞赛: ${comp.title}`);
    },
    
    // 样式与辅助函数
    getCardBgStyle(comp, index) {
      if (comp.cover_img) {
        return { backgroundImage: `url(${comp.cover_img})` };
      }
      const gradients = [
        'linear-gradient(135deg, #FF9D00 0%, #FFC107 100%)',
        'linear-gradient(135deg, #6236FF 0%, #8B5CF6 100%)', 
        'linear-gradient(135deg, #2D79FF 0%, #4D94FF 100%)'
      ];
      return { background: gradients[index % gradients.length] };
    },
    hasStarted(comp) { return new Date() >= new Date(comp.start_time); },
    getStatusText(comp) {
      const now = new Date();
      if (now < new Date(comp.start_time)) return '未开始';
      if (now > new Date(comp.end_time)) return '已结束';
      return '进行中';
    },
    getStatusClass(comp) {
      return this.getStatusText(comp) === '进行中' ? 'live' : 'pending';
    },
    formatTime(time) {
      if(!time) return '';
      const date = new Date(time);
      return `${date.getMonth()+1}月${date.getDate()}日 ${date.getHours()}:${date.getMinutes().toString().padStart(2, '0')}`;
    },
    getDuration(comp) {
      const ms = new Date(comp.end_time) - new Date(comp.start_time);
      const hours = (ms / (1000 * 60 * 60)).toFixed(1);
      return `${hours}小时`;
    },
    getCountdown(startTime) {
      const diff = new Date(startTime) - new Date();
      if(diff < 0) return '';
      const days = Math.floor(diff / (1000 * 60 * 60 * 24));
      const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      return `${days}天 ${hours}时`;
    }
  }
}
</script>

<style scoped lang="scss">
.competition-home {
  background-color: #1a1a1a;
  min-height: calc(100vh - 60px);
  color: #fff;
  padding-bottom: 60px;
}

.container-1200 { width: 1200px; margin: 0 auto; }

.comp-banner {
  text-align: center;
  padding: 50px 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 30px;
  h1 { font-size: 32px; margin-bottom: 10px; font-weight: 600; color: #fff; }
  p { color: #bbb; margin: 0; }
}

.section-box {
  margin-bottom: 50px;
  .section-title { font-size: 20px; margin-bottom: 25px; font-weight: 500; color: #eee; }
}

/* 🟢 卡片样式 (仿 LeetCode) */
.comp-card {
  height: 240px; /* 增加高度，避免挤压 */
  border-radius: 20px;
  position: relative;
  overflow: hidden;
  cursor: pointer;
  box-shadow: 0 10px 30px rgba(0,0,0,0.3);
  transition: transform 0.3s;
  
  &:hover { transform: translateY(-5px); }

  .card-bg {
    position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    background-size: cover; background-position: center;
    transition: transform 0.5s;
  }
  &:hover .card-bg { transform: scale(1.05); }

  .card-mask {
    position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    background: linear-gradient(to bottom, rgba(0,0,0,0.2) 0%, rgba(0,0,0,0.7) 100%);
  }

  .card-content {
    position: relative; z-index: 2; padding: 25px;
    height: 100%; display: flex; flex-direction: column;
    
    .top-row {
      display: flex; justify-content: space-between; align-items: center;
      .status-badge {
        padding: 6px 12px; border-radius: 8px; font-size: 12px; font-weight: 600;
        background: rgba(255,255,255,0.2); backdrop-filter: blur(8px);
        &.live { background: #F56C6C; }
      }
      .countdown { font-size: 13px; font-weight: bold; text-shadow: 0 1px 2px rgba(0,0,0,0.5); }
    }

    .main-info {
      margin-top: auto; margin-bottom: 20px; /* 留出底部按钮空间 */
      .comp-title { font-size: 26px; font-weight: bold; margin-bottom: 8px; line-height: 1.3; }
      .comp-time { font-size: 14px; opacity: 0.9; }
    }

    /* 按钮绝对定位到右下角 */
    .action-btn-wrapper {
      position: absolute; bottom: 25px; right: 25px;
      
      .glass-btn {
        border: none; font-weight: bold; padding: 10px 24px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        &.primary { background: rgba(255,255,255,0.9); color: #333; &:hover{background:#fff;} }
      }
    }
  }
}

.empty-state { height: 150px; background: #252526; border-radius: 12px; display: flex; align-items: center; justify-content: center; color: #666; }

/* 🟢 Tab 切换样式 */
.history-section {
  .tab-header {
    display: flex; position: relative; margin-bottom: 20px;
    border-bottom: 1px solid #333; padding-bottom: 10px;
    
    .tab-item {
      font-size: 16px; color: #999; cursor: pointer; margin-right: 40px; padding-bottom: 5px; transition: color 0.3s;
      &.active { color: #fff; font-weight: bold; }
      &:hover { color: #ccc; }
    }
    .tab-indicator {
      position: absolute; bottom: -1px; width: 64px; height: 3px; background: #409EFF; border-radius: 2px; transition: left 0.3s;
    }
  }
}

.history-list {
  background: #252526; border: none; border-radius: 12px;
  .history-item {
    display: flex; align-items: center; padding: 15px 0; border-bottom: 1px solid #333;
    &:last-child { border-bottom: none; }
    
    .cover {
      width: 100px; height: 56px; border-radius: 6px; overflow: hidden; background: #333;
      display: flex; align-items: center; justify-content: center;
      .thumb-img { width: 100%; height: 100%; object-fit: cover; }
      i { font-size: 24px; color: #555; }
    }
    .info { flex: 1; margin-left: 20px; color: #fff; 
      .title { font-size: 16px; margin-bottom: 5px; }
      .time { color: #888; font-size: 12px; }
    }
  }
  .empty-text { text-align: center; padding: 30px; color: #666; }
}
</style>