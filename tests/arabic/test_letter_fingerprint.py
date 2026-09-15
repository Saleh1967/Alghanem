"""اختباراتُ بصمة الحرف: الرفضُ مُسمًّى، والتقريبُ مُعلَن، والتفرُّدُ بخطِّ صفره."""

from __future__ import annotations

from pathlib import Path

import pytest

from alghanem.arabic.letter_fingerprint import (
    DIMENSION_PROVENANCE,
    IMPORTED_ROLE_COUNTS,
    ITHLAQ_LETTERS,
    LETTER_VOCABULARY,
    NAMED_RESIDUALS,
    ROOT_COLUMN,
    ROOT_TYPE_COLUMN,
    TRILITERAL_ROOT_TYPE,
    DimensionProvenance,
    ExclusionReason,
    LetterFingerprint,
    LetterFingerprintError,
    LetterPositionCounts,
    PreferredPosition,
    compute_fingerprint_census,
    fold_root,
    read_triliteral_roots,
    round_half_up_percent,
    structural_collision_classes,
    uniform_null_unique_counts,
)


def _write_corpus(tmp_path: Path, rows: tuple[tuple[str, str], ...]) -> Path:
    path = tmp_path / "corpus.csv"
    lines = [f"{ROOT_COLUMN},{ROOT_TYPE_COLUMN}"]
    lines.extend(f"{root},{root_type}" for root, root_type in rows)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def test_the_closed_vocabulary_and_the_imported_tables_agree() -> None:
    assert len(LETTER_VOCABULARY) == 29
    assert set(IMPORTED_ROLE_COUNTS) == set(LETTER_VOCABULARY)
    assert ITHLAQ_LETTERS == frozenset("بفمنلر")


def test_two_of_the_four_dimensions_are_imported_not_measured() -> None:
    """أربعةُ أبعادٍ لا تعني أربعةَ قياسات؛ والفرقُ مُعلَنٌ في البنية."""

    measured = {
        name
        for name, provenance in DIMENSION_PROVENANCE.items()
        if provenance is DimensionProvenance.MEASURED
    }
    assert measured == {"preferred_position", "root_share_percent"}


def test_the_imported_tables_alone_leave_dal_and_qaf_in_one_class() -> None:
    """تصادمُ (د، ق) لازمٌ من الجدولين قبل قراءة أيّ مدوَّنة، لا اكتشافٌ رصديّ."""

    classes = dict(structural_collision_classes())
    assert set("دسغقيء") <= set(classes[(False, 1)])
    assert len(classes) == 8


def test_hamza_forms_fold_before_the_length_condition(tmp_path: Path) -> None:
    corpus = _write_corpus(
        tmp_path,
        (
            ("أكل", TRILITERAL_ROOT_TYPE),
            ("سَأَل", TRILITERAL_ROOT_TYPE),
            ("قرأ", TRILITERAL_ROOT_TYPE),
        ),
    )
    reading = read_triliteral_roots(corpus)
    assert reading.accepted_roots == ("ءكل", "سءل", "قرء")
    assert reading.exclusions == ()


def test_every_excluded_row_is_named_by_its_reason(tmp_path: Path) -> None:
    corpus = _write_corpus(
        tmp_path,
        (
            ("كتب", TRILITERAL_ROOT_TYPE),
            ("دحرج", TRILITERAL_ROOT_TYPE),
            ("زلزل", "رباعي"),
            ("", TRILITERAL_ROOT_TYPE),
            ("abc", TRILITERAL_ROOT_TYPE),
        ),
    )
    reading = read_triliteral_roots(corpus)
    assert reading.accepted_roots == ("كتب",)
    assert reading.row_count == 5
    counts = reading.exclusion_counts
    assert counts[ExclusionReason.LENGTH_NOT_THREE] == 1
    assert counts[ExclusionReason.ROOT_TYPE_NOT_TRILITERAL] == 1
    assert counts[ExclusionReason.EMPTY_ROOT] == 1
    assert counts[ExclusionReason.LETTER_OUT_OF_VOCABULARY] == 1


def test_a_missing_column_is_refused_not_guessed(tmp_path: Path) -> None:
    path = tmp_path / "corpus.csv"
    path.write_text(f"{ROOT_COLUMN}\nكتب\n", encoding="utf-8")
    with pytest.raises(LetterFingerprintError):
        read_triliteral_roots(path)


def test_rounding_is_half_up_not_bankers() -> None:
    """حدُّ ٠٫٥ يصعد دائمًا؛ فلا يتعلّق التصاقُ حرفين بزوجيّة ما قبله."""

    assert round_half_up_percent(1, 200) == 1
    assert round_half_up_percent(5, 200) == 3
    assert round_half_up_percent(0, 200) == 0
    assert round(0.5) == 0
    assert round(2.5) == 2


def test_an_empty_corpus_is_refused_not_divided_by_zero() -> None:
    with pytest.raises(LetterFingerprintError):
        round_half_up_percent(1, 0)
    with pytest.raises(LetterFingerprintError):
        compute_fingerprint_census(())


def test_a_positional_tie_is_declared_not_silently_broken() -> None:
    counts = LetterPositionCounts("ك", 2, 2, 1)
    assert counts.preferred_position is PreferredPosition.TIE
    clear = LetterPositionCounts("ك", 3, 2, 1)
    empty = LetterPositionCounts("ك", 0, 0, 0)
    assert clear.preferred_position is PreferredPosition.P1
    assert empty.preferred_position is PreferredPosition.TIE


def test_the_census_counts_positions_and_shares_as_declared() -> None:
    census = compute_fingerprint_census(("كتب", "كبر", "بكت", "تبك"))
    by_letter = census.by_letter
    assert census.corpus_size == 4
    kaf = next(count for count in census.counts if count.letter == "ك")
    assert (kaf.first, kaf.second, kaf.third) == (2, 1, 1)
    assert kaf.total == 4
    assert by_letter["ك"].root_share_percent == 100
    assert by_letter["ك"].preferred_position is PreferredPosition.P1
    assert by_letter["ج"].root_share_percent == 0


def test_the_share_denominator_is_roots_not_positions() -> None:
    """مجموعُ النصيب يقارب ٣٠٠٪ لا ١٠٠٪؛ وهو المُسجَّل في المُخلَّف المُسمّى."""

    census = compute_fingerprint_census(("كتب", "كبر", "بكت", "تبك"))
    total = sum(count.total for count in census.counts)
    assert total == 3 * census.corpus_size
    assert "ROOT_SHARE_IS_NOT_A_DENSITY" in NAMED_RESIDUALS


def test_imported_dimensions_cannot_be_written_by_hand() -> None:
    with pytest.raises(LetterFingerprintError):
        LetterFingerprint("د", PreferredPosition.P1, 10, True, 1)
    with pytest.raises(LetterFingerprintError):
        LetterFingerprint("د", PreferredPosition.P1, 10, False, 4)
    with pytest.raises(LetterFingerprintError):
        LetterFingerprint("d", PreferredPosition.P1, 10, False, 1)


def test_collisions_are_named_and_forced_ones_are_separated() -> None:
    census = compute_fingerprint_census(("كتب", "كبر", "بكت", "تبك"))
    collisions = dict(census.collisions)
    forced = dict(census.structurally_forced_collisions)
    assert collisions
    assert all(len(letters) > 1 for letters in collisions.values())
    assert set(forced) <= set(collisions)
    for key, letters in forced.items():
        classes = {census.by_letter[letter].imported_class for letter in letters}
        assert len(classes) == 1
        assert key in collisions


def test_out_of_vocabulary_letters_are_refused_by_the_census() -> None:
    with pytest.raises(LetterFingerprintError):
        compute_fingerprint_census(("abc",))
    with pytest.raises(LetterFingerprintError):
        compute_fingerprint_census(("كتبر",))


def test_the_null_baseline_is_deterministic_and_near_the_reported_number() -> None:
    """تفرُّدٌ عالٍ بلا خطِّ صفرٍ نصفُ قياس؛ والخطُّ هنا حتميٌّ يُعاد."""

    first = uniform_null_unique_counts(corpus_size=999, trials=5, seed=17)
    second = uniform_null_unique_counts(corpus_size=999, trials=5, seed=17)
    assert first == second
    assert all(1 <= value <= len(LETTER_VOCABULARY) for value in first)
    assert max(first) >= 20


def test_the_null_baseline_refuses_non_positive_arguments() -> None:
    with pytest.raises(LetterFingerprintError):
        uniform_null_unique_counts(corpus_size=0, trials=1, seed=1)
    with pytest.raises(LetterFingerprintError):
        uniform_null_unique_counts(corpus_size=10, trials=0, seed=1)


def test_fold_root_refuses_a_non_string() -> None:
    with pytest.raises(LetterFingerprintError):
        fold_root(3)  # type: ignore[arg-type]
    assert fold_root("  كَتَبَ ") == "كتب"
