from types import SimpleNamespace
from unittest.mock import patch

import pytest
from pydantic import SecretStr

from semiconductor_research.config.settings import Settings
from semiconductor_research.llm.groq import Groq
from semiconductor_research.retrieval.answer import Question


def test_live_provider_is_opt_in_and_missing_configuration_fails():
    with pytest.raises(ValueError):
        Groq(Settings(_env_file=None, enable_live_llm=False))


def test_question_shape_and_bounded_filters():
    for payload in [
        {"question": "x" * 1201},
        {"question": "hi", "mode": "shell"},
        {"question": "revenue", "filters": {"company": "NVDA; DROP TABLE sources"}},
    ]:
        with pytest.raises(ValueError):
            Question(**payload)


@pytest.mark.parametrize(
    "draft",
    [
        '{"abstained":false,"paragraphs":[{"text":"Invented claim","citations":[99],"classification":"evidence"}]}',
        '{"abstained":false,"paragraphs":[]}',
        '{"abstained":false,"paragraphs":[{"text":"Uncited claim","citations":[],"classification":"evidence"}]}',
    ],
)
def test_unresolvable_or_missing_model_citations_are_never_returned(draft):
    config = Settings(
        _env_file=None,
        enable_live_llm=True,
        groq_api_key=SecretStr("deliberate-test-only"),
        llm_model="mock-model",
    )
    response = SimpleNamespace(
        status_code=200, json=lambda: {"choices": [{"message": {"content": draft}}]}
    )
    with patch("httpx.Client.post", return_value=response), pytest.raises(RuntimeError):
        Groq(config).generate("What is revenue?", [{"citation_id": 1, "text": "Untrusted source"}])


def test_another_embedding_name_cannot_relabel_pinned_vectors():
    from semiconductor_research.documents.embedding import validate_model_config

    config = Settings(_env_file=None, embedding_model="different-model")
    with pytest.raises(ValueError, match="pinned"):
        validate_model_config(config)
