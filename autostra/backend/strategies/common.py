import asyncio
from .base import BaseStrategy

class WaitStrategy(BaseStrategy):
    async def run(self, page, params, logs):
        ms = int(params.get('time', 1000))
        logs.append(f"⏳ [系统] 等待 {ms} 毫秒...")
        await page.wait_for_timeout(ms)

# 循环节点本身不需要执行任何浏览器操作，它只是一个逻辑标记
# 真正的循环控制是在 engine.py 里完成的，这里留空即可
class LoopStartStrategy(BaseStrategy):
    async def run(self, page, params, logs):
        count = params.get('loop_count', 1)
        logs.append(f"🔄 [系统] 触达循环节点 (设定次数: {count})")