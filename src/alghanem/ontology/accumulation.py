"""رصيدٌ معرفيٌّ متراكمٌ بإصدارات، فوق سجلّ الوقائع القائم لا بجانبه.

الطلبُ كان: «استكمل النواة القائمة بمعماريّة معرفةٍ متراكمةٍ مستندةٍ إلى
النصوص، لا نسخَ محرِّكٍ موازٍ ولا تعدادًا جديدًا للكيانات». وهذه الوحدةُ
تُغلِق أربعَ فجواتٍ **قِيست في الشفرة** ولا تُعيد بناء ما هو مبنيّ::

    AdmissionLicence != AdoptionLicence
    ClaimStanding    != PropositionStanding
    TypeDifference   != TypeConflict
    Reinstatement    != Truth

**والمبنيُّ يُعاد استعمالُه بلا تعديل.** `FactRegister` يُودِع القضايا
بأدلّتها، ويُعلِّق توابعَ ما أُبطِل، ويُعيد التقييمَ بدليلٍ مستقلّ؛ و
`apply_rule` يقف عند أوّل مانعٍ مُسمًّى ويرفض نتيجةً لا تُسمّي مقدّماتِها
بأعيانها؛ و`IdentityNetwork` يرفض رابطًا لم تُقرأ كلُّ مفاتيح معياره. فلا
تُنسَخ واحدةٌ من هذه ههنا، وإنّما تُستهلَك.

**الفجوةُ الأولى: ترخيصان لا ترخيصٌ واحد.** في النواة القائمة تحمل القاعدةُ
`evidence_ref` واحدًا هو **مصدرُها**، وليس في الشفرة ما يفصل مصدرَ القاعدة عن
**اعتمادها**. فترخيصُ إدخال الحكم (أ) وترخيصُ اعتماد القاعدة (ب) هنا شيئان
مختلفا الشروط: الأوّل يشترط جنسَ دليلٍ يُثبِت واقعةً، والثاني يشترط أصلًا
مُسمًّى — تعميمًا أو نقلًا أو اشتقاقًا — وشاهدًا **يذكر القاعدة بإصدارها في
مضمونه**. فدليلُ الواقعة لا يصلح اعتمادًا لقاعدة، ولا العكس
(`A_RULE_LICENCE_IS_NOT_ITS_SOURCE`).

**والاستيرادُ ليس تعلُّمًا.** الأصلُ `IMPORTED_UNJUSTIFIED` عضوٌ مُصرَّحٌ به في
مفردة الأصول، وحضورُه يجعل القاعدةَ **مسجَّلةً لا معتمدة**: تُحفَظ ولا تُطبَّق.
فمن سمّى تسجيلَ قواعدَ مورَّدةٍ تعلُّمًا نسب إلى المنفِّذ ما لا يفعله
(`IMPORTING_RULES_IS_NOT_LEARNING_THEM`).

**الفجوةُ الثانية: الدعوى ليست القضيّة.** في `FactRegister` لكلّ قضيّةٍ
`evidence_ref` **واحد**، فتعدُّدُ البراهين لا يُمثَّل في القضيّة الواحدة. وقد
يُودَع مضمونٌ واحدٌ قضيّتين بمُعرِّفَين ودليلَين، فيبقى هو مدعومًا بعد إبطال
أحدهما — لكنّ السجلَّ لا يُخرِج هذا الحكم. فههنا **مفتاحُ دعوى** يُجمَع عليه،
وتُقرأ منزلتُه من مجموع أسانيده الحيّة.

**والاستقلالُ يُقاس ولا يُدَّعى.** سندانِ مستقلّان: دليلاهما مختلفا المُعرِّف،
**وليس أحدُهما مشتقًّا يرجع سندُه إلى دليل الآخر**. فإعادةُ حفظ نتيجةٍ مشتقّةٍ
بمُعرِّفٍ جديدٍ لا تُنشئ سندًا ثانيًا، ولا تُصبِح دليلًا على القاعدة التي
أنتجتها (`A_REDEPOSIT_OF_A_DERIVED_RESULT_IS_NOT_AN_INDEPENDENT_SUPPORT`).

**الفجوةُ الثالثة: اختلافُ النوعين ليس تعارضًا.** الإنسانُ والكائنُ الحيُّ
يجتمعان في فردٍ واحدٍ بلا خلل. فلا يُقرأ تعارضٌ من مجرّد تعدُّد الانتماء، ولا
يُقرأ إلّا بـ**شهادة تنافٍ** تُسمّي النوعَين ونطاقَها ودليلَها؛ وخارجَ نطاقها
لا تعمل (`A_DIFFERENCE_OF_TYPE_IS_NOT_A_CONFLICT` ·
`AN_INCOMPATIBILITY_IS_WITNESSED_NOT_INFERRED`).

**الفجوةُ الرابعة: التصحيحُ سجلٌّ لا إحلال.** التصحيحُ يشترط الحكمَين معًا،
ونطاقًا واحدًا، ورتبةَ تسجيلٍ لاحقة، وسببًا، وشاهدَ تصحيح، ورابطَ هويّةٍ حيًّا
عند اختلاف طرفَي الحكم. ولا يُمحى السابق: يُعلَّق ويبقى في السجلّ بتاريخه.
**ووقتُ التسجيل غيرُ وقت تعلُّق القضيّة بالواقع**: الأوّل رتبةٌ في هذا السجلّ،
والثاني نطاقُ القضيّة (`THE_RECORDED_TIME_IS_NOT_THE_TIME_OF_THE_CLAIM`).

**وعودةُ الحكم القديم سياسةٌ تُعلَن.** إذا سقط شرطُ التصحيح فللرصيد سياستان
مُسمّاتان: أن يعود السندُ الأقدم تشغيليًّا، أو أن يبقى معلَّقًا حتّى دليلٍ
جديد. والعودةُ التشغيليّةُ **ليست صدقًا**: هي رجوعُ سجلٍّ إلى حالٍ سابقةٍ لا
حكمٌ على الواقع (`REINSTATEMENT_IS_A_POLICY_NOT_A_TRUTH`).

**وحدُّ هذه الوحدة**: لا تقرأ عربيّةً، ولا تشتقّ مضمونًا من لفظ، ولا تمنح
شهادةَ ١١٦، ولا تُرقّي دليلًا مصنوعًا إلى مشاهدة. وكلُّ ما تُخرِجه حكمٌ عن
**هذا الرصيد** بمُعرِّفاته، لا عن العالم.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest
from .content import Polarity
from .epistemics import Evidence, EvidenceRef, Scope
from .facts import FactRegister, Proposition
from .identity import IdentityNetwork
from .substance import InferenceRule

__all__ = [
    "AN_INCOMPATIBILITY_IS_WITNESSED_NOT_INFERRED",
    "A_DIFFERENCE_OF_TYPE_IS_NOT_A_CONFLICT",
    "A_REDEPOSIT_OF_A_DERIVED_RESULT_IS_NOT_AN_INDEPENDENT_SUPPORT",
    "A_RULE_LICENCE_IS_NOT_ITS_SOURCE",
    "IMPORTING_RULES_IS_NOT_LEARNING_THEM",
    "REINSTATEMENT_IS_A_POLICY_NOT_A_TRUTH",
    "THE_RECORDED_TIME_IS_NOT_THE_TIME_OF_THE_CLAIM",
    "THE_SUSPENSION_IS_CONSERVATIVE_AND_HERE_IS_WHERE_IT_OVERSHOOTS",
    "AccumulationError",
    "AdmissionLicence",
    "AdoptionLicence",
    "ClaimKey",
    "ClaimStanding",
    "ClaimVerdict",
    "Correction",
    "IncompatibilityWitness",
    "KnowledgeStock",
    "ReinstatementPolicy",
    "RuleOrigin",
    "TypeReading",
    "claim_verdict",
    "independent_supports",
    "type_reading",
]


A_RULE_LICENCE_IS_NOT_ITS_SOURCE: Final[str] = (
    "مصدرُ القاعدة شيءٌ واعتمادُها شيءٌ آخر: الأوّل يقول من أين جاءت، والثاني "
    "يأذن بتطبيقها. ودليلُ واقعةٍ لا يصلح اعتمادًا لقاعدة، وشاهدُ اعتمادٍ لا "
    "يُثبِت واقعة."
)

IMPORTING_RULES_IS_NOT_LEARNING_THEM: Final[str] = (
    "قاعدةٌ أُدخِلت بأصلٍ غيرِ مُبرَّرٍ تُسجَّل ولا تُعتمَد؛ وتسميةُ تسجيلِ "
    "قواعدَ مورَّدةٍ «تعلُّمًا» نسبةُ قدرةٍ إلى منفِّذٍ لا يملكها."
)

A_REDEPOSIT_OF_A_DERIVED_RESULT_IS_NOT_AN_INDEPENDENT_SUPPORT: Final[str] = (
    "سندٌ مشتقٌّ ترجع مقدّماتُه إلى دليلِ سندٍ آخرَ ليس مستقلًّا عنه؛ وإعادةُ "
    "حفظِ النتيجة بمُعرِّفٍ جديدٍ لا تُنشئ برهانًا ثانيًا."
)

A_DIFFERENCE_OF_TYPE_IS_NOT_A_CONFLICT: Final[str] = (
    "انتماءُ فردٍ إلى نوعين لا يُقرَأ تعارضًا: الإنسانُ والكائنُ الحيُّ "
    "يجتمعان. والتعارضُ يحتاج شهادةَ تنافٍ مُسمّاةَ الطرفين والنطاق."
)

AN_INCOMPATIBILITY_IS_WITNESSED_NOT_INFERRED: Final[str] = (
    "شهادةُ التنافي تعمل في نطاقها المُعلَن وحدَه؛ ولا تُعمَّم على نطاقٍ آخرَ "
    "بالسهو، ولا تُشتَقّ من اختلاف الأسماء."
)

REINSTATEMENT_IS_A_POLICY_NOT_A_TRUTH: Final[str] = (
    "عودةُ الحكم الأقدم بعد سقوط شرطِ تصحيحه رجوعُ سجلٍّ إلى حالٍ سابقة، لا "
    "حكمٌ بأنّ الأقدمَ صار حقيقة. والسياسةُ تُعلَن باسمها ولا تُفترَض."
)

THE_RECORDED_TIME_IS_NOT_THE_TIME_OF_THE_CLAIM: Final[str] = (
    "رتبةُ التسجيل موضعٌ في هذا الرصيد، ونطاقُ القضيّة زمنُ تعلُّقها بالواقع؛ "
    "وخلطُهما يجعل الأحدثَ تسجيلًا أصدقَ مضمونًا."
)

THE_SUSPENSION_IS_CONSERVATIVE_AND_HERE_IS_WHERE_IT_OVERSHOOTS: Final[str] = (
    "تعليقُ التبعيّات يمشي على **الاشتقاق** لا على المضمون: فنتيجةٌ اشتُقّت "
    "من مقدّمتين تُعلَّق بتصحيح إحداهما، وإن كان البديلُ يحمل مضمونَ "
    "المصحَّحة نفسَه وكانت القاعدةُ تنطلق عليه. والمثالُ المُسمّى هو "
    "`test_a_correction_suspends_a_conclusion_its_replacement_would_relicense`: "
    "ثَمّ تُعلَّق نتيجةٌ كان يُعاد اشتقاقُها. وهذا اختيارٌ مُعلَن: إعادةُ "
    "الاشتقاق **فعلٌ جديدٌ بترخيصه**، لا أثرٌ تلقائيٌّ للتصحيح؛ ولو جرت "
    "تلقائيًّا لصارت نتيجةٌ قائمةً بلا ترخيصِ إدخالٍ يُسمّي مقدّماتِها."
)


class AccumulationError(ValueError):
    """رفضٌ بنيويٌّ في طبقة التراكم؛ لا حملَ على أقرب حالةٍ مقبولة."""


def _require_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise AccumulationError(f"{label} نصٌّ غير فارغ")
    return value


class RuleOrigin(Enum):
    """أصلُ القاعدة؛ مفردةٌ مغلقةٌ فيها عضوٌ غيرُ مُبرَّرٍ مُصرَّحٌ به."""

    GENERALISED_FROM_CASES = "عُمِّمت_من_حالات"
    TRANSMITTED_FROM_A_SOURCE = "نُقِلت_عن_مصدر"
    DERIVED_FROM_ADOPTED_RULES = "اشتُقّت_من_قواعدَ_معتمدة"
    IMPORTED_UNJUSTIFIED = "أُدخِلت_بلا_تبرير"

    @property
    def licenses_application(self) -> bool:
        """أيأذن هذا الأصلُ بالتطبيق؟ خاصّيّةٌ تُشتَقّ لا حقلٌ يُكتَب."""

        return self is not RuleOrigin.IMPORTED_UNJUSTIFIED


class ReinstatementPolicy(Enum):
    """سياسةُ ما بعد سقوط شرط التصحيح؛ تُعلَن ولا تُفترَض."""

    RESTORE_THE_EARLIER_SUPPORT = "يعود_السندُ_الأقدمُ_تشغيليًّا"
    KEEP_SUSPENDED_UNTIL_NEW_EVIDENCE = "يبقى_معلَّقًا_حتّى_دليلٍ_جديد"


class ClaimStanding(Enum):
    """منزلةُ دعوى في هذا الرصيد؛ تُشتَقّ من أسانيدها الحيّة."""

    SUPPORTED_IN_SCOPE = "مدعومةٌ_في_النطاق"
    NEGATED_IN_SCOPE = "منفيّةٌ_في_النطاق"
    CONFLICT = "تعارضٌ_مباشر"
    DEPENDENCY_CONFLICT = "تعارضٌ_في_المقدّمات"
    UNKNOWN = "لا_دعمَ_ولا_نفي"

    @property
    def is_decided(self) -> bool:
        """أحُسِمت الدعوى إيجابًا أو سلبًا؟"""

        return self in (
            ClaimStanding.SUPPORTED_IN_SCOPE,
            ClaimStanding.NEGATED_IN_SCOPE,
        )


@dataclass(frozen=True, slots=True)
class AdmissionLicence:
    """ترخيصُ (أ): إدخالُ حكمٍ إلى الرصيد بنطاقه ورتبته وتبعيّاته.

    والرتبةُ هنا **رتبةُ تسجيلٍ** في هذا الرصيد، لا زمنُ تعلُّق القضيّة
    بالواقع؛ ذاك نطاقُ القضيّة نفسِها.
    """

    proposition_id: str
    scope: Scope
    evidence_ref: EvidenceRef
    recorded_order: int
    depends_on_proposition_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _require_text(self.proposition_id, "مُعرِّفُ الحكم المُرخَّص")
        if not isinstance(self.scope, Scope):
            raise AccumulationError("نطاقُ الترخيص نطاقٌ قائم")
        if not isinstance(self.evidence_ref, EvidenceRef):
            raise AccumulationError("دليلُ الترخيص إشارةٌ مبصومة")
        if not isinstance(self.recorded_order, int) or self.recorded_order < 0:
            raise AccumulationError("رتبةُ التسجيل عددٌ صحيحٌ غيرُ سالب")
        if not isinstance(self.depends_on_proposition_ids, tuple):
            raise AccumulationError("تبعيّاتُ الترخيص صفٌّ مجمَّد")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الترخيص للبصمة."""

        return {
            "proposition_id": self.proposition_id,
            "scope": self.scope.as_canonical_content(),
            "evidence_ref": self.evidence_ref.as_canonical_content(),
            "recorded_order": self.recorded_order,
            "depends_on": list(self.depends_on_proposition_ids),
        }


@dataclass(frozen=True, slots=True)
class AdoptionLicence:
    """ترخيصُ (ب): اعتمادُ قاعدةٍ بأصلها وشروطها ودليل تعميمها أو نقلها.

    وشاهدُ الاعتماد **يذكر القاعدةَ بإصدارها في مضمونه**؛ فشاهدٌ لا يُسمّي ما
    يأذن به إذنٌ بلا موضوع.
    """

    rule_versioned_id: str
    origin: RuleOrigin
    condition_note: str
    evidence_ref: EvidenceRef
    revoked: bool = False

    def __post_init__(self) -> None:
        _require_text(self.rule_versioned_id, "مُعرِّفُ القاعدة بإصدارها")
        if "@" not in self.rule_versioned_id:
            raise AccumulationError(
                "الاعتمادُ يقع على قاعدةٍ **بإصدارها**؛ ومُعرِّفٌ بلا إصدارٍ "
                "يُبقي الإذنَ ساريًا على نصٍّ تغيّر"
            )
        if not isinstance(self.origin, RuleOrigin):
            raise AccumulationError("أصلُ القاعدة عضوٌ في مفردته المغلقة")
        _require_text(self.condition_note, "شرطُ انطباق القاعدة المعتمدة")
        if not isinstance(self.evidence_ref, EvidenceRef):
            raise AccumulationError("شاهدُ الاعتماد إشارةٌ مبصومة")
        if not isinstance(self.revoked, bool):
            raise AccumulationError("نقضُ الاعتماد قيمةٌ ثنائيّة")

    @property
    def is_live(self) -> bool:
        """أما زال الإذنُ قائمًا وأصلُه يأذن بالتطبيق؟"""

        return not self.revoked and self.origin.licenses_application

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الاعتماد للبصمة."""

        return {
            "rule_versioned_id": self.rule_versioned_id,
            "origin": self.origin.value,
            "condition_note": self.condition_note,
            "evidence_ref": self.evidence_ref.as_canonical_content(),
            "revoked": self.revoked,
        }


@dataclass(frozen=True, slots=True)
class IncompatibilityWitness:
    """شهادةُ تنافي نوعين في نطاقٍ مُعلَن؛ وخارجَه لا تعمل."""

    witness_id: str
    type_a_id: str
    type_b_id: str
    scope: Scope
    evidence_ref: EvidenceRef

    def __post_init__(self) -> None:
        _require_text(self.witness_id, "مُعرِّفُ شهادة التنافي")
        _require_text(self.type_a_id, "طرفُ التنافي الأوّل")
        _require_text(self.type_b_id, "طرفُ التنافي الثاني")
        if self.type_a_id == self.type_b_id:
            raise AccumulationError("لا تنافيَ بين النوع ونفسِه")
        if not isinstance(self.scope, Scope):
            raise AccumulationError("نطاقُ شهادة التنافي نطاقٌ قائم")
        if not isinstance(self.evidence_ref, EvidenceRef):
            raise AccumulationError("دليلُ شهادة التنافي إشارةٌ مبصومة")

    def covers(self, first: str, second: str, scope: Scope) -> bool:
        """أتشمل هذه الشهادةُ هذين النوعَين في هذا النطاق؟"""

        pair = {self.type_a_id, self.type_b_id}
        return pair == {first, second} and self.scope.covers(scope)

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الشهادة للبصمة."""

        return {
            "witness_id": self.witness_id,
            "types": sorted((self.type_a_id, self.type_b_id)),
            "scope": self.scope.as_canonical_content(),
            "evidence_ref": self.evidence_ref.as_canonical_content(),
        }


@dataclass(frozen=True, slots=True)
class Correction:
    """قرارُ تصحيحٍ مُسجَّل: الحكمُ القديم والجديد، ونطاقٌ واحد، وسببٌ وشاهد."""

    correction_id: str
    corrected_proposition_id: str
    replacement_proposition_id: str
    scope: Scope
    recorded_order: int
    reason: str
    evidence_ref: EvidenceRef
    identity_link_id: str | None = None
    policy: ReinstatementPolicy = ReinstatementPolicy.KEEP_SUSPENDED_UNTIL_NEW_EVIDENCE

    def __post_init__(self) -> None:
        _require_text(self.correction_id, "مُعرِّفُ التصحيح")
        _require_text(self.corrected_proposition_id, "مُعرِّفُ الحكم المُصحَّح")
        _require_text(self.replacement_proposition_id, "مُعرِّفُ الحكم البديل")
        if self.corrected_proposition_id == self.replacement_proposition_id:
            raise AccumulationError("تصحيحٌ يُحيل الحكمَ على نفسِه ليس تصحيحًا")
        if not isinstance(self.scope, Scope):
            raise AccumulationError("نطاقُ التصحيح نطاقٌ قائم")
        if not isinstance(self.recorded_order, int) or self.recorded_order < 0:
            raise AccumulationError("رتبةُ تسجيل التصحيح عددٌ صحيحٌ غيرُ سالب")
        _require_text(self.reason, "سببُ التصحيح")
        if not isinstance(self.evidence_ref, EvidenceRef):
            raise AccumulationError("شاهدُ التصحيح إشارةٌ مبصومة")
        if self.identity_link_id is not None:
            _require_text(self.identity_link_id, "رابطُ الهويّة المُحتَجُّ به")
        if not isinstance(self.policy, ReinstatementPolicy):
            raise AccumulationError("سياسةُ العودة عضوٌ في مفردتها المغلقة")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى التصحيح للبصمة."""

        return {
            "correction_id": self.correction_id,
            "corrected": self.corrected_proposition_id,
            "replacement": self.replacement_proposition_id,
            "scope": self.scope.as_canonical_content(),
            "recorded_order": self.recorded_order,
            "reason": self.reason,
            "evidence_ref": self.evidence_ref.as_canonical_content(),
            "identity_link_id": self.identity_link_id,
            "policy": self.policy.value,
        }


@dataclass(frozen=True, slots=True)
class ClaimKey:
    """مفتاحُ دعوى: أطرافُها وقطبيّتُها ونطاقُها، بلا مُعرِّفِ قضيّةٍ ولا دليل.

    فالدعوى الواحدةُ قد تحملها قضيّتان بمُعرِّفَين ودليلَين، وهذا المفتاحُ هو
    ما يجمعهما.
    """

    subject_id: str
    predicate_id: str
    value: str | None
    polarity: Polarity
    scope: Scope

    def __post_init__(self) -> None:
        _require_text(self.subject_id, "موضوعُ الدعوى")
        _require_text(self.predicate_id, "محمولُ الدعوى")
        if self.value is not None:
            _require_text(self.value, "قيمةُ محمول الدعوى إن ذُكرت")
        if not isinstance(self.polarity, Polarity):
            raise AccumulationError("قطبيّةُ الدعوى عضوٌ في مفردتها المغلقة")
        if not isinstance(self.scope, Scope):
            raise AccumulationError("نطاقُ الدعوى نطاقٌ قائم")

    @property
    def negated(self) -> ClaimKey:
        """الدعوى نفسُها بقطبيّةٍ معكوسة؛ تُشتَقّ ولا تُكتَب."""

        flipped = (
            Polarity.NEGATED
            if self.polarity is Polarity.AFFIRMED
            else Polarity.AFFIRMED
        )
        return replace(self, polarity=flipped)

    def matches(self, proposition: Proposition) -> bool:
        """أتحمل هذه القضيّةُ هذه الدعوى بعينها؟"""

        return (
            proposition.subject_id == self.subject_id
            and proposition.predicate_id == self.predicate_id
            and proposition.value == self.value
            and proposition.polarity is self.polarity
            and proposition.scope == self.scope
        )

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى المفتاح للبصمة."""

        return {
            "subject_id": self.subject_id,
            "predicate_id": self.predicate_id,
            "value": self.value,
            "polarity": self.polarity.value,
            "scope": self.scope.as_canonical_content(),
        }


@dataclass(frozen=True, slots=True)
class ClaimVerdict:
    """حكمٌ على دعوى: منزلتُها، وأسانيدُها الحيّة، وأسانيدُ نقيضها."""

    claim: ClaimKey
    standing: ClaimStanding
    supporting_proposition_ids: tuple[str, ...]
    negating_proposition_ids: tuple[str, ...]
    independent_support_count: int

    @property
    def survives_one_retraction(self) -> bool:
        """أتبقى مدعومةً لو سقط أحدُ أسانيدها؟ خاصّيّةٌ تُشتَقّ لا حقلٌ يُكتَب."""

        return self.independent_support_count >= 2

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الحكم للبصمة."""

        return {
            "claim": self.claim.as_canonical_content(),
            "standing": self.standing.value,
            "supporting": list(self.supporting_proposition_ids),
            "negating": list(self.negating_proposition_ids),
            "independent_support_count": self.independent_support_count,
        }


def _evidence_roots(register: FactRegister, proposition_id: str) -> frozenset[str]:
    """أدلّةُ أصلِ قضيّةٍ: دليلُها إن كانت مباشرة، وأدلّةُ مقدّماتها إن اشتُقّت.

    وبهذا يُقاس الاستقلالُ ولا يُدَّعى: سندانِ يرجعان إلى دليلٍ واحدٍ سندٌ واحد.
    """

    item = register.proposition_of(proposition_id)
    if not item.is_derived:
        return frozenset({item.evidence_ref.evidence_id})
    roots: set[str] = set()
    for premise_id in item.derived_from_proposition_ids:
        roots |= _evidence_roots(register, premise_id)
    return frozenset(roots)


def independent_supports(
    register: FactRegister, proposition_ids: tuple[str, ...]
) -> tuple[tuple[str, ...], ...]:
    """اقسِم الأسانيدَ طوائفَ مستقلّة؛ وما تقاطعت أصولُه طائفةٌ واحدة.

    المدخل: سجلٌّ، ومُعرِّفاتُ قضايا حيّةٍ تحمل الدعوى نفسَها.
    الشرط: كلُّ مُعرِّفٍ قائمٌ في السجلّ.
    المخرج: صفوفٌ من المُعرِّفات، كلُّ صفٍّ أصولُه متقاطعةٌ مع نفسه لا مع غيره.
    حدُّها: لا تحكم على صدق السند، بل على تقاطع أصوله.
    """

    groups: list[tuple[set[str], list[str]]] = []
    for proposition_id in proposition_ids:
        roots = set(_evidence_roots(register, proposition_id))
        merged: list[tuple[set[str], list[str]]] = []
        members = [proposition_id]
        for existing_roots, existing_members in groups:
            if existing_roots & roots:
                roots |= existing_roots
                members = [*existing_members, *members]
            else:
                merged.append((existing_roots, existing_members))
        merged.append((roots, members))
        groups = merged
    return tuple(tuple(members) for _, members in groups)


def claim_verdict(register: FactRegister, claim: ClaimKey) -> ClaimVerdict:
    """احكم على دعوى من أسانيدها الحيّة في السجلّ، لا من قضيّةٍ بعينها.

    المدخل: سجلُّ وقائع، ومفتاحُ دعوى.
    الشرط: لا شرطَ على السجلّ؛ وغيابُ السند يُقرَأ جهلًا لا نفيًا.
    المخرج: منزلةٌ، وأسانيدُ الدعوى، وأسانيدُ نقيضها، وعددُ الطوائف المستقلّة.
    حدُّها: المعلَّقُ لا يُحسَب سندًا، والسكوتُ ليس نفيًا.
    """

    if not isinstance(register, FactRegister):
        raise AccumulationError("الحكمُ يُقرأ من سجلٍّ قائم")
    if not isinstance(claim, ClaimKey):
        raise AccumulationError("الدعوى مفتاحٌ قائمٌ لا نصٌّ حرّ")
    opposite = claim.negated
    supporting = tuple(
        item.proposition_id
        for item in register.active_propositions
        if claim.matches(item)
    )
    negating = tuple(
        item.proposition_id
        for item in register.active_propositions
        if opposite.matches(item)
    )
    families = independent_supports(register, supporting)
    if supporting and negating:
        standing = ClaimStanding.CONFLICT
    elif supporting:
        standing = ClaimStanding.SUPPORTED_IN_SCOPE
    elif negating:
        standing = ClaimStanding.NEGATED_IN_SCOPE
    else:
        suspended_dependents = any(
            claim.matches(item) and item.suspended and item.is_derived
            for item in register.propositions
        )
        standing = (
            ClaimStanding.DEPENDENCY_CONFLICT
            if suspended_dependents
            else ClaimStanding.UNKNOWN
        )
    return ClaimVerdict(
        claim=claim,
        standing=standing,
        supporting_proposition_ids=supporting,
        negating_proposition_ids=negating,
        independent_support_count=len(families),
    )


@dataclass(frozen=True, slots=True)
class TypeReading:
    """قراءةُ انتماءِ فردٍ إلى أنواعٍ في نطاق: ما اجتمع، وما تنافى بشهادة."""

    individual_id: str
    scope: Scope
    type_ids: tuple[str, ...]
    conflicting_pairs: tuple[tuple[str, str], ...]
    witness_ids: tuple[str, ...]

    @property
    def is_conflicted(self) -> bool:
        """أفي القراءة تعارضٌ مشهودٌ عليه؟ خاصّيّةٌ تُشتَقّ لا حقلٌ يُكتَب."""

        return bool(self.conflicting_pairs)

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى القراءة للبصمة."""

        return {
            "individual_id": self.individual_id,
            "scope": self.scope.as_canonical_content(),
            "type_ids": list(self.type_ids),
            "conflicting_pairs": [list(pair) for pair in self.conflicting_pairs],
            "witness_ids": list(self.witness_ids),
        }


def type_reading(
    register: FactRegister,
    witnesses: tuple[IncompatibilityWitness, ...],
    individual_id: str,
    scope: Scope,
) -> TypeReading:
    """اقرأ انتماءَ فردٍ في نطاق؛ ولا تُسمِّ اجتماعَ نوعين تعارضًا بلا شهادة.

    المدخل: سجلٌّ، وشهاداتُ تنافٍ، ومُعرِّفُ فرد، ونطاق.
    الشرط: لا شرط؛ وغيابُ الشهادة يُقرَأ اجتماعًا مقبولًا لا تعارضًا.
    المخرج: الأنواعُ المثبتةُ في النطاق، والأزواجُ المتنافيةُ بشهادةٍ مُسمّاة.
    حدُّها: لا تُثبِت نوعًا ولا تنفيه، وإنّما تقرأ ما أُودِع.
    """

    from .facts import PropositionForm

    types = tuple(
        sorted(
            {
                item.predicate_id
                for item in register.active_propositions
                if item.subject_id == individual_id
                and item.form is PropositionForm.TYPE_MEMBERSHIP
                and item.polarity is Polarity.AFFIRMED
                and item.scope == scope
            }
        )
    )
    pairs: list[tuple[str, str]] = []
    seen: list[str] = []
    for index, first in enumerate(types):
        for second in types[index + 1 :]:
            for witness in witnesses:
                if witness.covers(first, second, scope):
                    pairs.append((first, second))
                    if witness.witness_id not in seen:
                        seen.append(witness.witness_id)
                    break
    return TypeReading(
        individual_id=individual_id,
        scope=scope,
        type_ids=types,
        conflicting_pairs=tuple(pairs),
        witness_ids=tuple(seen),
    )


def _suspend_with_dependents(
    register: FactRegister, proposition_id: str
) -> FactRegister:
    """علِّق حكمًا وما اشتُقّ منه، ولا تمسّ دليلَه ولا قضيّةً أخرى تحمله.

    المدخل: سجلٌّ، ومُعرِّفُ حكم.
    الشرط: الحكمُ قائمٌ في السجلّ.
    المخرج: سجلٌّ فيه الحكمُ معلَّقٌ وما تبعه معلَّق.
    حدُّها: التعليقُ **محفوظٌ لا ممحوّ**، وهو محدودٌ بالتبعيّات المتأثّرة؛
        فقضيّةٌ تشارك الدليلَ نفسَه ولا تشتقّ من هذا الحكم تبقى قائمة. وهو مع
        ذلك **محافظٌ بقدرٍ مُسمًّى**، وموضعُ تجاوزه مُعلَنٌ ومُمتحَنٌ في
        `THE_SUSPENSION_IS_CONSERVATIVE_AND_HERE_IS_WHERE_IT_OVERSHOOTS`.
    """

    items = list(register.propositions)
    touched = {proposition_id}
    for index, item in enumerate(items):
        if item.proposition_id == proposition_id and not item.suspended:
            items[index] = replace(item, suspended=True)
    changed = True
    while changed:
        changed = False
        for index, item in enumerate(items):
            if item.suspended:
                continue
            if touched & set(item.derived_from_proposition_ids):
                items[index] = replace(item, suspended=True)
                touched.add(item.proposition_id)
                changed = True
    return replace(register, propositions=tuple(items))


@dataclass(frozen=True, slots=True)
class KnowledgeStock:
    """رصيدُ `K_t`: سجلُّ الوقائع، وشبكةُ الهويّة، والقواعدُ وتراخيصُها.

    وهو **منفصلٌ عن شروط التأسيس** `PK_0`: تلك لا تُراجَع بهذا السجلّ ولا
    تُودَع فيه، وهذا ينمو ويُراجَع ويحمل إصدارَه.
    """

    stock_id: str
    version: int
    register: FactRegister
    identity: IdentityNetwork
    rules: tuple[InferenceRule, ...] = ()
    admissions: tuple[AdmissionLicence, ...] = ()
    adoptions: tuple[AdoptionLicence, ...] = ()
    incompatibilities: tuple[IncompatibilityWitness, ...] = ()
    corrections: tuple[Correction, ...] = ()

    def __post_init__(self) -> None:
        _require_text(self.stock_id, "مُعرِّفُ الرصيد")
        if not isinstance(self.version, int) or self.version < 0:
            raise AccumulationError("إصدارُ الرصيد عددٌ صحيحٌ غيرُ سالب")
        if not isinstance(self.register, FactRegister):
            raise AccumulationError("سجلُّ الوقائع سجلٌّ قائم")
        if not isinstance(self.identity, IdentityNetwork):
            raise AccumulationError("شبكةُ الهويّة شبكةٌ قائمة")

    # ----- قراءةٌ -----

    def rule_of(self, versioned_id: str) -> InferenceRule:
        """هاتِ قاعدةً بإصدارها، أو ارفض باسمها."""

        for rule in self.rules:
            if rule.versioned_id == versioned_id:
                return rule
        raise AccumulationError(f"لا قاعدةَ بهذا الإصدار في الرصيد: `{versioned_id}`")

    def adoption_of(self, versioned_id: str) -> AdoptionLicence:
        """هاتِ اعتمادَ قاعدةٍ بإصدارها، أو ارفض باسمها."""

        for licence in self.adoptions:
            if licence.rule_versioned_id == versioned_id:
                return licence
        raise AccumulationError(f"لا اعتمادَ لهذه القاعدة في الرصيد: `{versioned_id}`")

    def is_adopted(self, versioned_id: str) -> bool:
        """أمعتمدةٌ هذه القاعدةُ الآن؟ يُقرَأ من الاعتماد لا من حضور القاعدة."""

        try:
            return self.adoption_of(versioned_id).is_live
        except AccumulationError:
            return False

    def verdict_for(self, claim: ClaimKey) -> ClaimVerdict:
        """احكم على دعوى من هذا الرصيد."""

        return claim_verdict(self.register, claim)

    def types_of(self, individual_id: str, scope: Scope) -> TypeReading:
        """اقرأ انتماءَ فردٍ بشهادات التنافي المُودَعة في هذا الرصيد."""

        return type_reading(self.register, self.incompatibilities, individual_id, scope)

    def corrections_of(self, proposition_id: str) -> tuple[Correction, ...]:
        """تاريخُ تصحيحِ حكمٍ بعينه، مرتّبًا برتبة التسجيل."""

        return tuple(
            sorted(
                (
                    item
                    for item in self.corrections
                    if item.corrected_proposition_id == proposition_id
                ),
                key=lambda item: item.recorded_order,
            )
        )

    # ----- كتابةٌ؛ وكلُّ عمليّةٍ تُخرِج رصيدًا جديدًا بإصدارٍ أعلى -----

    def _next(self, **changes: object) -> KnowledgeStock:
        return replace(self, version=self.version + 1, **changes)  # type: ignore[arg-type]

    def admit(
        self, proposition: Proposition, licence: AdmissionLicence
    ) -> KnowledgeStock:
        """أدخِل حكمًا بترخيصِ (أ): دليلٌ يُثبِت، ونطاقٌ مطابق، وتبعيّاتٌ مُسمّاة.

        المدخل: قضيّةٌ، وترخيصُ إدخالٍ يُسمّيها.
        الشرط: الترخيصُ يُسمّي القضيّةَ بعينها، ونطاقُه نطاقُها، ودليلُه دليلُها.
        المخرج: رصيدٌ جديدٌ بإصدارٍ أعلى فيه القضيّةُ وترخيصُها.
        حدُّها: لا تُرقّي جنسَ الدليل، ولا تُثبِت مضمونًا لم يُودَع.
        """

        if not isinstance(licence, AdmissionLicence):
            raise AccumulationError("الإدخالُ بترخيصٍ قائمٍ لا باسمٍ حرّ")
        if licence.proposition_id != proposition.proposition_id:
            raise AccumulationError("ترخيصُ إدخالٍ يُسمّي حكمًا غيرَ المُدخَل إذنٌ بلا موضوع")
        if licence.scope != proposition.scope:
            raise AccumulationError("نطاقُ الترخيص نطاقُ الحكم نفسُه، لا نطاقٌ أوسعُ منه")
        if licence.evidence_ref != proposition.evidence_ref:
            raise AccumulationError(A_RULE_LICENCE_IS_NOT_ITS_SOURCE)
        if tuple(licence.depends_on_proposition_ids) != tuple(
            proposition.derived_from_proposition_ids
        ):
            raise AccumulationError("تبعيّاتُ الترخيص مقدّماتُ الحكم بأعيانها")
        return self._next(
            register=self.register.with_proposition(proposition),
            admissions=(*self.admissions, licence),
        )

    def adopt_rule(
        self, rule: InferenceRule, licence: AdoptionLicence, evidence: Evidence
    ) -> KnowledgeStock:
        """اعتمِد قاعدةً بترخيصِ (ب): أصلٌ مُسمًّى، وشاهدٌ يذكرها بإصدارها.

        المدخل: قاعدةٌ، وترخيصُ اعتمادٍ، وشاهدُه.
        الشرط: الشاهدُ يُطابِق إشارةَ الترخيص، ويذكر القاعدةَ بإصدارها في
            مضمونه، وجنسُه ليس جنسَ واقعةٍ مباشرة.
        المخرج: رصيدٌ فيه القاعدةُ واعتمادُها، وإصدارٌ أعلى.
        حدُّها: الأصلُ `IMPORTED_UNJUSTIFIED` يُسجَّل ولا يُعتمَد.
        """

        if not isinstance(rule, InferenceRule):
            raise AccumulationError("المعتمَدُ قاعدةٌ قائمة")
        if not isinstance(licence, AdoptionLicence):
            raise AccumulationError("الاعتمادُ بترخيصٍ قائم")
        if licence.rule_versioned_id != rule.versioned_id:
            raise AccumulationError("اعتمادٌ يُسمّي إصدارًا غيرَ المعتمَد إذنٌ بلا موضوع")
        if not licence.evidence_ref.matches(evidence):
            raise AccumulationError("شاهدُ الاعتماد لا يُطابِق إشارتَه مُعرِّفًا وبصمة")
        if rule.versioned_id not in evidence.statement:
            raise AccumulationError(
                A_RULE_LICENCE_IS_NOT_ITS_SOURCE
                + f"؛ ومضمونُ الشاهد لا يذكر `{rule.versioned_id}`"
            )
        known = any(
            one.evidence_id == evidence.evidence_id for one in self.register.evidence
        )
        store = self.register if known else self.register.with_evidence(evidence)
        return self._next(
            register=store,
            rules=(*self.rules, rule),
            adoptions=(*self.adoptions, licence),
        )

    def revoke_adoption(self, versioned_id: str) -> KnowledgeStock:
        """انقُض اعتمادَ قاعدةٍ: تُعلَّق تطبيقاتُها، ويبقى السندُ المستقلّ.

        المدخل: مُعرِّفُ قاعدةٍ بإصدارها.
        الشرط: لها اعتمادٌ قائم.
        المخرج: رصيدٌ فيه الاعتمادُ منقوضٌ والمشتقُّ بها معلَّق.
        حدُّها: لا تمحو القاعدةَ ولا تاريخَها، ولا تمسّ قضيّةً لم تُشتَقّ بها.
        """

        licence = self.adoption_of(versioned_id)
        if licence.revoked:
            raise AccumulationError("اعتمادٌ منقوضٌ لا يُنقَض مرّتين")
        updated = tuple(
            replace(item, revoked=True)
            if item.rule_versioned_id == versioned_id
            else item
            for item in self.adoptions
        )
        suspended: set[str] = set()
        propositions = list(self.register.propositions)
        for index, item in enumerate(propositions):
            if item.derived_by_rule == versioned_id and not item.suspended:
                propositions[index] = replace(item, suspended=True)
                suspended.add(item.proposition_id)
        changed = True
        while changed:
            changed = False
            for index, item in enumerate(propositions):
                if item.suspended:
                    continue
                if suspended & set(item.derived_from_proposition_ids):
                    propositions[index] = replace(item, suspended=True)
                    suspended.add(item.proposition_id)
                    changed = True
        return self._next(
            register=replace(self.register, propositions=tuple(propositions)),
            adoptions=updated,
        )

    def apply_adopted_rule(
        self,
        versioned_id: str,
        premise_proposition_ids: tuple[str, ...],
        conclusion: Proposition,
        licence: AdmissionLicence,
        active_blocker_ids: tuple[str, ...] = (),
    ) -> tuple[KnowledgeStock, str | None]:
        """طبِّق قاعدةً معتمدة، وافحص انطباقَها **عند هذا الاستعمال**.

        المدخل: إصدارُ قاعدة، ومقدّماتٌ، ونتيجةٌ، وترخيصُ إدخالها، وموانعُ قائمة.
        الشرط: الاعتمادُ حيّ، والمقدّماتُ غيرُ معلَّقة، ولا مانعَ قائم.
        المخرج: رصيدٌ بعد التطبيق، واسمُ المانع إن لم تنطلق القاعدة.
        حدُّها: حضورُ القاعدة في الرصيد ليس إذنًا؛ الإذنُ اعتمادُها الحيّ.
        """

        from .operations import apply_rule

        rule = self.rule_of(versioned_id)
        licence_of_rule = self.adoption_of(versioned_id)
        if not licence_of_rule.is_live:
            blocked = (
                IMPORTING_RULES_IS_NOT_LEARNING_THEM
                if not licence_of_rule.origin.licenses_application
                else f"اعتمادٌ منقوض: `{versioned_id}`"
            )
            return self, blocked
        outcome = apply_rule(
            rule,
            premise_proposition_ids,
            conclusion,
            self.register,
            active_blocker_ids,
        )
        if not outcome.fired:
            return self, outcome.blocked_by
        return (
            self._next(
                register=outcome.register,
                admissions=(*self.admissions, licence),
            ),
            None,
        )

    def with_evidence(self, evidence: Evidence) -> KnowledgeStock:
        """أودِع دليلًا في السجلّ؛ والإيداعُ ليس حكمًا ولا ترخيصًا."""

        return self._next(register=self.register.with_evidence(evidence))

    def with_identity(self, network: IdentityNetwork) -> KnowledgeStock:
        """استبدِل شبكةَ الهويّة بعد عمليّةٍ من عمليّاتها القائمة."""

        if not isinstance(network, IdentityNetwork):
            raise AccumulationError("شبكةُ الهويّة شبكةٌ قائمة")
        return self._next(identity=network)

    def retract_evidence(self, evidence_id: str) -> KnowledgeStock:
        """أبطِل دليلًا بإحالة العمليّة إلى السجلّ القائم؛ ولا تُعاد كتابتُها."""

        return self._next(register=self.register.retract(evidence_id))

    def correct(
        self,
        correction: Correction,
        replacement: Proposition,
        licence: AdmissionLicence,
    ) -> KnowledgeStock:
        """صحِّح حكمًا: يُعلَّق القديمُ ويبقى، ويُودَع البديلُ بترخيصه.

        المدخل: قرارُ تصحيحٍ، والحكمُ البديل، وترخيصُ إدخاله.
        الشرط: الحكمُ القديمُ قائمٌ غيرُ معلَّق، ونطاقُ التصحيح نطاقُه ونطاقُ
            البديل، ورتبةُ التسجيل لاحقةٌ لترخيص القديم، وعند اختلاف طرفَي
            الحكم يلزم رابطُ هويّةٍ **حيّ** في شبكة هذا الرصيد.
        المخرج: رصيدٌ فيه القديمُ معلَّقًا بتاريخه، والبديلُ مودَعًا.
        حدُّها: لا يُمحى القديم، ولا يتقدّم الأحدثُ بمجرّد حداثته.
        """

        if not isinstance(correction, Correction):
            raise AccumulationError("التصحيحُ قرارٌ قائمٌ لا نصٌّ حرّ")
        corrected = self.register.proposition_of(correction.corrected_proposition_id)
        if corrected.suspended:
            raise AccumulationError("لا تصحيحَ لحكمٍ معلَّقٍ أصلًا؛ والتعليقُ ليس تصحيحًا")
        if correction.replacement_proposition_id != replacement.proposition_id:
            raise AccumulationError("قرارُ التصحيح يُسمّي بديلًا غيرَ المُودَع")
        if not (correction.scope == corrected.scope == replacement.scope):
            raise AccumulationError(
                "التصحيحُ في نطاقٍ واحد؛ وحكمٌ في نطاقٍ آخرَ ليس تصحيحًا لهذا"
            )
        earlier = [
            one.recorded_order
            for one in self.admissions
            if one.proposition_id == corrected.proposition_id
        ]
        if earlier and correction.recorded_order <= max(earlier):
            raise AccumulationError(
                THE_RECORDED_TIME_IS_NOT_THE_TIME_OF_THE_CLAIM
                + "؛ ورتبةُ التصحيح لاحقةٌ لرتبةِ ما يُصحِّحه"
            )
        if corrected.subject_id != replacement.subject_id:
            if correction.identity_link_id is None:
                raise AccumulationError(
                    "تصحيحٌ يُبدِّل طرفَ الحكم بلا رابطِ هويّةٍ محتَجٍّ به نقلُ "
                    "حكمٍ من فردٍ إلى آخر"
                )
            link = self.identity.link_of(correction.identity_link_id)
            if not link.is_live:
                raise AccumulationError("رابطُ الهويّة المحتَجُّ به منقوض؛ فلا ينقل حكمًا")
            if {corrected.subject_id, replacement.subject_id} != set(link.endpoints()):
                raise AccumulationError("رابطُ الهويّة لا يصل طرفَي هذا التصحيح")
        register = _suspend_with_dependents(self.register, corrected.proposition_id)
        deposited = replace(self, register=register).admit(replacement, licence)
        return replace(deposited, corrections=(*self.corrections, correction))

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الرصيد للبصمة؛ والإصدارُ جزءٌ منه."""

        return {
            "stock_id": self.stock_id,
            "version": self.version,
            "register": self.register.as_canonical_content(),
            "identity": self.identity.as_canonical_content(),
            "rules": [rule.as_canonical_content() for rule in self.rules],
            "admissions": [one.as_canonical_content() for one in self.admissions],
            "adoptions": [one.as_canonical_content() for one in self.adoptions],
            "incompatibilities": [
                one.as_canonical_content() for one in self.incompatibilities
            ],
            "corrections": [one.as_canonical_content() for one in self.corrections],
        }

    @property
    def content_id(self) -> str:
        """بصمةُ مضمون الرصيد كلِّه."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))
