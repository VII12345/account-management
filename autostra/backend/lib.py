#!/usr/bin/env python3
import random
from pathlib import Path

import numpy as np
import onnxruntime as ort


def load_model(model_path: Path):
    session = ort.InferenceSession(str(model_path), providers=["CPUExecutionProvider"])
    input_meta = session.get_inputs()[0]
    input_name = input_meta.name
    input_shape = input_meta.shape
    return session, input_name, input_shape


def predict_points(session, input_name, input_shape, dx, dy):
    arr = np.array([[dx, dy]], dtype=np.float32)
    if input_shape is not None and len(input_shape) == 3:
        arr = arr.reshape(1, 1, 2)
    outputs = session.run(None, {input_name: arr})
    pts = outputs[0].reshape(-1, 2)
    return [(float(x), float(y)) for x, y in pts]


def interpolate_path(points, steps_per_segment):
    if not points:
        return []
    out = []
    for i in range(len(points) - 1):
        x0, y0 = points[i]
        x1, y1 = points[i + 1]
        for j in range(1, steps_per_segment + 1):
            t = j / (steps_per_segment + 1)
            out.append((x0 + (x1 - x0) * t, y0 + (y1 - y0) * t))
    out.append(points[-1])
    return out


def delay_multiplier(progress, profile, profile_min, profile_max, profile_gamma):
    if progress is None:
        return 1.0
    p = max(0.0, min(1.0, float(progress)))
    p_min = float(profile_min)
    p_max = float(profile_max)
    if p_min > p_max:
        p_min, p_max = p_max, p_min
    gamma = max(0.01, float(profile_gamma))
    if profile == "ease-in":
        t = (1.0 - p) ** gamma
        return p_min + (p_max - p_min) * t
    if profile == "ease-out":
        t = p**gamma
        return p_min + (p_max - p_min) * t
    if profile == "ease-in-out":
        edge = abs(2 * p - 1.0) ** gamma
        return p_min + (p_max - p_min) * edge
    if profile == "random":
        return random.uniform(p_min, p_max)
    return 1.0


async def maybe_wait(
    page,
    min_delay,
    max_delay,
    progress=None,
    profile="linear",
    jitter=0,
    profile_min=0.6,
    profile_max=1.4,
    profile_gamma=1.0,
):
    if min_delay < 0:
        min_delay = 0
    if max_delay < 0:
        max_delay = 0
    if min_delay > max_delay:
        min_delay, max_delay = max_delay, min_delay

    base = 0
    if max_delay > 0:
        base = random.randint(min_delay, max_delay)

    scale = delay_multiplier(progress, profile, profile_min, profile_max, profile_gamma)
    delay = int(round(base * scale))

    if jitter > 0:
        delay += random.randint(-jitter, jitter)

    if delay <= 0:
        return
    await page.wait_for_timeout(delay)


def build_model_path(predicted_points, dx, dy, steps_per_segment):
    pts = [(0.0, 0.0)] + list(predicted_points)
    if pts:
        last_x, last_y = pts[-1]
        if abs(last_x - dx) > 2 or abs(last_y - dy) > 2:
            pts.append((dx, dy))
    return interpolate_path(pts, steps_per_segment)


async def move_mouse_with_model(
    page,
    session,
    input_name,
    input_shape,
    cur_pos,
    target_pos,
    steps,
    min_delay,
    max_delay,
    speed_profile,
    delay_jitter,
    profile_min,
    profile_max,
    profile_gamma,
    hold=False,
):
    cur_x, cur_y = cur_pos
    target_x, target_y = target_pos
    dx = int(round(target_x - cur_x))
    dy = int(round(target_y - cur_y))

    predicted = predict_points(session, input_name, input_shape, dx, dy)
    path = build_model_path(predicted, dx, dy, steps)

    if hold:
        await page.mouse.down()
        await maybe_wait(
            page,
            min_delay,
            max_delay,
            progress=0.0,
            profile=speed_profile,
            jitter=delay_jitter,
            profile_min=profile_min,
            profile_max=profile_max,
            profile_gamma=profile_gamma,
        )

    path_len = max(1, len(path) - 1)
    for idx, (px, py) in enumerate(path):
        await page.mouse.move(cur_x + px, cur_y + py)
        progress = idx / path_len
        await maybe_wait(
            page,
            min_delay,
            max_delay,
            progress=progress,
            profile=speed_profile,
            jitter=delay_jitter,
            profile_min=profile_min,
            profile_max=profile_max,
            profile_gamma=profile_gamma,
        )

    await page.mouse.move(target_x, target_y)

    if hold:
        await maybe_wait(
            page,
            min_delay,
            max_delay,
            progress=1.0,
            profile=speed_profile,
            jitter=delay_jitter,
            profile_min=profile_min,
            profile_max=profile_max,
            profile_gamma=profile_gamma,
        )
        await page.mouse.up()

    return target_x, target_y


async def element_center(element):
    await element.scroll_into_view_if_needed()
    box = await element.bounding_box()
    if not box:
        raise RuntimeError("Element has no bounding box")
    return box["x"] + box["width"] / 2, box["y"] + box["height"] / 2


async def wait_between_actions(page, min_ms=500, max_ms=2000):
    if min_ms < 0:
        min_ms = 0
    if max_ms < 0:
        max_ms = 0
    if min_ms > max_ms:
        min_ms, max_ms = max_ms, min_ms
    if max_ms <= 0:
        return
    await page.wait_for_timeout(random.randint(min_ms, max_ms))


class HumanMouse:
    def __init__(
        self,
        model_path="mouse.onnx",
        steps=6,
        min_delay=12,
        max_delay=30,
        speed_profile="linear",
        delay_jitter=0,
        profile_min=0.3,
        profile_max=3.0,
        profile_gamma=1.6,
    ):
        self.model_path = Path(model_path)
        self.session, self.input_name, self.input_shape = load_model(self.model_path)
        self.steps = steps
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.speed_profile = speed_profile
        self.delay_jitter = delay_jitter
        self.profile_min = profile_min
        self.profile_max = profile_max
        self.profile_gamma = profile_gamma
        self.cur_pos = None

    async def init_position(self, page):
        if page.viewport_size:
            viewport = page.viewport_size
        else:
            viewport = await page.evaluate("() => ({ width: window.innerWidth, height: window.innerHeight })")
        self.cur_pos = (viewport["width"] / 2, viewport["height"] / 2)
        await page.mouse.move(self.cur_pos[0], self.cur_pos[1])
        return self.cur_pos

    async def move_to(self, page, target_pos, hold=False):
        if self.cur_pos is None:
            await self.init_position(page)
        self.cur_pos = await move_mouse_with_model(
            page,
            self.session,
            self.input_name,
            self.input_shape,
            self.cur_pos,
            target_pos,
            self.steps,
            self.min_delay,
            self.max_delay,
            self.speed_profile,
            self.delay_jitter,
            self.profile_min,
            self.profile_max,
            self.profile_gamma,
            hold=hold,
        )
        return self.cur_pos

    async def click_element(self, page, element, pause_after=True):
        target_pos = await element_center(element)
        await self.move_to(page, target_pos, hold=False)
        await page.mouse.down()
        await maybe_wait(
            page,
            self.min_delay,
            self.max_delay,
            progress=0.0,
            profile=self.speed_profile,
            jitter=self.delay_jitter,
            profile_min=self.profile_min,
            profile_max=self.profile_max,
            profile_gamma=self.profile_gamma,
        )
        await page.mouse.up()
        if pause_after:
            await wait_between_actions(page, 500, 2000)

    async def drag_to(self, page, start_pos, target_pos):
        await self.move_to(page, start_pos, hold=False)
        await self.move_to(page, target_pos, hold=True)

