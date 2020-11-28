from db.database import SQL_SessionLocal, SE_SessionLocal, REDIS_CONNECTION


def get_sql_db():
    sql_db = SQL_SessionLocal()
    try:
        yield sql_db
    finally:
        sql_db.close()


def get_search_engine_db():
    se_db = SE_SessionLocal()
    try:
        yield se_db
    finally:
        se_db.close()


def get_redis_db():
    try:
        yield REDIS_CONNECTION
    finally:
        REDIS_CONNECTION.close()
