"""فجواتُ السلطة المعماريّة: نوعٌ مستقلٌّ عن البقايا المرصودة، وكلُّ فجوةٍ بشرط رفعها.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

from dataclasses import replace

import pytest

from alghanem.generation.authority_gaps import (
    GENERATION_AUTHORITY_GAPS,
    NO_INDEPENDENT_ANCHOR_TO_SYNTACTIC_FUNCTION_AUTHORITY,
    NO_VERIFIED_LEXICAL_ATTESTATION,
    GenerationAuthorityGap,
    GenerationAuthorityGapError,
)
from alghanem.generation.trace import GenerationResidual


def test_every_frozen_gap_names_its_claim_authority_and_discharge() -> None:
    for gap in GENERATION_AUTHORITY_GAPS.values():
        assert gap.claim.strip()
        assert gap.missing_authority.strip()
        assert gap.discharge_condition.strip()


def test_a_gap_is_not_a_residual() -> None:
    assert not issubclass(GenerationAuthorityGap, GenerationResidual)
    assert not hasattr(NO_VERIFIED_LEXICAL_ATTESTATION, "kind")
    assert not hasattr(NO_VERIFIED_LEXICAL_ATTESTATION, "stage")


def test_a_gap_without_a_discharge_condition_is_refused() -> None:
    with pytest.raises(GenerationAuthorityGapError):
        replace(NO_VERIFIED_LEXICAL_ATTESTATION, discharge_condition="   ")


def test_a_gap_is_attributed_to_the_stage_that_lacked_the_authority() -> None:
    with pytest.raises(GenerationAuthorityGapError):
        replace(NO_VERIFIED_LEXICAL_ATTESTATION, gap_id="RES.OTHER.Something")


def test_the_two_frozen_gaps_are_registered_by_their_identifiers() -> None:
    assert set(GENERATION_AUTHORITY_GAPS) == {
        NO_INDEPENDENT_ANCHOR_TO_SYNTACTIC_FUNCTION_AUTHORITY.gap_id,
        NO_VERIFIED_LEXICAL_ATTESTATION.gap_id,
    }
    with pytest.raises(TypeError):
        GENERATION_AUTHORITY_GAPS["RES.GEN0.Other"] = (  # type: ignore[index]
            NO_VERIFIED_LEXICAL_ATTESTATION
        )
