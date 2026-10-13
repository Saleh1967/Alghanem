"""بوّاباتُ المعنى (ADR ٥٥): الزمنُ والعطفُ والتخصيصُ والعمومُ — مرآةُ `formal/Slge/Bawwabat.lean`.

كلُّ بوّابةٍ بمفتاحها في `bawwabat_table` (عباراتُها في سطرٍ واحد من ج3 المختوم)، والمعنى هنا قراءةُ تلك
العبارات
لا غيرُها. لا نصَّ يدخل: الأدواتُ تُسمّى بأسمائها في Lean ويُربط كلٌّ منها بفهرسه في جدول الحروف الموحَّد.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import Final, TypeVar

from slge.bawwabat_table import KEYS
from slge.huruf import TABLE as HURUF

__all__ = [
    "ADAT", "ATF", "DAWR", "HAYAA", "SIYAGH", "Azmina", "apply", "ghaya", "istithna",
    "mafhum_shart", "nakira_nafy", "qalb", "reach", "shart", "sidq", "sifa", "takhlis", "umum",
    "zaman_of",
]

T = TypeVar("T")

Azmina = tuple[bool, bool, bool, bool]
"""(ماضٍ، ماضٍ قريبٌ من الحال، حال، مستقبل)."""

PAST: Final[Azmina] = (True, True, False, False)
HAL_MUSTAQBAL: Final[Azmina] = (False, False, True, True)
MUSTAQBAL: Final[Azmina] = (False, False, False, True)
HAL: Final[Azmina] = (False, False, True, False)
QARIB: Final[Azmina] = (False, True, False, False)

HAYAA: Final[tuple[str, ...]] = ("madi", "mudari", "amr")
ADAT: Final[tuple[str, ...]] = ("sin", "sawfa", "an", "inShart", "la", "lan", "lam", "lamma", "ma",
                                "inNafy", "qad")

ADAT_KEY: Final[dict[str, str]] = {
    "sin": "Z_FIL", "sawfa": "Z_FIL", "an": "T_ISTIQBAL", "inShart": "T_ISTIQBAL", "la": "N_LA",
    "lan": "N_LAN", "lam": "N_LAM", "lamma": "N_LAM", "ma": "N_MA", "inNafy": "N_IN",
    "qad": "T_QAD"}
ADAT_HARF: Final[dict[str, int]] = {
    "sin": 45, "sawfa": 46, "an": 31, "inShart": 43, "la": 61, "lan": 63, "lam": 62, "lamma": 40,
    "ma": 60, "inNafy": 64, "qad": 48}
NAFY: Final[frozenset[str]] = frozenset({"la", "lan", "lam", "lamma", "ma", "inNafy"})

_APPLY: Final[dict[tuple[str, str], Azmina]] = {
    **{(a, "mudari"): MUSTAQBAL for a in ("sin", "sawfa", "an", "inShart", "la", "lan")},
    ("lam", "mudari"): PAST, ("lamma", "mudari"): PAST,
    ("ma", "mudari"): HAL, ("ma", "madi"): QARIB,
    ("inNafy", "mudari"): HAL, ("inNafy", "madi"): HAL,
    ("qad", "madi"): QARIB,
}


def zaman_of(h: str) -> Azmina | None:
    """زمنُ الهيئة؛ الأمرُ لا يسمّي النصُّ زمنَه (`AMR_TIME_UNSOURCED`)."""

    return {"madi": PAST, "mudari": HAL_MUSTAQBAL}.get(h)


def apply(a: str, h: str) -> Azmina | None:
    return _APPLY.get((a, h))


def _sub(x: Azmina, y: Azmina) -> bool:
    return all(not i or j for i, j in zip(x, y, strict=True))


def _disj(x: Azmina, y: Azmina) -> bool:
    return not any(i and j for i, j in zip(x, y, strict=True))


def takhlis(a: str, h: str) -> bool:
    z, t = apply(a, h), zaman_of(h)
    return z is not None and t is not None and _sub(z, t)


def qalb(a: str, h: str) -> bool:
    z, t = apply(a, h), zaman_of(h)
    return z is not None and t is not None and _disj(z, t)


def _dedup(xs: Iterable[T]) -> list[T]:
    out: list[T] = []
    for x in xs:
        if x not in out:
            out.append(x)
    return out


def reach() -> list[Azmina]:
    hs = [z for h in HAYAA if (z := zaman_of(h)) is not None]
    ps = [z for a in ADAT for h in HAYAA if (z := apply(a, h)) is not None]
    return _dedup(hs + ps)


# ٢. العطف

ATF: Final[tuple[str, ...]] = ("waw", "fa", "thumma", "hatta", "aw", "am", "la", "bal", "lakin")
ATF_KEY: Final[dict[str, str]] = {
    "waw": "A_WAW", "fa": "A_FA", "thumma": "A_THUMMA", "hatta": "A_HATTA", "aw": "A_AW",
    "am": "A_AM", "la": "A_MUKHALAFA", "bal": "A_MUKHALAFA", "lakin": "A_MUKHALAFA"}
ATF_HARF: Final[dict[str, int]] = {t: 49 + i for i, t in enumerate(ATF)}


def sidq(t: str, a: bool, b: bool, ta: int, tb: int) -> bool:
    """صدقُ العطف على الواقعة (صدقُ الجزأين ووقتاهما)."""

    if t == "waw":
        return a and b
    if t == "fa":
        return a and b and tb == ta + 1
    if t == "thumma":
        return a and b and ta + 1 < tb
    if t == "hatta":
        return a and b and ta < tb
    if t in ("aw", "am"):
        return a or b
    if t in ("la", "bal", "lakin"):
        return a != b
    raise KeyError(t)


# ٣. التخصيص

Pred = Callable[[T], bool]


def istithna(amm: Pred[T], m: Pred[T], x: T) -> bool:
    return amm(x) and not m(x)


def shart(amm: Pred[T], c: Pred[T], x: T) -> bool:
    return amm(x) and c(x)


def mafhum_shart(amm: Pred[T], c: Pred[T], x: T) -> bool:
    return amm(x) and not c(x)


def sifa(amm: Pred[T], s: Pred[T], x: T) -> bool:
    return amm(x) and s(x)


def ghaya(amm: Pred[int], g: int, x: int) -> bool:
    """الغايةُ تُخرج ما بعدها، والحدُّ نفسُه بعدها."""

    return amm(x) and x < g


def nakira_nafy(p: Pred[T], dom: Iterable[T]) -> bool:
    return not any(p(x) for x in dom)


# ٤. العموم

SIYAGH: Final[tuple[str, ...]] = ("أي", "كل", "جميع", "الذين", "اللاتي", "من", "ما", "أين", "حيث",
                                  "متى")
DAWR: Final[tuple[str, ...]] = ("shart", "istifham", "mawsul", "mawsuf", "hal", "munada", "taajjub")


def umum(s: str, d: str) -> str | None:
    if s == "أي":
        return "kull" if d in ("shart", "istifham") else None
    if s == "من":
        return "aqil" if d in ("shart", "istifham") else None
    if s == "ما":
        return None if d in ("mawsuf", "taajjub") else "ghayrAqil"
    if s in ("أين", "حيث"):
        return "amkina"
    if s == "متى":
        return "zaman"
    return "kull" if s in SIYAGH else None


def _check() -> None:
    assert all(k in KEYS for k in ADAT_KEY.values()) and all(k in KEYS for k in ATF_KEY.values())
    assert all(i < len(HURUF) for i in (*ADAT_HARF.values(), *ATF_HARF.values()))


_check()
