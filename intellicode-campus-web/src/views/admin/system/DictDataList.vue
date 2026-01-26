<template>
  <div class="page-container">
    <el-card shadow="never" class="search-card">
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <el-page-header @back="goBack" :content="dictName + ' - 数据管理'" title="返回列表"></el-page-header>
        <div>
           <el-button type="success" icon="el-icon-plus" size="small" @click="handleAdd">新增数据</el-button>
           <el-button icon="el-icon-refresh" size="small" @click="fetchData">刷新</el-button>
        </div>
      </div>
    </el-card>

    <el-card shadow="never" class="table-card" style="margin-top:20px;">
      <el-table :data="tableData" border stripe v-loading="loading">
        <el-table-column prop="label" label="字典标签" align="center"></el-table-column>
        <el-table-column prop="value" label="字典键值" align="center">
           <template slot-scope="scope">
              <el-tag size="medium">{{ scope.row.value }}</el-tag>
           </template>
        </el-table-column>
        <el-table-column prop="sort" label="排序" align="center" width="100"></el-table-column>
        <el-table-column prop="is_default" label="默认" align="center" width="100">
          <template slot-scope="scope">
             <el-tag v-if="scope.row.is_default" type="success" effect="dark">默认</el-tag>
             <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" align="center" width="180">
          <template slot-scope="scope">
            <el-button type="text" style="color:#67C23A" icon="el-icon-edit" @click="handleEdit(scope.row)">修改</el-button>
            <el-button type="text" style="color:#F56C6C" icon="el-icon-delete" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog :title="title" :visible.sync="open" width="500px" append-to-body>
      <el-form ref="form" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="字典标签" prop="label">
          <el-input v-model="form.label" placeholder="例如: 算法竞赛" />
        </el-form-item>
        <el-form-item label="字典键值" prop="value">
          <el-input v-model="form.value" placeholder="例如: algorithm" />
        </el-form-item>
        <el-form-item label="显示排序" prop="sort">
          <el-input-number v-model="form.sort" :min="0" controls-position="right"></el-input-number>
        </el-form-item>
        <el-form-item label="系统默认">
           <el-switch v-model="form.is_default"></el-switch>
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
  name: "DictDataList",
  data() {
    return {
      loading: false,
      tableData: [],
      open: false,
      title: "",
      dictId: null,   // 当前所属的字典类型ID
      dictName: "",   // 字典类型名称（用于显示）
      form: {},
      rules: {
        label: [{ required: true, message: "标签不能为空", trigger: "blur" }],
        value: [{ required: true, message: "键值不能为空", trigger: "blur" }]
      }
    };
  },
  created() {
    // 从路由参数中获取 dictId
    // 例如：/system/dict-data?dictId=1&dictName=竞赛类型
    this.dictId = this.$route.query.dictId;
    this.dictName = this.$route.query.dictName || '字典';
    
    if (this.dictId) {
      this.fetchData();
    } else {
      this.$message.error("缺少字典类型ID");
      this.goBack();
    }
  },
  methods: {
    async fetchData() {
      this.loading = true;
      try {
        // 🟢 [关键修改] 请求路径已改为 dict-data/，不再是 system/dict/data/
        const res = await this.$axios.get('dict-data/', { 
            params: { dict_type: this.dictId } 
        });
        this.tableData = res.data;
      } finally {
        this.loading = false;
      }
    },
    goBack() {
      // 返回上一页 (DictList)
      this.$router.go(-1);
    },
    handleAdd() {
      this.form = { 
          dict_type: this.dictId, // 自动关联当前类型ID
          sort: 0, 
          is_default: false 
      };
      this.title = "新增字典数据";
      this.open = true;
    },
    handleEdit(row) {
      this.form = { ...row };
      this.title = "修改字典数据";
      this.open = true;
    },
    submitForm() {
      this.$refs["form"].validate(async valid => {
        if (valid) {
          // 🟢 [关键修改] 请求路径已改为 dict-data/
          if (this.form.id) {
            await this.$axios.patch(`dict-data/${this.form.id}/`, this.form);
            this.$message.success("修改成功");
          } else {
            await this.$axios.post('dict-data/', this.form);
            this.$message.success("新增成功");
          }
          this.open = false;
          this.fetchData();
        }
      });
    },
    handleDelete(row) {
      this.$confirm('确认删除?', '警告', { type: 'warning' }).then(async () => {
        // 🟢 [关键修改] 请求路径已改为 dict-data/
        await this.$axios.delete(`dict-data/${row.id}/`);
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