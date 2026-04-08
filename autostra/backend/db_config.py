import os
from dataclasses import dataclass

import aiomysql


@dataclass
class DBConfig:
    host: str = "hk.xzzzs.icu"
    port: int = 3306
    user: str = "root"
    password: str = "`123456789Xzz"
    database: str = "account_db"


def get_db_config() -> DBConfig:
    return DBConfig(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "`123456789Xzz"),
        database=os.getenv("DB_NAME", "account_db"),
    )


async def get_db_conn():
    config = get_db_config()
    return await aiomysql.connect(
        host=config.host,
        port=config.port,
        user=config.user,
        password=config.password,
        db=config.database,
        autocommit=False,
        charset="utf8mb4",
    )
