"""طريقُ توليد اللفظ وتاريخُه — لا حالُ علاقته بمدلوله.

`RelationStateIsNotGenerationHistory`. السباعيّةُ في
`signifier_signified_relation` تصف **حالَ** العلاقة الآن، وهذه المفردةُ تصف
**كيف صار** اللفظُ إلى العربيّة: وضعًا، أو اشتقاقًا، أو تعريبًا، أو نقلًا، أو
بقيّةً لا تنتمي إلى الأربعة. والأعضاءُ خمسةٌ لا تشترك في اسمٍ واحدٍ مع أعضاء
السباعيّة، واختبارُ التمايز يفحص ذلك بنيويًّا لا بالوصف.

**والبقيّةُ عضوٌ لا فراغ**: `NoPathIsNotTheDefaultPath`. السكوتُ عن الطريق ليس
طريقًا افتراضيًّا، و`RESIDUAL` تصريحٌ بأنّ الطريقَ لم يُحدَّد لا ادّعاءُ طريق.

**وأربعةُ ردودٍ بنيويّة** تُنفَّذ هنا لأنّ كلًّا منها قفزةٌ من شاهدٍ إلى حكم:

- `DerivationPatternIsNotDerivationHistory` — موافقةُ الوزن ليست تاريخَ اشتقاق،
  و`WadhIsNotInferredFromForm`: الوضعُ لا يُستنبَط من الصورة.
- `ForeignLookIsNotTarib` — غرابةُ الصورة ليست تعريبًا، ولو ثبت التعريبُ فـ
  `ForeignOriginIsNotCurrentArabicIdentity`.
- `SemanticShiftIsNotNaql` — اختلافُ المعنى ليس نقلًا مُثبَتًا.
- `FrequencyIsNotWadh` — الشيوعُ ليس وضعًا، وهو عينُ
  `StatisticsRaiseDirayaNeverMakeRiwaya` المُقرَّر في `wad_naql`.

و`DerivedFormDoesNotAuthorizeDerivedMeaning`: إثباتُ الطريق لا يُرخِّص معنًى.

تسجيلٌ لا سلطة.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

from .lexical_evidence_specification import (
    DERIVED_FORM_DOES_NOT_AUTHORIZE_DERIVED_MEANING_NOTE,
    FOREIGN_ORIGIN_IS_NOT_CURRENT_ARABIC_IDENTITY_NOTE,
    NO_PATH_IS_NOT_THE_DEFAULT_PATH_NOTE,
    RELATION_STATE_IS_NOT_GENERATION_HISTORY_NOTE,
    WADH_IS_NOT_INFERRED_FROM_FORM_NOTE,
)
from .wad_naql import STATISTICS_RAISE_DIRAYA_NEVER_MAKE_RIWAYA_NOTE

__all__ = [
    "REFUSED_PATH_EVIDENCE_NOTES",
    "LexicalGenerationPath",
    "LexicalPathCandidate",
    "LexicalPathError",
    "RefusedPathEvidenceKind",
    "refuse_path_evidence_kind",
]


class LexicalPathError(ValueError):
    """رفضٌ في طريق التوليد؛ ولا يُحمَل المدخلُ على البقيّة."""


class LexicalGenerationPath(Enum):
    """طرقُ صيرورة اللفظ؛ خماسيّةٌ مغلقةٌ بأسماء لا تشارك السباعيّة شيئًا."""

    WADH_HISTORY = "WADH_HISTORY"
    DERIVATION = "DERIVATION"
    TARIB = "TARIB"
    TRANSMISSION = "TRANSMISSION"
    RESIDUAL = "RESIDUAL"


class RefusedPathEvidenceKind(Enum):
    """أجناسُ الشاهد المردودة بنيويًّا؛ عضويّتُها تصريحٌ بالردّ لا بالقبول."""

    DERIVATION_PATTERN = "DERIVATION_PATTERN"
    FOREIGN_LOOK = "FOREIGN_LOOK"
    SEMANTIC_SHIFT = "SEMANTIC_SHIFT"
    FREQUENCY = "FREQUENCY"


REFUSED_PATH_EVIDENCE_NOTES: Final[dict[RefusedPathEvidenceKind, str]] = {
    RefusedPathEvidenceKind.DERIVATION_PATTERN: (
        "DerivationPatternIsNotDerivationHistory: موافقةُ الوزن صورةٌ حاضرة، "
        "وتاريخُ الاشتقاق خبرٌ عن ماضٍ لا تحمله الصورة؛ "
        + WADH_IS_NOT_INFERRED_FROM_FORM_NOTE
    ),
    RefusedPathEvidenceKind.FOREIGN_LOOK: (
        "ForeignLookIsNotTarib: غرابةُ الصورة انطباعٌ لا روايةَ تعريب؛ "
        + FOREIGN_ORIGIN_IS_NOT_CURRENT_ARABIC_IDENTITY_NOTE
    ),
    RefusedPathEvidenceKind.SEMANTIC_SHIFT: (
        "SemanticShiftIsNotNaql: اختلافُ المعنى أثرٌ يحتمل النقلَ وغيرَه، "
        "والنقلُ دعوى تحتاج ناقلًا مُسمًّى لا فرقًا مُلاحَظًا"
    ),
    RefusedPathEvidenceKind.FREQUENCY: (
        "FrequencyIsNotWadh: الشيوعُ عددٌ في الاستعمال لا وضعٌ في اللغة؛ "
        + STATISTICS_RAISE_DIRAYA_NEVER_MAKE_RIWAYA_NOTE
    ),
}


def refuse_path_evidence_kind(kind: RefusedPathEvidenceKind) -> None:
    """ارفض جنسَ شاهدٍ مردودًا برفعٍ صريحٍ يحمل نصَّ قانونه."""

    if not isinstance(kind, RefusedPathEvidenceKind):
        raise LexicalPathError("جنسُ الشاهد المردود عضوٌ في مفردته الرباعية.")
    raise LexicalPathError(REFUSED_PATH_EVIDENCE_NOTES[kind])


@dataclass(frozen=True, slots=True)
class LexicalPathCandidate:
    """مُرشَّحُ طريقٍ: عضوٌ من الخماسيّة، وناقلٌ مُسمًّى، وأثرُ مصدره.

    و`RESIDUAL` وحدَه يُبنى بلا ناقلٍ مُسمًّى، لأنّه تصريحٌ بعدم التحديد؛ وما
    عداه دعوى طريقٍ فيلزمها من رواها.
    """

    signifier_ref: str
    path: LexicalGenerationPath
    reported_by: str | None
    source_trace: str

    def __post_init__(self) -> None:
        if not isinstance(self.signifier_ref, str) or not self.signifier_ref.strip():
            raise LexicalPathError("مرجعُ الدالّ نصٌّ غير فارغ.")
        if not isinstance(self.path, LexicalGenerationPath):
            raise LexicalPathError(NO_PATH_IS_NOT_THE_DEFAULT_PATH_NOTE)
        if not isinstance(self.source_trace, str) or not self.source_trace.strip():
            raise LexicalPathError("أثرُ المصدر نصٌّ غير فارغ.")
        if self.path is LexicalGenerationPath.RESIDUAL:
            if self.reported_by is not None:
                raise LexicalPathError(
                    "`RESIDUAL` تصريحٌ بعدم التحديد، فلا يُنسَب إلى ناقل."
                )
        elif not isinstance(self.reported_by, str) or not self.reported_by.strip():
            raise LexicalPathError(
                "دعوى الطريق تلزمها روايةٌ عن ناقلٍ مُسمًّى؛ "
                + WADH_IS_NOT_INFERRED_FROM_FORM_NOTE
            )

    @property
    def authorizes_derived_meaning(self) -> bool:
        """إثباتُ الطريق لا يُرخِّص معنًى؛ الجوابُ ثابت."""

        return False

    @property
    def meaning_note(self) -> str:
        return DERIVED_FORM_DOES_NOT_AUTHORIZE_DERIVED_MEANING_NOTE

    @property
    def separation_note(self) -> str:
        return RELATION_STATE_IS_NOT_GENERATION_HISTORY_NOTE
