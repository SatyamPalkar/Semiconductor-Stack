from alembic import context

from semiconductor_research.database.models import Base
from semiconductor_research.database.session import engine

with engine().connect() as connection:
    context.configure(connection=connection, target_metadata=Base.metadata)
    with context.begin_transaction():
        context.run_migrations()
