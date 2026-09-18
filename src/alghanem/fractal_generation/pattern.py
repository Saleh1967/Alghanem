"""عقدُ النمط: ما يَعِد النمطُ بحفظه، وما يسمح به من فرق، ومدى سلطته.

    PatternContract  =  declaration  ≠  proof

**والإعلانُ ليس برهانًا** (`PatternDeclarationIsNotPatternProof`): العقدُ
يُصرِّح بثوابتَ وشروطٍ وموانع، ولا يُثبِت أنّ تطبيقًا بعينه حفِظها؛ ولذلك لا
اسمَ `Proven` ولا `Licensed` في هذه الرتبة، ولا `licensed_variation_class`:
الفرقُ المسموحُ به عقدٌ مُصرَّحٌ (`declared_variation_contract`) لا ترخيص.

**والمقاييسُ التي يجري عليها النمطُ مراجعُ مُحَلّة** لا أسماءٌ مُدّعاة.

تسجيلٌ لا سلطة: لا ولادةَ، ولا حكمَ ولادةٍ، ولا تجميدَ `E0`.
"""

from __future__ import annotations

from dataclasses import dataclass

from ..canonical_content import canonical_bytes, canonical_digest, is_canonical_digest
from .scale import FractalScaleRef, ScaleSpace

__all__ = [
    "PatternContract",
    "PatternContractError",
    "PatternRef",
]


class PatternContractError(ValueError):
    """رفضٌ عند تكوين عقدِ نمطٍ أو مرجعِه."""


def _named_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PatternContractError(f"{label} نصٌّ غير فارغ")
    return value


def _named_texts(values: object, label: str) -> tuple[str, ...]:
    if not isinstance(values, tuple):
        raise PatternContractError(f"{label} مجموعةٌ مُصرَّحٌ بها")
    for value in values:
        _named_text(value, f"عضوٌ في {label}")
    if len(set(values)) != len(values):
        raise PatternContractError(f"عضوٌ مُكرَّرٌ في {label}")
    return values


@dataclass(frozen=True, slots=True)
class PatternContract:
    """عقدُ نمطٍ مُصرَّح: مداه، ومقاييسُه، وثوابتُه، وفرقُه، وموانعُه، وسلطتُه."""

    pattern_id: str
    domain_id: str
    applicable_scales: tuple[FractalScaleRef, ...]
    admissible_seed_contract: str
    operation_contract: str
    preserved_invariants: tuple[str, ...]
    declared_variation_contract: str
    reapplication_condition: str
    closure_requirements: tuple[str, ...]
    branch_conditions: tuple[str, ...]
    blockers: tuple[str, ...]
    residual_policy: str
    authority_scope: str

    def __post_init__(self) -> None:
        _named_text(self.pattern_id, "مُعرِّفُ النمط")
        _named_text(self.domain_id, "مجالُ النمط")
        if not isinstance(self.applicable_scales, tuple) or not self.applicable_scales:
            raise PatternContractError("النمطُ يجري على مقياسٍ واحدٍ فأكثر بمراجعها")
        for ref in self.applicable_scales:
            if not isinstance(ref, FractalScaleRef):
                raise PatternContractError("عضوٌ في مقاييس النمط خارج نوع المرجع")
        _named_text(self.admissible_seed_contract, "عقدُ البذرة المقبولة")
        _named_text(self.operation_contract, "عقدُ العمليّة")
        _named_texts(self.preserved_invariants, "ثوابتُ النمط المحفوظة")
        _named_text(self.declared_variation_contract, "عقدُ الفرق المُصرَّح")
        _named_text(self.reapplication_condition, "شرطُ إعادة التطبيق")
        _named_texts(self.closure_requirements, "متطلّباتُ الإغلاق")
        _named_texts(self.branch_conditions, "شروطُ التفرّع")
        _named_texts(self.blockers, "موانعُ النمط")
        _named_text(self.residual_policy, "سياسةُ البقايا")
        _named_text(self.authority_scope, "مدى سلطة النمط")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى العقد للبصمة."""

        return {
            "pattern_id": self.pattern_id,
            "domain_id": self.domain_id,
            "applicable_scales": [
                {
                    "scale_id": ref.scale_id,
                    "contract_content_id": ref.contract_content_id,
                }
                for ref in self.applicable_scales
            ],
            "admissible_seed_contract": self.admissible_seed_contract,
            "operation_contract": self.operation_contract,
            "preserved_invariants": list(self.preserved_invariants),
            "declared_variation_contract": self.declared_variation_contract,
            "reapplication_condition": self.reapplication_condition,
            "closure_requirements": list(self.closure_requirements),
            "branch_conditions": list(self.branch_conditions),
            "blockers": list(self.blockers),
            "residual_policy": self.residual_policy,
            "authority_scope": self.authority_scope,
        }

    @property
    def content_id(self) -> str:
        """بصمةُ عقد النمط؛ مُشتَقّةٌ لا مكتوبة."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))

    def as_ref(self) -> PatternRef:
        """مرجعٌ إلى هذا العقد بعينه."""

        return PatternRef(
            pattern_id=self.pattern_id, contract_content_id=self.content_id
        )

    def applies_at(self, scale_ref: FractalScaleRef) -> bool:
        """أيجري هذا النمطُ عند هذا المقياس بمرجعه بعينه؟"""

        return scale_ref in self.applicable_scales

    def scales_resolved_in(self, space: ScaleSpace) -> bool:
        """أكلُّ مقاييسِ النمط مُحَلّةٌ في هذا الفضاء؟"""

        return all(space.admits(ref) for ref in self.applicable_scales)


@dataclass(frozen=True, slots=True)
class PatternRef:
    """مرجعُ نمط: مُعرِّفُه وبصمةُ عقده."""

    pattern_id: str
    contract_content_id: str

    def __post_init__(self) -> None:
        _named_text(self.pattern_id, "مُعرِّفُ النمط المُشار إليه")
        if not is_canonical_digest(self.contract_content_id):
            raise PatternContractError("مرجعُ النمط يحمل بصمةَ عقدٍ قانونيّة")
