<!--
  文件注释：frontend/src/components/Login.vue

  职责：承载当前页面/组件的视图结构、交互事件与状态绑定。
  边界：仅处理前端展示与交互编排，不在此文件实现后端业务规则。
-->

<script setup lang="ts">
import { reactive, ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { loginApi, registerApi, resetPasswordApi, setToken, setUserInfo } from '../utils/auth';

// --- 类型定义 ---
type ViewState = 'login' | 'register' | 'forgot';

interface LoginForm {
  email: string;
  password: string;
}

interface RegisterForm {
  username: string;
  email: string;
  password: string;
  confirmPassword: string;
}

interface ForgotForm {
  email: string;
}

// --- 状态管理 ---
const router = useRouter();
const currentView = ref<ViewState>('login');
const isLoading = ref(false);

// 表单数据
const loginForm = reactive<LoginForm>({ email: '', password: '' });
const registerForm = reactive<RegisterForm>({ username: '', email: '', password: '', confirmPassword: '' });
const forgotForm = reactive<ForgotForm>({ email: '' });

// 错误信息状态
const errors = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
});

// --- 辅助函数 ---
const clearErrors = () => {
  errors.username = '';
  errors.email = '';
  errors.password = '';
  errors.confirmPassword = '';
};

const switchView = (view: ViewState) => {
  clearErrors();
  currentView.value = view;
};

// --- 提交处理 ---

// 1. 登录逻辑
const handleLogin = async () => {
  clearErrors();
  if (!loginForm.email) errors.email = '请输入邮箱';
  if (!loginForm.password) errors.password = '请输入密码';
  if (errors.email || errors.password) return;

  isLoading.value = true;
  try {
    const response = await loginApi(loginForm.email, loginForm.password);
    // 保存 token 和用户信息
    setToken(response.access_token);
    setUserInfo(response.user);
    // 跳转到原目标页面或首页
    const redirect = router.currentRoute.value.query.redirect as string;
    router.push(redirect || '/');
  } catch (error: any) {
    errors.password = error.response?.data?.detail || error.message || '登录失败，请检查账号密码';
  } finally {
    isLoading.value = false;
  }
};

// 2. 注册逻辑
const handleRegister = async () => {
  clearErrors();
  let isValid = true;
  if (!registerForm.username) { errors.username = '请输入用户名'; isValid = false; }
  if (!registerForm.email.includes('@')) { errors.email = '请输入有效的邮箱'; isValid = false; }
  if (registerForm.password.length < 6) { errors.password = '密码至少6位'; isValid = false; }
  if (registerForm.password !== registerForm.confirmPassword) {
    errors.confirmPassword = '两次输入的密码不一致';
    isValid = false;
  }

  if (!isValid) return;

  isLoading.value = true;
  try {
    await registerApi(registerForm.email, registerForm.password);
    alert('注册成功，请登录');
    switchView('login'); // 注册成功跳回登录
  } catch (error: any) {
    errors.email = error.response?.data?.detail || error.message || '注册失败';
  } finally {
    isLoading.value = false;
  }
};

// 新密码输入
const newPassword = ref('');

// 3. 忘记密码逻辑
const handleForgot = async () => {
  clearErrors();
  if (!forgotForm.email.includes('@')) {
    errors.email = '请输入有效的邮箱地址';
    return;
  }
  if (!newPassword.value || newPassword.value.length < 6) {
    errors.password = '新密码至少6位';
    return;
  }

  isLoading.value = true;
  try {
    await resetPasswordApi(forgotForm.email, newPassword.value);
    alert('密码已重置，请使用新密码登录');
    switchView('login');
  } catch (error: any) {
    errors.email = error.response?.data?.detail || error.message || '重置密码失败';
  } finally {
    isLoading.value = false;
  }
};

// 动态标题
const title = computed(() => {
  switch (currentView.value) {
    case 'login': return 'Welcome Back';
    case 'register': return 'Create Account';
    case 'forgot': return 'Reset Password';
  }
});

const subtitle = computed(() => {
  switch (currentView.value) {
    case 'login': return '请输入您的账号密码登录';
    case 'register': return '填写以下信息完成注册';
    case 'forgot': return '我们将向您的邮箱发送重置链接';
  }
});
</script>

<template>
  <div class="auth-container">
    <!-- 背景装饰 -->
    <div class="circle circle-1"></div>
    <div class="circle circle-2"></div>

    <div class="auth-card">
      <div class="card-header">
        <h1>{{ title }}</h1>
        <p>{{ subtitle }}</p>
      </div>

      <!-- 使用 Transition 实现切换动画 -->
      <Transition name="fade" mode="out-in">

        <!-- 1. 登录表单 -->
        <form v-if="currentView === 'login'" @submit.prevent="handleLogin" class="auth-form">
          <div class="form-group">
            <label>邮箱</label>
            <div class="input-wrapper" :class="{ 'has-error': errors.email }">
              <input type="email" v-model="loginForm.email" placeholder="user@example.com" />
            </div>
            <span class="error-msg">{{ errors.email }}</span>
          </div>

          <div class="form-group">
            <label>密码</label>
            <div class="input-wrapper" :class="{ 'has-error': errors.password }">
              <input type="password" v-model="loginForm.password" placeholder="••••••••" />
            </div>
            <span class="error-msg">{{ errors.password }}</span>
          </div>

          <div class="form-actions space-between">
            <!-- <label class="checkbox-wrapper">
              <input type="checkbox"> <span>记住我</span>
            </label> -->
            <a href="#" @click.prevent="switchView('forgot')" class="link-btn">忘记密码?</a>
          </div>

          <button type="submit" class="submit-btn" :disabled="isLoading">
            {{ isLoading ? 'Loading...' : '立即登录' }}
          </button>

          <div class="card-footer">
            <p>还没有账号? <a href="#" @click.prevent="switchView('register')">立即注册</a></p>
          </div>
        </form>

        <!-- 2. 注册表单 -->
        <form v-else-if="currentView === 'register'" @submit.prevent="handleRegister" class="auth-form">
          <div class="form-group">
            <label>用户名</label>
            <div class="input-wrapper" :class="{ 'has-error': errors.username }">
              <input type="text" v-model="registerForm.username" placeholder="Your Name" />
            </div>
            <span class="error-msg">{{ errors.username }}</span>
          </div>

          <div class="form-group">
            <label>邮箱</label>
            <div class="input-wrapper" :class="{ 'has-error': errors.email }">
              <input type="email" v-model="registerForm.email" placeholder="name@company.com" />
            </div>
            <span class="error-msg">{{ errors.email }}</span>
          </div>

          <div class="form-group">
            <label>密码</label>
            <div class="input-wrapper" :class="{ 'has-error': errors.password }">
              <input type="password" v-model="registerForm.password" placeholder="••••••••" />
            </div>
            <span class="error-msg">{{ errors.password }}</span>
          </div>

          <div class="form-group">
            <label>确认密码</label>
            <div class="input-wrapper" :class="{ 'has-error': errors.confirmPassword }">
              <input type="password" v-model="registerForm.confirmPassword" placeholder="••••••••" />
            </div>
            <span class="error-msg">{{ errors.confirmPassword }}</span>
          </div>

          <button type="submit" class="submit-btn" :disabled="isLoading">
            {{ isLoading ? 'Processing...' : '注册账号' }}
          </button>

          <div class="card-footer">
            <p>已有账号? <a href="#" @click.prevent="switchView('login')">去登录</a></p>
          </div>
        </form>

        <!-- 3. 忘记密码表单 -->
        <form v-else-if="currentView === 'forgot'" @submit.prevent="handleForgot" class="auth-form">
          <div class="form-group">
            <label>注册邮箱</label>
            <div class="input-wrapper" :class="{ 'has-error': errors.email }">
              <input type="email" v-model="forgotForm.email" placeholder="name@company.com" />
            </div>
            <span class="error-msg">{{ errors.email }}</span>
          </div>

          <div class="form-group">
            <label>新密码</label>
            <div class="input-wrapper" :class="{ 'has-error': errors.password }">
              <input type="password" v-model="newPassword" placeholder="输入新密码（至少6位）" />
            </div>
            <span class="error-msg">{{ errors.password }}</span>
          </div>

          <button type="submit" class="submit-btn" :disabled="isLoading">
            {{ isLoading ? '重置中...' : '重置密码' }}
          </button>

          <div class="card-footer">
            <a href="#" @click.prevent="switchView('login')" class="back-link">
              ← 返回登录
            </a>
          </div>
        </form>

      </Transition>
    </div>
  </div>
</template>

<style scoped>
/* --- 全局布局与背景 (复用之前风格) --- */
.auth-container {
  min-height: 100vh;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  position: relative;
  overflow: hidden;
  font-family: 'Inter', sans-serif;
}

/* 装饰球 */
.circle {
  position: absolute;
  border-radius: 50%;
  filter: blur(60px);
  z-index: 0;
  animation: float 10s infinite ease-in-out;
}

.circle-1 {
  width: 300px;
  height: 300px;
  background: rgba(99, 102, 241, 0.4);
  top: -50px;
  left: -50px;
}

.circle-2 {
  width: 250px;
  height: 250px;
  background: rgba(236, 72, 153, 0.4);
  bottom: -50px;
  right: -50px;
  animation-delay: -5s;
}

@keyframes float {

  0%,
  100% {
    transform: translate(0, 0);
  }

  50% {
    transform: translate(30px, 20px);
  }
}

/* --- 卡片主体 --- */
.auth-card {
  width: 100%;
  max-width: 400px;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.5);
  border-radius: 24px;
  padding: 40px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  z-index: 1;
  /* 确保切换内容时卡片高度平滑变化（可选） */
  transition: all 0.3s ease;
}

/* Header */
.card-header {
  text-align: center;
  margin-bottom: 30px;
}

.card-header h1 {
  font-size: 26px;
  color: #1f2937;
  margin-bottom: 8px;
  font-weight: 700;
}

.card-header p {
  color: #6b7280;
  font-size: 14px;
}

/* 表单通用 */
.form-group {
  margin-bottom: 18px;
}

.form-group label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 6px;
}

.input-wrapper {
  background: #f9fafb;
  border: 2px solid transparent;
  border-radius: 10px;
  transition: all 0.3s ease;
}

.input-wrapper:focus-within {
  background: #fff;
  border-color: #6366f1;
  box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.1);
}

.input-wrapper.has-error {
  border-color: #ef4444;
  background: #fef2f2;
}

.input-wrapper input {
  width: 100%;
  padding: 12px;
  border: none;
  background: transparent;
  outline: none;
  font-size: 14px;
  color: #1f2937;
  box-sizing: border-box;
  /* 关键修正 */
}

.error-msg {
  color: #ef4444;
  font-size: 12px;
  margin-top: 4px;
  display: block;
  min-height: 18px;
}

/* 底部操作区 */
.form-actions {
  display: flex;
  align-items: center;
  margin-bottom: 24px;
  font-size: 13px;
}

.space-between {
  justify-content: space-between;
}

.checkbox-wrapper {
  display: flex;
  align-items: center;
  cursor: pointer;
  color: #4b5563;
}

.checkbox-wrapper input {
  margin-right: 8px;
  accent-color: #6366f1;
}

.link-btn {
  color: #6366f1;
  text-decoration: none;
  font-weight: 500;
}

.link-btn:hover {
  text-decoration: underline;
}

/* 按钮 */
.submit-btn {
  width: 100%;
  padding: 12px;
  background: linear-gradient(to right, #6366f1, #8b5cf6);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
}

.submit-btn:disabled {
  opacity: 0.7;
  cursor: wait;
}

/* 底部切换链接 */
.card-footer {
  margin-top: 20px;
  text-align: center;
  font-size: 13px;
  color: #6b7280;
}

.card-footer a {
  color: #6366f1;
  font-weight: 600;
  text-decoration: none;
}

.card-footer a:hover {
  text-decoration: underline;
}

.back-link {
  display: inline-block;
  margin-top: 10px;
  color: #6b7280 !important;
}

.back-link:hover {
  color: #1f2937 !important;
}

/* --- 动画效果 --- */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.fade-enter-from {
  opacity: 0;
  transform: translateX(10px);
}

.fade-leave-to {
  opacity: 0;
  transform: translateX(-10px);
}
</style>