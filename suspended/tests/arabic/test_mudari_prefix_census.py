"""اختباراتُ عدِّ حروف المضارعة — كلُّ رقمٍ يُعاد من القرص لا يُصدَّق عن النثر."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from alghanem.arabic.mudari_prefix_census import (
    MUDARI_CENSUS_NAMED_RESIDUALS,
    THE_ABSENT_IDENTIFIERS,
    THE_HAND_AUDITED_TOP_TYPES,
    THE_TANWIN_EXCLUDED_TYPES,
    CarrierKey,
    CensusError,
    ExpectationVerdict,
    HandAudit,
    MudariCensus,
    NounFilter,
    SlotClass,
    SlotReading,
    census_under,
    every_census,
    the_carrier_ladder_movement,
    the_expectation_verdict,
    the_tanwin_filter_precision,
)
from alghanem.arabic.mudari_prefix_preregistration import (
    THE_ENTAILED_EXPECTATION_FLOOR,
)

MODULE_PATH = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "alghanem"
    / "arabic"
    / "mudari_prefix_census.py"
)

SEALED = SlotReading.SEALED_PENULTIMATE
POST_HOC = SlotReading.POST_HOC_THIRD_SLOT


def _filtered() -> MudariCensus:
    return census_under(
        CarrierKey.NARROW_HAMZA_ON_ALIF, NounFilter.TANWIN_BEARING_EXCLUDED
    )


def test_all_four_censuses_are_published() -> None:
    assert len(every_census()) == 4
    assert len({(c.carrier, c.noun_filter) for c in every_census()}) == 4


def test_the_sealed_expectation_is_falsified_on_these_bytes() -> None:
    assert the_expectation_verdict() is ExpectationVerdict.FALSIFIED
    share = _filtered().kasra_and_fatha_share(SEALED)
    assert share < THE_ENTAILED_EXPECTATION_FLOOR


def test_the_transcribed_sealed_figures_match_what_disk_measures() -> None:
    census = _filtered()
    assert census.matches == 1003
    assert census.distinct_surfaces == 449
    assert census.counts(SEALED) == {
        SlotClass.FATHA: 173,
        SlotClass.DAMMA: 62,
        SlotClass.KASRA: 266,
        SlotClass.SUKUN: 52,
        SlotClass.UNMARKED: 450,
    }
    assert census.kasra_and_fatha_share(SEALED) == pytest.approx(0.4377, abs=5e-5)


def test_the_unfiltered_count_matches_its_transcription() -> None:
    census = census_under(CarrierKey.NARROW_HAMZA_ON_ALIF, NounFilter.NO_FILTER)
    assert census.matches == 1029
    assert census.distinct_surfaces == 456


def test_the_unmarked_penultimate_slot_is_overwhelmingly_a_waw() -> None:
    letters = dict(_filtered().unmarked_penultimate_letters)
    assert letters["\u0648"] == 427
    assert letters["\u064a"] == 22
    assert sum(letters.values()) == 450
    assert (letters["\u0648"] + letters["\u064a"]) / 450 > 0.99


def test_the_post_hoc_reading_clears_the_floor_but_is_named_post_hoc() -> None:
    census = _filtered()
    assert census.counts(POST_HOC) == {
        SlotClass.FATHA: 308,
        SlotClass.DAMMA: 57,
        SlotClass.KASRA: 638,
    }
    assert census.kasra_and_fatha_share(POST_HOC) == pytest.approx(0.9432, abs=5e-5)
    assert census.kasra_and_fatha_share(POST_HOC) > THE_ENTAILED_EXPECTATION_FLOOR
    assert (
        census.verdict is ExpectationVerdict.FALSIFIED
    ), "الحكمُ للقراءة المختومة وحدَها؛ ونجاحُ البعديّة لا يرفع تكذيبَها."


def test_the_kasra_to_fatha_split_is_reported_without_a_prediction() -> None:
    kasra, fatha = _filtered().kasra_to_fatha(POST_HOC)
    assert (kasra, fatha) == (638, 308)


def test_the_carrier_ladder_is_flat_on_these_bytes() -> None:
    movement = the_carrier_ladder_movement()
    assert set(movement) == set(NounFilter)
    assert set(movement.values()) == {0}


def test_widening_the_carrier_changes_no_class_table() -> None:
    for noun_filter in NounFilter:
        narrow = census_under(CarrierKey.NARROW_HAMZA_ON_ALIF, noun_filter)
        wide = census_under(CarrierKey.WIDE_ANY_ALIF_SHAPE, noun_filter)
        assert narrow.sealed_classes == wide.sealed_classes
        assert narrow.post_hoc_classes == wide.post_hoc_classes


def test_the_tanwin_filter_removes_exactly_its_named_types() -> None:
    unfiltered = census_under(CarrierKey.NARROW_HAMZA_ON_ALIF, NounFilter.NO_FILTER)
    filtered = _filtered()
    assert unfiltered.matches - filtered.matches == 26
    assert unfiltered.distinct_surfaces - filtered.distinct_surfaces == 7
    assert len(THE_TANWIN_EXCLUDED_TYPES) == 7
    assert len(set(THE_TANWIN_EXCLUDED_TYPES)) == 7


def test_the_named_excluded_types_really_occur_and_really_bear_tanwin() -> None:
    from alghanem.arabic.quran_corpus_word_total import read_quran_corpus_bytes

    words = set(read_quran_corpus_bytes().decode("utf-8").split())
    tanwin = set("\u064b\u064c\u064d")
    for surface in THE_TANWIN_EXCLUDED_TYPES:
        assert surface in words, f"صورةٌ مُسمّاةٌ مُخرَجةً وليست في البايتات: {surface}"
        assert tanwin & set(surface)


def test_the_filter_is_precise_but_the_audit_shows_it_incomplete() -> None:
    nouns, total = the_tanwin_filter_precision()
    assert (nouns, total) == (7, 7)
    surviving_nouns = [item for item in THE_HAND_AUDITED_TOP_TYPES if item.is_a_noun]
    assert surviving_nouns, "مصفاةٌ تُعلَن تامّةً بلا باقٍ دعوى لا قياس."
    assert [item.surface for item in surviving_nouns] == ["أُخْرَى"]


def test_the_hand_audit_covers_ten_types_in_descending_order() -> None:
    assert len(THE_HAND_AUDITED_TOP_TYPES) == 10
    occurrences = [item.occurrences for item in THE_HAND_AUDITED_TOP_TYPES]
    assert occurrences == sorted(occurrences, reverse=True)


def test_the_hand_audited_counts_reproduce_from_the_bytes() -> None:
    from collections import Counter

    from alghanem.arabic.quran_corpus_word_total import read_quran_corpus_bytes

    tally = Counter(read_quran_corpus_bytes().decode("utf-8").split())
    for item in THE_HAND_AUDITED_TOP_TYPES:
        assert tally[item.surface] == item.occurrences


def test_the_prefix_letters_are_not_four_equal_quarters() -> None:
    letters = dict(_filtered().prefix_letters)
    assert letters == {"\u064a": 577, "\u062a": 287, "\u0623": 86, "\u0646": 53}
    assert sum(letters.values()) == _filtered().matches
    assert letters["\u064a"] / _filtered().matches > 0.5


def test_the_class_tables_always_sum_to_the_match_count() -> None:
    for census in every_census():
        for reading in SlotReading:
            assert sum(census.counts(reading).values()) == census.matches


def test_a_census_whose_table_does_not_sum_is_refused() -> None:
    with pytest.raises(CensusError):
        MudariCensus(
            carrier=CarrierKey.NARROW_HAMZA_ON_ALIF,
            noun_filter=NounFilter.NO_FILTER,
            matches=10,
            distinct_surfaces=3,
            sealed_classes=((SlotClass.KASRA, 4),),
            post_hoc_classes=((SlotClass.KASRA, 10),),
            unmarked_penultimate_letters=(),
            prefix_letters=(),
        )


def test_an_audit_without_a_surface_is_refused() -> None:
    with pytest.raises(CensusError):
        HandAudit("  ", 3, False, "نصّ")
    with pytest.raises(CensusError):
        HandAudit("يُؤْمِنُ", 0, False, "نصّ")


def test_an_empty_census_has_no_share() -> None:
    empty = MudariCensus(
        carrier=CarrierKey.NARROW_HAMZA_ON_ALIF,
        noun_filter=NounFilter.NO_FILTER,
        matches=0,
        distinct_surfaces=0,
        sealed_classes=(),
        post_hoc_classes=(),
        unmarked_penultimate_letters=(),
        prefix_letters=(),
    )
    with pytest.raises(CensusError):
        empty.kasra_and_fatha_share(SEALED)


def test_the_absent_identifier_is_still_absent_from_the_tree() -> None:
    assert "c35956ef" in THE_ABSENT_IDENTIFIERS
    root = Path(__file__).resolve().parents[2]
    for folder in ("src", "docs"):
        for path in (root / folder).rglob("*"):
            if not path.is_file() or path.suffix not in {".py", ".md"}:
                continue
            if path.name == "mudari_prefix_census.py":
                continue
            assert "c35956ef" not in path.read_text(
                encoding="utf-8"
            ), f"المُعرَّفُ المُسجَّلُ غائبًا وُجد في {path}؛ فليُرفَع من السجلّ."


def test_the_verdict_is_derived_and_never_stored() -> None:
    assert not any(
        "verdict" in field for field in MudariCensus.__dataclass_fields__
    ), "حكمُ التوقُّع يُشتَقّ من طرفيه ولا يُودَع حقلًا."
    source = MODULE_PATH.read_text(encoding="utf-8")
    assert "def verdict" in source


def test_every_named_residual_carries_its_own_token() -> None:
    for token, text in MUDARI_CENSUS_NAMED_RESIDUALS.items():
        assert text.startswith(f"{token}:")


def test_the_prose_transcribes_the_numbers_it_measured() -> None:
    source = MODULE_PATH.read_text(encoding="utf-8")
    prose = source.split('"""')[1]
    for figure in ("1,003", "43.77", "94.32", "427", "450", "638", "308"):
        assert figure in prose, f"رقمٌ مقيسٌ غائبٌ عن نثره: {figure}"


def test_the_prose_never_calls_the_post_hoc_reading_a_confirmation() -> None:
    source = MODULE_PATH.read_text(encoding="utf-8")
    prose = source.split('"""')[1]
    assert "بعديّة" in prose
    assert "لا تُقرأ هذه تصديقًا للتوقُّع" in prose
    assert not re.search(r"التوقُّعُ\s+تحقّق", prose)


def test_the_module_imports_no_authority() -> None:
    source = MODULE_PATH.read_text(encoding="utf-8")
    for forbidden in ("from ..kernel", "from ..program", "from alghanem.kernel"):
        assert forbidden not in source
