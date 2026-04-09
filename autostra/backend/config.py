"""
自动化子系统后端配置模块。

职责：集中读取环境变量并提供运行时可用的配置常量，避免业务代码散落解析逻辑。
边界：仅负责配置值定义与默认值，不承担数据库连接、服务启动或任务执行。
"""

import os
import sys
import io

def setup_env():
    # --- 代理设置 (防止连接本地浏览器被拦截) ---
    os.environ["http_proxy"] = ""
    os.environ["https_proxy"] = ""
    os.environ["all_proxy"] = ""
    os.environ["no_proxy"] = "localhost,127.0.0.1,::1"

    # --- 强制 UTF-8 输出 ---
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 全局配置
CDP_URL_DEFAULT = "http://127.0.0.1:9222"
# VIEWPORT = {"width": 1920, "height": 1080}