"""عددُ المرخَّص لكلّ طول بمصفوفة الانتقال (`A116.TawafiqMasfufa`، ADR ١١٦، STEP-0010).

`masfufa.csv` يطبعه Lean المترجَم (`lake exe a116-table masfufa`) ويطابقه CI: مصفوفتا الوصل والوقف
(42 × 42) ومتّجها القبول، والقيمُ للأطوال 0–14.

١. الضربُ هنا مستقلٌّ عن Lean: أعدادُ بايثون الصحيحة تضرب المصفوفةَ المطبوعة في متّجهها، ورأسُ الناتج
   (حالُ الابتداء أوّلًا) هو القيمةُ المطبوعة لكلّ طول.
٢. المرساة: الأطوالُ 1–3 هي أعدادُ `tawafiq.csv`؛ والثالثُ فيه يعيده `tests/test_tawafiq.py`
   بمرآة البوّابة (`gate.licence`) لا بـLean تحت `-m slow` وحدَه. والأطوالُ 4–14 لا مرساةَ لها خارج Lean
   (`LENGTH4_NO_INDEPENDENT_ANCHOR`).
٣. كلُّ صفٍّ مجموعُه 113 (`rows_113`).
٤. التكرارُ بمعاملاته مكتوبةً هنا باليد (84، 2436، 84): يصدق وصلًا من الطول الرابع ووقفًا من الخامس
   حتى الرابعَ عشرَ، ولا يصدق قبلهما (الحدُّ الأدنى للأساس في `base_wasl`، `base_waqf`)؛ والمعاملاتُ
   هي التي في نصّ المبرهنتين `wasl_rec`، `waqf_rec`.

الطفرات: `MUTANT_MATRIX_ENTRY` (مدخلٌ زائد) و`MUTANT_ACCEPT_FLIP` (حالٌ مقبولة تُرفض) طفرتا اتّساقٍ
للجدول المطبوع، و`MUTANT_REC_COEFF` (2437 بدل 2436) تقتل المعاملات.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "formal" / "a116" / "masfufa.csv"
TAWAFIQ = ROOT / "formal" / "a116" / "tawafiq.csv"
LEAN = ROOT / "formal" / "a116" / "A116" / "TawafiqMasfufa.lean"
COEFF = (84, 2436, 84)  # باليد: ‎x³ = 84x² + 2436x + 84‎


def load() -> tuple[dict[str, list[list[int]]], dict[str, list[int]], dict[int, tuple[int, int]]]:
    mats: dict[str, list[list[int]]] = {"W": [], "Q": []}
    acc: dict[str, list[int]] = {}
    vals: dict[int, tuple[int, int]] = {}
    for ln in TABLE.read_text(encoding="utf-8").splitlines():
        tag, *rest = ln.split(",")
        if tag in mats:
            mats[tag].append([int(x) for x in rest])
        elif tag in ("aW", "aQ"):
            acc[tag] = [int(x) for x in rest]
        elif tag == "val":
            vals[int(rest[0])] = (int(rest[1]), int(rest[2]))
    return mats, acc, vals


def powers(m: list[list[int]], a: list[int], k: int) -> list[int]:
    out, v = [], a
    for _ in range(k):
        out.append(v[0])
        v = [sum(x * y for x, y in zip(row, v)) for row in m]
    return out


def mismatches(mats: dict[str, list[list[int]]], acc: dict[str, list[int]],
               vals: dict[int, tuple[int, int]], coeff: tuple[int, int, int] = COEFF) -> list[str]:
    bad = []
    seq = {"W": powers(mats["W"], acc["aW"], 15), "Q": powers(mats["Q"], acc["aQ"], 15)}
    for n, (w, q) in vals.items():
        if seq["W"][n] != w or seq["Q"][n] != q:
            bad.append(f"val {n}")
    a, b, c = coeff
    for tag, start in (("W", 4), ("Q", 5)):
        s = seq[tag]
        holds = [k for k in range(12) if s[k + 3] == a * s[k + 2] + b * s[k + 1] + c * s[k]]
        if holds != list(range(start, 12)):
            bad.append(f"rec {tag} {holds}")
    return bad


def test_shape() -> None:
    mats, acc, vals = load()
    assert [len(mats["W"]), len(mats["Q"])] == [42, 42]
    assert all(len(r) == 42 for r in mats["W"] + mats["Q"])
    assert len(acc["aW"]) == len(acc["aQ"]) == 42 and sorted(vals) == list(range(15))


def test_rows_sum_113() -> None:
    mats, _acc, _vals = load()
    assert {sum(r) for r in mats["W"] + mats["Q"]} == {113}


def test_power_and_recurrence() -> None:
    assert mismatches(*load()) == []


def test_anchor_on_gate_mirror() -> None:
    _m, _a, vals = load()
    rows = {}
    for ln in TAWAFIQ.read_text(encoding="utf-8").splitlines()[1:]:
        n, *rest = ln.split(",")
        if n.isdigit():
            rows[int(n)] = (int(rest[1]), int(rest[2]))
    assert {n: vals[n] for n in (1, 2, 3)} == rows
    assert vals[0] == (1, 1)


def test_coefficients_in_lean_text() -> None:
    text = LEAN.read_text(encoding="utf-8")
    for name, shift in (("wasl_rec", (7, 6, 5, 4)), ("waqf_rec", (8, 7, 6, 5))):
        stmt = text[text.index(f"theorem {name}"):]
        stmt = " ".join(stmt[:stmt.index(":= by")].split())
        nums = [int(x) for x in re.findall(r"(\d+) \*", stmt)]
        assert nums == list(COEFF), name
        assert [int(x) for x in re.findall(r"\(n \+ (\d+)\)", stmt)] == list(shift), name


@pytest.mark.parametrize("name", ["MUTANT_MATRIX_ENTRY", "MUTANT_ACCEPT_FLIP", "MUTANT_REC_COEFF"])
def test_mutants_killed(name: str) -> None:
    mats, acc, vals = load()
    if name == "MUTANT_MATRIX_ENTRY":
        mats["W"][0][3] += 1
        assert mismatches(mats, acc, vals) != []
    elif name == "MUTANT_ACCEPT_FLIP":
        i = acc["aQ"].index(1, 1)
        acc["aQ"][i] = 0
        assert mismatches(mats, acc, vals) != []
    else:
        assert mismatches(mats, acc, vals, (84, 2437, 84)) != []
