"""شواهدُ «لا صامتَ بلا صائتٍ رياضيًّا»: لكلِّ قراءةٍ حكمُها وحدُّها."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from alghanem.arabic import no_consonant_without_a_vowel as module
from alghanem.arabic.no_consonant_without_a_vowel import (
    NO_CONSONANT_WITHOUT_A_VOWEL_NAMED_RESIDUALS,
    THE_CLAIM,
    ClaimReading,
    ClaimVerdict,
    NoConsonantWithoutAVowelError,
    ReadingVerdict,
    SyllableCensus,
    every_frozen_template_has_a_nucleus,
    no_template_opens_without_a_vowel,
    read_the_claim,
    take_syllable_census,
)
from alghanem.import_boundary import ImportBoundaryPolicy, audit_import_boundary


@pytest.fixture(scope="module")
def census() -> SyllableCensus:
    return take_syllable_census()


@pytest.fixture(scope="module")
def verdicts(census: SyllableCensus) -> tuple[ReadingVerdict, ...]:
    return read_the_claim(census)


def test_the_claim_is_stated_before_it_is_divided() -> None:
    assert THE_CLAIM == "لا صامتَ بلا صائتٍ رياضيًّا"


def test_every_reading_is_read_and_none_is_dropped(
    verdicts: tuple[ReadingVerdict, ...],
) -> None:
    assert {verdict.reading for verdict in verdicts} == set(ClaimReading)


def test_the_four_readings_do_not_share_one_verdict(
    verdicts: tuple[ReadingVerdict, ...],
) -> None:
    assert len({verdict.verdict for verdict in verdicts}) == len(ClaimVerdict)


def _verdict_of(
    verdicts: tuple[ReadingVerdict, ...], reading: ClaimReading
) -> ReadingVerdict:
    return next(item for item in verdicts if item.reading is reading)


def test_no_syllable_without_a_nucleus_holds_by_construction(
    verdicts: tuple[ReadingVerdict, ...],
) -> None:
    verdict = _verdict_of(verdicts, ClaimReading.NO_SYLLABLE_WITHOUT_A_NUCLEUS)
    assert verdict.verdict is ClaimVerdict.HELD_BY_CONSTRUCTION


def test_the_first_reading_names_the_corpus_as_no_proof(
    verdicts: tuple[ReadingVerdict, ...],
) -> None:
    verdict = _verdict_of(verdicts, ClaimReading.NO_SYLLABLE_WITHOUT_A_NUCLEUS)
    assert any("لا شهادةُ استقراء" in note for note in verdict.residuals)


def test_the_absolute_reading_is_refuted(
    verdicts: tuple[ReadingVerdict, ...],
) -> None:
    verdict = _verdict_of(verdicts, ClaimReading.NO_CONSONANT_AT_ALL_WITHOUT_A_VOWEL)
    assert verdict.verdict is ClaimVerdict.REFUTED
    assert verdict.witness_count > 0


def test_the_absolute_reading_is_refuted_by_the_algebra_not_only_the_count(
    verdicts: tuple[ReadingVerdict, ...],
) -> None:
    verdict = _verdict_of(verdicts, ClaimReading.NO_CONSONANT_AT_ALL_WITHOUT_A_VOWEL)
    assert any("لو خلا الإيداعُ من إغلاقٍ واحد" in note for note in verdict.residuals)


def test_the_onset_reading_holds_as_a_refusal_not_as_an_affirmation(
    verdicts: tuple[ReadingVerdict, ...],
) -> None:
    verdict = _verdict_of(verdicts, ClaimReading.NO_ONSET_WITHOUT_A_VOWEL)
    assert verdict.verdict is ClaimVerdict.HELD_AS_A_REFUSAL


def test_the_phonetic_reading_is_untestable_and_carries_no_count(
    verdicts: tuple[ReadingVerdict, ...],
) -> None:
    verdict = _verdict_of(
        verdicts,
        ClaimReading.NO_PRONOUNCED_CONSONANT_WITHOUT_A_PRONOUNCED_VOWEL,
    )
    assert verdict.verdict is ClaimVerdict.UNTESTABLE_HERE
    assert verdict.witness_count == 0
    assert "UnicodeIsNotRecordedSound" in verdict.what_decided_it


def test_an_untestable_reading_may_not_carry_a_count() -> None:
    with pytest.raises(NoConsonantWithoutAVowelError, match="لا يُعَدّ"):
        ReadingVerdict(
            reading=ClaimReading.NO_PRONOUNCED_CONSONANT_WITHOUT_A_PRONOUNCED_VOWEL,
            verdict=ClaimVerdict.UNTESTABLE_HERE,
            what_decided_it="مانعٌ مكتوب",
            witness_count=3,
            residuals=("بقيّة",),
        )


def test_a_verdict_without_a_written_reason_is_refused() -> None:
    with pytest.raises(NoConsonantWithoutAVowelError, match="سببٍ مكتوب"):
        ReadingVerdict(
            reading=ClaimReading.NO_SYLLABLE_WITHOUT_A_NUCLEUS,
            verdict=ClaimVerdict.REFUTED,
            what_decided_it="   ",
            witness_count=1,
            residuals=("بقيّة",),
        )


def test_a_verdict_without_a_named_residual_is_refused() -> None:
    with pytest.raises(NoConsonantWithoutAVowelError, match="بلا بقيّةٍ مُسمّاة"):
        ReadingVerdict(
            reading=ClaimReading.NO_SYLLABLE_WITHOUT_A_NUCLEUS,
            verdict=ClaimVerdict.REFUTED,
            what_decided_it="سبب",
            witness_count=1,
            residuals=(),
        )


def test_the_frozen_templates_all_carry_a_nucleus() -> None:
    assert every_frozen_template_has_a_nucleus() is True


def test_the_template_maker_refuses_a_missing_or_doubled_onset() -> None:
    assert no_template_opens_without_a_vowel() is True


def test_the_census_is_taken_from_the_fingerprinted_deposit(
    census: SyllableCensus,
) -> None:
    assert census.deposit_sha256 == (
        "d435d63a4e49ea03a75344b050df01dd99d5bfb77335c807e2d6309f52174341"
    )


def test_no_syllable_in_the_deposit_lacks_a_nucleus(census: SyllableCensus) -> None:
    assert census.syllable_total > 0
    assert census.syllables_without_a_nucleus == 0


def test_the_deposit_does_carry_vowelless_codas(census: SyllableCensus) -> None:
    assert census.coda_consonants > 0


def test_coda_count_agrees_with_the_closed_templates_seen(
    census: SyllableCensus,
) -> None:
    seen = dict(census.templates_seen)
    expected = sum(
        count * (len(template) - template.count("V"))
        for template, count in seen.items()
    ) - sum(seen.values())
    assert census.coda_consonants == expected


def test_unsegmented_words_are_carried_in_the_denominator(
    census: SyllableCensus,
) -> None:
    assert census.unsegmented_words > 0
    assert census.segmented_words + census.unsegmented_words == census.word_total


def test_every_halt_is_named_not_silently_skipped(census: SyllableCensus) -> None:
    assert census.onsetless_halts >= census.unsegmented_words


def test_the_written_surface_shows_sukun_bearing_carriers(
    census: SyllableCensus,
) -> None:
    assert 0 < census.surface_carriers_bearing_a_sukun < census.surface_carriers


def test_a_census_whose_parts_do_not_sum_is_refused(census: SyllableCensus) -> None:
    with pytest.raises(NoConsonantWithoutAVowelError, match="المقامُ لا يُنقَص"):
        replace(census, unsegmented_words=census.unsegmented_words + 1)


def test_a_census_with_more_vowelled_carriers_than_carriers_is_refused(
    census: SyllableCensus,
) -> None:
    with pytest.raises(NoConsonantWithoutAVowelError, match="أكثرُ من الحوامل"):
        replace(census, surface_carriers_bearing_a_vowel=census.surface_carriers + 1)


def test_a_nucleusless_syllable_would_be_raised_not_folded_away(
    census: SyllableCensus,
) -> None:
    with pytest.raises(NoConsonantWithoutAVowelError, match="يُرفَع لا يُطوى"):
        read_the_claim(replace(census, syllables_without_a_nucleus=1))


def test_a_template_without_a_nucleus_would_halt_the_reading(
    census: SyllableCensus, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(module, "every_frozen_template_has_a_nucleus", lambda: False)
    with pytest.raises(NoConsonantWithoutAVowelError, match="قالبٌ في الستّة بلا نواة"):
        read_the_claim(census)


def test_a_permissive_template_maker_would_halt_the_reading(
    census: SyllableCensus, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(module, "no_template_opens_without_a_vowel", lambda: False)
    with pytest.raises(NoConsonantWithoutAVowelError, match="خارجَ المُعلَن"):
        read_the_claim(census)


def test_the_named_residuals_are_all_present() -> None:
    assert len(NO_CONSONANT_WITHOUT_A_VOWEL_NAMED_RESIDUALS) == 5
    assert all(note.strip() for note in NO_CONSONANT_WITHOUT_A_VOWEL_NAMED_RESIDUALS)


def test_the_divided_verdict_residual_is_named() -> None:
    assert any(
        "AnAbsoluteReadingHidesADividedVerdict" in note
        for note in NO_CONSONANT_WITHOUT_A_VOWEL_NAMED_RESIDUALS
    )


def test_this_reading_reaches_no_kernel_module() -> None:
    source = Path(str(module.__file__))
    report = audit_import_boundary(
        (source,),
        ImportBoundaryPolicy(
            policy_id="no-consonant-without-a-vowel-reaches-no-kernel",
            permitted_modules=("alghanem.arabic",),
            forbidden_packages=("alghanem.kernel",),
        ),
    )
    assert not [
        name for name in report.reached_modules if name.startswith("alghanem.kernel")
    ]
