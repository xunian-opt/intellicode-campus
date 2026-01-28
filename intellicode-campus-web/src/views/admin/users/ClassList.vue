<template>
  <div class="page-container">
    <el-card shadow="never" class="search-card">
      <el-form :inline="true" :model="queryForm" size="small">
        <el-form-item label="班级名称">
          <el-input 
            v-model="queryForm.name" 
            placeholder="输入班级名称搜索" 
            clearable 
            @keyup.enter.native="fetchData"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="el-icon-search" :loading="loading" @click="fetchData">查询</el-button>
          <el-button icon="el-icon-refresh" @click="resetQuery">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card shadow="never" class="table-card" style="margin-top:20px">
      <div class="table-toolbar" style="margin-bottom: 15px;">
        <el-button type="success" icon="el-icon-plus" size="small" @click="handleAdd">新建班级</el-button>
      </div>
      <el-table :data="tableData" border stripe v-loading="loading">
         <el-table-column prop="id" label="ID" width="80" align="center"></el-table-column>
         <el-table-column prop="name" label="班级名称" align="center"></el-table-column>
         <el-table-column prop="teacher_name" label="班主任" align="center">
            <template slot-scope="scope">
              <el-tag v-if="scope.row.teacher_name" size="small">{{ scope.row.teacher_name }}</el-tag>
              <span v-else class="text-gray">-</span>
            </template>
         </el-table-column>
         <el-table-column prop="student_count" label="学生人数" align="center" width="120">
           <template slot-scope="scope">
             <el-tag type="info" effect="plain">{{ scope.row.student_count || 0 }} 人</el-tag>
           </template>
         </el-table-column>
         <el-table-column prop="created_at" label="创建时间" align="center" width="180">
            <template slot-scope="scope">{{ formatTime(scope.row.created_at) }}</template>
         </el-table-column>
         <el-table-column label="操作" align="center" width="300">
           <template slot-scope="scope">
             <el-button type="text" icon="el-icon-edit" @click="handleEdit(scope.row)">编辑</el-button>
             <el-button type="text" icon="el-icon-user" @click="handleStudents(scope.row)">学生管理</el-button>
             <el-button type="text" style="color:red" icon="el-icon-delete" @click="handleDelete(scope.row)">删除</el-button>
           </template>
         </el-table-column>
      </el-table>
    </el-card>

    <el-dialog :title="title" :visible.sync="open" width="500px" append-to-body :close-on-click-modal="false">
      <el-form :model="form" label-width="80px" :rules="rules" ref="form">
        <el-form-item label="班级名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入班级名称"></el-input>
        </el-form-item>
        <el-form-item label="班主任" prop="teacher">
          <el-select v-model="form.teacher" placeholder="选择教师" style="width:100%" filterable clearable>
            <el-option v-for="t in teachers" :key="t.id" :label="t.nickname || t.username" :value="t.id"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer">
        <el-button @click="open = false">取 消</el-button>
        <el-button type="primary" :loading="submitLoading" @click="submitForm">确 定</el-button>
      </div>
    </el-dialog>

    <el-dialog :title="'管理学生 - ' + currentClassName" :visible.sync="studentOpen" width="900px" append-to-body top="5vh">
       <div style="margin-bottom: 15px; display: flex; justify-content: space-between;">
        <el-input 
          v-model="studentQuery" 
          placeholder="在此处输入姓名或学号筛选列表..." 
          prefix-icon="el-icon-search" 
          clearable
          size="small"
          style="width: 300px;"
        ></el-input>
        
        <el-alert
          title="提示：列表中展示所有学生，点击右侧按钮即可加入或移出本班"
          type="info"
          :closable="false"
          show-icon
          style="width: 450px; padding: 5px;"
        ></el-alert>
      </div>

      <el-table :data="filteredStudentData" border height="500" v-loading="studentLoading" stripe>
        <el-table-column prop="username" label="学号" width="130" align="center"></el-table-column>
        <el-table-column prop="nickname" label="姓名" width="130" align="center"></el-table-column>
        <el-table-column prop="phone" label="手机号" align="center"></el-table-column>
        
        <el-table-column label="当前状态" align="center" width="180">
          <template slot-scope="scope">
            <el-tag v-if="scope.row.class_info === currentClassId" type="success" effect="dark">
              <i class="el-icon-check"></i> 本班学生
            </el-tag>
            <el-tag v-else-if="scope.row.class_info" type="info" effect="plain">
              已在: {{ scope.row.display_class_name }}
            </el-tag>
            <el-tag v-else type="warning" effect="plain">暂无班级</el-tag>
          </template>
        </el-table-column>

        <el-table-column label="操作" align="center" width="120">
          <template slot-scope="scope">
            <el-button 
              v-if="scope.row.class_info === currentClassId"
              type="danger" 
              size="mini"
              icon="el-icon-remove" 
              plain
              @click="removeFromClass(scope.row)">
              移出
            </el-button>
            
            <el-button 
              v-else
              type="primary" 
              size="mini"
              icon="el-icon-plus" 
              @click="addToClass(scope.row)">
              加入
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div slot="footer">
        <el-button @click="studentOpen = false">关 闭</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: "ClassList",
  data() {
    return {
      loading: false,
      submitLoading: false, // 🟢 新增
      tableData: [],
      queryForm: { name: "" },
      teachers: [],
      open: false,
      title: "",
      form: {},
      rules: {
        name: [{ required: true, message: "班级名称不能为空", trigger: "blur" }]
      },
      // ... 学生管理数据 ...
      studentOpen: false,
      studentLoading: false,
      allStudents: [],
      studentQuery: "",
      currentClassId: null,
      currentClassName: ""
    };
  },
  computed: {
    filteredStudentData() {
      // ... 保持不变 ...
      if (!this.studentQuery) {
        return [...this.allStudents].sort((a, b) => {
          if (a.class_info === this.currentClassId && b.class_info !== this.currentClassId) return -1;
          if (a.class_info !== this.currentClassId && b.class_info === this.currentClassId) return 1;
          return 0;
        });
      }
      const lowerKey = this.studentQuery.toLowerCase();
      return this.allStudents.filter(s => 
        (s.username && s.username.toLowerCase().includes(lowerKey)) ||
        (s.nickname && s.nickname.toLowerCase().includes(lowerKey))
      );
    }
  },
  created() { 
    this.fetchData(); 
    this.getTeachers(); 
  },
  methods: {
    async fetchData() {
      this.loading = true;
      try {
        const params = {};
        if (this.queryForm.name) params.search = this.queryForm.name;
        const res = await this.$axios.get('classes/', { params });
        this.tableData = res.data.results || res.data;
      } finally {
        this.loading = false;
      }
    },
    resetQuery() {
      this.queryForm.name = "";
      this.fetchData();
    },
    async getTeachers() {
      const res = await this.$axios.get('users/', { params: { role: 2 } });
      this.teachers = res.data.results || res.data;
    },
    formatTime(time) {
      if(!time) return '-';
      return new Date(time).toLocaleString();
    },
    handleAdd() { 
      this.form = {}; 
      this.title="新建班级"; 
      this.open = true; 
    },
    handleEdit(row) { 
      this.form = {...row}; 
      this.title="编辑班级"; 
      this.open = true; 
    },
    async submitForm() {
      this.$refs["form"].validate(async valid => {
        if (valid) {
          this.submitLoading = true; // 🟢 开启
          try {
            if(this.form.id) {
                await this.$axios.patch(`classes/${this.form.id}/`, this.form);
                this.$message.success("修改成功");
            } else {
                await this.$axios.post('classes/', this.form);
                this.$message.success("新建成功");
            }
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
    // ... 删除和学生管理逻辑保持不变 ...
    handleDelete(row) {
        this.$confirm('确认删除该班级? 删除后该班级学生将变为无班级状态。', '警告', { type: 'warning' })
        .then(async () => {
            await this.$axios.delete(`classes/${row.id}/`);
            this.$message.success("删除成功");
            this.fetchData();
        }).catch(()=>{});
    },
    handleStudents(row) {
        this.currentClassId = row.id;
        this.currentClassName = row.name;
        this.studentOpen = true;
        this.studentQuery = "";
        this.fetchAllStudents();
    },
    async fetchAllStudents() {
        this.studentLoading = true;
        try {
            const res = await this.$axios.get('users/', { params: { role: 1, page_size: 1000 } });
            this.allStudents = res.data.results || res.data;
        } finally {
            this.studentLoading = false;
        }
    },
    async addToClass(studentRow) {
        if (studentRow.class_info && studentRow.class_info !== this.currentClassId) {
            try {
                await this.$confirm(`该学生当前已在【${studentRow.display_class_name}】，确定要调入本班吗？`, '转班确认', {
                    confirmButtonText: '确定转班',
                    cancelButtonText: '取消',
                    type: 'warning'
                });
            } catch(e) { return; }
        }
        try {
            await this.$axios.patch(`users/${studentRow.id}/`, { class_info: this.currentClassId });
            this.$message.success("加入成功");
            studentRow.class_info = this.currentClassId;
            studentRow.display_class_name = this.currentClassName;
            this.fetchData();
        } catch (e) {
            this.$message.error("操作失败");
        }
    },
    async removeFromClass(studentRow) {
        try {
            await this.$confirm(`确定将学生 ${studentRow.nickname} 移出本班吗?`, '提示', { type: 'warning' });
            await this.$axios.patch(`users/${studentRow.id}/`, { class_info: null });
            this.$message.success("已移出");
            studentRow.class_info = null;
            studentRow.display_class_name = "暂无班级";
            this.fetchData();
        } catch(e) {}
    }
  }
};
</script>

<style scoped>
.search-card { border: none; }
.table-card { border: none; }
.text-gray { color: #909399; }
</style>