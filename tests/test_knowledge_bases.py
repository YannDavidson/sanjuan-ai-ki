from pathlib import Path

from packages.knowledge.knowledge_base import load_knowledge_base, validate_knowledge_bases

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_initial_knowledge_bases_are_valid() -> None:
    result = validate_knowledge_bases(REPO_ROOT / "knowledge" / "bases")

    assert result["valid"] is True
    assert result["knowledge_base_count"] == 6
    assert result["source_count"] >= 6
    assert result["errors"] == []


def test_transportation_base_requires_official_evidence() -> None:
    base = load_knowledge_base(REPO_ROOT / "knowledge" / "bases" / "transportation" / "knowledge-base.yml")

    assert base.id == "kb-transportation"
    assert base.sensitive_topics is True
    assert any(source.trust_level == "official" for source in base.sources)
    assert base.review_status == "active"
    assert base.maintainers


def test_all_active_bases_have_source_policies() -> None:
    result = validate_knowledge_bases(REPO_ROOT / "knowledge" / "bases")

    for base in result["knowledge_bases"]:
        assert base["source_policy"]
        if base["review_status"] == "active":
            assert base["maintainers"]
