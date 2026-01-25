const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  // 关闭 ESLint 的 component name 校验
    lintOnSave: false
})
