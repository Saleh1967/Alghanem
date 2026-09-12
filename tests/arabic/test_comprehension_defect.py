"""The closed usuli vocabulary of causes of defective comprehension.

These tests fix three things: the vocabulary is closed and its priority order
is fully argued, the classification is inert with respect to every authority,
and its application to the four existing cards is honest — a competing reading
is classified only when one of the five causes actually describes it.
"""

import json
from itertools import combinations
from pathlib import Path

import pytest

from alghanem.arabic.comprehension_defect import (
    CLOSED_VOCABULARY,
    DECLARABLE_VALUES,
    NOT_APPLICABLE,
    PRIORITY_ARGUMENTS,
    SCOPE_NOTE,
    ComprehensionDefectCause,
    ComprehensionDefectError,
    canonical_defect_classification,
    compare_defect_priority,
    defect_priority,
    priority_argument,
)
from alghanem.arabic.external_audit import (
    ExternalAuditError,
    audit_card,
    build_birth_spec_from_card,
)

_EXAMPLES = Path(__file__).resolve().parents[2] / "examples" / "external_audit"


def _card(name: str) -> Path:
    return _EXAMPLES / name


def test_the_vocabulary_is_exactly_the_five_usuli_causes() -> None:
    assert CLOSED_VOCABULARY == ("اشتراك", "نقل", "مجاز", "إضمار", "تخصيص")
    assert DECLARABLE_VALUES == CLOSED_VOCABULARY + ("لا_ينطبق",)
    assert NOT_APPLICABLE == "لا_ينطبق"


def test_the_declared_priority_order_matches_the_documented_ranking() -> None:
    ranks = {cause: defect_priority(cause) for cause in ComprehensionDefectCause}

    assert ranks[ComprehensionDefectCause.TAKHSIS] == 1
    assert ranks[ComprehensionDefectCause.MAJAZ] == 2
    assert ranks[ComprehensionDefectCause.IDMAR] == 2
    assert ranks[ComprehensionDefectCause.NAQL] == 3
    assert ranks[ComprehensionDefectCause.ISHTIRAK] == 4
    assert (
        compare_defect_priority(
            ComprehensionDefectCause.MAJAZ, ComprehensionDefectCause.IDMAR
        )
        == 0
    )
    assert (
        compare_defect_priority(
            ComprehensionDefectCause.TAKHSIS, ComprehensionDefectCause.ISHTIRAK
        )
        == -1
    )
    assert (
        compare_defect_priority(
            ComprehensionDefectCause.ISHTIRAK, ComprehensionDefectCause.NAQL
        )
        == 1
    )


def test_every_pairwise_comparison_carries_its_own_textual_argument() -> None:
    pairs = {frozenset(pair) for pair in combinations(ComprehensionDefectCause, 2)}

    assert {argument.pair for argument in PRIORITY_ARGUMENTS} == pairs
    assert len(PRIORITY_ARGUMENTS) == len(pairs) == 10
    for argument in PRIORITY_ARGUMENTS:
        assert argument.argument.strip()
        assert argument.source.strip()
        assert argument.verdict.strip()


def test_each_argument_agrees_with_the_rank_it_justifies() -> None:
    for argument in PRIORITY_ARGUMENTS:
        order = compare_defect_priority(argument.first, argument.second)
        if argument.verdict == "سواء":
            assert order == 0
        else:
            assert order != 0
            preferred = argument.first if order < 0 else argument.second
            assert preferred.value in argument.verdict


def test_a_comparison_is_symmetric_and_never_self_referential() -> None:
    assert priority_argument(
        ComprehensionDefectCause.MAJAZ, ComprehensionDefectCause.NAQL
    ) is priority_argument(
        ComprehensionDefectCause.NAQL, ComprehensionDefectCause.MAJAZ
    )
    with pytest.raises(ComprehensionDefectError, match="itself"):
        priority_argument(ComprehensionDefectCause.NAQL, ComprehensionDefectCause.NAQL)


def test_declared_values_are_read_and_invented_terms_are_rejected() -> None:
    assert canonical_defect_classification("إضمار") is ComprehensionDefectCause.IDMAR
    assert canonical_defect_classification("اضمار") is ComprehensionDefectCause.IDMAR
    assert canonical_defect_classification("لا_ينطبق") is None

    for invented in ("تأويل", "قياس", "ضعف_النقل", "إضمارية", ""):
        with pytest.raises(ComprehensionDefectError):
            canonical_defect_classification(invented)


def test_the_scope_note_records_the_two_things_the_framework_does_not_cover() -> None:
    assert "تعدد" in SCOPE_NOTE.replace("ّ", "")
    assert "ضعف النقل" in SCOPE_NOTE


def _write(directory: Path, card: dict) -> Path:
    path = directory / "variant.json"
    path.write_text(json.dumps(card, ensure_ascii=False), encoding="utf-8")
    return path


def test_the_card_field_is_optional_and_absent_readings_are_not_reported(
    tmp_path: Path,
) -> None:
    card = json.loads(_card("maa_2_197.yaml").read_text(encoding="utf-8"))
    for reading in card["القراءات_المنافسة"]:
        del reading["سبب_الإخلال_بالفهم"]

    assert audit_card(_write(tmp_path, card)).تصنيف_أسباب_الإخلال_بالفهم == ()


def test_an_invented_card_classification_is_rejected(tmp_path: Path) -> None:
    card = json.loads(_card("maa_2_197.yaml").read_text(encoding="utf-8"))
    card["القراءات_المنافسة"][0]["سبب_الإخلال_بالفهم"] = "ضعف_النقل"
    path = tmp_path / "invented.json"
    path.write_text(json.dumps(card, ensure_ascii=False), encoding="utf-8")

    with pytest.raises(ExternalAuditError, match="سبب_الإخلال_بالفهم"):
        audit_card(path)


def test_the_classification_moves_no_authority_and_no_derived_specification(
    tmp_path: Path,
) -> None:
    """Removing every classification changes nothing but the report field."""

    for index, name in enumerate(
        sorted(path.name for path in _EXAMPLES.glob("*.yaml"))
    ):
        card = json.loads(_card(name).read_text(encoding="utf-8"))
        classified = audit_card(_card(name)).to_dict()

        for reading in card["القراءات_المنافسة"]:
            reading.pop("سبب_الإخلال_بالفهم", None)
        directory = tmp_path / str(index)
        directory.mkdir()
        stripped = audit_card(_write(directory, card)).to_dict()

        assert stripped.pop("تصنيف_أسباب_الإخلال_بالفهم") == []
        assert classified.pop("تصنيف_أسباب_الإخلال_بالفهم") != []
        assert stripped.pop("حالة_استنفاد_الأسباب_الأقوى") == []
        classified.pop("حالة_استنفاد_الأسباب_الأقوى")
        assert stripped == classified
        assert build_birth_spec_from_card(card) == build_birth_spec_from_card(
            json.loads(_card(name).read_text(encoding="utf-8"))
        )


def test_the_four_existing_cards_are_classified_honestly() -> None:
    """The observed classification of every competing reading, as it stands.

    Only three of the eight competing readings are described by one of the five
    causes. The rest are declared `لا_ينطبق` rather than forced into a label,
    because their dispute is over the recited wording or over the strength of
    transmission, neither of which this framework addresses.
    """

    observed = {
        name: audit_card(_card(f"{name}.yaml")).تصنيف_أسباب_الإخلال_بالفهم
        for name in ("hadhan_20_63", "imran_3_33", "maa_2_197", "man_2_255")
    }

    assert observed == {
        "hadhan_20_63": (
            ("تصحيح_لفظي_هذين", "لا_ينطبق"),
            ("تخفيف_إن_وضمير_شأن", "إضمار"),
            ("مذهب_كنانة_قلب_الألف_ياء", "لا_ينطبق"),
            ("شاذ_آحاد_ما_هذان_إلا_ساحران", "لا_ينطبق"),
        ),
        "imran_3_33": (("علمية_وزيادة_ألف_ونون", "لا_ينطبق"),),
        "maa_2_197": (("ما_موصولة", "اشتراك"),),
        "man_2_255": (("شرطية", "اشتراك"), ("موصولة", "اشتراك")),
    }
    applicable = [
        (name, reading)
        for name, rows in observed.items()
        for reading, classification in rows
        if classification != NOT_APPLICABLE
    ]
    assert applicable == [
        ("hadhan_20_63", "تخفيف_إن_وضمير_شأن"),
        ("maa_2_197", "ما_موصولة"),
        ("man_2_255", "شرطية"),
        ("man_2_255", "موصولة"),
    ]


def test_only_one_hadhan_competitor_is_described_by_the_framework() -> None:
    rows = audit_card(_card("hadhan_20_63.yaml")).تصنيف_أسباب_الإخلال_بالفهم

    assert [classification for _, classification in rows].count(NOT_APPLICABLE) == 3
    assert [reading for reading, cause in rows if cause != NOT_APPLICABLE] == [
        "تخفيف_إن_وضمير_شأن"
    ]
