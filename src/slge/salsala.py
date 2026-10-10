"""السلسلة: أركانُ المدلول الكونيّ على سلالم النبهانيّ الثلاثة — مرآةُ `Slge.Salsala` (ADR ٣١).

جدولُ المالك أُعيد ترتيبُه على ثلاثة سلالم بوسمٍ مرتَّب: (أ) المعلوماتُ السابقة — الجذرُ الأركانُ
الأربعة، والوجودُ والحقائقُ يقينًا، والكنهُ وما بعده ظنًّا؛ (ب) الوضعُ والنسبُ الثلاث والإفادة؛ (ج) الحكم:
علاقاتُ المجاز. كلُّ ركنٍ بسطره من المختومَين (`salsala_table`) أو معلَنٌ باسمه؛ لا شيءَ من الذاكرة.
"""

from __future__ import annotations

from typing import Final

from slge.salsala_table import DECLARED, GRADES, LADDERS, ROWS, SALAF_ANCHORED, Row

__all__ = ["DECLARED", "GRADES", "LADDERS", "ROWS", "SALAF_ANCHORED", "anchored", "grade",
           "ladder", "rukn", "salaf"]

ARKAN: Final[tuple[str, ...]] = ("الواقع", "الإحساس", "الذهن", "المعلومات السابقة")
"""الأركانُ الأربعة (ج3 393: «نقل الواقع بواسطة الإحساس إلى الذهن مع معلومات سابقة»)."""


def rukn(i: int) -> Row:
    return ROWS[i]


def ladder(i: int) -> str:
    return LADDERS[ROWS[i][1]]


def grade(i: int) -> str:
    """مرتبةُ الركن: يقينٌ (الوجودُ والحقائق)، ظنٌّ (الكنهُ وما بعده)، — (ليس حكمًا على واقع)."""

    return GRADES[ROWS[i][3]]


def anchored(i: int) -> bool:
    """أمرسًى بسطرٍ من المختوم؟ وإلّا فمعلَنٌ بقرار المالك (`DECLARED`)."""

    return bool(ROWS[i][4])


def salaf(i: int) -> tuple[tuple[int, bool], ...]:
    """سوالفُ الركن (شرطُ إمكانه) كلٌّ مع وسمه: منصوصٌ أم رأيٌ من جدول المالك."""

    return tuple((s, (i, s) in SALAF_ANCHORED) for s in ROWS[i][5])


def _check() -> None:
    assert len(ROWS) == 22 and [r[0] for r in ROWS] == list(range(22))
    assert [i for i in range(22) if grade(i) == "يقين"] == [1, 2]
    assert all(grade(i) == "—" for i in range(22) if ROWS[i][1] != 0)
    assert all(anchored(i) != (i in DECLARED) for i in range(22))
    assert all(s < i for i in range(22) for s, _ in salaf(i))
    assert [ROWS[i][2] for i in (13, 14, 15)] == ["الإسناد", "التقييد", "الإضافة"]
    assert not any("التضمين" in r[2] for r in ROWS)


_check()
