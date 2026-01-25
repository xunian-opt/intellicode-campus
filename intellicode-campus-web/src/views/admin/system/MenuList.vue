<template>
  <div class="app-container">
    <el-card shadow="never" class="search-card">
      <el-form :inline="true" size="small">
        <el-form-item label="菜单名称:">
          <el-input v-model="queryParams.title" placeholder="请输入菜单名称" clearable @keyup.enter.native="fetchData"/>
        </el-form-item>
        <el-form-item>
          <el-button type="success" icon="el-icon-search" @click="fetchData">查询</el-button>
          <el-button icon="el-icon-refresh" @click="resetQuery">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card shadow="never" class="table-card">
      <div class="table-toolbar">
        <div class="left-title">菜单列表</div>
        <el-button type="success" icon="el-icon-plus" size="small" @click="handleAdd()">新增</el-button>
      </div>

      <el-table
        v-loading="loading"
        :data="menuList"
        row-key="id"
        border
        default-expand-all
        :tree-props="{children: 'children', hasChildren: 'hasChildren'}"
        class="custom-table">
        
        <el-table-column prop="title" label="菜单名称" :show-overflow-tooltip="true" width="200"></el-table-column>
        
        <el-table-column prop="id" label="菜单ID" align="center" width="80"></el-table-column>
        
        <el-table-column prop="icon" label="图标" align="center" width="80">
          <template slot-scope="scope">
            <i :class="scope.row.icon" v-if="scope.row.icon"></i>
            <span v-else>-</span>
          </template>
        </el-table-column>
        
        <el-table-column prop="order_num" label="排序" align="center" width="60"></el-table-column>
        
        <el-table-column prop="perms" label="权限标识" :show-overflow-tooltip="true" align="center"></el-table-column>
        
        <el-table-column prop="path" label="路由地址" :show-overflow-tooltip="true" align="center"></el-table-column>
        
        <el-table-column prop="component" label="组件路径" :show-overflow-tooltip="true" align="center"></el-table-column>

        <el-table-column prop="menu_type" label="菜单类型" align="center" width="100">
          <template slot-scope="scope">
            <el-tag v-if="scope.row.menu_type === 'M'" type="warning">目录</el-tag>
            <el-tag v-else-if="scope.row.menu_type === 'C'" type="success">菜单</el-tag>
            <el-tag v-else type="info">按钮</el-tag>
          </template>
        </el-table-column>
        
        <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
          <template slot-scope="scope">
            <el-button 
              size="mini" 
              type="text" 
              class="btn-text-edit" 
              icon="el-icon-edit" 
              @click="handleEdit(scope.row)"
            >修改</el-button>
            <el-button 
              size="mini" 
              type="text" 
              class="btn-text-add" 
              icon="el-icon-plus" 
              @click="handleAdd(scope.row)"
              v-if="scope.row.menu_type !== 'F'" 
            >新增</el-button>
            <el-button 
              size="mini" 
              type="text" 
              class="btn-text-delete" 
              icon="el-icon-delete" 
              @click="handleDelete(scope.row)"
            >删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog :title="title" :visible.sync="open" width="680px" append-to-body>
      <el-form ref="form" :model="form" :rules="rules" label-width="100px">
        <el-row>
          <el-col :span="24">
            <el-form-item label="上级菜单">
               <el-select v-model="form.parent" placeholder="选择上级菜单" clearable style="width:100%">
                  <el-option label="主目录" :value="null"></el-option>
                  <el-option v-for="item in flatMenuList" :key="item.id" :label="item.title" :value="item.id" :disabled="item.menu_type === 'F'">
                    <span style="float: left">{{ item.title }}</span>
                    <span style="float: right; color: #8492a6; font-size: 13px">{{ item.menu_type === 'M' ? '目录' : '菜单' }}</span>
                  </el-option>
               </el-select>
            </el-form-item>
          </el-col>
          
          <el-col :span="24">
            <el-form-item label="菜单类型" prop="menu_type">
              <el-radio-group v-model="form.menu_type">
                <el-radio label="M">目录</el-radio>
                <el-radio label="C">菜单</el-radio>
                <el-radio label="F">按钮</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>

          <el-col :span="24">
            <el-form-item v-if="form.menu_type !== 'F'" label="菜单图标">
              <el-input v-model="form.icon" placeholder="请输入图标类名，如 el-icon-user" />
            </el-form-item>
          </el-col>

          <el-col :span="12">
            <el-form-item label="菜单名称" prop="title">
              <el-input v-model="form.title" placeholder="请输入菜单名称" />
            </el-form-item>
          </el-col>

          <el-col :span="12">
            <el-form-item label="显示排序" prop="order_num">
              <el-input-number v-model="form.order_num" controls-position="right" :min="0" />
            </el-form-item>
          </el-col>

          <el-col :span="12" v-if="form.menu_type !== 'F'">
            <el-form-item label="路由地址" prop="path">
              <el-input v-model="form.path" placeholder="请输入路由地址" />
            </el-form-item>
          </el-col>

          <el-col :span="12" v-if="form.menu_type === 'C'">
            <el-form-item label="组件路径" prop="component">
              <el-input v-model="form.component" placeholder="请输入组件路径" />
            </el-form-item>
          </el-col>

          <el-col :span="12" v-if="form.menu_type !== 'M'">
            <el-form-item label="权限标识">
              <el-input v-model="form.perms" placeholder="请输入权限标识" maxlength="100" />
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="submitForm">确 定</el-button>
        <el-button @click="cancel">取 消</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: "MenuList",
  data() {
    return {
      loading: true,
      menuList: [],
      flatMenuList: [], 
      title: "",
      open: false,
      queryParams: {
        title: undefined
      },
      form: {},
      rules: {
        title: [
          { required: true, message: "菜单名称不能为空", trigger: "blur" }
        ],
        order_num: [
          { required: true, message: "菜单顺序不能为空", trigger: "blur" }
        ],
        path: [
          { required: true, message: "路由地址不能为空", trigger: "blur" }
        ]
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
            // 菜单一般数据量不大，建议一次性拉取，前端做过滤，以保持树形结构完整
            const res = await this.$axios.get("system/menu/");
            this.menuList = res.data;
            this.flatMenuList = this.flattenMenu(res.data);
            
            // 如果有查询参数，执行前端过滤
            if (this.queryParams.title) {
               this.filterMenu(this.queryParams.title);
            }
          } finally {
            this.loading = false;
          }
        },
		// 前端树形过滤逻辑
		    filterMenu(keyword) {
		       if (!keyword) return;
		       // 简单的过滤：这里为了演示，如果数据量大建议用后端搜索
		       // 实际上，Element UI 的 Tree Table 不支持内置过滤，我们需要自己处理数据
		       // 这里简单处理：重新请求后端带参数（如果后端支持 title 过滤）
		       // 根据上面的后端代码，我们开启了 filterset_fields=['title']
		       
		       this.loading = true;
		       this.$axios.get("system/menu/", { params: { title: keyword } }).then(res => {
		          this.menuList = res.data;
		          this.loading = false;
		       });
		    },
			// 重置
			    resetQuery() {
			      this.queryParams = {};
			      this.fetchData(); // 重新拉取全量
			    },
    flattenMenu(list) {
      let res = [];
      list.forEach(item => {
        res.push(item);
        if (item.children && item.children.length > 0) {
          res = res.concat(this.flattenMenu(item.children));
        }
      });
      return res;
    },
    cancel() {
      this.open = false;
      this.reset();
    },
    reset() {
      this.form = {
        id: undefined,
        parent: null,
        title: undefined,
        icon: undefined,
        menu_type: "C", 
        order_num: 0
      };
      if (this.$refs.form) {
        this.$refs.form.resetFields();
      }
    },
    resetQuery() {
      this.queryParams = {};
      this.fetchData();
    },
    handleAdd(row) {
      this.reset();
      if (row != null && row.id) {
        this.form.parent = row.id;
      } else {
        this.form.parent = null;
      }
      this.title = "添加菜单";
      this.open = true;
    },
    handleEdit(row) {
      this.reset();
      this.form = JSON.parse(JSON.stringify(row));
      this.title = "修改菜单";
      this.open = true;
    },
    submitForm: function() {
      this.$refs["form"].validate(async valid => {
        if (valid) {
          if (this.form.id !== undefined) {
            await this.$axios.put(`system/menu/${this.form.id}/`, this.form);
            this.$message.success("修改成功");
          } else {
            await this.$axios.post("system/menu/", this.form);
            this.$message.success("新增成功");
          }
          this.open = false;
          this.fetchData();
        }
      });
    },
    handleDelete(row) {
      this.$confirm('是否确认删除名称为"' + row.title + '"的数据项?', "警告", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning"
      }).then(async () => {
        await this.$axios.delete(`system/menu/${row.id}/`);
        this.fetchData();
        this.$message.success("删除成功");
      }).catch(() => {});
    }
  }
};
</script>

<style lang="scss" scoped>
.app-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.search-card {
  border: none;
  .el-form-item { margin-bottom: 0; }
}
.table-card {
  border: none;
}
.table-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  .left-title {
    font-size: 14px;
    color: #67C23A;
    background: #f0f9eb;
    padding: 5px 10px;
    border: 1px solid #c2e7b0;
    border-radius: 3px;
  }
}
.btn-text-edit { color: #67C23A; }
.btn-text-add { color: #1890ff; }
.btn-text-delete { color: #F56C6C; }
</style>