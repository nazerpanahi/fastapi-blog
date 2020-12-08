from db.database import SQL_SessionLocal, REDIS_CONNECTION


def get_sql_db():
    sql_db = SQL_SessionLocal()
    try:
        yield sql_db
    finally:
        sql_db.close()


def get_redis_db():
    try:
        yield REDIS_CONNECTION
    finally:
        REDIS_CONNECTION.close()
