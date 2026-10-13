"""ألفُ التأنيث زيادةٌ بعد الأصول — مرآةُ `A116.Tanith` (ADR ٥٣).

الهيكلُ حروفُ الكلمة بلا حركات (حواملُ ذرّات الشهادة: `skeleton`)؛ آخرُه ألفٌ فمقصورٌ مرشَّح، أو ألفٌ
ثمّ همزة فممدودٌ مرشَّح (`final_alif`)؛ وهو ألفُ تأنيثٍ إن وقعت الأصولُ بترتيبها فيما قبله (`in_order`)
بالمطابقة المسمّاة (`rad_match`). والشكلُ وحدَه (`shape`) لا يفرّق «أَبْنَاء» من «أَصْدِقَاء»
(`A116.Tanith.no_shape_function`)؛ الجذرُ يفرّق.
"""

from __future__ import annotations

from typing import Final

HAMZA_LIKE: Final[frozenset[str]] = frozenset("ءأإؤئآاوي")
WEAK_LIKE: Final[frozenset[str]] = frozenset("ويای")
MAQSURA: Final[str] = "maqsura"
MAMDUDA: Final[str] = "mamduda"


def rad_match(r: str, c: str) -> bool:
    return r == c or (r in "وي" and c in WEAK_LIKE) or (r == "ء" and c in HAMZA_LIKE)


def in_order(sk: str, root: str) -> bool:
    i = 0
    for c in sk:
        if i < len(root) and rad_match(root[i], c):
            i += 1
    return i == len(root)


def final_alif(sk: str) -> tuple[str, str] | None:
    if sk.endswith("اء"):
        return MAMDUDA, sk[:-2]
    if sk.endswith(("ا", "ى")):
        return MAQSURA, sk[:-1]
    return None


def tanith(sk: str, root: str) -> str | None:
    f = final_alif(sk)
    return f[0] if f is not None and in_order(f[1], root) else None


def shape(sk: str) -> bool:
    return final_alif(sk) is not None


def skeleton(atoms: tuple[str, ...]) -> str:
    """حواملُ ذرّات الشهادة بترتيبها."""

    return "".join(a[0] for a in atoms)
