<template>
  <div class="rules-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>规则管理</span>
          <el-select v-model="selectedDepartment" @change="loadRules">
            <el-option
              v-for="dept in departments"
              :key="dept.id"
              :label="dept.name"
              :value="dept.id"
            />
          </el-select>
        </div>
      </template>
      
      <!-- 规则统计 -->
      <div class="rules-stats">
        <el-row :gutter="20">
          <el-col :span="6">
            <div class="stat-item">
              <div class="stat-value">{{ rules.length }}</div>
              <div class="stat-label">总规则数</div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="stat-item enabled">
              <div class="stat-value">{{ enabledCount }}</div>
              <div class="stat-label">已启用</div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="stat-item disabled">
              <div class="stat-value">{{ disabledCount }}</div>
              <div class="stat-label">已禁用</div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="stat-item">
              <el-button type="primary" @click="showAddDialog">
                <el-icon><Plus /></el-icon>
                添加规则
              </el-button>
            </div>
          </el-col>
        </el-row>
      </div>
      
      <!-- 添加/编辑规则对话框 -->
      <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑规则' : '添加规则'" width="600px">
        <el-form :model="ruleForm" label-width="100px">
          <el-form-item label="规则ID">
            <el-input v-model="ruleForm.id" :disabled="isEdit" placeholder="如: INV001" />
          </el-form-item>
          <el-form-item label="规则名称">
            <el-input v-model="ruleForm.name" placeholder="如: 投资范围审查" />
          </el-form-item>
          <el-form-item label="描述">
            <el-input v-model="ruleForm.description" type="textarea" :rows="3" placeholder="描述规则的审查要点" />
          </el-form-item>
          <el-form-item label="风险等级">
            <el-select v-model="ruleForm.risk_level">
              <el-option label="高" value="high" />
              <el-option label="中" value="medium" />
              <el-option label="低" value="low" />
            </el-select>
          </el-form-item>
          <el-form-item label="关键词">
            <el-select v-model="ruleForm.keywords" multiple filterable allow-create default-first-option style="width: 100%">
              <el-option label="投资范围" value="投资范围" />
              <el-option label="投资比例" value="投资比例" />
              <el-option label="托管人职责" value="托管人职责" />
              <el-option label="反洗钱" value="反洗钱" />
            </el-select>
          </el-form-item>
          <el-form-item label="启用">
            <el-switch v-model="ruleForm.enabled" />
          </el-form-item>
        </el-form>
        <template #footer>
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveRule">保存</el-button>
        </template>
      </el-dialog>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import axios from 'axios'

const selectedDepartment = ref('investment_supervision')
const rules = ref([])
const dialogVisible = ref(false)
const isEdit = ref(false)
const ruleForm = ref({
  id: '',
  name: '',
  description: '',
  risk_level: 'medium',
  keywords: [],
  enabled: true
})

const departments = ref([
  { id: 'investment_supervision', name: '投资监督部' },
  { id: 'risk_compliance', name: '风险合规部' },
  { id: 'valuation_service', name: '估值服务部' },
  { id: 'settlement_service', name: '结算服务部' }
])

const enabledCount = computed(() => rules.value.filter(r => r.enabled).length)
const disabledCount = computed(() => rules.value.filter(r => !r.enabled).length)

const getRiskType = (level) => {
  const types = { high: 'danger', medium: 'warning', low: 'success' }
  return types[level] || 'info'
}

const loadRules = async () => {
  try {
    const response = await axios.get(`/api/rules/${selectedDepartment.value}`)
    rules.value = response.data.rules || []
  } catch (error) {
    ElMessage.error('加载规则失败')
  }
}

const toggleRule = async (rule) => {
  try {
    await axios.put(`/api/rules/${selectedDepartment.value}/${rule.id}`, { updates: { enabled: rule.enabled } })
    ElMessage.success(rule.enabled ? '规则已启用' : '规则已禁用')
  } catch (error) {
    rule.enabled = !rule.enabled
    ElMessage.error('操作失败')
  }
}

const showAddDialog = () => {
  isEdit.value = false
  ruleForm.value = { id: '', name: '', description: '', risk_level: 'medium', keywords: [], enabled: true }
  dialogVisible.value = true
}

const editRule = (rule) => {
  isEdit.value = true
  ruleForm.value = { ...rule }
  dialogVisible.value = true
}

const saveRule = async () => {
  try {
    await axios.put(`/api/rules/${selectedDepartment.value}/${ruleForm.value.id}`, { updates: ruleForm.value })
    ElMessage.success('规则保存成功')
    dialogVisible.value = false
    loadRules()
  } catch (error) {
    ElMessage.error('保存规则失败')
  }
}

const deleteRule = async (rule) => {
  try {
    await ElMessageBox.confirm('确定要删除这条规则吗？', '确认', { type: 'warning' })
    ElMessage.success('规则已删除')
  } catch { }
}

onMounted(() => {
  loadRules()
})
</script>

<style lang="scss" scoped>
.rules-page {
  .rules-stats {
    margin-bottom: 20px;
    
    .stat-item {
      padding: 20px;
      border-radius: 8px;
      text-align: center;
      background: #f5f7fa;
      
      &.enabled { background: #e8f5e9; }
      &.disabled { background: #ffebee; }
      
      .stat-value {
        font-size: 32px;
        font-weight: bold;
        color: #303133;
      }
      
      .stat-label {
        font-size: 14px;
        color: #909399;
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
