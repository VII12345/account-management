"""
虚拟人管理路由模块。

职责：提供虚拟人实体的增删改查、状态维护和关联查询能力。
边界：仅关注虚拟人资源，不承担账号认证与代理验证功能。
"""

# virtual_people.py
import uuid
import json
import aiomysql
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from db import get_conn

router = APIRouter(prefix="/virtual-people", tags=["Virtual People"])

# 创建虚拟人请求模型
class VirtualPersonCreate(BaseModel):
    name: str
    gender: str
    age: int
    position: str
    region: str | None = None
    group_name: str | None = None
    avatar_url: str | None = None
    tags: list[str] | None = None

# 返回模型（可选）
class VirtualPerson(BaseModel):
    id: str
    name: str
    gender: str
    age: int
    position: str
    region: str | None
    group_name: str | None
    avatar_url: str | None
    tags: list[str] | None


def parse_tags(value):
    if not value:
        return None
    try:
        parsed = json.loads(value)
        return parsed if isinstance(parsed, list) else None
    except Exception:
        return None


@router.get("/")
async def list_virtual_people():
    conn = await get_conn()
    try:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                SELECT id, name, gender, age, position, region, group_name, avatar_url, tags
                FROM virtual_people
                ORDER BY id DESC
                """
            )
            rows = await cur.fetchall()

        data = []
        for row in rows:
            data.append(
                {
                    "id": row[0],
                    "name": row[1],
                    "gender": row[2],
                    "age": row[3],
                    "position": row[4],
                    "region": row[5],
                    "group_name": row[6],
                    "avatar_url": row[7],
                    "tags": parse_tags(row[8]),
                }
            )

        return {"data": data, "total": len(data)}
    finally:
        conn.close()


@router.get("/{person_id}")
async def get_virtual_person(person_id: str):
    conn = await get_conn()
    try:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                SELECT id, name, gender, age, position, region, group_name, avatar_url, tags
                FROM virtual_people
                WHERE id=%s
                LIMIT 1
                """,
                (person_id,),
            )
            row = await cur.fetchone()

        if not row:
            raise HTTPException(status_code=404, detail="Virtual person not found")

        return {
            "id": row[0],
            "name": row[1],
            "gender": row[2],
            "age": row[3],
            "position": row[4],
            "region": row[5],
            "group_name": row[6],
            "avatar_url": row[7],
            "tags": parse_tags(row[8]),
        }
    finally:
        conn.close()


@router.post("/")
async def create_virtual_person(data: VirtualPersonCreate):
    person_id = str(uuid.uuid4())

    conn = await get_conn()
    async with conn.cursor() as cur:
        await cur.execute(
            """
            INSERT INTO virtual_people
            (id, name, gender, age, position, region, group_name, avatar_url, tags)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """,
            (
                person_id,
                data.name,
                data.gender,
                data.age,
                data.position,
                data.region,
                data.group_name,
                data.avatar_url,
                json.dumps(data.tags) if data.tags else None
            )
        )
        await conn.commit()

    conn.close()
    return {"message": "虚拟人创建成功", "id": person_id}
