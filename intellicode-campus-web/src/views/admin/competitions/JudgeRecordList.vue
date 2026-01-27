<template>
  <div class="page-container">
    <el-card class="search-card" shadow="never">
      <div slot="header" class="clearfix">
        <span style="font-weight: bold; font-size: 16px;">评测记录 / 成绩管理</span>
      </div>
      <el-form :inline="true" :model="queryForm" size="small">
        <el-form-item label="关键词">
          <el-input 
            v-model="queryForm.keyword" 
            placeholder="输入学生姓名或题目名称" 
            clearable 
            @keyup.enter.native="fetchData"
            style="width: 200px;"
          />
        </el-form-item>
        <el-form-item label="判题结果">
          <el-select v-model="queryForm.result" placeholder="全部结果" clearable @change="fetchData" style="width: 150px">
            <el-option label="通过 (AC)" value="AC"></el-option>
            <el-option label="答案错误 (WA)" value="WA"></el-option>
            <el-option label="超时 (TLE)" value="TLE"></el-option>
            <el-option label="运行错误 (RE)" value="RE"></el-option>
            <el-option label="判题中 (Pending)" value="Pending"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="el-icon-search" @click="fetchData">查询</el-button>
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
        empty-text="暂无提交记录"
        style="width: 100%"
      >
        <el-table-column prop="id" label="ID" width="80" align="center" fixed="left"></el-table-column>
        
        <el-table-column prop="student_name" label="提交者" width="150" align="center">
          <template slot-scope="scope">
            <el-tag size="small" type="info" effect="plain">{{ scope.row.student_name || '未知用户' }}</el-tag>
          </template>
        </el-table-column>

        <el-table-column prop="problem_title" label="题目名称" min-width="200" show-overflow-tooltip>
          <template slot-scope="scope">
            <span style="color: #409EFF; cursor: pointer;">{{ scope.row.problem_title }}</span>
          </template>
        </el-table-column>

        <el-table-column prop="result" label="评测结果" width="140" align="center">
          <template slot-scope="scope">
            <el-tag v-if="scope.row.result === 'AC'" type="success" effect="dark">Accepted</el-tag>
            <el-tag v-else-if="scope.row.result === 'Pending'" type="info">Pending</el-tag>
            <el-tag v-else-if="scope.row.result === 'WA'" type="danger">Wrong Answer</el-tag>
            <el-tag v-else-if="scope.row.result === 'TLE'" type="warning">Time Limit</el-tag>
            <el-tag v-else type="danger">{{ scope.row.result }}</el-tag>
          </template>
        </el-table-column>

        <el-table-column prop="score" label="得分" width="100" align="center" sortable>
          <template slot-scope="scope">
            <span :style="{ color: scope.row.score === 100 ? '#67C23A' : '#F56C6C', fontWeight: 'bold' }">
              {{ scope.row.score }}
            </span>
          </template>
        </el-table-column>

        <el-table-column prop="submit_time" label="提交时间" width="180" align="center">
           <template slot-scope="scope">{{ formatTime(scope.row.submit_time) }}</template>
        </el-table-column>

        <el-table-column label="操作" width="120" align="center" fixed="right">
          <template slot-scope="scope">
            <el-button type="text" icon="el-icon-document" @click="handleViewCode(scope.row)">查看代码</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div style="margin-top: 20px; text-align: right;">
        </div>
    </el-card>

    <el-dialog title="代码详情" :visible.sync="open" width="800px" append-to-body>
      <div v-if="currentRow">
        <el-descriptions title="提交信息" :column="2" border size="small" style="margin-bottom: 20px;">
          <el-descriptions-item label="题目">{{ currentRow.problem_title }}</el-descriptions-item>
          <el-descriptions-item label="提交者">{{ currentRow.student_name }}</el-descriptions-item>
          <el-descriptions-item label="结果">
             <el-tag size="mini" :type="currentRow.result === 'AC' ? 'success' : 'danger'">{{ currentRow.result }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="提交时间">{{ formatTime(currentRow.submit_time) }}</el-descriptions-item>
        </el-descriptions>
        <div style="position: relative;">
          <pre style="background:#282c34; color:#abb2bf; padding:15px; border-radius:4px; overflow:auto; font-family: 'Consolas', monospace; max-height: 500px;">{{ currentRow.code }}</pre>
        </div>
      </div>
      <div slot="footer">
        <el-button @click="open = false">关 闭</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: "JudgeRecordList",
  data() {
    return {
      loading: true,
      tableData: [],
      open: false,
      currentRow: null,
      queryForm: { 
        keyword: "", 
        result: "" 
      }
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
        
        // 调用后端 JudgeRecordViewSet 接口
        const res = await this.$axios.get('judge_records/', { params });
        this.tableData = res.data;
      } catch (error) {
        this.$message.error("获取评测记录失败");
      } finally {
        this.loading = false;
      }
    },
    resetQuery() {
      this.queryForm = { keyword: "", result: "" };
      this.fetchData();
    },
    handleViewCode(row) {
      this.currentRow = row;
      this.open = true;
    },
    formatTime(time) {
      return time ? new Date(time).toLocaleString() : '-';
    }
  }
};
</script>

<style scoped>
.page-container { padding: 20px; }
.search-card { border: none; margin-bottom: 10px; }
.table-card { border: none; }
</style>