<template>
  <div v-if="!item.hidden">
    <template v-if="hasOneShowingChild(item.children, item) && (!onlyOneChild.children || onlyOneChild.noShowingChildren)">
      <el-menu-item 
        :index="resolvePath(onlyOneChild.path)" 
        :class="{'submenu-title-noDropdown':!isNest}">
        <i :class="onlyOneChild.meta?.icon || onlyOneChild.icon || (item.meta && item.meta.icon)"></i>
        
        <span slot="title">{{ onlyOneChild.meta?.title || onlyOneChild.title || (item.meta && item.meta.title) || item.title }}</span>
      </el-menu-item>
    </template>

    <el-submenu v-else ref="subMenu" :index="resolvePath(item.path)" popper-append-to-body>
      <template slot="title">
        <i :class="item.meta?.icon || item.icon || (item.meta && item.meta.icon)"></i>
        
        <span slot="title">{{ item.meta?.title || item.title || (item.meta && item.meta.title) }}</span>
      </template>
      
      <sidebar-item
        v-for="child in item.children"
        :key="child.path"
        :is-nest="true"
        :item="child"
        :base-path="resolvePath(child.path)" 
        class="nest-menu"
      />
    </el-submenu>
  </div>
</template>

<script>
export default {
  name: 'SidebarItem',
  props: {
    item: { type: Object, required: true },
    isNest: { type: Boolean, default: false },
    basePath: { type: String, default: '' }
  },
  data() {
    return { onlyOneChild: null }
  },
  methods: {
    hasOneShowingChild(children = [], parent) {
      const showingChildren = children.filter(item => {
        if (item.hidden) return false
        this.onlyOneChild = item
        return true
      })
      if (showingChildren.length === 1) return true
      if (showingChildren.length === 0) {
        this.onlyOneChild = { ...parent, path: '', noShowingChildren: true }
        return true
      }
      return false
    },
    resolvePath(routePath) {
      if (this.isExternal(routePath)) return routePath
      if (this.isExternal(this.basePath)) return this.basePath
      if (routePath.startsWith('/')) return routePath

      let base = this.basePath
      if (base.length > 0 && !base.endsWith('/')) {
        base += '/'
      }
      if (base.length > 0 && !base.startsWith('/')) {
        base = '/' + base
      }
      return base + routePath
    },
    isExternal(path) {
      return /^(https?:|mailto:|tel:)/.test(path)
    }
  }
}
</script>