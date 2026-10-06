"""مطابقةُ البايثون لتعريفات Lean، على مخرجات `lake exe slge-table` المودَعة في `formal/out/`.

ويفحص CI أنّ هذه المخرجاتِ هي ما يُخرجه Lean الآن (يعيد توليدها ثمّ `git diff --exit-code`)،
فتنتقل مبرهناتُ `formal/Slge/` إلى الدوالّ البايثونيّة بهذا التطابق.
"""

from __future__ import annotations

import csv
from pathlib import Path

from conftest import ROOT, licensed_words
from slge.cells import ALPHABET, CELLS, STATES, Cell, a116_code, count, fold, index, licensed
from slge.knowledge import Degree, Form, productive

OUT = ROOT / "formal" / "out"


def _rows(name: str) -> list[list[str]]:
    with Path(OUT / name).open(encoding="utf-8", newline="") as f:
        return list(csv.reader(f))


def _cell(i: int) -> Cell:
    return (ALPHABET[i // 4], STATES[i % 4])


def test_bridge_matches_lean() -> None:
    rows = _rows("bridge.csv")
    assert len(rows) == 116
    for (carrier, state, code), cell in zip(rows, CELLS, strict=True):
        assert (ALPHABET[int(carrier)], STATES[int(state)]) == cell
        assert int(code) == a116_code(cell)


def test_counts_match_lean() -> None:
    rows = _rows("counts.csv")
    assert [int(n) for n, _ in rows] == list(range(13))
    assert all(int(u) == count(int(n)) for n, u in rows)


def test_folds_match_lean() -> None:
    lean = {r[0]: int(r[1]) for r in _rows("folds.csv")}
    ours = {"-".join(str(index(c)) for c in w): fold(w)
            for n in (0, 1, 2) for w in licensed_words(n)}
    assert lean == ours  # المجموعتان واحدة: فالترخيصُ واحدٌ أيضًا على الطول ≤ 2
    assert all(_cell(int(i)) in CELLS for k in lean if k for i in k.split("-"))


def test_ghazali_matches_lean() -> None:
    names = {"akhass": Degree.اخص, "musawi": Degree.مساو}
    forms = {f.value: f for f in Form}
    rows = _rows("ghazali.csv")
    assert len(rows) == 8
    for d, f, p in rows:
        assert productive(names[d], forms[f]) == (p == "true")


def test_sequence_matches_lean() -> None:
    """`stream.encode_word` = `Sequence.encodeWord` على كلّ مرخَّصةٍ بطول ‎≤ 2‎،
    والعرضُ والكلفةُ كما في Lean،
    وكلُّ تيارٍ مرمَّزٍ يُفكّ بعينه (مرآةُ `decode_encode`)."""

    from slge.stream import cost, decode, encode, encode_word, width

    rows = _rows("sequence.csv")
    widths = {int(r[1]): (int(r[2]), int(r[3])) for r in rows if r[0] == "width"}
    assert widths == {k: (width(k), cost(k)) for k in (0, 1, 2)}
    lean = {r[0]: r[1] for r in rows if r[0] != "width"}
    ours = {"-".join(str(index(c)) for c in w): "".join("1" if b else "0" for b in encode_word(w))
            for n in (0, 1, 2) for w in licensed_words(n)}
    assert lean == ours
    words = [w for n in (1, 2) for w in licensed_words(n)][:500]
    assert decode(encode(words)) == [tuple(w) for w in words]


def test_categories_match_lean() -> None:
    """الضمائرُ الاثنا عشر خاناتٍ وأعدادًا = جدولُ `Categories.pronouns` في Lean."""

    from slge.categories import PRONOUNS, fingerprints, pronoun

    rows = [r for r in _rows("categories.csv") if r[0] == "pronoun"]
    assert [r[1] for r in rows] == ["-".join(str(index(c)) for c in w) for w in PRONOUNS]
    assert [int(r[2]) for r in rows] == list(fingerprints())
    assert len(set(fingerprints())) == 12 and all(pronoun(w) for w in PRONOUNS)


def test_wazn_matches_lean() -> None:
    """الأوزانُ المودَعة (104) بميزانها خاناتٍ، ترخيصُها، وردُّها الأصلَ = جدولُ `Wazn.awzan`."""

    from slge.wazn import AWZAN, FAL, mizan, root_of

    rows = _rows("wazn.csv")
    assert len(rows) == len(AWZAN) == 113
    for r, w in zip(rows, AWZAN, strict=True):
        m = mizan(w.template)
        assert r[1] == "-".join(str(index(c)) for c in m), w.name
        assert r[2] == "true" and licensed(m), w.name
        assert r[3] == "-".join(str(ALPHABET.index(c)) for c in FAL)
        assert root_of(w.template, m) == FAL


def test_shabaka_matches_lean() -> None:
    """حوافُّ البصريّين: (ابن، أب، عددُ العمليّات، يبلغ الجذر) = جدولُ `Shabaka.edges`."""

    from slge.shabaka import CLASSICAL, ROOT, diff
    from slge.wazn import AWZAN

    names = [w.name for w in AWZAN]
    by = {w.name: w.template for w in AWZAN}
    rows = _rows("shabaka.csv")
    assert len(rows) == len(CLASSICAL) == 112 and names[29] == ROOT
    for r, (child, parent) in zip(rows, CLASSICAL.items(), strict=True):
        assert (int(r[0]), int(r[1])) == (names.index(child), names.index(parent))
        assert int(r[2]) == len(diff(by[parent], by[child])) and r[3] == "true"


def test_khamsa_matches_lean() -> None:
    """الصورُ الخمسَ عشرة خاناتٍ وأعدادًا = جدولُ `Khamsa.forms`."""

    from slge.khamsa import CASES, KHAMSA, form

    rows = _rows("khamsa.csv")
    forms = [form(s, c) for s in KHAMSA for c in CASES]
    assert [r[0] for r in rows] == ["-".join(str(index(c)) for c in w) for w in forms]
    assert [int(r[1]) for r in rows] == [fold(w) for w in forms]


def test_afal_matches_lean() -> None:
    """الصورُ الثلاثون (4 جذوع × ضمائرُها × 3 حالات) = جدولُ `Afal.forms`."""

    from slge.afal import MOODS, PRONOUNS, STEMS, agree, form

    rows = _rows("afal.csv")
    forms = [form(s, p, m) for s in STEMS for p in PRONOUNS if agree(s.prefix, p) for m in MOODS]
    assert len(rows) == len(forms) == 30
    assert [r[0] for r in rows] == ["-".join(str(index(c)) for c in w) for w in forms]
    assert [r[1] for r in rows] == ["true"] * 30


def test_rawabit_matches_lean() -> None:
    """الأدواتُ السبعون خاناتٍ وعملًا واتّصالًا = جدولُ `Rawabit.particles`."""

    from slge.rawabit import PARTICLES

    rows = _rows("rawabit.csv")
    amal = {"": "none", "جزم": "jazm", "نصب": "nasb", "جرّ": "jarr",
            "نصب الاسم ورفع الخبر": "nasbIsm"}
    assert len(rows) == len(PARTICLES) == 70
    for r, p in zip(rows, PARTICLES, strict=True):
        assert r[0] == p.name and r[1] == "-".join(str(index(c)) for c in p.cells)
        assert r[2] == amal[p.amal] and r[3] == str(p.proclitic).lower() and r[4] == "true"
