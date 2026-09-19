"""الحدُّ الأدنى المكتمل: مبرهنةٌ **مشروطةٌ** قابلةٌ للاختبار، لا شهادةَ ولادة.

**المعادلةُ التأسيسيّة**، مُودَعةً بنصّها: ليكن `a` مرساةَ هويّة، و`g` جنسَها
المرخَّص، و`P(g)` فضاءَ المحمولات الممكنة لها، و`R(a,p)` فضاءَ العلاقات التي
يمكن فحصها بين `a` والمحمول `p`. فالليفُ المرشَّح:

    E_(a,g) = ⨆_{p ∈ P(g)} R(a,p)

وعنصرُه الداخليّ `u = (a, g, p, r)`، حيث `r` **تعيينُ نوع** الربط — إخبارٌ، أو
تقييدٌ، أو علاقةٌ حدثيّة — لا مجرّدُ وجود رابط.

**وأربعةُ حقولٍ في التمثيل تؤدّي ثلاثَ وظائفَ بنيويّة**: الهويّةُ والتصنيفُ
(`a` و`g`)، والمحمولُ (`p`)، والإسنادُ (`r`). وإذا كان الجنسُ مستنتَجًا بصورةٍ
وحيدةٍ ومرخَّصةٍ من المرساة فلا يلزم تكرارُ تخزينه؛ فالحدُّ الأدنى يحفظ
**معلومةَ** التصنيف ولا يفرض **حقلًا** باسم الجنس
(`FOUR_FIELDS_CARRY_THREE_FUNCTIONS`).

**ومبرهنةُ الحدّ الأدنى المكتمل مشروطةٌ بطرفين لا طرف**. أوّلُهما الكفاية:
قارئٌ مستقلٌّ `D` يُرجِع مضمونَ الإفادة من مخرج التمثيل وحدَه،
`D(T(x)) = F(x)` لكلّ `x ∈ 𝒟`. وثانيهما الضرورة: مكوّنٌ `i` لا يجوز إسقاطُ
معلوماته إن وُجد شاهدان `T_{-i}(x) = T_{-i}(y)` مع `F(x) ≠ F(y)`، إذ دمجَ
التمثيلُ الناقصُ مدخلين يحتاجان مخرجين، فيستحيل قارئٌ يردُّهما من قيمةٍ واحدة.
فالمعيار:

    MCM(T) ⟺ Sufficient(T) ∧ ⋀_{i ∈ I} Necessary(i)

**والشطران يُجرَيان تجربةً لا يُفحَصان بالأسماء**. فالكفايةُ تُقاس بقارئٍ لا
يُمرَّر إليه إلّا `T(x)`؛ والحجبُ بنيويٌّ: يُنادى القارئُ مرّةً واحدةً لكلّ
مخرجٍ متمايز، ثمّ يُقابَل جوابُه بمضمون كلّ حالةٍ تشترك في ذلك المخرج، فلا
يملك ما يفرّق به بين حالتين دمجهما التمثيل. والضرورةُ تُقاس بإجراء التجربة
نفسِها على `T_{-i}` بأفضلِ قارئٍ ممكنٍ على مخرجاتها. وجنسُ المجال **مُشتَقٌّ لا مكتوب**:
لا حقلَ يُعلِن فيه صاحبُ المجال أنّه «لغويٌّ مُعلَن»؛ بل يُرفَع إلى ذلك متى
وُثِّقت كلُّ حالةٍ فيه توثيقًا يتحقّق من **ثلاث جهاتٍ مترابطة**: تطابقُ بصمة
مصدرٍ مُسجَّلٍ تُعاد حوسبتُها عند كلّ فحص، ووقوعٌ **يُحَلّ** عند محدِّد موضعٍ
صالحٍ فيطابق مرساةَ الحالة، ووسمٌ من **جهةٍ غيرِ مُعلِن المجال** يربط ذلك
الوقوعَ بالجنس والمحمول والمضمون المقصود. وسقوطُ جهةٍ منها يُبقي المجالَ
مصمَّمًا أو **غيرَ محسوم**، ولا تُجبَر جهةٌ بأخرى: فشهادةُ ورود اللفظ ليست
شهادةَ صحّةِ تفسيره (`AN_OCCURRENCE_IS_NOT_A_GLOSS`)، ووسمٌ يكتبه صاحبُ الدعوى
على دعواه مردودٌ بالبناء (`A_SELF_AUTHORED_GLOSS_IS_REFUSED`). فبوّابةُ الشهادة
لا تُفتَح بالتسمية (`A_DOMAIN_KIND_IS_DERIVED_FROM_ATTESTATIONS_NOT_WRITTEN`).
والمجالُ المُجرَى عليه ههنا مصمَّمٌ لاختبار التمثيل — صفرٌ من حالاته موثَّق —
فقيامُ المعيار عليه حكمٌ على مجاله وحدَه
(`A_DESIGNED_DOMAIN_IS_NOT_A_LINGUISTIC_CERTIFICATE`)، وقارئُ الجدول يثبت
تباينَ التمثيل لا فهمَه (`A_LOOKUP_READER_PROVES_INJECTIVITY_NOT_UNDERSTANDING`)
فلا يُغلِق شرطَ القارئ المستقلّ ولو قامت به الكفاية.

**والشواهدُ العربيّةُ الثلاثةُ تُجرى بمقامٍ مثبَّتٍ وتوافقٍ نوعيٍّ مفحوص**:
«عينٌ غائرة» بجنسَي البصر والماء لحذف التصنيف، و«زيد طويل/قصير» لحذف المحمول،
و«الرجل الطويل»/«الرجل طويل» لحذف نوع الربط. ويُشترَط في كلّ عنصرٍ انتماءُ
محموله إلى `P(g)` المُعلَن (`THE_PREDICATE_SPACE_IS_DECLARED_NOT_MEASURED`)،
ويُكتَب مقامُه قبل الحذف. وكلُّ تجربةٍ من الثلاث تدمج مضمونين فتنقض الكفاية،
لكنّ المُجرَى عليه أزواجٌ مكتوبةٌ ههنا، **لا شهادةٌ بأنّ اختبارًا نُفِّذ على
المِرماز**
(`A_DESIGNED_WITNESS_IS_NOT_AN_EXECUTED_CODEC_TEST`). وتصادمُها تصادمٌ **في
التمثيل**: يمنع أن يُنسَخ المحذوفُ في حقلٍ آخر ههنا، ولا يُغني عن تثبيت المجال
والسياق ومنعِ استعادته من الأصل
(`A_COLLISION_IN_THE_REPRESENTATION_IS_NOT_A_COLLISION_IN_CONTEXT`).

**و`zero`/`one` حالتان للعمليّة نفسِها، مُودَعتان شكلًا بلا عمليّة**:
`Z = (a, g, p, ⊥)` حاملٌ مصنَّفٌ ومحمولٌ مرشَّحٌ بلا وجهِ ربطٍ مُعيَّن، و
`O = (a, g, p, r, e, ε)` إسنادٌ مُعيَّنٌ بدليلٍ وبقايا. و`RefineSlot` **غيرُ
مُصدَّرةٍ ههنا**: ضرورتُها غيرُ مبرهنة، والشكلُ يُودَع ولا يُرخَّص. ولا تعني
`one` صدقَ القضيّة في الواقع (`ONE_IS_A_NAMED_ATTRIBUTION_NOT_A_TRUE_PROPOSITION`)،
ولا تعني `zero` ليفًا خاليًا ولا صفةً منفيّة، بل عدمَ تعيينِ رابطة
(`ZERO_IS_AN_UNNAMED_RELATION_NOT_AN_EMPTY_FIBER`).

**والإغلاقُ لا يُعلَن**: قائمةُ التدقيق سبعةُ شروطٍ، وكلُّ شرطٍ يُقرَأ من
**نتيجة تجربته المعيّنة** وسندِها معًا: شاهدٌ مُجرًى، ونتيجةٌ تُغلِق ذلك الشرطَ
بعينه، ومجالٌ لغويٌّ مُعلَنٌ مفحوصُ التوثيق. فلا يُستوفى شرطٌ بمجالٍ موثَّقٍ
وتجربةٍ فاشلة، ولا بتجربةٍ ناجحةٍ على مجالٍ مصمَّم، ولا بشاهدٍ نجح في تجربةِ
مكوّنٍ غيرِ المكوّن الذي يُسأل عنه الشرط. فالمستوفى **صفرٌ** مُشتقًّا بالتشغيل
لا مكتوبًا. واستيفاؤها جميعًا — لو وقع — فحصٌ مسجَّلٌ لا شهادةٌ صادرة؛ فإصدارُ
الشهادة تفويضٌ إلى جهةٍ حاكمةٍ خطوةً مستقلّة
(`A_RECORDED_CONDITION_IS_NOT_AN_ISSUED_CERTIFICATE`). وما
يثبت — لو ثبت — حدٌّ أدنى **بالنسبة إلى**
المكوّنات المرشَّحة وصنفِ البدائل المختبَر، لا إلزامٌ لكلّ ترميزٍ بثلاثة حقولٍ
منفصلة (`THE_MINIMUM_IS_RELATIVE_TO_THE_TESTED_ALTERNATIVES`).

ولا سلطةَ لهذه الوحدة: لا ولادةَ، ولا حكمَ ولادة، ولا ترخيصَ `RefineSlot`، ولا
استيرادَ من `kernel/`.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from typing import Final

from .fatiha_source_text import FATIHA_SOURCE_ID
from .fatiha_source_text import source_sha256 as fatiha_source_sha256
from .gloss_registry import (
    GlossEntry,
    GlossRegistry,
    SourceLocator,
    in_tree_gloss_registry,
    normalize,
    resolve_locator,
)

__all__ = [
    "AN_ATTESTED_CORPUS_IS_NOT_A_SUFFICIENT_SAMPLE",
    "AN_OCCURRENCE_IS_NOT_A_GLOSS_NOTE",
    "A_RECORDED_CONDITION_IS_NOT_AN_ISSUED_CERTIFICATE_NOTE",
    "A_SELF_AUTHORED_GLOSS_IS_REFUSED_NOTE",
    "AttestationStanding",
    "ConditionRunKind",
    "ProvenancedReader",
    "ReaderRuleOrigin",
    "SealedReaderRule",
    "a_rule_sealed_before_any_case",
    "a_rule_trained_on",
    "hold_out_reader",
    "ReaderProvenance",
    "the_deposited_gloss_registry",
    "NO_EVIDENCE_KIND_HERE_CLOSES",
    "THE_DOMAIN_DECLARER_ID",
    "assess_attestation",
    "reader_provenance_of",
    "requirement_is_closed_by",
    "A_DOMAIN_KIND_IS_DERIVED_FROM_ATTESTATIONS_NOT_WRITTEN",
    "A_COLLISION_IN_THE_REPRESENTATION_IS_NOT_A_COLLISION_IN_CONTEXT_NOTE",
    "A_DESIGNED_DOMAIN_IS_NOT_A_LINGUISTIC_CERTIFICATE_NOTE",
    "A_DESIGNED_RUN",
    "A_DESIGNED_WITNESS_IS_NOT_AN_EXECUTED_CODEC_TEST_NOTE",
    "A_LOOKUP_READER_PROVES_INJECTIVITY_NOT_UNDERSTANDING_NOTE",
    "FOUR_FIELDS_CARRY_THREE_FUNCTIONS_NOTE",
    "MINIMAL_COMPLETE_FIBER_NAMED_RESIDUALS",
    "ONE_IS_A_NAMED_ATTRIBUTION_NOT_A_TRUE_PROPOSITION_NOTE",
    "THE_CLOSURE_CHECKLIST",
    "THE_DECLARED_DOMAIN",
    "THE_DECLARED_PREDICATE_SPACE",
    "THE_DESIGNED_WITNESSES",
    "THE_PREDICATE_SPACE_IS_DECLARED_NOT_MEASURED_NOTE",
    "THE_REFERENCE_READER",
    "THE_MINIMUM_IS_RELATIVE_TO_THE_TESTED_ALTERNATIVES_NOTE",
    "THE_RELATION_VOCABULARY_IS_NOT_CLAIMED_EXHAUSTIVE_NOTE",
    "ZERO_IS_AN_UNNAMED_RELATION_NOT_AN_EMPTY_FIBER_NOTE",
    "AttributionCandidate",
    "ChecklistCondition",
    "ClosureChecklist",
    "ClosureRequirement",
    "ConditionEvidence",
    "DeclaredDomain",
    "DeletedComponent",
    "DomainCase",
    "CaseAttestation",
    "DomainKind",
    "FiberElement",
    "MinimalCompleteFiberError",
    "MinimalCompleteFiberVerdict",
    "NecessityStanding",
    "NecessityWitnessPair",
    "Reader",
    "RelationKind",
    "Representation",
    "StructuralFunction",
    "SufficiencyExperimentResult",
    "SufficiencyStanding",
    "a_separate_genus_field_is_required",
    "assess_minimal_complete_fiber",
    "assess_sufficiency",
    "carried_functions",
    "classification_information_is_required",
    "delete",
    "deleting_representation",
    "full_representation",
    "genus_is_declared",
    "licensed_predicates",
    "lookup_reader",
    "registered_corpus_digests",
    "necessity_deletion_experiment",
    "necessity_standing_of",
    "predicate_is_licensed_for",
    "run_sufficiency_experiment",
]


class MinimalCompleteFiberError(ValueError):
    """رفضٌ صريح: شاهدٌ لا يتصادم، أو إسنادٌ بلا دليل، أو إغلاقٌ يُعلَن بلا شرطه."""


# --- المعادلةُ التأسيسيّة: الحقولُ الأربعةُ ووظائفُها الثلاث -------------------


class RelationKind(Enum):
    """وجهُ الربط مُعيَّنًا؛ ومفردتُها مفتوحةُ الذيل بتصريحٍ لا بإغفال.

    فالمعادلةُ نصّت «أو غير ذلك»، فلا تُقرَأ هذه الثلاثةُ حصرًا لأوجه الربط
    (`THE_RELATION_VOCABULARY_IS_NOT_CLAIMED_EXHAUSTIVE`).
    """

    PREDICATION = "إخبار"
    RESTRICTION = "تقييد"
    EVENTIVE = "علاقةٌ_حدثيّة"


class StructuralFunction(Enum):
    """الوظائفُ البنيويّةُ الثلاث؛ وهي أقلُّ من حقول التمثيل الأربعة."""

    IDENTITY_AND_CLASSIFICATION = "الهويّةُ_والتصنيف"
    PREDICATE = "المحمول"
    ATTRIBUTION = "الإسناد"


FIELD_FUNCTIONS: Final[dict[str, StructuralFunction]] = {
    "anchor": StructuralFunction.IDENTITY_AND_CLASSIFICATION,
    "genus": StructuralFunction.IDENTITY_AND_CLASSIFICATION,
    "predicate": StructuralFunction.PREDICATE,
    "relation": StructuralFunction.ATTRIBUTION,
}
"""أيُّ حقلٍ يحمل أيَّ وظيفة؛ وحقلان يشتركان في الأولى، فلذلك كانت ثلاثًا."""


def carried_functions() -> tuple[int, int]:
    """(عددُ الحقول، عددُ الوظائف)؛ مُشتقًّا بالعدّ لا مكتوبًا بجانب الجدول."""

    return len(FIELD_FUNCTIONS), len(set(FIELD_FUNCTIONS.values()))


def classification_information_is_required(genus_is_uniquely_derivable: bool) -> bool:
    """أتلزم **معلومةُ** التصنيف؟ نعم دائمًا، وإن لم يلزم **حقلٌ** باسم الجنس.

    فاشتقاقُ الجنس من المرساة بصورةٍ وحيدةٍ مرخَّصةٍ يرفع تكرارَ التخزين، ولا
    يرفع لزومَ المعلومة؛ والخلطُ بينهما هو الذي يُقرَأ إسقاطًا للتصنيف.
    """

    del genus_is_uniquely_derivable
    return True


def a_separate_genus_field_is_required(genus_is_uniquely_derivable: bool) -> bool:
    """أيلزم حقلٌ مستقلٌّ للجنس؟ لا، متى اشتُقَّ بصورةٍ وحيدةٍ مرخَّصة."""

    return not genus_is_uniquely_derivable


THE_DECLARED_PREDICATE_SPACE: Final[dict[str, frozenset[str]]] = {
    "عضوُ الإبصار": frozenset({"مُبصِرة", "غائرة", "كحلاء"}),
    "نبعُ الماء": frozenset({"غائرة", "عذبة", "جارية"}),
    "شخصٌ مُعيَّن": frozenset({"طويل", "قصير", "قائم"}),
}
"""`P(g)`: فضاءُ المحمولات الممكنة لكلّ جنسٍ مُعلَن؛ **مُعلَنٌ ههنا لا مقيسٌ**."""


def genus_is_declared(genus: str) -> bool:
    """أهذا الجنسُ مُعلَنٌ في `P`؟ فما لم يُعلَن لا يُفحَص توافقُه بل يُردّ."""

    return genus in THE_DECLARED_PREDICATE_SPACE


def licensed_predicates(genus: str) -> frozenset[str]:
    """`P(g)` لجنسٍ مُعلَن؛ وجنسٌ غيرُ مُعلَنٍ يُرفَض ولا يُعامَل فضاءً خاليًا."""

    if not genus_is_declared(genus):
        raise MinimalCompleteFiberError(
            "جنسٌ غيرُ مُعلَنٍ في `P`؛ ولا يُقرَأ عدمُ الإعلان فضاءً خاليًا"
        )
    return THE_DECLARED_PREDICATE_SPACE[genus]


def predicate_is_licensed_for(genus: str, predicate: str) -> bool:
    """أينتمي المحمولُ إلى `P(g)`؟ فاحصُ التوافق النوعيّ بين الجنس والمحمول.

    ولا يقيس هذا الفاحصُ عربيّةَ التركيب، بل ينظر في جدولٍ **مُعلَنٍ** ههنا
    (`THE_PREDICATE_SPACE_IS_DECLARED_NOT_MEASURED`).
    """

    return predicate.strip() in licensed_predicates(genus)


@dataclass(frozen=True, slots=True)
class FiberElement:
    """`u = (a, g, p, r)`؛ و`r = None` هي `⊥`، أي وجهُ ربطٍ لم يُعيَّن بعد."""

    anchor: str
    genus: str
    predicate: str
    relation: RelationKind | None

    def __post_init__(self) -> None:
        if not self.anchor.strip():
            raise MinimalCompleteFiberError("عنصرٌ بلا مرساةِ هويّةٍ لا يُكتَب")
        if not self.genus.strip():
            raise MinimalCompleteFiberError("عنصرٌ بلا جنسٍ مرخَّصٍ لا يُصنَّف")
        if not self.predicate.strip():
            raise MinimalCompleteFiberError("عنصرٌ بلا محمولٍ مرشَّحٍ لا يُحمَل عليه")

    @property
    def is_zero(self) -> bool:
        """أهو `Z = (a, g, p, ⊥)`؟ أي حاملٌ ومحمولٌ بلا وجهِ ربطٍ مُعيَّن."""

        return self.relation is None

    @property
    def is_an_empty_fiber(self) -> bool:
        """أهو ليفٌ خالٍ؟ لا — والجوابُ ثابتٌ بالبناء؛ فـ`zero` ليست خلوًّا."""

        return False


@dataclass(frozen=True, slots=True)
class AttributionCandidate:
    """`O = (a, g, p, r, e, ε)`: إسنادٌ مُعيَّنٌ بدليلٍ وبقايا، ولا صدقَ يُدَّعى."""

    element: FiberElement
    evidence: str
    residues: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.element.relation is None:
            raise MinimalCompleteFiberError(
                "إسنادٌ مُعيَّنٌ بلا وجهِ ربطٍ مُسمًّى تناقضٌ؛ وتلك حالُ `zero` لا `one`"
            )
        if not self.evidence.strip():
            raise MinimalCompleteFiberError("إسنادٌ بلا دليلٍ مكتوبٍ لا يُودَع")

    @property
    def asserts_the_proposition_is_true(self) -> bool:
        """أتدّعي صدقَ القضيّة في الواقع؟ لا — والتعيينُ غيرُ التصديق."""

        return False


# --- إسقاطاتُ الحذف الثلاثة ---------------------------------------------------


class DeletedComponent(Enum):
    """`I`: المعلوماتُ المستقلّةُ التي يُختبَر حذفُها، بعد إزالة التكرار بينها."""

    CLASSIFICATION = "التصنيف"
    PREDICATE = "المحمول"
    RELATION = "نوعُ_الربط"


def delete(
    element: FiberElement, component: DeletedComponent
) -> tuple[str | None, ...]:
    """`T_{-i}(u)`: مخرجُ التمثيل بعد إسقاط معلومات المكوّن المُسمّى وحدَه."""

    relation = None if element.relation is None else element.relation.value
    if component is DeletedComponent.CLASSIFICATION:
        return (element.anchor, None, element.predicate, relation)
    if component is DeletedComponent.PREDICATE:
        return (element.anchor, element.genus, None, relation)
    if component is DeletedComponent.RELATION:
        return (element.anchor, element.genus, element.predicate, None)
    raise MinimalCompleteFiberError("مكوّنٌ غيرُ مُسمًّى؛ ولا يُسقَط ما لا يُسمّى")


class DomainKind(Enum):
    """جنسُ المجال، **مُشتقًّا** من شواهد حالاته لا مكتوبًا عليه."""

    DESIGNED_DOMAIN = "مجالٌ_مصمَّمٌ_لاختبار_التمثيل"
    UNDECIDED_DOMAIN = "مجالٌ_ادُّعي_توثيقُه_ولم_يُحسَم"
    DECLARED_LINGUISTIC_DOMAIN = "مجالٌ_لغويٌّ_مُعلَنٌ_ومُبصَّم"


class AttestationStanding(Enum):
    """حالُ توثيق حالةٍ بعد **فحصٍ مُجرًى** على ثلاث جهاتٍ مترابطة."""

    NO_ATTESTATION_OFFERED = "لا_شاهدَ_ورودٍ_مُقدَّم"
    SOURCE_IS_NOT_REGISTERED = "مصدرٌ_ليس_مُسجَّلًا_في_الشجرة"
    SOURCE_DIGEST_DOES_NOT_MATCH = "بصمةُ_المصدر_لا_تُطابِق"
    LOCATOR_DOES_NOT_RESOLVE = "محدِّدُ_الموضع_لا_يُحَلّ"
    OCCURRENCE_DOES_NOT_MATCH_THE_ANCHOR = "الوقوعُ_لا_يُطابِق_المرساة"
    NO_GLOSS_AT_THIS_LOCATOR = "لا_وسمَ_عند_هذا_الموضع"
    THE_GLOSS_IS_AUTHORED_BY_THE_DOMAIN_DECLARER = "الوسمُ_كتبه_مُعلِنُ_المجال"
    THE_GLOSS_DISAGREES_WITH_THE_CASE = "الوسمُ_يخالف_جنسَ_الحالة_أو_محمولَها_أو_مضمونَها"
    ATTESTED_BY_AN_INDEPENDENT_GLOSS = "موثَّقةٌ_بوسمٍ_من_جهةٍ_غيرِ_مُعلِن_المجال"


def registered_corpus_digests() -> dict[str, str]:
    """بصماتُ المدوّنات المُسجَّلةِ في الشجرة، **محسوبةً الآن** من بايتاتها.

    فالمصدرُ لا يُصدَّق باسمه: إن لم يكن في هذه المقابلة فليس مدوّنةً في هذه
    الشجرة، وإن كان فبصمتُه تُعاد حوسبتُها عند كلّ فحص.
    """

    return {FATIHA_SOURCE_ID: fatiha_source_sha256()}


@dataclass(frozen=True, slots=True)
class CaseAttestation:
    """شاهدُ ورودٍ لحالة: مدوّنةٌ مُسجَّلةٌ، وبصمتُها، وموضعُ الورود فيها.

    وموضعُه **محدِّدٌ يُحَلّ** لا نصٌّ يُقرَأ: سطرٌ ومجالٌ نصفُ مفتوحٍ بنقاط
    الشفرة بعد التسوية المُعلَنة؛ فلا يُكتفى بكون الموضع نصًّا غيرَ فارغ.
    """

    source_id: str
    source_sha256: str
    locator: SourceLocator

    def __post_init__(self) -> None:
        if not self.source_id.strip():
            raise MinimalCompleteFiberError("شاهدُ ورودٍ بلا مصدرٍ مُسمًّى")
        if not isinstance(self.locator, SourceLocator):
            raise MinimalCompleteFiberError(
                "شاهدُ ورودٍ بموضعٍ لا يُحَلّ؛ والموضعُ محدِّدٌ مفحوصٌ لا عبارةٌ مكتوبة"
            )
        if len(self.source_sha256) != 64 or any(
            character not in "0123456789abcdef" for character in self.source_sha256
        ):
            raise MinimalCompleteFiberError(
                "بصمةٌ ليست `sha256` سداسيًّا صغيرًا بأربعٍ وستّين خانة"
            )

    @property
    def digest_matches_the_tree(self) -> bool:
        """أوافقت بصمتُه بصمةَ مدوّنةٍ مُسجَّلةٍ محسوبةً الآن؟ لا يُقرَأ من اسمه."""

        return registered_corpus_digests().get(self.source_id) == self.source_sha256

    @property
    def source_is_registered(self) -> bool:
        """أهذا المصدرُ مُسجَّلٌ في الشجرة أصلًا؟ يُفحَص قبل البصمة."""

        return self.source_id in registered_corpus_digests()

    @property
    def resolved_surface(self) -> str | None:
        """السطحُ الواقعُ عند الموضع، محلولًا الآن؛ وتعذُّرُ الحلّ `None` مُسمًّى."""

        return resolve_locator(self.source_id, self.locator)


@dataclass(frozen=True, slots=True)
class DomainCase:
    """حالةٌ واحدة `x`: عنصرُها، ومضمونُ إفادتها `F(x)`، ومقامُها، وشاهدُ ورودها."""

    element: FiberElement
    content: str
    context: str
    attestation: CaseAttestation | None = None

    def __post_init__(self) -> None:
        if not self.content.strip():
            raise MinimalCompleteFiberError("حالةٌ بلا مضمونِ إفادةٍ مكتوبٍ لا تُقابَل")
        if not self.context.strip():
            raise MinimalCompleteFiberError(
                "حالةٌ بلا مقامٍ محدَّدٍ لا تُختبَر؛ فالمقامُ شرطُ تثبيت المجال"
            )
        if not predicate_is_licensed_for(self.element.genus, self.element.predicate):
            raise MinimalCompleteFiberError(
                "محمولٌ خارجَ `P(g)`؛ والتوافقُ النوعيُّ شرطُ دخولِ المجال"
            )

    def gloss_agrees(self, gloss: GlossEntry) -> bool:
        """أيوافق الوسمُ جنسَ الحالة ومحمولَها ومضمونَ إفادتها جميعًا؟"""

        return (
            normalize(gloss.genus.strip()) == normalize(self.element.genus.strip())
            and normalize(gloss.predicate.strip())
            == normalize(self.element.predicate.strip())
            and normalize(gloss.content.strip()) == normalize(self.content.strip())
        )


def assess_attestation(
    case: DomainCase, declarer_id: str, registry: GlossRegistry
) -> AttestationStanding:
    """افحص توثيقَ حالةٍ على ثلاث جهاتٍ مترابطة، وسمِّ أوّلَ ما تخلّف منها.

    الجهاتُ: تطابقُ بصمة المصدر المُسجَّل، ووقوعٌ **يُحَلّ** عند محدِّد موضعٍ
    صالحٍ يطابق مرساةَ الحالة، ووسمٌ مستقلٌّ عن مُعلِن المجال يربط ذلك الوقوعَ
    بالجنس والمحمول والمضمون المقصود. وسقوطُ واحدةٍ يمنع الرفعَ إلى موثَّقة،
    ولا تُجبَر جهةٌ بأخرى (`AN_OCCURRENCE_IS_NOT_A_GLOSS`).
    """

    attestation = case.attestation
    if attestation is None:
        return AttestationStanding.NO_ATTESTATION_OFFERED
    if not attestation.source_is_registered:
        return AttestationStanding.SOURCE_IS_NOT_REGISTERED
    if not attestation.digest_matches_the_tree:
        return AttestationStanding.SOURCE_DIGEST_DOES_NOT_MATCH
    surface = attestation.resolved_surface
    if surface is None:
        return AttestationStanding.LOCATOR_DOES_NOT_RESOLVE
    if normalize(surface) != normalize(case.element.anchor):
        return AttestationStanding.OCCURRENCE_DOES_NOT_MATCH_THE_ANCHOR
    gloss = registry.lookup(attestation.source_id, attestation.locator)
    if gloss is None:
        return AttestationStanding.NO_GLOSS_AT_THIS_LOCATOR
    if registry.authority_id.strip() == declarer_id.strip():
        return AttestationStanding.THE_GLOSS_IS_AUTHORED_BY_THE_DOMAIN_DECLARER
    if not case.gloss_agrees(gloss):
        return AttestationStanding.THE_GLOSS_DISAGREES_WITH_THE_CASE
    return AttestationStanding.ATTESTED_BY_AN_INDEPENDENT_GLOSS


def the_deposited_gloss_registry() -> GlossRegistry:
    """سجلُّ الوسم المُودَع في الشجرة، مقروءًا الآن ببصمةٍ مُعادةِ الحوسبة."""

    return in_tree_gloss_registry()


@dataclass(frozen=True, slots=True)
class DeclaredDomain:
    """`𝒟` مع `F`: مجالٌ مُعلَنٌ قبل التجربة، وجنسُه **مُشتَقٌّ** لا مكتوب.

    و`declarer_id` هويّةُ مُعلِن المجال؛ تُكتَب لتُقارَن بجهة الوسم، فيُردّ وسمٌ
    كتبه صاحبُ الدعوى على دعواه (`A_SELF_AUTHORED_GLOSS_IS_REFUSED`).
    """

    identifier: str
    declarer_id: str
    cases: tuple[DomainCase, ...]

    def __post_init__(self) -> None:
        if not self.identifier.strip():
            raise MinimalCompleteFiberError("مجالٌ بلا اسمٍ لا يُحال عليه")
        if not self.declarer_id.strip():
            raise MinimalCompleteFiberError(
                "مجالٌ بلا مُعلِنٍ مُسمًّى لا تُقارَن جهةُ وسمه به فيُقرَأ مستقلًّا"
            )
        if not self.cases:
            raise MinimalCompleteFiberError("مجالٌ خالٍ تُثبَت عليه كلُّ دعوى")
        elements = tuple(item.element for item in self.cases)
        if len(set(elements)) != len(elements):
            raise MinimalCompleteFiberError(
                "عنصرٌ تكرّر في المجال؛ والتكرارُ يُخفي تعارضَ المضمون"
            )

    def attestation_standings(
        self, registry: GlossRegistry | None = None
    ) -> tuple[AttestationStanding, ...]:
        """حالُ توثيق كلّ حالةٍ، مفحوصًا الآن على سجلّ وسمٍ مُسمًّى."""

        book = the_deposited_gloss_registry() if registry is None else registry
        return tuple(
            assess_attestation(case, self.declarer_id, book) for case in self.cases
        )

    def kind_against(self, registry: GlossRegistry | None = None) -> DomainKind:
        """جنسُ المجال على سجلّ وسمٍ مُسمًّى؛ مُشتقًّا بالفحص لا مكتوبًا.

        ولا حقلَ يكتب فيه صاحبُ المجال جنسَه؛ فالتسميةُ الكاذبة ليست مرفوضةً
        بعد وقوعها بل **غيرُ قابلةٍ للقول**. وما بين المصمَّم واللغويّ المُعلَن
        منزلةٌ ثالثةٌ مُسمّاة: مجالٌ ادُّعي توثيقُه ولم يُحسَم، فلا يُقرَأ
        تخلُّفُ جهةٍ من جهات التوثيق تصميمًا يُطمئَنّ إليه.
        """

        standings = self.attestation_standings(registry)
        if all(
            item is AttestationStanding.ATTESTED_BY_AN_INDEPENDENT_GLOSS
            for item in standings
        ):
            return DomainKind.DECLARED_LINGUISTIC_DOMAIN
        if all(
            item is AttestationStanding.NO_ATTESTATION_OFFERED for item in standings
        ):
            return DomainKind.DESIGNED_DOMAIN
        return DomainKind.UNDECIDED_DOMAIN

    @property
    def kind(self) -> DomainKind:
        """جنسُ المجال على سجلّ الوسم المُودَع في الشجرة."""

        return self.kind_against()

    def attested_case_count_against(self, registry: GlossRegistry | None = None) -> int:
        """عددُ الحالات الموثَّقة بوسمٍ مستقلٍّ، مُشتقًّا بالعدّ."""

        return sum(
            1
            for item in self.attestation_standings(registry)
            if item is AttestationStanding.ATTESTED_BY_AN_INDEPENDENT_GLOSS
        )

    @property
    def attested_case_count(self) -> int:
        """عددُ الحالات الموثَّقة على سجلّ الوسم المُودَع."""

        return self.attested_case_count_against()

    @property
    def case_count(self) -> int:
        """عددُ حالات المجال، مُشتقًّا بالعدّ."""

        return len(self.cases)


Representation = Callable[[FiberElement], tuple[str | None, ...]]
"""`T`: تمثيلٌ يُرجِع مخرجًا مجرَّدًا؛ ولا يُمرَّر العنصرُ نفسُه إلى القارئ."""

Reader = Callable[[tuple[str | None, ...]], str]
"""`D`: قارئٌ لا يرى إلّا `T(x)`؛ والحجبُ بنيويٌّ في شكل النداء لا بالوصيّة."""


def full_representation(element: FiberElement) -> tuple[str | None, ...]:
    """`T`: المخرجُ الكامل `(a, g, p, r)` بلا إسقاطِ مكوّن."""

    relation = None if element.relation is None else element.relation.value
    return (element.anchor, element.genus, element.predicate, relation)


def deleting_representation(component: DeletedComponent) -> Representation:
    """`T_{-i}`: تمثيلٌ يُسقِط معلوماتِ المكوّن المُسمّى وحدَه."""

    def representation(element: FiberElement) -> tuple[str | None, ...]:
        return delete(element, component)

    return representation


class SufficiencyStanding(Enum):
    """حالُ شطر الكفاية بعد **إجراء** التجربة، لا بعد فحص الأسماء."""

    NO_INDEPENDENT_READER_IN_THIS_TREE = "لا_قارئَ_مستقلًّا_في_هذه_الشجرة"
    HELD_ON_A_DECLARED_DOMAIN = "قائمةٌ_على_مجالٍ_مُعلَن"
    REFUTED_ON_A_DECLARED_DOMAIN = "منتقضةٌ_على_مجالٍ_مُعلَن"


class ReaderProvenance(Enum):
    """منشأُ القارئ، **مُشتقًّا من آليّةٍ** لا موسومًا بيدِ مستدعيه."""

    BUILT_FROM_THE_DOMAIN_TARGET_TABLE = "مبنيٌّ_من_جدول_أهداف_المجال"
    FIXED_BEFORE_THE_EVALUATION_DATA = "قاعدتُه_مثبَّتةٌ_قبل_بيانات_التقييم"
    UNDECLARED_PROVENANCE = "منشأٌ_غيرُ_مُعلَن"


class ReaderRuleOrigin(Enum):
    """من أين جاءت قاعدةُ القارئ: من ختمٍ سابقٍ لكلّ حالة، أم من جدولِ حالات."""

    SEALED_BEFORE_ANY_CASE = "مختومةٌ_قبل_كلّ_حالة"
    A_TABLE_BUILT_FROM_CASES = "جدولٌ_مبنيٌّ_من_حالات"


@dataclass(frozen=True, slots=True)
class SealedReaderRule:
    """قاعدةُ قراءةٍ مختومةٌ مع **ما رأته من حالات**، محسوبًا لا مُصرَّحًا به.

    ولا يُمرَّر إلى هذه البنية جدولُ ما رآه القارئُ من خارجها: إمّا أن تُختَم
    قاعدةٌ مغلقةٌ لم تُعطَ حالةً قطّ، وإمّا أن يبنيَ هذا الإيداعُ الجدولَ من
    شطرِ تدريبٍ مُسمًّى فيعرف بالبناء ما رآه.
    """

    rule_note: str
    origin: ReaderRuleOrigin
    disclosed_elements: frozenset[FiberElement]
    _rule: Reader

    def __post_init__(self) -> None:
        if not self.rule_note.strip():
            raise MinimalCompleteFiberError("قاعدةٌ بلا بيانٍ مكتوبٍ لا تُراجَع")
        if (
            self.origin is ReaderRuleOrigin.SEALED_BEFORE_ANY_CASE
            and self.disclosed_elements
        ):
            raise MinimalCompleteFiberError(
                "قاعدةٌ يُدّعى ختمُها قبل الحالات وقد رأت حالاتٍ؛ والدعوى تناقض بناءها"
            )


def a_rule_sealed_before_any_case(rule: Reader, rule_note: str) -> SealedReaderRule:
    """اختِم قاعدةً مغلقةً لم تُعطَ حالةً قطّ؛ فما رأته من الحالات خالٍ بالبناء.

    وهذا الختمُ يضبط **مدخلَ** القاعدة لا ذاكرتَها: لا سبيل لهذه الوحدة أن تفحص
    جوفَ دالّةٍ مكتوبةٍ بلغة البرمجة، فتبقى صحّةُ كونِها مغلقةً مقروءةً من
    شفرتها لا مبرهنةً ههنا (`A_SEALED_RULE_IS_CHECKED_FOR_OVERLAP_NOT_FOR_MEMORY`).
    """

    return SealedReaderRule(
        rule_note=rule_note,
        origin=ReaderRuleOrigin.SEALED_BEFORE_ANY_CASE,
        disclosed_elements=frozenset(),
        _rule=rule,
    )


def a_rule_trained_on(
    training_domain: DeclaredDomain, representation: Representation, rule_note: str
) -> SealedReaderRule:
    """ابنِ جدولَ قراءةٍ من شطر تدريبٍ مُسمًّى؛ وما رآه يُحسَب من بنائه لا يُعلَن.

    والمخرجُ المدموجُ في شطر التدريب يُترَك بلا جواب، فيُردّ عنه نصٌّ فارغٌ
    يُخالف كلَّ مضمون.
    """

    table: dict[tuple[str | None, ...], set[str]] = {}
    for case in training_domain.cases:
        table.setdefault(representation(case.element), set()).add(case.content)
    answers = {
        output: next(iter(contents))
        for output, contents in table.items()
        if len(contents) == 1
    }

    def rule(output: tuple[str | None, ...]) -> str:
        return answers.get(output, "")

    return SealedReaderRule(
        rule_note=rule_note,
        origin=ReaderRuleOrigin.A_TABLE_BUILT_FROM_CASES,
        disclosed_elements=frozenset(case.element for case in training_domain.cases),
        _rule=rule,
    )


@dataclass(frozen=True, slots=True)
class ProvenancedReader:
    """قارئٌ حُجِب عن مجالِ تقييمٍ مُسمًّى؛ ومنشؤه **مُشتَقٌّ** من الحجب نفسِه.

    فلا حقلَ يُكتَب فيه «مستقلّ»: يُقارَن ما رأته القاعدةُ من حالاتٍ بحالات
    مجال التقييم، فإن تقاطعا فالقارئُ مبنيٌّ ممّا يُقيَّم عليه، وإن انفصلا
    فقاعدتُه سابقةٌ لبيانات التقييم بالبناء.
    """

    rule: SealedReaderRule
    evaluation_elements: frozenset[FiberElement]

    @property
    def leaked_elements(self) -> frozenset[FiberElement]:
        """حالاتُ التقييم التي رأتها القاعدةُ قبلها، مُشتقّةً بالتقاطع."""

        return self.rule.disclosed_elements & self.evaluation_elements

    @property
    def is_held_out(self) -> bool:
        """أحُجِب عن مجال تقييمه؟ يُقرَأ من خلوّ التقاطع لا من وصفٍ مكتوب."""

        return not self.leaked_elements

    @property
    def rule_note(self) -> str:
        """بيانُ قاعدة القارئ، مقروءًا من ختمها."""

        return self.rule.rule_note

    @property
    def provenance(self) -> ReaderProvenance:
        """منشأُ القارئ، مُشتقًّا من آليّة الختم والحجب لا من وسمٍ يُعطى."""

        if not self.is_held_out:
            return ReaderProvenance.BUILT_FROM_THE_DOMAIN_TARGET_TABLE
        return ReaderProvenance.FIXED_BEFORE_THE_EVALUATION_DATA

    def __call__(self, output: tuple[str | None, ...]) -> str:
        return self.rule._rule(output)


def reader_provenance_of(reader: Reader) -> ReaderProvenance:
    """منشأُ القارئ، مُشتقًّا من نوعه؛ وقارئٌ لا يُعلِن منشأه لا يُفترَض مستقلًّا."""

    if isinstance(reader, ProvenancedReader):
        return reader.provenance
    return ReaderProvenance.UNDECLARED_PROVENANCE


def hold_out_reader(
    rule: SealedReaderRule, evaluation_domain: DeclaredDomain
) -> ProvenancedReader:
    """احجِب قاعدةً مختومةً عن مجال تقييمٍ مُسمًّى، ثمّ اقرأ منشأها من الحجب.

    وهذه هي السبيلُ الوحيدةُ إلى `FIXED_BEFORE_THE_EVALUATION_DATA`: لا تُعطى
    بالتسمية، وإنّما تُشتَقّ من انفصال ما رأته القاعدةُ عمّا تُقيَّم عليه
    (`READER_INDEPENDENCE_IS_A_MECHANISM_NOT_A_LABEL`).
    """

    return ProvenancedReader(
        rule=rule,
        evaluation_elements=frozenset(
            case.element for case in evaluation_domain.cases
        ),
    )


@dataclass(frozen=True, slots=True)
class SufficiencyExperimentResult:
    """نتيجةُ تجربةٍ مُجراةٍ: مخرجاتٌ مدموجة، ومواضعُ اختلافِ القارئ عن الهدف."""

    domain_identifier: str
    domain_kind: DomainKind
    reader_provenance: ReaderProvenance
    distinct_output_count: int
    merged_contents: tuple[tuple[str, ...], ...]
    mismatched_contents: tuple[str, ...]
    standing: SufficiencyStanding

    @property
    def no_reader_can_exist(self) -> bool:
        """أيستحيل قارئٌ أصلًا؟ نعم متى دمج التمثيلُ مضمونين مختلفين."""

        return bool(self.merged_contents)


def run_sufficiency_experiment(
    domain: DeclaredDomain, representation: Representation, reader: Reader
) -> SufficiencyExperimentResult:
    """أجرِ `D(T(x)) ≟ F(x)` على `𝒟`، ولا يُمرَّر إلى `D` إلّا `T(x)`.

    والحجبُ ليس وصيّةً: يُنادى القارئُ **مرّةً واحدةً لكلّ مخرجٍ متمايز**، ثمّ
    تُقابَل قيمتُه بمضمون كلّ حالةٍ تشترك في ذلك المخرج. فلو دمج التمثيلُ
    حالتين مختلفتَي المضمون لَعجز أيُّ قارئٍ عن ردّهما، إذ لا يملك ما يفرّق به؛
    فالدمجُ يُسجَّل نقضًا للكفاية قبل سؤال القارئ أصلًا.
    """

    grouped: dict[tuple[str | None, ...], list[DomainCase]] = {}
    for case in domain.cases:
        grouped.setdefault(representation(case.element), []).append(case)

    merged: list[tuple[str, ...]] = []
    mismatched: list[str] = []
    for output, cases in grouped.items():
        contents = tuple(sorted({case.content for case in cases}))
        if len(contents) > 1:
            merged.append(contents)
            continue
        answer = reader(output)
        if answer != cases[0].content:
            mismatched.append(cases[0].content)

    if merged or mismatched:
        standing = SufficiencyStanding.REFUTED_ON_A_DECLARED_DOMAIN
    else:
        standing = SufficiencyStanding.HELD_ON_A_DECLARED_DOMAIN

    return SufficiencyExperimentResult(
        domain_identifier=domain.identifier,
        domain_kind=domain.kind,
        reader_provenance=reader_provenance_of(reader),
        distinct_output_count=len(grouped),
        merged_contents=tuple(merged),
        mismatched_contents=tuple(mismatched),
        standing=standing,
    )


def lookup_reader(domain: DeclaredDomain, representation: Representation) -> Reader:
    """قارئٌ مُعلَنٌ بجدولٍ من مخرجات التمثيل إلى المضمون؛ ولا يرى الأصل.

    والمخرجُ المدموجُ يُترَك بلا جواب، فيُردّ عنه نصٌّ فارغٌ يُخالف كلَّ مضمون؛
    وهذا قارئٌ **أفضلُ ما يمكن** على هذا الجدول، ويثبت تباينَ التمثيل لا فهمَه
    (`A_LOOKUP_READER_PROVES_INJECTIVITY_NOT_UNDERSTANDING`).
    """

    return hold_out_reader(
        a_rule_trained_on(
            domain,
            representation,
            "جدولٌ من مخرجات التمثيل إلى مضمون المجال نفسِه؛ يثبت تباينَ `T` "
            "ولا يُغلِق شرطَ القارئ المستقلّ بحال",
        ),
        domain,
    )


@dataclass(frozen=True, slots=True)
class NecessityWitnessPair:
    """شاهدا ضرورةٍ: يتصادمان تحت `T_{-i}` ويختلف مضمونُ إفادتهما.

    والتصادمُ مفحوصٌ بالبناء لا مُصرَّحٌ به؛ فزوجٌ لا يتصادم لا يشهد بضرورة،
    وزوجٌ متّفقُ المضمون لا يحتاج مخرجين فلا يُفنِّد حذفًا.
    """

    component: DeletedComponent
    first: FiberElement
    second: FiberElement
    first_content: str
    second_content: str
    context: str
    scope_note: str

    def __post_init__(self) -> None:
        if not self.first_content.strip() or not self.second_content.strip():
            raise MinimalCompleteFiberError("شاهدٌ بلا مضمونِ إفادةٍ مكتوبٍ لا يُقابَل")
        if not self.context.strip():
            raise MinimalCompleteFiberError(
                "شاهدٌ بلا مقامٍ محدَّدٍ لا يُختبَر؛ فالمقامُ يُثبَّت قبل الحذف"
            )
        if not self.scope_note.strip():
            raise MinimalCompleteFiberError(
                "شاهدٌ بلا نطاقٍ مكتوبٍ يُقرَأ بعد حين شهادةَ تنفيذٍ على المِرماز"
            )
        for element in (self.first, self.second):
            if not predicate_is_licensed_for(element.genus, element.predicate):
                raise MinimalCompleteFiberError(
                    "محمولٌ خارجَ `P(g)`؛ وشاهدٌ غيرُ متوافقٍ نوعيًّا لا يُقابِل مثلَه"
                )
        if self.first == self.second:
            raise MinimalCompleteFiberError("عنصرٌ لا يشهد على نفسه")
        if delete(self.first, self.component) != delete(self.second, self.component):
            raise MinimalCompleteFiberError(
                "شاهدان لا يتصادمان تحت الإسقاط لا يُثبتان ضرورةً؛ فاختلافُهما "
                "باقٍ في المخرج، والقارئُ قد يردُّ المخرجين"
            )
        if self.first_content.strip() == self.second_content.strip():
            raise MinimalCompleteFiberError(
                "شاهدان متّفقا المضمون لا يحتاجان مخرجين؛ ولا تُفنَّد بهما عمليّةُ حذف"
            )

    @property
    def collides_under_deletion(self) -> bool:
        """أيتصادمان تحت `T_{-i}`؟ نعم بالبناء، وإلّا لم يُنشَأ الشاهد."""

        return True

    @property
    def the_deleted_information_is_copied_in_another_field(self) -> bool:
        """أنُسخ المحذوفُ في حقلٍ آخرَ ههنا؟ لا — وإلّا لَما تصادم الإسقاط."""

        return False

    @property
    def cases(self) -> tuple[DomainCase, ...]:
        """حالتا الشاهد داخلتين في مجالٍ مُعلَن، بمقامٍ واحدٍ مثبَّتٍ لهما."""

        return (
            DomainCase(
                element=self.first, content=self.first_content, context=self.context
            ),
            DomainCase(
                element=self.second, content=self.second_content, context=self.context
            ),
        )


THE_DESIGNED_WITNESSES: Final[tuple[NecessityWitnessPair, ...]] = (
    NecessityWitnessPair(
        component=DeletedComponent.CLASSIFICATION,
        first=FiberElement(
            anchor="عين",
            genus="عضوُ الإبصار",
            predicate="غائرة",
            relation=RelationKind.PREDICATION,
        ),
        second=FiberElement(
            anchor="عين",
            genus="نبعُ الماء",
            predicate="غائرة",
            relation=RelationKind.PREDICATION,
        ),
        first_content="الإخبارُ بغؤور عضو الإبصار",
        second_content="الإخبارُ بغؤور نبع الماء",
        context="«عينٌ غائرة» مُفرَدةً، بلا قرينةٍ سابقةٍ تعيّن المجالَ المفهوميّ",
        scope_note=(
            "تصميمُ شاهدٍ مضادٍّ لحذف التصنيف: تطابقُ الدالّ لا يعيّن المجالَ "
            "المفهوميّ؛ ويلزم عند التنفيذ تثبيتُ المجال والسياق ومنعُ استعادة "
            "التصنيف من الأصل"
        ),
    ),
    NecessityWitnessPair(
        component=DeletedComponent.PREDICATE,
        first=FiberElement(
            anchor="زيد",
            genus="شخصٌ مُعيَّن",
            predicate="طويل",
            relation=RelationKind.PREDICATION,
        ),
        second=FiberElement(
            anchor="زيد",
            genus="شخصٌ مُعيَّن",
            predicate="قصير",
            relation=RelationKind.PREDICATION,
        ),
        first_content="الإخبارُ بطول زيد",
        second_content="الإخبارُ بقِصَر زيد",
        context="خبرٌ عن مرجعٍ مثبَّتٍ واحدٍ، ونوعُ الإسناد مثبَّتٌ إخبارًا",
        scope_note=(
            "تصميمُ شاهدٍ مضادٍّ لحذف المحمول مع تثبيت المرجع ونوع الإسناد؛ "
            "فحذفُ الفرق بين المحمولين يدمج مضمونين مختلفين"
        ),
    ),
    NecessityWitnessPair(
        component=DeletedComponent.RELATION,
        first=FiberElement(
            anchor="الرجل",
            genus="شخصٌ مُعيَّن",
            predicate="طويل",
            relation=RelationKind.RESTRICTION,
        ),
        second=FiberElement(
            anchor="الرجل",
            genus="شخصٌ مُعيَّن",
            predicate="طويل",
            relation=RelationKind.PREDICATION,
        ),
        first_content="تعيينُ رجلٍ بوصفه: «الرجل الطويل»",
        second_content="الإخبارُ عن الرجل بالطول: «الرجل طويل»",
        context="مرجعٌ ومحمولٌ مثبَّتان، والفرقُ في وجه الربط وحدَه",
        scope_note=(
            "تصميمُ شاهدٍ مضادٍّ لحذف نوع الربط: تشترك العبارتان في المفهومين "
            "ويفترقان في التقييد والإخبار، فحذفُ الفرق يُفقِد معلومةً لازمة"
        ),
    ),
)
"""ثلاثةُ أزواجٍ مصمَّمةٍ، تصادمُها مفحوصٌ عند الإنشاء؛ وهي تصميمٌ لا تنفيذ."""


THE_DOMAIN_DECLARER_ID: Final[str] = "alghanem-in-tree-deposit"
"""مُعلِنُ المجالات المكتوبة ههنا؛ يُسمّى ليُقارَن بجهة الوسم فيُردّ اتّحادُهما."""


THE_DECLARED_DOMAIN: Final[DeclaredDomain] = DeclaredDomain(
    identifier="المجالُ المصمَّم لشواهد الحذف الثلاثة",
    declarer_id=THE_DOMAIN_DECLARER_ID,
    cases=tuple(case for item in THE_DESIGNED_WITNESSES for case in item.cases),
)
"""`𝒟` مُعلَنٌ بحالاته ومقاماته؛ وهو **مصمَّمٌ** لاختبار التمثيل لا مدوّنةٌ عربيّة."""


THE_REFERENCE_READER: Final[Reader] = lookup_reader(
    THE_DECLARED_DOMAIN, full_representation
)
"""`D` مُعلَنٌ على المخرج الكامل؛ لا يرى إلّا `T(x)`، ولا يُمرَّر إليه الأصل."""


def assess_sufficiency(
    domain: DeclaredDomain = THE_DECLARED_DOMAIN,
    representation: Representation = full_representation,
    reader: Reader = THE_REFERENCE_READER,
) -> SufficiencyStanding:
    """أثبتت `D(T(x)) = F(x)`؟ يُجاب بإجراء التجربة لا بفحص أسماء الواجهة."""

    return run_sufficiency_experiment(domain, representation, reader).standing


class NecessityStanding(Enum):
    """حالُ ضرورةِ مكوّن؛ والمشهودُ على مجالٍ مصمَّمٍ غيرُ المشهود على المِرماز."""

    WITNESSED_ON_THE_DESIGNED_PAIRS = "مشهودةٌ_على_الأزواج_المصمَّمة"
    NOT_WITNESSED = "لا_شاهدَ_لها_ههنا"


def necessity_deletion_experiment(
    component: DeletedComponent, domain: DeclaredDomain = THE_DECLARED_DOMAIN
) -> SufficiencyExperimentResult:
    """أجرِ تجربةَ الكفاية على `T_{-i}` بأفضلِ قارئٍ ممكنٍ على ذلك التمثيل.

    فلو انتقضت الكفايةُ بعد الإسقاط، وكان القارئُ المُقابَلُ هو **أفضلَ** ما
    يمكن بناؤه على مخرجات `T_{-i}` نفسِها، لم يبقَ للنقض سببٌ إلّا الإسقاط.
    """

    representation = deleting_representation(component)
    return run_sufficiency_experiment(
        domain, representation, lookup_reader(domain, representation)
    )


def necessity_standing_of(
    component: DeletedComponent, domain: DeclaredDomain = THE_DECLARED_DOMAIN
) -> NecessityStanding:
    """أمشهودةٌ ضرورةُ هذا المكوّن؟ تُقرَأ من نقضِ تجربةٍ مُجراةٍ لا من وجود زوج."""

    result = necessity_deletion_experiment(component, domain)
    if result.standing is SufficiencyStanding.REFUTED_ON_A_DECLARED_DOMAIN:
        return NecessityStanding.WITNESSED_ON_THE_DESIGNED_PAIRS
    return NecessityStanding.NOT_WITNESSED


@dataclass(frozen=True, slots=True)
class MinimalCompleteFiberVerdict:
    """حكمُ المعيار بشطريه على مجالٍ مُسمًّى؛ ولا يُرفَع الحكمُ فوق مجاله."""

    domain: DeclaredDomain
    sufficiency: SufficiencyStanding
    necessity: tuple[tuple[DeletedComponent, NecessityStanding], ...]

    def __post_init__(self) -> None:
        components = tuple(item for item, _ in self.necessity)
        if len(set(components)) != len(components):
            raise MinimalCompleteFiberError("مكوّنٌ تكرّر في الحكم؛ والتكرارُ يُخفي نقصًا")
        if set(components) != set(DeletedComponent):
            raise MinimalCompleteFiberError(
                "المكوّناتُ تُحكَم كلُّها أو لا تُحكَم؛ وإسقاطُ واحدٍ إثباتٌ صامتٌ لضرورته"
            )

    @property
    def domain_identifier(self) -> str:
        """اسمُ المجال، مُشتقًّا من المجال نفسِه؛ فلا يُحكَم بلا مجالٍ يُحال عليه."""

        return self.domain.identifier

    @property
    def domain_kind(self) -> DomainKind:
        """جنسُ المجال، مُشتقًّا من شواهده؛ ولا يُكتَب في الحكم فيُفتَح به الباب."""

        return self.domain.kind

    @property
    def every_component_is_witnessed(self) -> bool:
        """أمشهودةٌ ضرورةُ المكوّنات كلِّها على هذا المجال؟ يُعَدّ ولا يُدَّعى."""

        return all(
            standing is NecessityStanding.WITNESSED_ON_THE_DESIGNED_PAIRS
            for _, standing in self.necessity
        )

    @property
    def is_established_on_its_domain(self) -> bool:
        """أثبت شطرا المعيار على هذا المجال وحدَه؟ يُقرَأ من نتيجتي التجربتين."""

        return (
            self.sufficiency is SufficiencyStanding.HELD_ON_A_DECLARED_DOMAIN
            and self.every_component_is_witnessed
        )

    @property
    def meets_the_recorded_certificate_conditions(self) -> bool:
        """أاستوفى ما سُجِّل ههنا من شروط الشهادة؟ لا ما دام المجالُ مصمَّمًا.

        وهذا الجوابُ **تسجيلُ فحصٍ لا إصدارُ شهادة**: استيفاءُ الشروط المسجّلة
        ههنا لا يُنشئ شهادةً لغويّة، وإصدارُها تفويضٌ إلى جهةٍ حاكمةٍ خطوةً
        مستقلّةً عن تسجيل الأدلّة وفحصها
        (`A_RECORDED_CONDITION_IS_NOT_AN_ISSUED_CERTIFICATE`).
        """

        return (
            self.domain_kind is DomainKind.DECLARED_LINGUISTIC_DOMAIN
            and self.is_established_on_its_domain
        )

    @property
    def certificate_issuance_is_delegated(self) -> bool:
        """أتُصدِر هذه الوحدةُ شهادةً؟ لا — والجوابُ ثابتٌ بالبناء."""

        return True

    @property
    def minimality_is_relative_to_the_tested_alternatives(self) -> bool:
        """أهي دنيا مطلقًا؟ لا — بل بالنسبة إلى المكوّنات وصنفِ البدائل المختبَر."""

        return True


def assess_minimal_complete_fiber(
    domain: DeclaredDomain = THE_DECLARED_DOMAIN,
) -> MinimalCompleteFiberVerdict:
    """قِس المعيارَ بشطريه بإجراء تجربتين: كفايةٌ على `T`، ونقضٌ على كلّ `T_{-i}`."""

    reader = lookup_reader(domain, full_representation)
    return MinimalCompleteFiberVerdict(
        domain=domain,
        sufficiency=assess_sufficiency(domain, full_representation, reader),
        necessity=tuple(
            (component, necessity_standing_of(component, domain))
            for component in DeletedComponent
        ),
    )


# --- قائمةُ التدقيق: سبعةُ شروطٍ والمستوفى صفرٌ بالعدّ -------------------------


class ClosureRequirement(Enum):
    """شروطُ شهادة الحدّ الأدنى المكتمل؛ قائمةُ تدقيقٍ للبرهان لا تقريرُ نجاح."""

    FUNCTION_AND_DOMAIN_FIXED_BEFOREHAND = "تحديدُ_وظيفة_الإفادة_ومجالها_قبل_التجربة"
    CONTENT_REBUILT_FROM_THE_OUTPUT_ALONE = "إعادةُ_بناء_المضمون_من_المخرج_وحدَه"
    CLASSIFICATION_NECESSARY_OR_DERIVABLE = "ضرورةُ_التصنيف_أو_بيانُ_اشتقاقه"
    PREDICATE_NECESSARY = "ضرورةُ_معلومة_المحمول"
    ATTRIBUTION_NECESSARY_WITH_ITS_SCOPE = "ضرورةُ_نوع_الإسناد_ونطاقه"
    WEAKER_ALTERNATIVES_EXHAUSTED = "استنفادُ_البدائل_الأضعف_المحدَّدة_مسبقًا"
    EVIDENCE_RANK_AND_RESIDUE_CLOSED = "فحصُ_الدليل_والرتبة_والبقايا_وإغلاقُ_الفشل"


class ConditionRunKind(Enum):
    """جنسُ التجربة التي يُجريها الشاهد؛ ومنها تُقرَأ نتيجتُه لا من جنس مجاله."""

    SUFFICIENCY_ON_THE_FULL_REPRESENTATION = "كفايةٌ_على_التمثيل_الكامل"
    DELETION_OF_A_NAMED_COMPONENT = "حذفُ_مكوّنٍ_مُسمًّى"


@dataclass(frozen=True, slots=True)
class ConditionEvidence:
    """شاهدٌ موثَّقٌ لشرطٍ: ما أُجري، وأين سُجِّل، وعلى أيّ مجالٍ، وبأيّ تجربة.

    ونتيجتُه **تُجرى عند كلّ قراءة** ولا تُكتَب في حقلٍ بجانبها؛ فشاهدٌ يُعلِن
    نجاحًا لا يُنتجه تشغيلُه ليس شاهدًا.
    """

    what_was_run: str
    where_it_is_recorded: str
    domain: DeclaredDomain
    run_kind: ConditionRunKind
    component: DeletedComponent | None = None
    reader: Reader | None = None

    def __post_init__(self) -> None:
        if not self.what_was_run.strip():
            raise MinimalCompleteFiberError("شاهدٌ بلا بيانِ ما أُجري ليس شاهدًا")
        if not self.where_it_is_recorded.strip():
            raise MinimalCompleteFiberError(
                "شاهدٌ بلا موضعِ تسجيلٍ لا يُراجَع؛ والمراجعةُ شرطُ التوثيق"
            )
        if self.run_kind is ConditionRunKind.DELETION_OF_A_NAMED_COMPONENT:
            if self.component is None:
                raise MinimalCompleteFiberError(
                    "تجربةُ حذفٍ بلا مكوّنٍ مُسمًّى لا يُعرَف أيَّ شرطٍ تُغلِق"
                )
            if self.reader is not None:
                raise MinimalCompleteFiberError(
                    "تجربةُ الحذف تُجرى بأفضلِ قارئٍ على مخرجاتها، فلا يُمرَّر إليها قارئ"
                )
        else:
            if self.component is not None:
                raise MinimalCompleteFiberError(
                    "تجربةُ كفايةٍ على التمثيل الكامل لا تُسمّي مكوّنًا محذوفًا"
                )
            if self.reader is None:
                raise MinimalCompleteFiberError(
                    "تجربةُ كفايةٍ بلا قارئٍ مُسمًّى لا تُقرَأ إعادةَ بناء"
                )

    @property
    def domain_kind(self) -> DomainKind:
        """جنسُ مجال الشاهد، مُشتقًّا من مجاله نفسِه لا مكتوبًا في الشاهد.

        فلا يُرفَع شاهدٌ إلى «لغويٍّ مُعلَن» بكتابة جنسه؛ يُرفَع بتوثيق كلّ
        حالةٍ من حالات مجاله توثيقًا مفحوصَ البصمة والموضع والوسم.
        """

        return self.domain.kind

    @property
    def outcome(self) -> SufficiencyExperimentResult:
        """نتيجةُ التجربة، **مُجراةً الآن** لا مقروءةً من حقلٍ مكتوب."""

        if self.run_kind is ConditionRunKind.DELETION_OF_A_NAMED_COMPONENT:
            assert self.component is not None
            return necessity_deletion_experiment(self.component, self.domain)
        assert self.reader is not None
        return run_sufficiency_experiment(self.domain, full_representation, self.reader)


_NECESSITY_REQUIREMENTS: Final[dict[ClosureRequirement, DeletedComponent]] = {
    ClosureRequirement.CLASSIFICATION_NECESSARY_OR_DERIVABLE: (
        DeletedComponent.CLASSIFICATION
    ),
    ClosureRequirement.PREDICATE_NECESSARY: DeletedComponent.PREDICATE,
    ClosureRequirement.ATTRIBUTION_NECESSARY_WITH_ITS_SCOPE: DeletedComponent.RELATION,
}
"""أيُّ شرطِ ضرورةٍ يُغلَق بتجربة حذفِ أيِّ مكوّنٍ بعينه؛ ولا يُغلِقه سواه."""


NO_EVIDENCE_KIND_HERE_CLOSES: Final[frozenset[ClosureRequirement]] = frozenset(
    {
        ClosureRequirement.FUNCTION_AND_DOMAIN_FIXED_BEFOREHAND,
        ClosureRequirement.WEAKER_ALTERNATIVES_EXHAUSTED,
        ClosureRequirement.EVIDENCE_RANK_AND_RESIDUE_CLOSED,
    }
)
"""شروطٌ لا يُغلِقها جنسُ شاهدٍ مُعرَّفٌ في هذه الوحدة، فتبقى مفتوحةً بالبناء."""


def requirement_is_closed_by(
    requirement: ClosureRequirement, evidence: ConditionEvidence
) -> bool:
    """أتُغلِق نتيجةُ هذا الشاهد هذا الشرطَ بعينه؟ يُقرَأ من التشغيل لا من المجال.

    * شرطُ إعادة البناء: كفايةٌ **قائمة** بقارئٍ مثبَّتةٍ قاعدتُه قبل البيانات؛
      وقارئُ الجدول لا يُغلِقه ولو قامت به الكفاية.
    * شروطُ الضرورة الثلاثة: نقضٌ في تجربة حذفِ **ذلك المكوّن بعينه**.
    * ما عداها: لا يُغلِقه جنسُ شاهدٍ ههنا.
    """

    if requirement in NO_EVIDENCE_KIND_HERE_CLOSES:
        return False
    outcome = evidence.outcome
    if requirement is ClosureRequirement.CONTENT_REBUILT_FROM_THE_OUTPUT_ALONE:
        return (
            evidence.run_kind is ConditionRunKind.SUFFICIENCY_ON_THE_FULL_REPRESENTATION
            and outcome.standing is SufficiencyStanding.HELD_ON_A_DECLARED_DOMAIN
            and outcome.reader_provenance
            is ReaderProvenance.FIXED_BEFORE_THE_EVALUATION_DATA
        )
    expected = _NECESSITY_REQUIREMENTS[requirement]
    return (
        evidence.run_kind is ConditionRunKind.DELETION_OF_A_NAMED_COMPONENT
        and evidence.component is expected
        and outcome.standing is SufficiencyStanding.REFUTED_ON_A_DECLARED_DOMAIN
    )


@dataclass(frozen=True, slots=True)
class ChecklistCondition:
    """شرطٌ واحد: ما يستوفيه، ولمَ لم يُستوفَ بعد، وشاهدُه الموثَّقُ إن وُجد."""

    requirement: ClosureRequirement
    what_would_satisfy_it: str
    why_it_is_open: str
    evidence: ConditionEvidence | None = None

    def __post_init__(self) -> None:
        if not self.what_would_satisfy_it.strip():
            raise MinimalCompleteFiberError(
                "شرطٌ بلا مُستوفًى مكتوبٍ يبقى مفتوحًا بلا بابٍ يُغلَق به"
            )
        if not self.why_it_is_open.strip():
            raise MinimalCompleteFiberError("شرطٌ بلا سببٍ مكتوبٍ لانفتاحه يُقرَأ مستوفًى")

    @property
    def is_attempted(self) -> bool:
        """أأُجري لهذا الشرط شيءٌ موثَّق؟ يُقرَأ من وجود الشاهد لا من الدعوى."""

        return self.evidence is not None

    @property
    def is_satisfied(self) -> bool:
        """أاستُوفي؟ يُقرَأ من **نتيجة تجربته** وسندِها معًا لا من جنس المجال.

        فيلزم ثلاثةٌ مجتمعة: شاهدٌ مُجرًى، ونتيجةٌ تُغلِق هذا الشرطَ بعينه،
        ومجالٌ لغويٌّ مُعلَنٌ مفحوصُ التوثيق. وسقوطُ واحدةٍ يُبقي الشرطَ مفتوحًا،
        فلا يُستوفى شرطٌ بمجالٍ موثَّقٍ وتجربةٍ فاشلة، ولا بتجربةٍ ناجحةٍ على
        مجالٍ مصمَّم.
        """

        evidence = self.evidence
        return (
            evidence is not None
            and evidence.domain_kind is DomainKind.DECLARED_LINGUISTIC_DOMAIN
            and requirement_is_closed_by(self.requirement, evidence)
        )


@dataclass(frozen=True, slots=True)
class ClosureChecklist:
    """قائمةُ التدقيق كاملةً؛ والمستوفى والمُجرى يُعَدّان ولا يُكتَبان بجانبها."""

    conditions: tuple[ChecklistCondition, ...]

    def __post_init__(self) -> None:
        if len(self.conditions) != len(ClosureRequirement):
            raise MinimalCompleteFiberError(
                "الشروطُ تُذكَر كلُّها أو لا تُذكَر؛ وإسقاطُ واحدٍ استيفاءٌ صامت"
            )
        if len({item.requirement for item in self.conditions}) != len(self.conditions):
            raise MinimalCompleteFiberError("شرطٌ تكرّر؛ والتكرارُ يُخفي نقصًا")

    @property
    def satisfied_count(self) -> int:
        """المستوفى في القائمة، مُشتقًّا بقراءة الشواهد."""

        return sum(1 for item in self.conditions if item.is_satisfied)

    @property
    def attempted_count(self) -> int:
        """ما أُجري له شيءٌ موثَّقٌ ولمّا يُستوفَ، مُشتقًّا بالعدّ."""

        return sum(1 for item in self.conditions if item.is_attempted)

    @property
    def total_count(self) -> int:
        """عددُ الشروط كلِّها."""

        return len(self.conditions)

    @property
    def is_complete(self) -> bool:
        """أتُعلَن الشهادة؟ لا ما بقي شرطٌ مفتوح، والرتبةُ لا تُرفَع بالتقريب."""

        return self.satisfied_count == self.total_count

    @property
    def is_a_live_audit(self) -> bool:
        """أهي تدقيقٌ حيّ؟ نعم — تُقرَأ من شواهد الشروط لا من إعلانٍ ثابت."""

        return True


A_DESIGNED_RUN: Final[ConditionEvidence] = ConditionEvidence(
    what_was_run=(
        "تجربةُ كفايةٍ مُجراةٌ على المجال المصمَّم: يُنادى القارئُ مرّةً لكلّ "
        "مخرجٍ متمايز، ثمّ يُقابَل جوابُه بمضمون كلّ حالةٍ تشترك في ذلك المخرج"
    ),
    where_it_is_recorded="`run_sufficiency_experiment` و`THE_DECLARED_DOMAIN`",
    domain=THE_DECLARED_DOMAIN,
    run_kind=ConditionRunKind.SUFFICIENCY_ON_THE_FULL_REPRESENTATION,
    reader=THE_REFERENCE_READER,
)
"""شاهدُ إجراءٍ على المجال المُعلَن؛ وجنسُه مُشتَقٌّ منه، لا مكتوبٌ فيه."""


def _deletion_run(component: DeletedComponent) -> ConditionEvidence:
    """شاهدُ إجراءٍ لتجربة حذفِ مكوّنٍ على المجال المصمَّم، بمقاماتٍ مثبَّتة."""

    return ConditionEvidence(
        what_was_run=(
            f"تجربةُ حذفِ «{component.value}» على المجال المصمَّم بأفضلِ قارئٍ "
            "ممكنٍ على مخرجات التمثيل الناقص، ومقامُ كلّ حالةٍ مثبَّتٌ فيه"
        ),
        where_it_is_recorded=(
            "`necessity_deletion_experiment` و`THE_DESIGNED_WITNESSES`"
        ),
        domain=THE_DECLARED_DOMAIN,
        run_kind=ConditionRunKind.DELETION_OF_A_NAMED_COMPONENT,
        component=component,
    )


THE_CLOSURE_CHECKLIST: Final[ClosureChecklist] = ClosureChecklist(
    conditions=(
        ChecklistCondition(
            requirement=ClosureRequirement.FUNCTION_AND_DOMAIN_FIXED_BEFOREHAND,
            what_would_satisfy_it=(
                "تسجيلٌ قبليٌّ مُجمَّدٌ يحدّد `F` و`𝒟` قبل أيّ تجربة، بترتيبٍ " "تاريخيٍّ يُتحقَّق منه"
            ),
            why_it_is_open=(
                "المجالُ ودالّةُ الإفادة مُعلَنان ههنا نصًّا في `THE_DECLARED_DOMAIN`، "
                "ولا تسجيلَ قبليًّا مُجمَّدًا يُثبِت سبقَهما للتجربة"
            ),
            evidence=A_DESIGNED_RUN,
        ),
        ChecklistCondition(
            requirement=ClosureRequirement.CONTENT_REBUILT_FROM_THE_OUTPUT_ALONE,
            what_would_satisfy_it=(
                "قارئٌ مستقلٌّ `D` يُرجِع `F(x)` من `T(x)` وحدَه، بلا قراءةِ الأصل"
            ),
            why_it_is_open=(
                "القارئُ مُجرًّى على المجال المصمَّم وحدَه، وهو قارئُ جدولٍ يثبت "
                "تباينَ التمثيل لا فهمَه؛ ولا مدوّنةَ عربيّةً مُبصَّمةً يُقاس عليها"
            ),
            evidence=A_DESIGNED_RUN,
        ),
        ChecklistCondition(
            requirement=ClosureRequirement.CLASSIFICATION_NECESSARY_OR_DERIVABLE,
            what_would_satisfy_it=(
                "شاهدان متصادمان تحت `T_{-G}` على مجالٍ مُعلَن، أو بيانُ اشتقاق "
                "الجنس اشتقاقًا وحيدًا مرخَّصًا من المرساة"
            ),
            why_it_is_open=(
                "تجربةُ الحذف مُجراةٌ، لكنّها على مجالٍ مصمَّمٍ مكتوبٍ ههنا؛ "
                "ولم تُجرَ على مدوّنةٍ عربيّةٍ مُعلَنةٍ ولا على المِرماز"
            ),
            evidence=_deletion_run(DeletedComponent.CLASSIFICATION),
        ),
        ChecklistCondition(
            requirement=ClosureRequirement.PREDICATE_NECESSARY,
            what_would_satisfy_it=(
                "شاهدان متصادمان تحت `T_{-P}` على مجالٍ مُعلَن، مع تثبيت المرجع "
                "ونوع الإسناد"
            ),
            why_it_is_open=(
                "زوجُ «زيد طويل/قصير» تجربةٌ مُجراةٌ على مجالٍ مصمَّمٍ بمقامٍ "
                "مثبَّت، لا على مدوّنةٍ عربيّةٍ مُعلَنة"
            ),
            evidence=_deletion_run(DeletedComponent.PREDICATE),
        ),
        ChecklistCondition(
            requirement=ClosureRequirement.ATTRIBUTION_NECESSARY_WITH_ITS_SCOPE,
            what_would_satisfy_it=(
                "شاهدان متصادمان تحت `T_{-R}` مع تسمية نطاق الإسناد، ومنعُ استعادة "
                "نوعه من حقلٍ آخرَ أو من الأصل"
            ),
            why_it_is_open=(
                "زوجُ «الرجل الطويل/الرجل طويل» مُجرًّى بمقامٍ مثبَّتٍ يمنع النسخَ "
                "داخل التمثيل، ولا يُغني عن مدوّنةٍ تمنع الاستعادة من الأصل"
            ),
            evidence=_deletion_run(DeletedComponent.RELATION),
        ),
        ChecklistCondition(
            requirement=ClosureRequirement.WEAKER_ALTERNATIVES_EXHAUSTED,
            what_would_satisfy_it=(
                "صنفُ بدائلَ أضعفَ محدَّدٌ مسبقًا، يُختبَر كلُّ عضوٍ فيه ويُسقَط بشاهد"
            ),
            why_it_is_open=(
                "لم يُحدَّد صنفُ البدائل بعد؛ وبلا تحديدِه يكون «استنفادٌ» دعوًى "
                "لا يمكن تكذيبُها"
            ),
        ),
        ChecklistCondition(
            requirement=ClosureRequirement.EVIDENCE_RANK_AND_RESIDUE_CLOSED,
            what_would_satisfy_it=(
                "فحصُ الدليل والرتبة والبقايا في عقد الترخيص، وإغلاقُ حدود الفشل "
                "بشواهدَ مكتوبة"
            ),
            why_it_is_open=(
                "الدليلُ والبقايا مُمثَّلان في `AttributionCandidate` شكلًا فقط، "
                "ولا عقدَ ترخيصٍ يُفحَص ههنا"
            ),
        ),
    )
)
"""سبعةُ شروطٍ، والمستوفى صفرٌ؛ فلا تُرفَع رتبةُ المرشَّح إلى شهادةٍ مكتملة."""


# --- البواقي المُسمّاة --------------------------------------------------------


A_COLLISION_IN_THE_REPRESENTATION_IS_NOT_A_COLLISION_IN_CONTEXT_NOTE: Final[str] = (
    "ACollisionInTheRepresentationIsNotACollisionInContext: تصادمُ الشاهدين "
    "تحت الإسقاط يمنع أن يكون المحذوفُ منسوخًا في حقلٍ آخرَ من التمثيل؛ ولا "
    "يُغني عن تثبيت المجال والسياق ومنعِ القارئ من استعادة المحذوف من الأصل، "
    "وتلك شروطُ تنفيذٍ لم تُستوفَ ههنا"
)

A_DESIGNED_WITNESS_IS_NOT_AN_EXECUTED_CODEC_TEST_NOTE: Final[str] = (
    "ADesignedWitnessIsNotAnExecutedCodecTest: تجاربُ الحذف الثلاثُ مُجراةٌ "
    "فعلًا على المجال المصمَّم، وكلُّ واحدةٍ تدمج مضمونين فتنقض الكفاية؛ ومع "
    "ذلك فالمُجرَى عليه أزواجٌ مكتوبةٌ ههنا، لا المِرماز ولا مدوّنةٌ مُبصَّمة، "
    "والفرقُ فرقُ جنسٍ لا فرقُ درجة"
)

FOUR_FIELDS_CARRY_THREE_FUNCTIONS_NOTE: Final[str] = (
    "FourFieldsCarryThreeFunctions: `(a, g, p, r)` أربعةُ حقولٍ تؤدّي ثلاثَ "
    "وظائفَ بنيويّة، إذ يشترك `a` و`g` في الهويّة والتصنيف؛ ومتى اشتُقَّ الجنسُ "
    "من المرساة اشتقاقًا وحيدًا مرخَّصًا لزمت **معلومةُ** التصنيف ولم يلزم "
    "**حقلٌ** باسم الجنس"
)

ONE_IS_A_NAMED_ATTRIBUTION_NOT_A_TRUE_PROPOSITION_NOTE: Final[str] = (
    "OneIsANamedAttributionNotATrueProposition: بلوغُ `one` تعيينُ وجه الربط "
    "بدليلٍ وبقايا، ولا يعني صدقَ القضيّة في الواقع؛ فقد يُعيَّن مضمونُ خبرٍ "
    "لغويٍّ كاملٍ من غير إثبات صدقه، والتعيينُ غيرُ التصديق"
)

THE_MINIMUM_IS_RELATIVE_TO_THE_TESTED_ALTERNATIVES_NOTE: Final[str] = (
    "TheMinimumIsRelativeToTheTestedAlternatives: ما يثبته المعيارُ — لو ثبت — "
    "حدٌّ أدنى بالنسبة إلى المكوّنات المرشَّحة وصنفِ البدائل المختبَر؛ ولا يُلزِم "
    "كلَّ ترميزٍ بثلاثة حقولٍ منفصلة، إذ قد تُشفَّر المعلوماتُ الضروريّةُ نفسُها "
    "بطريقةٍ أخرى"
)

THE_RELATION_VOCABULARY_IS_NOT_CLAIMED_EXHAUSTIVE_NOTE: Final[str] = (
    "TheRelationVocabularyIsNotClaimedExhaustive: الإخبارُ والتقييدُ والعلاقةُ "
    "الحدثيّةُ أوجهٌ مُسمّاةٌ للربط، ونصُّ المعادلة «أو غير ذلك»؛ فلا تُقرَأ "
    "الثلاثةُ حصرًا، وتوسيعُ المفردة يلزمه شاهدٌ لا إضافةٌ صامتة"
)

A_LOOKUP_READER_PROVES_INJECTIVITY_NOT_UNDERSTANDING_NOTE: Final[str] = (
    "ALookupReaderProvesInjectivityNotUnderstanding: القارئُ المُجرّى ههنا "
    "جدولٌ من مخرجات التمثيل إلى المضمون؛ فنجاحُه يثبت أنّ `T` مُتباينٌ على "
    "المجال المُعلَن، لا أنّ مضمونَ الإفادة مُستخرَجٌ بقواعدَ لغويّة"
)

A_DESIGNED_DOMAIN_IS_NOT_A_LINGUISTIC_CERTIFICATE_NOTE: Final[str] = (
    "ADesignedDomainIsNotALinguisticCertificate: `𝒟` المُجرَى عليه مصمَّمٌ "
    "لاختبار التمثيل، بستّ حالاتٍ مكتوبةٍ ههنا ومقاماتٍ مثبَّتة؛ فقيامُ المعيار "
    "عليه حكمٌ على مجاله وحدَه، ولا يُرقّى شهادةً لغويّةً بلا مدوّنةٍ مُعلَنةٍ "
    "مُبصَّمةٍ وتسجيلٍ قبليٍّ مُجمَّد"
)

THE_PREDICATE_SPACE_IS_DECLARED_NOT_MEASURED_NOTE: Final[str] = (
    "ThePredicateSpaceIsDeclaredNotMeasured: `P(g)` جدولٌ مُعلَنٌ في هذه الوحدة؛ "
    "وفاحصُ التوافق النوعيّ يمنع دخولَ محمولٍ خارجَه، ولا يقيس عربيّةَ التركيب "
    "ولا يُثبِت أنّ الجدولَ مستوعِبٌ لمحمولات الجنس"
)

ZERO_IS_AN_UNNAMED_RELATION_NOT_AN_EMPTY_FIBER_NOTE: Final[str] = (
    "ZeroIsAnUnnamedRelationNotAnEmptyFiber: `Z = (a, g, p, ⊥)` حاملٌ مصنَّفٌ "
    "ومحمولٌ مرشَّحٌ لم يُعيَّن وجهُ ربطهما؛ فليست `zero` ليفًا خاليًا ولا صفةً "
    "منفيّة، والخلطُ بينهما يجعل عدمَ التعيين نفيًا"
)

A_DOMAIN_KIND_IS_DERIVED_FROM_ATTESTATIONS_NOT_WRITTEN: Final[str] = (
    "ADomainKindIsDerivedFromAttestationsNotWritten: لا حقلَ يُكتَب فيه جنسُ "
    "المجال؛ يُشتَقّ من توثيق **كلّ** حالةٍ بمدوّنةٍ مُسجَّلةٍ في الشجرة "
    "تُحسَب بصمتُها عند كلّ فحص. فبوّابةُ الشهادة لا تُفتَح بتسميةِ مجالٍ "
    "مصمَّمٍ «لغويًّا مُعلَنًا»، وشاهدُ الشرط كذلك يستمدّ جنسَه من مجاله"
)

AN_ATTESTED_CORPUS_IS_NOT_A_SUFFICIENT_SAMPLE: Final[str] = (
    "AnAttestedCorpusIsNotASufficientSample: توثيقُ الحالات بمدوّنةٍ مُبصَّمةٍ "
    "يرفع تهمةَ الاختلاق، ولا يُثبِت أنّ المدوّنةَ عيّنةٌ كافيةٌ ولا ممثِّلة؛ "
    "فالفاتحةُ نصٌّ واحدٌ قصير، وقيامُ المعيار عليها حكمٌ عليها لا على العربية"
)

AN_OCCURRENCE_IS_NOT_A_GLOSS_NOTE: Final[str] = (
    "AnOccurrenceIsNotAGloss: شهادةُ ورودِ اللفظ ليست شهادةَ صحّةِ تفسيره. "
    "فقد يُثبَت أنّ «عين» وقعت في موضعٍ مُحدَّدٍ من مدوّنةٍ مُبصَّمة، ويبقى "
    "تعيينُ جنسها ومحمولها ومضمونها محتاجًا إلى وسمٍ من جهةٍ غيرِ صاحب الدعوى؛ "
    "ولا تصلح مدوّنةُ الفاتحة سندًا لحالة «زيد طويل» بإلحاق بصمتها بها"
)

A_SELF_AUTHORED_GLOSS_IS_REFUSED_NOTE: Final[str] = (
    "ASelfAuthoredGlossIsRefused: وسمٌ جهتُه هي مُعلِنُ المجال نفسُه يُردّ "
    "بالبناء، ولا يُرقّى مجالُه إلى لغويٍّ مُعلَن؛ وفصلُ ملفّ الوسم وإبصامُه "
    "يمنعان التبدّلَ الصامت ولا يُنشئان جهةً مستقلّة. وإذا تعذّر وسمٌ مرجعيٌّ "
    "صحيحٌ بقي المجالُ مصمَّمًا أو غيرَ محسوم، ولا يُصطنَع شاهدٌ لاستيفاء شرط"
)

A_RECORDED_CONDITION_IS_NOT_AN_ISSUED_CERTIFICATE_NOTE: Final[str] = (
    "ARecordedConditionIsNotAnIssuedCertificate: استيفاءُ الشروط السبعة "
    "المسجّلة ههنا فحصٌ مُجرًى لا شهادةٌ صادرة؛ وإصدارُ الشهادة تفويضٌ إلى جهةٍ "
    "حاكمةٍ خطوةً مستقلّةً عن تسجيل الأدلّة وفحصها، ولا تملكه هذه الوحدة"
)

MINIMAL_COMPLETE_FIBER_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    A_DOMAIN_KIND_IS_DERIVED_FROM_ATTESTATIONS_NOT_WRITTEN,
    AN_ATTESTED_CORPUS_IS_NOT_A_SUFFICIENT_SAMPLE,
    AN_OCCURRENCE_IS_NOT_A_GLOSS_NOTE,
    A_SELF_AUTHORED_GLOSS_IS_REFUSED_NOTE,
    A_RECORDED_CONDITION_IS_NOT_AN_ISSUED_CERTIFICATE_NOTE,
    FOUR_FIELDS_CARRY_THREE_FUNCTIONS_NOTE,
    THE_PREDICATE_SPACE_IS_DECLARED_NOT_MEASURED_NOTE,
    A_LOOKUP_READER_PROVES_INJECTIVITY_NOT_UNDERSTANDING_NOTE,
    A_DESIGNED_DOMAIN_IS_NOT_A_LINGUISTIC_CERTIFICATE_NOTE,
    A_DESIGNED_WITNESS_IS_NOT_AN_EXECUTED_CODEC_TEST_NOTE,
    A_COLLISION_IN_THE_REPRESENTATION_IS_NOT_A_COLLISION_IN_CONTEXT_NOTE,
    ZERO_IS_AN_UNNAMED_RELATION_NOT_AN_EMPTY_FIBER_NOTE,
    ONE_IS_A_NAMED_ATTRIBUTION_NOT_A_TRUE_PROPOSITION_NOTE,
    THE_RELATION_VOCABULARY_IS_NOT_CLAIMED_EXHAUSTIVE_NOTE,
    THE_MINIMUM_IS_RELATIVE_TO_THE_TESTED_ALTERNATIVES_NOTE,
)
"""خمسَ عشرةَ بقيّةً مُسمّاةً تُقابَل بها أيُّ إحالةٍ إلى «الحدّ الأدنى المكتمل»."""
