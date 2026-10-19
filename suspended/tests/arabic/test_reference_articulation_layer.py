"""شواهدُ الطبقة المرجعيّة: كلُّ عددٍ يُعاد اشتقاقُه، ولا مُخرَجَ يُرقَّى."""

from __future__ import annotations

import pytest

from alghanem.arabic.fath_ayah_source_text import (
    FATH_AYAH_NAMED_RESIDUALS,
    FATH_AYAH_SOURCE_TEXT,
    TRANSCRIPTION_STANDING,
    TranscriptionStanding,
    source_byte_length,
    source_sha256,
    written_word_count,
)
from alghanem.arabic.reference_articulation_layer import (
    REFERENCE_ARTICULATION_NAMED_RESIDUALS,
    THE_AXES,
    THE_REFERENCE_INVENTORY,
    Axis,
    InternalLawStanding,
    Manner,
    PhoneticWaslAndWaqfRemainDeferred,
    PlaceGranularity,
    ReferenceArticulationError,
    ReferencePattern,
    add_constraint,
    assess_internal_law,
    axis_deletion_experiment,
    granularity_sensitivity,
    read_the_deposited_ayah,
    the_empty_constraint,
    transition_census,
)


def test_the_deposited_ayah_derives_its_own_digest_and_counts() -> None:
    """البصمةُ والأعدادُ مُشتقّةٌ من الحروف، ورتبةُ النقل هي الدنيا."""

    assert (
        source_sha256()
        == __import__("hashlib")
        .sha256(FATH_AYAH_SOURCE_TEXT.encode("utf-8"))
        .hexdigest()
    )
    assert source_byte_length() == len(FATH_AYAH_SOURCE_TEXT.encode("utf-8"))
    assert written_word_count() == len(FATH_AYAH_SOURCE_TEXT.split())
    assert TRANSCRIPTION_STANDING is (
        TranscriptionStanding.TRANSCRIBED_IN_TREE_NOT_COLLATED
    )
    assert "AN_EXTERNAL_RUNS_DIGEST_IS_NOT_THIS_DEPOSITS_DIGEST" in (
        FATH_AYAH_NAMED_RESIDUALS
    )


def test_the_inventory_is_twenty_eight_patterns_with_distinct_vectors() -> None:
    """ثمانيةٌ وعشرون نمطًا، لا حرفَ مكرَّرًا ولا مُتَّجِهَين متطابقين."""

    assert len(THE_REFERENCE_INVENTORY) == 28
    assert len({one.letter for one in THE_REFERENCE_INVENTORY}) == 28
    assert len({one.vector() for one in THE_REFERENCE_INVENTORY}) == 28
    assert len(THE_AXES) == 4


def test_a_reference_pattern_is_named_by_one_letter() -> None:
    """حارسُ البناء يرفض تسميةَ نمطٍ بأكثرَ من حرف."""

    with pytest.raises(ReferenceArticulationError):
        ReferencePattern(
            letter="با",
            manner=THE_REFERENCE_INVENTORY[1].manner,
            place=THE_REFERENCE_INVENTORY[1].place,
            voicing=THE_REFERENCE_INVENTORY[1].voicing,
            emphasis=THE_REFERENCE_INVENTORY[1].emphasis,
        )


def test_the_reading_partitions_every_written_occurrence() -> None:
    """كلُّ وقعةٍ مكتوبةٍ إمّا مُعيَّنةٌ وإمّا مُسجَّلةُ الامتناع؛ لا ثالثَ ولا مهمَل."""

    reading = read_the_deposited_ayah()
    assert reading.written_occurrence_count == len(reading.resolved) + len(
        reading.unresolved
    )
    assert sum(reading.unresolved_by_graphic.values()) == len(reading.unresolved)
    assert set(reading.unresolved_by_graphic) <= set("اوىيةآ")


def test_the_carrier_ambiguous_graphics_are_never_resolved() -> None:
    """الواوُ والياءُ لا تُعيَّنان من الرسم، فلا تُشاهَدان مرشَّحتَين بلا لبس."""

    reading = read_the_deposited_ayah()
    unobserved = {one.letter for one in reading.unobserved_patterns}
    assert {"و", "ي"} <= unobserved
    assert all(one.graphic in "اوىيةآ" for one in reading.unresolved)


def test_each_axis_is_necessary_for_this_chosen_coding() -> None:
    """حذفُ كلّ محورٍ يُدمِج نمطين، بشواهدَ مُسمّاةٍ مفحوصةٍ بالتشغيل."""

    merged = {
        axis: {
            frozenset(group) for group in axis_deletion_experiment(axis).merged_groups
        }
        for axis in THE_AXES
    }
    assert all(groups for groups in merged.values())
    assert any({"ب", "م"} <= set(group) for group in merged[Axis.MANNER])
    assert frozenset({"ت", "د"}) in merged[Axis.VOICING]
    assert frozenset({"س", "ص"}) in merged[Axis.EMPHASIS]
    assert any({"ت", "ك"} <= set(group) for group in merged[Axis.PLACE])


def test_no_deletion_leaves_the_inventory_fully_distinct() -> None:
    """عددُ المخرجات بعد أيّ حذفٍ أقلُّ من ثمانيةٍ وعشرين، وهو مُشتقٌّ لا مكتوب."""

    for axis in THE_AXES:
        result = axis_deletion_experiment(axis)
        assert result.axis_is_necessary_here is True
        assert result.distinct_output_count < len(THE_REFERENCE_INVENTORY)


def test_the_place_granularity_changes_the_emphasis_result() -> None:
    """النتيجةُ السالبةُ الأقوى: تبديلُ دقّة المخرج يبدّل أزواجَ الروادف."""

    sensitivity = granularity_sensitivity()
    fine = sensitivity[PlaceGranularity.FINE].merged_groups
    coarse = sensitivity[PlaceGranularity.COARSE].merged_groups
    assert fine != coarse
    assert len(coarse) > len(fine)
    assert ("س", "ص") in fine
    assert ("س", "ص") not in coarse


def test_the_transition_census_is_counted_but_stays_deferred() -> None:
    """الأزواجُ تُحصى، والوصلُ والوقفُ الصوتيّان باقيان على الإرجاء."""

    reading = read_the_deposited_ayah()
    census = transition_census(reading)
    assert census.pair_count == len(census.pairs)
    assert census.pair_count > 0
    assert len(census.transition_types) <= census.pair_count
    assert census.phonetic_wasl_and_waqf is (PhoneticWaslAndWaqfRemainDeferred.DEFER)
    assert len(PhoneticWaslAndWaqfRemainDeferred) == 1


def test_a_pair_never_crosses_a_word_boundary() -> None:
    """لا زوجَ بين كلمتين؛ فما بينهما يمسّ الوصلَ وهو مُرجأ."""

    reading = read_the_deposited_ayah()
    single_word = read_the_deposited_ayah("مُحَمَّدٌ")
    assert (
        transition_census(single_word).pair_count
        < transition_census(reading).pair_count
    )
    assert transition_census(read_the_deposited_ayah("بَ تَ")).pair_count == 0


def test_the_empty_constraint_is_neutral_for_every_pattern() -> None:
    """`e ⊕ p = p` لكلّ نمط؛ وهو فحصُ اتّساقٍ لا اكتشاف."""

    for pattern in THE_REFERENCE_INVENTORY:
        constraint: dict[Axis, object] = {
            Axis.MANNER: pattern.manner,
            Axis.PLACE: pattern.place,
            Axis.VOICING: pattern.voicing,
            Axis.EMPHASIS: pattern.emphasis,
        }
        assert add_constraint(the_empty_constraint(), constraint) == constraint
        assert add_constraint(constraint, the_empty_constraint()) == constraint
    assert the_empty_constraint() == {}


def test_conflicting_constraints_are_refused_not_arbitrated() -> None:
    """قيدان متعارضان يُرَدّان؛ ولا يُرجَّح أحدُهما ضمنًا."""

    with pytest.raises(ReferenceArticulationError):
        add_constraint({Axis.MANNER: Manner.STOP}, {Axis.MANNER: Manner.FRICATIVE})


def test_the_outcome_is_a_relative_necessity_not_a_born_law() -> None:
    """المُخرَجُ ضرورةٌ نسبيّةٌ لترميزٍ مختار، ولا ليفَ مولودًا ولا فيبوناتشي."""

    decision = assess_internal_law()
    assert decision.standing is (
        InternalLawStanding.RELATIVE_NECESSITY_OF_A_CHOSEN_CODING
    )
    assert decision.standing is not InternalLawStanding.A_MINIMAL_INTERNAL_LAW_IS_BORN
    assert set(decision.necessary_axes) == set(THE_AXES)
    assert decision.granularity_changes_the_result is True
    assert decision.a_mechanical_fiber_is_born is False
    assert decision.a_fibonacci_law_is_extracted is False


def test_the_named_residuals_are_deposited_with_their_own_names() -> None:
    """كلُّ بقيّةٍ تحمل اسمَها في نصّها، فلا يُبدَّل الاسمُ دون النصّ."""

    assert len(REFERENCE_ARTICULATION_NAMED_RESIDUALS) == 11
    for name, text in REFERENCE_ARTICULATION_NAMED_RESIDUALS.items():
        assert text.startswith(f"{name}: ")
    assert "NO_FIBONACCI_LAW_IS_EXTRACTED_HERE" in (
        REFERENCE_ARTICULATION_NAMED_RESIDUALS
    )
    assert "NO_MECHANICAL_FIBER_IS_BORN_HERE" in REFERENCE_ARTICULATION_NAMED_RESIDUALS
