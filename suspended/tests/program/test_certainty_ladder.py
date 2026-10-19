"""اختبارات سُلَّم اليقين: لا رتبةَ مطلقة، والسقفُ مُشتَقٌّ لا مكتوب."""

from __future__ import annotations

import pkgutil

import pytest

import alghanem.kernel as kernel_package
from alghanem.arabic.encoding.carrier_state_candidate import (
    DECLARED_CARRIERS,
    CarrierState,
)
from alghanem.program.certainty_ladder import (
    CERTAINTY_LADDER_NAMED_RESIDUALS,
    CORPUS_BOUNDED_LAW_NAME,
    LADDER_RUNGS,
    CertaintyLadderError,
    LadderRung,
    RungAssessment,
    RungStanding,
    derive_declared_carrier_state_product,
    derive_embedded_round_trip_span,
    derive_ladder_ceiling,
    rung_assessment,
)
from alghanem.program.direct_certainty import (
    REPORTED_UNVERIFIED_FIGURES,
    CertaintySourceGenus,
)

# --- لا عضوَ اسمُه يقينٌ مطلق، وذلك أصلُ التصحيح -----------------------------


def test_no_standing_supports_an_unqualified_hundred_percent_claim() -> None:
    assert not any(standing.supports_an_unqualified_claim for standing in RungStanding)


def test_the_standing_vocabulary_holds_no_absolute_member() -> None:
    names = {standing.name for standing in RungStanding}
    assert not any("ABSOLUTE" in name or "PROVEN" in name for name in names)
    assert len(RungStanding) == 3


def test_every_rung_carries_a_standing_a_reason_and_a_named_constraint() -> None:
    for rung in LADDER_RUNGS:
        assessment = rung_assessment(rung)
        assert assessment.rung is rung
        assert assessment.reason.strip()
        assert assessment.named_constraint.strip()


def test_an_assessment_without_a_reason_or_a_constraint_is_refused() -> None:
    with pytest.raises(CertaintyLadderError, match="بلا علّةٍ مكتوبة"):
        RungAssessment(
            rung=LadderRung.BITS_TO_NUMBER,
            standing=RungStanding.CERTAIN_RELATIVE_TO_A_DECLARATION,
            reason="  ",
            named_constraint="X",
        )
    with pytest.raises(CertaintyLadderError, match="تحت قيدٍ مُسمًّى"):
        RungAssessment(
            rung=LadderRung.BITS_TO_NUMBER,
            standing=RungStanding.CERTAIN_RELATIVE_TO_A_DECLARATION,
            reason="علّة",
            named_constraint=" ",
        )


def test_a_rung_outside_the_closed_vocabulary_is_refused() -> None:
    with pytest.raises(CertaintyLadderError, match="عضوٌ في `LadderRung`"):
        rung_assessment("bits_to_number")  # type: ignore[arg-type]


# --- الدرجتان الأوليان: يقينٌ نسبيٌّ إلى إعلان --------------------------------


def test_the_first_two_rungs_are_certain_only_relative_to_a_declaration() -> None:
    for rung in (LadderRung.BITS_TO_NUMBER, LadderRung.NUMBER_TO_CARRIER_STATE):
        assert (
            rung_assessment(rung).standing
            is RungStanding.CERTAIN_RELATIVE_TO_A_DECLARATION
        )


def test_the_carrier_rung_names_the_declaration_it_rests_on() -> None:
    assessment = rung_assessment(LadderRung.NUMBER_TO_CARRIER_STATE)
    assert assessment.named_constraint == "CARRIER_SET_IS_DECLARED_NOT_DERIVED"


# --- الدرجة الثالثة: موضعُ التصحيح -------------------------------------------


def test_the_round_trip_rung_is_corpus_bounded_and_not_certain() -> None:
    assessment = rung_assessment(LadderRung.CARRIER_STATE_TO_VOCALIZED_TEXT)
    assert assessment.standing is RungStanding.CORPUS_BOUNDED_INDUCTION
    assert CORPUS_BOUNDED_LAW_NAME in assessment.reason


def test_the_corpus_bounded_law_is_written_in_the_constitution() -> None:
    with open("docs/CONSTITUTION.md", encoding="utf-8") as handle:
        text = handle.read()
    assert CORPUS_BOUNDED_LAW_NAME in text


# --- الدرجتان الأخيرتان، والسقفُ المُشتَقّ -------------------------------------


def test_the_last_two_rungs_are_not_reached() -> None:
    for rung in (LadderRung.VOCALIZED_TEXT_TO_SYNTAX, LadderRung.TEXT_TO_MEANING):
        assert (
            rung_assessment(rung).standing
            is RungStanding.NOT_REACHED_WITH_A_COUNTEREXAMPLE_IN_HAND
        )


def test_the_ceiling_is_derived_by_walking_the_rungs_in_order() -> None:
    ceiling = derive_ladder_ceiling()
    assert ceiling is LadderRung.CARRIER_STATE_TO_VOCALIZED_TEXT
    assert ceiling.position == 2


def test_the_ceiling_is_not_a_rung_that_was_reached_with_certainty() -> None:
    standing = rung_assessment(derive_ladder_ceiling()).standing
    assert standing is not RungStanding.CERTAIN_RELATIVE_TO_A_DECLARATION
    assert not standing.supports_an_unqualified_claim


def test_the_rungs_are_five_and_their_positions_are_contiguous() -> None:
    assert [rung.position for rung in LADDER_RUNGS] == list(range(5))


# --- ما تُخرجه الشجرة فعلًا، مقابلًا للمنقول ----------------------------------


def test_the_declared_product_is_derived_from_this_tree_now() -> None:
    carriers, states, product = derive_declared_carrier_state_product()
    assert carriers == len(DECLARED_CARRIERS)
    assert states == len(CarrierState)
    assert product == carriers * states


def test_the_derived_product_is_not_the_quoted_figure() -> None:
    _, _, product = derive_declared_carrier_state_product()
    assert product != 131


def test_the_round_trip_span_this_tree_can_re_run_is_small_and_holds() -> None:
    span, holds = derive_embedded_round_trip_span()
    assert holds
    assert 0 < span < 100


def test_the_quoted_ladder_figures_are_filed_as_prose_not_measurement() -> None:
    subjects = " ".join(record.subject for record in REPORTED_UNVERIFIED_FIGURES)
    figures = " ".join(record.figure_text for record in REPORTED_UNVERIFIED_FIGURES)
    assert "الحامل/الحالة" in subjects
    assert "١٣١/١٣١" in figures
    assert "٧٨٬٢٤٥" in figures
    assert "٢٨/٢٨" in figures
    for record in REPORTED_UNVERIFIED_FIGURES:
        assert record.source_genus is not (
            CertaintySourceGenus.RERUN_NOW_IN_THIS_PROCESS
        )


# --- السلطة: هذا السُّلَّم خامل -------------------------------------------------


def test_no_kernel_module_reads_the_ladder() -> None:
    for module in pkgutil.iter_modules(kernel_package.__path__):
        path = f"{kernel_package.__path__[0]}/{module.name}.py"
        try:
            with open(path, encoding="utf-8") as handle:
                source = handle.read()
        except OSError:  # pragma: no cover - a package, not a module file
            continue
        assert "certainty_ladder" not in source


def test_every_named_residual_is_reachable_and_names_itself() -> None:
    assert len(CERTAINTY_LADDER_NAMED_RESIDUALS) == 4
    for name, text in CERTAINTY_LADDER_NAMED_RESIDUALS.items():
        assert name.isupper()
        assert name in text
