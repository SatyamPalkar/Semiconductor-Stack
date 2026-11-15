import copy

import pytest
from pydantic import ValidationError

from semiconductor_research.sources.directory import Directory, load_directory, public_url


def catalog():
    data = load_directory()
    data.pop("link_observations")
    for c in data["companies"]:
        c.pop("financial_loaded")
    return data


def test_directory_has_distinct_roles_and_no_implicit_financial_coverage():
    unloaded = load_directory()
    assert not any(c["financial_loaded"] for c in unloaded["companies"])
    loaded = load_directory({"MU", "ASML"})
    assert {c["name"] for c in loaded["companies"] if c["financial_loaded"]} == {"Micron", "ASML"}
    assert {role["id"] for role in loaded["categories"]} == {
        r for c in loaded["companies"] for r in c["roles"]
    }
    assert {c["name"] for c in loaded["companies"]} >= {
        "NVIDIA",
        "TSMC",
        "ASML",
        "Micron",
        "Texas Instruments",
        "Amkor",
    }
    assert any(r["category"] == "open-tools" for r in loaded["resources"])


@pytest.mark.parametrize(
    "url",
    [
        "http://example.com",
        "https://localhost/",
        "https://127.0.0.1/",
        "https://[::1]/",
        "https://user:secret@example.com/",
        "https://private.internal/",
        "https://example.com:8100/",
    ],
)
def test_directory_refuses_private_or_credential_destinations(url):
    with pytest.raises(ValueError):
        public_url(url)


def test_duplicate_ids_and_unknown_roles_are_rejected():
    data = catalog()
    data["companies"].append(copy.deepcopy(data["companies"][0]))
    with pytest.raises(ValidationError, match="Duplicate"):
        Directory.model_validate(data)
    data = catalog()
    data["companies"][0]["roles"] = ["unknown"]
    with pytest.raises(ValidationError, match="Unknown"):
        Directory.model_validate(data)
