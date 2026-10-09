"""السياق: الكلمةُ في حدّها — إسقاطٌ وردّ؛ مرآةُ `Slge.Siyaq` (ADR ٢٨).

مودَعُ الغانم الثاني (`context-certificates.json.gz`) يحمل كلَّ موقعٍ من المصحف **بسياقه** (ابتداء/وصل،
استمرار/وقف). الكلمةُ من حيث هي تُسقَط إلى صورتها في الحدّ بعمليّتين: **الوقفُ** بأحد أوجهه الأربعة كما
طبعتها البوّابة (`WAQF`: تسكينُ الآخر؛ تنوينُ النصب ألفًا؛ حذفُ تنوين الرفع والجرّ مع التسكين؛ تاءُ
التأنيث هاءً ساكنة)، و**الوصلُ** يُسقط همزةَ الوصل (`project`؛ أهمزةُ وصلٍ هي وأيُّ وجهٍ للوقف؟ قراءتان
تُؤخذان معاملَين). والردُّ `restore` يعكسهما مرشَّحاتٍ: ما أوّلُه ساكنٌ في الوصل يُرفع بهمزةٍ على قاعدة
`sawabiq.lift` أو يبقى، وفي الوقف كلُّ ما يُسقَط إلى الصورة بوجهٍ من الأربعة — كلُّ مرشَّحٍ يُسقَط إلى
الصورة بعينها (`project_restore`) والصورةُ نفسُها مرشَّحة (`self_mem_restore`) والعددُ ≤ 26
(`restore_length_le`). و`classify` يسمّي علاقةَ صورة الابتداء بصورة السياق كما طبعتهما البوّابة.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from slge.cells import STATES, SUKUN, Cell
from slge.sawabiq import lift
from slge.zuruf import set_last

__all__ = ["WAQF", "Hadd", "classify", "project", "relation", "restore", "waqf"]

Word = tuple[Cell, ...]
WAQF: Final[tuple[str, ...]] = ("سكون", "ألف", "حذف", "هاء")
"""أوجهُ الوقف (`Waqf`): تسكينُ الآخر؛ تنوينُ النصب ألفًا؛ حذفُ التنوين مع التسكين؛ تاءُ التأنيث هاءً."""
TANWIN: Final[Cell] = ("ن", SUKUN)
_ALIF: Final[Cell] = ("ا", SUKUN)
_HA: Final[Cell] = ("ه", SUKUN)


@dataclass(frozen=True, slots=True)
class Hadd:
    """الحدُّ: وصلٌ (أم ابتداء) ووقفٌ (أم استمرار)."""

    joined: bool
    pause: bool


def waqf(kind: str, w: Word) -> Word:
    """الوقفُ بوجهه (`waqf`)."""

    if kind == "سكون":
        return set_last(w, SUKUN)
    if kind == "ألف":
        return (*w[:-1], _ALIF)
    if kind == "حذف":
        return set_last(w[:-1], SUKUN)
    assert kind == "هاء", kind
    u = w[:-1] if w and w[-1] == TANWIN else w
    return (*u[:-1], _HA)


def project(h: Hadd, wasl: bool, kind: str, w: Word) -> Word:
    """إسقاطُ الكلمة من حيث هي إلى صورتها في الحدّ (`project`): الوقفُ بوجهه ثمّ الوصلُ يُسقط الهمزة."""

    p = waqf(kind, w) if h.pause else w
    return p[1:] if h.joined and wasl else p


def _waqf_candidates(x: Word) -> tuple[Word, ...]:
    out: list[Word] = [set_last(x, s) for s in STATES]
    if x and x[-1] == _ALIF:
        out.append((*x[:-1], TANWIN))
    out += [(*set_last(x, "كسر"), TANWIN), (*set_last(x, "ضم"), TANWIN)]
    if x and x[-1] == _HA:
        out += [(*x[:-1], ("ت", s)) for s in STATES[:3]]
        out += [(*x[:-1], ("ت", s), TANWIN) for s in STATES[:3]]
    return tuple(out)


def _heads(h: Hadd, x: Word) -> tuple[Word, ...]:
    if h.joined and x and x[0][1] == SUKUN:
        return (lift(x), x)
    return (x,)


def restore(h: Hadd, x: Word) -> tuple[Word, ...]:
    """مرشَّحاتُ الكلمة من حيث هي من صورتها في الحدّ (`restore`)؛ عددُها ≤ 26 (`restore_length_le`)."""

    hs = _heads(h, x)
    if h.pause:
        return tuple(c for u in hs for c in _waqf_candidates(u))
    return hs


def classify(start: Word, ctx: Word) -> tuple[bool, str | None] | None:
    """علاقةُ صورة السياق بصورة الابتداء كما طبعتهما البوّابة: (أسقطت الهمزة؟، وجهُ الوقف أو لا وقف)،
    أو لا شيء إن لم تكن إسقاطًا مسمًّى. وجهُ الوقف يُسمّى بشرطه: الألفُ عن تنوين نصب، والحذفُ عن
    تنوين، والهاءُ عن تاء."""

    for dropped in (False, True):
        s = start[1:] if dropped else start
        if dropped and not (start and start[0][0] == "ء"):
            continue
        if ctx == s:
            return (dropped, None)
        if ctx == waqf("سكون", s):
            return (dropped, "سكون")
        if len(s) >= 2 and s[-1] == TANWIN and s[-2][1] == "فتح" and ctx == waqf("ألف", s):
            return (dropped, "ألف")
        if s and s[-1] == TANWIN and ctx == waqf("حذف", s):
            return (dropped, "حذف")
        u = s[:-1] if s and s[-1] == TANWIN else s
        if u and u[-1][0] == "ت" and ctx == waqf("هاء", s):
            return (dropped, "هاء")
    return None


def relation(r: tuple[bool, str | None] | None) -> str:
    """اسمُ العلاقة للعرض."""

    if r is None:
        return "غير ذلك"
    dropped, k = r
    parts = (["ساقطة الوصل"] if dropped else []) + ([f"وقف {k}"] if k else [])
    return "، ".join(parts) or "هي"


def _check() -> None:
    from slge.rawabit import cells_of

    lillahi = cells_of("لْلَهِ")
    assert restore(Hadd(True, False), lillahi) == ((("ء", "فتح"), *lillahi), lillahi)
    assert restore(Hadd(False, False), lillahi) == (lillahi,)
    sabilan, sabilan_p = cells_of("سَبِيْلَنْ"), (*cells_of("سَبِيْلَ"), _ALIF)  # الألفُ خانةً لا رسمًا
    assert waqf("ألف", sabilan) == sabilan_p and sabilan in restore(Hadd(True, True), sabilan_p)
    wa = (("و", "فتح"), _ALIF)
    wahida, wahida_p = (*wa, *cells_of("حِدَتُنْ")), (*wa, *cells_of("حِدَهْ"))
    assert waqf("هاء", wahida) == wahida_p and wahida in restore(Hadd(True, True), wahida_p)
    assert len(restore(Hadd(True, True), wahida_p)) == 12
    ahad, ahad_p = cells_of("ءَحَدُنْ"), cells_of("ءَحَدْ")
    assert waqf("حذف", ahad) == ahad_p and ahad in restore(Hadd(True, True), ahad_p)
    for h in (Hadd(True, True), Hadd(False, True), Hadd(True, False)):
        for x in (sabilan_p, wahida_p, ahad_p, lillahi):
            if h.pause and x[-1][1] != SUKUN:
                continue
            assert x in restore(h, x)
            for u in restore(h, x):
                assert any(project(h, b, k, u) == x for b in (False, True) for k in WAQF), (h, x, u)
    start = cells_of("ءَلْحَمْدُ")
    assert classify(start, start) == (False, None) and classify(start, start[1:]) == (True, None)
    assert classify(start, set_last(start, SUKUN)) == (False, "سكون")
    assert classify(start, set_last(start[1:], SUKUN)) == (True, "سكون")
    assert classify(sabilan, sabilan_p) == (False, "ألف")
    assert classify(ahad, ahad_p) == (False, "حذف")
    assert classify(wahida, wahida_p) == (False, "هاء") and classify(start, cells_of("كَتَبَ")) is None
    assert relation((True, "هاء")) == "ساقطة الوصل، وقف هاء" and relation((False, None)) == "هي"


_check()
