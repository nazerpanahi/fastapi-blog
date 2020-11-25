from db.database import SQL_SessionLocal, SE_SessionLocal


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
