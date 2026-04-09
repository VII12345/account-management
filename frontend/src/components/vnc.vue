<!--
  文件注释：frontend/src/components/vnc.vue

  职责：承载当前页面/组件的视图结构、交互事件与状态绑定。
  边界：仅处理前端展示与交互编排，不在此文件实现后端业务规则。
-->

<template>
  <div class="vnc-container">
    <h1>just a try</h1>
    <iframe
      src="https://120.26.177.167:6080/vnc.html"
      allowfullscreen
    ></iframe>
  </div>
</template>

<script setup lang="ts">
// 这里暂时不需要逻辑，如果以后要动态传入地址，可以用 props
</script>

<style scoped>
.vnc-container {
  margin: 0;
  padding: 0;
  height: 100vh; /* 占满整个视口高度 */
  width: 100vw;  /* 占满整个视口宽度 */
  display: flex;
  flex-direction: column;
}

.vnc-container h1 {
  margin: 0;
  padding: 8px;
  background: #f0f0f0;
  font-size: 18px;
}

.vnc-container iframe {
  flex: 1;
  border: none;
  width: 100%;
}
</style>
