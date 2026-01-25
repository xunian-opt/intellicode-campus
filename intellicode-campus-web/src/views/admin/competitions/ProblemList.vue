<template>
  <div class="page-container">
    <el-card class="search-card" shadow="never">
      <el-form :inline="true" :model="queryForm" size="small">
        <el-form-item label="题目名称">
          <el-input 
            v-model="queryForm.title" 
            placeholder="请输入题目名称" 
            clearable 
            @keyup.enter.native="fetchData"
          />
        </el-form-item>
        <el-form-item label="难度">
          <el-select v-model="queryForm.difficulty" placeholder="全部" clearable @change="fetchData">
            <el-option label="简单" value="Easy"></el-option>
            <el-option label="中等" value="Medium"></el-option>
            <el-option label="困难" value="Hard"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchData">查询</el-button>
          <el-button icon="el-icon-refresh" @click="resetQuery">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="table-card" shadow="never" style="margin-top:20px;">
      <div class="table-toolbar" style="margin-bottom:15px;">
        <el-button type="success" icon="el-icon-plus" size="small" @click="handleAdd">新增题目</el-button>
      </div>

      <el-table :data="tableData" border stripe v-loading="loading" empty-text="暂无数据">
        <el-table-column prop="id" label="ID" width="80" align="center"></el-table-column>
        <el-table-column prop="title" label="题目名称" show-overflow-tooltip></el-table-column>
        <el-table-column prop="difficulty" label="难度" width="100" align="center">
          <template slot-scope="scope">
            <el-tag v-if="scope.row.difficulty === 'Easy'" type="success">简单</el-tag>
            <el-tag v-else-if="scope.row.difficulty === 'Medium'" type="warning">中等</el-tag>
            <el-tag v-else type="danger">困难</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="time_limit" label="时间限制" width="120" align="center">
           <template slot-scope="scope">{{ scope.row.time_limit }} ms</template>
        </el-table-column>
        <el-table-column prop="memory_limit" label="内存限制" width="120" align="center">
           <template slot-scope="scope">{{ scope.row.memory_limit }} MB</template>
        </el-table-column>
        <el-table-column label="操作" width="200" align="center">
          <template slot-scope="scope">
            <el-button type="text" class="btn-edit" icon="el-icon-edit" @click="handleEdit(scope.row)">修改</el-button>
            <el-button type="text" class="btn-delete" style="color:red;" icon="el-icon-delete" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog :title="title" :visible.sync="open" width="700px" append-to-body>
      <el-form ref="form" :model="form" :rules="rules" label-width="100px">
        <el-row>
          <el-col :span="12">
            <el-form-item label="题目名称" prop="title">
              <el-input v-model="form.title" placeholder="请输入题目名称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="难度" prop="difficulty">
              <el-select v-model="form.difficulty" placeholder="请选择" style="width:100%">
                <el-option label="简单" value="Easy"></el-option>
                <el-option label="中等" value="Medium"></el-option>
                <el-option label="困难" value="Hard"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="时间限制(ms)" prop="time_limit">
              <el-input-number v-model="form.time_limit" :min="100" :step="100" style="width:100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="内存限制(MB)" prop="memory_limit">
              <el-input-number v-model="form.memory_limit" :min="16" :step="16" style="width:100%" />
            </el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item label="题目描述" prop="content">
              <el-input type="textarea" :rows="5" v-model="form.content" placeholder="支持 Markdown 格式" />
            </el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item label="测试用例" prop="test_cases_str">
              <el-input type="textarea" :rows="5" v-model="form.test_cases_str" placeholder='JSON格式, 例如: [{"input": "1 2", "output": "3"}]' />
            </el-form-item>
          </el-col>
        </el-row>
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
  name: "ProblemList",
  data() {
    return {
      loading: true,
      tableData: [],
      open: false,
      title: "",
      queryForm: { title: "", difficulty: "" },
      form: {},
      rules: {
        title: [{ required: true, message: "必填项", trigger: "blur" }],
        content: [{ required: true, message: "必填项", trigger: "blur" }]
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
        const params = {};
        if (this.queryForm.title) params.search = this.queryForm.title;
        if (this.queryForm.difficulty) params.difficulty = this.queryForm.difficulty;
        const res = await this.$axios.get('problems/', { params });
        this.tableData = res.data;
      } finally {
        this.loading = false;
      }
    },
    resetQuery() {
      this.queryForm = { title: "", difficulty: "" };
      this.fetchData();
    },
    handleAdd() {
      this.form = { 
        difficulty: "Easy", 
        time_limit: 1000, 
        memory_limit: 256,
        test_cases_str: '[]' 
      };
      this.title = "新增题目";
      this.open = true;
    },
    handleEdit(row) {
      // 将 JSON 对象转为字符串方便编辑
      const strCases = JSON.stringify(row.test_cases, null, 2);
      this.form = { ...row, test_cases_str: strCases };
      this.title = "修改题目";
      this.open = true;
    },
    submitForm() {
      this.$refs["form"].validate(async valid => {
        if (valid) {
          try {
            // 将字符串转回 JSON
            this.form.test_cases = JSON.parse(this.form.test_cases_str);
          } catch (e) {
            this.$message.error("测试用例格式错误，必须是有效的 JSON");
            return;
          }

          if (this.form.id) {
            await this.$axios.patch(`problems/${this.form.id}/`, this.form);
            this.$message.success("修改成功");
          } else {
            await this.$axios.post('problems/', this.form);
            this.$message.success("新增成功");
          }
          this.open = false;
          this.fetchData();
        }
      });
    },
    handleDelete(row) {
      this.$confirm('确认删除?', '警告', { type: 'warning' }).then(async () => {
        await this.$axios.delete(`problems/${row.id}/`);
        this.$message.success("删除成功");
        this.fetchData();
      }).catch(() => {});
    }
  }
};
</script>

<style scoped>
.btn-edit { color: #67C23A; }
.search-card { border: none; }
.table-card { border: none; }
</style>