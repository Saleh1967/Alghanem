import json
from pathlib import Path

import pytest

from alghanem.arabic.external_audit import (
    ExternalAuditError,
    audit_card,
    build_birth_spec_from_card,
    canonical_relation,
    comparison_key,
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
            {"قراءة": "C", "علاقة_بالنموذج_المختبر": "مكافئ_صوريًّا"},
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
        ("C", "مكافئ_صوريًّا"),
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


def test_external_audit_defers_for_maa_2_197_card() -> None:
    card_path = (
        Path(__file__).resolve().parents[2]
        / "examples"
        / "external_audit"
        / "maa_2_197.yaml"
    )

    result = audit_card(card_path)

    assert result.نتيجة_التدقيق_الخارجي == "DEFER_التدقيق"
    assert result.النموذج_المختبر == "ما_شرطية"
    assert result.مخروط_الأضعف_المشتق == ()
    assert result.الإسقاطات_المنافسة_المشتقة == ("ما_موصولة",)
    assert result.عدد_القراءات_المنافسة == 1
    assert result.عدد_العلاقات_غير_المتعينة == 1
    assert result.حالة_إغلاق_Down_E == "غير_متعينة"


def _relation_card(relation: str) -> dict[str, object]:
    return {
        "معرف_السؤال": "q",
        "معرف_الفرضية": "h",
        "الفرضية": "x",
        "النموذج_المختبر": "A",
        "القراءات_المنافسة": [{"قراءة": "B", "علاقة_بالنموذج_المختبر": relation}],
        "تعريف_التجربة": {
            "experiment_id": "e",
            "revision_id": "r1",
            "evidence_mode": "FORMAL",
            "domain": "d",
            "projections": ["A", "B"],
            "strict_relations": [],
            "residual_definition_id": "res",
            "residual_definition": "residual",
            "closure_criterion_id": "c",
            "closure_criterion": "close",
            "evidence_requirements": "req",
        },
    }


@pytest.mark.parametrize(
    "relation",
    [
        "غير_متعينة",
        "غير_متعيّنة",
        "غَيْر_متعينة",
        "غيــر_متعينة",
        "غير_متعينه",
        "غير_متعينة\u200f",
    ],
)
def test_undetermined_relation_is_orthography_insensitive(
    tmp_path: Path, relation: str
) -> None:
    path = tmp_path / "relation.json"
    path.write_text(
        json.dumps(_relation_card(relation), ensure_ascii=False), encoding="utf-8"
    )

    result = audit_card(path)

    assert result.نتيجة_التدقيق_الخارجي == "DEFER_التدقيق"
    assert result.عدد_العلاقات_غير_المتعينة == 1
    assert result.حالة_إغلاق_Down_E == "غير_متعينة"
    assert result.تفاصيل_القراءات_المنافسة == (("B", relation),)


def test_determined_relation_is_still_distinguished(tmp_path: Path) -> None:
    path = tmp_path / "determined.json"
    path.write_text(
        json.dumps(_relation_card("مكافئ_صوريًّا"), ensure_ascii=False),
        encoding="utf-8",
    )

    result = audit_card(path)

    assert result.نتيجة_التدقيق_الخارجي == "PASS_التدقيق"
    assert result.عدد_العلاقات_غير_المتعينة == 0
    assert result.عدد_المنافسات_غير_القابلة_للمقارنة_الحاجبة == 0


@pytest.mark.parametrize(
    "relation",
    ["منافس_غير_أضعف", "أضعف", "اقوى_صوريا", "أضعف_صوري", ""],
)
def test_relation_outside_closed_vocabulary_is_rejected(
    tmp_path: Path, relation: str
) -> None:
    path = tmp_path / "unknown_relation.json"
    path.write_text(
        json.dumps(_relation_card(relation), ensure_ascii=False), encoding="utf-8"
    )

    with pytest.raises(ExternalAuditError):
        audit_card(path)


@pytest.mark.parametrize("relation", ["أضعف_صوريًّا", "اضعف_صوريا", "مكافئ_صوريًّا"])
def test_resolved_relations_are_orthography_insensitive(
    tmp_path: Path, relation: str
) -> None:
    path = tmp_path / "resolved.json"
    path.write_text(
        json.dumps(_relation_card(relation), ensure_ascii=False), encoding="utf-8"
    )

    result = audit_card(path)

    assert result.نتيجة_التدقيق_الخارجي == "PASS_التدقيق"
    assert result.تفاصيل_القراءات_المنافسة == (("B", relation),)


def test_incomparable_complete_rival_explanation_still_defers(
    tmp_path: Path,
) -> None:
    card = _relation_card("غير_قابل_للمقارنة")
    readings = card["القراءات_المنافسة"]
    assert isinstance(readings, list)
    readings[0]["تفسير_منافس_كامل"] = True
    path = tmp_path / "incomparable_blocking.json"
    path.write_text(json.dumps(card, ensure_ascii=False), encoding="utf-8")

    result = audit_card(path)

    assert result.نتيجة_التدقيق_الخارجي == "DEFER_التدقيق"
    assert result.عدد_العلاقات_غير_المتعينة == 0
    assert result.عدد_المنافسات_غير_القابلة_للمقارنة_الحاجبة == 1


def test_incomparable_without_declared_rival_explanation_defers(
    tmp_path: Path,
) -> None:
    path = tmp_path / "incomparable_silent.json"
    path.write_text(
        json.dumps(_relation_card("غير_قابل_للمقارنة"), ensure_ascii=False),
        encoding="utf-8",
    )

    result = audit_card(path)

    assert result.نتيجة_التدقيق_الخارجي == "DEFER_التدقيق"
    assert result.عدد_المنافسات_غير_القابلة_للمقارنة_الحاجبة == 1


def test_incomparable_non_rival_explanation_does_not_block(tmp_path: Path) -> None:
    card = _relation_card("غير_قابل_للمقارنة")
    readings = card["القراءات_المنافسة"]
    assert isinstance(readings, list)
    readings[0]["تفسير_منافس_كامل"] = False
    path = tmp_path / "incomparable_open.json"
    path.write_text(json.dumps(card, ensure_ascii=False), encoding="utf-8")

    result = audit_card(path)

    assert result.نتيجة_التدقيق_الخارجي == "PASS_التدقيق"
    assert result.عدد_المنافسات_غير_القابلة_للمقارنة_الحاجبة == 0


def test_rival_explanation_flag_is_rejected_for_other_relations(
    tmp_path: Path,
) -> None:
    card = _relation_card("مكافئ_صوريًّا")
    readings = card["القراءات_المنافسة"]
    assert isinstance(readings, list)
    readings[0]["تفسير_منافس_كامل"] = True
    path = tmp_path / "flag_misuse.json"
    path.write_text(json.dumps(card, ensure_ascii=False), encoding="utf-8")

    with pytest.raises(ExternalAuditError, match="تفسير_منافس_كامل"):
        audit_card(path)


def test_rival_explanation_flag_must_be_boolean(tmp_path: Path) -> None:
    card = _relation_card("غير_قابل_للمقارنة")
    readings = card["القراءات_المنافسة"]
    assert isinstance(readings, list)
    readings[0]["تفسير_منافس_كامل"] = "نعم"
    path = tmp_path / "flag_text.json"
    path.write_text(json.dumps(card, ensure_ascii=False), encoding="utf-8")

    with pytest.raises(ExternalAuditError, match="تفسير_منافس_كامل"):
        audit_card(path)


def test_canonical_relation_maps_spellings_to_closed_vocabulary() -> None:
    assert canonical_relation("غَيْر_متعينه") == "غير_متعينة"
    assert canonical_relation("اضعف_صوريا") == "أضعف_صوريًّا"
    assert canonical_relation("غير_قابل_للمقارنه") == "غير_قابل_للمقارنة"
    with pytest.raises(ExternalAuditError):
        canonical_relation("مكافي_صوريا")


def _down_e_card(model: str, status: str) -> dict[str, object]:
    return {
        "معرف_السؤال": "q",
        "معرف_الفرضية": "h",
        "الفرضية": "x",
        "النموذج_المختبر": "أضعف",
        "القراءات_المنافسة": [],
        "تعريف_التجربة": {
            "experiment_id": "e",
            "revision_id": "r1",
            "evidence_mode": "FORMAL",
            "domain": "d",
            "projections": ["أضعف", "اضعف_سابق"],
            "strict_relations": [["اضعف_سابق", "أضعف"]],
            "residual_definition_id": "res",
            "residual_definition": "residual",
            "closure_criterion_id": "c",
            "closure_criterion": "close",
            "evidence_requirements": "req",
        },
        "اغلاق_سوابق_Down_E": [{"نموذج": model, "حالة": status}],
    }


@pytest.mark.parametrize("model", ["اضعف_سابق", "أضعف_سابق", "آضعف_سابق"])
@pytest.mark.parametrize("status", ["مغلق", "مغلَق", "مُغْلَق"])
def test_down_e_closure_is_orthography_insensitive(
    tmp_path: Path, model: str, status: str
) -> None:
    path = tmp_path / "down_e.json"
    path.write_text(
        json.dumps(_down_e_card(model, status), ensure_ascii=False), encoding="utf-8"
    )

    result = audit_card(path)

    assert result.مخروط_الأضعف_المشتق == ("اضعف_سابق",)
    assert result.حالة_إغلاق_Down_E == "مغلق"
    assert result.نتيجة_التدقيق_الخارجي == "PASS_التدقيق"


def test_down_e_non_closed_status_reports_the_card_spelling(tmp_path: Path) -> None:
    path = tmp_path / "down_e_open.json"
    path.write_text(
        json.dumps(_down_e_card("أضعف_سابق", "غير_مغلق"), ensure_ascii=False),
        encoding="utf-8",
    )

    result = audit_card(path)

    assert result.حالة_إغلاق_Down_E == "غير_مغلق"
    assert "أضعف_سابق" in result.سبب_حالة_إغلاق_Down_E


def test_comparison_key_preserves_distinct_readings() -> None:
    assert comparison_key("غير_متعيّنة") == comparison_key("غير_متعينة")
    assert comparison_key("منافس_غير_أضعف") != comparison_key("غير_متعينة")
    assert comparison_key("أولى") == comparison_key("اولي")
    assert comparison_key("غير_متعينة") != comparison_key("غير_متعينى")


def _example_card(name: str) -> Path:
    return Path(__file__).resolve().parents[2] / "examples" / "external_audit" / name


def test_external_audit_defers_for_imran_3_33_card() -> None:
    result = audit_card(_example_card("imran_3_33.yaml"))

    assert result.نتيجة_التدقيق_الخارجي == "DEFER_التدقيق"
    assert result.النموذج_المختبر == "علمية_وعجمة"
    assert result.مخروط_الأضعف_المشتق == ("علمية_فقط",)
    assert result.الإسقاطات_المنافسة_المشتقة == ("علمية_وزيادة_ألف_ونون",)
    assert result.عدد_العلاقات_غير_المتعينة == 1
    assert result.حالة_إغلاق_Down_E == "غير_متعينة"


def test_unresolved_relation_outranks_documented_down_e_closure(
    tmp_path: Path,
) -> None:
    card = json.loads(_example_card("imran_3_33.yaml").read_text(encoding="utf-8"))
    card["اغلاق_سوابق_Down_E"] = [{"نموذج": "علمية_فقط", "حالة": "مغلق"}]
    path = tmp_path / "imran_documented.json"
    path.write_text(json.dumps(card, ensure_ascii=False), encoding="utf-8")

    result = audit_card(path)

    assert result.مخروط_الأضعف_المشتق == ("علمية_فقط",)
    assert result.حالة_إغلاق_Down_E == "غير_متعينة"
    assert result.نتيجة_التدقيق_الخارجي == "DEFER_التدقيق"
