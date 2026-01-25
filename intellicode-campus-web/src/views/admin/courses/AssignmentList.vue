<template>
  <div class="page-container">
    <el-card class="search-card" shadow="never">
      <el-form :inline="true" :model="queryForm" size="small">
        <el-form-item label="作业标题">
          <el-input 
            v-model="queryForm.title" 
            placeholder="请输入作业标题" 
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
        <el-button type="success" icon="el-icon-plus" size="small" @click="handleAdd">发布新作业</el-button>
      </div>

      <el-table 
        :data="tableData" 
        border 
        stripe 
        v-loading="loading" 
        empty-text="暂无数据"
      >
        <el-table-column prop="id" label="ID" width="80" align="center"></el-table-column>
        <el-table-column prop="title" label="作业标题" show-overflow-tooltip></el-table-column>
        <el-table-column prop="course" label="所属课程ID" width="120" align="center">
           <template slot-scope="scope">
             {{ getCourseName(scope.row.course) }}
           </template>
        </el-table-column>
        <el-table-column prop="deadline" label="截止时间" width="180" align="center">
           <template slot-scope="scope">
             <span style="color: #F56C6C">{{ formatTime(scope.row.deadline) }}</span>
           </template>
        </el-table-column>
        <el-table-column prop="created_at" label="发布时间" width="180" align="center">
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
        <el-form-item label="作业标题" prop="title">
          <el-input v-model="form.title" placeholder="请输入作业标题" />
        </el-form-item>
        <el-form-item label="所属课程" prop="course">
          <el-select v-model="form.course" placeholder="请选择课程" style="width:100%" filterable>
            <el-option
              v-for="item in courseList"
              :key="item.id"
              :label="item.title"
              :value="item.id">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="截止时间" prop="deadline">
          <el-date-picker
            v-model="form.deadline"
            type="datetime"
            placeholder="选择截止日期时间"
            style="width: 100%;"
            value-format="yyyy-MM-dd HH:mm:ss">
          </el-date-picker>
        </el-form-item>
        <el-form-item label="作业内容" prop="content">
          <el-input type="textarea" :rows="5" v-model="form.content" placeholder="请输入详细的作业要求..."></el-input>
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
  name: "AssignmentList",
  data() {
    return {
      loading: true,
      tableData: [],
      courseList: [],
      open: false,
      title: "",
      queryForm: { title: "" },
      form: {},
      rules: {
        title: [{ required: true, message: "标题不能为空", trigger: "blur" }],
        course: [{ required: true, message: "请选择所属课程", trigger: "change" }],
        deadline: [{ required: true, message: "请选择截止时间", trigger: "change" }],
        content: [{ required: true, message: "作业内容不能为空", trigger: "blur" }]
      }
    };
  },
  created() {
    this.fetchData();
    this.getCourses();
  },
  methods: {
    async fetchData() {
      this.loading = true;
      try {
        const params = {};
        if(this.queryForm.title) params.search = this.queryForm.title;
        const res = await this.$axios.get('assignments/', { params });
        this.tableData = res.data;
      } finally {
        this.loading = false;
      }
    },
    async getCourses() {
      const res = await this.$axios.get('courses/');
      this.courseList = res.data;
    },
    getCourseName(id) {
      const course = this.courseList.find(c => c.id === id);
      return course ? course.title : id;
    },
    resetQuery() {
      this.queryForm = { title: "" };
      this.fetchData();
    },
    handleAdd() {
      this.form = {};
      this.title = "发布作业";
      this.open = true;
    },
    handleEdit(row) {
      this.form = { ...row };
      this.title = "修改作业";
      this.open = true;
    },
    submitForm() {
      this.$refs["form"].validate(async valid => {
        if (valid) {
          if (this.form.id) {
            await this.$axios.patch(`assignments/${this.form.id}/`, this.form);
            this.$message.success("修改成功");
          } else {
            await this.$axios.post('assignments/', this.form);
            this.$message.success("发布成功");
          }
          this.open = false;
          this.fetchData();
        }
      });
    },
    handleDelete(row) {
      this.$confirm('确认删除?', '警告', { type: 'warning' }).then(async () => {
        await this.$axios.delete(`assignments/${row.id}/`);
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