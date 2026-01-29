<template>
  <div class="container-1200" style="padding: 20px;">
    <el-card shadow="never">
      <div slot="header">
        <span style="font-weight: bold; font-size: 18px;">📢 全部公告</span>
      </div>
      
      <el-table :data="tableData" v-loading="loading" style="width: 100%" @row-click="handleRowClick">
        <el-table-column label="状态" width="80" align="center">
          <template slot-scope="scope">
            <el-tag v-if="scope.row.is_top" type="danger" size="mini" effect="dark">置顶</el-tag>
          </template>
        </el-table-column>

        <el-table-column label="类型" width="120" align="center">
          <template slot-scope="scope">
            <el-tag :type="getDictTagType(scope.row.type)">
              {{ getDictLabel(scope.row.type) }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column prop="title" label="标题" show-overflow-tooltip></el-table-column>
        <el-table-column prop="author_name" label="发布人" width="150" align="center"></el-table-column>
        <el-table-column prop="created_at" label="发布时间" width="180" align="center">
          <template slot-scope="scope">{{ new Date(scope.row.created_at).toLocaleString() }}</template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
export default {
  data() { 
    return { 
      tableData: [], 
      loading: false,
      // 🟢 字典数据
      noticeDicts: [] 
    } 
  },
  created() { 
    this.getList();
    // 🟢 加载字典
    this.getDicts();
  },
  methods: {
    async getList() {
      this.loading = true;
      const res = await this.$axios.get('notices/');
      this.tableData = res.data.results || res.data;
      this.loading = false;
    },
    
    // 🟢 获取字典数据
    async getDicts() {
      try {
        const res = await this.$axios.get('dict-data/', { params: { dict_type__type: 'notice_type' } });
        this.noticeDicts = res.data.results || res.data;
      } catch (e) {
        console.error("加载字典失败", e);
      }
    },

    // 🟢 翻译文本
    getDictLabel(value) {
      if (!this.noticeDicts.length) return '...';
      const found = this.noticeDicts.find(item => item.value == value);
      return found ? found.label : value;
    },

    // 🟢 翻译颜色
    getDictTagType(value) {
      if (!this.noticeDicts.length) return '';
      const found = this.noticeDicts.find(item => item.value == value);
      return found && found.list_class ? found.list_class : ''; 
    },

    handleRowClick(row) {
      this.$router.push(`/student/notice/${row.id}`);
    }
  }
}
</script>
<style scoped>.container-1200 { width: 1200px; margin: 0 auto; cursor: pointer; }</style>