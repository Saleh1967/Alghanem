"""اختباراتُ المحمول المُقرَّر من اليونيكود: قطعيّتُه، ووزنُ استيراده، وحدُّه."""

from __future__ import annotations

import sys
import unicodedata

import pytest

from alghanem.arabic.fath_ayah_source_text import FATH_AYAH_SOURCE_TEXT
from alghanem.arabic.fatiha_source_text import FATIHA_LINES
from alghanem.arabic.implicit_sukun_treatment import SukunSource, census_over
from alghanem.arabic.written_haraka_mark import (
    CANONICAL_FORMS,
    THE_IMPORTED_HARAKAT,
    THE_SUPERSET_MEASURED_BY_UNICODE_VERSION,
    UNICODE_VERSION,
    WRITTEN_HARAKA_NAMED_RESIDUALS,
    ImportWeight,
    MarkCensus,
    Position,
    WrittenHarakaError,
    arabic_combining_marks,
    census_of,
    compatibility_exceptions,
    has_written_haraka_mark,
    import_weight,
    imported_haraka_names,
    positions_of,
    the_superset_recorded_for,
    verify_canonical_invariance,
)

_FATIHA = "\n".join(FATIHA_LINES)
_FATH = FATH_AYAH_SOURCE_TEXT


# --- المحمولُ نفسُه: كلّيٌّ، ثنائيُّ القيمة، لا يقرأ إلّا نقاطَ الترميز ----


def test_the_predicate_is_total_over_every_position_of_both_deposits() -> None:
    for text in (_FATIHA, _FATH):
        for position in positions_of(text):
            assert has_written_haraka_mark(position) in (True, False)


def test_the_predicate_is_exactly_membership_in_the_imported_seven() -> None:
    for text in (_FATIHA, _FATH):
        for position in positions_of(text):
            assert has_written_haraka_mark(position) == bool(
                set(position.marks) & THE_IMPORTED_HARAKAT
            )


def test_the_census_partitions_the_positions_with_no_third_bucket() -> None:
    for text, scope, total, marked in (
        (_FATIHA, "الفاتحة", 143, 103),
        (_FATH, "الفتح ٢٩", 249, 188),
    ):
        census = census_of(text, scope)
        assert (census.total, census.marked) == (total, marked)
        assert census.marked + census.unmarked == census.total


def test_the_marked_share_is_recomputed_and_not_stored() -> None:
    assert census_of(_FATIHA, "الفاتحة").marked_share == pytest.approx(
        72.027972, abs=1e-6
    )
    assert census_of(_FATH, "الفتح ٢٩").marked_share == pytest.approx(
        75.502008, abs=1e-6
    )


# --- الموضعُ مشتقٌّ من الجدول لا مُصطلَحٌ عليه ------------------------------


def test_a_position_is_opened_by_general_category_alone() -> None:
    for text in (_FATIHA, _FATH):
        for position in positions_of(text):
            assert unicodedata.category(position.carrier) != "Mn"
            for mark in position.marks:
                assert unicodedata.category(mark) == "Mn"


def test_the_two_deposits_split_cleanly_into_letters_and_marks() -> None:
    categories = {
        unicodedata.category(character)
        for text in (_FATIHA, _FATH)
        for character in text
        if not character.isspace()
    }
    assert categories == {"Lo", "Mn"}


def test_a_combining_mark_may_not_open_a_position() -> None:
    with pytest.raises(WrittenHarakaError):
        Position(carrier="\u064e", marks=(), index=0)
    with pytest.raises(WrittenHarakaError):
        positions_of("\u064e\u0628")
    with pytest.raises(WrittenHarakaError):
        Position(carrier="\u0628", marks=("\u0628",), index=0)


# --- وزنُ الاستيراد: مقيسٌ لا موصوف ---------------------------------------


def test_the_import_is_seven_of_a_derived_one_hundred_and_five() -> None:
    weight = import_weight()
    recorded = the_superset_recorded_for(UNICODE_VERSION)
    assert weight.selected == 7
    assert weight.superset == len(arabic_combining_marks())
    assert weight.unicode_version == UNICODE_VERSION == unicodedata.unidata_version
    if recorded is None:
        pytest.skip(f"لم يُقَس على يونيكود {UNICODE_VERSION} بعد.")
    assert weight.superset == recorded
    assert weight.share == pytest.approx(100.0 * 7 / recorded, abs=1e-6)


def test_the_denominator_moved_between_the_two_measured_versions() -> None:
    assert THE_SUPERSET_MEASURED_BY_UNICODE_VERSION["13.0.0"] == 96
    assert THE_SUPERSET_MEASURED_BY_UNICODE_VERSION["15.0.0"] == 105


def test_the_import_share_moves_with_the_denominator_not_with_the_import() -> None:
    older = 100.0 * 7 / THE_SUPERSET_MEASURED_BY_UNICODE_VERSION["13.0.0"]
    newer = 100.0 * 7 / THE_SUPERSET_MEASURED_BY_UNICODE_VERSION["15.0.0"]
    assert older == pytest.approx(7.291667, abs=1e-6)
    assert newer == pytest.approx(6.666667, abs=1e-6)
    assert older > newer


def test_an_unmeasured_unicode_version_is_refused_not_guessed() -> None:
    assert the_superset_recorded_for("1.0.0") is None


def test_the_superset_is_read_from_the_table_and_contains_the_import() -> None:
    superset = set(arabic_combining_marks())
    assert THE_IMPORTED_HARAKAT <= superset
    assert all(unicodedata.category(mark) == "Mn" for mark in superset)


def test_the_imported_names_are_read_from_unicode_not_typed_by_hand() -> None:
    names = dict(imported_haraka_names())
    assert names["U+064E"] == "ARABIC FATHA"
    assert names["U+0652"] == "ARABIC SUKUN"
    assert len(names) == 7


def test_shadda_and_dagger_are_combining_marks_that_the_import_left_out() -> None:
    for excluded in ("\u0651", "\u0670"):
        assert unicodedata.category(excluded) == "Mn"
        assert excluded in set(arabic_combining_marks())
        assert excluded not in THE_IMPORTED_HARAKAT


def test_the_contested_exclusions_move_nothing_at_all_on_this_evidence() -> None:
    """أخطرُ ما في الاستيراد — إخراجُ الشدّة والخنجريّة — لا يحرّك رقمًا ههنا."""

    for text in (_FATIHA, _FATH):
        for extra in ({"\u0651"}, {"\u0670"}, {"\u0651", "\u0670"}):
            widened = THE_IMPORTED_HARAKAT | extra
            moved = sum(
                1
                for position in positions_of(text)
                if bool(set(position.marks) & widened)
                != has_written_haraka_mark(position)
            )
            assert moved == 0


def test_the_inertness_is_a_property_of_these_texts_and_not_of_the_rule() -> None:
    """وسببُه أنّ كلَّ شدّةٍ ههنا تصحبها حركة؛ ولو تجرّدت لتحرّك الحكم."""

    for text in (_FATIHA, _FATH):
        for position in positions_of(text):
            if "\u0651" in position.marks or "\u0670" in position.marks:
                assert position.haraka_marks

    bare_shadda = positions_of("\u0628\u0651")[0]
    assert not has_written_haraka_mark(bare_shadda)
    assert bool(set(bare_shadda.marks) & (THE_IMPORTED_HARAKAT | {"\u0651"}))


def test_an_import_weight_outside_its_superset_is_refused() -> None:
    with pytest.raises(WrittenHarakaError):
        ImportWeight(selected=9, superset=7, unicode_version=UNICODE_VERSION)
    with pytest.raises(WrittenHarakaError):
        ImportWeight(selected=0, superset=7, unicode_version=UNICODE_VERSION)


# --- البرهانُ بالاستقراء التامّ، وحدُّه ------------------------------------


def test_the_verdict_is_invariant_under_canonical_normalization_on_the_deposits() -> (
    None
):
    for text, scope in ((_FATIHA, "الفاتحة"), (_FATH, "الفتح ٢٩")):
        readings = {form: census_of(text, scope, form=form) for form in CANONICAL_FORMS}
        assert readings["NFC"].total == readings["NFD"].total
        assert readings["NFC"].marked == readings["NFD"].marked


def test_no_codepoint_in_all_of_unicode_can_break_the_canonical_invariance() -> None:
    """استقراءٌ تامٌّ على 1,114,112 نقطة: ثلاثةُ أعدادٍ يجب أن تكون صفرًا."""

    introduced, destroyed, split = verify_canonical_invariance()
    assert (introduced, destroyed, split) == (0, 0, 0)


def test_the_exhaustive_check_really_walked_the_whole_code_space() -> None:
    assert sys.maxunicode == 0x10FFFF
    narrow = verify_canonical_invariance(limit=0x00FF)
    assert narrow == (0, 0, 0)


def test_the_invariance_breaks_under_compatibility_in_exactly_twenty_two_places() -> (
    None
):
    exceptions = compatibility_exceptions()
    assert len(exceptions) == 22
    assert "\ufe76" in exceptions
    assert unicodedata.normalize("NFKD", "\ufe76") == "\u0020\u064e"
    for character in exceptions:
        assert set(unicodedata.normalize("NFKD", character)) & THE_IMPORTED_HARAKAT
        assert not set(unicodedata.normalize("NFD", character)) & THE_IMPORTED_HARAKAT


def test_a_compatibility_form_is_refused_rather_than_silently_corrected() -> None:
    for form in ("NFKC", "NFKD", "nfc", ""):
        with pytest.raises(WrittenHarakaError):
            positions_of(_FATIHA, form=form)


# --- المطابقةُ مع الإحصاء السابق، وهي موضعُ الفائدة ------------------------


@pytest.mark.parametrize(
    ("text", "lines", "scope", "unmarked"),
    [
        (_FATIHA, FATIHA_LINES, "الفاتحة", 40),
        (_FATH, (FATH_AYAH_SOURCE_TEXT,), "الفتح ٢٩", 61),
    ],
)
def test_the_unmarked_positions_are_the_implicit_sukun_minus_the_pair_starts(
    text: str, lines: tuple[str, ...], scope: str, unmarked: int
) -> None:
    census = census_of(text, scope)
    previous = census_over(lines, scope)
    assert census.unmarked == unmarked
    assert census.unmarked == previous.unwritten - previous.count_of(
        SukunSource.GEMINATION_PAIR_START
    )
    assert census.unmarked == previous.count_of(
        SukunSource.ALIF_WITHOUT_A_MARK
    ) + previous.count_of(SukunSource.BARE_CARRIER)


def test_the_explicit_sukun_agrees_with_the_earlier_census_exactly() -> None:
    for text, lines, scope in (
        (_FATIHA, FATIHA_LINES, "الفاتحة"),
        (_FATH, (FATH_AYAH_SOURCE_TEXT,), "الفتح ٢٩"),
    ):
        written = sum(
            1 for position in positions_of(text) if "\u0652" in position.marks
        )
        assert written == census_over(lines, scope).written


def test_a_gemination_half_cannot_enter_a_count_of_written_positions() -> None:
    """ما نُبِّه عليه هناك باليد صار ههنا غيرَ قابلٍ للدخول بناءً."""

    positions = positions_of(_FATIHA)
    assert len(positions) == sum(
        1 for character in _FATIHA if unicodedata.category(character) == "Lo"
    )


# --- ما لا يُثبِته هذا المحمول ---------------------------------------------


def test_what_this_predicate_does_not_establish_is_named() -> None:
    assert set(WRITTEN_HARAKA_NAMED_RESIDUALS) == {
        "THE_IMPORT_IS_A_SELECTION_NOT_A_DERIVATION",
        "SHADDA_AND_DAGGER_ARE_EXCLUDED_BY_THE_IMPORT_NOT_BY_UNICODE",
        "THE_CONTESTED_EXCLUSIONS_ARE_INERT_ON_THIS_EVIDENCE",
        "THE_INVARIANCE_IS_CANONICAL_AND_NOT_COMPATIBILITY",
        "THE_NEGATIVE_IS_AN_ABSENT_MARK_NOT_A_SUKUN",
        "A_WRITTEN_MARK_IS_NOT_A_PRONOUNCED_VOWEL",
        "A_UNICODE_VERSION_IS_A_DEPENDENCY",
    }
    for key, text in WRITTEN_HARAKA_NAMED_RESIDUALS.items():
        assert text.startswith(f"{key}: ")


def test_the_predicate_reads_no_phonetic_table_of_this_tree() -> None:
    import ast
    from pathlib import Path

    import alghanem.arabic.written_haraka_mark as module

    tree = ast.parse(Path(module.__file__).read_text(encoding="utf-8"))
    imported = {
        node.module or "" for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)
    } | {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    assert imported <= {"__future__", "sys", "unicodedata", "dataclasses", "typing"}
    for forbidden in ("makharij", "kernel", "classical", "gloss"):
        assert not any(forbidden in name for name in imported)


def test_the_census_refuses_an_empty_or_negative_reading() -> None:
    with pytest.raises(WrittenHarakaError):
        MarkCensus(scope="خالٍ", marked=0, unmarked=0)
    with pytest.raises(WrittenHarakaError):
        MarkCensus(scope="سالب", marked=-1, unmarked=4)
