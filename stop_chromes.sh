#!/bin/bash

echo "🛑 正在尝试关闭 9220-9228 端口的 Chromium 实例..."

# 1. 杀死所有由 chromeuser 运行的进程
sudo pkill -u chromeuser chromium

# 2. 等待 2 秒确保进程完全退出
sleep 2

# 3. 检查是否还有残余进程
REMAINING=$(pgrep -u chromeuser chromium)

if [ -z "$REMAINING" ]; then
    echo "✅ 所有 Chromium 进程已成功关闭。"
else
    echo "⚠️ 仍有残余进程，正在尝试强制杀死..."
    sudo pkill -9 -u chromeuser chromium
    echo "💀 已执行强制清理。"
fi

# 4. 可选：清理缓存文件夹以节省磁盘空间（如果不需要保留登录状态的话）
# echo "🧹 正在清理临时数据目录..."
# rm -rf /home/chromeuser/chrome_data_*

echo "✨ 任务完成。"
