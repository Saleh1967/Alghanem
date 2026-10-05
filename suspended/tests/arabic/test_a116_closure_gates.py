"""بوّاباتُ الإغلاق مقيسةً: التغطية، والضرورة، وبديلُ شهادة الولادة، وفجوةُ الوقف."""

from alghanem.arabic.a116_closure_gates import (
    cell_witnesses,
    pause_final_clusters,
    segment_coverage,
    short_nouns,
)


def test_every_aligned_segment_is_syllabified_or_deferred_by_name() -> None:
    reading = segment_coverage()
    assert reading["segments"] == 144811
    assert reading["syllabified"] == 140448
    assert reading["deferred"] == {
        "TANWIN_ATTACHMENT_IS_AMBIGUOUS": 3116,
        "THE_ROLE_OF_THIS_ALIF_IS_UNDECIDED": 968,
        "HARAKA_IS_ABSENT_AND_IS_NEVER_GUESSED": 273,
        "ALIF_AFTER_A_POSSIBLE_PREFIX_MAY_BE_WASL": 6,
    }
    assert reading["syllabified"] + sum(reading["deferred"].values()) == 144811
    assert reading["unaligned_words"] == 2434


def test_113_of_the_116_cells_are_witnessed_and_the_rest_is_the_vowelled_alif() -> None:
    reading = cell_witnesses()
    assert reading["witnessed"] == 113
    assert reading["unwitnessed"] == ["اَ", "اُ", "اِ"]
    assert reading["atoms_outside_the_116"] == []


def test_a_whole_noun_of_two_atoms_exists() -> None:
    reading = short_nouns()
    assert reading["whole_words"] == {"ذُو": 25, "ذِي": 19, "يَدُ": 2, "ذَا": 11}
    assert len(reading["stems"]) == 30


def test_a_quarter_of_ready_verse_endings_close_on_two_sukuns_at_pause() -> None:
    reading = pause_final_clusters()
    assert reading["ready"] == 606
    assert reading["final_double_sukun"] == 156
    assert reading["deferred"] == 5630
