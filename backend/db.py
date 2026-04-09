"""
数据库连接与基础访问模块。

职责：管理数据库连接池、基础查询执行与通用数据库工具函数。
边界：仅提供通用持久化能力，不包含业务规则判断。
"""

import aiomysql

async def get_conn():
    return await aiomysql.connect(
        host="127.0.0.1",
        port=3306,
        user="appuser",
        password="AppUser123!",   
        db="account_db",
        autocommit=False
    )
