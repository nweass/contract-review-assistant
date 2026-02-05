<template>
  <el-config-provider :locale="locale">
    <div class="app-container">
      <el-container>
        <!-- 侧边栏 -->
        <el-aside width="220px" class="sidebar">
          <div class="logo">
            <el-icon size="32" color="#409EFF"><DocumentChecked /></el-icon>
            <span>合同审查系统</span>
          </div>
          
          <el-menu
            :default-active="activeMenu"
            router
            background-color="#304156"
            text-color="#bfcbd9"
            active-text-color="#409EFF"
          >
            <el-menu-item index="/">
              <el-icon><HomeFilled /></el-icon>
              <span>首页</span>
            </el-menu-item>
            
            <el-menu-item index="/review">
              <el-icon><Document /></el-icon>
              <span>合同审查</span>
            </el-menu-item>
            
            <el-menu-item index="/batch">
              <el-icon><Files /></el-icon>
              <span>批量审查</span>
            </el-menu-item>
            
            <el-menu-item index="/rules">
              <el-icon><Setting /></el-icon>
              <span>规则管理</span>
            </el-menu-item>
            
            <el-menu-item index="/history">
              <el-icon><Clock /></el-icon>
              <span>审查历史</span>
            </el-menu-item>
          </el-menu>
        </el-aside>
        
        <!-- 主内容 -->
        <el-container>
          <el-header class="header">
            <div class="header-title">{{ pageTitle }}</div>
            <div class="header-actions">
              <el-button type="text" @click="refreshDepartments">
                <el-icon><Refresh /></el-icon>
                刷新部门
              </el-button>
            </div>
          </el-header>
          
          <el-main class="main-content">
            <router-view />
          </el-main>
        </el-container>
      </el-container>
    </div>
  </el-config-provider>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'

const locale = zhCn
const route = useRoute()

const activeMenu = computed(() => route.path)
const pageTitle = computed(() => {
  const titles = {
    '/': '首页',
    '/review': '合同审查',
    '/batch': '批量审查',
    '/rules': '规则管理',
    '/history': '审查历史'
  }
  return titles[route.path] || '合同审查系统'
})

const refreshDepartments = () => {
  ElMessage.success('部门信息已刷新')
}
</script>

<style lang="scss" scoped>
.app-container {
  height: 100vh;
}

.sidebar {
  background-color: #304156;
  
  .logo {
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    color: #fff;
    font-size: 16px;
    font-weight: bold;
  }
}

.header {
  background: #fff;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  
  .header-title {
    font-size: 18px;
    font-weight: 600;
    color: #303133;
  }
}

.main-content {
  background-color: #f0f2f5;
  padding: 20px;
}
</style>
