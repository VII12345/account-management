import random
from ..base import BaseStrategy


class Strategy(BaseStrategy):
    async def run(self, page, params, logs):
        # 1. 确保在推特页面
        if "x.com" not in page.url:
            logs.append("-> [推特点赞] 当前不在推特，正在跳转...")
            await page.goto("https://x.com/home")
            await page.wait_for_timeout(3000)  # 等待加载

        logs.append("-> [推特点赞] 正在寻找推文...")

        # 2. 等待推文加载
        try:
            await page.wait_for_selector('article[data-testid="tweet"]', timeout=10000)
        except:
            logs.append("❌ [推特点赞] 错误: 未找到推文，请检查是否已登录")
            return

        # 3. 获取当前视图内所有可见的推文
        tweets = await page.locator('article[data-testid="tweet"]').all()

        if not tweets:
            logs.append("❌ [推特点赞] 未找到可见推文")
            return

        # 4. 随机选一个
        target_tweet = random.choice(tweets)
        await target_tweet.scroll_into_view_if_needed()
        await page.wait_for_timeout(500)

        # 5. 寻找点赞按钮 (data-testid="like")
        # 如果是 "unlike" 说明已经点赞过了
        like_btn = target_tweet.locator('[data-testid="like"]')

        if await like_btn.count() > 0:
            # 获取博主名字用于日志展示 (可选)
            try:
                author = await target_tweet.locator(
                    '[data-testid="User-Name"]'
                ).first.text_content()
                logs.append(
                    f"-> [推特点赞] 目标: {author.split('@')[0] if '@' in author else 'Unknown'}"
                )
            except:
                logs.append("-> [推特点赞] 选中了一条推文")

            # 执行点击
            await like_btn.click()
            logs.append("✅ [推特点赞] 点赞成功")
            await page.wait_for_timeout(1000)  # 稍微停顿模拟真人
        else:
            logs.append("⚠️ [推特点赞] 跳过: 该推文已经点赞过了")
