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