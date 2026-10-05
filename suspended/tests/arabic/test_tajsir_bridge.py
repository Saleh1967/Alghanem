"""شواهدُ جسر الطبقات الثلاث: الفكُّ واللحامُ والثمنُ والمعلَّقُ والقوانين."""

from __future__ import annotations

import pytest

from alghanem.arabic import tajsir_bridge as module
from alghanem.arabic.fath_ayah_source_text import FATH_AYAH_SOURCE_TEXT
from alghanem.arabic.fatiha_source_text import FATIHA_LINES
from alghanem.arabic.tajsir_bridge import (
    DOUBLED_ROOT_TYPE,
    TAJSIR_BRIDGE_NAMED_RESIDUALS,
    THE_DECLARED_FOLD,
    THE_IBTIDA_COUNTERFACTUAL,
    THE_TA_MARBUTA,
    BridgedPosition,
    LawStanding,
    PausePosition,
    PhoneticState,
    Ratio,
    SegmentSource,
    ShaddaSource,
    TajsirError,
    bridge_word,
    declared_doubled_roots,
    encoding_positions,
    fold_map,
    fold_price_over,
    law_of_ibtida,
    law_of_waqf,
    law_of_wasl,
    nun_census_of,
    phonetic_segments,
    shadda_census_of,
    state_census_of,
    ta_marbuta_census_of,
    ta_marbuta_reading,
    words_of,
)

DEPOSITED: str = "\n".join(FATIHA_LINES) + "\n" + FATH_AYAH_SOURCE_TEXT


# --- الطبقاتُ الثلاثُ مفصولةٌ، والمعرِّفاتُ متلازمة --------------------------


def test_the_encoding_layer_keeps_the_written_form_unfolded() -> None:
    """طبقةُ الترميز لا تطوي: «أ» تبقى «أ» فيها وإن طُويت في الإملاء."""

    positions = bridge_word("\u0623\u064e\u0646\u0652\u062a\u064e")
    assert positions[0].encoding_carrier == "\u0623"
    assert positions[0].orthographic_carrier == "\u0627"


def test_every_position_carries_all_three_identities_at_once() -> None:
    for word in words_of(DEPOSITED):
        for position in bridge_word(word):
            assert position.encoding_carrier
            assert position.orthographic_carrier
            assert isinstance(position.state, PhoneticState)


def test_a_position_without_its_warrant_is_refused() -> None:
    """اللحامُ بلا قرينةٍ استبدالٌ صامت، فيُرفَض عند البناء لا يُقبَل بصمت."""

    with pytest.raises(TajsirError):
        BridgedPosition(
            index=0,
            encoding_carrier="\u0628",
            encoding_marks=(),
            orthographic_carrier="\u0628",
            state=PhoneticState.IMPLIED_SUKUN,
            warrant="",
        )


def test_the_ta_marbuta_is_deliberately_outside_the_declared_fold() -> None:
    assert THE_TA_MARBUTA not in fold_map()
    assert all(rule.written != THE_TA_MARBUTA for rule in THE_DECLARED_FOLD)


def test_every_fold_rule_carries_a_warrant_and_moves_something() -> None:
    for rule in THE_DECLARED_FOLD:
        assert rule.warrant
        assert rule.written != rule.folded


def test_a_fold_rule_that_moves_nothing_is_refused() -> None:
    with pytest.raises(TajsirError):
        module.FoldRule("\u0627", "\u0627", "لا يحرّك شيئًا")


# --- بواباتُ العُري الثلاث، والمعلَّقُ صنفٌ لا بقيّة ------------------------


def test_a_madd_letter_after_its_homogeneous_haraka_is_read_as_madd() -> None:
    positions = bridge_word("\u0642\u064e\u0627\u0644\u064e")
    assert positions[1].state is PhoneticState.MADD


def test_an_initial_alif_before_a_written_sukun_is_an_elided_hamzat_wasl() -> None:
    positions = bridge_word("\u0627\u0644\u0652\u062d\u064e\u0645\u0652\u062f\u064f")
    assert positions[0].state is PhoneticState.ELIDED_HAMZAT_WASL


def test_a_bare_position_that_no_gate_admits_is_suspended_not_guessed() -> None:
    """أوّلُ كلمةٍ عارٍ ليس همزةَ وصلٍ يُعلَّق: لا يُبتدأ بساكنٍ فلا يُقدَّر."""

    positions = bridge_word("\u0628\u0633\u064e\u0645")
    assert positions[0].state is PhoneticState.SUSPENDED


def test_a_madd_letter_without_its_homogeneous_haraka_is_suspended() -> None:
    positions = bridge_word("\u0631\u064f\u0643\u064e\u0639\u064b\u0627")
    assert positions[-1].state is PhoneticState.SUSPENDED


def test_both_suspended_sub_classes_occur_on_the_deposited_text() -> None:
    """المعلَّقُ صنفٌ له شرطان، وكلاهما ينقدح فعلًا — فليس بقيّةً خاملة."""

    warrants = {
        position.warrant
        for word in words_of(DEPOSITED)
        for position in bridge_word(word)
        if position.is_suspended
    }
    assert len(warrants) == 2


def test_the_implied_sukun_gate_can_fail_so_it_is_not_a_catch_all() -> None:
    census = state_census_of(DEPOSITED)
    assert census[PhoneticState.IMPLIED_SUKUN] > 0
    assert census[PhoneticState.SUSPENDED] > 0


def test_the_states_are_eleven_and_three_of_them_are_unwritten() -> None:
    unwritten = {state for state in PhoneticState if not state.is_written}
    assert len(tuple(PhoneticState)) == 11
    assert unwritten == {
        PhoneticState.IMPLIED_SUKUN,
        PhoneticState.MADD,
        PhoneticState.ELIDED_HAMZAT_WASL,
        PhoneticState.SUSPENDED,
    }


# --- ثمنُ الطيّ مقيسٌ لا مُقدَّر ---------------------------------------------


def test_the_fold_price_is_measured_rule_by_rule() -> None:
    prices = fold_price_over(DEPOSITED)
    assert len(prices) == len(THE_DECLARED_FOLD)
    assert any(price.positions_moved > 0 for price in prices)


def test_an_inert_fold_rule_is_shown_inert_and_not_dropped() -> None:
    """بندٌ لم يحرّك موضعًا يبقى في الجدول خاملًا؛ والخمولُ حكمٌ على هذا النصّ."""

    prices = fold_price_over(DEPOSITED)
    assert any(price.is_inert_here for price in prices)
    assert len(prices) == len(THE_DECLARED_FOLD)


# --- الشدّةُ تُعدّ بمصدرها لا بعلامتها ---------------------------------------


def test_the_shadda_is_a_table_of_named_columns_not_one_number() -> None:
    census = shadda_census_of(DEPOSITED, declared_doubled_roots())
    assert len(census.columns) > 1
    assert census.resolved < census.marks


def test_the_sun_lam_column_is_not_empty_on_this_evidence() -> None:
    census = shadda_census_of(DEPOSITED)
    assert census.columns[ShaddaSource.SUN_LAM] > 0


def test_without_the_root_witness_no_position_enters_the_root_column() -> None:
    """غيابُ الشاهد امتناعٌ عن الإخراج لا قيمةٌ افتراضيّة."""

    blind = shadda_census_of(DEPOSITED)
    seeing = shadda_census_of(DEPOSITED, declared_doubled_roots())
    assert ShaddaSource.ROOT_GEMINATION not in blind.columns
    assert seeing.columns[ShaddaSource.ROOT_GEMINATION] > 0
    assert blind.marks == seeing.marks


def test_the_pattern_column_is_named_without_an_admitting_rule() -> None:
    census = shadda_census_of(DEPOSITED, declared_doubled_roots())
    assert ShaddaSource.PATTERN_GEMINATION in tuple(ShaddaSource)
    assert not ShaddaSource.PATTERN_GEMINATION.has_an_admitting_rule
    assert census.columns.get(ShaddaSource.PATTERN_GEMINATION, 0) == 0


def test_a_shadda_opening_a_word_is_read_as_assimilation_across_the_boundary() -> None:
    census = shadda_census_of("\u0644\u0651\u064e\u0647\u064f")
    assert census.columns[ShaddaSource.ASSIMILATION_ACROSS_BOUNDARY] == 1


def test_the_doubled_roots_are_read_from_the_sealed_table_by_its_own_door() -> None:
    roots = declared_doubled_roots()
    assert DOUBLED_ROOT_TYPE == "\u0645\u0636\u0627\u0639\u0641"
    assert len(roots) > 100


# --- التنوينُ نونٌ ساكنة، والعدّان مُعلَنان ----------------------------------


def test_a_tanwin_adds_an_unwritten_nun_marked_with_its_source() -> None:
    segments = phonetic_segments("\u0647\u064f\u062f\u064b\u0649")
    added = [
        segment for segment in segments if segment.source is SegmentSource.FROM_TANWIN
    ]
    assert len(added) == 1
    assert added[0].carrier == "\u0646"
    assert added[0].state is PhoneticState.WRITTEN_SUKUN


def test_the_written_and_spoken_nun_counts_are_both_declared() -> None:
    census = nun_census_of(DEPOSITED)
    assert census.from_tanwin > 0
    assert census.spoken == census.written + census.from_tanwin
    assert census.spoken > census.written


def test_the_tanwin_seat_keeps_its_own_haraka_in_the_phonetic_chain() -> None:
    segments = phonetic_segments("\u0647\u064f\u062f\u064b\u0649")
    added = next(
        index
        for index, segment in enumerate(segments)
        if segment.source is SegmentSource.FROM_TANWIN
    )
    assert segments[added - 1].state is PhoneticState.FATHA
    assert segments[added - 1].source is SegmentSource.WRITTEN


# --- «ة» بدالّتَين لا بطيّ ---------------------------------------------------


def test_the_ta_marbuta_is_read_by_two_functions_not_folded() -> None:
    assert ta_marbuta_reading(PausePosition.JOINED) == "\u062a"
    assert ta_marbuta_reading(PausePosition.PAUSED) == "\u0647"
    assert ta_marbuta_reading(PausePosition.UNKNOWN) is None


def test_an_undeclared_pause_position_suspends_the_ta_marbuta() -> None:
    census = ta_marbuta_census_of(DEPOSITED)
    assert census.suspended == census.occurrences
    assert census.as_ta == 0
    assert census.as_ha == 0


def test_a_declared_pause_position_moves_it_into_one_count_only() -> None:
    order = next(
        index
        for index, word in enumerate(words_of(DEPOSITED))
        if THE_TA_MARBUTA in word
    )
    joined = ta_marbuta_census_of(DEPOSITED, {order: PausePosition.JOINED})
    paused = ta_marbuta_census_of(DEPOSITED, {order: PausePosition.PAUSED})
    assert joined.as_ta == 1
    assert paused.as_ha == 1
    assert joined.occurrences == paused.occurrences


# --- النسبةُ عند الطرفين محجوزةٌ حتّى يُبرَز شاهدُ إمكانِ خلافها -------------


def test_a_ratio_at_an_extreme_is_withheld_until_a_counterfactual_fires() -> None:
    withheld = Ratio(numerator=0, denominator=100)
    assert withheld.is_withheld
    with pytest.raises(TajsirError):
        withheld.value
    released = Ratio(numerator=0, denominator=100, counterfactual_fired=True)
    assert released.value == 0.0


def test_a_ratio_away_from_the_extremes_is_read_without_a_counterfactual() -> None:
    assert Ratio(numerator=1, denominator=4).value == 0.25


def test_a_ratio_with_a_non_positive_denominator_is_refused() -> None:
    with pytest.raises(TajsirError):
        Ratio(numerator=0, denominator=0)


def test_the_ibtida_counterfactual_actually_fires_when_run() -> None:
    """الشاهدُ يُشغَّل ولا يُروى: القاعدةُ تنقدح عليه فعلًا، فصفرُها قابلٌ للخلاف."""

    assert module._starts_with_written_sukun(THE_IBTIDA_COUNTERFACTUAL)


# --- القوانينُ الثلاثةُ مصوغةً قابلةً للسقوط ---------------------------------


def test_the_waqf_law_is_suspended_and_yields_no_figure() -> None:
    reading = law_of_waqf(DEPOSITED)
    assert reading.standing is LawStanding.SUSPENDED_FOR_WANT_OF_MATERIAL
    assert reading.cases == 0
    with pytest.raises(TajsirError):
        reading.rate()


def test_the_ibtida_law_is_measured_on_verified_starts_not_on_every_token() -> None:
    reading = law_of_ibtida(DEPOSITED)
    assert reading.standing is LawStanding.MEASURED
    assert reading.cases == len(
        [line for line in DEPOSITED.split("\n") if line.strip()]
    )
    assert reading.cases < len(words_of(DEPOSITED))


def test_the_ibtida_zero_is_withheld_until_the_counterfactual_is_run() -> None:
    reading = law_of_ibtida(DEPOSITED)
    assert reading.rate().is_withheld
    fired = module._starts_with_written_sukun(THE_IBTIDA_COUNTERFACTUAL)
    assert reading.rate(counterfactual_fired=fired).value == 0.0


def test_the_wasl_law_is_measured_and_its_violations_are_not_zero_by_construction() -> (
    None
):
    reading = law_of_wasl(DEPOSITED)
    assert reading.standing is LawStanding.MEASURED
    assert 0 < reading.violations < reading.cases
    assert not reading.rate().is_withheld


def test_a_suspended_law_with_counted_cases_is_refused() -> None:
    with pytest.raises(TajsirError):
        module.LawReading(
            name="قانونٌ معلَّق",
            standing=LawStanding.SUSPENDED_FOR_WANT_OF_MATERIAL,
            cases=3,
            violations=0,
            note="لا تُحسَب له مواضع",
        )


def test_more_violations_than_cases_is_refused() -> None:
    with pytest.raises(TajsirError):
        module.LawReading(
            name="قانونٌ فاسد",
            standing=LawStanding.MEASURED,
            cases=1,
            violations=2,
            note="",
        )


# --- حدودُ القراءة ----------------------------------------------------------


def test_a_combining_mark_without_a_position_before_it_is_refused() -> None:
    with pytest.raises(TajsirError):
        encoding_positions("\u064e\u0628")


def test_a_token_with_no_arabic_letter_is_not_a_word() -> None:
    assert words_of("<sel> \u0628\u064e") == ("\u0628\u064e",)


def test_the_named_residuals_are_all_exported() -> None:
    for name in TAJSIR_BRIDGE_NAMED_RESIDUALS:
        assert name in module.__all__
        assert getattr(module, name).startswith(name)
