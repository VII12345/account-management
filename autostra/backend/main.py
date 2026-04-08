import os
import sys
import io
import json
import uvicorn
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Query
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
            # 创建主策略表
            await cur.execute(
                """
                CREATE TABLE IF NOT EXISTS autostra_strategies (
                  id BIGINT NOT NULL AUTO_INCREMENT,
                  group_id VARCHAR(100) NOT NULL,
                  account_id VARCHAR(100) NOT NULL DEFAULT 'default',
                  strategy_name VARCHAR(255) NOT NULL,
                  flow_json LONGTEXT NOT NULL,
                  is_public TINYINT(1) NOT NULL DEFAULT 0,
                  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                  PRIMARY KEY (id),
                  UNIQUE KEY uq_autostra_strategy (group_id, account_id, strategy_name),
                  KEY idx_autostra_group (group_id),
                  KEY idx_autostra_group_account (group_id, account_id),
                  KEY idx_autostra_public (group_id, is_public)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
                """
            )
            # 创建公共策略映射表
            await cur.execute(
                """
                CREATE TABLE IF NOT EXISTS autostra_public_strategy_mappings (
                  id BIGINT NOT NULL AUTO_INCREMENT,
                  strategy_id BIGINT NOT NULL,
                  group_id VARCHAR(100) NOT NULL,
                  strategy_name VARCHAR(255) NOT NULL,
                  target_account_id VARCHAR(100) NOT NULL,
                  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                  PRIMARY KEY (id),
                  UNIQUE KEY uq_mapping (strategy_id, target_account_id),
                  KEY idx_strategy (group_id, strategy_name),
                  KEY idx_target_account (group_id, target_account_id)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
                """
            )
            # 尝试添加 is_public 列（如果不存在）- 使用 IGNORE 忽略错误
            await cur.execute(
                """
                ALTER IGNORE TABLE autostra_strategies
                ADD COLUMN is_public TINYINT(1) NOT NULL DEFAULT 0
                """
            )
        await conn.commit()
    except Exception as e:
        # 表可能已经存在或字段已存在，忽略这个错误
        print(f"表初始化警告: {e}")
        try:
            await conn.commit()
        except:
            pass
    finally:
        conn.close()


def resolve_account_id(account_id: Optional[str]) -> str:
    return account_id or "default"


async def validate_target_accounts(target_accounts: List[str]):
    if not target_accounts:
        return

    invalid_format_ids = [account_id for account_id in target_accounts if not str(account_id).isdigit()]
    if invalid_format_ids:
        raise HTTPException(
            status_code=400,
            detail=f"存在无效账号 ID: {', '.join(map(str, invalid_format_ids))}"
        )

    placeholders = ", ".join(["%s"] * len(target_accounts))
    conn = await get_db_conn()
    try:
        async with conn.cursor() as cur:
            await cur.execute(
                f"""
                SELECT CAST(id AS CHAR)
                FROM accounts
                WHERE CAST(id AS CHAR) IN ({placeholders})
                """,
                tuple(target_accounts),
            )
            rows = await cur.fetchall()
            existing_ids = {str(account_id) for (account_id,) in rows}

        missing_ids = [account_id for account_id in target_accounts if account_id not in existing_ids]
        if missing_ids:
            raise HTTPException(
                status_code=400,
                detail=f"存在无效账号 ID: {', '.join(missing_ids)}",
            )
    finally:
        conn.close()


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


# --- 6. 保存公共策略并绑定到多个账号 ---
@app.post("/save-public/{group_id}/{name}")
async def save_public_strategy(
    group_id: str,
    name: str,
    flow: FlowRequest,
    target_accounts: Optional[List[str]] = Query(None)
):
    """
    保存公共策略到 account_id='__public__'
    同时绑定到指定的目标账号列表
    
    Args:
        group_id: 平台 ID
        name: 策略名称
        flow: 策略流程数据
        target_accounts: 目标账号 ID 列表，例如 ["account1", "account2"]
    """
    if target_accounts is None:
        target_accounts = []

    await validate_target_accounts(target_accounts)
    
    payload = json.dumps(flow.dict(), ensure_ascii=False)
    
    conn = await get_db_conn()
    try:
        async with conn.cursor() as cur:
            # 保存公共策略（account_id='__public__'）
            await cur.execute(
                """
                INSERT INTO autostra_strategies (group_id, account_id, strategy_name, flow_json, is_public)
                VALUES (%s, %s, %s, %s, 1)
                ON DUPLICATE KEY UPDATE
                  flow_json=VALUES(flow_json),
                  is_public=1,
                  updated_at=CURRENT_TIMESTAMP
                """,
                (group_id, "__public__", name, payload),
            )
            
            # 获取策略 ID
            await cur.execute(
                """
                SELECT id FROM autostra_strategies
                WHERE group_id=%s AND account_id=%s AND strategy_name=%s
                """,
                (group_id, "__public__", name),
            )
            result = await cur.fetchone()
            strategy_id = result[0] if result else None
            
            if strategy_id:
                # 删除旧的映射关系
                await cur.execute(
                    """
                    DELETE FROM autostra_public_strategy_mappings
                    WHERE strategy_id=%s
                    """,
                    (strategy_id,),
                )
                
                # 添加新的映射关系
                for account_id in target_accounts:
                    await cur.execute(
                        """
                        INSERT INTO autostra_public_strategy_mappings 
                        (strategy_id, group_id, strategy_name, target_account_id)
                        VALUES (%s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE created_at=created_at
                        """,
                        (strategy_id, group_id, name, account_id),
                    )
        
        await conn.commit()
        return {"status": "success", "target_count": len(target_accounts)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


# --- 7. 列出某平台的所有公共策略 ---
@app.get("/list-public/{group_id}")
async def list_public_strategies(group_id: str):
    """
    列出某平台的所有公共策略
    """
    conn = await get_db_conn()
    try:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                SELECT strategy_name
                FROM autostra_strategies
                WHERE group_id=%s AND account_id=%s AND is_public=1
                ORDER BY strategy_name ASC
                """,
                (group_id, "__public__"),
            )
            rows = await cur.fetchall()
            strategies = [name for (name,) in rows]
            return {"strategies": strategies}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


# --- 8. 获取公共策略的目标账号列表 ---
@app.get("/public-targets/{group_id}/{name}")
async def get_public_strategy_targets(group_id: str, name: str):
    """
    获取某个公共策略绑定的目标账号列表
    """
    conn = await get_db_conn()
    try:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                SELECT DISTINCT target_account_id
                FROM autostra_public_strategy_mappings
                WHERE group_id=%s AND strategy_name=%s
                ORDER BY target_account_id ASC
                """,
                (group_id, name),
            )
            rows = await cur.fetchall()
            targets = [account_id for (account_id,) in rows]
            return {"targets": targets}
    finally:
        conn.close()


# --- 9. 更新公共策略的目标账号列表 ---
@app.post("/update-public-targets/{group_id}/{name}")
async def update_public_strategy_targets(
    group_id: str,
    name: str,
    target_accounts: Optional[List[str]] = Query(None)
):
    """
    更新公共策略的目标账号列表（替换所有映射）
    
    Args:
        group_id: 平台 ID
        name: 策略名称
        target_accounts: 新的目标账号 ID 列表
    """
    if target_accounts is None:
        target_accounts = []

    await validate_target_accounts(target_accounts)
    
    conn = await get_db_conn()
    try:
        async with conn.cursor() as cur:
            # 获取策略 ID
            await cur.execute(
                """
                SELECT id FROM autostra_strategies
                WHERE group_id=%s AND account_id=%s AND strategy_name=%s
                """,
                (group_id, "__public__", name),
            )
            result = await cur.fetchone()
            
            if not result:
                raise HTTPException(status_code=404, detail="公共策略不存在")
            
            strategy_id = result[0]
            
            # 删除所有旧的映射
            await cur.execute(
                """
                DELETE FROM autostra_public_strategy_mappings
                WHERE strategy_id=%s
                """,
                (strategy_id,),
            )
            
            # 添加新的映射
            for account_id in target_accounts:
                await cur.execute(
                    """
                    INSERT INTO autostra_public_strategy_mappings 
                    (strategy_id, group_id, strategy_name, target_account_id)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (strategy_id, group_id, name, account_id),
                )
        
        await conn.commit()
        return {"status": "success", "target_count": len(target_accounts)}
    except HTTPException:
        raise
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
