"""اختباراتُ مِسبار التمييز: عمودان لا يُدمجان، ومنزلةٌ لا تُرفَع بالكتابة."""

from __future__ import annotations

import unicodedata
from dataclasses import replace

import pytest

from alghanem.arabic.arabic_round_trip_v1 import LayerOutcome, RoundTripLayer
from alghanem.arabic.segmentation_discrimination_probe import (
    DISCRIMINATION_PROBE_WORDS,
    INDEPENDENT_REFERENCE_REQUIREMENTS,
    ClassificationStanding,
    DiscriminationProbeError,
    ProbeClass,
    ProbeWord,
    declared_pairs,
    render_report,
    run_probe,
)

_REPORT = run_probe()


def _row(key: str):
    for row in _REPORT.rows:
        if row.word.key == key:
            return row
    raise AssertionError(f"لا صفَّ لـ{key!r}")


def test_allathina_returns_its_own_bytes() -> None:
    """السؤالُ الأوّل يُقاس بالتشغيل: أترجع «الَّذِينَ» بايتًا ببايت؟"""

    row = _row("allathina")
    assert row.bytes_returned is True
    assert row.reached is RoundTripLayer.FINAL_BYTES
    assert row.outcome is LayerOutcome.RECONSTRUCTED
    assert row.refusal is None


def test_every_probe_word_returns_its_bytes_and_this_is_counted() -> None:
    """العددُ مُشتَقٌّ بالتشغيل لا مكتوب؛ وإن سقطت كلمةٌ ظهر السقوط."""

    assert _REPORT.word_total == len(DISCRIMINATION_PROBE_WORDS)
    assert _REPORT.returned_total == _REPORT.word_total
    for row in _REPORT.rows:
        assert row.bytes_returned is True
        assert row.shape is not None


def test_allathina_is_not_conflated_in_shape_with_ad_dallina() -> None:
    """السؤالُ الثاني يُقاس شكلًا: أخرج الخطُّ للكلمتَين توقيعَين مختلفَين؟"""

    left, right = _row("allathina"), _row("ad_dallina")
    assert left.shape is not None and right.shape is not None
    assert left.shape.signature != right.shape.signature
    assert left.shape.digest != right.shape.digest


def test_the_difference_is_read_from_where_the_shadda_is_written() -> None:
    """المفتتحُ غيرُ المكتوب يقف عند اللام المُشدَّدة ويبتلع اللام العارية."""

    allathina = _row("allathina").shape
    dallina = _row("ad_dallina").shape
    assert allathina is not None and dallina is not None
    assert allathina.syllables[0].undecided_opening_length == 1
    assert dallina.syllables[0].undecided_opening_length == 2


def test_no_declared_pair_is_conflated_in_this_probe() -> None:
    """المقارناتُ مُعلَنةٌ قبل التشغيل، والخلطُ يُعرَض لو وقع ولا يُحذَف."""

    assert _REPORT.pairs
    assert len(_REPORT.pairs) == len(declared_pairs())
    assert _REPORT.conflated_pairs == ()
    for pair in _REPORT.pairs:
        assert pair.shapes_differ is True
        assert pair.conflated_in_shape is False
        assert pair.both_returned_their_bytes is True
        assert pair.why_the_pair_matters.strip()


def test_distinct_shapes_are_counted_not_asserted() -> None:
    """تساوي توقيعَين إخفاقُ تمييزٍ يُعَدّ؛ والعددُ ههنا مشتقٌّ من التشغيل."""

    assert _REPORT.distinct_shape_total == _REPORT.word_total


def test_reconstruction_does_not_raise_the_classification_standing() -> None:
    """الاسترجاعُ التامُّ لا يرفع منزلةَ التصنيف؛ وهي واحدةٌ للتقرير كلِّه."""

    assert _REPORT.returned_total == _REPORT.word_total
    assert (
        _REPORT.classification_standing
        is ClassificationStanding.NOT_ASSESSED_NO_REFERENCE_DEPOSITED
    )
    for row in _REPORT.rows:
        assert (
            row.classification_standing
            is ClassificationStanding.NOT_ASSESSED_NO_REFERENCE_DEPOSITED
        )


def test_a_higher_standing_cannot_be_written_without_a_deposited_reference() -> None:
    """المرتبتان الأعلى عضوان بلا مدخل؛ ولا تُبلَغ إحداهما بالكتابة."""

    row = _row("allathina")
    for standing in (
        ClassificationStanding.MEASURED_AGAINST_A_DEPOSITED_REFERENCE,
        ClassificationStanding.DECLARED_AND_AWAITING_A_REFERENCE,
    ):
        with pytest.raises(DiscriminationProbeError):
            replace(row, classification_standing=standing)


def test_every_probe_class_names_what_would_lift_it() -> None:
    """لكلّ صنفٍ شرطُ مرجعٍ مكتوب؛ ولا صنفَ يُترَك بلا طريقٍ إلى القياس."""

    covered = {
        requirement.probe_class for requirement in INDEPENDENT_REFERENCE_REQUIREMENTS
    }
    assert covered == set(ProbeClass)
    used = {word.probe_class for word in DISCRIMINATION_PROBE_WORDS}
    assert used == set(ProbeClass)
    for requirement in INDEPENDENT_REFERENCE_REQUIREMENTS:
        assert requirement.what_the_reference_must_supply.strip()


def test_every_probe_word_states_why_it_is_in_the_probe() -> None:
    for word in DISCRIMINATION_PROBE_WORDS:
        assert word.why_it_is_here.strip()
        assert word.raw_bytes == word.surface.encode("utf-8")


def test_a_probe_word_is_refused_when_its_surface_is_not_normalised() -> None:
    """المرمازُ يقرأ سطحًا مُسوًّى، فلا يُخزَّن في المِسبار سطحٌ خام."""

    raw = "\u0644\u0651\u064e"
    assert raw != unicodedata.normalize("NFC", raw)
    with pytest.raises(DiscriminationProbeError):
        ProbeWord(
            key="raw",
            surface=raw,
            probe_class=ProbeClass.SHADDA_WITHOUT_AN_OPENING,
            why_it_is_here="سطحٌ غيرُ مُسوًّى",
        )


def test_a_probe_word_is_refused_without_a_reason_or_a_key() -> None:
    with pytest.raises(DiscriminationProbeError):
        ProbeWord(
            key="  ",
            surface="\u0642\u064e\u0645",
            probe_class=ProbeClass.MADD_SHAPE,
            why_it_is_here="سبب",
        )
    with pytest.raises(DiscriminationProbeError):
        ProbeWord(
            key="k",
            surface="\u0642\u064e\u0645",
            probe_class=ProbeClass.MADD_SHAPE,
            why_it_is_here="   ",
        )


def test_a_pair_that_names_a_word_outside_the_probe_is_refused() -> None:
    """المقارنةُ المُعلَنة تُحيل إلى كلماتٍ مُشغَّلة، ولا تُسقَط صامتةً."""

    only = tuple(word for word in DISCRIMINATION_PROBE_WORDS if word.key == "allathina")
    with pytest.raises(DiscriminationProbeError):
        run_probe(only)


def test_an_empty_probe_is_refused_rather_than_reported_as_perfect() -> None:
    with pytest.raises(DiscriminationProbeError):
        run_probe(())


def test_the_rendered_report_keeps_the_two_questions_apart() -> None:
    """المعروضُ عمودان: بايتاتٌ رجعت، وتوقيعٌ اختلف، ومنزلةٌ لم تُقَس."""

    rendered = render_report(_REPORT)
    assert "bytes returned: 8/8" in rendered
    assert "distinct shapes: 8/8" in rendered
    assert ClassificationStanding.NOT_ASSESSED_NO_REFERENCE_DEPOSITED.value in rendered
    assert "allathina" in rendered
    assert "CONFLATED" not in rendered
