"""شواهدُ استخراج مخارج سيبويه وصفاته من بايتات «الكتاب» المختومة.

تُتخطّى شواهدُ البايتات إن لم تكن حاضرةً مختومة، وتسقط إن حضرت وخالفت؛ أمّا
شواهدُ البنية فتجري في الحالين.
"""

from __future__ import annotations

import pytest

from alghanem.arabic.letter_fingerprint import LETTER_VOCABULARY
from alghanem.arabic.sibawayh_phonetics import (
    SIBAWAYH_PHONETICS_NAMED_RESIDUALS,
    THE_CHAPTER_START,
    THE_FEATURE_SPANS,
    THE_LETTER_NAMES,
    THE_SOURCE,
    FeatureRule,
    SibawayhPhoneticsError,
    chapter_text,
    reading,
    source_is_resolvable,
)

_ABSENT_SOURCE_REASON = (
    f"«{THE_SOURCE.title}» غيرُ حاضرةٍ مختومة؛ تُحضَر عبر "
    f"{THE_SOURCE.path_environment_variable}. والبايتاتُ الحاضرةُ المخالفةُ "
    "لا تُتخطّى بل تسقط."
)


def test_the_letter_names_map_onto_the_whole_vocabulary_one_to_one() -> None:
    assert sorted(THE_LETTER_NAMES.values()) == sorted(LETTER_VOCABULARY)
    assert len(set(THE_LETTER_NAMES.values())) == len(THE_LETTER_NAMES) == 29


def test_every_feature_has_two_anchors_and_a_declared_rule() -> None:
    names = [span.name for span in THE_FEATURE_SPANS]
    assert len(names) == len(set(names))
    for span in THE_FEATURE_SPANS:
        assert span.start.strip() and span.end.strip()
        if span.rule is FeatureRule.COMPLEMENT:
            assert span.complement_of in names


def test_the_named_residuals_are_published() -> None:
    assert "THE_LAM_MAKHRAJ_CLAUSE_IS_ABSENT_FROM_THE_DEPOSITED_TEXT" in (
        SIBAWAYH_PHONETICS_NAMED_RESIDUALS
    )
    assert "A_DEFERRED_RECORDING_IS_NOT_A_SUSPENDED_THEORY" in (
        SIBAWAYH_PHONETICS_NAMED_RESIDUALS
    )


def test_an_absent_source_refuses_reading_instead_of_guessing() -> None:
    if source_is_resolvable():
        pytest.skip("المصدرُ حاضرٌ مختوم؛ هذا شاهدُ الغياب وحدَه")
    with pytest.raises(SibawayhPhoneticsError):
        chapter_text()


@pytest.mark.skipif(not source_is_resolvable(), reason=_ABSENT_SOURCE_REASON)
def test_the_chapter_is_found_once_between_its_anchors() -> None:
    text = chapter_text()
    assert text.startswith(THE_CHAPTER_START)
    assert "ستة عشر مخرجا" in text


@pytest.mark.skipif(not source_is_resolvable(), reason=_ABSENT_SOURCE_REASON)
def test_voicing_partitions_the_vocabulary_and_matches_the_stated_counts() -> None:
    found = reading()
    assert found.voicing_is_a_partition
    assert len(found.features["المجهورة"]) == 19
    assert len(found.features["المهموسة"]) == 10


@pytest.mark.skipif(not source_is_resolvable(), reason=_ABSENT_SOURCE_REASON)
def test_every_makhraj_cell_is_separated_by_its_letters_signatures() -> None:
    found = reading()
    assert found.unseparated_cells == ()
    assert all(found.signature(letter) for letter in LETTER_VOCABULARY)


@pytest.mark.skipif(not source_is_resolvable(), reason=_ABSENT_SOURCE_REASON)
def test_the_stated_sixteen_and_the_derived_count_are_shown_apart() -> None:
    """البابُ يُعلن ستّةَ عشر، والمذكورُ صراحةً خمسةَ عشر؛ والفرقُ اللامُ وحدَها."""

    found = reading()
    assert found.khayshum_is_stated
    assert found.derived_makharij_count == 15
    assert found.letters_without_a_makhraj == ("ل",)


@pytest.mark.skipif(not source_is_resolvable(), reason=_ABSENT_SOURCE_REASON)
def test_the_tradition_differs_from_a_modern_description_where_it_is_named() -> None:
    """الطاءُ والقافُ والهمزةُ مجهورةٌ في الباب، والضادُ رخوةٌ مطبقة."""

    found = reading()
    for letter in ("ط", "ق", "ء"):
        assert letter in found.features["المجهورة"]
    assert {"الرخوة", "المطبقة"} <= found.signature("ض")
