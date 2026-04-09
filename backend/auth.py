"""
认证与会话管理路由模块。

职责：处理登录、令牌校验、会话状态维护等鉴权相关接口。
边界：仅负责认证安全域，不承载账号中心的业务读写。
"""

# auth.py
import aiomysql
import bcrypt
import jwt
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
import uuid
from db import get_conn

SECRET_KEY = "your_jwt_secret"
ALGORITHM = "HS256"

router = APIRouter(prefix="/auth", tags=["Auth"])

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class ResetPasswordRequest(BaseModel):
    email: EmailStr
    new_password: str


@router.post("/register")
async def register(data: RegisterRequest):
    conn = await get_conn()
    async with conn.cursor() as cur:
        await cur.execute("SELECT id FROM system_users WHERE email=%s", (data.email,))
        if await cur.fetchone():
            raise HTTPException(status_code=400, detail="该邮箱已被注册")

        hashed = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt())
        user_id = str(uuid.uuid4())

        await cur.execute(
            "INSERT INTO system_users (id, email, password_hash) VALUES (%s,%s,%s)",
            (user_id, data.email, hashed.decode())
        )
        await conn.commit()

    conn.close()
    return {"message": "注册成功", "user_id": user_id}


@router.post("/login")
async def login(data: LoginRequest):
    conn = await get_conn()
    async with conn.cursor(aiomysql.DictCursor) as cur:
        await cur.execute("SELECT * FROM system_users WHERE email=%s", (data.email,))
        user = await cur.fetchone()
    conn.close()

    if not user:
        raise HTTPException(status_code=401, detail="用户不存在")

    if not bcrypt.checkpw(data.password.encode(), user["password_hash"].encode()):
        raise HTTPException(status_code=401, detail="密码错误")

    token = jwt.encode(
        {"user_id": user["id"], "email": user["email"]},
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {"access_token": token, "user": {"id": user["id"], "email": user["email"]}}


@router.post("/reset-password")
async def reset_password(data: ResetPasswordRequest):
    conn = await get_conn()
    async with conn.cursor() as cur:
        hashed = bcrypt.hashpw(data.new_password.encode(), bcrypt.gensalt())
        await cur.execute(
            "UPDATE system_users SET password_hash=%s WHERE email=%s",
            (hashed.decode(), data.email)
        )
        await conn.commit()

    conn.close()
    return {"message": "密码已重置"}
