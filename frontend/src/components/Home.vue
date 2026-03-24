
<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import axios from 'axios'

// 类型定义
interface QuickEntry {
  title: string
  icon: string
}

interface StrategyItem {
  name: string
  platformId: string
  platformName: string
  platformIcon: string
  platformColor: string
  logo: string
}

interface TaskStats {
  total: number
  inProgress: number
  completed: number
}

// 平台配置
const PLATFORMS = [
  { id: 'x', name: 'X (Twitter)', icon: '𝕏', color: '#000000', logo: '/icons/twitter.png' },
  { id: 'youtube', name: 'YouTube', icon: '▶️', color: '#ff0000', logo: '/icons/youtube.png' },
  { id: 'tiktok', name: 'TikTok', icon: '🎵', color: '#00f2ea', logo: '/icons/tiktok.png' },
  { id: 'instagram', name: 'Instagram', icon: '📷', color: '#E1306C', logo: '/icons/insgram.png' },
  { id: 'facebook', name: 'Facebook', icon: '📘', color: '#1877f2', logo: '/icons/facebook.png' },
  { id: 'threads', name: 'Threads', icon: '🌀', color: '#000000', logo: '/icons/threads.png' },
  { id: 'tinder', name: 'Tinder', icon: '🔥', color: '#fe3c72', logo: '/icons/tinder.png' },
]

// 状态
const platformAccount = ref<string>('')
const recommendedStrategies = ref<StrategyItem[]>([])
const loadingStrategies = ref<boolean>(false)
const currentDateText = ref<string>('')

// 任务统计
const taskStats: TaskStats = {
  total: 1604,
  inProgress: 0,
  completed: 1604
}

// 快捷入口
const quickEntries: QuickEntry[] = [
  { title: '导入账号', icon: '/image/导入账号.jpg' },
  { title: '运维中心', icon: '/image/日常培育.jpg' },
  { title: '日常培育', icon: '/image/新建任务.jpg'},
  { title: '新增策略', icon: '/image/新增策略.jpg' },
  { title: '新建任务', icon: '/image/运维中心.jpg'}
]

// 随机打乱数组
const shuffleArray = <T>(array: T[]): T[] => {
  const shuffled = [...array]
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    const temp = shuffled[i]
    shuffled[i] = shuffled[j] as T
    shuffled[j] = temp as T
  }
  return shuffled
}

// 获取策略中心的已保存策略
const fetchStrategies = async () => {
  loadingStrategies.value = true
  try {
    const allStrategies: StrategyItem[] = []
    
    // 遍历所有平台获取策略列表
    for (const platform of PLATFORMS) {
      try {
        const res = await axios.get(`http://${window.location.hostname}:8000/list/${platform.id}`)
        if (res.data && res.data.strategies && res.data.strategies.length > 0) {
          res.data.strategies.forEach((strategyName: string) => {
            allStrategies.push({
              name: strategyName,
              platformId: platform.id,
              platformName: platform.name,
              platformIcon: platform.icon,
              platformColor: platform.color,
              logo: platform.logo
            })
          })
        }
      } catch (e) {
        // 某个平台获取失败，继续获取其他平台
        console.log(`获取 ${platform.name} 策略失败`)
      }
    }
    
    // 随机打乱并取最多4个策略
    const shuffled = shuffleArray(allStrategies)
    recommendedStrategies.value = shuffled.slice(0, 4)
    
  } catch (e) {
    console.error('获取策略失败:', e)
  } finally {
    loadingStrategies.value = false
  }
}

const updateCurrentDate = (): void => {
  const now = new Date()
  const year = now.getFullYear()
  const month = now.getMonth() + 1
  const day = now.getDate()
  const weekdays = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六']
  currentDateText.value = `${year}年${month}月${day}日 ${weekdays[now.getDay()]}`
}

let dateTimer: number | undefined

// 组件挂载时获取策略
onMounted(() => {
  fetchStrategies()
  updateCurrentDate()
  dateTimer = window.setInterval(updateCurrentDate, 60 * 1000)
})

onBeforeUnmount(() => {
  if (dateTimer !== undefined) {
    window.clearInterval(dateTimer)
  }
})

// 方法
const handleQuickEntry = (title: string): void => {
  console.log(`点击快捷入口: ${title}`)
}


const handleView = (strategy: StrategyItem): void => {
  console.log(`查看策略: ${strategy.name}`)
  // 跳转到策略中心编辑该策略
  window.location.href = `/strategy?platform=${strategy.platformId}&strategy=${strategy.name}`
}

const handleDelete = (strategy: StrategyItem): void => {
  console.log(`删除策略: ${strategy.name}`)
  // 这里添加删除逻辑，比如弹出确认对话框
}

// 刷新推荐策略
const refreshStrategies = (): void => {
  fetchStrategies()
}

</script>

<template>

  <div class="page-container">
    <!-- Header
    <div>
      <Navigation />
    </div> -->
   

    <!-- Main Content -->
    <main class="main-content">
      <!-- Welcome Section -->
      <div class="welcome-section">
        <h2 class="welcome-title">
          欢迎使用 <span class="welcome-subtitle">账号培育与管理系统</span>
        </h2>
        <div class="stats-container">
          <span class="date-text">{{ currentDateText }}</span>
          <div class="stat-item">
            <span class="stat-label">任务总数</span>
            <span class="stat-value stat-blue">{{ taskStats.total }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">进行中任务数</span>
            <span class="stat-value stat-orange">{{ taskStats.inProgress }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">已完成任务数</span>
            <span class="stat-value stat-green">{{ taskStats.completed }}</span>
          </div>
        </div>
      </div>

      <!-- Platform Account Input -->
      <div class="input-section">
        <input
          v-model="platformAccount"
          type="text"
          placeholder="平台账号"
          class="account-input"
        />
      </div>

      <!-- Quick Entry Cards -->
      <section class="section">
        <h3 class="section-title">快捷入口</h3>
        <div class="quick-grid">
          <div
            v-for="(entry, index) in quickEntries"
            :key="index"
            @click="handleQuickEntry(entry.title)"
            class="quick-card"

          >
            <div class="card-bg"></div>
            <div class="card-content">
              <div class="card-header">
                <h4 class="card-title">{{ entry.title }}</h4>
                <svg class="arrow-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </div>
              <div class="icon-container">
                <img class="entry-icon" :src="entry.icon" :alt="entry.title" />

              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Strategy Recommendations -->
      <section class="section">
        <div class="section-header">
          <h3 class="section-title">策略推荐</h3>
          <button @click="refreshStrategies" class="refresh-btn" :disabled="loadingStrategies">
            <svg class="refresh-icon" :class="{ spinning: loadingStrategies }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            换一批
          </button>
        </div>
        
        <!-- 加载中状态 -->
        <div v-if="loadingStrategies" class="loading-container">
          <div class="loading-spinner"></div>
          <span>加载策略中...</span>
        </div>
        
        <!-- 无策略时的空状态 -->
        <div v-else-if="recommendedStrategies.length === 0" class="empty-state">
          <div class="empty-icon">📋</div>
          <p>暂无已保存的策略</p>
          <p class="empty-hint">前往策略中心创建新策略</p>
        </div>
        
        <!-- 策略列表 -->
        <div v-else class="platform-grid">
          <div
            v-for="(strategy, index) in recommendedStrategies"
            :key="index"
            class="platform-card"
          >
            <div class="platform-header">
              <div class="platform-info">
                <div class="platform-logo-wrapper">
                  <img 
                    class="platform-logo" 
                    :src="strategy.logo" 
                    :alt="strategy.platformName"
                    @error="(e: Event) => (e.target as HTMLImageElement).style.display = 'none'"
                  />
                  <span class="platform-logo-fallback" :style="{ background: strategy.platformColor }">
                    {{ strategy.platformIcon }}
                  </span>
                </div>
                <div>
                  <h4 class="platform-name">{{ strategy.name }}</h4>
                  <p class="platform-desc">{{ strategy.platformName }}</p>
                </div>
              </div>
              <span class="platform-badge" :style="{ background: strategy.platformColor }">
                {{ strategy.platformIcon }}
              </span>
            </div>
            
            <div class="platform-details">
              <div class="detail-row">
                <span class="detail-label">所属平台</span>
                <span class="detail-value-blue">{{ strategy.platformName }}</span>
              </div>
              
              <div class="detail-row">
                <span class="detail-label">策略类型</span>
                <span class="detail-value-blue">RPA 自动化</span>
              </div>
              
              <div class="detail-row">
                <span class="detail-label">适用容器</span>
                <span class="detail-value-blue">浏览器</span>
              </div>
            </div>

            <!-- 操作按钮 -->
            <div class="action-buttons">
              <button 
                @click.stop="handleView(strategy)" 
                class="btn-view"
              >
                <svg class="btn-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
                查看
              </button>
              <button 
                @click.stop="handleDelete(strategy)" 
                class="btn-delete"
              >
                <svg class="btn-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
                删除
              </button>
            </div>

          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.page-container {
  background: url('/image/background.jpg') no-repeat center center;
background-size: cover;

}


/* Main Content */
.main-content {
  max-width: 1280px;
  margin: 0 auto;
  padding: 2rem 1.5rem;
}

/* Welcome Section */
.welcome-section {
  margin-bottom: 2rem;
}

.welcome-title {
  font-size: 1.875rem;
  font-weight: bold;
  color: rgba(255, 255, 255, 0.95);
  margin-bottom: 1rem;
}

.welcome-subtitle {
  color: rgba(255, 255, 255, 0.85);
}

.stats-container {
  display: flex;
  align-items: center;
  gap: 2rem;
  font-size: 0.875rem;
}

.date-text {
  color: rgba(255, 255, 255, 0.85);
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.stat-label {
  color: rgba(255, 255, 255, 0.85);
}

.stat-value {
  font-weight: 600;
}

.stat-blue { color: #2563eb; }
.stat-orange { color: #ea580c; }
.stat-green { color: #16a34a; }

/* Input Section */
.input-section {
  margin-bottom: 2rem;
}

.account-input {
  padding: 0.5rem 1rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  width: 16rem;
  font-size: 0.875rem;
  outline: none;
}

.account-input:focus {
  border-color: #60a5fa;
  box-shadow: 0 0 0 3px rgba(96, 165, 250, 0.1);
}

/* Section */
.section {
  margin-bottom: 3rem;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.section-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #6b7a91;
}

.refresh-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: #f3f4f6;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  color: #4b5563;
  cursor: pointer;
  transition: all 0.2s;
}

.refresh-btn:hover:not(:disabled) {
  background: #e5e7eb;
}

.refresh-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.refresh-icon {
  width: 16px;
  height: 16px;
}

.refresh-icon.spinning {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* 加载状态 */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  color: #6b7280;
  gap: 1rem;
}

.loading-spinner {
  width: 32px;
  height: 32px;
  border: 3px solid #e5e7eb;
  border-top-color: #2563eb;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

/* 空状态 */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  background: white;
  border-radius: 0.75rem;
  color: #6b7280;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.empty-hint {
  font-size: 0.875rem;
  color: #9ca3af;
  margin-top: 0.5rem;
}

/* 平台徽章 */
.platform-badge {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 0.375rem;
  font-size: 14px;
  color: white;
}

/* Quick Entry Grid */
.quick-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 1.5rem;
}

.quick-card {
  background: white;
  border-radius: 0.75rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: box-shadow 0.2s;
}

.quick-card:hover {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}


.card-content {
  position: relative;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.card-title {
  color: #1f2937;
  font-weight: 500;
  font-size: 0.875rem;
}

.arrow-icon {
  width: 20px;
  height: 20px;
  color: #9ca3af;
  transition: all 0.2s;
}

.quick-card:hover .arrow-icon {
  color: #4b5563;
  transform: translateX(4px);
}

.icon-container {
  display: flex;
  justify-content: center;
}

.entry-icon {
  object-fit: contain;
  opacity: 1; /* 取消透明 */
  border-radius: 0.5rem; /* 可选：圆角 */
}


/* Platform Grid */
.platform-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
}

.platform-card {
  background: white;
  border-radius: 0.75rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: box-shadow 0.2s;
}

.platform-card:hover {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.platform-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.platform-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.platform-logo-wrapper {
  position: relative;
  width: 32px;
  height: 32px;
}

.platform-logo {
  width: 32px;
  height: 32px;
  object-fit: contain;
  border-radius: 0.25rem;
  position: relative;
  z-index: 1;
}

.platform-logo-fallback {
  position: absolute;
  top: 0;
  left: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 0.25rem;
  font-size: 16px;
  color: white;
}

.platform-name {
  font-weight: 600;
  color: #1f2937;
  font-size: 0.875rem;
}

.platform-desc {
  font-size: 0.75rem;
  color: #6b7280;
}

.platform-details {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  font-size: 0.875rem;
}

.detail-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.detail-label {
  color: #6b7280;
}

.detail-value-blue {
  color: #2563eb;
  font-weight: 600;
}

.detail-value-gray {
  color: #9ca3af;
  font-weight: 600;
}

.detail-time {
  padding-top: 0.5rem;
  border-top: 1px solid #f3f4f6;
}

.time-label {
  font-size: 0.75rem;
  color: #6b7280;
}

.time-value {
  font-size: 0.75rem;
  color: #374151;
  margin-top: 0.25rem;
}

/* 操作按钮 */
.action-buttons {
  display: flex;
  gap: 0.75rem;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #f3f4f6;
}

.btn-view,
.btn-delete {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-view {
  background: #eff6ff;
  color: #1e40af;
}

.btn-view:hover {
  background: #dbeafe;
}

.btn-delete {
  background: #fef2f2;
  color: #dc2626;
}

.btn-delete:hover {
  background: #fee2e2;
}

.btn-icon {
  width: 18px;
  height: 18px;
}

/* 响应式 */
@media (max-width: 1024px) {
  .quick-grid {
    grid-template-columns: repeat(3, 1fr);
  }
  
  .platform-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .quick-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .platform-grid {
    grid-template-columns: 1fr;
  }
}
</style>
