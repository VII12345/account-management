<!--
  文件注释：frontend/src/components/OpsCenter/Layout.vue

  职责：作为运维中心的布局容器，负责模块导航、路由切换与内容区挂载。
  边界：只负责视图层结构组织，不实现运维资源的业务处理规则。
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
  <div class="ops-layout">
    <!-- 左侧菜单 -->
    <aside class="sidebar">
      <div class="menu-title">运维中心</div>
      <div class="menu-item" :class="{ active: active.includes('/proxy') }" @click="go('/ops/proxy')">
        代理管理
      </div>
      <div class="menu-item" :class="{ active: active.includes('/container') }" @click="go('/ops/container')">
        容器管理
      </div>
      <div class="menu-item" :class="{ active: active.includes('/email') }" @click="go('/ops/email')">
        邮箱管理
      </div>
    </aside>

    <!-- 右侧内容 -->
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<style scoped>
.ops-layout {
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
