"""`Σ_L` — النواةُ اللغويّةُ العامّة: لغةُ النسبة، لا العربيّةُ ولا قانونُ التمثيل.

    Σ_M (لغةُ التمثيل)  →  Σ_L (لغةُ النسبة)  →  Σ_AR (التحقيقُ العربيّ)

والمعيارُ الذي تقوم عليه هذه الحزمة:

    MetaRepresentation  ≠  LinguisticRelation  ≠  ArabicInstantiation

ثلاثةُ مستوياتٍ يفشل كلٌّ منها مستقلًّا عن الآخر: سقوطُ دعوى النسبة لا يُسقِط
قانونَ التمثيل، وسقوطُ تحقيقٍ عربيٍّ لا يُسقِط النواةَ اللغويّة.

**والتبعيّةُ أحاديّةُ الاتّجاه**: وحداتُ `v1` السبعُ تستورد من `metaalgebra/`
ومن `canonical_content` وحدَهما؛ ووحدةُ `anchored` تضيف إليها `ontology/`
و`prior/`، لأنّ `Σ_L` يعمل على ما رخّصته `O_L` ولا يُولّده. ولا تستورد هذه
الحزمةُ من `arabic/` ولا من `kernel/` حرفًا، ولا تقرأ `ontology/` منها شيئًا؛
والعكسُ مسموح: `arabic/` تُحقّق هذه النواةَ وتقرأ منها. ويُفحَص الاتّجاهُ بشاهدٍ
لا يُترَك لانتباه.

وحداتُها:

* `hypothesis` — نصُّ الفرضية مُجمَّدًا، وفاحصُ أمانةٍ قبليٌّ لمواضعه الحاسمة.
* `role` — `LinguisticObject(x) = Representation(x) + RelationalRole(x)`،
  بفصلٍ **نوعيٍّ** بين مرجع التمثيل ومرجع الدور.
* `nisbah` — `TermAnchor` و`Predicate_n` و`ArgumentSlot` و`Operator` و`Constraint`.
* `closure` — الإغلاقُ خماسيُّ المكوّنات، وناتجُه `PreIfadahClosure` لا الإفادة.
* `schema` — `Σ_L` نفسُها: سبعةُ أصنافٍ وقوانينُها، مبنيّةً على بصمة `Σ_M`.
* `relativization` — ترتيبُ المنزلة بين التمثيل والوظيفة، لا نسخٌ ولا منافسة.
* `null_model` — النماذجُ الأضعفُ وشروطُ المدوّنة المستقلّة، تسجيلًا بلا تشغيل.
* `anchored` — `v2`: النسبةُ مُسنَدةً إلى `O_L`، بجانب `v1` لا فوقه؛ وهي
  وحدَها من هذه الحزمة تقرأ `ontology/`، والعكسُ ممنوع.

**والمعرّفاتُ لاتينيّةٌ والتوثيقُ عربيّ**، لأنّ هذه الحزمةَ غيرُ مخصوصةٍ
بالعربيّة وإن كانت العربيّةُ أوّلَ ميادين تحقيقها.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`، ولا تقرأ هذه الحزمةَ
بوّابةٌ في `kernel/`.
"""

from __future__ import annotations

from .anchored import (
    A_LICENSE_OF_ANOTHER_ONTOLOGY_IS_NOT_A_LICENSE,
    AN_ANCHOR_ROLE_IS_A_LICENSE_NOT_A_PRIMITIVE,
    ANCHORED_NISBAH_SCHEMA,
    ANCHORED_SCHEMA_VERSION,
    FREE_TEXT_CONDITION_IS_NOT_A_LICENSED_CONDITION,
    V2_STANDS_BESIDE_V1_NOT_OVER_IT,
    AnchoredArgumentSlot,
    AnchoredLayerError,
    AnchoredNisbahSchema,
    AnchoredNisbahSignature,
    AnchoredPredicateSignature,
    AnchoredTermAnchor,
    BaseSchemaRef,
    LicensedConditionRef,
    LicensedRoleRef,
)
from .closure import (
    ARGUMENT_FILLING_IS_NOT_CLOSURE,
    CLOSURE_COMPONENT_NAMES,
    CLOSURE_COVERAGE_IS_EXACT_NOT_BEST_EFFORT,
    IFADA_PREREQUISITE_NAMES,
    IFADA_VOCABULARY_IS_NOT_DUPLICATED,
    RELATIONAL_CLOSURE_IS_NOT_IFADAH,
    ClosureComponent,
    ClosureComponentReading,
    IfadaPrerequisite,
    RelationalClosureAssessment,
    RelationalClosureError,
    RelationalClosureStanding,
    assess_relational_closure,
)
from .hypothesis import (
    AN_INTERNAL_HYPOTHESIS_IS_NOT_A_TRANSMITTED_SOURCE_NOTE,
    FIDELITY_IS_DERIVED_NOT_PROMISED_NOTE,
    NISBAH_HYPOTHESIS_NAMED_RESIDUALS,
    NISBAH_HYPOTHESIS_TEXT,
    NISBAH_TEXT_DIGEST,
    NO_READOUT_EXISTS_FOR_NSB0_YET_NOTE,
    REQUIRED_NOTATION_SITES,
    THREE_LEVELS_ARE_NOT_TWO_NOTE,
    FidelityReport,
    FidelitySiteReading,
    FidelityStanding,
    NisbahHypothesisError,
    NotationSite,
    derive_fidelity_report,
    nisbah_text_digest,
)
from .nisbah import (
    AN_OPERATOR_WITHOUT_SCOPE_IS_NOT_SCOPED,
    ARGUMENT_ROLES_ARE_DEFERRED_TO_THEIR_OWN_LAYER,
    ARITY_MUST_BE_LICENSED_BEFORE_USE,
    CANDIDATE_BRANCH_IS_NOT_A_BORN_KIND,
    DEFERRED_ARGUMENT_ROLE_NAMES,
    NISBAH_COMPONENT_NAMES,
    PREDICATE_COMPONENT_NAMES,
    TERM_ANCHOR_IS_WIDER_THAN_GENUS,
    ArgumentSlot,
    ArityLicenseGenus,
    ConstraintKind,
    ConstraintSpecification,
    NisbahError,
    NisbahSignature,
    OperatorSignature,
    PredicateSignature,
    TermAnchorKind,
    TermAnchorSignature,
)
from .null_model import (
    A_WEAKER_REPRESENTATION_THAT_TIES_DEFEATS_THE_CLAIM,
    CORPUS_INDEPENDENCE_CONDITIONS,
    NISBAH_NULL_MODELS,
    REGISTRATION_IS_NOT_A_RUN,
    THE_CORPUS_IS_NAMED_BEFORE_THE_RESULT,
    CorpusIndependenceCondition,
    NullModelRegistration,
    NullModelRegistrationError,
    RunStanding,
)
from .relativization import (
    ONLY_A_DEMONSTRATED_CONTRADICTION_COMPETES,
    RELATIVIZATION_IS_NOT_COMPETITION,
    ContradictionStanding,
    HigherOrderRelativizationRecord,
    RelativizationError,
    RelativizedStatementRef,
)
from .role import (
    AN_UNREAD_ROLE_IS_NOT_AN_ABSENT_ONE,
    RELATION_IS_NOT_REPRESENTATION,
    LinguisticObjectSignature,
    RelationalRole,
    RelationalRoleError,
    RelationalRoleRef,
    RepresentationRef,
)
from .schema import (
    LINGUISTIC_NISBAH_SCHEMA,
    LINGUISTIC_SORT_IDS,
    LINGUISTIC_SORTS_ARE_NOT_META_SORTS,
    NO_CONCRETE_NISBAH_IN_THE_NUCLEUS,
    SCHEMA_VERSION,
    LinguisticLaw,
    LinguisticNisbahSchema,
    LinguisticNisbahSchemaError,
    LinguisticSortDeclaration,
)

__all__ = [
    "ANCHORED_NISBAH_SCHEMA",
    "ANCHORED_SCHEMA_VERSION",
    "AN_ANCHOR_ROLE_IS_A_LICENSE_NOT_A_PRIMITIVE",
    "AN_INTERNAL_HYPOTHESIS_IS_NOT_A_TRANSMITTED_SOURCE_NOTE",
    "AN_OPERATOR_WITHOUT_SCOPE_IS_NOT_SCOPED",
    "AN_UNREAD_ROLE_IS_NOT_AN_ABSENT_ONE",
    "ARGUMENT_FILLING_IS_NOT_CLOSURE",
    "ARGUMENT_ROLES_ARE_DEFERRED_TO_THEIR_OWN_LAYER",
    "ARITY_MUST_BE_LICENSED_BEFORE_USE",
    "A_LICENSE_OF_ANOTHER_ONTOLOGY_IS_NOT_A_LICENSE",
    "A_WEAKER_REPRESENTATION_THAT_TIES_DEFEATS_THE_CLAIM",
    "CANDIDATE_BRANCH_IS_NOT_A_BORN_KIND",
    "CLOSURE_COMPONENT_NAMES",
    "CLOSURE_COVERAGE_IS_EXACT_NOT_BEST_EFFORT",
    "CORPUS_INDEPENDENCE_CONDITIONS",
    "DEFERRED_ARGUMENT_ROLE_NAMES",
    "FIDELITY_IS_DERIVED_NOT_PROMISED_NOTE",
    "FREE_TEXT_CONDITION_IS_NOT_A_LICENSED_CONDITION",
    "IFADA_PREREQUISITE_NAMES",
    "IFADA_VOCABULARY_IS_NOT_DUPLICATED",
    "LINGUISTIC_NISBAH_SCHEMA",
    "LINGUISTIC_SORTS_ARE_NOT_META_SORTS",
    "LINGUISTIC_SORT_IDS",
    "NISBAH_COMPONENT_NAMES",
    "NISBAH_HYPOTHESIS_NAMED_RESIDUALS",
    "NISBAH_HYPOTHESIS_TEXT",
    "NISBAH_NULL_MODELS",
    "NISBAH_TEXT_DIGEST",
    "NO_CONCRETE_NISBAH_IN_THE_NUCLEUS",
    "NO_READOUT_EXISTS_FOR_NSB0_YET_NOTE",
    "ONLY_A_DEMONSTRATED_CONTRADICTION_COMPETES",
    "PREDICATE_COMPONENT_NAMES",
    "REGISTRATION_IS_NOT_A_RUN",
    "RELATION_IS_NOT_REPRESENTATION",
    "RELATIONAL_CLOSURE_IS_NOT_IFADAH",
    "RELATIVIZATION_IS_NOT_COMPETITION",
    "REQUIRED_NOTATION_SITES",
    "SCHEMA_VERSION",
    "TERM_ANCHOR_IS_WIDER_THAN_GENUS",
    "THE_CORPUS_IS_NAMED_BEFORE_THE_RESULT",
    "THREE_LEVELS_ARE_NOT_TWO_NOTE",
    "V2_STANDS_BESIDE_V1_NOT_OVER_IT",
    "AnchoredArgumentSlot",
    "AnchoredLayerError",
    "AnchoredNisbahSchema",
    "AnchoredNisbahSignature",
    "AnchoredPredicateSignature",
    "AnchoredTermAnchor",
    "ArgumentSlot",
    "ArityLicenseGenus",
    "BaseSchemaRef",
    "ClosureComponent",
    "ClosureComponentReading",
    "ConstraintKind",
    "ConstraintSpecification",
    "ContradictionStanding",
    "CorpusIndependenceCondition",
    "FidelityReport",
    "FidelitySiteReading",
    "FidelityStanding",
    "HigherOrderRelativizationRecord",
    "IfadaPrerequisite",
    "LicensedConditionRef",
    "LicensedRoleRef",
    "LinguisticLaw",
    "LinguisticNisbahSchema",
    "LinguisticNisbahSchemaError",
    "LinguisticObjectSignature",
    "LinguisticSortDeclaration",
    "NisbahError",
    "NisbahHypothesisError",
    "NisbahSignature",
    "NotationSite",
    "NullModelRegistration",
    "NullModelRegistrationError",
    "OperatorSignature",
    "PredicateSignature",
    "RelationalClosureAssessment",
    "RelationalClosureError",
    "RelationalClosureStanding",
    "RelationalRole",
    "RelationalRoleError",
    "RelationalRoleRef",
    "RelativizationError",
    "RelativizedStatementRef",
    "RepresentationRef",
    "RunStanding",
    "TermAnchorKind",
    "TermAnchorSignature",
    "assess_relational_closure",
    "derive_fidelity_report",
    "nisbah_text_digest",
]
