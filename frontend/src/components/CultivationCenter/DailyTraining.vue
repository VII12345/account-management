<!-- DailyTraining.vue -->
<script setup lang="ts">
import { ref } from 'vue'

// 类型定义
interface TrainingAccount {
  id: number
  platform: string
  level: string
  status: string
  tag: string
  region: string
  browser: string
  lastActive: string
}

// 菜单状态
const activeMenu = ref<string>('培育中心')
const activeSubMenu = ref<string>('日常培育')

// 菜单结构
const menuItems = [
  { id: 'training', label: '培育中心', children: ['日常培育', '账号监控'] },
  { id: 'task', label: '任务管理', children: ['任务列表', '任务日志'] },
  { id: 'tools', label: '工具中心', children: [] },
]

// 筛选条件
const selectedPlatform = ref<string>('')
const selectedLevel = ref<string[]>([])
const selectedStatus = ref<string>('')
const selectedTag = ref<string>('')
const selectedRegion = ref<string>('')
const selectedBrowser = ref<string>('')


const searchKeyword = ref<string>('')

const platforms = ['抖音', '快手', '小红书', 'B站', '微博']
const accountLevels = ['普通号', '培育号', '精品号', '大V号']
const lifeStatus = ['正常', '异常', '封禁']
const tags = ['美食', '旅游', '科技', '娱乐']
const regions = ['华北', '华东', '华南', '西南', '东北']
const browsers = ['Chrome', 'Edge', 'Firefox', 'Safari']

// 表格数据
const tableData = ref<TrainingAccount[]>([])
const totalRecords = ref<number>(0)
const currentPage = ref<number>(1)
const pageSize = ref<number>(20)

// 方法
const handleClearFilters = () => {
  selectedPlatform.value = ''
  selectedLevel.value = []
  selectedStatus.value = ''
  selectedTag.value = ''
  selectedRegion.value = ''
  selectedBrowser.value = ''
  searchKeyword.value = ''
}

const handleCreateTask = () => {
  console.log('创建任务')
}

const handlePageChange = (page: number) => {
  if (page < 1) return
  currentPage.value = page
}

const handleMenuClick = (label: string) => {
  activeMenu.value = label
}
const handleSearch = (): void => {
  console.log('搜索:', searchKeyword.value)
}
const handleSubMenuClick = (label: string) => {
  activeSubMenu.value = label
}
</script>

<template>
  <div class="training-container">
    <!-- 左侧菜单栏 -->

    <!-- 主体部分 -->
    <main class="main-content">
      <!-- 面包屑 -->
      <div class="breadcrumb">
        <span class="breadcrumb-item">培育中心</span>
        <span class="breadcrumb-separator">›</span>
        <span class="breadcrumb-item active">日常培育</span>
      </div>

      <!-- 页头 -->
      <div class="page-header">
        <h2 class="page-title">账号列表</h2>
        <div class="header-actions">
          <div class="search-box">
            <input
                v-model="selectedTag"
                type="text"
                placeholder="请输入关键词"
                class="search-input"
              />
              <button @click="handleSearch" class="search-button">
                <svg class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </button>
            </div>
          <button class="btn-primary" @click="handleCreateTask">创建任务</button>
        </div>
      </div>

      <!-- 筛选区 -->
      <div class="filters-section">
        <div class="filter-row">
          <div class="filter-item">
            <label class="filter-label">平台：</label>
            <select v-model="selectedPlatform" class="filter-select">
              <option value="">请选择</option>
              <option v-for="p in platforms" :key="p" :value="p">{{ p }}</option>
            </select>
          </div>

          <div class="filter-item">
            <label class="filter-label">账号等级：</label>
            <div class="multi-select">
              <button class="select-button">
                {{ selectedLevel.length ? selectedLevel.join('、') : '请选择' }}
                <span class="arrow">▾</span>
              </button>
              <div class="dropdown">
                <label v-for="level in accountLevels" :key="level" class="dropdown-item">
                  <input type="checkbox" :value="level" v-model="selectedLevel" />
                  {{ level }}
                </label>
              </div>
            </div>
          </div>

          <div class="filter-item">
            <label class="filter-label">生存状态：</label>
            <select v-model="selectedStatus" class="filter-select">
              <option value="">请选择</option>
              <option v-for="s in lifeStatus" :key="s" :value="s">{{ s }}</option>
            </select>
          </div>

          <div class="filter-item">
            <label class="filter-label">标签：</label>
            <select v-model="selectedTag" class="filter-select">
              <option value="">请选择</option>
              <option v-for="t in tags" :key="t" :value="t">{{ t }}</option>
            </select>
          </div>

          <div class="filter-item">
            <label class="filter-label">地区：</label>
            <select v-model="selectedRegion" class="filter-select">
              <option value="">请选择</option>
              <option v-for="r in regions" :key="r" :value="r">{{ r }}</option>
            </select>
          </div>

          <div class="filter-item">
            <label class="filter-label">浏览器类型：</label>
            <select v-model="selectedBrowser" class="filter-select">
              <option value="">请选择</option>
              <option v-for="b in browsers" :key="b" :value="b">{{ b }}</option>
            </select>
          </div>

          <button class="btn-clear" @click="handleClearFilters">清空筛选</button>
        </div>
      </div>

      <!-- 表格 -->
      <div class="table-container">
        <table class="data-table">
          <thead>
            <tr>
              <th>序号</th>
              <th>平台</th>
              <th>账号等级</th>
              <th>状态</th>
              <th>标签</th>
              <th>地区</th>
              <th>浏览器</th>
              <th>最近活跃</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="tableData.length === 0">
              <td colspan="8" class="empty-data">暂无数据</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 分页 -->
      <div class="pagination">
        <div class="pagination-info">共 {{ totalRecords }} 条数据</div>
        <div class="pagination-controls">
          <select v-model="pageSize" class="page-size-select">
            <option :value="20">20 条/页</option>
            <option :value="50">50 条/页</option>
            <option :value="100">100 条/页</option>
          </select>
          <button
            class="page-btn"
            :disabled="currentPage === 1"
            @click="handlePageChange(currentPage - 1)"
          >
            ‹
          </button>
          <button class="page-btn page-btn-active">{{ currentPage }}</button>
          <button class="page-btn" @click="handlePageChange(currentPage + 1)">›</button>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
/* 整体布局 */
.training-container {
  display: flex;
  min-height: 100vh;
  width: 100%;
  flex-direction: column;
  background-image: url('/image/background.jpg'); /* 替换为你的图片路径 */
  background-size: cover; /* 图片铺满容器 */
  background-position: center; /* 图片居中显示 */
  background-repeat: no-repeat; /* 不重复 */
}


/* 主体 */
.main-content {
  display: flex;
  flex-direction: column;
  flex: 1;
  padding: 1.5rem 2rem;
  min-height: 0; /* 防止子元素溢出 */
}

/* 面包屑 */
.breadcrumb {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  font-size: 0.875rem;
}
.breadcrumb-item {
  color: #9da0a4;
}
.breadcrumb-item.active {
  color: #d4d4d4;
}
.breadcrumb-separator {
  color: #9ca3af;
}

/* 页头 */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}
.page-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #111827;
}
.header-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}
.search-box {
  display: flex;
  align-items: center;
  background: white;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  overflow: hidden;
}

.search-input {
  border: none;
  outline: none;
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
  width: 240px;
}

.search-button {
  background: transparent;
  border: none;
  padding: 0.5rem 0.75rem;
  cursor: pointer;
  display: flex;
  align-items: center;
}

.search-button .icon {
  width: 18px;
  height: 18px;
  color: #6b7280;
}

.btn-primary {
  background: #2563eb;
  color: white;
  border: none;
  padding: 0.5rem 1.5rem;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-primary:hover {
  background: #1d4ed8;
}

/* 筛选区 */
.filters-section {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  padding: 1rem;
  margin-bottom: 1rem;
}
.filter-row {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  align-items: center;
}
.filter-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.filter-label {
  color: #374151;
  font-size: 0.875rem;
}
.filter-select {
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  padding: 0.375rem 0.75rem;
  font-size: 0.875rem;
  outline: none;
}
.btn-clear {
  background: white;
  border: 1px solid #d1d5db;
  color: #374151;
  padding: 0.375rem 1rem;
  border-radius: 0.375rem;
  cursor: pointer;
  margin-left: auto;
}
.btn-clear:hover {
  background: #f9fafb;
}

/* 多选下拉 */
.multi-select {
  position: relative;
}
.select-button {
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  padding: 0.375rem 0.75rem;
  background: white;
  cursor: pointer;
  font-size: 0.875rem;
}
.dropdown {
  display: none;
  position: absolute;
  top: 110%;
  left: 0;
  background: white;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
  padding: 0.5rem;
  z-index: 10;
}
.multi-select:hover .dropdown {
  display: block;
}
.dropdown-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  padding: 0.25rem 0;
}

/* 表格 */
.table-container {
  flex:1;
  background: white;
  border-radius: 0.5rem;
  overflow: auto;
  border: 1px solid #e5e7eb;
  margin-bottom: 1rem;
}
.data-table {
  width: 100%;
  border-collapse: collapse;
}
.data-table th,
.data-table td {
  padding: 0.75rem 1rem;
  text-align: left;
  font-size: 0.875rem;
  border-bottom: 1px solid #f3f4f6;
}
.data-table thead {
  background: #f9fafb;
  font-weight: 600;
  color: #374151;
}
.empty-data {
  text-align: center;
  color: #9ca3af;
  padding: 2rem;
}

/* 分页 */
.pagination {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: auto;
  padding: 1rem;
  background: white;
  border-radius: 0.5rem;
}
.pagination-info {
  color: #6b7280;
  font-size: 0.875rem;
}
.pagination-controls {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.page-size-select,
.page-btn {
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  padding: 0.375rem 0.75rem;
  font-size: 0.875rem;
  cursor: pointer;
  background: white;
}
.page-btn-active {
  background: #2563eb;
  color: white;
  border-color: #2563eb;
}
.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
