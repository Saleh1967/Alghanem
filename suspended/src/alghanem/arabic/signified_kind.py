"""المحورُ الثاني: **المدلولُ وحدَه** — قسمتُه الخماسيّةُ المُبرهَنة، بلا ترجيح.

`SignifiedIsNotSemanticConcept`. المدلولُ في هذه الشجرة ليس «مفهومًا دلاليًّا»
يُسقَط على كلّ وقوع: القسمةُ مُبرهَنةٌ في `madlul_alone_formal` على خمسةِ
أقسامٍ — معنًى، ولفظٌ مفردٌ مستعمَل، ولفظٌ مفردٌ مهمَل، ولفظٌ مركّبٌ مستعمَل،
وهذيان — فيُستورَد `MadlulSection` مجالًا مُغلَقًا ولا يُكتَب ثانيةً.

**ولا انزلاقَ إلى «معنًى»**: لا قيمةَ افتراضيّةً، ولا اشتقاقَ قسمٍ من صورة
الوقوع، ولا حملَ المسكوتِ عنه على أوّل الأقسام. القسمُ يُصرَّح به مع دليله أو
لا يُبنى المُرشَّح؛ و`EmptyIsNotAbsent`: السكوتُ عن القسم ليس قسمًا.

**وحملُ عضوٍ ليس إسنادًا ثابتًا**: `ProvenVocabularyIsNotProvenAssignment`.

هذا المحورُ **لا يستورد** محورَ الدالّ ولا محورَ العلاقة.

تسجيلٌ لا سلطة.
"""

from __future__ import annotations

from dataclasses import dataclass

from .lexical_evidence_layer import PrimarySignificationAnchor
from .lexical_evidence_specification import (
    EMPTY_IS_NOT_ABSENT_NOTE,
    PROVEN_VOCABULARY_IS_NOT_PROVEN_ASSIGNMENT_NOTE,
)
from .madlul_alone_formal import MadlulSection

__all__ = [
    "SignifiedKindCandidate",
    "SignifiedKindError",
    "refuse_default_signified_section",
]


class SignifiedKindError(ValueError):
    """رفضٌ في محور المدلول وحدَه."""


def refuse_default_signified_section(section: object) -> None:
    """ارفض قسمًا غائبًا يُراد حملُه على «معنًى»؛ فالسكوتُ ليس قسمًا."""

    if not isinstance(section, MadlulSection):
        raise SignifiedKindError(EMPTY_IS_NOT_ABSENT_NOTE)


@dataclass(frozen=True, slots=True)
class SignifiedKindCandidate:
    """مُرشَّحُ قسمٍ للمدلول: عضوٌ من القسمة المُبرهَنة، بدليله ومرساته."""

    anchor: PrimarySignificationAnchor
    section: MadlulSection
    evidence_ref: str

    def __post_init__(self) -> None:
        if not isinstance(self.anchor, PrimarySignificationAnchor):
            raise SignifiedKindError(
                "مُرشَّحُ القسم إسقاطٌ عن مرساةٍ مُرخَّصة؛ "
                + PROVEN_VOCABULARY_IS_NOT_PROVEN_ASSIGNMENT_NOTE
            )
        refuse_default_signified_section(self.section)
        if not isinstance(self.evidence_ref, str) or not self.evidence_ref.strip():
            raise SignifiedKindError("مرجعُ الدليل نصٌّ غير فارغ.")

    @property
    def is_proven_assignment(self) -> bool:
        """حملُ عضوٍ مُبرهَنٍ ليس إسنادًا مُبرهَنًا؛ الجوابُ ثابت."""

        return False

    @property
    def assignment_note(self) -> str:
        return PROVEN_VOCABULARY_IS_NOT_PROVEN_ASSIGNMENT_NOTE
