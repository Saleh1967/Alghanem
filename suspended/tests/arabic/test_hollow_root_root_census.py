"""اختباراتُ إحصاء الجذور المتنافسة على المدوَّنة الصرفية المُبصَّمة.

والأسطرُ المكتوبة هنا **مُصطنَعةٌ مُصرَّحٌ بجنسها**، لا مقتطعةٌ من المدوَّنة:
رخصتُها تمنع نسخَ بايتاتها إلى هذه الشجرة. وبنيتُها وحدَها هي المُحاكاة.

وفيها الحالةُ التي **كسرت** أوّلَ نسخةٍ من الوحدة عند تشغيلها على البايتات:
عمودُ الصورة الفارغ في لاحقة ضمير المتكلّم. فاختبارٌ لا يحوي ما أسقط النسخةَ
السابقة اختبارٌ بُني ليمرّ.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from alghanem.arabic.hollow_root_root_census import (
    ANNOTATOR_AGREEMENT_IS_NOT_TRUTH_NOTE,
    COMPETING_ROOT_PAIRS,
    HOLLOW_ROOT_CENSUS_NAMED_RESIDUALS,
    QYL_EXAMINED_OCCURRENCES,
    RARE_ROOT_LOCATION_LIMIT,
    REDERIVED_ROOT_COUNTS,
    REDERIVED_SEGMENT_COUNT,
    THE_CENSUS_IS_NOT_A_ROOT_EXTRACTOR_NOTE,
    HollowRootCensusError,
    RootCensusRow,
    RootCountingRule,
    census_rows,
    corpus_lines,
    parse_segment_line,
    rederive_segment_count,
    root_of_features,
)
from alghanem.arabic.irab_corpus_witness import QURANIC_ARABIC_CORPUS_WITNESS

CORPUS_PATH_VARIABLE = "ALGHANEM_QAC_MORPHOLOGY_PATH"

HAND_BUILT_LINES: tuple[str, ...] = (
    "# a copyright block line, not a segment",
    "LOCATION\tFORM\tTAG\tFEATURES",
    "(1:1:1:1)\tyaxaAfu\tV\tSTEM|POS:V|IMPF|LEM:xaAfa|ROOT:xwf|3MS",
    "(1:1:1:2)\t\tPRON\tSUFFIX|PRON:1S",
    "(1:2:1:1)\txawofFA\tN\tSTEM|POS:N|LEM:xawof|ROOT:xwf|M|INDEF|ACC",
    "(1:2:1:2)\tsomi\tN\tSTEM|POS:N|LEM:{som|ROOT:xwfr|M|GEN",
    "(2:1:1:1)\t{l\tDET\tPREFIX|Al+",
    "",
)


def _roots() -> tuple[tuple[str, str], ...]:
    return (("xwf", "خوف"), ("xyf", "خيف"))


def _records() -> list:
    return [
        record
        for record in (parse_segment_line(line) for line in HAND_BUILT_LINES)
        if record is not None
    ]


def test_comment_header_and_blank_lines_are_not_segments() -> None:
    assert parse_segment_line(HAND_BUILT_LINES[0]) is None
    assert parse_segment_line(HAND_BUILT_LINES[1]) is None
    assert parse_segment_line("") is None
    assert rederive_segment_count(HAND_BUILT_LINES) == 5


def test_an_empty_form_column_is_a_segment_not_a_malformed_line() -> None:
    record = parse_segment_line(HAND_BUILT_LINES[3])

    assert record is not None
    assert record.form == ""
    assert record.tag == "PRON"
    assert record.location == "(1:1:1:2)"


def test_a_line_with_the_wrong_column_count_is_refused_not_skipped() -> None:
    with pytest.raises(HollowRootCensusError):
        parse_segment_line("(1:1:1:1)\tyaxaAfu\tV")


def test_a_location_outside_the_declared_shape_is_refused() -> None:
    with pytest.raises(HollowRootCensusError):
        parse_segment_line("1:1:1:1\tyaxaAfu\tV\tSTEM|POS:V")
    with pytest.raises(HollowRootCensusError):
        parse_segment_line("(1:1:1)\tyaxaAfu\tV\tSTEM|POS:V")
    with pytest.raises(HollowRootCensusError):
        parse_segment_line("(1:1:1:x)\tyaxaAfu\tV\tSTEM|POS:V")


def test_a_segment_without_a_root_feature_reads_as_none() -> None:
    assert root_of_features("PREFIX|Al+") is None
    assert root_of_features("STEM|POS:V|ROOT:xwf|3MS") == "xwf"


def test_a_longer_root_is_not_counted_as_its_prefix() -> None:
    assert root_of_features("STEM|ROOT:xwfr|M") == "xwfr"

    rows = census_rows(_records(), _roots())

    assert rows[0].count_under(RootCountingRule.SEGMENTS) == 2


def test_the_three_counting_rules_do_not_collapse_into_one() -> None:
    rows = census_rows(_records(), _roots())

    assert rows[0].count_under(RootCountingRule.SEGMENTS) == 2
    assert rows[0].count_under(RootCountingRule.WORDS) == 2
    assert rows[0].count_under(RootCountingRule.VERSES) == 2
    assert rows[1].count_under(RootCountingRule.SEGMENTS) == 0


def test_a_duplicated_requested_root_is_refused() -> None:
    with pytest.raises(HollowRootCensusError):
        census_rows(_records(), (("xwf", "خوف"), ("xwf", "خوف")))


def test_a_row_may_not_claim_more_words_than_segments() -> None:
    with pytest.raises(HollowRootCensusError):
        RootCensusRow(
            root_buckwalter="xwf",
            root_arabic="خوف",
            segment_count=1,
            word_count=2,
            verse_count=1,
            locations=("(1:1:1:1)",),
        )


def test_a_frequent_root_may_not_deposit_hand_picked_locations() -> None:
    with pytest.raises(HollowRootCensusError):
        RootCensusRow(
            root_buckwalter="qwl",
            root_arabic="قول",
            segment_count=1_722,
            word_count=1_722,
            verse_count=1_383,
            locations=("(1:1:1:1)",),
        )


def test_a_rare_root_deposits_all_of_its_locations_not_some() -> None:
    with pytest.raises(HollowRootCensusError):
        RootCensusRow(
            root_buckwalter="qyl",
            root_arabic="قيل",
            segment_count=2,
            word_count=2,
            verse_count=2,
            locations=("(7:4:10:1)",),
        )


def test_the_frozen_census_covers_every_side_of_every_competing_pair() -> None:
    frozen = {row.root_buckwalter for row in REDERIVED_ROOT_COUNTS}
    declared = {
        side
        for pair in COMPETING_ROOT_PAIRS
        for side in (pair.waw_root_buckwalter, pair.ya_root_buckwalter)
    }

    assert frozen == declared
    assert len(REDERIVED_ROOT_COUNTS) == len(declared)


def test_the_frozen_census_records_the_numbers_that_arrived() -> None:
    counts = {
        row.root_buckwalter: row.count_under(RootCountingRule.SEGMENTS)
        for row in REDERIVED_ROOT_COUNTS
    }

    assert REDERIVED_SEGMENT_COUNT == 128_219
    assert counts == {
        "xwf": 124,
        "xyf": 0,
        "nwm": 9,
        "nym": 0,
        "hwb": 0,
        "hyb": 0,
        "qwl": 1_722,
        "qyl": 2,
    }


def test_the_two_qyl_occurrences_are_examined_by_their_own_tags() -> None:
    locations = tuple(item.location for item in QYL_EXAMINED_OCCURRENCES)
    qyl = next(row for row in REDERIVED_ROOT_COUNTS if row.root_buckwalter == "qyl")

    assert locations == qyl.locations
    assert len(locations) <= RARE_ROOT_LOCATION_LIMIT
    for occurrence in QYL_EXAMINED_OCCURRENCES:
        assert "ROOT:qyl" in occurrence.features
        assert "LEM:qaAl" not in occurrence.features
        assert occurrence.what_it_does_not_establish.strip()


def test_the_module_does_not_claim_a_root_extractor_or_annotator_truth() -> None:
    assert "ليس في هذه الوحدة مستخرِجُ جذورٍ" in THE_CENSUS_IS_NOT_A_ROOT_EXTRACTOR_NOTE
    assert "لا مُعادةُ الاشتقاق هنا" in ANNOTATOR_AGREEMENT_IS_NOT_TRUTH_NOTE
    assert len(HOLLOW_ROOT_CENSUS_NAMED_RESIDUALS) == 9


def test_the_census_exposes_no_birth_or_verdict_surface() -> None:
    forbidden = ("verdict", "birth", "resolution", "resolved", "authority")
    fields = set(RootCensusRow.__dataclass_fields__)

    assert not any(marker in name for name in fields for marker in forbidden)


def test_bytes_that_do_not_match_the_witness_are_refused(tmp_path: Path) -> None:
    impostor = tmp_path / "morphology-0.4.txt"
    impostor.write_bytes(b"(1:1:1:1)\tbi\tP\tPREFIX|bi+\r\n")

    with pytest.raises(HollowRootCensusError):
        corpus_lines(impostor)


def test_an_absent_corpus_path_is_refused_by_name(tmp_path: Path) -> None:
    with pytest.raises(HollowRootCensusError):
        corpus_lines(tmp_path / "absent.txt")


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

    lines = corpus_lines(path)
    records = [
        record
        for record in (parse_segment_line(line) for line in lines)
        if record is not None
    ]
    roots = tuple(
        side
        for pair in COMPETING_ROOT_PAIRS
        for side in (
            (pair.waw_root_buckwalter, pair.waw_root_arabic),
            (pair.ya_root_buckwalter, pair.ya_root_arabic),
        )
    )

    assert rederive_segment_count(lines) == REDERIVED_SEGMENT_COUNT
    assert census_rows(records, roots) == REDERIVED_ROOT_COUNTS


def test_the_witness_bytes_are_still_not_in_this_tree() -> None:
    repository_root = Path(__file__).resolve().parents[2]
    name = Path(QURANIC_ARABIC_CORPUS_WITNESS.measured_path).name

    assert list(repository_root.rglob(name)) == [], (
        "the corpus bytes appear in this tree; both licences forbid that, and "
        "WITNESS_BYTES_ARE_STILL_NOT_VENDORED_NOTE would then be false"
    )
