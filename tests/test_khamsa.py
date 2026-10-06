"""الأسماء الخمسة: الصورُ من القانون تطابق شهاداتِ البوّابة، والحالةُ تُقرأ من الصورة."""

from __future__ import annotations

import pytest

from slge.cells import STATES, licensed
from slge.khamsa import CASES, KHAMSA, WITNESS, Ctx, Stem, case_of, decline, form, tanwin, with_ya

BY = {s.name: s for s in KHAMSA}


def test_forms_match_gate_witnesses() -> None:
    assert form(BY["أب"], "رفع") == WITNESS["أَبُوهُمْ"][:3]
    assert form(BY["أب"], "نصب") == WITNESS["أَبَا"]
    assert form(BY["أب"], "جر") == WITNESS["أَبِي"]
    assert form(BY["أخ"], "رفع") == WITNESS["أَخُوهُمْ"][:3]
    assert form(BY["أخ"], "نصب") == WITNESS["أَخَا"]
    assert form(BY["أخ"], "جر") == WITNESS["أَخِي"]
    assert [form(BY["ذو"], c) for c in CASES] == [WITNESS["ذُو"], WITNESS["ذَا"], WITNESS["ذِي"]]
    assert tanwin(BY["أخ"], "رفع") == WITNESS["أَخٌ"]
    assert with_ya(BY["أب"]) == WITNESS["أَبِي"]


def test_case_is_read_back_from_every_form() -> None:
    for s in KHAMSA:
        for c in CASES:
            w = form(s, c)
            assert licensed(w) and case_of(w) == c
            assert case_of(tanwin(s, c)) is None  # التنوين لا يحمل الحالة في حرفه


def test_mutation_swapping_the_madd_letter_changes_the_case() -> None:
    w = list(form(BY["حم"], "رفع"))
    w[-1] = ("ي", STATES[3])
    assert case_of(tuple(w)) == "جر"
    w[-2] = ("م", STATES[0])  # حركةٌ لا تجانس الحرف: الصورةُ خارج القانون
    assert tuple(w) not in {form(BY["حم"], c) for c in CASES}


def test_conditions_decide_and_never_guess() -> None:
    ab = BY["أب"]
    assert decline(ab, Ctx(), "نصب") == form(ab, "نصب")
    assert decline(ab, Ctx(mudaf=False), "نصب") == tanwin(ab, "نصب")
    assert {decline(ab, Ctx(ila_ya=True), c) for c in CASES} == {with_ya(ab)}
    assert decline(ab, Ctx(mufrad=False), "رفع") is None  # الجمع: آبَاء خارج القانون
    assert decline(ab, Ctx(mukabbar=False), "رفع") is None  # التصغير: أُبَيّ
    with pytest.raises(ValueError):
        decline(ab, Ctx(), "جزم")


def test_fifteen_distinct_forms_and_stem_recovered() -> None:
    forms = [form(s, c) for s in KHAMSA for c in CASES]
    assert len(set(forms)) == 15
    assert isinstance(Stem("x", (), "ب"), Stem)
