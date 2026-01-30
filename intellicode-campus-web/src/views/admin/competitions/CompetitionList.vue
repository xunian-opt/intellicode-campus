<template>
  <div class="page-container">
    <el-card class="search-card" shadow="never">
      <el-form :inline="true" :model="queryForm" size="small">
        <el-form-item label="竞赛名称">
          <el-input v-model="queryForm.title" placeholder="请输入名称" clearable @keyup.enter.native="fetchData"/>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="el-icon-search" @click="fetchData">查询</el-button>
          <el-button icon="el-icon-refresh" @click="resetQuery">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="table-card" shadow="never" style="margin-top:20px;">
      <div class="table-toolbar" style="margin-bottom:15px;">
        <el-button type="success" icon="el-icon-plus" size="small" @click="handleAdd">新增竞赛</el-button>
      </div>

      <el-table :data="tableData" border stripe v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" align="center"></el-table-column>
        
        <el-table-column label="背景图" width="120" align="center">
          <template slot-scope="scope">
            <el-image 
              v-if="scope.row.cover_img"
              style="width: 80px; height: 45px; border-radius: 4px;"
              :src="scope.row.cover_img" 
              :preview-src-list="[scope.row.cover_img]">
            </el-image>
            <span v-else>无</span>
          </template>
        </el-table-column>

        <el-table-column prop="title" label="竞赛名称" show-overflow-tooltip></el-table-column>
        <el-table-column prop="start_time" label="开始时间" width="160"></el-table-column>
        <el-table-column prop="end_time" label="结束时间" width="160"></el-table-column>
        <el-table-column label="操作" width="200" align="center">
          <template slot-scope="scope">
            <el-button type="text" icon="el-icon-edit" @click="handleEdit(scope.row)">修改</el-button>
            <el-button type="text" style="color:red" icon="el-icon-delete" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog :title="title" :visible.sync="open" width="650px" append-to-body @close="resetForm">
      <el-form ref="form" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="竞赛名称" prop="title">
          <el-input v-model="form.title" placeholder="请输入竞赛名称" />
        </el-form-item>
        
        <el-form-item label="竞赛背景图" prop="cover_img">
          <el-upload
            class="avatar-uploader"
            action=""
            :auto-upload="false"
            :show-file-list="false"
            :on-change="handleFileChange"
            accept="image/jpeg,image/png">
            <img v-if="imageUrl" :src="imageUrl" class="avatar">
            <i v-else class="el-icon-plus avatar-uploader-icon"></i>
          </el-upload>
          <div style="font-size:12px; color:#999;">建议上传深色背景图，尺寸 800x450，支持 JPG/PNG</div>
        </el-form-item>

        <el-row>
          <el-col :span="12">
            <el-form-item label="开始时间" prop="start_time">
              <el-date-picker v-model="form.start_time" type="datetime" placeholder="选择日期时间" value-format="yyyy-MM-dd HH:mm:ss" style="width: 100%;"/>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="结束时间" prop="end_time">
              <el-date-picker v-model="form.end_time" type="datetime" placeholder="选择日期时间" value-format="yyyy-MM-dd HH:mm:ss" style="width: 100%;"/>
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="包含题目">
           <el-input v-model="form.problem_ids_str" placeholder="自动关联，此处仅作展示 (开发中)" disabled />
        </el-form-item>

        <el-form-item label="竞赛规则" prop="description">
          <el-input type="textarea" :rows="4" v-model="form.description" />
        </el-form-item>
      </el-form>
      <div slot="footer">
        <el-button type="primary" :loading="submitLoading" @click="submitForm">确 定</el-button>
        <el-button @click="open = false">取 消</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: "AdminCompetitionList",
  data() {
    return {
      loading: true,
      submitLoading: false,
      tableData: [],
      open: false,
      title: "",
      queryForm: { title: "" },
      form: {},
      imageUrl: "",
      uploadRawFile: null,
      rules: {
        title: [{ required: true, message: "必填", trigger: "blur" }],
        start_time: [{ required: true, message: "必填", trigger: "change" }],
        end_time: [{ required: true, message: "必填", trigger: "change" }]
      }
    };
  },
  created() { this.fetchData(); },
  methods: {
    async fetchData() {
      this.loading = true;
      try {
        const res = await this.$axios.get('competitions/', { params: this.queryForm });
        this.tableData = res.data.results || res.data;
      } finally { this.loading = false; }
    },
    resetQuery() { this.queryForm = {}; this.fetchData(); },
    
    resetForm() {
      this.form = {};
      this.imageUrl = "";
      this.uploadRawFile = null;
      if(this.$refs.form) this.$refs.form.resetFields();
    },
    handleAdd() {
      this.resetForm();
      this.title = "新增竞赛";
      this.open = true;
    },
    handleEdit(row) {
      this.resetForm();
      this.form = { ...row };
      this.imageUrl = row.cover_img;
      this.title = "修改竞赛";
      this.open = true;
    },
    handleFileChange(file) {
      this.uploadRawFile = file.raw;
      this.imageUrl = URL.createObjectURL(file.raw);
    },
    async submitForm() {
      this.$refs["form"].validate(async valid => {
        if (valid) {
          this.submitLoading = true;
          try {
            const formData = new FormData();
            Object.keys(this.form).forEach(key => {
                if (this.form[key] !== null && key !== 'cover_img' && key !== 'problems') {
                    formData.append(key, this.form[key]);
                }
            });
            
            if (this.uploadRawFile) {
                formData.append('cover_img', this.uploadRawFile);
            }

            if (this.form.id) {
              await this.$axios.patch(`competitions/${this.form.id}/`, formData);
            } else {
              await this.$axios.post('competitions/', formData);
            }
            this.$message.success("操作成功");
            this.open = false;
            this.fetchData();
          } catch(e) {
            this.$message.error("操作失败");
          } finally {
            this.submitLoading = false;
          }
        }
      });
    },
    handleDelete(row) {
      this.$confirm('确认删除?', '提示').then(async () => {
        await this.$axios.delete(`competitions/${row.id}/`);
        this.fetchData();
      });
    }
  }
};
</script>

<style scoped>
.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}
.avatar-uploader .el-upload:hover { border-color: #409EFF; }
.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 150px;
  height: 80px;
  line-height: 80px;
  text-align: center;
}
.avatar {
  width: 150px;
  height: 80px;
  display: block;
  object-fit: cover;
}
</style>