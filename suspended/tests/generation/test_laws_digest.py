"""دستورُ الإنتاج مُجمَّدٌ ببصمته؛ وتعديلُ نصِّ قانونٍ يُسقِط هذا الاختبار.

ومراجعةُ `G0.GEN-0.SPEC-H` **مجموعةٌ ثانية** لا تعديلٌ للأولى: تبقى بصمةُ
`G0.GEN-0` كما جُمِّدت، وتُضاف مجموعةٌ مستقلّةٌ بمُعرِّفها وبصمتها تضمّ الأصلَ
وثلاثةَ قوانينَ جديدةٍ بأسمائها.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

import pytest

from alghanem.canonical_content import canonical_bytes, canonical_digest
from alghanem.generation.authority_gaps import (
    GENERATION_AUTHORITY_GAPS,
    NO_INDEPENDENT_ANCHOR_TO_SYNTACTIC_FUNCTION_AUTHORITY,
    NO_VERIFIED_LEXICAL_ATTESTATION,
)
from alghanem.generation.laws import (
    GENERATION_LAW_SET_DIGEST,
    GENERATION_LAW_SET_ID,
    GENERATION_LAWS,
    GENERATION_SPEC_H_LAW_SET_DIGEST,
    GENERATION_SPEC_H_LAW_SET_ID,
    GENERATION_SPEC_H_LAWS,
)

FROZEN_GENERATION_LAW_SET_DIGEST = (
    "eae41f962d559f69e6909ae7cd9f667e8ce541bb0f49600752d2613cb007c16c"
)

FROZEN_SPEC_H_LAW_SET_DIGEST = (
    "d69e662ff1ccc729262564c5ea5703f8e268bdd79271c41a5649e76170703773"
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

SPEC_H_ADDED_LAW_NAMES = (
    "ConformanceIsNotLicensing",
    "ContractMustBindClassNotFactory",
    "LexicalChoiceRefIsAClaimUntilTheReadout",
)


def test_the_law_set_names_exactly_the_frozen_laws() -> None:
    assert tuple(sorted(GENERATION_LAWS)) == tuple(sorted(EXPECTED_LAW_NAMES))


def test_every_law_carries_a_non_blank_text() -> None:
    assert all(text.strip() for text in GENERATION_SPEC_H_LAWS.values())


def test_the_law_set_digest_is_derived_from_its_own_text() -> None:
    recomputed = canonical_digest(
        canonical_bytes(
            {"law_set_id": GENERATION_LAW_SET_ID, "laws": dict(GENERATION_LAWS)}
        )
    )
    assert recomputed == GENERATION_LAW_SET_DIGEST


def test_the_law_set_digest_is_frozen() -> None:
    assert GENERATION_LAW_SET_DIGEST == FROZEN_GENERATION_LAW_SET_DIGEST


def test_the_revision_is_a_second_law_set_not_an_edit_of_the_first() -> None:
    assert GENERATION_SPEC_H_LAW_SET_ID == "alghanem.generation.laws.G0.GEN-0.SPEC-H"
    assert GENERATION_SPEC_H_LAW_SET_ID != GENERATION_LAW_SET_ID
    assert GENERATION_SPEC_H_LAW_SET_DIGEST != GENERATION_LAW_SET_DIGEST
    assert GENERATION_SPEC_H_LAW_SET_DIGEST == FROZEN_SPEC_H_LAW_SET_DIGEST


def test_the_revision_keeps_every_original_law_verbatim() -> None:
    for name, text in GENERATION_LAWS.items():
        assert GENERATION_SPEC_H_LAWS[name] == text
    assert tuple(sorted(GENERATION_SPEC_H_LAWS)) == tuple(
        sorted(EXPECTED_LAW_NAMES + SPEC_H_ADDED_LAW_NAMES)
    )


def test_the_revision_digest_is_derived_from_its_own_text() -> None:
    recomputed = canonical_digest(
        canonical_bytes(
            {
                "law_set_id": GENERATION_SPEC_H_LAW_SET_ID,
                "laws": dict(GENERATION_SPEC_H_LAWS),
            }
        )
    )
    assert recomputed == GENERATION_SPEC_H_LAW_SET_DIGEST


def test_authority_gaps_are_named_outside_both_law_sets() -> None:
    for gap in (
        NO_INDEPENDENT_ANCHOR_TO_SYNTACTIC_FUNCTION_AUTHORITY,
        NO_VERIFIED_LEXICAL_ATTESTATION,
    ):
        assert gap.gap_id in GENERATION_AUTHORITY_GAPS
        assert gap.gap_id not in GENERATION_LAWS
        assert gap.gap_id not in GENERATION_SPEC_H_LAWS
        assert gap.discharge_condition.strip()


def test_neither_law_set_is_writable() -> None:
    with pytest.raises(TypeError):
        GENERATION_LAWS["NewLaw"] = "قانونٌ يُضاف بعد التجميد"  # type: ignore[index]
    with pytest.raises(TypeError):
        GENERATION_SPEC_H_LAWS["NewLaw"] = "قانونٌ يُضاف"  # type: ignore[index]
