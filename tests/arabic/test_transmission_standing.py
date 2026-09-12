"""Tests for the three transmission standings and the two induction scopes."""

from __future__ import annotations

import json
import pkgutil
from dataclasses import fields
from pathlib import Path

import pytest

import alghanem.kernel as kernel_package
from alghanem.arabic import (
    CLOSED_CORPUS_TEMPORAL_STRUCTURE,
    FIRST_ORGANIZED_INFORMATION_QUESTION,
    EvidenceTemporalStructure,
    ExemptionHypothesis,
    ExemptionOpenQuestion,
    IstiqraScope,
    KnowledgeBasis,
    RepetitionPattern,
    ScopedFinding,
    SourceIndependence,
    TawaturQuestionStanding,
    TransmissionStanding,
    TransmissionStandingError,
    TransmissionStandingRecord,
    UnconstructibilityGenus,
    derive_scope_statement,
    derive_standing,
    tawatur_question_standing,
    unconstructibility_genus,
)
from alghanem.arabic.external_audit import audit_card
from alghanem.arabic.transmission_standing import (
    DESIGN_CONVERGENCE_PROVENANCE_IS_UNVERIFIED,
    MUTAWATIR_IS_UNCONSTRUCTIBLE_NOTE,
    NAMED_RESIDUALS,
    NO_IMPORT_ENTRY_FOR_A_FOREIGN_RECURRENCE_CLAIM_NOTE,
    SIBLING_HOLDS_ARE_NOT_CLASSIFIED_HERE,
    SUCCESSION_CARRIER_IS_WRITABLE_WITHOUT_A_TEMPORAL_AUTHORITY,
)

_EXAMPLES = Path(__file__).resolve().parents[2] / "examples" / "external_audit"
_CARDS = (
    "man_2_255.yaml",
    "maa_2_197.yaml",
    "imran_3_33.yaml",
    "hadhan_20_63.yaml",
)


def record(**overrides: object) -> TransmissionStandingRecord:
    base: dict[str, object] = {
        "report_id": "report-1",
        "basis": KnowledgeBasis.DIRECT_OBSERVATION,
        "independence": SourceIndependence.NOT_ESTABLISHED,
        "repetition": RepetitionPattern.SINGLE_BATCH,
        "declared_standing": TransmissionStanding.AHAD,
        "justification": "\u062a\u062b\u0628\u0651\u062a \u0648\u0627\u062d\u062f",
    }
    base.update(overrides)
    return TransmissionStandingRecord(**base)  # type: ignore[arg-type]


def test_the_three_standings_are_one_closed_vocabulary() -> None:
    assert len(TransmissionStanding) == 3
    assert {standing.value for standing in TransmissionStanding} == {
        "\u0645\u062a\u0648\u0627\u062a\u0631",
        "\u0622\u062d\u0627\u062f",
        "\u0641\u0631\u0636",
    }


@pytest.mark.parametrize(
    ("independence", "repetition", "expected"),
    (
        (
            SourceIndependence.COLLUSION_IMPOSSIBLE,
            RepetitionPattern.SUCCESSIVE_GENERATIONS,
            TransmissionStanding.MUTAWATIR,
        ),
        (
            SourceIndependence.COLLUSION_IMPOSSIBLE,
            RepetitionPattern.SINGLE_BATCH,
            TransmissionStanding.AHAD,
        ),
        (
            SourceIndependence.NOT_ESTABLISHED,
            RepetitionPattern.SUCCESSIVE_GENERATIONS,
            TransmissionStanding.AHAD,
        ),
        (
            SourceIndependence.NOT_ESTABLISHED,
            RepetitionPattern.NONE,
            TransmissionStanding.AHAD,
        ),
    ),
)
def test_direct_observation_derives_its_standing_from_the_two_other_carriers(
    independence: SourceIndependence,
    repetition: RepetitionPattern,
    expected: TransmissionStanding,
) -> None:
    assert (
        derive_standing(KnowledgeBasis.DIRECT_OBSERVATION, independence, repetition)
        is expected
    )


@pytest.mark.parametrize("independence", tuple(SourceIndependence))
@pytest.mark.parametrize("repetition", tuple(RepetitionPattern))
def test_inference_without_direct_observation_is_always_fard(
    independence: SourceIndependence, repetition: RepetitionPattern
) -> None:
    assert (
        derive_standing(KnowledgeBasis.INFERENCE, independence, repetition)
        is TransmissionStanding.FARD
    )


def test_a_carrier_outside_its_vocabulary_is_refused_not_approximated() -> None:
    with pytest.raises(TransmissionStandingError):
        derive_standing(
            "\u0645\u0634\u0627\u0647\u062f\u0629",  # type: ignore[arg-type]
            SourceIndependence.NOT_ESTABLISHED,
            RepetitionPattern.NONE,
        )


def test_the_recurrent_standing_is_declared_and_unconstructible() -> None:
    with pytest.raises(TransmissionStandingError, match="غيرُ مستقيم الوضع"):
        record(
            independence=SourceIndependence.COLLUSION_IMPOSSIBLE,
            repetition=RepetitionPattern.SUCCESSIVE_GENERATIONS,
            declared_standing=TransmissionStanding.MUTAWATIR,
        )


def test_claiming_recurrence_over_weaker_carriers_is_refused_by_its_own_message() -> (
    None
):
    with pytest.raises(TransmissionStandingError, match="غيرُ مستقيم الوضع"):
        record(declared_standing=TransmissionStanding.MUTAWATIR)


def test_the_refusal_of_recurrence_names_a_category_mismatch_not_a_missing_tool() -> (
    None
):
    assert "خطأٍ فئويٍّ بنيويّ" in MUTAWATIR_IS_UNCONSTRUCTIBLE_NOTE
    assert "لا بغياب سلطةٍ اليوم" in MUTAWATIR_IS_UNCONSTRUCTIBLE_NOTE
    assert "لا سلطةَ في هذا المستودع" not in MUTAWATIR_IS_UNCONSTRUCTIBLE_NOTE


def test_a_closed_corpus_is_a_synchronic_section_so_the_question_is_ill_posed() -> None:
    assert (
        CLOSED_CORPUS_TEMPORAL_STRUCTURE
        is EvidenceTemporalStructure.SYNCHRONIC_FROZEN_SECTION
    )
    assert unconstructibility_genus(CLOSED_CORPUS_TEMPORAL_STRUCTURE) is (
        UnconstructibilityGenus.REFUSED_BY_STRUCTURAL_CATEGORY_MISMATCH
    )
    assert tawatur_question_standing(CLOSED_CORPUS_TEMPORAL_STRUCTURE) is (
        TawaturQuestionStanding.ILL_POSED_ON_THIS_STRUCTURE
    )


def test_a_diachronic_succession_is_held_by_missing_authority_not_by_category() -> None:
    succession = EvidenceTemporalStructure.DIACHRONIC_INDEPENDENT_SUCCESSION
    assert unconstructibility_genus(succession) is (
        UnconstructibilityGenus.HELD_BY_MISSING_AUTHORITY_TODAY
    )
    assert tawatur_question_standing(succession) is (
        TawaturQuestionStanding.WELL_POSED_AND_UNVERIFIED_HERE
    )


def test_an_unsettled_genus_is_declared_and_never_derived_by_default() -> None:
    assert UnconstructibilityGenus.GENUS_NOT_SETTLED not in {
        unconstructibility_genus(structure) for structure in EvidenceTemporalStructure
    }


def test_a_temporal_structure_outside_its_vocabulary_is_refused() -> None:
    with pytest.raises(TransmissionStandingError, match="مفردتها المغلقة"):
        unconstructibility_genus("\u0645\u0642\u0637\u0639")  # type: ignore[arg-type]


def test_the_residuals_name_the_meta_provenance_and_the_unclassified_siblings() -> None:
    assert set(NAMED_RESIDUALS) == {
        SUCCESSION_CARRIER_IS_WRITABLE_WITHOUT_A_TEMPORAL_AUTHORITY,
        SIBLING_HOLDS_ARE_NOT_CLASSIFIED_HERE,
        DESIGN_CONVERGENCE_PROVENANCE_IS_UNVERIFIED,
    }
    for text in NAMED_RESIDUALS.values():
        assert text.strip()


def test_no_import_entry_exists_for_a_foreign_recurrence_claim() -> None:
    source = (
        Path(__file__).resolve().parents[2]
        / "src"
        / "alghanem"
        / "arabic"
        / "transmission_standing.py"
    ).read_text(encoding="utf-8")
    declarations = tuple(
        line
        for line in source.splitlines()
        if line.startswith(("import ", "from ", "class ", "def "))
    )
    assert not any("Foreign" in line or "Imported" in line for line in declarations)
    assert "\u0641\u0626\u0648\u064a" in (
        NO_IMPORT_ENTRY_FOR_A_FOREIGN_RECURRENCE_CLAIM_NOTE
    )


def test_a_written_standing_that_contradicts_its_carriers_is_refused() -> None:
    with pytest.raises(TransmissionStandingError, match="تخالف المُشتَقّة"):
        record(declared_standing=TransmissionStanding.FARD)


def test_the_derived_standing_is_read_from_the_carriers_not_the_written_field() -> None:
    written = record()
    assert written.standing is TransmissionStanding.AHAD
    assert written.awaits_independent_measurement is False
    assert written.requires_recheck_before_every_acceptance is True

    estimated = record(
        basis=KnowledgeBasis.INFERENCE,
        declared_standing=TransmissionStanding.FARD,
    )
    assert estimated.standing is TransmissionStanding.FARD
    assert estimated.awaits_independent_measurement is True


def test_no_type_here_carries_a_count_or_verdict_field() -> None:
    for declaring_type in (
        TransmissionStandingRecord,
        ScopedFinding,
        ExemptionOpenQuestion,
    ):
        declared = {item.name for item in fields(declaring_type)}
        for marker in ("count", "number", "size", "total", "verdict", "birth"):
            assert not any(marker in name for name in declared), marker


def finding(**overrides: object) -> ScopedFinding:
    scope = overrides.pop("scope", IstiqraScope.COMPLETE_WITHIN_CLOSED_SET)
    enumerated = overrides.pop("enumerated_set", "\u0627\u0644\u0642\u0631\u0622\u0646")
    wider = overrides.pop("wider_set", "\u0627\u0644\u0639\u0631\u0628\u064a\u0629")
    base: dict[str, object] = {
        "finding_id": "finding-1",
        "scope": scope,
        "enumerated_set": enumerated,
        "wider_set": wider,
        "declared_statement": derive_scope_statement(
            scope,  # type: ignore[arg-type]
            enumerated,  # type: ignore[arg-type]
            wider,  # type: ignore[arg-type]
        ),
    }
    base.update(overrides)
    return ScopedFinding(**base)  # type: ignore[arg-type]


def test_a_complete_induction_is_certain_inside_and_presumptive_outside() -> None:
    complete = finding()
    assert complete.is_certain_within_the_enumerated_set is True
    assert complete.is_certain_beyond_the_enumerated_set is False
    assert "\u064a\u0642\u064a\u0646\u064b\u0627 \u062f\u0627\u062e\u0644" in (
        complete.derived_statement
    )
    assert "\u0638\u0646\u064a\u064b\u0651\u0627" in complete.derived_statement


def test_an_incomplete_induction_is_presumptive_on_both_sides() -> None:
    incomplete = finding(scope=IstiqraScope.INCOMPLETE)
    assert incomplete.is_certain_within_the_enumerated_set is False
    assert "\u062a\u0627\u0645\u064b\u0651\u0627" in incomplete.derived_statement


def test_a_statement_generalizing_directly_to_the_wider_set_is_refused() -> None:
    with pytest.raises(TransmissionStandingError, match="تُشتَقّ ولا تُكتَب"):
        ScopedFinding(
            finding_id="finding-1",
            scope=IstiqraScope.COMPLETE_WITHIN_CLOSED_SET,
            enumerated_set="\u0627\u0644\u0642\u0631\u0622\u0646",
            wider_set="\u0627\u0644\u0639\u0631\u0628\u064a\u0629",
            declared_statement=(
                "\u062b\u0628\u062a \u0627\u0644\u0623\u0645\u0631 "
                "\u064a\u0642\u064a\u0646\u064b\u0627 \u0641\u064a "
                "\u0627\u0644\u0639\u0631\u0628\u064a\u0629"
            ),
        )


def test_an_enumerated_set_equal_to_the_wider_set_is_refused() -> None:
    with pytest.raises(TransmissionStandingError, match="لا نطاقَ يُتجاوَز"):
        finding(wider_set="\u0627\u0644\u0642\u0631\u0622\u0646")


def test_the_exemption_question_declares_all_three_hypotheses_and_no_answer() -> None:
    assert FIRST_ORGANIZED_INFORMATION_QUESTION.remains_open is True
    assert set(FIRST_ORGANIZED_INFORMATION_QUESTION.hypotheses) == set(
        ExemptionHypothesis
    )
    declared = {item.name for item in fields(ExemptionOpenQuestion)}
    assert not any(
        marker in name
        for name in declared
        for marker in ("answer", "exemption_granted")
    )


def test_an_exemption_question_missing_a_hypothesis_is_refused() -> None:
    with pytest.raises(TransmissionStandingError, match="ثنائيةً كاذبة"):
        ExemptionOpenQuestion(
            question_id="partial",
            hypotheses=(ExemptionHypothesis.EXEMPT_BY_GENUINE_RECURRENCE,),
            why_open="\u0633\u0628\u0628",
        )


def test_the_module_reads_no_kernel_authority() -> None:
    source = (
        Path(__file__).resolve().parents[2]
        / "src"
        / "alghanem"
        / "arabic"
        / "transmission_standing.py"
    ).read_text(encoding="utf-8")
    imports = tuple(
        line for line in source.splitlines() if line.startswith(("import ", "from "))
    )
    assert imports
    assert not any("kernel" in line for line in imports)


def test_no_kernel_module_reads_the_transmission_standings() -> None:
    for module in pkgutil.walk_packages(
        kernel_package.__path__, prefix="alghanem.kernel."
    ):
        source = module.module_finder.find_spec(  # type: ignore[union-attr]
            module.name
        )
        assert source is not None and source.origin is not None
        text = Path(source.origin).read_text(encoding="utf-8")
        assert "transmission_standing" not in text, module.name
        assert "TransmissionStanding" not in text, module.name
        assert "ScopedFinding" not in text, module.name


@pytest.mark.parametrize("card", _CARDS)
def test_the_standing_record_changes_no_external_audit_field(card: str) -> None:
    before = json.dumps(
        audit_card(_EXAMPLES / card).to_dict(), ensure_ascii=False, sort_keys=True
    )
    record()
    finding()
    after = json.dumps(
        audit_card(_EXAMPLES / card).to_dict(), ensure_ascii=False, sort_keys=True
    )
    assert before == after
