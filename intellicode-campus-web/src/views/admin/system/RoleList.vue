<template>
  <div class="app-container">
    <el-card shadow="never">
      <div style="margin-bottom: 15px;">
        <el-button type="success" icon="el-icon-plus" size="small" @click="handleAdd">新增角色</el-button>
      </div>
      <el-table :data="roleList" border stripe v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" align="center"></el-table-column>
        <el-table-column prop="name" label="角色名称" align="center"></el-table-column>
        <el-table-column prop="key" label="权限字符" align="center"></el-table-column>
        <el-table-column label="状态" align="center">
          <template slot-scope="scope">
            <el-switch v-model="scope.row.status" active-color="#13ce66" @change="handleStatusChange(scope.row)"></el-switch>
          </template>
        </el-table-column>
        <el-table-column label="操作" align="center">
          <template slot-scope="scope">
            <el-button type="text" style="color:#67C23A" icon="el-icon-edit" @click="handleEdit(scope.row)">修改</el-button>
            <el-button type="text" style="color:#F56C6C" icon="el-icon-delete" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog :title="title" :visible.sync="open" width="500px">
      <el-form ref="form" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="角色名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入角色名称" />
        </el-form-item>
        <el-form-item label="权限字符" prop="key">
          <el-input v-model="form.key" placeholder="请输入权限字符" />
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="form.remark" type="textarea" placeholder="请输入内容" />
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
  name: "RoleList",
  data() {
    return {
      loading: false,
      roleList: [],
      open: false,
      title: "",
      form: {},
      rules: {
        name: [{ required: true, message: "角色名称不能为空", trigger: "blur" }],
        key: [{ required: true, message: "权限字符不能为空", trigger: "blur" }]
      }
    };
  },
  created() {
    this.getList();
  },
  methods: {
    async getList() {
      this.loading = true;
      try {
        const res = await this.$axios.get('system/role/');
        this.roleList = res.data;
      } finally { this.loading = false; }
    },
    handleAdd() {
      this.form = { status: true };
      this.title = "新增角色";
      this.open = true;
    },
    handleEdit(row) {
      this.form = { ...row };
      this.title = "修改角色";
      this.open = true;
    },
    async submitForm() {
      this.$refs["form"].validate(async valid => {
        if (valid) {
          if (this.form.id) {
            await this.$axios.put(`system/role/${this.form.id}/`, this.form);
          } else {
            await this.$axios.post('system/role/', this.form);
          }
          this.$message.success("操作成功");
          this.open = false;
          this.getList();
        }
      });
    },
    handleDelete(row) {
      this.$confirm('是否确认删除?', '警告', { type: 'warning' }).then(async () => {
        await this.$axios.delete(`system/role/${row.id}/`);
        this.$message.success("删除成功");
        this.getList();
      }).catch(() => {});
    },
    async handleStatusChange(row) {
       await this.$axios.patch(`system/role/${row.id}/`, { status: row.status });
       this.$message.success("状态已更新");
    }
  }
};
</script>