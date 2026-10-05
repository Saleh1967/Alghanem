"""بصمةُ مجموعة قوانين `FGEN-0`: محتوًى مُجمَّدٌ مستقلٌّ عن مجموعتَي `GEN-0`.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

from alghanem.canonical_content import canonical_bytes, canonical_digest
from alghanem.fractal_generation.laws import (
    FRACTAL_GENERATION_LAW_SET_DIGEST,
    FRACTAL_GENERATION_LAW_SET_ID,
    FRACTAL_GENERATION_LAWS,
)
from alghanem.generation.laws import (
    GENERATION_LAW_SET_DIGEST,
    GENERATION_SPEC_H_LAW_SET_DIGEST,
)

_FRACTAL_LAW_SET_DIGEST = (
    "2bbf7a4136ba8bf7f75bcd701c79ee405cf4db867b531666ecc521768d126f40"
)

_GENERATION_LAW_SET_DIGEST = (
    "eae41f962d559f69e6909ae7cd9f667e8ce541bb0f49600752d2613cb007c16c"
)

_GENERATION_SPEC_H_LAW_SET_DIGEST = (
    "d69e662ff1ccc729262564c5ea5703f8e268bdd79271c41a5649e76170703773"
)


def test_the_fractal_law_set_has_its_own_identifier() -> None:
    assert FRACTAL_GENERATION_LAW_SET_ID == "alghanem.fractal_generation.laws.G0.FGEN-0"


def test_the_fractal_law_set_digest_is_frozen_content() -> None:
    assert FRACTAL_GENERATION_LAW_SET_DIGEST == _FRACTAL_LAW_SET_DIGEST


def test_the_digest_is_recomputable_from_the_law_texts() -> None:
    assert FRACTAL_GENERATION_LAW_SET_DIGEST == canonical_digest(
        canonical_bytes(
            {
                "law_set_id": FRACTAL_GENERATION_LAW_SET_ID,
                "laws": dict(FRACTAL_GENERATION_LAWS),
            }
        )
    )


def test_every_named_law_carries_a_text() -> None:
    assert len(FRACTAL_GENERATION_LAWS) == 15
    for name, text in FRACTAL_GENERATION_LAWS.items():
        assert name and text.strip()


def test_the_law_set_is_not_the_generation_law_set() -> None:
    assert FRACTAL_GENERATION_LAW_SET_DIGEST != GENERATION_LAW_SET_DIGEST
    assert FRACTAL_GENERATION_LAW_SET_DIGEST != GENERATION_SPEC_H_LAW_SET_DIGEST


def test_the_historical_generation_digests_are_untouched() -> None:
    assert GENERATION_LAW_SET_DIGEST == _GENERATION_LAW_SET_DIGEST
    assert GENERATION_SPEC_H_LAW_SET_DIGEST == _GENERATION_SPEC_H_LAW_SET_DIGEST


def test_the_containment_law_is_declared_not_proven() -> None:
    text = FRACTAL_GENERATION_LAWS["LinearGenerationIsContainedInFractalGeneration"]
    assert "قانونٌ معماريٌّ مُعلَنٌ" in text
