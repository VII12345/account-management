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
