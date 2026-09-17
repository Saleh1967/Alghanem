"""تحقيقُ `Σ_A` في ميدانٍ مُسمًّى: قالبُ التحقيق، لا حكمٌ عليه.

    Σ_A  ⟶  Realization(Σ_A, D),   D ∈ { أيّ ميدانٍ يُسجِّل نفسَه }

**والأصلُ واحدٌ والتمثيلان فرعان:** لا Python أصلٌ للعربيّة، ولا العربيّةُ أصلٌ
لـPython؛ الاثنان يرجعان إلى `Σ_A`
(`SIGMA_IS_THE_ORIGIN_NOT_ITS_REALIZATIONS`). ولذلك **لا مفردةَ ميادينَ مغلقةً
هنا**: `domain_id` معرّفٌ حرٌّ، لأنّ مفردةً فيها `ARABIC` و`PYTHON` تكون
معماريّةً مُعلَنةً سلفًا، وهو ما يمنعه `G0.MA`.

**والتغطيةُ تامّةٌ بالضبط**: لا مكوّنَ ناقصًا — فتحقيقٌ صامتٌ يمرّ — ولا مكوّنَ
زائدًا — فبنيةُ الميدان تتسلّل إلى الجبر (`REALIZATION_COVERAGE_IS_EXACT`).

**وكلُّ تحقيقٍ يذكر مُفنِّدَه**: تحقيقٌ لا يقول ما الذي يُكذّبه إعادةُ تسميةٍ لا
تحقيق (`A_RENAMING_IS_NOT_A_REALIZATION`).

**والبقيّةُ قد تُدين المجالَ لا التطبيق**: مصائرُ البقايا أربعةٌ — `CLOSE`،
`REFINE`، `REVISE_DOMAIN`، `DEFER` — لأنّ ما يبقى قد يكشف أنّ المجالَ نفسَه
يحتاج إعادةَ تعريف؛ وفي Python كذلك: ليس كلُّ استثناءٍ خطأَ بيانات
(`A_RESIDUAL_MAY_INDICT_THE_DOMAIN`).

تسجيلٌ لا سلطة: لا منزلةَ تُصدَر هنا (`NO_REALIZATION_GRANTS_STANDING`)، ولا
تحويلَ يُشغَّل، ولا استيرادَ من `kernel/` ولا من `arabic/` ولا من حزمة التوليد.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest
from .clause import Clause, require_clause
from .layer import LAYER_COMPONENT_NAMES
from .specification import AbstractSystemSpecification
from .transition import TRANSITION_COMPONENT_NAMES, TransitionOutcome

__all__ = [
    "A_RENAMING_IS_NOT_A_REALIZATION",
    "A_RESIDUAL_MAY_INDICT_THE_DOMAIN",
    "NO_REALIZATION_GRANTS_STANDING",
    "REALIZATION_COVERAGE_IS_EXACT",
    "REALIZED_TRANSITION_COMPONENT_NAMES",
    "SIGMA_IS_THE_ORIGIN_NOT_ITS_REALIZATIONS",
    "ComponentRealization",
    "LayerRealization",
    "Realization",
    "RealizationCoverageError",
    "RealizationDomainRef",
    "RealizationError",
    "ResidualDisposition",
    "ResidualDispositionRealization",
    "TransitionRealization",
]


class RealizationError(ValueError):
    """رفضٌ عند الإنشاء: ميدانٌ بلا رفض، أو تحقيقٌ بلا مُفنِّد."""


class RealizationCoverageError(RealizationError):
    """رفضٌ عند الإنشاء: تغطيةٌ ناقصةٌ أو زائدةٌ لمواضع المكوّنات."""


SIGMA_IS_THE_ORIGIN_NOT_ITS_REALIZATIONS: Final[str] = (
    "`Σ_A` أصلٌ وتمثيلاها فرعان: لا Python أصلٌ للعربيّة، ولا العربيّةُ أصلٌ "
    "لـPython؛ وبصمةُ النظريّة لا تتغيّر بتغيّر تحقيقٍ من تحقيقاتها"
)

REALIZATION_COVERAGE_IS_EXACT: Final[str] = (
    "تغطيةُ التحقيق تامّةٌ بالضبط: مكوّنٌ ناقصٌ تحقيقٌ صامتٌ يمرّ، ومكوّنٌ زائدٌ "
    "بنيةُ ميدانٍ تتسلّل إلى الجبر"
)

A_RENAMING_IS_NOT_A_REALIZATION: Final[str] = (
    "تحقيقٌ لا يذكر ما الذي يُكذّبه إعادةُ تسميةٍ لا تحقيق؛ والمُفنِّدُ شرطُ "
    "إنشاءٍ لا حاشيةٌ تُستحسَن"
)

A_RESIDUAL_MAY_INDICT_THE_DOMAIN: Final[str] = (
    "ليست كلُّ بقيّةٍ فشلَ تطبيق: بعضُها دليلٌ أنّ المجالَ نفسَه يحتاج إعادةَ "
    "تعريف؛ ولذلك `REVISE_DOMAIN` مصيرٌ مُعلَنٌ لا حالةُ خطأ"
)

NO_REALIZATION_GRANTS_STANDING: Final[str] = (
    "التحقيقُ تسجيلٌ لا منزلة: لا يُصدِر حكمًا، ولا يرفع دعوى، وإصدارُ المنزلة "
    "لمحورَي `G0.ST` وحدَهما"
)

REALIZED_TRANSITION_COMPONENT_NAMES: Final[tuple[str, ...]] = (
    TRANSITION_COMPONENT_NAMES + ("handoff",)
)
"""مواضعُ الانتقال السبعة في التحقيق؛ الستّةُ وشرطُ التسليم معها."""

_REQUIRED_UNLICENSED_OUTCOMES: Final[frozenset[TransitionOutcome]] = frozenset(
    {TransitionOutcome.BLOCK, TransitionOutcome.DEFER}
)


class ResidualDisposition(Enum):
    """مصائرُ البقيّة الأربعة؛ مفردةٌ مغلقةٌ لا خامسَ لها.

    و`REVISE_DOMAIN` عضوٌ أصيلٌ لا حالةُ عطب: بقيّةٌ قد تكشف أنّ تعريفَ المجال
    ناقصٌ لا أنّ المُدخَل فاسد.
    """

    CLOSE = "CLOSE"
    REFINE = "REFINE"
    REVISE_DOMAIN = "REVISE_DOMAIN"
    DEFER = "DEFER"


def _require_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise RealizationError(f"{label} نصٌّ غير فارغ")
    return value


@dataclass(frozen=True, slots=True)
class RealizationDomainRef:
    """الميدانُ الذي يتحقّق فيه الجبر: اسمُه، ووصفُه، وما ليس منه.

    `domain_id` معرّفٌ حرٌّ لا عضوٌ في مفردةٍ مغلقة؛ ومفردةٌ مغلقةٌ بأسماء
    ميادينَ بعينها معماريّةٌ مُعلَنةٌ سلفًا يمنعها `G0.MA`.
    """

    domain_id: str
    description: str
    what_is_not_this_domain: str

    def __post_init__(self) -> None:
        _require_text(self.domain_id, "اسمُ الميدان")
        _require_text(self.description, "وصفُ الميدان")
        _require_text(self.what_is_not_this_domain, "ما ليس من الميدان")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الميدان للبصمة."""

        return {
            "domain_id": self.domain_id,
            "description": self.description,
            "what_is_not_this_domain": self.what_is_not_this_domain,
        }


@dataclass(frozen=True, slots=True)
class ComponentRealization:
    """تحقيقُ موضعٍ واحدٍ من مواضع الطبقة أو الانتقال في الميدان.

    و`realization_condition` بندٌ من النوعين: تصريحيٌّ يُقرأ ولا يُترجَم، أو
    قابلٌ للتنفيذ يُترجَم؛ والفرقُ نوعيٌّ لا سمةٌ تُقلَب.
    """

    component_name: str
    realized_as: str
    realization_condition: Clause
    what_would_falsify_this_realization: str

    def __post_init__(self) -> None:
        _require_text(self.component_name, "اسمُ الموضع المُحقَّق")
        _require_text(self.realized_as, "بماذا يتحقّق الموضع")
        require_clause(self.realization_condition, "شرطُ التحقيق")
        if (
            not isinstance(self.what_would_falsify_this_realization, str)
            or not self.what_would_falsify_this_realization.strip()
        ):
            raise RealizationError(A_RENAMING_IS_NOT_A_REALIZATION)
        if self.what_would_falsify_this_realization.strip() == self.realized_as.strip():
            raise RealizationError(A_RENAMING_IS_NOT_A_REALIZATION)

    @property
    def is_executable(self) -> bool:
        """أَشَرطُ التحقيق مُترجَمٌ؟ خاصّيّةٌ تُشتَقّ من نوع البند لا حقلٌ يُكتَب."""

        return self.realization_condition.is_executable

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى تحقيق الموضع للبصمة."""

        return {
            "component_name": self.component_name,
            "realized_as": self.realized_as,
            "realization_condition": (
                self.realization_condition.as_canonical_content()
            ),
            "what_would_falsify_this_realization": (
                self.what_would_falsify_this_realization
            ),
        }


@dataclass(frozen=True, slots=True)
class ResidualDispositionRealization:
    """مصيرُ بقيّةٍ متاحٌ في هذا الميدان، وشرطُ بلوغه."""

    disposition: ResidualDisposition
    holds_when: str

    def __post_init__(self) -> None:
        if not isinstance(self.disposition, ResidualDisposition):
            raise RealizationError("مصيرُ البقيّة عضوٌ في مفردته المغلقة")
        _require_text(self.holds_when, f"شرطُ `{self.disposition.value}`")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى المصير للبصمة."""

        return {
            "disposition": self.disposition.value,
            "holds_when": self.holds_when,
        }


def _require_exact_coverage(
    realized: tuple[ComponentRealization, ...],
    expected: tuple[str, ...],
    label: str,
) -> None:
    if not isinstance(realized, tuple) or not realized:
        raise RealizationCoverageError(f"{label} مجموعةٌ غير فارغة")
    for item in realized:
        if not isinstance(item, ComponentRealization):
            raise RealizationCoverageError(f"عضوٌ في {label} خارج نوعه")
    names = tuple(item.component_name for item in realized)
    if len(set(names)) != len(names):
        raise RealizationCoverageError(
            f"موضعٌ مكرّرٌ في {label} يُخفي تحقيقًا تحت آخر؛ و"
            + REALIZATION_COVERAGE_IS_EXACT
        )
    missing = set(expected) - set(names)
    if missing:
        raise RealizationCoverageError(
            f"{label} ناقصةُ المواضع: "
            + "، ".join(sorted(missing))
            + "؛ و"
            + REALIZATION_COVERAGE_IS_EXACT
        )
    extra = set(names) - set(expected)
    if extra:
        raise RealizationCoverageError(
            f"{label} فيها موضعٌ زائد: "
            + "، ".join(sorted(extra))
            + "؛ و"
            + REALIZATION_COVERAGE_IS_EXACT
        )


@dataclass(frozen=True, slots=True)
class LayerRealization:
    """تحقيقُ طبقةٍ واحدةٍ من `Σ_A`: مواضعُها الثمانيةُ كلُّها، ومصائرُ بقاياها."""

    layer_id: str
    components: tuple[ComponentRealization, ...]
    residual_dispositions: tuple[ResidualDispositionRealization, ...]

    def __post_init__(self) -> None:
        _require_text(self.layer_id, "اسمُ الطبقة المُحقَّقة")
        _require_exact_coverage(
            self.components, LAYER_COMPONENT_NAMES, f"مواضعُ `{self.layer_id}`"
        )
        if (
            not isinstance(self.residual_dispositions, tuple)
            or not self.residual_dispositions
        ):
            raise RealizationError(
                "تحقيقٌ بلا مصيرِ بقيّةٍ واحدٍ يطوي البقايا؛ و"
                + A_RESIDUAL_MAY_INDICT_THE_DOMAIN
            )
        dispositions = []
        for item in self.residual_dispositions:
            if not isinstance(item, ResidualDispositionRealization):
                raise RealizationError("عضوٌ في مصائر البقايا خارج نوعه")
            dispositions.append(item.disposition)
        if len(set(dispositions)) != len(dispositions):
            raise RealizationError("مصيرُ بقيّةٍ مكرّرٌ يُرفَض لا يُطوى")

    @property
    def component_names(self) -> tuple[str, ...]:
        """أسماءُ المواضع المُحقَّقة؛ خاصّيّةٌ تُشتَقّ لا حقلٌ يُكتَب."""

        return tuple(item.component_name for item in self.components)

    def component(self, component_name: str) -> ComponentRealization:
        """تحقيقُ موضعٍ باسمه؛ والغيابُ رفضٌ لا `None` يُقرأ صمتًا."""

        for item in self.components:
            if item.component_name == component_name:
                return item
        raise RealizationError(
            f"لا تحقيقَ لموضعٍ اسمُه `{component_name}` في `{self.layer_id}`"
        )

    @property
    def available_dispositions(self) -> frozenset[ResidualDisposition]:
        """مصائرُ البقايا المتاحةُ في هذا التحقيق؛ خاصّيّةٌ تُشتَقّ كذلك."""

        return frozenset(item.disposition for item in self.residual_dispositions)

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى تحقيق الطبقة للبصمة."""

        return {
            "layer_id": self.layer_id,
            "components": [item.as_canonical_content() for item in self.components],
            "residual_dispositions": [
                item.as_canonical_content() for item in self.residual_dispositions
            ],
        }


@dataclass(frozen=True, slots=True)
class TransitionRealization:
    """تحقيقُ انتقالٍ واحدٍ من `Σ_A`: مواضعُه السبعةُ، ومخرَجا عدمِ الترخيص.

    وميدانٌ لا يملك «رفضًا مُسمّى» لا يحقّق بوّابةً: تحقيقٌ بلا `BLOCK` و`DEFER`
    تحقيقٌ يمرّر النجاحَ الصامت، وهو القفزةُ بعينها.
    """

    transition_id: str
    components: tuple[ComponentRealization, ...]
    unlicensed_outcome_realizations: tuple[tuple[TransitionOutcome, str], ...]

    def __post_init__(self) -> None:
        _require_text(self.transition_id, "اسمُ الانتقال المُحقَّق")
        _require_exact_coverage(
            self.components,
            REALIZED_TRANSITION_COMPONENT_NAMES,
            f"مواضعُ `{self.transition_id}`",
        )
        if not isinstance(self.unlicensed_outcome_realizations, tuple):
            raise RealizationError("تحقيقاتُ مخرَجات الرفض مجموعةٌ مُصرَّحٌ بها")
        realized: list[TransitionOutcome] = []
        for entry in self.unlicensed_outcome_realizations:
            if not isinstance(entry, tuple) or len(entry) != 2:
                raise RealizationError("تحقيقُ مخرَج الرفض زوجٌ من مخرَجٍ وبيانِ تحقيقه")
            outcome, realized_as = entry
            if outcome not in _REQUIRED_UNLICENSED_OUTCOMES:
                raise RealizationError("مخرَجُ عدم الترخيص `BLOCK` أو `DEFER` لا غير")
            _require_text(realized_as, f"تحقيقُ `{outcome.value}` في الميدان")
            realized.append(outcome)
        missing = _REQUIRED_UNLICENSED_OUTCOMES - set(realized)
        if missing:
            raise RealizationError(
                "ميدانٌ لا يحقّق مخرَجَ رفضٍ لا يحقّق بوّابةً؛ والناقصُ: "
                + "، ".join(sorted(item.value for item in missing))
            )
        if len(set(realized)) != len(realized):
            raise RealizationError("تحقيقُ مخرَجِ رفضٍ مكرّرٌ يُرفَض لا يُطوى")

    @property
    def component_names(self) -> tuple[str, ...]:
        """أسماءُ المواضع المُحقَّقة؛ خاصّيّةٌ تُشتَقّ لا حقلٌ يُكتَب."""

        return tuple(item.component_name for item in self.components)

    def component(self, component_name: str) -> ComponentRealization:
        """تحقيقُ موضعٍ باسمه؛ والغيابُ رفضٌ كذلك."""

        for item in self.components:
            if item.component_name == component_name:
                return item
        raise RealizationError(
            f"لا تحقيقَ لموضعٍ اسمُه `{component_name}` في `{self.transition_id}`"
        )

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى تحقيق الانتقال للبصمة."""

        return {
            "transition_id": self.transition_id,
            "components": [item.as_canonical_content() for item in self.components],
            "unlicensed_outcome_realizations": [
                {"outcome": outcome.value, "realized_as": realized_as}
                for outcome, realized_as in self.unlicensed_outcome_realizations
            ],
        }


@dataclass(frozen=True, slots=True)
class Realization:
    """تحقيقُ `Σ_A` كاملةً في ميدانٍ واحد، مبصومًا بمحتواه.

    و`deferred_layer_ids` و`deferred_transition_ids` تصريحٌ **صريحٌ** بما لم
    يُحقَّق بعد؛ فالسكوتُ عن طبقةٍ ليس تأجيلًا معلنًا بل تحقيقٌ ناقصٌ يمرّ.
    """

    realization_id: str
    domain: RealizationDomainRef
    specification: AbstractSystemSpecification
    layer_realizations: tuple[LayerRealization, ...]
    transition_realizations: tuple[TransitionRealization, ...] = ()
    deferred_layer_ids: tuple[str, ...] = ()
    deferred_transition_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _require_text(self.realization_id, "اسمُ التحقيق")
        if not isinstance(self.domain, RealizationDomainRef):
            raise RealizationError("الميدانُ إشارةُ ميدانٍ لا نصٌّ مرسَل")
        if not isinstance(self.specification, AbstractSystemSpecification):
            raise RealizationError(
                "التحقيقُ تحقيقُ نظريّةٍ مُسمّاة؛ و"
                + SIGMA_IS_THE_ORIGIN_NOT_ITS_REALIZATIONS
            )
        for value, member_type, label in (
            (self.layer_realizations, LayerRealization, "تحقيقاتُ الطبقات"),
            (
                self.transition_realizations,
                TransitionRealization,
                "تحقيقاتُ الانتقالات",
            ),
        ):
            if not isinstance(value, tuple):
                raise RealizationError(f"{label} مجموعةٌ مُصرَّحٌ بها")
            for item in value:
                if not isinstance(item, member_type):
                    raise RealizationError(f"عضوٌ في {label} خارج نوعه")
        _check_domain_partition(
            realized=tuple(item.layer_id for item in self.layer_realizations),
            deferred=self.deferred_layer_ids,
            declared=self.specification.layer_ids,
            label="الطبقات",
        )
        _check_domain_partition(
            realized=tuple(item.transition_id for item in self.transition_realizations),
            deferred=self.deferred_transition_ids,
            declared=self.specification.transition_ids,
            label="الانتقالات",
        )

    @property
    def realized_layer_ids(self) -> tuple[str, ...]:
        """أسماءُ الطبقات المُحقَّقة؛ خاصّيّةٌ تُشتَقّ لا حقلٌ يُكتَب."""

        return tuple(item.layer_id for item in self.layer_realizations)

    @property
    def realized_transition_ids(self) -> tuple[str, ...]:
        """أسماءُ الانتقالات المُحقَّقة؛ خاصّيّةٌ تُشتَقّ كذلك."""

        return tuple(item.transition_id for item in self.transition_realizations)

    def layer_realization(self, layer_id: str) -> LayerRealization:
        """تحقيقُ طبقةٍ باسمها؛ والغيابُ رفضٌ لا `None` يُقرأ صمتًا."""

        for item in self.layer_realizations:
            if item.layer_id == layer_id:
                return item
        raise RealizationError(f"لا تحقيقَ لطبقةٍ اسمُها `{layer_id}` في هذا الميدان")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى التحقيق للبصمة؛ والنظريّةُ داخلةٌ ببصمتها لا بمحتواها كلِّه."""

        return {
            "realization_id": self.realization_id,
            "domain": self.domain.as_canonical_content(),
            "specification_id": self.specification.spec_id,
            "specification_content_id": self.specification.content_id,
            "layer_realizations": [
                item.as_canonical_content() for item in self.layer_realizations
            ],
            "transition_realizations": [
                item.as_canonical_content() for item in self.transition_realizations
            ],
            "deferred_layer_ids": list(self.deferred_layer_ids),
            "deferred_transition_ids": list(self.deferred_transition_ids),
        }

    @property
    def content_id(self) -> str:
        """بصمةُ التحقيق؛ وهي غيرُ بصمة النظريّة ولا تدخل فيها."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))


def _check_domain_partition(
    *,
    realized: tuple[str, ...],
    deferred: tuple[str, ...],
    declared: tuple[str, ...],
    label: str,
) -> None:
    if not isinstance(deferred, tuple):
        raise RealizationError(f"{label} المؤجَّلةُ مجموعةٌ مُصرَّحٌ بها")
    for item in deferred:
        _require_text(item, f"اسمٌ في {label} المؤجَّلة")
    if len(set(realized)) != len(realized):
        raise RealizationError(f"تحقيقٌ مكرّرٌ في {label} يُرفَض لا يُطوى")
    if len(set(deferred)) != len(deferred):
        raise RealizationError(f"تأجيلٌ مكرّرٌ في {label} يُرفَض لا يُطوى")
    overlap = set(realized) & set(deferred)
    if overlap:
        raise RealizationError(
            f"عضوٌ في {label} مُحقَّقٌ ومؤجَّلٌ معًا دعوى متناقضة: " + "، ".join(sorted(overlap))
        )
    outside = (set(realized) | set(deferred)) - set(declared)
    if outside:
        raise RealizationError(
            f"{label}: اسمٌ خارج النظريّة لا يُحقَّق ولا يُؤجَّل: " + "، ".join(sorted(outside))
        )
    uncovered = set(declared) - set(realized) - set(deferred)
    if uncovered:
        raise RealizationCoverageError(
            f"{label}: عضوٌ في النظريّة بلا تحقيقٍ ولا تأجيلٍ مُصرَّحٍ به: "
            + "، ".join(sorted(uncovered))
            + "؛ و"
            + REALIZATION_COVERAGE_IS_EXACT
        )


_JUDGEMENT_FIELD_MARKERS: Final[tuple[str, ...]] = (
    "verdict",
    "standing",
    "birth",
    "proved",
    "grade",
)

_REALIZATION_TYPES: Final[tuple[type, ...]] = (
    ComponentRealization,
    LayerRealization,
    Realization,
    RealizationDomainRef,
    ResidualDispositionRealization,
    TransitionRealization,
)

for _declaring_type in _REALIZATION_TYPES:  # pragma: no cover - import guard
    for _field in fields(_declaring_type):
        if any(marker in _field.name for marker in _JUDGEMENT_FIELD_MARKERS):
            raise RuntimeError(NO_REALIZATION_GRANTS_STANDING)

if {member.value for member in ResidualDisposition} != {
    "CLOSE",
    "REFINE",
    "REVISE_DOMAIN",
    "DEFER",
}:  # pragma: no cover - import guard
    raise RuntimeError(A_RESIDUAL_MAY_INDICT_THE_DOMAIN)
