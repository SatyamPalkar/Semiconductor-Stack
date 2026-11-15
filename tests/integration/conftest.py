import os

import pytest
from sqlalchemy.orm import Session


@pytest.fixture
def session():
    if os.environ.get("RUN_DB_TESTS") != "1":
        pytest.skip("Set RUN_DB_TESTS=1 after preparing the isolated PostgreSQL/pgvector database")
    from semiconductor_research.database.session import engine

    with engine().connect() as connection:
        transaction = connection.begin()
        with Session(bind=connection, join_transaction_mode="create_savepoint") as session:
            yield session
        transaction.rollback()


@pytest.fixture(scope="session")
def encoder():
    from semiconductor_research.documents.embedding import MiniLM

    return MiniLM()
