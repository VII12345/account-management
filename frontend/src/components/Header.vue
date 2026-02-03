<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getUserInfo, logout, type UserInfo } from '../utils/auth'

const router = useRouter()
const user = ref<UserInfo | null>(null)
const showDropdown = ref(false)

onMounted(() => {
  user.value = getUserInfo()
})

// 登出
const handleLogout = () => {
  logout()
  router.push('/login')
}

// 导航菜单
const navItems: string[] = ['主页', '账号中心', '培育中心', '任务中心', '策略中心', '运维中心', '机器人识别']

const getRoutePath = (name: string): string => {
  switch (name) {
    case '主页': return '/'
    case '账号中心': return '/account'
    case '培育中心': return '/cultivation'
    case '任务中心': return '/tasks'
    case '策略中心': return '/strategy'
    case '运维中心': return '/ops'
    case '机器人识别': return '/bot'
    default: return '/'
  }
}
</script>

<template>


    <div>
        <header class="header">
      <div class="header-content">
        <div class="header-left">
          <svg class="menu-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
          <h1 class="header-title">账号培育与管理系统</h1>
        </div>
        
        <nav class="nav">
          <router-link
            v-for="item in navItems"
            :key="item"
            :to="getRoutePath(item)"
            class="nav-item"
            active-class="nav-item-active"
          >
            {{ item }}
          </router-link>
        </nav>

        <!-- 用户头像下拉菜单 -->
        <div class="user-menu" @mouseenter="showDropdown = true" @mouseleave="showDropdown = false">
          <div class="user-avatar">
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
            </svg>
          </div>
          <transition name="dropdown">
            <div v-show="showDropdown" class="dropdown-menu">
              <div class="dropdown-header">
                <span class="user-name">{{ user?.email?.split('@')[0] || '用户' }}</span>
                <span class="user-email">{{ user?.email || '' }}</span>
              </div>
              <div class="dropdown-divider"></div>
              <router-link to="/profile" class="dropdown-item">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                  <circle cx="12" cy="7" r="4"/>
                </svg>
                个人中心
              </router-link>
              <button class="dropdown-item logout" @click="handleLogout">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
                  <polyline points="16 17 21 12 16 7"/>
                  <line x1="21" y1="12" x2="9" y2="12"/>
                </svg>
                退出登录
              </button>
            </div>
          </transition>
        </div>
      </div>
    </header>
    </div>
</template>


<style scoped>

/* Header */
.header {
  background: white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.header-content {
  max-width: 1280px;
  margin: 0 auto;
  padding: 1rem 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.menu-icon {
  width: 24px;
  height: 24px;
  color: #4b5563;
}

.header-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
}

.nav {
  display: flex;
  gap: 2rem;
}

.nav-item {
  font-size: 0.875rem;
  color: #4b5563;
  background: none;
  border: none;
  transition: color 0.2s;
  padding: 0.5rem 0;
}

.nav-item:hover {
  color: #111827;
}

.nav-item-active {
  color: #2563eb;
  font-weight: 500;
}

/* 用户菜单 */
.user-menu {
  position: relative;
  margin-left: 1.5rem;
}

.user-avatar {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.user-avatar:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
}

.user-avatar svg {
  width: 20px;
  height: 20px;
  color: white;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 8px;
  width: 220px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
  overflow: hidden;
  z-index: 100;
}

.dropdown-header {
  padding: 16px;
  background: #f9fafb;
}

.user-name {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: #1f2937;
}

.user-email {
  display: block;
  font-size: 12px;
  color: #6b7280;
  margin-top: 2px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.dropdown-divider {
  height: 1px;
  background: #e5e7eb;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  padding: 12px 16px;
  font-size: 14px;
  color: #4b5563;
  background: none;
  border: none;
  cursor: pointer;
  transition: background 0.2s;
  text-decoration: none;
}

.dropdown-item:hover {
  background: #f3f4f6;
}

.dropdown-item svg {
  width: 18px;
  height: 18px;
}

.dropdown-item.logout {
  color: #dc2626;
}

.dropdown-item.logout:hover {
  background: #fef2f2;
}

/* 下拉动画 */
.dropdown-enter-active,
.dropdown-leave-active {
  transition: opacity 0.2s, transform 0.2s;
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>