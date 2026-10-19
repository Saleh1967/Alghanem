"""مختبرُ حامل–حالةٍ كتابيٍّ بالقوانين الثلاثة: يُثبِت نجاحًا محدودًا، أو يكشف
فشلًا، أو يُسجِّل إرجاءً — ولا يُهندَس فيه المُخرَج قبل التشغيل.

**والقوانينُ الثلاثةُ عملياتٌ جزئيةٌ لا صفاتٌ للوقوع المفرد.** تحفظ الهويةَ
وتنظّم ما يجري داخلَ البنية وعند حدودها::

    الابتداء  →  تنظيمُ الدخول إلى البنية
    الوصل     →  تنظيمُ الانتقال عبر الحدّ بين بنيتَين
    الوقف     →  تنظيمُ الإغلاق عند الحدّ الأخير

فلا يُفسَّر الوصلُ تجاورَ رسمَين، ولا الوقفُ نهايةَ سلسلةٍ مكتوبة. ولكلّ تطبيقِ
عمليةٍ صفٌّ كاملُ الحقول: مدخلٌ ومجالٌ وشرطٌ وسببٌ ومانع، وحالةُ دخولٍ وحالةُ
خروج، **ومحلُّ التغيّر**، وثابتٌ محفوظٌ وفرقٌ قادحٌ وأثرٌ ودليلٌ وبقايا. وصفٌّ
بلا محلٍّ للتغيّر أو بلا ثابتٍ محفوظٍ يُرَدّ عند الإنشاء لا يُقبَل ناقصًا.

**والنصُّ مرجعٌ لا دليل.** تُستورَد `THE_THREE_LAWS` من
`ibtida_wasl_waqf_registration` بهويتها ومرتبتها المُودَعتَين، ولا يُنسَخ نصٌّ
ولا تُرفَع رتبة؛ فاستيرادُ قانونٍ لا يرفعه من `مُورَدة_بلا_مصدرٍ_مُسمًّى` إلى
قانونٍ مُثبَت (`THE_THREE_LAWS_ARE_REFERENCED_NOT_PROVEN`).

**والمطلوبُ مفصولٌ عمّا توافرت شواهدُه.** `REQUIRED_LAWS` تُجمَّد قبل التشغيل
وتضمّ الثلاثةَ كاملةً، ومجموعةُ ما توافر له شاهدٌ تُشتَقّ عند التشغيل. وغيابُ
الشاهد لا يُخرِج قانونًا من معيار الاكتمال، بل يُسجَّل `DEFER` **بمانعٍ
مُسمًّى** (`WASL_AND_WAQF_HAVE_NO_WITNESS_IN_THIS_TREE`).

**والحارسُ الأوّل: لا `PASS` على مجالٍ فقير.** صدقُ ``ker T_k ⊆ ker F_k`` على
مجالٍ خالٍ صدقٌ فارغ، فكلُّ دالّةٍ تحتوي نواةَ العدم. فبوّابةُ قدرةِ المجال على
التكذيب تسبق الحكم: مجالٌ خالٍ ⇒ إرجاء، ومجالٌ لا يفرّقه الهدفُ المستقلُّ في
زوجٍ واحدٍ على الأقلّ ⇒ إرجاء، ولا يُحتمَل `PASS` إلّا في مجالٍ ذي فرقٍ قادح،
ويُسجَّل معه عددُ الأزواج القادحة التي اجتازت
(`AN_EMPTY_OR_UNDISCRIMINATING_DOMAIN_YIELDS_DEFER_NOT_PASS`).

**والحارسُ الثاني: جنسٌ وصفةٌ وإسنادٌ في الطبقة السابقة للمقطع وحدَها.** الجنسُ
صنفُ الحامل الكتابيّ، والصفةُ حالتُه المقيسةُ على محاورها المُجمَّدة، والإسنادُ
علاقةُ إلحاق الحالة بالحامل لا غير. ولا يُستورَد إلى هذه الطبقة إسنادٌ نحويٌّ
ولا دلاليٌّ من `minimal_complete_fiber`؛ والفصلُ في النوع لا في التعليق:
`StateAttribution` لا تقبل إلّا حاملًا وصفةً مقيسة
(`GENUS_ATTRIBUTE_AND_ATTRIBUTION_ARE_PRE_SYLLABLE_ONLY`).

**واستقلالُ الهدف بحسب نوع الدعوى لا بمصدرٍ واحدٍ مفروض.** الدعوى الكتابيةُ
هدفُها مقيسٌ من وقوعات المصدر المبصَّم **بآلةٍ منفصلةٍ عن التمثيل المرشَّح**،
والدعوى الصوتيةُ تلزمها شاهدَ أداءٍ مُسمَّى القراءةِ واللهجةِ والسياق،
والدعوى الدلاليةُ تلزمها وسمًا مستقلًّا. ولا يُقبَل هدفٌ منشؤه التمثيلُ نفسُه
ولا المقطّعُ البرمجيُّ في هذه الشجرة
(`THE_IN_TREE_SYLLABIFIER_IS_NOT_A_REFERENCE_FOR_ITS_OWN_RESULTS`).

**والاكتمالُ مشروطٌ بالتغطية.** نجاحُ الابتداء وحدَه مع غياب شاهدَي الوصل
والوقف يُخرِج `DEFER` إجماليًّا لا `PASS`؛ والتجميعُ `FAIL > DEFER > PASS`
بمكوّناتٍ مفصولةٍ لا برقمٍ واحد. و`FAIL` مقيَّدةٌ بدعواها ومجالها، لا تُعمَّم
على كلّ نموذجٍ ممكن (`A_PARTIAL_PASS_DOES_NOT_COMPLETE_THE_CARRIER_STATE`).

**والمخرجاتُ ثلاثةٌ مفصولةٌ في النوع.** حامل–حالةٍ كتابيٌّ **مرشَّح** لا مولود،
وحامل–حالةٍ صوتيٌّ **مؤجَّلٌ بالبناء** لا بالاختيار — إذ لا يُنشأ إلّا بشاهد
أداءٍ مُودَع، ولا شاهدَ في الشجرة — ومقطعٌ **لم تصدر شهادةُ ولادته**. ولا مسارَ
ترقيةٍ بين الثلاثة، ولا تُورَّث سلطةٌ إلى المقطع ولا إلى المبنى النحويّ
(`NO_AUTHORITY_IS_INHERITED_BY_THE_SYLLABLE_OR_THE_SYNTAX`).

**ولا شهادةَ ولادةٍ تصدر من هنا.** إصدارُها مفوَّضٌ إلى الجهة الحاكمة بحدود
المجال والرتبة والبقايا المثبتة (`THIS_LABORATORY_ISSUES_NO_BIRTH_CERTIFICATE`).
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from enum import Enum
from typing import Final

from .carrier_state_observed_fiber import (
    Boundary,
    ObservedFiberTable,
    OccurrenceRow,
    run_observed_fiber_on_the_deposited_fatiha,
)
from .ibtida_wasl_waqf_registration import (
    THE_THREE_LAWS,
    IbtidaReadingTable,
    LawStanding,
    SuppliedLaw,
    read_ibtida_on_the_deposited_fatiha,
)

__all__ = [
    "AN_EMPTY_OR_UNDISCRIMINATING_DOMAIN_YIELDS_DEFER_NOT_PASS",
    "A_PARTIAL_PASS_DOES_NOT_COMPLETE_THE_CARRIER_STATE",
    "A_WEAKER_ALTERNATIVE_MAY_ALSO_PASS_SO_NECESSITY_IS_NOT_ASSUMED",
    "CARRIER_STATE_BIRTH_NAMED_RESIDUALS",
    "GENUS_ATTRIBUTE_AND_ATTRIBUTION_ARE_PRE_SYLLABLE_ONLY",
    "NO_AUTHORITY_IS_INHERITED_BY_THE_SYLLABLE_OR_THE_SYNTAX",
    "NO_PERFORMANCE_WITNESS_IS_DEPOSITED",
    "ORTHOGRAPHIC_TARGET_INSTRUMENT_ID",
    "PRESERVING_THE_ISOLATED_STATE_IS_NOT_COMPLETENESS",
    "REPRESENTATION_INSTRUMENT_ID",
    "REQUIRED_LAWS",
    "REQUIRED_LAW_KEYS",
    "THE_IN_TREE_SYLLABIFIER_IS_NOT_A_REFERENCE_FOR_ITS_OWN_RESULTS",
    "THE_THREE_LAWS_ARE_REFERENCED_NOT_PROVEN",
    "THE_TWO_INSTRUMENTS_READ_THE_SAME_WRITTEN_MARKS",
    "THIS_LABORATORY_ISSUES_NO_BIRTH_CERTIFICATE",
    "WASL_AND_WAQF_HAVE_NO_WITNESS_IN_THIS_TREE",
    "BirthExperimentOutcome",
    "CandidateOrthographicCarrierState",
    "CandidateRepresentation",
    "CarrierStateBirthError",
    "ClaimKind",
    "ContainmentBlocker",
    "ContextOutcome",
    "ContextualLaw",
    "CoverageDecision",
    "DeferredPhoneticCarrierState",
    "IndependentTarget",
    "KernelContainmentDecision",
    "LawApplicationRow",
    "LawRole",
    "MeasuredAttribute",
    "MergeWitness",
    "NecessityDecision",
    "PerformanceWitness",
    "StateAttribution",
    "SyllableWithoutBirthCertificate",
    "WeakerAlternative",
    "WrittenCarrierGenus",
    "assess_coverage",
    "assess_kernel_containment",
    "assess_necessity",
    "build_candidate_representation",
    "deposited_performance_witnesses",
    "measure_ibtida_target",
    "run_birth_experiment_on_the_deposited_fatiha",
]


class CarrierStateBirthError(ValueError):
    """رُوجِع المختبرُ بما لا يقوم به؛ ولا يُحمَل على أقرب حالةٍ مقبولة."""


def _require_non_blank(value: str, name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise CarrierStateBirthError(f"{name} لا يكون فارغًا")


# --- الطبقةُ السابقةُ للمقطع: جنسٌ وصفةٌ وإسنادٌ بحدودها ----------------------


@dataclass(frozen=True, slots=True)
class WrittenCarrierGenus:
    """الجنسُ في هذه الطبقة: صنفُ الحامل الكتابيّ، لا جنسٌ نحويٌّ ولا دلاليّ."""

    carrier: str

    def __post_init__(self) -> None:
        if not isinstance(self.carrier, str) or len(self.carrier) != 1:
            raise CarrierStateBirthError("جنسُ الحامل الكتابيِّ رمزٌ واحد")


@dataclass(frozen=True, slots=True)
class MeasuredAttribute:
    """الصفةُ في هذه الطبقة: حالةُ الحامل المقيسةُ على محاورها المُجمَّدة."""

    state_vector: tuple[tuple[str, str], ...]

    def __post_init__(self) -> None:
        if not isinstance(self.state_vector, tuple) or not self.state_vector:
            raise CarrierStateBirthError("صفةُ الحامل متَّجِهٌ غيرُ فارغٍ على محاوره")
        for pair in self.state_vector:
            if not isinstance(pair, tuple) or len(pair) != 2:
                raise CarrierStateBirthError("كلُّ محورٍ زوجُ اسمٍ وقيمة")


@dataclass(frozen=True, slots=True)
class StateAttribution:
    """الإسنادُ في هذه الطبقة: إلحاقُ الصفةِ المقيسةِ بالحامل، لا غير.

    ولا حقلَ محمولٍ ههنا أصلًا: لا `PredicateRef` ولا وسمٌ دلاليٌّ ولا موقعٌ
    نحويّ. فامتناعُ الإسناد النحويِّ والدلاليِّ **بالبناء** لا بالتعليق.
    """

    genus: WrittenCarrierGenus
    attribute: MeasuredAttribute

    def __post_init__(self) -> None:
        if type(self.genus) is not WrittenCarrierGenus:
            raise CarrierStateBirthError("الإسنادُ لا يقبل إلّا جنسَ حاملٍ كتابيّ")
        if type(self.attribute) is not MeasuredAttribute:
            raise CarrierStateBirthError("الإسنادُ لا يقبل إلّا صفةً مقيسة")

    @property
    def output(self) -> tuple[str, tuple[tuple[str, str], ...]]:
        """مخرَجُ الإسناد مفتاحًا يُقارَن: الجنسُ والصفةُ معًا."""

        return (self.genus.carrier, self.attribute.state_vector)


# --- القوانينُ الثلاثةُ عملياتٍ جزئيةً، مستورَدةً بمرتبتها -------------------


class LawRole(Enum):
    """دورُ القانون في البنية: دخولٌ أو انتقالٌ أو إغلاق، لا صفةُ وقوع."""

    TANZIM_AL_DUKHUL = "تنظيمُ_الدخول"
    TANZIM_AL_INTIQAL = "تنظيمُ_الانتقال"
    TANZIM_AL_IGHLAQ = "تنظيمُ_الإغلاق"


@dataclass(frozen=True, slots=True)
class ContextualLaw:
    """عمليةٌ جزئيةٌ واحدة: قانونُها المُودَع، ودورُها، ومجالُها وشرطُها ومانعُها.

    والقانونُ **مرجعٌ لا دليل**: يُشترَط أن يكون عضوًا بعينه في
    `THE_THREE_LAWS`، وأن تبقى مرتبتُه `مُورَدة_بلا_مصدرٍ_مُسمًّى`، فلا يرفعه
    استيرادُه ههنا رتبةً واحدة.
    """

    law: SuppliedLaw
    role: LawRole
    domain_note: str
    condition_note: str
    cause_note: str
    blocker_note: str

    def __post_init__(self) -> None:
        if not any(self.law is member for member in THE_THREE_LAWS):
            raise CarrierStateBirthError(
                "لا يُبنى قانونٌ سياقيٌّ إلّا على عضوٍ بعينه من `THE_THREE_LAWS`؛ "
                "ونسخُ النصّ يُنشئ قانونًا ثانيًا ينزلق عن الأوّل"
            )
        if self.law.standing is not LawStanding.MUWRADA_BILA_MASDARIN_MUSAMMA:
            raise CarrierStateBirthError(
                "استيرادُ القانون لا يرفع مرتبتَه؛ فمرتبتُه المُودَعةُ تُحفَظ"
            )
        if not isinstance(self.role, LawRole):
            raise CarrierStateBirthError("دورُ القانون عضوٌ في مفردته المغلقة")
        _require_non_blank(self.domain_note, "مجالُ العملية")
        _require_non_blank(self.condition_note, "شرطُ العملية")
        _require_non_blank(self.cause_note, "سببُ العملية")
        _require_non_blank(self.blocker_note, "مانعُ العملية")

    @property
    def key(self) -> str:
        """اسمُ القانون كما أُودِع، لا اسمٌ مُنشأٌ ههنا."""

        return self.law.key


def _law_named(key: str) -> SuppliedLaw:
    for member in THE_THREE_LAWS:
        if member.key == key:
            return member
    raise CarrierStateBirthError("لا قانونَ بهذا الاسم في التسجيل المُودَع")


REQUIRED_LAWS: Final[tuple[ContextualLaw, ...]] = (
    ContextualLaw(
        law=_law_named("الابتداء"),
        role=LawRole.TANZIM_AL_DUKHUL,
        domain_note="مواضعُ الدخول إلى البنية: أوّلُ حاملٍ في كلّ كلمةٍ مكتوبة",
        condition_note="أن تكون للموضع صفةٌ مقيسةٌ وهدفٌ مستقلٌّ مُعلَنٌ قبل التشغيل",
        cause_note="الدخولُ يفتتح البنيةَ فيلزمه تحديدُ حالِ مفتتحها",
        blocker_note=(
            "همزةُ الوصل لا اختبارَ سطحيًّا لها، فموضعُها متعذّرُ القياس لا موافقٌ " "ولا مخالف"
        ),
    ),
    ContextualLaw(
        law=_law_named("الوصل"),
        role=LawRole.TANZIM_AL_INTIQAL,
        domain_note="حدودُ الانتقال بين بنيتَين متجاورتَين في سلسلةٍ واحدة",
        condition_note="أن يُقاس حالُ الحدّ من شاهدٍ مستقلٍّ لا من تجاور الرسمَين",
        cause_note="الانتقالُ يمسّ آخرَ الأولى ومفتتحَ الثانية معًا فيلزمه حدٌّ مقيس",
        blocker_note="لا قراءةَ للوصل في هذه الشجرة، فالمجالُ بلا شاهد",
    ),
    ContextualLaw(
        law=_law_named("الوقف"),
        role=LawRole.TANZIM_AL_IGHLAQ,
        domain_note="حدُّ الإغلاق الأخير في السلسلة المنطوقة لا في السطر المكتوب",
        condition_note="أن يُقاس حالُ الإغلاق من شاهدٍ مستقلٍّ لا من نهاية الرسم",
        cause_note="الإغلاقُ يُنهي البنيةَ فيلزمه تحديدُ حالِ خاتمتها",
        blocker_note="لا قراءةَ للوقف في هذه الشجرة، فالمجالُ بلا شاهد",
    ),
)
"""القوانينُ **المطلوبة**، مُجمَّدةً قبل التشغيل؛ وهي الثلاثةُ كاملةً دائمًا."""


REQUIRED_LAW_KEYS: Final[tuple[str, ...]] = tuple(law.key for law in REQUIRED_LAWS)
"""أسماءُ القوانين المطلوبة بترتيبها؛ ومعيارُ الاكتمال يُقاس عليها لا على ما توافر."""


# --- صفُّ تطبيقِ عمليةٍ واحدة: كاملُ الحقول أو يُرَدّ ------------------------


@dataclass(frozen=True, slots=True)
class LawApplicationRow:
    """تطبيقُ عمليةٍ جزئيةٍ في سياقٍ واحد، بحقولها كلِّها لا ببعضها.

    وصفٌّ بلا محلٍّ للتغيّر أو بلا ثابتٍ محفوظٍ يُرَدّ: العمليةُ التي لا يُعرَف
    أين مسّت ولا ما حفظت ليست عمليةً مُراجَعة.
    """

    law_key: str
    context_id: str
    entry_state: str
    exit_state: str
    site_of_change: str
    preserved_invariant: str
    discriminating_difference: str
    effect_note: str
    evidence_id: str
    residue_note: str

    def __post_init__(self) -> None:
        if self.law_key not in REQUIRED_LAW_KEYS:
            raise CarrierStateBirthError("صفُّ تطبيقٍ لقانونٍ غيرِ مطلوبٍ لا يُقبَل")
        _require_non_blank(self.context_id, "اسمُ السياق")
        _require_non_blank(self.entry_state, "حالةُ الدخول")
        _require_non_blank(self.exit_state, "حالةُ الخروج")
        _require_non_blank(self.site_of_change, "محلُّ التغيّر")
        _require_non_blank(self.preserved_invariant, "الثابتُ المحفوظ")
        _require_non_blank(self.discriminating_difference, "الفرقُ القادح")
        _require_non_blank(self.effect_note, "أثرُ العملية")
        _require_non_blank(self.evidence_id, "دليلُ العملية")
        _require_non_blank(self.residue_note, "بقيّةُ العملية")


# --- الأهدافُ المستقلّة: استقلالٌ بحسب نوع الدعوى ----------------------------


class ClaimKind(Enum):
    """نوعُ الدعوى؛ ولكلّ نوعٍ منشأُ هدفٍ يخصُّه لا منشأٌ واحدٌ مفروضٌ عليها."""

    KITABIYYA = "دعوى_كتابية"
    SAWTIYYA = "دعوى_صوتية"
    DALALIYYA = "دعوى_دلالية"


class TargetProvenance(Enum):
    """منشأُ الهدف المستقلّ؛ وفيه عضوان مرفوضان بالبناء لا بالتوصية."""

    MAQIS_BI_ALA_MUNFASILA = "مقيسٌ_بآلةٍ_منفصلةٍ_عن_التمثيل"
    SHAHID_ADA_MUSAMMA = "شاهدُ_أداءٍ_مُسمَّى_القراءةِ_واللهجةِ_والسياق"
    WASM_MUSTAQILL = "وسمٌ_مستقلٌّ_من_جهةٍ_غيرِ_المُعلِن"
    AL_TAMTHIL_NAFSUH = "التمثيلُ_المرشَّحُ_نفسُه"
    AL_MUQATTI_FI_AL_SHAJARA = "المقطّعُ_البرمجيُّ_في_هذه_الشجرة"


REFUSED_TARGET_PROVENANCES: Final[frozenset[TargetProvenance]] = frozenset(
    {
        TargetProvenance.AL_TAMTHIL_NAFSUH,
        TargetProvenance.AL_MUQATTI_FI_AL_SHAJARA,
    }
)
"""منشآنِ لا يُقبَلان هدفًا: التمثيلُ نفسُه، والمقطّعُ البرمجيُّ على نتائجه."""


ACCEPTED_PROVENANCE_BY_CLAIM_KIND: Final[Mapping[ClaimKind, TargetProvenance]] = {
    ClaimKind.KITABIYYA: TargetProvenance.MAQIS_BI_ALA_MUNFASILA,
    ClaimKind.SAWTIYYA: TargetProvenance.SHAHID_ADA_MUSAMMA,
    ClaimKind.DALALIYYA: TargetProvenance.WASM_MUSTAQILL,
}
"""لكلّ نوعِ دعوى منشؤه؛ فلا يُشترَط الوسمُ المستقلُّ لهدفٍ كتابيٍّ مقيس."""


@dataclass(frozen=True, slots=True)
class IndependentTarget:
    """هدفٌ مستقلٌّ لقانونٍ في مجالٍ، مُعلَنٌ بآلته ونوعِ دعواه قبل التشغيل."""

    law_key: str
    claim_kind: ClaimKind
    provenance: TargetProvenance
    instrument_id: str
    values: tuple[tuple[str, str], ...]

    def __post_init__(self) -> None:
        if self.law_key not in REQUIRED_LAW_KEYS:
            raise CarrierStateBirthError("هدفٌ لقانونٍ غيرِ مطلوبٍ لا يُقبَل")
        if not isinstance(self.claim_kind, ClaimKind):
            raise CarrierStateBirthError("نوعُ الدعوى عضوٌ في مفردته المغلقة")
        if not isinstance(self.provenance, TargetProvenance):
            raise CarrierStateBirthError("منشأُ الهدف عضوٌ في مفردته المغلقة")
        if self.provenance in REFUSED_TARGET_PROVENANCES:
            raise CarrierStateBirthError(
                "لا يُقبَل هدفًا مستقلًّا منشؤه التمثيلُ نفسُه ولا المقطّعُ "
                "البرمجيُّ في هذه الشجرة على نتائجه"
            )
        if ACCEPTED_PROVENANCE_BY_CLAIM_KIND[self.claim_kind] is not self.provenance:
            raise CarrierStateBirthError(
                "منشأُ الهدف لا يوافق نوعَ الدعوى؛ والدعوى الصوتيةُ محجوبةٌ عن "
                "الأدلّة الكتابية"
            )
        _require_non_blank(self.instrument_id, "اسمُ آلة الهدف")
        if not isinstance(self.values, tuple):
            raise CarrierStateBirthError("قيمُ الهدف أزواجٌ مُجمَّدة")
        seen: set[str] = set()
        for pair in self.values:
            if not isinstance(pair, tuple) or len(pair) != 2:
                raise CarrierStateBirthError("كلُّ قيمةِ هدفٍ زوجُ سياقٍ ومحتوى")
            if pair[0] in seen:
                raise CarrierStateBirthError("تكرّر سياقٌ في قيم الهدف")
            seen.add(pair[0])

    @property
    def contexts(self) -> tuple[str, ...]:
        """سياقاتُ الهدف بترتيب إعلانها."""

        return tuple(context for context, _content in self.values)

    def content_for(self, context_id: str) -> str | None:
        """محتوى الهدف في سياقٍ بعينه، أو `None` إن لم يُعلَن له."""

        for context, content in self.values:
            if context == context_id:
                return content
        return None


# --- التمثيلُ المرشَّح وبدائلُه الأضعف ---------------------------------------


class WeakerAlternative(Enum):
    """بدائلُ التمثيل المُعلَنةُ قبل التشغيل؛ والكاملُ عضوٌ فيها لا خارجٌ عنها."""

    AL_JINS_WAHDAH = "الجنسُ_وحدَه"
    AL_SIFA_WAHDAHA = "الصفةُ_وحدَها"
    AL_ISNAD_AL_KAMIL = "الجنسُ_والصفةُ_معًا"


@dataclass(frozen=True, slots=True)
class CandidateRepresentation:
    """التمثيلُ المرشَّح: إسنادٌ لكلّ سياق، بآلته المُسمّاة وبإسقاطه المُعلَن."""

    instrument_id: str
    attributions: tuple[tuple[str, StateAttribution], ...]
    projection: WeakerAlternative = WeakerAlternative.AL_ISNAD_AL_KAMIL

    def __post_init__(self) -> None:
        _require_non_blank(self.instrument_id, "اسمُ آلة التمثيل")
        if not isinstance(self.projection, WeakerAlternative):
            raise CarrierStateBirthError("إسقاطُ التمثيل عضوٌ في مفردته المغلقة")
        if not isinstance(self.attributions, tuple):
            raise CarrierStateBirthError("إسناداتُ التمثيل أزواجٌ مُجمَّدة")
        seen: set[str] = set()
        for pair in self.attributions:
            if not isinstance(pair, tuple) or len(pair) != 2:
                raise CarrierStateBirthError("كلُّ إسنادٍ زوجُ سياقٍ وإسناد")
            if type(pair[1]) is not StateAttribution:
                raise CarrierStateBirthError("التمثيلُ لا يحمل إلّا إسنادَ هذه الطبقة")
            if pair[0] in seen:
                raise CarrierStateBirthError("تكرّر سياقٌ في إسنادات التمثيل")
            seen.add(pair[0])

    @property
    def contexts(self) -> tuple[str, ...]:
        """سياقاتُ التمثيل بترتيب ورودها."""

        return tuple(context for context, _attribution in self.attributions)

    def output_for(self, context_id: str) -> tuple[object, ...] | None:
        """مخرَجُ التمثيل في سياقٍ بعينه بحسب إسقاطه المُعلَن."""

        for context, attribution in self.attributions:
            if context != context_id:
                continue
            if self.projection is WeakerAlternative.AL_JINS_WAHDAH:
                return (attribution.genus.carrier,)
            if self.projection is WeakerAlternative.AL_SIFA_WAHDAHA:
                return (attribution.attribute.state_vector,)
            return attribution.output
        return None

    def projected(self, alternative: WeakerAlternative) -> CandidateRepresentation:
        """التمثيلُ نفسُه بإسقاطٍ أضعف، بلا إعادةِ قياسٍ ولا تغييرِ آلة."""

        return CandidateRepresentation(
            instrument_id=self.instrument_id,
            attributions=self.attributions,
            projection=alternative,
        )


# --- بوّابةُ احتواء النواتين، وقبلَها بوّابةُ قدرةِ المجال على التكذيب --------


class ContextOutcome(Enum):
    """مُخرَجُ اختبارِ قانونٍ في مجاله: اجتيازٌ أو نقضٌ أو إرجاء، لا رابعَ لها."""

    IJTIYAZ = "اجتياز"
    NAQD = "نقض"
    IRJA = "إرجاء"


class ContainmentBlocker(Enum):
    """مانعُ الحكم مُسمًّى؛ فالإرجاءُ لا يكون بلا اسمِ مانعه."""

    LA_WUQUAT_FI_AL_MAJAL = "لا_وقوعاتِ_في_المجال"
    LA_ZAWJ_YUFARRIQUH_AL_HADAF = "لا_زوجَ_يفرّقه_الهدفُ_المستقلّ"
    LA_HADAF_MUSTAQILL = "لا_هدفَ_مستقلًّا_مُعلَنًا"
    LA_SHAHID_LI_HADHA_AL_QANUN = "لا_شاهدَ_لهذا_القانون"


@dataclass(frozen=True, slots=True)
class MergeWitness:
    """شاهدُ نقص: سياقان يفرّقهما الهدفُ ويدمجهما التمثيل."""

    first_context: str
    second_context: str
    first_target: str
    second_target: str

    def __post_init__(self) -> None:
        _require_non_blank(self.first_context, "السياقُ الأوّل")
        _require_non_blank(self.second_context, "السياقُ الثاني")
        if self.first_target == self.second_target:
            raise CarrierStateBirthError(
                "شاهدُ النقص يلزمه هدفان مختلفان؛ وتساويهما ليس فرقًا قادحًا"
            )


@dataclass(frozen=True, slots=True)
class KernelContainmentDecision:
    """حكمُ ``ker T_k ⊆ ker F_k`` في مجالٍ واحد، بسعةِ اجتيازه لا بنعمٍ ولا."""

    law_key: str
    outcome: ContextOutcome
    blocker: ContainmentBlocker | None
    domain_size: int
    discriminating_pairs: int
    passed_pairs: int
    merge_witnesses: tuple[MergeWitness, ...]
    projection: WeakerAlternative

    def __post_init__(self) -> None:
        if self.law_key not in REQUIRED_LAW_KEYS:
            raise CarrierStateBirthError("حكمٌ لقانونٍ غيرِ مطلوبٍ لا يُقبَل")
        if self.domain_size < 0 or self.discriminating_pairs < 0:
            raise CarrierStateBirthError("أعدادُ المجال والأزواج غيرُ سالبة")
        if self.outcome is ContextOutcome.IRJA and self.blocker is None:
            raise CarrierStateBirthError("إرجاءٌ بلا اسمِ مانعٍ ليس إرجاءً مُراجَعًا")
        if self.outcome is not ContextOutcome.IRJA and self.blocker is not None:
            raise CarrierStateBirthError("حكمٌ مع مانعٍ خلطٌ بين التعذّر والحكم")
        if self.outcome is ContextOutcome.IJTIYAZ:
            if self.discriminating_pairs <= 0:
                raise CarrierStateBirthError(
                    "لا اجتيازَ على مجالٍ لا يفرّقه الهدفُ في زوجٍ واحد؛ فصدقُ "
                    "الاحتواء عليه صدقٌ فارغ"
                )
            if self.merge_witnesses:
                raise CarrierStateBirthError("اجتيازٌ مع شاهدِ نقصٍ تناقض")
            if self.passed_pairs != self.discriminating_pairs:
                raise CarrierStateBirthError("سعةُ الاجتياز تُساوي الأزواجَ القادحة")
        if self.outcome is ContextOutcome.NAQD and not self.merge_witnesses:
            raise CarrierStateBirthError("نقضٌ بلا شاهدِ نقصٍ لا يُسجَّل")

    @property
    def scope_note(self) -> str:
        """حدُّ الحكم: دعوى هذا التمثيل في هذا المجال، لا كلُّ نموذجٍ ممكن."""

        return (
            f"حكمُ «{self.law_key}» مقصورٌ على هذا التمثيل وهذا المجال "
            f"({self.domain_size} سياقًا)، ولا يُعمَّم على كلّ نموذجٍ ممكن"
        )


def assess_kernel_containment(
    law: ContextualLaw,
    representation: CandidateRepresentation,
    target: IndependentTarget | None,
) -> KernelContainmentDecision:
    """احكم ``ker T_k ⊆ ker F_k`` بعد بوّابةِ قدرةِ المجال على التكذيب.

    والترتيبُ مقصود: يُسأل أوّلًا أفي المجال ما يمكن أن يُكذِّب الدعوى، فإن لم
    يكن فالمُخرَجُ إرجاءٌ بمانعٍ مُسمًّى. ولا يُقرأ خلوُّ الشاهد المخالف من مجالٍ
    لا يفرّق فيه الهدفُ بين موضعَين تصديقًا للتمثيل.
    """

    if type(law) is not ContextualLaw:
        raise CarrierStateBirthError("الحكمُ يلزمه قانونًا سياقيًّا مبنيًّا")
    if type(representation) is not CandidateRepresentation:
        raise CarrierStateBirthError("الحكمُ يلزمه تمثيلًا مرشَّحًا مبنيًّا")
    if target is None:
        return KernelContainmentDecision(
            law_key=law.key,
            outcome=ContextOutcome.IRJA,
            blocker=ContainmentBlocker.LA_HADAF_MUSTAQILL,
            domain_size=0,
            discriminating_pairs=0,
            passed_pairs=0,
            merge_witnesses=(),
            projection=representation.projection,
        )
    if type(target) is not IndependentTarget:
        raise CarrierStateBirthError("الهدفُ هدفٌ مستقلٌّ مبنيٌّ أو لا شيء")
    if target.law_key != law.key:
        raise CarrierStateBirthError("هدفُ قانونٍ لا يُحكَم به على قانونٍ آخر")
    if target.claim_kind is not ClaimKind.KITABIYYA:
        raise CarrierStateBirthError(
            "هذا المجالُ كتابيٌّ، ولا تُحكَم به دعوى صوتيةٌ ولا دلالية؛ "
            "والدعوى الصوتيةُ محجوبةٌ عن الأدلّة الكتابية"
        )
    if target.instrument_id == representation.instrument_id:
        raise CarrierStateBirthError(
            "آلةُ الهدف هي آلةُ التمثيل نفسُها، فليس الهدفُ مستقلًّا"
        )

    domain = tuple(
        context
        for context in representation.contexts
        if target.content_for(context) is not None
    )
    if not domain:
        return KernelContainmentDecision(
            law_key=law.key,
            outcome=ContextOutcome.IRJA,
            blocker=ContainmentBlocker.LA_WUQUAT_FI_AL_MAJAL,
            domain_size=0,
            discriminating_pairs=0,
            passed_pairs=0,
            merge_witnesses=(),
            projection=representation.projection,
        )

    discriminating = 0
    witnesses: list[MergeWitness] = []
    for index, first in enumerate(domain):
        for second in domain[index + 1 :]:
            first_target = target.content_for(first)
            second_target = target.content_for(second)
            if first_target is None or second_target is None:
                continue
            if first_target == second_target:
                continue
            discriminating += 1
            if representation.output_for(first) == representation.output_for(second):
                witnesses.append(
                    MergeWitness(
                        first_context=first,
                        second_context=second,
                        first_target=first_target,
                        second_target=second_target,
                    )
                )

    if discriminating == 0:
        return KernelContainmentDecision(
            law_key=law.key,
            outcome=ContextOutcome.IRJA,
            blocker=ContainmentBlocker.LA_ZAWJ_YUFARRIQUH_AL_HADAF,
            domain_size=len(domain),
            discriminating_pairs=0,
            passed_pairs=0,
            merge_witnesses=(),
            projection=representation.projection,
        )
    if witnesses:
        return KernelContainmentDecision(
            law_key=law.key,
            outcome=ContextOutcome.NAQD,
            blocker=None,
            domain_size=len(domain),
            discriminating_pairs=discriminating,
            passed_pairs=discriminating - len(witnesses),
            merge_witnesses=tuple(witnesses),
            projection=representation.projection,
        )
    return KernelContainmentDecision(
        law_key=law.key,
        outcome=ContextOutcome.IJTIYAZ,
        blocker=None,
        domain_size=len(domain),
        discriminating_pairs=discriminating,
        passed_pairs=discriminating,
        merge_witnesses=(),
        projection=representation.projection,
    )


# --- ضرورةُ المعلومة: البدائلُ الأضعفُ تُشغَّل ولا تُفترَض -------------------


@dataclass(frozen=True, slots=True)
class NecessityDecision:
    """أضروريّةٌ معلومةُ البديل المحذوف في نطاق هذا القانون؟ بتشغيلٍ لا بظنّ."""

    law_key: str
    alternative: WeakerAlternative
    outcome: ContextOutcome
    information_is_necessary: bool | None

    def __post_init__(self) -> None:
        if self.law_key not in REQUIRED_LAW_KEYS:
            raise CarrierStateBirthError("حكمُ ضرورةٍ لقانونٍ غيرِ مطلوبٍ لا يُقبَل")
        if self.outcome is ContextOutcome.IRJA and (
            self.information_is_necessary is not None
        ):
            raise CarrierStateBirthError(
                "بديلٌ مُرجأٌ لا يقول في الضرورة شيئًا، فلا يُكتَب له حكم"
            )


def assess_necessity(
    law: ContextualLaw,
    representation: CandidateRepresentation,
    target: IndependentTarget | None,
) -> tuple[NecessityDecision, ...]:
    """شغِّل البدائلَ الأضعفَ في نطاق هذا القانون، وسجِّل ما قالته كلُّ واحدة.

    فبديلٌ أضعفُ يجتاز يدلّ على أنّ المحذوف **غيرُ ضروريٍّ في هذا المجال**؛
    وبديلٌ يُنقَض يدلّ على ضرورته فيه. والإرجاءُ لا يقول في الضرورة شيئًا.
    """

    decisions: list[NecessityDecision] = []
    for alternative in (
        WeakerAlternative.AL_JINS_WAHDAH,
        WeakerAlternative.AL_SIFA_WAHDAHA,
    ):
        decision = assess_kernel_containment(
            law, representation.projected(alternative), target
        )
        if decision.outcome is ContextOutcome.IRJA:
            necessary: bool | None = None
        else:
            necessary = decision.outcome is ContextOutcome.NAQD
        decisions.append(
            NecessityDecision(
                law_key=law.key,
                alternative=alternative,
                outcome=decision.outcome,
                information_is_necessary=necessary,
            )
        )
    return tuple(decisions)


# --- الاكتمالُ مشروطٌ بالتغطية ------------------------------------------------


@dataclass(frozen=True, slots=True)
class CoverageDecision:
    """حكمُ الاكتمال مشروطًا بتغطية القوانين المطلوبة كلِّها لا ببعضها."""

    decisions: tuple[KernelContainmentDecision, ...]

    def __post_init__(self) -> None:
        keys = tuple(decision.law_key for decision in self.decisions)
        if sorted(keys) != sorted(REQUIRED_LAW_KEYS):
            raise CarrierStateBirthError(
                "حكمُ التغطية يلزمه حكمًا لكلّ قانونٍ مطلوبٍ مرّةً واحدة؛ "
                "وإخراجُ قانونٍ من المعيار لغيابِ شاهده تضييقٌ للسؤال"
            )

    def decision_for(self, law_key: str) -> KernelContainmentDecision:
        """حكمُ قانونٍ بعينه؛ وقانونٌ غيرُ مطلوبٍ يُرَدّ باسمه."""

        for decision in self.decisions:
            if decision.law_key == law_key:
                return decision
        raise CarrierStateBirthError("لا حكمَ لقانونٍ غيرِ مطلوب")

    @property
    def laws_with_witnesses(self) -> tuple[str, ...]:
        """القوانينُ التي توافرت لها شواهدُ فعلًا، مُشتقّةً لا مكتوبة."""

        return tuple(
            decision.law_key
            for decision in self.decisions
            if decision.outcome is not ContextOutcome.IRJA
        )

    @property
    def failed_laws(self) -> tuple[str, ...]:
        """القوانينُ التي نُقِضت دعوى كفاية التمثيل فيها، بحدود مجالها."""

        return tuple(
            decision.law_key
            for decision in self.decisions
            if decision.outcome is ContextOutcome.NAQD
        )

    @property
    def deferred_laws(self) -> tuple[str, ...]:
        """القوانينُ المُرجأةُ بمانعٍ مُسمًّى؛ وهي داخلةٌ في المعيار لا خارجةٌ عنه."""

        return tuple(
            decision.law_key
            for decision in self.decisions
            if decision.outcome is ContextOutcome.IRJA
        )

    @property
    def overall(self) -> ContextOutcome:
        """التجميعُ بأولويّةِ `نقض > إرجاء > اجتياز`، مستقلًّا عن ترتيب القوانين."""

        if self.failed_laws:
            return ContextOutcome.NAQD
        if self.deferred_laws:
            return ContextOutcome.IRJA
        return ContextOutcome.IJTIYAZ

    @property
    def is_complete(self) -> bool:
        """الاكتمالُ لا يكون إلّا باجتيازٍ إجماليٍّ يغطّي القوانينَ الثلاثة."""

        return self.overall is ContextOutcome.IJTIYAZ


def assess_coverage(
    decisions: Iterable[KernelContainmentDecision],
) -> CoverageDecision:
    """اجمع أحكامَ القوانين المطلوبة في حكمٍ واحدٍ مشروطٍ بالتغطية."""

    return CoverageDecision(decisions=tuple(decisions))


# --- المخرجاتُ الثلاثةُ مفصولةً في النوع -------------------------------------


@dataclass(frozen=True, slots=True)
class PerformanceWitness:
    """شاهدُ أداءٍ مُودَع: قراءتُه ولهجتُه وسياقُه وبصمةُ مصدره، أو لا شاهد."""

    witness_id: str
    reading: str
    dialect: str
    context: str
    source_sha256: str

    def __post_init__(self) -> None:
        _require_non_blank(self.witness_id, "اسمُ شاهد الأداء")
        _require_non_blank(self.reading, "القراءةُ المُسمّاة")
        _require_non_blank(self.dialect, "اللهجةُ المُسمّاة")
        _require_non_blank(self.context, "سياقُ الأداء")
        if len(self.source_sha256) != 64 or any(
            character not in "0123456789abcdef" for character in self.source_sha256
        ):
            raise CarrierStateBirthError("بصمةُ شاهد الأداء بصمةٌ قانونيّةٌ بشكلها")


def deposited_performance_witnesses() -> tuple[PerformanceWitness, ...]:
    """شواهدُ الأداء المُودَعةُ في هذه الشجرة؛ وهي اليومَ لا شيء.

    وخلوُّها هو الذي يجعل المُخرَجَ الصوتيَّ مؤجَّلًا **بالبناء** لا بالاختيار.
    """

    return ()


@dataclass(frozen=True, slots=True)
class CandidateOrthographicCarrierState:
    """المُخرَجُ الأوّل: حامل–حالةٍ كتابيٌّ **مرشَّح**، لا مولودٌ ولا مُشهَّد."""

    source_id: str
    attribution_count: int
    coverage: CoverageDecision
    applications: tuple[LawApplicationRow, ...]
    necessity: tuple[NecessityDecision, ...]

    def __post_init__(self) -> None:
        _require_non_blank(self.source_id, "اسمُ مصدر المرشَّح")
        if self.attribution_count < 0:
            raise CarrierStateBirthError("عددُ الإسنادات غيرُ سالب")
        if type(self.coverage) is not CoverageDecision:
            raise CarrierStateBirthError("المرشَّحُ يلزمه حكمَ تغطيةٍ مبنيًّا")

    @property
    def is_born(self) -> bool:
        """لا ولادةَ ههنا بحالٍ؛ والصفةُ مُشتقّةٌ لا حقلٌ يُكتَب."""

        return False

    @property
    def carries_a_complete_certificate(self) -> bool:
        """لا شهادةَ مكتملةٌ ما بقي قانونٌ من الثلاثة مُرجأً أو منقوضًا."""

        return False


@dataclass(frozen=True, slots=True)
class DeferredPhoneticCarrierState:
    """المُخرَجُ الثاني: حامل–حالةٍ صوتيٌّ لا يُنشَأ إلّا بشاهد أداءٍ مُودَع.

    ولا مدخلَ له من الأدلّة الكتابية: مُنشئُه لا يقبل إلّا `PerformanceWitness`،
    فحجبُ الدعوى الصوتية عن الرسم يقع بالنوع لا بالتوصية.
    """

    witness: PerformanceWitness

    def __post_init__(self) -> None:
        if type(self.witness) is not PerformanceWitness:
            raise CarrierStateBirthError(
                "الدعوى الصوتيةُ لا تُبنى على دليلٍ كتابيّ؛ ولا يُنشأ هذا المُخرَج "
                "إلّا بشاهد أداءٍ مُسمَّى القراءةِ واللهجةِ والسياق"
            )


@dataclass(frozen=True, slots=True)
class SyllableWithoutBirthCertificate:
    """المُخرَجُ الثالث: مقطعٌ لم تصدر شهادةُ ولادته، ولا مسارَ ترقيةٍ إليها."""

    reason: str

    def __post_init__(self) -> None:
        _require_non_blank(self.reason, "سببُ انتفاء شهادة المقطع")

    @property
    def certificate_issued(self) -> bool:
        """لا شهادةَ تصدر من هذه الوحدة بحال."""

        return False


@dataclass(frozen=True, slots=True)
class BirthExperimentOutcome:
    """مُخرَجُ التجربة: ثلاثةٌ مفصولةٌ في النوع، بلا مسارِ ترقيةٍ بينها."""

    orthographic_candidate: CandidateOrthographicCarrierState
    phonetic_carrier_state: DeferredPhoneticCarrierState | None
    phonetic_deferral_reason: str
    syllable: SyllableWithoutBirthCertificate

    def __post_init__(self) -> None:
        if type(self.orthographic_candidate) is not CandidateOrthographicCarrierState:
            raise CarrierStateBirthError("المُخرَجُ الكتابيُّ مرشَّحٌ مبنيٌّ لا سواه")
        if self.phonetic_carrier_state is None:
            _require_non_blank(self.phonetic_deferral_reason, "سببُ التأجيل الصوتيّ")
        if type(self.syllable) is not SyllableWithoutBirthCertificate:
            raise CarrierStateBirthError("المقطعُ مُخرَجٌ بلا شهادةٍ لا سواه")

    @property
    def certificate_issuance_is_delegated(self) -> bool:
        """إصدارُ شهادة الولادة مفوَّضٌ إلى الجهة الحاكمة، لا يقع ههنا."""

        return True

    @property
    def grants_authority_to_the_syllable_or_the_syntax(self) -> bool:
        """لا تُورَّث سلطةٌ إلى المقطع ولا إلى المبنى النحويِّ بنجاح تشغيل."""

        return False


# --- الآلتان المتمايزتان، والتشغيلُ على النصّ المُودَع ------------------------


REPRESENTATION_INSTRUMENT_ID: Final[str] = (
    "alghanem.arabic.carrier_state_observed_fiber.tabulate_observed_fibers"
)
"""آلةُ التمثيل المرشَّح: قياسُ متَّجِه الحالة على المحاور المُجمَّدة."""


ORTHOGRAPHIC_TARGET_INSTRUMENT_ID: Final[str] = (
    "alghanem.arabic.ibtida_wasl_waqf_registration.read_ibtida_positions"
)
"""آلةُ الهدف الكتابيِّ المستقلّ: قراءةُ منزلة أوّلِ حاملٍ بمعيارها المُصرَّح."""


def _context_id(line_index: int, word_index: int) -> str:
    return f"{line_index}:{word_index}"


def build_candidate_representation(
    table: ObservedFiberTable,
) -> CandidateRepresentation:
    """ابنِ التمثيلَ المرشَّحَ على مواضع الدخول: أوّلُ حاملٍ في كلّ كلمة."""

    if type(table) is not ObservedFiberTable:
        raise CarrierStateBirthError("بناءُ التمثيل يلزمه جدولَ ليفٍ مرصود")
    attributions: list[tuple[str, StateAttribution]] = []
    for row in table.rows:
        if not isinstance(row, OccurrenceRow):
            continue
        if row.boundary not in (Boundary.WORD_INITIAL, Boundary.WORD_SOLE):
            continue
        attributions.append(
            (
                _context_id(row.line_index, row.word_index),
                StateAttribution(
                    genus=WrittenCarrierGenus(carrier=row.carrier),
                    attribute=MeasuredAttribute(state_vector=row.state_vector),
                ),
            )
        )
    return CandidateRepresentation(
        instrument_id=REPRESENTATION_INSTRUMENT_ID,
        attributions=tuple(attributions),
    )


def measure_ibtida_target(reading: IbtidaReadingTable) -> IndependentTarget:
    """اقرأ الهدفَ الكتابيَّ المستقلَّ لقانون الابتداء بآلةٍ غيرِ آلة التمثيل."""

    if type(reading) is not IbtidaReadingTable:
        raise CarrierStateBirthError("قياسُ الهدف يلزمه جدولَ قراءةِ ابتداء")
    return IndependentTarget(
        law_key="الابتداء",
        claim_kind=ClaimKind.KITABIYYA,
        provenance=TargetProvenance.MAQIS_BI_ALA_MUNFASILA,
        instrument_id=ORTHOGRAPHIC_TARGET_INSTRUMENT_ID,
        values=tuple(
            (_context_id(row.line_index, row.word_index), row.reading.value)
            for row in reading.rows
        ),
    )


def _ibtida_applications(
    reading: IbtidaReadingTable,
    representation: CandidateRepresentation,
) -> tuple[LawApplicationRow, ...]:
    rows: list[LawApplicationRow] = []
    for row in reading.rows:
        context = _context_id(row.line_index, row.word_index)
        output = representation.output_for(context)
        if output is None:
            continue
        rows.append(
            LawApplicationRow(
                law_key="الابتداء",
                context_id=context,
                entry_state="ما قبل الدخول غيرُ مكتوبٍ في الخطّ",
                exit_state=str(output),
                site_of_change="أوّلُ حاملٍ في الكلمة المكتوبة",
                preserved_invariant="هويةُ الحامل الكتابيِّ لا تتغيّر بالدخول",
                discriminating_difference=row.reading.value,
                effect_note="تحديدُ حالِ مفتتح البنية عند الدخول إليها",
                evidence_id=f"{ORTHOGRAPHIC_TARGET_INSTRUMENT_ID}#{context}",
                residue_note=(
                    "همزةُ الوصل لا اختبارَ سطحيًّا لها، والحالةُ غيرُ المكتوبة "
                    "متعذّرةُ القياس"
                ),
            )
        )
    return tuple(rows)


def run_birth_experiment_on_the_deposited_fatiha() -> BirthExperimentOutcome:
    """شغِّل المختبرَ على النصّ المُودَع: القوانينُ الثلاثةُ كاملةً في المعيار.

    ومدخلٌ عديمُ الوسائط عن قصد، على منوال مداخل هذه الشجرة.
    """

    table = run_observed_fiber_on_the_deposited_fatiha()
    reading = read_ibtida_on_the_deposited_fatiha()
    representation = build_candidate_representation(table)
    ibtida_target = measure_ibtida_target(reading)

    targets: dict[str, IndependentTarget | None] = {
        "الابتداء": ibtida_target,
        "الوصل": None,
        "الوقف": None,
    }
    decisions = tuple(
        assess_kernel_containment(law, representation, targets[law.key])
        for law in REQUIRED_LAWS
    )
    coverage = assess_coverage(decisions)
    necessity = tuple(
        decision
        for law in REQUIRED_LAWS
        for decision in assess_necessity(law, representation, targets[law.key])
    )

    candidate = CandidateOrthographicCarrierState(
        source_id=table.deposit.source_id,
        attribution_count=len(representation.attributions),
        coverage=coverage,
        applications=_ibtida_applications(reading, representation),
        necessity=necessity,
    )
    witnesses = deposited_performance_witnesses()
    phonetic = DeferredPhoneticCarrierState(witness=witnesses[0]) if witnesses else None
    return BirthExperimentOutcome(
        orthographic_candidate=candidate,
        phonetic_carrier_state=phonetic,
        phonetic_deferral_reason=NO_PERFORMANCE_WITNESS_IS_DEPOSITED,
        syllable=SyllableWithoutBirthCertificate(
            reason=THIS_LABORATORY_ISSUES_NO_BIRTH_CERTIFICATE
        ),
    )


# --- ما لا يحسمه هذا المختبر، مُسمًّى ----------------------------------------


THE_THREE_LAWS_ARE_REFERENCED_NOT_PROVEN: Final[str] = (
    "THE_THREE_LAWS_ARE_REFERENCED_NOT_PROVEN: تُستورَد القوانينُ الثلاثةُ "
    "بهويتها ومرتبتها المُودَعتَين، ومرتبتُها `مُورَدة_بلا_مصدرٍ_مُسمًّى`؛ "
    "فاستعمالُها ههنا استعمالُ مرجعٍ لا احتجاجٌ بمُثبَت، ولا يرفعها تشغيلُ "
    "المختبر رتبةً واحدة"
)

THE_TWO_INSTRUMENTS_READ_THE_SAME_WRITTEN_MARKS: Final[str] = (
    "THE_TWO_INSTRUMENTS_READ_THE_SAME_WRITTEN_MARKS: آلةُ الهدف الكتابيِّ "
    "منفصلةٌ عن آلة التمثيل شفرةً ومسارًا، لكنّ الاثنتين تقرآن العلاماتِ "
    "المكتوبةَ نفسَها؛ فالاستقلالُ المُدقَّق استقلالُ آلةٍ لا استقلالُ معلومة، "
    "واحتواءُ النواتين ههنا أقربُ إلى التحليل منه إلى التنبّؤ"
)

AN_EMPTY_OR_UNDISCRIMINATING_DOMAIN_YIELDS_DEFER_NOT_PASS: Final[str] = (
    "AN_EMPTY_OR_UNDISCRIMINATING_DOMAIN_YIELDS_DEFER_NOT_PASS: صدقُ احتواء "
    "النواتين على مجالٍ خالٍ صدقٌ فارغ، وكذلك على مجالٍ لا يفرّق فيه الهدفُ "
    "المستقلُّ بين موضعَين؛ فالمُخرَجُ في الحالَين إرجاءٌ بمانعٍ مُسمًّى، "
    "و`PASS` نحيفٌ يُقرأ بعدد أزواجه القادحة لا بوصفه اجتيازًا واسعًا"
)

WASL_AND_WAQF_HAVE_NO_WITNESS_IN_THIS_TREE: Final[str] = (
    "WASL_AND_WAQF_HAVE_NO_WITNESS_IN_THIS_TREE: لا قراءةَ للوصل ولا للوقف في "
    "هذه الشجرة، ولا هدفَ مستقلًّا لهما؛ فهما مُرجأان بمانعٍ مُسمًّى، وبقاؤهما "
    "في معيار الاكتمال مقصود: إخراجُهما منه لغياب شواهدهما تضييقٌ للسؤال لا حلٌّ له"
)

A_PARTIAL_PASS_DOES_NOT_COMPLETE_THE_CARRIER_STATE: Final[str] = (
    "A_PARTIAL_PASS_DOES_NOT_COMPLETE_THE_CARRIER_STATE: اجتيازُ قانونٍ واحدٍ "
    "في مجاله لا يجعل حامل–الحالة مكتملًا؛ والحكمُ الإجماليُّ مشروطٌ بالتغطية، "
    "والنقضُ مقصورٌ على دعوى هذا التمثيل في مجاله لا يُعمَّم على كلّ نموذجٍ ممكن"
)

THE_IN_TREE_SYLLABIFIER_IS_NOT_A_REFERENCE_FOR_ITS_OWN_RESULTS: Final[str] = (
    "THE_IN_TREE_SYLLABIFIER_IS_NOT_A_REFERENCE_FOR_ITS_OWN_RESULTS: لا يُقبَل "
    "هدفًا مستقلًّا منشؤه المقطّعُ البرمجيُّ في هذه الشجرة، ولا التمثيلُ "
    "المرشَّحُ نفسُه؛ والمنعُ في مُنشئ الهدف لا في التوصية"
)

GENUS_ATTRIBUTE_AND_ATTRIBUTION_ARE_PRE_SYLLABLE_ONLY: Final[str] = (
    "GENUS_ATTRIBUTE_AND_ATTRIBUTION_ARE_PRE_SYLLABLE_ONLY: الجنسُ ههنا صنفُ "
    "الحامل الكتابيّ، والصفةُ حالتُه المقيسة، والإسنادُ إلحاقُ الحالة بالحامل "
    "لا غير؛ ولا يُستورَد إلى هذه الطبقة إسنادٌ نحويٌّ ولا دلاليٌّ من "
    "`minimal_complete_fiber`، والمنعُ بالنوع لا بالتعليق"
)

PRESERVING_THE_ISOLATED_STATE_IS_NOT_COMPLETENESS: Final[str] = (
    "PRESERVING_THE_ISOLATED_STATE_IS_NOT_COMPLETENESS: حفظُ حالة الحامل "
    "معزولةً ليس اكتمالًا؛ الاكتمالُ حفظُ الهوية والفروق اللازمة عند العمليات "
    "السياقية المرخَّصة، مع إثبات الكفاية والضرورة والإغلاق المستقلّ"
)

NO_AUTHORITY_IS_INHERITED_BY_THE_SYLLABLE_OR_THE_SYNTAX: Final[str] = (
    "NO_AUTHORITY_IS_INHERITED_BY_THE_SYLLABLE_OR_THE_SYNTAX: لا تكتسب الوحدةُ "
    "سلطةً نحويةً ولا دلاليةً بنجاح اختبارات الابتداء والوصل والوقف، ولا يُنقَل "
    "إلى المقطع ولا إلى المبنى النحويِّ شيءٌ من سلطة هذا التشغيل"
)

THIS_LABORATORY_ISSUES_NO_BIRTH_CERTIFICATE: Final[str] = (
    "THIS_LABORATORY_ISSUES_NO_BIRTH_CERTIFICATE: لا تصدر من هذه الوحدة شهادةُ "
    "ولادة؛ إصدارُها مفوَّضٌ إلى الجهة الحاكمة بحدود المجال والرتبة والبقايا "
    "المثبتة، ولا تستورد هذه الوحدةُ من `kernel/` شيئًا"
)

A_WEAKER_ALTERNATIVE_MAY_ALSO_PASS_SO_NECESSITY_IS_NOT_ASSUMED: Final[str] = (
    "A_WEAKER_ALTERNATIVE_MAY_ALSO_PASS_SO_NECESSITY_IS_NOT_ASSUMED: اجتيازُ "
    "التمثيل الكامل لا يُثبِت ضرورةَ معلوماته؛ فإن اجتاز بديلٌ أضعفُ المجالَ "
    "نفسَه فالمحذوفُ غيرُ ضروريٍّ فيه، وهذه نتيجةُ تشغيلٍ تُسجَّل لا تُعالَج "
    "بتضييق المجال حتّى يصير التمثيلُ الكاملُ لازمًا"
)

NO_PERFORMANCE_WITNESS_IS_DEPOSITED: Final[str] = (
    "NO_PERFORMANCE_WITNESS_IS_DEPOSITED: لا شاهدَ أداءٍ مُسمَّى القراءةِ "
    "واللهجةِ والسياق مُودَعٌ في هذه الشجرة؛ فالمُخرَجُ الصوتيُّ مؤجَّلٌ "
    "بالبناء لا بالاختيار، إذ لا يُنشَأ مُنشئُه أصلًا بغير شاهد"
)

CARRIER_STATE_BIRTH_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "THE_THREE_LAWS_ARE_REFERENCED_NOT_PROVEN": (
        THE_THREE_LAWS_ARE_REFERENCED_NOT_PROVEN
    ),
    "THE_TWO_INSTRUMENTS_READ_THE_SAME_WRITTEN_MARKS": (
        THE_TWO_INSTRUMENTS_READ_THE_SAME_WRITTEN_MARKS
    ),
    "AN_EMPTY_OR_UNDISCRIMINATING_DOMAIN_YIELDS_DEFER_NOT_PASS": (
        AN_EMPTY_OR_UNDISCRIMINATING_DOMAIN_YIELDS_DEFER_NOT_PASS
    ),
    "WASL_AND_WAQF_HAVE_NO_WITNESS_IN_THIS_TREE": (
        WASL_AND_WAQF_HAVE_NO_WITNESS_IN_THIS_TREE
    ),
    "A_PARTIAL_PASS_DOES_NOT_COMPLETE_THE_CARRIER_STATE": (
        A_PARTIAL_PASS_DOES_NOT_COMPLETE_THE_CARRIER_STATE
    ),
    "THE_IN_TREE_SYLLABIFIER_IS_NOT_A_REFERENCE_FOR_ITS_OWN_RESULTS": (
        THE_IN_TREE_SYLLABIFIER_IS_NOT_A_REFERENCE_FOR_ITS_OWN_RESULTS
    ),
    "GENUS_ATTRIBUTE_AND_ATTRIBUTION_ARE_PRE_SYLLABLE_ONLY": (
        GENUS_ATTRIBUTE_AND_ATTRIBUTION_ARE_PRE_SYLLABLE_ONLY
    ),
    "PRESERVING_THE_ISOLATED_STATE_IS_NOT_COMPLETENESS": (
        PRESERVING_THE_ISOLATED_STATE_IS_NOT_COMPLETENESS
    ),
    "NO_AUTHORITY_IS_INHERITED_BY_THE_SYLLABLE_OR_THE_SYNTAX": (
        NO_AUTHORITY_IS_INHERITED_BY_THE_SYLLABLE_OR_THE_SYNTAX
    ),
    "THIS_LABORATORY_ISSUES_NO_BIRTH_CERTIFICATE": (
        THIS_LABORATORY_ISSUES_NO_BIRTH_CERTIFICATE
    ),
    "A_WEAKER_ALTERNATIVE_MAY_ALSO_PASS_SO_NECESSITY_IS_NOT_ASSUMED": (
        A_WEAKER_ALTERNATIVE_MAY_ALSO_PASS_SO_NECESSITY_IS_NOT_ASSUMED
    ),
    "NO_PERFORMANCE_WITNESS_IS_DEPOSITED": NO_PERFORMANCE_WITNESS_IS_DEPOSITED,
}
"""ما لا يحسمه هذا المختبر، مُسمًّى هنا لا متروكًا ليُفترَض."""
