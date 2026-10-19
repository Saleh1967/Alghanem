"""اختبارُ تجميدِ صور الجذر الأجوف قبل قياسها: بصمةٌ تُعاد، وحارسٌ يُسقِط ما تغيّر."""

from __future__ import annotations

import pytest

from alghanem.arabic.hollow_root_levels_preregistration import (
    FROZEN_SURFACES,
    LEVEL_ORDER,
    NAMED_RESIDUALS,
    PRE_REGISTERED_EXPECTATION,
    SURFACE_SET_DIGEST,
    ExampleProvenance,
    FrozenSurface,
    HollowRootLevel,
    surface_set_digest,
)


def test_the_surface_set_digest_is_rederived_not_declared() -> None:
    assert surface_set_digest() == SURFACE_SET_DIGEST
    assert len(SURFACE_SET_DIGEST) == 64


def test_adding_one_surface_changes_the_digest() -> None:
    widened = FROZEN_SURFACES + (
        FrozenSurface(
            surface="سَارَ",
            declared_root="سير",
            provenance=ExampleProvenance.MANUALLY_CONSTRUCTED_EXAMPLE,
        ),
    )
    assert surface_set_digest(widened) != SURFACE_SET_DIGEST


def test_no_surface_claims_to_be_a_corpus_occurrence() -> None:
    assert all(
        item.provenance is ExampleProvenance.MANUALLY_CONSTRUCTED_EXAMPLE
        for item in FROZEN_SURFACES
    )


def test_a_corpus_occurrence_cannot_be_declared_without_a_corpus() -> None:
    with pytest.raises(ValueError):
        FrozenSurface(
            surface="قَالَ",
            declared_root="قول",
            provenance=ExampleProvenance.MEASURED_CORPUS_OCCURRENCE,
        )


def test_the_level_order_covers_every_named_level_exactly_once() -> None:
    assert len(LEVEL_ORDER) == len(set(LEVEL_ORDER)) == len(HollowRootLevel)
    assert set(LEVEL_ORDER) == set(HollowRootLevel)


def test_the_expectation_is_frozen_text_not_a_result() -> None:
    assert isinstance(PRE_REGISTERED_EXPECTATION, str)
    assert PRE_REGISTERED_EXPECTATION.strip()


def test_the_named_residuals_are_present_and_nonempty() -> None:
    assert NAMED_RESIDUALS
    assert all(isinstance(note, str) and note.strip() for note in NAMED_RESIDUALS)


def test_the_hollow_minimal_pair_is_inside_the_frozen_set() -> None:
    surfaces = {item.surface: item.declared_root for item in FROZEN_SURFACES}
    assert surfaces["يَخَافُ"] == "خوف"
    assert surfaces["يَهَابُ"] == "هيب"
