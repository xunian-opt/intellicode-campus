<template>
  <div class="app-container">
    <el-card shadow="never">
      <div slot="header" class="clearfix" style="display: flex; justify-content: space-between; align-items: center;">
        <span style="font-weight: bold; font-size: 16px;">首页轮播图管理</span>
        <el-button type="primary" icon="el-icon-plus" size="small" @click="handleAdd">新增轮播图</el-button>
      </div>

      <el-table v-loading="loading" :data="tableData" border stripe style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" align="center" />
        
        <el-table-column label="轮播图预览" width="220" align="center">
          <template slot-scope="scope">
            <el-image 
              style="width: 180px; height: 80px; border-radius: 4px; cursor: pointer;"
              :src="scope.row.image" 
              fit="cover"
              :preview-src-list="[scope.row.image]">
              <div slot="error" class="image-slot">
                <i class="el-icon-picture-outline"></i>
              </div>
            </el-image>
          </template>
        </el-table-column>
        
        <el-table-column prop="title" label="标题" align="center" show-overflow-tooltip />
        
        <el-table-column prop="url" label="跳转链接" align="center" show-overflow-tooltip>
          <template slot-scope="scope">
            <a v-if="scope.row.url" :href="scope.row.url" target="_blank" style="color: #409EFF">{{ scope.row.url }}</a>
            <span v-else style="color: #999">无</span>
          </template>
        </el-table-column>

        <el-table-column prop="order" label="排序权重" width="100" align="center" sortable />
        
        <el-table-column label="状态" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="scope.row.is_active ? 'success' : 'info'" effect="dark">
              {{ scope.row.is_active ? '启用' : '已禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column label="操作" width="180" align="center" fixed="right">
          <template slot-scope="scope">
            <el-button type="primary" size="mini" icon="el-icon-edit" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button type="danger" size="mini" icon="el-icon-delete" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog :title="dialogTitle" :visible.sync="dialogVisible" width="600px" :close-on-click-modal="false" @close="resetForm">
      <el-form ref="dataForm" :model="formData" :rules="rules" label-width="100px">
        
        <el-form-item label="标题" prop="title">
          <el-input v-model="formData.title" placeholder="请输入轮播图标题（用于显示和Alt文本）" />
        </el-form-item>

        <el-form-item label="轮播图片" prop="image" ref="imageItem">
          <el-upload
            class="banner-uploader"
            action=""
            :auto-upload="false"
            :show-file-list="false"
            :on-change="handleFileChange"
            accept="image/jpeg,image/png,image/jpg"
          >
            <img v-if="imageUrl" :src="imageUrl" class="banner-image" />
            <i v-else class="el-icon-plus banner-uploader-icon"></i>
          </el-upload>
          <div style="font-size: 12px; color: #999; margin-top: 8px; line-height: 1.5;">
            支持 JPG/PNG 格式，建议尺寸：1200px * 350px，大小不超过 2MB。<br>
            点击上方区域可更换图片。
          </div>
        </el-form-item>

        <el-form-item label="跳转链接" prop="url">
          <el-input v-model="formData.url" placeholder="点击图片跳转的地址 (选填，例如 http://...)" >
            <template slot="prepend">Http://</template>
          </el-input>
        </el-form-item>

        <el-row>
          <el-col :span="12">
            <el-form-item label="排序权重" prop="order">
               <el-input-number v-model="formData.order" :min="0" :max="9999" controls-position="right" style="width: 100%;"></el-input-number>
               <div style="font-size: 12px; color: #999;">数值越大越靠前</div>
            </el-form-item>
          </el-col>
          <el-col :span="12">
             <el-form-item label="是否启用" prop="is_active">
              <el-switch v-model="formData.is_active" active-text="启用" inactive-text="禁用" active-color="#13ce66"></el-switch>
            </el-form-item>
          </el-col>
        </el-row>

      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" :loading="submitLoading" @click="submitForm">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: "BannerList",
  data() {
    return {
      loading: false,
      submitLoading: false,
      tableData: [],
      dialogVisible: false,
      dialogTitle: "",
      // 表单数据
      formData: {
        id: undefined,
        title: "",
        url: "",
        order: 0,
        is_active: true,
      },
      // 图片预览地址（本地Blob或远程URL）
      imageUrl: "",
      // 实际要上传的文件对象
      uploadFile: null,
      // 表单验证规则
      rules: {
        title: [{ required: true, message: "请输入标题", trigger: "blur" }],
        // 图片验证需要自定义逻辑
        image: [{ 
          validator: (rule, value, callback) => {
            // 如果是新增且没有上传文件，或者编辑时既没有新文件也没有旧图回显
            if (!this.formData.id && !this.uploadFile) {
              callback(new Error('请上传轮播图片'));
            } else if (this.formData.id && !this.imageUrl && !this.uploadFile) {
              callback(new Error('请上传轮播图片'));
            } else {
              callback();
            }
          }, 
          trigger: 'change' 
        }]
      }
    };
  },
  created() {
    this.fetchData();
  },
  methods: {
    // 获取列表数据
    async fetchData() {
      this.loading = true;
      try {
        const res = await this.$axios.get("banners/");
        // 兼容分页和不分页的返回接口
        this.tableData = res.data.results || res.data;
      } catch (error) {
        console.error(error);
        this.$message.error("获取数据失败");
      } finally {
        this.loading = false;
      }
    },

    // 打开新增弹窗
    handleAdd() {
      this.resetForm();
      this.dialogTitle = "新增轮播图";
      this.dialogVisible = true;
    },

    // 打开编辑弹窗
    handleEdit(row) {
      this.resetForm();
      this.dialogTitle = "编辑轮播图";
      // 复制现有数据
      this.formData = { 
        id: row.id,
        title: row.title,
        url: row.url,
        order: row.order,
        is_active: row.is_active
      };
      // 设置回显图片URL，清空上传文件对象
      this.imageUrl = row.image; 
      this.uploadFile = null; 
      this.dialogVisible = true;
    },

    // 处理文件选择变动（核心预览逻辑）
    handleFileChange(file) {
      const isJPG = file.raw.type === 'image/jpeg' || file.raw.type === 'image/png';
      const isLt2M = file.size / 1024 / 1024 < 2;

      if (!isJPG) {
        this.$message.error('上传图片只能是 JPG/PNG 格式!');
        return;
      }
      if (!isLt2M) {
        this.$message.error('上传图片大小不能超过 2MB!');
        return;
      }

      // 保存文件对象用于提交
      this.uploadFile = file.raw;
      // 生成本地预览URL
      this.imageUrl = URL.createObjectURL(file.raw);
      // 手动触发一下表单验证清除错误提示
      this.$refs.imageItem?.clearValidate();
    },

    // 重置表单
    resetForm() {
      this.formData = {
        id: undefined,
        title: "",
        url: "",
        order: 0,
        is_active: true,
      };
      this.imageUrl = "";
      this.uploadFile = null;
      this.$nextTick(() => {
        this.$refs["dataForm"]?.clearValidate();
      });
    },

    // 提交表单
    submitForm() {
      this.$refs["dataForm"].validate(async (valid) => {
        if (!valid) return;

        this.submitLoading = true;
        try {
          // 使用 FormData 处理文件上传
          const submitData = new FormData();
          submitData.append("title", this.formData.title);
          // 如果url为空则不传或传空字符串，避免传递 "null" 或 "undefined" 字符串
          submitData.append("url", this.formData.url || "");
          submitData.append("order", this.formData.order);
          // Django BooleanField 有时需要明确的 True/False 字符串在 FormData 中
          submitData.append("is_active", this.formData.is_active ? "True" : "False");

          // 只有当用户选择了新文件时，才添加 image 字段
          if (this.uploadFile) {
            submitData.append("image", this.uploadFile);
          }

          if (this.formData.id) {
            // 编辑模式 (PATCH)
            await this.$axios.patch(`banners/${this.formData.id}/`, submitData);
            this.$message.success("更新成功");
          } else {
            // 新增模式 (POST)
            // 双重校验，确保有文件
            if (!this.uploadFile) {
                this.$message.warning("请选择要上传的图片");
                this.submitLoading = false;
                return;
            }
            await this.$axios.post("banners/", submitData);
            this.$message.success("创建成功");
          }
          
          this.dialogVisible = false;
          this.fetchData(); // 刷新列表
        } catch (error) {
          console.error(error);
          // 如果后端返回了详细错误字段信息
          if (error.response && error.response.data) {
              const errors = error.response.data;
              let sendMsg = false;
              // 尝试将后端错误映射到表单字段
              Object.keys(errors).forEach(key => {
                  // 如果是列表类型的错误信息
                  if (Array.isArray(errors[key])) {
                      this.$message.error(errors[key][0]);
                      sendMsg = true;
                  }
              })
              if (!sendMsg) this.$message.error("操作失败，请检查输入");
          } else {
              this.$message.error("操作失败，服务器错误");
          }
        } finally {
          this.submitLoading = false;
        }
      });
    },

    // 删除
    handleDelete(row) {
      this.$confirm(`确认删除标题为 "${row.title}" 的轮播图吗？`, "警告", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(async () => {
          await this.$axios.delete(`banners/${row.id}/`);
          this.$message.success("删除成功");
          this.fetchData();
        })
        .catch(() => {});
    },
  },
};
</script>

<style lang="scss" scoped>
/* 🟢 核心 CSS：复刻标准的 Element UI 图片上传样式 */

// 外部容器，控制整体宽高比，这里设置为适合轮播图的长方形
.banner-uploader {
  ::v-deep .el-upload {
    border: 1px dashed #d9d9d9; // 虚线边框
    border-radius: 6px;         // 圆角
    cursor: pointer;            // 鼠标手势
    position: relative;
    overflow: hidden;
    width: 100%;                // 宽度占满表单项
    height: 160px;              // 固定高度，形成长方形区域
    display: flex;              // 使用 flex 居中内部元素
    justify-content: center;
    align-items: center;
    transition: border-color 0.3s;
    background-color: #fbfdff;  // 淡淡的背景色

    &:hover {
      border-color: #409eff;    // 悬停时边框变蓝
    }
  }
}

// 加号图标样式
.banner-uploader-icon {
  font-size: 32px;              // 大小
  color: #8c939d;               // 灰色
  text-align: center;
}

// 图片预览样式
.banner-image {
  width: 100%;
  height: 100%;
  object-fit: cover;            // 关键：保持比例填充，裁剪多余部分
  display: block;
}
</style>