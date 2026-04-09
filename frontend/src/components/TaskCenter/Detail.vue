<!--
  文件注释：frontend/src/components/TaskCenter/Detail.vue

  职责：承载当前页面/组件的视图结构、交互事件与状态绑定。
  边界：仅处理前端展示与交互编排，不在此文件实现后端业务规则。
-->

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

// 基础信息
const taskName = ref('Instagram-主页发帖 (Instagram)')

// 图标 SVG 字符串 (精美线性图标)
const icons = {
  browser: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>`,
  address: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path></svg>`,
  scroll: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="2" width="14" height="20" rx="7"></rect><line x1="12" y1="6" x2="12" y2="10"></line></svg>`,
  close: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="15" y1="9" x2="9" y2="15"></line><line x1="9" y1="9" x2="15" y2="15"></line></svg>`,
  accounts: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path></svg>`,
  tasks: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><path d="M8 2v4"></path><path d="M16 2v4"></path><path d="M3 10h18"></path><path d="M8 14h.01"></path><path d="M12 14h4"></path><path d="M8 18h.01"></path><path d="M12 18h4"></path></svg>`,
  pending: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>`,
  running: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>`,
  success: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>`,
  failed: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>`
}

// 步骤统计数据
const stepStats = ref([
  { label: '打开浏览器', value: 1, icon: icons.browser },
  { label: '输入地址', value: 1, icon: icons.address },
  { label: '滑动页面', value: 1, icon: icons.scroll },
  { label: '关闭浏览器', value: 1, icon: icons.close }
])

// 核心指标数据
const coreMetrics = ref([
  { label: '执行账号数', value: 1, type: 'blue', icon: icons.accounts },
  { label: '子任务总数', value: 1, type: 'purple', icon: icons.tasks },
  { label: '待执行子任务', value: 0, type: 'gray', icon: icons.pending },
  { label: '进行中子任务', value: 0, type: 'orange', icon: icons.running },
  { label: '成功子任务', value: 1, type: 'green', icon: icons.success },
  { label: '失败子任务', value: 0, type: 'red', icon: icons.failed }
])

// 搜索关键词
const searchKeyword = ref('')

// 表格数据接口
interface SubTask {
  id: number
  batchNo: string
  username: string
  nickname: string
  status: 'success' | 'failed' | 'running' | 'waiting'
  platform: string
  vnc: string
  startTime: string
  endTime: string
}

// 表格模拟数据
const tableData = ref<SubTask[]>([
  {
    id: 1,
    batchNo: '2025-08-18-001',
    username: 'princessmpson',
    nickname: 'nabil',
    status: 'success',
    platform: 'Instagram',
    vnc: '指纹浏览器',
    startTime: '中国 北京 UTC+8\n2025-08-18 20:26:40',
    endTime: '中国 北京 UTC+8\n2025-08-18 20:31:15'
  }
])

// 分页数据
const total = ref(1)
const currentPage = ref(1)
const pageSize = ref(20)

const router = useRouter()

// 动作方法
const handleBack = () => {
  router.back()
}
const handleSearch = () => {
  console.log('搜索:', searchKeyword.value)
}
</script>

<template>
  <div class="page-wrapper">
    <header class="page-header">
      <div class="breadcrumb">
        <span>任务中心</span>
        <span class="separator">&gt;</span>
        <span class="current">执行计划管理</span>
      </div>
      <div class="title-row">
        <h2 class="page-title">执行计划管理</h2>
        <button class="btn-back" @click="handleBack">返回</button>
      </div>
    </header>

    <section class="dashboard-card">
      <div class="task-name">
        <strong>任务名称：</strong>{{ taskName }}
      </div>
      
      <div class="stats-container">
        <div class="steps-group">
          <div v-for="(step, index) in stepStats" :key="index" class="step-item">
            <div class="step-icon" v-html="step.icon"></div>
            <div class="step-info">
              <div class="step-label">{{ step.label }}</div>
              <div class="step-value">{{ step.value }}</div>
            </div>
            <div v-if="index < stepStats.length - 1" class="step-connector"></div>
          </div>
        </div>

        <div class="metrics-group">
          <div 
            v-for="(metric, index) in coreMetrics" 
            :key="index"
            class="metric-card"
            :class="`metric-${metric.type}`"
          >
            <div class="metric-icon-wrapper" v-html="metric.icon"></div>
            <div class="metric-content">
              <div class="metric-label">{{ metric.label }}</div>
              <div class="metric-value">{{ metric.value }}</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="table-section">
      <div class="table-header">
        <div class="tab-active">子任务列表</div>
        <div class="search-box">
          <input type="text" v-model="searchKeyword" placeholder="请输入关键词" />
          <span class="search-icon" @click="handleSearch">🔍</span>
        </div>
      </div>

      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th width="40"><input type="checkbox" /></th>
              <th width="60">序号</th>
              <th>批次号</th>
              <th>用户名</th>
              <th>昵称</th>
              <th>子任务状态 ▽</th>
              <th>平台 ▽</th>
              <th>VNC</th>
              <th>开始执行时间</th>
              <th>结束执行时间</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(row, index) in tableData" :key="row.id">
              <td><input type="checkbox" /></td>
              <td>{{ index + 1 }}</td>
              <td>{{ row.batchNo }}</td>
              <td>{{ row.username }}</td>
              <td>{{ row.nickname }}</td>
              <td>
                <span class="status-badge success" v-if="row.status === 'success'">
                  <span class="icon">✓</span> 成功
                </span>
              </td>
              <td>
                <span class="platform-info">
                  <span class="platform-icon">📷</span> {{ row.platform }}
                </span>
              </td>
              <td>
                <span class="vnc-info">
                  <span class="vnc-icon">💻</span> {{ row.vnc }}
                </span>
              </td>
              <td class="time-cell">{{ row.startTime }}</td>
              <td class="time-cell">{{ row.endTime }}</td>
              <td class="action-links">
                <a href="#">查看</a>
                <a href="#" class="disabled">重试</a>
                <a href="#" class="disabled">取消</a>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="pagination-area">
        <div class="total-info">共 {{ total }} 条数据</div>
        <div class="pagination-controls">
          <select v-model="pageSize">
            <option :value="20">20 条/页</option>
            <option :value="50">50 条/页</option>
          </select>
          <button class="page-btn disabled">&lt;</button>
          <button class="page-btn active">1</button>
          <button class="page-btn disabled">&gt;</button>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
/* 页面基础 */
.page-wrapper {
  padding: 20px 24px;
  min-height: 100vh;
  background-color: #f4f7f9; /* 浅灰偏蓝背景，类似图中的半透明底 */
  background-image: url('/image/background.jpg');
  background-size: cover;
  background-position: center top;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  color: #333;
}

/* 头部样式 */
.page-header {
  margin-bottom: 20px;
}
.breadcrumb {
  font-size: 13px;
  color: #666;
  margin-bottom: 12px;
}
.breadcrumb .separator {
  margin: 0 6px;
  color: #999;
}
.title-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.page-title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #333;
}
.btn-back {
  padding: 6px 16px;
  background: white;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  color: #333;
  transition: all 0.2s;
}
.btn-back:hover {
  border-color: #40a9ff;
  color: #40a9ff;
}

/* 仪表盘卡片 */
.dashboard-card {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  margin-bottom: 20px;
}
.task-name {
  font-size: 15px;
  margin-bottom: 20px;
  color: #1f2937;
}

/* 统计卡片区布局 */
.stats-container {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* 步骤条样式 */
.steps-group {
  display: flex;
  gap: 32px;
  align-items: center;
  flex-wrap: wrap;
}
.step-item {
  display: flex;
  align-items: center;
  background: white;
  border-radius: 12px;
  padding: 12px 20px;
  min-width: 150px;
  position: relative;
  box-shadow: 0 2px 10px rgba(0,0,0,0.03);
  border: 1px solid #f0f0f0;
  gap: 12px;
}
.step-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #f0fdfa;
  color: #0d9488;
  display: flex;
  align-items: center;
  justify-content: center;
}
.step-icon :deep(svg) {
  width: 20px;
  height: 20px;
}
.step-info {
  display: flex;
  flex-direction: column;
}
.step-label {
  font-size: 13px;
  color: #64748b;
  margin-bottom: 2px;
}
.step-value {
  font-size: 18px;
  font-weight: 700;
  color: #0f172a;
}
/* 步骤之间的连接 */
.step-connector {
  position: absolute;
  right: -26px;
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 12px;
  background-color: #cbd5e1;
  z-index: 1;
  height: 2px;
}
.step-connector::after {
  content: '';
  position: absolute;
  right: -4px;
  top: -3px;
  border-width: 4px;
  border-style: solid;
  border-color: transparent transparent transparent #cbd5e1;
}

/* 独立指标块 */
.metrics-group {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
}
.metric-card {
  border-radius: 12px;
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 16px;
  background: white;
  box-shadow: 0 2px 10px rgba(0,0,0,0.03);
  border: 1px solid #f0f0f0;
  transition: transform 0.2s, box-shadow 0.2s;
}
.metric-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0,0,0,0.08);
}
.metric-icon-wrapper {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.metric-icon-wrapper :deep(svg) {
  width: 24px;
  height: 24px;
}
.metric-content {
  display: flex;
  flex-direction: column;
}
.metric-label {
  font-size: 13px;
  color: #64748b;
  margin-bottom: 4px;
}
.metric-value {
  font-size: 24px;
  font-weight: 700;
  color: #0f172a;
}

/* 具体颜色 */
.metric-blue .metric-icon-wrapper { background: #eff6ff; color: #3b82f6; }
.metric-purple .metric-icon-wrapper { background: #faf5ff; color: #a855f7; }
.metric-gray .metric-icon-wrapper { background: #f1f5f9; color: #64748b; }
.metric-orange .metric-icon-wrapper { background: #fff7ed; color: #f97316; }
.metric-green .metric-icon-wrapper { background: #f0fdf4; color: #22c55e; }
.metric-red .metric-icon-wrapper { background: #fef2f2; color: #ef4444; }

/* 列表区 */
.table-section {
  background: white;
  border-radius: 8px;
  padding: 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  overflow: hidden;
}
.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  border-bottom: 1px solid #eee;
  background-color: rgba(255, 255, 255, 0.8);
}
.tab-active {
  padding: 16px 0;
  font-size: 15px;
  font-weight: 600;
  color: #3b82f6;
  border-bottom: 2px solid #3b82f6;
  margin-bottom: -1px;
}
.search-box {
  position: relative;
  display: flex;
  align-items: center;
}
.search-box input {
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  padding: 6px 30px 6px 12px;
  font-size: 13px;
  outline: none;
  width: 200px;
}
.search-box input:focus {
  border-color: #3b82f6;
}
.search-icon {
  position: absolute;
  right: 10px;
  color: #999;
  cursor: pointer;
  font-size: 14px;
}

/* 表格样式 */
.table-container {
  overflow-x: auto;
}
table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  font-size: 13px;
}
th {
  background-color: #fafafa;
  color: #666;
  font-weight: 500;
  padding: 12px 16px;
  white-space: nowrap;
}
td {
  padding: 12px 16px;
  border-bottom: 1px solid #f0f0f0;
  color: #333;
  vertical-align: middle;
}
tr:hover td {
  background-color: #f9f9f9;
}
.time-cell {
  white-space: pre-line; /* 支持换行符显示 */
  color: #666;
  line-height: 1.4;
}

/* 状态徽章与图标 */
.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 12px;
  border: 1px solid transparent;
}
.status-badge.success {
  background-color: #e6f4ea;
  color: #1e8e3e;
  border-color: #a8dab5;
}
.status-badge .icon {
  font-size: 10px;
  background: #1e8e3e;
  color: white;
  border-radius: 50%;
  width: 12px;
  height: 12px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
.platform-icon, .vnc-icon {
  color: #e1306c; /* IG代表色 */
  margin-right: 4px;
}
.vnc-icon {
  color: #3b82f6;
}

/* 操作列链接 */
.action-links a {
  color: #3b82f6;
  text-decoration: none;
  margin-right: 12px;
  font-size: 13px;
}
.action-links a.disabled {
  color: #ccc;
  cursor: not-allowed;
}
.action-links a:last-child {
  margin-right: 0;
}

/* 底部与分页 */
.pagination-area {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  color: #666;
  font-size: 13px;
}
.pagination-controls {
  display: flex;
  align-items: center;
  gap: 12px;
}
.pagination-controls select {
  border: 1px solid #d9d9d9;
  padding: 4px 8px;
  border-radius: 4px;
  outline: none;
}
.page-btn {
  border: 1px solid #d9d9d9;
  background: white;
  border-radius: 4px;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #333;
}
.page-btn.active {
  background: #3b82f6;
  color: white;
  border-color: #3b82f6;
}
.page-btn.disabled {
  color: #ccc;
  background: #f5f5f5;
  cursor: not-allowed;
}
</style>