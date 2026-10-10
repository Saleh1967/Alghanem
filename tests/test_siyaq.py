"""السياق: توقّعاتٌ مستقلّةٌ عن الشيفرة — الإسقاطُ إلى الحدّ بوجوه الوقف الأربعة والوصل، والردُّ مغلقٌ على
الإسقاط ويحوي الصورةَ نفسَها ومحدودٌ، وعلاقاتُ المودَعين مسمّاةٌ كلُّها على المصحف؛ وطفراتٌ مرفوضة."""

from __future__ import annotations

import gzip
import json
from pathlib import Path

import pytest

from slge.cells import SUKUN
from slge.rawabit import cells_of
from slge.sawabiq import lift
from slge.siyaq import TANWIN, WAQF, Hadd, classify, project, relation, restore, waqf
from slge.zuruf import set_last

DATA = Path(__file__).parent / "data"
ALIF = ("ا", SUKUN)
HADDS = (Hadd(False, False), Hadd(True, False), Hadd(False, True), Hadd(True, True))


def test_the_four_pausal_forms_are_the_classical_ones() -> None:
    """تسكينٌ؛ تنوينُ النصب ألفًا؛ حذفُ تنوين الرفع والجرّ؛ تاءُ التأنيث هاءً — كما في كتب الوقف."""

    assert waqf("سكون", cells_of("نَعْبُدُ")) == cells_of("نَعْبُدْ")
    assert waqf("ألف", cells_of("سَبِيْلَنْ")) == (*cells_of("سَبِيْلَ"), ALIF)
    assert waqf("حذف", cells_of("ءَحَدُنْ")) == cells_of("ءَحَدْ")
    assert waqf("حذف", cells_of("جَاْنِبِنْ")) == cells_of("جَاْنِبْ")
    assert waqf("هاء", cells_of("رَحْمَتُنْ")) == cells_of("رَحْمَهْ")
    assert waqf("هاء", cells_of("ءَلْقِيَاْمَتِ")) == cells_of("ءَلْقِيَاْمَهْ")
    assert len(WAQF) == 4 and len({waqf(k, cells_of("رَحْمَتُنْ")) for k in WAQF}) == 4


def test_projection_composes_pause_then_junction() -> None:
    w = cells_of("ءَلْحَمْدُ")
    assert project(Hadd(False, False), True, "سكون", w) == w
    assert project(Hadd(True, False), True, "سكون", w) == w[1:]
    assert project(Hadd(True, False), False, "سكون", w) == w  # همزةُ قطعٍ لا تسقط
    assert project(Hadd(False, True), True, "سكون", w) == set_last(w, SUKUN)
    assert project(Hadd(True, True), True, "سكون", w) == set_last(w[1:], SUKUN)
    assert project(Hadd(True, True), True, "هاء", cells_of("ءَلْقِيَاْمَتِ")) == cells_of("لْقِيَاْمَهْ")


def test_restore_is_closed_under_projection_and_contains_the_form() -> None:
    """`project_restore` و`self_mem_restore` و`restore_length_le` على صورٍ شاهدة."""

    forms = [cells_of("لْلَهِ"), cells_of("نَعْبُدْ"), cells_of("ءَحَدْ"), cells_of("رَحْمَهْ"),
             (*cells_of("سَبِيْلَ"), ALIF), cells_of("لْقِيَاْمَهْ"), cells_of("كَتَبَ")]
    for h in HADDS:
        for x in forms:
            if h.pause and x[-1][1] != SUKUN:
                continue
            cands = restore(h, x)
            assert x in cands and len(cands) <= 39 and len(set(cands)) == len(cands)
            for u in cands:
                assert any(project(h, b, k, u) == x for b in (False, True) for k in WAQF), (h, x, u)
    assert restore(Hadd(False, False), cells_of("كَتَبَ")) == (cells_of("كَتَبَ"),)
    assert restore(Hadd(True, False), cells_of("كَتَبَ")) == (cells_of("كَتَبَ"),)  # لا ساكنَ في الصدر
    assert restore(Hadd(True, False), cells_of("لْلَهِ"))[0] == cells_of("ءَلْلَهِ")
    assert cells_of("سَبِيْلَنْ") in restore(Hadd(False, True), (*cells_of("سَبِيْلَ"), ALIF))
    assert cells_of("رَحْمَتُنْ") in restore(Hadd(False, True), cells_of("رَحْمَهْ"))
    assert cells_of("رَحْمَتَ") in restore(Hadd(False, True), cells_of("رَحْمَهْ"))
    assert cells_of("ءَحَدُنْ") in restore(Hadd(False, True), cells_of("ءَحَدْ"))
    assert cells_of("ءَحَدَنْ") not in restore(Hadd(False, True), cells_of("ءَحَدْ"))  # النصبُ ألفًا لا حذفًا


def test_classify_names_the_relation_with_its_condition() -> None:
    al = cells_of("ءَلْحَمْدُ")
    assert classify(al, al) == (False, None) and classify(al, al[1:]) == (True, None)
    assert classify(al, set_last(al[1:], SUKUN)) == (True, "سكون")
    assert classify(cells_of("سَبِيْلَنْ"), (*cells_of("سَبِيْلَ"), ALIF)) == (False, "ألف")
    assert classify(cells_of("ءَحَدُنْ"), cells_of("ءَحَدْ")) == (False, "حذف")
    assert classify(cells_of("رَحْمَتُنْ"), cells_of("رَحْمَهْ")) == (False, "هاء")
    assert classify(cells_of("ءَلْقِيَاْمَتِ"), cells_of("لْقِيَاْمَهْ")) == (True, "هاء")
    # لا تُسمّى علاقةٌ بلا شرطها: حذفُ آخرٍ ليس تنوينًا، أو ألفٌ عن غير تنوين نصب، أو كلمةٌ أخرى
    assert classify(cells_of("مِنْ"), cells_of("مِ")) is None
    assert classify(cells_of("كَتَبَ"), cells_of("كَتَبْ")) == (False, "سكون")
    assert classify(cells_of("كَتَبَ"), cells_of("ذَهَبَ")) is None
    assert classify(cells_of("نَعْبُدُ"), cells_of("نَعْبُدُ")[1:]) is None  # لا همزةَ تسقط
    assert relation(None) == "غير ذلك" and relation((True, "ألف")) == "ساقطة الوصل، وقف ألف"


def test_every_position_of_the_mushaf_has_a_named_relation() -> None:
    """المودَعان على المواقع نفسِها: كلُّ موقعٍ جاهزٍ في الحالين علاقتُه مسمّاة، والردُّ يحوي الأصلَ إلّا
    حيث تُخطئ قاعدةُ الهمزة حركتَها (مثلان في الصدر: اتَّخَذَ، اثَّاقَلْتُمْ) — وهي معدودةٌ باسمها (127 بعد
    سدّ التقاء الساكنين في الغانم: 78,188 موقعًا جاهزًا في الحالين؛ كانت 96 على 75,431)."""

    with gzip.open(DATA / "corpus-certificates.json.gz", "rt", encoding="utf-8") as f:
        start = json.load(f)
    with gzip.open(DATA / "context-certificates.json.gz", "rt", encoding="utf-8") as f:
        ctx = json.load(f)
    assert start["tokens"] == ctx["tokens"] == 78245 and sum(ctx["line_lengths"]) == 78245
    sf = [tuple((a, b) for a, b in x["cells"]) for x in start["forms"]]
    cf = [tuple((a, b) for a, b in x["cells"]) for x in ctx["forms"]]
    pos = unnamed = both = missed = 0
    for n in ctx["line_lengths"]:
        for i in range(n):
            s_idx, (c_idx, exit_, _, _) = start["stream"][pos], ctx["stream"][pos]
            pos += 1
            if s_idx < 0 or c_idx < 0:
                continue
            both += 1
            s, c, h = sf[s_idx], cf[c_idx], Hadd(i > 0, exit_ == 1)
            r = classify(s, c)
            if r is None:
                unnamed += 1
                continue
            if s not in restore(h, c):
                missed += 1
                # مثلان في الصدر (اتَّخَذَ، اثَّاقَلْتُمْ): `lift` يقرؤهما أل الشمسيّة والبوّابةُ تقرأ وصلَ الفعل
                assert r[0] and lift(c)[0] != s[0], (s, c)
                assert c[0][0] == c[1][0] and c[0][1] == SUKUN, (s, c)
    assert unnamed == 0 and both == 78188 and missed == 127


def test_mutations_are_refused() -> None:
    for bad in ("", "وقف", "ضم"):
        with pytest.raises(AssertionError):
            waqf(bad, cells_of("رَحْمَتُنْ"))
    assert TANWIN == ("ن", SUKUN)
