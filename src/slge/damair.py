"""الضمائر: الحصرُ الجامع مفهرَسًا على درجات الترخيص التدريجيّ — مرآةُ `formal/Slge/Damair.lean`.

**المنفصلة (24):** الرفعُ الاثنا عشر (`categories.PRONOUNS`، من شهادات البوّابة)، والنصبُ الاثنا عشر
**جبرًا** الحاملُ «إِيَّا» + الضميرُ المتّصل نفسُه (`iyya_is_carrier_plus_suffix`).
**المتّصلة (9):** الرفعُ (ت و ا ن ي نا) والنصبُ/الجرّ (نا هـ ي ك).

المبرهَن على الخانات، لكلّ حاملٍ: **قانونُ نا** — سكونُ الصحيح قبلها رفعٌ، وحركتُه أو مدُّه نصبٌ/جرّ (إِيَّانَا)
(`na_raf_reads_sukun`، `na_nasb_reads_vowel`)؛ **قانونُ التاء** — الشخصُ في حالتها بعد ساكن
(`ta_person`)؛ والإلحاقُ يحفظ الترخيص (`attach_licensed`). وما لا يفصله الحرف مسمًّى: الياءُ
الساكنة بعد كسرٍ مخاطبةٌ (رفع) أو متكلّمٌ (نصب/جرّ) — الفصلُ من الحامل لا من الخانة (`ya_ambiguous`)؛
ونصبٌ أم جرٌّ بعد المتحرّك — من الحامل (فعل/اسم/حرف) لا من الخانة. والمستترُ ليس خانةً: خارج الحصر
باسمه.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from slge.categories import PRONOUNS
from slge.cells import STATES, Cell, licensed

__all__ = ["ATTACHED_NASB", "ATTACHED_RAF", "DETACHED_NASB", "DETACHED_RAF", "IYYA", "WITNESS",
           "Pronoun", "attach", "na_role", "ta_person", "tier"]

_A, _I, _U, SUKUN = STATES
IYYA: Final[tuple[Cell, ...]] = (("ء", _I), ("ي", SUKUN), ("ي", _A), ("ا", SUKUN))


@dataclass(frozen=True, slots=True)
class Pronoun:
    name: str
    cells: tuple[Cell, ...]
    group: str  # "منفصل رفع" | "منفصل نصب" | "متصل رفع" | "متصل نصب/جر"
    role: str  # الدورُ الإعرابيّ الثابت (معلن)
    law: str  # ما يقرؤه الحرف: "" | "نا" | "ت" | "ي: لا يفصل"


def attach(host: tuple[Cell, ...], suffix: tuple[Cell, ...]) -> tuple[Cell, ...]:
    return (*host, *suffix)


def na_role(word: tuple[Cell, ...]) -> str | None:
    """قانونُ نا: ما قبل «نَاْ» ساكنٌ صحيح ⇒ رفع؛ متحرّكٌ أو مدٌّ ⇒ نصب/جرّ."""

    if len(word) < 3 or word[-1] != ("ا", SUKUN) or word[-2] != ("ن", _A):
        return None
    prev = word[-3]
    return "رفع" if prev[1] == SUKUN and prev[0] not in "اوي" else "نصب/جرّ"


def ta_person(word: tuple[Cell, ...]) -> str | None:
    """قانونُ التاء: بعد ساكنٍ، ضمٌّ متكلّم، فتحٌ مخاطَب، كسرٌ مخاطَبة."""

    if len(word) < 2 or word[-1][0] != "ت" or word[-2][1] != SUKUN:
        return None
    return {_U: "متكلم", _A: "مخاطب", _I: "مخاطبة"}.get(word[-1][1])


_NAMES_RAF = ("أَنَا", "نَحْنُ", "أَنْتَ", "أَنْتِ", "أَنْتُمَا", "أَنْتُمْ", "أَنْتُنَّ", "هُوَ", "هِيَ", "هُمَا", "هُمْ",
              "هُنَّ")
DETACHED_RAF: Final[tuple[Pronoun, ...]] = tuple(
    Pronoun(n, cells, "منفصل رفع", "مبتدأ أو فاعل", "")
    for n, cells in zip(_NAMES_RAF, PRONOUNS, strict=True)
)

ATTACHED_NASB: Final[tuple[Pronoun, ...]] = (
    Pronoun("ـيَ", (("ي", _A),), "متصل نصب/جر", "مفعول به / مضاف إليه / مجرور", "ي: لا يفصل"),
    Pronoun("ـنَا", (("ن", _A), ("ا", SUKUN)), "متصل نصب/جر", "مفعول به / مضاف إليه / مجرور", "نا"),
    Pronoun("ـكَ", (("ك", _A),), "متصل نصب/جر", "مفعول به / مضاف إليه / مجرور", ""),
    Pronoun("ـكِ", (("ك", _I),), "متصل نصب/جر", "مفعول به / مضاف إليه / مجرور", ""),
    Pronoun("ـكُمَا", (("ك", _U), ("م", _A), ("ا", SUKUN)), "متصل نصب/جر", "مفعول به / مضاف", ""),
    Pronoun("ـكُمْ", (("ك", _U), ("م", SUKUN)), "متصل نصب/جر", "مفعول به / مضاف إليه / مجرور", ""),
    Pronoun("ـكُنَّ", (("ك", _U), ("ن", SUKUN), ("ن", _A)), "متصل نصب/جر", "مفعول به / مضاف إليه", ""),
    Pronoun("ـهُ", (("ه", _U),), "متصل نصب/جر", "مفعول به / مضاف إليه / مجرور", ""),
    Pronoun("ـهَا", (("ه", _A), ("ا", SUKUN)), "متصل نصب/جر", "مفعول به / مضاف إليه / مجرور", ""),
    Pronoun("ـهُمَا", (("ه", _U), ("م", _A), ("ا", SUKUN)), "متصل نصب/جر", "مفعول به / مضاف", ""),
    Pronoun("ـهُمْ", (("ه", _U), ("م", SUKUN)), "متصل نصب/جر", "مفعول به / مضاف إليه / مجرور", ""),
    Pronoun("ـهُنَّ", (("ه", _U), ("ن", SUKUN), ("ن", _A)), "متصل نصب/جر", "مفعول به / مضاف إليه", ""),
)

DETACHED_NASB: Final[tuple[Pronoun, ...]] = tuple(
    Pronoun("إِيَّا" + p.name[1:], attach(IYYA, p.cells), "منفصل نصب", "مفعول به مقدَّم", "")
    for p in ATTACHED_NASB
)

ATTACHED_RAF: Final[tuple[Pronoun, ...]] = (
    Pronoun("ـتُ", (("ت", _U),), "متصل رفع", "فاعل / نائب فاعل / اسم كان", "ت"),
    Pronoun("ـتَ", (("ت", _A),), "متصل رفع", "فاعل / نائب فاعل / اسم كان", "ت"),
    Pronoun("ـتِ", (("ت", _I),), "متصل رفع", "فاعل / نائب فاعل / اسم كان", "ت"),
    Pronoun("ـتُمَا", (("ت", _U), ("م", _A), ("ا", SUKUN)), "متصل رفع", "فاعل", "ت"),
    Pronoun("ـتُمْ", (("ت", _U), ("م", SUKUN)), "متصل رفع", "فاعل", "ت"),
    Pronoun("ـتُنَّ", (("ت", _U), ("ن", SUKUN), ("ن", _A)), "متصل رفع", "فاعل", "ت"),
    Pronoun("ـُوا", (("و", SUKUN),), "متصل رفع", "فاعل (واو الجماعة؛ الألفُ الفارقة بقيّةُ رسم)", ""),
    Pronoun("ـَا", (("ا", SUKUN),), "متصل رفع", "فاعل (ألف الاثنين)", ""),
    Pronoun("ـْنَ", (("ن", _A),), "متصل رفع", "فاعل (نون النسوة)", ""),
    Pronoun("ـِي", (("ي", SUKUN),), "متصل رفع", "فاعل (ياء المخاطبة)", "ي: لا يفصل"),
    Pronoun("ـْنَا", (("ن", _A), ("ا", SUKUN)), "متصل رفع", "فاعل (نا الفاعلين)", "نا"),
)

WITNESS: Final[dict[str, tuple[Cell, ...]]] = {
    "كُنْتُ": (("ك", _U), ("ن", SUKUN), ("ت", _U)), "كُنْتَ": (("ك", _U), ("ن", SUKUN), ("ت", _A)),
    "كُنْتِ": (("ك", _U), ("ن", SUKUN), ("ت", _I)),
    "كُنْتُمْ": (("ك", _U), ("ن", SUKUN), ("ت", _U), ("م", SUKUN)),
    "قُلْنَا": (("ق", _U), ("ل", SUKUN), ("ن", _A), ("ا", SUKUN)),
    "جِئْنَا": (("ج", _I), ("ء", SUKUN), ("ن", _A), ("ا", SUKUN)),
    "جَاءَنَا": (("ج", _A), ("ا", SUKUN), ("ء", _A), ("ن", _A), ("ا", SUKUN)),
    "لَنَا": (("ل", _A), ("ن", _A), ("ا", SUKUN)),
    "إِنَّنَا": (("ء", _I), ("ن", SUKUN), ("ن", _A), ("ن", _A), ("ا", SUKUN)),
    "إِيَّانَا": attach(IYYA, (("ن", _A), ("ا", SUKUN))),
    "إِيَّاكَ": attach(IYYA, (("ك", _A),)),
    "إِيَّاهُ": attach(IYYA, (("ه", _U),)),
}
"""ذرّاتُ `gate.enter` (2026-10-06) خاناتٍ؛ والشدّةُ كما في المدوّنة (الشدّةُ قبل الحركة)."""


def tier(p: Pronoun) -> str:
    if p.law in ("نا", "ت"):
        return "د١٦ الإعراب من الخانة"
    if p.group.startswith("متصل"):
        return "د٨ الحدّ (إلحاق)"
    return "د٤ الخانة"


def _check() -> None:
    for p in DETACHED_RAF + DETACHED_NASB:
        if not licensed(p.cells):
            raise ValueError(f"UNLICENSED:{p.name}")
    assert na_role(WITNESS["قُلْنَا"]) == "رفع" and na_role(WITNESS["جَاءَنَا"]) == "نصب/جرّ"
    assert ta_person(WITNESS["كُنْتِ"]) == "مخاطبة"


_check()
