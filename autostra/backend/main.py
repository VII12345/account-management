import os
import sys
import io
import json
import uvicorn
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas import FlowRequest
import engine
from db_config import get_db_conn

# 环境配置
os.environ["no_proxy"] = "localhost,127.0.0.1,::1"
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def ensure_strategy_table():
    conn = await get_db_conn()
    try:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                CREATE TABLE IF NOT EXISTS autostra_strategies (
                  id BIGINT NOT NULL AUTO_INCREMENT,
                  group_id VARCHAR(100) NOT NULL,
                  account_id VARCHAR(100) NOT NULL DEFAULT 'default',
                  strategy_name VARCHAR(255) NOT NULL,
                  flow_json LONGTEXT NOT NULL,
                  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                  PRIMARY KEY (id),
                  UNIQUE KEY uq_autostra_strategy (group_id, account_id, strategy_name),
                  KEY idx_autostra_group (group_id),
                  KEY idx_autostra_group_account (group_id, account_id)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
                """
            )
        await conn.commit()
    finally:
        conn.close()


def resolve_account_id(account_id: Optional[str]) -> str:
    return account_id or "default"


@app.on_event("startup")
async def startup_event():
    await ensure_strategy_table()


# --- 1. 获取所有平台的策略数量 (用于侧边栏 Badge) ---
@app.get("/stats")
async def get_stats():
    conn = await get_db_conn()
    try:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                SELECT group_id, COUNT(*)
                FROM autostra_strategies
                GROUP BY group_id
                """
            )
            rows = await cur.fetchall()
            return {group_id: count for group_id, count in rows}
    finally:
        conn.close()


# --- 2.1 获取某平台下的账号列表 ---
@app.get("/accounts/{group_id}")
async def list_accounts(group_id: str):
    conn = await get_db_conn()
    try:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                SELECT DISTINCT account_id
                FROM autostra_strategies
                WHERE group_id=%s
                ORDER BY account_id ASC
                """,
                (group_id,),
            )
            rows = await cur.fetchall()
            accounts = [account_id for (account_id,) in rows]
            return {"accounts": accounts}
    finally:
        conn.close()


# --- 2. 获取某平台下的所有策略列表 ---
@app.get("/list/{group_id}")
async def list_strategies(group_id: str, account_id: Optional[str] = None):
    resolved_account_id = resolve_account_id(account_id)
    conn = await get_db_conn()
    try:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                SELECT strategy_name
                FROM autostra_strategies
                WHERE group_id=%s AND account_id=%s
                ORDER BY updated_at DESC, strategy_name ASC
                """,
                (group_id, resolved_account_id),
            )
            rows = await cur.fetchall()
            strategies = [strategy_name for (strategy_name,) in rows]
            return {"strategies": strategies}
    finally:
        conn.close()


# --- 3. 保存具体的策略 ---
@app.post("/save/{group_id}/{name}")
async def save_strategy(
    group_id: str, name: str, flow: FlowRequest, account_id: Optional[str] = None
):
    resolved_account_id = resolve_account_id(account_id)
    payload = json.dumps(flow.dict(), ensure_ascii=False)

    conn = await get_db_conn()
    try:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                INSERT INTO autostra_strategies (group_id, account_id, strategy_name, flow_json)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                  flow_json=VALUES(flow_json),
                  updated_at=CURRENT_TIMESTAMP
                """,
                (group_id, resolved_account_id, name, payload),
            )
        await conn.commit()
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


# --- 4. 加载具体的策略 ---
@app.get("/load/{group_id}/{name}")
async def load_strategy(group_id: str, name: str, account_id: Optional[str] = None):
    resolved_account_id = resolve_account_id(account_id)
    conn = await get_db_conn()
    try:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                SELECT flow_json
                FROM autostra_strategies
                WHERE group_id=%s AND account_id=%s AND strategy_name=%s
                LIMIT 1
                """,
                (group_id, resolved_account_id, name),
            )
            row = await cur.fetchone()

        if not row:
            return {"nodes": [], "edges": []}

        flow_json = row[0]
        return json.loads(flow_json)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


# --- 5. 运行 ---
@app.post("/run")
async def run_flow(flow: FlowRequest):
    target_url = flow.cdp_url or "http://127.0.0.1:9222"
    return await engine.execute_task(flow.nodes, flow.edges, target_url)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
