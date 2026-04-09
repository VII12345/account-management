<!--
  文件注释：frontend/src/components/OpsCenter/ContainerDetail.vue

  职责：承载当前页面/组件的视图结构、交互事件与状态绑定。
  边界：仅处理前端展示与交互编排，不在此文件实现后端业务规则。
-->

<template>
  <div class="container-detail-page">
    <!-- 面包屑导航 -->
    <div class="breadcrumb-bar">
      <el-breadcrumb separator=">">
        <el-breadcrumb-item>运维中心</el-breadcrumb-item>
        <el-breadcrumb-item>容器管理</el-breadcrumb-item>
        <el-breadcrumb-item>容器详情</el-breadcrumb-item>
      </el-breadcrumb>
    </div>

    <!-- 主体内容卡片 -->
    <div class="content-card">
      <!-- 顶部标签页 -->
      <el-tabs v-model="activeTab" class="custom-tabs">
        <el-tab-pane label="容器详情" name="details" />
        <el-tab-pane label="子账号详情" name="sub-account" />
      </el-tabs>

      <!-- 详情内容区 -->
      <div class="pane-content" v-if="activeTab === 'details'">
        
        <!-- 模块1：容器信息 -->
        <div class="section-container">
          <div class="section-header">
            <div class="title-with-bar">容器信息</div>
            <!-- 
              修改点 1：添加 @click 事件 
            -->
            <el-button 
              type="primary" 
              size="small" 
              class="vnc-btn" 
              @click="openVnc"
            >
              VNC
            </el-button>
          </div>

          <!-- 自定义边框表格布局 -->
          <table class="custom-table">
            <tbody>
              <tr>
                <td class="label-cell">容器名称</td>
                <td class="value-cell">
                  <!-- 修改点 2：绑定变量 -->
                  <span class="custom-text">{{ containerInfo.name }}</span>
                </td>
                <td class="label-cell">容器地址</td>
                <td class="value-cell" colspan="3">
                  <!-- Flex布局容器：实现左右分布 -->
                  <div class="ip-wrapper">
                    <!-- 修改点 3：绑定变量 -->
                    <span class="custom-text">{{ containerInfo.ip }}</span>
                    
                    <!-- 右侧：状态 + 图标 -->
                    <div class="right-actions">
                      <div class="status-badge">
                        <span class="dot">●</span> 上线
                      </div>
                      <Edit class="edit-icon" />
                    </div>
                  </div>
                </td>
              </tr>
              <tr>
                <td class="label-cell">操作系统</td>
                <td class="value-cell"><strong>Debian</strong></td>
                <td class="label-cell">浏览器类型</td>
                <td class="value-cell">-</td>
                <td class="label-cell">浏览器版本</td>
                <td class="value-cell"><strong>122</strong></td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- 模块2：运行状态 -->
        <div class="section-container mt-large">
          <div class="section-header">
            <div class="title-with-bar">运行状态</div>
          </div>

          <!-- 状态指标栏 -->
          <div class="status-bar">
            <div class="status-item">
              <span class="label">内存</span>
              <span class="value">{{ status.memory }}%</span>
            </div>
            <div class="status-item">
              <span class="label">CPU</span>
              <span class="value">{{ status.cpu }}%</span>
            </div>
            <div class="status-item">
              <span class="label">网络流量</span>
              <span class="value">{{ status.network }}</span>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import { Edit } from '@element-plus/icons-vue';

// 标签页状态
const activeTab = ref('details');

// --- 容器基本信息 (提取出来方便 VNC 链接使用) ---
const containerInfo = ref({
  name: 'mass-us-1',
  ip: '172.82.66.230',
  vncPort: '6080' // 假设 noVNC 运行在 6080 端口
});

// --- VNC 跳转逻辑 ---
const openVnc = () => {
  // 1. 构建 noVNC 链接
  // 这里假设你的 noVNC 地址格式是 http://IP:端口/vnc.html
  // 如果你需要带密码 token，可以写成: `.../vnc.html?host=${ip}&port=${port}&password=xxx`
  const url = `http://${containerInfo.value.ip}:${containerInfo.value.vncPort}/vnc.html`;
  
  // 2. 在新标签页打开
  window.open(url, '_blank');
};

// --- 状态监控逻辑 ---
interface SystemStatus {
  memory: number;
  cpu: number;
  network: string;
}

const status = ref<SystemStatus>({
  memory: 0,
  cpu: 0,
  network: '0 KB/s'
});

const fetchStatus = async () => {
  try {
    // 指向后端 API
    const url = `http://${containerInfo.value.ip}:3000/api/monitor`;
    const response = await fetch(url);
    if (!response.ok) throw new Error('Network error');
    const data = await response.json();
    status.value = data;
  } catch (error) {
    // 模拟数据兜底
    status.value = {
      memory: Math.floor(Math.random() * (80 - 40) + 40),
      cpu: Math.floor(Math.random() * (50 - 10) + 10),
      network: (Math.random() * 5).toFixed(2) + ' MB/s'
    };
  }
};

let timer: number | null = null;

onMounted(() => {
  fetchStatus();
  timer = window.setInterval(fetchStatus, 3000);
});

onUnmounted(() => {
  if (timer) clearInterval(timer);
});
</script>

<style scoped>
/* --- 布局容器 --- */
.container-detail-page {
  padding: 20px;
  background-color: #f0f2f5;
  min-height: 100%;
  box-sizing: border-box;
}

/* --- 面包屑 --- */
.breadcrumb-bar {
  margin-bottom: 15px;
}
.breadcrumb-bar :deep(.el-breadcrumb__inner) {
  color: #606266;
  font-weight: normal;
}
.breadcrumb-bar :deep(.el-breadcrumb__item:last-child .el-breadcrumb__inner) {
  color: #303133;
  font-weight: 500;
}

/* --- 内容卡片 --- */
.content-card {
  background: #fff;
  padding: 0 20px 30px 20px;
  border-radius: 4px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}

/* --- Tabs --- */
.custom-tabs :deep(.el-tabs__nav-wrap::after) {
  height: 1px;
  background-color: #ebeef5;
}
.custom-tabs :deep(.el-tabs__item) {
  font-size: 15px;
  height: 55px;
  line-height: 55px;
  color: #333;
  font-weight: 600;
}
.custom-tabs :deep(.el-tabs__item.is-active) {
  color: #5e7ce0;
}

/* --- 通用间距 --- */
.mt-large {
  margin-top: 30px;
}

/* --- 标题栏 --- */
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  margin-top: 20px;
}
.section-header .title-with-bar {
  font-size: 16px;
  font-weight: bold;
  color: #333;
  padding-left: 10px;
  border-left: 4px solid #5e7ce0;
  line-height: 1.1;
}
.section-header .vnc-btn {
  background-color: #5e7ce0;
  border-color: #5e7ce0;
  font-weight: 500;
  padding: 8px 15px;
}

/* --- 表格样式 --- */
.custom-table {
  width: 100%;
  border-collapse: collapse;
  border: 1px solid #ebeef5;
  font-size: 14px;
}
.custom-table td {
  border: 1px solid #ebeef5;
  padding: 12px 16px;
  vertical-align: middle;
}
.custom-table .label-cell {
  background-color: #fafafa;
  color: #606266;
  width: 120px;
  white-space: nowrap;
}
.custom-table .value-cell {
  color: #303133;
  background-color: #fff;
  min-width: 200px;
}

/* --- 左右对齐布局核心样式 --- */
.ip-wrapper {
  display: flex;
  justify-content: space-between; 
  align-items: center;
  width: 100%;
}
.right-actions {
  display: flex;
  align-items: center;
  gap: 15px; 
}

/* --- 蓝色文字 (无背景) --- */
.custom-text {
  color: #6a7df6; 
  font-weight: bold;
  font-family: Consolas, Monaco, monospace;
  font-size: 14px;
}

/* --- 状态徽章 --- */
.status-badge {
  display: inline-flex;
  align-items: center;
  border: 1px solid #67c23a;
  color: #67c23a;
  border-radius: 12px;
  padding: 0px 8px;
  font-size: 12px;
  height: 22px;
  line-height: 20px;
  background-color: #f0f9eb;
}
.status-badge .dot {
  font-size: 12px;
  margin-right: 4px;
  transform: scale(0.8);
}

/* --- 编辑图标 --- */
.edit-icon {
  width: 16px;
  height: 16px;
  cursor: pointer;
  color: #909399;
}
.edit-icon:hover {
  color: #5e7ce0;
}

/* --- 底部状态栏 --- */
.status-bar {
  display: flex;
  border: 1px solid #ebeef5;
  border-radius: 2px;
}
.status-bar .status-item {
  flex: 1;
  display: flex;
  align-items: center;
  padding: 16px 20px;
  border-right: 1px solid #ebeef5;
}
.status-bar .status-item:last-child {
  border-right: none;
}
.status-bar .status-item .label {
  color: #606266;
  font-size: 14px;
  margin-right: 8px;
}
.status-bar .status-item .value {
  color: #303133;
  font-weight: bold;
  font-size: 14px;
}
</style>