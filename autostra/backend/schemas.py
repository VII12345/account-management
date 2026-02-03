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