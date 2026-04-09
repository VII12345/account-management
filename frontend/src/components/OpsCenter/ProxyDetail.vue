<!--
  文件注释：frontend/src/components/OpsCenter/ProxyDetail.vue

  职责：承载当前页面/组件的视图结构、交互事件与状态绑定。
  边界：仅处理前端展示与交互编排，不在此文件实现后端业务规则。
-->

<template>
  <div class="container-management">
    <!-- 面包屑 -->
    <div class="breadcrumb">
      <span>运维中心</span>
      <span class="separator">›</span>
      <span class="active">容器管理</span>
    </div>

    <!-- 统计卡片区域 -->
    <div class="stats-grid">
      <!-- 容器类型分布 -->
      <div class="card">
        <div class="card-header">
          <h3>容器类型分布</h3>
          <div class="total-info">
            <div class="label">总数量</div>
            <div class="value">{{ totalContainers }}</div>
          </div>
        </div>
        <div class="chart-container">
          <div class="pie-chart">
            <svg viewBox="0 0 100 100">
              <circle cx="50" cy="50" r="40" fill="none" stroke="#5CD1C8" stroke-width="20" stroke-dasharray="188 251" transform="rotate(-90 50 50)" />
              <circle cx="50" cy="50" r="40" fill="none" stroke="#5B8FF9" stroke-width="20" stroke-dasharray="63 251" stroke-dashoffset="-188" transform="rotate(-90 50 50)" />
            </svg>
            <div class="pie-center">
              <div class="center-label">使用内存</div>
            </div>
          </div>
        </div>
        <div class="legend">
          <div class="legend-item">
            <span class="legend-color" style="background-color: #5B8FF9;"></span>
            <span>比特浏览器</span>
          </div>
          <div class="legend-item">
            <span class="legend-color" style="background-color: #5CD1C8;"></span>
            <span>自研浏览器</span>
          </div>
        </div>
      </div>

      <!-- 使用内存 -->
      <div class="card">
        <h3 class="card-title">使用内存</h3>
        <div class="gauge-container">
          <div class="gauge-chart">
            <svg viewBox="0 0 200 120">
              <defs>
                <linearGradient id="gaugeGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" stop-color="#5B8FF9" />
                  <stop offset="100%" stop-color="#7BA3FF" />
                </linearGradient>
              </defs>
              <path d="M 20 100 A 80 80 0 0 1 180 100" fill="none" stroke="#E8E8E8" stroke-width="20" stroke-linecap="round" />
              <path d="M 20 100 A 80 80 0 0 1 114 32" fill="none" stroke="url(#gaugeGradient)" stroke-width="20" stroke-linecap="round" />
            </svg>
            <div class="gauge-value">{{ usagePercentage }}</div>
          </div>
        </div>
        <div class="gauge-labels">
          <span>0</span>
          <span>50</span>
          <span>100</span>
        </div>
      </div>

      <!-- 容器运行情况 -->
      <div class="card">
        <h3 class="card-title">容器运行情况</h3>
        <div class="status-card">
          <div class="total-count">{{ totalContainers }}</div>
          <div class="total-label">容器总数</div>
        </div>
        <div class="status-grid">
          <div class="status-item">
            <div class="status-value online">{{ onlineContainers }}</div>
            <div class="status-label">上线数量</div>
          </div>
          <div class="status-item">
            <div class="status-value offline">{{ offlineContainers }}</div>
            <div class="status-label">下线数量</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 容器管理表格 -->
    <div class="table-card">
      <div class="table-header">
        <h3>容器管理</h3>
      </div>

      <!-- 筛选栏 -->
      <div class="filter-bar">
        <div class="filter-item">
          <span class="filter-label">使用状态：</span>
          <button class="filter-select">
            请选择
            <span class="arrow">▼</span>
          </button>
        </div>
        <div class="filter-item">
          <span class="filter-label">资源状态：</span>
          <button class="filter-select">
            请选择
            <span class="arrow">▼</span>
          </button>
        </div>
        <div class="filter-item">
          <span class="filter-label">浏览器类型：</span>
          <button class="filter-select">
            请选择
            <span class="arrow">▼</span>
          </button>
        </div>
        <button class="clear-filter">清空筛选</button>
        <div class="spacer"></div>
        <div class="search-box">
          <input v-model="searchText" type="text" placeholder="请输入关键词" />
          <span class="search-icon">🔍</span>
        </div>
      </div>

      <!-- 表格 -->
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>
                <input v-model="selectAll" type="checkbox" @change="handleSelectAll" />
              </th>
              <th>序号</th>
              <th>容器名称</th>
              <th>镜像版本号</th>
              <th>容器地址</th>
              <th>浏览器类型</th>
              <th>操作系统</th>
              <th>浏览器版本号</th>
              <th>账号</th>
              <th>创建时间</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="container in containers" :key="container.id">
              <td>
                <input v-model="selectedContainers" :value="container.id" type="checkbox" />
              </td>
              <td>{{ container.id }}</td>
              <td>{{ container.name }}</td>
              <td>{{ container.mirrorVersion }}</td>
              <td>{{ container.address }}</td>
              <td>{{ container.browserType }}</td>
              <td>{{ container.os }}</td>
              <td>{{ container.browserVersion }}</td>
              <td>{{ container.account }}</td>
              <td>-</td>
              <td>
                <div class="action-buttons">
                  <button @click="handleDetail(container.id)" class="action-btn">详情</button>
                  <button @click="handleVNC(container.id)" class="action-btn">VNC</button>
                  <button @click="handleRestart(container.id)" class="action-btn">重启</button>
                  <button class="action-more">⋮</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 代理详情弹窗 -->
    <div v-if="showDetailDialog" class="dialog-overlay" @click="closeDialog">
      <div class="dialog-content" @click.stop>
        <div class="dialog-header">
          <h2>代理详情</h2>
          <button class="close-btn" @click="closeDialog">✕</button>
        </div>

        <div class="dialog-tabs">
          <button class="tab-btn active">暂无数据</button>
        </div>

        <div class="dialog-body">
          <div class="account-section">
            <h3 class="section-title">绑定账号</h3>
            
            <div class="search-bar">
              <input 
                v-model="searchKeyword" 
                type="text" 
                placeholder="请输入关键词" 
                class="search-input"
              />
              <button class="search-btn" @click="handleSearch">查询</button>
            </div>

            <div class="account-grid">
              <div v-for="account in accounts" :key="account.id" class="account-card">
                <div class="account-avatar">
                  <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ccircle cx='50' cy='50' r='50' fill='%23e0e0e0'/%3E%3Ccircle cx='50' cy='40' r='18' fill='%23999'/%3E%3Cpath d='M20,85 Q20,65 50,65 Q80,65 80,85 Z' fill='%23999'/%3E%3C/svg%3E" alt="avatar" />
                  <span class="account-badge">📧</span>
                </div>
                <div class="account-info">
                  <div class="account-name">{{ account.username }}</div>
                  <div class="account-stats">
                    账号异常次数 <span class="count-red">{{ account.loginCount }}</span> 次
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="dialog-footer">
            <button class="footer-btn" @click="closeDialog">取消</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';

// 类型定义
interface Container {
  id: number;
  name: string;
  mirrorVersion: string;
  address: string;
  browserType: string;
  os: string;
  browserVersion: string;
  account: number;
}

// 响应式数据
const searchText = ref('');
const selectedContainers = ref<number[]>([]);
const totalContainers = ref(16);
const onlineContainers = ref(16);
const offlineContainers = ref(0);
const usagePercentage = ref(43);

// 模拟数据
const containers = ref<Container[]>([
  { id: 1, name: '生产-115虚拟机', mirrorVersion: '1.2', address: '10.51.20.115', browserType: '自研浏览器', os: 'windows', browserVersion: '122', account: 54 },
  { id: 2, name: '生产-113虚拟机', mirrorVersion: '1.2', address: '10.51.20.113', browserType: '自研浏览器', os: 'windows', browserVersion: '122', account: 15 },
  { id: 3, name: '生产-109虚拟机', mirrorVersion: '1.2', address: '10.51.20.109', browserType: '自研浏览器', os: 'windows', browserVersion: '122', account: 20 },
  { id: 4, name: '生产-110虚拟机', mirrorVersion: '1.2', address: '10.51.20.110', browserType: '自研浏览器', os: 'windows', browserVersion: '122', account: 49 },
  { id: 5, name: '生产-111虚拟机', mirrorVersion: '1.2', address: '10.51.20.111', browserType: '自研浏览器', os: 'windows', browserVersion: '122', account: 18 },
  { id: 6, name: '生产-114虚拟机', mirrorVersion: '1.2', address: '10.51.20.114', browserType: '自研浏览器', os: 'windows', browserVersion: '122', account: 19 },
]);

// 计算属性：全选状态
const selectAll = computed({
  get: () => selectedContainers.value.length === containers.value.length,
  set: () => {}
});

// 方法
const handleSelectAll = () => {
  if (selectedContainers.value.length === containers.value.length) {
    selectedContainers.value = [];
  } else {
    selectedContainers.value = containers.value.map(c => c.id);
  }
};

// 弹窗控制
const showDetailDialog = ref(false);
const searchKeyword = ref('');

// 模拟账号数据
const accounts = ref([
  { id: 1, username: 'naaszvdaveM00l8', loginCount: 0 },
  { id: 2, username: 'pacasfowjJ52q3', loginCount: 0 },
  { id: 3, username: 'rehercbrinZ72v5', loginCount: 0 },
  { id: 4, username: 'furcousagum51w8', loginCount: 0 },
  { id: 5, username: 'pirasnrahmL63i6', loginCount: 0 },
  { id: 6, username: 'uvinagbazey21A0', loginCount: 0 },
  { id: 7, username: 'benetygeliD19Y4', loginCount: 0 },
  { id: 8, username: 'bergegratkf84G4', loginCount: 0 },
  { id: 9, username: 'rehercbrina43hqfg@hotma...', loginCount: 0 },
  { id: 10, username: 'furcousagummfk7@hotma...', loginCount: 0 },
]);

const handleDetail = (id: number) => {
  showDetailDialog.value = true;
};

const closeDialog = () => {
  showDetailDialog.value = false;
};

const handleSearch = () => {
  console.log('搜索:', searchKeyword.value);
};

const handleVNC = (id: number) => {
  console.log('VNC连接:', id);
};

const handleRestart = (id: number) => {
  console.log('重启容器:', id);
};
</script>

<style scoped>
.container-management {
  min-height: 100vh;
  background-color: #f5f5f5;
  padding: 24px;
}

/* 面包屑 */
.breadcrumb {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #666;
  margin-bottom: 24px;
}

.breadcrumb .separator {
  color: #999;
}

.breadcrumb .active {
  color: #333;
}

/* 统计卡片区域 */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  margin-bottom: 32px;
}

.card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 24px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
}

.card-header h3 {
  font-size: 16px;
  font-weight: 500;
  color: #333;
  margin: 0;
}

.total-info {
  text-align: right;
}

.total-info .label {
  font-size: 12px;
  color: #999;
  margin-bottom: 4px;
}

.total-info .value {
  font-size: 24px;
  font-weight: 600;
  color: #333;
}

.card-title {
  font-size: 16px;
  font-weight: 500;
  color: #333;
  margin: 0 0 32px 0;
}

/* 饼图 */
.chart-container {
  display: flex;
  justify-content: center;
  margin-bottom: 16px;
}

.pie-chart {
  position: relative;
  width: 192px;
  height: 192px;
}

.pie-chart svg {
  width: 100%;
  height: 100%;
}

.pie-center {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}

.center-label {
  font-size: 12px;
  color: #999;
}

.legend {
  display: flex;
  justify-content: center;
  gap: 24px;
  margin-top: 16px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #666;
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 2px;
}

/* 仪表盘 */
.gauge-container {
  display: flex;
  justify-content: center;
  margin-bottom: 8px;
}

.gauge-chart {
  position: relative;
  width: 224px;
  height: 128px;
}

.gauge-chart svg {
  width: 100%;
  height: 100%;
}

.gauge-value {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 36px;
  font-weight: 700;
  color: #333;
  margin-top: 16px;
}

.gauge-labels {
  display: flex;
  justify-content: space-between;
  padding: 0 16px;
  font-size: 12px;
  color: #ccc;
}

/* 运行状态 */
.status-card {
  background: linear-gradient(135deg, #4B7BEC 0%, #3867D6 100%);
  border-radius: 8px;
  padding: 24px;
  text-align: center;
  color: white;
  margin-bottom: 16px;
}

.total-count {
  font-size: 48px;
  font-weight: 700;
  line-height: 1;
}

.total-label {
  font-size: 14px;
  margin-top: 8px;
  opacity: 0.9;
}

.status-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.status-item {
  text-align: center;
}

.status-value {
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 4px;
}

.status-value.online {
  color: #2ecc71;
}

.status-value.offline {
  color: #f39c12;
}

.status-label {
  font-size: 14px;
  color: #999;
}

/* 表格卡片 */
.table-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.table-header {
  padding: 24px;
  border-bottom: 1px solid #e8e8e8;
}

.table-header h3 {
  font-size: 18px;
  font-weight: 500;
  color: #333;
  margin: 0;
}

/* 筛选栏 */
.filter-bar {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 24px;
  border-bottom: 1px solid #e8e8e8;
}

.filter-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-label {
  font-size: 14px;
  color: #666;
}

.filter-select {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  background: white;
  font-size: 14px;
  color: #666;
  cursor: pointer;
  transition: border-color 0.3s;
}

.filter-select:hover {
  border-color: #999;
}

.filter-select .arrow {
  font-size: 10px;
  color: #999;
}

.clear-filter {
  padding: 6px 16px;
  border: none;
  background: none;
  color: #4B7BEC;
  font-size: 14px;
  cursor: pointer;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.clear-filter:hover {
  background-color: #e6f0ff;
}

.spacer {
  flex: 1;
}

.search-box {
  position: relative;
  width: 256px;
}

.search-box input {
  width: 100%;
  padding: 6px 32px 6px 12px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.3s;
}

.search-box input:focus {
  border-color: #4B7BEC;
}

.search-icon {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #999;
  font-size: 14px;
}

/* 表格 */
.table-container {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  background-color: #fafafa;
}

th {
  padding: 16px 24px;
  text-align: left;
  font-size: 14px;
  font-weight: 500;
  color: #333;
}

tbody tr {
  border-bottom: 1px solid #f0f0f0;
  transition: background-color 0.3s;
}

tbody tr:hover {
  background-color: #fafafa;
}

td {
  padding: 16px 24px;
  font-size: 14px;
  color: #666;
}

td:nth-child(3) {
  color: #333;
  font-weight: 500;
}

/* 操作按钮 */
.action-buttons {
  display: flex;
  align-items: center;
  gap: 12px;
}

.action-btn {
  border: none;
  background: none;
  color: #4B7BEC;
  font-size: 14px;
  cursor: pointer;
  padding: 0;
  transition: color 0.3s;
}

.action-btn:hover {
  color: #3867D6;
}

.action-more {
  border: none;
  background: none;
  color: #999;
  font-size: 18px;
  cursor: pointer;
  padding: 0;
  transition: color 0.3s;
}

.action-more:hover {
  color: #666;
}

/* 复选框样式 */
input[type="checkbox"] {
  width: 16px;
  height: 16px;
  cursor: pointer;
}

/* 弹窗样式 */
.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.dialog-content {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 1200px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #e8e8e8;
}

.dialog-header h2 {
  font-size: 18px;
  font-weight: 500;
  color: #333;
  margin: 0;
}

.close-btn {
  width: 32px;
  height: 32px;
  border: none;
  background: none;
  font-size: 20px;
  color: #999;
  cursor: pointer;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.close-btn:hover {
  background-color: #f5f5f5;
  color: #666;
}

.dialog-tabs {
  padding: 16px 24px 0;
  border-bottom: 1px solid #e8e8e8;
}

.tab-btn {
  padding: 8px 16px;
  border: none;
  background: none;
  color: #666;
  font-size: 14px;
  cursor: pointer;
  position: relative;
  margin-bottom: -1px;
}

.tab-btn.active {
  color: #4B7BEC;
}

.tab-btn.active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 2px;
  background-color: #4B7BEC;
}

.dialog-body {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
}

.account-section {
  margin-bottom: 24px;
}

.section-title {
  font-size: 16px;
  font-weight: 500;
  color: #333;
  margin: 0 0 16px 0;
}

.search-bar {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
}

.search-input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.3s;
}

.search-input:focus {
  border-color: #4B7BEC;
}

.search-btn {
  padding: 8px 24px;
  background-color: #4B7BEC;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.search-btn:hover {
  background-color: #3867D6;
}

.account-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.account-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  border: 1px solid #e8e8e8;
  border-radius: 8px;
  transition: box-shadow 0.3s;
}

.account-card:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.account-avatar {
  position: relative;
  width: 48px;
  height: 48px;
  flex-shrink: 0;
}

.account-avatar img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
}

.account-badge {
  position: absolute;
  bottom: -2px;
  right: -2px;
  width: 20px;
  height: 20px;
  background-color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.account-info {
  flex: 1;
}

.account-name {
  font-size: 15px;
  font-weight: 500;
  color: #333;
  margin-bottom: 4px;
}

.account-stats {
  font-size: 13px;
  color: #666;
}

.count-red {
  color: #e74c3c;
  font-weight: 600;
}

.dialog-footer {
  display: flex;
  justify-content: center;
  padding-top: 24px;
  border-top: 1px solid #e8e8e8;
  margin-top: 24px;
}

.footer-btn {
  padding: 8px 32px;
  border: 1px solid #d9d9d9;
  background: white;
  border-radius: 4px;
  font-size: 14px;
  color: #666;
  cursor: pointer;
  transition: all 0.3s;
}

.footer-btn:hover {
  border-color: #4B7BEC;
  color: #4B7BEC;
}
</style>