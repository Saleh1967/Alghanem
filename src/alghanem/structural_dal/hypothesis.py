"""`G0.SDAL-0.HYPOTHESIS`: حالةُ الصفر البنيويّة، ومجموعةُ فرضيّات التقسيم.

عند الصفر: أصغرُ كلٍّ مكتملٍ بخانةٍ واحدة، يُثبِت إعادةَ البناء والتغطيةَ التامّة
وحفظَ الهويّة والأثر، ولا يُثبِت شيئًا لغويًّا:

    StructuralBaseCase  !=  LinguisticRootProof

وعند الواحد: خانتان تُنتِجان `ShapePartitionHypothesisSet` بلا فائزٍ مفروض:

    ShapePartitionHypothesis  !=  RootCandidate
    ShapePartitionHypothesis  !=  WeightCandidate

والدورُ `RESIDUAL` هنا إسقاطُ خاناتٍ داخل التقسيم، لا سجلُّ البقايا المُصنَّفة؛
فالأوّلُ موضعٌ في البنية، والثاني حكمٌ على ما لم يُحسَم.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from itertools import product

from alghanem.fractal_generation import FractalResidual

from .laws import (
    NO_FORCED_WINNER_AMONG_SHAPE_PARTITIONS,
    NO_SILENT_DROPPED_SLOT,
    SHAPE_PARTITION_HYPOTHESIS_IS_NOT_A_ROOT_CANDIDATE,
    SHAPE_PARTITION_HYPOTHESIS_IS_NOT_A_WEIGHT_CANDIDATE,
    STRUCTURAL_BASE_CASE_IS_NOT_A_LINGUISTIC_ROOT_PROOF,
    STRUCTURAL_PART_IS_NOT_A_SUBSTRING,
    ZERO_ONE_BOUND,
    OutputContractComponent,
    StructuralDalError,
)
from .residual import (
    PromotionStanding,
    ResidualReading,
    promotion_standing_of,
    read_residuals,
    unassigned_role_basis_residual,
    uncovered_core_residual,
)
from .slots import StructuralSlot, StructuralWhole

__all__ = [
    "PartWholeRelation",
    "ShapePartitionHypothesis",
    "ShapePartitionHypothesisSet",
    "SlotRole",
    "StructuralDecomposition",
    "StructuralPart",
    "ZeroStructuralState",
    "decompose",
    "enumerate_shape_partitions",
    "zero_structural_state",
]


class SlotRole(Enum):
    """أدوارُ الخانات؛ مفردةٌ مغلقةٌ لا تُزاد إلّا بسلطةٍ تُفتَح."""

    CORE = "core"
    TRANSFORM = "transform"
    RESIDUAL = "residual"


class PartWholeRelation(Enum):
    """نسبةُ الجزء إلى الكلّ؛ مُشتَقّةٌ من مواضعه لا مُصرَّحةٌ معه."""

    EMPTY_SELECTION = "empty_selection"
    CONTIGUOUS_SEGMENT = "contiguous_segment"
    ORDERED_PROJECTION = "ordered_projection"


@dataclass(frozen=True, slots=True)
class ShapePartitionHypothesis:
    """فرضيّةُ تقسيمٍ: دورٌ لكلِّ خانةٍ بترتيبها؛ صورةٌ لا دعوى."""

    hypothesis_id: str
    roles: tuple[SlotRole, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.hypothesis_id, str) or not self.hypothesis_id.strip():
            raise StructuralDalError("مُعرِّفُ الفرضيّة نصٌّ غيرُ فارغ")
        if not isinstance(self.roles, tuple) or not self.roles:
            raise StructuralDalError("الفرضيّةُ دورٌ واحدٌ فأكثر")
        for role in self.roles:
            if not isinstance(role, SlotRole):
                raise StructuralDalError("دورٌ خارج المفردة المغلقة")

    @property
    def slot_count(self) -> int:
        """عددُ الخانات التي تُسنِد إليها الفرضيّةُ أدوارًا."""

        return len(self.roles)

    def indices_of(self, role: SlotRole) -> tuple[int, ...]:
        """مواضعُ الخانات التي أخذت دورًا بعينه."""

        return tuple(
            position for position, value in enumerate(self.roles) if value is role
        )

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الفرضيّة للعرض والبصمة."""

        return {
            "hypothesis_id": self.hypothesis_id,
            "roles": [role.value for role in self.roles],
        }


@dataclass(frozen=True, slots=True)
class ShapePartitionHypothesisSet:
    """مجموعةُ الفرضيّات كاملةً بلا ترجيح؛ ولا فائزَ فيها مفروض."""

    whole_id: str
    hypotheses: tuple[ShapePartitionHypothesis, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.whole_id, str) or not self.whole_id.strip():
            raise StructuralDalError("مُعرِّفُ الكلّ نصٌّ غيرُ فارغ")
        if not isinstance(self.hypotheses, tuple) or not self.hypotheses:
            raise StructuralDalError("مجموعةُ الفرضيّات فرضيّةٌ واحدةٌ فأكثر")
        identifiers = [item.hypothesis_id for item in self.hypotheses]
        if len(set(identifiers)) != len(identifiers):
            raise StructuralDalError("فرضيّةٌ مُكرَّرةُ المُعرِّف")
        shapes = [item.roles for item in self.hypotheses]
        if len(set(shapes)) != len(shapes):
            raise StructuralDalError("فرضيّتان بتوزيع أدوارٍ واحد")

    @property
    def count(self) -> int:
        """عددُ الفرضيّات؛ مُشتَقٌّ وقتَ القياس لا مُجمَّدٌ قبله."""

        return len(self.hypotheses)

    @property
    def forced_winner(self) -> None:
        """لا فائزَ مفروض؛ والقيمةُ عدمٌ دائمًا بحكم قانونها."""

        return None

    @property
    def refusal(self) -> str:
        """قانونُ رفعِ الترجيح عن المجموعة."""

        return NO_FORCED_WINNER_AMONG_SHAPE_PARTITIONS

    @property
    def what_it_is_not(self) -> tuple[str, ...]:
        """ما لا تكونه الفرضيّةُ مهما كثرت."""

        return (
            SHAPE_PARTITION_HYPOTHESIS_IS_NOT_A_ROOT_CANDIDATE,
            SHAPE_PARTITION_HYPOTHESIS_IS_NOT_A_WEIGHT_CANDIDATE,
        )


@dataclass(frozen=True, slots=True)
class StructuralPart:
    """جزءٌ بنيويّ: دورٌ، وإسقاطٌ مرتّبٌ على خانات، ومِرساةُ أبٍ محفوظة."""

    part_id: str
    parent_anchor_id: str
    role: SlotRole
    slot_map: tuple[StructuralSlot, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.part_id, str) or not self.part_id.strip():
            raise StructuralDalError("مُعرِّفُ الجزء نصٌّ غيرُ فارغ")
        if not isinstance(self.parent_anchor_id, str) or not (
            self.parent_anchor_id.strip()
        ):
            raise StructuralDalError("الجزءُ يحمل مِرساةَ أبيه نصًّا غيرَ فارغ")
        if not isinstance(self.role, SlotRole):
            raise StructuralDalError("دورُ الجزء عضوٌ في مفردته المغلقة")
        if not isinstance(self.slot_map, tuple):
            raise StructuralDalError("إسقاطُ الجزء مجموعةُ خاناتٍ مرتّبة")
        previous = -1
        for slot in self.slot_map:
            if not isinstance(slot, StructuralSlot):
                raise StructuralDalError("عضوٌ في الإسقاط خارج نوع الخانة")
            if slot.index <= previous:
                raise StructuralDalError("إسقاطُ الجزء مرتّبٌ صاعدٌ بلا تكرار")
            previous = slot.index

    @property
    def indices(self) -> tuple[int, ...]:
        """مواضعُ خانات الجزء في الكلّ."""

        return tuple(slot.index for slot in self.slot_map)

    @property
    def tokens(self) -> tuple[str, ...]:
        """رموزُ خانات الجزء بترتيبها."""

        return tuple(slot.token for slot in self.slot_map)

    @property
    def is_empty(self) -> bool:
        """هل الجزءُ خالٍ من الخانات؟"""

        return not self.slot_map

    @property
    def relation_to_whole(self) -> PartWholeRelation:
        """نسبةُ الجزء إلى الكلّ؛ والمتباعدةُ ليست مقطعًا متّصلًا من نصّ."""

        indices = self.indices
        if not indices:
            return PartWholeRelation.EMPTY_SELECTION
        span = indices[-1] - indices[0] + 1
        if span == len(indices):
            return PartWholeRelation.CONTIGUOUS_SEGMENT
        return PartWholeRelation.ORDERED_PROJECTION

    @property
    def refusal(self) -> str:
        """قانونُ نفي كون الجزء مقطعًا نصّيًّا."""

        return STRUCTURAL_PART_IS_NOT_A_SUBSTRING

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الجزء للعرض والبصمة."""

        return {
            "part_id": self.part_id,
            "parent_anchor_id": self.parent_anchor_id,
            "role": self.role.value,
            "slot_map": [[slot.index, slot.token] for slot in self.slot_map],
            "relation_to_whole": self.relation_to_whole.value,
        }


@dataclass(frozen=True, slots=True)
class StructuralDecomposition:
    """تفكيكُ كلٍّ على فرضيّةٍ واحدة: ثلاثةُ أجزاءٍ تُغطّي كلَّ خانةٍ مرّةً واحدة."""

    decomposition_id: str
    whole: StructuralWhole
    hypothesis: ShapePartitionHypothesis
    parts: tuple[StructuralPart, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.decomposition_id, str) or not (
            self.decomposition_id.strip()
        ):
            raise StructuralDalError("مُعرِّفُ التفكيك نصٌّ غيرُ فارغ")
        if not isinstance(self.whole, StructuralWhole):
            raise StructuralDalError("التفكيكُ يقع على كلٍّ من نوعه")
        if not isinstance(self.hypothesis, ShapePartitionHypothesis):
            raise StructuralDalError("التفكيكُ يقوم على فرضيّةٍ من نوعها")
        if self.hypothesis.slot_count != self.whole.slot_count:
            raise StructuralDalError("الفرضيّةُ تُسنِد دورًا لكلِّ خانةٍ بلا زيادةٍ ولا نقص")
        roles = tuple(part.role for part in self.parts)
        if roles != tuple(SlotRole):
            raise StructuralDalError("التفكيكُ جزءٌ واحدٌ لكلِّ دورٍ بترتيب مفردته")
        covered: list[int] = []
        for part in self.parts:
            if part.parent_anchor_id != self.whole.anchor_id:
                raise StructuralDalError("جزءٌ لا يحمل مِرساةَ كلِّه")
            covered.extend(part.indices)
        if sorted(covered) != list(range(self.whole.slot_count)):
            raise StructuralDalError(
                "تغطيةٌ ناقصةٌ أو مُكرَّرةٌ للخانات؛ و" + NO_SILENT_DROPPED_SLOT
            )
        for part in self.parts:
            for slot in part.slot_map:
                if self.hypothesis.roles[slot.index] is not part.role:
                    raise StructuralDalError("خانةٌ في جزءٍ يخالف دورَها في الفرضيّة")

    def part_of(self, role: SlotRole) -> StructuralPart:
        """جزءُ دورٍ بعينه."""

        for part in self.parts:
            if part.role is role:
                return part
        raise StructuralDalError(f"دورٌ غيرُ مُفكَّك: {role.value}")

    @property
    def reconstruction(self) -> tuple[str, ...]:
        """إعادةُ بناء رموز الكلّ من أجزائه بمواضعها."""

        placed: dict[int, str] = {}
        for part in self.parts:
            for slot in part.slot_map:
                placed[slot.index] = slot.token
        return tuple(placed[index] for index in sorted(placed))

    @property
    def reconstructs_whole(self) -> bool:
        """هل تُطابق إعادةُ البناء الكلَّ خانةً خانة؟"""

        return self.reconstruction == self.whole.tokens

    @property
    def covers_every_slot_once(self) -> bool:
        """هل غُطِّيت كلُّ خانةٍ مرّةً واحدةً بالضبط؟"""

        covered = sorted(index for part in self.parts for index in part.indices)
        return covered == list(range(self.whole.slot_count))

    @property
    def preserves_parent_anchor(self) -> bool:
        """هل حمل كلُّ جزءٍ مِرساةَ كلِّه؟"""

        return all(
            part.parent_anchor_id == self.whole.anchor_id for part in self.parts
        )

    @property
    def raw_residuals(self) -> tuple[FractalResidual, ...]:
        """البقايا بأعيانها: أساسُ الأدوار غيرُ مُبرهن، وغيابُ الأساس حاجب."""

        residuals = [unassigned_role_basis_residual(self.decomposition_id)]
        if self.part_of(SlotRole.CORE).is_empty:
            residuals.append(uncovered_core_residual(self.decomposition_id))
        return tuple(residuals)

    @property
    def residuals(self) -> tuple[ResidualReading, ...]:
        """قراءةُ البقايا مُصنَّفةً حاجبةً وغيرَ حاجبة."""

        return read_residuals(self.raw_residuals)

    @property
    def promotion_standing(self) -> PromotionStanding:
        """موقفُ الترقية؛ مُشتَقٌّ من البقايا لا مُصرَّح."""

        return promotion_standing_of(self.residuals)

    @property
    def satisfied_contract_components(self) -> tuple[OutputContractComponent, ...]:
        """مُركّباتُ عقد المخرج التي وفّاها هذا التفكيك."""

        satisfied: list[OutputContractComponent] = []
        if self.reconstructs_whole:
            satisfied.append(OutputContractComponent.WHOLE_RECONSTRUCTION)
        if self.covers_every_slot_once:
            satisfied.append(OutputContractComponent.TYPED_SLOT_PARTITION)
        if self.preserves_parent_anchor:
            satisfied.append(OutputContractComponent.PART_WHOLE_IDENTITY)
        if self.residuals:
            satisfied.append(OutputContractComponent.EXPLICIT_RESIDUALS)
        if self.whole.trace is not None or self.whole.descent_depth == 0:
            satisfied.append(OutputContractComponent.TRACE_COMPLETENESS)
        return tuple(satisfied)

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى التفكيك للعرض والبصمة."""

        return {
            "decomposition_id": self.decomposition_id,
            "whole_id": self.whole.whole_id,
            "hypothesis": self.hypothesis.as_canonical_content(),
            "parts": [part.as_canonical_content() for part in self.parts],
            "reconstruction": list(self.reconstruction),
            "reconstructs_whole": self.reconstructs_whole,
            "residuals": [reading.as_canonical_content() for reading in self.residuals],
            "promotion_standing": self.promotion_standing.value,
        }


@dataclass(frozen=True, slots=True)
class ZeroStructuralState:
    """`ZeroStructuralState`: أصغرُ كلٍّ مكتملٍ بخانةٍ واحدةٍ كلُّها أساس."""

    whole: StructuralWhole
    decomposition: StructuralDecomposition

    def __post_init__(self) -> None:
        if self.whole.slot_count != 1:
            raise StructuralDalError("حالةُ الصفر خانةٌ واحدةٌ لا أكثر")
        if self.decomposition.whole is not self.whole:
            raise StructuralDalError("تفكيكُ حالة الصفر يقع على كلِّها بعينه")
        if self.decomposition.hypothesis.roles != (SlotRole.CORE,):
            raise StructuralDalError("حالةُ الصفر خانتُها أساسٌ لا غير")
        if not self.decomposition.part_of(SlotRole.TRANSFORM).is_empty:
            raise StructuralDalError("تحويلُ حالة الصفر خالٍ")
        if not self.decomposition.part_of(SlotRole.RESIDUAL).is_empty:
            raise StructuralDalError("إسقاطُ بقيّة حالة الصفر خالٍ")

    @property
    def reconstructs_exactly(self) -> bool:
        """`Reconstruct(W_0) = W_0` خانةً خانة."""

        return self.decomposition.reconstructs_whole

    @property
    def covers_every_slot_once(self) -> bool:
        """تغطيةٌ تامّةٌ للخانة الواحدة."""

        return self.decomposition.covers_every_slot_once

    @property
    def preserves_identity(self) -> bool:
        """`anchor(W_0) = anchor(Core(W_0))`."""

        return (
            self.decomposition.part_of(SlotRole.CORE).parent_anchor_id
            == self.whole.anchor_id
        )

    @property
    def preserves_trace(self) -> bool:
        """أثرُ حالة الصفر مُصرَّحٌ: لا خطوةَ قبلها إن كانت أصلًا."""

        return self.whole.trace_steps == 0 or self.whole.descent_depth > 0

    @property
    def establishes(self) -> tuple[str, ...]:
        """ما تُثبِته حالةُ الصفر بأعيانه."""

        established: list[str] = []
        if self.reconstructs_exactly:
            established.append("exact_reconstruction")
        if self.covers_every_slot_once:
            established.append("complete_slot_coverage")
        if self.preserves_identity:
            established.append("identity_preservation")
        if self.preserves_trace:
            established.append("trace_preservation")
        return tuple(established)

    @property
    def does_not_establish(self) -> str:
        """ما لا تُثبِته مهما صحّت."""

        return STRUCTURAL_BASE_CASE_IS_NOT_A_LINGUISTIC_ROOT_PROOF


def enumerate_shape_partitions(whole: StructuralWhole) -> ShapePartitionHypothesisSet:
    """عدِّد كلَّ توزيعات الأدوار على خانات الكلّ بلا ترجيحٍ ولا حذف."""

    if not isinstance(whole, StructuralWhole):
        raise StructuralDalError("التعدادُ يقع على كلٍّ من نوعه")
    if whole.slot_count > ZERO_ONE_BOUND:
        raise StructuralDalError(
            f"تعدادٌ فوق حدِّ هذا الطور {ZERO_ONE_BOUND}؛ وسلطتُه لم تُفتَح"
        )
    hypotheses = tuple(
        ShapePartitionHypothesis(
            hypothesis_id=(
                f"{whole.whole_id}.shape."
                + "-".join(role.value for role in combination)
            ),
            roles=combination,
        )
        for combination in product(tuple(SlotRole), repeat=whole.slot_count)
    )
    return ShapePartitionHypothesisSet(
        whole_id=whole.whole_id, hypotheses=hypotheses
    )


def decompose(
    whole: StructuralWhole, hypothesis: ShapePartitionHypothesis
) -> StructuralDecomposition:
    """فكِّك الكلَّ على فرضيّةٍ واحدة؛ ولا تُسقِط خانةً صامتة."""

    slots = whole.slots
    parts = tuple(
        StructuralPart(
            part_id=f"{hypothesis.hypothesis_id}.part.{role.value}",
            parent_anchor_id=whole.anchor_id,
            role=role,
            slot_map=tuple(slots[index] for index in hypothesis.indices_of(role)),
        )
        for role in SlotRole
    )
    return StructuralDecomposition(
        decomposition_id=f"{hypothesis.hypothesis_id}.decomposition",
        whole=whole,
        hypothesis=hypothesis,
        parts=parts,
    )


def zero_structural_state(whole: StructuralWhole) -> ZeroStructuralState:
    """حالةُ الصفر لكلٍّ بخانةٍ واحدة: أساسٌ كلُّه، وتحويلٌ وبقيّةٌ خاليان."""

    if whole.slot_count != 1:
        raise StructuralDalError("حالةُ الصفر لا تُبنى إلّا على خانةٍ واحدة")
    hypothesis = ShapePartitionHypothesis(
        hypothesis_id=f"{whole.whole_id}.shape.{SlotRole.CORE.value}",
        roles=(SlotRole.CORE,),
    )
    return ZeroStructuralState(
        whole=whole, decomposition=decompose(whole, hypothesis)
    )
