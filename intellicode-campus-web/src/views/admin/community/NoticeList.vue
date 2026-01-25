<template>
  <div class="page-container">
    <el-card class="search-card" shadow="never">
      <el-form :inline="true" :model="queryForm" size="small">
        <el-form-item label="公告标题">
          <el-input 
            v-model="queryForm.title" 
            placeholder="请输入标题" 
            clearable 
            @keyup.enter.native="fetchData"
          />
        </el-form-item>
        <el-form-item label="公告类型">
          <el-select v-model="queryForm.type" placeholder="全部" clearable @change="fetchData">
            <el-option label="普通公告" :value="1"></el-option>
            <el-option label="竞赛通知" :value="2"></el-option>
            <el-option label="考试提醒" :value="3"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchData">查询</el-button>
          <el-button icon="el-icon-refresh" @click="resetQuery">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="table-card" shadow="never" style="margin-top:20px;">
      <div class="table-toolbar" style="margin-bottom:15px;">
        <el-button type="success" icon="el-icon-plus" size="small" @click="handleAdd">发布公告</el-button>
      </div>

      <el-table 
        :data="tableData" 
        border 
        stripe 
        v-loading="loading" 
        empty-text="暂无数据"
      >
        <el-table-column prop="id" label="ID" width="80" align="center"></el-table-column>
        <el-table-column prop="title" label="标题" show-overflow-tooltip></el-table-column>
        <el-table-column prop="type" label="类型" width="120" align="center">
          <template slot-scope="scope">
            <el-tag v-if="scope.row.type === 1" type="info">普通公告</el-tag>
            <el-tag v-else-if="scope.row.type === 2" type="warning">竞赛通知</el-tag>
            <el-tag v-else type="danger">考试提醒</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="author_name" label="发布人" width="120" align="center"></el-table-column>
        <el-table-column prop="created_at" label="发布时间" width="160" align="center">
           <template slot-scope="scope">{{ formatTime(scope.row.created_at) }}</template>
        </el-table-column>
        <el-table-column label="操作" width="200" align="center">
          <template slot-scope="scope">
            <el-button type="text" class="btn-edit" icon="el-icon-edit" @click="handleEdit(scope.row)">修改</el-button>
            <el-button type="text" class="btn-delete" style="color:red;" icon="el-icon-delete" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog :title="title" :visible.sync="open" width="600px" append-to-body>
      <el-form ref="form" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="公告标题" prop="title">
          <el-input v-model="form.title" placeholder="请输入标题" />
        </el-form-item>
        <el-form-item label="类型" prop="type">
          <el-radio-group v-model="form.type">
            <el-radio :label="1">普通</el-radio>
            <el-radio :label="2">竞赛</el-radio>
            <el-radio :label="3">考试</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="内容" prop="content">
          <el-input type="textarea" :rows="6" v-model="form.content" placeholder="请输入公告内容..."></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="submitForm">确 定</el-button>
        <el-button @click="open = false">取 消</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: "NoticeList",
  data() {
    return {
      loading: true,
      tableData: [],
      open: false,
      title: "",
      queryForm: { title: "", type: undefined },
      form: {},
      rules: {
        title: [{ required: true, message: "标题不能为空", trigger: "blur" }],
        type: [{ required: true, message: "请选择类型", trigger: "change" }],
        content: [{ required: true, message: "内容不能为空", trigger: "blur" }]
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
        if (this.queryForm.title) params.search = this.queryForm.title;
        if (this.queryForm.type) params.type = this.queryForm.type;
        const res = await this.$axios.get('notices/', { params });
        this.tableData = res.data;
      } finally {
        this.loading = false;
      }
    },
    resetQuery() {
      this.queryForm = { title: "", type: undefined };
      this.fetchData();
    },
    handleAdd() {
      this.form = { type: 1 };
      this.title = "发布公告";
      this.open = true;
    },
    handleEdit(row) {
      this.form = { ...row };
      this.title = "修改公告";
      this.open = true;
    },
    submitForm() {
      this.$refs["form"].validate(async valid => {
        if (valid) {
          if (this.form.id) {
            await this.$axios.patch(`notices/${this.form.id}/`, this.form);
            this.$message.success("修改成功");
          } else {
            await this.$axios.post('notices/', this.form);
            this.$message.success("发布成功");
          }
          this.open = false;
          this.fetchData();
        }
      });
    },
    handleDelete(row) {
      this.$confirm('确认删除?', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        await this.$axios.delete(`notices/${row.id}/`);
        this.$message.success("删除成功");
        this.fetchData();
      }).catch(() => {
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
.btn-edit { color: #67C23A; }
.search-card { border: none; }
.table-card { border: none; }
</style>