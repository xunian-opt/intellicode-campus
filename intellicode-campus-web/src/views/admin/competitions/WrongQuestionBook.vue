<template>
  <div class="page-container">
    <el-card class="search-card" shadow="never">
      <div slot="header" class="clearfix">
        <span style="font-weight: bold; font-size: 16px; color: #F56C6C;">
          <i class="el-icon-notebook-2"></i> 错题本管理
        </span>
        <span style="font-size: 12px; color: #909399; margin-left: 10px;">
          (仅显示未通过的提交记录，用于教学分析与针对性复习)
        </span>
      </div>

      <el-form :inline="true" :model="queryForm" size="small">
        <el-form-item label="学生/题目">
          <el-input 
            v-model="queryForm.keyword" 
            placeholder="搜索学生或错题名称" 
            clearable 
            @keyup.enter.native="fetchData"
            style="width: 200px;"
          />
        </el-form-item>
        <el-form-item label="错误类型">
          <el-select v-model="queryForm.result" placeholder="全部错误" clearable @change="fetchData" style="width: 150px">
            <el-option label="答案错误 (WA)" value="WA"></el-option>
            <el-option label="超时 (TLE)" value="TLE"></el-option>
            <el-option label="运行错误 (RE)" value="RE"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="danger" plain icon="el-icon-search" @click="fetchData">查询错题</el-button>
          <el-button icon="el-icon-refresh" @click="resetQuery">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="table-card" shadow="never" style="margin-top:20px;">
      <el-table 
        :data="tableData" 
        border 
        stripe 
        v-loading="loading" 
        empty-text="太棒了，目前没有错题记录！"
      >
        <el-table-column prop="id" label="ID" width="80" align="center"></el-table-column>
        
        <el-table-column prop="problem_title" label="错题名称" min-width="180" show-overflow-tooltip>
           <template slot-scope="scope">
             <i class="el-icon-warning-outline" style="color: #F56C6C; margin-right: 5px;"></i>
             <span>{{ scope.row.problem_title }}</span>
           </template>
        </el-table-column>

        <el-table-column prop="student_name" label="学生姓名" width="120" align="center"></el-table-column>

        <el-table-column prop="result" label="错误原因" width="140" align="center">
          <template slot-scope="scope">
            <el-tag v-if="scope.row.result === 'WA'" type="danger" effect="plain">答案错误</el-tag>
            <el-tag v-else-if="scope.row.result === 'TLE'" type="warning" effect="plain">运行超时</el-tag>
            <el-tag v-else-if="scope.row.result === 'RE'" type="danger" effect="dark">运行错误</el-tag>
            <el-tag v-else type="danger">{{ scope.row.result }}</el-tag>
          </template>
        </el-table-column>

        <el-table-column prop="score" label="得分" width="80" align="center">
           <template slot-scope="scope">
             <span style="color: #909399;">{{ scope.row.score }}</span>
           </template>
        </el-table-column>

        <el-table-column prop="submit_time" label="提交时间" width="160" align="center">
           <template slot-scope="scope">{{ formatTime(scope.row.submit_time) }}</template>
        </el-table-column>

        <el-table-column label="分析" width="140" align="center">
          <template slot-scope="scope">
            <el-button type="text" icon="el-icon-search" @click="handleAnalyze(scope.row)">查看代码</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog title="错题分析" :visible.sync="open" width="800px" append-to-body>
      <div v-if="currentRow">
         <el-alert
            title="错误提示"
            type="error"
            :description="getErrorTip(currentRow.result)"
            show-icon
            :closable="false"
            style="margin-bottom: 15px;">
          </el-alert>
          
          <h3>提交代码：</h3>
          <pre style="background:#fff1f0; border:1px solid #ffa39e; padding:15px; border-radius:4px; overflow:auto; color: #5c0011;">{{ currentRow.code }}</pre>
      </div>
      <div slot="footer">
        <el-button @click="open = false">关 闭</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: "WrongQuestionBook",
  data() {
    return {
      loading: true,
      tableData: [],
      open: false,
      currentRow: null,
      queryForm: { keyword: "", result: "" }
    };
  },
  created() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      this.loading = true;
      try {
        const params = {};
        if (this.queryForm.keyword) params.search = this.queryForm.keyword;
        if (this.queryForm.result) params.result = this.queryForm.result;
        
        // 【关键修改】调用后端 WrongQuestionBookViewSet 接口
        // 该接口已在后端过滤掉 AC 记录
        const res = await this.$axios.get('wrong_books/', { params });
        this.tableData = res.data;
      } catch (error) {
        this.$message.error("获取错题本数据失败");
      } finally {
        this.loading = false;
      }
    },
    resetQuery() {
      this.queryForm = { keyword: "", result: "" };
      this.fetchData();
    },
    handleAnalyze(row) {
      this.currentRow = row;
      this.open = true;
    },
    formatTime(time) {
      return time ? new Date(time).toLocaleString() : '-';
    },
    getErrorTip(result) {
      const tips = {
        'WA': '程序输出的答案与预期不符，请检查算法逻辑或边界条件。',
        'TLE': '程序运行时间超过了限制，请优化算法复杂度（如减少循环嵌套）。',
        'RE': '程序运行时崩溃，可能是数组越界、除以零或内存溢出。',
        'Pending': '正在排队等待判题...'
      };
      return tips[result] || '请检查代码逻辑。';
    }
  }
};
</script>

<style scoped>
.page-container { padding: 20px; }
.search-card { border: none; }
.table-card { border: none; }
</style>