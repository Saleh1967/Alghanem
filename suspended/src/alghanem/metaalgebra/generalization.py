"""G0.GEN — مانعُ التعميم: إغلاقٌ في نطاقٍ جزئيٍّ ليس إغلاقًا في النطاق كلِّه.

هذه الوحدةُ تحمل بالبناء قانونًا تكرّر خرقُه في هذه الشجرة حتى صار منوالًا لا
حادثة:

    LocalClosure            ⇏ GlobalClosure
    CoverageOnSubdomain     ⇏ UniversalCapacity

أي لا يجوز الانتقالُ من:

    ∀x ∈ D₀,  P(x)

إلى:

    ∀x ∈ D,   P(x)

إلا بواحدٍ من اثنين لا ثالثَ لهما: برهانٍ على أنّ `D₀ = D`، أو قانونِ تعميمٍ
مُسمًّى يُبرَّر به الامتداد. وما عدا ذلك امتدادٌ غيرُ مُرخَّص، يُرفَض عند
الإنشاء ولا يُصحَّح عند القراءة.

**والسندُ يُسمّى ولا يُترَك للصمت.** `GeneralizationWarrant` مفردةٌ مغلقة
بثلاثة أعضاء: مطابقةُ النطاقين، وقانونُ تعميمٍ مُسمًّى، ولا سندَ. والثالثُ
مقبولٌ **بشرط أن تُعلَن الدعوى مقيَّدةً بنطاقها الجزئيّ**؛ فمَن لا سندَ له لا
يُمنَع من التسجيل، يُمنَع من الترقية وحدَها
(`AN_UNWARRANTED_CLAIM_MAY_BE_RECORDED_IN_ITS_SUBDOMAIN`).

**ومطابقةُ النطاقين دعوى لا تُقبَل مرسلة**: تحتاج شاهدًا مُسمًّى يُراجَع، لأنّ
«النطاقان واحد» هي عينُ الخطوة التي تُهرَّب فيها النتيجةُ إذا قيلت بلا دليل
(`DOMAIN_IDENTITY_IS_A_CLAIM_NOT_A_CONVENIENCE`).

**وقانونُ التعميم اسمٌ ونصٌّ لا لفتةٌ نحوَ الاستقراء**: سردُ أمثلةٍ أكثر ليس
قانونَ تعميم، وإغلاقُ مدوّنةٍ منتهيةٍ لا يمتدّ إلى لغةٍ مفتوحة
(`ENUMERATION_IS_NOT_A_GENERALIZATION_LAW`).

**ولا تُصدِر هذه الوحدةُ حكمًا على أيّ دعوى قائمة**: تحمل المفردةَ والرفضَ
البنيويَّ فقط، ولا ولادةَ فيها ولا تجميدَ `E0`، ولا تستورد من `kernel/` حرفًا.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from typing import Final

__all__ = [
    "AN_UNWARRANTED_CLAIM_MAY_BE_RECORDED_IN_ITS_SUBDOMAIN",
    "COVERAGE_ON_SUBDOMAIN_IS_NOT_UNIVERSAL_CAPACITY",
    "DOMAIN_IDENTITY_IS_A_CLAIM_NOT_A_CONVENIENCE",
    "ENUMERATION_IS_NOT_A_GENERALIZATION_LAW",
    "GENERALIZATION_NAMED_RESIDUALS",
    "LOCAL_CLOSURE_IS_NOT_GLOBAL_CLOSURE",
    "DomainIdentityEvidence",
    "GeneralizationLaw",
    "GeneralizationWarrant",
    "MetaAlgebraGeneralizationError",
    "ScopedClaim",
    "ScopedClaimExtension",
]


class MetaAlgebraGeneralizationError(ValueError):
    """رفضٌ عند الإنشاء: امتدادٌ من نطاقٍ جزئيٍّ إلى نطاقٍ أوسعَ بلا سند."""


LOCAL_CLOSURE_IS_NOT_GLOBAL_CLOSURE: Final[str] = (
    "LOCAL_CLOSURE_IS_NOT_GLOBAL_CLOSURE: انغلاقُ دعوى في نطاقٍ جزئيٍّ لا "
    "يجعلها منغلقةً في النطاق كلِّه؛ والامتدادُ خطوةٌ تحتاج سندًا، لا نتيجةٌ "
    "تَلزَم عن الإغلاق الجزئيّ"
)

COVERAGE_ON_SUBDOMAIN_IS_NOT_UNIVERSAL_CAPACITY: Final[str] = (
    "COVERAGE_ON_SUBDOMAIN_IS_NOT_UNIVERSAL_CAPACITY: تغطيةُ نموذجٍ لكلّ ما في "
    "نطاقٍ جزئيٍّ ليست سَعةً كلّية؛ وقياسُ السَعة على ما لم يُقَس هو عينُ الخطوة "
    "التي يمنعها هذا القانون"
)

DOMAIN_IDENTITY_IS_A_CLAIM_NOT_A_CONVENIENCE: Final[str] = (
    "DOMAIN_IDENTITY_IS_A_CLAIM_NOT_A_CONVENIENCE: «`D₀ = D`» دعوى تحتاج "
    "شاهدًا مُسمًّى يُراجَع؛ وقولُها مرسلةً يُهرِّب النتيجةَ في مقدّمةٍ لم تُفحَص"
)

ENUMERATION_IS_NOT_A_GENERALIZATION_LAW: Final[str] = (
    "ENUMERATION_IS_NOT_A_GENERALIZATION_LAW: كثرةُ الأمثلة ليست قانونَ تعميم، "
    "وإغلاقُ مدوّنةٍ منتهيةٍ لا يمتدّ إلى لغةٍ مفتوحة؛ والقانونُ اسمٌ ونصٌّ "
    "يُراجَعان لا لفتةٌ نحوَ الاستقراء"
)

AN_UNWARRANTED_CLAIM_MAY_BE_RECORDED_IN_ITS_SUBDOMAIN: Final[str] = (
    "AN_UNWARRANTED_CLAIM_MAY_BE_RECORDED_IN_ITS_SUBDOMAIN: غيابُ السند يمنع "
    "الترقيةَ لا التسجيل؛ فالدعوى تبقى مقروءةً في نطاقها الجزئيّ كما قِيست، "
    "ويُرفَض امتدادُها وحدَه"
)


class GeneralizationWarrant(Enum):
    """سندُ الامتداد من نطاقٍ جزئيٍّ إلى نطاقٍ أوسع؛ مفردةٌ مغلقةٌ بثلاثة."""

    DOMAIN_IDENTITY_PROVED = "DOMAIN_IDENTITY_PROVED"
    NAMED_GENERALIZATION_LAW = "NAMED_GENERALIZATION_LAW"
    NO_WARRANT = "NO_WARRANT"

    @property
    def licenses_extension(self) -> bool:
        """أيُرخِّص هذا السندُ الامتداد؟ الاستبعادُ مُصرَّحٌ به لا مُستنتَجٌ من صمت."""

        return self is not GeneralizationWarrant.NO_WARRANT


def _require_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise MetaAlgebraGeneralizationError(f"{label} نصٌّ غير فارغ")
    return value


@dataclass(frozen=True, slots=True)
class DomainIdentityEvidence:
    """شاهدُ أنّ النطاقين واحد: موضعُه، ونصُّه، وما يدّعيه بالضبط."""

    subdomain_id: str
    domain_id: str
    citation: str
    argument: str

    def __post_init__(self) -> None:
        _require_text(self.subdomain_id, "اسمُ النطاق الجزئيّ")
        _require_text(self.domain_id, "اسمُ النطاق")
        _require_text(self.citation, "موضعُ الشاهد")
        _require_text(self.argument, "نصُّ الحجّة")


@dataclass(frozen=True, slots=True)
class GeneralizationLaw:
    """قانونُ تعميمٍ مُسمًّى: اسمُه، ونصُّه، والشرطُ الذي يلزم لإعماله."""

    law_id: str
    statement: str
    precondition: str

    def __post_init__(self) -> None:
        _require_text(self.law_id, "اسمُ قانون التعميم")
        _require_text(self.statement, "نصُّ قانون التعميم")
        _require_text(self.precondition, "شرطُ إعمال القانون")


@dataclass(frozen=True, slots=True)
class ScopedClaim:
    """دعوى مقيَّدةٌ بنطاقها المقيس؛ والنطاقُ جزءٌ من الدعوى لا حاشيةٌ بجانبها."""

    claim_id: str
    predicate: str
    measured_domain_id: str

    def __post_init__(self) -> None:
        _require_text(self.claim_id, "اسمُ الدعوى")
        _require_text(self.predicate, "نصُّ المحمول")
        _require_text(self.measured_domain_id, "النطاقُ المقيس")


@dataclass(frozen=True, slots=True)
class ScopedClaimExtension:
    """طلبُ امتدادِ دعوى من نطاقها المقيس إلى نطاقٍ أوسع، وسندُه.

    ويُرفَض عند الإنشاء: امتدادٌ سندُه `NO_WARRANT`، وسندٌ مُعلَنٌ بلا شاهده أو
    بلا قانونه، وشاهدُ مطابقةٍ لا يذكر النطاقين المذكورَين في الطلب نفسِه.
    ولا حقلَ في هذا النوع يُعلِن نجاحًا أو رتبة، فالترخيصُ مُشتَقٌّ من السند لا
    مكتوبٌ بجانبه.
    """

    claim: ScopedClaim
    target_domain_id: str
    warrant: GeneralizationWarrant
    domain_identity_evidence: DomainIdentityEvidence | None
    generalization_law: GeneralizationLaw | None
    reason: str

    def __post_init__(self) -> None:
        if type(self.claim) is not ScopedClaim:
            raise MetaAlgebraGeneralizationError("الامتدادُ يلزمه دعوى مقيَّدةً بنطاقها")
        _require_text(self.target_domain_id, "النطاقُ المقصود")
        _require_text(self.reason, "سببُ الامتداد")
        if not isinstance(self.warrant, GeneralizationWarrant):
            raise MetaAlgebraGeneralizationError("السندُ عضوٌ في مفردته المغلقة")
        if self.target_domain_id == self.claim.measured_domain_id:
            raise MetaAlgebraGeneralizationError(
                "امتدادٌ إلى النطاق المقيس نفسِه ليس امتدادًا؛ والدعوى قائمةٌ فيه "
                "بلا هذا الطلب"
            )
        if self.warrant is GeneralizationWarrant.NO_WARRANT:
            raise MetaAlgebraGeneralizationError(
                f"{LOCAL_CLOSURE_IS_NOT_GLOBAL_CLOSURE}؛ و"
                f"{AN_UNWARRANTED_CLAIM_MAY_BE_RECORDED_IN_ITS_SUBDOMAIN}"
            )
        self._check_domain_identity()
        self._check_generalization_law()

    def _check_domain_identity(self) -> None:
        if self.warrant is GeneralizationWarrant.DOMAIN_IDENTITY_PROVED:
            evidence = self.domain_identity_evidence
            if type(evidence) is not DomainIdentityEvidence:
                raise MetaAlgebraGeneralizationError(
                    DOMAIN_IDENTITY_IS_A_CLAIM_NOT_A_CONVENIENCE
                )
            if (
                evidence.subdomain_id != self.claim.measured_domain_id
                or evidence.domain_id != self.target_domain_id
            ):
                raise MetaAlgebraGeneralizationError(
                    "شاهدُ المطابقة يذكر نطاقين غيرَ نطاقَي هذا الطلب؛ وشاهدُ "
                    "غيرِ المسألة ليس شاهدًا فيها"
                )
            if self.generalization_law is not None:
                raise MetaAlgebraGeneralizationError(
                    "سندٌ واحدٌ يُعلَن لا سندان؛ وجمعُهما يُخفي أيُّهما حمل الامتداد"
                )
        elif self.domain_identity_evidence is not None:
            raise MetaAlgebraGeneralizationError(
                "شاهدُ مطابقةٍ مع سندٍ آخرَ شاهدٌ لا يُقرَأ في هذا الطلب"
            )

    def _check_generalization_law(self) -> None:
        if self.warrant is GeneralizationWarrant.NAMED_GENERALIZATION_LAW:
            if type(self.generalization_law) is not GeneralizationLaw:
                raise MetaAlgebraGeneralizationError(
                    ENUMERATION_IS_NOT_A_GENERALIZATION_LAW
                )
        elif self.generalization_law is not None:
            raise MetaAlgebraGeneralizationError(
                "قانونُ تعميمٍ مع سندٍ آخرَ قانونٌ لا يُقرَأ في هذا الطلب"
            )

    @property
    def is_licensed_extension(self) -> bool:
        """أمُرخَّصٌ هذا الامتداد؟ مُشتَقٌّ من السند لا مكتوبٌ في حقلٍ بجانبه."""

        return self.warrant.licenses_extension


_RESULT_BEARING_FIELD_MARKERS: Final[tuple[str, ...]] = (
    "licensed",
    "granted",
    "approved",
    "verdict",
    "rank",
    "status",
)

for _declaring_type in (
    ScopedClaim,
    ScopedClaimExtension,
):  # pragma: no cover - import guard
    for _field in fields(_declaring_type):
        if any(marker in _field.name for marker in _RESULT_BEARING_FIELD_MARKERS):
            raise RuntimeError(
                "an extension request may not carry its own licensing field"
            )


GENERALIZATION_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "LOCAL_CLOSURE_IS_NOT_GLOBAL_CLOSURE": LOCAL_CLOSURE_IS_NOT_GLOBAL_CLOSURE,
    "COVERAGE_ON_SUBDOMAIN_IS_NOT_UNIVERSAL_CAPACITY": (
        COVERAGE_ON_SUBDOMAIN_IS_NOT_UNIVERSAL_CAPACITY
    ),
    "DOMAIN_IDENTITY_IS_A_CLAIM_NOT_A_CONVENIENCE": (
        DOMAIN_IDENTITY_IS_A_CLAIM_NOT_A_CONVENIENCE
    ),
    "ENUMERATION_IS_NOT_A_GENERALIZATION_LAW": ENUMERATION_IS_NOT_A_GENERALIZATION_LAW,
    "AN_UNWARRANTED_CLAIM_MAY_BE_RECORDED_IN_ITS_SUBDOMAIN": (
        AN_UNWARRANTED_CLAIM_MAY_BE_RECORDED_IN_ITS_SUBDOMAIN
    ),
}
"""ما لا يحسمه هذا المانع، مُسمًّى هنا لا متروكًا ليُفترَض."""
