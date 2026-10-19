"""الهويّةُ والبذرةُ والعقدة: حاملٌ مُعرَّفٌ عند مقياسٍ مُحَلّ، وبصمةٌ مُشتَقّةٌ لا مكتوبة.

    FractalIdentity  =  instance identity  +  resolved scale  +  identity criterion

**والهويّةُ هويّةُ نسخةٍ لا جنسِ هويّة** (`InstanceIdentityIsNotIdentityType`):
حفظُ الهويّة في تحويلٍ حافظٍ معناه أنّ الهويّةَ عينُها لا أنّ نوعَها واحد؛
فتساوي المعيارَين مع اختلاف المُعرِّف اختلافُ هويّةٍ لا حفظُها.

**والبصمةُ مُشتَقّة** (`DoNotStoreDerivableIdentityAsASecondClaim`): `content_id`
خاصّيّةٌ تُحسَب من المحتوى القانونيِّ لا حقلٌ يكتبه المستدعي فيختلف عن محتواه.

**والبقيّةُ مرصودةٌ لا مكتوبةٌ في المدخل**، وهي ليست حالةَ وقوفٍ
(`Residual ≠ Disposition`): تُسمّي حاملَها وجنسَها وسببَها، وتبقى في القرار
وفي العقدة المغلقة بلا محو.

تسجيلٌ لا سلطة: لا ولادةَ، ولا حكمَ ولادةٍ، ولا تجميدَ `E0`.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest, is_canonical_digest
from .laws import RESIDUAL_IS_NOT_DISPOSITION
from .scale import FractalScaleRef, ScaleSpace

__all__ = [
    "DO_NOT_STORE_DERIVABLE_IDENTITY_AS_A_SECOND_CLAIM",
    "FractalContent",
    "FractalIdentity",
    "FractalNode",
    "FractalNodeError",
    "FractalNodeRef",
    "FractalResidual",
    "FractalResidualKind",
    "FractalSeed",
    "INSTANCE_IDENTITY_IS_NOT_IDENTITY_TYPE",
]


INSTANCE_IDENTITY_IS_NOT_IDENTITY_TYPE: Final[str] = (
    "هويّةُ النسخة ليست جنسَ الهويّة: `InstanceIdentity ≠ IdentityType`؛ فحفظُ "
    "الهويّة حفظُ عينِها، ووحدةُ المعيار مع اختلاف المُعرِّف اختلافٌ لا حفظ"
)

DO_NOT_STORE_DERIVABLE_IDENTITY_AS_A_SECOND_CLAIM: Final[str] = (
    "لا تُخزَّن هويّةٌ قابلةٌ للاشتقاق دعوًى ثانية: البصمةُ تُحسَب من المحتوى، "
    "وحقلٌ مكتوبٌ بجانبه دعوى قد تُخالِفه"
)

FractalContent = tuple[tuple[str, str], ...]


class FractalNodeError(ValueError):
    """رفضٌ عند تكوين هويّةٍ أو بذرةٍ أو عقدةٍ أو بقيّة."""


def _named_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise FractalNodeError(f"{label} نصٌّ غير فارغ")
    return value


def _checked_content(content: object) -> FractalContent:
    if not isinstance(content, tuple):
        raise FractalNodeError("محتوى الحامل أزواجٌ مُصرَّحٌ بها في مجموعةٍ مُرتَّبة")
    seen: set[str] = set()
    for entry in content:
        if not isinstance(entry, tuple) or len(entry) != 2:
            raise FractalNodeError("كلُّ مدخلةِ محتوًى زوجُ اسمٍ وقيمة")
        key, value = entry
        _named_text(key, "اسمُ مدخلة المحتوى")
        _named_text(value, "قيمةُ مدخلة المحتوى")
        if key in seen:
            raise FractalNodeError("اسمُ مدخلةٍ مُكرَّرٌ في محتوًى واحد")
        seen.add(key)
    return content


class FractalResidualKind(Enum):
    """أجناسُ البقايا؛ مفردةٌ مغلقةٌ لا نصٌّ حرٌّ يُخفي تحته حجبًا غيرَ مُسمًّى."""

    UNRESOLVED_DIFFERENCE = "unresolved_difference"
    UNVERIFIED_PATTERN_PROOF = "unverified_pattern_proof"
    UNCOVERED_MINIMUM_REQUIREMENT = "uncovered_minimum_requirement"
    DEFERRED_BRANCH = "deferred_branch"
    BLOCKED_BRANCH = "blocked_branch"
    IRREDUCIBLE_AT_CURRENT_SCALE = "irreducible_at_current_scale"


@dataclass(frozen=True, slots=True)
class FractalResidual:
    """بقيّةٌ مرصودة: جنسُها، وحاملُها، وسببُها؛ وهي ليست حكمًا على فرع."""

    kind: FractalResidualKind
    subject_id: str
    reason: str
    blocking: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.kind, FractalResidualKind):
            raise FractalNodeError(
                "جنسُ البقيّة عضوٌ في مفردته المغلقة؛ و" + RESIDUAL_IS_NOT_DISPOSITION
            )
        _named_text(self.subject_id, "موضوعُ البقيّة")
        _named_text(self.reason, "سببُ البقيّة")
        if type(self.blocking) is not bool:
            raise FractalNodeError("كونُ البقيّة مانعةً حكمٌ ثنائيٌّ صريح")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى البقيّة للبصمة."""

        return {
            "kind": self.kind.value,
            "subject_id": self.subject_id,
            "reason": self.reason,
            "blocking": self.blocking,
        }


@dataclass(frozen=True, slots=True)
class FractalIdentity:
    """هويّةُ نسخةٍ عند مقياسٍ مُحَلٍّ بمعيارِ هويّةٍ مُسمًّى."""

    identity_id: str
    scale_ref: FractalScaleRef
    identity_criterion_id: str

    def __post_init__(self) -> None:
        _named_text(self.identity_id, "مُعرِّفُ هويّة النسخة")
        if not isinstance(self.scale_ref, FractalScaleRef):
            raise FractalNodeError("الهويّةُ تقع عند مقياسٍ بمرجعه")
        _named_text(self.identity_criterion_id, "معيارُ الهويّة")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الهويّة للبصمة."""

        return {
            "identity_id": self.identity_id,
            "scale_id": self.scale_ref.scale_id,
            "scale_contract_content_id": self.scale_ref.contract_content_id,
            "identity_criterion_id": self.identity_criterion_id,
        }

    @property
    def content_id(self) -> str:
        """بصمةُ الهويّة؛ مُشتَقّةٌ لا مكتوبة."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))

    def is_same_instance_as(self, other: object) -> bool:
        """أهي الهويّةُ عينُها؟ لا أهي من جنسها."""

        return (
            isinstance(other, FractalIdentity) and self.content_id == other.content_id
        )


@dataclass(frozen=True, slots=True)
class FractalSeed:
    """بذرةٌ: حاملٌ ومحتوًى وهويّةٌ ابتدائيّةٌ عند مقياسٍ مُحَلّ."""

    seed_id: str
    identity: FractalIdentity
    carrier_id: str
    content: FractalContent

    def __post_init__(self) -> None:
        _named_text(self.seed_id, "مُعرِّفُ البذرة")
        if not isinstance(self.identity, FractalIdentity):
            raise FractalNodeError("البذرةُ تحمل هويّةً من نوعها")
        _named_text(self.carrier_id, "حاملُ البذرة")
        _checked_content(self.content)

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى البذرة للبصمة."""

        return {
            "seed_id": self.seed_id,
            "identity": self.identity.as_canonical_content(),
            "carrier_id": self.carrier_id,
            "content": [list(entry) for entry in self.content],
        }

    @property
    def content_id(self) -> str:
        """بصمةُ البذرة؛ مُشتَقّةٌ لا مكتوبة."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))


@dataclass(frozen=True, slots=True)
class FractalNodeRef:
    """مرجعُ عقدة: مُعرِّفُها وبصمةُ محتواها بعينه."""

    node_id: str
    content_id: str

    def __post_init__(self) -> None:
        _named_text(self.node_id, "مُعرِّفُ العقدة المُشار إليها")
        if not is_canonical_digest(self.content_id):
            raise FractalNodeError("مرجعُ العقدة يحمل بصمةً قانونيّةً لا وصفًا حرًّا")


@dataclass(frozen=True, slots=True)
class FractalNode:
    """عقدةٌ فراكتاليّة: هويّةُ نسخةٍ، وحاملٌ، ومحتوًى، وأصلٌ مُسمًّى."""

    node_id: str
    identity: FractalIdentity
    carrier_id: str
    content: FractalContent
    origin_id: str

    def __post_init__(self) -> None:
        _named_text(self.node_id, "مُعرِّفُ العقدة")
        if not isinstance(self.identity, FractalIdentity):
            raise FractalNodeError("العقدةُ تحمل هويّةً من نوعها")
        _named_text(self.carrier_id, "حاملُ العقدة")
        _checked_content(self.content)
        _named_text(self.origin_id, "أصلُ العقدة")

    @classmethod
    def from_seed(cls, seed: FractalSeed, *, node_id: str) -> FractalNode:
        """عقدةٌ ابتدائيّةٌ من بذرةٍ بعينها؛ وأصلُها بصمةُ تلك البذرة."""

        if not isinstance(seed, FractalSeed):
            raise FractalNodeError("العقدةُ الابتدائيّةُ تُبنى من بذرةٍ من نوعها")
        return cls(
            node_id=node_id,
            identity=seed.identity,
            carrier_id=seed.carrier_id,
            content=seed.content,
            origin_id=seed.content_id,
        )

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى العقدة للبصمة."""

        return {
            "node_id": self.node_id,
            "identity": self.identity.as_canonical_content(),
            "carrier_id": self.carrier_id,
            "content": [list(entry) for entry in self.content],
            "origin_id": self.origin_id,
        }

    @property
    def content_id(self) -> str:
        """بصمةُ العقدة؛ مُشتَقّةٌ لا مكتوبة."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))

    def as_ref(self) -> FractalNodeRef:
        """مرجعٌ إلى هذه العقدة بعينها."""

        return FractalNodeRef(node_id=self.node_id, content_id=self.content_id)

    def resolved_scale(self, space: ScaleSpace) -> str:
        """مُعرِّفُ مقياسها بعد حلِّ مرجعه في فضاءٍ مُسجَّل."""

        return space.resolve(self.identity.scale_ref).scale_id
