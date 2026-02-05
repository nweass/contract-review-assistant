<template>
  <div class="history-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>审查历史</span>
          <el-button type="primary" @click="exportHistory">
            <el-icon><Download /></el-icon>
            导出记录
          </el-button>
        </div>
      </template>
      
      <!-- 筛选条件 -->
      <div class="filters">
        <el-form :inline="true">
          <el-form-item label="审查部门">
            <el-select v-model="filterDepartment" clearable>
              <el-option label="全部" value="" />
              <el-option label="投资监督部" value="investment_supervision" />
              <el-option label="风险合规部" value="risk_compliance" />
              <el-option label="估值服务部" value="valuation_service" />
              <el-option label="结算服务部" value="settlement_service" />
            </el-select>
          </el-form-item>
          <el-form-item label="状态">
            <el-select v-model="filterStatus" clearable>
              <el-option label="全部" value="" />
              <el-option label="通过" value="passed" />
              <el-option label="警告" value="warning" />
              <el-option label="问题" value="failed" />
            </el-select>
          </el-form-item>
          <el-form-item label="日期">
            <el-date-picker
              v-model="filterDate"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
            />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="search">查询</el-button>
            <el-button @click="resetFilter">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
      
      <!-- 历史列表 -->
      <el-table :data="historyList" stripe style="width: 100%">
        <el-table-column type="index" width="50" />
        <el-table-column prop="fileName" label="文件名称" min-width="200" />
        <el-table-column prop="department" label="审查部门" width="120" />
        <el-table-column prop="productName" label="产品名称" width="150" />
        <el-table-column prop="result" label="结果" width="100">
          <template #default="{ row }">
            <el-tag :type="getResultType(row.result)">
              {{ getResultText(row.result) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="summary" label="统计" width="150">
          <template #default="{ row }">
            <span>通过:{{ row.passed }} 警告:{{ row.warnings }} 问题:{{ row.errors }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="reviewTime" label="审查时间" width="180" />
        <el-table-column label="操作" width="150">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="viewDetail(row)">查看</el-button>
            <el-button type="info" size="small" @click="reReview(row)">重审</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="loadHistory"
          @current-change="loadHistory"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Download } from '@element-plus/icons-vue'

const historyList = ref([])
const filterDepartment = ref('')
const filterStatus = ref('')
const filterDate = ref(null)
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(100)

const getResultType = (status) => {
  const types = { passed: 'success', warning: 'warning', failed: 'danger' }
  return types[status] || 'info'
}

const getResultText = (status) => {
  const texts = { passed: '通过', warning: '警告', failed: '问题' }
  return texts[status] || status
}

const loadHistory = () => {
  // 模拟数据
  historyList.value = [
    { fileName: 'XX基金合同.pdf', department: '投资监督部', productName: 'XX公募基金', result: 'passed', passed: 8, warnings: 2, errors: 0, reviewTime: '2025-02-05 10:30:00' },
    { fileName: 'YY托管协议.docx', department: '风险合规部', productName: 'YY企业年金', result: 'warning', passed: 6, warnings: 3, errors: 1, reviewTime: '2025-02-05 09:15:00' },
    { fileName: 'ZZ基金合同.pdf', department: '结算服务部', productName: 'ZZ货币基金', result: 'passed', passed: 10, warnings: 0, errors: 0, reviewTime: '2025-02-04 16:45:00' }
  ]
}

const search = () => {
  currentPage.value = 1
  loadHistory()
}

const resetFilter = () => {
  filterDepartment.value = ''
  filterStatus.value = ''
  filterDate.value = null
  search()
}

const viewDetail = (row) => {
  ElMessage.info('查看详情功能开发中')
}

const reReview = (row) => {
  ElMessage.info('重新审查功能开发中')
}

const exportHistory = () => {
  ElMessage.success('导出功能开发中')
}

onMounted(() => {
  loadHistory()
})
</script>

<style lang="scss" scoped>
.history-page {
  .filters {
    margin-bottom: 20px;
  }
  
  .pagination {
    margin-top: 20px;
    display: flex;
    justify-content: flex-end;
  }
  
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
}
</style>
