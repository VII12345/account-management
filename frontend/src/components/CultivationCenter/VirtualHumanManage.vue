<script setup lang="ts">
import { ref, computed, watch } from 'vue'

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

// 新增、删除标签逻辑
const newTagName = ref('')
const handleAddTag = () => {
  const name = newTagName.value.trim()
  if (!name) return
  if (tags.value.some((t) => t.name === name)) {
    alert('该标签已存在')
    return
  }
  tags.value.unshift({ name, checked: true })
  newTagName.value = ''
}

const handleDeleteTag = (tagName: string) => {
  if (window.confirm(`确定要删除标签 "${tagName}" 吗？`)) {
    tags.value = tags.value.filter((t) => t.name !== tagName)
  }
}

// 筛选条件
const selectedPlatform = ref<string>('')
const selectedRegion = ref<string>('')

// 地区选项
const regions = ref<string[]>([
  '中国大陆', '中国香港', '中国澳门', '中国台湾', '美国', '加拿大', '英国', '法国', 
  '德国', '意大利', '西班牙', '俄罗斯', '日本', '韩国', '新加坡', '马来西亚', 
  '泰国', '越南', '印度', '澳大利亚', '新西兰', '巴西', '阿根廷', '南非', '欧洲', '其他'
])

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
    gender: '男',
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
    gender: '男',
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
    gender: '男',
    avatar: 'https://i.pravatar.cc/150?img=5',
  },
])

// ================= 新增：前端过滤与分页逻辑 =================
const filteredPersons = computed(() => {
  return persons.value.filter((p) => {
    // 关键词匹配（匹配姓名或职业）
    const matchKeyword = p.name.includes(keyword.value) || p.job.includes(keyword.value)
    // 平台和地区匹配
    const matchPlatform = selectedPlatform.value ? p.platform === selectedPlatform.value : true
    const matchRegion = selectedRegion.value ? p.country === selectedRegion.value : true
    
    // 标签匹配
    const checkedTags = tags.value.filter(t => t.checked).map(t => t.name)
    const matchTag = allChecked.value || checkedTags.includes(p.tag)

    return matchKeyword && matchPlatform && matchRegion && matchTag
  })
})

const totalRecords = computed(() => filteredPersons.value.length)
const currentPage = ref(1)
const pageSize = ref(20)
const totalPages = computed(() => Math.ceil(totalRecords.value / pageSize.value) || 1)

const paginatedPersons = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredPersons.value.slice(start, end)
})

// 监听筛选条件变化自动回到第一页
watch([keyword, selectedPlatform, selectedRegion, tags, allChecked, pageSize], () => {
  currentPage.value = 1
}, { deep: true })

// ================= 编辑、新增与删除逻辑 =================
const isModalVisible = ref(false)
const modalMode = ref<'add' | 'edit'>('add')
const currentPerson = ref<Partial<VirtualPerson>>({})

const handleAdd = () => {
  modalMode.value = 'add'
  currentPerson.value = {
    name: '',
    gender: '男',
    country: '中国大陆',
    age: 20,
    job: '',
    tag: tags.value[0]?.name || '',
    platform: '未注册平台',
    avatar: `https://i.pravatar.cc/150?img=${Math.floor(Math.random() * 70)}`
  }
  isModalVisible.value = true
}

const handleEdit = (person: VirtualPerson) => {
  modalMode.value = 'edit'
  currentPerson.value = { ...person }
  isModalVisible.value = true
}

const handleSave = () => {
  if (!currentPerson.value.name) {
    alert('请输入姓名')
    return
  }
  if (modalMode.value === 'add') {
    const newId = persons.value.length > 0 ? Math.max(...persons.value.map(p => p.id)) + 1 : 1
    persons.value.unshift({ ...currentPerson.value, id: newId } as VirtualPerson)
  } else {
    const index = persons.value.findIndex((p) => p.id === currentPerson.value.id)
    if (index !== -1) {
      persons.value[index] = { ...currentPerson.value } as VirtualPerson
    }
  }
  isModalVisible.value = false
}

const handleCancel = () => {
  isModalVisible.value = false
}

const handleDelete = (id: number) => {
  const isConfirmed = window.confirm('确定要删除这位虚拟人吗？操作后不可恢复。')
  if (isConfirmed) {
    persons.value = persons.value.filter((p) => p.id !== id)
  }
}
// ========================================================

const handleMenuClick = (label: string) => {
  activeMenu.value = label
}
const handleSubMenuClick = (label: string) => {
  activeSubMenu.value = label
}
const handleSearch = () => {
  currentPage.value = 1
}
const handleReset = () => {
  selectedPlatform.value = ''
  selectedRegion.value = ''
  keyword.value = ''
  allChecked.value = true
  tags.value.forEach((t) => (t.checked = true))
  currentPage.value = 1
}
const handlePageChange = (page: number) => {
  if (page < 1 || page > totalPages.value) return
  currentPage.value = page
}
</script>

<template>
  <div class="vh-container">
    <main class="main-content">
      <div class="breadcrumb">
        <span>培育中心</span>
        <span class="breadcrumb-separator">›</span>
        <span class="active">虚拟人管理</span>
      </div>

      <div class="vh-layout">
        <div class="tag-panel">
          <h3 class="tag-title">标签</h3>
          
          <div class="add-tag-box">
            <input v-model="newTagName" placeholder="输入新标签" class="add-tag-input" @keyup.enter="handleAddTag" />
            <button class="btn-add-tag" @click="handleAddTag">+</button>
          </div>

          <div class="tag-item">
            <label><input type="checkbox" v-model="allChecked" @change="toggleAll" /> 全部</label>
          </div>
          <div v-for="tag in tags" :key="tag.name" class="tag-item with-delete">
            <label>
              <input type="checkbox" v-model="tag.checked" />
              {{ tag.name }}
            </label>
            <button class="btn-delete-tag" @click="handleDeleteTag(tag.name)">✖</button>
          </div>
        </div>

        <div class="content-panel">
          <div class="filters-section">
            <select v-model="selectedPlatform" class="filter-select">
              <option value="">平台</option>
              <option>抖音</option>
              <option>B站</option>
              <option>微博</option>
            </select>
            <select v-model="selectedRegion" class="filter-select">
              <option value="">地区</option>
              <option v-for="region in regions" :key="region" :value="region">{{ region }}</option>
            </select>
            <input v-model="keyword" placeholder="请输入关键词" class="search-input" type="text" />
            <button class="btn-search" @click="handleSearch">🔍 搜索</button>
            <button class="btn-reset" @click="handleReset">🔄 重置</button>
            <button class="btn-primary" @click="handleAdd">新增虚拟人</button>
          </div>

          <div class="cards-grid">
            <div v-for="person in paginatedPersons" :key="person.id" class="person-card">
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
                <button class="icon-btn" @click="handleEdit(person)">✏️</button>
                <button class="icon-btn" @click="handleDelete(person.id)">🗑️</button>
              </div>
            </div>
          </div>

          <div class="pagination">
            <div class="pagination-info">共 {{ totalRecords }} 条数据</div>
            <div class="pagination-controls">
              <select v-model="pageSize" class="page-size-select">
                <option :value="20">20 条/页</option>
                <option :value="50">50 条/页</option>
                <option :value="100">100 条/页</option>
              </select>
              <button class="page-btn" :disabled="currentPage === 1" @click="handlePageChange(currentPage - 1)">‹</button>
              <button class="page-btn page-btn-active">{{ currentPage }} / {{ totalPages }}</button>
              <button class="page-btn" :disabled="currentPage === totalPages" @click="handlePageChange(currentPage + 1)">›</button>
            </div>
          </div>
        </div>
      </div>
    </main>

    <div v-if="isModalVisible" class="modal-overlay" @click.self="handleCancel">
      <div class="modal-content">
        <h3>{{ modalMode === 'add' ? '新增虚拟人' : '编辑虚拟人' }}</h3>
        <div class="form-group" v-if="currentPerson">
          <label>姓名：</label>
          <input v-model="currentPerson.name" class="form-input" placeholder="请输入姓名" />
          
          <label>性别：</label>
          <select v-model="currentPerson.gender" class="form-input">
            <option value="男">男</option>
            <option value="女">女</option>
          </select>

          <label>国家/地区：</label>
          <select v-model="currentPerson.country" class="form-input">
            <option v-for="region in regions" :key="region" :value="region">{{ region }}</option>
          </select>

          <label>年龄：</label>
          <input type="number" v-model="currentPerson.age" class="form-input" placeholder="请输入年龄" />

          <label>职业：</label>
          <input v-model="currentPerson.job" class="form-input" placeholder="请输入职业" />

          <label>标签：</label>
          <select v-model="currentPerson.tag" class="form-input">
            <option v-for="tag in tags" :key="tag.name" :value="tag.name">{{ tag.name }}</option>
          </select>

          <label>平台：</label>
          <select v-model="currentPerson.platform" class="form-input">
            <option value="未注册平台">未注册平台</option>
            <option value="抖音">抖音</option>
            <option value="B站">B站</option>
            <option value="微博">微博</option>
          </select>
        </div>
        <div class="modal-actions">
          <button class="btn-reset" @click="handleCancel">取消</button>
          <button class="btn-primary" @click="handleSave">保存</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.vh-container {
  display: flex;
  min-height: 100vh;
  width: 100%;
  flex-direction: column;
  background-image: url('/image/background.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
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

/* 新增/删除标签样式 */
.add-tag-box {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}
.add-tag-input {
  flex: 1;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  padding: 0.25rem 0.5rem;
  font-size: 0.8125rem;
  outline: none;
  width: 0; /* 配合 flex: 1 避免撑破容器 */
}
.add-tag-input:focus {
  border-color: #2563eb;
}
.btn-add-tag {
  background: #2563eb;
  color: white;
  border: none;
  border-radius: 0.375rem;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 1rem;
  line-height: 1;
  flex-shrink: 0;
}
.btn-add-tag:hover {
  background: #1d4ed8;
}
.tag-item.with-delete {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.tag-item label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  flex: 1;
}
.btn-delete-tag {
  background: transparent;
  border: none;
  color: #9ca3af;
  cursor: pointer;
  font-size: 0.75rem;
  padding: 0.25rem;
  visibility: hidden;
}
.tag-item.with-delete:hover .btn-delete-tag {
  visibility: visible;
}
.btn-delete-tag:hover {
  color: #ef4444;
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
  transition: transform 0.2s;
}
.icon-btn:hover {
  transform: scale(1.1);
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

/* ================= 新增：弹窗样式 ================= */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}
.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 0.75rem;
  width: 400px;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}
.modal-content h3 {
  margin-top: 0;
  margin-bottom: 1.5rem;
  font-size: 1.25rem;
  color: #111827;
}
.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  max-height: 60vh;
  overflow-y: auto;
}
.form-group label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
  margin-top: 0.5rem;
}
.form-input {
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  padding: 0.5rem;
  font-size: 0.875rem;
  outline: none;
  transition: border-color 0.2s;
}
.form-input:focus {
  border-color: #2563eb;
}
.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}
</style>

