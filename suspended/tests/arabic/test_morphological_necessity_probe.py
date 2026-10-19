"""اختبارُ تجميدِ الفحص قبل إجرائه: هدفٌ مُجمَّدٌ بحارسه، ومخروطٌ مقروءٌ من الشجرة."""

from __future__ import annotations

import pytest

from alghanem.arabic.morphological_necessity_probe import (
    CATALOG_RELATIVE_PATH,
    DISCRIMINATION_TARGET_DIGEST,
    FROZEN_DISCRIMINATION_TARGET,
    NAMED_RESIDUALS,
    PRE_REGISTERED_EXPECTATION,
    DiscriminationPair,
    MorphologicalNecessityProbeError,
    discrimination_target_digest,
    read_weaker_domain_cone,
)
from alghanem.arabic.pipeline_stations import repository_root_path
from alghanem.arabic.text_key import comparison_key


def test_the_target_is_exactly_the_three_catalogued_pairs() -> None:
    assert len(FROZEN_DISCRIMINATION_TARGET) == 3
    assert {
        (pair.surface_a, pair.surface_b) for pair in FROZEN_DISCRIMINATION_TARGET
    } == {("مِن", "مَن"), ("أَمْ", "أُمّ"), ("هَمَّ", "هُمْ")}


def test_every_pair_collides_under_the_trees_own_comparison_key() -> None:
    for pair in FROZEN_DISCRIMINATION_TARGET:
        assert comparison_key(pair.surface_a) == comparison_key(pair.surface_b)
        assert pair.collided_key == comparison_key(pair.surface_a)


def test_a_non_colliding_pair_is_refused_as_a_discrimination_target() -> None:
    with pytest.raises(MorphologicalNecessityProbeError):
        DiscriminationPair(
            surface_a="نور",
            surface_b="نار",
            catalog_locus="مُختلَق",
            catalog_excerpt="نور و نار",
        )


def test_a_pair_absent_from_its_recorded_excerpt_is_refused() -> None:
    with pytest.raises(MorphologicalNecessityProbeError):
        DiscriminationPair(
            surface_a="مِن",
            surface_b="مَن",
            catalog_locus="موضعٌ مذكور",
            catalog_excerpt="نصٌّ لا يرد فيه الطرفان بحروفهما",
        )


def test_the_recorded_locus_exists_in_the_tree_and_carries_the_excerpt() -> None:
    catalog = (repository_root_path() / CATALOG_RELATIVE_PATH).read_text(
        encoding="utf-8"
    )
    for pair in FROZEN_DISCRIMINATION_TARGET:
        assert CATALOG_RELATIVE_PATH in pair.catalog_locus
        assert pair.surface_a in catalog
        assert pair.surface_b in catalog


def test_adding_a_pair_after_the_freeze_is_structurally_refused() -> None:
    intruder = DiscriminationPair(
        surface_a="هَذا",
        surface_b="هذَا",
        catalog_locus="زوجٌ يُضاف بعد التجميد",
        catalog_excerpt="هَذا / هذَا",
    )
    widened = FROZEN_DISCRIMINATION_TARGET + (intruder,)
    assert discrimination_target_digest(widened) != DISCRIMINATION_TARGET_DIGEST


def test_dropping_a_pair_after_the_freeze_is_structurally_refused() -> None:
    narrowed = FROZEN_DISCRIMINATION_TARGET[:-1]
    assert discrimination_target_digest(narrowed) != DISCRIMINATION_TARGET_DIGEST


def test_reordering_the_target_is_structurally_refused() -> None:
    reordered = tuple(reversed(FROZEN_DISCRIMINATION_TARGET))
    assert discrimination_target_digest(reordered) != DISCRIMINATION_TARGET_DIGEST


def test_the_frozen_digest_is_rederived_not_trusted() -> None:
    assert discrimination_target_digest() == DISCRIMINATION_TARGET_DIGEST


def test_the_cone_is_read_from_the_tree_not_written() -> None:
    cone = read_weaker_domain_cone()
    assert len(cone) == 4
    for reference in cone:
        assert reference.is_present_in_tree
        assert reference.module_path.is_file()
        assert reference.domain is not None


def test_the_expectation_is_registered_before_any_measurement() -> None:
    assert "غير_محسوم_لتعذّر_القياس" in PRE_REGISTERED_EXPECTATION


def test_no_outcome_vocabulary_exists_in_the_freezing_module() -> None:
    import alghanem.arabic.morphological_necessity_probe as module

    assert not hasattr(module, "derive_pair_standing")
    assert not hasattr(module, "PairStanding")
    assert "NO_DOMAIN_IS_APPLIED_IN_THIS_MODULE" in NAMED_RESIDUALS


def test_the_limits_of_the_freeze_are_named_not_left_to_the_reader() -> None:
    for key in (
        "FREEZE_BEFORE_MEASUREMENT",
        "TARGET_PREDATES_THE_QUESTION",
        "COLLISION_IS_REDERIVED_NOT_ASSERTED",
        "CONE_IS_READ_NOT_CHOSEN",
        "MEASURED_NEGATIVE_IS_NOT_A_CONSTITUTIONAL_NECESSITY",
        "THREE_PAIRS_ARE_NOT_THE_LANGUAGE",
        "COMPARISON_KEY_IS_A_TOOL_LIMIT_NOT_A_LANGUAGE_FACT",
        "CATALOG_IS_TESTIMONY_NOT_MEASUREMENT",
    ):
        assert key in NAMED_RESIDUALS
        assert NAMED_RESIDUALS[key].strip()
