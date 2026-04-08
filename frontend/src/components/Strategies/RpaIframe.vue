<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

// 你的 React 项目地址
const REACT_APP_URL = 'http://hk.xzzzs.icu:3001' 

const iframeRef = ref<HTMLIFrameElement | null>(null)
const isLoading = ref(true)

const handleLoad = () => {
  isLoading.value = false
}
</script>

<template>
  <!-- 这个根 div 会直接被放入 App.vue 的 .content-area 中 -->
  <div class="iframe-wrapper">
    
    <div v-if="isLoading" class="loading-mask">
      加载中...
    </div>

    <iframe 
      ref="iframeRef"
      :src="REACT_APP_URL" 
      class="rpa-frame"
      @load="handleLoad"
    ></iframe>
  </div>
</template>

<style scoped>
/* 1. 组件根容器：必须宽高 100% 才能接住父级给的空间 */
.iframe-wrapper {
  width: 100%;
  height: 100%; 
  position: relative;
  display: flex;
  flex-direction: column;
}

/* 2. Iframe 本体：撑满根容器 */
.rpa-frame {
  flex: 1; /* 或者 height: 100% */
  width: 100%;
  border: none;
  display: block;
}

.loading-mask {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
}
</style>