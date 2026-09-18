"""دستورُ الإنتاج مُجمَّدٌ ببصمته؛ وتعديلُ نصِّ قانونٍ يُسقِط هذا الاختبار.

وبصمةُ `G0.GEN-0.SPEC` كانت `eae41f96…`؛ ثمّ أُعلنت مراجعةُ `G0.GEN-0.SPEC-H`
فأُضيفت ثلاثةُ قوانينَ بأسمائها ولم يُحذَف نصٌّ ولا بُدِّل، فصارت البصمةُ أدناه.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

import pytest

from alghanem.canonical_content import canonical_bytes, canonical_digest
from alghanem.generation.laws import (
    GENERATION_ARCHITECTURAL_RESIDUALS,
    GENERATION_LAW_SET_DIGEST,
    GENERATION_LAW_SET_ID,
    GENERATION_LAWS,
    NO_INDEPENDENT_ANCHOR_TO_SYNTACTIC_FUNCTION_AUTHORITY_ID,
)

SPEC_GENERATION_LAW_SET_DIGEST = (
    "eae41f962d559f69e6909ae7cd9f667e8ce541bb0f49600752d2613cb007c16c"
)

FROZEN_GENERATION_LAW_SET_DIGEST = (
    "6065bbd404c4b7e2587dc1ba7fb955cbdb183bf11ebc3f1db8ea889e839b0a67"
)

EXPECTED_LAW_NAMES = (
    "AnUnrealizedLayerIsAWithheldStageNotANull",
    "AnalysisIsNotInvertedGeneration",
    "APositionIsNotASemanticRole",
    "CallerDoesNotOwnGenerationRank",
    "ConformanceIsNotLicensing",
    "ContractMustBindClassNotFactory",
    "GenerationDoesNotInventIntent",
    "LexicalChoiceRefIsAClaimUntilTheReadout",
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


def test_the_spec_h_revision_moved_the_digest_by_addition_alone() -> None:
    assert GENERATION_LAW_SET_DIGEST != SPEC_GENERATION_LAW_SET_DIGEST
    added = {
        "ContractMustBindClassNotFactory",
        "ConformanceIsNotLicensing",
        "LexicalChoiceRefIsAClaimUntilTheReadout",
    }
    assert added <= set(GENERATION_LAWS)
    assert len(GENERATION_LAWS) == 14 + len(added)


def test_the_architectural_residual_is_named_outside_the_law_set() -> None:
    assert NO_INDEPENDENT_ANCHOR_TO_SYNTACTIC_FUNCTION_AUTHORITY_ID == (
        "RES.GEN0.NoIndependentAnchorToSyntacticFunctionAuthority"
    )
    assert GENERATION_ARCHITECTURAL_RESIDUALS[
        NO_INDEPENDENT_ANCHOR_TO_SYNTACTIC_FUNCTION_AUTHORITY_ID
    ].strip()
    assert NO_INDEPENDENT_ANCHOR_TO_SYNTACTIC_FUNCTION_AUTHORITY_ID not in (
        GENERATION_LAWS
    )
    with pytest.raises(TypeError):
        GENERATION_ARCHITECTURAL_RESIDUALS["RES.GEN0.Other"] = "بقيّةٌ تُضاف"  # type: ignore[index]


def test_the_law_set_is_not_writable() -> None:
    with pytest.raises(TypeError):
        GENERATION_LAWS["NewLaw"] = "قانونٌ يُضاف بعد التجميد"  # type: ignore[index]
