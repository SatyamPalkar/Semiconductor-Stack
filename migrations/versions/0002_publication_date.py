"""Separate the stated publication date from the conservative availability cutoff."""

import sqlalchemy as sa
from alembic import op

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("sources", sa.Column("publication_date", sa.Date, nullable=True))
    op.execute(
        "UPDATE sources SET publication_date = DATE '2025-02-26' WHERE id LIKE 'nvda-fy2025-%'"
    )


def downgrade():
    op.drop_column("sources", "publication_date")
