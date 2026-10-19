"""اتّساقُ الرسم والذرّات: فاحصٌ مستقلٌّ لا يستورد الجسر ولا المولِّد.

الفاحصُ القديم (`check_codebooks`) يتحقّق من البصمة والقسمة والحقن، لكنّه يقبل
ذرّاتٍ خاطئةً تمامًا إن أُعيدت البصمة: كلمةٌ أُعطيت الذرّةَ `بَ` وحدها مرّت. وهذا
الفاحصُ يسدّ ذلك بسؤالٍ واحدٍ يُجاب من الجدول وحده:

    هل يمكن أن تخرج هذه الذرّاتُ من هذا الرسم بقواعدِ تمدّدٍ معلنةٍ ههنا؟

لكلّ عنقودٍ في الرسم (حرفٌ وعلاماته) قائمةٌ منتهيةٌ من التمدّدات الممكنة إلى
حوامل وحالات، مكتوبةٌ في `_expansions` بأسمائها، ثمّ برمجةٌ ديناميكيّةٌ تطابق
العناقيدَ بالذرّات من أوّلها إلى آخرها. فإن لم يوجد تقابلٌ، فالذرّاتُ لا تُشتَقّ
من الرسم: `RASM_ATOMS_INCONSISTENT`.

ما يثبته: أنّ كلَّ حاملٍ في الذرّات له مصدرٌ في الرسم بقاعدةٍ مسمّاة، وأنّ كلَّ
حركةٍ مكتوبةٍ في الرسم على غير الطرف محفوظةٌ في ذرّتها. وما لا يثبته: أنّ
القواعدَ صحيحةٌ لغويًّا، ولا أنّ الجسرَ اختار التمدّدَ الصحيح حين يجوز اثنان
(ألفٌ تُنطَق أو تسقط). فهو فحصُ اشتقاقٍ ممكن، لا فحصُ قراءة.
"""

from __future__ import annotations

import unicodedata
from functools import cache

FATHA, DAMMA, KASRA, SUKUN = "َ", "ُ", "ِ", "ْ"
VOWELS = {FATHA, DAMMA, KASRA}
SHADDA = "ّ"
TANWIN = {"ً": FATHA, "ٌ": DAMMA, "ٍ": KASRA}
DAGGER, MADDA, HAMZA_ABOVE, HAMZA_BELOW = "ٰ", "ٓ", "ٔ", "ٕ"
WASLA = "ٱ"
TATWEEL = "ـ"
HAMZA_SEATS = {"ء", "أ", "إ", "ؤ", "ئ"}


def clusters(surface: str) -> list[tuple[str, frozenset[str]]]:
    out: list[tuple[str, list[str]]] = []
    for ch in unicodedata.normalize("NFD", surface):
        if ch == TATWEEL:
            continue
        if unicodedata.category(ch) == "Mn" and out:
            out[-1][1].append(ch)
        else:
            out.append((ch, []))
    return [(b, frozenset(m)) for b, m in out]


def _haraka(marks: frozenset[str]) -> str | None:
    for m in marks:
        if m in VOWELS:
            return m
    if SUKUN in marks:
        return SUKUN
    return None


def _expansions(
    base: str, marks: frozenset[str], final: bool
) -> list[tuple[tuple[str, str | None], ...]]:
    """التمدّداتُ الممكنةُ لعنقود: كلُّ ذرّةٍ (حامل، حالةٌ مطلوبة أو None لأيّ حالة).

    الحالةُ المطلوبةُ هي الحركةُ المكتوبة؛ وفي الطرف يُقبل السكونُ مكانها (الوقف).
    """

    # بعد NFD: أ إ ؤ ئ حرفٌ وعليه علامةُ همزة؛ فالكرسيُّ أيًّا كان يُقرأ همزةً.
    hamza = HAMZA_ABOVE in marks or HAMZA_BELOW in marks or base in HAMZA_SEATS
    written = _haraka(marks)
    tanwin = next((TANWIN[m] for m in marks if m in TANWIN), None)

    def head(carrier: str) -> list[tuple[tuple[str, str | None], ...]]:
        # الحاملُ بحالته: المكتوبةُ إن وُجدت، وفي الطرف يجوز السكون (الوقف).
        states: list[str | None] = [written] if written else [None]
        if final and written in VOWELS:
            states.append(SUKUN)
        core: list[tuple[tuple[str, str | None], ...]] = []
        for st in states:
            seq: tuple[tuple[str, str | None], ...] = ((carrier, st),)
            if SHADDA in marks:
                seq = ((carrier, SUKUN),) + seq
            core.append(seq)
        if tanwin is not None:
            with_t = []
            for seq in core:
                body = seq[:-1]
                with_t.append(body + ((carrier, tanwin), ("ن", SUKUN)))  # وصل
                with_t.append(body + ((carrier, SUKUN),))  # وقفٌ على الرفع والجرّ
                with_t.append(body + ((carrier, FATHA), ("ا", SUKUN)))  # وقفُ النصب
            core = with_t
        if DAGGER in marks:
            core = core + [seq + (("ا", SUKUN),) for seq in core]
        return core

    if base == "ا" and MADDA in marks:
        return [(("ء", FATHA), ("ا", SUKUN))]
    if hamza:
        return head("ء")
    if base == WASLA:
        return [(), (("ء", None),)]
    if base in {"ا", "ى"}:
        options: list[tuple[tuple[str, str | None], ...]] = [()]  # صامتةٌ أو دعامة
        options += head("ا")
        options.append((("ء", None),))  # ألفُ وصلٍ يُبتدأ بها
        return options
    if base == "ة":
        return head("ت") + [(("ه", SUKUN),)]
    if "ء" <= base <= "ي":
        return head(base)
    return []


def consistent(surface: str, atoms: list[str] | tuple[str, ...]) -> bool:
    """أيوجد تقابلٌ بين عناقيد الرسم وذرّاته بالتمدّدات المعلنة؟"""

    cs = clusters(surface)
    target = tuple((a[0], a[1]) for a in atoms)
    last = len(cs) - 1
    while last > 0 and cs[last][0] in {"ا", "ى"} and not cs[last][1]:
        last -= 1  # ألفُ دعامةِ التنوين لا تُزحزح الطرف

    @cache
    def go(i: int, j: int) -> bool:
        if i == len(cs):
            return j == len(target)
        base, marks = cs[i]
        for seq in _expansions(base, marks, final=i >= last):
            n = len(seq)
            if j + n > len(target):
                continue
            if all(
                target[j + k][0] == c and (st is None or target[j + k][1] == st)
                for k, (c, st) in enumerate(seq)
            ) and go(i + 1, j + n):
                return True
        return False

    return go(0, 0)
