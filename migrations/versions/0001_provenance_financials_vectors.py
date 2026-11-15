"""Initial provenance, reported facts and vector retrieval schema."""

import sqlalchemy as sa
from alembic import op
from pgvector.sqlalchemy import Vector

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.create_table(
        "sources",
        sa.Column("id", sa.String(100), primary_key=True),
        sa.Column("company", sa.String(16), nullable=False),
        sa.Column("title", sa.Text, nullable=False),
        sa.Column("publisher", sa.String(120), nullable=False),
        sa.Column("url", sa.Text, nullable=False),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("retrieved_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("checksum", sa.String(64), nullable=False),
        sa.Column("stored_checksum", sa.String(64), nullable=False),
        sa.Column("storage_key", sa.Text, nullable=False),
        sa.Column("document_type", sa.String(50), nullable=False),
        sa.Column("accession", sa.String(30)),
        sa.Column("accounting_basis", sa.String(40), nullable=False),
        sa.Column("capture_kind", sa.String(50), nullable=False),
    )
    op.create_table(
        "financial_facts",
        sa.Column("id", sa.String(120), primary_key=True),
        sa.Column("source_id", sa.String(100), sa.ForeignKey("sources.id"), nullable=False),
        sa.Column("company", sa.String(16), nullable=False),
        sa.Column("metric", sa.String(50), nullable=False),
        sa.Column("value", sa.Numeric(30, 8), nullable=False),
        sa.Column("currency", sa.String(3), nullable=False),
        sa.Column("unit_scale", sa.Integer, nullable=False),
        sa.Column("period_start", sa.Date, nullable=False),
        sa.Column("period_end", sa.Date, nullable=False),
        sa.Column("period_kind", sa.String(12), nullable=False),
        sa.Column("fiscal_label", sa.String(20), nullable=False),
        sa.Column("locator", sa.Text, nullable=False),
        sa.Column("classification", sa.String(24), nullable=False),
        sa.Column("transformations", sa.JSON, nullable=False),
        sa.UniqueConstraint("source_id", "metric", "period_start", "period_end", "period_kind"),
        sa.CheckConstraint("period_end >= period_start", name="valid_period"),
        sa.CheckConstraint("unit_scale > 0", name="positive_scale"),
    )
    op.create_table(
        "chunks",
        sa.Column("id", sa.String(120), primary_key=True),
        sa.Column("source_id", sa.String(100), sa.ForeignKey("sources.id"), nullable=False),
        sa.Column("company", sa.String(16), nullable=False),
        sa.Column("text", sa.Text, nullable=False),
        sa.Column("locator", sa.Text, nullable=False),
        sa.Column("topic", sa.String(40), nullable=False),
        sa.Column("period_end", sa.Date, nullable=False),
        sa.Column("embedding", Vector(384), nullable=False),
        sa.Column("embedding_id", sa.Text, nullable=False),
    )
    op.create_index(
        "chunks_embedding_hnsw",
        "chunks",
        ["embedding"],
        postgresql_using="hnsw",
        postgresql_ops={"embedding": "vector_cosine_ops"},
    )
    op.execute("CREATE INDEX chunks_text_gin ON chunks USING gin (to_tsvector('english', text))")
    op.create_index("sources_available_company", "sources", ["company", "published_at"])
    op.create_index("facts_company_period", "financial_facts", ["company", "period_end", "metric"])


def downgrade():
    op.drop_table("chunks")
    op.drop_table("financial_facts")
    op.drop_table("sources")
