<template>
  <div class="app-container">
    <el-card shadow="never" class="search-card">
      <el-form :inline="true" :model="queryParams" size="small">
        <el-form-item label="字典名称">
          <el-input v-model="queryParams.name" placeholder="请输入字典名称" clearable @keyup.enter.native="fetchData"/>
        </el-form-item>
        <el-form-item label="字典类型">
          <el-input v-model="queryParams.type" placeholder="请输入字典类型" clearable @keyup.enter.native="fetchData"/>
        </el-form-item>
        <el-form-item>
          <el-button type="success" icon="el-icon-search" @click="fetchData">查询</el-button>
          <el-button icon="el-icon-refresh" @click="resetQuery">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card shadow="never" class="table-card">
      <div style="margin-bottom: 15px;">
        <el-button type="success" icon="el-icon-plus" size="small" @click="handleAdd">新增字典类型</el-button>
      </div>

      <el-table 
        :data="dictList" 
        border 
        stripe 
        v-loading="loading"
        element-loading-text="加载中..."
        empty-text="暂无数据"
      >
        <el-table-column label="序号" type="index" width="60" align="center"></el-table-column>
        <el-table-column prop="name" label="字典名称" align="center"></el-table-column>
        <el-table-column prop="type" label="字典类型" align="center">
          <template slot-scope="scope">
            <el-link type="primary">{{ scope.row.type }}</el-link>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" align="center">
          <template slot-scope="scope">
            <el-tag v-if="scope.row.status" type="success">正常</el-tag>
            <el-tag v-else type="danger">停用</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="remark" label="备注" align="center"></el-table-column>
        <el-table-column label="操作" align="center" width="200">
          <template slot-scope="scope">
            <el-button type="text" style="color:#67C23A" icon="el-icon-edit" @click="handleEdit(scope.row)">修改</el-button>
            <el-button type="text" style="color:#F56C6C" icon="el-icon-delete" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog :title="title" :visible.sync="open" width="500px">
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
      dictList: [],
      open: false,
      title: "",
      queryParams: {
        name: '',
        type: ''
      },
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
        // 使用 params 传递搜索参数，后端 SearchFilter 会识别 ?search=xxx
        // 或者 ?name=xxx 取决于后端配置。我们在后端配置了 search_fields，
        // 所以应该用 search 参数，或者如果用了 DjangoFilterBackend 也可以用字段名
        const params = {};
        if (this.queryParams.name) params.search = this.queryParams.name; 
        if (this.queryParams.type && !params.search) params.search = this.queryParams.type;
        // 注意：Django默认 SearchFilter 的参数名是 search，它会同时搜 name 和 type
        
        const res = await this.$axios.get('system/dict/', { params });
        this.dictList = res.data;
      } finally { this.loading = false; }
    },
    resetQuery() {
      this.queryParams = { name: '', type: '' };
      this.fetchData();
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
    async submitForm() {
      this.$refs["form"].validate(async valid => {
        if (valid) {
          if (this.form.id) {
            await this.$axios.put(`system/dict/${this.form.id}/`, this.form);
          } else {
            await this.$axios.post('system/dict/', this.form);
          }
          this.$message.success("操作成功");
          this.open = false;
          this.fetchData();
        }
      });
    },
    handleDelete(row) {
      this.$confirm('确认删除?', '警告', { type: 'warning' }).then(async () => {
        await this.$axios.delete(`system/dict/${row.id}/`);
        this.$message.success("删除成功");
        this.fetchData();
      }).catch(() => {});
    }
  }
};
</script>

<style lang="scss" scoped>
.app-container { display: flex; flex-direction: column; gap: 20px; }
.search-card { border: none; .el-form-item { margin-bottom: 0; } }
.table-card { border: none; }
</style>