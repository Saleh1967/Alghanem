"""`Σ_L`: ترتيبُ منزلةٍ أعلى، لا نسخٌ ولا منافسة.

    Representation(x)      = (Carrier, State)        ← كيف يوجد الكيان؟
    LinguisticFunction(x)  = RelationalRole(x)       ← ماذا يفعل بوصفه لغة؟

**والنسبيّةُ ليست منافسة** (`RelativizationIsNotCompetition`): بيانٌ يُنزِل
نتيجةً قائمةً منزلتَها لا يُفنّدها. فنصُّ `G0.FLT-1.Q` يبقى بلفظه وبصمته
ونتيجتِه المقروءة، ولا `SupersessionRecord` هنا ولا `CompetingStatementRecord`؛
وإنّما تُسجَّل علاقةُ مستوًى بمستوًى.

**والمنافسةُ لا تُعلَن إلا بتناقضٍ مُبرهَن** (`OnlyADemonstratedContradictionCompetes`):
ما دام الأصلان يجيبان سؤالين مختلفين فلا تعارضَ بينهما؛ ومن أعلن التنافسَ بلا
تناقضٍ محدَّدٍ **مُبيَّنِ الموضع** حوّل ترتيبَ المنزلة إلى دعوى نقضٍ لم تُبرهَن.
ولذلك يُرفَض بناءُ سجلّ نسبيّةٍ يُعلن تناقضًا: التناقضُ المُبرهَن يطلب سجلًّا من
جنسٍ آخر لا تُصدِره هذه الوحدةُ ولا أيُّ وحدةٍ في هذه الشجرة اليوم.

**ولا بصمةَ تُكتَب باليد**: إشارةُ النصّ المُرتَّبةِ منزلتُه تُبنى من بصمته
المُشتَقّة في موضعها؛ ونسخُ بصمةٍ في هذا الموضع يُنشئ نسختين تنحرفان.

تسجيلٌ لا سلطة: لا حكمَ هنا، ولا استيرادَ من `kernel/` ولا من `arabic/`.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

__all__ = [
    "ONLY_A_DEMONSTRATED_CONTRADICTION_COMPETES",
    "RELATIVIZATION_IS_NOT_COMPETITION",
    "ContradictionStanding",
    "HigherOrderRelativizationRecord",
    "RelativizationError",
    "RelativizedStatementRef",
]


class RelativizationError(ValueError):
    """رفضٌ عند الإنشاء: نسبيّةٌ تُعلن تناقضًا، أو إشارةٌ بلا بصمة."""


RELATIVIZATION_IS_NOT_COMPETITION: Final[str] = (
    "ترتيبُ المنزلة ليس منافسة: نصٌّ يُبيّن أنّ نتيجةً قائمةً تجيب سؤالًا آخر "
    "لا يَنسخها ولا يزاحمها، ويبقى النصُّ الأوّلُ بلفظه وبصمته ونتيجته"
)

ONLY_A_DEMONSTRATED_CONTRADICTION_COMPETES: Final[str] = (
    "لا منافسةَ إلا بتناقضٍ مُبرهَنٍ مُبيَّنِ الموضع: وسجلُّ النسبيّة لا يحمل "
    "تناقضًا، فالتناقضُ المُبرهَن يطلب سجلًّا من جنسٍ آخر لا تُصدِره هذه الوحدة"
)


class ContradictionStanding(Enum):
    """موقفُ التناقض بين المستويين؛ عضوانِ لا ثالثَ لهما."""

    NO_CONTRADICTION_DEMONSTRATED = "لم_يُبرهَن_تناقضٌ_بين_المستويين"
    CONTRADICTION_DEMONSTRATED = "تناقضٌ_مُبرهَنٌ_يطلب_سجلًّا_من_جنسٍ_آخر"


@dataclass(frozen=True, slots=True)
class RelativizedStatementRef:
    """إشارةٌ إلى نصٍّ قائمٍ رُتِّبت منزلتُه: اسمُه، وموضعُه، وبصمتُه المُشتَقّة."""

    statement_id: str
    module_path: str
    text_digest: str

    def __post_init__(self) -> None:
        for value, label in (
            (self.statement_id, "اسمُ النصّ"),
            (self.module_path, "موضعُ النصّ في الشجرة"),
            (self.text_digest, "بصمةُ النصّ"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise RelativizationError(f"{label} نصٌّ غير فارغ")
        if len(self.text_digest) != 64 or any(
            character not in "0123456789abcdef" for character in self.text_digest
        ):
            raise RelativizationError(
                "بصمةُ النصّ بصمةٌ معياريّةٌ مُشتَقّةٌ من موضعها، لا وصفٌ يُكتَب"
            )

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الإشارة للبصمة."""

        return {
            "statement_id": self.statement_id,
            "module_path": self.module_path,
            "text_digest": self.text_digest,
        }


@dataclass(frozen=True, slots=True)
class HigherOrderRelativizationRecord:
    """سجلُّ ترتيبِ منزلةٍ بين قانون التمثيل والوظيفة اللغويّة."""

    record_id: str
    relativized: RelativizedStatementRef
    representation_question: str
    relational_question: str
    contradiction_standing: ContradictionStanding
    what_would_make_it_competing: str

    def __post_init__(self) -> None:
        for value, label in (
            (self.record_id, "اسمُ السجلّ"),
            (self.representation_question, "سؤالُ التمثيل"),
            (self.relational_question, "سؤالُ الوظيفة اللغويّة"),
            (self.what_would_make_it_competing, "ما الذي يجعله منافسًا"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise RelativizationError(f"{label} نصٌّ غير فارغ")
        if not isinstance(self.relativized, RelativizedStatementRef):
            raise RelativizationError("النصُّ المُرتَّبةُ منزلتُه إشارةٌ مبصومةٌ بنوعها")
        if not isinstance(self.contradiction_standing, ContradictionStanding):
            raise RelativizationError("موقفُ التناقض عضوٌ في مفردته المغلقة")
        if (
            self.contradiction_standing
            is ContradictionStanding.CONTRADICTION_DEMONSTRATED
        ):
            raise RelativizationError(ONLY_A_DEMONSTRATED_CONTRADICTION_COMPETES)
        if self.representation_question == self.relational_question:
            raise RelativizationError(
                "سؤالان متّحدان ليسا مستويين: اتّحادُهما يُعيد التنافسَ الذي "
                "قام هذا السجلُّ لمنعه"
            )

    @property
    def supersedes(self) -> bool:
        """أينسخ هذا السجلُّ النصَّ المُرتَّبةَ منزلتُه؟ لا، وخاصّيّتُه مُشتَقّة."""

        return False

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى السجلّ للبصمة."""

        return {
            "record_id": self.record_id,
            "relativized": self.relativized.as_canonical_content(),
            "representation_question": self.representation_question,
            "relational_question": self.relational_question,
            "contradiction_standing": self.contradiction_standing.value,
            "what_would_make_it_competing": self.what_would_make_it_competing,
        }
