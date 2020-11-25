from conf.settings import DB_SETTINGS
from db.db_connection import SQLAlchemyDB


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


_sql = DBSettings('SQL')
_search_engine = DBSettings('SEARCH_ENGINES')

SQL_engine, SQL_SessionLocal, SQL_Base = SQLAlchemyDB(url=_sql.url,
                                                      autocommit=_sql.auto_commit,
                                                      autoflush=_sql.auto_flush,
                                                      connect_args=_sql.connect_args).get_connection()

SE_engine, SE_SessionLocal, SE_Base = SQLAlchemyDB(url=_search_engine.url,
                                                   autocommit=_search_engine.auto_commit,
                                                   autoflush=_search_engine.auto_flush,
                                                   connect_args=_search_engine.connect_args).get_connection()
