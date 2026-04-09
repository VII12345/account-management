"""
主后端 FastAPI 应用入口模块。

职责：创建应用实例、挂载各业务路由、配置中间件与统一启动行为。
边界：入口文件负责组装，不应堆积具体业务实现细节。
"""

from fastapi import FastAPI
from auth import router as auth_router
from accounts import router as accounts_router
from accounts import ensure_accounts_schema
from email_accounts import router as email_accounts_router
from virtual_people import router as virtual_people_router

app = FastAPI(title="养号系统后端")  

app.include_router(auth_router)            
app.include_router(accounts_router)
app.include_router(email_accounts_router)
app.include_router(virtual_people_router)


@app.on_event("startup")
async def startup_event():
    await ensure_accounts_schema()

@app.get("/")
def root():
    return {"message": "养号系统后端运行正常"}
