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
        <el-table-column label="操作" align="center" width="250">
          <template slot-scope="scope">
            <el-button type="text" icon="el-icon-setting" @click="handlePermission(scope.row)">分配权限</el-button>
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

    <el-dialog title="分配菜单权限" :visible.sync="permOpen" width="500px">
      <el-form label-width="80px">
        <el-form-item label="角色名称">
          <el-input v-model="currentRole.name" disabled />
        </el-form-item>
        <el-form-item label="菜单权限">
          <el-tree
            ref="menuTree"
            :data="menuOptions"
            show-checkbox
            node-key="id"
            :props="defaultProps"
            :default-expand-all="true"
            empty-text="加载中..."
          ></el-tree>
        </el-form-item>
      </el-form>
      <div slot="footer">
        <el-button type="primary" @click="submitPermission">提 交</el-button>
        <el-button @click="permOpen = false">取 消</el-button>
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
      permOpen: false, // 权限弹窗开关
      title: "",
      form: {},
      currentRole: {}, // 当前操作的角色
      menuOptions: [], // 菜单树数据
      defaultProps: {
        children: 'children',
        label: 'title'
      },
      rules: {
        name: [{ required: true, message: "必填", trigger: "blur" }],
        key: [{ required: true, message: "必填", trigger: "blur" }]
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
    // 获取完整菜单树
    async getMenuTreeselect() {
      const res = await this.$axios.get('system/menu/', { params: { tree: 'true' } });
      this.menuOptions = res.data;
    },
    // 🟢 打开权限分配弹窗
    async handlePermission(row) {
      this.currentRole = row;
      this.permOpen = true;
      
      // 1. 获取所有菜单树
      await this.getMenuTreeselect();
      
      // 2. 设置已选中的节点 (row.menu_ids 是后端序列化返回的)
      // 注意：ElementUI Tree 如果父节点选中，所有子节点都会选中。
      // 为了避免“半选”问题，通常只设置叶子节点的选中状态，或者依靠后端返回准确的ID
      this.$nextTick(() => {
        // 假设后端返回了 menu_ids
        if (row.menu_ids) {
           this.$refs.menuTree.setCheckedKeys(row.menu_ids);
        } else {
           this.$refs.menuTree.setCheckedKeys([]);
        }
      });
    },
    // 🟢 提交权限
    async submitPermission() {
      // 获取全选和半选的节点ID
      const checkedKeys = this.$refs.menuTree.getCheckedKeys();
      const halfCheckedKeys = this.$refs.menuTree.getHalfCheckedKeys();
      const finalKeys = [...checkedKeys, ...halfCheckedKeys];

      try {
        await this.$axios.put(`system/role/${this.currentRole.id}/assign_permissions/`, {
          menu_ids: finalKeys
        });
        this.$message.success("权限分配成功");
        this.permOpen = false;
        this.getList(); // 刷新列表
      } catch (e) {
        this.$message.error("操作失败");
      }
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
      this.$confirm('确认删除?', '警告').then(async () => {
        await this.$axios.delete(`system/role/${row.id}/`);
        this.$message.success("删除成功");
        this.getList();
      }).catch(() => {});
    },
    async handleStatusChange(row) {
       await this.$axios.patch(`system/role/${row.id}/`, { status: row.status });
       this.$message.success("状态更新");
    }
  }
};
</script>