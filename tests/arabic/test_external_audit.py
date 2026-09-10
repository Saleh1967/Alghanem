from pathlib import Path

import pytest

from alghanem.arabic.external_audit import (
    ExternalAuditError,
    audit_card,
    build_birth_spec_from_card,
)


def test_external_audit_defers_when_relations_are_undetermined() -> None:
    card_path = Path(
        "/home/runner/work/Alghanem/Alghanem/examples/external_audit/man_2_255.yaml"
    )

    result = audit_card(card_path)

    assert result.الجهة == "مدقق_خارجي"
    assert result.نتيجة_التدقيق_الخارجي == "DEFER_التدقيق"
    assert result.النموذج_المختبر == "استفهامية"
    assert result.مخروط_الأضعف_المشتق == ()
    assert set(result.الإسقاطات_المنافسة_المشتقة) == {"شرطية", "موصولة"}


def test_weaker_cone_is_derived_not_caller_declared() -> None:
    card = {
        "معرف_السؤال": "q",
        "معرف_الفرضية": "h",
        "الفرضية": "x",
        "النموذج_المختبر": "A",
        "القراءات_المنافسة": [],
        "نماذج_أضعف_معلنة": ["B"],
        "تعريف_التجربة": {
            "experiment_id": "e",
            "revision_id": "r1",
            "evidence_mode": "FORMAL",
            "domain": "d",
            "projections": ["A", "B"],
            "strict_relations": [["B", "A"]],
            "residual_definition_id": "res",
            "residual_definition": "residual",
            "closure_criterion_id": "c",
            "closure_criterion": "close",
            "evidence_requirements": "req",
        },
    }

    with pytest.raises(ExternalAuditError, match="derived"):
        build_birth_spec_from_card(card)
