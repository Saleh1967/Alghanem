"""المربّعُ التبادليّ لكلّ انتقال، والتزامُ استقلال التمثيل.

    R_{i+1}^D ∘ T_i  =  T_i^D ∘ R_i^D

**والصيغةُ لكلّ انتقالٍ على حدة، لا صيغةٌ عامّةٌ واحدة:** تحقيقُ الحامل المصدر
غيرُ تحقيقِ الحامل الهدف، فكتابةُ `R ∘ T = T_D ∘ R` بـ`R` واحدةٍ تُخفي أنّ
الطرفين يقعان في تحقيقين مختلفين. ولذلك يُطلَب هنا معرّفان متمايزان.

**وكسرُ المربّع لا يُبطل الجبر:** يُبطل دعوى أنّ **هذا التحقيق** يحقّق **هذا
الانتقال** كما ينبغي (`A_BROKEN_SQUARE_INDICTS_THE_REALIZATION_NOT_THE_ALGEBRA`).

**وميدانان لا يُثبتان استقلالَ التمثيل:** يُثبتان `InstantiationCoverage ≥ 2`
فقط. أمّا الاستقلالُ فيحتاج تفريغَ المربّعات؛ ولذلك الاسمُ هنا **التزامٌ** لا
دعوى (`TWO_DOMAINS_PROVE_COVERAGE_NOT_INDEPENDENCE`)، وإصدارُ المنزلة متروكٌ
لمحورَي `G0.ST` بعد التفريغ.

تسجيلٌ لا سلطة: لا دالّةَ هنا تُشغّل `T` ولا `T^D` ولا تقيس تبادلَهما؛ التشغيلُ
يخصّ كلَّ ميدانٍ في موضعه.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest
from .realization import Realization
from .specification import AbstractSystemSpecification
from .transition import TransitionOutcome

__all__ = [
    "A_BROKEN_SQUARE_INDICTS_THE_REALIZATION_NOT_THE_ALGEBRA",
    "COMMUTATION_LAW",
    "TWO_DOMAINS_PROVE_COVERAGE_NOT_INDEPENDENCE",
    "CommutationObligation",
    "CommutationObligationError",
    "RepresentationIndependenceObligation",
]


class CommutationObligationError(ValueError):
    """رفضٌ عند الإنشاء: تحقيقُ حاملين مطابقٌ، أو كسرٌ يمرّ نجاحًا."""


COMMUTATION_LAW: Final[str] = (
    "R_{i+1}^D ∘ T_i = T_i^D ∘ R_i^D؛ لكلّ انتقالٍ على حدة، وبتحقيقَي حاملٍ "
    "متمايزَين لا بتحقيقٍ واحدٍ يُكتَب مرّتين"
)

A_BROKEN_SQUARE_INDICTS_THE_REALIZATION_NOT_THE_ALGEBRA: Final[str] = (
    "كسرُ المربّع لا يُبطل الميتا-جبر: يُبطل دعوى أنّ هذا التحقيقَ يحقّق هذا "
    "الانتقالَ كما ينبغي، ويبقى القانونُ على حاله"
)

TWO_DOMAINS_PROVE_COVERAGE_NOT_INDEPENDENCE: Final[str] = (
    "ميدانان يُثبتان `InstantiationCoverage ≥ 2` لا استقلالَ التمثيل؛ "
    "والاستقلالُ يلزمه تفريغُ المربّعات، وإصدارُ المنزلة بعدُ لمحورَي `G0.ST`"
)

_BREAK_OUTCOMES: Final[frozenset[TransitionOutcome]] = frozenset(
    {TransitionOutcome.BLOCK, TransitionOutcome.DEFER}
)


def _require_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CommutationObligationError(f"{label} نصٌّ غير فارغ")
    return value


@dataclass(frozen=True, slots=True)
class CommutationObligation:
    """التزامُ مربّعٍ تبادليٍّ واحدٍ، مُسجَّلًا لا مُفرَّغًا.

    `source_carrier_realization_id` و`target_carrier_realization_id` هما
    `R_i^D` و`R_{i+1}^D`، ويُشترَط تمايزُهما لأنّ الطبقتين متمايزتان في `Σ_A`.
    """

    obligation_id: str
    transition_id: str
    domain_id: str
    source_carrier_realization_id: str
    target_carrier_realization_id: str
    realized_transition_id: str
    witness_of_commutation: str
    witness_of_break: str
    break_outcome: TransitionOutcome

    def __post_init__(self) -> None:
        _require_text(self.obligation_id, "اسمُ الالتزام")
        _require_text(self.transition_id, "اسمُ الانتقال في النظريّة")
        _require_text(self.domain_id, "اسمُ الميدان")
        _require_text(self.source_carrier_realization_id, "تحقيقُ الحامل المصدر `R_i^D`")
        _require_text(
            self.target_carrier_realization_id, "تحقيقُ الحامل الهدف `R_{i+1}^D`"
        )
        _require_text(self.realized_transition_id, "الانتقالُ المُحقَّق `T_i^D`")
        _require_text(self.witness_of_commutation, "شاهدُ التبادل")
        _require_text(self.witness_of_break, "شاهدُ الكسر")
        if (
            self.source_carrier_realization_id.strip()
            == self.target_carrier_realization_id.strip()
        ):
            raise CommutationObligationError(COMMUTATION_LAW)
        if self.witness_of_commutation.strip() == self.witness_of_break.strip():
            raise CommutationObligationError(
                "شاهدُ التبادل وشاهدُ الكسر شاهدان متمايزان؛ وتطابقُهما يُلغي المُفنِّد"
            )
        if self.break_outcome not in _BREAK_OUTCOMES:
            raise CommutationObligationError(
                "كسرُ المربّع يُخرِج `BLOCK` أو `DEFER`، ولا يمرّ نجاحًا صامتًا؛ "
                f"و{A_BROKEN_SQUARE_INDICTS_THE_REALIZATION_NOT_THE_ALGEBRA}"
            )

    @property
    def law_statement(self) -> str:
        """نصُّ الالتزام لهذا الانتقال بعينه؛ خاصّيّةٌ تُشتَقّ لا حقلٌ يُكتَب."""

        return (
            f"{self.target_carrier_realization_id} ∘ {self.transition_id} = "
            f"{self.realized_transition_id} ∘ {self.source_carrier_realization_id}"
        )

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الالتزام للبصمة."""

        return {
            "obligation_id": self.obligation_id,
            "transition_id": self.transition_id,
            "domain_id": self.domain_id,
            "source_carrier_realization_id": self.source_carrier_realization_id,
            "target_carrier_realization_id": self.target_carrier_realization_id,
            "realized_transition_id": self.realized_transition_id,
            "witness_of_commutation": self.witness_of_commutation,
            "witness_of_break": self.witness_of_break,
            "break_outcome": self.break_outcome.value,
        }


@dataclass(frozen=True, slots=True)
class RepresentationIndependenceObligation:
    """التزامٌ لا دعوى: ما يلزم تفريغُه قبل الكلام عن استقلال التمثيل.

    ولا حقلَ هنا يُكتَب فيه الجواب: `instantiation_coverage` و
    `discharged_square_count` خاصّيّتان تُشتَقّان من الأعضاء، على منهج
    `CompositionChain.instantiation_coverage`.
    """

    obligation_id: str
    specification: AbstractSystemSpecification
    realizations: tuple[Realization, ...]
    commutation_obligations: tuple[CommutationObligation, ...]
    discharged_obligation_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _require_text(self.obligation_id, "اسمُ التزام الاستقلال")
        if not isinstance(self.specification, AbstractSystemSpecification):
            raise CommutationObligationError("الالتزامُ منسوبٌ إلى نظريّةٍ مُسمّاة")
        if not isinstance(self.realizations, tuple) or not self.realizations:
            raise CommutationObligationError("الالتزامُ تحقيقٌ فأكثر")
        for realization in self.realizations:
            if not isinstance(realization, Realization):
                raise CommutationObligationError("عضوٌ في التحقيقات خارج نوعه")
            if realization.specification.content_id != self.specification.content_id:
                raise CommutationObligationError(
                    "تحقيقٌ لنظريّةٍ أخرى لا يُعَدّ تمثيلًا موازيًا لهذه النظريّة"
                )
        domain_ids = tuple(item.domain.domain_id for item in self.realizations)
        if len(set(domain_ids)) != len(domain_ids):
            raise CommutationObligationError(
                "ميدانٌ مكرّرٌ في التحقيقات لا يزيد تغطيةً؛ والتكرارُ يُرفَض"
            )
        if not isinstance(self.commutation_obligations, tuple):
            raise CommutationObligationError("التزاماتُ المربّعات مجموعةٌ مُصرَّحٌ بها")
        declared_ids: list[str] = []
        for obligation in self.commutation_obligations:
            if not isinstance(obligation, CommutationObligation):
                raise CommutationObligationError("عضوٌ في التزامات المربّعات خارج نوعه")
            if obligation.transition_id not in set(self.specification.transition_ids):
                raise CommutationObligationError(
                    f"التزامُ مربّعٍ لانتقالٍ `{obligation.transition_id}` " "خارج النظريّة"
                )
            if obligation.domain_id not in set(domain_ids):
                raise CommutationObligationError(
                    f"التزامُ مربّعٍ لميدانٍ `{obligation.domain_id}` بلا تحقيقٍ مُسجَّل"
                )
            declared_ids.append(obligation.obligation_id)
        if len(set(declared_ids)) != len(declared_ids):
            raise CommutationObligationError("التزامُ مربّعٍ مكرّرُ الاسم يُرفَض")
        if not isinstance(self.discharged_obligation_ids, tuple):
            raise CommutationObligationError("المُفرَّغةُ مجموعةٌ مُصرَّحٌ بها")
        if len(set(self.discharged_obligation_ids)) != len(
            self.discharged_obligation_ids
        ):
            raise CommutationObligationError("تفريغٌ مكرّرٌ يُرفَض لا يُطوى")
        unknown = set(self.discharged_obligation_ids) - set(declared_ids)
        if unknown:
            raise CommutationObligationError(
                "تفريغُ التزامٍ غيرِ مُسجَّلٍ دعوى بلا محلّ: " + "، ".join(sorted(unknown))
            )

    @property
    def instantiation_coverage(self) -> int:
        """عددُ الميادين المُحقَّقة؛ تغطيةٌ لا استقلال."""

        return len(self.realizations)

    @property
    def discharged_square_count(self) -> int:
        """عددُ المربّعات المُفرَّغة؛ خاصّيّةٌ تُشتَقّ لا حقلٌ يُكتَب."""

        return len(self.discharged_obligation_ids)

    @property
    def outstanding_obligation_ids(self) -> tuple[str, ...]:
        """ما بقي من الالتزامات بلا تفريغ؛ مرتّبةً ترتيبًا ثابتًا."""

        discharged = set(self.discharged_obligation_ids)
        return tuple(
            sorted(
                obligation.obligation_id
                for obligation in self.commutation_obligations
                if obligation.obligation_id not in discharged
            )
        )

    @property
    def why_this_is_not_yet_independence(self) -> str:
        """تصريحٌ ثابتٌ بأنّ هذا التزامٌ لا منزلة؛ يُقرأ مع كلّ تغطيةٍ تُحسَب."""

        return TWO_DOMAINS_PROVE_COVERAGE_NOT_INDEPENDENCE

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الالتزام للبصمة."""

        return {
            "obligation_id": self.obligation_id,
            "specification_id": self.specification.spec_id,
            "specification_content_id": self.specification.content_id,
            "realization_content_ids": [item.content_id for item in self.realizations],
            "commutation_obligations": [
                item.as_canonical_content() for item in self.commutation_obligations
            ],
            "discharged_obligation_ids": list(self.discharged_obligation_ids),
        }

    @property
    def content_id(self) -> str:
        """بصمةُ الالتزام."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))


_CLAIM_FIELD_MARKERS: Final[tuple[str, ...]] = (
    "claim",
    "verdict",
    "standing",
    "proved",
    "independent",
    "count",
    "coverage",
)

_OBLIGATION_TYPES: Final[tuple[type, ...]] = (
    CommutationObligation,
    RepresentationIndependenceObligation,
)

for _declaring_type in _OBLIGATION_TYPES:  # pragma: no cover - import guard
    for _field in fields(_declaring_type):
        if any(marker in _field.name for marker in _CLAIM_FIELD_MARKERS):
            raise RuntimeError(TWO_DOMAINS_PROVE_COVERAGE_NOT_INDEPENDENCE)
