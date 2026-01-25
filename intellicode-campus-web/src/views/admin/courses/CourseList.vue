<template>
  <div class="page-container">
    <el-card class="search-card" shadow="never">
      <el-form :inline="true" :model="queryForm" size="small">
        <el-form-item label="课程名称">
          <el-input 
            v-model="queryForm.title" 
            placeholder="输入课程名称搜索" 
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
      <div class="table-toolbar" style="margin-bottom:15px;">
        <el-button type="success" icon="el-icon-plus" size="small" @click="handleAdd">新增课程</el-button>
      </div>

      <el-table 
        :data="tableData" 
        border 
        stripe 
        v-loading="loading" 
        empty-text="暂无数据"
      >
        <el-table-column prop="id" label="ID" width="80" align="center"></el-table-column>
        <el-table-column prop="title" label="课程名称" show-overflow-tooltip></el-table-column>
        <el-table-column prop="category" label="分类" width="120" align="center">
           <template slot-scope="scope">
             <el-tag size="medium">{{ scope.row.category }}</el-tag>
           </template>
        </el-table-column>
        <el-table-column prop="teacher_name" label="授课教师" width="120" align="center"></el-table-column>
        <el-table-column prop="view_count" label="浏览量" width="100" align="center"></el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="160" align="center">
           <template slot-scope="scope">
             {{ formatTime(scope.row.created_at) }}
           </template>
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
        <el-form-item label="课程名称" prop="title">
          <el-input v-model="form.title" placeholder="请输入课程名称" />
        </el-form-item>
        <el-form-item label="课程分类" prop="category">
          <el-input v-model="form.category" placeholder="例如: Python基础, 数据结构" />
        </el-form-item>
        <el-form-item label="授课教师" prop="teacher">
          <el-select v-model="form.teacher" placeholder="请选择教师" style="width:100%">
            <el-option
              v-for="item in teacherList"
              :key="item.id"
              :label="item.nickname || item.username"
              :value="item.id">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="课程简介" prop="description">
          <el-input type="textarea" :rows="4" v-model="form.description" placeholder="请输入课程简介"></el-input>
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
  name: "CourseList",
  data() {
    return {
      loading: true,
      tableData: [],
      teacherList: [],
      open: false,
      title: "",
      queryForm: { title: "" },
      form: {},
      rules: {
        title: [{ required: true, message: "课程名称不能为空", trigger: "blur" }],
        category: [{ required: true, message: "分类不能为空", trigger: "blur" }],
        teacher: [{ required: true, message: "请选择授课教师", trigger: "change" }],
        description: [{ required: true, message: "简介不能为空", trigger: "blur" }]
      }
    };
  },
  created() {
    this.fetchData();
    this.getTeachers();
  },
  methods: {
    async fetchData() {
      this.loading = true;
      try {
        const params = {};
        if (this.queryForm.title) params.search = this.queryForm.title;
        const res = await this.$axios.get('courses/', { params });
        this.tableData = res.data;
      } finally {
        this.loading = false;
      }
    },
    async getTeachers() {
      const res = await this.$axios.get('users/', { params: { role: 2 } });
      this.teacherList = res.data;
    },
    resetQuery() {
      this.queryForm = { title: "" };
      this.fetchData();
    },
    handleAdd() {
      this.form = {};
      this.title = "新增课程";
      this.open = true;
    },
    handleEdit(row) {
      this.form = { ...row };
      this.title = "修改课程";
      this.open = true;
    },
    submitForm() {
      this.$refs["form"].validate(async valid => {
        if (valid) {
          if (this.form.id) {
            await this.$axios.patch(`courses/${this.form.id}/`, this.form);
            this.$message.success("修改成功");
          } else {
            await this.$axios.post('courses/', this.form);
            this.$message.success("新增成功");
          }
          this.open = false;
          this.fetchData();
        }
      });
    },
    handleDelete(row) {
      this.$confirm('确认删除该课程吗?', '警告', { type: 'warning' }).then(async () => {
        await this.$axios.delete(`courses/${row.id}/`);
        this.$message.success("删除成功");
        this.fetchData();
      }).catch(() => {});
    },
    formatTime(time) {
      if(!time) return '';
      return new Date(time).toLocaleString();
    }
  }
};
</script>

<style scoped>
/* 移除 .page-container 的 padding，避免与 AdminLayout 的 el-main padding 叠加 */
.btn-edit {
  color: #67C23A;
}
.search-card {
  border: none;
}
.table-card {
  border: none;
}
</style>