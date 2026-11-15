from datetime import date

from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from semiconductor_research.database.models import Chunk, Source
from semiconductor_research.documents.embedding import EmbeddingProvider
from semiconductor_research.financials.engine import cutoff


class RetrievalFilters(BaseModel):
    model_config = ConfigDict(extra="forbid")
    company: str = Field(default="NVDA", pattern=r"^[A-Z]{1,6}$")
    as_of: date = date(2025, 3, 1)
    document_type: str | None = Field(default=None, max_length=50)
    publication_from: date | None = None
    period_end: date | None = None
    topic: str | None = Field(default=None, max_length=40)


def retrieve(
    session: Session, encoder: EmbeddingProvider, question: str, filters: RetrievalFilters, k=4
):
    vector = encoder.encode([question])[0]
    conditions = [
        Chunk.company == filters.company,
        Source.published_at <= cutoff(filters.as_of),
        Chunk.embedding_id == encoder.identifier,
    ]
    if filters.document_type:
        conditions.append(Source.document_type == filters.document_type)
    if filters.publication_from:
        conditions.append(
            Source.published_at
            >= cutoff(filters.publication_from).replace(hour=0, minute=0, second=0, microsecond=0)
        )
    if filters.period_end:
        conditions.append(Chunk.period_end == filters.period_end)
    if filters.topic:
        conditions.append(Chunk.topic == filters.topic)
    base = select(Chunk, Source).join(Source, Source.id == Chunk.source_id).where(*conditions)
    semantic = session.execute(
        base.add_columns((1 - Chunk.embedding.cosine_distance(vector)).label("cosine"))
        .order_by(Chunk.embedding.cosine_distance(vector))
        .limit(16)
    ).all()
    query = func.websearch_to_tsquery("english", question)
    rank = func.ts_rank_cd(func.to_tsvector("english", Chunk.text), query)
    lexical = session.execute(
        base.add_columns(rank.label("lexical"))
        .where(func.to_tsvector("english", Chunk.text).op("@@")(query))
        .order_by(rank.desc(), Chunk.id)
        .limit(16)
    ).all()
    scores, data = {}, {}
    for ranking in (semantic, lexical):
        for position, row in enumerate(ranking, 1):
            chunk, source, _ = row
            scores[chunk.id] = scores.get(chunk.id, 0) + 1 / (60 + position)
            data[chunk.id] = (chunk, source)
    cosine = {c.id: float(score) for c, _, score in semantic}
    qualified = [key for key in scores if cosine.get(key, -1) >= 0.38]
    results = []
    for key in sorted(qualified, key=lambda x: (-scores[x], x))[:k]:
        chunk, source = data[key]
        results.append(
            {
                "citation_id": len(results) + 1,
                "chunk_id": chunk.id,
                "source_id": source.id,
                "text": chunk.text,
                "company": chunk.company,
                "topic": chunk.topic,
                "period_end": str(chunk.period_end),
                "published_at": source.published_at.isoformat(),
                "locator": chunk.locator,
                "url": source.url,
                "title": source.title,
                "document_checksum": source.checksum,
                "cosine_similarity": round(cosine[key], 5),
                "rank_fusion_score": round(scores[key], 8),
            }
        )
    return results
