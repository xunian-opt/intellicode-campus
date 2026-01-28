<template>
  <div class="page-container">
    <el-card shadow="never">
      <div style="margin-bottom:15px; display:flex; justify-content:space-between;">
        <span style="font-size:18px; font-weight:bold;">试卷管理 / 组卷</span>
        <el-button type="primary" icon="el-icon-plus" @click="handleAdd">新建试卷</el-button>
      </div>
      <el-table :data="tableData" border stripe v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" align="center"></el-table-column>
        <el-table-column prop="title" label="试卷标题"></el-table-column>
        <el-table-column label="题目统计" align="center">
          <template slot-scope="scope">
            <el-tag size="small">选择题: {{ scope.row.choice_count }}</el-tag>
            <el-tag size="small" type="success" style="margin-left:5px;">编程题: {{ scope.row.prog_count }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="duration" label="时长(分)" width="100" align="center"></el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="160" align="center">
           <template slot-scope="scope">{{ new Date(scope.row.created_at).toLocaleString() }}</template>
        </el-table-column>
        <el-table-column label="操作" width="200" align="center">
          <template slot-scope="scope">
            <el-button type="text" @click="handleEdit(scope.row)">编辑组卷</el-button>
            <el-button type="text" style="color:red;" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog :title="title" :visible.sync="open" fullscreen append-to-body :close-on-click-modal="false">
      <div style="padding: 0 20px;">
        <el-form ref="form" :model="form" :rules="rules" label-width="100px" inline style="border-bottom:1px solid #eee; margin-bottom:20px;">
          <el-form-item label="试卷标题" prop="title">
            <el-input v-model="form.title" placeholder="例如: 期末考试A卷" style="width:300px;" />
          </el-form-item>
          <el-form-item label="考试时长" prop="duration">
            <el-input-number v-model="form.duration" :min="10" label="分钟"></el-input-number>
          </el-form-item>
          <el-form-item label="总分" prop="total_score">
            <el-input-number v-model="form.total_score" :min="10"></el-input-number>
          </el-form-item>
        </el-form>

        <el-row :gutter="20" style="height: calc(100vh - 200px);">
          <el-col :span="12" style="height:100%; display:flex; flex-direction:column;">
            <el-tabs v-model="activeTab" type="card">
              <el-tab-pane label="选择题库" name="choice"></el-tab-pane>
              <el-tab-pane label="编程题库" name="program"></el-tab-pane>
            </el-tabs>
            <div style="flex:1; overflow:auto; border:1px solid #e4e7ed; padding:10px;">
              <div v-show="activeTab === 'choice'">
                <el-input placeholder="搜索选择题" v-model="searchChoice" size="small" suffix-icon="el-icon-search" style="margin-bottom:10px;"></el-input>
                <el-table :data="filteredChoices" size="small" @selection-change="handleChoiceSelection">
                  <el-table-column type="selection" width="55"></el-table-column>
                  <el-table-column prop="title" label="题干" show-overflow-tooltip></el-table-column>
                  <el-table-column prop="difficulty" label="难度" width="80"></el-table-column>
                </el-table>
              </div>
              <div v-show="activeTab === 'program'">
                <el-input placeholder="搜索编程题" v-model="searchProg" size="small" suffix-icon="el-icon-search" style="margin-bottom:10px;"></el-input>
                <el-table :data="filteredProgs" size="small" @selection-change="handleProgSelection">
                  <el-table-column type="selection" width="55"></el-table-column>
                  <el-table-column prop="title" label="题目名称" show-overflow-tooltip></el-table-column>
                  <el-table-column prop="difficulty" label="难度" width="80"></el-table-column>
                </el-table>
              </div>
            </div>
          </el-col>

          <el-col :span="12" style="height:100%; display:flex; flex-direction:column;">
            <div style="background:#f5f7fa; padding:10px; border:1px solid #e4e7ed; flex:1; overflow:auto;">
              <h3 style="margin-top:0;">试卷预览</h3>
              <div style="margin-bottom:20px;">
                <h4>一、选择题 (共 {{ form.choice_problems.length }} 题)</h4>
                <div v-for="(id, idx) in form.choice_problems" :key="'c'+id" style="font-size:13px; margin-bottom:5px; color:#606266;">
                  {{ idx + 1 }}. {{ getChoiceTitle(id) }}
                </div>
              </div>
              <div>
                <h4>二、编程题 (共 {{ form.programming_problems.length }} 题)</h4>
                <div v-for="(id, idx) in form.programming_problems" :key="'p'+id" style="font-size:13px; margin-bottom:5px; color:#606266;">
                  {{ idx + 1 }}. {{ getProgTitle(id) }}
                </div>
              </div>
            </div>
          </el-col>
        </el-row>
      </div>
      <div slot="footer">
        <el-button @click="open = false">关 闭</el-button>
        <el-button type="primary" :loading="submitLoading" @click="submitForm">保存试卷</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: "ExamPaperList",
  data() {
    return {
      loading: false,
      submitLoading: false, // 🟢 新增
      tableData: [],
      open: false,
      title: "",
      form: { choice_problems: [], programming_problems: [] },
      rules: { title: [{ required: true, message: "必填" }] },
      
      activeTab: 'choice',
      allChoices: [],
      allProgs: [],
      searchChoice: '',
      searchProg: '',
      
      selectedChoiceRows: [],
      selectedProgRows: []
    };
  },
  computed: {
    filteredChoices() {
      return this.allChoices.filter(i => i.title.includes(this.searchChoice));
    },
    filteredProgs() {
      return this.allProgs.filter(i => i.title.includes(this.searchProg));
    }
  },
  created() {
    this.fetchData();
    this.fetchAllQuestions(); 
  },
  methods: {
    async fetchData() {
      this.loading = true;
      const res = await this.$axios.get('exam_papers/');
      this.tableData = res.data.results || res.data;
      this.loading = false;
    },
    async fetchAllQuestions() {
      const [resC, resP] = await Promise.all([
        this.$axios.get('choice_problems/?page_size=1000'),
        this.$axios.get('problems/?page_size=1000')
      ]);
      this.allChoices = resC.data.results || resC.data;
      this.allProgs = resP.data.results || resP.data;
    },
    handleAdd() {
      this.form = { duration: 90, total_score: 100, choice_problems: [], programming_problems: [] };
      this.title = "新建试卷";
      this.open = true;
    },
    handleEdit(row) {
      this.form = JSON.parse(JSON.stringify(row));
      this.title = "编辑试卷";
      this.open = true;
    },
    handleChoiceSelection(val) {
      this.form.choice_problems = val.map(v => v.id);
    },
    handleProgSelection(val) {
      this.form.programming_problems = val.map(v => v.id);
    },
    getChoiceTitle(id) {
      const q = this.allChoices.find(i => i.id === id);
      return q ? q.title : `题目ID:${id}`;
    },
    getProgTitle(id) {
      const q = this.allProgs.find(i => i.id === id);
      return q ? q.title : `题目ID:${id}`;
    },
    async submitForm() {
      this.$refs["form"].validate(async valid => {
        if (valid) {
          this.submitLoading = true; // 🟢 开启
          try {
            const api = this.form.id ? this.$axios.patch : this.$axios.post;
            const url = this.form.id ? `exam_papers/${this.form.id}/` : 'exam_papers/';
            await api(url, this.form);
            this.$message.success("试卷保存成功");
            this.open = false;
            this.fetchData();
          } catch(e) {
            console.error(e);
          } finally {
            this.submitLoading = false; // 🟢 关闭
          }
        }
      });
    },
    handleDelete(row) {
      this.$confirm('确认删除?').then(async () => {
        await this.$axios.delete(`exam_papers/${row.id}/`);
        this.fetchData();
      });
    }
  }
};
</script>