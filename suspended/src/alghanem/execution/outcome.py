"""مفرداتُ الحكم: خمسُ منازلَ للفحص، وثلاثةُ أحكامٍ لا رابعَ لها.

    ExecutionOutcome  =  PASS | BLOCK | DEFER

**وغيابُ الدعوى ليس تصديقًا لها** (`NoClaimIsNotAnAgreement`): إذا لم تُعلَن
هويّةٌ متوقَّعةٌ أصلًا فليس في الباب ما يُطابَق، فلا يُسجَّل الفحصُ مُتحقِّقًا
بالسهو، بل `NOT_APPLICABLE_NO_CLAIM`.

**والحجبُ ليس نقصَ دليل** (`ABlockedDependentIsNotMissingEvidence`): قانونٌ
تابعٌ لم يُنفَّذ لأنّ قانونًا سابقًا حجب مادّتَه يُسجَّل
`NOT_EVALUATED_BY_PREREQUISITE`، ولا يُضاف إلى البقايا؛ وإلّا بدت القضيّةُ
المحجوبةُ ناقصةَ الدليل، وسببُ عدم الفحص هو الحجبُ نفسُه لا نقصُ الدليل.

فتنفصل خمسُ حالاتٍ معرفيّةٍ لا ثلاث:

    صدقٌ مثبت ≠ مخالفةٌ مثبتة ≠ دليلٌ غيرُ مكتمل
    ≠ فحصٌ حجبه شرطٌ سابق ≠ لا دعوى أصلًا

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

__all__ = [
    "A_BLOCKED_DEPENDENT_IS_NOT_MISSING_EVIDENCE",
    "NO_CLAIM_IS_NOT_AN_AGREEMENT",
    "NO_DEFAULT_SUCCESS_AND_NO_DEFAULT_BLOCK",
    "CheckStanding",
    "ExecutionOutcome",
    "Identity",
    "LawCheckEntry",
    "Violation",
]


NO_CLAIM_IS_NOT_AN_AGREEMENT: Final[str] = (
    "غيابُ الدعوى ليس تصديقًا لها: هويّةٌ لم تُعلَن لا يُقال إنّها وافقت الناتج، "
    "فـ«لا دعوى» منزلةٌ ثالثةٌ بجانب الموافقة والمخالفة لا اختصارٌ لإحداهما"
)

A_BLOCKED_DEPENDENT_IS_NOT_MISSING_EVIDENCE: Final[str] = (
    "القانونُ المحجوبُ ليس دليلًا ناقصًا: عدمُ تنفيذه سببُه حجبُ قانونٍ سابقٍ "
    "لمادّته، لا نقصٌ في دليل القضيّة؛ وخلطُهما يُظهِر المحجوبَ مؤجَّلًا"
)

NO_DEFAULT_SUCCESS_AND_NO_DEFAULT_BLOCK: Final[str] = (
    "لا نجاحَ افتراضيَّ ولا حجبَ افتراضيّ: كلُّ قانونٍ يُقيَّم بنفسه، والحكمُ "
    "يُجمَع من المنازل المُسجَّلة لا من صمتٍ يُقرَأ في أحد الاتّجاهين"
)


class ExecutionOutcome(Enum):
    """حكمُ التنفيذ؛ مفردةٌ مغلقةٌ ليس فيها عضوٌ لبطلان التكوين ألبتّة."""

    PASS = "pass"
    BLOCK = "block"
    DEFER = "defer"


class CheckStanding(Enum):
    """منزلةُ فحصِ قانونٍ واحد؛ خمسُ حالاتٍ لا تُضغَط في ثلاث."""

    SATISFIED = "satisfied"
    VIOLATED = "violated"
    UNRESOLVED = "unresolved"
    NOT_EVALUATED_BY_PREREQUISITE = "not_evaluated_by_prerequisite"
    NOT_APPLICABLE_NO_CLAIM = "not_applicable_no_claim"

    @property
    def bears_on_the_outcome(self) -> bool:
        """أتدخل هذه المنزلةُ في جمع الحكم؟ والاستثناءُ مُسمًّى لا مُستنتَج."""

        return self in (
            CheckStanding.SATISFIED,
            CheckStanding.VIOLATED,
            CheckStanding.UNRESOLVED,
        )


@dataclass(frozen=True, slots=True)
class Identity:
    """هويّةُ مستوًى: مُعرِّفُه وبصمتُه معًا؛ ومُعرِّفٌ بلا بصمةٍ نصفُ هويّة."""

    id: str
    content_id: str

    def __post_init__(self) -> None:
        for value, label in ((self.id, "المُعرِّف"), (self.content_id, "البصمة")):
            if not isinstance(value, str) or not value.strip():
                raise TypeError(f"{label} نصٌّ غير فارغ")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الهويّة للبصمة."""

        return {"id": self.id, "content_id": self.content_id}


@dataclass(frozen=True, slots=True)
class LawCheckEntry:
    """سطرُ أثرٍ واحد: القانونُ ومنزلتُه، وموضوعُه، والمتوقَّعُ والملحوظ."""

    law: str
    standing: CheckStanding
    subject_id: str | None
    expected: Identity | None
    observed: Identity | None
    blocked_by: str | None

    def __post_init__(self) -> None:
        if not isinstance(self.standing, CheckStanding):
            raise TypeError("منزلةُ الفحص عضوٌ في مفردتها المغلقة")
        if not isinstance(self.law, str) or not self.law.strip():
            raise TypeError("اسمُ القانون نصٌّ غير فارغ")
        blocked = self.standing is CheckStanding.NOT_EVALUATED_BY_PREREQUISITE
        if blocked != (self.blocked_by is not None):
            raise TypeError(
                "القانونُ المحجوبُ يُسمّي حاجبَه، وغيرُ المحجوب لا حاجبَ له؛ و"
                + A_BLOCKED_DEPENDENT_IS_NOT_MISSING_EVIDENCE
            )
        if self.standing is CheckStanding.NOT_APPLICABLE_NO_CLAIM:
            if self.expected is not None:
                raise TypeError(NO_CLAIM_IS_NOT_AN_AGREEMENT)

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى السطر للبصمة."""

        return {
            "law": self.law,
            "standing": self.standing.value,
            "subject_id": self.subject_id,
            "expected": None
            if self.expected is None
            else self.expected.as_canonical_content(),
            "observed": None
            if self.observed is None
            else self.observed.as_canonical_content(),
            "blocked_by": self.blocked_by,
        }


@dataclass(frozen=True, slots=True)
class Violation:
    """مخالفةٌ ثبتت: قانونُها وموضوعُها، والمتوقَّعُ والملحوظُ بلا نثرٍ يفسّرهما."""

    law: str
    subject_id: str | None
    expected: Identity | None
    observed: Identity | None

    def __post_init__(self) -> None:
        if not isinstance(self.law, str) or not self.law.strip():
            raise TypeError("اسمُ القانون نصٌّ غير فارغ")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى المخالفة للبصمة."""

        return {
            "law": self.law,
            "subject_id": self.subject_id,
            "expected": None
            if self.expected is None
            else self.expected.as_canonical_content(),
            "observed": None
            if self.observed is None
            else self.observed.as_canonical_content(),
        }
