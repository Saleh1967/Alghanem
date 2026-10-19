"""تجاربُ قطاعات العقدة: تعدادُ Γ(π)، وتمييزُ الأجناس، وحوسبةُ السلسلة."""

from __future__ import annotations

import pytest

from alghanem.arabic.position_bundle_sections import (
    ASCENT_CHAIN_AS_DECLARED,
    POSITION_BUNDLE_NAMED_RESIDUALS,
    THE_DECLARED_FIBRE,
    THE_FINAL_POSITION_GRID,
    THE_FIRST_POSITION_GRID,
    BaseState,
    ConstantLawStanding,
    OccurrenceLabelling,
    PositionBundleError,
    Section,
    assess_constant_law,
    entropy_bits,
    fibre_of,
    pushforward_to_base,
    read_ascent_chain,
    run_position_bundle,
    sections,
    total_space,
)

_READING = run_position_bundle()


def test_the_fibre_is_one_over_zero_and_three_over_one() -> None:
    """الليفُ مُعلَنٌ `{1, 3}`، والفضاءُ الكلّيُّ أربعُ نقاطٍ لا أكثر."""

    assert len(fibre_of(BaseState.QUIESCENT)) == 1
    assert len(fibre_of(BaseState.MOVING)) == 3
    assert len(total_space()) == 4
    assert _READING.total_space_size == 4
    assert set(THE_DECLARED_FIBRE) == set(BaseState)


def test_the_sections_are_three_and_all_quiescent_at_zero() -> None:
    """`|Γ(π)| = 1 × 3 = 3`، وكلُّها تأخذ «سكون» فوق `b=0`."""

    found = sections()
    assert len(found) == 3
    assert _READING.section_count == 3
    assert _READING.every_section_is_quiescent_at_zero
    assert {section.choice[BaseState.MOVING] for section in found} == {
        "فتحة",
        "كسرة",
        "ضمة",
    }
    assert all(section.projects_to_identity() for section in found)


def test_a_section_missing_a_base_point_is_refused() -> None:
    """قطاعٌ لا يُسنِد فوق كلّ نقطةٍ قاعديّةٍ ليس قطاعًا ناقصًا بل ليس بقطاع."""

    with pytest.raises(PositionBundleError):
        Section(choice={BaseState.MOVING: "فتحة"})


def test_a_section_out_of_its_fibre_is_refused() -> None:
    """«سكون» فوق `b=1` ينقض `π∘s = id`، فيُردّ عند الإنشاء."""

    with pytest.raises(PositionBundleError):
        Section(choice={BaseState.QUIESCENT: "سكون", BaseState.MOVING: "سكون"})


def test_the_two_grids_conserve_their_declared_denominators() -> None:
    """مجموعُ الأعمدة الأربعةِ محسوبًا يُطابق المقامَ المُعلَن في الجدولين."""

    assert THE_FIRST_POSITION_GRID.recomputed_total == 78215
    assert THE_FIRST_POSITION_GRID.conserves_the_declared_denominator
    assert THE_FINAL_POSITION_GRID.recomputed_total == 78076
    assert THE_FINAL_POSITION_GRID.conserves_the_declared_denominator


def test_the_pushforward_reproduces_the_supplied_shares() -> None:
    """الدفعُ الأماميُّ يُخرِج ٨٧٫٨٣٪ و١٢٫١٧٪ حسابًا لا نقلًا."""

    shares = pushforward_to_base(THE_FINAL_POSITION_GRID)
    assert round(shares[BaseState.MOVING] * 100, 2) == 87.83
    assert round(shares[BaseState.QUIESCENT] * 100, 2) == 12.17


def test_both_constant_laws_are_refuted_by_the_supplied_columns() -> None:
    """«ثابتٌ قطعيّ» مكذوبٌ في الموضعين بعمودِ الجدولِ نفسِه."""

    inchoative = _READING.inchoative_law
    pausal = _READING.pausal_law
    assert inchoative.standing is ConstantLawStanding.REFUTED_BY_THE_SUPPLIED_COLUMN
    assert inchoative.counterexamples == 10339
    assert round(inchoative.counterexample_share * 100, 4) == 13.2187
    assert pausal.standing is ConstantLawStanding.REFUTED_BY_THE_SUPPLIED_COLUMN
    assert pausal.counterexamples == 68576
    assert round(pausal.counterexample_share * 100, 4) == 87.8324


def test_the_pausal_law_entropy_is_not_zero() -> None:
    """دعوى `H=0` مكذوبةٌ: عطالةُ القاعدة في الموضع الأخير ≈ 0.5342 بِتّ."""

    assert round(_READING.pausal_law.base_entropy_bits, 6) == 0.534160
    assert round(_READING.inchoative_law.base_entropy_bits, 6) == 0.563405
    assert round(THE_FINAL_POSITION_GRID.total_entropy_bits, 6) == 1.876082


def test_the_last_ascent_step_does_not_agree_with_its_written_output() -> None:
    """`116 × 734/29 = 2936` لا `21286`، والنسبةُ بينهما `29/4` بالضبط."""

    chain = read_ascent_chain()
    assert len(chain) == len(ASCENT_CHAIN_AS_DECLARED) == 3
    assert chain[0].agrees and chain[1].agrees
    last = chain[2]
    assert not last.agrees
    assert last.recomputed_output == 2936.0
    assert last.step.declared_output == 21286
    assert round(last.declared_over_recomputed, 6) == round(29 / 4, 6)
    assert _READING.chain_disagreements == (last,)


def test_entropy_refuses_a_non_positive_total() -> None:
    """لا عطالةَ على مجموعٍ غيرِ موجب، ولا عدٍّ سالبٍ يُقرأ تكرارًا."""

    with pytest.raises(PositionBundleError):
        entropy_bits({"أ": 0})
    with pytest.raises(PositionBundleError):
        entropy_bits({"أ": -1, "ب": 5})


def test_a_labelling_refuses_a_non_positive_denominator() -> None:
    """مقامٌ غيرُ موجبٍ لا تُقسَم عليه نسبة، ويُردّ عند الإنشاء."""

    with pytest.raises(PositionBundleError):
        OccurrenceLabelling(
            position="موضعٌ مُصطنَع",
            fatha=1,
            kasra=1,
            damma=1,
            sukun=1,
            declared_denominator=0,
            source="مُصطنَعٌ في التجربة",
        )


def test_a_constant_law_may_stand_on_counts_that_do_not_refute_it() -> None:
    """الحكمُ مقيسٌ لا محتوم: عمودٌ خالٍ من المخالف لا يُكذِّب الدعوى."""

    labelling = OccurrenceLabelling(
        position="موضعٌ مُصطنَع",
        fatha=0,
        kasra=0,
        damma=0,
        sukun=7,
        declared_denominator=7,
        source="مُصطنَعٌ في التجربة، ولا يخرج منه رقمٌ عن مدوَّنة",
    )
    reading = assess_constant_law(labelling, BaseState.QUIESCENT)
    assert reading.standing is ConstantLawStanding.NOT_REFUTED_IN_THESE_COUNTS
    assert reading.counterexamples == 0
    assert reading.base_entropy_bits == 0.0


def test_the_named_residuals_are_present_and_self_naming() -> None:
    """كلُّ بقيّةٍ تحمل اسمَها في نصِّها، ولا حقلَ سلطةٍ في البنى."""

    assert len(POSITION_BUNDLE_NAMED_RESIDUALS) >= 11
    for name, text in POSITION_BUNDLE_NAMED_RESIDUALS.items():
        assert text.startswith(f"{name}: ")
