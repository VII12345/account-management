<!-- TaskCenter.vue -->
<script setup lang="ts">
import { ref } from 'vue'

// 类型定义
interface TaskData {
  id: number
  name: string
  type: string
  status: string
  createTime: string
  isOfficial: string
  platform: string
  platformIcon: string
  strategyName: string
  accountCount: number
  batchCount: number
}

interface ChartData {
  name: string
  values: number[]
}

interface StrategyRank {
  rank: number
  name: string
  count: number
}

// 状态
const searchKeyword = ref<string>('')
const selectedRows = ref<number[]>([])

// 各平台任务数数据
const platformTaskData: ChartData[] = [
  { name: 'X(Twitter)', values: [270, 30, 240] },
  { name: 'Tik Tok（Web）', values: [115, 15, 100] },
  { name: 'YouTube', values: [45, 5, 40] }
]

// 各容器任务数数据
const containerTaskData: ChartData[] = [
  { name: '指纹浏览器', values: [750, 50, 700] }
]

// 策略排行
const strategyRankings: StrategyRank[] = [
  { rank: 1, name: 'x(推荐浏览-培育', count: 30 },
  { rank: 2, name: 'fb_首页浏览-培育', count: 5 },
  { rank: 3, name: 'ins_首页浏览-培育', count: 5 }
]

// 任务列表数据
const taskList = ref<TaskData[]>([
  {
    id: 1,
    name: 'Instagram-主页...',
    type: '指令任务',
    status: '结束',
    createTime: '2025-08-18 20:26:32',
    isOfficial: '否',
    platform: 'Instagram',
    platformIcon: '📷',
    strategyName: '-',
    accountCount: 1,
    batchCount: 1
  },
  {
    id: 2,
    name: 'Tik Tok(Web)-主...',
    type: '指令任务',
    status: '结束',
    createTime: '2025-08-18 20:00:00',
    isOfficial: '否',
    platform: 'TikTok',
    platformIcon: '🎵',
    strategyName: '-',
    accountCount: 1,
    batchCount: 1
  },
  {
    id: 3,
    name: 'X(Twitter)-主页...',
    type: '指令任务',
    status: '结束',
    createTime: '2025-08-18 19:06:43',
    isOfficial: '否',
    platform: 'X',
    platformIcon: '❌',
    strategyName: '-',
    accountCount: 1,
    batchCount: 1
  },
  {
    id: 4,
    name: 'Instagram-主页...',
    type: '指令任务',
    status: '结束',
    createTime: '2025-08-18 19:00:56',
    isOfficial: '否',
    platform: 'Instagram',
    platformIcon: '📷',
    strategyName: '-',
    accountCount: 1,
    batchCount: 1
  }
])

// 方法
const handleRowSelect = (id: number): void => {
  const index = selectedRows.value.indexOf(id)
  if (index !== -1) {
    selectedRows.value.splice(index, 1)
  } else {
    selectedRows.value.push(id)
  }
}

const handleBatchSelect = (): void => {
  console.log('批量取消')
}

const handleAddTask = (): void => {
  console.log('添加任务')
}

const handleSearch = (): void => {
  console.log('搜索:', searchKeyword.value)
}

const getBarHeight = (value: number, maxValue: number): number => {
  return (value / maxValue) * 100
}

const maxPlatformValue = Math.max(...platformTaskData.flatMap(d => d.values))
const maxContainerValue = Math.max(...containerTaskData.flatMap(d => d.values))
</script>

<template>
  <div class="task-center-container">
    <!-- 页面标题 -->
    <div class="page-header">
      <h2 class="page-title">任务中心</h2>
    </div>

    <!-- 数据统计图表区域 -->
    <div class="charts-grid">
      <!-- 各平台任务数 -->
      <div class="chart-card">
        <div class="chart-header">
          <div class="chart-title-wrapper">
            <h3 class="chart-title">各平台任务数</h3>
            <svg class="help-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <circle cx="12" cy="12" r="10" stroke-width="2"/>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 16v-4M12 8h.01"/>
            </svg>
          </div>
          <div class="chart-unit">
            单位：
            <svg width="14" height="14" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/>
            </svg>
          </div>
        </div>
        <div class="chart-legend">
          <span class="legend-item"><span class="legend-dot blue"></span>全部任务</span>
          <span class="legend-item"><span class="legend-dot red"></span>策略任务</span>
          <span class="legend-item"><span class="legend-dot gray"></span>指令任务</span>
        </div>
        <div class="chart-content">
          <div class="bar-chart">
            <div class="bar-group" v-for="data in platformTaskData" :key="data.name">
              <div class="bars-container">
                <div class="bar blue" :style="{ height: getBarHeight(data.values[0] ?? 0, maxPlatformValue) + '%' }">
                  <span class="bar-value">{{ data.values[0] ?? 0 }}</span>
                </div>
                <div class="bar red" :style="{ height: getBarHeight(data.values[1] ?? 0, maxPlatformValue) + '%' }">
                  <span class="bar-value">{{ data.values[1] ?? 0 }}</span>
                </div>
                <div class="bar gray" :style="{ height: getBarHeight(data.values[2] ?? 0, maxPlatformValue) + '%' }">
                  <span class="bar-value">{{ data.values[2] ?? 0 }}</span>
                </div>
              </div>
              <div class="bar-label">{{ data.name }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 各容器任务数 -->
      <div class="chart-card">
        <div class="chart-header">
          <div class="chart-title-wrapper">
            <h3 class="chart-title">各容器任务数</h3>
            <svg class="help-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <circle cx="12" cy="12" r="10" stroke-width="2"/>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 16v-4M12 8h.01"/>
            </svg>
          </div>
          <div class="chart-unit">
            单位：
            <svg width="14" height="14" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/>
            </svg>
          </div>
        </div>
        <div class="chart-legend">
          <span class="legend-item"><span class="legend-dot blue"></span>全部任务</span>
          <span class="legend-item"><span class="legend-dot red"></span>策略任务</span>
          <span class="legend-item"><span class="legend-dot gray"></span>指令任务</span>
        </div>
        <div class="chart-content">
          <div class="bar-chart">
            <div class="bar-group" v-for="data in containerTaskData" :key="data.name">
              <div class="bars-container">
                <div class="bar blue wide" :style="{ height: getBarHeight(data.values[0] ?? 0, maxContainerValue) + '%' }">
                  <span class="bar-value">{{ data.values[0] ?? 0 }}</span>
                </div>
                <div class="bar red wide" :style="{ height: getBarHeight(data.values[1] ?? 0, maxContainerValue) + '%' }">
                  <span class="bar-value">{{ data.values[1] ?? 0 }}</span>
                </div>
                <div class="bar gray wide" :style="{ height: getBarHeight(data.values[2] ?? 0, maxContainerValue) + '%' }">
                  <span class="bar-value">{{ data.values[2] ?? 0 }}</span>
                </div>
              </div>
              <div class="bar-label">{{ data.name }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 策略排行 -->
      <div class="chart-card ranking-card">
        <div class="chart-header">
          <div class="chart-title-wrapper">
            <h3 class="chart-title">策略排行</h3>
            <svg class="help-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <circle cx="12" cy="12" r="10" stroke-width="2"/>
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 16v-4M12 8h.01"/>
            </svg>
          </div>
        </div>
        <div class="ranking-list">
          <div v-for="item in strategyRankings" :key="item.rank" class="ranking-item">
            <div class="rank-badge">{{ item.rank }}</div>
            <div class="rank-name">{{ item.name }}</div>
            <div class="rank-count">{{ item.count }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 任务列表 -->
    <div class="task-list-section">
      <div class="task-list-header">
        <h3 class="section-title">任务列表</h3>
        <div class="task-actions">
          <button @click="handleBatchSelect" class="btn-secondary">批量取消</button>
          <button @click="handleAddTask" class="btn-primary-dropdown">
            添加任务
            <svg class="dropdown-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </button>
          <div class="search-box">
            <input
              v-model="searchKeyword"
              type="text"
              placeholder="请输入关键词"
              class="search-input"
              @keyup.enter="handleSearch"
            />
            <svg class="search-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
        </div>
      </div>

      <!-- 表格 -->
      <div class="table-container">
        <table class="task-table">
          <thead>
            <tr>
              <th class="col-checkbox" rowspan="2">
                <input type="checkbox" />
              </th>
              <th class="col-id" rowspan="2">序号</th>
              <th colspan="2" class="col-task-info">任务信息</th>
              <th colspan="4" class="col-strategy-info">策略信息</th>
              <th class="col-actions" rowspan="2">操作</th>
            </tr>
            <tr class="sub-header">
              <th class="sortable">任务名称 ▼</th>
              <th class="sortable">任务类型 ▼</th>
              <th class="sortable">任务状态 ▼</th>
              <th>任务创建时间</th>
              <th class="sortable">是否器平台 ▼</th>
              <th class="sortable">平台 ▼</th>
              <th>策略名称</th>
              <th>账号数量</th>
              <th>批次个</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="task in taskList" :key="task.id">
              <td>
                <input
                  type="checkbox"
                  :checked="selectedRows.includes(task.id)"
                  @change="() => handleRowSelect(task.id)"
                />
              </td>
              <td>{{ task.id }}</td>
              <td class="task-name">{{ task.name }}</td>
              <td>{{ task.type }}</td>
              <td>
                <span class="status-badge status-completed">{{ task.status }}</span>
              </td>
              <td class="time-cell">{{ task.createTime }}</td>
              <td>{{ task.isOfficial }}</td>
              <td>
                <span class="platform-icon">{{ task.platformIcon }}</span>
              </td>
              <td>{{ task.strategyName }}</td>
              <td>{{ task.accountCount }}</td>
              <td>{{ task.batchCount }}</td>
              <td class="actions-cell">
                <button class="action-link">查看</button>
                <button class="action-link">分天查看</button>
                <button class="action-link">取消</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.task-center-container {
  padding: 1.5rem 2rem;
  background: #f5f7fa;
  min-height: 100vh;
}

.page-header {
  margin-bottom: 1.5rem;
}

.page-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #111827;
}

/* 图表网格 */
.charts-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.chart-card {
  background: white;
  border-radius: 0.5rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.chart-title-wrapper {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.chart-title {
  font-size: 1rem;
  font-weight: 600;
  color: #374151;
}

.help-icon {
  width: 16px;
  height: 16px;
  color: #9ca3af;
  cursor: pointer;
}

.chart-unit {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.875rem;
  color: #6b7280;
}

.chart-legend {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  font-size: 0.875rem;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.legend-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.legend-dot.blue { background: #60a5fa; }
.legend-dot.red { background: #f87171; }
.legend-dot.gray { background: #94a3b8; }

/* 柱状图 */
.chart-content {
  height: 250px;
}

.bar-chart {
  display: flex;
  align-items: flex-end;
  justify-content: space-around;
  height: 100%;
  padding: 1rem 0;
}

.bar-group {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
}

.bars-container {
  display: flex;
  align-items: flex-end;
  gap: 0.25rem;
  height: 200px;
  margin-bottom: 0.5rem;
}

.bar {
  width: 30px;
  border-radius: 0.25rem 0.25rem 0 0;
  position: relative;
  transition: all 0.3s;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding-top: 0.25rem;
}

.bar.wide {
  width: 50px;
}

.bar.blue { background: #60a5fa; }
.bar.red { background: #f87171; }
.bar.gray { background: #94a3b8; }

.bar-value {
  font-size: 0.75rem;
  color: white;
  font-weight: 600;
}

.bar-label {
  font-size: 0.75rem;
  color: #6b7280;
  text-align: center;
  max-width: 100px;
}

/* 策略排行 */
.ranking-card {
  display: flex;
  flex-direction: column;
}

.ranking-list {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.ranking-item {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.rank-badge {
  width: 36px;
  height: 36px;
  border-radius: 0.375rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  font-size: 0.875rem;
  background: #3b82f6;
}

.rank-name {
  flex: 1;
  font-size: 0.875rem;
  color: #374151;
}

.rank-count {
  font-size: 1rem;
  font-weight: 600;
  color: #111827;
}

/* 任务列表 */
.task-list-section {
  background: white;
  border-radius: 0.5rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.task-list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.section-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #111827;
}

.task-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.btn-secondary {
  background: white;
  border: 1px solid #d1d5db;
  color: #374151;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-secondary:hover {
  background: #f9fafb;
  border-color: #9ca3af;
}

.btn-primary-dropdown {
  background: #2563eb;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: background 0.2s;
}

.btn-primary-dropdown:hover {
  background: #1d4ed8;
}

.dropdown-icon {
  width: 16px;
  height: 16px;
}

.search-box {
  position: relative;
}

.search-input {
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  padding: 0.5rem 2.5rem 0.5rem 1rem;
  font-size: 0.875rem;
  outline: none;
  width: 240px;
}

.search-input:focus {
  border-color: #2563eb;
}

.search-icon {
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  width: 18px;
  height: 18px;
  color: #9ca3af;
}

/* 表格 */
.table-container {
  overflow-x: auto;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
}

.task-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.875rem;
}

.task-table thead {
  background: #f9fafb;
}

.task-table th {
  padding: 0.75rem 1rem;
  text-align: left;
  font-weight: 600;
  color: #374151;
  border-bottom: 1px solid #e5e7eb;
}

.task-table .sub-header th {
  font-size: 0.8125rem;
  color: #6b7280;
  padding: 0.5rem 1rem;
}

.col-task-info {
  background: #fef3c7;
}

.col-strategy-info {
  background: #dbeafe;
}

.sortable {
  cursor: pointer;
}

.task-table td {
  padding: 0.75rem 1rem;
  color: #374151;
  border-bottom: 1px solid #f3f4f6;
}

.task-table tbody tr:hover {
  background: #f9fafb;
}

.task-name {
  color: #2563eb;
  font-weight: 500;
}

.status-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
}

.status-completed {
  background: #d1fae5;
  color: #065f46;
}

.time-cell {
  font-size: 0.8125rem;
  color: #6b7280;
}

.platform-icon {
  font-size: 1.25rem;
}

.actions-cell {
  display: flex;
  gap: 0.5rem;
}

.action-link {
  background: none;
  border: none;
  color: #2563eb;
  cursor: pointer;
  font-size: 0.875rem;
  padding: 0.25rem 0.5rem;
  transition: color 0.2s;
}

.action-link:hover {
  color: #1d4ed8;
  text-decoration: underline;
}

.col-checkbox {
  width: 40px;
}

.col-id {
  width: 60px;
}

.col-actions {
  width: 200px;
}

@media (max-width: 1280px) {
  .charts-grid {
    grid-template-columns: 1fr;
  }
}
</style>