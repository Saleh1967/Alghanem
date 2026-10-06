"""أسماءُ الاستفهام: المعربُ الواحد والتركيبُ على الخانات — مرآةُ `formal/Slge/Istifham.lean`.

المبرهَن: **أَيّ المعربُ الوحيد** — صورُه الثلاث تختلف في حالة الخانة الأخيرة لا غير، والحالةُ تُقرأ
منها (`caseOf_ayy`)، وسائرُ الأسماء صورةٌ واحدة (`mabni_single_form`). **التركيب**: مَاذَا = مَا ++ ذَا
بعينها، مَنْ ذَا وصلٌ مرخَّص، أَمَّنْ = أَمْ ++ مَنْ. **«ما» بعد الجارّ تحذف ألفَها**: بِمَ، لِمَ، فِيمَ؛
وعَمَّ ومِمَّ بإدغام نون الجارّ في الميم — عمليّةٌ على الخانات (`idgham_nm`). والحرفان: الهمزةُ
حرفٌ متّصل، وهَلْ كلمة. 22 صورةً، 21 منها من شهادات البوّابة بعينها (مَنْ ذَا كلمتان).

**الصدارة** قانونُ تيارٍ لا خانةٍ: يُقاس على MASAQ (`precedence`) ولا يُبرهَن؛ والدلالةُ (عاقل،
زمان، مكان، حال، عدد) من الحصر المُرسَل معلَنة.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from slge.cells import STATES, Cell, licensed
from slge.ishara import DHA

__all__ = ["FORMS", "MABNI", "Istifham", "ayy", "case_of", "idgham_nm", "ma_after_jarr", "tier"]

_A, _I, _U, SUKUN = STATES


def ayy(state: str) -> tuple[Cell, ...]:
    return (("ء", _A), ("ي", SUKUN), ("ي", state))


def case_of(word: tuple[Cell, ...]) -> str | None:
    """حالةُ المعرب من الخانة الأخيرة (أَيّ وحدَه)."""

    if not word or word[:2] != (("ء", _A), ("ي", SUKUN)) or word[-1][0] != "ي":
        return None
    return {_U: "رفع", _A: "نصب", _I: "جرّ"}.get(word[-1][1])


def idgham_nm(word: tuple[Cell, ...]) -> tuple[Cell, ...]:
    """نونٌ ساكنةٌ قبل ميمٍ تصير ميمًا ساكنة (أوّلُ موضع)."""

    out = list(word)
    for i in range(len(out) - 1):
        if out[i] == ("ن", SUKUN) and out[i + 1][0] == "م":
            out[i] = ("م", SUKUN)
            break
    return tuple(out)


MA_JARR: Final[tuple[Cell, ...]] = (("م", _A),)


def ma_after_jarr(jarr: tuple[Cell, ...]) -> tuple[Cell, ...]:
    """«ما» بعد الجارّ: ميمٌ مفتوحةٌ بلا ألف، ثمّ الإدغامُ إن سبقتها نونٌ ساكنة."""

    return idgham_nm((*jarr, *MA_JARR))


@dataclass(frozen=True, slots=True)
class Istifham:
    name: str
    cells: tuple[Cell, ...]
    kind: str  # "اسم" | "حرف" | "تركيب"
    dalala: str
    witnessed: bool


MA: Final[tuple[Cell, ...]] = (("م", _A), ("ا", SUKUN))
MAN: Final[tuple[Cell, ...]] = (("م", _A), ("ن", SUKUN))
AM: Final[tuple[Cell, ...]] = (("ء", _A), ("م", SUKUN))
AN: Final[tuple[Cell, ...]] = (("ع", _A), ("ن", SUKUN))
MIN: Final[tuple[Cell, ...]] = (("م", _I), ("ن", SUKUN))
BI: Final[tuple[Cell, ...]] = (("ب", _I),)
LI: Final[tuple[Cell, ...]] = (("ل", _I),)
FI: Final[tuple[Cell, ...]] = (("ف", _I), ("ي", SUKUN))

FORMS: Final[tuple[Istifham, ...]] = (
    Istifham("مَنْ", MAN, "اسم", "العاقل", True),
    Istifham("مَا", MA, "اسم", "غير العاقل", True),
    Istifham("مَتَى", (("م", _A), ("ت", _A), ("ا", SUKUN)), "اسم", "الزمان", True),
    Istifham("أَيَّانَ", (("ء", _A), ("ي", SUKUN), ("ي", _A), ("ا", SUKUN), ("ن", _A)), "اسم",
             "الزمان المستقبل", True),
    Istifham("أَيْنَ", (("ء", _A), ("ي", SUKUN), ("ن", _A)), "اسم", "المكان", True),
    Istifham("كَيْفَ", (("ك", _A), ("ي", SUKUN), ("ف", _A)), "اسم", "الحال", True),
    Istifham("كَمْ", (("ك", _A), ("م", SUKUN)), "اسم", "العدد", True),
    Istifham("أَنَّى", (("ء", _A), ("ن", SUKUN), ("ن", _A), ("ا", SUKUN)), "اسم",
             "الحال / المكان / الزمان", True),
    Istifham("أَيُّ", ayy(_U), "اسم", "لجميع المعاني (معرب: رفع)", True),
    Istifham("أَيَّ", ayy(_A), "اسم", "لجميع المعاني (معرب: نصب)", True),
    Istifham("أَيِّ", ayy(_I), "اسم", "لجميع المعاني (معرب: جرّ)", True),
    Istifham("مَاذَا", (*MA, *DHA), "تركيب", "مَا + ذَا", True),
    Istifham("مَنْ ذَا", (*MAN, *DHA), "تركيب", "مَنْ + ذَا (كلمتان موصولتان)", False),
    Istifham("أَمَّنْ", (*AM, *MAN), "تركيب", "أَمْ + مَنْ", True),
    Istifham("هَلْ", (("ه", _A), ("ل", SUKUN)), "حرف", "حرفُ استفهام", True),
    Istifham("أَ", (("ء", _A),), "حرف", "همزةُ الاستفهام (متّصلة)", True),
    Istifham("بِمَ", ma_after_jarr(BI), "تركيب", "بِ + مَا بحذف الألف", True),
    Istifham("لِمَ", ma_after_jarr(LI), "تركيب", "لِ + مَا بحذف الألف", True),
    Istifham("فِيمَ", ma_after_jarr(FI), "تركيب", "فِي + مَا بحذف الألف", True),
    Istifham("عَمَّ", ma_after_jarr(AN), "تركيب", "عَنْ + مَا بحذف الألف والإدغام", True),
    Istifham("مِمَّ", ma_after_jarr(MIN), "تركيب", "مِنْ + مَا بحذف الألف والإدغام", True),
    Istifham("لِأَيِّ", (*LI, *ayy(_I)), "تركيب", "لِ + أَيِّ (معرب بعد الجارّ)", True),
)

MABNI: Final[tuple[str, ...]] = ("مَنْ", "مَا", "مَتَى", "أَيَّانَ", "أَيْنَ", "كَيْفَ", "كَمْ", "أَنَّى")


def tier(f: Istifham) -> str:
    if case_of(f.cells) is not None or f.name == "لِأَيِّ":
        return "د١٦ الإعراب من الخانة (أَيّ)"
    if f.kind == "تركيب":
        return "د٨ الحدّ (تركيبٌ على الخانات)"
    return "د٤ الخانة (مبنيٌّ أو حرف)"


def _check() -> None:
    for f in FORMS:
        if not licensed(f.cells):
            raise ValueError(f"UNLICENSED:{f.name}")
    assert ma_after_jarr(AN) == (("ع", _A), ("م", SUKUN), ("م", _A))


_check()
