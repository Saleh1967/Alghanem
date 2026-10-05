"""شواهدُ جسر المعجم: تُصادم أرقامَه ولا تنقلها، وتُمسِك الوكيلَ باسمه."""

from __future__ import annotations

import pytest

from alghanem.arabic.lexicon_bridge import (
    DECLARED_CARDINALITY,
    LEXICON_BRIDGE_NAMED_RESIDUALS,
    THE_LOCKED_COUNTS,
    THE_QUOTED_FIRST_EXHIBIT,
    THE_THREE_LEGS,
    THE_TWENTY_MATERIALS,
    BridgeLeg,
    EntryStage,
    LegStanding,
    LexiconBridgeError,
    QuotedStanding,
    corpus_ayahs,
    corpus_tokens,
    entry_leg_census,
    family_leg_census,
    locked_counts_have_drifted,
    material_readings,
    price_of_the_refused_collapse,
    proxy_false_admissions,
    quoted_figures_reading,
    witness_leg_reading,
)


def test_the_bridge_has_three_legs_and_no_leg_is_declared_twice() -> None:
    assert len(THE_THREE_LEGS) == 3
    assert {declaration.leg for declaration in THE_THREE_LEGS} == set(BridgeLeg)


def test_the_witness_leg_is_the_only_one_that_is_half_built() -> None:
    half = [
        declaration
        for declaration in THE_THREE_LEGS
        if declaration.standing is LegStanding.HALF_BUILT_AND_ITS_VACANCY_MEASURED
    ]
    assert [declaration.leg for declaration in half] == [BridgeLeg.WITNESS_TO_AYAH]


def test_the_closed_list_carries_its_declared_cardinality_without_repetition() -> None:
    assert len(THE_TWENTY_MATERIALS) == DECLARED_CARDINALITY == 20
    assert len(set(THE_TWENTY_MATERIALS)) == DECLARED_CARDINALITY


def test_every_locked_count_is_regenerated_from_the_bytes_it_names() -> None:
    """العددُ المقفلُ يُعاد اشتقاقُه، فانزياحُه يُسمّى باسمه لا يُبتلَع."""

    assert locked_counts_have_drifted() == ()


def test_the_corpus_is_read_under_the_declared_token_rule_not_the_field_rule() -> None:
    """بايتاتُ هذه المدوّنة بلا فواصلِ حقول، فقاعدةُ السطر مسنونةٌ بنصّها."""

    from alghanem.arabic.quran_corpus_word_total import (
        ayah_texts,
        read_quran_corpus_bytes,
    )

    assert ayah_texts(read_quran_corpus_bytes().decode("utf-8")) == ()
    assert len(corpus_ayahs()) == 6236
    assert len(corpus_tokens()) == 78245


def test_the_twenty_are_all_present_in_the_corpus_by_count_not_by_claim() -> None:
    census = family_leg_census()
    assert census.presence_is_complete
    assert census.present == 20
    assert all(reading.is_present for reading in material_readings())


def test_presence_in_the_text_is_not_presence_in_the_lexicon() -> None:
    """الرجلان تفترقان بالعدّ: عشرون في المدوّنة، وثمانيَ عشرةَ مدخلًا."""

    as_written = entry_leg_census(EntryStage.AS_WRITTEN)
    assert as_written.entries_in_the_lexicon == 18
    assert as_written.absent == ("قرأ", "هدي")
    assert family_leg_census().present == 20


def test_normalisation_moves_the_entry_count_and_both_hamza_stages_agree() -> None:
    """التطبيعُ يُغيّر الرقم، وقاعدتا الهمزة تبلغان الرقمَ نفسَه على العشرين."""

    bare = entry_leg_census(EntryStage.HAMZA_TO_BARE_ALIF)
    carried = entry_leg_census(EntryStage.HAMZA_TO_CARRIED_ALIF)
    assert bare.entries_in_the_lexicon == carried.entries_in_the_lexicon == 19
    assert bare.absent == carried.absent == ("قرأ",)


def test_the_last_absent_entry_is_blocked_by_a_rule_this_tree_refuses() -> None:
    """«قرأ» لا تبلغ «قري» إلّا بحسمِ هويّة العلّة، وهو مرفوضٌ باسمه."""

    from alghanem.arabic.maqayis_root_table_deposit import root_table_rows
    from alghanem.arabic.root_orthography_bridge import REFUSED_RULES

    entries = {row["root_full"] for row in root_table_rows()}
    assert "قري" in entries
    assert "قرأ" not in entries
    assert "ألف_إلى_واو_أو_ياء" in {rule.name for rule in REFUSED_RULES}


def test_the_stage_is_a_required_argument_and_is_not_chosen_for_the_caller() -> None:
    with pytest.raises(LexiconBridgeError):
        entry_leg_census("همزة_إلى_ألف_عارية")  # type: ignore[arg-type]


def test_the_proxy_admits_forms_it_does_not_claim_to_derive() -> None:
    """وكيلُ الإطار يُصيب ما ليس من المادّة، ويُعرَض ذلك ولا يُطوى."""

    admitted = proxy_false_admissions("كتب")
    assert admitted
    assert any("اكتسب" in form for form in admitted)


def test_a_material_outside_the_closed_list_is_refused_not_measured() -> None:
    with pytest.raises(LexiconBridgeError):
        proxy_false_admissions("درس")


def test_the_network_is_measured_and_the_lexicon_side_of_it_is_not() -> None:
    reading = witness_leg_reading()
    assert reading.edges == 4643
    assert reading.ayahs_touched == 3014
    assert reading.ayahs_in_the_corpus == 6236
    assert not reading.the_join_is_readable


def test_the_vacancy_of_the_witness_leg_survives_a_positive_witness() -> None:
    """النفيُ بعد شاهدٍ موجِب: المداخلُ والمقاطعُ بالآلاف، فالأداةُ تقرأ."""

    reading = witness_leg_reading()
    assert reading.lexicon_witness_segments > 1000
    assert entry_leg_census(EntryStage.AS_WRITTEN).deposited_entries > 1000
    assert not reading.lexicon_has_an_ayah_column


def test_the_refused_collapse_is_priced_and_is_never_licensed() -> None:
    price = price_of_the_refused_collapse()
    assert price.rule_name == "حذف_التضعيف"
    assert not price.is_licensed
    assert price.occurrences_added == 395
    assert price.families_added == 153


def test_every_quoted_figure_is_collided_and_none_is_merely_transcribed() -> None:
    collided = quoted_figures_reading()
    assert {figure.name for figure in collided} == set(THE_QUOTED_FIRST_EXHIBIT)
    assert all(
        figure.quoted == THE_QUOTED_FIRST_EXHIBIT[figure.name] for figure in collided
    )


def test_the_quoted_totals_fall_and_the_quoted_leader_stands() -> None:
    standings = {figure.name: figure for figure in quoted_figures_reading()}
    assert standings["الاتّساع: عائلات"].standing is QuotedStanding.REFUTED
    assert standings["الاتّساع: عائلات"].measured == 1058
    assert standings["الورود: مواضع"].standing is QuotedStanding.REFUTED
    assert standings["الورود: مواضع"].measured == 5385
    assert standings["صدرُ الورود: علم"].standing is QuotedStanding.REPRODUCED


def test_the_second_ranked_quoted_figure_needs_a_refused_rule_to_be_reached() -> None:
    """«حب 399» لا تبلغه بايتاتُنا إلّا بقاعدةٍ مرفوضة؛ فحكمُه ثالثٌ لا ثانٍ."""

    standings = {figure.name: figure for figure in quoted_figures_reading()}
    figure = standings["تاليه: حب"]
    assert figure.standing is QuotedStanding.REACHED_ONLY_BY_A_REFUSED_RULE
    assert figure.measured == 4


def test_a_reading_with_more_families_than_occurrences_is_refused() -> None:
    from alghanem.arabic.lexicon_bridge import MaterialReading

    with pytest.raises(LexiconBridgeError):
        MaterialReading(material="كتب", families=9, occurrences=2, ayahs=1)


def test_every_named_residual_is_a_sentence_not_a_label() -> None:
    assert len(LEXICON_BRIDGE_NAMED_RESIDUALS) == 9
    assert all(len(text) > 80 for text in LEXICON_BRIDGE_NAMED_RESIDUALS.values())


def test_every_locked_count_names_a_generator_that_exists() -> None:
    from alghanem.arabic import lexicon_bridge

    assert THE_LOCKED_COUNTS
    for locked in THE_LOCKED_COUNTS:
        assert callable(getattr(lexicon_bridge, locked.generator))
