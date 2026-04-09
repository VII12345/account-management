/**
 * 文件注释：frontend/src/router.ts
 *
 * 职责：封装当前模块的初始化、常量、工具函数或组件逻辑。
 * 边界：仅承担本模块职责，不在此处定义跨模块业务规则。
 */

// src/router.ts
import { createRouter, createWebHistory } from 'vue-router'
import HomePage from './components/Home.vue'
import AccountCenter from './components/AccountCenter.vue'
import CultivationLayout from './components/CultivationCenter/Layout.vue'
import DailyTraining from './components/CultivationCenter/DailyTraining.vue'
import VirtualHumanManage from './components/CultivationCenter/VirtualHumanManage.vue'
import TaskCenter from './components/TaskCenter/TaskCenter.vue'
import TaskDetail from './components/TaskCenter/Detail.vue'
import RpaIframe from './components/Strategies/RpaIframe.vue'
import OpsLayout from './components/OpsCenter/Layout.vue'
import ContainerDetail from './components/OpsCenter/ContainerDetail.vue'
import ProxyDetail from './components/OpsCenter/ProxyDetail.vue'
import EmailDetail from './components/OpsCenter/EmailDetail.vue'
import Login from './components/Login.vue'
import Profile from './components/Profile.vue'
import { isAuthenticated } from './utils/auth'

const routes = [
  { path: '/', name: 'home', component: HomePage, meta: { requiresAuth: true } },
  { path: '/login', name: 'login', component: Login, meta: { requiresAuth: false } },
  { path: '/profile', name: 'profile', component: Profile, meta: { requiresAuth: true } },
  { path: '/account', name: 'account', component: AccountCenter, meta: { requiresAuth: true } },
  {
    path: '/cultivation',
    name: 'cultivation',
    component: CultivationLayout,
    redirect: '/cultivation/daily-training',
    meta: { requiresAuth: true },
    children: [
      {
        path: 'daily-training',
        name: 'daily-training',
        component: DailyTraining,
      },
      {
        path: 'virtual-human',
        name: 'virtual-human',
        component: VirtualHumanManage,
      },
    ],
  },
  { path: '/tasks', name: 'tasks', component: TaskCenter, meta: { requiresAuth: true } },
  { path: '/task/detail/:id', name: 'task-detail', component: TaskDetail, meta: { requiresAuth: true } },
  { path: '/strategy', name: 'strategy', component: RpaIframe, meta: { requiresAuth: true } },
  {
    path: '/ops',
    name: 'ops',
    component: OpsLayout,
    redirect: '/ops/proxy',
    meta: { requiresAuth: true },
    children: [
      {
        path: 'proxy',
        name: 'proxy',
        component: ProxyDetail,
      },
      {
        path: 'container',
        name: 'container',
        component: ContainerDetail,
      },
      {
        path: 'email',
        name: 'email',
        component: EmailDetail,
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫 - 检测登录状态
router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)

  if (requiresAuth && !isAuthenticated()) {
    // 需要登录但未登录，跳转到登录页
    next({
      path: '/login',
      query: { redirect: to.fullPath }
    })
  } else if (to.path === '/login' && isAuthenticated()) {
    // 已登录但访问登录页，跳转到首页
    next('/')
  } else {
    next()
  }
})

export default router
