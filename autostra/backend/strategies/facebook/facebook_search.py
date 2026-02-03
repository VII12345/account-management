from ..base import BaseStrategy
import asyncio

class Strategy(BaseStrategy):
    async def run(self, page, params, logs):
        keyword = params.get("keyword", "OpenAI")
        
        # 1. 确保在 Facebook
        if "facebook.com" not in page.url:
            logs.append("-> [FB] 正在跳转首页...")
            await page.goto("https://www.facebook.com")
            await page.wait_for_timeout(3000)

        logs.append(f"-> [FB] 准备搜索: {keyword}")

        # 2. 定位搜索框
        # 策略：找 input[type="search"] 或者 aria-label="搜索 Facebook"
        # 你提供的源码里有 aria-label="搜索 Facebook"
        search_input = page.locator('input[type="search"], input[aria-label="搜索 Facebook"], input[placeholder="搜索 Facebook"]')
        
        try:
            # 有时候移动端视图需要先点击一个搜索图标才能看到输入框
            if not await search_input.is_visible():
                search_icon = page.locator('div[aria-label="搜索"], div[role="button"]:has(svg circle)')
                if await search_icon.count() > 0:
                    await search_icon.first.click()
                    await page.wait_for_timeout(1000)
            
            await search_input.click()
            await search_input.fill(keyword)
            await page.keyboard.press("Enter")
            
            logs.append("✅ [FB] 搜索指令已发送")
            
            # 等待结果加载 (检查 URL 变化或结果列表)
            try:
                await page.wait_for_url("**/search/**", timeout=5000)
                logs.append("-> 结果页面加载成功")
            except:
                pass
                
        except Exception as e:
            logs.append(f"❌ [FB] 搜索失败: {e}")

        await page.wait_for_timeout(2000)