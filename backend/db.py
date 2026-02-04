# db.py
import aiomysql


async def get_conn():
    return await aiomysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="050614Xzz",
        db="account_db",
        autocommit=False,
    )
