"""
邮箱验证路由模块。

职责：执行邮箱连通性、登录有效性或验证码相关验证流程。
边界：仅处理验证动作，不负责邮箱账号主数据维护。
"""

# email_verify.py
import imaplib
import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from db import get_conn

router = APIRouter(prefix="/email", tags=["Email Verification"])


class EmailVerifyRequest(BaseModel):
    email: EmailStr
    password: str
    protocol: str = "imap"
    host: str
    port: int
    proxy_id: str | None = None


def verify_imap(email, password, host, port):
    try:
        mail = imaplib.IMAP4_SSL(host, port)
        mail.login(email, password)
        mail.logout()
        return True, None
    except Exception as e:
        return False, str(e)


@router.post("/verify")
async def verify_email(data: EmailVerifyRequest):
    if data.protocol.lower() != "imap":
        raise HTTPException(status_code=400, detail="目前仅支持 IMAP 验证")

    success, error = verify_imap(
        data.email,
        data.password,
        data.host,
        data.port
    )

    # 写入数据库 email_accounts（如果你需要）
    conn = await get_conn()
    async with conn.cursor() as cur:
        email_id = str(uuid.uuid4())
        await cur.execute(
            """
            INSERT INTO email_accounts
            (id, email_address, email_password, protocol, host, port, last_login_status, last_error, proxy_id)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                email_id,
                data.email,
                data.password,
                data.protocol,
                data.host,
                data.port,
                "success" if success else "fail",
                error,
                data.proxy_id
            )
        )
        await conn.commit()
    conn.close()

    return {
        "email": data.email,
        "success": success,
        "error": error
    }
