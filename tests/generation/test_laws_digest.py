"""دستورُ الإنتاج مُجمَّدٌ ببصمته؛ وتعديلُ نصِّ قانونٍ يُسقِط هذا الاختبار.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

import pytest

from alghanem.canonical_content import canonical_bytes, canonical_digest
from alghanem.generation.laws import (
    GENERATION_LAW_SET_DIGEST,
    GENERATION_LAW_SET_ID,
    GENERATION_LAWS,
)

FROZEN_GENERATION_LAW_SET_DIGEST = (
    "eae41f962d559f69e6909ae7cd9f667e8ce541bb0f49600752d2613cb007c16c"
)

EXPECTED_LAW_NAMES = (
    "AnUnrealizedLayerIsAWithheldStageNotANull",
    "AnalysisIsNotInvertedGeneration",
    "APositionIsNotASemanticRole",
    "CallerDoesNotOwnGenerationRank",
    "GenerationDoesNotInventIntent",
    "NoCertifiedGenerationWithoutRoundTrip",
    "NoCompositionWithoutRelation",
    "NoGenerationAuthorityBeyondItsSource",
    "NoInflectionWithoutLicensedSlot",
    "NoLexemeOutsideAFrozenLexicalSource",
    "NoSurfaceWithoutSourceAnchor",
    "NoWordFormWithoutMorphologicalTrace",
    "OrthographyNeedNotClaimPhonologicalDerivation",
    "ResidualsAreObservedNotAuthored",
)


def test_the_law_set_names_exactly_the_frozen_laws() -> None:
    assert tuple(sorted(GENERATION_LAWS)) == tuple(sorted(EXPECTED_LAW_NAMES))


def test_every_law_carries_a_non_blank_text() -> None:
    assert all(text.strip() for text in GENERATION_LAWS.values())


def test_the_law_set_digest_is_derived_from_its_own_text() -> None:
    recomputed = canonical_digest(
        canonical_bytes(
            {"law_set_id": GENERATION_LAW_SET_ID, "laws": dict(GENERATION_LAWS)}
        )
    )
    assert recomputed == GENERATION_LAW_SET_DIGEST


def test_the_law_set_digest_is_frozen() -> None:
    assert GENERATION_LAW_SET_DIGEST == FROZEN_GENERATION_LAW_SET_DIGEST


def test_the_law_set_is_not_writable() -> None:
    with pytest.raises(TypeError):
        GENERATION_LAWS["NewLaw"] = "قانونٌ يُضاف بعد التجميد"  # type: ignore[index]
