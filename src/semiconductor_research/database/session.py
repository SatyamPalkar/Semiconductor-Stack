from contextlib import contextmanager
from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from semiconductor_research.config.settings import settings


@lru_cache
def engine():
    return create_engine(settings().database_url, pool_pre_ping=True, pool_size=3, max_overflow=1)


@contextmanager
def session_scope():
    with Session(engine()) as session, session.begin():
        yield session
