"""
策略包初始化模块。

职责：提供策略子包统一入口，便于外部按平台加载策略实现。
边界：不实现具体业务动作，仅做包级组织与导出。
"""

# backend/strategies/__init__.py
from .x.login_x import Strategy as LoginStrategyX
from .x.like_x import Strategy as LikeStrategyX
from .x.zhuan_x import Strategy as ZhuanStrategyX
from .common import WaitStrategy, LoopStartStrategy
from .youtube.youtube_login import Strategy as YouTubeLoginStrategy
from .youtube.youtube_search import Strategy as YouTubeSearchStrategy
from .youtube.youtube_watch import Strategy as YouTubeWatchStrategy
from .youtube.youtube_interact import Strategy as YouTubeInteractStrategy
from .youtube.youtube_like import Strategy as YouTubeLikeStrategy
from .facebook.facebook_search import Strategy as FacebookSearchStrategy
from .facebook.facebook_like import Strategy as FacebookLikeStrategy
from .facebook.facebook_post import Strategy as FacebookPostStrategy

# 注册表：前端 nodeType -> 具体的策略实例
# 如果你加了新文件，记得在这里注册一下
REGISTRY = {
    "wait": WaitStrategy(),
    "loop_start": LoopStartStrategy(),
    "login_x": LoginStrategyX(),
    "like_x": LikeStrategyX(),
    "zhuan_x": ZhuanStrategyX(),
    "youtube_login": YouTubeLoginStrategy(),
    "youtube_search": YouTubeSearchStrategy(),
    "youtube_watch": YouTubeWatchStrategy(),
    "youtube_interact": YouTubeInteractStrategy(),
    "youtube_like": YouTubeLikeStrategy(),
    "facebook_search": FacebookSearchStrategy(),
    "facebook_like": FacebookLikeStrategy(),
    "facebook_post": FacebookPostStrategy(),
}


def get_strategy(name: str):
    return REGISTRY.get(name)
