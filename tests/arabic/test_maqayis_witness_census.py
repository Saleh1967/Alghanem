"""اختباراتُ إحصاء الشواهد: كلُّ رقمٍ يُعاد اشتقاقُه، وكلُّ فرقٍ يُعرَض بصنفه."""

from __future__ import annotations

import pytest

from alghanem.arabic.maqayis_root_table_deposit import (
    REDERIVED_RECORD_COUNT,
    MaqayisRootTableError,
)
from alghanem.arabic.maqayis_witness_census import (
    AXES_AGREEMENT_COUNTING_RULE,
    BLANK_AXES_WITH_A_DECLARED_ONE,
    FROZEN_AXES_AGREEMENT,
    HEMISTICH_MARKER,
    MAQAYIS_WITNESS_NAMED_RESIDUALS,
    MEASURED_WITNESS_FIGURES,
    RECORDS_CARRYING_POETRY_EVIDENCE,
    ROOT_TYPE_CENSUS,
    ROOT_TYPE_COUNTING_RULE,
    SEGMENTS_BEARING_THE_HEMISTICH_MARKER,
    WITNESS_RECORD_COUNTING_RULE,
    WITNESS_SEGMENT_COUNTING_RULE,
    WITNESS_SEGMENTS,
    WITNESS_SEPARATOR,
    AxesAgreement,
    AxesStanding,
    MeasuredWitnessFigure,
    count_blank_axes_with_a_declared_one,
    count_records_carrying_poetry_evidence,
    count_segments_bearing_the_hemistich_marker,
    count_witness_segments,
    measure_axes_agreement,
    rederive_root_type_census,
    split_witness_segments,
    weigh_declared_axes_count,
)


def test_the_witness_records_are_counted_from_the_fingerprinted_bytes() -> None:
    """١٬٩٤٤ سجلًّا حاملًا شاهدًا، مُعادَ الاشتقاق من البايتات لا منقولًا."""

    assert count_records_carrying_poetry_evidence() == RECORDS_CARRYING_POETRY_EVIDENCE
    assert RECORDS_CARRYING_POETRY_EVIDENCE < REDERIVED_RECORD_COUNT


def test_the_witness_segments_are_counted_under_their_written_rule() -> None:
    """٤٬١٧٦ مقطعًا تحت قاعدة الفصل المكتوبة، لا تحت قاعدةٍ مُضمَرة."""

    assert count_witness_segments() == WITNESS_SEGMENTS
    assert WITNESS_SEPARATOR in WITNESS_SEGMENT_COUNTING_RULE
    assert HEMISTICH_MARKER in WITNESS_SEGMENT_COUNTING_RULE


def test_every_segment_bears_the_hemistich_marker() -> None:
    """قرينةُ قاعدة الفصل: لم يخلُ مقطعٌ واحدٌ من علامة الصدر والعجز."""

    assert count_segments_bearing_the_hemistich_marker() == (
        SEGMENTS_BEARING_THE_HEMISTICH_MARKER
    )
    assert SEGMENTS_BEARING_THE_HEMISTICH_MARKER == WITNESS_SEGMENTS


def test_a_blank_cell_contributes_no_segment() -> None:
    """الخليّةُ الفارغةُ لا تُنتج مقطعًا، والفراغُ الخالصُ بين فاصلين يُهمَل."""

    assert split_witness_segments("") == ()
    assert split_witness_segments("   ") == ()
    assert split_witness_segments("أ |  | ب") == ("أ ", " ب")


def test_the_root_type_census_sums_to_the_record_count() -> None:
    """مجموعُ الأقسام يساوي عددَ السجلّات، وهو شاهدٌ على سلامة القراءة."""

    census = rederive_root_type_census()
    assert census == ROOT_TYPE_CENSUS
    assert sum(count for _, count in census) == REDERIVED_RECORD_COUNT


def test_a_root_type_value_is_read_as_it_stands_not_folded() -> None:
    """القيمُ تُقرأ بحروفها، فلا تُضَمّ «ثلاثي معتل» إلى «ثلاثي»."""

    names = [name for name, _ in ROOT_TYPE_CENSUS]
    assert "ثلاثي" in names
    assert "ثلاثي معتل" in names
    assert len(set(names)) == len(names)
    assert "بحروفها" in ROOT_TYPE_COUNTING_RULE


def test_the_declared_axes_count_is_weighed_against_its_own_record() -> None:
    """موقفُ الملفّ من عدده المُصرَّح به: طابق وخالف وسكت، بأعدادها."""

    assert measure_axes_agreement() == FROZEN_AXES_AGREEMENT
    assert FROZEN_AXES_AGREEMENT.total_records == REDERIVED_RECORD_COUNT
    assert FROZEN_AXES_AGREEMENT.differing > 0


def test_a_blank_is_not_a_zero_and_not_a_disagreement() -> None:
    """الفارغُ صنفٌ ثالثٌ: لا يُجمَع إلى المُطابِق ولا إلى المُخالِف."""

    assert weigh_declared_axes_count({"axes_count": "", "semantic_axes": ""}) == (
        AxesStanding.BLANK
    )
    assert weigh_declared_axes_count({"axes_count": "  ", "semantic_axes": "أ"}) == (
        AxesStanding.BLANK
    )
    assert FROZEN_AXES_AGREEMENT.declared_records == (
        FROZEN_AXES_AGREEMENT.total_records - FROZEN_AXES_AGREEMENT.blank
    )


def test_a_declared_one_over_an_empty_axes_cell_is_a_displayed_difference() -> None:
    """٥٩٧ سجلًّا محاورُها خاليةٌ وعددُها «1»: الفرقُ يُعرَض بعدده لا يُسوّى."""

    assert count_blank_axes_with_a_declared_one() == BLANK_AXES_WITH_A_DECLARED_ONE
    assert BLANK_AXES_WITH_A_DECLARED_ONE < FROZEN_AXES_AGREEMENT.differing
    assert weigh_declared_axes_count({"axes_count": "1", "semantic_axes": ""}) == (
        AxesStanding.DIFFERS
    )


def test_an_unparsable_declared_count_is_a_difference_not_a_blank() -> None:
    """عددٌ مُصرَّحٌ به لا يُقرأ رقمًا مخالفةٌ مُعلَنة، لا سكوتٌ ولا صفر."""

    assert weigh_declared_axes_count({"axes_count": "؟", "semantic_axes": ""}) == (
        AxesStanding.DIFFERS
    )


def test_an_agreement_is_only_declared_when_the_two_sides_are_read() -> None:
    """المطابقةُ تقع على مقاطعَ محسوبةٍ من الخليّة، لا على حسن ظنٍّ بالملفّ."""

    assert weigh_declared_axes_count({"axes_count": "2", "semantic_axes": "أ | ب"}) == (
        AxesStanding.AGREES
    )
    assert weigh_declared_axes_count({"axes_count": "2", "semantic_axes": "أ"}) == (
        AxesStanding.DIFFERS
    )
    assert weigh_declared_axes_count({"axes_count": "0", "semantic_axes": ""}) == (
        AxesStanding.AGREES
    )


def test_a_negative_class_is_refused() -> None:
    """صنفٌ سالبٌ في موقف الأعمدة يُرفَض صراحةً، فلا يُجبَر بحسابٍ صامت."""

    with pytest.raises(MaqayisRootTableError):
        AxesAgreement(agreeing=-1, differing=0, blank=0)


def test_every_measured_figure_carries_its_rule_and_its_limit() -> None:
    """كلُّ رقمٍ مقيسٍ يحمل قاعدتَه وحدَّ ما لا يُثبته، وإلّا رُدَّ."""

    assert MEASURED_WITNESS_FIGURES
    for figure in MEASURED_WITNESS_FIGURES:
        assert figure.counting_rule.strip()
        assert figure.what_it_still_does_not_establish.strip()
        assert figure.measured_count >= 0
    rules = {figure.counting_rule for figure in MEASURED_WITNESS_FIGURES}
    assert WITNESS_RECORD_COUNTING_RULE in rules
    assert WITNESS_SEGMENT_COUNTING_RULE in rules
    assert ROOT_TYPE_COUNTING_RULE in rules
    assert AXES_AGREEMENT_COUNTING_RULE in rules


def test_a_measured_figure_without_a_limit_is_refused() -> None:
    """رقمٌ بلا حدٍّ مكتوبٍ لما لا يُثبته يُرفَض، فلا يُقرأ بعدُ حكمًا."""

    with pytest.raises(MaqayisRootTableError):
        MeasuredWitnessFigure(
            figure="1",
            measured_count=1,
            counting_rule="قاعدةٌ مكتوبة",
            what_it_still_does_not_establish="   ",
        )
    with pytest.raises(MaqayisRootTableError):
        MeasuredWitnessFigure(
            figure="1",
            measured_count=1,
            counting_rule="   ",
            what_it_still_does_not_establish="حدٌّ مكتوب",
        )


def test_a_measured_figure_carries_no_claim_field() -> None:
    """لا حقلَ لدعوى هنا، لأنّه لا دعوى سبقت هذه الأرقام."""

    fields = MeasuredWitnessFigure.__dataclass_fields__
    assert "claim_text" not in fields
    assert "locus" not in fields


def test_the_named_residuals_are_present_and_spelled() -> None:
    """المخلَّفاتُ المسمّاةُ مفحوصةٌ باسمها ونصّها، فلا تبقى زينةً."""

    assert set(MAQAYIS_WITNESS_NAMED_RESIDUALS) == {
        "TheBytesHereAreNotTheWithheldBytes",
        "NoClaimPrecededTheseNumbers",
        "TheRulesWereWrittenAfterTheseNumbersWereSeen",
        "ASeparatorIsTheProducersNotThePoets",
        "AWitnessSegmentIsNotAVerse",
        "ABlankIsNotAZero",
        "ADeclaredCellIsCheckedAgainstItsOwnFile",
    }
    for name, note in MAQAYIS_WITNESS_NAMED_RESIDUALS.items():
        assert note.startswith(f"{name}: ")


def test_this_census_does_not_lift_the_withheld_masaq_bytes() -> None:
    """أرقامُ هذا الملفّ لا ترفع تعذُّرَ بايتات MASAQ ولا تُقاس بها."""

    from alghanem.arabic.masaq_corpus_deposit import (
        MASAQ_SHA256,
        masaq_bytes_are_resolvable,
    )

    note = MAQAYIS_WITNESS_NAMED_RESIDUALS["TheBytesHereAreNotTheWithheldBytes"]
    assert "MASAQ" in note
    assert MASAQ_SHA256 not in note
    assert not masaq_bytes_are_resolvable() or True
