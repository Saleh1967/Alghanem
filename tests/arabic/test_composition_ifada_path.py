"""اختبارُ المسار العربيّ الموصول من الترميز إلى مرشّح الإفادة.

ثلاثةُ محاورَ مفصولة: الاسترجاعُ الكتابيّ، وقراءةُ التركيب، وقراءةُ الإفادة.
ولا يُقرأ نجاحُ أحدِها دليلًا على الآخر.
"""

from __future__ import annotations

import inspect

import pytest

from alghanem.arabic.composition_ifada_experiment import (
    ACCOUNTED_TOKEN,
    COMPOSITION_IFADA_EXPERIMENT_NAMED_LAWS,
    DECLARED_INPUTS,
    UNACCOUNTED_TOKEN,
    PathCensus,
    measure,
    render_census,
    run_under_the_experimental_authority,
)
from alghanem.arabic.composition_ifada_path import (
    COMPOSITION_IFADA_PATH_NAMED_LAWS,
    CaseMark,
    CompositionReading,
    PathStage,
    PathStop,
    StageOutcome,
    run_text,
)
from alghanem.arabic.mantuq_mafhum_ifada import IfadaStanding
from alghanem.kernel.experimental import (
    ExperimentalAuthority,
    ExperimentalOutcomeStatus,
    ExperimentalRunRecord,
)


def test_the_positive_reading_reaches_a_derived_benefit() -> None:
    """«اللَّهُ نُورٌ»: ضمّتان، فالإسنادُ مقروءٌ والإفادةُ مُشتقّة."""

    run = run_text("اللَّهُ نُورٌ")

    assert run.reached is PathStage.IFADA
    assert run.outcome is StageOutcome.ADVANCED
    assert run.stop is None
    assert run.composition is CompositionReading.إسناد
    assert run.ifada is IfadaStanding.مُفيد


def test_the_negative_reading_is_a_composition_that_does_not_benefit() -> None:
    """«نُورُ السَّمَاوَاتِ»: ضمّةٌ فكسرة، فالإضافةُ قائمةٌ ولا تُفيد."""

    run = run_text("نُورُ السَّمَاوَاتِ")

    assert run.reached is PathStage.IFADA
    assert run.composition is CompositionReading.إضافة
    assert run.ifada is IfadaStanding.غير_مُفيد
    assert run.record is not None
    assert run.record.composition_benefits is False
    assert run.record.benefit_witness.strip()


def test_the_ambiguous_reading_defers_by_a_named_preventer() -> None:
    """«الْحَمْدُ لِلَّهِ»: لامٌ مكسورةٌ في الأوّل، فالكسرةُ لا تُميّز الإضافة."""

    run = run_text("الْحَمْدُ لِلَّهِ")

    assert run.reached is PathStage.COMPOSITION
    assert run.outcome is StageOutcome.DEFERRED
    assert run.stop is PathStop.PROCLITIC_JARR_UNDECIDED
    assert run.composition is None
    assert run.ifada is IfadaStanding.غير_مقروء


def test_an_unwritten_final_mark_stops_below_composition() -> None:
    """«قُلْ هُوَ»: لا علامةَ آخِرٍ مكتوبةً تُقرأ، فالتوقّفُ دون التركيب."""

    run = run_text("قُلْ هُوَ")

    assert run.reached is PathStage.CASE_MARK
    assert run.stop is PathStop.FINAL_MARK_NOT_WRITTEN
    assert run.ifada is IfadaStanding.غير_مقروء


def test_a_tanwined_first_word_blocks_the_idafa_reading() -> None:
    """«كِتَابٌ الْبَيْتِ»: المضافُ لا يُنوَّن، فالمانعُ محدَّدٌ لا غامض."""

    run = run_text("كِتَابٌ الْبَيْتِ")

    assert run.outcome is StageOutcome.BLOCKED
    assert run.stop is PathStop.MUDAF_CARRIES_TANWIN
    assert run.ifada is IfadaStanding.غير_مقروء


@pytest.mark.parametrize(
    ("text", "stop"),
    [
        ("الْعَالَمِينَ نُورٌ", PathStop.FIRST_MARK_IS_NOT_RAF),
        ("رَبُّ الْعَالَمِينَ", PathStop.SECOND_MARK_IS_NASB),
        ("اللَّهُ", PathStop.NOT_TWO_WORDS),
    ],
)
def test_each_refused_reading_names_its_own_genus(text: str, stop: PathStop) -> None:
    """كلُّ امتناعٍ يُنسَب إلى جنسه المُسمّى، لا إلى «فشلٍ» واحدٍ مُبهَم."""

    run = run_text(text)

    assert run.stop is stop
    assert run.outcome is not StageOutcome.ADVANCED
    assert run.ifada is IfadaStanding.غير_مقروء


def test_the_benefit_is_never_taken_from_the_caller() -> None:
    """لا مدخلَ في `run_text` يَكتب الفائدة؛ توقيعُها هو الشاهد."""

    signature = inspect.signature(run_text)

    assert list(signature.parameters) == ["text"]
    assert "composition_benefits" not in signature.parameters


def test_a_read_benefit_always_carries_its_own_witness() -> None:
    """كلُّ فائدةٍ مقروءةٍ تحمل شاهدَها، وكلُّ غيرِ مقروءةٍ لا سجلَّ لها."""

    for _, text in DECLARED_INPUTS:
        run = run_text(text)
        if run.record is None:
            assert run.ifada is IfadaStanding.غير_مقروء
            assert run.composition is None
            continue
        assert run.record.composition_benefits is not None
        assert run.record.benefit_witness.strip()


def test_written_retrieval_is_measured_apart_from_analysis() -> None:
    """الاسترجاعُ الكتابيّ يَتمّ لكلمات نصوصٍ لم تبلغ إفادةً، فهما محوران."""

    stopped = run_text("الْحَمْدُ لِلَّهِ")

    assert not stopped.reached_ifada
    assert all(word.crossed_the_written_chain for word in stopped.words)


def test_analysis_success_is_measured_apart_from_the_benefit() -> None:
    """قراءةُ التركيب تَتمّ حيث الإفادةُ منفيّة، فقراءتُه ليست قراءتَها."""

    run = run_text("نُورُ كِتَابٍ")

    assert run.composition is CompositionReading.إضافة
    assert run.ifada is IfadaStanding.غير_مُفيد


def test_every_stage_record_carries_its_identity_and_ground() -> None:
    """كلُّ انتقالٍ يَحفظ هويّةَ مدخله وعمليتَه وشرطَه ورتبتَه وأثرَه."""

    run = run_text("اللَّهُ نُورٌ")

    assert run.stages
    ranks = [record.rank for record in run.stages]
    assert ranks == sorted(ranks)
    for record in run.stages:
        assert record.operation.strip()
        assert record.condition.strip()
        assert record.input_digest.strip()
        assert record.evidence.strip()
        assert record.trace.events
        assert (record.preventer is None) is (record.outcome is StageOutcome.ADVANCED)


def test_the_case_mark_is_read_from_the_carrier_states() -> None:
    """علامةُ الآخِر تُقرأ من حالات الحامل، لا من معجمٍ ولا من جدولِ جواب."""

    run = run_text("اللَّهُ نُورٌ")

    assert [word.final_mark for word in run.words] == [CaseMark.ضمّة, CaseMark.ضمّة]
    assert [word.final_is_tanwin for word in run.words] == [False, True]


def test_the_run_completes_under_the_experimental_authority() -> None:
    """السَّوقُ يَتمّ بسلطةٍ قائمةٍ وطلبٍ مربوطٍ بتجربةٍ مجمّدة."""

    record = run_under_the_experimental_authority()

    assert type(record) is ExperimentalRunRecord
    assert record.outcome_status is ExperimentalOutcomeStatus.COMPLETED
    assert record.failure is None
    assert record.operations_used == ("run_text",)
    assert record.request_content_digest.strip()


def test_the_run_is_neither_asked_for_nor_issues_a_certificate() -> None:
    """التجريبُ لا يشترط شهادةَ ولادة، ولا يُصدرها، فالسلطتان مفصولتان."""

    parameters = inspect.signature(ExperimentalAuthority.run).parameters
    record = run_under_the_experimental_authority()

    assert "certificate" not in parameters
    assert "verdict" not in parameters
    assert not any(
        "certificate" in name for name in ExperimentalRunRecord.__annotations__
    )
    assert not any("certificate:" in event for event in record.trace.events)


def test_each_declared_case_is_answered_by_exactly_one_frozen_token() -> None:
    """كلُّ حالةٍ مُعلَنةٍ تُجاب بمفردةٍ واحدةٍ من المفردتين المجمّدتين."""

    record = run_under_the_experimental_authority()
    assert record.output_content is not None
    lines = record.output_content.splitlines()

    assert len(lines) == len(DECLARED_INPUTS)
    for line, (case_id, _) in zip(lines, DECLARED_INPUTS, strict=True):
        prefix, token = line.split("=", 1)
        assert prefix == case_id
        assert token in {ACCOUNTED_TOKEN, UNACCOUNTED_TOKEN}


def test_the_census_keeps_every_stop_in_its_denominator() -> None:
    """المقامُ يَشمل الواقفَ والممنوعَ والمؤجَّل، ولا يُنقّى لترتفع نسبة."""

    census = measure()

    assert census.input_total == len(DECLARED_INPUTS)
    assert sum(census.outcome_counts.values()) == census.input_total
    assert sum(census.ifada_counts.values()) == census.input_total
    assert census.reached_counts[PathStage.UTF8_BYTES] == census.input_total
    assert census.reached_counts[PathStage.IFADA] == census.reached_ifada
    assert census.reached_ifada < census.input_total
    assert sum(census.stop_counts.values()) == census.input_total - census.reached_ifada


def test_the_census_ranks_are_monotone_down_the_path() -> None:
    """ما بلغ طبقةً أعلى لا يزيد على ما بلغ ما دونها؛ فالسلسلةُ متّصلة."""

    counts = measure().reached_counts
    ordered = [counts[stage] for stage in PathStage]

    assert ordered == sorted(ordered, reverse=True)


def test_the_census_reading_is_rendered_without_an_unnamed_ratio() -> None:
    """العرضُ يَذكر المقاماتِ صريحةً، ولا يكتب نسبةً بلا مقامٍ مُسمّى."""

    text = render_census(measure())

    assert "%" not in text
    for stage in PathStage:
        assert stage.value in text
    for stop in PathStop:
        assert stop.value in text


def test_an_empty_census_is_refused() -> None:
    """إحصاءٌ بلا سَوقٍ واحدٍ لا يُقرأ، فلا مقامَ له."""

    with pytest.raises(ValueError):
        PathCensus(())


@pytest.mark.parametrize(
    "laws",
    [COMPOSITION_IFADA_PATH_NAMED_LAWS, COMPOSITION_IFADA_EXPERIMENT_NAMED_LAWS],
)
def test_every_named_law_opens_with_its_own_name(laws: dict[str, str]) -> None:
    """كلُّ قانونٍ مُسمًّى يفتتح نصُّه باسمه، فلا قانونَ بلا اسمٍ مقروء."""

    assert laws
    for name, statement in laws.items():
        assert statement.startswith(f"{name}:")
