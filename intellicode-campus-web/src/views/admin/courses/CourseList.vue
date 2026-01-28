<template>
  <div class="page-container">
    <el-card class="search-card" shadow="never">
      <el-form :inline="true" :model="queryForm" size="small">
        <el-form-item label="课程名称">
          <el-input v-model="queryForm.title" placeholder="输入课程名称搜索" clearable @keyup.enter.native="fetchData"/>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="el-icon-search" :loading="loading" @click="fetchData">查询</el-button>
          <el-button icon="el-icon-refresh" @click="resetQuery">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="table-card" shadow="never" style="margin-top:20px;">
      <div class="table-toolbar" style="margin-bottom:15px;">
        <el-button type="success" icon="el-icon-plus" size="small" @click="handleAdd">新建课程</el-button>
      </div>
      <el-table :data="tableData" border stripe v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" align="center"></el-table-column>
        <el-table-column prop="title" label="课程名称" show-overflow-tooltip></el-table-column>
        <el-table-column prop="teacher_name" label="授课教师" width="120" align="center"></el-table-column>
        <el-table-column prop="category" label="分类" width="120" align="center">
           <template slot-scope="scope"><el-tag>{{ scope.row.category }}</el-tag></template>
        </el-table-column>
        <el-table-column label="操作" width="300" align="center">
          <template slot-scope="scope">
            <el-button type="text" icon="el-icon-folder-opened" @click="handleResource(scope.row)">内容管理</el-button>
            <el-button type="text" style="color:#67C23A" icon="el-icon-edit" @click="handleEdit(scope.row)">修改</el-button>
            <el-button type="text" style="color:red" icon="el-icon-delete" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog :title="title" :visible.sync="open" width="600px" append-to-body :close-on-click-modal="false">
      <el-form ref="form" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="课程名称" prop="title">
          <el-input v-model="form.title" placeholder="请输入课程名称" />
        </el-form-item>
        <el-form-item label="课程分类" prop="category">
          <el-input v-model="form.category" placeholder="例如: Python基础" />
        </el-form-item>
        <el-form-item label="课程简介" prop="description">
          <el-input type="textarea" :rows="4" v-model="form.description" />
        </el-form-item>
        <el-form-item label="课程大纲" prop="outline">
          <el-input type="textarea" :rows="6" v-model="form.outline" placeholder="请输入详细的教学大纲..." />
        </el-form-item>
      </el-form>
      <div slot="footer">
        <el-button type="primary" :loading="submitLoading" @click="submitForm">确 定</el-button>
        <el-button @click="open = false">取 消</el-button>
      </div>
    </el-dialog>

    <el-dialog :title="'课程资源 - ' + currentCourseTitle" :visible.sync="resourceOpen" width="800px" append-to-body>
      <div style="margin-bottom: 15px;">
        <el-upload
          class="upload-demo"
          action="#"
          :http-request="uploadFile"
          :show-file-list="false">
          <el-button size="small" type="primary" icon="el-icon-upload">上传视频/课件</el-button>
          <div slot="tip" class="el-upload__tip" style="display:inline-block; margin-left:10px;">支持 MP4, PDF, PPT 等格式</div>
        </el-upload>
      </div>

      <el-table :data="resourceList" border stripe height="400">
        <el-table-column prop="name" label="资源名称"></el-table-column>
        <el-table-column prop="resource_type" label="类型" width="100" align="center">
          <template slot-scope="scope">
            <el-tag v-if="scope.row.resource_type===1">视频</el-tag>
            <el-tag v-else-if="scope.row.resource_type===2" type="warning">课件</el-tag>
            <el-tag v-else type="info">其他</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150" align="center">
          <template slot-scope="scope">
            <el-button type="text" @click="downloadFile(scope.row.file)">下载</el-button>
            <el-button type="text" style="color:red" @click="deleteResource(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: "CourseList",
  data() {
    return {
      loading: true,
      submitLoading: false, // 🟢 新增
      tableData: [],
      open: false,
      resourceOpen: false,
      title: "",
      queryForm: { title: "" },
      form: {},
      rules: {
        title: [{ required: true, message: "必填", trigger: "blur" }],
        category: [{ required: true, message: "必填", trigger: "blur" }]
      },
      currentCourseId: null,
      currentCourseTitle: "",
      resourceList: []
    };
  },
  created() { this.fetchData(); },
  methods: {
    async fetchData() {
      this.loading = true;
      try {
        const res = await this.$axios.get('courses/', { params: { search: this.queryForm.title } });
        this.tableData = res.data;
      } finally { this.loading = false; }
    },
    resetQuery() { this.queryForm.title = ""; this.fetchData(); },
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
    async submitForm() {
      this.$refs["form"].validate(async valid => {
        if (valid) {
          this.submitLoading = true; // 🟢 开启
          try {
            const api = this.form.id ? this.$axios.patch : this.$axios.post;
            const url = this.form.id ? `courses/${this.form.id}/` : 'courses/';
            await api(url, this.form);
            this.$message.success("操作成功");
            this.open = false;
            this.fetchData();
          } catch(e) {
            console.error(e);
          } finally {
            this.submitLoading = false; // 🟢 关闭
          }
        }
      });
    },
    handleDelete(row) {
      this.$confirm('确认删除?', '提示').then(async () => {
        await this.$axios.delete(`courses/${row.id}/`);
        this.fetchData();
      });
    },
    // ... 资源管理保持不变 ...
    handleResource(row) {
      this.currentCourseId = row.id;
      this.currentCourseTitle = row.title;
      this.resourceOpen = true;
      this.fetchResources();
    },
    async fetchResources() {
      const res = await this.$axios.get('course_resources/', { params: { course: this.currentCourseId } });
      this.resourceList = res.data.results || res.data;
    },
    async uploadFile(param) {
      const formData = new FormData();
      formData.append('file', param.file);
      formData.append('course', this.currentCourseId);
      formData.append('name', param.file.name);
      let type = 3;
      if (param.file.name.endsWith('.mp4')) type = 1;
      else if (param.file.name.match(/\.(pdf|ppt|pptx)$/)) type = 2;
      formData.append('resource_type', type);

      try {
        await this.$axios.post('course_resources/', formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
        this.$message.success("上传成功");
        this.fetchResources();
      } catch(e) {
        this.$message.error("上传失败");
      }
    },
    async deleteResource(row) {
      await this.$axios.delete(`course_resources/${row.id}/`);
      this.$message.success("已删除");
      this.fetchResources();
    },
    downloadFile(url) {
      window.open(url, '_blank');
    }
  }
};
</script>