from datetime import date, datetime
from decimal import Decimal

from pgvector.sqlalchemy import Vector
from sqlalchemy import (
    JSON,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Source(Base):
    __tablename__ = "sources"
    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    company: Mapped[str] = mapped_column(String(16), index=True)
    title: Mapped[str] = mapped_column(Text)
    publisher: Mapped[str] = mapped_column(String(120))
    url: Mapped[str] = mapped_column(Text)
    publication_date: Mapped[date | None] = mapped_column()
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    retrieved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    checksum: Mapped[str] = mapped_column(String(64))
    stored_checksum: Mapped[str] = mapped_column(String(64))
    storage_key: Mapped[str] = mapped_column(Text)
    document_type: Mapped[str] = mapped_column(String(50))
    accession: Mapped[str | None] = mapped_column(String(30))
    accounting_basis: Mapped[str] = mapped_column(String(40))
    capture_kind: Mapped[str] = mapped_column(String(50))


class Fact(Base):
    __tablename__ = "financial_facts"
    __table_args__ = (
        UniqueConstraint(
            "source_id", "metric", "period_end", "period_kind", name="uq_fact_source_period"
        ),
        CheckConstraint("period_end >= period_start", name="valid_period"),
        CheckConstraint("unit_scale > 0", name="positive_scale"),
    )
    id: Mapped[str] = mapped_column(String(120), primary_key=True)
    source_id: Mapped[str] = mapped_column(ForeignKey("sources.id"), index=True)
    company: Mapped[str] = mapped_column(String(16), index=True)
    metric: Mapped[str] = mapped_column(String(50), index=True)
    value: Mapped[Decimal] = mapped_column(Numeric(30, 8))
    currency: Mapped[str] = mapped_column(String(3))
    unit_scale: Mapped[int] = mapped_column()
    period_start: Mapped[date | None] = mapped_column()
    period_end: Mapped[date] = mapped_column(index=True)
    period_kind: Mapped[str] = mapped_column(String(12))
    fiscal_label: Mapped[str] = mapped_column(String(20))
    locator: Mapped[str] = mapped_column(Text)
    classification: Mapped[str] = mapped_column(String(24), default="reported_fact")
    transformations: Mapped[dict] = mapped_column(JSON)


class Chunk(Base):
    __tablename__ = "chunks"
    id: Mapped[str] = mapped_column(String(120), primary_key=True)
    source_id: Mapped[str] = mapped_column(ForeignKey("sources.id"), index=True)
    company: Mapped[str] = mapped_column(String(16), index=True)
    text: Mapped[str] = mapped_column(Text)
    locator: Mapped[str] = mapped_column(Text)
    topic: Mapped[str] = mapped_column(String(40), index=True)
    period_end: Mapped[date] = mapped_column(index=True)
    embedding: Mapped[list[float]] = mapped_column(Vector(384))
    embedding_id: Mapped[str] = mapped_column(Text)


Index(
    "chunks_embedding_hnsw",
    Chunk.embedding,
    postgresql_using="hnsw",
    postgresql_ops={"embedding": "vector_cosine_ops"},
)
