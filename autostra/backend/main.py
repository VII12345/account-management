import os
import sys
import io
import json
import glob
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas import FlowRequest
import engine 

# 环境配置
os.environ["no_proxy"] = "localhost,127.0.0.1,::1"
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SAVE_DIR = "saved_data"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 辅助函数：确保目录存在
def ensure_dir(group_id):
    path = os.path.join(SAVE_DIR, group_id)
    if not os.path.exists(path):
        os.makedirs(path)
    return path

# --- 1. 获取所有平台的策略数量 (用于侧边栏 Badge) ---
@app.get("/stats")
async def get_stats():
    stats = {}
    # 遍历 saved_data 下的所有文件夹
    if os.path.exists(SAVE_DIR):
        for group_id in os.listdir(SAVE_DIR):
            group_path = os.path.join(SAVE_DIR, group_id)
            if os.path.isdir(group_path):
                # 计算该文件夹下 json 文件的数量
                count = len(glob.glob(os.path.join(group_path, "*.json")))
                stats[group_id] = count
    return stats

# --- 2. 获取某平台下的所有策略列表 ---
@app.get("/list/{group_id}")
async def list_strategies(group_id: str):
    path = ensure_dir(group_id)
    files = glob.glob(os.path.join(path, "*.json"))
    # 返回文件名（去掉路径和后缀）
    strategies = [os.path.splitext(os.path.basename(f))[0] for f in files]
    return {"strategies": strategies}

# --- 3. 保存具体的策略 ---
@app.post("/save/{group_id}/{name}")
async def save_strategy(group_id: str, name: str, flow: FlowRequest):
    try:
        path = ensure_dir(group_id)
        file_path = os.path.join(path, f"{name}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(flow.dict(), f, indent=2, ensure_ascii=False)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- 4. 加载具体的策略 ---
@app.get("/load/{group_id}/{name}")
async def load_strategy(group_id: str, name: str):
    file_path = os.path.join(SAVE_DIR, group_id, f"{name}.json")
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    return {"nodes": [], "edges": []}

# --- 5. 运行 ---
@app.post("/run")
async def run_flow(flow: FlowRequest):
    target_url = flow.cdp_url or "http://127.0.0.1:9222"
    return await engine.execute_task(flow.nodes, flow.edges, target_url)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)