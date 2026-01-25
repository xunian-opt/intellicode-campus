<template>
  <div class="page-container">
    <el-card class="search-card" shadow="never">
      <el-form :inline="true" :model="queryForm" size="small">
        <el-form-item label="关键词">
          <el-input 
            v-model="queryForm.search" 
            placeholder="搜索提问或学生姓名" 
            clearable 
            @keyup.enter.native="fetchData"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchData">查询</el-button>
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
        empty-text="暂无数据"
      >
        <el-table-column prop="id" label="ID" width="80" align="center"></el-table-column>
        <el-table-column prop="student_name" label="提问学生" width="120" align="center"></el-table-column>
        <el-table-column prop="user_query" label="用户提问" show-overflow-tooltip></el-table-column>
        <el-table-column prop="ai_response" label="AI回答" show-overflow-tooltip>
           <template slot-scope="scope">
             {{ scope.row.ai_response.substring(0, 50) }}...
           </template>
        </el-table-column>
        <el-table-column prop="created_at" label="提问时间" width="160" align="center">
           <template slot-scope="scope">{{ formatTime(scope.row.created_at) }}</template>
        </el-table-column>
        <el-table-column label="操作" width="150" align="center">
          <template slot-scope="scope">
            <el-button type="text" icon="el-icon-view" @click="handleDetail(scope.row)">查看详情</el-button>
            <el-button type="text" class="btn-delete" style="color:red;" icon="el-icon-delete" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog title="对话详情" :visible.sync="open" width="600px" append-to-body>
      <div style="margin-bottom: 20px;">
        <div style="font-weight: bold; margin-bottom: 10px; color: #409EFF;">
          <i class="el-icon-user"></i> {{ currentItem.student_name }} 问：
        </div>
        <div style="background: #f4f4f5; padding: 10px; border-radius: 4px; line-height: 1.6;">
          {{ currentItem.user_query }}
        </div>
      </div>
      <div>
        <div style="font-weight: bold; margin-bottom: 10px; color: #67C23A;">
          <i class="el-icon-cpu"></i> AI 答：
        </div>
        <div style="background: #f0f9eb; padding: 10px; border-radius: 4px; line-height: 1.6; white-space: pre-wrap;">
          {{ currentItem.ai_response }}
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
  name: "AIChatList",
  data() {
    return {
      loading: true,
      tableData: [],
      open: false,
      currentItem: { user_query: '', ai_response: '' },
      queryForm: { search: "" }
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
        if (this.queryForm.search) params.search = this.queryForm.search;
        const res = await this.$axios.get('ai_chats/', { params });
        this.tableData = res.data;
      } finally {
        this.loading = false;
      }
    },
    resetQuery() {
      this.queryForm = { search: "" };
      this.fetchData();
    },
    handleDetail(row) {
      this.currentItem = { ...row };
      this.open = true;
    },
    handleDelete(row) {
      this.$confirm('确认删除该条记录?', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        await this.$axios.delete(`ai_chats/${row.id}/`);
        this.$message.success("删除成功");
        this.fetchData();
      }).catch(() => {
        // 捕获取消操作，防止报错
        this.$message.info('已取消删除');
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