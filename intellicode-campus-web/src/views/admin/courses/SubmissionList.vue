<template>
  <div class="page-container">
    <el-card class="search-card" shadow="never">
      <el-form :inline="true" :model="queryForm" size="small">
        <el-form-item label="所属作业">
          <el-select v-model="queryForm.assignment" placeholder="全部作业" clearable filterable @change="fetchData">
            <el-option
              v-for="item in assignmentList"
              :key="item.id"
              :label="item.title"
              :value="item.id">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="批改状态">
          <el-select v-model="queryForm.is_graded" placeholder="全部" clearable @change="fetchData" style="width: 100px">
            <el-option label="已批改" :value="true"></el-option>
            <el-option label="未批改" :value="false"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="学生姓名">
          <el-input 
            v-model="queryForm.student_name" 
            placeholder="输入学生姓名搜索" 
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
      <el-table 
        :data="tableData" 
        border 
        stripe 
        v-loading="loading" 
        empty-text="暂无数据"
      >
        <el-table-column prop="id" label="ID" width="80" align="center"></el-table-column>
        <el-table-column prop="assignment" label="作业标题" show-overflow-tooltip>
           <template slot-scope="scope">
             {{ getAssignmentTitle(scope.row.assignment) }}
           </template>
        </el-table-column>
        <el-table-column prop="student_name" label="提交学生" width="120" align="center"></el-table-column>
        <el-table-column prop="submit_time" label="提交时间" width="160" align="center">
           <template slot-scope="scope">{{ formatTime(scope.row.submit_time) }}</template>
        </el-table-column>
        <el-table-column prop="is_graded" label="状态" width="100" align="center">
           <template slot-scope="scope">
             <el-tag v-if="scope.row.is_graded" type="success">已批改</el-tag>
             <el-tag v-else type="warning">未批改</el-tag>
           </template>
        </el-table-column>
        <el-table-column prop="score" label="得分" width="100" align="center">
           <template slot-scope="scope">
             <span v-if="scope.row.score !== null" style="font-weight:bold; color:#67C23A">{{ scope.row.score }}</span>
             <span v-else>-</span>
           </template>
        </el-table-column>
        
        <el-table-column label="操作" width="150" align="center">
          <template slot-scope="scope">
            <el-button 
              type="text" 
              icon="el-icon-edit-outline" 
              class="btn-edit"
              @click="handleGrade(scope.row)"
            >批改打分</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog title="作业批改" :visible.sync="open" width="500px" append-to-body>
      <el-form ref="form" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="学生姓名">
          <el-input v-model="form.student_name" disabled />
        </el-form-item>
        <el-form-item label="作业内容">
           <div style="padding: 5px 0; line-height: 1.5; color: #606266;">
             {{ form.content || '无文本内容' }}
           </div>
           <div v-if="form.file" style="margin-top: 5px;">
             <a :href="form.file" target="_blank" style="color: #409EFF; text-decoration: none;">
               <i class="el-icon-document"></i> 下载/预览附件
             </a>
           </div>
        </el-form-item>
        <el-form-item label="给予评分" prop="score">
          <el-input-number v-model="form.score" :min="0" :max="100" :precision="1" style="width: 100%;"></el-input-number>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="submitGrade">确认打分</el-button>
        <el-button @click="open = false">取 消</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: "SubmissionList",
  data() {
    return {
      loading: true,
      tableData: [],
      assignmentList: [], // 用于筛选的作业列表
      open: false,
      queryForm: { 
        assignment: undefined,
        student_name: "",
        is_graded: undefined
      },
      form: {},
      rules: {
        score: [{ required: true, message: "请输入分数", trigger: "blur" }]
      }
    };
  },
  created() {
    this.fetchData();
    this.getAssignments();
  },
  methods: {
    async fetchData() {
      this.loading = true;
      try {
        const params = {};
        if (this.queryForm.student_name) params.search = this.queryForm.student_name;
        if (this.queryForm.assignment) params.assignment = this.queryForm.assignment;
        if (this.queryForm.is_graded !== undefined && this.queryForm.is_graded !== "") {
            params.is_graded = this.queryForm.is_graded;
        }
        
        const res = await this.$axios.get('submissions/', { params });
        this.tableData = res.data;
      } finally {
        this.loading = false;
      }
    },
    async getAssignments() {
      const res = await this.$axios.get('assignments/');
      this.assignmentList = res.data;
    },
    getAssignmentTitle(id) {
      const item = this.assignmentList.find(a => a.id === id);
      return item ? item.title : id;
    },
    resetQuery() {
      this.queryForm = { 
        assignment: undefined, 
        student_name: "", 
        is_graded: undefined 
      };
      this.fetchData();
    },
    handleGrade(row) {
      this.form = { ...row };
      this.open = true;
    },
    submitGrade() {
      this.$refs["form"].validate(async valid => {
        if (valid) {
          // 提交打分，同时将状态改为已批改
          const payload = {
            score: this.form.score,
            is_graded: true
          };
          await this.$axios.patch(`submissions/${this.form.id}/`, payload);
          this.$message.success("批改完成");
          this.open = false;
          this.fetchData();
        }
      });
    },
    formatTime(time) {
      if(!time) return '';
      return new Date(time).toLocaleString();
    }
  }
};
</script>

<style scoped>
/* 修正点：去除了 .page-container 的 padding */
.btn-edit {
  color: #67C23A;
}
.search-card {
  border: none;
}
.table-card {
  border: none;
}
</style>