<template>
  <div class="review-page">
    <el-card class="upload-card">
      <template #header>
        <div class="card-header">
          <span>上传合同</span>
        </div>
      </template>
      
      <el-upload
        class="upload-area"
        drag
        :auto-upload="false"
        :on-change="handleFileChange"
        :limit="1"
        accept=".pdf,.docx,.doc,.txt"
      >
        <el-icon size="48"><UploadFilled /></el-icon>
        <div class="upload-text">将文件拖到此处，或<em>点击上传</em></div>
        <div class="upload-hint">支持 PDF、Word、TXT 格式，单个文件不超过50MB</div>
      </el-upload>
      
      <!-- 部门选择 -->
      <div class="department-select" v-if="file">
        <el-form label-width="100px">
          <el-form-item label="审查部门">
            <el-select v-model="selectedDepartment" placeholder="选择审查部门">
              <el-option
                v-for="dept in departments"
                :key="dept.id"
                :label="dept.name"
                :value="dept.id"
                :disabled="!dept.enabled"
              />
            </el-select>
          </el-form-item>
        </el-form>
      </div>
      
      <!-- 审查按钮 -->
      <div class="actions" v-if="file">
        <el-button 
          type="primary" 
          @click="startReview" 
          :loading="reviewing"
          size="large"
        >
          <el-icon><Document /></el-icon>
          开始审查
        </el-button>
        <el-button @click="reset" size="large">
          <el-icon><Refresh /></el-icon>
          重新上传
        </el-button>
      </div>
    </el-card>
    
    <!-- 审查结果 -->
    <el-card class="result-card" v-if="result">
      <template #header>
        <div class="card-header">
          <span>审查结果</span>
          <el-tag :type="getResultType(result.summary)">
            {{ getResultText(result.summary) }}
          </el-tag>
        </div>
      </template>
      
      <!-- 基本信息 -->
      <div class="basic-info">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="产品名称">{{ result.product_name || '-' }}</el-descriptions-item>
          <el-descriptions-item label="产品类型">{{ result.product_type || '-' }}</el-descriptions-item>
          <el-descriptions-item label="审查部门">{{ getDeptName(result.department) }}</el-descriptions-item>
          <el-descriptions-item label="审查时间">{{ result.metadata?.review_time || '-' }}</el-descriptions-item>
        </el-descriptions>
      </div>
      
      <!-- 统计摘要 -->
      <div class="summary-stats">
        <el-row :gutter="20">
          <el-col :span="6">
            <div class="stat-item passed">
              <div class="stat-value">{{ result.summary?.passed || 0 }}</div>
              <div class="stat-label">通过</div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="stat-item warning">
              <div class="stat-value">{{ result.summary?.warnings || 0 }}</div>
              <div class="stat-label">警告</div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="stat-item error">
              <div class="stat-value">{{ result.summary?.errors || 0 }}</div>
              <div class="stat-label">问题</div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="stat-item total">
              <div class="stat-value">{{ result.summary?.total || 0 }}</div>
              <div class="stat-label">总计</div>
            </div>
          </el-col>
        </el-row>
      </div>
      
      <!-- 详细发现 -->
      <div class="findings">
        <el-table :data="result.findings" stripe style="width: 100%">
          <el-table-column prop="item" label="审查项目" min-width="150" />
          <el-table-column prop="status" label="状态" width="100">
            <template #default="{ row }">
              <el-tag :type="getFindingType(row.status)" size="small">
                {{ getFindingText(row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="risk_level" label="风险等级" width="100">
            <template #default="{ row }">
              <el-tag :type="getRiskType(row.risk_level)" size="small">
                {{ row.risk_level }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="finding" label="发现内容" min-width="200" />
          <el-table-column prop="recommendation" label="建议" min-width="150" />
          <el-table-column prop="evidence" label="证据" min-width="150" />
        </el-table>
      </div>
      
      <!-- 导出按钮 -->
      <div class="export-actions">
        <el-button type="primary" @click="exportReport">
          <el-icon><Download /></el-icon>
          导出报告
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { UploadFilled, Document, Refresh, Download } from '@element-plus/icons-vue'
import axios from 'axios'

const file = ref(null)
const fileContent = ref(null)
const selectedDepartment = ref('investment_supervision')
const reviewing = ref(false)
const result = ref(null)

const departments = ref([
  { id: 'investment_supervision', name: '投资监督部', enabled: true },
  { id: 'risk_compliance', name: '风险合规部', enabled: true },
  { id: 'valuation_service', name: '估值服务部', enabled: true },
  { id: 'settlement_service', name: '结算服务部', enabled: true }
])

const handleFileChange = async (uploadFile) => {
  file.value = uploadFile.raw
  
  // 读取文件内容
  const reader = new FileReader()
  reader.onload = (e) => {
    fileContent.value = e.target.result
  }
  reader.readAsText(uploadFile.raw)
}

const startReview = async () => {
  if (!file.value) {
    ElMessage.warning('请先上传文件')
    return
  }
  
  reviewing.value = true
  result.value = null
  
  try {
    const formData = new FormData()
    formData.append('file', file.value)
    formData.append('department', selectedDepartment.value)
    
    const response = await axios.post('/api/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    
    result.value = response.data.data
    ElMessage.success('审查完成')
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '审查失败')
  } finally {
    reviewing.value = false
  }
}

const reset = () => {
  file.value = null
  fileContent.value = null
  result.value = null
}

const getDeptName = (deptId) => {
  const dept = departments.value.find(d => d.id === deptId)
  return dept ? dept.name : deptId
}

const getResultType = (summary) => {
  if (summary?.errors > 0) return 'danger'
  if (summary?.warnings > 0) return 'warning'
  return 'success'
}

const getResultText = (summary) => {
  if (summary?.errors > 0) return '存在问题'
  if (summary?.warnings > 0) return '需要关注'
  return '审查通过'
}

const getFindingType = (status) => {
  const types = { pass: 'success', warning: 'warning', fail: 'danger' }
  return types[status] || 'info'
}

const getFindingText = (status) => {
  const texts = { pass: '通过', warning: '警告', fail: '不通过' }
  return texts[status] || status
}

const getRiskType = (level) => {
  const types = { low: 'success', medium: 'warning', high: 'danger' }
  return types[level] || 'info'
}

const exportReport = () => {
  ElMessage.success('报告导出功能开发中')
}
</script>

<style lang="scss" scoped>
.review-page {
  .upload-card {
    margin-bottom: 20px;
  }
  
  .upload-area {
    width: 100%;
    
    :deep(.el-upload-dragger) {
      padding: 40px;
    }
    
    .upload-text {
      margin: 16px 0 8px;
      font-size: 16px;
      
      em {
        color: #409EFF;
        font-style: normal;
      }
    }
    
    .upload-hint {
      font-size: 12px;
      color: #909399;
    }
  }
  
  .department-select {
    margin: 20px 0;
    max-width: 400px;
  }
  
  .actions {
    display: flex;
    gap: 16px;
    margin-top: 20px;
  }
  
  .result-card {
    .basic-info {
      margin-bottom: 20px;
    }
    
    .summary-stats {
      margin-bottom: 20px;
      
      .stat-item {
        padding: 20px;
        border-radius: 8px;
        text-align: center;
        color: #fff;
        
        &.passed { background: #67C23A; }
        &.warning { background: #E6A23C; }
        &.error { background: #F56C6C; }
        &.total { background: #409EFF; }
        
        .stat-value {
          font-size: 32px;
          font-weight: bold;
        }
        
        .stat-label {
          font-size: 14px;
          opacity: 0.9;
        }
      }
    }
    
    .export-actions {
      margin-top: 20px;
      text-align: right;
    }
  }
  
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
}
</style>
