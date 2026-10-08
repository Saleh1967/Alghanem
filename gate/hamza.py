"""الهمزة: كرسيُّها دالّةٌ في سياق الخانة — مرآةُ `formal/a116/A116/Hamza.lean`.

الهمزةُ حاملٌ كسائر الحوامل؛ وكرسيُّها (أ إ ؤ ئ ء) **رسمٌ مشتقٌّ** من: موضعها، حركتها، حركة ما قبلها،
أمدٌّ ما قبلها، أياءٌ هو، أواوٌ ما بعدها (`seat_of` = `Hamza.seatOf`، مطابَقٌ بجدول Lean على
الـ384 سياقًا). وما خالف القاعدةَ في الطبعة بقيّةٌ مسمّاة، لا تخمين — والمقيسُ على المصحف في
`tests/test_hamza.py`.

وتحديدُ «الابتداء» يحتاج معرفةَ اللواصق (وَ فَ بِ لِ كَ أَ سَ، و«ال»): وهذه معلَنةٌ هنا بالقاعدة
نفسِها التي في `residue.py`، لا بمعجم.
"""

from __future__ import annotations

from typing import Final

from .residue import _proclitics, clusters

__all__ = ["SEATS", "Ctx", "predict_seat", "seat_of"]

SEATS: Final[frozenset[str]] = frozenset("أإؤئء")
_MARKS: Final[dict[str, str]] = {
    "َ": "fatha", "ُ": "damma", "ِ": "kasra", "ْ": "sukun",
    "ً": "fatha", "ٌ": "damma", "ٍ": "kasra",
}
_STRENGTH: Final[dict[str, int]] = {"sukun": 0, "fatha": 1, "damma": 2, "kasra": 3}
_SEAT_OF_HARAKA: Final[dict[str, str]] = {"kasra": "ئ", "damma": "ؤ", "fatha": "أ", "sukun": "ء"}

Ctx = tuple[str, str, str, bool, bool, bool]
"""(pos, own, prev, prevLong, prevYa, nextWaw) — `Hamza.Ctx` بعينه."""


def seat_of(ctx: Ctx) -> str:
    """`Hamza.seatOf`: الكرسيُّ من السياق."""

    pos, own, prev, prev_long, prev_ya, next_waw = ctx
    if pos == "initial":
        return "إ" if own == "kasra" else "أ"
    if pos == "final":
        return "ء" if prev_long else _SEAT_OF_HARAKA[prev]
    if prev_long:
        if prev_ya:
            return "ئ"
        if own == "kasra":
            return "ئ"
        if own == "damma" and not next_waw:
            return "ؤ"
        return "ء"
    best = own if _STRENGTH[own] >= _STRENGTH[prev] else prev
    if best == "damma" and next_waw:
        return "ء"
    return _SEAT_OF_HARAKA[best]


def _mark(c: str) -> str:
    for ch in c[1:]:
        if ch in _MARKS:
            return _MARKS[ch]
    return "sukun"


def _initial(cl: list[str], i: int) -> bool:
    if i == 0:
        return True
    pre = cl[:i]
    last = pre[-1]
    if (len(pre) >= 2 and last[0] == "ل" and _mark(last) == "sukun"
            and (pre[-2][0] == "ٱ" or (pre[-2][0] == "ل" and _mark(pre[-2]) == "kasra"))):
        return True  # «ال» بعد وصلٍ أو بعد لام الجرّ
    if last[0] == "س" and _mark(last) == "fatha" and (i == 1 or _proclitics(pre[:-1])):
        return True  # سَأُرِيكُم
    return _proclitics(pre) and last[0] != "أ"  # همزةُ الاستفهام تجعل ما بعدها وسطًا


def context(cl: list[str], i: int) -> Ctx:
    """سياقُ الهمزة في الموضع ‎i‎ من عناقيد الصورة القانونيّة."""

    own = _mark(cl[i])
    final = i == len(cl) - 1
    if _initial(cl, i):
        return ("initial", own, "sukun", False, False, False)
    prev = cl[i - 1]
    prev_mark = _mark(prev)
    prev_long = prev[0] in "اوي" and prev_mark == "sukun"
    next_waw = (not final) and cl[i + 1][0] == "و"
    return ("final" if final else "medial", own, prev_mark, prev_long, prev[0] == "ي", next_waw)


def predict_seat(canonical: str, i: int) -> str:
    """كرسيُّ الهمزة في الموضع ‎i‎ من الصورة القانونيّة."""

    return seat_of(context(clusters(canonical), i))


def seat_census(surfaces: list[str]) -> dict[str, object]:
    """قاعدةُ الكرسيّ على رسومٍ مختومة: كم كرسيًّا وافقت القاعدةُ وأيُّ كراسٍ خالفت، عدًّا لا تخمينًا.

    تُقرأ الرسومُ من المدوّنة في `tests/test_hamza.py` و`tools/gen_claims.py`؛ هنا العدُّ وحدَه."""

    from gate import Refusal, enter
    from gate.residue import repair

    total, agree, miss = 0, 0, {}
    for s in sorted(surfaces):
        if isinstance(enter(s.encode("utf-8")), Refusal):
            continue
        canonical, _ = repair(s)
        cl = clusters(canonical)
        for i, c in enumerate(cl):
            if c[0] in SEATS:
                total += 1
                if predict_seat(canonical, i) == c[0]:
                    agree += 1
                else:
                    miss[c[0]] = miss.get(c[0], 0) + 1
    return {"seats": total, "by_rule": agree, "miss": dict(sorted(miss.items()))}
