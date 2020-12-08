from redis import Redis, ConnectionPool
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class SQLAlchemyDB:
    def __init__(self, url, connect_args=None, autocommit=False, autoflush=False):
        self.url = url
        self.connect_args = connect_args
        self.autocommit = autocommit
        self.autoflush = autoflush
        self.engine = None
        self.SessionLocal = None
        self.Base = None

    def _make_engine(self):
        if self.connect_args is None:
            engine = create_engine(self.url)
        else:
            engine = create_engine(self.url, connect_args=self.connect_args)
        return engine

    def _make_session(self, engine):
        return sessionmaker(autocommit=self.autocommit, autoflush=self.autoflush, bind=engine)

    def _get_engine(self):
        if self.engine is None:
            self.engine = self._make_engine()
        return self.engine

    def _get_session_local(self):
        if self.SessionLocal is None:
            self.SessionLocal = self._make_session(self._get_engine())
        return self.SessionLocal

    def _get_base(self):
        if self.Base is None:
            self.Base = declarative_base()
        return self.Base

    def get_connection(self):
        if self._get_engine() is None or self._get_session_local() is None or self._get_base() is None:
            self.engine = self._get_engine()
            self.SessionLocal = self._get_session_local()
            self.Base = self._get_base()
        return self.engine, self.SessionLocal, self.Base

    def _make_new_connection(self):
        self.engine = self._make_engine()
        self.SessionLocal = self._make_session(engine=self.engine)
        self.Base = declarative_base()
        return self.engine, self.SessionLocal, self.Base


class RedisDB:
    def __init__(self, host='localhost', port=6379,
                 db=0, password=None, connection_pool=None):
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.connection_pool = connection_pool

        self._connection = Redis(
            host=host,
            port=port,
            db=db,
            password=password,
            connection_pool=connection_pool
        )

    @property
    def connection(self) -> Redis:
        return self._connection

    @staticmethod
    def make_connection_pool():
        return ConnectionPool()
