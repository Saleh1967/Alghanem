"""اختباراتُ مقابلة النسختين: كلُّ رقمٍ مُجمَّدٍ يُعاد اشتقاقُه من البايتات."""

from __future__ import annotations

import unicodedata

import pytest

from alghanem.arabic.quran_mirror_collation import (
    AYAH_ROWS,
    THE_COLLATION_AT_MEASUREMENT,
    THE_DEPOSITS,
    THE_WAQF_RANGE,
    CollationLadder,
    FoldRung,
    GateStanding,
    MirrorCollationError,
    ResidueRow,
    ayah_rows_of,
    collation_ladder,
    deposit_reading,
    gate_readings,
    residue_rows,
    the_declared_rungs,
)
from alghanem.arabic.tajsir_bridge import fold_map

_OURS = "quran-simple-enhanced.txt"
_REFERENCE = "globalquran-simple-enhanced.txt"


def test_the_frozen_collation_is_what_the_sealed_bytes_give() -> None:
    assert collation_ladder() == THE_COLLATION_AT_MEASUREMENT


def test_both_deposits_match_their_declared_length_and_fingerprint() -> None:
    for name, (length, sha) in THE_DEPOSITS.items():
        reading = deposit_reading(name)
        assert (reading.byte_length, reading.sha256) == (length, sha)


def test_a_file_that_fails_its_seal_is_refused_rather_than_skipped(
    tmp_path: object,
) -> None:
    with pytest.raises(MirrorCollationError):
        deposit_reading("a-name-that-was-never-declared.txt")


def test_the_row_count_agrees_only_after_naming_the_dropped_lines() -> None:
    """المرجعُ 6,248 سطرًا؛ والموافقةُ على 6,236 تقع بعد إسقاطٍ يُكتَب."""

    ours = deposit_reading(_OURS)
    reference = deposit_reading(_REFERENCE)
    assert ours.lines == AYAH_ROWS
    assert ours.rows_beyond_the_ayahs == 0
    assert reference.lines == 6_248
    assert reference.rows_beyond_the_ayahs == 12
    assert len(ayah_rows_of(_REFERENCE)) == AYAH_ROWS


def test_the_waqf_counter_is_not_blind_and_its_zero_is_a_property_of_one_text() -> None:
    """صفرُ الوقف عندنا صفةُ النقل؛ والعدّادُ يُثبِت بصرَه بالمُودَع الثاني."""

    assert deposit_reading(_OURS).waqf_marks == 0
    assert deposit_reading(_REFERENCE).waqf_marks == 4_578
    assert 0x06DA in THE_WAQF_RANGE
    assert ord("ب") not in THE_WAQF_RANGE


def test_the_deferral_is_replaced_by_a_count_that_sums() -> None:
    ladder = THE_COLLATION_AT_MEASUREMENT
    assert ladder.identical_as_deposited == 1_864
    assert ladder.differing_as_deposited == 4_372
    assert ladder.identical_as_deposited + ladder.differing_as_deposited == AYAH_ROWS
    assert ladder.rungs[-1].still_differing == 111
    assert ladder.basmala_prefixed_rows + ladder.unexplained_rows == 111


def test_a_ladder_whose_explanation_does_not_sum_is_refused() -> None:
    with pytest.raises(MirrorCollationError):
        CollationLadder(
            identical_as_deposited=AYAH_ROWS - 10,
            differing_as_deposited=10,
            rungs=(FoldRung(name="رتبة", still_differing=10, removed=0),),
            basmala_prefixed_rows=1,
            residue=(),
        )


def test_a_census_that_loses_rows_is_refused() -> None:
    with pytest.raises(MirrorCollationError):
        CollationLadder(
            identical_as_deposited=1,
            differing_as_deposited=1,
            rungs=(FoldRung(name="رتبة", still_differing=0, removed=1),),
            basmala_prefixed_rows=0,
            residue=(),
        )


def test_a_rung_that_explains_nothing_is_emitted_rather_than_dropped() -> None:
    """صفرُ رتبةٍ مقروءٌ: `<sel>` أربعةُ آلافٍ ومئتان وسبعةٌ وثمانون ولا تُزيل صفًّا."""

    ladder = collation_ladder()
    barren = [rung for rung in ladder.rungs if rung.explains_nothing]
    assert [rung.name for rung in barren] == [
        "علامةُ ترتيب البايتات",
        "وسمُ الناشر <sel>",
    ]
    assert deposit_reading(_OURS).publisher_tags == 4_287
    assert len(ladder.rungs) == len(the_declared_rungs())


def test_the_rungs_remove_what_they_say_they_remove() -> None:
    ladder = collation_ladder()
    total = sum(rung.removed for rung in ladder.rungs)
    assert ladder.differing_as_deposited - total == ladder.rungs[-1].still_differing


def test_the_agreed_fold_is_the_one_used_and_it_moves_three_rows() -> None:
    """الطيُّ مقروءٌ من الجسر المتّفق عليه، وثمنُه ههنا ثلاثةُ صفوفٍ مقيسة."""

    fold = [rung for rung in collation_ladder().rungs if "الهمزة" in rung.name]
    assert len(fold) == 1
    assert fold[0].removed == 3
    assert fold_map()["أ"] == "ا"


def test_the_residue_is_one_named_row_and_it_is_not_rounded_away() -> None:
    """البقيّةُ صفٌّ واحدٌ: قاعدةُ المرجع نزعت بسملةً هي من متن الآية."""

    residue = residue_rows()
    assert len(residue) == 1
    row = residue[0]
    assert row.row_number == 3_189
    assert row.ours.startswith(row.reference)
    bare = "".join(
        ch for ch in row.ours[len(row.reference) :] if unicodedata.category(ch) != "Mn"
    )
    assert bare.strip() == "بسم الله الرحمن الرحيم"


def test_an_identical_row_is_not_recorded_as_a_residue() -> None:
    with pytest.raises(MirrorCollationError):
        ResidueRow(row_number=1, ours="نصّ", reference="نصّ")
    with pytest.raises(MirrorCollationError):
        ResidueRow(row_number=0, ours="أ", reference="ب")


def test_not_one_submitted_gate_is_read_exactly_as_it_was_submitted() -> None:
    gates = gate_readings()
    assert len(gates) == 4
    assert [gate.is_read_as_submitted for gate in gates] == [False] * 4
    assert {gate.standing for gate in gates} == {
        GateStanding.REFUSED_FOR_ABSENT_REFERENCE_BYTES,
        GateStanding.REDERIVED_WITH_A_NAMED_CONDITION,
        GateStanding.REPLACED_BY_A_NAMED_COUNT,
        GateStanding.SUSPENDED_FOR_ABSENT_MARKS,
    }
    for gate in gates:
        assert gate.because.strip()


def test_the_waqf_gate_is_suspended_rather_than_passed() -> None:
    """صفرٌ يوافق صفرًا ليس موافقةً؛ فالبوّابةُ تُعلَّق باسم مادّتها."""

    waqf = [gate for gate in gate_readings() if "الوقف" in gate.gate]
    assert len(waqf) == 1
    assert waqf[0].standing is GateStanding.SUSPENDED_FOR_ABSENT_MARKS
