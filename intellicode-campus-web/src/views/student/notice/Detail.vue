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
          类型：{{ notice.type_display }}
        </div>
        <div style="font-size: 16px; line-height: 1.8; white-space: pre-wrap;">{{ notice.content }}</div>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  data() { return { notice: {}, loading: false } },
  created() {
    const id = this.$route.params.id;
    if(id) this.getDetail(id);
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
    }
  }
}
</script>
<style scoped>.container-1200 { width: 1200px; margin: 0 auto; }</style>