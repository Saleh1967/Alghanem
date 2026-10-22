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


def depth(f: tuple) -> int:
    return 0 if f[0] in ("T", "F", "a") else 1 + max(depth(f[1]), depth(f[2]))


def domain() -> set[str]:
    """المجالُ المعلن مولَّدًا هنا من نحوه لا من الجدول: الأوراقُ ثمّ ‎(p&q)‎ و‎(p|q)‎ حتى العمق 2.

    وصفةُ التوليد هي وصفةُ `Main.lean` نفسُها، فلا تشهد عليها وحدها؛ والشاهدُ عليها `trees(2)`،
    توليدٌ ثانٍ عودًا بالعمق، يُطابَق بها في `test_domain_exact`.
    """
    d0 = ["T", "F", "a0", "a1"]

    def up(xs: list[str]) -> list[str]:
        return [f"({p}{op}{q})" for p in xs for q in xs for op in "&|"]
    d1 = d0 + up(d0)
    return set(d0 + up(d1))


def domain_violations(rows: list[dict[str, str]]) -> list[str]:
    """ما يخالف المجالَ المعلن.

    صيغةٌ خارجه أو فائتة، أو عمقٌ فوق 2، أو ذرّةٌ غير 0 و1، أو دليلٌ خارج P/N/U،
    أو صيغةٌ بغير البيئات التسع، أو صفٌّ مكرّر.
    """
    out: list[str] = []
    dom = domain()
    forms = {r["sigha"] for r in rows}
    out += [f"خارج:{x}" for x in sorted(forms - dom)] + [f"فائت:{x}" for x in sorted(dom - forms)]
    envs: dict[str, set[tuple[str, str]]] = {}
    keys = set()
    for r in rows:
        f = parse(r["sigha"])
        if depth(f) > 2:
            out.append(f"عمق:{r['sigha']}")

        def atoms(g: tuple) -> set[int]:
            return {g[1]} if g[0] == "a" else (set() if g[0] in "TF" else atoms(g[1]) | atoms(g[2]))
        if not atoms(f) <= {0, 1}:
            out.append(f"ذرّة:{r['sigha']}")
        if r["e0"] not in ("P", "N", "U") or r["e1"] not in ("P", "N", "U"):
            out.append(f"دليل:{r['sigha']}")
        envs.setdefault(r["sigha"], set()).add((r["e0"], r["e1"]))
        k = (r["sigha"], r["e0"], r["e1"])
        if k in keys:
            out.append(f"مكرّر:{k}")
        keys.add(k)
    nine = {(x, y) for x in "PNU" for y in "PNU"}
    out += [f"بيئات:{f}" for f, e in envs.items() if e != nine]
    return out


def trees(d: int) -> set[str]:
    """توليدٌ ثانٍ بطريقةٍ أخرى: كلُّ صيغةٍ عمقُها ‎≤ d‎ عودًا بالعمق، لا بوصفة `Main.lean`."""
    if d == 0:
        return {"T", "F", "a0", "a1"}
    sub = trees(d - 1)
    return sub | {f"({p}{op}{q})" for op in "|&" for p in sub for q in sub}


def test_domain_exact() -> None:
    """الجدولُ يغطّي المجالَ المعلن بعينه: كلُّ صيغةٍ فيه بالبيئات التسع، ولا شيءَ خارجه."""
    assert domain() == trees(2) and len(domain()) == 2596
    ds = [depth(parse(f)) for f in trees(2)]
    assert max(ds) == 2
    assert domain_violations(ROWS) == []


def test_mutant_equivalent_out_of_domain_refused() -> None:
    """طفرةُ المالك (2026-10-21 22:27): ‎T‎ مستبدَلةٌ بـ‎(((T&T)&T)&T)‎ تكافئها حكمًا ومطلوبًا؛ يقبلها
    فحصا الدلالة، ويرفضها فحصُ المجال باسمها."""
    rows = [dict(r) for r in ROWS]
    for r in rows:
        if r["sigha"] == "T":
            r["sigha"] = "(((T&T)&T)&T)"
    assert family_mismatches(rows) == 0 and hukm_mismatches(rows) == 0
    v = domain_violations(rows)
    assert "خارج:(((T&T)&T)&T)" in v and "فائت:T" in v and "عمق:(((T&T)&T)&T)" in v
    gone = [r for r in ROWS if r["sigha"] != "(a0&a1)"]
    assert "فائت:(a0&a1)" in domain_violations(gone)
    a2 = [dict(r) for r in ROWS]
    for r in a2:
        if r["sigha"] == "(a0|a1)":
            r["sigha"] = "(a0|a2)"
    assert "ذرّة:(a0|a2)" in domain_violations(a2)
    bad = [dict(r) for r in ROWS]
    bad[0]["e0"], bad[0]["e1"] = "", "PN"
    assert any(x.startswith("دليل:") for x in domain_violations(bad))
    dup = ROWS + ROWS[:1]
    assert any(x.startswith("مكرّر:") for x in domain_violations(dup))
    short = [r for r in ROWS if not (r["sigha"] == "a0" and r["e0"] == "N" and r["e1"] == "N")]
    assert "بيئات:a0" in domain_violations(short)


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
