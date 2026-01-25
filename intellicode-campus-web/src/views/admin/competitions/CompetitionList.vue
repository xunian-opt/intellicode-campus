<template>
  <div class="page-container">
    <el-card class="search-card" shadow="never">
      <el-form :inline="true" :model="queryForm" size="small">
        <el-form-item label="竞赛名称">
          <el-input 
            v-model="queryForm.title" 
            placeholder="请输入竞赛名称" 
            clearable 
            @keyup.enter.native="fetchData"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchData">查询</el-button>
          <el-button icon="el-icon-refresh" @click="resetQuery">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="table-card" shadow="never" style="margin-top:20px;">
      <div class="table-toolbar" style="margin-bottom:15px;">
        <el-button type="success" icon="el-icon-plus" size="small" @click="handleAdd">新增竞赛</el-button>
      </div>

      <el-table :data="tableData" border stripe v-loading="loading" empty-text="暂无数据">
        <el-table-column prop="id" label="ID" width="80" align="center"></el-table-column>
        <el-table-column prop="title" label="竞赛名称" show-overflow-tooltip></el-table-column>
        <el-table-column label="起止时间" width="300" align="center">
          <template slot-scope="scope">
            <div>{{ formatTime(scope.row.start_time) }}</div>
            <div style="color: #909399; font-size: 12px;">至</div>
            <div>{{ formatTime(scope.row.end_time) }}</div>
          </template>
        </el-table-column>
        <el-table-column prop="problems" label="题目数量" width="100" align="center">
           <template slot-scope="scope">{{ scope.row.problems ? scope.row.problems.length : 0 }}</template>
        </el-table-column>
        <el-table-column label="操作" width="200" align="center">
          <template slot-scope="scope">
            <el-button type="text" class="btn-edit" icon="el-icon-edit" @click="handleEdit(scope.row)">修改</el-button>
            <el-button type="text" class="btn-delete" style="color:red;" icon="el-icon-delete" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog :title="title" :visible.sync="open" width="600px" append-to-body>
      <el-form ref="form" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="竞赛名称" prop="title">
          <el-input v-model="form.title" placeholder="请输入竞赛名称" />
        </el-form-item>
        <el-form-item label="开始时间" prop="start_time">
          <el-date-picker v-model="form.start_time" type="datetime" placeholder="选择开始时间" style="width: 100%;" value-format="yyyy-MM-dd HH:mm:ss" />
        </el-form-item>
        <el-form-item label="结束时间" prop="end_time">
          <el-date-picker v-model="form.end_time" type="datetime" placeholder="选择结束时间" style="width: 100%;" value-format="yyyy-MM-dd HH:mm:ss" />
        </el-form-item>
        <el-form-item label="包含题目" prop="problems">
           <el-select v-model="form.problems" multiple placeholder="请选择题目" style="width: 100%">
             <el-option
               v-for="item in problemOptions"
               :key="item.id"
               :label="item.title"
               :value="item.id">
               <span style="float: left">{{ item.title }}</span>
               <span style="float: right; color: #8492a6; font-size: 13px">{{ item.difficulty }}</span>
             </el-option>
           </el-select>
        </el-form-item>
        <el-form-item label="竞赛规则" prop="description">
          <el-input type="textarea" :rows="4" v-model="form.description" placeholder="请输入竞赛规则说明" />
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
  name: "CompetitionList",
  data() {
    return {
      loading: true,
      tableData: [],
      problemOptions: [],
      open: false,
      title: "",
      queryForm: { title: "" },
      form: {},
      rules: {
        title: [{ required: true, message: "必填项", trigger: "blur" }],
        start_time: [{ required: true, message: "必填项", trigger: "change" }],
        end_time: [{ required: true, message: "必填项", trigger: "change" }]
      }
    };
  },
  created() {
    this.fetchData();
    this.getProblems();
  },
  methods: {
    async fetchData() {
      this.loading = true;
      try {
        const params = {};
        if (this.queryForm.title) params.search = this.queryForm.title;
        const res = await this.$axios.get('competitions/', { params });
        this.tableData = res.data;
      } finally {
        this.loading = false;
      }
    },
    async getProblems() {
      const res = await this.$axios.get('problems/');
      this.problemOptions = res.data;
    },
    resetQuery() {
      this.queryForm = { title: "" };
      this.fetchData();
    },
    handleAdd() {
      this.form = { problems: [] };
      this.title = "新增竞赛";
      this.open = true;
    },
    handleEdit(row) {
      // 提取题目ID列表用于回显
      const problemIds = row.problems.map(p => p.id);
      this.form = { ...row, problems: problemIds };
      this.title = "修改竞赛";
      this.open = true;
    },
    submitForm() {
      this.$refs["form"].validate(async valid => {
        if (valid) {
          if (this.form.id) {
            await this.$axios.patch(`competitions/${this.form.id}/`, this.form);
            this.$message.success("修改成功");
          } else {
            await this.$axios.post('competitions/', this.form);
            this.$message.success("新增成功");
          }
          this.open = false;
          this.fetchData();
        }
      });
    },
    handleDelete(row) {
      this.$confirm('确认删除?', '警告', { type: 'warning' }).then(async () => {
        await this.$axios.delete(`competitions/${row.id}/`);
        this.$message.success("删除成功");
        this.fetchData();
      }).catch(() => {});
    },
    formatTime(time) {
      return time ? new Date(time).toLocaleString() : '';
    }
  }
};
</script>

<style scoped>
.btn-edit { color: #67C23A; }
.search-card { border: none; }
.table-card { border: none; }
</style>