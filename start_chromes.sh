#!/bin/bash

# 定义起始和结束端口
START_PORT=9220
END_PORT=9228

# 确保 chromeuser 有权限访问它自己的家目录
sudo chown -R chromeuser:chromeuser /home/chromeuser

echo "🚀 正在启动 9 个 Chromium 实例 (端口 $START_PORT - $END_PORT)..."

for port in $(seq $START_PORT $END_PORT)
do
    # 为每个实例指定独立的家目录，防止配置冲突
    USER_DATA_DIR="/home/chromeuser/chrome_data_$port"
    
    # 以后台运行模式启动
    sudo -u chromeuser nohup chromium \
        --headless \
        --no-sandbox \
        --remote-debugging-port=$port \
        --remote-debugging-address=0.0.0.0 \
        --user-data-dir="$USER_DATA_DIR" \
        --disable-gpu \
        --disable-dev-shm-usage \
        --blink-settings=imagesEnabled=false \
        --incognito > /dev/null 2>&1 &

    echo "✅ 端口 $port 启动指令已发出"
done

echo "🎉 全部启动任务已转入后台运行。"
echo "💡 输入 'ss -tunlp | grep chromium' 检查运行状态。"
