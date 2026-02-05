<template>
  <div class="batch-review-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>批量审查</span>
        </div>
      </template>
      
      <el-upload
        class="batch-upload"
        drag
        :auto-upload="false"
        :on-change="handleFilesChange"
        :on-remove="handleRemove"
        multiple
        accept=".pdf,.docx,.doc,.txt"
      >
        <el-icon size="48"><UploadFilled /></el-icon>
        <div class="upload-text">将文件拖到此处，或<em>点击上传</em></div>
        <div class="upload-hint">支持批量上传多个文件</div>
      </el-upload>
      
      <!-- 部门选择 -->
      <div class="department-select">
        <el-form label-width="100px">
          <el-form-item label="审查部门">
            <el-select v-model="selectedDepartment" placeholder="选择审查部门">
              <el-option
                v-for="dept in departments"
                :key="dept.id"
                :label="dept.name"
                :value="dept.id"
              />
            </el-select>
          </el-form-item>
        </el-form>
      </div>
      
      <!-- 文件列表 -->
      <div class="file-list" v-if="fileList.length > 0">
        <el-table :data="fileList" style="width: 100%">
          <el-table-column type="index" width="50" />
          <el-table-column prop="name" label="文件名" min-width="200" />
          <el-table-column prop="size" label="大小" width="120">
            <template #default="{ row }">
              {{ formatFileSize(row.size) }}
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态" width="150">
            <template #default="{ row }">
              <el-tag :type="getStatusType(row.status)" size="small">
                {{ getStatusText(row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="100">
            <template #default="{ row }">
              <el-button 
                type="danger" 
                size="small" 
                @click="removeFile(row)"
                :disabled="row.status === 'completed'"
              >
                移除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
      
      <!-- 审查按钮 -->
      <div class="actions" v-if="fileList.length > 0">
        <el-button 
          type="primary" 
          @click="startBatchReview" 
          :loading="reviewing"
          size="large"
        >
          <el-icon><Document /></el-icon>
          开始批量审查 ({{ fileList.length }}个文件)
        </el-button>
        <el-button @click="clearAll" size="large">
          <el-icon><Delete /></el-icon>
          清空列表
        </el-button>
      </div>
    </el-card>
    
    <!-- 批量结果 -->
    <el-card class="batch-results" v-if="results.length > 0">
      <template #header>
        <div class="card-header">
          <span>审查结果 ({{ results.length }}/{{ fileList.length }})</span>
          <el-button type="primary" @click="exportAllReports">
            <el-icon><Download /></el-icon>
            导出全部报告
          </el-button>
        </div>
      </template>
      
      <el-table :data="results" stripe style="width: 100%">
        <el-table-column prop="fileName" label="文件名" min-width="200" />
        <el-table-column prop="department" label="审查部门" width="150" />
        <el-table-column prop="summary" label="结果统计" width="200">
          <template #default="{ row }">
            <span>
              通过:{{ row.summary?.passed || 0 }} / 
              警告:{{ row.summary?.warnings || 0 }} / 
              问题:{{ row.summary?.errors || 0 }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getResultTagType(row.summary)">
              {{ getResultText(row.summary) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120">
          <template #default="{ row }">
            <el-button type="text" @click="viewDetail(row)">查看详情</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { UploadFilled, Document, Delete, Download } from '@element-plus/icons-vue'
import axios from 'axios'

const fileList = ref([])
const selectedDepartment = ref('investment_supervision')
const reviewing = ref(false)
const results = ref([])

const departments = ref([
  { id: 'investment_supervision', name: '投资监督部' },
  { id: 'risk_compliance', name: '风险合规部' },
  { id: 'valuation_service', name: '估值服务部' },
  { id: 'settlement_service', name: '结算服务部' }
])

const handleFilesChange = (uploadFile, uploadFiles) => {
  fileList.value = uploadFiles.map(f => ({
    uid: f.uid,
    name: f.name,
    size: f.size,
    raw: f.raw,
    status: 'pending'
  }))
}

const handleRemove = (file) => {
  const index = fileList.value.findIndex(f => f.uid === file.uid)
  if (index > -1) {
    fileList.value.splice(index, 1)
  }
}

const removeFile = (row) => {
  const index = fileList.value.findIndex(f => f.uid === row.uid)
  if (index > -1) {
    fileList.value.splice(index, 1)
  }
}

const clearAll = () => {
  fileList.value = []
  results.value = []
}

const formatFileSize = (bytes) => {
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
}

const getStatusType = (status) => {
  const types = { pending: 'info', reviewing: 'warning', completed: 'success', failed: 'danger' }
  return types[status] || 'info'
}

const getStatusText = (status) => {
  const texts = { pending: '待审查', reviewing: '审查中', completed: '已完成', failed: '失败' }
  return texts[status] || status
}

const getResultTagType = (summary) => {
  if (!summary) return 'danger'
  if (summary.errors > 0) return 'danger'
  if (summary.warnings > 0) return 'warning'
  return 'success'
}

const getResultText = (summary) => {
  if (!summary) return '失败'
  if (summary.errors > 0) return '存在问题'
  if (summary.warnings > 0) return '需关注'
  return '通过'
}

const startBatchReview = async () => {
  reviewing.value = true
  results.value = []
  
  for (const file of fileList.value) {
    file.status = 'reviewing'
    
    try {
      const formData = new FormData()
      formData.append('file', file.raw)
      formData.append('department', selectedDepartment.value)
      
      const response = await axios.post('/api/upload', formData)
      
      results.value.push({
        fileName: file.name,
        department: departments.value.find(d => d.id === selectedDepartment.value)?.name,
        ...response.data.data
      })
      
      file.status = 'completed'
    } catch (error) {
      file.status = 'failed'
      results.value.push({
        fileName: file.name,
        error: error.response?.data?.detail || '审查失败'
      })
    }
  }
  
  reviewing.value = false
  ElMessage.success('批量审查完成')
}

const viewDetail = (row) => {
  ElMessage.info('详情功能开发中')
}

const exportAllReports = () => {
  ElMessage.success('导出功能开发中')
}
</script>

<style lang="scss" scoped>
.batch-review-page {
  .batch-upload {
    width: 100%;
    
    :deep(.el-upload-dragger) {
      padding: 40px;
    }
  }
  
  .department-select {
    margin: 20px 0;
    max-width: 400px;
  }
  
  .file-list {
    margin: 20px 0;
  }
  
  .actions {
    display: flex;
    gap: 16px;
    margin-top: 20px;
  }
  
  .batch-results {
    margin-top: 20px;
  }
  
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
}
</style>
