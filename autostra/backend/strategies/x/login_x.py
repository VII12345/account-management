from ..base import BaseStrategy


class Strategy(BaseStrategy):
    async def run(self, page, params, logs):
        print("正在访问X.com...")
        # await page.goto("https://x.com")

        # # 获取页面标题
        # title = await page.title()
        # print(f"页面标题: {title}")

        # await page.wait_for_timeout(2000)
