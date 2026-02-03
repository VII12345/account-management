<!-- AccountCenter.vue -->
<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue'
import { authFetch } from '../utils/auth'

const API_BASE_URL = '/api'

// 类型定义
interface AccountData {
  id: number
  platform: string | null
  username: string
  password: string
  email: string | null
  phone: string | null
  status: string | null
  created_at: string | null
  tags: string | null
}

interface AccountForm {
  platform: string
  username: string
  password: string
  email: string
  phone: string
  status: string
  tags: string
}

// 状态
const activeMenu = ref<string>('账号管理')
const activeSubMenu = ref<string>('账号列表')
const searchKeyword = ref<string>('')
const selectedPlatform = ref<string>('')
const selectedStatus = ref<string>('')
const currentPage = ref<number>(1)
const pageSize = ref<number>(20)
const loading = ref<boolean>(false)

// 菜单数据
const menuItems = [
  { id: 'account', label: '账号管理', children: ['账号列表', '批量导入'] }
]

// 表格数据
const tableData = ref<AccountData[]>([])
const totalRecords = ref<number>(0)

// 弹窗状态
const showModal = ref<boolean>(false)
const modalMode = ref<'create' | 'edit'>('create')
const editingId = ref<number | null>(null)
const accountForm = ref<AccountForm>({
  platform: '',
  username: '',
  password: '',
  email: '',
  phone: '',
  status: 'active',
  tags: ''
})

// 导入弹窗状态
const showImportModal = ref<boolean>(false)
const importType = ref<'json' | 'csv'>('json')
const jsonInput = ref<string>('')
const csvFile = ref<File | null>(null)
const importLoading = ref<boolean>(false)

// 删除确认弹窗
const showDeleteModal = ref<boolean>(false)
const deletingId = ref<number | null>(null)

// 筛选选项
const platformOptions = ['Facebook', 'Instagram', 'Twitter', 'TikTok', 'YouTube', 'LinkedIn', 'WhatsApp', 'reddit', 'facebook', 'instagram', 'twitter', 'tiktok']
const statusOptions = ['active', 'inactive', 'suspended', 'pending', 'risk', 'banned']

// 计算总页数
const totalPages = computed(() => Math.ceil(totalRecords.value / pageSize.value))

// 获取账号列表
const fetchAccounts = async (): Promise<void> => {
  loading.value = true
  try {
    const response = await authFetch(
      `${API_BASE_URL}/accounts/?page=${currentPage.value}&page_size=${pageSize.value}`
    )
    if (response.ok) {
      const data = await response.json()
      // 后端返回的是数组格式 [id, platform, username, password, email, phone, status, created_at, tags]
      // 需要转换为对象格式
      tableData.value = (data.data || []).map((row: any[]) => ({
        id: row[0],
        platform: row[1],
        username: row[2],
        password: row[3],
        email: row[4],
        phone: row[5],
        status: row[6],
        created_at: row[7],
        tags: row[8]
      }))
      totalRecords.value = data.total || 0
    } else {
      console.error('获取账号列表失败')
    }
  } catch (error) {
    console.error('获取账号列表出错:', error)
  } finally {
    loading.value = false
  }
}

// 创建账号
const createAccount = async (): Promise<void> => {
  try {
    const response = await authFetch(`${API_BASE_URL}/accounts/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        platform: accountForm.value.platform || null,
        username: accountForm.value.username,
        password: accountForm.value.password,
        email: accountForm.value.email || null,
        phone: accountForm.value.phone || null,
        status: accountForm.value.status || 'active',
        tags: accountForm.value.tags || null
      })
    })
    if (response.ok) {
      alert('账号创建成功')
      closeModal()
      fetchAccounts()
    } else {
      const error = await response.json()
      alert(error.detail || '创建失败')
    }
  } catch (error) {
    console.error('创建账号出错:', error)
    alert('创建账号出错')
  }
}

// 更新账号
const updateAccount = async (): Promise<void> => {
  if (!editingId.value) return
  try {
    const response = await authFetch(`${API_BASE_URL}/accounts/${editingId.value}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        platform: accountForm.value.platform || null,
        username: accountForm.value.username,
        password: accountForm.value.password,
        email: accountForm.value.email || null,
        phone: accountForm.value.phone || null,
        status: accountForm.value.status || 'active',
        tags: accountForm.value.tags || null
      })
    })
    if (response.ok) {
      alert('账号更新成功')
      closeModal()
      fetchAccounts()
    } else {
      const error = await response.json()
      alert(error.detail || '更新失败')
    }
  } catch (error) {
    console.error('更新账号出错:', error)
    alert('更新账号出错')
  }
}

// 删除账号
const deleteAccount = async (): Promise<void> => {
  if (!deletingId.value) return
  try {
    const response = await authFetch(`${API_BASE_URL}/accounts/${deletingId.value}`, {
      method: 'DELETE'
    })
    if (response.ok) {
      alert('账号删除成功')
      showDeleteModal.value = false
      deletingId.value = null
      fetchAccounts()
    } else {
      const error = await response.json()
      alert(error.detail || '删除失败')
    }
  } catch (error) {
    console.error('删除账号出错:', error)
    alert('删除账号出错')
  }
}

// JSON 批量导入
const importJson = async (): Promise<void> => {
  if (!jsonInput.value.trim()) {
    alert('请输入 JSON 数据')
    return
  }
  importLoading.value = true
  try {
    const accounts = JSON.parse(jsonInput.value)
    if (!Array.isArray(accounts)) {
      alert('JSON 数据必须是数组格式')
      return
    }
    const response = await authFetch(`${API_BASE_URL}/accounts/import/json`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(accounts)
    })
    if (response.ok) {
      const result = await response.json()
      alert(result.message || '导入成功')
      closeImportModal()
      fetchAccounts()
    } else {
      const error = await response.json()
      alert(error.detail || '导入失败')
    }
  } catch (error) {
    console.error('JSON 导入出错:', error)
    alert('JSON 格式错误或导入出错')
  } finally {
    importLoading.value = false
  }
}

// CSV 批量导入
const importCsv = async (): Promise<void> => {
  if (!csvFile.value) {
    alert('请选择 CSV 文件')
    return
  }
  importLoading.value = true
  try {
    const formData = new FormData()
    formData.append('file', csvFile.value)
    const response = await authFetch(`${API_BASE_URL}/accounts/import/csv`, {
      method: 'POST',
      body: formData
    })
    if (response.ok) {
      const result = await response.json()
      alert(result.message || '导入成功')
      closeImportModal()
      fetchAccounts()
    } else {
      const error = await response.json()
      alert(error.detail || '导入失败')
    }
  } catch (error) {
    console.error('CSV 导入出错:', error)
    alert('CSV 导入出错')
  } finally {
    importLoading.value = false
  }
}

// 处理导入
const handleImport = (): void => {
  if (importType.value === 'json') {
    importJson()
  } else {
    importCsv()
  }
}

// 处理 CSV 文件选择
const handleFileChange = (event: Event): void => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    csvFile.value = target.files[0] as File
  }
}

// 打开创建弹窗
const openCreateModal = (): void => {
  modalMode.value = 'create'
  editingId.value = null
  accountForm.value = {
    platform: '',
    username: '',
    password: '',
    email: '',
    phone: '',
    status: 'active',
    tags: ''
  }
  showModal.value = true
}

// 打开编辑弹窗
const openEditModal = (account: AccountData): void => {
  modalMode.value = 'edit'
  editingId.value = account.id
  accountForm.value = {
    platform: account.platform || '',
    username: account.username,
    password: account.password,
    email: account.email || '',
    phone: account.phone || '',
    status: account.status || 'active',
    tags: account.tags || ''
  }
  showModal.value = true
}

// 关闭弹窗
const closeModal = (): void => {
  showModal.value = false
  editingId.value = null
}

// 打开导入弹窗
const openImportModal = (): void => {
  importType.value = 'json'
  jsonInput.value = ''
  csvFile.value = null
  showImportModal.value = true
}

// 关闭导入弹窗
const closeImportModal = (): void => {
  showImportModal.value = false
  jsonInput.value = ''
  csvFile.value = null
}

// 打开删除确认弹窗
const openDeleteModal = (id: number): void => {
  deletingId.value = id
  showDeleteModal.value = true
}

// 提交表单
const handleSubmit = (): void => {
  if (!accountForm.value.username || !accountForm.value.password) {
    alert('用户名和密码是必填项')
    return
  }
  if (modalMode.value === 'create') {
    createAccount()
  } else {
    updateAccount()
  }
}

// 搜索（前端过滤，也可以扩展为后端搜索）
const filteredData = computed(() => {
  let data = tableData.value
  if (searchKeyword.value) {
    const keyword = searchKeyword.value.toLowerCase()
    data = data.filter(item =>
      item.username.toLowerCase().includes(keyword) ||
      (item.email && item.email.toLowerCase().includes(keyword)) ||
      (item.platform && item.platform.toLowerCase().includes(keyword))
    )
  }
  if (selectedPlatform.value) {
    data = data.filter(item => item.platform === selectedPlatform.value)
  }
  if (selectedStatus.value) {
    data = data.filter(item => item.status === selectedStatus.value)
  }
  return data
})

// 清空筛选
const handleClearFilters = (): void => {
  selectedPlatform.value = ''
  selectedStatus.value = ''
  searchKeyword.value = ''
}

// 分页切换
const handlePageChange = (page: number): void => {
  if (page < 1 || page > totalPages.value) return
  currentPage.value = page
}

// 菜单点击
const handleMenuClick = (label: string): void => {
  activeMenu.value = label
}

const handleSubMenuClick = (label: string): void => {
  activeSubMenu.value = label
  if (label === '批量导入') {
    openImportModal()
  }
}

// 格式化日期
const formatDate = (dateStr: string | null): string => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN')
}

// 获取状态显示文本
const getStatusText = (status: string | null): string => {
  const statusMap: Record<string, string> = {
    'active': '正常',
    'inactive': '停用',
    'suspended': '暂停',
    'pending': '待验证',
    'risk': '风控',
    'banned': '封禁'
  }
  return statusMap[status || ''] || status || '-'
}

// 获取状态样式类
const getStatusClass = (status: string | null): string => {
  const classMap: Record<string, string> = {
    'active': 'status-active',
    'inactive': 'status-inactive',
    'suspended': 'status-suspended',
    'pending': 'status-pending',
    'risk': 'status-risk',
    'banned': 'status-banned'
  }
  return classMap[status || ''] || ''
}

// 监听分页变化
watch([currentPage, pageSize], () => {
  fetchAccounts()
})

// 组件挂载时获取数据
onMounted(() => {
  fetchAccounts()
})
</script>

<template>
  <div class="account-center-container">
    <!-- 左侧边栏 -->
    <aside class="sidebar">
      <div class="menu-group" v-for="item in menuItems" :key="item.id">
        <div 
          class="menu-item"
          :class="{ 'menu-item-active': activeMenu === item.label }"
          @click="handleMenuClick(item.label)"
        >
          {{ item.label }}
        </div>
        <div 
          v-for="child in item.children" 
          :key="child"
          class="submenu-item"
          :class="{ 'submenu-item-active': activeSubMenu === child }"
          @click="handleSubMenuClick(child)"
        >
          {{ child }}
        </div>
      </div>
    </aside>

    <!-- 主内容区 -->
    <main class="main-content">
      <!-- 面包屑导航 -->
      <div class="breadcrumb">
        <span class="breadcrumb-item">账号中心</span>
        <span class="breadcrumb-separator">›</span>
        <span class="breadcrumb-item active">{{ activeSubMenu }}</span>
      </div>

      <!-- 页面标题和操作按钮 -->
      <div class="page-header">
        <h2 class="page-title">{{ activeSubMenu }}</h2>
        <div class="header-actions">
          <div class="search-box">
            <input
              v-model="searchKeyword"
              type="text"
              placeholder="搜索用户名、邮箱、平台"
              class="search-input"
            />
            <button class="search-button">
              <svg class="icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </button>
          </div>
          <button @click="openImportModal" class="btn-secondary">
            批量导入
          </button>
          <button @click="openCreateModal" class="btn-primary">
            添加账号
          </button>
        </div>
      </div>

      <!-- 筛选条件 -->
      <div class="filters-section">
        <div class="filter-row">
          <div class="filter-item">
            <label class="filter-label">平台：</label>
            <select v-model="selectedPlatform" class="filter-select">
              <option value="">全部</option>
              <option v-for="option in platformOptions" :key="option" :value="option">
                {{ option }}
              </option>
            </select>
          </div>

          <div class="filter-item">
            <label class="filter-label">状态：</label>
            <select v-model="selectedStatus" class="filter-select">
              <option value="">全部</option>
              <option v-for="option in statusOptions" :key="option" :value="option">
                {{ getStatusText(option) }}
              </option>
            </select>
          </div>

          <button @click="handleClearFilters" class="btn-clear">
            清空筛选
          </button>
        </div>
      </div>

      <!-- 表格 -->
      <div class="table-container">
        <div v-if="loading" class="loading-overlay">
          <div class="loading-spinner"></div>
          加载中...
        </div>
        <table class="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>平台</th>
              <th>用户名</th>
              <th>密码</th>
              <th>邮箱</th>
              <th>手机号</th>
              <th>状态</th>
              <th>标签</th>
              <th>创建时间</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="filteredData.length === 0">
              <td colspan="10" class="empty-data">
                暂无数据
              </td>
            </tr>
            <tr v-for="row in filteredData" :key="row.id">
              <td>{{ row.id }}</td>
              <td>{{ row.platform || '-' }}</td>
              <td>{{ row.username }}</td>
              <td class="password-cell">
                <span class="password-hidden">••••••••</span>
              </td>
              <td>{{ row.email || '-' }}</td>
              <td>{{ row.phone || '-' }}</td>
              <td>
                <span class="status-badge" :class="getStatusClass(row.status)">
                  {{ getStatusText(row.status) }}
                </span>
              </td>
              <td>{{ row.tags || '-' }}</td>
              <td>{{ formatDate(row.created_at) }}</td>
              <td class="action-cell">
                <button class="btn-action btn-edit" @click="openEditModal(row)">编辑</button>
                <button class="btn-action btn-delete" @click="openDeleteModal(row.id)">删除</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 分页 -->
      <div class="pagination">
        <div class="pagination-info">
          共 {{ totalRecords }} 条数据
        </div>
        <div class="pagination-controls">
          <select v-model="pageSize" class="page-size-select">
            <option :value="20">20 条/页</option>
            <option :value="50">50 条/页</option>
            <option :value="100">100 条/页</option>
            <option :value="200">200 条/页</option>
          </select>
          <button class="page-btn" @click="handlePageChange(1)" :disabled="currentPage === 1">
            «
          </button>
          <button class="page-btn" @click="handlePageChange(currentPage - 1)" :disabled="currentPage === 1">
            ‹
          </button>
          <span class="page-info">{{ currentPage }} / {{ totalPages || 1 }}</span>
          <button class="page-btn" @click="handlePageChange(currentPage + 1)" :disabled="currentPage >= totalPages">
            ›
          </button>
          <button class="page-btn" @click="handlePageChange(totalPages)" :disabled="currentPage >= totalPages">
            »
          </button>
        </div>
      </div>
    </main>

    <!-- 创建/编辑账号弹窗 -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>{{ modalMode === 'create' ? '添加账号' : '编辑账号' }}</h3>
          <button class="modal-close" @click="closeModal">×</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label class="form-label">平台</label>
            <select v-model="accountForm.platform" class="form-input">
              <option value="">请选择</option>
              <option v-for="option in platformOptions" :key="option" :value="option">
                {{ option }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">用户名 <span class="required">*</span></label>
            <input v-model="accountForm.username" type="text" class="form-input" placeholder="请输入用户名" />
          </div>
          <div class="form-group">
            <label class="form-label">密码 <span class="required">*</span></label>
            <input v-model="accountForm.password" type="text" class="form-input" placeholder="请输入密码" />
          </div>
          <div class="form-group">
            <label class="form-label">邮箱</label>
            <input v-model="accountForm.email" type="email" class="form-input" placeholder="请输入邮箱" />
          </div>
          <div class="form-group">
            <label class="form-label">手机号</label>
            <input v-model="accountForm.phone" type="text" class="form-input" placeholder="请输入手机号" />
          </div>
          <div class="form-group">
            <label class="form-label">状态</label>
            <select v-model="accountForm.status" class="form-input">
              <option v-for="option in statusOptions" :key="option" :value="option">
                {{ getStatusText(option) }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">标签</label>
            <input v-model="accountForm.tags" type="text" class="form-input" placeholder="请输入标签，用逗号分隔" />
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-cancel" @click="closeModal">取消</button>
          <button class="btn-primary" @click="handleSubmit">
            {{ modalMode === 'create' ? '创建' : '保存' }}
          </button>
        </div>
      </div>
    </div>

    <!-- 批量导入弹窗 -->
    <div v-if="showImportModal" class="modal-overlay" @click.self="closeImportModal">
      <div class="modal-content modal-large">
        <div class="modal-header">
          <h3>批量导入账号</h3>
          <button class="modal-close" @click="closeImportModal">×</button>
        </div>
        <div class="modal-body">
          <div class="import-tabs">
            <button 
              class="import-tab" 
              :class="{ active: importType === 'json' }"
              @click="importType = 'json'"
            >
              JSON 导入
            </button>
            <button 
              class="import-tab" 
              :class="{ active: importType === 'csv' }"
              @click="importType = 'csv'"
            >
              CSV 导入
            </button>
          </div>

          <div v-if="importType === 'json'" class="import-content">
            <p class="import-hint">
              请输入 JSON 数组格式的账号数据，每个账号包含以下字段：<br />
              <code>platform</code>, <code>username</code>(必填), <code>password</code>(必填), 
              <code>email</code>, <code>phone</code>, <code>status</code>, <code>tags</code>
            </p>
            <textarea 
              v-model="jsonInput" 
              class="json-textarea" 
              placeholder='[
  {
    "platform": "Facebook",
    "username": "user1",
    "password": "pass123",
    "email": "user1@example.com",
    "phone": "13800000001",
    "status": "active",
    "tags": "测试,新用户"
  }
]'
            ></textarea>
          </div>

          <div v-if="importType === 'csv'" class="import-content">
            <p class="import-hint">
              请上传 CSV 文件，文件需要包含以下列标题：<br />
              <code>platform</code>, <code>username</code>(必填), <code>password</code>(必填), 
              <code>email</code>, <code>phone</code>, <code>status</code>, <code>tags</code>
            </p>
            <div class="file-upload">
              <input 
                type="file" 
                accept=".csv" 
                @change="handleFileChange" 
                id="csv-file"
                class="file-input"
              />
              <label for="csv-file" class="file-label">
                <svg class="upload-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                </svg>
                {{ csvFile ? csvFile.name : '点击选择文件或拖拽文件到此处' }}
              </label>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn-cancel" @click="closeImportModal">取消</button>
          <button class="btn-primary" @click="handleImport" :disabled="importLoading">
            {{ importLoading ? '导入中...' : '开始导入' }}
          </button>
        </div>
      </div>
    </div>

    <!-- 删除确认弹窗 -->
    <div v-if="showDeleteModal" class="modal-overlay" @click.self="showDeleteModal = false">
      <div class="modal-content modal-small">
        <div class="modal-header">
          <h3>确认删除</h3>
          <button class="modal-close" @click="showDeleteModal = false">×</button>
        </div>
        <div class="modal-body">
          <p class="delete-warning">确定要删除这个账号吗？此操作不可恢复。</p>
        </div>
        <div class="modal-footer">
          <button class="btn-cancel" @click="showDeleteModal = false">取消</button>
          <button class="btn-danger" @click="deleteAccount">确认删除</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.account-center-container {
  display: flex;
  min-height: 100vh;
  background-image: url('/image/background.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

/* 侧边栏 */
.sidebar {
  width: 180px;
  background: #f0f2f5;
  padding: 1rem 0;
  border-right: 1px solid #e5e7eb;
}

.menu-group {
  margin-bottom: 0.5rem;
}

.menu-item {
  padding: 0.75rem 1.5rem;
  color: #374151;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s;
  background: transparent;
}

.menu-item:hover {
  background: #e5e7eb;
}

.menu-item-active {
  background: #e0e7ff;
  color: #4f46e5;
  font-weight: 500;
}

.submenu-item {
  padding: 0.625rem 2rem;
  color: #6b7280;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s;
}

.submenu-item:hover {
  background: #e5e7eb;
}

.submenu-item-active {
  background: #dbeafe;
  color: #2563eb;
}

/* 主内容区 */
.main-content {
  display: flex;
  flex-direction: column;
  flex: 1;
  padding: 1.5rem 2rem;
  min-height: 0;
}

/* 面包屑 */
.breadcrumb {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  font-size: 0.875rem;
}

.breadcrumb-item {
  color: #bac3d4;
}

.breadcrumb-item.active {
  color: #edf2fa;
}

.breadcrumb-separator {
  color: #9ca3af;
}

/* 页面头部 */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.page-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #111827;
}

.header-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.search-box {
  display: flex;
  align-items: center;
  background: white;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  overflow: hidden;
}

.search-input {
  border: none;
  outline: none;
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
  width: 240px;
}

.search-button {
  background: transparent;
  border: none;
  padding: 0.5rem 0.75rem;
  cursor: pointer;
  display: flex;
  align-items: center;
}

.search-button .icon {
  width: 18px;
  height: 18px;
  color: #6b7280;
}

.btn-primary {
  background: #2563eb;
  color: white;
  border: none;
  padding: 0.5rem 1.5rem;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-primary:hover {
  background: #1d4ed8;
}

.btn-primary:disabled {
  background: #93c5fd;
  cursor: not-allowed;
}

.btn-secondary {
  background: white;
  color: #374151;
  border: 1px solid #d1d5db;
  padding: 0.5rem 1.5rem;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-secondary:hover {
  background: #f9fafb;
  border-color: #9ca3af;
}

/* 筛选区域 */
.filters-section {
  background: white;
  padding: 1.5rem;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
}

.filter-row {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.filter-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.filter-label {
  font-size: 0.875rem;
  color: #374151;
  white-space: nowrap;
}

.filter-select {
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  padding: 0.375rem 0.75rem;
  font-size: 0.875rem;
  outline: none;
  min-width: 120px;
}

.filter-select:focus {
  border-color: #2563eb;
}

.btn-clear {
  background: white;
  border: 1px solid #d1d5db;
  color: #374151;
  padding: 0.375rem 1rem;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s;
  margin-left: auto;
}

.btn-clear:hover {
  background: #f9fafb;
  border-color: #9ca3af;
}

/* 表格 */
.table-container {
  flex: 1;
  background: white;
  border-radius: 0.5rem;
  overflow: auto;
  border: 1px solid #e5e7eb;
  margin-bottom: 1rem;
  position: relative;
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.8);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  z-index: 10;
}

.loading-spinner {
  width: 32px;
  height: 32px;
  border: 3px solid #e5e7eb;
  border-top-color: #2563eb;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table thead {
  background: #f9fafb;
  position: sticky;
  top: 0;
  z-index: 5;
}

.data-table th {
  padding: 0.75rem 1rem;
  text-align: left;
  font-size: 0.875rem;
  font-weight: 600;
  color: #374151;
  border-bottom: 1px solid #e5e7eb;
  white-space: nowrap;
}

.data-table td {
  padding: 0.75rem 1rem;
  font-size: 0.875rem;
  color: #6b7280;
  border-bottom: 1px solid #f3f4f6;
}

.data-table tbody tr:hover {
  background: #f9fafb;
}

.empty-data {
  text-align: center;
  padding: 3rem 1rem !important;
  color: #9ca3af;
}

.password-cell .password-hidden {
  font-family: monospace;
  letter-spacing: 2px;
}

.status-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
}

.status-active {
  background: #dcfce7;
  color: #166534;
}

.status-inactive {
  background: #f3f4f6;
  color: #6b7280;
}

.status-suspended {
  background: #fee2e2;
  color: #991b1b;
}

.status-pending {
  background: #fef3c7;
  color: #92400e;
}

.status-risk {
  background: #ffedd5;
  color: #c2410c;
}

.status-banned {
  background: #fecaca;
  color: #b91c1c;
}

.action-cell {
  white-space: nowrap;
}

.btn-action {
  padding: 0.25rem 0.75rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  cursor: pointer;
  border: none;
  transition: all 0.2s;
  margin-right: 0.5rem;
}

.btn-edit {
  background: #dbeafe;
  color: #1d4ed8;
}

.btn-edit:hover {
  background: #bfdbfe;
}

.btn-delete {
  background: #fee2e2;
  color: #991b1b;
}

.btn-delete:hover {
  background: #fecaca;
}

/* 分页 */
.pagination {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: auto;
  padding: 1rem;
  background: white;
  border-radius: 0.5rem;
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

.page-size-select {
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  padding: 0.375rem 0.5rem;
  font-size: 0.875rem;
  outline: none;
}

.page-btn {
  min-width: 32px;
  height: 32px;
  border: 1px solid #d1d5db;
  background: white;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s;
}

.page-btn:hover:not(:disabled) {
  background: #f9fafb;
  border-color: #2563eb;
  color: #2563eb;
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  font-size: 0.875rem;
  color: #374151;
  padding: 0 0.5rem;
}

/* 弹窗 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 0.5rem;
  width: 100%;
  max-width: 480px;
  max-height: 90vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.modal-large {
  max-width: 640px;
}

.modal-small {
  max-width: 400px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.modal-header h3 {
  font-size: 1.125rem;
  font-weight: 600;
  color: #111827;
}

.modal-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #6b7280;
  cursor: pointer;
  line-height: 1;
}

.modal-close:hover {
  color: #374151;
}

.modal-body {
  padding: 1.5rem;
  overflow-y: auto;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  padding: 1rem 1.5rem;
  border-top: 1px solid #e5e7eb;
}

.btn-cancel {
  background: white;
  color: #374151;
  border: 1px solid #d1d5db;
  padding: 0.5rem 1.5rem;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  cursor: pointer;
}

.btn-cancel:hover {
  background: #f9fafb;
}

.btn-danger {
  background: #dc2626;
  color: white;
  border: none;
  padding: 0.5rem 1.5rem;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  cursor: pointer;
}

.btn-danger:hover {
  background: #b91c1c;
}

/* 表单 */
.form-group {
  margin-bottom: 1rem;
}

.form-label {
  display: block;
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
  margin-bottom: 0.5rem;
}

.required {
  color: #dc2626;
}

.form-input {
  width: 100%;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  padding: 0.5rem 0.75rem;
  font-size: 0.875rem;
  outline: none;
}

.form-input:focus {
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

/* 导入弹窗 */
.import-tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.import-tab {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  background: white;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s;
}

.import-tab.active {
  background: #2563eb;
  color: white;
  border-color: #2563eb;
}

.import-tab:not(.active):hover {
  background: #f9fafb;
}

.import-content {
  margin-top: 1rem;
}

.import-hint {
  font-size: 0.875rem;
  color: #6b7280;
  margin-bottom: 1rem;
  line-height: 1.6;
}

.import-hint code {
  background: #f3f4f6;
  padding: 0.125rem 0.375rem;
  border-radius: 0.25rem;
  font-size: 0.8125rem;
}

.json-textarea {
  width: 100%;
  min-height: 200px;
  border: 1px solid #d1d5db;
  border-radius: 0.375rem;
  padding: 0.75rem;
  font-family: monospace;
  font-size: 0.875rem;
  resize: vertical;
  outline: none;
}

.json-textarea:focus {
  border-color: #2563eb;
}

.file-upload {
  border: 2px dashed #d1d5db;
  border-radius: 0.5rem;
  padding: 2rem;
  text-align: center;
  transition: all 0.2s;
}

.file-upload:hover {
  border-color: #2563eb;
  background: #f9fafb;
}

.file-input {
  display: none;
}

.file-label {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  color: #6b7280;
  font-size: 0.875rem;
}

.upload-icon {
  width: 48px;
  height: 48px;
  color: #9ca3af;
}

.delete-warning {
  font-size: 0.875rem;
  color: #6b7280;
  text-align: center;
}
</style>