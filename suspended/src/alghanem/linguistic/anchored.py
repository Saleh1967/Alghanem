"""`Σ_L` مُسنَدًا إلى `O_L`: الجبرُ يعمل على موجوداتٍ رُخِّصت، ولا يُولّدها.

    O_L  ⊨  LicensedAnchorRole        ثمّ        Σ_L  يبني عليها
    Σ_L  ⊭  TermAnchorKind            أصلًا لغويًّا أوّليًّا

**والدورُ مرجعُ ترخيصٍ لا أصلٌ لغويّ** (`AnAnchorRoleIsALicenseNotAPrimitive`):
`TermAnchorKind` في `nisbah` يُسمّي الجنسَ والفردَ والإحالةَ والحدثَ والكمّيّةَ
فروعًا لمرساة الطرف؛ وتلك ليست أصنافًا لغويّةً خالصةً بل مرشَّحاتٌ أنطولوجيّةٌ
تستعملها اللغةُ بعد أن تَثبُت في طبقةٍ أسبق. فهنا لا يُكتَب النوعُ في المرساة،
بل تُحمَل **رخصةٌ** من `O_L` تقول إنّ موجودًا مُسجَّلًا يستطيع أن يؤدّيَ وظيفةَ
المرساة، بشرطٍ يمكن أن يسقط.

**والشرطُ مرجعٌ مُرخَّصٌ لا نصٌّ حرّ** (`FreeTextConditionIsNotALicensedCondition`،
مُصرَّفًا هنا لا مؤجَّلًا): `identity_condition` و`admissibility_condition` في
`v1` نصّان حرّان، وذلك كافٍ لمرحلة التسجيل وغيرُ كافٍ متى ادُّعي برهانٌ
أنطولوجيّ، إذ لا يتحقّق النظامُ من صدق نثرٍ حرّ ولا من صلته بالمعلومات السابقة.
فالمرساةُ والموضعُ هنا يحملان مرجعًا إلى شرطٍ مولودٍ في `PK_0`، مبصومًا بقاعدته.

**وهذا المستوى بجانب `v1` لا فوقه** (`V2StandsBesideV1NotOverIt`): نصُّ
`G0.NSB-0` ونسخةُ مخطّطه وبصمتُه قائمةٌ بحروفها، لأنّ `v1` نصٌّ قُرِئ، والنسخُ
فوق نصٍّ قُرِئ يمحو تاريخَ الحجّة. وهذه الوحدةُ تُضيف `v2` مبنيًّا على بصمة
`v1` نفسِها، فمن أراد المستوى الأوّلَ وجده كما تُرك.

**والاتّجاهُ لا ينعكس** (`TheAlgebraDoesNotCreateItsObjects`): هذه الوحدةُ
وحدَها من `linguistic/` تقرأ `ontology/`؛ و`ontology/` لا تقرأ `linguistic/`
حرفًا، وإلّا صارت الطبقةُ المُرخِّصةُ مولودةً ممّن تُرخّص له.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`، ولا مدوّنةَ مُسمّاة.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest
from ..ontology.linguistic import (
    FunctionalLicense,
    LinguisticFunction,
    LinguisticOntology,
)
from ..prior.conditions import PriorCondition, PriorConditionKind, PriorInformationBase
from .nisbah import (
    ARGUMENT_ROLES_ARE_DEFERRED_TO_THEIR_OWN_LAYER,
    DEFERRED_ARGUMENT_ROLE_NAMES,
    ArityLicenseGenus,
    TermAnchorKind,
)
from .schema import LINGUISTIC_NISBAH_SCHEMA, SCHEMA_VERSION

__all__ = [
    "ANCHORED_NISBAH_SCHEMA",
    "ANCHORED_SCHEMA_VERSION",
    "AN_ANCHOR_ROLE_IS_A_LICENSE_NOT_A_PRIMITIVE",
    "A_LICENSE_OF_ANOTHER_ONTOLOGY_IS_NOT_A_LICENSE",
    "FREE_TEXT_CONDITION_IS_NOT_A_LICENSED_CONDITION",
    "V2_STANDS_BESIDE_V1_NOT_OVER_IT",
    "AnchoredArgumentSlot",
    "AnchoredLayerError",
    "AnchoredNisbahSchema",
    "AnchoredNisbahSignature",
    "AnchoredPredicateSignature",
    "AnchoredTermAnchor",
    "BaseSchemaRef",
    "LicensedConditionRef",
    "LicensedRoleRef",
]


class AnchoredLayerError(ValueError):
    """رفضٌ عند الإنشاء في الطبقة المُسنَدة؛ لا حملَ على أقرب حالةٍ مقبولة."""


AN_ANCHOR_ROLE_IS_A_LICENSE_NOT_A_PRIMITIVE: Final[str] = (
    "دورُ المرساة رخصةٌ لا أصلٌ لغويّ: الجنسُ والفردُ والحدثُ والكمّيّةُ "
    "والإحالةُ مرشَّحاتٌ أنطولوجيّةٌ تُرخَّص لوظيفةٍ لغويّة، ومن كتبها نوعًا "
    "في المرساة جعل ماهيّةَ الشيء وظيفتَه بلا برهان"
)

FREE_TEXT_CONDITION_IS_NOT_A_LICENSED_CONDITION: Final[str] = (
    "الشرطُ الحرُّ ليس شرطًا مُرخَّصًا: النظامُ لا يتحقّق من صدق نثرٍ حرٍّ ولا "
    "من صلته بالمعلومات السابقة، فشرطُ الهويّة وشرطُ الموضع مرجعان إلى شرطٍ "
    "مولودٍ في `PK_0` مبصومٍ بقاعدته"
)

A_LICENSE_OF_ANOTHER_ONTOLOGY_IS_NOT_A_LICENSE: Final[str] = (
    "رخصةٌ من أنطولوجيا أخرى ليست رخصةً هنا: النسبةُ المُسنَدةُ مشدودةٌ إلى "
    "بصمة `O_L` واحدة، وخلطُ رخصٍ من بصمتين يبني على أساسٍ لم يَعُد قائمًا"
)

V2_STANDS_BESIDE_V1_NOT_OVER_IT: Final[str] = (
    "`v2` بجانب `v1` لا فوقه: نصُّ `G0.NSB-0` ونسخةُ مخطّطه وبصمتُه قائمةٌ "
    "بحروفها، والنسخُ فوق نصٍّ قُرِئ يمحو تاريخَ الحجّة لا يُصحّحه"
)

ANCHORED_SCHEMA_VERSION: Final[str] = "linguistic-nisbah.schema.v2"
"""إصدارُ الطبقة المُسنَدة؛ يقوم بجانب `v1` ولا يحلّ محلَّه."""


def _require_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise AnchoredLayerError(f"{label} نصٌّ غير فارغ")
    return value


@dataclass(frozen=True, slots=True)
class LicensedConditionRef:
    """مرجعٌ إلى شرطٍ مولودٍ في `PK_0`: موضعُه، ومُعرِّفُه، وبصمةُ قاعدته."""

    condition_id: str
    place: PriorConditionKind
    base_id: str
    base_content_id: str

    def __post_init__(self) -> None:
        _require_text(self.condition_id, "مُعرِّفُ الشرط المُشارِ إليه")
        if not isinstance(self.place, PriorConditionKind):
            raise AnchoredLayerError(
                "موضعُ الشرط عضوٌ في مفردة `PK_0` المغلقة؛ و"
                + FREE_TEXT_CONDITION_IS_NOT_A_LICENSED_CONDITION
            )
        _require_text(self.base_id, "مُعرِّفُ القاعدة المُشارِ إليها")
        _require_text(self.base_content_id, "بصمةُ القاعدة المُشارِ إليها")

    @classmethod
    def of(
        cls, base: PriorInformationBase, place: PriorConditionKind
    ) -> LicensedConditionRef:
        """اشتقّ المرجعَ من قاعدةٍ قائمة؛ وشرطٌ غيرُ مُرخَّصٍ لا يُشار إليه."""

        if not isinstance(base, PriorInformationBase):
            raise AnchoredLayerError(
                "المرجعُ يُشتَقّ من قاعدةٍ قائمةٍ لا من اسمٍ حرّ؛ و"
                + FREE_TEXT_CONDITION_IS_NOT_A_LICENSED_CONDITION
            )
        if not isinstance(place, PriorConditionKind):
            raise AnchoredLayerError("موضعُ الشرط عضوٌ في مفردة `PK_0` المغلقة")
        condition: PriorCondition = base.condition(place)
        if not condition.is_usable:
            raise AnchoredLayerError(
                f"الشرطُ `{condition.condition_id}` غيرُ مُرخَّصٍ للاستعمال، "
                "فلا يُبنى عليه شرطُ هويّةٍ ولا شرطُ موضع"
            )
        return cls(
            condition_id=condition.condition_id,
            place=condition.kind,
            base_id=base.base_id,
            base_content_id=base.content_id,
        )

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى المرجع للبصمة."""

        return {
            "condition_id": self.condition_id,
            "place": self.place.value,
            "base_id": self.base_id,
            "base_content_id": self.base_content_id,
        }


@dataclass(frozen=True, slots=True)
class LicensedRoleRef:
    """مرجعُ رخصةٍ وظيفيّةٍ من `O_L`؛ يحلّ محلَّ نوعِ المرساة المكتوب في `v1`."""

    license_id: str
    candidate_id: str
    ontology_id: str
    ontology_content_id: str

    def __post_init__(self) -> None:
        _require_text(self.license_id, "مُعرِّفُ الرخصة")
        _require_text(self.candidate_id, "مُعرِّفُ المرشَّح المُرخَّص")
        _require_text(self.ontology_id, "مُعرِّفُ الأنطولوجيا اللغويّة")
        _require_text(self.ontology_content_id, "بصمةُ الأنطولوجيا اللغويّة")

    @classmethod
    def of(
        cls,
        ontology: LinguisticOntology,
        license_id: str,
        function: LinguisticFunction,
    ) -> LicensedRoleRef:
        """اشتقّ المرجعَ من رخصةٍ قائمةٍ لوظيفةٍ بعينها؛ وما عداها رفضٌ."""

        if not isinstance(ontology, LinguisticOntology):
            raise AnchoredLayerError(
                "المرجعُ يُشتَقّ من أنطولوجيا لغويّةٍ قائمةٍ لا من اسمٍ حرّ؛ و"
                + AN_ANCHOR_ROLE_IS_A_LICENSE_NOT_A_PRIMITIVE
            )
        if not isinstance(function, LinguisticFunction):
            raise AnchoredLayerError("الوظيفةُ عضوٌ في مفردتها المغلقة لا نصٌّ حرّ")
        granted = _licence_by_id(ontology, license_id)
        if granted.function_ref.function is not function:
            raise AnchoredLayerError(
                f"الرخصةُ `{license_id}` مُنِحت لوظيفة "
                f"`{granted.function_ref.function.value}` لا لـ`{function.value}`؛ "
                "ورخصةٌ لوظيفةٍ تُقرَأ لأخرى ترخيصٌ لم يُمنَح"
            )
        if not granted.is_operative:
            raise AnchoredLayerError(
                f"الرخصةُ `{license_id}` وظيفتُها غيرُ مقروءة، ورخصةٌ غيرُ عاملةٍ "
                "لا تُقرَأ عاملةً بالسهو"
            )
        return cls(
            license_id=granted.license_id,
            candidate_id=granted.candidate_ref.candidate_id,
            ontology_id=ontology.ontology_id,
            ontology_content_id=ontology.content_id,
        )

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى المرجع للبصمة."""

        return {
            "license_id": self.license_id,
            "candidate_id": self.candidate_id,
            "ontology_id": self.ontology_id,
            "ontology_content_id": self.ontology_content_id,
        }


def _licence_by_id(ontology: LinguisticOntology, license_id: str) -> FunctionalLicense:
    _require_text(license_id, "مُعرِّفُ الرخصة المطلوبة")
    for granted in ontology.licenses:
        if granted.license_id == license_id:
            return granted
    raise AnchoredLayerError(
        f"لا رخصةَ في `O_L` مُعرِّفُها `{license_id}`؛ والغيابُ رفضٌ لا صمت"
    )


@dataclass(frozen=True, slots=True)
class AnchoredTermAnchor:
    """مرساةُ طرفٍ مُسنَدة: رخصةٌ من `O_L`، وشرطُ هويّةٍ مرجعُه `PK_0`."""

    anchor_id: str
    role_ref: LicensedRoleRef
    identity_condition_ref: LicensedConditionRef

    def __post_init__(self) -> None:
        _require_text(self.anchor_id, "مُعرِّفُ المرساة")
        if not isinstance(self.role_ref, LicensedRoleRef):
            raise AnchoredLayerError(AN_ANCHOR_ROLE_IS_A_LICENSE_NOT_A_PRIMITIVE)
        if not isinstance(self.identity_condition_ref, LicensedConditionRef):
            raise AnchoredLayerError(FREE_TEXT_CONDITION_IS_NOT_A_LICENSED_CONDITION)

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى المرساة للبصمة."""

        return {
            "anchor_id": self.anchor_id,
            "role_ref": self.role_ref.as_canonical_content(),
            "identity_condition_ref": (
                self.identity_condition_ref.as_canonical_content()
            ),
        }


@dataclass(frozen=True, slots=True)
class AnchoredArgumentSlot:
    """موضعُ حجّةٍ مُسنَد: رتبتُه، وشرطُ ما يقع فيه مرجعًا لا نثرًا حرًّا."""

    slot_id: str
    position: int
    admissibility_condition_ref: LicensedConditionRef

    def __post_init__(self) -> None:
        _require_text(self.slot_id, "مُعرِّفُ الموضع")
        if type(self.position) is not int or self.position < 1:
            raise AnchoredLayerError("رتبةُ الموضع عددٌ صحيحٌ موجبٌ يبدأ من واحد")
        if not isinstance(self.admissibility_condition_ref, LicensedConditionRef):
            raise AnchoredLayerError(FREE_TEXT_CONDITION_IS_NOT_A_LICENSED_CONDITION)
        lowered = self.slot_id.casefold()
        for deferred in DEFERRED_ARGUMENT_ROLE_NAMES:
            if deferred in lowered:
                raise AnchoredLayerError(ARGUMENT_ROLES_ARE_DEFERRED_TO_THEIR_OWN_LAYER)

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الموضع للبصمة."""

        return {
            "slot_id": self.slot_id,
            "position": self.position,
            "admissibility_condition_ref": (
                self.admissibility_condition_ref.as_canonical_content()
            ),
        }


@dataclass(frozen=True, slots=True)
class AnchoredPredicateSignature:
    """محمولٌ مُسنَد: رخصةُ محمولٍ من `O_L`، ورتبةٌ مُرخَّصةٌ بجنسها المُعاد استعمالُه."""

    predicate_id: str
    role_ref: LicensedRoleRef
    arity: int
    arity_license: ArityLicenseGenus
    slots: tuple[AnchoredArgumentSlot, ...]

    def __post_init__(self) -> None:
        _require_text(self.predicate_id, "مُعرِّفُ المحمول")
        if not isinstance(self.role_ref, LicensedRoleRef):
            raise AnchoredLayerError(AN_ANCHOR_ROLE_IS_A_LICENSE_NOT_A_PRIMITIVE)
        if type(self.arity) is not int or self.arity < 1:
            raise AnchoredLayerError("رتبةُ المحمول عددٌ صحيحٌ موجب")
        if not isinstance(self.arity_license, ArityLicenseGenus):
            raise AnchoredLayerError("ترخيصُ الرتبة عضوٌ في مفردته المغلقة")
        if not self.arity_license.licenses_use:
            raise AnchoredLayerError(
                "رتبةٌ منتزعةٌ من الحالة المستهدَفة لا تُرخِّص استعمالَها"
            )
        if not isinstance(self.slots, tuple) or not self.slots:
            raise AnchoredLayerError("المحمولُ موضعُ حجّةٍ فأكثر")
        for slot in self.slots:
            if not isinstance(slot, AnchoredArgumentSlot):
                raise AnchoredLayerError("عضوٌ في مواضع الحجج خارج نوعه")
        if len(self.slots) != self.arity:
            raise AnchoredLayerError(
                "عددُ مواضع الحجج هو الرتبةُ نفسُها؛ ورتبةٌ تخالف مواضعَها "
                "رتبةٌ مكتوبةٌ لا مُشتَقّة"
            )
        positions = tuple(slot.position for slot in self.slots)
        if sorted(positions) != list(range(1, self.arity + 1)):
            raise AnchoredLayerError("مواضعُ الحجج متتابعةٌ من واحدٍ إلى الرتبة بلا ثغرة")
        slot_ids = tuple(slot.slot_id for slot in self.slots)
        if len(set(slot_ids)) != len(slot_ids):
            raise AnchoredLayerError("أسماءُ المواضع بلا تكرار؛ والمكرّرُ يُخفي موضعًا")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى المحمول للبصمة."""

        return {
            "predicate_id": self.predicate_id,
            "role_ref": self.role_ref.as_canonical_content(),
            "arity": self.arity,
            "arity_license": self.arity_license.value,
            "slots": [slot.as_canonical_content() for slot in self.slots],
        }


@dataclass(frozen=True, slots=True)
class AnchoredNisbahSignature:
    """نسبةٌ مُسنَدة: كلُّ رخصةٍ فيها من بصمة `O_L` واحدة، لا من بصمتين."""

    nisbah_id: str
    ontology_content_id: str
    predicate: AnchoredPredicateSignature
    anchors: tuple[AnchoredTermAnchor, ...]

    def __post_init__(self) -> None:
        _require_text(self.nisbah_id, "مُعرِّفُ النسبة")
        _require_text(self.ontology_content_id, "بصمةُ الأنطولوجيا اللغويّة")
        if not isinstance(self.predicate, AnchoredPredicateSignature):
            raise AnchoredLayerError("النسبةُ محمولٌ واحدٌ بنوعه لا نصٌّ يُسمّيه")
        if not isinstance(self.anchors, tuple):
            raise AnchoredLayerError("مراسي الأطراف مجموعةٌ مُصرَّحٌ بها")
        for anchor in self.anchors:
            if not isinstance(anchor, AnchoredTermAnchor):
                raise AnchoredLayerError("عضوٌ في مراسي الأطراف خارج نوعه")
        anchor_ids = tuple(anchor.anchor_id for anchor in self.anchors)
        if len(set(anchor_ids)) != len(anchor_ids):
            raise AnchoredLayerError("أسماءُ المراسي بلا تكرار في النسبة الواحدة")
        if len(self.anchors) > self.predicate.arity:
            raise AnchoredLayerError(
                "مراسي الأطراف لا تزيد على رتبة المحمول؛ وزيادتُها طرفٌ بلا موضع"
            )
        bound = (self.predicate.role_ref,) + tuple(
            anchor.role_ref for anchor in self.anchors
        )
        for role_ref in bound:
            if role_ref.ontology_content_id != self.ontology_content_id:
                raise AnchoredLayerError(A_LICENSE_OF_ANOTHER_ONTOLOGY_IS_NOT_A_LICENSE)

    @classmethod
    def licensed_by(
        cls,
        nisbah_id: str,
        ontology: LinguisticOntology,
        predicate: AnchoredPredicateSignature,
        anchors: tuple[AnchoredTermAnchor, ...],
    ) -> AnchoredNisbahSignature:
        """ابنِ نسبةً على أنطولوجيا قائمة؛ والبصمةُ تُؤخَذ منها لا تُكتَب بجانبها."""

        if not isinstance(ontology, LinguisticOntology):
            raise AnchoredLayerError(
                "النسبةُ المُسنَدةُ تُبنى على أنطولوجيا لغويّةٍ قائمةٍ لا على اسمٍ حرّ"
            )
        return cls(
            nisbah_id=nisbah_id,
            ontology_content_id=ontology.content_id,
            predicate=predicate,
            anchors=anchors,
        )

    @property
    def unfilled_slot_count(self) -> int:
        """كم موضعَ حجّةٍ بقي بلا مرساة؟ خاصّيّةٌ تُشتَقّ لا حقلٌ يُكتَب."""

        return self.predicate.arity - len(self.anchors)

    @property
    def are_arguments_closed(self) -> bool:
        """أامتلأت المواضع؟ **مكوّنٌ واحدٌ** من الإغلاق لا الإغلاقُ كلُّه."""

        return self.unfilled_slot_count == 0

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى النسبة المُسنَدة للبصمة."""

        return {
            "nisbah_id": self.nisbah_id,
            "ontology_content_id": self.ontology_content_id,
            "predicate": self.predicate.as_canonical_content(),
            "anchors": [anchor.as_canonical_content() for anchor in self.anchors],
        }

    @property
    def content_id(self) -> str:
        """بصمةُ النسبة المُسنَدة؛ ونسبتان بمحتوًى واحدٍ نسبةٌ واحدة."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))


@dataclass(frozen=True, slots=True)
class BaseSchemaRef:
    """إشارةٌ مبصومةٌ إلى `v1`؛ تُشتَقّ من المخطّط القائم ولا تُكتَب يدويًّا."""

    schema_version: str
    content_id: str

    def __post_init__(self) -> None:
        _require_text(self.schema_version, "إصدارُ المخطّط المُشارِ إليه")
        _require_text(self.content_id, "بصمةُ المخطّط المُشارِ إليه")

    @classmethod
    def of(cls) -> BaseSchemaRef:
        """الإشارةُ إلى `v1` القائم؛ ومصدرُها المخطّطُ نفسُه لا نسخةٌ عنه."""

        return cls(
            schema_version=LINGUISTIC_NISBAH_SCHEMA.schema_version,
            content_id=LINGUISTIC_NISBAH_SCHEMA.content_id,
        )

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الإشارة للبصمة."""

        return {
            "schema_version": self.schema_version,
            "content_id": self.content_id,
        }


@dataclass(frozen=True, slots=True)
class AnchoredNisbahSchema:
    """`v2`: مخطّطٌ مُسنَدٌ إلى `O_L`، مبنيٌّ على بصمة `v1` وقائمٌ بجانبه."""

    schema_version: str
    base_schema_ref: BaseSchemaRef
    ontology_bound: bool

    def __post_init__(self) -> None:
        _require_text(self.schema_version, "إصدارُ المخطّط المُسنَد")
        if not isinstance(self.base_schema_ref, BaseSchemaRef):
            raise AnchoredLayerError(V2_STANDS_BESIDE_V1_NOT_OVER_IT)
        if self.base_schema_ref.schema_version == self.schema_version:
            raise AnchoredLayerError(
                "إصدارُ `v2` غيرُ إصدار `v1`؛ وإصدارٌ يحمل اسمَ سابقه نسخٌ فوقه"
            )
        if (
            self.base_schema_ref.schema_version != SCHEMA_VERSION
            or self.base_schema_ref.content_id != LINGUISTIC_NISBAH_SCHEMA.content_id
        ):
            raise AnchoredLayerError(
                "بصمةُ `v1` غيرُ مطابقةٍ للقائم: مخطّطٌ مُسنَدٌ إلى نواةٍ لم تَعُد قائمة"
            )
        if self.ontology_bound is not True:
            raise AnchoredLayerError(
                "المخطّطُ المُسنَدُ مشدودٌ إلى `O_L`؛ ومخطّطٌ غيرُ مشدودٍ هو `v1` باسمٍ آخر"
            )

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى المخطّط المُسنَد للبصمة."""

        return {
            "schema_version": self.schema_version,
            "base_schema_ref": self.base_schema_ref.as_canonical_content(),
            "ontology_bound": self.ontology_bound,
        }

    @property
    def content_id(self) -> str:
        """بصمةُ `v2`؛ وهي غيرُ بصمة `v1` ولا تحلّ محلَّها."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))


ANCHORED_NISBAH_SCHEMA: Final[AnchoredNisbahSchema] = AnchoredNisbahSchema(
    schema_version=ANCHORED_SCHEMA_VERSION,
    base_schema_ref=BaseSchemaRef.of(),
    ontology_bound=True,
)
"""`v2` قائمًا بجانب `v1`، مبنيًّا على بصمته لا على اسمه."""


def _refuse_a_written_kind_in_the_anchored_layer() -> None:
    """لا حقلَ من نوع `TermAnchorKind` هنا: الدورُ يُرخَّص ولا يُكتَب نوعًا."""

    declaring = (
        LicensedRoleRef,
        LicensedConditionRef,
        AnchoredTermAnchor,
        AnchoredArgumentSlot,
        AnchoredPredicateSignature,
        AnchoredNisbahSignature,
    )
    for owner in declaring:
        for field in fields(owner):
            annotation = field.type
            name = annotation.__name__ if isinstance(annotation, type) else annotation
            if TermAnchorKind.__name__ in str(name):
                raise RuntimeError(AN_ANCHOR_ROLE_IS_A_LICENSE_NOT_A_PRIMITIVE)


def _refuse_a_free_text_condition_field() -> None:
    """لا حقلَ شرطٍ نصًّا حرًّا هنا؛ وكلُّ شرطٍ مرجعٌ مبصومٌ إلى `PK_0`."""

    for owner in (AnchoredTermAnchor, AnchoredArgumentSlot):
        for field in fields(owner):
            if "condition" not in field.name:
                continue
            annotation = field.type
            name = annotation.__name__ if isinstance(annotation, type) else annotation
            if LicensedConditionRef.__name__ not in str(name):
                raise RuntimeError(FREE_TEXT_CONDITION_IS_NOT_A_LICENSED_CONDITION)


def _refuse_a_version_that_overwrites_the_read_one() -> None:
    """`v1` قائمٌ بحروفه؛ وتغيُّرُ إصداره أو بصمته يُوقف هذه الطبقةَ لا يُطوى."""

    if SCHEMA_VERSION != "linguistic-nisbah.schema.v1":  # pragma: no cover
        raise RuntimeError(V2_STANDS_BESIDE_V1_NOT_OVER_IT)
    if ANCHORED_SCHEMA_VERSION == SCHEMA_VERSION:  # pragma: no cover
        raise RuntimeError(V2_STANDS_BESIDE_V1_NOT_OVER_IT)


_refuse_a_written_kind_in_the_anchored_layer()
_refuse_a_free_text_condition_field()
_refuse_a_version_that_overwrites_the_read_one()
