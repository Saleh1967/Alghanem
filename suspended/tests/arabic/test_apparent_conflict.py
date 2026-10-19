"""المفردة المغلقة لأسباب التعارض الظاهر بين شاهدين.

تُثبِّت هذه الاختبارات ثلاثة أمور: أن المفردة ثلاثية مغلقة لا رتبة فيها، وأنها
متمايزة عن مفردة أسباب الإخلال بالفهم الخمسة فلا يُحمل `الاشتباه` على
`الاشتراك`، وأن التصنيف خاملٌ سلطويًّا لا يُحرّك شيئًا.
"""

import json
from pathlib import Path

import pytest

from alghanem.arabic import apparent_conflict, comprehension_defect
from alghanem.arabic.apparent_conflict import (
    CLOSED_VOCABULARY,
    DECLARABLE_VALUES,
    DEFAULT_IS_DIFFERENCE_NOT_CONTRADICTION_NOTE,
    DIAGNOSES,
    ISHTIBAH_IS_NOT_ISHTIRAK_NOTE,
    NO_PRIORITY_AMONG_APPARENT_CONFLICT_CAUSES_NOTE,
    NOT_APPLICABLE,
    REMEDY_PRINCIPLE,
    REMEDY_STEPS,
    SCOPE_NOTE,
    SOURCE,
    ApparentConflictCause,
    ApparentConflictError,
    apparent_conflict_diagnosis,
    canonical_apparent_conflict_classification,
)
from alghanem.arabic.comprehension_defect import (
    CLOSED_VOCABULARY as DEFECT_VOCABULARY,
)
from alghanem.arabic.external_audit import (
    ExternalAuditError,
    audit_card,
    build_birth_spec_from_card,
)
from alghanem.arabic.text_key import comparison_key

_EXAMPLES = Path(__file__).resolve().parents[2] / "examples" / "external_audit"


def _card(name: str) -> Path:
    return _EXAMPLES / name


def _write(directory: Path, card: dict) -> Path:
    path = directory / "variant.json"
    path.write_text(json.dumps(card, ensure_ascii=False), encoding="utf-8")
    return path


def test_the_vocabulary_is_exactly_the_three_apparent_conflict_causes() -> None:
    assert CLOSED_VOCABULARY == ("التعميم", "التجريد", "الاشتباه")
    assert DECLARABLE_VALUES == CLOSED_VOCABULARY + ("لا_ينطبق",)
    assert NOT_APPLICABLE == "لا_ينطبق"


def test_declared_values_are_read_and_invented_terms_are_rejected() -> None:
    assert (
        canonical_apparent_conflict_classification("التعميم")
        is ApparentConflictCause.TAMIM
    )
    assert canonical_apparent_conflict_classification("لا_ينطبق") is None

    for invented in ("التناقض", "النسخ", "تعميم_جزئي", "", "   "):
        with pytest.raises(ApparentConflictError):
            canonical_apparent_conflict_classification(invented)


def test_the_five_causes_of_defective_comprehension_are_not_accepted_here() -> None:
    """`الاشتباه` is not `الاشتراك`: neither vocabulary absorbs the other."""

    for value in DEFECT_VOCABULARY:
        with pytest.raises(ApparentConflictError):
            canonical_apparent_conflict_classification(value)
    for value in CLOSED_VOCABULARY:
        with pytest.raises(comprehension_defect.ComprehensionDefectError):
            comprehension_defect.canonical_defect_classification(value)

    defect_keys = {comparison_key(value) for value in DEFECT_VOCABULARY}
    conflict_keys = {comparison_key(value) for value in CLOSED_VOCABULARY}
    assert defect_keys.isdisjoint(conflict_keys)
    assert "الاشتباه" in ISHTIBAH_IS_NOT_ISHTIRAK_NOTE
    assert "الاشتراك" in ISHTIBAH_IS_NOT_ISHTIRAK_NOTE


def test_the_module_declares_no_rank_and_no_comparison_between_its_causes() -> None:
    exported = dir(apparent_conflict)

    assert not [name for name in exported if "priority" in name or "rank" in name]
    assert not [name for name in exported if "compare" in name]
    assert "لا رتبة بينها" in NO_PRIORITY_AMONG_APPARENT_CONFLICT_CAUSES_NOTE


def test_every_cause_carries_a_definition_a_remedy_and_a_named_source() -> None:
    assert {item.cause for item in DIAGNOSES} == set(ApparentConflictCause)
    assert len(DIAGNOSES) == len(ApparentConflictCause) == 3
    for item in DIAGNOSES:
        assert item.definition.strip()
        assert item.remedy in REMEDY_STEPS
        assert item.source == SOURCE
        assert apparent_conflict_diagnosis(item.cause) is item

    assert len(REMEDY_STEPS) == 3
    assert len(set(item.remedy for item in DIAGNOSES)) == 3
    assert "سياقه الكامل قبل أي مقارنة" in REMEDY_PRINCIPLE


def test_the_governing_rule_and_scope_are_recorded_in_full() -> None:
    assert "الأصل فيهما الاختلاف" in DEFAULT_IS_DIFFERENCE_NOT_CONTRADICTION_NOTE
    assert "دعوى تحتاج إثباتًا" in DEFAULT_IS_DIFFERENCE_NOT_CONTRADICTION_NOTE
    assert "لا غموض لفظٍ مفرد" in SCOPE_NOTE
    assert "ثبوت النصّ" in SCOPE_NOTE


def test_a_diagnosis_is_refused_for_anything_but_a_closed_vocabulary_cause() -> None:
    with pytest.raises(ApparentConflictError):
        apparent_conflict_diagnosis("التعميم")  # type: ignore[arg-type]


def test_the_card_field_is_optional_and_absent_readings_are_not_reported() -> None:
    for path in sorted(_EXAMPLES.glob("*.yaml")):
        assert audit_card(path).تصنيف_أسباب_التعارض_الظاهر == ()


def test_a_declared_card_classification_is_read_and_reported(tmp_path: Path) -> None:
    card = json.loads(_card("quru_2_228.yaml").read_text(encoding="utf-8"))
    card["القراءات_المنافسة"][0]["سبب_التعارض_الظاهر"] = "التجريد"

    result = audit_card(_write(tmp_path, card))

    assert result.تصنيف_أسباب_التعارض_الظاهر == (("طهر", "التجريد"),)
    assert result.to_dict()["تصنيف_أسباب_التعارض_الظاهر"] == [
        {"قراءة": "طهر", "سبب_التعارض_الظاهر": "التجريد"}
    ]


def test_an_explicit_non_applicability_is_a_classification_not_a_silence(
    tmp_path: Path,
) -> None:
    card = json.loads(_card("quru_2_228.yaml").read_text(encoding="utf-8"))
    card["القراءات_المنافسة"][0]["سبب_التعارض_الظاهر"] = "لا_ينطبق"

    assert audit_card(_write(tmp_path, card)).تصنيف_أسباب_التعارض_الظاهر == (
        ("طهر", "لا_ينطبق"),
    )


def test_an_invented_card_classification_is_rejected(tmp_path: Path) -> None:
    card = json.loads(_card("quru_2_228.yaml").read_text(encoding="utf-8"))
    card["القراءات_المنافسة"][0]["سبب_التعارض_الظاهر"] = "اشتراك"

    with pytest.raises(ExternalAuditError, match="سبب_التعارض_الظاهر"):
        audit_card(_write(tmp_path, card))


def test_the_classification_moves_no_authority_and_no_derived_specification(
    tmp_path: Path,
) -> None:
    original = json.loads(_card("quru_2_228.yaml").read_text(encoding="utf-8"))
    baseline = audit_card(_card("quru_2_228.yaml")).to_dict()
    classified = json.loads(json.dumps(original, ensure_ascii=False))
    classified["القراءات_المنافسة"][0]["سبب_التعارض_الظاهر"] = "الاشتباه"
    reported = audit_card(_write(tmp_path, classified)).to_dict()

    assert reported.pop("تصنيف_أسباب_التعارض_الظاهر") == [
        {"قراءة": "طهر", "سبب_التعارض_الظاهر": "الاشتباه"}
    ]
    assert baseline.pop("تصنيف_أسباب_التعارض_الظاهر") == []
    assert reported == baseline
    assert build_birth_spec_from_card(classified) == build_birth_spec_from_card(
        original
    )
