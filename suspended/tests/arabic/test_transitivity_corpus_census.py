"""اختباراتُ قياس اللزوم والتعدّي على المدوَّنة الصرفية المُبصَّمة.

والأسطرُ المكتوبة هنا **مُصطنَعةٌ مُصرَّحٌ بجنسها**، لا مقتطعةٌ من المدوَّنة:
رخصتُها تمنع نسخَ بايتاتها إلى هذه الشجرة. وبنيتُها وحدَها هي المُحاكاة.

وفيها الحالتان اللتان تكسران أقربَ قراءةٍ خاطئة: فعلٌ معلومٌ **بلا** وَسْم
`ACT` (فمن اشترط حضورَه خرج بصفر)، وفعلٌ مجرَّدٌ بلا وَسْم `(I)` (فمن اشترط
حضورَه خرج بصفرٍ آخر).

وإعادةُ الاشتقاق من البايتات نفسِها اختبارٌ اختياريّ يُفعَّل بمتغيّر بيئةٍ
مُسمًّى، لأنّ البايتات ليست في الشجرة ولن تكون.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from alghanem.arabic.hollow_root_root_census import (
    SegmentRecord,
    corpus_lines,
    parse_segment_line,
)
from alghanem.arabic.transitivity_corpus_census import (
    ARRIVING_FIGURE_DIVERGENCES,
    AUGMENTED_PASSIVE_EXAMPLES,
    REDERIVED_ACTIVE_PARTICIPLE_TEST,
    REDERIVED_AUGMENTED_PASSIVE_TEST,
    REDERIVED_BARE_PERFECT_ACTIVE_ROOTS,
    REDERIVED_CONFIRMED_TRANSITIVE,
    REDERIVED_INTRANSITIVE_CANDIDATES,
    REDERIVED_PARTICIPLE_RATES,
    REDERIVED_PASSIVE_PARTICIPLE_TEST,
    REDERIVED_TAGGED_ROOTS,
    REDERIVED_TENSE_SPLIT,
    TRANSITIVITY_CENSUS_NAMED_RESIDUALS,
    ParticipleRates,
    Tense,
    TransitivityCensusError,
    Voice,
    participle_rates,
    partition_roots,
    permutation_test,
    read_segment,
    root_profiles,
    tense_split,
)
from alghanem.arabic.transitivity_probe_preregistration import (
    PERMUTATION_PROTOCOL,
    TransitivityClass,
)

CORPUS_PATH_VARIABLE = "ALGHANEM_QAC_MORPHOLOGY_PATH"

HAND_BUILT_LINES: tuple[str, ...] = (
    "# a copyright block line, not a segment",
    "LOCATION\tFORM\tTAG\tFEATURES",
    # جذرٌ متعدٍّ مؤكَّد: ماضٍ مجرَّدٌ معلومٌ بلا ACT، وماضٍ مجرَّدٌ مجهول
    "(1:1:1:1)\tkataba\tV\tSTEM|POS:V|PERF|LEM:katab|ROOT:ktb|3MS",
    "(1:1:2:1)\tkutiba\tV\tSTEM|POS:V|PERF|PASS|LEM:katab|ROOT:ktb|3MS",
    "(1:1:3:1)\tmakotuwb\tN\tSTEM|POS:N|PASS|PCPL|LEM:makotuwb|ROOT:ktb|M|NOM",
    # جذرٌ مرشَّحٌ لازم: ماضٍ مجرَّدٌ معلومٌ ولا مجهولَ مجرَّد، ومجهولٌ في وزنٍ مزيد
    "(2:1:1:1)\tEalima\tV\tSTEM|POS:V|PERF|LEM:Ealim|ROOT:Elm|3MS",
    "(2:1:2:1)\tEul~ima\tV\tSTEM|POS:V|PERF|PASS|(II)|LEM:Eal~ama|ROOT:Elm|3MS",
    "(2:1:3:1)\tyuEolamu\tV\tSTEM|POS:V|IMPF|PASS|LEM:Ealim|ROOT:Elm|3MS",
    "(2:1:4:1)\tEaAlim\tN\tSTEM|POS:N|ACT|PCPL|LEM:EaAlim|ROOT:Elm|M|NOM",
    # جذرٌ بلا ماضٍ مجرَّدٍ معلومٍ البتّة: خارجَ مجال التقسيم كلِّه
    "(3:1:1:1)\t>anozala\tV\tSTEM|POS:V|PERF|(IV)|LEM:>anozala|ROOT:nzl|3MS",
    # مقطعٌ بلا جذرٍ أصلًا: لا يدخل في أيّ عدّ
    "(3:1:2:1)\t{l\tDET\tPREFIX|Al+",
)


def hand_built_records() -> list[SegmentRecord]:
    return [
        record
        for record in (parse_segment_line(line) for line in HAND_BUILT_LINES)
        if record is not None
    ]


def record_at(location: str) -> SegmentRecord:
    """المقطعُ بموضعه لا بترتيبه: الترتيبُ يتبدّل بزيادة سطرٍ مُصطنَعٍ واحد."""

    for record in hand_built_records():
        if record.location == location:
            return record
    raise AssertionError(f"لا مقطعَ مُصطنَعًا في الموضع {location}")


def test_an_active_verb_is_read_from_the_absence_of_pass_not_the_presence_of_act() -> (
    None
):
    record = record_at("(1:1:1:1)")

    reading = read_segment(record)

    assert reading is not None
    assert reading.voice is Voice.ACTIVE
    assert reading.tense is Tense.PERFECT
    assert reading.is_bare


def test_a_bare_form_is_read_from_the_absence_of_a_form_tag() -> None:
    augmented = read_segment(record_at("(3:1:1:1)"))

    assert augmented is not None
    assert augmented.form == "IV"
    assert not augmented.is_bare


def test_a_segment_without_a_root_is_not_read_as_a_reading() -> None:
    assert read_segment(record_at("(3:1:2:1)")) is None


def test_a_segment_with_a_root_and_no_part_of_speech_is_refused() -> None:
    record = SegmentRecord(
        sura=1,
        aya=1,
        word=1,
        segment=1,
        form="kataba",
        tag="V",
        features="STEM|PERF|ROOT:ktb",
    )

    with pytest.raises(TransitivityCensusError):
        read_segment(record)


def test_the_partition_separates_the_two_classes_by_the_bare_passive_perfect() -> None:
    profiles = root_profiles(hand_built_records())

    partition = partition_roots(profiles)

    assert partition.confirmed_transitive == ("ktb",)
    assert partition.intransitive_candidates == ("Elm",)
    assert "nzl" not in partition.confirmed_transitive
    assert "nzl" not in partition.intransitive_candidates


def test_a_root_may_carry_a_bare_imperfect_passive_without_a_bare_perfect_one() -> None:
    profiles = root_profiles(hand_built_records())

    split = tense_split(profiles)

    assert split.imperfect_passive_only == 1
    assert profiles["Elm"].has_bare(Tense.IMPERFECT, Voice.PASSIVE)
    assert not profiles["Elm"].has_bare(Tense.PERFECT, Voice.PASSIVE)


def test_an_augmented_passive_is_kept_apart_from_a_bare_one() -> None:
    profiles = root_profiles(hand_built_records())

    assert profiles["Elm"].has_augmented_passive()
    assert profiles["Elm"].augmented_passive_forms() == ("II",)
    assert not profiles["ktb"].has_augmented_passive()


def test_participle_rates_count_roots_not_segments() -> None:
    profiles = root_profiles(hand_built_records())
    partition = partition_roots(profiles)

    rates = participle_rates(
        profiles,
        partition.roots_of(TransitivityClass.CONFIRMED_TRANSITIVE),
        TransitivityClass.CONFIRMED_TRANSITIVE,
    )

    assert rates.group_size == 1
    assert rates.passive_participle_roots == 1
    assert rates.passive_percentage == 100.0


def test_an_empty_group_is_refused_rather_than_divided_by_zero() -> None:
    with pytest.raises(TransitivityCensusError):
        ParticipleRates(
            transitivity_class=TransitivityClass.CONFIRMED_TRANSITIVE,
            group_size=0,
            active_participle_roots=0,
            passive_participle_roots=0,
        )


def test_the_permutation_test_is_deterministic_under_its_declared_seed() -> None:
    first = [True] * 8 + [False] * 2
    second = [False] * 8 + [True] * 2

    one = permutation_test("فارقٌ مُصطنَع", first, second, seed=7, permutations=200)
    two = permutation_test("فارقٌ مُصطنَع", first, second, seed=7, permutations=200)

    assert one == two
    assert one.p_value == (1 + one.at_least_as_extreme) / 201


def test_a_permutation_p_value_never_reaches_zero() -> None:
    outcome = permutation_test(
        "فارقٌ مُصطنَع",
        [True] * 10,
        [False] * 10,
        seed=PERMUTATION_PROTOCOL.seed,
        permutations=100,
    )

    assert outcome.p_value == 1 / 101
    assert outcome.p_value > 0


def test_the_arriving_figures_are_recorded_as_diverged_not_silently_dropped() -> None:
    assert len(ARRIVING_FIGURE_DIVERGENCES) == 15
    assert not any(item.matched for item in ARRIVING_FIGURE_DIVERGENCES)
    assert (
        "TheArrivingNumbersDidNotMatchAndTheRuleWasNotTuned"
        in TRANSITIVITY_CENSUS_NAMED_RESIDUALS
    )


def test_the_frozen_totals_agree_with_one_another() -> None:
    assert (
        REDERIVED_CONFIRMED_TRANSITIVE + REDERIVED_INTRANSITIVE_CANDIDATES
        == REDERIVED_BARE_PERFECT_ACTIVE_ROOTS
    )
    sizes = {
        item.transitivity_class: item.group_size for item in REDERIVED_PARTICIPLE_RATES
    }
    assert (
        sizes[TransitivityClass.CONFIRMED_TRANSITIVE] == REDERIVED_CONFIRMED_TRANSITIVE
    )
    assert (
        sizes[TransitivityClass.INTRANSITIVE_CANDIDATE]
        == REDERIVED_INTRANSITIVE_CANDIDATES
    )


def test_the_passive_participle_gap_is_significant_and_the_active_one_is_too() -> None:
    assert REDERIVED_PASSIVE_PARTICIPLE_TEST.p_value == 1 / 5001
    assert REDERIVED_ACTIVE_PARTICIPLE_TEST.p_value < 0.01
    assert (
        REDERIVED_ACTIVE_PARTICIPLE_TEST.observed_gap_points
        < REDERIVED_ACTIVE_PARTICIPLE_TEST.maximum_null_gap_points
    )


def test_the_augmentation_hypothesis_is_refuted_as_a_rule_not_as_a_possibility() -> (
    None
):
    assert REDERIVED_AUGMENTED_PASSIVE_TEST.p_value > 0.05
    assert len(AUGMENTED_PASSIVE_EXAMPLES) == 3
    assert {item.form for item in AUGMENTED_PASSIVE_EXAMPLES} == {"II", "IV", "X"}


@pytest.mark.skipif(
    not os.environ.get(CORPUS_PATH_VARIABLE),
    reason=(
        "the Quranic Arabic Corpus bytes are not vendored in this repository "
        "and never will be: its GPL licence and the CC BY-ND Tanzil text it "
        f"embeds forbid modification. Set {CORPUS_PATH_VARIABLE} to the exact "
        "quranic-corpus-morphology-0.4.txt named in the witness to re-derive "
        "the census here"
    ),
)
def test_the_frozen_census_rederives_from_the_witness_bytes() -> None:
    path = Path(os.environ[CORPUS_PATH_VARIABLE])

    records = [
        record
        for record in (parse_segment_line(line) for line in corpus_lines(path))
        if record is not None
    ]
    profiles = root_profiles(records)
    partition = partition_roots(profiles)

    assert len(profiles) == REDERIVED_TAGGED_ROOTS
    assert len(partition.confirmed_transitive) == REDERIVED_CONFIRMED_TRANSITIVE
    assert len(partition.intransitive_candidates) == REDERIVED_INTRANSITIVE_CANDIDATES
    assert tense_split(profiles) == REDERIVED_TENSE_SPLIT
    for frozen in REDERIVED_PARTICIPLE_RATES:
        assert (
            participle_rates(
                profiles,
                partition.roots_of(frozen.transitivity_class),
                frozen.transitivity_class,
            )
            == frozen
        )
    assert (
        permutation_test(
            REDERIVED_PASSIVE_PARTICIPLE_TEST.label,
            [
                profiles[root].has_participle(Voice.PASSIVE)
                for root in partition.confirmed_transitive
            ],
            [
                profiles[root].has_participle(Voice.PASSIVE)
                for root in partition.intransitive_candidates
            ],
        )
        == REDERIVED_PASSIVE_PARTICIPLE_TEST
    )
