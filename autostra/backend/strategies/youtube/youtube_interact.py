from ..base import BaseStrategy
import asyncio
from pathlib import Path
from lib import HumanMouse

_MODEL_PATH = Path(__file__).resolve().parents[2] / "mouse.onnx"
_HUMAN_MOUSE = HumanMouse(model_path=_MODEL_PATH)

class Strategy(BaseStrategy):
    async def run(self, page, params, logs):
        logs.append("-> [YouTube] 准备执行：订阅频道")

        # 1. 检查是否在播放页
        if "/watch" not in page.url:
            logs.append("❌ [YouTube] 当前不在视频播放页，无法订阅。")
            return

        # 2. 寻找订阅按钮 (JS 内部寻找)
        # 订阅按钮通常包裹在 ytd-subscribe-button-renderer 标签内
        target_btn_handle = await page.evaluate_handle("""
            () => {
                // 策略 A: 找标准的订阅组件容器 (最准)
                const renderer = document.querySelector('ytd-subscribe-button-renderer');
                if (renderer) {
                    // 里面那个实际的 button 元素
                    return renderer.querySelector('button');
                }

                // 策略 B: 找包含"订阅"或"Subscribe"文字的按钮 (兜底)
                const buttons = Array.from(document.querySelectorAll('button'));
                return buttons.find(b => {
                    const text = b.innerText.trim();
                    return text === 'Subscribe' || text === '订阅' || text === 'Subscribed' || text === '已订阅';
                });
            }
        """)

        target_btn = target_btn_handle.as_element()

        if target_btn:
            # 3. 检查状态 (防止取订)
            try:
                # 获取按钮内部的文本
                btn_text = await target_btn.inner_text()
                btn_text = btn_text.strip()
                
                # 定义已订阅的关键词
                subscribed_keywords = ["Subscribed", "已订阅"]
                
                if any(k in btn_text for k in subscribed_keywords):
                    logs.append(f"ℹ️ [YouTube] 已经订阅过了 ({btn_text})，跳过。")
                else:
                    # 4. 执行订阅 (JS 强制点击)
                    logs.append(f"-> 找到按钮，当前状态: {btn_text}")
                    
                    # 滚动并高亮
                    await target_btn.evaluate("el => el.scrollIntoView({block: 'center', inline: 'center'})")
                    await page.wait_for_timeout(500)
                    
                    # 点击（HumanMouse）
                    await _HUMAN_MOUSE.click_element(page, target_btn)
                    logs.append("✅ [YouTube] 已发送订阅点击指令")
                    
                    # 5. 验证结果
                    await page.wait_for_timeout(2000)
                    new_text = await target_btn.inner_text()
                    if any(k in new_text for k in subscribed_keywords):
                        logs.append(f"-> 状态确认：订阅成功 (现显示: {new_text.strip()})")
                    else:
                        logs.append(f"⚠️ 警告：状态似乎未变 (现显示: {new_text.strip()})，可能未登录")
                        
            except Exception as e:
                logs.append(f"❌ 订阅操作失败: {e}")
        else:
            logs.append("❌ 未找到订阅按钮。请确认页面是否加载完成。")

        await page.wait_for_timeout(1000)
