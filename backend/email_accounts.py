"""
邮箱账号管理路由模块。

职责：提供邮箱账号增删改查、状态维护和查询接口。
边界：仅处理邮箱账号资源，不扩展到代理或虚拟人管理。
"""

# email_accounts.py
import uuid
import csv
from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from pydantic import BaseModel, EmailStr
from db import get_conn

router = APIRouter(prefix="/email_accounts", tags=["Email Account Management"])


# -------------------------
# 数据模型
# -------------------------
class EmailAccount(BaseModel):
    email: EmailStr
    password: str
    protocol: str | None = None
    host: str | None = None
    port: int | None = None
    status: str | None = "active"
    tags: str | None = None


# -------------------------
# 创建邮箱账号（前端手动添加）
# -------------------------
@router.post("/")
async def create_email_account(data: EmailAccount):
    conn = await get_conn()
    async with conn.cursor() as cur:
        await cur.execute(
            """
            INSERT INTO email_accounts
            (email_address, email_password, protocol, host, port, status, created_at, tags)
            VALUES (%s, %s, %s, %s, %s, %s, NOW(), %s)
            """,
            (data.email, data.password, data.protocol, data.host, data.port, data.status, data.tags)
        )
        await conn.commit()
    conn.close()
    return {"message": "Email account created"}


# -------------------------
# 获取邮箱账号列表（支持分页）
# -------------------------
@router.get("/")
async def list_email_accounts(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=200)
):
    offset = (page - 1) * page_size

    conn = await get_conn()
    async with conn.cursor() as cur:
        await cur.execute("SELECT COUNT(*) FROM email_accounts")
        total = (await cur.fetchone())[0]

        await cur.execute(
            "SELECT * FROM email_accounts ORDER BY id DESC LIMIT %s OFFSET %s",
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
# 获取单个邮箱账号
# -------------------------
@router.get("/{email_id}")
async def get_email_account(email_id: int):
    conn = await get_conn()
    async with conn.cursor() as cur:
        await cur.execute("SELECT * FROM email_accounts WHERE id=%s", (email_id,))
        row = await cur.fetchone()
    conn.close()

    if not row:
        raise HTTPException(404, "Email account not found")

    return row


# -------------------------
# 更新邮箱账号（前端编辑）
# -------------------------
@router.put("/{email_id}")
async def update_email_account(email_id: int, data: EmailAccount):
    conn = await get_conn()
    async with conn.cursor() as cur:
        await cur.execute(
            """
            UPDATE email_accounts
            SET email_address=%s, email_password=%s, protocol=%s, host=%s, port=%s, status=%s, tags=%s
            WHERE id=%s
            """,
            (data.email, data.password, data.protocol, data.host, data.port, data.status, data.tags, email_id)
        )
        await conn.commit()
    conn.close()
    return {"message": "Email account updated"}


# -------------------------
# 删除邮箱账号
# -------------------------
@router.delete("/{email_id}")
async def delete_email_account(email_id: int):
    conn = await get_conn()
    async with conn.cursor() as cur:
        await cur.execute("DELETE FROM email_accounts WHERE id=%s", (email_id,))
        await conn.commit()
    conn.close()
    return {"message": "Email account deleted"}


# -------------------------
# 批量导入（JSON）
# -------------------------
@router.post("/import/json")
async def import_json(accounts: list[EmailAccount]):
    conn = await get_conn()
    async with conn.cursor() as cur:
        for acc in accounts:
            await cur.execute(
                """
                INSERT INTO email_accounts
                (email_address, email_password, protocol, host, port, status, created_at, tags)
                VALUES (%s, %s, %s, %s, %s, %s, NOW(), %s)
                """,
                (acc.email, acc.password, acc.protocol, acc.host, acc.port, acc.status, acc.tags)
            )
        await conn.commit()
    conn.close()
    return {"message": f"Imported {len(accounts)} email accounts"}


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
                INSERT INTO email_accounts
                (email_address, email_password, protocol, host, port, status, created_at, tags)
                VALUES (%s, %s, %s, %s, %s, %s, NOW(), %s)
                """,
                (
                    row.get("email"),
                    row.get("password"),
                    row.get("protocol"),
                    row.get("host"),
                    row.get("port"),
                    row.get("status", "active"),
                    row.get("tags")
                )
            )
            count += 1
        await conn.commit()
    conn.close()

    return {"message": f"Imported {count} email accounts"}
