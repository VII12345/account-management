/**
 * 文件注释：frontend/src/main.ts
 *
 * 职责：封装当前模块的初始化、常量、工具函数或组件逻辑。
 * 边界：仅承担本模块职责，不在此处定义跨模块业务规则。
 */

// src/main.ts
import { createApp } from 'vue'
import './assets/tailwind.css'
import App from './App.vue'
import router from './router'


createApp(App).use(router).mount('#app')