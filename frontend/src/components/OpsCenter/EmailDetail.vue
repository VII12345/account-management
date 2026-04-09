<!--
  文件注释：frontend/src/components/OpsCenter/EmailDetail.vue

  职责：承载当前页面/组件的视图结构、交互事件与状态绑定。
  边界：仅处理前端展示与交互编排，不在此文件实现后端业务规则。
-->

<template>
  <div class="mailbox-management">
    <!-- 面包屑 -->
    <div class="breadcrumb">
      <span>运维中心</span>
      <span class="separator">›</span>
      <span class="active">邮箱管理</span>
    </div>

    <!-- 统计卡片区域 -->
    <div class="stats-grid">
      <!-- 邮箱国家分布 -->
      <div class="card">
        <h3 class="card-title">邮箱国家分布</h3>
        <div class="chart-container">
          <div class="empty-chart">
            <svg viewBox="0 0 100 100">
              <circle cx="50" cy="50" r="40" fill="none" stroke="#e0e0e0" stroke-width="20" />
            </svg>
          </div>
        </div>
      </div>

      <!-- 邮箱运行状态统计 -->
      <div class="card">
        <h3 class="card-title">邮箱运行状态统计</h3>
        <div class="status-main">
          <div class="status-number">{{ totalMailboxes }}</div>
          <div class="status-change">
            较昨日 <span class="red-dot">●</span> {{ changeRate }}%
          </div>
        </div>
        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: progressPercentage + '%' }"></div>
        </div>
        <div class="status-list">
          <div class="status-item">
            <span class="status-label">
              <span class="status-dot gray"></span>
              未启用邮箱
            </span>
            <span class="status-value">{{ unusedMailboxes }}</span>
          </div>
          <div class="status-item">
            <span class="status-label">
              <span class="status-dot green"></span>
              正常邮箱
            </span>
            <span class="status-value">{{ normalMailboxes }}</span>
          </div>
          <div class="status-item">
            <span class="status-label">
              <span class="status-dot orange"></span>
              异常邮箱
            </span>
            <span class="status-value">{{ abnormalMailboxes }}</span>
          </div>
          <div class="status-item">
            <span class="status-label">
              <span class="status-dot brown"></span>
              废弃邮箱
            </span>
            <span class="status-value">{{ discardedMailboxes }}</span>
          </div>
        </div>
      </div>

      <!-- 邮件接收状态统计 -->
      <div class="card">
        <div class="card-header-row">
          <h3 class="card-title">邮件接收状态统计</h3>
          <button class="refresh-btn" @click="handleRefresh">
            刷新 <span class="refresh-icon">🔄</span>
          </button>
        </div>
        <div class="receive-grid">
          <div class="receive-item">
            <div class="receive-label">今天</div>
            <div class="receive-value">{{ todayReceived }}</div>
            <div class="receive-compare">较昨天 持平</div>
          </div>
          <div class="receive-item">
            <div class="receive-label">昨天</div>
            <div class="receive-value">{{ yesterdayReceived }}</div>
          </div>
          <div class="receive-item">
            <div class="receive-label">本周</div>
            <div class="receive-value">{{ thisWeekReceived }}</div>
            <div class="receive-compare">较上周 持平</div>
          </div>
          <div class="receive-item">
            <div class="receive-label">上周</div>
            <div class="receive-value">{{ lastWeekReceived }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 已支持邮箱注册的平台 -->
    <div class="platform-card">
      <div class="platform-header">
        <h3>已支持邮箱注册的平台</h3>
        <a href="#" class="view-details">
          仔细看看 <span class="arrow">›</span>
        </a>
      </div>
    </div>

    <!-- 邮箱管理表格 -->
    <div class="table-card">
      <div class="table-header">
        <h3>邮箱管理</h3>
        <div class="header-actions">
          <button class="primary-btn" @click="openPOPDialog">邮箱POP管理</button>
          <button class="dropdown-btn" @click="openImportModal">
            导入 <span class="arrow-down">▼</span>
          </button>
          <button class="primary-btn" @click="openCreateModal">添加邮箱</button>
        </div>
      </div>

      <!-- 筛选栏 -->
      <div class="filter-bar">
        <div class="filter-item">
          <span class="filter-label">状态：</span>
          <select v-model="selectedStatus" class="filter-select-input">
            <option value="">全部</option>
            <option v-for="option in statusOptions" :key="option" :value="option">
              {{ getStatusText(option) }}
            </option>
          </select>
        </div>
        <div class="filter-item">
          <span class="filter-label">协议：</span>
          <select v-model="selectedProtocol" class="filter-select-input">
            <option value="">全部</option>
            <option v-for="option in protocolOptions" :key="option" :value="option">
              {{ option }}
            </option>
          </select>
        </div>
        <div class="spacer"></div>
        <div class="search-box">
          <input v-model="searchText" type="text" placeholder="搜索邮箱、主机、标签" />
          <span class="search-icon">🔍</span>
        </div>
        <button class="clear-filter" @click="handleClearFilters">清空筛选</button>
      </div>

      <!-- 表格 -->
      <div class="table-container">
        <div v-if="loading" class="loading-overlay">
          <div class="loading-spinner"></div>
          加载中...
        </div>
        <table>
          <thead>
            <tr>
              <th>
                <input v-model="selectAll" type="checkbox" @change="handleSelectAll" />
              </th>
              <th>ID</th>
              <th>状态</th>
              <th>邮箱地址</th>
              <th>密码</th>
              <th>协议</th>
              <th>主机</th>
              <th>端口</th>
              <th>标签</th>
              <th>创建时间</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="filteredMailboxes.length === 0">
              <td colspan="11" class="empty-data">暂无数据</td>
            </tr>
            <tr v-for="mailbox in filteredMailboxes" :key="mailbox.id">
              <td>
                <input v-model="selectedMailboxes" :value="mailbox.id" type="checkbox" />
              </td>
              <td>{{ mailbox.id }}</td>
              <td>
                <span class="status-badge" :class="getStatusClass(mailbox.status)">
                  <span class="badge-dot"></span>
                  {{ getStatusText(mailbox.status) }}
                </span>
              </td>
              <td>{{ mailbox.email }}</td>
              <td class="password-cell">
                <span class="password-hidden">••••••••</span>
              </td>
              <td>{{ mailbox.protocol || '-' }}</td>
              <td>{{ mailbox.host || '-' }}</td>
              <td>{{ mailbox.port || '-' }}</td>
              <td>{{ mailbox.tags || '-' }}</td>
              <td>{{ formatDate(mailbox.created_at) }}</td>
              <td>
                <div class="action-buttons">
                  <button @click="openEditModal(mailbox)" class="action-btn">编辑</button>
                  <button @click="openDeleteModal(mailbox.id)" class="action-btn action-btn-danger">删除</button>
                </div>
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
          <button class="page-btn" @click="handlePageChange(1)" :disabled="currentPage === 1">«</button>
          <button class="page-btn" @click="handlePageChange(currentPage - 1)" :disabled="currentPage === 1">‹</button>
          <span class="page-info">{{ currentPage }} / {{ totalPages || 1 }}</span>
          <button class="page-btn" @click="handlePageChange(currentPage + 1)" :disabled="currentPage >= totalPages">›</button>
          <button class="page-btn" @click="handlePageChange(totalPages)" :disabled="currentPage >= totalPages">»</button>
        </div>
      </div>
    </div>

    <!-- 创建/编辑邮箱弹窗 -->
    <div v-if="showModal" class="dialog-overlay" @click.self="closeModal">
      <div class="modal-content">
        <div class="dialog-header">
          <h2>{{ modalMode === 'create' ? '添加邮箱' : '编辑邮箱' }}</h2>
          <button class="close-btn" @click="closeModal">✕</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label class="form-label">邮箱地址 <span class="required">*</span></label>
            <input v-model="emailForm.email" type="email" class="form-input" placeholder="请输入邮箱地址" />
          </div>
          <div class="form-group">
            <label class="form-label">密码 <span class="required">*</span></label>
            <input v-model="emailForm.password" type="text" class="form-input" placeholder="请输入密码" />
          </div>
          <div class="form-group">
            <label class="form-label">协议</label>
            <select v-model="emailForm.protocol" class="form-input">
              <option value="">请选择</option>
              <option v-for="option in protocolOptions" :key="option" :value="option">{{ option }}</option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">主机地址</label>
            <input v-model="emailForm.host" type="text" class="form-input" placeholder="如: imap.gmail.com" />
          </div>
          <div class="form-group">
            <label class="form-label">端口</label>
            <input v-model="emailForm.port" type="number" class="form-input" placeholder="如: 993" />
          </div>
          <div class="form-group">
            <label class="form-label">状态</label>
            <select v-model="emailForm.status" class="form-input">
              <option v-for="option in statusOptions" :key="option" :value="option">{{ getStatusText(option) }}</option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">标签</label>
            <input v-model="emailForm.tags" type="text" class="form-input" placeholder="请输入标签，用逗号分隔" />
          </div>
        </div>
        <div class="modal-footer">
          <button class="footer-secondary-btn" @click="closeModal">取消</button>
          <button class="footer-primary-btn" @click="handleSubmit">
            {{ modalMode === 'create' ? '创建' : '保存' }}
          </button>
        </div>
      </div>
    </div>

    <!-- 批量导入弹窗 -->
    <div v-if="showImportModal" class="dialog-overlay" @click.self="closeImportModal">
      <div class="modal-content modal-large">
        <div class="dialog-header">
          <h2>批量导入邮箱</h2>
          <button class="close-btn" @click="closeImportModal">✕</button>
        </div>
        <div class="modal-body">
          <div class="import-tabs">
            <button class="import-tab" :class="{ active: importType === 'json' }" @click="importType = 'json'">
              JSON 导入
            </button>
            <button class="import-tab" :class="{ active: importType === 'csv' }" @click="importType = 'csv'">
              CSV 导入
            </button>
          </div>

          <div v-if="importType === 'json'" class="import-content">
            <p class="import-hint">
              请输入 JSON 数组格式的邮箱数据，每个邮箱包含以下字段：<br />
              <code>email</code>(必填), <code>password</code>(必填), 
              <code>protocol</code>, <code>host</code>, <code>port</code>, <code>status</code>, <code>tags</code>
            </p>
            <textarea 
              v-model="jsonInput" 
              class="json-textarea" 
              placeholder='[
  {
    "email": "test@gmail.com",
    "password": "password123",
    "protocol": "IMAP",
    "host": "imap.gmail.com",
    "port": 993,
    "status": "active",
    "tags": "测试"
  }
]'
            ></textarea>
          </div>

          <div v-if="importType === 'csv'" class="import-content">
            <p class="import-hint">
              请上传 CSV 文件，文件需要包含以下列标题：<br />
              <code>email</code>(必填), <code>password</code>(必填), 
              <code>protocol</code>, <code>host</code>, <code>port</code>, <code>status</code>, <code>tags</code>
            </p>
            <div class="file-upload">
              <input type="file" accept=".csv" @change="handleFileChange" id="csv-file" class="file-input" />
              <label for="csv-file" class="file-label">
                <span class="upload-icon">📁</span>
                {{ csvFile ? csvFile.name : '点击选择文件或拖拽文件到此处' }}
              </label>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="footer-secondary-btn" @click="closeImportModal">取消</button>
          <button class="footer-primary-btn" @click="handleImport" :disabled="importLoading">
            {{ importLoading ? '导入中...' : '开始导入' }}
          </button>
        </div>
      </div>
    </div>

    <!-- 删除确认弹窗 -->
    <div v-if="showDeleteModal" class="dialog-overlay" @click.self="showDeleteModal = false">
      <div class="modal-content modal-small">
        <div class="dialog-header">
          <h2>确认删除</h2>
          <button class="close-btn" @click="showDeleteModal = false">✕</button>
        </div>
        <div class="modal-body">
          <p class="delete-warning">确定要删除这个邮箱账号吗？此操作不可恢复。</p>
        </div>
        <div class="modal-footer">
          <button class="footer-secondary-btn" @click="showDeleteModal = false">取消</button>
          <button class="footer-danger-btn" @click="deleteEmailAccount">确认删除</button>
        </div>
      </div>
    </div>

    <!-- 邮箱POP配置弹窗 -->
    <div v-if="showPOPDialog" class="dialog-overlay" @click="closePOPDialog">
      <div class="pop-dialog-content" @click.stop>
        <div class="dialog-header">
          <h2>邮箱POP配置</h2>
          <button class="close-btn" @click="closePOPDialog">✕</button>
        </div>

        <div class="pop-dialog-body">
          <!-- Outlook 邮箱 -->
          <div class="config-section">
            <h3 class="config-title">Outlook 邮箱</h3>
            <div class="config-grid">
              <div class="config-row">
                <div class="config-label">地址</div>
                <div class="config-label">端口</div>
                <div class="config-label">加密</div>
              </div>
              <div class="config-row">
                <span class="row-label">IMAP</span>
                <input v-model="outlookConfig.imap.host" type="text" class="config-input" readonly />
                <input v-model="outlookConfig.imap.port" type="text" class="config-input" readonly />
                <input v-model="outlookConfig.imap.ssl" type="text" class="config-input" readonly />
              </div>
              <div class="config-row">
                <span class="row-label">SMTP</span>
                <input v-model="outlookConfig.smtp.host" type="text" class="config-input" readonly />
                <input v-model="outlookConfig.smtp.port" type="text" class="config-input" readonly />
                <input v-model="outlookConfig.smtp.ssl" type="text" class="config-input" readonly />
              </div>
              <div class="config-row">
                <span class="row-label">POP</span>
                <input v-model="outlookConfig.pop.host" type="text" class="config-input" readonly />
                <input v-model="outlookConfig.pop.port" type="text" class="config-input" readonly />
                <input v-model="outlookConfig.pop.ssl" type="text" class="config-input" readonly />
              </div>
            </div>
          </div>

          <!-- Gmail 邮箱 -->
          <div class="config-section">
            <h3 class="config-title">Gmail 邮箱</h3>
            <div class="config-grid">
              <div class="config-row">
                <div class="config-label">地址</div>
                <div class="config-label">端口</div>
                <div class="config-label">加密</div>
              </div>
              <div class="config-row">
                <span class="row-label">IMAP</span>
                <input v-model="gmailConfig.imap.host" type="text" class="config-input" placeholder="请输入" />
                <input v-model="gmailConfig.imap.port" type="text" class="config-input" placeholder="请输入" />
                <input v-model="gmailConfig.imap.ssl" type="text" class="config-input" placeholder="请输入" />
              </div>
              <div class="config-row">
                <span class="row-label">SMTP</span>
                <input v-model="gmailConfig.smtp.host" type="text" class="config-input" placeholder="请输入" />
                <input v-model="gmailConfig.smtp.port" type="text" class="config-input" placeholder="请输入" />
                <input v-model="gmailConfig.smtp.ssl" type="text" class="config-input" placeholder="请输入" />
              </div>
              <div class="config-row">
                <span class="row-label">POP</span>
                <input v-model="gmailConfig.pop.host" type="text" class="config-input" readonly />
                <input v-model="gmailConfig.pop.port" type="text" class="config-input" readonly />
                <input v-model="gmailConfig.pop.ssl" type="text" class="config-input" readonly />
              </div>
            </div>
          </div>

          <!-- Hotmail 邮箱 -->
          <div class="config-section">
            <h3 class="config-title">Hotmail 邮箱</h3>
            <div class="config-grid">
              <div class="config-row">
                <div class="config-label">地址</div>
                <div class="config-label">端口</div>
                <div class="config-label">加密</div>
              </div>
              <div class="config-row">
                <span class="row-label">IMAP</span>
                <input v-model="hotmailConfig.imap.host" type="text" class="config-input" placeholder="请输入" />
                <input v-model="hotmailConfig.imap.port" type="text" class="config-input" placeholder="请输入" />
                <input v-model="hotmailConfig.imap.ssl" type="text" class="config-input" placeholder="请输入" />
              </div>
              <div class="config-row">
                <span class="row-label">SMTP</span>
                <input v-model="hotmailConfig.smtp.host" type="text" class="config-input" placeholder="请输入" />
                <input v-model="hotmailConfig.smtp.port" type="text" class="config-input" placeholder="请输入" />
                <input v-model="hotmailConfig.smtp.ssl" type="text" class="config-input" placeholder="请输入" />
              </div>
              <div class="config-row">
                <span class="row-label">POP</span>
                <input v-model="hotmailConfig.pop.host" type="text" class="config-input" placeholder="请输入" />
                <input v-model="hotmailConfig.pop.port" type="text" class="config-input" placeholder="请输入" />
                <input v-model="hotmailConfig.pop.ssl" type="text" class="config-input" placeholder="请输入" />
              </div>
            </div>
          </div>
        </div>

        <div class="pop-dialog-footer">
          <button class="footer-secondary-btn" @click="closePOPDialog">关闭</button>
          <button class="footer-primary-btn" @click="handleSavePOP">编辑</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import { authFetch } from '../../utils/auth';

const API_BASE_URL = '/api';

// 类型定义
interface EmailAccount {
  id: number;
  email: string;
  password: string;
  protocol: string | null;
  host: string | null;
  port: number | null;
  status: string | null;
  created_at: string | null;
  tags: string | null;
}

interface EmailForm {
  email: string;
  password: string;
  protocol: string;
  host: string;
  port: string;
  status: string;
  tags: string;
}

// 响应式数据
const searchText = ref('');
const selectedMailboxes = ref<number[]>([]);
const loading = ref(false);
const currentPage = ref(1);
const pageSize = ref(20);
const totalRecords = ref(0);

// 筛选条件
const selectedStatus = ref('');
const selectedProtocol = ref('');

// 统计数据
const totalMailboxes = ref(0);
const changeRate = ref(0);
const progressPercentage = ref(100);
const unusedMailboxes = ref(0);
const normalMailboxes = ref(0);
const abnormalMailboxes = ref(0);
const discardedMailboxes = ref(0);

// 接收统计
const todayReceived = ref(0);
const yesterdayReceived = ref(0);
const thisWeekReceived = ref(0);
const lastWeekReceived = ref(0);

// 邮箱列表数据
const mailboxes = ref<EmailAccount[]>([]);

// 弹窗状态
const showModal = ref(false);
const modalMode = ref<'create' | 'edit'>('create');
const editingId = ref<number | null>(null);
const emailForm = ref<EmailForm>({
  email: '',
  password: '',
  protocol: '',
  host: '',
  port: '',
  status: 'active',
  tags: ''
});

// 导入弹窗
const showImportModal = ref(false);
const importType = ref<'json' | 'csv'>('json');
const jsonInput = ref('');
const csvFile = ref<File | null>(null);
const importLoading = ref(false);

// 删除确认弹窗
const showDeleteModal = ref(false);
const deletingId = ref<number | null>(null);

// 筛选选项
const statusOptions = ['active', 'inactive', 'error', 'disabled'];
const protocolOptions = ['IMAP', 'POP3', 'SMTP'];

// 计算总页数
const totalPages = computed(() => Math.ceil(totalRecords.value / pageSize.value));

// 计算属性：全选状态
const selectAll = computed({
  get: () => mailboxes.value.length > 0 && selectedMailboxes.value.length === mailboxes.value.length,
  set: () => {}
});

// 前端筛选
const filteredMailboxes = computed(() => {
  let data = mailboxes.value;
  if (searchText.value) {
    const keyword = searchText.value.toLowerCase();
    data = data.filter(item =>
      item.email.toLowerCase().includes(keyword) ||
      (item.host && item.host.toLowerCase().includes(keyword)) ||
      (item.tags && item.tags.toLowerCase().includes(keyword))
    );
  }
  if (selectedStatus.value) {
    data = data.filter(item => item.status === selectedStatus.value);
  }
  if (selectedProtocol.value) {
    data = data.filter(item => item.protocol === selectedProtocol.value);
  }
  return data;
});

// 获取邮箱列表
const fetchEmailAccounts = async (): Promise<void> => {
  loading.value = true;
  try {
    const response = await authFetch(
      `${API_BASE_URL}/email_accounts/?page=${currentPage.value}&page_size=${pageSize.value}`
    );
    if (response.ok) {
      const data = await response.json();
      // 后端返回数组格式 [id, email, password, protocol, host, port, status, created_at, tags]
      mailboxes.value = (data.data || []).map((row: any[]) => ({
        id: row[0],
        email: row[1],
        password: row[2],
        protocol: row[3],
        host: row[4],
        port: row[5],
        status: row[6],
        created_at: row[7],
        tags: row[8]
      }));
      totalRecords.value = data.total || 0;
      totalMailboxes.value = data.total || 0;
      updateStats();
    } else {
      console.error('获取邮箱列表失败');
    }
  } catch (error) {
    console.error('获取邮箱列表出错:', error);
  } finally {
    loading.value = false;
  }
};

// 更新统计数据
const updateStats = () => {
  normalMailboxes.value = mailboxes.value.filter(m => m.status === 'active').length;
  abnormalMailboxes.value = mailboxes.value.filter(m => m.status === 'error').length;
  unusedMailboxes.value = mailboxes.value.filter(m => m.status === 'inactive' || m.status === 'disabled').length;
  discardedMailboxes.value = mailboxes.value.filter(m => m.status === 'discarded').length;
  if (totalMailboxes.value > 0) {
    progressPercentage.value = (normalMailboxes.value / totalMailboxes.value) * 100;
  }
};

// 创建邮箱账号
const createEmailAccount = async (): Promise<void> => {
  try {
    const response = await authFetch(`${API_BASE_URL}/email_accounts/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: emailForm.value.email,
        password: emailForm.value.password,
        protocol: emailForm.value.protocol || null,
        host: emailForm.value.host || null,
        port: emailForm.value.port ? parseInt(emailForm.value.port) : null,
        status: emailForm.value.status || 'active',
        tags: emailForm.value.tags || null
      })
    });
    if (response.ok) {
      alert('邮箱账号创建成功');
      closeModal();
      fetchEmailAccounts();
    } else {
      const error = await response.json();
      alert(error.detail || '创建失败');
    }
  } catch (error) {
    console.error('创建邮箱账号出错:', error);
    alert('创建邮箱账号出错');
  }
};

// 更新邮箱账号
const updateEmailAccount = async (): Promise<void> => {
  if (!editingId.value) return;
  try {
    const response = await authFetch(`${API_BASE_URL}/email_accounts/${editingId.value}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: emailForm.value.email,
        password: emailForm.value.password,
        protocol: emailForm.value.protocol || null,
        host: emailForm.value.host || null,
        port: emailForm.value.port ? parseInt(emailForm.value.port) : null,
        status: emailForm.value.status || 'active',
        tags: emailForm.value.tags || null
      })
    });
    if (response.ok) {
      alert('邮箱账号更新成功');
      closeModal();
      fetchEmailAccounts();
    } else {
      const error = await response.json();
      alert(error.detail || '更新失败');
    }
  } catch (error) {
    console.error('更新邮箱账号出错:', error);
    alert('更新邮箱账号出错');
  }
};

// 删除邮箱账号
const deleteEmailAccount = async (): Promise<void> => {
  if (!deletingId.value) return;
  try {
    const response = await authFetch(`${API_BASE_URL}/email_accounts/${deletingId.value}`, {
      method: 'DELETE'
    });
    if (response.ok) {
      alert('邮箱账号删除成功');
      showDeleteModal.value = false;
      deletingId.value = null;
      fetchEmailAccounts();
    } else {
      const error = await response.json();
      alert(error.detail || '删除失败');
    }
  } catch (error) {
    console.error('删除邮箱账号出错:', error);
    alert('删除邮箱账号出错');
  }
};

// JSON 批量导入
const importJson = async (): Promise<void> => {
  if (!jsonInput.value.trim()) {
    alert('请输入 JSON 数据');
    return;
  }
  importLoading.value = true;
  try {
    const accounts = JSON.parse(jsonInput.value);
    if (!Array.isArray(accounts)) {
      alert('JSON 数据必须是数组格式');
      return;
    }
    const response = await authFetch(`${API_BASE_URL}/email_accounts/import/json`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(accounts)
    });
    if (response.ok) {
      const result = await response.json();
      alert(result.message || '导入成功');
      closeImportModal();
      fetchEmailAccounts();
    } else {
      const error = await response.json();
      alert(error.detail || '导入失败');
    }
  } catch (error) {
    console.error('JSON 导入出错:', error);
    alert('JSON 格式错误或导入出错');
  } finally {
    importLoading.value = false;
  }
};

// CSV 批量导入
const importCsv = async (): Promise<void> => {
  if (!csvFile.value) {
    alert('请选择 CSV 文件');
    return;
  }
  importLoading.value = true;
  try {
    const formData = new FormData();
    formData.append('file', csvFile.value);
    const response = await authFetch(`${API_BASE_URL}/email_accounts/import/csv`, {
      method: 'POST',
      body: formData
    });
    if (response.ok) {
      const result = await response.json();
      alert(result.message || '导入成功');
      closeImportModal();
      fetchEmailAccounts();
    } else {
      const error = await response.json();
      alert(error.detail || '导入失败');
    }
  } catch (error) {
    console.error('CSV 导入出错:', error);
    alert('CSV 导入出错');
  } finally {
    importLoading.value = false;
  }
};

// 处理导入
const handleImport = (): void => {
  if (importType.value === 'json') {
    importJson();
  } else {
    importCsv();
  }
};

// 处理 CSV 文件选择
const handleFileChange = (event: Event): void => {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files.length > 0) {
    csvFile.value = target.files[0] as File;
  }
};

// 打开创建弹窗
const openCreateModal = (): void => {
  modalMode.value = 'create';
  editingId.value = null;
  emailForm.value = {
    email: '',
    password: '',
    protocol: '',
    host: '',
    port: '',
    status: 'active',
    tags: ''
  };
  showModal.value = true;
};

// 打开编辑弹窗
const openEditModal = (account: EmailAccount): void => {
  modalMode.value = 'edit';
  editingId.value = account.id;
  emailForm.value = {
    email: account.email,
    password: account.password,
    protocol: account.protocol || '',
    host: account.host || '',
    port: account.port?.toString() || '',
    status: account.status || 'active',
    tags: account.tags || ''
  };
  showModal.value = true;
};

// 关闭弹窗
const closeModal = (): void => {
  showModal.value = false;
  editingId.value = null;
};

// 打开导入弹窗
const openImportModal = (): void => {
  importType.value = 'json';
  jsonInput.value = '';
  csvFile.value = null;
  showImportModal.value = true;
};

// 关闭导入弹窗
const closeImportModal = (): void => {
  showImportModal.value = false;
  jsonInput.value = '';
  csvFile.value = null;
};

// 打开删除确认弹窗
const openDeleteModal = (id: number): void => {
  deletingId.value = id;
  showDeleteModal.value = true;
};

// 提交表单
const handleSubmit = (): void => {
  if (!emailForm.value.email || !emailForm.value.password) {
    alert('邮箱地址和密码是必填项');
    return;
  }
  if (modalMode.value === 'create') {
    createEmailAccount();
  } else {
    updateEmailAccount();
  }
};

// 全选操作
const handleSelectAll = () => {
  if (selectedMailboxes.value.length === mailboxes.value.length) {
    selectedMailboxes.value = [];
  } else {
    selectedMailboxes.value = mailboxes.value.map(m => m.id);
  }
};

// 清空筛选
const handleClearFilters = (): void => {
  selectedStatus.value = '';
  selectedProtocol.value = '';
  searchText.value = '';
};

// 刷新数据
const handleRefresh = () => {
  fetchEmailAccounts();
};

// 分页切换
const handlePageChange = (page: number): void => {
  if (page < 1 || page > totalPages.value) return;
  currentPage.value = page;
};

// 格式化日期
const formatDate = (dateStr: string | null): string => {
  if (!dateStr) return '-';
  const date = new Date(dateStr);
  return date.toLocaleString('zh-CN');
};

// 获取状态显示文本
const getStatusText = (status: string | null): string => {
  const statusMap: Record<string, string> = {
    'active': '正常',
    'inactive': '未启用',
    'error': '异常',
    'disabled': '禁用',
    'discarded': '废弃'
  };
  return statusMap[status || ''] || status || '-';
};

// 获取状态样式类
const getStatusClass = (status: string | null): string => {
  const classMap: Record<string, string> = {
    'active': 'status-normal',
    'inactive': 'status-inactive',
    'error': 'status-error',
    'disabled': 'status-disabled',
    'discarded': 'status-discarded'
  };
  return classMap[status || ''] || '';
};

// POP配置弹窗
const showPOPDialog = ref(false);

const outlookConfig = ref({
  imap: { host: 'outlook.office365.com', port: '993', ssl: 'TLS' },
  smtp: { host: 'smtp-mail.outlook.com', port: '587', ssl: 'STARTTLS' },
  pop: { host: 'outlook.office365.com', port: '995', ssl: 'TLS' }
});

const gmailConfig = ref({
  imap: { host: 'imap.gmail.com', port: '993', ssl: 'TLS' },
  smtp: { host: 'smtp.gmail.com', port: '587', ssl: 'STARTTLS' },
  pop: { host: 'pop.gmail.com', port: '995', ssl: 'TLS' }
});

const hotmailConfig = ref({
  imap: { host: 'outlook.office365.com', port: '993', ssl: 'TLS' },
  smtp: { host: 'smtp-mail.outlook.com', port: '587', ssl: 'STARTTLS' },
  pop: { host: 'outlook.office365.com', port: '995', ssl: 'TLS' }
});

const openPOPDialog = () => {
  showPOPDialog.value = true;
};

const closePOPDialog = () => {
  showPOPDialog.value = false;
};

const handleSavePOP = () => {
  console.log('保存POP配置');
  closePOPDialog();
};

// 监听分页变化
watch([currentPage, pageSize], () => {
  fetchEmailAccounts();
});

// 组件挂载时获取数据
onMounted(() => {
  fetchEmailAccounts();
});
</script>

<style scoped>
.mailbox-management {
  min-height: 100vh;
  background-color: #f5f5f5;
  padding: 24px;
}

/* 面包屑 */
.breadcrumb {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #666;
  margin-bottom: 24px;
}

.breadcrumb .separator {
  color: #999;
}

.breadcrumb .active {
  color: #333;
}

/* 统计卡片区域 */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  margin-bottom: 24px;
}

.card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 24px;
}

.card-title {
  font-size: 16px;
  font-weight: 500;
  color: #333;
  margin: 0 0 24px 0;
}

.card-header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.card-header-row .card-title {
  margin: 0;
}

.refresh-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 4px 12px;
  border: none;
  background: none;
  color: #4B7BEC;
  font-size: 14px;
  cursor: pointer;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.refresh-btn:hover {
  background-color: #e6f0ff;
}

.refresh-icon {
  font-size: 12px;
}

/* 空饼图 */
.chart-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
}

.empty-chart {
  width: 160px;
  height: 160px;
}

.empty-chart svg {
  width: 100%;
  height: 100%;
  transform: rotate(-90deg);
}

/* 运行状态统计 */
.status-main {
  text-align: center;
  margin-bottom: 16px;
}

.status-number {
  font-size: 48px;
  font-weight: 700;
  color: #333;
  line-height: 1;
}

.status-change {
  font-size: 14px;
  color: #666;
  margin-top: 8px;
}

.red-dot {
  color: #e74c3c;
  font-size: 12px;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background-color: #e8e8e8;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 20px;
}

.progress-fill {
  height: 100%;
  background-color: #2ecc71;
  transition: width 0.3s;
}

.status-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.status-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 14px;
}

.status-label {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #666;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.status-dot.gray {
  background-color: #999;
}

.status-dot.green {
  background-color: #2ecc71;
}

.status-dot.orange {
  background-color: #f39c12;
}

.status-dot.brown {
  background-color: #8b4513;
}

.status-value {
  font-weight: 600;
  color: #333;
}

/* 接收统计 */
.receive-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.receive-item {
  background-color: #f5f5f5;
  padding: 16px;
  border-radius: 8px;
}

.receive-label {
  font-size: 14px;
  color: #666;
  margin-bottom: 8px;
}

.receive-value {
  font-size: 32px;
  font-weight: 700;
  color: #333;
  margin-bottom: 4px;
}

.receive-compare {
  font-size: 12px;
  color: #999;
}

/* 平台卡片 */
.platform-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 24px;
  margin-bottom: 24px;
}

.platform-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.platform-header h3 {
  font-size: 16px;
  font-weight: 500;
  color: #333;
  margin: 0;
}

.view-details {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
  color: #666;
  text-decoration: none;
  transition: color 0.3s;
}

.view-details:hover {
  color: #4B7BEC;
}

.view-details .arrow {
  font-size: 16px;
}

/* 表格卡片 */
.table-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px;
  border-bottom: 1px solid #e8e8e8;
}

.table-header h3 {
  font-size: 18px;
  font-weight: 500;
  color: #333;
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.primary-btn {
  padding: 8px 16px;
  background-color: #4B7BEC;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.primary-btn:hover {
  background-color: #3867D6;
}

.dropdown-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border: 1px solid #d9d9d9;
  background: white;
  border-radius: 4px;
  font-size: 14px;
  color: #333;
  cursor: pointer;
  transition: border-color 0.3s;
}

.dropdown-btn:hover {
  border-color: #4B7BEC;
  color: #4B7BEC;
}

.arrow-down {
  font-size: 10px;
}

/* 筛选栏 */
.filter-bar {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 24px;
  border-bottom: 1px solid #e8e8e8;
}

.filter-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-label {
  font-size: 14px;
  color: #666;
}

.filter-select {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  background: white;
  font-size: 14px;
  color: #666;
  cursor: pointer;
  transition: border-color 0.3s;
}

.filter-select:hover {
  border-color: #999;
}

.filter-select .arrow {
  font-size: 10px;
  color: #999;
}

.spacer {
  flex: 1;
}

.search-box {
  position: relative;
  width: 256px;
}

.search-box input {
  width: 100%;
  padding: 6px 32px 6px 12px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.3s;
}

.search-box input:focus {
  border-color: #4B7BEC;
}

.search-icon {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #999;
  font-size: 14px;
}

.clear-filter {
  padding: 6px 16px;
  border: none;
  background: none;
  color: #4B7BEC;
  font-size: 14px;
  cursor: pointer;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.clear-filter:hover {
  background-color: #e6f0ff;
}

/* 表格 */
.table-container {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  background-color: #fafafa;
}

th {
  padding: 16px 24px;
  text-align: left;
  font-size: 14px;
  font-weight: 500;
  color: #333;
}

tbody tr {
  border-bottom: 1px solid #f0f0f0;
  transition: background-color 0.3s;
}

tbody tr:hover {
  background-color: #fafafa;
}

td {
  padding: 16px 24px;
  font-size: 14px;
  color: #666;
}

/* 状态徽章 */
.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 13px;
}

.status-badge.status-normal {
  background-color: #e8f5e9;
  color: #2ecc71;
}

.badge-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background-color: currentColor;
}

/* 操作按钮 */
.action-buttons {
  display: flex;
  align-items: center;
  gap: 12px;
}

.action-btn {
  border: none;
  background: none;
  color: #4B7BEC;
  font-size: 14px;
  cursor: pointer;
  padding: 0;
  transition: color 0.3s;
}

.action-btn:hover {
  color: #3867D6;
}

/* 复选框样式 */
input[type="checkbox"] {
  width: 16px;
  height: 16px;
  cursor: pointer;
}

/* POP配置弹窗样式 */
.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.pop-dialog-content {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 900px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid #e8e8e8;
}

.dialog-header h2 {
  font-size: 18px;
  font-weight: 500;
  color: #333;
  margin: 0;
}

.close-btn {
  width: 32px;
  height: 32px;
  border: none;
  background: none;
  font-size: 20px;
  color: #999;
  cursor: pointer;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.close-btn:hover {
  background-color: #f5f5f5;
  color: #666;
}

.pop-dialog-body {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
}

.config-section {
  margin-bottom: 32px;
}

.config-section:last-child {
  margin-bottom: 0;
}

.config-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin: 0 0 16px 0;
}

.config-grid {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.config-row {
  display: grid;
  grid-template-columns: 80px 1fr 1fr 1fr;
  gap: 12px;
  align-items: center;
}

.config-row:first-child {
  margin-bottom: 4px;
}

.config-label {
  font-size: 14px;
  font-weight: 500;
  color: #4B7BEC;
  text-align: center;
}

.row-label {
  font-size: 14px;
  font-weight: 500;
  color: #333;
}

.config-input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  font-size: 14px;
  color: #333;
  background-color: white;
  outline: none;
  transition: border-color 0.3s;
}

.config-input:focus {
  border-color: #4B7BEC;
}

.config-input:read-only {
  background-color: #f5f5f5;
  color: #999;
  cursor: not-allowed;
}

.config-input::placeholder {
  color: #bbb;
}

.pop-dialog-footer {
  display: flex;
  justify-content: center;
  gap: 12px;
  padding: 20px 24px;
  border-top: 1px solid #e8e8e8;
}

.footer-secondary-btn {
  padding: 8px 32px;
  border: 1px solid #d9d9d9;
  background: white;
  border-radius: 4px;
  font-size: 14px;
  color: #666;
  cursor: pointer;
  transition: all 0.3s;
}

.footer-secondary-btn:hover {
  border-color: #4B7BEC;
  color: #4B7BEC;
}

.footer-primary-btn {
  padding: 8px 32px;
  border: none;
  background: #4B7BEC;
  color: white;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.footer-primary-btn:hover {
  background: #3867D6;
}

.footer-primary-btn:disabled {
  background: #93c5fd;
  cursor: not-allowed;
}

/* 新增样式 */
.filter-select-input {
  padding: 6px 12px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  font-size: 14px;
  outline: none;
  min-width: 120px;
}

.filter-select-input:focus {
  border-color: #4B7BEC;
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
  gap: 8px;
  z-index: 10;
}

.loading-spinner {
  width: 32px;
  height: 32px;
  border: 3px solid #e5e7eb;
  border-top-color: #4B7BEC;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.empty-data {
  text-align: center;
  padding: 48px 16px !important;
  color: #9ca3af;
}

.password-cell .password-hidden {
  font-family: monospace;
  letter-spacing: 2px;
}

.action-btn-danger {
  color: #dc2626 !important;
}

.action-btn-danger:hover {
  color: #b91c1c !important;
}

/* 分页样式 */
.pagination {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  border-top: 1px solid #e8e8e8;
}

.pagination-info {
  font-size: 14px;
  color: #666;
}

.pagination-controls {
  display: flex;
  align-items: center;
  gap: 8px;
}

.page-size-select {
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  padding: 6px 8px;
  font-size: 14px;
  outline: none;
}

.page-btn {
  min-width: 32px;
  height: 32px;
  border: 1px solid #d9d9d9;
  background: white;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.page-btn:hover:not(:disabled) {
  border-color: #4B7BEC;
  color: #4B7BEC;
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  font-size: 14px;
  color: #333;
  padding: 0 8px;
}

/* 弹窗样式 */
.modal-content {
  background: white;
  border-radius: 8px;
  width: 100%;
  max-width: 500px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.modal-large {
  max-width: 640px;
}

.modal-small {
  max-width: 400px;
}

.modal-body {
  padding: 24px;
  overflow-y: auto;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 16px 24px;
  border-top: 1px solid #e8e8e8;
}

/* 表单样式 */
.form-group {
  margin-bottom: 16px;
}

.form-label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: #333;
  margin-bottom: 8px;
}

.required {
  color: #dc2626;
}

.form-input {
  width: 100%;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  padding: 8px 12px;
  font-size: 14px;
  outline: none;
}

.form-input:focus {
  border-color: #4B7BEC;
  box-shadow: 0 0 0 3px rgba(75, 123, 236, 0.1);
}

/* 导入弹窗样式 */
.import-tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
}

.import-tab {
  flex: 1;
  padding: 12px;
  border: 1px solid #d9d9d9;
  background: white;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

.import-tab.active {
  background: #4B7BEC;
  color: white;
  border-color: #4B7BEC;
}

.import-tab:not(.active):hover {
  background: #f5f5f5;
}

.import-content {
  margin-top: 16px;
}

.import-hint {
  font-size: 14px;
  color: #666;
  margin-bottom: 16px;
  line-height: 1.6;
}

.import-hint code {
  background: #f3f4f6;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 13px;
}

.json-textarea {
  width: 100%;
  min-height: 200px;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  padding: 12px;
  font-family: monospace;
  font-size: 14px;
  resize: vertical;
  outline: none;
}

.json-textarea:focus {
  border-color: #4B7BEC;
}

.file-upload {
  border: 2px dashed #d9d9d9;
  border-radius: 8px;
  padding: 32px;
  text-align: center;
  transition: all 0.2s;
}

.file-upload:hover {
  border-color: #4B7BEC;
  background: #f9fafb;
}

.file-input {
  display: none;
}

.file-label {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  color: #666;
  font-size: 14px;
}

.upload-icon {
  font-size: 32px;
}

.delete-warning {
  font-size: 14px;
  color: #666;
  text-align: center;
}

.footer-danger-btn {
  padding: 8px 32px;
  border: none;
  background: #dc2626;
  color: white;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.footer-danger-btn:hover {
  background: #b91c1c;
}

/* 状态样式 */
.status-badge.status-inactive {
  background-color: #f3f4f6;
  color: #6b7280;
}

.status-badge.status-error {
  background-color: #fee2e2;
  color: #dc2626;
}

.status-badge.status-disabled {
  background-color: #fef3c7;
  color: #d97706;
}

.status-badge.status-discarded {
  background-color: #fecaca;
  color: #991b1b;
}

.table-container {
  overflow-x: auto;
  position: relative;
}
</style>    