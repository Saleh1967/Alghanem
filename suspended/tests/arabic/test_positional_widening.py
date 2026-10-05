"""شواهدُ توسيع الموضع: العشرُ كانت خبرًا عن موضعَين لا عن الخطّ."""

from __future__ import annotations

import pytest

from alghanem.arabic.blind_skeleton_transport import (
    THE_DEPOSITS_READ,
    classes_that_transport,
    geometric_classes_of,
)
from alghanem.arabic.font_deposit import AMIRI, NOTO_KUFI, SCHEHERAZADE, load_font
from alghanem.arabic.positional_widening import (
    POSITIONAL_WIDENING_NAMED_RESIDUALS,
    POSITIONS,
    PositionalCensus,
    PositionalWideningError,
    census_at,
    classes_that_transport_at,
    classes_that_transport_everywhere,
    letters_present_in,
    letters_uncovered_by,
    positional_classes_of,
    positional_map,
    positional_sample_of,
    shared_classes_of,
    substitutions_refused_in,
    the_classes_only_a_wider_question_finds,
    the_uncovered_set_is_the_same_in_every_deposit,
)

_JOINED = ("init", "medi", "fina")


def test_the_four_positions_are_the_ones_measured() -> None:
    assert POSITIONS == ("isol", "init", "medi", "fina")


@pytest.mark.parametrize("filename", THE_DEPOSITS_READ)
@pytest.mark.parametrize("position", POSITIONS)
def test_every_positional_sample_is_opaque_numbers_only(
    filename: str, position: str
) -> None:
    sample = positional_sample_of(filename, position)
    assert sample
    assert all(isinstance(glyph, int) for glyph in sample)
    assert sample == tuple(sorted(set(sample)))


def test_the_isolated_position_is_not_read_from_a_substitution() -> None:
    with pytest.raises(PositionalWideningError):
        positional_map(AMIRI, "isol")


def test_a_position_that_does_not_exist_is_refused() -> None:
    with pytest.raises(PositionalWideningError):
        positional_sample_of(AMIRI, "final")


@pytest.mark.parametrize("filename", THE_DEPOSITS_READ)
@pytest.mark.parametrize("position", _JOINED)
def test_no_two_letters_are_sent_to_one_glyph(filename: str, position: str) -> None:
    font = load_font(filename)
    substituted = positional_map(filename, position)
    landed = [
        substituted[glyph]
        for letter in letters_present_in(filename)
        if (glyph := font.glyph_for(letter)) in substituted
    ]
    assert len(landed) == len(set(landed))


def test_sharing_is_geometric_and_never_glyph_identity() -> None:
    font = load_font(AMIRI)
    substituted = positional_map(AMIRI, "init")
    beh, teh = (substituted[font.glyph_for(letter)] for letter in ("\u0628", "\u062a"))
    assert beh != teh
    assert any(
        {"\u0628", "\u062a"} <= found for found in positional_classes_of(AMIRI, "init")
    )


@pytest.mark.parametrize("filename", THE_DEPOSITS_READ)
def test_the_isolated_position_reproduces_the_earlier_milestone(filename: str) -> None:
    assert set(shared_classes_of(filename, "isol")) == set(
        geometric_classes_of(filename)
    )


@pytest.mark.parametrize(
    ("filename", "letters"), [(AMIRI, 47), (SCHEHERAZADE, 47), (NOTO_KUFI, 42)]
)
def test_the_letter_inventory_is_what_was_published(
    filename: str, letters: int
) -> None:
    assert len(letters_present_in(filename)) == letters


def test_the_kufi_lacks_five_letters_the_naskh_deposits_carry() -> None:
    naskh = set(letters_present_in(AMIRI))
    assert naskh == set(letters_present_in(SCHEHERAZADE))
    assert naskh - set(letters_present_in(NOTO_KUFI)) == set(
        "\u063b\u063c\u063d\u063e\u063f"
    )


@pytest.mark.parametrize(
    ("filename", "covered"),
    [
        (AMIRI, (47, 29, 29, 40)),
        (SCHEHERAZADE, (47, 29, 29, 40)),
        (NOTO_KUFI, (42, 24, 24, 35)),
    ],
)
def test_the_coverage_per_position_is_what_was_published(
    filename: str, covered: tuple[int, ...]
) -> None:
    assert tuple(census_at(filename, p).covered for p in POSITIONS) == covered


@pytest.mark.parametrize(
    ("filename", "classes"),
    [
        (AMIRI, (27, 11, 11, 21)),
        (SCHEHERAZADE, (25, 11, 11, 19)),
        (NOTO_KUFI, (25, 10, 11, 19)),
    ],
)
def test_the_class_count_per_position_is_what_was_published(
    filename: str, classes: tuple[int, ...]
) -> None:
    assert tuple(census_at(filename, p).classes for p in POSITIONS) == classes


@pytest.mark.parametrize(
    ("filename", "shared"),
    [
        (AMIRI, (13, 8, 8, 13)),
        (SCHEHERAZADE, (14, 8, 8, 13)),
        (NOTO_KUFI, (14, 6, 7, 13)),
    ],
)
def test_the_shared_class_count_per_position_is_what_was_published(
    filename: str, shared: tuple[int, ...]
) -> None:
    assert tuple(census_at(filename, p).shared for p in POSITIONS) == shared


@pytest.mark.parametrize("filename", THE_DEPOSITS_READ)
@pytest.mark.parametrize("position", POSITIONS)
def test_the_shared_classes_are_a_subset_of_the_partition(
    filename: str, position: str
) -> None:
    census = census_at(filename, position)
    assert census.shared <= census.classes <= census.covered
    assert set(shared_classes_of(filename, position)) <= set(
        positional_classes_of(filename, position)
    )


@pytest.mark.parametrize("position", _JOINED)
def test_the_three_deposits_agree_exactly_on_who_has_this_position(
    position: str,
) -> None:
    assert the_uncovered_set_is_the_same_in_every_deposit(position)
    found = {letters_uncovered_by(name, position) for name in THE_DEPOSITS_READ}
    assert len(found) == 1


@pytest.mark.parametrize(
    ("position", "size"), [("init", 18), ("medi", 18), ("fina", 7)]
)
def test_the_uncovered_sets_are_the_published_sizes(position: str, size: int) -> None:
    assert len(letters_uncovered_by(AMIRI, position)) == size


def test_the_letters_with_no_initial_form_include_the_known_non_joiners() -> None:
    uncovered = letters_uncovered_by(AMIRI, "init")
    assert set("\u0627\u062f\u0630\u0631\u0632\u0648") <= uncovered
    assert "\u0628" not in uncovered


def test_a_final_form_exists_for_letters_that_have_no_initial_one() -> None:
    assert set("\u0627\u062f\u0630\u0631\u0632\u0648") <= letters_uncovered_by(
        AMIRI, "init"
    )
    assert not set("\u0627\u062f\u0630\u0631\u0632\u0648") & letters_uncovered_by(
        AMIRI, "fina"
    )


@pytest.mark.parametrize(
    ("position", "count"), [("isol", 10), ("init", 3), ("medi", 4), ("fina", 10)]
)
def test_the_transport_per_position_is_what_was_published(
    position: str, count: int
) -> None:
    assert len(classes_that_transport_at(position)) == count


def test_the_isolated_transport_equals_the_earlier_milestone() -> None:
    assert set(classes_that_transport_at("isol")) == set(classes_that_transport())


def test_the_isolated_and_final_positions_transport_the_same_classes() -> None:
    assert set(classes_that_transport_at("isol")) == set(
        classes_that_transport_at("fina")
    )


def test_only_two_classes_survive_all_four_positions() -> None:
    surviving = classes_that_transport_everywhere()
    assert len(surviving) == 2
    assert {"".join(sorted(c)) for c in surviving} == {"\u0633\u0634", "\u0639\u063a"}


def test_the_flagship_class_falls_in_the_joined_positions() -> None:
    family = frozenset("\u0628\u062a\u062b")
    assert family in classes_that_transport_at("isol")
    assert family in classes_that_transport_at("fina")
    assert family not in classes_that_transport_at("init")
    assert family not in classes_that_transport_at("medi")


def test_the_flagship_falls_by_widening_not_by_disagreement_over_it() -> None:
    for filename in (AMIRI, SCHEHERAZADE):
        holding = [c for c in positional_classes_of(filename, "init") if "\u0628" in c]
        assert len(holding) == 1
        assert set("\u062a\u062b\u0646\u064a") <= holding[0]
        assert len(holding[0]) > 3


def test_widening_the_question_adds_a_class_it_could_not_have_seen() -> None:
    added = the_classes_only_a_wider_question_finds()
    assert {"".join(sorted(c)) for c in added} == {"\u0641\u0642"}


def test_the_added_class_is_absent_from_the_unjoined_positions() -> None:
    feh_qaf = frozenset("\u0641\u0642")
    assert feh_qaf in classes_that_transport_at("init")
    assert feh_qaf in classes_that_transport_at("medi")
    assert feh_qaf not in classes_that_transport_at("isol")
    assert feh_qaf not in classes_that_transport_at("fina")


def test_the_union_over_positions_exceeds_the_intersection() -> None:
    union: set[frozenset[str]] = set()
    for position in POSITIONS:
        union |= set(classes_that_transport_at(position))
    assert len(union) == 11
    assert len(classes_that_transport_everywhere()) == 2


def test_transport_needs_more_than_one_deposit() -> None:
    with pytest.raises(PositionalWideningError):
        classes_that_transport_at("init", (AMIRI,))


def test_transport_across_the_two_naskh_exceeds_transport_to_the_kufi() -> None:
    naskh = classes_that_transport_at("init", (AMIRI, SCHEHERAZADE))
    assert len(naskh) > len(classes_that_transport_at("init"))


@pytest.mark.parametrize(
    ("filename", "refused"),
    [(AMIRI, (1, 1, 3)), (SCHEHERAZADE, (0, 0, 0)), (NOTO_KUFI, (0, 0, 0))],
)
def test_the_refused_substitutions_are_counted_and_published(
    filename: str, refused: tuple[int, ...]
) -> None:
    assert tuple(substitutions_refused_in(filename, p) for p in _JOINED) == refused


def test_a_refusal_count_is_asked_of_a_substituted_position_only() -> None:
    with pytest.raises(PositionalWideningError):
        substitutions_refused_in(AMIRI, "isol")


def test_a_census_with_more_classes_than_letters_is_refused() -> None:
    with pytest.raises(PositionalWideningError):
        PositionalCensus(
            filename=AMIRI, position="init", covered=5, classes=6, shared=1
        )


def test_a_census_of_an_unknown_position_is_refused() -> None:
    with pytest.raises(PositionalWideningError):
        PositionalCensus(
            filename=AMIRI, position="fnal", covered=5, classes=2, shared=1
        )


def test_an_empty_census_is_refused_rather_than_defaulted() -> None:
    with pytest.raises(PositionalWideningError):
        PositionalCensus(
            filename=AMIRI, position="init", covered=0, classes=0, shared=0
        )


def test_more_shared_classes_than_classes_is_refused() -> None:
    with pytest.raises(PositionalWideningError):
        PositionalCensus(
            filename=AMIRI, position="init", covered=9, classes=3, shared=4
        )


def test_every_residual_is_named_by_its_own_key() -> None:
    for key, text in POSITIONAL_WIDENING_NAMED_RESIDUALS.items():
        assert text.startswith(f"{key}: ")


def test_the_residuals_refuse_a_shaping_claim_and_a_cross_position_one() -> None:
    assert (
        "A_NAMED_POSITION_IS_NOT_A_SHAPED_WORD" in POSITIONAL_WIDENING_NAMED_RESIDUALS
    )
    assert (
        "NO_CLASS_HERE_CROSSES_A_POSITION_BOUNDARY"
        in POSITIONAL_WIDENING_NAMED_RESIDUALS
    )
