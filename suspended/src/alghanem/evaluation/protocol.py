"""`G0.EVAL-0.PROTOCOL`: بروتوكولُ تقييمٍ مُجمَّدٌ، ونوعُه جزءٌ من هويّته.

    EvaluationProtocolKind
      =  FORMAL_CLASSIFICATION   يُعطى القارئُ الحواملَ والقواعدَ المسموحة
       |  RULE_DISCOVERY         يُعطى أقلَّ، ويُختبَر اكتشافُه للعلاقة

النوعُ يدخل بصمةَ البروتوكول، فلا يُقارَن تشغيلٌ من نوعٍ بتشغيلٍ من نوعٍ آخر ولو
تشابهت مخرجاتُهما. ومادّةُ التجربتين لا تُبنى هنا: هذا الطورُ يُجمِّد الهويّة
وحدَها، ولا يُجري تجربةً ولا مقارنة.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from ..canonical_content import canonical_bytes, canonical_digest
from ..prior_fiber import SuccessCriterion
from .laws import EvaluationError

__all__ = [
    "EvaluationProtocolKind",
    "FrozenEvaluationProtocol",
]


class EvaluationProtocolKind(Enum):
    """نوعُ البروتوكول؛ مفردةٌ مغلقةٌ تدخل بصمتَه ولا تُقرَأ وصفًا جانبيًّا."""

    FORMAL_CLASSIFICATION = "formal_classification"
    RULE_DISCOVERY = "rule_discovery"

    @property
    def declares_the_admissible_rules(self) -> bool:
        """أتُعطى القواعدُ المسموحة للقارئ في هذا النوع؟"""

        return self is EvaluationProtocolKind.FORMAL_CLASSIFICATION


def _require_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise EvaluationError(f"{label} نصٌّ غير فارغ")
    return value


@dataclass(frozen=True, slots=True)
class FrozenEvaluationProtocol:
    """بروتوكولٌ مُجمَّد: نوعُه، ومعاييرُه، وإحالةُ بقاياه، وصيغةُ حمولته."""

    protocol_id: str
    kind: EvaluationProtocolKind
    success_criteria: tuple[SuccessCriterion, ...]
    residual_policy_ref: str
    payload_scheme: str
    contract_interface_version: str

    def __post_init__(self) -> None:
        _require_text(self.protocol_id, "مُعرِّفُ البروتوكول")
        if not isinstance(self.kind, EvaluationProtocolKind):
            raise EvaluationError("نوعُ البروتوكول عضوٌ في مفردته المغلقة")
        if not isinstance(self.success_criteria, tuple) or not self.success_criteria:
            raise EvaluationError("بروتوكولٌ بلا معيارِ نجاحٍ لا يُقيِّم شيئًا")
        for criterion in self.success_criteria:
            if not isinstance(criterion, SuccessCriterion):
                raise EvaluationError("معيارٌ خارج مفردته المغلقة")
        if len(set(self.success_criteria)) != len(self.success_criteria):
            raise EvaluationError("معيارٌ مُكرَّر؛ والمكرّرُ يُرفَض لا يُطوى")
        _require_text(self.residual_policy_ref, "إحالةُ سياسة البقايا")
        _require_text(self.payload_scheme, "بيانُ صيغة الحمولة")
        _require_text(self.contract_interface_version, "إصدارُ واجهة العقد")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى البروتوكول للبصمة."""

        return {
            "protocol_id": self.protocol_id,
            "kind": self.kind.value,
            "success_criteria": [
                criterion.value
                for criterion in sorted(
                    self.success_criteria, key=lambda item: item.value
                )
            ],
            "residual_policy_ref": self.residual_policy_ref,
            "payload_scheme": self.payload_scheme,
            "contract_interface_version": self.contract_interface_version,
        }

    @property
    def protocol_digest(self) -> str:
        """بصمةُ البروتوكول؛ يدخلها نوعُه، فنوعان لا يشتركان في بصمة."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))
