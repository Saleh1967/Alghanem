"""السلسلة: أركانُ المدلول الكونيّ على سلالم النبهانيّ الثلاثة — مرآةُ `Slge.Salsala` (ADR ٣١، ٣٢).

جدولُ المالك أُعيد ترتيبُه على ثلاثة سلالم بوسمٍ مرتَّب: (أ) المعلوماتُ السابقة — الجذرُ الأركانُ
الأربعة، والوجودُ والحقائقُ يقينًا، والكنهُ وما بعده ظنًّا؛ (ب) الوضعُ والنسبُ الثلاث والإفادة؛ (ج) الحكم:
علاقاتُ المجاز. ثمّ خارج العمود، من مودَع الغزاليّ المختوم باسم صاحبه (ADR ٣٢): (د) مصادرُ اليقين
السبعة، و(هـ) أوليّاتُه خلافًا مسجَّلًا بلا سالفٍ في العمود. كلُّ ركنٍ بسطره من المختوم (`salsala_table`)
أو معلَنٌ باسمه؛ لا شيءَ من الذاكرة. وشواهدُ الغزاليّ الثانية على أركان العمود (`SHAWAHID`، ADR ٣٣) رأيٌ
ثانٍ: لا تُرسي ولا ترفع الإعلان (`shahid_does_not_anchor`).
"""

from __future__ import annotations

from typing import Final

from slge.salsala_table import (
    DECLARED,
    GRADES,
    LADDERS,
    ROWS,
    SALAF_ANCHORED,
    SHAWAHID,
    SPINE,
    Row,
    Shahid,
)

__all__ = ["DECLARED", "GRADES", "LADDERS", "ROWS", "SALAF_ANCHORED", "SHAWAHID", "SPINE",
           "anchored", "grade", "ladder", "rukn", "salaf", "shahid"]

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


def shahid(i: int) -> tuple[Shahid, ...]:
    """شواهدُ الغزاليّ الثانية على الركن (رأيٌ ثانٍ لا مرساة)؛ فارغةٌ لما لا شاهدَ له."""

    return tuple(s for s in SHAWAHID if s[0] == i)


def _check() -> None:
    n = len(ROWS)
    assert n == 34 and [r[0] for r in ROWS] == list(range(n)) and len(LADDERS) == 5
    assert [i for i in range(n) if grade(i) == "يقين"] == [1, 2]
    assert all(grade(i) == "—" for i in range(n) if ROWS[i][1] != 0)
    assert all(anchored(i) != (i in DECLARED) for i in range(n))
    assert all(s < i for i in range(n) for s, _ in salaf(i))
    assert [ROWS[i][2] for i in (13, 14, 15)] == ["الإسناد", "التقييد", "الإضافة"]
    assert not any("التضمين" in r[2] for r in ROWS)
    # خارج العمود (السلّمان الأخيران): لا سالفَ في العمود، ومرساةٌ باسم صاحبها
    assert all(not ROWS[i][5] for i in range(n) if ROWS[i][1] >= 3)
    assert all(anchored(i) for i in range(n) if ROWS[i][1] >= 3)
    # الشاهدُ الثاني من خارج العمود على ركنٍ فيه، ولا يرفع الإعلان
    assert all(s[1] not in SPINE and ROWS[s[0]][1] < 3 for s in SHAWAHID)
    assert all(not anchored(i) for i in DECLARED)

_check()
