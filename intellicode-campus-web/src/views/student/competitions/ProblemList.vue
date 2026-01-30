<template>
  <div class="problem-list-container">
    <div class="main-content">
      <div class="hero-section">
        <div class="hero-text">
          <h2>💻 编程题库</h2>
          <p>精选算法与数据结构题目，提升编程核心能力</p>
        </div>
        <img src="https://assets.leetcode.cn/aliyun-lc-upload/users/leetcode/images/59e5f530-36e2-43d1-9311-536442655078_1669694660.7029421.png" class="hero-img">
      </div>

      <el-card shadow="never" class="list-card">
        <div class="filter-bar">
          <el-select v-model="query.difficulty" placeholder="难度" size="small" clearable @change="fetchData" style="width: 120px; margin-right: 10px;">
            <el-option label="简单" value="Easy" style="color: #67C23A"></el-option>
            <el-option label="中等" value="Medium" style="color: #E6A23C"></el-option>
            <el-option label="困难" value="Hard" style="color: #F56C6C"></el-option>
          </el-select>
          <el-input v-model="query.search" placeholder="搜索题目..." size="small" prefix-icon="el-icon-search" @keyup.enter.native="fetchData" style="width: 240px;"></el-input>
        </div>

        <el-table :data="tableData" v-loading="loading" :header-cell-style="{background:'#f7f8fa', color:'#909399', fontWeight:'500'}" @row-click="goDetail" style="cursor: pointer;">
          
          <el-table-column label="状态" width="60" align="center">
            <template slot-scope="scope">
              <i v-if="scope.row.user_status === 'AC'" class="el-icon-check" style="color: #67C23A; font-weight: bold;"></i>
              <i v-else-if="scope.row.user_status === 'Attempted'" class="el-icon-minus" style="color: #E6A23C;"></i>
              <span v-else></span>
            </template>
          </el-table-column>

          <el-table-column prop="title" label="题目名称" min-width="200">
            <template slot-scope="scope">
              <span class="problem-title">{{ scope.row.title }}</span>
            </template>
          </el-table-column>

          <el-table-column prop="acceptance_rate" label="通过率" width="120" align="center"></el-table-column>

          <el-table-column prop="difficulty" label="难度" width="100" align="center">
            <template slot-scope="scope">
              <span :class="'diff-' + scope.row.difficulty">{{ getDiffLabel(scope.row.difficulty) }}</span>
            </template>
          </el-table-column>
        </el-table>

        </el-card>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StudentProblemList',
  data() {
    return {
      tableData: [],
      loading: false,
      query: {
        difficulty: '',
        search: ''
      }
    }
  },
  created() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      this.loading = true;
      try {
        const res = await this.$axios.get('problems/', { 
          params: { 
            difficulty: this.query.difficulty, 
            search: this.query.search 
          } 
        });
        // 兼容处理：如果是分页结构取 .results，否则取 .data
        this.tableData = res.data.results || res.data;
      } finally {
        this.loading = false;
      }
    },
    getDiffLabel(val) {
      const map = { 'Easy': '简单', 'Medium': '中等', 'Hard': '困难' };
      return map[val] || val;
    },
    goDetail(row) {
      this.$router.push(`/student/problem/${row.id}`);
    }
  }
}
</script>

<style scoped lang="scss">
.problem-list-container {
  background-color: #f7f8fa;
  min-height: 100vh;
  padding-bottom: 40px;
}

.main-content {
  width: 1200px;
  margin: 0 auto;
  padding-top: 20px;
}

.hero-section {
  background: white;
  border-radius: 8px;
  padding: 30px 40px;
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 12px rgba(0,0,0,0.05);

  .hero-text h2 { margin: 0 0 10px 0; font-size: 24px; color: #262626; }
  .hero-text p { color: #909399; margin: 0; }
  .hero-img { height: 80px; object-fit: contain; }
}

.list-card {
  border-radius: 8px;
  border: none;
  box-shadow: 0 2px 12px rgba(0,0,0,0.05);
}

.filter-bar {
  display: flex;
  margin-bottom: 20px;
}

.problem-title {
  color: #262626;
  font-weight: 500;
  &:hover { color: #409EFF; text-decoration: underline; }
}

.diff-Easy { color: #00AF9B; }
.diff-Medium { color: #FFB800; }
.diff-Hard { color: #FF2D55; }
</style>