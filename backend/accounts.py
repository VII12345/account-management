# accounts.py
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
    account_ip: str | None = None
    account_port: int | None = None


DEFAULT_ACCOUNT_IP = "hk.xzzzs.icu"
BASE_ACCOUNT_PORT = 9220


async def ensure_accounts_schema():
    conn = await get_conn()
    try:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                SELECT column_name
                FROM information_schema.columns
                WHERE table_schema = DATABASE() AND table_name='accounts'
                """
            )
            existing_columns = {name for (name,) in await cur.fetchall()}

            if "account_ip" not in existing_columns:
                await cur.execute("ALTER TABLE accounts ADD COLUMN account_ip VARCHAR(255) NULL")

            if "account_port" not in existing_columns:
                await cur.execute("ALTER TABLE accounts ADD COLUMN account_port INT NULL")

            # 回填为空的账号 IP
            await cur.execute(
                """
                UPDATE accounts
                SET account_ip=%s
                WHERE account_ip IS NULL OR account_ip=''
                """,
                (DEFAULT_ACCOUNT_IP,),
            )

            # 端口按 id 升序从 9220 开始回填，仅回填空值
            await cur.execute(
                """
                SELECT id
                FROM accounts
                WHERE account_port IS NULL
                ORDER BY id ASC
                """
            )
            missing_port_ids = [acc_id for (acc_id,) in await cur.fetchall()]

            await cur.execute("SELECT COALESCE(MAX(account_port), %s) FROM accounts", (BASE_ACCOUNT_PORT - 1,))
            current_max_port = (await cur.fetchone())[0]

            next_port = max(current_max_port + 1, BASE_ACCOUNT_PORT)
            for acc_id in missing_port_ids:
                await cur.execute(
                    "UPDATE accounts SET account_port=%s WHERE id=%s",
                    (next_port, acc_id),
                )
                next_port += 1

        await conn.commit()
    finally:
        conn.close()


async def get_next_account_port(cur):
    await cur.execute("SELECT COALESCE(MAX(account_port), %s) FROM accounts", (BASE_ACCOUNT_PORT - 1,))
    current_max_port = (await cur.fetchone())[0]
    return max(current_max_port + 1, BASE_ACCOUNT_PORT)


# -------------------------
# 创建账号（前端手动添加）
# -------------------------
@router.post("/")
async def create_account(data: Account):
    conn = await get_conn()
    async with conn.cursor() as cur:
        account_ip = data.account_ip or DEFAULT_ACCOUNT_IP
        account_port = data.account_port
        if account_port is None:
            account_port = await get_next_account_port(cur)

        await cur.execute(
            """
            INSERT INTO accounts (platform, username, password, email, phone, status, created_at, tags, account_ip, account_port)
            VALUES (%s, %s, %s, %s, %s, %s, NOW(), %s, %s, %s)
            """,
            (
                data.platform,
                data.username,
                data.password,
                data.email,
                data.phone,
                data.status,
                data.tags,
                account_ip,
                account_port,
            )
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
        account_ip = data.account_ip or DEFAULT_ACCOUNT_IP
        account_port = data.account_port
        if account_port is None:
            await cur.execute("SELECT account_port FROM accounts WHERE id=%s", (acc_id,))
            row = await cur.fetchone()
            if not row:
                raise HTTPException(404, "Account not found")
            account_port = row[0]

        await cur.execute(
            """
            UPDATE accounts
            SET platform=%s, username=%s, password=%s, email=%s, phone=%s, status=%s, tags=%s, account_ip=%s, account_port=%s
            WHERE id=%s
            """,
            (
                data.platform,
                data.username,
                data.password,
                data.email,
                data.phone,
                data.status,
                data.tags,
                account_ip,
                account_port,
                acc_id,
            )
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
        next_port = await get_next_account_port(cur)
        for acc in accounts:
            account_ip = acc.account_ip or DEFAULT_ACCOUNT_IP
            account_port = acc.account_port if acc.account_port is not None else next_port
            if acc.account_port is None:
                next_port += 1

            await cur.execute(
                """
                INSERT INTO accounts (platform, username, password, email, phone, status, created_at, tags, account_ip, account_port)
                VALUES (%s, %s, %s, %s, %s, %s, NOW(), %s, %s, %s)
                """,
                (
                    acc.platform,
                    acc.username,
                    acc.password,
                    acc.email,
                    acc.phone,
                    acc.status,
                    acc.tags,
                    account_ip,
                    account_port,
                )
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
        next_port = await get_next_account_port(cur)
        count = 0
        for row in reader:
            csv_port = row.get("account_port")
            account_port = int(csv_port) if csv_port not in (None, "") else next_port
            if csv_port in (None, ""):
                next_port += 1

            await cur.execute(
                """
                INSERT INTO accounts (platform, username, password, email, phone, status, created_at, tags, account_ip, account_port)
                VALUES (%s, %s, %s, %s, %s, %s, NOW(), %s, %s, %s)
                """,
                (
                    row.get("platform"),
                    row.get("username"),
                    row.get("password"),
                    row.get("email"),
                    row.get("phone"),
                    row.get("status", "active"),
                    row.get("tags"),
                    row.get("account_ip") or DEFAULT_ACCOUNT_IP,
                    account_port,
                )
            )
            count += 1
        await conn.commit()
    conn.close()

    return {"message": f"Imported {count} accounts"}
