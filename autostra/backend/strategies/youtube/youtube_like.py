from ..base import BaseStrategy
import asyncio

class Strategy(BaseStrategy):
    async def run(self, page, params, logs):
        logs.append("-> [YouTube] 准备执行：点赞")

        # 1. 检查是否在播放页
        if "/watch" not in page.url:
            logs.append("❌ [YouTube] 当前不在视频播放页，无法点赞。")
            return

        # 2. 寻找点赞按钮 (JS 内部寻找)
        # 寻找逻辑保持不变，因为之前的日志显示已经"✅ 已定位到点赞按钮"，说明找是对的
        target_btn_handle = await page.evaluate_handle("""
            () => {
                // 策略 A: 找最新的 ViewModel 结构
                const viewModelBtn = document.querySelector('like-button-view-model button');
                if (viewModelBtn) return viewModelBtn;

                // 策略 B: 找特定图标
                const icon = document.querySelector('yt-animated-icon[animated-icon-type="CUSTOM_LIKE"]');
                if (icon) return icon.closest('button');

                // 策略 C: 旧版 ID
                const segmentBtn = document.querySelector('#segmented-like-button button');
                if (segmentBtn) return segmentBtn;

                return null;
            }
        """)

        target_btn = target_btn_handle.as_element()

        if target_btn:
            # 3. 检查状态
            is_pressed = await target_btn.get_attribute("aria-pressed")
            
            if is_pressed == "true":
                logs.append("ℹ️ [YouTube] 检测到已经点过赞了，跳过。")
            else:
                try:
                    logs.append("-> 正在尝试强制点击...")
                    
                    # 1. 强制滚动到视图中心 (JS)
                    # 这一步不会报错，浏览器会尽力滚
                    await target_btn.evaluate("el => el.scrollIntoView({block: 'center', inline: 'center'})")
                    
                    # 2. 稍微等一下滚动动画
                    await page.wait_for_timeout(1000)
                    
                    # 3. 强制点击 (JS)
                    # 即使元素被遮挡、透明度为0、或者在视口外，JS click 都能触发事件
                    await target_btn.evaluate("el => el.click()")
                    
                    logs.append("✅ [YouTube] 已发送点击指令")
                    
                    # 4. 验证结果
                    await page.wait_for_timeout(1500)
                    new_state = await target_btn.get_attribute("aria-pressed")
                    if new_state == "true":
                        logs.append("-> 状态确认：点赞成功 (图标变亮)")
                    else:
                        logs.append("⚠️ 警告：点击后状态未变，可能需要登录或网络延迟")
                        
                except Exception as e:
                    # 如果连 JS 都报错，那说明元素在这一瞬间被销毁了
                    logs.append(f"❌ JS执行异常: {e}")
        else:
            logs.append("❌ 未找到点赞按钮。")

        await page.wait_for_timeout(1000)