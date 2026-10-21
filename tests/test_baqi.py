"""المتبقّي (ADR ١٢٢، `A116/Baqi.lean`) مطابَقًا بتعدادٍ مستقلّ للاستكمالات.

* **الجدول** `formal/a116/baqi.csv`: تطبعه `lake exe a116-table baqi`.
  * صفوفُه كلُّ صيغةٍ بعمقٍ ≤ 2 على ⊤ و⊥ وذرّتين، مع كلّ أدلّةٍ ثلاثيّة على الذرّتين.
  * لكلّ صفٍّ الحكمُ والمطلوبُ الأدنى من Lean.
* **الشاهدُ المستقلّ** مكتوبٌ هنا ولا يقرأ شيفرةَ Lean:
  * محلّلٌ للصيغة، وتقييمٌ ثلاثيٌّ بجدولَي كليني.
  * وتعدادٌ لكلّ مجموعةٍ من الذرّات المجهولة: الكافيةُ ما يستوفي الصيغةَ بإثباتها،
    والدنيا ما لا تحتوي كافيةً أصغر منها.
* **المطابقة:**
  * المطلوبُ الأدنى من Lean مجموعةً هو الدنيا بالتعداد.
  * والحكمُ هو التقييمُ الثلاثيّ، وهو إسقاطُ المطلوب: ‎{} ∈ M‎ مستوفًى، و‎M‎ فارغةٌ ممتنع، وإلّا لا حكم.
* **طفراتٌ على الجدول** (حذفُ خطّة، وإضافةُ خطّةٍ غير دنيا، وقلبُ الحكم) يلتقطها الفحصان؛
  وطفرتان على الشاهد (الفصلُ اقترانًا، وبلا تدنية) تُثبتان أنّه يميّز.
"""

from __future__ import annotations

import csv
from collections.abc import Callable
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "formal" / "a116" / "baqi.csv"
Val = str | None  # "P" "N" أو None


def parse(s: str) -> tuple:
    if s == "T":
        return ("T",)
    if s == "F":
        return ("F",)
    if s.startswith("a"):
        return ("a", int(s[1:]))
    assert s[0] == "(" and s[-1] == ")"
    depth = 0
    for i, ch in enumerate(s[1:-1], start=1):
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        elif ch in "&|" and depth == 0:
            return (ch, parse(s[1:i]), parse(s[i + 1:-1]))
    raise AssertionError(s)


def k_and(x: str, y: str) -> str:
    if "N" in (x, y):
        return "N"
    return "P" if x == y == "P" else "U"


def k_or(x: str, y: str) -> str:
    if "P" in (x, y):
        return "P"
    return "N" if x == y == "N" else "U"


def ev(f: tuple, e: dict[int, str], OR: Callable[[str, str], str] = k_or) -> str:
    if f[0] == "T":
        return "P"
    if f[0] == "F":
        return "N"
    if f[0] == "a":
        return e[f[1]]
    a, b = ev(f[1], e, OR), ev(f[2], e, OR)
    return k_and(a, b) if f[0] == "&" else OR(a, b)


def minimal(f: tuple, e: dict[int, str], OR: Callable[[str, str], str] = k_or,
            keep_all: bool = False) -> set[frozenset[int]]:
    unknown = [a for a in (0, 1) if e[a] == "U"]
    suff = []
    for k in range(len(unknown) + 1):
        for T in combinations(unknown, k):
            e2 = dict(e)
            for a in T:
                e2[a] = "P"
            if ev(f, e2, OR) == "P":
                suff.append(frozenset(T))
    if keep_all:
        return set(suff)
    return {s for s in suff if not any(t < s for t in suff)}


def lean_family(cell: str) -> set[frozenset[int]]:
    if cell == "":
        return set()
    out = set()
    for part in cell.split("/"):
        out.add(frozenset() if part == "{}" else frozenset(int(x[1:]) for x in part.split("+")))
    return out


def rows() -> list[dict[str, str]]:
    with TABLE.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


ROWS = rows()


def test_table_size() -> None:
    # الصيغُ بعمقٍ ≤ 2 متمايزةً: ‎4‎ أوراقٍ و‎2·36²‎ عقدةً فوق ما عمقُه ≤ 1 (‎36 = 4 + 2·4²‎)،
    # أي ‎2596‎؛ × ‎3² = 9‎ أدلّة.
    forms = {r["sigha"] for r in ROWS}
    assert len(forms) == 4 + 2 * 36 ** 2 == 2596
    assert len(ROWS) == len({(r["sigha"], r["e0"], r["e1"]) for r in ROWS}) == 2596 * 9


def family_mismatches(rows: list[dict[str, str]]) -> int:
    return sum(1 for r in rows
               if lean_family(r["matlub"]) != minimal(parse(r["sigha"]), {0: r["e0"], 1: r["e1"]}))


def hukm_mismatches(rows: list[dict[str, str]]) -> int:
    bad = 0
    for r in rows:
        M = lean_family(r["matlub"])
        proj = "P" if frozenset() in M else ("N" if not M else "U")
        if not r["hukm"] == ev(parse(r["sigha"]), {0: r["e0"], 1: r["e1"]}) == proj:
            bad += 1
    return bad


def test_minimal_family_matches_enumeration() -> None:
    assert family_mismatches(ROWS) == 0


def test_hukm_is_kleene_and_projection() -> None:
    assert hukm_mismatches(ROWS) == 0


def test_table_mutants_caught() -> None:
    """طفراتٌ على الجدول المطبوع من Lean، كلٌّ في صفٍّ واحد.

    حذفُ خطّة، وإضافةُ خطّةٍ غير دنيا، وقلبُ الحكم.
    """
    two = next(i for i, r in enumerate(ROWS)
               if r["matlub"].count("/") == 1 and len(set(r["matlub"].split("/"))) == 2)
    drop = [dict(r) for r in ROWS]
    drop[two]["matlub"] = drop[two]["matlub"].split("/")[0]
    assert family_mismatches(drop) == 1
    one = next(i for i, r in enumerate(ROWS) if r["matlub"] == "a0" and r["sigha"] == "a0")
    add = [dict(r) for r in ROWS]
    add[one]["matlub"] = "a0/a0+a1"
    assert family_mismatches(add) == 1
    flip = [dict(r) for r in ROWS]
    flip[one]["hukm"] = "N"
    assert hukm_mismatches(flip) == 1


def test_u_hides_the_name() -> None:
    """صفّان بحكم «لا حكم» نفسِه ومطلوبين مختلفين: الاسمُ لا يُستردّ من الحكم."""
    a0 = next(r for r in ROWS if r["sigha"] == "a0" and r["e0"] == r["e1"] == "U")
    a1 = next(r for r in ROWS if r["sigha"] == "a1" and r["e0"] == r["e1"] == "U")
    assert a0["hukm"] == a1["hukm"] == "U" and a0["matlub"] != a1["matlub"]


def test_mutant_or_as_and_refused() -> None:
    bad = sum(1 for r in ROWS
              if lean_family(r["matlub"]) != minimal(parse(r["sigha"]), {0: r["e0"], 1: r["e1"]},
                                                     OR=k_and))
    assert bad > 0


def test_mutant_without_minimality_refused() -> None:
    bad = sum(1 for r in ROWS
              if lean_family(r["matlub"]) != minimal(parse(r["sigha"]), {0: r["e0"], 1: r["e1"]},
                                                     keep_all=True))
    assert bad > 0


def test_lean_witness_text() -> None:
    """فحصٌ نصّيٌّ لشاهد Lean (ليس من المطابقة): الثاني يُعاد هنا بالتعداد على ثلاث ذرّات."""
    A, B, C = ("a", 0), ("a", 1), ("a", 2)
    f = ("&", ("|", A, B), ("|", A, C))
    unknown = (0, 1, 2)
    suff = [frozenset(T) for k in range(4) for T in combinations(unknown, k)
            if ev(f, {a: ("P" if a in T else "U") for a in unknown}) == "P"]
    assert {s for s in suff if not any(t < s for t in suff)} == {frozenset({0}), frozenset({1, 2})}
    lean = (ROOT / "formal" / "a116" / "A116" / "Baqi.lean").read_text(encoding="utf-8")
    assert "= [[0], [1]] ∧" in lean and "= [[0], [1, 2]] := by" in lean
    assert "sorry" not in lean
