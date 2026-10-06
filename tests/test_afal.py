"""الأفعال الخمسة: الصورُ من القانون تطابق شهاداتِ البوّابة؛ الرفعُ بتٌّ واحد؛ النصبُ هو الجزم."""

from __future__ import annotations

import pytest

from slge.afal import FIVE, MOODS, PRONOUNS, STEMS, WITNESS, Stem, agree, form, mood_of, pronoun_of
from slge.cells import STATES, licensed

BY = {s.name: s for s in STEMS}


def test_forms_match_gate_witnesses() -> None:
    assert form(BY["يَفْعَلُ"], "الجماعة", "رفع") == WITNESS["يَفْعَلُونَ"]
    assert form(BY["يَفْعَلُ"], "الجماعة", "نصب") == WITNESS["يَفْعَلُوا"]
    assert form(BY["تَعْلَمُ"], "الجماعة", "رفع") == WITNESS["تَعْلَمُونَ"]
    assert form(BY["تَعْلَمُ"], "الجماعة", "جزم") == WITNESS["تَعْلَمُوا"]
    assert form(BY["يَقْتَتِلُ"], "الاثنين", "رفع") == WITNESS["يَقْتَتِلَانِ"]
    assert form(BY["تَخَافُ"], "المخاطبة", "جزم") == WITNESS["تَخَافِي"]


def test_exactly_five_and_ghaib_never_takes_ya() -> None:
    assert len(FIVE) == 5 and ("غائب", "المخاطبة") not in FIVE
    with pytest.raises(ValueError):
        form(BY["يَفْعَلُ"], "المخاطبة", "رفع")


def test_mood_is_one_bit_and_nasb_equals_jazm() -> None:
    for s in STEMS:
        for p in PRONOUNS:
            if not agree(s.prefix, p):
                continue
            assert form(s, p, "نصب") == form(s, p, "جزم")
            assert mood_of(form(s, p, "رفع")) == "رفع"
            assert mood_of(form(s, p, "نصب")) == "نصب/جزم"
            assert len(form(s, p, "رفع")) == len(form(s, p, "نصب")) + 1


def test_pronoun_read_back_and_licensed() -> None:
    for s in STEMS:
        for p in PRONOUNS:
            if agree(s.prefix, p):
                for m in MOODS:
                    assert licensed(form(s, p, m)) and pronoun_of(form(s, p, m)) == p


def test_mutation_breaks_the_harmony_law() -> None:
    w = list(form(BY["يَفْعَلُ"], "الجماعة", "رفع"))
    w[3] = ("ل", STATES[1])  # كسرة قبل الواو: خارج القانون
    assert tuple(w) not in {form(BY["يَفْعَلُ"], p, m) for p in PRONOUNS[:2] for m in MOODS}
    assert isinstance(Stem("x", "غائب", STATES[0], (), "ب"), Stem)
