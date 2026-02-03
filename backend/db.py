# db.py
import aiomysql

async def get_conn():
    return await aiomysql.connect(
        host="165.154.4.83",
        port=3306,
        user="root",
        password="Ww2689058228",
        db="account_db",
        autocommit=False
    )
