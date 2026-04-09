<!--
  文件注释：frontend/src/App.vue

  职责：承载当前页面/组件的视图结构、交互事件与状态绑定。
  边界：仅处理前端展示与交互编排，不在此文件实现后端业务规则。
-->

<script setup lang="ts">
import Header from './components/Header.vue'
</script>

<template>
  <div class="page-container">
    <!-- 顶部导航栏 (固定不动) -->
    <Header />

    <!-- 页面内容区域 (内容多了在这里滚动) -->
    <div class="content-area">
      <router-view />
    </div>
  </div>
</template>

<style scoped>
/* 1. 根容器：占满屏幕，禁止 Body 滚动 */
.page-container {
  display: flex;
  flex-direction: column;
  height: 100vh; 
  width: 100vw;
  overflow: hidden; /* 关键：防止整个网页出现双滚动条 */
  background-color: #f0f2f5;
}

/* 2. 内容区域：占据剩余空间，并允许内部滚动 */
.content-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  
  /* 👇👇👇 修改这里 👇👇👇 */
  overflow-y: auto; /* 允许纵向滚动 */
  overflow-x: hidden; /* 防止横向滚动条 */
  /* 👆👆👆 修改结束 👆👆👆 */
  
  position: relative;
}
</style>