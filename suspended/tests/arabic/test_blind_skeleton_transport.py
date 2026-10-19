"""شواهدُ الولادة العمياء: المُعلَنُ لا ينتقل، والمقيسُ ينتقل."""

from __future__ import annotations

import pytest

from alghanem.arabic.blind_skeleton_transport import (
    BLIND_SAMPLE_RANGE,
    SKELETON_TRANSPORT_NAMED_RESIDUALS,
    THE_DEPOSITS_READ,
    BlindSkeletonError,
    DescriptionLength,
    blind_sample_of,
    classes_that_transport,
    declared_classes_of,
    description_length_of,
    fused_alef_class_in,
    geometric_classes_of,
    group_blindly,
    open_identities,
    the_canonical_fusion_is_realized_in,
    the_whole_font_sample_of,
)
from alghanem.arabic.font_deposit import AMIRI, NOTO_KUFI, SCHEHERAZADE


def test_the_three_deposits_are_the_ones_read() -> None:
    assert THE_DEPOSITS_READ == (AMIRI, SCHEHERAZADE, NOTO_KUFI)


@pytest.mark.parametrize("filename", THE_DEPOSITS_READ)
def test_the_blind_sample_is_opaque_numbers_only(filename: str) -> None:
    sample = blind_sample_of(filename)
    assert sample
    assert all(isinstance(glyph, int) for glyph in sample)
    assert sample == tuple(sorted(set(sample)))


def test_the_blind_sample_range_is_the_arabic_letters_and_marks() -> None:
    low, high = BLIND_SAMPLE_RANGE
    assert (low, high) == (0x0621, 0x064F)


@pytest.mark.parametrize("filename", THE_DEPOSITS_READ)
def test_grouping_partitions_the_sample_without_loss(filename: str) -> None:
    sample = blind_sample_of(filename)
    grouped = group_blindly(filename, sample)
    members = [glyph for group in grouped for glyph in group]
    assert sorted(members) == sorted(sample)
    assert len(members) == len(set(members))


def test_grouping_is_indifferent_to_the_order_it_is_given() -> None:
    sample = blind_sample_of(AMIRI)
    forward = set(group_blindly(AMIRI, sample))
    backward = set(group_blindly(AMIRI, tuple(reversed(sample))))
    assert forward == backward


def test_an_empty_sample_groups_to_nothing() -> None:
    assert group_blindly(AMIRI, ()) == ()


def test_opening_identities_reports_only_classes_of_more_than_one_letter() -> None:
    opened = open_identities(AMIRI, group_blindly(AMIRI, blind_sample_of(AMIRI)))
    assert all(len(letters) > 1 for letters in opened)


@pytest.mark.parametrize(
    ("filename", "declared", "measured"),
    [(AMIRI, 12, 13), (SCHEHERAZADE, 14, 14), (NOTO_KUFI, 4, 14)],
)
def test_the_declared_and_measured_counts_are_what_was_published(
    filename: str, declared: int, measured: int
) -> None:
    assert len(declared_classes_of(filename)) == declared
    assert len(geometric_classes_of(filename)) == measured


def test_the_kufi_declares_far_less_than_it_measures() -> None:
    assert len(declared_classes_of(NOTO_KUFI)) < len(geometric_classes_of(NOTO_KUFI))


def test_everything_the_kufi_declares_is_a_hamza_carrier_family() -> None:
    for letters in declared_classes_of(NOTO_KUFI):
        assert letters & {"\u0622", "\u0623", "\u0624", "\u0625", "\u0626"}


def test_no_declared_decomposition_transports_to_all_three_deposits() -> None:
    assert classes_that_transport(declared=True) == ()


def test_ten_measured_classes_transport_to_all_three_deposits() -> None:
    assert len(classes_that_transport()) == 10


def test_the_transporting_classes_are_the_rasm_families() -> None:
    found = {"".join(sorted(letters)) for letters in classes_that_transport()}
    assert found == {
        "\u0628\u062a\u062b",
        "\u062c\u062d\u062e",
        "\u062f\u0630",
        "\u0631\u0632",
        "\u0633\u0634",
        "\u0635\u0636",
        "\u0637\u0638",
        "\u0639\u063a",
        "\u0629\u0647",
        "\u0624\u0648",
    }


def test_beh_teh_theh_share_one_skeleton_in_every_deposit() -> None:
    family = frozenset({"\u0628", "\u062a", "\u062b"})
    for filename in THE_DEPOSITS_READ:
        assert family in geometric_classes_of(filename)


def test_beh_and_noon_are_not_in_one_class_in_any_deposit() -> None:
    for filename in THE_DEPOSITS_READ:
        for letters in geometric_classes_of(filename):
            assert not {"\u0628", "\u0646"} <= letters


def test_transport_across_the_two_naskh_exceeds_transport_to_the_kufi() -> None:
    naskh = classes_that_transport((AMIRI, SCHEHERAZADE))
    everywhere = classes_that_transport()
    assert len(naskh) > len(everywhere)


def test_transport_needs_more_than_one_deposit() -> None:
    with pytest.raises(BlindSkeletonError):
        classes_that_transport((AMIRI,))


def test_transport_over_one_deposit_is_just_its_own_classes() -> None:
    pair = classes_that_transport((AMIRI, AMIRI))
    assert set(pair) == set(geometric_classes_of(AMIRI))


def test_widening_the_blind_sample_leaves_the_naskh_where_it_was() -> None:
    for filename in (AMIRI, SCHEHERAZADE):
        narrow = len(geometric_classes_of(filename))
        wide = len(geometric_classes_of(filename, True))
        assert narrow == wide


def test_widening_the_blind_sample_collapses_the_kufi() -> None:
    assert len(geometric_classes_of(NOTO_KUFI)) == 14
    assert len(geometric_classes_of(NOTO_KUFI, True)) == 10


def test_the_collapse_is_a_chain_that_merges_families() -> None:
    merged = [
        letters
        for letters in geometric_classes_of(NOTO_KUFI, True)
        if {"\u0639", "\u0647"} <= letters
    ]
    assert merged
    assert len(merged[0]) > 2


@pytest.mark.parametrize("filename", THE_DEPOSITS_READ)
def test_the_whole_font_sample_covers_every_glyph(filename: str) -> None:
    from alghanem.arabic.font_deposit import load_font

    assert len(the_whole_font_sample_of(filename)) == load_font(filename).glyph_count


@pytest.mark.parametrize("filename", THE_DEPOSITS_READ)
def test_the_structural_model_is_never_longer_than_the_independent_one(
    filename: str,
) -> None:
    measured = description_length_of(filename)
    assert measured.shared_points <= measured.independent_points
    assert 0.0 < measured.saving < 100.0


@pytest.mark.parametrize(
    ("filename", "saving"),
    [(AMIRI, 32.463), (SCHEHERAZADE, 34.660), (NOTO_KUFI, 30.416)],
)
def test_the_saving_is_what_was_published(filename: str, saving: float) -> None:
    assert round(description_length_of(filename).saving, 3) == saving


def test_the_saving_is_close_in_three_unlike_designs() -> None:
    savings = [description_length_of(name).saving for name in THE_DEPOSITS_READ]
    assert max(savings) - min(savings) < 5.0


def test_a_description_length_longer_when_shared_is_refused() -> None:
    with pytest.raises(BlindSkeletonError):
        DescriptionLength(
            scope="محال", independent_points=10, shared_points=11, references=1
        )


def test_a_description_length_without_a_scope_is_refused() -> None:
    with pytest.raises(BlindSkeletonError):
        DescriptionLength(
            scope="  ", independent_points=10, shared_points=5, references=1
        )


def test_only_scheherazade_realizes_the_canonical_alef_fusion() -> None:
    realized = [
        name for name in THE_DEPOSITS_READ if the_canonical_fusion_is_realized_in(name)
    ]
    assert realized == [SCHEHERAZADE]


def test_amiri_groups_the_alef_family_but_leaves_out_the_hamza_above() -> None:
    found = fused_alef_class_in(AMIRI)
    assert {"\u0627", "\u0622", "\u0625"} <= found
    assert "\u0623" not in found


def test_the_kufi_splits_the_alef_family_in_two() -> None:
    found = fused_alef_class_in(NOTO_KUFI)
    assert found == frozenset({"\u0627", "\u0625"})


def test_the_deposits_disagree_exactly_where_the_table_fuses() -> None:
    classes = {name: fused_alef_class_in(name) for name in THE_DEPOSITS_READ}
    assert len({frozenset(value) for value in classes.values()}) == 3


def test_every_residual_is_named_by_its_own_key() -> None:
    for key, text in SKELETON_TRANSPORT_NAMED_RESIDUALS.items():
        assert text.startswith(f"{key}: ")


def test_the_residuals_refuse_a_linguistic_reading_and_a_model_selection() -> None:
    assert "SHARED_GEOMETRY_IS_NOT_A_LINGUISTIC_IDENTITY" in (
        SKELETON_TRANSPORT_NAMED_RESIDUALS
    )
    assert "THE_DESCRIPTION_LENGTH_IS_A_NUMBER_NOT_A_SELECTION" in (
        SKELETON_TRANSPORT_NAMED_RESIDUALS
    )
