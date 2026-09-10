import json
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
    assert result.عدد_القراءات_المنافسة == 2
    assert result.عدد_العلاقات_غير_المتعينة == 2
    assert result.تفاصيل_القراءات_المنافسة == (
        ("شرطية", "غير_متعينة"),
        ("موصولة", "غير_متعينة"),
    )
    assert result.حالة_إغلاق_Down_E == "غير_متعينة"


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


def test_external_audit_processes_all_competing_readings() -> None:
    card = {
        "معرف_السؤال": "q",
        "معرف_الفرضية": "h",
        "الفرضية": "x",
        "النموذج_المختبر": "A",
        "القراءات_المنافسة": [
            {"قراءة": "B", "علاقة_بالنموذج_المختبر": "غير_متعينة"},
            {"قراءة": "C", "علاقة_بالنموذج_المختبر": "منافس_غير_أضعف"},
            {"قراءة": "D", "علاقة_بالنموذج_المختبر": "غير_متعينة"},
        ],
        "تعريف_التجربة": {
            "experiment_id": "e",
            "revision_id": "r1",
            "evidence_mode": "FORMAL",
            "domain": "d",
            "projections": ["A", "B", "C", "D"],
            "strict_relations": [],
            "residual_definition_id": "res",
            "residual_definition": "residual",
            "closure_criterion_id": "c",
            "closure_criterion": "close",
            "evidence_requirements": "req",
        },
    }
    path = Path("/tmp/external_audit_all_competitors.json")
    path.write_text(json.dumps(card, ensure_ascii=False), encoding="utf-8")

    result = audit_card(path)

    assert result.نتيجة_التدقيق_الخارجي == "DEFER_التدقيق"
    assert result.عدد_القراءات_المنافسة == 3
    assert result.عدد_العلاقات_غير_المتعينة == 2
    assert result.تفاصيل_القراءات_المنافسة == (
        ("B", "غير_متعينة"),
        ("C", "منافس_غير_أضعف"),
        ("D", "غير_متعينة"),
    )
    assert result.حالة_إغلاق_Down_E == "غير_متعينة"


def test_external_audit_requires_down_e_closure_for_non_empty_cone() -> None:
    card = {
        "معرف_السؤال": "q",
        "معرف_الفرضية": "h",
        "الفرضية": "x",
        "النموذج_المختبر": "A",
        "القراءات_المنافسة": [],
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
        "اغلاق_سوابق_Down_E": [
            {"نموذج": "B", "حالة": "غير_مغلق"},
        ],
    }
    path = Path("/tmp/external_audit_down_e_not_closed.json")
    path.write_text(json.dumps(card, ensure_ascii=False), encoding="utf-8")

    result = audit_card(path)

    assert result.نتيجة_التدقيق_الخارجي == "DEFER_التدقيق"
    assert result.مخروط_الأضعف_المشتق == ("B",)
    assert result.حالة_إغلاق_Down_E == "غير_مغلق"
