"""مواصفةُ طبقة الشاهد المعجميّ `G0.LEX-0`: مفرداتُها وحدودُها، بلا رقمٍ ولا ملفّ.

**اسمُ هذه الوحدة «مواصفة» لا «تسجيلٌ سابق»** وهذا فرقٌ في الدعوى لا في اللفظ:
بايتاتُ `maqayis_by_root_csv_999.csv` قُرئت في هذه الشجرة واشتُقّت منها أعدادٌ
قبل اليوم (`maqayis_root_table_deposit`، `maqayis_witness_census`،
`maqayis_qac_root_overlap_census`). فالمُجمَّدُ هنا سابقٌ على **قياس `G0.LEX-0`
الجديد** (`SpecificationFrozenBeforeNewLEX0Measurement`)، ولا يُدَّعى أنّه سابقٌ
على أيّ تعرّضٍ للمقاييس (`NoRetroactivePreregistrationOfMaqayis`)؛ ودعوى التسجيل
المسبق بأثرٍ رجعيٍّ تُبطِل معنى التسجيل المسبق كلَّه.

`PROVEN_VOCABULARY_IS_NOT_PROVEN_ASSIGNMENT`: المفرداتُ المبرهَنةُ في هذه الشجرة
— `DalalaKind` و`MadlulSection` و`LafzMadlulRelation` — تُستورَد **فضاءاتِ قيمٍ
مرخَّصةً مغلقة**، ولا تُنسَخ ولا يُبنى لها نظيرٌ ثانٍ. وحملُ مُرشَّحٍ عضوًا منها
يعني أنّ تصنيفَه — إن ثبت — لا يخرج عن المفردة المبرهَنة، **لا أنّ وقوعَه ثبت**.
فسلطةُ المفردة (`VocabularyAuthority`) وسلطةُ تصنيف الوقوع
(`OccurrenceAssignmentAuthority`) سلطتان متمايزتان، والخطأُ يقع في الثانية بلا
أن يمسَّ الأولى.

`CONDITION_IS_NOT_MUJIB`: الشرطُ لا يُنتج النتيجة. والصيغةُ المقبولة رباعيّة:

    Output = Trigger + Condition + Gate + Evidence

ولا يُقبَل `Condition ⇒ Output`. وفي الدلالة: الموجِبُ إطلاقُ اللفظِ بعد قيام
الدلالة الأصليّة، واللزومُ شرطٌ (`LazimIsConditionNotMujib`)، وكذلك كونُ المعنى
جزءًا من معنًى (`PartOfMeaningIsConditionNotGenerativeAuthority`). وهذان فرعان
من قانونٍ أعمَّ من اللغة: `NecessaryRelationIsNotGenerativeAuthority` — وجودُ
`A ⇒ B` في بنيةٍ معرفيّةٍ لا يمنح النظامَ حقَّ إنتاج `B`، بل يلزم الحدثُ الذي
فعّل العلاقة. ونطاقُ هذا القانون مُصرَّحٌ في `GENERAL_TRANSITION_LAW_SCOPE`:
إعلانٌ عامٌّ في الدستور، وتنفيذٌ في `G0.LEX-0` وحدها، ولا دعوى إثباتٍ عالميّ
(`GeneralDeclaration != GlobalRuntimeProof`).

`RELATION_STATE_IS_NOT_GENERATION_HISTORY`: المترادفُ والمشتركُ والمنقولُ
والحقيقةُ والمجاز **حالاتٌ في علاقة الدالّ بالمدلول**، لا طرقَ توليدِ لفظ.
فمفردةُ `LexicalGenerationPath` لا تحمل واحدًا منها، ومفردةُ العلاقة
(`LafzMadlulRelation`) لا تحمل حدثًا تاريخيًّا.

`CORE_OUTPUT_IS_NOT_AUDIT_RECORD`: سقفُ نواتج النواة خمسةَ عشرَ عضوًا بأعيانها
في `LexicalCoreOutput`، وسجلُّ الاتّفاق الصرفيّ خارجَه في `LexicalAuditArtifact`
لأنّ اتّفاقَ مصدرين أو اختلافَهما لا يغيّر هويّةَ مُرشَّح.

وهذه الوحدة **لا تفتح ملفًّا ولا تُخرِج عددًا**، وحارسٌ في آخرها يرفض حقلًا
يحمل عددًا أو حكمًا. وهي تسجيلٌ لا سلطة: لا ولادة، ولا إفادة، ولا معنًى نهائيّ،
ولا `License`، ولا `E0`، ولا استيراد من `kernel/`.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from typing import Any, Final

from .root_orthography_bridge import (
    HAMZA_TO_BARE_ALIF_RULE,
    HAMZA_TO_CARRIED_ALIF_RULE,
)

__all__ = [
    "AMBIGUITY_IS_RECORDED_NOT_RESOLVED_NOTE",
    "A_LEXICON_IS_A_WITNESS_NOT_AN_AUTHORITY_NOTE",
    "A_MATCH_IS_NOT_A_MEANING_NOTE",
    "AXES_ARE_INDEPENDENT_IN_AUTHORITY_NOT_IN_DATA_NOTE",
    "CONDITION_IS_NOT_MUJIB_NOTE",
    "CORE_OUTPUT_IS_NOT_AUDIT_RECORD_NOTE",
    "COVERAGE_IS_NOT_DISCRIMINATION_NOTE",
    "DERIVED_FORM_DOES_NOT_AUTHORIZE_DERIVED_MEANING_NOTE",
    "EMPTY_IS_NOT_ABSENT_NOTE",
    "EXACT_FORM_IS_PRESERVED_UNDER_EVERY_NORMALIZED_BRANCH_NOTE",
    "FOREIGN_ORIGIN_IS_NOT_CURRENT_ARABIC_IDENTITY_NOTE",
    "GENERAL_TRANSITION_LAW_SCOPE",
    "REFERENCE_IS_NOT_ISSUANCE_NOTE",
    "LAZIM_IS_CONDITION_NOT_MUJIB_NOTE",
    "LEX0_IS_NOT_A_GATE_NOTE",
    "MAJAZ_REQUIRES_LICENSED_RELATION_NOTE",
    "NECESSARY_RELATION_IS_NOT_GENERATIVE_AUTHORITY_NOTE",
    "NORMALIZATION_BRANCH_RULE_NAMES",
    "NORMALIZATION_IS_NOT_IDENTITY_NOTE",
    "NOT_COMPARABLE_IS_NOT_FAILURE_NOTE",
    "NO_PATH_IS_NOT_THE_DEFAULT_PATH_NOTE",
    "NO_RETROACTIVE_PREREGISTRATION_OF_MAQAYIS_NOTE",
    "ORIGINAL_HAQIQAH_IS_NOT_URFI_HAQIQAH_NOTE",
    "PARTICLE_EVIDENCE_IS_RELATIONAL_NOTE",
    "PART_OF_MEANING_IS_CONDITION_NOT_GENERATIVE_AUTHORITY_NOTE",
    "PROVEN_VOCABULARY_IS_NOT_PROVEN_ASSIGNMENT_NOTE",
    "QUOTED_DEFINITION_IS_NOT_DERIVED_SIGNIFIED_NOTE",
    "RELATION_STATE_IS_NOT_GENERATION_HISTORY_NOTE",
    "REPORTED_MORPHOLOGY_IS_NOT_DERIVED_MORPHOLOGY_NOTE",
    "ROOT_EVIDENCE_IS_NOT_SURFACE_MEANING_NOTE",
    "SIGNIFIED_CANDIDATE_IS_DEFERRED_NOTE",
    "SPECIFICATION_FROZEN_BEFORE_NEW_LEX0_MEASUREMENT_NOTE",
    "WADH_IS_NOT_INFERRED_FROM_FORM_NOTE",
    "CandidateCore",
    "CandidateGateState",
    "GeneralLawScope",
    "LexicalAuditArtifact",
    "LexicalCoreOutput",
    "LexicalEvidenceSpecificationError",
    "NormalizationBranch",
    "refuse_numeric_or_verdict_fields",
]


class LexicalEvidenceSpecificationError(ValueError):
    """رفضٌ صريحٌ في مواصفة الطبقة؛ لا يُحمَل المدخلُ على أقرب حالةٍ مقبولة."""


SPECIFICATION_FROZEN_BEFORE_NEW_LEX0_MEASUREMENT_NOTE: Final[str] = (
    "SpecificationFrozenBeforeNewLEX0Measurement: المُجمَّد هنا سابقٌ على قياس "
    "`G0.LEX-0` الجديد وحده، لا على أيّ تعرّضٍ لمادّةٍ سبق قياسُها"
)

NO_RETROACTIVE_PREREGISTRATION_OF_MAQAYIS_NOTE: Final[str] = (
    "NoRetroactivePreregistrationOfMaqayis: بايتاتُ «مقاييس اللغة» قُرئت في هذه "
    "الشجرة واشتُقّت منها أعدادٌ قبل اليوم، فوصفُ هذه الوحدة تسجيلًا سابقًا "
    "عليها تسجيلٌ بأثرٍ رجعيّ، وهو مرفوضٌ بنصّه لا مسكوتٌ عنه"
)

PROVEN_VOCABULARY_IS_NOT_PROVEN_ASSIGNMENT_NOTE: Final[str] = (
    "ProvenVocabularyIsNotProvenAssignment: المفردةُ المبرهَنةُ فضاءُ قيمٍ "
    "مرخَّصٌ مغلق، وحملُ مُرشَّحٍ عضوًا منها لا يجعل وقوعَه مبرهَنًا؛ فسلطةُ "
    "المفردة غيرُ سلطةِ تصنيف الوقوع، والخطأُ يقع في التصنيف لا في المفردة"
)

CONDITION_IS_NOT_MUJIB_NOTE: Final[str] = (
    "ConditionIsNotMujib: الشرطُ لا يُنتج النتيجة؛ والصيغةُ المقبولة "
    "`Output = Trigger + Condition + Gate + Evidence`، ولا يُقبَل "
    "`Condition ⇒ Output` ولا يحلُّ حقلُ الشرط محلَّ حقل الموجِب"
)

NECESSARY_RELATION_IS_NOT_GENERATIVE_AUTHORITY_NOTE: Final[str] = (
    "NecessaryRelationIsNotGenerativeAuthority: وجودُ `A ⇒ B` في بنيةٍ معرفيّةٍ "
    "لا يمنح النظامَ حقَّ إنتاج `B`؛ بل يلزم الحدثُ الذي فعّل العلاقة. وهو "
    "قانونُ انتقالٍ عامٌّ مُعلَنٌ في الدستور، مُنفَّذٌ في `G0.LEX-0` وحدها"
)

LAZIM_IS_CONDITION_NOT_MUJIB_NOTE: Final[str] = (
    "LazimIsConditionNotMujib: «اللزومُ شرطٌ وليس بموجِب»؛ فالموجِبُ إطلاقُ "
    "اللفظ بعد قيام الدلالة الأصليّة المُرخَّصة، واللازمُ الذهنيُّ شرطُ "
    "تفعيلٍ. و`MentalLazim(M,l) ⇒ IltizamCandidate` مرفوضٌ بالبناء"
)

PART_OF_MEANING_IS_CONDITION_NOT_GENERATIVE_AUTHORITY_NOTE: Final[str] = (
    "PartOfMeaningIsConditionNotGenerativeAuthority: كونُ `p` جزءًا من `M` شرطٌ "
    "لا موجِب؛ ولو كان موجِبًا لصار كلُّ تحليلٍ مفهوميٍّ دلالةً لغويّة. "
    "و`PartOf(M,p) ⇒ Tadammun(L,p)` مرفوضٌ بالبناء"
)

A_MATCH_IS_NOT_A_MEANING_NOTE: Final[str] = (
    "AMatchIsNotAMeaning: مطابقةُ مدخلٍ معجميٍّ ليست إثباتَ دلالةٍ للوقوع"
)

A_LEXICON_IS_A_WITNESS_NOT_AN_AUTHORITY_NOTE: Final[str] = (
    "ALexiconIsAWitnessNotAnAuthority: المعجمُ شاهدُ نقلٍ لا حَكَم، ولا يُقدَّم "
    "معجمٌ على معجمٍ بهذه الطبقة"
)

ROOT_EVIDENCE_IS_NOT_SURFACE_MEANING_NOTE: Final[str] = (
    "RootEvidenceIsNotSurfaceMeaning: شاهدُ الجذر ومحاورُه المنقولةُ لا تُقرأ "
    "معنًى لوقوعٍ سطحيٍّ بعينه"
)

QUOTED_DEFINITION_IS_NOT_DERIVED_SIGNIFIED_NOTE: Final[str] = (
    "QuotedDefinitionIsNotDerivedSignified: نصُّ المعجم منقولٌ بموضعه، ونقلُه "
    "ليس اشتقاقًا لمدلول"
)

AMBIGUITY_IS_RECORDED_NOT_RESOLVED_NOTE: Final[str] = (
    "AmbiguityIsRecordedNotResolved: تعدُّدُ المُرشَّحات يُسجَّل بأعيانه، ولا "
    "يُختار منه واحدٌ صامتًا"
)

COVERAGE_IS_NOT_DISCRIMINATION_NOTE: Final[str] = (
    "CoverageIsNotDiscrimination: نسبةُ ما بلغ شاهدًا معجميًّا تغطيةٌ مقيسة، "
    "ولا تُقرأ تميّزًا بنيويًّا؛ فالمحوران منفصلان بلا دمج"
)

EMPTY_IS_NOT_ABSENT_NOTE: Final[str] = (
    "EmptyIsNotAbsent: خلوُّ مدخلٍ من مادّةٍ ليس نفيًا لوجودها في العربية"
)

NORMALIZATION_IS_NOT_IDENTITY_NOTE: Final[str] = (
    "NormalizationIsNotIdentity: الصورةُ المُطبَّعةُ ليست الصورةَ الخام، ولا "
    "تُقرأ رسمًا في معجم؛ والتطبيعُ قاعدةٌ تُسَنّ لا خاصّيّةٌ تُقرأ"
)

EXACT_FORM_IS_PRESERVED_UNDER_EVERY_NORMALIZED_BRANCH_NOTE: Final[str] = (
    "ExactFormIsPreservedUnderEveryNormalizedBranch: الصورةُ الخامُّ محفوظةٌ "
    "في كلّ فرعٍ من فروع التطبيع، ولا فرعَ يُسقِطها"
)

REPORTED_MORPHOLOGY_IS_NOT_DERIVED_MORPHOLOGY_NOTE: Final[str] = (
    "ReportedMorphologyIsNotDerivedMorphology: الجذرُ المُبلَّغُ عنه في مصدرٍ "
    "خارجيٍّ شاهدٌ محجوبٌ عن التوليد، ولا يصير جذرًا اشتقّه الجبر؛ وهي حالةٌ "
    "خاصّةٌ من `NecessaryRelationIsNotGenerativeAuthority`"
)

AXES_ARE_INDEPENDENT_IN_AUTHORITY_NOT_IN_DATA_NOTE: Final[str] = (
    "AxesAreIndependentInAuthorityNotInData: المحاورُ الثلاثةُ إسقاطاتٌ على "
    "مرساةٍ واحدة (`PrimarySignificationAnchor`)، فلا يستورد محورٌ آخرَ ولا "
    "يُشتَقّ منه؛ و«الدالُّ وحده» اعتبارٌ تصنيفيٌّ لا استخراجٌ من رسم الدالّ"
)

CORE_OUTPUT_IS_NOT_AUDIT_RECORD_NOTE: Final[str] = (
    "CoreOutputIsNotAuditRecord: سجلُّ الاتّفاق الصرفيِّ أثرُ تدقيقٍ لا ناتجَ "
    "نواة؛ فالاتّفاقُ والاختلافُ لا يغيّران هويّةَ المُرشَّحين"
)

RELATION_STATE_IS_NOT_GENERATION_HISTORY_NOTE: Final[str] = (
    "RelationStateIsNotGenerationHistory: المنقولُ حالةٌ في علاقة الدالّ "
    "بالمدلول، وحدثُ النقل التاريخيُّ شيءٌ آخر؛ فلا يُدمَجان في مفردةٍ واحدة"
)

NO_PATH_IS_NOT_THE_DEFAULT_PATH_NOTE: Final[str] = (
    "NoPathIsNotTheDefaultPath: `RESIDUAL` عضوٌ مُسمًّى لا فراغ؛ وغيابُ دليلٍ "
    "لمسارٍ لا يجعل مسارًا آخر أصلًا صامتًا"
)

NOT_COMPARABLE_IS_NOT_FAILURE_NOTE: Final[str] = (
    "NotComparableIsNotFailure: اختلافُ وحدة الفهرسة يمنع المقارنة، وعدمُ "
    "قابليّة المقارنة لا يُقلَب فشلًا ولا دعمًا"
)

WADH_IS_NOT_INFERRED_FROM_FORM_NOTE: Final[str] = (
    "WadhIsNotInferredFromForm: الوضعُ لا يُستنبَط من وزنٍ ولا شكلٍ ولا تكرار"
)

FOREIGN_ORIGIN_IS_NOT_CURRENT_ARABIC_IDENTITY_NOTE: Final[str] = (
    "ForeignOriginIsNotCurrentArabicIdentity: أصلٌ أعجميٌّ ليس هويّةً عربيّةً "
    "راهنة، ولا صورةٌ تبدو أعجميّةً دليلَ تعريب"
)

DERIVED_FORM_DOES_NOT_AUTHORIZE_DERIVED_MEANING_NOTE: Final[str] = (
    "DerivedFormDoesNotAuthorizeDerivedMeaning: الاشتقاقُ يفتح علاقةً بالصورة "
    "والأصل، ولا يُثبت المدلولَ النهائيّ"
)

MAJAZ_REQUIRES_LICENSED_RELATION_NOTE: Final[str] = (
    "MajazRequiresLicensedRelation: مشابهةٌ حسابيّةٌ أو انزياحٌ دلاليٌّ لا "
    "يصنع مجازًا؛ العلاقةُ تُرخَّص بدليلها المستقلّ"
)

ORIGINAL_HAQIQAH_IS_NOT_URFI_HAQIQAH_NOTE: Final[str] = (
    "OriginalHaqiqahIsNotUrfiHaqiqah: الحقيقةُ اللغويّةُ والعرفيّةُ والشرعيّةُ "
    "أجناسٌ متمايزةٌ يُصرَّح بجنسها، ولا يُقرأ أحدُها صورةً من الآخر"
)

PARTICLE_EVIDENCE_IS_RELATIONAL_NOTE: Final[str] = (
    "ParticleEvidenceIsRelationalNotIndependentLexicalMeaning: شاهدُ الحرف "
    "علاقيٌّ لأنّه «لا يستقلّ بمعناه»، فلا يُعامَل معاملةَ الاسم الجامد"
)

SIGNIFIED_CANDIDATE_IS_DEFERRED_NOTE: Final[str] = (
    "SignifiedCandidateIsDeferredNotForgotten: `LexicalSignifiedCandidate` "
    "مؤجَّلٌ بالقصد لا بالتقصير؛ وطريقُه شاهدٌ معجميٌّ ومسارٌ ومحاورُ الدلالة "
    "مع شاهدِ استعمالٍ وسياق، لا الشاهدُ المعجميُّ وحده"
)

LEX0_IS_NOT_A_GATE_NOTE: Final[str] = (
    "تسجيلٌ لا سلطة: لا تُصدر هذه الطبقة معنًى نهائيًّا ولا إفادةً ولا حكمًا "
    "ولا `License` ولا `E0`، ولا تستورد من `kernel/` شيئًا"
)


@dataclass(frozen=True, slots=True)
class GeneralLawScope:
    """نطاقُ قانونٍ عامّ: إعلانُه، وموضعُ تنفيذه، وحالُ إثباته عالميًّا."""

    law_names: tuple[str, ...]
    constitutional_scope: str
    runtime_enforcement_scope: str
    global_runtime_status: str

    def __post_init__(self) -> None:
        if not self.law_names:
            raise LexicalEvidenceSpecificationError("نطاقُ قانونٍ بلا اسمِ قانون")
        for value, label in (
            (self.constitutional_scope, "النطاقُ الدستوريّ"),
            (self.runtime_enforcement_scope, "نطاقُ التنفيذ"),
            (self.global_runtime_status, "حالُ الإثبات العالميّ"),
        ):
            if not value.strip():
                raise LexicalEvidenceSpecificationError(f"{label} نصٌّ غير فارغ.")


GENERAL_TRANSITION_LAW_SCOPE: Final[GeneralLawScope] = GeneralLawScope(
    law_names=("NecessaryRelationIsNotGenerativeAuthority", "ConditionIsNotMujib"),
    constitutional_scope="GENERAL",
    runtime_enforcement_scope="G0.LEX-0",
    global_runtime_status="NOT_YET_ESTABLISHED",
)


class LexicalCoreOutput(Enum):
    """سقفُ نواتج النواة؛ خمسةَ عشرَ عضوًا بأعيانها لا سادسَ عشرَ لها."""

    SURFACE_OCCURRENCE = "SurfaceOccurrence"
    SIGNIFIER_CANDIDATE = "SignifierCandidate"
    DERIVED_MORPHOLOGICAL_CANDIDATE = "DerivedMorphologicalCandidate"
    REPORTED_MORPHOLOGICAL_EVIDENCE = "ReportedMorphologicalEvidence"
    LEXICAL_MATCH_CANDIDATE = "LexicalMatchCandidate"
    LEXICAL_EVIDENCE_CANDIDATE = "LexicalEvidenceCandidate"
    PRIMARY_SIGNIFICATION_ANCHOR = "PrimarySignificationAnchor"
    SIGNIFIER_ALGEBRA_CANDIDATE = "SignifierAlgebraCandidate"
    SIGNIFIED_KIND_CANDIDATE = "SignifiedKindCandidate"
    SIGNIFIER_SIGNIFIED_RELATION_CANDIDATE = "SignifierSignifiedRelationCandidate"
    LEXICAL_PATH_CANDIDATE = "LexicalPathCandidate"
    LEXICAL_TASK_OUTCOME = "LexicalTaskOutcome"
    LEXICAL_COMPARATIVE_STANDING = "LexicalComparativeStanding"
    LEXICAL_AMBIGUITY_RECORD = "LexicalAmbiguityRecord"
    LEXICAL_NORMALIZATION_TRACE = "LexicalNormalizationTrace"


class LexicalAuditArtifact(Enum):
    """آثارُ التدقيق؛ خارج سقف النواة بالتصريح لا بالنسيان."""

    MORPHOLOGICAL_AGREEMENT_RECORD = "MorphologicalAgreementRecord"


class NormalizationBranch(Enum):
    """فروعُ الهمزة الثلاثة؛ و`EXACT` فرعٌ مُسمًّى لا غيابُ فرع."""

    EXACT = "EXACT"
    NORMALIZE_TO_ALIF = "NORMALIZE_TO_ALIF"
    NORMALIZE_TO_HAMZA_ALIF = "NORMALIZE_TO_HAMZA_ALIF"


NORMALIZATION_BRANCH_RULE_NAMES: Final[dict[NormalizationBranch, str | None]] = {
    NormalizationBranch.EXACT: None,
    NormalizationBranch.NORMALIZE_TO_ALIF: HAMZA_TO_BARE_ALIF_RULE.name,
    NormalizationBranch.NORMALIZE_TO_HAMZA_ALIF: HAMZA_TO_CARRIED_ALIF_RULE.name,
}


class CandidateGateState(Enum):
    """حالُ البوّابة في الصيغة الرباعيّة؛ ولا عضوَ فيها اسمُه «مُثبَت»."""

    ADMITTED_AS_CANDIDATE = "ADMITTED_AS_CANDIDATE"
    REFUSED = "REFUSED"
    DEFERRED = "DEFERRED"


@dataclass(frozen=True, slots=True)
class CandidateCore:
    """الصيغةُ الرباعيّة لكلّ مُرشَّح: موجِبٌ وشرطٌ وبوّابةٌ ودليل.

    `trigger_ref` هو **وقوعُ الدالّ نفسُه**، فيُطابِق `occurrence_ref` مطابقةً
    مفحوصة؛ ولو قُبِل موجِبٌ آخرُ لصار الموجِبُ حقلًا حرًّا يُكتَب فيه الشرط.
    و`condition_evidence_ref` يخالف الموجِبَ بالضرورة، وإلّا كان الشرطُ سببًا
    باسمٍ آخر.
    """

    occurrence_ref: str
    primary_signification_ref: str
    trigger_ref: str
    condition_evidence_ref: str
    gate_state: CandidateGateState
    evidence_refs: tuple[str, ...]
    residuals: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for value, label in (
            (self.occurrence_ref, "مرجعُ الوقوع"),
            (self.primary_signification_ref, "مرجعُ الدلالة الأصليّة المُرخَّصة"),
            (self.trigger_ref, "مرجعُ الموجِب"),
            (self.condition_evidence_ref, "مرجعُ دليل الشرط"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise LexicalEvidenceSpecificationError(f"{label} نصٌّ غير فارغ.")
        if not isinstance(self.gate_state, CandidateGateState):
            raise LexicalEvidenceSpecificationError(
                "حالُ البوّابة عضوٌ في مفردته المغلقة."
            )
        if self.trigger_ref != self.occurrence_ref:
            raise LexicalEvidenceSpecificationError(
                "الموجِبُ وقوعُ الدالّ نفسُه؛ " + CONDITION_IS_NOT_MUJIB_NOTE
            )
        if self.condition_evidence_ref == self.trigger_ref:
            raise LexicalEvidenceSpecificationError(
                "الشرطُ لا يكون هو الموجِب؛ " + CONDITION_IS_NOT_MUJIB_NOTE
            )
        if not self.evidence_refs:
            raise LexicalEvidenceSpecificationError(
                "مُرشَّحٌ بلا دليلٍ واحد؛ "
                + NECESSARY_RELATION_IS_NOT_GENERATIVE_AUTHORITY_NOTE
            )
        for reference in (*self.evidence_refs, *self.residuals):
            if not isinstance(reference, str) or not reference.strip():
                raise LexicalEvidenceSpecificationError(
                    "مراجعُ الدليل والفضلات نصوصٌ غير فارغة."
                )


_MEASURE_FIELD_MARKERS: Final[tuple[str, ...]] = (
    "count",
    "total",
    "score",
    "rank",
)

_ISSUANCE_FIELD_MARKERS: Final[tuple[str, ...]] = (
    "verdict",
    "license",
    "birth",
    "freeze",
    "proved",
    "proven",
)

REFERENCE_IS_NOT_ISSUANCE_NOTE: Final[str] = (
    "ReferenceIsNotIssuance: حقلٌ ينتهي بـ`_ref` يسمّي سجلًّا أصدرته سلطةٌ "
    "أخرى، وحقلٌ بالاسم نفسه بلا `_ref` يجعل هذه الطبقة هي المُصدِرة؛ "
    "فالاستثناءُ مقصورٌ على الإشارة، ولا يمتدّ إلى المقادير لأنّ العددَ عددٌ "
    "وإن أُشير إليه"
)


def refuse_numeric_or_verdict_fields(candidate_type: Any) -> None:
    """ارفض حقلًا يحمل عددًا أو حكمًا في بنيةٍ من بنى هذه الطبقة.

    عددٌ في بنيةٍ مُرشَّحةٍ يُقرأ قياسًا، وحكمٌ فيها يُقرأ سلطةً؛ وكلاهما خارج
    ما تبلغه `G0.LEX-0`. و`ReferenceIsNotIssuance`: حقلُ إشارةٍ ينتهي بـ`_ref`
    إلى سجلٍّ أصدرته سلطةٌ أخرى مقبولٌ بالتصريح، والمقاديرُ لا يشملها الاستثناء.
    """

    for field in fields(candidate_type):
        lowered = field.name.lower()
        for marker in _MEASURE_FIELD_MARKERS:
            if marker in lowered:
                raise LexicalEvidenceSpecificationError(
                    f"الحقل `{field.name}` يحمل مقدارًا؛ {LEX0_IS_NOT_A_GATE_NOTE}"
                )
        if lowered.endswith("_ref") or lowered.endswith("_refs"):
            continue
        for marker in _ISSUANCE_FIELD_MARKERS:
            if marker in lowered:
                raise LexicalEvidenceSpecificationError(
                    f"الحقل `{field.name}` يحمل حكمًا؛ {LEX0_IS_NOT_A_GATE_NOTE}"
                )
