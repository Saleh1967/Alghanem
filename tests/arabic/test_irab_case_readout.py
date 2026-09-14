"""اختباراتُ قراءةِ الحالة الإعرابية من السطح وقياسِها على شاهدٍ خارجيّ.

والشواهدُ المكتوبةُ هنا مأخوذةٌ بحروفها من المواضع التي **كسرت** الفاحصَ عند
تشغيله على المدوَّنة، لا من أمثلةٍ اختيرت لتنجح. فاختبارٌ لا يحوي الحالةَ التي
أسقطت النسخةَ السابقة اختبارٌ بُني ليمرّ.
"""

from __future__ import annotations

import unicodedata

import pytest

from alghanem.arabic.irab_case_readout import (
    ACCUSATIVE_IS_NOT_OBJECTHOOD_NOTE,
    AS_STATED_HYPOTHESIS_BASELINE,
    DEVELOPMENT_SPLIT_MEASUREMENT,
    HELD_OUT_SPLIT_MEASUREMENT,
    IRAB_CASE_READOUT_NAMED_RESIDUALS,
    NAMED_RESIDUAL_ERROR_GENERA,
    NORMALIZATION_FORM,
    WHOLE_CORPUS_MEASUREMENT,
    CaseReadout,
    CaseReadoutError,
    CaseReadoutMeasurement,
    ReadoutGenus,
    development_split_contains,
    read_surface_case,
)
from alghanem.arabic.irab_corpus_witness import (
    QURANIC_ARABIC_CORPUS_WITNESS,
    IrabCorpusWitness,
    IrabCorpusWitnessError,
)


def test_witness_names_its_licences_and_a_full_digest() -> None:
    witness = QURANIC_ARABIC_CORPUS_WITNESS
    assert len(witness.sha256) == 64
    assert witness.byte_length == 6_309_503
    assert len(witness.licenses) == 2
    assert "corpus.quran.com" in witness.attribution_requirement
    assert "tanzil.info" in witness.attribution_requirement


def test_witness_refuses_a_short_digest() -> None:
    with pytest.raises(IrabCorpusWitnessError):
        IrabCorpusWitness(
            corpus="c",
            version="v",
            upstream="u",
            measured_mirror="m",
            measured_path="p",
            sha256="abc",
            byte_length=1,
            licenses=("L",),
            attribution_requirement="a",
            annotation_note="n",
        )


def test_witness_refuses_a_corpus_without_a_named_licence() -> None:
    with pytest.raises(IrabCorpusWitnessError):
        IrabCorpusWitness(
            corpus="c",
            version="v",
            upstream="u",
            measured_mirror="m",
            measured_path="p",
            sha256="a" * 64,
            byte_length=1,
            licenses=(),
            attribution_requirement="a",
            annotation_note="n",
        )


def test_the_defect_that_manufactured_one_hundred_percent_is_refused() -> None:
    """لا تُقرَأ الحالةُ من اسمِ حركةٍ مكتوبٍ في نصّ، بل من الحركة نفسها.

    «قَالُوا» كان يُقرأ مفعولًا به لأنّ نصَّ المتوقَّع يحوي لفظَ «فتحة»؛ وآخرُ
    ما يُقرَأ فيه ألفٌ لا فتحةَ إعرابٍ البتّة.
    """

    reading = read_surface_case("قَالُوا")
    assert reading.readout is CaseReadout.متعذّر_القياس
    assert reading.genus is ReadoutGenus.مقصور_لا_علامة_ظاهرة


def test_attached_preposition_with_pronoun_is_not_accusative() -> None:
    assert read_surface_case("لَكُمْ").readout is not CaseReadout.منصوب
    assert read_surface_case("لِلْكَٰفِرِينَ").readout is not CaseReadout.منصوب
    assert read_surface_case("بِـَٔايَٰتِنَا").readout is not CaseReadout.منصوب


def test_final_vowel_of_an_attached_pronoun_is_not_the_case_vowel() -> None:
    """«رَبُّكَ» مرفوعٌ وآخرُ حركةٍ فيه فتحةٌ على الكاف."""

    assert read_surface_case("رَبُّكَ").readout is CaseReadout.مرفوع
    assert read_surface_case("قُلُوبُنَا").readout is CaseReadout.مرفوع
    assert read_surface_case("رَبُّهَا").readout is CaseReadout.مرفوع


def test_divine_name_is_read_after_canonical_reordering() -> None:
    """صورتان لبايتاتٍ مختلفةِ الترتيب لفظٌ واحد؛ يُغلَق البابُ بـ`NFC` لا بحيلة."""

    shadda_first = "\u0671\u0644\u0644\u0651\u064e\u0647\u064f"
    fatha_first = unicodedata.normalize(NORMALIZATION_FORM, shadda_first)
    assert shadda_first != fatha_first
    assert read_surface_case(shadda_first).readout is CaseReadout.مرفوع
    assert read_surface_case(shadda_first).genus is ReadoutGenus.لفظ_الجلالة
    assert read_surface_case("وَٱللَّهِ").readout is CaseReadout.مجرور


def test_unmarked_shapes_are_untestable_not_wrong() -> None:
    for surface, genus in (
        ("مُوسَىٰ", ReadoutGenus.مقصور_لا_علامة_ظاهرة),
        ("ٱلنَّصَٰرَىٰ", ReadoutGenus.مقصور_لا_علامة_ظاهرة),
        ("ٱلصَّٰلِحَٰتِ", ReadoutGenus.جمع_مؤنث_سالم_ملتبس),
        ("ٱلْكَٰفِرِينَ", ReadoutGenus.جمع_مذكر_سالم_بالياء_ملتبس),
    ):
        reading = read_surface_case(surface)
        assert reading.readout is CaseReadout.متعذّر_القياس
        assert reading.genus is genus


def test_letter_marked_and_vowel_marked_readings_are_distinguished() -> None:
    assert read_surface_case("ٱلنَّبِيُّونَ").genus is ReadoutGenus.جمع_مذكر_سالم_بالواو
    assert read_surface_case("كَثِيرًا").genus is ReadoutGenus.تنوين
    assert read_surface_case("كَثِيرًا").readout is CaseReadout.منصوب
    assert read_surface_case("ٱلْكِتَٰبَ").readout is CaseReadout.منصوب


def test_reading_refuses_an_empty_surface() -> None:
    with pytest.raises(CaseReadoutError):
        read_surface_case("   ")


def test_split_rule_is_independent_of_the_answer() -> None:
    assert development_split_contains(2) is True
    assert development_split_contains(3) is False
    with pytest.raises(CaseReadoutError):
        development_split_contains(0)


def test_recorded_measurements_partition_their_population() -> None:
    for measurement in (
        DEVELOPMENT_SPLIT_MEASUREMENT,
        HELD_OUT_SPLIT_MEASUREMENT,
        WHOLE_CORPUS_MEASUREMENT,
    ):
        assert (
            measurement.correct + measurement.wrong + measurement.untestable
            == measurement.population
        )
        assert measurement.witness is QURANIC_ARABIC_CORPUS_WITNESS


def test_whole_corpus_is_the_sum_of_the_two_splits() -> None:
    for field in ("population", "correct", "wrong", "untestable"):
        assert getattr(WHOLE_CORPUS_MEASUREMENT, field) == getattr(
            DEVELOPMENT_SPLIT_MEASUREMENT, field
        ) + getattr(HELD_OUT_SPLIT_MEASUREMENT, field)


def test_held_out_accuracy_is_derived_and_is_not_the_development_number() -> None:
    held_out = HELD_OUT_SPLIT_MEASUREMENT.accuracy_on_decided
    development = DEVELOPMENT_SPLIT_MEASUREMENT.accuracy_on_decided
    assert 0.97 <= held_out < development
    assert HELD_OUT_SPLIT_MEASUREMENT.untestable_share > 0.15


def test_measurement_refuses_counts_that_do_not_exhaust_the_population() -> None:
    with pytest.raises(CaseReadoutError):
        CaseReadoutMeasurement(
            witness=QURANIC_ARABIC_CORPUS_WITNESS,
            split="s",
            normalization_form=NORMALIZATION_FORM,
            unicode_database_version="15.0.0",
            population=10,
            correct=5,
            wrong=1,
            untestable=1,
        )


def test_measurement_refuses_a_foreign_normalization_form() -> None:
    with pytest.raises(CaseReadoutError):
        CaseReadoutMeasurement(
            witness=QURANIC_ARABIC_CORPUS_WITNESS,
            split="s",
            normalization_form="NFD",
            unicode_database_version="15.0.0",
            population=2,
            correct=2,
            wrong=0,
            untestable=0,
        )


def test_measurement_refuses_a_ratio_with_no_decided_position() -> None:
    with pytest.raises(CaseReadoutError):
        CaseReadoutMeasurement(
            witness=QURANIC_ARABIC_CORPUS_WITNESS,
            split="s",
            normalization_form=NORMALIZATION_FORM,
            unicode_database_version="15.0.0",
            population=3,
            correct=0,
            wrong=0,
            untestable=3,
        )


def test_the_as_stated_hypothesis_scores_far_below_what_was_claimed() -> None:
    baseline = AS_STATED_HYPOTHESIS_BASELINE
    assert baseline.predicted_positive == 4265
    assert baseline.accusative_in_gold == 1444
    assert 0.33 < baseline.measured_precision < 0.35
    assert "١٠٠٪" in baseline.claimed_accuracy_before_measurement
    assert "٤٨٪" in baseline.claimed_accuracy_before_measurement


def test_the_remaining_gap_between_case_and_objecthood_is_named() -> None:
    assert "AccusativeIsNotObjecthood" in IRAB_CASE_READOUT_NAMED_RESIDUALS
    assert ACCUSATIVE_IS_NOT_OBJECTHOOD_NOTE.startswith("AccusativeIsNotObjecthood")
    assert set(NAMED_RESIDUAL_ERROR_GENERA) == {
        "ممنوع_من_الصرف",
        "منادى_مضاف_محذوف_الياء",
        "لام_من_بنية_الكلمة",
    }


def test_named_error_genera_are_reproduced_by_the_shipped_reader() -> None:
    """الأخطاءُ المُسمّاة تُعاد باستدعاء القارئ، لا يُخبَر عنها نثرًا."""

    assert read_surface_case("جَهَنَّمَ").readout is CaseReadout.منصوب
    assert read_surface_case("ثَمُودَ").readout is CaseReadout.منصوب
    assert read_surface_case("لِقَآءَ").readout is CaseReadout.مجرور


def test_module_reads_nothing_from_the_kernel() -> None:
    from alghanem.arabic import irab_case_readout, irab_corpus_witness

    for module in (irab_case_readout, irab_corpus_witness):
        source = module.__doc__ or ""
        assert "kernel/" in source
        assert not any(
            name.startswith("alghanem.kernel")
            for name in getattr(module, "__dict__", {})
        )
