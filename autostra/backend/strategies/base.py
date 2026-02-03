# backend/strategies/base.py
from playwright.async_api import Page
from typing import Dict, Any, List

class BaseStrategy:
    """所有自动化策略的父类"""
    
    async def run(self, page: Page, params: Dict[str, Any], logs: List[str]):
        """
        核心执行方法，所有子类必须实现这个方法
        :param page: Playwright 的页面对象
        :param params: 前端传来的节点数据 (如 keyword, username)
        :param logs: 日志列表，把执行过程写进去
        """
        raise NotImplementedError("必须在子类中实现 run 方法")

    # --- 通用工具方法 (子类可以直接用) ---
    async def smart_click(self, page: Page, selector: str):
        """智能点击：等待元素出现 + 强制点击"""
        await page.wait_for_selector(selector, state='attached', timeout=5000)
        await page.click(selector, force=True)

    async def smart_fill(self, page: Page, selector: str, text: str):
        """智能输入：等待元素 + 强制输入"""
        await page.wait_for_selector(selector, state='attached', timeout=5000)
        await page.fill(selector, str(text), force=True)