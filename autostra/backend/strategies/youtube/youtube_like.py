from ..base import BaseStrategy
import asyncio
from pathlib import Path
from lib import HumanMouse

_MODEL_PATH = Path(__file__).resolve().parents[2] / "mouse.onnx"
_HUMAN_MOUSE = HumanMouse(
    model_path=_MODEL_PATH,
    steps=5,
    min_delay=0,
    max_delay=10,
    speed_profile="ease-in-out",
    delay_jitter=5,
)


class Strategy(BaseStrategy):
    async def run(self, page, params, logs):
        logs.append("-> [YouTube] 准备执行：点赞")

        # 1. 检查是否在播放页
        if "/watch" not in page.url:
            logs.append("❌ [YouTube] 当前不在视频播放页，无法点赞。")
            return

        # 2. 使用指定 XPath 定位点赞（不使用 JS）
        like_xpath = '//*[@id="top-level-buttons-computed"]/segmented-like-dislike-button-view-model/yt-smartimation/div/div/like-button-view-model/toggle-button-view-model/button-view-model/button/yt-touch-feedback-shape/div[2]'

        target_btn = None
        try:
            await page.wait_for_selector(f"xpath={like_xpath}", timeout=5000)
            target_btn = await page.locator(
                f"xpath={like_xpath}"
            ).first.element_handle()
        except Exception:
            target_btn = None

        if target_btn:
            # 3. 检查状态
            is_pressed = None
            try:
                btn_locator = page.locator(f"xpath={like_xpath}/ancestor::button[1]")
                if await btn_locator.count():
                    is_pressed = await btn_locator.first.get_attribute("aria-pressed")
            except Exception:
                pass

            if is_pressed == "true":
                logs.append("ℹ️ [YouTube] 检测到已经点过赞了，跳过。")
            else:
                try:
                    logs.append("-> 正在使用 HumanMouse 点击...")

                    # 1. 强制滚动到视图中心
                    await target_btn.evaluate(
                        "el => el.scrollIntoView({block: 'center', inline: 'center'})"
                    )
                    await page.wait_for_timeout(1000)

                    # 2. HumanMouse 点击（使用 lib.py）
                    await _HUMAN_MOUSE.click_element(page, target_btn)

                    logs.append("✅ [YouTube] HumanMouse 点击完成")

                    # 3. 验证结果
                    await page.wait_for_timeout(1500)
                    new_state = None
                    try:
                        btn_locator = page.locator(
                            f"xpath={like_xpath}/ancestor::button[1]"
                        )
                        if await btn_locator.count():
                            new_state = await btn_locator.first.get_attribute(
                                "aria-pressed"
                            )
                    except Exception:
                        pass
                    if new_state == "true":
                        logs.append("-> 状态确认：点赞成功 (图标变亮)")
                    else:
                        logs.append("⚠️ 警告：点击后状态未变，可能需要登录或网络延迟")

                except Exception as e:
                    logs.append(f"❌ HumanMouse 执行异常: {e}")
        else:
            logs.append("❌ 未找到点赞按钮。")

        await page.wait_for_timeout(1000)
