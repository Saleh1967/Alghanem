"""العلمُ ولفظُ الجلالة: لفظٌ منفردٌ بلا قياس — مرآةُ `Slge.Alam` (بتوقيع المالك، ADR ٢٤).

لا قالبَ ولا قياس: الاسمُ علمٌ موسومٌ بعينه من المودَع الموقَّع (`alam_table`)، يُقرأ بسوابقه
(من `jidh.PROCLITICS` وتاءِ القسم، حتى اثنتين) وحالةِ آخره، ويُردّ بعينه (`restore`).
لفظُ الجلالة صورُه ثلاثٌ مسمّاة: `ءَلْلَه` ابتداءً، و`لْلَه` بعد سابقةٍ (بِ وَ فَ لِ)،
و`اْلْلَه` مدًّا بعد تاء القسم أو همزة الاستفهام؛ واللهمّ لفظٌ منفرد.
الحالةُ من الآخر: الممنوعُ جرُّه بالفتح فالفتحُ «نصب/جرّ» (`sarf.mamnu_jarr`)،
والمنصرفُ بالتنوين، والمقصورُ لا تُقرأ حالتُه. المرجعُ في قسمة هذه الألفاظ توقيعُ المالك
لا وسمُ MASAQ (الذي يعدّ أل في لفظ الجلالة سابقةً) — خلافٌ مفصولٌ بقرارٍ مكتوب.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from slge.alam_table import (
    ALAM,
    JALALA_CASES,
    JALALA_HEAD,
    JALALA_INITIAL,
    JALALA_LAST,
    JALALA_MADD,
    LAHUMMA,
)
from slge.cells import SUKUN, Cell, licensed
from slge.jidh import PROCLITICS

__all__ = ["ALAM", "ALAM_PROCLITICS", "JALALA_FORMS", "Ilm", "case_of", "ilm", "restore"]

Word = tuple[Cell, ...]
KINDS: Final[tuple[str, ...]] = ("جلالة", "عربي", "أعجمي")
_TANWIN: Final[Cell] = ("ن", SUKUN)


@dataclass(frozen=True)
class Ilm:
    """قراءةُ علم: السوابقُ، الرسمُ، البابُ، الصرفُ، صورتُه في الكلمة، اسمُ صورته، حالتُه المقروءة."""

    pre: tuple[Word, ...]
    rasm: str
    kind: str
    sarf: str
    surface: Word
    form: str
    case: str


def restore(m: Ilm) -> Word:
    return (*(c for p in m.pre for c in p), *m.surface)


def _jalala_forms() -> tuple[tuple[str, Word], ...]:
    out: list[tuple[str, Word]] = []
    for st in JALALA_CASES:
        base = (*JALALA_HEAD, (JALALA_LAST, st))
        out += [("INITIAL", (*JALALA_INITIAL, *base)), ("AFTER_PREFIX", base),
                ("MADD", (*JALALA_MADD, *base))]
    out.append(("LAHUMMA", LAHUMMA))
    return tuple(out)


JALALA_FORMS: Final[tuple[tuple[str, Word], ...]] = _jalala_forms()
"""صورُ لفظ الجلالة العشر: ثلاثُ حالاتٍ × (ابتداءً، بعد سابقة، مدًّا) + اللهمّ."""


def case_of(sarf: str, last_state: str, tanwin: bool) -> str:
    """الحالةُ من آخر العلم: صرفُه وحركةُ آخره وتنوينُه (`caseOf`)."""

    if sarf == "مقصور" or last_state == SUKUN:
        return "لا تقرؤه الخانة"
    if last_state == "ضم":
        return "رفع"
    if last_state == "كسر":
        return "جرّ"
    if sarf == "ممنوع" or (sarf == "غير مشهود الجرّ" and not tanwin):
        return "نصب/جرّ"  # جرُّ الممنوع بالفتح: `sarf.mamnu_jarr`
    return "نصب"


ALAM_PROCLITICS: Final[tuple[Word, ...]] = (*PROCLITICS, (("ت", "فتح"),))
"""سوابقُ الجذع وتاءُ القسم (من `rawabit.PARTICLES` المتّصلة: تَاللهِ)."""

_PRES: Final[tuple[tuple[Word, ...], ...]] = (
    (), *((p,) for p in ALAM_PROCLITICS),
    *((p, q) for p in ALAM_PROCLITICS for q in ALAM_PROCLITICS))


def _jalala_at(pre: tuple[Word, ...], rest: Word) -> tuple[Ilm, ...]:
    out: list[Ilm] = []
    for form, cells in JALALA_FORMS:
        if cells != rest:
            continue
        if form == "INITIAL" and pre:
            continue  # الهمزةُ لا تبقى بعد سابقة
        if form == "AFTER_PREFIX" and (not pre or pre[-1][0][0] == "ء"):
            continue  # لا ابتداءَ بساكن؛ وبعد همزة الاستفهام تُمدّ (ءَاْلْلَهُ) لا تُحذف
        if form == "MADD" and not (pre and pre[-1][0][0] in ("ت", "ء")):
            continue  # المدُّ بعد تاء القسم أو همزة الاستفهام فقط
        st = "لا تقرؤه الخانة" if form == "LAHUMMA" else rest[-1][1]
        case = st if form == "LAHUMMA" else case_of("منصرف", st, False)
        out.append(Ilm(pre, "الله" if form != "LAHUMMA" else "اللهم", "جلالة", "منفرد", rest, form,
                       case))
    return tuple(out)


def _alam_at(pre: tuple[Word, ...], rest: Word) -> tuple[Ilm, ...]:
    out: list[Ilm] = []
    for rasm, head, last, fixed, kind, sarf in ALAM:
        n = len(head) + 1
        tanwin = len(rest) == n + 1 and rest[-1] == _TANWIN
        body = rest[:n] if tanwin else rest
        if len(body) != n or body[:-1] != head or body[-1][0] != last:
            continue
        if fixed is not None and body[-1][1] != fixed:
            continue
        if tanwin and sarf in ("ممنوع", "مقصور"):
            continue  # الممنوعُ لا يُنوَّن؛ المقصورُ آخرُه ألف
        case = case_of(sarf, body[-1][1], tanwin)
        out.append(Ilm(pre, rasm, kind, sarf, rest, "TANWIN" if tanwin else "", case))
    return tuple(out)


def ilm(w: Word) -> tuple[Ilm, ...]:
    """قراءاتُ الكلمة علمًا أو لفظَ جلالة: كلُّ (سوابق، صورةٌ موقَّعة) يردّ الكلمةَ بعينها (`ilm`)."""

    out: list[Ilm] = []
    for pre in _PRES:
        flat = tuple(c for p in pre for c in p)
        if w[: len(flat)] != flat or len(w) == len(flat):
            continue
        rest = w[len(flat):]
        for m in (*_jalala_at(pre, rest), *_alam_at(pre, rest)):
            assert restore(m) == w
            out.append(m)
    return tuple(out)


def _check() -> None:
    from slge.rawabit import cells_of

    assert len(JALALA_FORMS) == 10
    # الباقي لا يُرخَّص إلّا بسابقته (لا ابتداءَ بساكن)
    assert all(licensed(c) for f, c in JALALA_FORMS if f in ("INITIAL", "LAHUMMA"))
    assert len(ALAM) == 57 and all(licensed((*h, (last, "فتح"))) for _, h, last, _, _, _ in ALAM)
    j = ilm(cells_of("ءَلْلَهُ"))
    assert len(j) == 1 and j[0].kind == "جلالة" and j[0].form == "INITIAL" and j[0].case == "رفع"
    b = ilm(cells_of("بِلْلَهِ"))
    assert any(m.form == "AFTER_PREFIX" and m.case == "جرّ" and m.pre for m in b)
    assert any(m.form == "LAHUMMA" for m in ilm(cells_of("ءَلْلَهُمْمَ")))
    assert not ilm(cells_of("لْلَهِ")) and not ilm(cells_of("ءَلْلَهُ")[:-1])  # لا ابتداءَ بساكن؛ ولا بترٌ
    ib = ilm(cells_of("إِبْرَاهِيمَ"))
    assert ib and ib[0].sarf == "ممنوع" and ib[0].case == "نصب/جرّ"
    lt = ilm(cells_of("لُوطٍ"))
    assert lt and lt[0].form == "TANWIN" and lt[0].case == "جرّ"
    assert case_of("مقصور", "سكون", False) == "لا تقرؤه الخانة"
    assert not ilm(cells_of("كَتَبَ"))


_check()
