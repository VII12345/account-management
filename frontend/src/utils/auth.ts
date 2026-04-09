/**
 * 文件注释：frontend/src/utils/auth.ts
 *
 * 职责：封装当前模块的初始化、常量、工具函数或组件逻辑。
 * 边界：仅承担本模块职责，不在此处定义跨模块业务规则。
 */

// src/utils/auth.ts
// 认证工具函数

const API_BASE_URL = '/api' // 根据实际后端地址调整

// Token 存储键名
const TOKEN_KEY = 'access_token'
const USER_KEY = 'user_info'

// 用户信息类型
export interface UserInfo {
    id: string
    email: string
}

// 登录响应类型
export interface LoginResponse {
    access_token: string
    user: UserInfo
}

// API 响应类型
export interface ApiResponse<T = any> {
    message?: string
    detail?: string
    data?: T
}

/**
 * 保存 Token 到本地存储
 */
export function setToken(token: string): void {
    localStorage.setItem(TOKEN_KEY, token)
}

/**
 * 获取 Token
 */
export function getToken(): string | null {
    return localStorage.getItem(TOKEN_KEY)
}

/**
 * 移除 Token
 */
export function removeToken(): void {
    localStorage.removeItem(TOKEN_KEY)
}

/**
 * 保存用户信息
 */
export function setUserInfo(user: UserInfo): void {
    localStorage.setItem(USER_KEY, JSON.stringify(user))
}

/**
 * 获取用户信息
 */
export function getUserInfo(): UserInfo | null {
    const userStr = localStorage.getItem(USER_KEY)
    if (userStr) {
        try {
            return JSON.parse(userStr)
        } catch {
            return null
        }
    }
    return null
}

/**
 * 移除用户信息
 */
export function removeUserInfo(): void {
    localStorage.removeItem(USER_KEY)
}

/**
 * 检查是否已登录
 */
export function isAuthenticated(): boolean {
    const token = getToken()
    return !!token
}

/**
 * 登出 - 清除所有认证信息
 */
export function logout(): void {
    removeToken()
    removeUserInfo()
}

/**
 * 登录 API
 */
export async function loginApi(email: string, password: string): Promise<LoginResponse> {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
    })

    if (!response.ok) {
        let errorMsg = '登录失败'
        try {
            const error = await response.json()
            errorMsg = error.detail || errorMsg
        } catch (e) {
            errorMsg = `服务器异常: ${response.status} ${response.statusText}`
        }
        throw new Error(errorMsg)
    }

    return response.json()
}

/**
 * 注册 API
 */
export async function registerApi(email: string, password: string): Promise<ApiResponse> {
    const response = await fetch(`${API_BASE_URL}/auth/register`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
    })

    if (!response.ok) {
        let errorMsg = '注册失败'
        try {
            const error = await response.json()
            errorMsg = error.detail || errorMsg
        } catch (e) {
            errorMsg = `服务器异常: ${response.status} ${response.statusText}`
        }
        throw new Error(errorMsg)
    }

    return response.json()
}

/**
 * 重置密码 API
 */
export async function resetPasswordApi(email: string, newPassword: string): Promise<ApiResponse> {
    const response = await fetch(`${API_BASE_URL}/auth/reset-password`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, new_password: newPassword }),
    })

    if (!response.ok) {
        let errorMsg = '重置密码失败'
        try {
            const error = await response.json()
            errorMsg = error.detail || errorMsg
        } catch (e) {
            errorMsg = `服务器异常: ${response.status} ${response.statusText}`
        }
        throw new Error(errorMsg)
    }

    return response.json()
}

/**
 * 带认证的 fetch 请求封装
 */
export async function authFetch(url: string, options: RequestInit = {}): Promise<Response> {
    const token = getToken()

    const headers = new Headers(options.headers)
    if (token) {
        headers.set('Authorization', `Bearer ${token}`)
    }

    return fetch(url, {
        ...options,
        headers,
    })
}
