"""الجسرُ في `gate` (ADR ١١٣): `gate.mantuq` مطابَقٌ لجدول Lean `mantuq.csv` سطرًا سطرًا،
وحالاتٌ على ترميز البنّاء، وطفرات.

* المطابقة: كلُّ سطرٍ من `lake exe a116-table mantuq` (المودَع `formal/a116/mantuq.csv`) هو مخرجُ المرآة،
  ومنه تركيبُ الرتبة على مخرج الجسر نفسِه (`tarkib`).
* حالاتٌ على ترميز البنّاء، لا على النصّ: المطابقةُ للنصّ في `test_mantuq_mafhum.py`.
* الطفرات (`MUTANT_*`): مرآةٌ مُفسَدة تُرقَّع في `gate.mantuq` فيسقط شرطُ المطابقة.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest

import gate.mantuq as M

ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "formal" / "a116" / "mantuq.csv"
QAYD = {
    "sifa1": ("sifa", True, False), "sifa0": ("sifa", False, False),
    "shart": ("shart", False, False), "ghaya": ("ghaya", False, False),
    "adad1": ("adad", False, True), "adad0": ("adad", False, False),
    "ism": ("ism", False, False), "innama": ("innama", False, False),
}
MS = {"m1": M.MafhumUsul("mukhalafa", "أ"), "m2": M.MafhumUsul("mukhalafa", "ب")}
HS: dict[str, M.Hukm] = {"yumal:m1": M.Yumal(MS["m1"]), "layumal:ism": M.Layumal("ism")}


def mudaa(s: str) -> list[tuple[M.MafhumUsul, M.Shahada]]:
    if s == "none":
        return []
    out = []
    for part in s.split("|"):
        m, kind = part.split(":")
        t, w = kind.split("-")
        out.append((MS[m], M.Shahada(t, w)))
    return out


def show(h: M.Hukm) -> str:
    return f"yumal:{h.m.naw}" if isinstance(h, M.Yumal) else f"layumal:{h.mani}"


def rows() -> list[list[str]]:
    return [ln.split(",") for ln in TABLE.read_text(encoding="utf-8").splitlines()]


def mismatches() -> list[str]:
    bad = []
    for r in rows():
        if r[0] == "naw":
            got, want = M.naw(*(c == "1" for c in r[1])), r[2]
        elif r[0] == "mukhalafa":
            q, f, s = QAYD[r[1]]
            got = show(M.mukhalafa(q, "م", f, s, r[2][0] == "1", r[2][1] == "1"))
            want = r[3]
        elif r[0] == "martaba":
            d, h = mudaa(r[1]), HS[r[2]]
            got = ",".join([M.martaba_waqi(d, h), M.hukm_naql("wad", d, h),
                            M.hukm_naql("wad", d, h, True), M.hukm_naql("waqi", d, h)])
            want = ",".join(r[3:7])
        else:
            q, f, s = QAYD[r[1]]
            h = M.mukhalafa(q, r[3], f, s, r[2][0] == "1", r[2][1] == "1")
            got, want = M.martaba_waqi(mudaa(r[4]), h), r[5]
        if got != want:
            bad.append(f"{','.join(r)} ≠ {got}")
    return bad


def test_table_shape() -> None:
    kinds = [r[0] for r in rows()]
    counts = tuple(kinds.count(k) for k in ("naw", "mukhalafa", "martaba", "tarkib"))
    assert counts == (16, 32, 34, 96)


def test_mirror_matches_lean() -> None:
    assert mismatches() == []


def test_on_builder_encoding() -> None:
    assert M.mukhalafa("sifa", "م", mufhim=True) == M.Yumal(M.MafhumUsul("mukhalafa", "م"))
    assert M.mukhalafa("adad", "", siyaq=False) == M.Layumal("adadBilaSiyaq")
    assert M.mukhalafa("ism", "") == M.Layumal("ism")
    assert M.mukhalafa("sifa", "", mufhim=True, aghlab=True) == M.Layumal("aghlab")
    m = M.MafhumUsul("mukhalafa", "أ")
    other = [(M.MafhumUsul("mukhalafa", "ب"), M.Shahada("hiss", "waqiMakhtum"))]
    assert M.martaba_waqi(other, M.Yumal(m)) == "maluma"
    with pytest.raises(ValueError, match="QAYD_UNKNOWN"):
        M.mukhalafa("lafz", "")
    with pytest.raises(ValueError, match="JISR_UNKNOWN"):
        M.hukm_naql("aql", [], M.Yumal(m))


Fake = Callable[..., Any]


def _kafi_any(o: Fake) -> Fake:
    """الكفايةُ بأيّ شهادةٍ كافية بدل كلّها: تُحذف غيرُ الكافية قبل الحكم."""
    ok = ("wad", "malumat", "waqiMakhtum")
    return lambda j, d, h, t=False: o(j, [p for p in d if p[1].mawda in ok] or d, h, t)


def _malumat_not_kafi(o: Fake) -> Fake:
    """«المعلوماتُ السابقة» لا تكفي (خلافَ المادّة ١٥ المعدَّلة)."""
    def f(j: str, d: Any, h: Any, t: bool = False) -> Any:
        d2 = [(m, M.Shahada(s.tariq, "marjaMahjub") if s.mawda == "malumat" else s) for m, s in d]
        return o(j, d2, h, t)
    return f


# كلُّ طفرةٍ: اسمُ الدالّة في `gate.mantuq`، وصانعُ بديلٍ مُفسَدٍ من الأصل.
MUTANTS: dict[str, tuple[str, Callable[[Fake], Fake]]] = {
    "MUTANT_ADAD_IGNORES_SIYAQ": ("mani_qayd", lambda o: lambda q, f=False, s=False:
                                  None if q == "adad" else o(q, f, s)),
    "MUTANT_WITNESS_OF_OTHER": ("shuhud_for", lambda o: lambda d, m: [s for _, s in d]),
    "MUTANT_NAW_ORDER_SWAPPED": ("naw", lambda o: lambda a, b, c, d:
                                 "tanbih" if b else o(a, b, c, d)),
    "MUTANT_KAFI_ANY": ("hukm_naql", _kafi_any),
    "MUTANT_MALUMAT_NOT_KAFI": ("hukm_naql", _malumat_not_kafi),
    "MUTANT_TAWATUR_IGNORED": ("hukm_naql", lambda o: lambda j, d, h, t=False: o(j, d, h, False)),
    "MUTANT_MANA_FIXED": ("mukhalafa", lambda o: lambda q, mana, *a, **k: o(q, "أ", *a, **k)),
}


@pytest.mark.parametrize("name", sorted(MUTANTS))
def test_mutant_killed(name: str, monkeypatch: pytest.MonkeyPatch) -> None:
    attr, make = MUTANTS[name]
    monkeypatch.setattr(M, attr, make(getattr(M, attr)))
    assert mismatches() != []
