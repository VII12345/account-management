"""
Facebook 发帖策略实现模块。

职责：封装 Facebook 发布内容相关的执行步骤与参数处理。
边界：仅关注发帖流程，不混入登录、搜索或互动聚合逻辑。
"""

from ..base import BaseStrategy
import asyncio

class Strategy(BaseStrategy):
    async def run(self, page, params, logs):
        content = params.get("content", "Hello World from RPA!")
        
        logs.append("-> [FB] 准备发布帖子...")

        # 1. 点击“创建帖子”入口
        # 源码中有 aria-label="创建帖子"
        # 还有 text="分享你的新鲜事吧！"
        create_post_triggers = [
            'div[aria-label="创建帖子"]',
            'span:has-text("分享你的新鲜事吧！")',
            'div[role="button"]:has-text("分享你的新鲜事吧")',
            'a[aria-label="创建帖子"]' # 侧边栏按钮
        ]
        
        trigger_found = False
        for sel in create_post_triggers:
            if await page.locator(sel).count() > 0:
                await page.locator(sel).first.click()
                trigger_found = True
                logs.append("-> 已点击发帖入口")
                break
        
        if not trigger_found:
            logs.append("❌ [FB] 未找到发帖按钮，请检查是否登录")
            return

        await page.wait_for_timeout(2000)

        # 2. 输入内容
        # 弹窗里的输入框通常是 div[role="textbox"]
        try:
            textbox = page.locator('div[role="textbox"][contenteditable="true"], div[aria-label^="分享你的新鲜事"]')
            await textbox.click()
            await textbox.fill(content)
            logs.append("-> 内容已填入")
            
            await page.wait_for_timeout(1000)

            # 3. 点击发布
            # 按钮通常叫 "发布" 或 "Post"
            post_btn = page.locator('div[aria-label="发布"], div[aria-label="Post"]')
            
            # 检查按钮是否可用 (有时候没输入内容是灰色的)
            if await post_btn.get_attribute("aria-disabled") == "true":
                logs.append("⚠️ 发帖按钮不可用，可能内容为空或被风控")
            else:
                await post_btn.click()
                logs.append("✅ [FB] 发布按钮已点击")
                
        except Exception as e:
            logs.append(f"❌ [FB] 发帖流程出错: {e}")

        await page.wait_for_timeout(3000)