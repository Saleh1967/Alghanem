"""`G0.METRIC-0`: قوانينُ المقياس، مُسمّاةً قبل أن يُشتَقّ رقمٌ واحد.

الخطرُ الذي تُغلقه هذه الوحدة ليس خطأً حسابيًّا بل خطأٌ في **المقام**: مقياسٌ
مقامُه ما بُني يقيس البناءَ بنفسه، فيبلغ المئةَ حين يُكمِل ما اختار تمثيلَه،
وتبقى العربيةُ التي لم تُبنَ خارجَ القسمة لا صفرًا فيها. ولذلك يُجمَّد هنا أنّ
المقامَ مُعلَنٌ من خارج التنفيذ، وأنّ القدرةَ غيرَ المبنيّة **صفٌّ لا فراغ**.

ولا سلطةَ لهذه الوحدة: لا تقرؤها بوّابةٌ في `kernel/`، ولا تُولِد ولا تُجمِّد.

و`G0.METRIC-0.HARDEN` يُغلِق ما بقي مفتوحًا بعد أوّل شهادة: لا حسابَ على رتب
البوّابات بلا أوزانٍ مُعلَنة، ولا اسمَ مصدرٍ يُقرأ موضعًا محقَّقًا، ولا عدَّ
أوراقٍ يُقرأ مقدارًا للعربية، ولا بوّابةَ أهليّةٍ مُصرَّحٍ بها تُقرأ مُشتَقّة.
"""

from __future__ import annotations

from typing import Final

__all__ = [
    "A_DECLARED_DENOMINATOR_IS_NOT_THE_COMPLETE_ONTOLOGY_OF_ARABIC",
    "A_DENOMINATOR_DERIVED_FROM_THE_IMPLEMENTATION_IS_NOT_A_MEASURE",
    "A_RATIO_CARRIES_ITS_DENOMINATOR",
    "BREADTH_IS_NOT_READINESS",
    "CAPABILITY_LAWS",
    "CITATION_NAME_IS_NOT_A_VERIFIED_SOURCE_LOCUS",
    "DECLARED_COVERAGE_IS_NOT_SYSTEM_CAPABILITY",
    "DIFFERENT_MEASUREMENT_SEMANTICS_ARE_NOT_COMPARABLE_CERTIFICATES",
    "EQUAL_DOMAIN_WEIGHTING_IS_STILL_A_WEIGHTING_PROTOCOL",
    "EVIDENCE_MUST_HAVE_AN_AUTHORITY_PATH",
    "KEEPING_A_QUESTION_DOES_NOT_LICENSE_A_FALSE_CITATION",
    "MISSING_IMPLEMENTATION_DOES_NOT_REMOVE_A_CAPABILITY",
    "NO_KERNEL_MODULE_CONSUMES_THE_CAPABILITY_MAP",
    "NO_ORDINAL_GATE_ARITHMETIC_WITHOUT_DECLARED_WEIGHTS",
    "OUR_CONCEPTUAL_MAPPING_IS_NOT_A_SOURCE_TEXT_ANCHOR",
    "REPEATED_REFERENCE_IS_NOT_INDEPENDENT_EVIDENCE",
    "SOURCE_CITATION_DOES_NOT_LICENSE_SYSTEM_CAPABILITY",
    "STANDINGS_ARE_GATES_NOT_EPISTEMIC_MAGNITUDES",
    "TAXONOMY_GRANULARITY_IS_NOT_CAPABILITY_IMPORTANCE",
    "THE_DENOMINATOR_IS_CITED_NOT_INVENTED",
    "THE_METRIC_MUST_BE_ALLOWED_TO_GO_DOWN",
    "UNIFORM_READINESS_GATE_IS_NOT_A_DERIVED_READINESS_REQUIREMENT",
    "UNIMPLEMENTED_CAPABILITY_MUST_REMAIN_VISIBLE",
]

A_DENOMINATOR_DERIVED_FROM_THE_IMPLEMENTATION_IS_NOT_A_MEASURE: Final[str] = (
    "ADenominatorDerivedFromTheImplementationIsNotAMeasure: مقامٌ مُشتَقٌّ من "
    "الشجرة المبنيّة يقيس البناءَ بنفسه، فيبلغ تمامَه حين يُكمِل ما اختار "
    "تمثيلَه وحدَه؛ والمقامُ هنا مُعلَنٌ من خارج التنفيذ ولا يقرأ `src/`"
)

A_DECLARED_DENOMINATOR_IS_NOT_THE_COMPLETE_ONTOLOGY_OF_ARABIC: Final[str] = (
    "ADeclaredDenominatorIsNotTheCompleteOntologyOfArabic: المئةُ في هذا "
    "المقياس مئةُ ما أُعلِن من أبواب، لا مئةُ العربية؛ فالمقامُ دعوى إعلانٍ "
    "قابلةٌ للتوسعة، ومن قرأه أنطولوجيا تامّةً نسب إلى المقياس ما لم يدَّعِه"
)

MISSING_IMPLEMENTATION_DOES_NOT_REMOVE_A_CAPABILITY: Final[str] = (
    "MissingImplementationDoesNotRemoveACapabilityFromTheDenominator: انتفاءُ "
    "التنفيذ لا يُخرِج القدرةَ من المقام؛ تبقى في الشجرة بحالتها الصريحة "
    "وتُخفِض التغطيةَ بصدق، فإسقاطُها من الحساب تحسينُ رقمٍ بحذف سؤاله"
)

UNIMPLEMENTED_CAPABILITY_MUST_REMAIN_VISIBLE: Final[str] = (
    "UnimplementedCapabilityMustRemainVisible: ورقةٌ بلا شاهدٍ ليست خطأَ بناء "
    "بل **غيابٌ مقيس**؛ تُعرَض برتبتها ومانِعِها وبوّابتها التالية، لأنّ "
    "رفضَها عند البناء يُخفي ما نريد أن نراه"
)

THE_DENOMINATOR_IS_CITED_NOT_INVENTED: Final[str] = (
    "TheDenominatorIsCitedNotInvented: كلُّ عقدةٍ في المقام تحمل استشهادَها "
    "من مصدرٍ مُعلَن وموضعٍ فيه؛ وعقدةٌ بلا استشهادٍ رأيٌ لا مقام"
)

STANDINGS_ARE_GATES_NOT_EPISTEMIC_MAGNITUDES: Final[str] = (
    "StandingsAreGatesNotEpistemicMagnitudes: درجاتُ النضج بوّاباتٌ مرتّبةٌ "
    "بالترخيص لا مقاديرُ معرفيّةٌ تُجمَع وتُطرَح؛ فالفرقُ بين درجتين فرقُ "
    "إذنٍ لا فرقُ قوّةٍ حسابيّة"
)

BREADTH_IS_NOT_READINESS: Final[str] = (
    "Breadth != Readiness: التغطيةُ مقدارُ ما بُني عبر المجال المُعلَن، "
    "والأهليةُ مدى صلاحيّة المبنيّ لأن تُبنى عليه الطبقةُ التالية؛ فاتّساعُ "
    "الأولى لا يُقرأ ارتفاعًا في الثانية، ولا يُجمَعان في رقمٍ واحد"
)

EVIDENCE_MUST_HAVE_AN_AUTHORITY_PATH: Final[str] = (
    "EvidenceMustHaveAnAuthorityPath: لكلّ شاهدٍ مسارُ سلطةٍ مُنمَّطٌ يُصدِره، "
    "ولا يلزم أن يكون إيصالَ تنفيذٍ بعينه؛ فإحالةُ الإحصاءِ والبرهانِ "
    "والقياسِ قسرًا إلى عمليّةِ قارئٍ تزييفُ جنسِ الشاهد لا تقويةٌ له"
)

REPEATED_REFERENCE_IS_NOT_INDEPENDENT_EVIDENCE: Final[str] = (
    "RepeatedReference != IndependentEvidence: الإحالةُ المكرَّرةُ إلى الشاهد "
    "نفسِه شاهدٌ واحد؛ والتوحيدُ على (القدرة + النطاق + مُلخَّص التجربة + "
    "مُلخَّص العقد + مُلخَّص البروتوكول) لا على عدد الملفّات"
)

THE_METRIC_MUST_BE_ALLOWED_TO_GO_DOWN: Final[str] = (
    "TheMetricMustBeAllowedToGoDown: توسعةُ المقام، أو سقوطُ شاهدٍ، أو فشلُ "
    "إعادةِ تشغيل، تُنقِص الرقمَ؛ ومقياسٌ لا ينزل ليس مقياسًا بل إعلانًا"
)

A_RATIO_CARRIES_ITS_DENOMINATOR: Final[str] = (
    "ARatioCarriesItsDenominator: لا تُعرَض نسبةٌ مجرّدةً عن بسطِها ومقامِها "
    "ومصدرِ تجميدِ مقامها؛ ونسبةٌ مقامُها صفرٌ غيرُ معرَّفةٍ لا صفرٌ ولا تمام"
)

NO_KERNEL_MODULE_CONSUMES_THE_CAPABILITY_MAP: Final[str] = (
    "NoKernelModuleConsumesTheCapabilityMap: لا تقرأ هذه الحزمةَ بوّابةٌ في "
    "`kernel/`، ولا تُولِد ولا تُجمِّد ولا تُصدِر حكمًا؛ وهي تقيس ما وقع"
)

NO_ORDINAL_GATE_ARITHMETIC_WITHOUT_DECLARED_WEIGHTS: Final[str] = (
    "NoOrdinalGateArithmeticWithoutDeclaredWeights: موضعُ البوّابة في التسلسل "
    "رتبةُ ترخيصٍ لا مقدار، فلا يُجمَع ولا يُتوسَّط `gate_index` ولا يُقسَم على "
    "عدد البوّابات؛ ورقمٌ مركّبٌ لا يصدر إلّا عن بروتوكول أوزانٍ مُعلَنٍ مُجمَّد "
    "يُبرِّر وزنَ كلِّ بوّابةٍ بعينها"
)

DECLARED_COVERAGE_IS_NOT_SYSTEM_CAPABILITY: Final[str] = (
    "DeclaredCoverage != SystemCapability: بلوغُ `DeclaredCoverage` تمامَه يعني "
    "أنّ أسئلةَ المقام كلَّها حاضرةٌ مُعلَنة، لا أنّ النظامَ يملك شيئًا لغويًّا؛ "
    "فالإعلانُ إثباتُ سؤالٍ لا إثباتُ قدرة"
)

CITATION_NAME_IS_NOT_A_VERIFIED_SOURCE_LOCUS: Final[str] = (
    "CitationName != VerifiedSourceLocus: تسميةُ المصدرِ ليست توثيقَ موضعٍ فيه، "
    "وإعادةُ اسمِ القدرة موضعًا استشهادٌ اسميّ؛ فلكلّ استشهادٍ مرتبةٌ مُصرَّحٌ "
    "بها تُظهِر ما تحقّق منه فعلًا وما لم يتحقّق بعد"
)

OUR_CONCEPTUAL_MAPPING_IS_NOT_A_SOURCE_TEXT_ANCHOR: Final[str] = (
    "OurConceptualMapping != SourceTextAnchor: بصمةُ صياغتنا المفهوميّة شاهدٌ "
    "على عملنا نحن لا مرساةٌ في نصّ المصدر؛ وخلطُهما يجعل تحليلَنا نفسَه يبدو "
    "نقلًا من الكتاب القديم"
)

KEEPING_A_QUESTION_DOES_NOT_LICENSE_A_FALSE_CITATION: Final[str] = (
    "KeepingAQuestionDoesNotLicenseAFalseCitation: بقاءُ البابِ في المقام واجبٌ "
    "لأنّ حذفَه تحسينُ رقمٍ بحذف سؤاله، ولا يُبيح ذلك نسبتَه إلى مصدرٍ لم يثبت "
    "فيه؛ فالسؤالُ يبقى والمرتبةُ تنزل"
)

SOURCE_CITATION_DOES_NOT_LICENSE_SYSTEM_CAPABILITY: Final[str] = (
    "SourceCitationDoesNotLicenseSystemCapability: توثيقُ المصدر يُثبِت المقامَ "
    "ومصدرَ السؤال، ولا يرفع درجةَ نضجٍ واحدة؛ فلا `MODELED` ولا `EXECUTABLE` "
    "ولا `GOLD` تُنال بجودة الاستشهاد"
)

TAXONOMY_GRANULARITY_IS_NOT_CAPABILITY_IMPORTANCE: Final[str] = (
    "TaxonomyGranularity != CapabilityImportance: عدُّ الأوراق يجعل بابًا "
    "قسمناه عشرًا أثقلَ من بابٍ قسمناه اثنتين، لا لأنّ ذلك ثبت بل لأنّنا "
    "فصّلناه أكثر؛ فلا يُقرأ `LeafCoverage` وحدَه مقدارًا للعربية"
)

EQUAL_DOMAIN_WEIGHTING_IS_STILL_A_WEIGHTING_PROTOCOL: Final[str] = (
    "EqualDomainWeightingIsStillAWeightingProtocol: تسويةُ المجالات في الوزن "
    "هندسةُ قياسٍ أخرى لا حقيقةٌ مُشتَقّة، كتسوية البوّابات سواءً بسواء؛ فتُعرَض "
    "نسبُ المجالات منفصلةً، ويبقى الرقمُ الموحَّد غيرَ معرَّفٍ حتى يُعلَن بروتوكولُ "
    "أوزان المجالات"
)

UNIFORM_READINESS_GATE_IS_NOT_A_DERIVED_READINESS_REQUIREMENT: Final[str] = (
    "UniformReadinessGate != DerivedReadinessRequirement: بوّابةُ أهليّةٍ واحدةٌ "
    "لكلّ العقد تصريحٌ أوّليّ لا نتيجةَ تحليلِ اعتماديّة؛ وتبقى مُعلَنةً بأصلها "
    "حتى تُشتَقّ من دور كلّ قدرةٍ في الطبقة التالية"
)

DIFFERENT_MEASUREMENT_SEMANTICS_ARE_NOT_COMPARABLE_CERTIFICATES: Final[str] = (
    "DifferentMeasurementSemanticsAreNotComparableCertificates: شهادتان على "
    "دلاليّتَي قياسٍ مختلفتين ليستا مقارنةً رقميّة؛ فتحمل كلُّ شهادةٍ إصدارَ "
    "مُخطَّطها، وتغيّرُ المُلخَّص بتغيّر العقد الدلاليّ ليس تراجعًا"
)

CAPABILITY_LAWS: Final[tuple[str, ...]] = (
    A_DENOMINATOR_DERIVED_FROM_THE_IMPLEMENTATION_IS_NOT_A_MEASURE,
    A_DECLARED_DENOMINATOR_IS_NOT_THE_COMPLETE_ONTOLOGY_OF_ARABIC,
    MISSING_IMPLEMENTATION_DOES_NOT_REMOVE_A_CAPABILITY,
    UNIMPLEMENTED_CAPABILITY_MUST_REMAIN_VISIBLE,
    THE_DENOMINATOR_IS_CITED_NOT_INVENTED,
    STANDINGS_ARE_GATES_NOT_EPISTEMIC_MAGNITUDES,
    NO_ORDINAL_GATE_ARITHMETIC_WITHOUT_DECLARED_WEIGHTS,
    DECLARED_COVERAGE_IS_NOT_SYSTEM_CAPABILITY,
    CITATION_NAME_IS_NOT_A_VERIFIED_SOURCE_LOCUS,
    OUR_CONCEPTUAL_MAPPING_IS_NOT_A_SOURCE_TEXT_ANCHOR,
    KEEPING_A_QUESTION_DOES_NOT_LICENSE_A_FALSE_CITATION,
    SOURCE_CITATION_DOES_NOT_LICENSE_SYSTEM_CAPABILITY,
    TAXONOMY_GRANULARITY_IS_NOT_CAPABILITY_IMPORTANCE,
    EQUAL_DOMAIN_WEIGHTING_IS_STILL_A_WEIGHTING_PROTOCOL,
    UNIFORM_READINESS_GATE_IS_NOT_A_DERIVED_READINESS_REQUIREMENT,
    DIFFERENT_MEASUREMENT_SEMANTICS_ARE_NOT_COMPARABLE_CERTIFICATES,
    BREADTH_IS_NOT_READINESS,
    EVIDENCE_MUST_HAVE_AN_AUTHORITY_PATH,
    REPEATED_REFERENCE_IS_NOT_INDEPENDENT_EVIDENCE,
    THE_METRIC_MUST_BE_ALLOWED_TO_GO_DOWN,
    A_RATIO_CARRIES_ITS_DENOMINATOR,
    NO_KERNEL_MODULE_CONSUMES_THE_CAPABILITY_MAP,
)
"""قوانينُ المرحلة مجموعةً، ليُقرأ سقفُ كلِّ رقمٍ معه لا بعده."""
