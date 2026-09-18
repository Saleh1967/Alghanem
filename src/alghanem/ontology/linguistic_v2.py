"""`O_L²`: الأنطولوجيا اللغويّة بأصلٍ مبصوم — بجانب `O_L` لا فوقها.

    FunctionalLicense  →  ReferencedFunctionalLicense
    condition_statement (نصٌّ حرّ)  →  PriorConditionRef (مرجعٌ مبصوم)

**وأصلُ الرخصة مرجعٌ لا نثر** (`ALicenseIsFoundedOnAStandingLicensedConditionNotOnProse`):
`O_L` الأولى تحمل في رخصتها بيانَ شرطٍ نصًّا حرًّا وتُسمّي **موضعَ** الشرط فقط،
فتستطيع أن تقول «رُخِّصتُ بشرطٍ من موضع كذا» ولا تستطيع أن تقول **أيُّ شرطٍ
بعينه** رخّصها ومن أيّ قاعدةٍ وما بصمتُها. وهذا الإصدارُ يستبدل بالنصّ الحرّ
مرجعًا إلى شرطٍ قائمٍ مُرخَّصٍ في `PK_0`، مبصومًا بقاعدته.

**والرخصةُ وشرطُها من قاعدةٍ واحدة** (`ALicenseAndItsConditionShareOneBase`):
رخصةٌ شرطُها من قاعدةٍ غيرِ القاعدة التي تأسّست عليها `O_0` رخصةُ مسارٍ وجوديٍّ
آخر؛ ولا يكفي اتّحادُ الاسم دون اتّحاد البصمة. والمخالفاتُ تُسمَّى جميعًا ولا
يُوقَف عند أوّلها، على منهج `PriorCoverageIsExactNotBestEffort`.

**وهذا الإصدارُ بجانب الأوّل لا فوقه** (`AHistoricalLayerKeepsItsDependencySemantics`):
`ontology/linguistic.py` لا تُمَسّ بحرف، لأنّ `linguistic/anchored.py` (`v2`)
مُسجَّلةٌ في `G0.ONT-1` وتستوردها؛ وتعديلُها يُغيِّر معنى `v2` التنفيذيَّ من
تحتها وإن بقيت بايتاتُها. فحفظُ الطبقة حفظُ ملفّها **وإغلاقِ اعتماداتها**.

**والمفرداتُ مُعادةُ الاستعمال لا منسوخة**: `LinguisticFunction` و
`OntologicalCandidateRef` و`LinguisticFunctionRef` تُقرَأ من الإصدار الأوّل ولا
تُكتَب ثانيةً، فمفردةٌ واحدةٌ لا مفردتان تتفرّقان.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest
from ..prior.conditions import PriorConditionKind, PriorInformationBase
from ..prior.references import PriorConditionRef
from .general import GeneralOntology, OntologicalCandidate, PriorBaseRef
from .linguistic import (
    LinguisticFunction,
    LinguisticFunctionRef,
    OntologicalCandidateRef,
)

__all__ = [
    "A_LICENSE_AND_ITS_CONDITION_SHARE_ONE_BASE",
    "A_LICENSE_IS_FOUNDED_ON_A_STANDING_LICENSED_CONDITION_NOT_ON_PROSE",
    "A_HISTORICAL_LAYER_KEEPS_ITS_DEPENDENCY_SEMANTICS",
    "LinguisticOntologyV2",
    "LinguisticOntologyV2Error",
    "ReferencedFunctionalLicense",
]


class LinguisticOntologyV2Error(ValueError):
    """رفضٌ عند الإنشاء في `O_L²`؛ لا حملَ على أقرب حالةٍ مقبولة."""


A_LICENSE_IS_FOUNDED_ON_A_STANDING_LICENSED_CONDITION_NOT_ON_PROSE: Final[str] = (
    "أصلُ الرخصة شرطٌ قائمٌ مُرخَّصٌ لا نثرٌ حرّ: رخصةٌ تحمل بيانًا تفسيريًّا "
    "تستطيع أن تُسمّي موضعَ الشرط ولا تستطيع أن تُسمّي الشرطَ بعينه ولا قاعدتَه "
    "ولا بصمتَها، فيبقى النصُّ الحرُّ في أصل الترخيص وإن أُغلِق بعده"
)

A_LICENSE_AND_ITS_CONDITION_SHARE_ONE_BASE: Final[str] = (
    "الرخصةُ وشرطُها من قاعدةٍ واحدة: رخصةٌ شرطُها من قاعدةٍ غيرِ التي تأسّست "
    "عليها الأنطولوجيا العامّةُ رخصةُ مسارٍ وجوديٍّ آخر، واتّحادُ الاسم دون "
    "اتّحاد البصمة قاعدةٌ أخرى باسمٍ مُعاد"
)

A_HISTORICAL_LAYER_KEEPS_ITS_DEPENDENCY_SEMANTICS: Final[str] = (
    "الطبقةُ التاريخيّةُ تحفظ دلالةَ اعتماداتها: لا يكفي ألّا يتغيّر ملفُّها، "
    "فمعناها التنفيذيُّ قائمٌ بما تستورده؛ وتعديلُ ما تحتها يُغيِّرها وإن بقيت "
    "بايتاتُها، فالحفظُ بايتاتٌ وإغلاقُ اعتماداتٍ معًا"
)


def _require_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise LinguisticOntologyV2Error(f"{label} نصٌّ غير فارغ")
    return value


@dataclass(frozen=True, slots=True)
class ReferencedFunctionalLicense:
    """رخصةٌ وظيفيّةٌ أصلُها مرجعُ شرطٍ مبصوم، لا بيانٌ تفسيريٌّ حرّ."""

    license_id: str
    candidate_ref: OntologicalCandidateRef
    function_ref: LinguisticFunctionRef
    condition_ref: PriorConditionRef

    def __post_init__(self) -> None:
        _require_text(self.license_id, "مُعرِّفُ الرخصة")
        if not isinstance(self.candidate_ref, OntologicalCandidateRef):
            raise LinguisticOntologyV2Error(
                "مرجعُ المرشَّح من نوعه المُعاد استعمالُه لا من اسمٍ حرّ"
            )
        if not isinstance(self.function_ref, LinguisticFunctionRef):
            raise LinguisticOntologyV2Error(
                "مرجعُ الوظيفة من نوعه المُعاد استعمالُه لا من اسمٍ حرّ"
            )
        if not isinstance(self.condition_ref, PriorConditionRef):
            raise LinguisticOntologyV2Error(
                A_LICENSE_IS_FOUNDED_ON_A_STANDING_LICENSED_CONDITION_NOT_ON_PROSE
            )

    @classmethod
    def granted(
        cls,
        license_id: str,
        candidate: OntologicalCandidate,
        function: LinguisticFunction,
        read_from: str,
        base: PriorInformationBase,
        place: PriorConditionKind,
    ) -> ReferencedFunctionalLicense:
        """امنح رخصةً من مرشَّحٍ قائمٍ وشرطٍ قائم؛ ولا يُكتَب مرجعٌ بجانبهما."""

        return cls(
            license_id=license_id,
            candidate_ref=OntologicalCandidateRef.of(candidate),
            function_ref=LinguisticFunctionRef(function=function, read_from=read_from),
            condition_ref=PriorConditionRef.of(base, place),
        )

    @property
    def licensing_place(self) -> PriorConditionKind:
        """موضعُ الشرط المُرخِّص؛ خاصّيّةٌ تُشتَقّ من المرجع لا حقلٌ يُكتَب بجانبه."""

        return self.condition_ref.place

    @property
    def is_operative(self) -> bool:
        """أرخصةٌ عاملة؟ رخصةٌ وظيفتُها غيرُ مقروءةٍ مُسجَّلةٌ ولا تُقرَأ عاملة."""

        return self.function_ref.is_read

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الرخصة للبصمة؛ ولا حقلَ نصٍّ حرٍّ فيه."""

        return {
            "license_id": self.license_id,
            "candidate_ref": self.candidate_ref.as_canonical_content(),
            "function_ref": self.function_ref.as_canonical_content(),
            "condition_ref": self.condition_ref.as_canonical_content(),
        }


@dataclass(frozen=True, slots=True)
class LinguisticOntologyV2:
    """`O_L²`: رخصٌ أصلُها مبصوم، وكلُّها راجعةٌ إلى قاعدة `O_0` نفسِها."""

    ontology_id: str
    general_ontology_id: str
    general_content_id: str
    prior_base_ref: PriorBaseRef
    licenses: tuple[ReferencedFunctionalLicense, ...]

    def __post_init__(self) -> None:
        _require_text(self.ontology_id, "مُعرِّفُ الأنطولوجيا اللغويّة")
        _require_text(self.general_ontology_id, "مُعرِّفُ الأنطولوجيا العامّة")
        _require_text(self.general_content_id, "بصمةُ الأنطولوجيا العامّة")
        if not isinstance(self.prior_base_ref, PriorBaseRef):
            raise LinguisticOntologyV2Error(
                "مرجعُ القاعدة السابقة مأخوذٌ من الأنطولوجيا العامّة لا مكتوبٌ بجانبها"
            )
        if not isinstance(self.licenses, tuple) or not self.licenses:
            raise LinguisticOntologyV2Error("الأنطولوجيا اللغويّةُ رخصةٌ فأكثر")
        for granted in self.licenses:
            if not isinstance(granted, ReferencedFunctionalLicense):
                raise LinguisticOntologyV2Error("عضوٌ في الرخص خارج نوعه")
        ids = tuple(granted.license_id for granted in self.licenses)
        if len(set(ids)) != len(ids):
            raise LinguisticOntologyV2Error(
                "مُعرِّفُ الرخصة لا يتكرّر؛ والمكرّرُ يُرفَض لا يُطوى"
            )
        offenders = tuple(
            granted.license_id
            for granted in self.licenses
            if granted.condition_ref.base_id != self.prior_base_ref.base_id
            or granted.condition_ref.base_content_id != self.prior_base_ref.content_id
        )
        if offenders:
            raise LinguisticOntologyV2Error(
                A_LICENSE_AND_ITS_CONDITION_SHARE_ONE_BASE
                + "؛ والرخصُ المخالفة: "
                + "، ".join(offenders)
            )

    @classmethod
    def founded_on(
        cls,
        ontology_id: str,
        general: GeneralOntology,
        licenses: tuple[ReferencedFunctionalLicense, ...],
    ) -> LinguisticOntologyV2:
        """أسِّس رخصًا على أنطولوجيا قائمة؛ وتُسمَّى المخالفاتُ كلُّها لا أوّلُها."""

        if not isinstance(general, GeneralOntology):
            raise LinguisticOntologyV2Error(
                "التأسيسُ على أنطولوجيا عامّةٍ قائمةٍ لا على اسمٍ حرّ"
            )
        if not isinstance(licenses, tuple) or not licenses:
            raise LinguisticOntologyV2Error("الأنطولوجيا اللغويّةُ رخصةٌ فأكثر")
        unknown: list[str] = []
        mismatched: list[str] = []
        for granted in licenses:
            if not isinstance(granted, ReferencedFunctionalLicense):
                raise LinguisticOntologyV2Error("عضوٌ في الرخص خارج نوعه")
            try:
                candidate = general.candidate(granted.candidate_ref.candidate_id)
            except ValueError:
                unknown.append(granted.license_id)
                continue
            if candidate.kind.value != granted.candidate_ref.kind_name:
                mismatched.append(granted.license_id)
        complaints: list[str] = []
        if unknown:
            complaints.append("رخصٌ لمرشَّحين غيرِ مُسجَّلين في `O_0`: " + "، ".join(unknown))
        if mismatched:
            complaints.append(
                "رخصٌ نوعُ مرشَّحها يخالف نوعَه في `O_0`: " + "، ".join(mismatched)
            )
        if complaints:
            raise LinguisticOntologyV2Error("؛ و".join(complaints))
        return cls(
            ontology_id=ontology_id,
            general_ontology_id=general.ontology_id,
            general_content_id=general.content_id,
            prior_base_ref=general.prior_base_ref,
            licenses=licenses,
        )

    def license(self, license_id: str) -> ReferencedFunctionalLicense:
        """الرخصةُ بمُعرِّفها؛ والغيابُ رفضٌ لا `None` يُقرَأ صمتًا."""

        for granted in self.licenses:
            if granted.license_id == license_id:
                return granted
        raise LinguisticOntologyV2Error(
            f"لا رخصةَ في `O_L²` مُعرِّفُها `{license_id}`؛ والغيابُ رفضٌ لا صمت"
        )

    def licenses_for(
        self, function: LinguisticFunction
    ) -> tuple[ReferencedFunctionalLicense, ...]:
        """الرخصُ الممنوحةُ لوظيفةٍ بعينها؛ والفراغُ فراغٌ لا يُقرَأ منعًا."""

        if not isinstance(function, LinguisticFunction):
            raise LinguisticOntologyV2Error("الوظيفةُ عضوٌ في مفردتها المغلقة")
        return tuple(
            granted
            for granted in self.licenses
            if granted.function_ref.function is function
        )

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى `O_L²` للبصمة."""

        return {
            "ontology_id": self.ontology_id,
            "general_ontology_id": self.general_ontology_id,
            "general_content_id": self.general_content_id,
            "prior_base_ref": self.prior_base_ref.as_canonical_content(),
            "licenses": [
                granted.as_canonical_content()
                for granted in sorted(self.licenses, key=lambda item: item.license_id)
            ],
        }

    @property
    def content_id(self) -> str:
        """بصمةُ `O_L²`؛ وهي غيرُ بصمة `O_L` ولا تحلّ محلَّها."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))


def _refuse_a_free_text_condition_field() -> None:
    """لا حقلَ شرطٍ نصًّا حرًّا في الرخصة؛ وكلُّ شرطٍ مرجعٌ مبصومٌ إلى `PK_0`."""

    for owner_field in fields(ReferencedFunctionalLicense):
        if "condition" not in owner_field.name:
            continue
        annotation = owner_field.type
        name = annotation.__name__ if isinstance(annotation, type) else annotation
        if PriorConditionRef.__name__ not in str(name):  # pragma: no cover - guard
            raise RuntimeError(
                A_LICENSE_IS_FOUNDED_ON_A_STANDING_LICENSED_CONDITION_NOT_ON_PROSE
            )


def _refuse_a_statement_field() -> None:
    """لا حقلَ بيانٍ تفسيريٍّ هنا؛ فالنصُّ الحرُّ أُغلِق في أصل الرخصة نفسه."""

    for owner in (ReferencedFunctionalLicense, LinguisticOntologyV2):
        for owner_field in fields(owner):
            lowered = owner_field.name.lower()
            for marker in ("statement", "note", "prose", "description"):
                if marker in lowered:  # pragma: no cover - guard
                    raise RuntimeError(
                        A_LICENSE_IS_FOUNDED_ON_A_STANDING_LICENSED_CONDITION_NOT_ON_PROSE
                    )


_refuse_a_free_text_condition_field()
_refuse_a_statement_field()
