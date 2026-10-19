"""فروعُ السلسلة وحملُ الحرف ومرشَّحو التقشير (ADR ١١٥): مرآةُ `tools/gen_silsila.py` مطابَقةٌ لجدول Lean
`furu.csv` (`lake exe a116-table furu`)، وحالاتٌ باليد، وطفرات.

* المطابقة: كلُّ سطرٍ هو مخرجُ المرآة على كلماتٍ ذرّاتُها مكتوبةٌ هنا باليد، وعلى صفوف
  `SilsilaFuru.maaniMithal` و`shWad` مكتوبةً هنا باليد.
* الطفرات (`MUTANT_*`): مرآةٌ مُفسَدة تُرقَّع فيسقط شرطُ المطابقة.
"""

from __future__ import annotations

import importlib.util
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "formal" / "a116" / "furu.csv"
_spec = importlib.util.spec_from_file_location("gen_silsila", ROOT / "tools" / "gen_silsila.py")
assert _spec and _spec.loader
S = importlib.util.module_from_spec(_spec)
sys.modules["gen_silsila"] = S
_spec.loader.exec_module(S)

ATOMS = {
    "بِسْمِ": ("بِ", "سْ", "مِ"), "وَلَاْ": ("وَ", "لَ", "اْ"),
    "وَبِلْغَيْبِ": ("وَ", "بِ", "لْ", "غَ", "يْ", "بِ"),
    "فَلِيَعْبُدُوْاْ": ("فَ", "لِ", "يَ", "عْ", "بُ", "دُ", "وْ", "اْ"),
    "كَمَثَلِ": ("كَ", "مَ", "ثَ", "لِ"), "لِلْ": ("لِ", "لْ"), "بِهِ": ("بِ", "هِ"),
    "ءِلَاْ": ("ءِ", "لَ", "اْ"), "ءِلْلَاْ": ("ءِ", "لْ", "لَ", "اْ"), "حَتْتَاْ": ("حَ", "تْ", "تَ", "اْ"),
    "مِنْ": ("مِ", "نْ"), "وَمَاْ": ("وَ", "مَ", "اْ"), "لَكُمْ": ("لَ", "كُ", "مْ"), "كَتَبَ": ("كَ", "تَ", "بَ"),
}
HIT = ("لا", "ما", "وما", "من", "لغيب", "يعبدوا")
J3, KIT = "nabhani", "sibawayh"
MAANI = [
    ("من", "لابتداء الغاية", [(J3, "469"), (KIT, "18417")]),
    ("من", "للتبعيض", [(J3, "469"), (KIT, "18419")]),
    ("من", "لبيان الجنس", [(J3, "469")]), ("من", "زائدة", [(J3, "469"), (KIT, "18421")]),
    ("و", "مبدلة عن باء الإلصاق", [(J3, "476"), (KIT, "18343")]),
    ("و", "لمطـلق الجـمـع لا تفيد ترتيباً ولا معية", [(J3, "486"), (KIT, "18333")]),
    ("رب", "للتقليل", [(J3, "475")]),
]
SHW = [(("صَ لَ اْ ت", "صلو"), ("lane", "0")), (("صَ لَ اْ ت", "صلو"), ("ibn-manzur", "1"))]
MANQUL = S.manqul()


def rows() -> list[list[str]]:
    return [ln.split(",") for ln in TABLE.read_text(encoding="utf-8").splitlines()]


def mn(h: Any) -> str:
    return "l" if h[0] == "l" else f"m:{h[1]}" if h[0] == "m" else "p:" + "|".join(h[1])


def mismatches() -> list[str]:
    bad = []
    for r in rows():
        if r[0] == "qashr":
            got = "|".join("".join(v) for v in S.qashr(ATOMS[r[1]]))
            want = r[2]
        elif r[0] == "key":
            got, want = S.harf_key(ATOMS[r[1]]), r[2]
        elif r[0] == "awwal":
            v = S.awwal(lambda x: S.harf_key(x) in HIT, ATOMS[r[1]])
            got, want = ("-" if v is None else "".join(v)), r[2]
        elif r[0] == "harf":
            m, _naw, rk = S.haml_harf(MAANI, r[1])
            got, want = f"{mn(m)},{rk}", ",".join(r[2:4])
        elif r[0] == "wad":
            out = S.haml_wad(MANQUL, SHW, "الصلاة", r[1].split("|"))
            got, want = "|".join(f"{x}:{rk}" for x, _n, rk in out), r[2]
        else:
            got, want = "?", ",".join(r)
        if got != want:
            bad.append(f"{','.join(r)} ≠ {got}")
    return bad


def test_table_shape() -> None:
    kinds = [r[0] for r in rows()]
    want = (14, 14, 14, 4, 3)
    assert tuple(kinds.count(k) for k in ("qashr", "key", "awwal", "harf", "wad")) == want


def test_mirror_matches_lean() -> None:
    assert mismatches() == []


def test_by_hand() -> None:
    assert S.qashr(("بِ", "سْ", "مِ")) == [("بِ", "سْ", "مِ"), ("ءِ", "سْ", "مِ")]
    assert S.qashr(("وَ", "بِ", "لْ", "غَ", "يْ", "بِ"))[1:] == [
        ("بِ", "لْ", "غَ", "يْ", "بِ"), ("لْ", "غَ", "يْ", "بِ")]
    assert S.harf_key(("حَ", "تْ", "تَ", "اْ")) == "حتا"
    assert S.haml_harf(MAANI, "رب") == (("m", "للتقليل"), "lughawiyya", "mafhum:zanni:nabhani:0")
    assert S.haml_harf(MAANI, "ءلا")[0] == ("l", "laHukm")
    assert S.jisr_wad([]) == "maluma:0"


def test_harf_from_deposit_is_lughawi() -> None:
    """حملُ كلّ حرفٍ في المودَع لغويٌّ ظنّيٌّ برأس شاهده من ج3، ومعانيه من صفوفه وحدَها."""
    hr = S.huruf()
    for k in {h for h, _m, _ws in hr}:
        m, naw, rk = S.haml_harf(hr, k)
        assert naw == "lughawiyya" and rk.startswith("mafhum:zanni:nabhani:")
        ms = (m[1],) if m[0] == "m" else m[1]
        assert set(ms) == {x for h, x, _ws in hr if h == k}
    assert S.haml_harf(hr, "ءلا")[0][0] == "p"


Fake = Callable[..., Any]


def _qishr_one(ps: Any, a: Any) -> Any:
    return a[1:] if a and a[0] in ps and len(a) > 1 else None


def _radd_lam(a: Any) -> Any:
    return ("ءِ",) + a if a and a[0][1:] == "ْ" else a


def _awwal_last(hit: Any, a: Any) -> Any:
    return next((v for v in reversed(S.qashr(a)) if hit(v)), None)


MUTANTS: dict[str, tuple[str, Callable[[Fake], Fake]]] = {
    "MUTANT_QISHR_ONE_CELL": ("qishr", lambda o: _qishr_one),
    "MUTANT_RADD_BEFORE_LAM": ("radd", lambda o: _radd_lam),
    "MUTANT_NO_RADD": ("radd", lambda o: lambda a: a),
    "MUTANT_HARFKEY_NO_COLLAPSE": ("harf_key", lambda o: lambda a: "".join(c[0] for c in a)),
    "MUTANT_AWWAL_LAST": ("awwal", lambda o: _awwal_last),
    "MUTANT_HARF_CHOOSES_FIRST": ("maani_harf", lambda o: lambda rows, k: o(rows, k)[:1]),
    "MUTANT_WAD_IGNORES_KEYS": ("haml_wad", lambda o: lambda m, sh, lafz, keys:
                                o(m, sh, lafz, [k for (k, _r), _s in sh])),
    "MUTANT_JISR_QATI": ("jisr_wad", lambda o: lambda ws: o(ws).replace("zanni", "qati")),
    "MUTANT_HARF_SHUHUD_DUPS": ("haml_harf", lambda o: lambda rows, k: (
        o(rows, k)[0], "lughawiyya", S.jisr_wad([w for h, _m, s in rows if h == k for w in s]))),
}


@pytest.mark.parametrize("name", sorted(MUTANTS))
def test_mutant_killed(name: str, monkeypatch: pytest.MonkeyPatch) -> None:
    attr, make = MUTANTS[name]
    monkeypatch.setattr(S, attr, make(getattr(S, attr)))
    assert mismatches() != []
