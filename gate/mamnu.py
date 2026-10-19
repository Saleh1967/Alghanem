"""الممنوعُ من الصرف — مرآةُ `A116.Mamnu` (ADR ٥٥).

`mamnu(s)`: علّةٌ قويّة (ألفُ التأنيث، منتهى الجموع)، أو وصفٌ مع (فعلان، أفعل، عدل)، أو علَمٌ مع
ثانية — بلا تنوينٍ ولا أل. والشكلُ على (حرف، حركة) من صورة الشهادة: `muntaha_shape`،
`afal_shape`، `falan_shape`.
و`read_j` القارئُ بحرف الجرّ المتّصل (`readJ`).
"""

from __future__ import annotations

from typing import Final

from gate.qism import ENDING, clusters

STRONG: Final[tuple[str, ...]] = ("tanithAlif", "muntaha")
WASF_SECOND: Final[tuple[str, ...]] = ("falan", "afal", "adl")
ALAM_SECOND: Final[tuple[str, ...]] = ("tarkib", "falan", "tanith", "ajamiOver3", "waznFil", "adl")
ADL_WASF: Final[frozenset[str]] = frozenset(
    {"مثنى", "ثلاث", "رباع", "أخر", "أحاد", "موحد", "ثناء", "مثلث", "مربع"})
"""ما عُدل في الوصف (الألفيّة س7241–7242: «مثنى وثلاث وأخر … من واحد لأربع»)، هيكلًا."""


def mamnu(s: dict[str, bool]) -> bool:
    if s.get("tanwin") or s.get("al"):
        return False
    if any(s.get(k) for k in STRONG):
        return True
    if s.get("wasf") and any(s.get(k) for k in WASF_SECOND):
        return True
    return bool(s.get("alam") and any(s.get(k) for k in ALAM_SECOND))


HAMZA: Final[frozenset[str]] = frozenset("ءأإؤئ")
VOWEL: Final[dict[str, str]] = {"َ": "a", "ُ": "u", "ِ": "i", "ْ": "o",
                                "ً": "a", "ٌ": "u", "ٍ": "i"}


def word(surface: str) -> list[tuple[str, str]]:
    """(حرف، حركة) — الهمزةُ بكراسيّها «ء»، وحرفُ المدّ بلا علامةٍ ساكن."""

    out: list[tuple[str, str]] = []
    for ch, marks in clusters(surface):
        v = next((VOWEL[m] for m in marks if m in VOWEL), "")
        if not v and ch in "اوىي":
            v = "o"
        out.append(("ء" if ch in HAMZA else "ا" if ch == "ى" else ch, v or "none"))
    return out


def muntaha_shape(w: list[tuple[str, str]]) -> bool:
    core = w[:-1] if w and w[-1] == ("ا", "o") else w  # ألفُ تنوين النصب ليست من الوزن
    if len(core) == 5:
        a, b, c, d, _ = core
        return a[1] == "a" and b[1] == "a" and c == ("ا", "o") and d[1] == "i"
    if len(core) == 6:
        a, b, c, d, e, _ = core
        return (a[1] == "a" and b[1] == "a" and c == ("ا", "o") and d[1] == "i"
                and e == ("ي", "o"))
    return False


def afal_shape(w: list[tuple[str, str]]) -> bool:
    return len(w) == 4 and w[0] == ("ء", "a") and w[1][1] == "o" and w[2][1] == "a"


def falan_shape(w: list[tuple[str, str]]) -> bool:
    return (len(w) == 5 and w[0][1] == "a" and w[1][1] == "o" and w[2][1] == "a"
            and w[3] == ("ا", "o") and w[4][0] == "ن")


def has_tanwin(surface: str) -> bool:
    return any(m in surface for m in ("ً", "ٌ", "ٍ"))


def read_j(c: str, e: str) -> str | None:
    """`readJ`: بحرف جرٍّ متّصل الحالةُ جرٌّ إن كان الصنفُ يُظهر الجرَّ بهذا الآخر."""

    return "jarr" if ENDING[c].get("jarr") == e else None
