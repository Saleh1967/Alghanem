"""`G0.EVAL-0.RESIDUAL`: البقيّةُ عضوٌ مُسمًّى برمزٍ وسببٍ وشاهد، لا نصٌّ حرّ.

    AResidualIsNamedNotStringly

نصٌّ حرٌّ تتغيّر دلالتُه بين طورٍ وطور: يُقرَأ اليومَ مُعرِّفَ عضوٍ متروك، ويُقرَأ
غدًا سببَ تركه. والبقيّةُ هنا بنيةٌ مغلقة: العضوُ الذي تُرِك، ورمزُ تركه من مفردةٍ
مغلقة، وهل يُعيق، ولماذا، وأينَ شاهدُه.

    RunResidual
      =  member_id
       + residual_code
       + blocking
       + reason
       + evidence_ref

و`blocking` يُسجَّل ولا يُبنى عليه حكمٌ في هذا الطور: الفتحُ ليس حكمًا، فلا تمنعه
بقيّةٌ مُعيقة. وأثرُ الإعاقة في الحكم يقرّره طورٌ لاحق، لا هذا.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from ..canonical_content import canonical_bytes, canonical_digest
from .laws import A_RESIDUAL_IS_NAMED_NOT_STRINGLY, EvaluationError

__all__ = [
    "ResidualCode",
    "RunResidual",
]


class ResidualCode(Enum):
    """رموزُ البقايا؛ مفردةٌ مغلقةٌ تدخل بصمةَ البقيّة ولا تُقرَأ وصفًا حرًّا."""

    UNCLASSIFIED_BY_READER = "unclassified_by_reader"
    AMBIGUOUS_BETWEEN_ADMISSIBLE_LABELS = "ambiguous_between_admissible_labels"
    INPUT_OUTSIDE_DECLARED_GEOMETRY = "input_outside_declared_geometry"
    REFUSED_BY_READER = "refused_by_reader"
    READER_RAISED_ON_MEMBER = "reader_raised_on_member"


def _require_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise EvaluationError(f"{label} نصٌّ غير فارغ")
    return value


@dataclass(frozen=True, slots=True)
class RunResidual:
    """بقيّةٌ مُسمّاة: عضوٌ مُترَك، ورمزُ تركه، وصفةُ إعاقته، وسببُه، وشاهدُه."""

    member_id: str
    residual_code: ResidualCode
    blocking: bool
    reason: str
    evidence_ref: str

    def __post_init__(self) -> None:
        _require_text(self.member_id, "مُعرِّفُ العضو في البقيّة")
        if not isinstance(self.residual_code, ResidualCode):
            raise EvaluationError("رمزُ البقيّة عضوٌ في مفردته المغلقة لا نصٌّ حرّ")
        if type(self.blocking) is not bool:
            raise EvaluationError("صفةُ الإعاقة قيمةٌ ثنائيّةٌ مُعلَنة")
        _require_text(self.reason, "سببُ البقيّة")
        _require_text(self.evidence_ref, "إحالةُ شاهد البقيّة")

    @property
    def naming_law(self) -> str:
        """قانونُ تسمية البقيّة: رمزٌ وسببٌ وشاهد، لا نصٌّ يتغيّر معناه."""

        return A_RESIDUAL_IS_NAMED_NOT_STRINGLY

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى البقيّة للبصمة والسجلّ."""

        return {
            "member_id": self.member_id,
            "residual_code": self.residual_code.value,
            "blocking": self.blocking,
            "reason": self.reason,
            "evidence_ref": self.evidence_ref,
        }

    @property
    def residual_digest(self) -> str:
        """بصمةُ البقيّة؛ مُشتَقّةٌ لا مكتوبة."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))
