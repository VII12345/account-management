<!-- VirtualHumanManage.vue -->
<script setup lang="ts">
import { ref } from 'vue'

// 菜单状态
const activeMenu = ref<string>('培育中心')
const activeSubMenu = ref<string>('虚拟人管理')

// 标签筛选
interface TagItem {
  name: string
  checked: boolean
}

const tags = ref<TagItem[]>([
  { name: '瑜伽修行者', checked: false },
  { name: '哲学思考者', checked: false },
  { name: '热血电竞选手', checked: false },
  { name: '创意设计天才', checked: false },
  { name: '摄影摄像发烧友', checked: false },
  { name: '时尚搭配达人', checked: false },
  { name: '热爱自然保护者', checked: false },
  { name: '深度心理学爱好者', checked: false },
  { name: '搞笑段子手', checked: false },
  { name: '推理迷', checked: false },
  { name: '独立思考者', checked: false },
  { name: '热爱公益志愿者', checked: false },
  { name: '爱心动物保护者', checked: false },
  { name: '音乐发烧友', checked: false },
  { name: '艺术创作狂热者', checked: false },
])

const allChecked = ref(true)
const toggleAll = () => {
  allChecked.value = !allChecked.value
  tags.value.forEach((t) => (t.checked = allChecked.value))
}

// 筛选条件
const selectedPlatform = ref<string>('')
const selectedRegion = ref<string>('')

// 搜索
const keyword = ref<string>('')

// 虚拟人数据
interface VirtualPerson {
  id: number
  name: string
  country: string
  age: number
  job: string
  tag: string
  avatar: string
  platform: string
  gender: string
}

const persons = ref<VirtualPerson[]>([
  {
    id: 1,
    name: 'Anderson Olivia',
    country: '美国',
    age: 35,
    job: '医生',
    tag: '瑜伽修行者',
    platform: '未注册平台',
    gender: '♂',
    avatar: 'https://i.pravatar.cc/150?img=3',
  },
  {
    id: 2,
    name: 'Smith Charlotte',
    country: '美国',
    age: 27,
    job: '建筑师',
    tag: '热血电竞选手',
    platform: '未注册平台',
    gender: '♂',
    avatar: 'https://i.pravatar.cc/150?img=8',
  },
  {
    id: 3,
    name: '曹廷宇',
    country: '中国台湾',
    age: 33,
    job: '医生',
    tag: '摄影摄像发烧友',
    platform: '未注册平台',
    gender: '♂',
    avatar: 'https://i.pravatar.cc/150?img=5',
  },
])

const totalRecords = ref(31346)
const currentPage = ref(1)
const pageSize = ref(20)

const handleMenuClick = (label: string) => {
  activeMenu.value = label
}
const handleSubMenuClick = (label: string) => {
  activeSubMenu.value = label
}
const handleSearch = () => {
  console.log('搜索:', keyword.value)
}
const handleReset = () => {
  selectedPlatform.value = ''
  selectedRegion.value = ''
  keyword.value = ''
  allChecked.value = true
  tags.value.forEach((t) => (t.checked = true))
}
const handleAdd = () => {
  console.log('新增虚拟人')
}
const handlePageChange = (page: number) => {
  if (page < 1) return
  currentPage.value = page
}
</script>

<template>
  <div class="vh-container">
    <!-- 左侧导航 -->

    <!-- 主体 -->
    <main class="main-content">
      <!-- 面包屑 -->
      <div class="breadcrumb">
        <span>培育中心</span>
        <span class="breadcrumb-separator">›</span>
        <span class="active">虚拟人管理</span>
      </div>

      <div class="vh-layout">
        <!-- 左侧标签栏 -->
        <div class="tag-panel">
          <h3 class="tag-title">标签</h3>
          <div class="tag-item">
            <label><input type="checkbox" v-model="allChecked" @change="toggleAll" /> 全部</label>
          </div>
          <div v-for="tag in tags" :key="tag.name" class="tag-item">
            <label>
              <input type="checkbox" v-model="tag.checked" />
              {{ tag.name }}
            </label>
          </div>
        </div>

        <!-- 右侧内容区 -->
        <div class="content-panel">
          <!-- 筛选条件 -->
          <div class="filters-section">
            <select v-model="selectedPlatform" class="filter-select">
              <option value="">平台</option>
              <option>抖音</option>
              <option>B站</option>
              <option>微博</option>
            </select>
            <select v-model="selectedRegion" class="filter-select">
              <option value="">地区</option>
              <option>中国大陆</option>
              <option>美国</option>
              <option>欧洲</option>
            </select>
            <input v-model="keyword" placeholder="请输入关键词" class="search-input" type="text" />
            <button class="btn-search" @click="handleSearch">🔍 搜索</button>
            <button class="btn-reset" @click="handleReset">🔄 重置</button>
            <button class="btn-primary" @click="handleAdd">新增虚拟人</button>
          </div>

          <!-- 卡片列表 -->
          <div class="cards-grid">
            <div v-for="person in persons" :key="person.id" class="person-card">
              <div class="card-top">
                <img :src="person.avatar" class="avatar" alt="" />
                <div class="person-info">
                  <h4>{{ person.name }} <span class="gender">{{ person.gender }}</span></h4>
                  <p class="meta">{{ person.country }} · {{ person.age }}岁 · {{ person.job }}</p>
                </div>
              </div>
              <div class="tag">{{ person.tag }}</div>
              <div class="platform">{{ person.platform }}</div>
              <div class="card-actions">
                <button class="icon-btn">✏️</button>
                <button class="icon-btn">🗑️</button>
              </div>
            </div>
          </div>

          <!-- 分页 -->
          <div class="pagination">
            <div class="pagination-info">共 {{ totalRecords }} 条数据</div>
            <div class="pagination-controls">
              <select v-model="pageSize" class="page-size-select">
                <option :value="20">20 条/页</option>
                <option :value="50">50 条/页</option>
                <option :value="100">100 条/页</option>
              </select>
              <button class="page-btn" :disabled="currentPage === 1" @click="handlePageChange(currentPage - 1)">‹</button>
              <button class="page-btn page-btn-active">{{ currentPage }}</button>
              <button class="page-btn" @click="handlePageChange(currentPage + 1)">›</button>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.vh-container {
  display: flex;
  min-height: 100vh;
  width: 100%;
  flex-direction: column;
  background-image: url('/image/background.jpg'); /* 替换为你的图片路径 */
  background-size: cover; /* 图片铺满容器 */
  background-position: center; /* 图片居中显示 */
  background-repeat: no-repeat; /* 不重复 */
}

/* 左侧菜单 */
.sidebar {
  width: 180px;
  background: #f0f2f5;
  border-right: 1px solid #e5e7eb;
  padding: 1rem 0;
}
.menu-item {
  padding: 0.75rem 1.5rem;
  cursor: pointer;
  color: #374151;
}
.menu-item-active {
  background: #e0e7ff;
  color: #4f46e5;
}
.submenu-item {
  padding: 0.625rem 2rem;
  cursor: pointer;
  color: #6b7280;
}
.submenu-item-active {
  background: #dbeafe;
  color: #2563eb;
}

/* 主体布局 */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 1.5rem 2rem;
}
.breadcrumb {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
  color: #6b7280;
}
.breadcrumb .active {
  color: #2563eb;
}

/* 两栏布局 */
.vh-layout {
  display: flex;
  gap: 1rem;
}

/* 标签栏 */
.tag-panel {
  width: 200px;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  padding: 1rem;
  overflow-y: auto;
  height: calc(100vh - 160px);
}
.tag-title {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}
.tag-item {
  margin-bottom: 0.25rem;
  font-size: 0.875rem;
  color: #374151;
}

/* 内容区 */
.content-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* 筛选区 */
.filters-section {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  padding: 0.75rem 1rem;
}
.filter-select,
.search-input {
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  padding: 0.375rem 0.75rem;
  font-size: 0.875rem;
}
.btn-search,
.btn-reset,
.btn-primary {
  border: none;
  border-radius: 0.375rem;
  padding: 0.5rem 0.875rem;
  cursor: pointer;
  font-size: 0.875rem;
}
.btn-search {
  background: #2563eb;
  color: white;
}
.btn-reset {
  background: #f9fafb;
  border: 1px solid #d1d5db;
}
.btn-primary {
  background: #2563eb;
  color: white;
  margin-left: auto;
}

/* 卡片 */
.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 1rem;
}
.person-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 0.75rem;
  padding: 1rem;
  position: relative;
}
.card-top {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}
.avatar {
  width: 56px;
  height: 56px;
  border-radius: 50%;
}
.person-info h4 {
  font-size: 1rem;
  font-weight: 600;
}
.meta {
  color: #6b7280;
  font-size: 0.875rem;
}
.tag {
  margin-top: 0.5rem;
  color: #2563eb;
  font-size: 0.875rem;
}
.platform {
  font-size: 0.75rem;
  color: #9ca3af;
}
.card-actions {
  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
  display: flex;
  gap: 0.25rem;
}
.icon-btn {
  background: transparent;
  border: none;
  cursor: pointer;
  font-size: 0.875rem;
}

/* 分页 */
.pagination {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  padding: 1rem;
}
.pagination-info {
  font-size: 0.875rem;
  color: #6b7280;
}
.pagination-controls {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.page-size-select,
.page-btn {
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  padding: 0.375rem 0.75rem;
  background: white;
  font-size: 0.875rem;
  cursor: pointer;
}
.page-btn-active {
  background: #2563eb;
  color: white;
}
.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
