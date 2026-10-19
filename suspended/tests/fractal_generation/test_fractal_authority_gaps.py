"""فجواتُ السلطة: مُجمَّدةٌ بأسمائها، ومفصولةٌ عن البقايا، ومرحليّةٌ لا أبديّة.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

import pytest

from alghanem.fractal_generation import (
    FRACTAL_AUTHORITY_GAPS,
    NO_ARABIC_SPECIALIZATION_AUTHORITY,
    NO_PATTERN_PROOF_WITHOUT_READOUT,
    NO_SCALE_NECESSITY_AUTHORITY,
    NO_SEMANTIC_AUTHORITY_IN_FORMAL_GENERATION,
    FractalAuthorityGap,
    FractalAuthorityGapError,
    FractalResidual,
)


def test_the_frozen_gaps_of_this_stage_are_named() -> None:
    assert set(FRACTAL_AUTHORITY_GAPS) == {
        "RES.FGEN0.NoScaleNecessityAuthority",
        "RES.FGEN0.NoPatternProofWithoutReadout",
        "RES.FGEN0.NoSemanticAuthorityInFormalGeneration",
        "RES.FGEN0.NoArabicSpecializationAuthority",
    }
    assert FRACTAL_AUTHORITY_GAPS["RES.FGEN0.NoScaleNecessityAuthority"] is (
        NO_SCALE_NECESSITY_AUTHORITY
    )


def test_every_gap_names_its_claim_its_absence_and_its_discharge() -> None:
    for gap in (
        NO_SCALE_NECESSITY_AUTHORITY,
        NO_PATTERN_PROOF_WITHOUT_READOUT,
        NO_SEMANTIC_AUTHORITY_IN_FORMAL_GENERATION,
        NO_ARABIC_SPECIALIZATION_AUTHORITY,
    ):
        assert gap.claim.strip()
        assert gap.missing_authority.strip()
        assert gap.discharge_condition.strip()


def test_a_gap_of_this_stage_is_identified_as_such() -> None:
    with pytest.raises(FractalAuthorityGapError):
        FractalAuthorityGap(
            gap_id="RES.OTHER.Something",
            claim="دعوى",
            missing_authority="سلطةٌ غائبة",
            discharge_condition="شرط",
        )


def test_a_gap_refuses_to_be_written_without_a_discharge_condition() -> None:
    with pytest.raises(FractalAuthorityGapError):
        FractalAuthorityGap(
            gap_id="RES.FGEN0.Nameless",
            claim="دعوى",
            missing_authority="سلطةٌ غائبة",
            discharge_condition="   ",
        )


def test_an_architectural_gap_is_not_a_runtime_residual() -> None:
    assert not isinstance(NO_SCALE_NECESSITY_AUTHORITY, FractalResidual)
    assert not hasattr(NO_SCALE_NECESSITY_AUTHORITY, "kind")
    assert not hasattr(NO_SCALE_NECESSITY_AUTHORITY, "blocking")


def test_the_gap_table_is_read_only() -> None:
    with pytest.raises(TypeError):
        FRACTAL_AUTHORITY_GAPS["RES.FGEN0.New"] = (  # type: ignore[index]
            NO_SCALE_NECESSITY_AUTHORITY
        )
