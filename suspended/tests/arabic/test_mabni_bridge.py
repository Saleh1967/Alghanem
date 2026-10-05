"""جسرُ المبنيّات: التوليدُ من الجذر، والاسترجاعُ بعكسه، والإسقاطُ على الـ116."""

from __future__ import annotations

import pytest

from alghanem.arabic.mabni_bridge import (
    MabniGenus,
    align,
    closedness_readings,
    genus_of,
    project_form,
    wasl_start_vowel,
)
from alghanem.arabic.mabni_verbs import (
    candidate_roots,
    normalize,
    root_class,
    roots_generating,
    verb_forms,
)


def analyses(root: str, word: str) -> list[tuple[str, str, str]]:
    target = normalize(word)
    return [
        a for w, an in verb_forms(root).items() if normalize(w) == target for a in an
    ]


@pytest.mark.parametrize(
    ("root", "word", "expected"),
    [
        ("ضرب", "ضَرَبُوا", ("PAST", "I-a", "3MP")),
        ("علم", "عَلِمْتُمْ", ("PAST", "I-i", "2MP")),
        ("نزل", "نَزَّلْنَا", ("PAST", "II", "1P")),
        ("غفر", "اسْتَغْفِرُوا", ("IMPERATIVE", "X", "2MP")),
        ("تبع", "اتَّبَعُوا", ("PAST", "VIII", "3MP")),
        ("صبر", "اصْطَبِرْ", ("IMPERATIVE", "VIII", "2MS")),
        ("قول", "قَالَ", ("PAST", "I", "3MS")),
        ("قول", "قُلْتُ", ("PAST", "I", "1S")),
        ("قول", "قِيلَ", ("PASSIVE", "I", "3MS")),
        ("قول", "قُلْ", ("IMPERATIVE", "I", "2MS")),
        ("قول", "قُولُوا", ("IMPERATIVE", "I", "2MP")),
        ("قوم", "أَقِيمُوا", ("IMPERATIVE", "IV", "2MP")),
        ("قوم", "اسْتَقَامُوا", ("PAST", "X", "3MP")),
        ("خير", "اخْتَارَ", ("PAST", "VIII", "3MS")),
        ("دعو", "دَعَا", ("PAST", "I-a", "3MS")),
        ("دعو", "دَعَوْا", ("PAST", "I-a", "3MP")),
        ("دعو", "ادْعُ", ("IMPERATIVE", "I", "2MS")),
        ("رمي", "رَمَى", ("PAST", "I-a", "3MS")),
        ("رضي", "رَضُوا", ("PAST", "I-i", "3MP")),
        ("رضي", "رَضِيتُ", ("PAST", "I-i", "1S")),
        ("عطو", "أَعْطَى", ("PAST", "IV", "3MS")),
        ("وقي", "اتَّقُوا", ("IMPERATIVE", "VIII", "2MP")),
        ("حيي", "أَحْيَا", ("PAST", "IV", "3MS")),
        ("مدد", "مَدَدْتُ", ("PAST", "I-a", "1S")),
        ("مدد", "مَدُّوا", ("PAST", "I-a", "3MP")),
        ("مدد", "امْدُدْ", ("IMPERATIVE", "I-u", "2MS")),
        ("وعد", "عِدْ", ("IMPERATIVE", "I", "2MS")),
        ("أخذ", "خُذْ", ("IMPERATIVE", "I", "2MS")),
        ("أخذ", "اتَّخَذَ", ("PAST", "VIII", "3MS")),
        ("أمن", "آمَنُوا", ("PAST", "IV", "3MP")),
        ("بيض", "ابْيَضَّتْ", ("PAST", "IX", "3FS")),
        ("طمأن", "اطْمَأَنَّ", ("PAST", "Q-IV", "3MS")),
        ("زلزل", "زُلْزِلُوا", ("PASSIVE", "Q-I", "3MP")),
    ],
)
def test_the_declared_rules_generate_the_attested_form(
    root: str, word: str, expected: tuple[str, str, str]
) -> None:
    assert expected in analyses(root, word)


def test_one_form_keeps_every_analysis() -> None:
    assert {("PAST", "III", "3MS"), ("PAST", "IV", "3MS")} <= set(
        analyses("أمن", "آمَنَ")
    )


def test_a_sound_root_never_spells_a_hollow_form() -> None:
    assert not analyses("ضرب", "ضَارَ")
    assert "قَوَلَ" not in verb_forms("قول")


def test_root_classes_are_read_from_the_letters() -> None:
    assert [root_class(r) for r in ("ضرب", "قول", "دعو", "مدد")] == [
        "SOUND",
        "HOLLOW",
        "DEFECTIVE",
        "DOUBLED",
    ]


def test_the_seat_and_the_final_haraka_are_normalised_on_both_sides() -> None:
    assert normalize("سُئِلَ") == normalize("سُءِلَ")
    assert normalize("عَلِمْتُمُ") == normalize("عَلِمْتُمْ")
    assert normalize("دَعَوُا") == normalize("دَعَوْا")


def test_a_root_absent_from_the_lexicon_is_named_from_the_letters() -> None:
    assert "ترك" in candidate_roots("تَرَكْنَا")
    assert "ترك" in roots_generating("تَرَكْنَا")


def test_the_genera_are_declared_by_tag() -> None:
    assert genus_of("PREP") is MabniGenus.LEXICAL
    assert genus_of("REL_PRON") is MabniGenus.LEXICAL
    assert genus_of("NOUN_VERB_LIKE") is MabniGenus.LEXICAL
    assert genus_of("PV") is MabniGenus.MORPHOLOGICAL
    assert genus_of("NOUN_PROP") is MabniGenus.POSITIONAL


def test_alignment_splits_the_vocalised_word_on_its_bare_segments() -> None:
    assert align("أَنْعَمْتَ", ["أنعم", "ت"]) == ["أَنْعَمْ", "تَ"]
    assert align("لِلَّهِ", ["ل", "ال", "له"]) is None


def test_a_generated_wasl_alif_carries_its_start_vowel() -> None:
    assert wasl_start_vowel("اكْتُبْ") == "ُ"
    assert wasl_start_vowel("اضْرِبْ") == "ِ"
    assert wasl_start_vowel("اسْتَغْفِرْ") == "ِ"
    assert wasl_start_vowel("قَالَ") is None
    status, atoms = project_form("اضْرِبُوا", "start_continue", generated=True)
    assert status == "READY"
    assert atoms == ("ءِ", "ضْ", "رِ", "بُ", "وْ")


def test_an_attested_surface_is_not_annotated() -> None:
    status, _ = project_form("اضْرِبُوا", "start_continue")
    assert status == "DEFER"


def test_the_lexical_genus_is_closed_and_the_others_are_not() -> None:
    readings = {r.genus: r for r in closedness_readings()}
    lexical = readings[MabniGenus.LEXICAL]
    verbal = readings[MabniGenus.MORPHOLOGICAL]
    assert lexical.token_coverage > 0.99
    assert verbal.token_coverage < lexical.token_coverage
    assert verbal.type_coverage < 0.7 < lexical.type_coverage


def test_the_dual_alif_is_read_and_the_plural_alif_is_silent() -> None:
    assert project_form("دَعَوَا", "start_pause", generated=True) == (
        "READY",
        ("دَ", "عَ", "وَ", "اْ"),
    )
    assert project_form("دَعَوْا", "start_pause", generated=True) == (
        "READY",
        ("دَ", "عَ", "وْ"),
    )
