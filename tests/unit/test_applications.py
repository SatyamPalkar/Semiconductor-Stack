import copy

import pytest
from pydantic import ValidationError

from semiconductor_research.sources.applications import ApplicationCatalog, load_applications


def test_application_catalog_separates_context_from_supplier_and_financial_claims():
    data = load_applications()
    assert {w["id"] for w in data["worlds"] if w["depth"] == "guided_story"} == {
        "ai-cloud",
        "electric-mobility",
        "smart-infrastructure",
    }
    assert {f["id"] for f in data["functions"]} == {
        "compute",
        "sense",
        "communicate",
        "control",
        "power",
    }
    assert not data["human_reviewed"]
    assert all(step["source_ids"] for w in data["worlds"] for step in w["steps"])
    assert {w["id"] for w in data["worlds"]} >= {
        "aviation",
        "engineering-design",
        "healthcare",
        "energy",
        "automation",
        "connected-life",
    }
    assert all(
        not s["company_ids"]
        for w in data["worlds"]
        if w["id"] == "connected-life"
        for s in w["steps"]
    )
    assert "revenue" not in data and "metrics" not in data


def test_unknown_or_unrelated_citations_cannot_support_a_portfolio_example():
    data = load_applications()
    data["worlds"][0]["steps"][0]["source_ids"] = ["missing"]
    with pytest.raises(ValidationError, match="source reference"):
        ApplicationCatalog.model_validate(data)
    data = load_applications()
    data["worlds"][0]["steps"][0]["company_ids"] = ["asml"]
    with pytest.raises(ValidationError, match="matching company reference"):
        ApplicationCatalog.model_validate(data)


def test_unsafe_source_urls_duplicate_tasks_and_unknown_functions_are_rejected():
    data = load_applications()
    data["sources"][0]["url"] = "https://localhost/private"
    with pytest.raises(ValidationError, match="public HTTPS"):
        ApplicationCatalog.model_validate(data)
    data = load_applications()
    data["worlds"][0]["steps"].append(copy.deepcopy(data["worlds"][0]["steps"][0]))
    with pytest.raises(ValidationError, match="Duplicate"):
        ApplicationCatalog.model_validate(data)
    data = load_applications()
    data["worlds"][0]["steps"][0]["functions"] = ["invented"]
    with pytest.raises(ValidationError):
        ApplicationCatalog.model_validate(data)


def test_geographic_examples_need_company_specific_evidence():
    data = load_applications()
    data["footprints"][0]["source_ids"] = ["sia-end-use"]
    with pytest.raises(ValidationError, match="Geographic example"):
        ApplicationCatalog.model_validate(data)


def test_restricted_application_references_cannot_hide_their_access_status():
    data = load_applications()
    restricted = next(s for s in data["sources"] if s["id"] == "adi-structures")
    assert restricted["link_status"] == 403 and restricted["access_note"]
    restricted["access_note"] = None
    with pytest.raises(ValidationError, match="visible access note"):
        ApplicationCatalog.model_validate(data)
