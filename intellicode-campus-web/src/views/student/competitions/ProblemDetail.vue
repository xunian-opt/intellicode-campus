<template>
  <div class="ide-container">
    <div class="ide-header">
      <div class="left">
        <el-button type="text" icon="el-icon-arrow-left" @click="$router.go(-1)">题库</el-button>
        <span class="divider">|</span>
        <span class="title">{{ problem.title }}</span>
      </div>
      <div class="right">
        <el-button size="small" type="primary" :loading="submitting" @click="submitCode" icon="el-icon-video-play">提交运行</el-button>
      </div>
    </div>

    <div class="ide-body">
      <div class="pane left-pane">
        <el-tabs v-model="activeTab" class="desc-tabs">
          <el-tab-pane label="题目描述" name="desc">
            <div class="problem-content" v-loading="loading">
              <div class="meta-row">
                <span class="difficulty-tag" :class="problem.difficulty">{{ getDiffLabel(problem.difficulty) }}</span>
                <span class="limit">时间限制: {{ problem.time_limit }}ms</span>
                <span class="limit">内存限制: {{ problem.memory_limit }}MB</span>
              </div>
              <div class="markdown-body" style="white-space: pre-wrap; line-height: 1.8; font-size: 15px;">
                {{ problem.content }}
              </div>
            </div>
          </el-tab-pane>
          <el-tab-pane label="提交记录" name="records">
            <el-table :data="records" size="small">
              <el-table-column prop="submit_time" label="时间" width="160"></el-table-column>
              <el-table-column prop="result" label="结果">
                <template slot-scope="scope">
                  <span :style="{color: getResultColor(scope.row.result)}">{{ scope.row.result }}</span>
                </template>
              </el-table-column>
            </el-table>
          </el-tab-pane>
        </el-tabs>
      </div>

      <div class="pane right-pane">
        <div class="editor-toolbar">
          <el-select v-model="language" size="mini" style="width: 100px;">
            <el-option value="Python" label="Python"></el-option>
            <el-option value="Java" label="Java" disabled></el-option>
            <el-option value="C++" label="C++" disabled></el-option>
          </el-select>
          <el-button type="text" icon="el-icon-refresh-left" size="mini" @click="resetCode">重置代码</el-button>
        </div>
        
        <div class="editor-wrapper">
          <textarea 
            class="code-textarea" 
            v-model="code" 
            spellcheck="false"
            @keydown.tab.prevent="insertTab"
          ></textarea>
        </div>

        <div class="console-box" :class="{ 'expanded': consoleOpen }">
          <div class="console-header" @click="consoleOpen = !consoleOpen">
            <span><i class="el-icon-s-order"></i> 执行结果</span>
            <i :class="consoleOpen ? 'el-icon-arrow-down' : 'el-icon-arrow-up'"></i>
          </div>
          <div class="console-body" v-if="consoleOpen">
            <div v-if="lastResult" class="result-display">
              <div class="status" :class="lastResult.result === 'AC' ? 'success' : 'error'">
                {{ getResultText(lastResult.result) }}
              </div>
              <div v-if="lastResult.result !== 'AC' && lastResult.result !== 'Pending'" class="error-msg">
                可能的原因：逻辑错误、边界条件未处理或语法错误。
              </div>
            </div>
            <div v-else class="placeholder">
              点击“提交运行”查看结果
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProblemDetail',
  data() {
    return {
      problem: {},
      loading: false,
      submitting: false,
      activeTab: 'desc',
      language: 'Python',
      code: '',
      records: [],
      consoleOpen: true,
      lastResult: null
    }
  },
  created() {
    this.fetchProblem();
    this.fetchRecords();
    // 默认代码模板
    this.code = "class Solution:\n    def solve(self, a, b):\n        # 在这里编写你的代码\n        pass";
  },
  methods: {
    async fetchProblem() {
      this.loading = true;
      try {
        const res = await this.$axios.get(`problems/${this.$route.params.id}/`);
        this.problem = res.data;
      } finally {
        this.loading = false;
      }
    },
    async fetchRecords() {
      // 获取当前用户对该题的提交记录
      const res = await this.$axios.get('judge_records/', {
        params: { problem: this.$route.params.id, student: this.$store.state.user.id }
      });
      this.records = (res.data.results || res.data).map(r => ({
        ...r, 
        submit_time: new Date(r.submit_time).toLocaleString()
      }));
    },
    async submitCode() {
      if (!this.code.trim()) return;
      this.submitting = true;
      this.consoleOpen = true;
      
      try {
        const payload = {
          problem: this.problem.id,
          student: this.$store.state.user.id,
          code: this.code,
          result: 'Pending' // 后端判题逻辑接入前，先标记为 Pending
        };
        // 模拟提交 (真实环境这里会触发判题机)
        const res = await this.$axios.post('judge_records/', payload);
        this.lastResult = res.data;
        
        // 模拟一个判题延迟效果（实际应轮询后端状态）
        setTimeout(() => {
           // 这里仅作前端演示，实际应由后端返回 AC/WA
           this.lastResult.result = 'AC'; // 假定通过
           this.fetchRecords();
           this.submitting = false;
           this.$message.success("执行完成");
        }, 1500);

      } catch (e) {
        this.$message.error("提交失败");
        this.submitting = false;
      }
    },
    insertTab(e) {
      // 简单的 Tab 键支持
      const target = e.target;
      const start = target.selectionStart;
      const end = target.selectionEnd;
      this.code = this.code.substring(0, start) + "    " + this.code.substring(end);
      this.$nextTick(() => {
        target.selectionStart = target.selectionEnd = start + 4;
      });
    },
    resetCode() {
      this.code = "class Solution:\n    def solve(self):\n        pass";
    },
    getDiffLabel(val) {
      const map = { 'Easy': '简单', 'Medium': '中等', 'Hard': '困难' };
      return map[val] || val;
    },
    getResultColor(res) {
      if (res === 'AC') return '#67C23A';
      if (res === 'Pending') return '#909399';
      return '#F56C6C';
    },
    getResultText(res) {
      const map = { 'AC': '通过', 'WA': '答案错误', 'TLE': '超时', 'RE': '运行错误', 'Pending': '执行中...' };
      return map[res] || res;
    }
  }
}
</script>

<style scoped lang="scss">
.ide-container {
  height: calc(100vh - 60px); /* 减去顶部导航栏高度 */
  display: flex;
  flex-direction: column;
  background-color: #fff;
  position: absolute; /* 全屏覆盖 */
  top: 0; left: 0; right: 0; bottom: 0;
  z-index: 2000; /* 覆盖原有布局 */
}

.ide-header {
  height: 50px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  background: #fff;
  
  .left {
    display: flex;
    align-items: center;
    .divider { margin: 0 10px; color: #ddd; }
    .title { font-weight: 600; font-size: 16px; }
  }
}

.ide-body {
  flex: 1;
  display: flex;
  overflow: hidden;
  
  .pane {
    height: 100%;
    overflow-y: auto;
  }
  
  .left-pane {
    width: 45%;
    border-right: 1px solid #eee;
    padding: 0 20px;
    
    .problem-content {
      padding-bottom: 40px;
      .meta-row { margin-bottom: 20px; display: flex; gap: 15px; font-size: 12px; color: #999; align-items: center;}
      .difficulty-tag { 
        padding: 2px 8px; border-radius: 12px; color: #fff; font-size: 12px;
        &.Easy { background: #00AF9B; }
        &.Medium { background: #FFB800; }
        &.Hard { background: #FF2D55; }
      }
    }
  }
  
  .right-pane {
    flex: 1;
    display: flex;
    flex-direction: column;
    background: #1e1e1e; /* 黑色编辑器背景 */
    
    .editor-toolbar {
      height: 40px;
      border-bottom: 1px solid #333;
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 0 15px;
      background: #252526;
    }
    
    .editor-wrapper {
      flex: 1;
      position: relative;
      
      .code-textarea {
        width: 100%;
        height: 100%;
        background: #1e1e1e;
        color: #d4d4d4;
        border: none;
        resize: none;
        padding: 15px;
        font-family: 'Consolas', 'Monaco', monospace;
        font-size: 14px;
        line-height: 1.5;
        outline: none;
        
        &:focus { box-shadow: none; }
      }
    }
    
    .console-box {
      background: #252526;
      border-top: 1px solid #333;
      transition: height 0.3s;
      display: flex;
      flex-direction: column;
      
      &.expanded { height: 200px; }
      &:not(.expanded) { height: 40px; }
      
      .console-header {
        height: 40px;
        padding: 0 15px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: #ccc;
        cursor: pointer;
        font-size: 13px;
        background: #333;
        &:hover { color: #fff; }
      }
      
      .console-body {
        flex: 1;
        padding: 15px;
        color: #fff;
        overflow-y: auto;
        
        .placeholder { color: #666; text-align: center; margin-top: 20px; }
        
        .result-display {
          .status { font-size: 18px; font-weight: bold; margin-bottom: 10px; }
          .status.success { color: #67C23A; }
          .status.error { color: #F56C6C; }
          .error-msg { background: #3c1e1e; color: #F56C6C; padding: 10px; border-radius: 4px; font-family: monospace; }
        }
      }
    }
  }
}
</style>