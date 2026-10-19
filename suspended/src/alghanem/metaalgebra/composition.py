"""الميتا-جبر: تركيبُ السلسلة، وشرطُ التجاور، وفصلُ الصحّة عن التغطية.

هذه الوحدةُ تحمل التزاماتِ مبرهنتَي `G0.T.1` كما جُمِّدتا نصًّا في الدستور:

* **مبرهنةُ التركيب المرخَّص**: إن تحقّق لكلّ `i` الشرطُ
  `Typed_i ∧ Licensed_i ∧ InvariantPreserving_i ∧ Traceable_i ∧ ResidualSafe_i`،
  وتحقّق `Cl_i(y) ∧ Handoff_i(y) ⇒ y ∈ Dom(T_{i+1})`، كان التركيبُ
  `T^{(n)} = T_{n-1} ∘ ⋯ ∘ T_0` معرَّفًا على كلّ `x` يجتاز البوّابات كلَّها،
  ومسارُه مرخَّصٌ في كلّ خطوةٍ بلا قفزة.
* **مبرهنةُ التدقيق الرجعيّ**، مستقلّةً: لا يُطلَب `T⁻¹`، بل شهادةٌ تكفي لتفسير
  **سببِ ترخيص** كلّ خطوة.

**وصحّةُ المبرهنة ليست تغطيةَ تمثيلها:**

    TheoremValidity  ≠  InstantiationCoverage

فالمبرهنةُ مُبرهَنةٌ رمزيًّا لكلّ `n`، وعددُ الانتقالات المبنيّة اليوم واقعةٌ
ثانيةٌ تُعَدّ وحدَها؛ وقلّةُ التغطية ليست عيبًا في المبرهنة، وكثرتُها ليست
بديلًا عن برهانها. والعددُ هنا **خاصّيّةٌ تُشتَقّ** من الأعضاء لا حقلٌ يُكتَب.

**وما لا تفعله هذه الوحدةُ بحال:** لا تُشغّل تحويلًا، ولا تقرأ حالةً، ولا
تُصدِر منزلةً، ولا تدّعي أنّ سلسلةً صحيحةَ التجاور سلسلةٌ مُبرهَنة. ما تفعله:
ترفض عند الإنشاء سلسلةً لا تتحقّق فيها شروطُ التجاور التي تفترضها المبرهنة
(`ADJACENCY_IS_A_HYPOTHESIS_NOT_A_CONCLUSION`).

تسجيلٌ لا سلطة: لا ولادةَ ولا تجميدَ `E0` ولا حكم، ولا استيرادَ من `kernel/`.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest
from .layer import LayerSignature
from .transition import TransitionSignature

__all__ = [
    "ADJACENCY_IS_A_HYPOTHESIS_NOT_A_CONCLUSION",
    "A_CHAIN_IS_NOT_A_PROOF",
    "BACKWARD_AUDITABILITY_OBLIGATION",
    "COMPOSITION_LAW",
    "THEOREM_VALIDITY_IS_NOT_INSTANTIATION_COVERAGE",
    "CompositionChain",
    "CompositionChainError",
    "StepObligation",
]


class CompositionChainError(ValueError):
    """رفضٌ عند الإنشاء: تجاورٌ مكسور، أو ثابتٌ محفوظٌ لا تعرفه إحدى الطبقتين."""


COMPOSITION_LAW: Final[str] = (
    "إن تحقّقت التزاماتُ كلّ خطوةٍ وشرطا الإغلاق والتسليم، كان "
    "`T^{(n)} = T_{n-1} ∘ ⋯ ∘ T_0` معرَّفًا على كلّ `x` يجتاز البوّابات كلَّها، "
    "ومسارُه مرخَّصًا في كلّ خطوةٍ بلا قفزة"
)

BACKWARD_AUDITABILITY_OBLIGATION: Final[str] = (
    "لا يُطلَب معكوسُ التحويل، بل شهادةٌ تكفي لتفسير سببِ ترخيص الخطوة: "
    "صنفُ المصدر، والعملية، والترخيص، والثوابتُ المحفوظة، والبقايا"
)

THEOREM_VALIDITY_IS_NOT_INSTANTIATION_COVERAGE: Final[str] = (
    "صحّةُ المبرهنة رمزيًّا لكلّ `n` واقعةٌ، وعددُ الانتقالات المبنيّة اليوم "
    "واقعةٌ ثانيةٌ؛ ولا تنوب إحداهما عن الأخرى ولا تُقرأ عيبًا فيها"
)

ADJACENCY_IS_A_HYPOTHESIS_NOT_A_CONCLUSION: Final[str] = (
    "شروطُ التجاور المفحوصةُ هنا فرضُ المبرهنة لا نتيجتُها؛ وسلسلةٌ صحيحةُ "
    "التجاور ليست بذلك سلسلةً مُبرهَنةً ولا مُشغَّلة"
)

A_CHAIN_IS_NOT_A_PROOF: Final[str] = (
    "بناءُ السلسلة تسجيلٌ لبنيةٍ، لا تشغيلٌ لتحويلٍ ولا إصدارٌ لمنزلة"
)


class StepObligation(Enum):
    """التزاماتُ الخطوة الواحدة كما وردت في فرض المبرهنة، مفردةً مغلقة."""

    TYPED = "Typed"
    LICENSED = "Licensed"
    INVARIANT_PRESERVING = "InvariantPreserving"
    TRACEABLE = "Traceable"
    RESIDUAL_SAFE = "ResidualSafe"
    HANDOFF_ENABLED = "HandoffEnabled"


@dataclass(frozen=True, slots=True)
class CompositionChain:
    """سلسلةُ طبقاتٍ وانتقالاتٍ بينها، مفحوصةَ التجاور عند الإنشاء.

    `layers` عددُها `n + 1`، و`transitions` عددُها `n`؛ والانتقالُ `i` مصدرُه
    الطبقةُ `i` وهدفُه الطبقةُ `i + 1`، ولا يُستنتَج ترتيبٌ من الأسماء.
    """

    chain_id: str
    layers: tuple[LayerSignature, ...]
    transitions: tuple[TransitionSignature, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.chain_id, str) or not self.chain_id.strip():
            raise CompositionChainError("اسمُ السلسلة نصٌّ غير فارغ")
        if not isinstance(self.layers, tuple) or not self.layers:
            raise CompositionChainError("السلسلةُ طبقةٌ فأكثر")
        if not isinstance(self.transitions, tuple):
            raise CompositionChainError("الانتقالاتُ مجموعةٌ مُصرَّحٌ بها")
        for layer in self.layers:
            if not isinstance(layer, LayerSignature):
                raise CompositionChainError("عضوٌ في الطبقات خارج نوعه")
        for transition in self.transitions:
            if not isinstance(transition, TransitionSignature):
                raise CompositionChainError("عضوٌ في الانتقالات خارج نوعه")
        layer_ids = tuple(layer.layer_id for layer in self.layers)
        if len(set(layer_ids)) != len(layer_ids):
            raise CompositionChainError("طبقةٌ مكرّرةٌ في السلسلة تُرفَض لا تُطوى")
        if len(self.transitions) != len(self.layers) - 1:
            raise CompositionChainError(
                "عددُ الانتقالات أقلُّ من عدد الطبقات بواحدٍ بالضبط؛ "
                "والنقصُ ثغرةٌ في المسار لا تفصيلٌ يُكمَّل لاحقًا"
            )
        for index, transition in enumerate(self.transitions):
            source = self.layers[index]
            target = self.layers[index + 1]
            if transition.source_layer_id != source.layer_id:
                raise CompositionChainError(
                    f"مصدرُ الانتقال `{transition.transition_id}` ليس الطبقةَ السابقة"
                )
            if transition.target_layer_id != target.layer_id:
                raise CompositionChainError(
                    f"هدفُ الانتقال `{transition.transition_id}` ليس الطبقةَ التالية"
                )
            preserved = set(transition.preservation.preserved_components)
            missing_in_source = preserved - set(source.invariant_component_names)
            if missing_in_source:
                raise CompositionChainError(
                    "مكوّنٌ محفوظٌ لا تُعلنه الطبقةُ المصدر: "
                    + "، ".join(sorted(missing_in_source))
                )
            missing_in_target = preserved - set(target.invariant_component_names)
            if missing_in_target:
                raise CompositionChainError(
                    "مكوّنٌ محفوظٌ لا تُعلنه الطبقةُ الهدف، فلا معنى لمطابقته: "
                    + "، ".join(sorted(missing_in_target))
                )

    @property
    def instantiation_coverage(self) -> int:
        """عددُ الانتقالات المبنيّة؛ خاصّيّةٌ تُشتَقّ لا حقلٌ يُكتَب.

        وهذا العددُ تغطيةٌ لا صحّة: المبرهنةُ رمزيّةٌ لكلّ `n`
        (`THEOREM_VALIDITY_IS_NOT_INSTANTIATION_COVERAGE`).
        """

        return len(self.transitions)

    @property
    def layer_count(self) -> int:
        """عددُ الطبقات المبنيّة؛ خاصّيّةٌ تُشتَقّ كذلك."""

        return len(self.layers)

    def step_obligations(self) -> tuple[StepObligation, ...]:
        """التزاماتُ كلّ خطوةٍ كما وردت في فرض المبرهنة، لا كما تُقاس هنا."""

        return tuple(StepObligation)

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى السلسلة للبصمة."""

        return {
            "chain_id": self.chain_id,
            "layers": [layer.as_canonical_content() for layer in self.layers],
            "transitions": [
                transition.as_canonical_content() for transition in self.transitions
            ],
        }

    @property
    def content_id(self) -> str:
        """بصمةُ محتوى السلسلة."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))


_COUNT_FIELD_MARKERS: Final[tuple[str, ...]] = ("count", "coverage", "total")

for _field in fields(CompositionChain):  # pragma: no cover - import guard
    if any(marker in _field.name for marker in _COUNT_FIELD_MARKERS):
        raise RuntimeError("التعدادُ خاصّيّةٌ تُحسَب لا حقلٌ يُكتَب")
