from ..base import BaseStrategy
import asyncio
from pathlib import Path
from lib import HumanMouse

_MODEL_PATH = Path(__file__).resolve().parents[2] / "mouse.onnx"
_HUMAN_MOUSE = HumanMouse(model_path=_MODEL_PATH)

class Strategy(BaseStrategy):
    async def run(self, page, params, logs):
        keyword = params.get("keyword", "Python教程")
        
        # 1. 确保在 YouTube
        if "youtube.com" not in page.url:
            logs.append("-> [YouTube] 正在跳转首页...")
            await page.goto("https://www.youtube.com")
        
        # 2. 处理可能出现的 "Before you continue" Cookie 弹窗 (欧盟地区常见)
        try:
            consent_btn = page.locator('button[aria-label="Accept all"]')
            if await consent_btn.is_visible():
                element = await consent_btn.element_handle()
                if element:
                    await _HUMAN_MOUSE.click_element(page, element)
                    logs.append("-> [YouTube] 已处理 Cookie 同意弹窗")
        except:
            pass

        logs.append(f"-> [YouTube] 正在搜索: {keyword}")

        # 3. 输入搜索词
        # 桌面端通用选择器: input[name="search_query"]
        await self.smart_fill(page, 'input[name="search_query"]', keyword)
        
        # 4. 点击搜索图标或回车
        await page.keyboard.press("Enter")
        
        # 5. 等待结果加载 (等待第一个视频标题出现)
        try:
            await page.wait_for_selector('ytd-video-renderer #video-title', timeout=5000)
            logs.append("✅ [YouTube] 搜索结果已加载")
        except:
            logs.append("⚠️ [YouTube] 等待结果超时，可能已加载或网络慢")
            
        await page.wait_for_timeout(2000)
