import argparse
import json
from datetime import UTC, date, datetime

from sqlalchemy import select

from semiconductor_research.config.settings import ROOT
from semiconductor_research.database.models import Fact, Source
from semiconductor_research.database.session import session_scope
from semiconductor_research.documents.embedding import MiniLM, prepare_model
from semiconductor_research.financials.engine import (
    DEFINITIONS,
    Metric,
    MissingEvidence,
    calculate_metric,
)
from semiconductor_research.ingestion.service import ingest_nvidia
from semiconductor_research.sources.catalog import COMPANIES


def snapshot(as_of: date):
    with session_scope() as session:
        source_rows = session.scalars(select(Source).order_by(Source.id)).all()
        if any(
            s.capture_kind not in {"original_primary_source", "recorded_primary_source_excerpt"}
            for s in source_rows
        ):
            raise ValueError(
                "Static export refused: non-primary or synthetic source records require review"
            )
        sources = [
            {
                "id": s.id,
                "company": s.company,
                "title": s.title,
                "url": s.url,
                "publisher": s.publisher,
                "publication_date": str(s.publication_date) if s.publication_date else None,
                "published_at": s.published_at.isoformat(),
                "retrieved_at": s.retrieved_at.isoformat(),
                "checksum": s.checksum,
                "capture_kind": s.capture_kind,
                "accounting_basis": s.accounting_basis,
            }
            for s in source_rows
        ]
        dates = session.scalars(select(Fact.period_end).distinct().order_by(Fact.period_end)).all()
        metrics = []
        for end in dates:
            for metric in Metric:
                try:
                    metrics.append(calculate_metric(session, "NVDA", metric, end, as_of))
                except MissingEvidence:
                    continue
        return {
            "title": "Semiconductor Research Platform",
            "version": "0.1.0",
            "generated_at": datetime.now(UTC).isoformat(),
            "research_as_of": str(as_of),
            "mode": "database_export; real reported facts, not synthetic",
            "sources": sources,
            "metrics": metrics,
            "companies": COMPANIES,
            "definitions": DEFINITIONS,
            "evaluation": {
                "executed": False,
                "note": "Run semi evaluate and export again to include results.",
            },
            "limitations": [
                "Historical FY2024/FY2025 NVIDIA pilot; not current market data.",
                "TSMC source returned HTTP 403; no TSMC financial figures are loaded.",
                "The remaining company roster is scope metadata, not an evidence-backed industry ranking.",
                "Original IR page captured later than its publication date; not an independently certified point-in-time archive.",
                "Investment-thesis workflow, cloud deployment, DCF and trading are not implemented in milestone 1.",
            ],
        }


def main():
    parser = argparse.ArgumentParser(description="Local semiconductor research operations")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("prepare-model")
    ingest = commands.add_parser("ingest")
    mode = ingest.add_mutually_exclusive_group()
    mode.add_argument("--recorded", action="store_true")
    mode.add_argument("--offline", action="store_true")
    export = commands.add_parser("export-showcase")
    export.add_argument("--as-of", type=date.fromisoformat, default=date(2025, 3, 1))
    commands.add_parser("evaluate")
    args = parser.parse_args()
    if args.command == "prepare-model":
        prepare_model()
        print("Pinned public embedding model prepared and verified")
    elif args.command == "ingest":
        with session_scope() as session:
            source, created = ingest_nvidia(
                session, MiniLM(), recorded=args.recorded, offline=args.offline
            )
        print(json.dumps({"source_id": source, "created": created}))
    elif args.command == "export-showcase":
        data = snapshot(args.as_of)
        results = ROOT / "evaluations/results/milestone1.json"
        if results.exists():
            data["evaluation"] = json.loads(results.read_text())
        path = ROOT / "apps/web/public/research-snapshot.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2) + "\n")
        print("Exported database-derived static research snapshot")
    elif args.command == "evaluate":
        from semiconductor_research.evaluation.runner import evaluate

        raise SystemExit(evaluate())


if __name__ == "__main__":
    main()
