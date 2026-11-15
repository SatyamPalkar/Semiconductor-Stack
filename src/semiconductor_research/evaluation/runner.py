import hashlib
import json
import statistics
from datetime import UTC, datetime

from semiconductor_research.config.settings import ROOT
from semiconductor_research.database.models import Source
from semiconductor_research.database.session import session_scope
from semiconductor_research.documents.embedding import MiniLM
from semiconductor_research.retrieval.answer import Question, answer_question


def evaluate():
    dataset_path = ROOT / "evaluations/datasets/milestone1.json"
    raw = dataset_path.read_bytes()
    dataset = json.loads(raw)
    encoder = MiniLM()
    pipeline_files = sorted(path for path in (ROOT / "src/semiconductor_research").rglob("*.py"))
    pipeline_hash = hashlib.sha256(
        b"".join(
            path.relative_to(ROOT).as_posix().encode() + path.read_bytes()
            for path in pipeline_files
        )
    ).hexdigest()
    results = []
    with session_scope() as session:
        for case in dataset["cases"]:
            body = Question(
                question=case["question"],
                filters={
                    "company": case.get("company", "NVDA"),
                    "as_of": case.get("as_of", "2025-03-01"),
                },
            )
            result = answer_question(session, encoder, body)
            checks = {
                "no_hosted_calls": result["model_calls"] == 0,
                "citation_resolution": all(
                    session.get(Source, item["source_id"]) is not None
                    for item in result["evidence"]
                ),
                "as_of": all(
                    item["published_at"][:10] <= str(body.filters.as_of)
                    for item in result["evidence"]
                ),
            }
            if "value" in case:
                checks["numerical_accuracy"] = (result.get("calculation") or {}).get(
                    "value"
                ) == case["value"]
                checks["reporting_period"] = bool(
                    result.get("calculation") and result["calculation"]["period_kind"] == "annual"
                )
            if "topic" in case:
                checks["retrieval_relevance"] = case["topic"] in {
                    item.get("topic") for item in result["evidence"]
                }
            if "abstained" in case:
                checks["abstention"] = result["abstained"] == case["abstained"]
            results.append(
                {
                    "id": case["id"],
                    "passed": all(checks.values()),
                    "checks": checks,
                    "latency_ms": result["latency_ms"],
                    "mode": result["mode"],
                    "sources": sorted({e["source_id"] for e in result["evidence"]}),
                }
            )
    report = {
        "executed": True,
        "generated_at": datetime.now(UTC).isoformat(),
        "version": "milestone1-v1.1",
        "dataset_sha256": hashlib.sha256(raw).hexdigest(),
        "pipeline_sha256": pipeline_hash,
        "embedding_identifier": encoder.identifier,
        "kind": "Deterministic local financial-tool and hybrid-retrieval development checks; no live LLM or investment-performance assessment",
        "human_reviewed": False,
        "citation_entailment_review": "pending independent human review",
        "research_workflow_comparison": "not implemented; no agent score reported",
        "total": len(results),
        "passed": sum(row["passed"] for row in results),
        "median_latency_ms": round(statistics.median(r["latency_ms"] for r in results), 2),
        "model_calls": 0,
        "hosted_input_tokens": 0,
        "hosted_output_tokens": 0,
        "hosted_model_cost_usd": "0.00",
        "scope_note": "Source resolution is checked; citation presence does not prove support for arbitrary generated claims. Restatement/conflict/injection protections are also tested separately in pytest.",
        "results": results,
    }
    path = ROOT / "evaluations/results/milestone1.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2) + "\n")
    print(
        f"Executed local evaluation: {report['passed']}/{report['total']} passed; live model calls: 0; human review: pending"
    )
    return 0 if report["passed"] == report["total"] else 1
