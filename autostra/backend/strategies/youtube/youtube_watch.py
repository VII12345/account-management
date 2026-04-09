"""
YouTube 观看策略实现模块。

职责：执行视频观看流程，控制进入目标视频、观看时长与进度行为。
边界：仅覆盖观看链路，不包含登录、搜索与互动聚合逻辑。
"""

from ..base import BaseStrategy
import random
import asyncio
from pathlib import Path
from lib import HumanMouse

_MODEL_PATH = Path(__file__).resolve().parents[2] / "mouse.onnx"
_HUMAN_MOUSE = HumanMouse(model_path=_MODEL_PATH)

class Strategy(BaseStrategy):
    async def run(self, page, params, logs):
        watch_time = int(params.get("time", 15000))
        
        logs.append(f"-> [YouTube] 准备观看视频...")

        # 1. 强制激活页面 (有时候页面在后台会导致JS不执行)
        try:
            await page.bring_to_front()
            await page.mouse.wheel(0, 300) # 稍微滚一下唤醒懒加载
            await page.wait_for_timeout(1000)
        except:
            pass

        # =====================================================
        # 2. 寻找视频 (使用最底层的 ID 和 HREF 特征)
        # =====================================================
        # 策略：直接找页面上所有的 <a> 标签，只要 href 包含 /watch?v= 且不是 shorts
        # 这种方法无视 HTML 结构变化，只要是视频链接就能抓到
        
        logs.append("-> 正在扫描所有视频链接...")

        # 使用 JS 在浏览器内部执行查找，这比 Playwright 选择器更直观
        # 我们返回一个包含 ElementHandle 的列表
        candidates = await page.evaluate_handle("""
            () => {
                // 1. 找大缩略图链接 (通常是 a#thumbnail)
                const thumbnails = Array.from(document.querySelectorAll('a#thumbnail'));
                
                // 2. 找标题链接 (通常是 a#video-title 或 a#video-title-link)
                const titles = Array.from(document.querySelectorAll('a#video-title, a#video-title-link'));
                
                // 3. 找所有带 watch 的链接 (作为兜底)
                const allLinks = Array.from(document.querySelectorAll('a[href*="/watch?v="]'));
                
                // 合并并去重
                const combined = [...thumbnails, ...titles, ...allLinks];
                
                // 过滤：必须有 href，必须不是 shorts，必须可见(宽或高大于0)
                return combined.filter(el => {
                    const href = el.getAttribute('href');
                    const rect = el.getBoundingClientRect();
                    return href && 
                           href.includes('/watch?v=') && 
                           !href.includes('/shorts/') &&
                           rect.width > 0 && rect.height > 0; // 简单的可见性检查
                });
            }
        """)

        # 将 JSHandle 转换为 Playwright 的 ElementHandles 列表
        # 注意：这里我们获取的是一个 JS 数组的 Handle
        properties = await candidates.get_properties()
        video_elements = []
        for _, val in properties.items():
            element = val.as_element()
            if element:
                video_elements.append(element)

        if not video_elements:
            logs.append("❌ [YouTube] 页面已加载，但未扫描到有效的视频链接。")
            logs.append("-> 尝试截图调试...")
            try:
                await page.screenshot(path="debug_not_found.png")
            except:
                pass
            return

        logs.append(f"✅ 扫描到 {len(video_elements)} 个潜在视频目标")

        # =====================================================
        # 3. 随机选择并点击 (JS 暴力点击)
        # =====================================================
        # 取前 8 个，避免点到页脚去
        target_video = random.choice(video_elements[:8])
        
        # --- 调试高亮：给选中的元素加个红框，让你看到 ---
        await target_video.evaluate("el => el.style.border = '5px solid red'")
        logs.append("-> 🎯 已高亮选中目标 (看屏幕红框)")
        await page.wait_for_timeout(1000) # 让你看清楚红框

        # 获取链接用于日志
        try:
            href = await target_video.get_attribute("href")
            logs.append(f"-> 准备跳转: {href}")
        except:
            pass

        # 核心：使用 HumanMouse 点击
        try:
            await _HUMAN_MOUSE.click_element(page, target_video)
            logs.append("-> 已触发 HumanMouse 点击")
        except Exception as e:
            logs.append(f"❌ HumanMouse 点击失败: {e}")
            return

        # =====================================================
        # 4. 观看监控
        # =====================================================
        # 检查 URL 是否变化
        try:
            await page.wait_for_url("**/watch?v=*", timeout=8000)
            logs.append("✅ 成功进入播放页")
        except:
            logs.append("⚠️ URL 未变化，点击可能未生效")

        elapsed = 0
        ad_selectors = [
            '.ytp-ad-skip-button', 
            '.ytp-ad-skip-button-modern',
            '.videoAdUiSkipButton',
            'button[id^="skip-button"]',
            '.ytp-ad-overlay-close-button'
        ]

        while elapsed < watch_time:
            # 简单的广告检测
            for ad_sel in ad_selectors:
                try:
                    locator = page.locator(ad_sel)
                    if await locator.is_visible():
                        handle = await locator.element_handle()
                        if handle:
                            logs.append("⚡ 跳过广告")
                            await _HUMAN_MOUSE.click_element(page, handle, pause_after=False)
                except:
                    pass
            
            await page.wait_for_timeout(1000)
            elapsed += 1000
            
        logs.append("✅ 观看结束")
