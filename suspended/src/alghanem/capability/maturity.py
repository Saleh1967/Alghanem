"""`G0.METRIC-0`: سُلَّمُ النضج بوّاباتٍ مرتّبةً، لا مقاديرَ معرفيّةً تُجمَع.

عشرُ درجاتٍ من الغياب إلى إعادة الإنتاج. وترتيبُها ترتيبُ **إذنٍ**: الدرجةُ
الأعلى لا تُمنَح قبل أن تُغلَق كلُّ بوّابةٍ دونها، فالقفزُ فوق بوّابةٍ ليس
تسريعًا بل ادّعاءٌ بلا طريق (`StandingsAreGatesNotEpistemicMagnitudes`).

والدرجةُ صفرٌ ليست خطأً في البناء: هي الحالةُ المقيسةُ لقدرةٍ أُعلِنت في المقام
ولم تُبنَ بعد (`UnimplementedCapabilityMustRemainVisible`).
"""

from __future__ import annotations

from enum import Enum
from typing import Final

from .laws import STANDINGS_ARE_GATES_NOT_EPISTEMIC_MAGNITUDES

__all__ = [
    "GATE_SEQUENCE",
    "MaturityStage",
    "blocking_reason_for_gate",
    "stage_at_or_above",
]


class MaturityStage(Enum):
    """بوّاباتُ النضج مرتّبةً؛ الترتيبُ ترخيصٌ لا مقدارٌ يُجمَع."""

    S0_ABSENT = "S0_ABSENT"
    S1_DECLARED = "S1_DECLARED"
    S2_MODELED = "S2_MODELED"
    S3_EXECUTABLE = "S3_EXECUTABLE"
    S4_TESTED = "S4_TESTED"
    S5_FROZEN_DOMAIN = "S5_FROZEN_DOMAIN"
    S6_GOLD_EVALUATED = "S6_GOLD_EVALUATED"
    S7_BLIND_VERIFIED = "S7_BLIND_VERIFIED"
    S8_TRANSFER_VERIFIED = "S8_TRANSFER_VERIFIED"
    S9_REPRODUCED = "S9_REPRODUCED"

    @property
    def gate_index(self) -> int:
        """موضعُ البوّابة في التسلسل؛ موضعٌ لا وزن."""

        return GATE_SEQUENCE.index(self)

    @property
    def is_an_attestable_gate(self) -> bool:
        """هل تُشهَد هذه الدرجةُ بشاهد؟ الغيابُ لا يُشهَد، بل يُقاس بانتفائه."""

        return self is not MaturityStage.S0_ABSENT

    @property
    def ordering_law(self) -> str:
        """سقفُ قراءة الترتيب، محمولًا مع الدرجة لا مفصولًا عنها."""

        return STANDINGS_ARE_GATES_NOT_EPISTEMIC_MAGNITUDES


GATE_SEQUENCE: Final[tuple[MaturityStage, ...]] = (
    MaturityStage.S0_ABSENT,
    MaturityStage.S1_DECLARED,
    MaturityStage.S2_MODELED,
    MaturityStage.S3_EXECUTABLE,
    MaturityStage.S4_TESTED,
    MaturityStage.S5_FROZEN_DOMAIN,
    MaturityStage.S6_GOLD_EVALUATED,
    MaturityStage.S7_BLIND_VERIFIED,
    MaturityStage.S8_TRANSFER_VERIFIED,
    MaturityStage.S9_REPRODUCED,
)
"""التسلسلُ المُجمَّد؛ لا درجةَ خارجه ولا إعادةَ ترتيبٍ في موضعٍ آخر."""

_BLOCKING_REASONS: Final[dict[MaturityStage, str]] = {
    MaturityStage.S1_DECLARED: "DECLARATION_ABSENT",
    MaturityStage.S2_MODELED: "MODEL_ABSENT",
    MaturityStage.S3_EXECUTABLE: "IMPLEMENTATION_ABSENT",
    MaturityStage.S4_TESTED: "TESTS_ABSENT",
    MaturityStage.S5_FROZEN_DOMAIN: "FROZEN_DOMAIN_ABSENT",
    MaturityStage.S6_GOLD_EVALUATED: "GOLD_ABSENT",
    MaturityStage.S7_BLIND_VERIFIED: "BLIND_EVALUATION_ABSENT",
    MaturityStage.S8_TRANSFER_VERIFIED: "EXTERNAL_TRANSFER_ABSENT",
    MaturityStage.S9_REPRODUCED: "REPRODUCTION_ABSENT",
}


def blocking_reason_for_gate(gate: MaturityStage) -> str:
    """اسمُ المانعِ عند بوّابةٍ مفتوحة؛ اسمٌ مُسنونٌ لا نصٌّ حُرّ."""

    if not isinstance(gate, MaturityStage):
        raise TypeError("a blocking reason is named for a maturity gate")
    if gate is MaturityStage.S0_ABSENT:
        return "NOTHING_IS_BLOCKED_BELOW_ABSENCE"
    return _BLOCKING_REASONS[gate]


def stage_at_or_above(stage: MaturityStage, floor: MaturityStage) -> bool:
    """هل بلغت الدرجةُ الأرضيّةَ المطلوبة أو جاوزتها في التسلسل المُجمَّد؟"""

    if not isinstance(stage, MaturityStage) or not isinstance(floor, MaturityStage):
        raise TypeError("gate comparison requires two maturity stages")
    return stage.gate_index >= floor.gate_index
