"""أسماءُ الإشارة: التنبيهُ والبعدُ والتثنيةُ عملياتٍ على الخانات — مرآةُ `formal/Slge/Ishara.lean`.

اسمُ الإشارة **نواةٌ** تدخل عليها ثلاثُ عمليّاتٍ لا غير: **التنبيه** هَ في الصدر (حرفٌ متحرّكٌ لا
يُفسد الترخيص: `tanbih_licensed`)، **البعدُ** لامٌ اختياريّةٌ فكافُ الخطاب في العجز (`bud_licensed`)،
**التثنيةُ** مدٌّ فنونٌ مكسورة، والحالةُ تُقرأ من المدّ (`caseOf_dual`)، ولا تفرّق الياءُ بين نصبٍ
وجرّ. والمبنيُّ ما لا تقرأ له الخانةُ حالةً (`mabni_no_case`). النوى كما تقرؤها البوّابة: هَذَا =
هَ ذَ اْ (لا ألفَ بعد الهاء في الرسم)، أُولَئِكَ = ءُ وْ لَ ءِ كَ (الواوُ مدّ). والشواهد: 13 صورةً من
شهادات البوّابة بعينها؛ الباقي بالقانون (معلن).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from slge.cells import STATES, Cell, licensed

__all__ = ["DUALS", "FORMS", "WITNESSED", "Ishara", "bud", "case_of", "dual", "tanbih", "tier"]

_A, _I, _U, SUKUN = STATES
HA: Final[Cell] = ("ه", _A)
KAF: Final[Cell] = ("ك", _A)


def tanbih(core: tuple[Cell, ...]) -> tuple[Cell, ...]:
    return (HA, *core)


def bud(core: tuple[Cell, ...], lam: str | None = None) -> tuple[Cell, ...]:
    """البعد: لامٌ (كسر/سكون) اختياريّة ثمّ كاف الخطاب."""

    return (*core, *((("ل", lam),) if lam else ()), KAF)


def dual(stem: tuple[Cell, ...], case: str) -> tuple[Cell, ...]:
    """التثنية: ا للرفع، ي للنصب والجرّ، ثمّ نِ."""

    glide = "ا" if case == "رفع" else "ي"
    return (*stem, (glide, SUKUN), ("ن", _I))


def case_of(word: tuple[Cell, ...]) -> str | None:
    """الحالةُ من المدّ قبل النون المكسورة (وقبل كاف الخطاب إن لحقت)؛ `None` للمبنيّ."""

    w = word[:-1] if word and word[-1] == KAF else word
    if len(w) < 2 or w[-1] != ("ن", _I) or w[-2][1] != SUKUN:
        return None
    return {"ا": "رفع", "ي": "نصب/جرّ"}.get(w[-2][0])


@dataclass(frozen=True, slots=True)
class Ishara:
    name: str
    cells: tuple[Cell, ...]
    bab: str  # "قريب" | "بعيد" | "مكان" | "نواة"
    dalala: str  # الدلالةُ من الحصر المُرسَل (معلن)
    witnessed: bool


DHA: Final[tuple[Cell, ...]] = (("ذ", _A), ("ا", SUKUN))
DHIHI: Final[tuple[Cell, ...]] = (("ذ", _I), ("ه", _I))
TI: Final[tuple[Cell, ...]] = (("ت", _I),)
ULAA: Final[tuple[Cell, ...]] = (("ء", _U), ("ل", _A), ("ا", SUKUN), ("ء", _I))
HUNA: Final[tuple[Cell, ...]] = (("ه", _U), ("ن", _A), ("ا", SUKUN))
THAMMA: Final[tuple[Cell, ...]] = (("ث", _A), ("م", SUKUN), ("م", _A))
_DH = (("ذ", _A),)
_T = (("ت", _A),)

FORMS: Final[tuple[Ishara, ...]] = (
    Ishara("هَذَا", tanbih(DHA), "قريب", "المفرد المذكّر", True),
    Ishara("هَذِهِ", tanbih(DHIHI), "قريب", "المفرد المؤنّث", True),
    Ishara("هَذَانِ", tanbih(dual(_DH, "رفع")), "قريب", "المثنّى المذكّر رفعًا", True),
    Ishara("هَذَيْنِ", tanbih(dual(_DH, "نصب")), "قريب", "المثنّى المذكّر نصبًا وجرًّا", False),
    Ishara("هَاتَانِ", tanbih((("ا", SUKUN), *dual(_T, "رفع"))), "قريب", "المثنّى المؤنّث رفعًا", False),
    Ishara("هَاتَيْنِ", tanbih((("ا", SUKUN), *dual(_T, "نصب"))), "قريب", "المثنّى المؤنّث نصبًا وجرًّا",
           True),
    Ishara("هَؤُلَاءِ", tanbih(ULAA), "قريب", "الجمع", True),
    Ishara("ذَاكَ", bud(DHA), "بعيد", "المفرد المذكّر", False),
    Ishara("ذَلِكَ", bud(_DH, _I), "بعيد", "المفرد المذكّر", True),
    Ishara("تِلْكَ", bud(TI, SUKUN), "بعيد", "المفرد المؤنّث", True),
    Ishara("ذَانِكَ", bud(dual(_DH, "رفع")), "بعيد", "المثنّى المذكّر رفعًا", False),
    Ishara("ذَيْنِكَ", bud(dual(_DH, "نصب")), "بعيد", "المثنّى المذكّر نصبًا وجرًّا", False),
    Ishara("تَانِكَ", bud(dual(_T, "رفع")), "بعيد", "المثنّى المؤنّث رفعًا", False),
    Ishara("تَيْنِكَ", bud(dual(_T, "نصب")), "بعيد", "المثنّى المؤنّث نصبًا وجرًّا", False),
    Ishara("أُولَئِكَ", bud((("ء", _U), ("و", SUKUN), ("ل", _A), ("ء", _I))), "بعيد", "الجمع", True),
    Ishara("هُنَا", HUNA, "مكان", "القريب", False),
    Ishara("هَهُنَا", tanbih(HUNA), "مكان", "القريب بالتنبيه", False),
    Ishara("هُنَاكَ", bud(HUNA), "مكان", "المتوسّط", False),
    Ishara("هُنَالِكَ", bud(HUNA, _I), "مكان", "البعيد", True),
    Ishara("ثَمَّ", THAMMA, "مكان", "الاتّجاه والبعيد", True),
    Ishara("ثَمَّةَ", (*THAMMA, ("ت", _A)), "مكان", "الاتّجاه والبعيد", False),
    Ishara("ذَا", DHA, "نواة", "نواةُ المذكّر", True),
    Ishara("ذِي", (("ذ", _I), ("ي", SUKUN)), "نواة", "نواةُ المؤنّث (لغة)", True),
    Ishara("أُولَاءِ", (("ء", _U), ("و", SUKUN), ("ل", _A), ("ا", SUKUN), ("ء", _I)), "نواة",
           "نواةُ الجمع", True),
    Ishara("تِي", (("ت", _I), ("ي", SUKUN)), "نواة", "نواةُ المؤنّث (لغة)", False),
)

DUALS: Final[frozenset[str]] = frozenset(
    {"هَذَانِ", "هَذَيْنِ", "هَاتَانِ", "هَاتَيْنِ", "ذَانِكَ", "ذَيْنِكَ", "تَانِكَ", "تَيْنِكَ"}
)
WITNESSED: Final[tuple[str, ...]] = tuple(f.name for f in FORMS if f.witnessed)


def tier(f: Ishara) -> str:
    if f.name in DUALS:
        return "د١٦ الإعراب من الخانة (المثنّى)"
    if f.cells[0] == HA or f.cells[-1] == KAF:
        return "د٨ الحدّ (تنبيهٌ أو بُعد)"
    return "د٤ الخانة (مبنيٌّ على نواته)"


def _check() -> None:
    for f in FORMS:
        if not licensed(f.cells):
            raise ValueError(f"UNLICENSED:{f.name}")
        has_case = case_of(f.cells) is not None
        if has_case != (f.name in DUALS):
            raise ValueError(f"CASE_LAW_BROKEN:{f.name}")


_check()
