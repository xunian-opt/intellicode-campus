<template>
  <div class="container-1200" style="padding: 20px;">
    <el-card shadow="never" v-loading="loading">
      <div slot="header">
        <el-page-header @back="$router.go(-1)" :content="notice.title || '公告详情'"></el-page-header>
      </div>
      <div v-if="notice.id" style="padding: 20px;">
        <h2 style="text-align: center; margin-bottom: 10px;">{{ notice.title }}</h2>
        <div style="text-align: center; color: #999; margin-bottom: 30px; font-size: 13px;">
          发布人：{{ notice.author_name }} &nbsp;|&nbsp; 
          发布时间：{{ new Date(notice.created_at).toLocaleString() }} &nbsp;|&nbsp;
          
          类型：{{ getDictLabel(notice.type) }}
        </div>
        <div style="font-size: 16px; line-height: 1.8; white-space: pre-wrap;">{{ notice.content }}</div>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  data() { 
    return { 
      notice: {}, 
      loading: false,
      // 🟢 [新增] 存储字典数据
      noticeDicts: [] 
    } 
  },
  created() {
    const id = this.$route.params.id;
    if(id) this.getDetail(id);
    // 🟢 [新增] 加载字典
    this.getDicts();
  },
  methods: {
    async getDetail(id) {
      this.loading = true;
      try {
        const res = await this.$axios.get(`notices/${id}/`);
        this.notice = res.data;
      } finally {
        this.loading = false;
      }
    },
    // 🟢 [新增] 获取字典数据
    async getDicts() {
      try {
        const res = await this.$axios.get('dict-data/', { params: { dict_type__type: 'notice_type' } });
        this.noticeDicts = res.data.results || res.data;
      } catch (e) {
        console.error("加载字典失败", e);
      }
    },
    // 🟢 [新增] 翻译类型文本
    getDictLabel(value) {
      if (!this.noticeDicts.length) return value || '...';
      const found = this.noticeDicts.find(item => item.value == value);
      return found ? found.label : value;
    }
  }
}
</script>
<style scoped>.container-1200 { width: 1200px; margin: 0 auto; }</style>