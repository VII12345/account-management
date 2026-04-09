<!--
  文件注释：frontend/src/components/CultivationCenter/Layout.vue

  职责：提供培养中心模块的统一布局、导航高亮与子路由切换骨架。
  边界：仅处理导航与布局编排，不承载具体业务数据读写逻辑。
-->
<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router'
import { computed } from 'vue'

const router = useRouter()
const route = useRoute()

const active = computed(() => route.path)

const go = (path: string) => {
  router.push(path)
}
</script>

<template>
  <div class="cultivation-layout">
    <!-- 左侧菜单 -->
    <aside class="sidebar">
      <div class="menu-title">培育中心</div>
      <div class="menu-item" :class="{ active: active.includes('/daily-training') }"
        @click="go('/cultivation/daily-training')">
        日常培育
      </div>
      <div class="menu-item" :class="{ active: active.includes('/virtual-human') }"
        @click="go('/cultivation/virtual-human')">
        虚拟人管理
      </div>
    </aside>

    <!-- 右侧内容 -->
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<style scoped>
.cultivation-layout {
  display: flex;
  min-height: 100vh;
  background: #f3f4f6;
}

/* 左侧菜单 */
.sidebar {
  width: 180px;
  background: #f0f2f5;
  border-right: 1px solid #e5e7eb;
  padding: 1rem 0;
}

.menu-title {
  font-size: 1rem;
  font-weight: 600;
  color: #374151;
  padding: 0.75rem 1.5rem;
  border-bottom: 1px solid #e5e7eb;
  margin-bottom: 0.5rem;
}

.menu-item {
  padding: 0.625rem 2rem;
  color: #6b7280;
  cursor: pointer;
  font-size: 0.875rem;
}

.menu-item.active {
  background: #dbeafe;
  color: #2563eb;
  font-weight: 500;
}

/* 右侧内容 */
.main-content {
  flex: 1;
  padding: 1.5rem 2rem;
  background: #f9fafb;
}
</style>
