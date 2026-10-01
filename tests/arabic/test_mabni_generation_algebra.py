"""شواهدُ جبر التوليد: الفضاءُ يُولَّد، والبايتاتُ تُثبِت أقلَّ منه وخارجَه."""

from __future__ import annotations

from pathlib import Path

import pytest

from alghanem.arabic.fath_ayah_source_text import FATH_AYAH_SOURCE_TEXT
from alghanem.arabic.fatiha_source_text import FATIHA_LINES
from alghanem.arabic.letter_haraka_partition import (
    THE_DECLARED_HARAKAT,
    THE_DECLARED_LETTERS,
)
from alghanem.arabic.mabni_generation_algebra import (
    MABNI_GENERATION_ALGEBRA_NAMED_RESIDUALS,
    THE_CHEAPEST_FIRST_ORDER,
    THE_LADDER_AT_MEASUREMENT,
    THE_LONG_VOWEL_COUNT,
    THE_SHORT_VOWELS,
    THE_TWELVE_REQUESTED_BUILDS,
    BuildStanding,
    ExhaustionRung,
    LadderReading,
    MabniGenerationError,
    RungStanding,
    cells_that_are_not_syllables,
    declared_consonant_count,
    exhaustion_ladder,
    licensing_stops_at,
    template_space,
    wazn_fibres,
)
from alghanem.arabic.syllable_preregistration import SyllableTemplate

DEPOSITED: tuple[str, ...] = tuple(
    (" ".join(FATIHA_LINES) + " " + FATH_AYAH_SOURCE_TEXT).split()
)


def _corpus_words() -> tuple[str, ...] | None:
    """رموزُ المدوّنة المختومة إن حُلَّت بايتاتُها، وإلّا `None` بلا اختراع."""

    try:
        from alghanem.arabic.quran_corpus_word_total import quran_corpus_path

        path = Path(quran_corpus_path())
    except Exception:  # noqa: BLE001 — تعذُّرُ الحلّ يُسمّى ولا يُخمَّن
        return None
    if not path.is_file():
        return None
    text = path.read_text(encoding="utf-8")
    return tuple(
        word
        for word in text.split()
        if any("\u0621" <= character <= "\u064a" for character in word)
    )


_CORPUS = _corpus_words()


# ── أوّلًا: السكونُ ليس صائتًا، فالـ112 خلايا لا مقاطع ──────────────────


def test_the_declared_alphabet_is_twenty_eight_and_is_read_not_written() -> None:
    """الثمانيةُ والعشرون مقروءةٌ من الأبجديّة المُعلَنة لا مكتوبةٌ رقمًا."""

    assert declared_consonant_count() == 28
    assert len(THE_DECLARED_LETTERS) == 28


def test_the_four_states_are_three_vowels_and_a_sukun_not_four_vowels() -> None:
    """الحالاتُ أربعٌ والصوائتُ ثلاثٌ؛ والرابعُ سكونٌ لا يكون نواة."""

    assert len(THE_DECLARED_HARAKAT) == 4
    assert len(THE_SHORT_VOWELS) == 3
    assert set(THE_SHORT_VOWELS) < set(THE_DECLARED_HARAKAT)
    assert THE_LONG_VOWEL_COUNT == 3


def test_the_hundred_and_twelve_is_a_cell_count_and_its_price_is_measured() -> None:
    """المئةُ والاثنتا عشرةَ خلايا، وثمانٍ وعشرون منها ليست مقاطعَ ألبتّة."""

    cells = declared_consonant_count() * len(THE_DECLARED_HARAKAT)
    assert cells == 112
    assert cells_that_are_not_syllables() == 28
    assert cells - cells_that_are_not_syllables() == 84
    assert template_space(SyllableTemplate.CV) == 84


def test_the_space_of_every_frozen_template_is_exact_arithmetic() -> None:
    """سعةُ كلِّ قالبٍ حاصلُ ضربٍ مضبوطٍ لا تقديرٌ ولا نقل."""

    assert template_space(SyllableTemplate.CV) == 28 * 3
    assert template_space(SyllableTemplate.CVV) == 28 * 3
    assert template_space(SyllableTemplate.CVC) == 28 * 28 * 3
    assert template_space(SyllableTemplate.CVVC) == 28 * 28 * 3
    assert template_space(SyllableTemplate.CVCC) == 28 * 28 * 28 * 3
    assert template_space(SyllableTemplate.CVVCC) == 28 * 28 * 28 * 3


def test_a_long_nucleus_does_not_multiply_the_space() -> None:
    """الطويلُ امتدادُ القصير لا جنسٌ خامس، فلا يُضاعِف سعةَ الفضاء."""

    assert template_space(SyllableTemplate.CVV) == template_space(SyllableTemplate.CV)
    assert template_space(SyllableTemplate.CVVC) == template_space(SyllableTemplate.CVC)


def test_the_space_refuses_a_template_that_is_not_one_of_the_six() -> None:
    """ما ليس عضوًا في القوالب الستّة لا تُخرَج له سعةٌ بل يُرفَع به خطأ."""

    with pytest.raises(MabniGenerationError):
        template_space("CVCV")  # type: ignore[arg-type]


# ── ثانيًا: السُّلَّم والاستنفاد قبل الترخيص ─────────────────────────────


def test_the_ladder_orders_the_six_templates_from_cheapest_to_dearest() -> None:
    """الترتيبُ ترتيبُ السعة: لا يسبق قالبٌ أوسعُ فضاءً قالبًا أضيق."""

    spaces = [template_space(template) for template in THE_CHEAPEST_FIRST_ORDER]
    assert spaces == sorted(spaces)
    assert len(THE_CHEAPEST_FIRST_ORDER) == len(SyllableTemplate)


def test_the_ladder_emits_all_six_rungs_even_when_a_rung_is_unattested() -> None:
    """الدرجةُ الخاليةُ تخرج خاليةً؛ وحذفُها يرفع التغطيةَ بإخفاء خلوٍّ مقيس."""

    reading = exhaustion_ladder(DEPOSITED)
    assert len(reading.rungs) == 6
    assert [rung.template for rung in reading.rungs] == list(THE_CHEAPEST_FIRST_ORDER)
    unattested = [
        rung for rung in reading.rungs if rung.standing is RungStanding.UNATTESTED_HERE
    ]
    assert unattested, "لا بدّ من درجةٍ خاليةٍ على هذه الوديعة ليُقرأ حملُها"


def test_a_ladder_missing_a_rung_is_refused_at_construction() -> None:
    """سُلَّمٌ نقصت منه درجةٌ لا يُقبَل بنيةً، فلا يُقرأ منه رقمٌ مرفوع."""

    reading = exhaustion_ladder(DEPOSITED)
    with pytest.raises(MabniGenerationError):
        LadderReading(
            rungs=reading.rungs[:-1],
            words_read=reading.words_read,
            words_unsegmented=reading.words_unsegmented,
        )


def test_the_licensing_stops_at_the_first_unexhausted_rung() -> None:
    """الترخيصُ يقف عند أوّلِ درجةٍ لم تُستنفَد، وهي الأرخصُ ههنا."""

    reading = exhaustion_ladder(DEPOSITED)
    stop = licensing_stops_at(reading)
    assert stop is not None
    assert stop.template is SyllableTemplate.CV
    assert stop.standing is not RungStanding.EXHAUSTED


def test_an_exhausted_rung_would_license_what_is_above_it() -> None:
    """الوقوفُ ليس بالبناء: درجةٌ مستنفَدةٌ تُرخِّص، فالشرطُ قابلٌ للخلاف."""

    exhausted = ExhaustionRung(
        template=SyllableTemplate.CV,
        space=84,
        attested_cells=84,
        attested_outside_space=0,
        occurrences=1,
    )
    assert exhausted.standing is RungStanding.EXHAUSTED
    assert exhausted.unfilled_cells == 0
    assert exhausted.coverage == 1.0


def test_a_rung_that_overflows_its_space_refutes_the_space_not_the_bytes() -> None:
    """المُثبَتُ إذا جاوز الفضاء فالفضاءُ ناقصٌ، ولا يُقصَّ المُثبَتُ عليه."""

    overflowing = ExhaustionRung(
        template=SyllableTemplate.CVV,
        space=84,
        attested_cells=85,
        attested_outside_space=4,
        occurrences=2,
    )
    assert overflowing.standing is RungStanding.OVERFLOWS_THE_SPACE
    assert overflowing.attested_inside_space == 81


def test_a_rung_refuses_outside_cells_greater_than_its_whole() -> None:
    """ما أُثبِتَ خارجَ الفضاء جزءٌ من المُثبَت، فلا يزيد على جملته."""

    with pytest.raises(MabniGenerationError):
        ExhaustionRung(
            template=SyllableTemplate.CV,
            space=84,
            attested_cells=3,
            attested_outside_space=4,
            occurrences=1,
        )


def test_coverage_counts_only_what_the_space_itself_can_produce() -> None:
    """بسطُ التغطية داخلُ الفضاء وحدَه؛ وضمُّ الخارج يرفع نسبةً بغير حقّ."""

    rung = ExhaustionRung(
        template=SyllableTemplate.CVC,
        space=2352,
        attested_cells=1434,
        attested_outside_space=119,
        occurrences=53046,
    )
    assert rung.attested_inside_space == 1315
    assert rung.coverage == 1315 / 2352
    assert rung.unfilled_cells == 2352 - 1315


def test_cells_attested_outside_the_declared_alphabet_are_counted_here() -> None:
    """الخارجُ ليس صفرًا على هذه الوديعة، فالنقصُ مقيسٌ لا مُدَّعى."""

    reading = exhaustion_ladder(DEPOSITED)
    assert sum(rung.attested_outside_space for rung in reading.rungs) > 0


def test_the_unsegmented_words_are_carried_in_the_denominator() -> None:
    """المتعذِّرُ محمولٌ في المقام؛ وطرحُه يرفع كلَّ نسبةٍ بإخفاء ما لم يُقرأ."""

    reading = exhaustion_ladder(DEPOSITED)
    assert reading.words_read == len(DEPOSITED)
    assert reading.words_unsegmented > 0
    assert 0.0 < reading.unsegmented_share < 1.0


def test_a_reading_refuses_more_unsegmented_than_it_read() -> None:
    """المتعذِّرُ لا يزيد على المقروء، وإلّا فالقراءةُ ليست قراءة."""

    reading = exhaustion_ladder(DEPOSITED)
    with pytest.raises(MabniGenerationError):
        LadderReading(
            rungs=reading.rungs,
            words_read=1,
            words_unsegmented=2,
        )


def test_the_ladder_reads_nothing_from_an_empty_input_without_inventing() -> None:
    """لا كلماتَ فلا وقوعات؛ والدرجاتُ تخرج خاليةً ولا تُخترَع لها أرقام."""

    reading = exhaustion_ladder(())
    assert reading.words_read == 0
    assert all(rung.attested_cells == 0 for rung in reading.rungs)
    assert all(rung.standing is RungStanding.UNATTESTED_HERE for rung in reading.rungs)
    with pytest.raises(MabniGenerationError):
        _ = reading.unsegmented_share


# ── ثالثًا: ليفُ الوزن ──────────────────────────────────────────────────


def test_the_wazn_map_is_not_injective_on_the_deposited_bytes() -> None:
    """وزنٌ واحدٌ يحمل أكثرَ من كلمةٍ، فلا مقلوبَ للدالّة ولا فرزَ منها."""

    fibres = wazn_fibres(DEPOSITED)
    assert fibres.heaviest_fibre > 1
    assert not fibres.is_injective
    assert fibres.mean_fibre > 1.0


def test_an_injective_wazn_map_is_readable_so_the_refutation_could_fail() -> None:
    """لو كان كلُّ ليفٍ مُفردًا لقُرئت الدالّةُ متباينة؛ فالنقضُ قابلٌ للخلاف."""

    fibres = wazn_fibres(("بِسْمِ",))
    assert fibres.heaviest_fibre == 1
    assert fibres.is_injective


def test_the_fibres_refuse_to_report_zero_where_they_mean_refusal() -> None:
    """لا وزنَ خرج فلا ليفَ يُقرأ؛ ويُرفَع امتناعٌ ولا يُخرَج صفرٌ مكانَه."""

    with pytest.raises(MabniGenerationError):
        wazn_fibres(())


# ── رابعًا: البناءاتُ الاثنتا عشرة ──────────────────────────────────────


def test_the_twelve_requested_builds_are_all_named_and_none_is_dropped() -> None:
    """المطلوبُ اثنا عشرَ بناءً، كلٌّ باسمه ومادّته؛ ولا يُحذَف منها واحد."""

    assert len(THE_TWELVE_REQUESTED_BUILDS) == 12
    assert len({build.name for build in THE_TWELVE_REQUESTED_BUILDS}) == 12
    assert all(build.required_material.strip() for build in THE_TWELVE_REQUESTED_BUILDS)


def test_no_requested_build_is_reported_as_built() -> None:
    """ليس في المنزلتين «مبنيٌّ»؛ فلا يُقرأ من هذه الوحدة بناءٌ قد تمّ."""

    standings = {build.standing for build in THE_TWELVE_REQUESTED_BUILDS}
    assert standings <= {
        BuildStanding.SUSPENDED_FOR_AN_UNDEPOSITED_MATERIAL,
        BuildStanding.REFUTED_AS_A_FUNCTION_OF_SHAPE,
    }
    assert len(standings) == 2


def test_the_refuted_builds_are_the_ones_the_shape_was_asked_to_sort() -> None:
    """ما طُلب فرزُه من الوزن وحدَه يُخرَج منقوضًا لا معلَّقًا، لأنّه قيس."""

    refuted = [
        build.name
        for build in THE_TWELVE_REQUESTED_BUILDS
        if build.standing is BuildStanding.REFUTED_AS_A_FUNCTION_OF_SHAPE
    ]
    assert "فرزُ المبنيِّ من المعرَب" in refuted
    assert len(refuted) == 3


def test_a_build_with_an_empty_field_is_not_a_registration() -> None:
    """حقلٌ خالٍ لا يُسجَّل؛ فالتعليقُ باسمِ مادّةٍ لا بفراغٍ يُسكَت عنه."""

    from alghanem.arabic.mabni_generation_algebra import RequestedBuild

    with pytest.raises(MabniGenerationError):
        RequestedBuild(
            name="  ",
            required_material="مادّة",
            standing=BuildStanding.SUSPENDED_FOR_AN_UNDEPOSITED_MATERIAL,
            reason="سبب",
        )


# ── خامسًا: المنقولُ يُصادَم بالمقيس ────────────────────────────────────


def test_the_transcribed_ladder_names_the_six_templates_and_no_more() -> None:
    """المنقولُ يُطابق القوالبَ الستّةَ اسمًا باسم، ولا سابعَ فيه."""

    assert set(THE_LADDER_AT_MEASUREMENT) == {
        template.value for template in SyllableTemplate
    }


@pytest.mark.skipif(
    _CORPUS is None,
    reason="بايتاتُ المدوّنة المختومة غيرُ محلولةٍ في هذه البيئة",
)
def test_the_transcribed_ladder_matches_what_the_sealed_corpus_measures() -> None:
    """كلُّ صفٍّ منقولٍ يُعاد من البايتات؛ والمنقولُ يسقط إن خالف المقيس."""

    assert _CORPUS is not None
    reading = exhaustion_ladder(_CORPUS)
    for rung in reading.rungs:
        assert THE_LADDER_AT_MEASUREMENT[rung.template.value] == (
            rung.space,
            rung.attested_cells,
            rung.attested_outside_space,
            rung.occurrences,
        )


@pytest.mark.skipif(
    _CORPUS is None,
    reason="بايتاتُ المدوّنة المختومة غيرُ محلولةٍ في هذه البيئة",
)
def test_the_second_rung_overflows_its_space_on_the_sealed_corpus() -> None:
    """الفائضُ مقيسٌ لا مرويّ: خمسةٌ وثمانون مُثبَتةً وفضاؤها أربعٌ وثمانون."""

    assert _CORPUS is not None
    reading = exhaustion_ladder(_CORPUS)
    second = reading.rungs[1]
    assert second.template is SyllableTemplate.CVV
    assert second.standing is RungStanding.OVERFLOWS_THE_SPACE
    assert second.attested_cells > second.space


@pytest.mark.skipif(
    _CORPUS is None,
    reason="بايتاتُ المدوّنة المختومة غيرُ محلولةٍ في هذه البيئة",
)
def test_the_licensing_stops_at_the_cheapest_rung_on_the_sealed_corpus() -> None:
    """على المدوّنة المختومة أيضًا: الأرخصُ لم يُستنفَد، فلا يُرخَّص ما فوقه."""

    assert _CORPUS is not None
    stop = licensing_stops_at(exhaustion_ladder(_CORPUS))
    assert stop is not None
    assert stop.template is SyllableTemplate.CV
    assert stop.attested_inside_space == 81


@pytest.mark.skipif(
    _CORPUS is None,
    reason="بايتاتُ المدوّنة المختومة غيرُ محلولةٍ في هذه البيئة",
)
def test_the_heaviest_wazn_carries_hundreds_of_words_on_the_sealed_corpus() -> None:
    """أثقلُ ليفٍ يحمل مئاتِ الكلمات، فلا يُفرَز منه بابٌ ولا تُعرَف كلمة."""

    assert _CORPUS is not None
    fibres = wazn_fibres(_CORPUS)
    assert fibres.heaviest_fibre >= 700
    assert fibres.singleton_fibres < fibres.distinct_wazn
    assert not fibres.is_injective


# ── سادسًا: البواقي المُسمّاة ────────────────────────────────────────────


def test_every_named_residual_is_exported_and_prefixed_by_its_own_name() -> None:
    """كلُّ باقٍ مُسمًّى مُصدَّرٌ، ونصُّه حاضرٌ غيرُ خالٍ؛ ولا اسمَ بلا نصّ."""

    import alghanem.arabic.mabni_generation_algebra as module

    for name, text in MABNI_GENERATION_ALGEBRA_NAMED_RESIDUALS.items():
        assert text.strip()
        assert f"{name}_NOTE" in module.__all__
        assert getattr(module, f"{name}_NOTE") == text
