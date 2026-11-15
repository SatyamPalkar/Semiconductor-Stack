"""Do not infer unreported start dates from annual-period end labels."""

import sqlalchemy as sa
from alembic import op

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade():
    for constraint in sa.inspect(op.get_bind()).get_unique_constraints("financial_facts"):
        if constraint["column_names"] == [
            "source_id",
            "metric",
            "period_start",
            "period_end",
            "period_kind",
        ]:
            op.drop_constraint(constraint["name"], "financial_facts", type_="unique")
    op.create_unique_constraint(
        "uq_fact_source_period",
        "financial_facts",
        ["source_id", "metric", "period_end", "period_kind"],
    )
    op.alter_column("financial_facts", "period_start", existing_type=sa.Date(), nullable=True)
    op.execute(
        "UPDATE financial_facts SET period_start = NULL WHERE source_id LIKE 'nvda-fy2025-%'"
    )


def downgrade():
    # Keep the newly nullable column rather than inventing dates during rollback.
    # The earlier schema's NOT NULL constraint can be restored only after a human
    # supplies verified starts; refuse to fabricate those values.
    missing = op.get_bind().scalar(
        sa.text("SELECT count(*) FROM financial_facts WHERE period_start IS NULL")
    )
    if missing:
        raise RuntimeError(
            "Cannot roll back without verified reporting-period starts; export/preserve data first"
        )
    op.drop_constraint("uq_fact_source_period", "financial_facts", type_="unique")
    op.create_unique_constraint(
        None,
        "financial_facts",
        ["source_id", "metric", "period_start", "period_end", "period_kind"],
    )
    op.alter_column("financial_facts", "period_start", existing_type=sa.Date(), nullable=False)
