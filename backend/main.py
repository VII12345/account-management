# main.py
from fastapi import FastAPI
from auth import router as auth_router
from accounts import router as accounts_router


app = FastAPI(title="养号系统后端")

app.include_router(auth_router)
app.include_router(accounts_router)
@app.get("/")
def root():
    return {"message": "养号系统后端运行正常"}
