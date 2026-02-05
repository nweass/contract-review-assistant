<template>
  <div class="home-page">
    <!-- 统计卡片 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-icon" style="background: #409EFF;">
            <el-icon size="32"><Document /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.totalReviews }}</div>
            <div class="stat-label">今日审查</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-icon" style="background: #67C23A;">
            <el-icon size="32"><CircleCheck /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.passed }}</div>
            <div class="stat-label">审查通过</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-icon" style="background: #E6A23C;">
            <el-icon size="32"><Warning /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.warnings }}</div>
            <div class="stat-label">风险提示</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-icon" style="background: #F56C6C;">
            <el-icon size="32"><CircleClose /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.errors }}</div>
            <div class="stat-label">审查问题</div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 快速开始 -->
    <el-card class="quick-start">
      <template #header>
        <div class="card-header">
          <span>快速开始</span>
        </div>
      </template>
      
      <el-row :gutter="20">
        <el-col :span="8">
          <div class="quick-action" @click="$router.push('/review')">
            <el-icon size="48" color="#409EFF"><Upload /></el-icon>
            <h3>上传审查</h3>
            <p>上传合同文件进行智能审查</p>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="quick-action" @click="$router.push('/batch')">
            <el-icon size="48" color="#67C23A"><Files /></el-icon>
            <h3>批量审查</h3>
            <p>批量上传多个合同文件</p>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="quick-action" @click="$router.push('/rules')">
            <el-icon size="48" color="#E6A23C"><Setting /></el-icon>
            <h3>规则管理</h3>
            <p>配置和调整审查规则</p>
          </div>
        </el-col>
      </el-row>
    </el-card>
    
    <!-- 支持的部门 -->
    <el-card class="departments">
      <template #header>
        <div class="card-header">
          <span>支持的审查部门</span>
        </div>
      </template>
      
      <el-row :gutter="20">
        <el-col :span="6" v-for="dept in departments" :key="dept.id">
          <div class="dept-card" :class="{ disabled: !dept.enabled }">
            <el-icon size="40"><OfficeBuilding /></el-icon>
            <h4>{{ dept.name }}</h4>
            <el-tag :type="dept.enabled ? 'success' : 'info'" size="small">
              {{ dept.enabled ? '已启用' : '未配置' }}
            </el-tag>
          </div>
        </el-col>
      </el-row>
    </el-card>
    
    <!-- 最近审查 -->
    <el-card class="recent-reviews">
      <template #header>
        <div class="card-header">
          <span>最近审查</span>
          <el-button type="text" @click="$router.push('/history')">查看全部</el-button>
        </div>
      </template>
      
      <el-table :data="recentReviews" style="width: 100%">
        <el-table-column prop="fileName" label="文件名称" />
        <el-table-column prop="department" label="审查部门" width="150" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="reviewTime" label="审查时间" width="180" />
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Document, CircleCheck, Warning, CircleClose, Upload, Files, Setting, OfficeBuilding } from '@element-plus/icons-vue'

const stats = ref({
  totalReviews: 12,
  passed: 8,
  warnings: 3,
  errors: 1
})

const departments = ref([
  { id: 'investment_supervision', name: '投资监督部', enabled: true },
  { id: 'risk_compliance', name: '风险合规部', enabled: true },
  { id: 'valuation_service', name: '估值服务部', enabled: true },
  { id: 'settlement_service', name: '结算服务部', enabled: true }
])

const recentReviews = ref([
  { fileName: 'XX公募基金合同.pdf', department: '投资监督部', status: 'passed', reviewTime: '2025-02-05 10:30:00' },
  { fileName: 'YY年金托管合同.docx', department: '风险合规部', status: 'warning', reviewTime: '2025-02-05 09:15:00' },
  { fileName: 'ZZ基金托管协议.pdf', department: '结算服务部', status: 'passed', reviewTime: '2025-02-04 16:45:00' }
])

const getStatusType = (status) => {
  const types = { passed: 'success', warning: 'warning', failed: 'danger' }
  return types[status] || 'info'
}

const getStatusText = (status) => {
  const texts = { passed: '通过', warning: '警告', failed: '不通过' }
  return texts[status] || status
}

onMounted(() => {
  // 加载部门信息
})
</script>

<style lang="scss" scoped>
.home-page {
  .stats-row {
    margin-bottom: 20px;
  }
  
  .stat-card {
    display: flex;
    align-items: center;
    gap: 16px;
    
    .stat-icon {
      width: 60px;
      height: 60px;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #fff;
    }
    
    .stat-value {
      font-size: 28px;
      font-weight: bold;
      color: #303133;
    }
    
    .stat-label {
      font-size: 14px;
      color: #909399;
    }
  }
  
  .quick-start {
    margin-bottom: 20px;
    
    .quick-action {
      padding: 30px;
      text-align: center;
      border-radius: 8px;
      cursor: pointer;
      transition: all 0.3s;
      
      &:hover {
        background: #f5f7fa;
      }
      
      h3 {
        margin: 16px 0 8px;
        color: #303133;
      }
      
      p {
        color: #909399;
        font-size: 14px;
      }
    }
  }
  
  .departments {
    margin-bottom: 20px;
    
    .dept-card {
      padding: 24px;
      text-align: center;
      border-radius: 8px;
      background: #f5f7fa;
      
      &.disabled {
        opacity: 0.6;
      }
      
      h4 {
        margin: 12px 0;
        color: #303133;
      }
    }
  }
  
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
}
</style>
