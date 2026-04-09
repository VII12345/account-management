<!--
  文件注释：frontend/src/components/TaskCenter/TaskCenter.vue

  职责：承载任务中心主页面，组织任务列表展示、筛选条件与批量操作入口。
  边界：仅处理页面交互与状态展示，不在本文件中实现任务调度执行能力。
-->
<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

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
  container: string
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
const router = useRouter()
const searchKeyword = ref<string>('')
const selectedRows = ref<number[]>([])
const isModalVisible = ref(false)
const newTask = ref<Partial<TaskData>>({})

// 过滤后的任务列表（根据搜索关键词动态过滤）
const filteredTaskList = computed<TaskData[]>(() => {
  const keyword = searchKeyword.value.trim().toLowerCase()
  if (!keyword) return taskList.value
  return taskList.value.filter(task =>
    task.name.toLowerCase().includes(keyword) ||
    task.strategyName.toLowerCase().includes(keyword) ||
    task.platform.toLowerCase().includes(keyword)
  )
})

// 各平台任务数数据
const platformTaskData = computed<ChartData[]>(() => {
  const platforms = [
    { key: 'X', label: 'X (Twitter)' },
    { key: 'TikTok', label: 'TikTok' },
    { key: 'Instagram', label: 'Instagram' },
    { key: 'Facebook', label: 'Facebook' },
    { key: 'YouTube', label: 'YouTube' }
  ]
  return platforms.map(p => {
    const tasks = filteredTaskList.value.filter(t => t.platform === p.key)
    const total = tasks.length
    const strategy = tasks.filter(t => t.type === '策略任务').length
    const instruction = tasks.filter(t => t.type === '指令任务').length
    return { name: p.label, values: [total, strategy, instruction] }
  })
})

// 各容器任务数数据
const containerTaskData = computed<ChartData[]>(() => {
  const containers = ['指纹浏览器 (AdsPower)', '云手机 (Redfinger)', '自研云环境']
  return containers.map(container => {
    const tasks = filteredTaskList.value.filter(t => t.container === container)
    const total = tasks.length
    const strategy = tasks.filter(t => t.type === '策略任务').length
    const instruction = tasks.filter(t => t.type === '指令任务').length
    return { name: container, values: [total, strategy, instruction] }
  })
})

// 策略排行
const strategyRankings = computed<StrategyRank[]>(() => {
  const counts: Record<string, number> = {}
  filteredTaskList.value.forEach(t => {
    if (t.strategyName && t.strategyName !== '-') {
      counts[t.strategyName] = (counts[t.strategyName] || 0) + 1
    }
  })
  const sorted = Object.entries(counts)
    .map(([name, count]) => ({ name, count }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 5) // 仅展示前5名，使其成为真正的“排行”
  return sorted.map((item, index) => ({ rank: index + 1, name: item.name, count: item.count }))
})

// 任务列表数据
const taskList = ref<TaskData[]>([
  {
    id: 1001,
    name: 'X-矩阵账号自动发文',
    type: '策略任务',
    status: '进行中',
    createTime: '2026-03-18 08:30:00',
    isOfficial: '是',
    platform: 'X',
    platformIcon: '✖️',
    strategyName: 'X-日常发推维护',
    accountCount: 150,
    batchCount: 5,
    container: '指纹浏览器 (AdsPower)'
  },
  {
    id: 1002,
    name: 'TikTok-美区达人评论区截流',
    type: '指令任务',
    status: '等待中',
    createTime: '2026-03-18 09:15:22',
    isOfficial: '否',
    platform: 'TikTok',
    platformIcon: '🎵',
    strategyName: '-',
    accountCount: 80,
    batchCount: 2,
    container: '云手机 (Redfinger)'
  },
  {
    id: 1003,
    name: 'Instagram-瑜伽标签点赞关注',
    type: '策略任务',
    status: '结束',
    createTime: '2026-03-17 14:20:10',
    isOfficial: '是',
    platform: 'Instagram',
    platformIcon: '📷',
    strategyName: 'Ins-精准粉引流',
    accountCount: 200,
    batchCount: 10,
    container: '指纹浏览器 (AdsPower)'
  },
  {
    id: 1004,
    name: 'YouTube-新视频前排刷赞',
    type: '指令任务',
    status: '异常',
    createTime: '2026-03-17 16:45:00',
    isOfficial: '否',
    platform: 'YouTube',
    platformIcon: '▶️',
    strategyName: '-',
    accountCount: 50,
    batchCount: 1,
    container: '自研云环境'
  },
  {
    id: 1005,
    name: 'Facebook-加密货币群组营销',
    type: '策略任务',
    status: '进行中',
    createTime: '2026-03-18 01:10:35',
    isOfficial: '是',
    platform: 'Facebook',
    platformIcon: '📘',
    strategyName: 'FB-群组定向推广',
    accountCount: 120,
    batchCount: 4,
    container: '指纹浏览器 (AdsPower)'
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

const handleView = (id: number): void => {
  router.push(`/task/detail/${id}`) // 请根据实际 router 配置调整跳转路径
}

const handleBatchCancel = (): void => {
  if (selectedRows.value.length === 0) {
    alert('请先选择要取消的任务')
    return
  }
  if (window.confirm(`确定要取消选中的 ${selectedRows.value.length} 个任务吗？`)) {
    taskList.value.forEach(task => {
      if (selectedRows.value.includes(task.id) && task.status !== '结束' && task.status !== '已取消') {
        task.status = '已取消'
      }
    })
    selectedRows.value = [] // 取消后清空选中状态
  }
}

const handleCancelSingle = (task: TaskData): void => {
  if (task.status === '结束' || task.status === '已取消') {
    alert('当前状态无法取消该任务')
    return
  }
  if (window.confirm(`确定要取消任务 "${task.name}" 吗？`)) {
    task.status = '已取消'
  }
}

const handleAddTask = (): void => {
  newTask.value = {
    name: '',
    type: '策略任务',
    platform: 'X',
    strategyName: '',
    accountCount: 1,
    batchCount: 1,
    container: '指纹浏览器 (AdsPower)'
  }
  isModalVisible.value = true
}

const handleSaveTask = (): void => {
  if (!newTask.value.name) {
    alert('请输入任务名称')
    return
  }

  const now = new Date()
  const createTime = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')} ${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}:${String(now.getSeconds()).padStart(2, '0')}`
  const platformIcons: Record<string, string> = { 'X': '✖️', 'TikTok': '🎵', 'Instagram': '📷', 'Facebook': '📘', 'YouTube': '▶️' }
  const newId = taskList.value.length > 0 ? Math.max(...taskList.value.map(t => t.id)) + 1 : 1001

  taskList.value.unshift({
    id: newId,
    name: newTask.value.name,
    type: newTask.value.type || '策略任务',
    status: '等待中',
    createTime,
    isOfficial: '否',
    platform: newTask.value.platform || 'X',
    platformIcon: platformIcons[newTask.value.platform || 'X'] || '❓',
    strategyName: newTask.value.strategyName || '-',
    accountCount: newTask.value.accountCount || 1,
    batchCount: newTask.value.batchCount || 1,
    container: newTask.value.container || '指纹浏览器 (AdsPower)'
  })
  isModalVisible.value = false
}

const handleCancelTask = (): void => {
  isModalVisible.value = false
}

const handleSearch = (): void => {
  // Vue computed 特性会自动监听 searchKeyword 并更新 filteredTaskList，此处仅作保留或供防抖处理
}

const getBarHeight = (value: number, maxValue: number): number => {
  return (value / maxValue) * 100
}

const getStatusClass = (status: string): string => {
  switch (status) {
    case '进行中': return 'status-running'
    case '结束': return 'status-completed'
    case '等待中': return 'status-waiting'
    case '异常': return 'status-error'
    case '已取消': return 'status-canceled'
    default: return ''
  }
}

const maxPlatformValue = computed(() => {
  const max = Math.max(...platformTaskData.value.flatMap(d => d.values))
  return max > 0 ? max : 1 // 防止全空时出现计算分母为 0 导致报错
})
const maxContainerValue = computed(() => {
  const max = Math.max(...containerTaskData.value.flatMap(d => d.values))
  return max > 0 ? max : 1
})
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
              <circle cx="12" cy="12" r="10" stroke-width="2" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 16v-4M12 8h.01" />
            </svg>
          </div>
          <div class="chart-unit">
            单位：
            <svg width="14" height="14" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
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
              <circle cx="12" cy="12" r="10" stroke-width="2" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 16v-4M12 8h.01" />
            </svg>
          </div>
          <div class="chart-unit">
            单位：
            <svg width="14" height="14" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
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
                <div class="bar blue wide"
                  :style="{ height: getBarHeight(data.values[0] ?? 0, maxContainerValue) + '%' }">
                  <span class="bar-value">{{ data.values[0] ?? 0 }}</span>
                </div>
                <div class="bar red wide"
                  :style="{ height: getBarHeight(data.values[1] ?? 0, maxContainerValue) + '%' }">
                  <span class="bar-value">{{ data.values[1] ?? 0 }}</span>
                </div>
                <div class="bar gray wide"
                  :style="{ height: getBarHeight(data.values[2] ?? 0, maxContainerValue) + '%' }">
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
              <circle cx="12" cy="12" r="10" stroke-width="2" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 16v-4M12 8h.01" />
            </svg>
          </div>
        </div>
        <div class="ranking-list">
          <div v-if="strategyRankings.length === 0" class="no-data">暂无策略数据</div>
          <template v-else>
            <div v-for="item in strategyRankings" :key="item.rank" class="ranking-item">
              <div class="rank-badge">{{ item.rank }}</div>
              <div class="rank-name">{{ item.name }}</div>
              <div class="rank-count">{{ item.count }}</div>
            </div>
          </template>
        </div>
      </div>
    </div>

    <!-- 任务列表 -->
    <div class="task-list-section">
      <div class="task-list-header">
        <h3 class="section-title">任务列表</h3>
        <div class="task-actions">
          <button @click="handleBatchCancel" class="btn-secondary">批量取消</button>
          <button @click="handleAddTask" class="btn-primary-dropdown">
            添加任务
            <svg class="dropdown-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </button>
          <div class="search-box">
            <input v-model="searchKeyword" type="text" placeholder="请输入关键词" class="search-input"
              @keyup.enter="handleSearch" />
            <svg class="search-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
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
            <tr v-for="task in filteredTaskList" :key="task.id">
              <td>
                <input type="checkbox" :checked="selectedRows.includes(task.id)"
                  @change="() => handleRowSelect(task.id)" />
              </td>
              <td>{{ task.id }}</td>
              <td class="task-name">{{ task.name }}</td>
              <td>{{ task.type }}</td>
              <td>
                <span class="status-badge" :class="getStatusClass(task.status)">
                  {{ task.status }}
                </span>
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
                <button class="action-link" @click="handleView(task.id)">查看</button>
                <button class="action-link">分天查看</button>
                <button class="action-link" @click="handleCancelSingle(task)">取消</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 添加任务弹窗 -->
    <div v-if="isModalVisible" class="modal-overlay" @click.self="handleCancelTask">
      <div class="modal-content">
        <h3>添加任务</h3>
        <div class="form-group">
          <label>任务名称：</label>
          <input v-model="newTask.name" class="form-input" placeholder="请输入任务名称" />

          <label>任务类型：</label>
          <select v-model="newTask.type" class="form-input">
            <option value="策略任务">策略任务</option>
            <option value="指令任务">指令任务</option>
          </select>

          <label>平台：</label>
          <select v-model="newTask.platform" class="form-input">
            <option value="X">X (Twitter)</option>
            <option value="TikTok">TikTok</option>
            <option value="Instagram">Instagram</option>
            <option value="Facebook">Facebook</option>
            <option value="YouTube">YouTube</option>
          </select>

          <label>策略名称：</label>
          <input v-model="newTask.strategyName" class="form-input" placeholder="请输入策略名称，如无请填-" />

          <label>账号数量：</label>
          <input type="number" v-model="newTask.accountCount" class="form-input" placeholder="请输入账号数量" />

          <label>批次：</label>
          <input type="number" v-model="newTask.batchCount" class="form-input" placeholder="请输入批次" />

          <label>运行容器：</label>
          <select v-model="newTask.container" class="form-input">
            <option value="指纹浏览器 (AdsPower)">指纹浏览器 (AdsPower)</option>
            <option value="云手机 (Redfinger)">云手机 (Redfinger)</option>
            <option value="自研云环境">自研云环境</option>
          </select>
        </div>
        <div class="modal-actions">
          <button class="btn-cancel" @click="handleCancelTask">取消</button>
          <button class="btn-confirm" @click="handleSaveTask">保存</button>
        </div>
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
  background-color: #f5f7fa;
  background-image: url('/image/background.jpg');
  background-size: cover;
  background-position: center top;
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

.legend-dot.blue {
  background: #60a5fa;
}

.legend-dot.red {
  background: #f87171;
}

.legend-dot.gray {
  background: #94a3b8;
}

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

.bar.blue {
  background: #60a5fa;
}

.bar.red {
  background: #f87171;
}

.bar.gray {
  background: #94a3b8;
}

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

.no-data {
  text-align: center;
  color: #9ca3af;
  font-size: 0.875rem;
  margin-top: 2rem;
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

.status-running {
  background: #dbeafe;
  color: #1e40af;
}

.status-waiting {
  background: #fef3c7;
  color: #92400e;
}

.status-error {
  background: #fee2e2;
  color: #991b1b;
}

.status-canceled {
  background: #f3f4f6;
  color: #6b7280;
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

/* 弹窗样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 0.75rem;
  width: 450px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

.modal-content h3 {
  margin-top: 0;
  margin-bottom: 1.5rem;
  font-size: 1.25rem;
  color: #111827;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  max-height: 60vh;
  overflow-y: auto;
}

.form-group label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
  margin-top: 0.5rem;
}

.form-input {
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  padding: 0.5rem;
  font-size: 0.875rem;
  outline: none;
  transition: border-color 0.2s;
}

.form-input:focus {
  border-color: #2563eb;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

.btn-cancel {
  background: #f9fafb;
  border: 1px solid #d1d5db;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  color: #374151;
  cursor: pointer;
}

.btn-confirm {
  background: #2563eb;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  cursor: pointer;
}
</style>