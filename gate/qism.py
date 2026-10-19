"""تقسيمُ الكلم والقراءةُ بالفرز — مرآةُ `A116.Qism` (ADR ٥٤).

`ENDING` جدولُ آخر المعرب لكلّ (صنف، حالة) من الألفيّة؛ و`read` القارئُ السليمُ الأتمّ بمنظور
(`read_sound`، `read_best`)؛ والمنظوراتُ الثلاثة: بلا فرز، وبفرز الاسم من الفعل، وبالصنف.
و`ending_of` يقرأ الآخرَ المرئيّ من صورة الشهادة الخارجة من البوّابة (`gate.exit`) لا من نصٍّ لم
يمرّ بها: حركةُ الحرف الأخير (والتنوينُ حركتُه)، أو حرفُ مدٍّ ساكنٌ أخير، أو نونُ المثنّى والجمع
بما قبلها.
"""

from __future__ import annotations

from collections.abc import Callable, Hashable
from typing import Final

RAF, NASB, JARR, JAZM = "raf", "nasb", "jarr", "jazm"
IRABS: Final[tuple[str, ...]] = (RAF, NASB, JARR, JAZM)

ENDING: Final[dict[str, dict[str, str]]] = {
    "iSahih": {RAF: "damma", NASB: "fatha", JARR: "kasra"},
    "iSitta": {RAF: "waw", NASB: "alif", JARR: "ya"},
    "iMuthanna": {RAF: "ani", NASB: "ayni", JARR: "ayni"},
    "iJamM": {RAF: "una", NASB: "ina", JARR: "ina"},
    "iJamF": {RAF: "damma", NASB: "kasra", JARR: "kasra"},
    "iMamnu": {RAF: "damma", NASB: "fatha", JARR: "fatha"},
    "iMaqsur": {RAF: "alif", NASB: "alif", JARR: "alif"},
    "iManqus": {RAF: "ya", NASB: "fatha", JARR: "ya"},
    "fSahih": {RAF: "damma", NASB: "fatha", JAZM: "sukun"},
    "fKhamsaA": {RAF: "ani", NASB: "alif", JAZM: "alif"},
    "fKhamsaW": {RAF: "una", NASB: "waw", JAZM: "waw"},
    "fKhamsaY": {RAF: "ina", NASB: "ya", JAZM: "ya"},
    "fMutalAlif": {RAF: "alif", NASB: "alif", JAZM: "fatha"},
    "fMutalW": {RAF: "waw", NASB: "fatha", JAZM: "damma"},
    "fMutalY": {RAF: "ya", NASB: "fatha", JAZM: "kasra"},
}
CLASSES: Final[tuple[str, ...]] = tuple(ENDING)
PAIRS: Final[tuple[tuple[str, str], ...]] = tuple(
    (c, i) for c in CLASSES for i in IRABS if i in ENDING[c])


def is_ism(c: str) -> bool:
    return c.startswith("i")


def blind_view(c: str) -> Hashable:
    return ()


def qism_view(c: str) -> Hashable:
    return is_ism(c)


def class_view(c: str) -> Hashable:
    return c


VIEWS: Final[dict[str, Callable[[str], Hashable]]] = {
    "blind": blind_view, "qism": qism_view, "class": class_view}


def cands(view: Callable[[str], Hashable], k: Hashable, e: str) -> list[str]:
    return [i for c, i in PAIRS if view(c) == k and ENDING[c][i] == e]


def read(view: Callable[[str], Hashable], k: Hashable, e: str) -> str | None:
    cs = cands(view, k, e)
    return cs[0] if cs and all(x == cs[0] for x in cs) else None


def naive(e: str) -> str | None:
    return {"damma": RAF, "fatha": NASB, "kasra": JARR, "sukun": JAZM}.get(e)


def covered(view: Callable[[str], Hashable]) -> int:
    return sum(1 for c, i in PAIRS if read(view, view(c), ENDING[c][i]) == i)


# ── الآخرُ المرئيّ من صورة الشهادة ─────────────────────────────────────────────

FATHA, DAMMA, KASRA, SUKUN = "َ", "ُ", "ِ", "ْ"
TANWIN: Final[dict[str, str]] = {"ً": "fatha", "ٌ": "damma", "ٍ": "kasra"}
SHORT: Final[dict[str, str]] = {FATHA: "fatha", DAMMA: "damma", KASRA: "kasra", SUKUN: "sukun"}
MARKS: Final[frozenset[str]] = frozenset(chr(c) for c in range(0x064B, 0x0653)) | {"ٰ"}


def clusters(word: str) -> list[tuple[str, str]]:
    """(حرف، علاماتُه) بالترتيب."""

    out: list[tuple[str, str]] = []
    for ch in word:
        if ch in MARKS and out:
            out[-1] = (out[-1][0], out[-1][1] + ch)
        elif ch not in MARKS:
            out.append((ch, ""))
    return out


def _vowel(marks: str) -> str | None:
    for m in marks:
        if m in TANWIN:
            return TANWIN[m]
    for m in marks:
        if m in SHORT:
            return SHORT[m]
    return None


def _bare(marks: str) -> bool:
    return _vowel(marks) in (None, "sukun")


def ending_of(word: str) -> str | None:
    """الآخرُ المرئيّ لصورةٍ مشكولة، أو None إن لم يُقرأ."""

    cl = clusters(word)
    if not cl:
        return None
    last, marks = cl[-1]
    prev = cl[-2] if len(cl) > 1 else ("", "")
    if last == "ا" and _bare(marks):
        if prev[0] == "و" and len(cl) > 2 and _vowel(cl[-3][1]) == "damma":
            return "waw"  # ألفُ الفارقة بعد واو الجماعة
        if "ً" in prev[1]:
            return "fatha"  # ألفُ تنوين النصب
        return "alif" if _vowel(prev[1]) == "fatha" else None
    if last == "ى" and _bare(marks):
        return "alif" if _vowel(prev[1]) == "fatha" or "ً" in prev[1] else None
    if last == "و" and _bare(marks):
        return "waw" if _vowel(prev[1]) == "damma" else None
    if last == "ي" and _bare(marks) and "ّ" not in marks:
        return "ya" if _vowel(prev[1]) == "kasra" else None
    v = _vowel(marks)
    if last == "ن" and len(cl) > 2 and _bare(prev[1]):
        before = _vowel(cl[-3][1])
        if v == "kasra" and prev[0] == "ا" and before == "fatha":
            return "ani"
        if v == "kasra" and prev[0] == "ي" and before == "fatha":
            return "ayni"
        if v == "fatha" and prev[0] == "و" and before == "damma":
            return "una"
        if v == "fatha" and prev[0] == "ي" and before == "kasra":
            return "ina"
    return v
