"""الصرف: الشبكة، والزوائد، والإعراب، والمقامات، والتصنيف."""

from __future__ import annotations

import random
from itertools import combinations

import pytest

from conftest import licensed_words
from slge.cells import ALPHABET, CELLS, SUKUN, Cell, is_cell, licensed, rho_admits
from slge.lexicon import MABNI, PARTICLES, WASL, entry
from slge.morphology import (
    GRID,
    GRID_NOM,
    MADI_SUFFIX,
    MUZARA_PREFIX,
    MUZARA_SUFFIX,
    OPS,
    PREFIX,
    SUFFIX,
    classify,
    conjugate,
    generate,
    iirab,
)

TEMPLATES = {**GRID, **GRID_NOM}


def _root(tid: str) -> str:
    keys = {k for kind, k, _ in TEMPLATES[tid] if kind == "s"}
    return "دحرج"[: max("فعلم".index(k) for k in keys) + 1] if "م" in keys else \
        "كتب"[: max("فعلم".index(k) for k in keys) + 1]


def _fixed_cells() -> list[Cell]:
    cells = [(k, s) for t in TEMPLATES.values() for kind, k, s in t if kind == "f"]
    for table in (*PREFIX, *SUFFIX, *MADI_SUFFIX.values(), *MUZARA_PREFIX.values(),
                  *MUZARA_SUFFIX.values()):
        cells += list(table)
    cells += [c for row, _, _ in OPS for c in row]
    return cells


def test_every_template_generates_licensed_words() -> None:
    for tid in TEMPLATES:
        assert licensed(generate(tid, _root(tid))), tid


def test_equivariance_all_transpositions() -> None:
    rng = random.Random(116)
    roots = ["".join(rng.choice(ALPHABET) for _ in range(4)) for _ in range(30)]
    for tid, tpl in TEMPLATES.items():
        n = len(_root(tid))
        for a, b in combinations(ALPHABET, 2):
            swap = {a: b, b: a}
            for root in roots:
                r = root[:n]  # n = عددُ مواضع الجذر في القالب
                left = [((swap.get(c, c), s) if kind == "s" else (c, s))
                        for (kind, _, _), (c, s) in zip(tpl, generate(tid, r), strict=True)]
                right = generate(tid, "".join(swap.get(c, c) for c in r))
                assert left == right, (tid, a, b, r)


def test_iirab_touches_only_last_cell() -> None:
    for n in (1, 2):
        for w in licensed_words(n):
            for case in ("رفع", "نصب", "جر"):
                v = iirab(w, case)
                assert v[:-1] == list(w[:-1]) and licensed(v)


def test_no_forbidden_cell_in_any_table() -> None:
    assert all(rho_admits(c) for c in _fixed_cells())


def test_tables_are_closed_in_116() -> None:
    assert all(is_cell(c) for c in _fixed_cells())
    assert all(s in {"فتح", "كسر", "ضم", SUKUN} for t in TEMPLATES.values() for *_, s in t)


def test_every_used_cell_respects_rho() -> None:
    used = set(_fixed_cells())
    for label in (*PARTICLES, *MABNI):
        used |= set(entry(label))
    assert all(rho_admits(c) for c in used)
    assert ("و", "فتح") in used and ("ي", "فتح") in used  # الواو والياء تتحرّكان
    assert used <= set(CELLS)


def test_ops_are_one_table() -> None:
    assert len(OPS) == 22
    assert set(PREFIX) == {r for r, p, _ in OPS if p == "مقدمة"}
    assert set(SUFFIX) == {r for r, p, _ in OPS if p == "خاتمة"}


@pytest.mark.parametrize("tense", ["ماضٍ", "مضارع"])
def test_conjugation_is_licensed_for_every_person(tense: str) -> None:
    for person in MADI_SUFFIX:
        assert licensed(conjugate("كتب", tense, person))


def test_classify_examples_from_the_original() -> None:
    assert classify([("ب", "كسر"), ("م", "فتح"), ("ن", SUKUN)])[0] == "bin1"
    sunnati = [("ل", "كسر"), ("س", "ضم"), ("ن", SUKUN), ("ن", "فتح"), ("ت", "كسر")]
    assert classify(sunnati)[0] == "bin1"
    assert classify([("ب", "فتح")] * 7)[0] == "bin2"


def test_wasl_entries_are_marked() -> None:
    assert set(MABNI) >= WASL


KNOWN_LABEL_DISAGREEMENTS = {"MS-7 مُفَاعَلَة", "NS-1 يَفْعُلِيّ"}
"""قالبٌ يخالف رسمَ اسمه في غير الخانة الأخيرة (والأخيرةُ في الاسم صورةُ وقف).
MS-7: اللامُ ثابتٌ ساكن ‎(f، ل، سكون)‎ والرسمُ «لَ» موضعٌ جذريٌّ متحرّك.
NS-1: الفاءُ مفتوحةٌ في القالب ساكنةٌ في الرسم «يَفْعُلِيّ».
سؤالان مفتوحان في `status.LEDGER` (GRID-NOM-labels)؛ لا يُصحَّحان هنا من الذاكرة."""


def test_nominal_templates_against_their_own_labels() -> None:
    from slge.orthography import to_atoms

    disagree = set()
    for tid, tpl in GRID_NOM.items():
        label = tid.split(" ", 1)[1]
        if to_atoms(label)[:-1] != [(k, s) for _, k, s in tpl][:-1]:
            disagree.add(tid)
    assert disagree == KNOWN_LABEL_DISAGREEMENTS
