"""
代理验证路由模块。

职责：校验代理可用性、连接质量与基础连通状态，供任务执行前置检查使用。
边界：仅做验证，不负责代理池生命周期管理。
"""

# proxy_verify.py
import time
import uuid
import requests
from fastapi import APIRouter
from pydantic import BaseModel
from db import get_conn

router = APIRouter(prefix="/proxy", tags=["Proxy Verification"])


class ProxyVerifyRequest(BaseModel):
    proxy: str  # 例如 socks5://user:pass@1.2.3.4:1080


def verify_proxy(proxy_url):
    proxies = {
        "http": proxy_url,
        "https": proxy_url
    }
    try:
        start = time.time()
        r = requests.get("https://www.google.com", proxies=proxies, timeout=5)
        latency = (time.time() - start) * 1000
        return True, latency, None
    except Exception as e:
        return False, None, str(e)


@router.post("/verify")
async def verify_proxy_api(data: ProxyVerifyRequest):
    success, latency, error = verify_proxy(data.proxy)

    # 写入数据库 proxies（如果你需要）
    conn = await get_conn()
    async with conn.cursor() as cur:
        proxy_id = str(uuid.uuid4())
        await cur.execute(
            """
            INSERT INTO proxies
            (id, proxy_url, last_check_status, latency_ms, last_error)
            VALUES (%s,%s,%s,%s,%s)
            """,
            (
                proxy_id,
                data.proxy,
                "success" if success else "fail",
                latency,
                error
            )
        )
        await conn.commit()
    conn.close()

    return {
        "proxy": data.proxy,
        "success": success,
        "latency_ms": latency,
        "error": error
    }
