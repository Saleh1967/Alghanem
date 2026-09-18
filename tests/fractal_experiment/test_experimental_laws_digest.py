"""بصمةُ مجموعة قوانين `G0.FGEN-EX-0`: محتوًى مُجمَّدٌ مستقلٌّ عن قوانين النواة.

تسجيلٌ لا سلطة: لا ترخيصَ، ولا رتبةَ دائمة، ولا حكمَ كفاية.
"""

from __future__ import annotations

from alghanem.canonical_content import canonical_bytes, canonical_digest
from alghanem.fractal_experiment.authority_gaps import EXPERIMENTAL_AUTHORITY_GAPS
from alghanem.fractal_experiment.laws import (
    FRACTAL_EXPERIMENT_LAW_SET_DIGEST,
    FRACTAL_EXPERIMENT_LAW_SET_ID,
    FRACTAL_EXPERIMENT_LAWS,
)
from alghanem.fractal_generation.authority_gaps import FRACTAL_AUTHORITY_GAPS
from alghanem.fractal_generation.laws import FRACTAL_GENERATION_LAW_SET_DIGEST

_EXPERIMENT_LAW_SET_DIGEST = (
    "11748f1fd63bfbfed04ecbdeeec44a5f56fabfb546c98ae5a271daaf6788e7ff"
)


def test_the_experimental_law_set_has_its_own_identifier() -> None:
    assert (
        FRACTAL_EXPERIMENT_LAW_SET_ID == "alghanem.fractal_experiment.laws.G0.FGEN-EX-0"
    )


def test_the_experimental_law_set_digest_is_frozen_content() -> None:
    assert FRACTAL_EXPERIMENT_LAW_SET_DIGEST == _EXPERIMENT_LAW_SET_DIGEST


def test_the_digest_is_recomputable_from_the_law_texts() -> None:
    assert FRACTAL_EXPERIMENT_LAW_SET_DIGEST == canonical_digest(
        canonical_bytes(
            {
                "law_set_id": FRACTAL_EXPERIMENT_LAW_SET_ID,
                "laws": dict(FRACTAL_EXPERIMENT_LAWS),
            }
        )
    )


def test_every_named_law_carries_a_text() -> None:
    assert len(FRACTAL_EXPERIMENT_LAWS) == 14
    for name, text in FRACTAL_EXPERIMENT_LAWS.items():
        assert name and text.strip()


def test_the_experimental_law_set_is_not_the_core_law_set() -> None:
    assert FRACTAL_EXPERIMENT_LAW_SET_DIGEST != FRACTAL_GENERATION_LAW_SET_DIGEST


def test_the_experimental_gaps_have_their_own_prefix() -> None:
    for gap_id in EXPERIMENTAL_AUTHORITY_GAPS:
        assert gap_id.startswith("RES.FGENEX0.")
    for gap_id in FRACTAL_AUTHORITY_GAPS:
        assert gap_id.startswith("RES.FGEN0.")
    assert not set(EXPERIMENTAL_AUTHORITY_GAPS) & set(FRACTAL_AUTHORITY_GAPS)
