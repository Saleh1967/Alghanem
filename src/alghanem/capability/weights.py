"""`G0.METRIC-0.HARDEN`: الأوزانُ مُعلَنةٌ أو الرقمُ غيرُ معرَّف.

تسعُ بوّاباتٍ نوعيّةٍ لا تصير رقمًا واحدًا بجمع مواضعها في التسلسل: الموضعُ
رتبةُ ترخيصٍ لا مقدار (`NoOrdinalGateArithmeticWithoutDeclaredWeights`). فإمّا
بروتوكولُ أوزانٍ مُعلَنٌ مُجمَّدٌ يُبرِّر وزنَ كلِّ بوّابةٍ بعينها، وإمّا يبقى
الرقمُ المركّبُ **غيرَ معرَّفٍ بسببٍ مُسنون**، لا صفرًا ولا تقديرًا.

وتسويةُ الأوزان ليست هروبًا من الاختيار: أن تُعطى المجالاتُ السبعةَ عشرَ وزنًا
واحدًا هندسةُ قياسٍ أخرى لا حقيقةٌ مُشتَقّة
(`EqualDomainWeightingIsStillAWeightingProtocol`).
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest
from .aggregate import DerivedRatio
from .laws import (
    EQUAL_DOMAIN_WEIGHTING_IS_STILL_A_WEIGHTING_PROTOCOL,
    NO_ORDINAL_GATE_ARITHMETIC_WITHOUT_DECLARED_WEIGHTS,
)
from .maturity import GATE_SEQUENCE, MaturityStage

__all__ = [
    "ATTESTABLE_GATES",
    "DeclaredScalar",
    "GateWeight",
    "MeasurementWeightProtocol",
    "MeasurementSemanticsError",
    "ScalarStanding",
    "UndeclaredScalar",
    "UndeclaredScalarReason",
    "derive_composite_coverage",
]


class MeasurementSemanticsError(ValueError):
    """رفضٌ بنيويٌّ مُسمًّى في دلاليّة القياس؛ لا رقمَ يخرج من وزنٍ غير مُعلَن."""


ATTESTABLE_GATES: Final[tuple[MaturityStage, ...]] = GATE_SEQUENCE[1:]
"""البوّاباتُ التسعُ التي تُشهَد؛ والغيابُ يُقاس بانتفائها لا يُوزَن."""


class ScalarStanding(Enum):
    """رتبةُ الرقم الموحَّد: مُعلَنُ الأوزان، أو غيرُ معرَّفٍ بسببٍ مُسنون."""

    DECLARED = "DECLARED"
    UNDECLARED = "UNDECLARED"


class UndeclaredScalarReason(Enum):
    """أسبابُ بقاء الرقم الموحَّد غيرَ معرَّف؛ مفردةٌ مغلقةٌ لا نصٌّ حُرّ."""

    NO_DECLARED_WEIGHT_PROTOCOL = "NO_DECLARED_WEIGHT_PROTOCOL"
    NO_DECLARED_DOMAIN_WEIGHT_PROTOCOL = "NO_DECLARED_DOMAIN_WEIGHT_PROTOCOL"
    NO_DECLARED_DEPENDENCY_GRAPH = "NO_DECLARED_DEPENDENCY_GRAPH"


@dataclass(frozen=True)
class UndeclaredScalar:
    """رقمٌ موحَّدٌ غيرُ معرَّف: اسمُه، ورتبتُه، وسببُ امتناعه؛ لا قيمةَ فيه."""

    name: str
    reason: UndeclaredScalarReason

    def __post_init__(self) -> None:
        if type(self.name) is not str or not self.name.strip():
            raise MeasurementSemanticsError("an undeclared scalar is still named")
        if not isinstance(self.reason, UndeclaredScalarReason):
            raise MeasurementSemanticsError(
                "an undeclared scalar names a sealed reason, never a free text"
            )

    @property
    def standing(self) -> ScalarStanding:
        """رتبةُ هذا الرقم: غيرُ مُعلَنٍ ما دام بروتوكولُ وزنه غائبًا."""

        return ScalarStanding.UNDECLARED

    @property
    def value(self) -> None:
        """لا قيمةَ لرقمٍ بلا بروتوكول وزن؛ و`None` هنا إفصاحٌ لا نقص."""

        return None

    @property
    def reading_law(self) -> str:
        """سقفُ قراءة الامتناع، محمولًا معه لا مفصولًا عنه."""

        if self.reason is UndeclaredScalarReason.NO_DECLARED_DOMAIN_WEIGHT_PROTOCOL:
            return EQUAL_DOMAIN_WEIGHTING_IS_STILL_A_WEIGHTING_PROTOCOL
        return NO_ORDINAL_GATE_ARITHMETIC_WITHOUT_DECLARED_WEIGHTS

    def as_canonical_content(self) -> dict[str, object]:
        """المحتوى القانونيّ للرقم غير المعرَّف."""

        return {
            "name": self.name,
            "standing": self.standing.value,
            "value": None,
            "reason": self.reason.value,
        }


@dataclass(frozen=True)
class GateWeight:
    """وزنُ بوّابةٍ واحدةٍ في بروتوكولٍ مُعلَن، ومعه تبريرُه لا رقمُه وحدَه."""

    gate: MaturityStage
    weight: int
    justification: str

    def __post_init__(self) -> None:
        if not isinstance(self.gate, MaturityStage):
            raise MeasurementSemanticsError("a gate weight weighs a maturity gate")
        if not self.gate.is_an_attestable_gate:
            raise MeasurementSemanticsError("absence is measured, never weighted")
        if type(self.weight) is not int or self.weight <= 0:
            raise MeasurementSemanticsError(
                f"«{self.gate.value}» requires a positive integer weight"
            )
        if type(self.justification) is not str or not self.justification.strip():
            raise MeasurementSemanticsError(
                f"«{self.gate.value}» requires a justification for its weight; "
                "a weight without a reason is an assumption wearing a number"
            )

    def as_canonical_content(self) -> dict[str, object]:
        """المحتوى القانونيّ لوزن البوّابة."""

        return {
            "gate": self.gate.value,
            "weight": self.weight,
            "justification": self.justification,
        }


@dataclass(frozen=True)
class MeasurementWeightProtocol:
    """بروتوكولُ أوزانٍ مُعلَنٌ مُجمَّد: كلُّ بوّابةٍ بوزنها وتبريرها، لا افتراضَ تسوية."""

    protocol_id: str
    weights: tuple[GateWeight, ...]

    def __post_init__(self) -> None:
        if type(self.protocol_id) is not str or not self.protocol_id.strip():
            raise MeasurementSemanticsError("a weight protocol requires a protocol_id")
        if type(self.weights) is not tuple or not self.weights:
            raise MeasurementSemanticsError("a weight protocol declares its weights")
        declared = [item.gate for item in self.weights]
        if len(set(declared)) != len(declared):
            raise MeasurementSemanticsError("a gate is weighed once, never twice")
        if set(declared) != set(ATTESTABLE_GATES):
            raise MeasurementSemanticsError(
                "a weight protocol covers every attestable gate exactly; a silent "
                "gap is an undeclared weight of zero"
            )

    @property
    def total_weight(self) -> int:
        """مجموعُ الأوزان المُعلَنة؛ مقامُ الرقم المركّب لا يُخترَع."""

        return sum(item.weight for item in self.weights)

    def weight_of(self, gate: MaturityStage) -> int:
        """وزنُ بوّابةٍ بعينها في هذا البروتوكول."""

        for item in self.weights:
            if item.gate is gate:
                return item.weight
        raise MeasurementSemanticsError(f"«{gate.value}» is not weighed here")

    def as_canonical_content(self) -> dict[str, object]:
        """المحتوى القانونيّ للبروتوكول."""

        by_gate = {item.gate: item for item in self.weights}
        return {
            "protocol_id": self.protocol_id,
            "weights": [
                by_gate[gate].as_canonical_content() for gate in ATTESTABLE_GATES
            ],
            "total_weight": self.total_weight,
        }

    @property
    def protocol_digest(self) -> str:
        """مُلخَّصُ البروتوكول؛ رقمان على بروتوكولين ليسا مقارنة."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))


@dataclass(frozen=True)
class DeclaredScalar:
    """رقمٌ موحَّدٌ صادرٌ عن بروتوكول أوزانٍ مُعلَن، محمولٌ بهويّة بروتوكوله."""

    name: str
    ratio: DerivedRatio
    protocol_id: str
    protocol_digest: str

    @property
    def standing(self) -> ScalarStanding:
        """رتبةُ هذا الرقم: مُعلَنُ الأوزان."""

        return ScalarStanding.DECLARED

    @property
    def value(self) -> float | None:
        """قيمةُ الرقم المركّب، محمولةً بمقامها في `ratio`."""

        return self.ratio.value

    def as_canonical_content(self) -> dict[str, object]:
        """المحتوى القانونيّ للرقم المُعلَن."""

        return {
            "name": self.name,
            "standing": self.standing.value,
            "value": self.value,
            "ratio": self.ratio.as_canonical_content(),
            "protocol_id": self.protocol_id,
            "protocol_digest": self.protocol_digest,
        }


def derive_composite_coverage(
    protocol: MeasurementWeightProtocol,
    gate_coverage: Mapping[MaturityStage, DerivedRatio],
    *,
    name: str = "CompositeCoverage",
) -> DeclaredScalar:
    """اشتقّ الرقمَ المركّبَ من تغطيات البوّابات وأوزانها المُعلَنة وحدَها.

    لا يدخل هنا `gate_index` البتّة: البسطُ مجموعُ (وزنِ البوّابة × ما بلغها من
    أوراق)، والمقامُ (مجموعُ الأوزان × عددِ الأوراق) — فالرقمُ وسطٌ موزونٌ
    بأوزانٍ مُبرَّرة، لا جمعُ رتبٍ.
    """

    if not isinstance(protocol, MeasurementWeightProtocol):
        raise MeasurementSemanticsError(
            "a composite figure requires a declared weight protocol; without one "
            "it stays undefined"
        )
    missing = set(ATTESTABLE_GATES) - set(gate_coverage)
    if missing:
        raise MeasurementSemanticsError(
            f"every attestable gate is covered before it is weighed: "
            f"{sorted(gate.value for gate in missing)}"
        )
    denominators = {gate_coverage[gate].denominator for gate in ATTESTABLE_GATES}
    if len(denominators) != 1:
        raise MeasurementSemanticsError(
            "gate coverages are weighed over one shared denominator only"
        )
    leaf_total = denominators.pop()
    numerator = sum(
        protocol.weight_of(gate) * gate_coverage[gate].numerator
        for gate in ATTESTABLE_GATES
    )
    sources = {gate_coverage[gate].denominator_source for gate in ATTESTABLE_GATES}
    source = sources.pop() if len(sources) == 1 else "mixed_denominator_sources"
    return DeclaredScalar(
        name=name,
        ratio=DerivedRatio(
            numerator=numerator,
            denominator=protocol.total_weight * leaf_total,
            denominator_source=f"{source} × {protocol.protocol_id}",
        ),
        protocol_id=protocol.protocol_id,
        protocol_digest=protocol.protocol_digest,
    )
