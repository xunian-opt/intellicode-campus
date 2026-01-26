<template>
  <div class="page-container">
    <el-card shadow="never" class="search-card">
      <el-form :inline="true" :model="queryForm" size="small">
        <el-form-item label="字典名称">
          <el-input v-model="queryForm.name" placeholder="请输入字典名称" clearable @keyup.enter.native="fetchData"/>
        </el-form-item>
        <el-form-item label="字典类型">
          <el-input v-model="queryForm.type" placeholder="请输入类型标识" clearable @keyup.enter.native="fetchData"/>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="el-icon-search" @click="fetchData">查询</el-button>
          <el-button icon="el-icon-refresh" @click="resetQuery">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card shadow="never" class="table-card" style="margin-top:20px;">
      <div class="table-toolbar" style="margin-bottom:15px;">
        <el-button type="success" icon="el-icon-plus" size="small" @click="handleAdd">新建字典</el-button>
      </div>

      <el-table :data="tableData" border stripe v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" align="center"></el-table-column>
        <el-table-column prop="name" label="字典名称" align="center"></el-table-column>
        <el-table-column prop="type" label="字典类型" align="center">
           <template slot-scope="scope">
             <el-tag>{{ scope.row.type }}</el-tag>
           </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" align="center" width="100">
           <template slot-scope="scope">
             <el-tag :type="scope.row.status ? 'success' : 'danger'">{{ scope.row.status ? '正常' : '停用' }}</el-tag>
           </template>
        </el-table-column>
        <el-table-column prop="remark" label="备注" align="center" show-overflow-tooltip></el-table-column>
        <el-table-column label="操作" align="center" width="300">
          <template slot-scope="scope">
            <el-button type="text" icon="el-icon-s-operation" @click="handleData(scope.row)">数据管理</el-button>
            <el-button type="text" icon="el-icon-edit" @click="handleEdit(scope.row)">修改</el-button>
            <el-button type="text" style="color:red" icon="el-icon-delete" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog :title="title" :visible.sync="open" width="500px" append-to-body>
      <el-form ref="form" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="字典名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入字典名称" />
        </el-form-item>
        <el-form-item label="字典类型" prop="type">
          <el-input v-model="form.type" placeholder="请输入字典类型" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="form.status">
            <el-radio :label="true">正常</el-radio>
            <el-radio :label="false">停用</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input v-model="form.remark" type="textarea" placeholder="请输入内容"></el-input>
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
  name: "DictList",
  data() {
    return {
      loading: false,
      tableData: [],
      open: false,
      title: "",
      queryForm: { name: "", type: "" },
      form: {},
      rules: {
        name: [{ required: true, message: "字典名称不能为空", trigger: "blur" }],
        type: [{ required: true, message: "字典类型不能为空", trigger: "blur" }]
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
        const params = { ...this.queryForm };
        // 注意：这里使用的是 system/dict 接口
        const res = await this.$axios.get('system/dict/', { params });
        this.tableData = res.data.results || res.data;
      } finally {
        this.loading = false;
      }
    },
    resetQuery() {
      this.queryForm = { name: "", type: "" };
      this.fetchData();
    },
    // 🟢 跳转到数据管理页面
    handleData(row) {
      // 路由跳转，携带 dictId
      this.$router.push({ 
        path: '/dict-manage/index', // 对应数据库里注册的 path
        query: { dictId: row.id, dictName: row.name } 
      });
    },
    handleAdd() {
      this.form = { status: true };
      this.title = "新增字典类型";
      this.open = true;
    },
    handleEdit(row) {
      this.form = { ...row };
      this.title = "修改字典类型";
      this.open = true;
    },
    submitForm() {
      this.$refs["form"].validate(async valid => {
        if (valid) {
          if (this.form.id) {
            await this.$axios.patch(`system/dict/${this.form.id}/`, this.form);
            this.$message.success("修改成功");
          } else {
            await this.$axios.post('system/dict/', this.form);
            this.$message.success("新增成功");
          }
          this.open = false;
          this.fetchData();
        }
      });
    },
    handleDelete(row) {
      this.$confirm('确认删除该字典类型吗?', '警告', { type: 'warning' }).then(async () => {
        await this.$axios.delete(`system/dict/${row.id}/`);
        this.$message.success("删除成功");
        this.fetchData();
      }).catch(() => {});
    }
  }
};
</script>

<style scoped>
.search-card { border: none; }
.table-card { border: none; }
</style>