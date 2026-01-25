<template>
  <div class="page-container">
    <el-card class="search-card" shadow="never">
      <el-form :inline="true" :model="queryForm" size="small">
        <el-form-item label="学生姓名">
          <el-input v-model="queryForm.student_name" placeholder="请输入学生姓名" clearable @keyup.enter.native="fetchData"/>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="queryForm.status" placeholder="全部" clearable @change="fetchData" style="width: 120px">
            <el-option label="待审核" :value="0"></el-option>
            <el-option label="已通过" :value="1"></el-option>
            <el-option label="已拒绝" :value="2"></el-option>
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
        <el-table-column prop="competition_title" label="申请竞赛" show-overflow-tooltip></el-table-column>
        <el-table-column prop="student_name" label="申请学生" align="center"></el-table-column>
        <el-table-column prop="created_at" label="申请时间" width="160" align="center">
           <template slot-scope="scope">{{ formatTime(scope.row.created_at) }}</template>
        </el-table-column>
        <el-table-column prop="status" label="状态" align="center" width="100">
          <template slot-scope="scope">
            <el-tag v-if="scope.row.status === 0">待审核</el-tag>
            <el-tag v-else-if="scope.row.status === 1" type="success">已通过</el-tag>
            <el-tag v-else type="danger">已拒绝</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" align="center">
          <template slot-scope="scope">
            <div v-if="scope.row.status === 0">
              <el-button type="text" style="color:#67C23A" icon="el-icon-check" @click="handleAudit(scope.row, 1)">通过</el-button>
              <el-button type="text" style="color:#F56C6C" icon="el-icon-close" @click="handleAudit(scope.row, 2)">拒绝</el-button>
            </div>
            <div v-else>
              <span style="color:#909399">已处理</span>
            </div>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
export default {
  name: "EnrollmentList",
  data() {
    return {
      loading: true,
      tableData: [],
      queryForm: { student_name: "", status: undefined }
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
        if (this.queryForm.student_name) params.search = this.queryForm.student_name;
        if (this.queryForm.status !== undefined) params.status = this.queryForm.status;
        const res = await this.$axios.get('enrollments/', { params });
        this.tableData = res.data;
      } finally {
        this.loading = false;
      }
    },
    resetQuery() {
      this.queryForm = { student_name: "", status: undefined };
      this.fetchData();
    },
    handleAudit(row, status) {
      const action = status === 1 ? '通过' : '拒绝';
      this.$confirm(`确认${action}该申请吗?`, '提示', { type: 'warning' }).then(async () => {
        await this.$axios.patch(`enrollments/${row.id}/`, { status: status });
        this.$message.success("操作成功");
        this.fetchData();
      });
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