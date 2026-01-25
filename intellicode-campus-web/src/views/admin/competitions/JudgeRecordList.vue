<template>
  <div class="page-container">
    <el-card class="search-card" shadow="never">
      <el-form :inline="true" :model="queryForm" size="small">
        <el-form-item label="学生/题目">
          <el-input v-model="queryForm.keyword" placeholder="输入学生或题目搜索" clearable @keyup.enter.native="fetchData"/>
        </el-form-item>
        <el-form-item label="结果">
          <el-select v-model="queryForm.result" placeholder="全部" clearable @change="fetchData" style="width: 120px">
            <el-option label="通过 (AC)" value="AC"></el-option>
            <el-option label="错误 (WA)" value="WA"></el-option>
            <el-option label="超时 (TLE)" value="TLE"></el-option>
            <el-option label="运行错误 (RE)" value="RE"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchData">查询</el-button>
          <el-button icon="el-icon-refresh" @click="resetQuery">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="table-card" shadow="never" style="margin-top:20px;">
      <el-table :data="tableData" border stripe v-loading="loading" empty-text="暂无数据">
        <el-table-column prop="id" label="ID" width="80" align="center"></el-table-column>
        <el-table-column prop="problem_title" label="题目" show-overflow-tooltip></el-table-column>
        <el-table-column prop="student_name" label="提交者" width="120" align="center"></el-table-column>
        <el-table-column prop="result" label="结果" width="120" align="center">
          <template slot-scope="scope">
            <el-tag v-if="scope.row.result === 'AC'" type="success">AC</el-tag>
            <el-tag v-else-if="scope.row.result === 'Pending'" type="info">Pending</el-tag>
            <el-tag v-else type="danger">{{ scope.row.result }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="score" label="得分" width="80" align="center"></el-table-column>
        <el-table-column prop="submit_time" label="提交时间" width="160" align="center">
           <template slot-scope="scope">{{ formatTime(scope.row.submit_time) }}</template>
        </el-table-column>
        <el-table-column label="操作" width="120" align="center">
          <template slot-scope="scope">
            <el-button type="text" icon="el-icon-view" @click="handleViewCode(scope.row)">查看代码</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog title="代码详情" :visible.sync="open" width="600px" append-to-body>
      <pre style="background:#f5f7fa; padding:15px; border-radius:4px; overflow:auto;">{{ currentCode }}</pre>
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
      currentCode: "",
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
        const res = await this.$axios.get('judge_records/', { params });
        this.tableData = res.data;
      } finally {
        this.loading = false;
      }
    },
    resetQuery() {
      this.queryForm = { keyword: "", result: "" };
      this.fetchData();
    },
    handleViewCode(row) {
      this.currentCode = row.code;
      this.open = true;
    },
    formatTime(time) {
      return time ? new Date(time).toLocaleString() : '';
    }
  }
};
</script>

<style scoped>
.search-card { border: none; }
.table-card { border: none; }
</style>