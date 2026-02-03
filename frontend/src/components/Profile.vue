<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getUserInfo, logout, type UserInfo } from '../utils/auth'

const router = useRouter()
const user = ref<UserInfo | null>(null)

onMounted(() => {
  user.value = getUserInfo()
})

// 登出
const handleLogout = () => {
  logout()
  router.push('/login')
}
</script>

<template>
  <div class="profile-container">
    <div class="profile-card">
      <!-- 头像区域 -->
      <div class="avatar-section">
        <div class="avatar">
          <svg viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
          </svg>
        </div>
        <h2 class="username">{{ user?.email?.split('@')[0] || '用户' }}</h2>
        <p class="user-email">{{ user?.email || '未登录' }}</p>
      </div>

      <!-- 用户信息 -->
      <div class="info-section">
        <h3 class="section-title">账号信息</h3>
        <div class="info-item">
          <span class="info-label">用户ID</span>
          <span class="info-value">{{ user?.id || '-' }}</span>
        </div>
        <div class="info-item">
          <span class="info-label">邮箱</span>
          <span class="info-value">{{ user?.email || '-' }}</span>
        </div>
        <div class="info-item">
          <span class="info-label">账号状态</span>
          <span class="info-value status-active">正常</span>
        </div>
      </div>

      <!-- 操作按钮 -->
      <div class="action-section">
        <button class="btn btn-outline" @click="router.push('/')">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
            <polyline points="9 22 9 12 15 12 15 22"/>
          </svg>
          返回首页
        </button>
        <button class="btn btn-danger" @click="handleLogout">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
            <polyline points="16 17 21 12 16 7"/>
            <line x1="21" y1="12" x2="9" y2="12"/>
          </svg>
          退出登录
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.profile-container {
  min-height: calc(100vh - 80px);
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
  padding: 40px 20px;
  display: flex;
  justify-content: center;
  align-items: flex-start;
}

.profile-card {
  width: 100%;
  max-width: 480px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

/* 头像区域 */
.avatar-section {
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  padding: 40px 20px;
  text-align: center;
}

.avatar {
  width: 100px;
  height: 100px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  margin: 0 auto 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 4px solid rgba(255, 255, 255, 0.3);
}

.avatar svg {
  width: 60px;
  height: 60px;
  color: white;
}

.username {
  font-size: 24px;
  font-weight: 600;
  color: white;
  margin: 0 0 4px;
}

.user-email {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.8);
  margin: 0;
}

/* 信息区域 */
.info-section {
  padding: 24px;
  border-bottom: 1px solid #f0f0f0;
}

.section-title {
  font-size: 14px;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin: 0 0 16px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #f5f5f5;
}

.info-item:last-child {
  border-bottom: none;
}

.info-label {
  font-size: 14px;
  color: #6b7280;
}

.info-value {
  font-size: 14px;
  color: #1f2937;
  font-weight: 500;
  max-width: 60%;
  word-break: break-all;
  text-align: right;
}

.status-active {
  color: #10b981;
  background: #d1fae5;
  padding: 2px 10px;
  border-radius: 12px;
  font-size: 12px;
}

/* 操作按钮 */
.action-section {
  padding: 24px;
  display: flex;
  gap: 12px;
}

.btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 12px 16px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.btn svg {
  width: 18px;
  height: 18px;
}

.btn-outline {
  background: #f3f4f6;
  color: #4b5563;
}

.btn-outline:hover {
  background: #e5e7eb;
}

.btn-danger {
  background: #fee2e2;
  color: #dc2626;
}

.btn-danger:hover {
  background: #fecaca;
}
</style>
