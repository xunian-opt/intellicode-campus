<template>
  <div class="page-container">
    <el-card class="search-card" shadow="never">
        <el-form :inline="true" :model="queryForm" size="small">
            <el-form-item label="用户名称">
              <el-input 
                v-model="queryForm.nickname" 
                placeholder="请输入用户昵称"
                clearable
                @keyup.enter.native="fetchData"
              ></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="fetchData">查询</el-button>
              <el-button icon="el-icon-refresh" @click="resetQuery">重置</el-button>
            </el-form-item>
        </el-form>
    </el-card>

    <el-card class="table-card" shadow="never" style="margin-top:20px;">
      <div class="table-toolbar" style="margin-bottom:15px;">
        <el-button type="success" icon="el-icon-plus" size="small" @click="handleAdd">新增用户</el-button>
      </div>

      <el-table 
        :data="tableData" 
        border 
        stripe 
        v-loading="loading"
        empty-text="暂无数据"
      >
        <el-table-column prop="username" label="账号" align="center"></el-table-column>
        <el-table-column prop="nickname" label="用户昵称" align="center"></el-table-column>
        <el-table-column prop="role" label="角色" align="center">
             <template slot-scope="scope">
                <el-tag>{{ scope.row.role === 1 ? '学生' : (scope.row.role === 2 ? '教师' : '管理员') }}</el-tag>
             </template>
        </el-table-column>
        <el-table-column prop="phone" label="手机号码" align="center"></el-table-column>
        
        <el-table-column label="操作" width="250" align="center">
          <template slot-scope="scope">
            <el-button type="text" class="btn-edit" icon="el-icon-edit" @click="handleEdit(scope.row)">修改</el-button>
            <el-button type="text" class="btn-delete" style="color:red;" icon="el-icon-delete" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      </el-card>

    <el-dialog :title="title" :visible.sync="open" width="500px" append-to-body>
      <el-form ref="form" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="用户昵称" prop="nickname">
          <el-input v-model="form.nickname" placeholder="请输入用户昵称" />
        </el-form-item>
        <el-form-item label="登录账号" prop="username">
          <el-input v-model="form.username" placeholder="请输入登录账号" :disabled="form.id !== undefined"/>
        </el-form-item>
        <el-form-item label="用户密码" prop="password" v-if="form.id === undefined">
          <el-input v-model="form.password" placeholder="请输入密码" type="password" />
        </el-form-item>
        <el-form-item label="角色" prop="role">
          <el-select v-model="form.role" placeholder="请选择">
            <el-option label="学生" :value="1"></el-option>
            <el-option label="教师" :value="2"></el-option>
            <el-option label="管理员" :value="3"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="手机号码" prop="phone">
          <el-input v-model="form.phone" placeholder="请输入手机号码" maxlength="11" />
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
  name: "UserList",
  data() {
    return {
      loading: true,
      tableData: [],
      open: false,
      title: "",
      // 保持原有变量名 queryForm
      queryForm: { nickname: "" },
      form: {},
      rules: {
        username: [{ required: true, message: "账号不能为空", trigger: "blur" }],
        password: [{ required: true, message: "密码不能为空", trigger: "blur" }],
        role: [{ required: true, message: "请选择角色", trigger: "change" }]
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
        // [修改] 构造查询参数
        const params = {};
        if (this.queryForm.nickname) {
           // 后端配置了 SearchFilter，通常使用 'search' 参数进行模糊匹配
           params.search = this.queryForm.nickname;
        }
        
        // [修改] 传递 params
        const res = await this.$axios.get('users/', { params });
        this.tableData = res.data; 
      } finally {
        this.loading = false;
      }
    },
    // [新增] 重置方法
    resetQuery() {
      this.queryForm = { nickname: "" };
      this.fetchData();
    },
    handleAdd() {
      this.form = { role: 1 }; // 默认选中学生
      this.title = "添加用户";
      this.open = true;
    },
    handleEdit(row) {
      this.form = { ...row }; // 深拷贝防止修改影响表格
      this.title = "修改用户";
      this.open = true;
    },
    async submitForm() {
      this.$refs["form"].validate(async valid => {
        if (valid) {
          if (this.form.id) {
            // [修改后] 使用 patch 进行局部更新
            await this.$axios.patch(`users/${this.form.id}/`, this.form);
            this.$message.success("修改成功");
          } else {
            await this.$axios.post('users/', this.form);
            this.$message.success("新增成功");
          }
          this.open = false;
          this.fetchData();
        }
      });
    },
    handleDelete(row) {
      this.$confirm('确认删除该用户吗?', '警告', { type: 'warning' }).then(async () => {
        await this.$axios.delete(`users/${row.id}/`);
        this.$message.success("删除成功");
        this.fetchData();
      }).catch(() => {});
    }
  }
};
</script>