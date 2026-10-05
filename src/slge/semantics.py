"""الدالُّ والمدلول: الوضع، والدلالاتُ الثلاث، والحقيقةُ والمجاز، والنسب، والمنطوقُ والمفهوم.

منقولٌ من `dal-madlul-constitution/src/slge/slge_dalil.py` (DL1–DL6). وهذه طبقةُ
تعريفاتٍ معلنة: تُغلق الأقسامَ وتمنع الخارجَ عنها، ولا تحكم على واقع؛ والحكمُ في
`knowledge` بقواعدَ مقبولةٍ بدليل. وطريقُ كلّ مفهومٍ إلى صورةٍ من صور الاستدلال
مكتوبٌ في `knowledge.MAFHUM_ROUTE`.
"""

from __future__ import annotations

from typing import Final

__all__ = [
    "CONVENTIONS",
    "DALALAT",
    "MAFHUM",
    "MANTUQ",
    "NASAB",
    "dalala",
    "haqiqa",
    "mafhum_of",
    "majaz",
    "mantuq_or_mafhum",
]

CONVENTIONS: Final[dict[str, str]] = {
    "كتاب": "مجموع صحائف تُقرأ", "عِلْم": "معرفة بمعلومات وواقع مدرَك",
    "جَهْل": "نقص المعرفة", "مِنْ": "ابتداء وانفصال", "عَلَى": "علوّ واستعلاء",
    "قائم": "ثابت منتصب", "حَسَن": "ممدوح", "قَبِيح": "مذموم",
}
"""DL1 الوضع: تخصيصُ لفظٍ بمعنى (عيّنةٌ معلنة؛ واستيفاؤها رواية)."""

DALALAT: Final[dict[str, str]] = {
    "مطابقة": "تمام المسمى", "تضمن": "جزء المسمى", "تلويح": "لازم المسمى غير الجزء",
}
NASAB: Final[frozenset[str]] = frozenset({"إسنادية", "تقييدية", "إضافية"})
MANTUQ: Final[frozenset[str]] = frozenset(DALALAT)
MAFHUM: Final[frozenset[str]] = frozenset(
    {"موافقة", "مخالفة_صفة", "مخالفة_شرط", "مخالفة_غاية", "مخالفة_عدد"}
)


def dalala(mode: str) -> bool:
    """DL2: الدلالةُ جائزةٌ إذا كان نمطُها من الثلاثة المغلقة."""

    return mode in DALALAT


def haqiqa(word: str, use: str) -> bool:
    """DL3: الحقيقةُ استعمالُ اللفظ فيما وُضع له."""

    return CONVENTIONS.get(word) == use


def majaz(word: str, use: str, qarina: str | None) -> bool:
    """DL3: المجازُ استعمالٌ في غير ما وُضع له، ولا يصحّ بلا قرينة."""

    return word in CONVENTIONS and CONVENTIONS[word] != use and bool(qarina)


def mantuq_or_mafhum(mode: str) -> str | None:
    """DL5: التقسيمُ مغلق: «منطوق» أو «مفهوم»، ولا ثالث (فيُعاد ‎None‎)."""

    if mode in MANTUQ:
        return "منطوق"
    if mode in MAFHUM:
        return "مفهوم"
    return None


def mafhum_of(word: str, has_reality: bool) -> str | None:
    """DL6: للمعنى مفهومٌ إذا كان له واقعٌ مدرَك؛ وإلّا فهو معلوماتٌ لا مفاهيم."""

    return CONVENTIONS.get(word) if has_reality else None
