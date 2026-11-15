import hashlib
import json
from datetime import UTC, date, datetime

import httpx
from sqlalchemy import select
from sqlalchemy.orm import Session

from semiconductor_research.config.settings import ROOT, settings
from semiconductor_research.database.models import Chunk, Fact, Source
from semiconductor_research.documents.chunking import fact_chunks
from semiconductor_research.documents.embedding import EmbeddingProvider
from semiconductor_research.ingestion.nvidia import parse_nvidia
from semiconductor_research.sources.catalog import NVIDIA
from semiconductor_research.storage.local import LocalStorage


def ingest_nvidia(session: Session, encoder: EmbeddingProvider, *, recorded=False, offline=False):
    conf = settings()
    if recorded:
        content = (ROOT / "data/fixtures/nvda-fy2025-tables.html").read_bytes()
        metadata = json.loads((ROOT / "data/fixtures/nvda-fy2025-metadata.json").read_text())
        if hashlib.sha256(content).hexdigest() != metadata["extract_sha256"]:
            raise ValueError("Recorded excerpt checksum mismatch")
        original_checksum = metadata["original_sha256"]
        retrieved_at = datetime.fromisoformat(metadata["retrieved_at"])
    elif offline:
        metadata = next(
            x
            for x in json.loads((conf.storage_root / "retrieval.json").read_text())
            if x["id"] == NVIDIA["key"]
        )
        content = (conf.storage_root / metadata["filename"]).read_bytes()
        original_checksum = hashlib.sha256(content).hexdigest()
        if original_checksum != metadata["sha256"]:
            raise ValueError("Stored original checksum mismatch")
        retrieved_at = datetime.fromisoformat(metadata["retrieved_at"])
    else:
        # Fixed catalog URL, one bounded request; user questions never become URLs.
        with httpx.Client(timeout=30, follow_redirects=False) as client:
            response = client.get(
                NVIDIA["url"],
                headers={"User-Agent": "SemiconductorResearchPlatform/0.1 (personal research)"},
            )
            if response.status_code != 200 or len(response.content) > 5_000_000:
                raise RuntimeError(
                    "Official source unavailable; no automatic retry or access-control bypass"
                )
            content = response.content
        original_checksum = hashlib.sha256(content).hexdigest()
        retrieved_at = datetime.now(UTC)
    facts = parse_nvidia(content)
    source_id = f"{NVIDIA['key']}-{original_checksum[:16]}"
    existing = session.get(Source, source_id)
    if existing:
        ids = session.scalars(select(Chunk.embedding_id).where(Chunk.source_id == source_id)).all()
        if not ids or any(x != encoder.identifier for x in ids):
            raise ValueError("Existing chunks use another encoder; rebuild explicitly")
        return source_id, False
    source = Source(
        id=source_id,
        company=NVIDIA["company"],
        title=NVIDIA["title"],
        publisher=NVIDIA["publisher"],
        url=NVIDIA["url"],
        publication_date=date.fromisoformat(NVIDIA["publication_date"]),
        published_at=NVIDIA["published_at"],
        retrieved_at=retrieved_at,
        checksum=original_checksum,
        stored_checksum=hashlib.sha256(content).hexdigest(),
        storage_key=LocalStorage(conf.storage_root).put(content, "html"),
        document_type=NVIDIA["document_type"],
        accession=None,
        accounting_basis=NVIDIA["accounting_basis"],
        capture_kind="recorded_primary_source_excerpt" if recorded else "original_primary_source",
    )
    session.add(source)
    session.flush()
    chunks = fact_chunks(facts)
    embeddings = encoder.encode([c["text"] for c in chunks])
    if len(embeddings) != len(chunks):
        raise ValueError("Encoder returned the wrong vector count")
    for fact, chunk, vector in zip(facts, chunks, embeddings, strict=True):
        fact_id = f"{source_id}:{fact['fiscal_label']}:{fact['metric']}"
        session.add(Fact(id=fact_id, source_id=source_id, company="NVDA", **fact))
        session.add(
            Chunk(
                id=fact_id,
                source_id=source_id,
                company="NVDA",
                embedding=vector,
                embedding_id=encoder.identifier,
                **chunk,
            )
        )
    session.flush()
    return source_id, True
