/**
 * 文件注释：frontend/src/main.js
 *
 * 职责：封装当前模块的初始化、常量、工具函数或组件逻辑。
 * 边界：仅承担本模块职责，不在此处定义跨模块业务规则。
 */

import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'

createApp(App).mount('#app')
