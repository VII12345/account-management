# accounts.py
import uuid
import csv
from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from pydantic import BaseModel
from db import get_conn

router = APIRouter(prefix="/accounts", tags=["Account Management"])


# -------------------------
# 数据模型
# -------------------------
class Account(BaseModel):
    platform: str | None = None
    username: str
    password: str
    email: str | None = None
    phone: str | None = None
    status: str | None = "active"
    tags: str | None = None


# -------------------------
# 创建账号（前端手动添加）
# -------------------------
@router.post("/")
async def create_account(data: Account):
    conn = await get_conn()
    async with conn.cursor() as cur:
        await cur.execute(
            """
            INSERT INTO accounts (platform, username, password, email, phone, status, created_at, tags)
            VALUES (%s, %s, %s, %s, %s, %s, NOW(), %s)
            """,
            (data.platform, data.username, data.password, data.email, data.phone, data.status, data.tags)
        )
        await conn.commit()
    conn.close()
    return {"message": "Account created"}


# -------------------------
# 获取账号列表（支持分页）
# -------------------------
@router.get("/")
async def list_accounts(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=200)
):
    offset = (page - 1) * page_size

    conn = await get_conn()
    async with conn.cursor() as cur:
        await cur.execute("SELECT COUNT(*) FROM accounts")
        total = (await cur.fetchone())[0]

        await cur.execute(
            "SELECT * FROM accounts ORDER BY id DESC LIMIT %s OFFSET %s",
            (page_size, offset)
        )
        rows = await cur.fetchall()

    conn.close()
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "data": rows
    }


# -------------------------
# 获取单个账号
# -------------------------
@router.get("/{acc_id}")
async def get_account(acc_id: int):
    conn = await get_conn()
    async with conn.cursor() as cur:
        await cur.execute("SELECT * FROM accounts WHERE id=%s", (acc_id,))
        row = await cur.fetchone()
    conn.close()

    if not row:
        raise HTTPException(404, "Account not found")

    return row


# -------------------------
# 更新账号（前端编辑）
# -------------------------
@router.put("/{acc_id}")
async def update_account(acc_id: int, data: Account):
    conn = await get_conn()
    async with conn.cursor() as cur:
        await cur.execute(
            """
            UPDATE accounts
            SET platform=%s, username=%s, password=%s, email=%s, phone=%s, status=%s, tags=%s
            WHERE id=%s
            """,
            (data.platform, data.username, data.password, data.email, data.phone, data.status, data.tags, acc_id)
        )
        await conn.commit()
    conn.close()
    return {"message": "Account updated"}


# -------------------------
# 删除账号
# -------------------------
@router.delete("/{acc_id}")
async def delete_account(acc_id: int):
    conn = await get_conn()
    async with conn.cursor() as cur:
        await cur.execute("DELETE FROM accounts WHERE id=%s", (acc_id,))
        await conn.commit()
    conn.close()
    return {"message": "Account deleted"}


# -------------------------
# 批量导入（JSON）
# -------------------------
@router.post("/import/json")
async def import_json(accounts: list[Account]):
    conn = await get_conn()
    async with conn.cursor() as cur:
        for acc in accounts:
            await cur.execute(
                """
                INSERT INTO accounts (platform, username, password, email, phone, status, created_at, tags)
                VALUES (%s, %s, %s, %s, %s, %s, NOW(), %s)
                """,
                (acc.platform, acc.username, acc.password, acc.email, acc.phone, acc.status, acc.tags)
            )
        await conn.commit()
    conn.close()
    return {"message": f"Imported {len(accounts)} accounts"}


# -------------------------
# 批量导入（CSV）
# -------------------------
@router.post("/import/csv")
async def import_csv(file: UploadFile = File(...)):
    content = (await file.read()).decode("utf-8").splitlines()
    reader = csv.DictReader(content)

    conn = await get_conn()
    async with conn.cursor() as cur:
        count = 0
        for row in reader:
            await cur.execute(
                """
                INSERT INTO accounts (platform, username, password, email, phone, status, created_at, tags)
                VALUES (%s, %s, %s, %s, %s, %s, NOW(), %s)
                """,
                (
                    row.get("platform"),
                    row.get("username"),
                    row.get("password"),
                    row.get("email"),
                    row.get("phone"),
                    row.get("status", "active"),
                    row.get("tags")
                )
            )
            count += 1
        await conn.commit()
    conn.close()

    return {"message": f"Imported {count} accounts"}
