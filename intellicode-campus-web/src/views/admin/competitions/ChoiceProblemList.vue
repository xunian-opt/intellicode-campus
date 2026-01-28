<template>
  <div class="page-container">
    <el-card shadow="never" class="search-card">
      <el-form :inline="true" :model="queryForm" size="small">
        <el-form-item label="题干">
          <el-input v-model="queryForm.title" placeholder="输入题干关键词" clearable @keyup.enter.native="fetchData"/>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchData">查询</el-button>
          <el-button icon="el-icon-plus" type="success" @click="handleAdd">新增选择题</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card shadow="never" style="margin-top:20px;">
      <el-table :data="tableData" border stripe v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" align="center"></el-table-column>
        <el-table-column prop="title" label="题干" show-overflow-tooltip></el-table-column>
        <el-table-column prop="difficulty" label="难度" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="scope.row.difficulty==='Easy'?'success':(scope.row.difficulty==='Medium'?'warning':'danger')">
              {{ scope.row.difficulty }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="correct_option" label="正确答案" width="100" align="center"></el-table-column>
        <el-table-column label="操作" width="180" align="center">
          <template slot-scope="scope">
            <el-button type="text" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button type="text" style="color:red" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog :title="title" :visible.sync="open" width="600px" append-to-body>
      <el-form ref="form" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="题干" prop="title">
          <el-input type="textarea" v-model="form.title" placeholder="请输入题目内容" />
        </el-form-item>
        <el-form-item label="难度" prop="difficulty">
          <el-select v-model="form.difficulty" style="width:100%">
            <el-option label="简单" value="Easy"></el-option>
            <el-option label="中等" value="Medium"></el-option>
            <el-option label="困难" value="Hard"></el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item label="选项">
          <div v-for="(opt, index) in form.options" :key="index" style="margin-bottom:10px; display:flex;">
            <el-input v-model="opt.key" style="width:60px; margin-right:10px;" placeholder="选项"></el-input>
            <el-input v-model="opt.value" placeholder="选项内容"></el-input>
            <el-button type="text" style="color:red; margin-left:5px;" @click="removeOption(index)">删除</el-button>
          </div>
          <el-button type="text" icon="el-icon-plus" @click="addOption">添加选项</el-button>
        </el-form-item>

        <el-form-item label="正确答案" prop="correct_option">
          <el-input v-model="form.correct_option" placeholder="例如: A" />
        </el-form-item>
        <el-form-item label="分值" prop="score">
          <el-input-number v-model="form.score" :min="1" />
        </el-form-item>
      </el-form>
      <div slot="footer">
        <el-button type="primary" @click="submitForm">确 定</el-button>
        <el-button @click="open = false">取 消</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: "ChoiceProblemList",
  data() {
    return {
      loading: true,
      tableData: [],
      open: false,
      title: "",
      queryForm: { title: "" },
      form: { options: [] },
      rules: {
        title: [{ required: true, message: "必填", trigger: "blur" }],
        correct_option: [{ required: true, message: "必填", trigger: "blur" }]
      }
    };
  },
  created() { this.fetchData(); },
  methods: {
    async fetchData() {
      this.loading = true;
      try {
        const res = await this.$axios.get('choice_problems/', { params: { search: this.queryForm.title } });
        this.tableData = res.data.results || res.data;
      } finally { this.loading = false; }
    },
    handleAdd() {
      this.form = { 
        difficulty: 'Easy', 
        score: 5, 
        options: [
          { key: 'A', value: '' }, 
          { key: 'B', value: '' },
          { key: 'C', value: '' },
          { key: 'D', value: '' }
        ] 
      };
      this.title = "新增选择题";
      this.open = true;
    },
    handleEdit(row) {
      // 深拷贝防止修改影响表格
      this.form = JSON.parse(JSON.stringify(row));
      this.title = "编辑选择题";
      this.open = true;
    },
    addOption() {
      this.form.options.push({ key: '', value: '' });
    },
    removeOption(index) {
      this.form.options.splice(index, 1);
    },
    async submitForm() {
      this.$refs["form"].validate(async valid => {
        if (valid) {
          const api = this.form.id ? this.$axios.patch : this.$axios.post;
          const url = this.form.id ? `choice_problems/${this.form.id}/` : 'choice_problems/';
          await api(url, this.form);
          this.$message.success("操作成功");
          this.open = false;
          this.fetchData();
        }
      });
    },
    handleDelete(row) {
      this.$confirm('确认删除?', '提示').then(async () => {
        await this.$axios.delete(`choice_problems/${row.id}/`);
        this.fetchData();
      });
    }
  }
};
</script>