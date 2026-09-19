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

**ولا قارئَ مستقلًّا في هذه الشجرة بعدُ**، فالكفايةُ **غيرُ مختبَرة**، وشطرُ
المعيار الأوّلُ مفتوح؛ ولا يُرفَع المرشَّحُ بشطرٍ واحد
(`WITHOUT_AN_INDEPENDENT_READER_SUFFICIENCY_IS_UNTESTED`).

**والشواهدُ العربيّةُ الثلاثةُ تُفحَص حيّةً بوصفها تصميمًا**: «عين» البصر
و«عين» الماء لحذف التصنيف، و«زيد طويل» و«زيد قصير» لحذف المحمول، و«الرجل
الطويل» و«الرجل طويل» لحذف نوع الربط. تصادمُها تحت الإسقاط مفحوصٌ بالبناء، وهي
**تصميمُ شواهدَ مضادّة لا شهادةٌ بأنّ اختبارًا نُفِّذ على المِرماز**
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

**والإغلاقُ لا يُعلَن**: قائمةُ التدقيق سبعةُ شروطٍ، والمستوفى منها **صفرٌ**
مُشتقًّا بالعدّ لا مكتوبًا. وما يثبت — لو ثبت — حدٌّ أدنى **بالنسبة إلى**
المكوّنات المرشَّحة وصنفِ البدائل المختبَر، لا إلزامٌ لكلّ ترميزٍ بثلاثة حقولٍ
منفصلة (`THE_MINIMUM_IS_RELATIVE_TO_THE_TESTED_ALTERNATIVES`).

ولا سلطةَ لهذه الوحدة: لا ولادةَ، ولا حكمَ ولادة، ولا ترخيصَ `RefineSlot`، ولا
استيرادَ من `kernel/`.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

__all__ = [
    "A_COLLISION_IN_THE_REPRESENTATION_IS_NOT_A_COLLISION_IN_CONTEXT_NOTE",
    "A_DESIGNED_WITNESS_IS_NOT_AN_EXECUTED_CODEC_TEST_NOTE",
    "FOUR_FIELDS_CARRY_THREE_FUNCTIONS_NOTE",
    "MINIMAL_COMPLETE_FIBER_NAMED_RESIDUALS",
    "ONE_IS_A_NAMED_ATTRIBUTION_NOT_A_TRUE_PROPOSITION_NOTE",
    "THE_CLOSURE_CHECKLIST",
    "THE_DESIGNED_WITNESSES",
    "THE_MINIMUM_IS_RELATIVE_TO_THE_TESTED_ALTERNATIVES_NOTE",
    "THE_RELATION_VOCABULARY_IS_NOT_CLAIMED_EXHAUSTIVE_NOTE",
    "WITHOUT_AN_INDEPENDENT_READER_SUFFICIENCY_IS_UNTESTED_NOTE",
    "ZERO_IS_AN_UNNAMED_RELATION_NOT_AN_EMPTY_FIBER_NOTE",
    "AttributionCandidate",
    "ChecklistCondition",
    "ClosureChecklist",
    "ClosureRequirement",
    "DeletedComponent",
    "FiberElement",
    "MinimalCompleteFiberError",
    "MinimalCompleteFiberVerdict",
    "NecessityStanding",
    "NecessityWitnessPair",
    "RelationKind",
    "StructuralFunction",
    "SufficiencyStanding",
    "a_separate_genus_field_is_required",
    "assess_minimal_complete_fiber",
    "assess_sufficiency",
    "carried_functions",
    "classification_information_is_required",
    "delete",
    "necessity_standing_of",
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
    scope_note: str

    def __post_init__(self) -> None:
        if not self.first_content.strip() or not self.second_content.strip():
            raise MinimalCompleteFiberError("شاهدٌ بلا مضمونِ إفادةٍ مكتوبٍ لا يُقابَل")
        if not self.scope_note.strip():
            raise MinimalCompleteFiberError(
                "شاهدٌ بلا نطاقٍ مكتوبٍ يُقرَأ بعد حين شهادةَ تنفيذٍ على المِرماز"
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


THE_DESIGNED_WITNESSES: Final[tuple[NecessityWitnessPair, ...]] = (
    NecessityWitnessPair(
        component=DeletedComponent.CLASSIFICATION,
        first=FiberElement(
            anchor="عين",
            genus="عضوُ الإبصار",
            predicate="مُبصِرة",
            relation=RelationKind.PREDICATION,
        ),
        second=FiberElement(
            anchor="عين",
            genus="نبعُ الماء",
            predicate="مُبصِرة",
            relation=RelationKind.PREDICATION,
        ),
        first_content="حديثٌ عن عضو الإبصار",
        second_content="حديثٌ عن نبع الماء",
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
        first_content="تركيبٌ تقييديّ: «الرجل الطويل»",
        second_content="إخبارٌ: «الرجل طويل»",
        scope_note=(
            "تصميمُ شاهدٍ مضادٍّ لحذف نوع الربط: تشترك العبارتان في المفهومين "
            "ويفترقان في التقييد والإخبار، فحذفُ الفرق يُفقِد معلومةً لازمة"
        ),
    ),
)
"""ثلاثةُ أزواجٍ مصمَّمةٍ، تصادمُها مفحوصٌ عند الإنشاء؛ وهي تصميمٌ لا تنفيذ."""


class NecessityStanding(Enum):
    """حالُ ضرورةِ مكوّن؛ والمشهودُ على التصميم غيرُ المشهود على المِرماز."""

    WITNESSED_ON_THE_DESIGNED_PAIRS = "مشهودةٌ_على_الأزواج_المصمَّمة"
    NOT_WITNESSED = "لا_شاهدَ_لها_ههنا"


def necessity_standing_of(
    component: DeletedComponent,
    witnesses: tuple[NecessityWitnessPair, ...] = THE_DESIGNED_WITNESSES,
) -> NecessityStanding:
    """أمشهودةٌ ضرورةُ هذا المكوّن؟ يُقرَأ من وجود زوجٍ متصادمٍ لا من دعوى."""

    if any(item.component is component for item in witnesses):
        return NecessityStanding.WITNESSED_ON_THE_DESIGNED_PAIRS
    return NecessityStanding.NOT_WITNESSED


# --- الكفاية: لا قارئَ مستقلًّا ههنا ------------------------------------------


class SufficiencyStanding(Enum):
    """حالُ شطر الكفاية؛ ولا يُقرَأ غيابُ القارئ سقوطًا ولا ثبوتًا."""

    NO_INDEPENDENT_READER_IN_THIS_TREE = "لا_قارئَ_مستقلًّا_في_هذه_الشجرة"
    HELD_ON_A_DECLARED_DOMAIN = "قائمةٌ_على_مجالٍ_مُعلَن"
    REFUTED_ON_A_DECLARED_DOMAIN = "منتقضةٌ_على_مجالٍ_مُعلَن"


def assess_sufficiency() -> SufficiencyStanding:
    """أثبتت `D(T(x)) = F(x)`؟ يُجاب بفحص وجود القارئ لا بترجيحه.

    ولا تُصدِّر هذه الوحدةُ قارئًا ولا دالّةَ إفادةٍ على مجالٍ مُعلَن، فالشطرُ
    الأوّلُ من المعيار **غيرُ مختبَر**؛ وهذا فحصٌ حيٌّ لواجهة الوحدة نفسِها.
    """

    reader_names = {"D", "read_content", "reconstruct_content", "independent_reader"}
    if reader_names & set(__all__):
        return SufficiencyStanding.HELD_ON_A_DECLARED_DOMAIN
    return SufficiencyStanding.NO_INDEPENDENT_READER_IN_THIS_TREE


@dataclass(frozen=True, slots=True)
class MinimalCompleteFiberVerdict:
    """حكمُ المعيار بشطريه؛ ولا يُرفَع بشطرٍ واحدٍ ولو تمّ الآخرُ كلُّه."""

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
    def every_component_is_witnessed(self) -> bool:
        """أمشهودةٌ ضرورةُ المكوّنات كلِّها على الأزواج المصمَّمة؟ يُعَدّ ولا يُدَّعى."""

        return all(
            standing is NecessityStanding.WITNESSED_ON_THE_DESIGNED_PAIRS
            for _, standing in self.necessity
        )

    @property
    def is_established(self) -> bool:
        """أثبت المعيار؟ يلزمه الشطران معًا، والكفايةُ ههنا غيرُ مختبَرة."""

        return (
            self.sufficiency is SufficiencyStanding.HELD_ON_A_DECLARED_DOMAIN
            and self.every_component_is_witnessed
        )

    @property
    def minimality_is_relative_to_the_tested_alternatives(self) -> bool:
        """أهي دنيا مطلقًا؟ لا — بل بالنسبة إلى المكوّنات وصنفِ البدائل المختبَر."""

        return True


def assess_minimal_complete_fiber(
    witnesses: tuple[NecessityWitnessPair, ...] = THE_DESIGNED_WITNESSES,
) -> MinimalCompleteFiberVerdict:
    """قِس المعيارَ بشطريه: كفايةٌ تُفحَص، وضرورةٌ تُشتَقّ من الشواهد المصمَّمة."""

    return MinimalCompleteFiberVerdict(
        sufficiency=assess_sufficiency(),
        necessity=tuple(
            (component, necessity_standing_of(component, witnesses))
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


@dataclass(frozen=True, slots=True)
class ChecklistCondition:
    """شرطٌ واحد: ما يستوفيه، ولمَ لم يُستوفَ بعد — ولا يُكتَب أحدُهما فارغًا."""

    requirement: ClosureRequirement
    what_would_satisfy_it: str
    why_it_is_open: str

    def __post_init__(self) -> None:
        if not self.what_would_satisfy_it.strip():
            raise MinimalCompleteFiberError(
                "شرطٌ بلا مُستوفًى مكتوبٍ يبقى مفتوحًا بلا بابٍ يُغلَق به"
            )
        if not self.why_it_is_open.strip():
            raise MinimalCompleteFiberError("شرطٌ بلا سببٍ مكتوبٍ لانفتاحه يُقرَأ مستوفًى")

    @property
    def is_satisfied(self) -> bool:
        """أاستُوفي؟ لا — والجوابُ ثابتٌ بالبناء لا بالحال الراهنة."""

        return False


@dataclass(frozen=True, slots=True)
class ClosureChecklist:
    """قائمةُ التدقيق كاملةً؛ والمستوفى يُعَدّ ولا يُكتَب بجانبها."""

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
        """المستوفى في القائمة، مُشتقًّا بالعدّ."""

        return sum(1 for item in self.conditions if item.is_satisfied)

    @property
    def total_count(self) -> int:
        """عددُ الشروط كلِّها."""

        return len(self.conditions)

    @property
    def is_complete(self) -> bool:
        """أتُعلَن الشهادة؟ لا ما بقي شرطٌ مفتوح، والرتبةُ لا تُرفَع بالتقريب."""

        return self.satisfied_count == self.total_count


THE_CLOSURE_CHECKLIST: Final[ClosureChecklist] = ClosureChecklist(
    conditions=(
        ChecklistCondition(
            requirement=ClosureRequirement.FUNCTION_AND_DOMAIN_FIXED_BEFOREHAND,
            what_would_satisfy_it=(
                "تسجيلٌ قبليٌّ مُجمَّدٌ يحدّد `F` و`𝒟` قبل أيّ تجربة، بترتيبٍ " "تاريخيٍّ يُتحقَّق منه"
            ),
            why_it_is_open=(
                "لم يُجمَّد ههنا مجالٌ ولا دالّةُ إفادة؛ والمعادلةُ مُودَعةٌ نصًّا "
                "لا تجربةً مُسجَّلةً قبلًا"
            ),
        ),
        ChecklistCondition(
            requirement=ClosureRequirement.CONTENT_REBUILT_FROM_THE_OUTPUT_ALONE,
            what_would_satisfy_it=(
                "قارئٌ مستقلٌّ `D` يُرجِع `F(x)` من `T(x)` وحدَه، بلا قراءةِ الأصل"
            ),
            why_it_is_open=(
                "لا قارئَ مستقلًّا في هذه الوحدة ولا في الشجرة لهذا المخرج، "
                "فالكفايةُ غيرُ مختبَرة"
            ),
        ),
        ChecklistCondition(
            requirement=ClosureRequirement.CLASSIFICATION_NECESSARY_OR_DERIVABLE,
            what_would_satisfy_it=(
                "شاهدان متصادمان تحت `T_{-G}` على مجالٍ مُعلَن، أو بيانُ اشتقاق "
                "الجنس اشتقاقًا وحيدًا مرخَّصًا من المرساة"
            ),
            why_it_is_open=(
                "الشاهدُ المُودَع مُصمَّمٌ على زوجٍ مكتوبٍ ههنا، ولم يُنفَّذ على "
                "مجالٍ مُعلَنٍ ولا على المِرماز"
            ),
        ),
        ChecklistCondition(
            requirement=ClosureRequirement.PREDICATE_NECESSARY,
            what_would_satisfy_it=(
                "شاهدان متصادمان تحت `T_{-P}` على مجالٍ مُعلَن، مع تثبيت المرجع "
                "ونوع الإسناد"
            ),
            why_it_is_open=(
                "زوجُ «زيد طويل/قصير» تصميمٌ مفحوصُ التصادم في التمثيل، لا تنفيذٌ "
                "على مجالٍ مُعلَن"
            ),
        ),
        ChecklistCondition(
            requirement=ClosureRequirement.ATTRIBUTION_NECESSARY_WITH_ITS_SCOPE,
            what_would_satisfy_it=(
                "شاهدان متصادمان تحت `T_{-R}` مع تسمية نطاق الإسناد، ومنعُ استعادة "
                "نوعه من حقلٍ آخرَ أو من الأصل"
            ),
            why_it_is_open=(
                "زوجُ «الرجل الطويل/الرجل طويل» يمنع النسخَ داخل التمثيل، ولا "
                "يُغني عن تثبيت السياق ومنع الاستعادة من الأصل"
            ),
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
    "ADesignedWitnessIsNotAnExecutedCodecTest: الأزواجُ الثلاثةُ تصميمُ شواهدَ "
    "مضادّة مفحوصُ التصادم بالبناء؛ وليست شهادةً بأنّ اختبارَ حذفٍ نُفِّذ على "
    "المِرماز أو على مدوّنةٍ مُبصَّمة، والفرقُ فرقُ جنسٍ لا فرقُ درجة"
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

WITHOUT_AN_INDEPENDENT_READER_SUFFICIENCY_IS_UNTESTED_NOTE: Final[str] = (
    "WithoutAnIndependentReaderSufficiencyIsUntested: `D(T(x)) = F(x)` شطرٌ لا "
    "يُفحَص بلا قارئٍ مستقلٍّ ودالّةِ إفادةٍ على مجالٍ مُعلَن؛ وغيابُه ليس سقوطَ "
    "الكفاية ولا ثبوتَها، بل عدمُ اختبارها — ولا يُرفَع المعيارُ بشطر الضرورة وحدَه"
)

ZERO_IS_AN_UNNAMED_RELATION_NOT_AN_EMPTY_FIBER_NOTE: Final[str] = (
    "ZeroIsAnUnnamedRelationNotAnEmptyFiber: `Z = (a, g, p, ⊥)` حاملٌ مصنَّفٌ "
    "ومحمولٌ مرشَّحٌ لم يُعيَّن وجهُ ربطهما؛ فليست `zero` ليفًا خاليًا ولا صفةً "
    "منفيّة، والخلطُ بينهما يجعل عدمَ التعيين نفيًا"
)

MINIMAL_COMPLETE_FIBER_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    FOUR_FIELDS_CARRY_THREE_FUNCTIONS_NOTE,
    WITHOUT_AN_INDEPENDENT_READER_SUFFICIENCY_IS_UNTESTED_NOTE,
    A_DESIGNED_WITNESS_IS_NOT_AN_EXECUTED_CODEC_TEST_NOTE,
    A_COLLISION_IN_THE_REPRESENTATION_IS_NOT_A_COLLISION_IN_CONTEXT_NOTE,
    ZERO_IS_AN_UNNAMED_RELATION_NOT_AN_EMPTY_FIBER_NOTE,
    ONE_IS_A_NAMED_ATTRIBUTION_NOT_A_TRUE_PROPOSITION_NOTE,
    THE_RELATION_VOCABULARY_IS_NOT_CLAIMED_EXHAUSTIVE_NOTE,
    THE_MINIMUM_IS_RELATIVE_TO_THE_TESTED_ALTERNATIVES_NOTE,
)
"""ثماني بقايا مُسمّاةٍ تُقابَل بها أيُّ إحالةٍ إلى «الحدّ الأدنى المكتمل»."""
