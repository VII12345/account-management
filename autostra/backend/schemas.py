"""
自动化子系统数据模型定义模块。

职责：使用 Pydantic 定义请求/响应结构，统一接口契约与字段验证。
边界：仅描述数据形状，不处理数据库读写与流程编排。
"""

from pydantic import BaseModel
from typing import List, Dict, Any, Optional

# 定义坐标模型
class Position(BaseModel):
    x: float
    y: float

class Node(BaseModel):
    id: str
    type: str = "default"
    data: Dict[str, Any] = {}
    # 👇👇👇 关键新增：必须定义 position，否则会被丢弃
    position: Position = {"x": 0, "y": 0} 
    # 👆👆👆

class Edge(BaseModel):
    source: str
    target: str
    # 连线也可能有 id 等属性，为了兼容性可以加个 loose dict
    id: Optional[str] = None

class FlowRequest(BaseModel):
    nodes: List[Node]
    edges: List[Edge]
    cdp_url: str = "http://127.0.0.1:9222"
    group_id: Optional[str] = None
    strategy_name: Optional[str] = None
    account_id: Optional[str] = None
    is_public: bool = False
    target_account_ids: Optional[List[str]] = None