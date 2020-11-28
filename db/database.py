from conf import DB_SETTINGS, REDIS_SETTINGS
from db.db_connection import SQLAlchemyDB, RedisDB


class DBSettings:
    """Import the database settings from global settings file(conf/settings)"""

    def __init__(self,
                 settings_file_key: str,
                 url_key='db_url',
                 autocommit_key='autocommit',
                 autoflush_key='autoflush',
                 connect_args_key='connect_args'):
        self._url = DB_SETTINGS[settings_file_key].get(url_key)
        self._autocommit = DB_SETTINGS[settings_file_key].get(autocommit_key, False)
        self._autoflush = DB_SETTINGS[settings_file_key].get(autoflush_key, False)
        self._connect_args = DB_SETTINGS[settings_file_key].get(connect_args_key, None)

    @property
    def url(self):
        """Get the database driver url"""
        return self._url

    @property
    def auto_commit(self):
        """Get the database autocommit property"""
        return self._autocommit

    @property
    def auto_flush(self):
        """Get the database autoflush property"""
        return self._autoflush

    @property
    def connect_args(self):
        """Get the database connect_args property"""
        return self._connect_args


class RedisSettings:
    """Import the redis settings from global settings file(conf/settings)"""

    def __init__(self,
                 host_key='host',
                 port_key='port',
                 db_key='db',
                 password_key='connect_args',
                 connection_pool_key='connection_pool'):
        self._host = REDIS_SETTINGS.get(host_key, 'localhost')
        self._port = REDIS_SETTINGS.get(port_key, 6379)
        self._db = REDIS_SETTINGS.get(db_key, 0)
        self._password = REDIS_SETTINGS.get(password_key, None)
        self._connection_pool = REDIS_SETTINGS.get(connection_pool_key, None)

    @property
    def host(self):
        """Get the database driver url"""
        return self._host

    @property
    def port(self):
        """Get the database autocommit property"""
        return self._port

    @property
    def db(self):
        """Get the database autoflush property"""
        return self._db

    @property
    def password(self):
        """Get the database connect_args property"""
        return self._password

    @property
    def connection_pool(self):
        """Get the database connect_args property"""
        return self._connection_pool


_sql = DBSettings('SQL')
_search_engine = DBSettings('SEARCH_ENGINES')
_redis = RedisSettings()

SQL_engine, SQL_SessionLocal, SQL_Base = SQLAlchemyDB(url=_sql.url,
                                                      autocommit=_sql.auto_commit,
                                                      autoflush=_sql.auto_flush,
                                                      connect_args=_sql.connect_args).get_connection()

SE_engine, SE_SessionLocal, SE_Base = SQLAlchemyDB(url=_search_engine.url,
                                                   autocommit=_search_engine.auto_commit,
                                                   autoflush=_search_engine.auto_flush,
                                                   connect_args=_search_engine.connect_args).get_connection()

REDIS_CONNECTION = RedisDB(host=_redis.host, port=_redis.port, db=_redis.db, password=_redis.password,
                           connection_pool=_redis.connection_pool).connection
