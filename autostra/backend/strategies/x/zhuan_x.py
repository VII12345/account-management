import random
import asyncio
from ..base import BaseStrategy


class Strategy(BaseStrategy):
    async def run(self, page, params, logs):
        # 1. 注入反检测脚本
        await page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
        """)

        # 2. 确保在推特页面
        if "x.com" not in page.url:
            logs.append("-> [推特转发] 正在跳转主页...")
            await page.goto("https://x.com/home")
            await page.wait_for_timeout(3000)

        # 3. 获取推文列表
        try:
            await page.wait_for_selector('article[data-testid="tweet"]', timeout=8000)
        except:
            logs.append("❌ [推特转发] 错误: 页面未加载推文")
            return

        tweets = await page.locator('article[data-testid="tweet"]').all()
        if not tweets:
            logs.append("❌ 未找到推文")
            return

        # 4. 随机选一个
        target_tweet = random.choice(tweets)
        await target_tweet.scroll_into_view_if_needed()
        await page.wait_for_timeout(random.randint(1000, 2000))

        # 5. 寻找转发按钮
        retweet_btn = target_tweet.locator('[data-testid="retweet"]')

        if await retweet_btn.count() > 0:
            logs.append("-> [推特转发] 准备点击图标...")

            menu_open_success = False
            confirm_selector = '[data-testid="retweetConfirm"]'

            # --- [策略 A] 第一次尝试：完全拟人化点击 ---
            try:
                box = await retweet_btn.bounding_box()
                if box:
                    # 慢速移过去
                    await page.mouse.move(
                        box["x"] + box["width"] / 2,
                        box["y"] + box["height"] / 2,
                        steps=random.randint(5, 10),
                    )
                    await page.wait_for_timeout(random.randint(200, 400))
                    await page.mouse.click(
                        box["x"] + box["width"] / 2, box["y"] + box["height"] / 2
                    )
                    # 快速检查菜单是否出来
                    await page.wait_for_selector(
                        confirm_selector, state="visible", timeout=2000
                    )
                    menu_open_success = True
            except:
                # 这里的异常被捕获，静默进入策略 B
                pass

            # --- [策略 B] 补救点击 (已优化拟人逻辑) ---
            if not menu_open_success:
                logs.append("⚠️ [推特转发] 第一次点击未响应，模拟人工重试...")

                # 1. 战术停顿：模拟人脑反应时间 "咦？怎么没弹出来？"
                # 这是一个非常重要的“人类特征”
                await page.wait_for_timeout(random.randint(800, 1500))

                try:
                    # 2. 鼠标微调：稍微动一下鼠标，假装在找准位置
                    # 即使我们要用 force=True，最好也把鼠标移过去，欺骗前端监听
                    box = await retweet_btn.bounding_box()
                    if box:
                        # 随机偏移 1-3 像素
                        jitter_x = random.randint(-3, 3)
                        jitter_y = random.randint(-3, 3)
                        await page.mouse.move(
                            box["x"] + box["width"] / 2 + jitter_x,
                            box["y"] + box["height"] / 2 + jitter_y,
                            steps=3,
                        )
                        await page.wait_for_timeout(300)

                    # 3. 执行点击 (使用 force=True 确保必须点到)
                    await retweet_btn.click(force=True)

                    # 4. 等待菜单弹出
                    await page.wait_for_selector(
                        confirm_selector, state="visible", timeout=3000
                    )
                    menu_open_success = True

                except Exception as e:
                    logs.append(f"❌ [推特转发] 菜单彻底打不开: {e}")
                    # 检查是否是风控弹窗
                    if await page.locator("text=Unlock more").is_visible():
                        logs.append("🛑 [警告] 账号被风控限制！")
                        await page.mouse.click(0, 0)
                    return

            # --- [第二阶段] 点击菜单中的 "Repost" ---
            if menu_open_success:
                logs.append("-> [推特转发] 菜单已出，正在确认...")

                # 1. 思考时间：看到菜单后停顿
                await page.wait_for_timeout(random.randint(1000, 2000))

                # 2. 寻找确认按钮
                confirm_btn = page.locator(confirm_selector)
                btn_box = await confirm_btn.bounding_box()

                if btn_box:
                    # 3. 鼠标慢速滑向确认按钮
                    target_x = (
                        btn_box["x"] + btn_box["width"] / 2 + random.randint(-15, 15)
                    )
                    target_y = (
                        btn_box["y"] + btn_box["height"] / 2 + random.randint(-5, 5)
                    )

                    await page.mouse.move(
                        target_x, target_y, steps=random.randint(20, 35)
                    )  # steps 越大越慢

                    # 4. 悬停确认
                    await page.wait_for_timeout(random.randint(400, 800))

                    # 5. 点击
                    await page.mouse.click(target_x, target_y)
                else:
                    await confirm_btn.click()

                logs.append("✅ [推特转发] 转发成功 (已减速)")

            # 操作完再休息一下
            await page.wait_for_timeout(random.randint(2000, 4000))

        else:
            logs.append("ℹ️ [推特转发] 跳过: 该推文似乎已经转发过了")
