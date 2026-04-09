"""
Facebook 点赞策略实现模块。

职责：定义 Facebook 场景下的点赞动作流程、步骤衔接与失败处理。
边界：仅聚焦点赞任务，不承担搜索、发帖等其他场景。
"""

from ..base import BaseStrategy
import asyncio
import random

class Strategy(BaseStrategy):
    async def run(self, page, params, logs):
        action = params.get("action_type", "like") # like / comment
        
        logs.append(f"-> [FB] 准备执行互动: {action}")

        # 1. 寻找信息流中的帖子
        # FB 帖子的容器通常有 role="article"
        try:
            await page.wait_for_selector('div[role="article"]', timeout=8000)
        except:
            logs.append("⚠️ 未找到帖子，尝试滚动加载...")
            await page.mouse.wheel(0, 500)
            await page.wait_for_timeout(2000)

        # 2. 获取所有帖子句柄
        posts = await page.locator('div[role="article"]').all()
        if not posts:
            logs.append("❌ [FB] 页面上没有可见的帖子")
            return
        
        # 随机选一个帖子 (前 3 个)
        target_post = random.choice(posts[:3])
        await target_post.scroll_into_view_if_needed()
        await page.wait_for_timeout(1000)

        # ==========================================
        # 👍 点赞逻辑
        # ==========================================
        if action == "like":
            # 在该帖子内部寻找点赞按钮
            # 按钮通常有 aria-label="赞" 或 "Like"
            like_btn = target_post.locator('div[aria-label="赞"], div[aria-label="Like"], div[aria-label="移除赞"]')
            
            if await like_btn.count() > 0:
                # 检查状态
                label = await like_btn.get_attribute("aria-label")
                if "移除" in label or "Remove" in label:
                    logs.append("ℹ️ [FB] 该帖子已经点过赞了")
                else:
                    await like_btn.click()
                    logs.append("✅ [FB] 点赞成功")
            else:
                logs.append("❌ 未在该帖子中找到点赞按钮")

        # ==========================================
        # 💬 评论逻辑 (简单版)
        # ==========================================
        elif action == "comment":
            comment_text = params.get("comment", "Great post! 👍")
            
            # 寻找评论按钮 aria-label="评论"
            comment_btn = target_post.locator('div[aria-label="评论"], div[aria-label="Comment"]')
            
            if await comment_btn.count() > 0:
                await comment_btn.click()
                await page.wait_for_timeout(1000)
                
                # 寻找输入框
                try:
                    # 评论框通常也是 role="textbox"
                    input_box = page.locator('div[role="textbox"][contenteditable="true"]').first
                    await input_box.fill(comment_text)
                    await page.keyboard.press("Enter")
                    logs.append("✅ [FB] 评论已发送")
                except:
                    logs.append("❌ 无法定位评论输入框")
            else:
                logs.append("❌ 未找到评论按钮")