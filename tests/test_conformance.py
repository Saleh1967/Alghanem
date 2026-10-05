"""مطابقةُ البايثون لتعريفات Lean، على مخرجات `lake exe slge-table` المودَعة في `formal/out/`.

ويفحص CI أنّ هذه المخرجاتِ هي ما يُخرجه Lean الآن (يعيد توليدها ثمّ `git diff --exit-code`)،
فتنتقل مبرهناتُ `formal/Slge/` إلى الدوالّ البايثونيّة بهذا التطابق.
"""

from __future__ import annotations

import csv
from pathlib import Path

from conftest import ROOT, licensed_words
from slge.cells import ALPHABET, CELLS, STATES, Cell, a116_code, count, fold, index
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


def test_rasm_matches_lean() -> None:
    """`to_rasm` هو `Rasm.write` رمزًا رمزًا، و`to_atoms` يعيد الخانات، على كلّ سلسلةٍ بطول ‎≤ 2‎."""

    from itertools import product

    from slge.orthography import to_atoms, to_rasm

    vowel = {"َ": 0, "ِ": 1, "ُ": 2, "ْ": 3}
    tanwin = {"ً": 0, "ٍ": 1, "ٌ": 2}
    seat = {"أ": {"َ": "H0", "ُ": "H2", "ً": "HT0", "ٌ": "HT2"}, "إ": {"ِ": "H1", "ٍ": "HT1"}}

    def glyphs(rasm: str) -> list[str]:
        out: list[str] = []
        i = 0
        while i < len(rasm):
            ch = rasm[i]
            nxt = rasm[i + 1] if i + 1 < len(rasm) else ""
            if ch == "آ":
                out.append("MADDA")
            elif ch == "ء":
                assert nxt == "ْ"
                out.append("H3")
                i += 1
            elif ch in seat:
                out.append(seat[ch][nxt])
                i += 1
            else:
                out.append(f"L{ALPHABET.index(ch)}")
                if nxt in vowel:
                    out.append(f"M{vowel[nxt]}")
                    i += 1
                elif nxt in tanwin:
                    out.append(f"T{tanwin[nxt]}")
                    i += 1
            i += 1
        return out

    lean = {row[0]: row[1] for row in _rows("rasm.csv")}
    assert len(lean) == 1 + 116 + 116 * 116
    for n in (0, 1, 2):
        for w in product(CELLS, repeat=n):
            key = "-".join(str(index(c)) for c in w)
            rasm = to_rasm(w)
            assert " ".join(glyphs(rasm)) == lean[key], (w, rasm)
            assert tuple(to_atoms(rasm)) == w, (w, rasm)
