"""برهان صوري شامل على نطاق محدود: تصنيف علاقة اللفظ بمدلوله سبعةَ أقسام.

المصدر النصّي — يُذكَر بالاسم لا إحالةً مبهمة — كتاب "الشخصية الإسلامية" الجزء
الثالث، في علاقة اللفظ بالمعنى:

    "أن يتحد اللفظ والمعنى كلفظ الله، فإنه واحد ومدلوله واحد، وهو المنفرد."
    "أن يتكثر اللفظ ويتكثر المعنى كالسواد والبياض، وهو المتباين."
    "أن يتكثر اللفظ ويتحد المعنى مثل الأسد والسبع، وهو المترادف."
    "أن يتكثر المعنى ويتحد اللفظ... كالعين للباصرة والجارية، وهو المشترك."
    "وُضع لمعنى ثم نُقل إلى غيره واشتهر في المعنى الثاني... كالصلاة... وهو
    المنقول."
    "وُضع لمعنى ثم نُقل إلى غيره لعلاقة، ولكنه لم يشتهر في المعنى الثاني...
    فإن أُطلق على المعنى الموضوع له فهو الحقيقة، وإن أُطلق على المعنى المنقول
    إليه فهو المجاز."

هذه الوحدة تبني — بنفس نمط `word_class_formal.py`، وعلى معيار
`NoBirthWithoutResidualOrFormalNecessity` في وضعه الصوري (`FORMAL`) وصفًا لا
تفعيلًا — مجالًا صوريًّا مجمَّدًا، ودالةَ قرارٍ كلّيةً عليه، ثم برهانًا شاملًا
على سبعة شواهد مُثبَتة بأعيانها في المصدر نفسه، واحدٍ لكل فرع بالضبط.

الفارق البنيوي عن الشهادة الأولى — تصريحٌ لا تفصيل لاحق: الوحدة المُصنَّفة هنا
**عنقود لفظي** (لفظ أو أكثر مرتبط بمعنى أو أكثر، مع الاستعمال المُختبَر بعينه)،
لا لفظٌ مفردٌ معزول؛ لأن "متباين" و"مترادف" يصفان علاقةً بين ألفاظ متعدّدة، ولأن
"حقيقة" و"مجاز" يفترقان بالاستعمال المُختبَر لا باللفظ المجرَّد. فـ"الأسد" في
معناها الأول و"الأسد" في المعنى المنقول إليه عنقودان متمايزان لا عنقودٌ واحد.

بنية المجال — `card(Ω) = 7` بالضبط، لا أكثر ولا أقل:

* س١ = "عدد الألفاظ في العنقود؟" (واحد / متعدّد)، تُطرَح دائمًا.
* س٢ = "عدد المعاني المرتبطة به؟" (واحد / متعدّد)، تُطرَح دائمًا.
* س٣ = "وُضع اللفظ لكل معنى من هذه المعاني ابتداءً؟"، ولا تُطرَح إلا إذا كانت
  س١ = واحد وس٢ = متعدّد.
* س٤ = "هل اشتهر اللفظ في المعنى الثاني حتى هُجر الأول؟"، ولا تُطرَح إلا إذا
  كانت إجابة س٣ = لا.
* س٥ = "أيّ معنى يُقصَد بإطلاق اللفظ في الاستعمال المُختبَر؟" (الأول / الثاني)،
  ولا تُطرَح إلا إذا كانت إجابة س٤ = لا.

فالحالات المقبولة سبع لا غير، وقيمة `غير_مطروح` قيمةٌ مصرَّح بها في المفردات
المغلقة، لا `None` صامتة ولا غياب حقل: التصريح بأن السؤال لم يُطرَح أصلًا جزءٌ
من البنية، وبه تُغلَق كل حالة خارج السبع بنيويًّا بدل أن تتسلّل بصمت.

ولا تُكتَب إجابةٌ اعتباطًا: كلٌّ منها تُشتَقّ من حقل بيانات مُدخَل، بنفس انضباط
"حامل الدلالة الزمنية" في الشهادة الأولى. فس١ وس٢ تُشتَقّان من عدد الألفاظ وعدد
المعاني الفعليّين، وس٣ من **حامل الوضع الابتدائي**، وس٤ من **حامل الاشتهار
والهجر**، وس٥ من **حامل المعنى المقصود بالاستعمال**؛ ويُرفَض أي شاهد كُتبت فيه
إجابةٌ مخالفةً لحاملها.

نطاق الوحدة وحدودها — تسجيل صريح، لا اعتذار لاحق:

* النطاق سبعة شواهد مُثبَتة من نصّ واحد بعينه، وسبعة تصنيفات لا ثامن لها هنا.
  ولا تتناول هذه الوحدة أقسام العلاقة المجازية (مشابهة، مجاورة، سببية...) ولا
  الكناية ولا الاستعارة: تلك تحتاج شواهد لكل قيمة ليكون المجال مكتمل الفروع
  بالبناء، ولا نملكها هنا، وإدخالها الآن ادّعاءُ نطاقٍ غير مبرهَن.
* سلطويًّا: `FormalClassification != BirthVerdict`، و
  `DeclaredRelation != BornOntology`. هذا توثيق وتصنيف صوري فقط: لا نوع في
  `kernel/`، ولا `Freeze`، ولا `E0`، ولا بوّابة نواة تقرأ هذه المخرجات. لا
  تدخل نتيجة هذه الوحدة في `BirthExperimentSpecification`، ولا يقرأها
  `IndependentClosureGate` ولا `BirthVerdictGate`، ولا تغيّر نتيجة التدقيق
  الخارجي.
* عند نجاح البرهان الشامل تُستعمل التسمية الدقيقة وحدها: "شهادة صورية شاملة
  ناجحة على نطاق محدود" — لا "ولادة"، فتلك تسمية لاحقة تحتاج `Freeze` و`E0` لم
  يُبنَيا بعد.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

from .text_key import comparison_key


class LafzMadlulRelationError(ValueError):
    """رُفض مدخلٌ خارج المجال الصوري المجمَّد؛ لا يُحمَل على أقرب حالة."""


class RelationCount(Enum):
    """مفردة العدد المغلقة: واحد أو متعدّد، لا ثالث لهما."""

    ONE = "واحد"
    MANY = "متعدّد"


class RelationAnswer(Enum):
    """مفردة الإجابات المغلقة؛ `غير_مطروح` تصريحٌ لا صمت."""

    YES = "نعم"
    NO = "لا"
    NOT_ASKED = "غير_مطروح"


class IntendedMeaning(Enum):
    """المعنى المقصود بالإطلاق؛ `غير_مطروح` تصريحٌ لا صمت."""

    FIRST = "الأول"
    SECOND = "الثاني"
    NOT_ASKED = "غير_مطروح"


class LafzMadlulRelation(Enum):
    """التصنيفات السبعة المغلقة؛ لا ثامن لها في هذا النطاق."""

    MUNFARID = "منفرد"
    MUTABAYIN = "متباين"
    MURADIF = "مترادف"
    MUSHTARAK = "مشترك"
    MANQUL = "منقول"
    HAQIQA = "حقيقة"
    MAJAZ = "مجاز"


class InitialAssignmentCarrier(Enum):
    """حامل الوضع الابتدائي؛ منه تُشتَقّ إجابة س٣ ولا تُكتَب اعتباطًا."""

    FOR_EACH_MEANING = "وُضع_لكل_معنى_ابتداءً"
    FOR_ONE_MEANING = "وُضع_لمعنى_واحد_ابتداءً"
    NOT_APPLICABLE = "لا_ينطبق"


class TransferFameCarrier(Enum):
    """حامل الاشتهار والهجر؛ منه تُشتَقّ إجابة س٤ ولا تُكتَب اعتباطًا."""

    FAMOUS_UNTIL_FIRST_ABANDONED = "اشتهر_حتى_هُجر_الأول"
    NOT_FAMOUS = "لم_يشتهر_هجرًا_للأول"
    NOT_APPLICABLE = "لا_ينطبق"


class UsageIntentCarrier(Enum):
    """حامل المعنى المقصود بالاستعمال؛ منه تُشتَقّ إجابة س٥ ولا تُكتَب اعتباطًا."""

    ASSIGNED_MEANING = "الموضوع_له_ابتداءً"
    TRANSFERRED_MEANING = "المنقول_إليه"
    NOT_APPLICABLE = "لا_ينطبق"


RELATION_SOURCE: Final = "الشخصية الإسلامية، الجزء الثالث، في علاقة اللفظ بالمعنى"

RELATION_FIRST_QUESTION: Final = "عدد الألفاظ في العنقود؟"

RELATION_SECOND_QUESTION: Final = "عدد المعاني المرتبطة به؟"

RELATION_THIRD_QUESTION: Final = "وُضع اللفظ لكل معنى من هذه المعاني ابتداءً؟"

RELATION_FOURTH_QUESTION: Final = "هل اشتهر اللفظ في المعنى الثاني حتى هُجر الأول؟"

RELATION_FIFTH_QUESTION: Final = "أيّ معنى يُقصَد بإطلاق اللفظ في الاستعمال المُختبَر؟"

RELATION_THIRD_QUESTION_CONDITION: Final = (
    "لا تُطرَح س٣ إلا إذا كانت س١ = واحد وس٢ = متعدّد"
)

RELATION_FOURTH_QUESTION_CONDITION: Final = "لا تُطرَح س٤ إلا إذا كانت إجابة س٣ = لا"

RELATION_FIFTH_QUESTION_CONDITION: Final = "لا تُطرَح س٥ إلا إذا كانت إجابة س٤ = لا"

RELATION_SUCCESS_TITLE: Final = "شهادة صورية شاملة ناجحة على نطاق محدود"

RELATION_SCOPE_NOTE: Final = (
    "نطاق هذا البرهان سبعة شواهد مُثبَتة من مصدر واحد بعينه وسبعة تصنيفات "
    "مغلقة؛ فأقسام العلاقة المجازية والكناية والاستعارة خارجه بالتصريح لا "
    "بالسهو، لافتقارها إلى شاهد لكل قيمة يجعل المجال مكتمل الفروع بالبناء"
)

RELATION_AUTHORITY_NOTE: Final = (
    "تصنيف صوري وتوثيق فقط: لا يُنتج ولادةً ولا حكم ولادة، ولا يُجمَّد، ولا "
    "تقرأه أيّ بوّابة في النواة"
)

NOT_APPLICABLE_TEXT: Final = "لا_ينطبق"

RelationState = tuple[
    RelationCount, RelationCount, RelationAnswer, RelationAnswer, IntendedMeaning
]

RELATION_ADMISSIBLE_STATES: Final[tuple[RelationState, ...]] = (
    (
        RelationCount.ONE,
        RelationCount.ONE,
        RelationAnswer.NOT_ASKED,
        RelationAnswer.NOT_ASKED,
        IntendedMeaning.NOT_ASKED,
    ),
    (
        RelationCount.MANY,
        RelationCount.MANY,
        RelationAnswer.NOT_ASKED,
        RelationAnswer.NOT_ASKED,
        IntendedMeaning.NOT_ASKED,
    ),
    (
        RelationCount.MANY,
        RelationCount.ONE,
        RelationAnswer.NOT_ASKED,
        RelationAnswer.NOT_ASKED,
        IntendedMeaning.NOT_ASKED,
    ),
    (
        RelationCount.ONE,
        RelationCount.MANY,
        RelationAnswer.YES,
        RelationAnswer.NOT_ASKED,
        IntendedMeaning.NOT_ASKED,
    ),
    (
        RelationCount.ONE,
        RelationCount.MANY,
        RelationAnswer.NO,
        RelationAnswer.YES,
        IntendedMeaning.NOT_ASKED,
    ),
    (
        RelationCount.ONE,
        RelationCount.MANY,
        RelationAnswer.NO,
        RelationAnswer.NO,
        IntendedMeaning.FIRST,
    ),
    (
        RelationCount.ONE,
        RelationCount.MANY,
        RelationAnswer.NO,
        RelationAnswer.NO,
        IntendedMeaning.SECOND,
    ),
)

_DECISION: Final[dict[RelationState, LafzMadlulRelation]] = {
    RELATION_ADMISSIBLE_STATES[0]: LafzMadlulRelation.MUNFARID,
    RELATION_ADMISSIBLE_STATES[1]: LafzMadlulRelation.MUTABAYIN,
    RELATION_ADMISSIBLE_STATES[2]: LafzMadlulRelation.MURADIF,
    RELATION_ADMISSIBLE_STATES[3]: LafzMadlulRelation.MUSHTARAK,
    RELATION_ADMISSIBLE_STATES[4]: LafzMadlulRelation.MANQUL,
    RELATION_ADMISSIBLE_STATES[5]: LafzMadlulRelation.HAQIQA,
    RELATION_ADMISSIBLE_STATES[6]: LafzMadlulRelation.MAJAZ,
}

_THIRD_ANSWER_BY_CARRIER: Final = {
    InitialAssignmentCarrier.FOR_EACH_MEANING: RelationAnswer.YES,
    InitialAssignmentCarrier.FOR_ONE_MEANING: RelationAnswer.NO,
    InitialAssignmentCarrier.NOT_APPLICABLE: RelationAnswer.NOT_ASKED,
}

_FOURTH_ANSWER_BY_CARRIER: Final = {
    TransferFameCarrier.FAMOUS_UNTIL_FIRST_ABANDONED: RelationAnswer.YES,
    TransferFameCarrier.NOT_FAMOUS: RelationAnswer.NO,
    TransferFameCarrier.NOT_APPLICABLE: RelationAnswer.NOT_ASKED,
}

_FIFTH_ANSWER_BY_CARRIER: Final = {
    UsageIntentCarrier.ASSIGNED_MEANING: IntendedMeaning.FIRST,
    UsageIntentCarrier.TRANSFERRED_MEANING: IntendedMeaning.SECOND,
    UsageIntentCarrier.NOT_APPLICABLE: IntendedMeaning.NOT_ASKED,
}

if len(RELATION_ADMISSIBLE_STATES) != len(
    set(RELATION_ADMISSIBLE_STATES)
):  # pragma: no cover - guard
    raise RuntimeError("the admissible states are not seven distinct states")
if set(_DECISION) != set(RELATION_ADMISSIBLE_STATES):  # pragma: no cover - guard
    raise RuntimeError("the decision function does not cover the admissible domain")
if set(_DECISION.values()) != set(LafzMadlulRelation):  # pragma: no cover - guard
    raise RuntimeError("a declared relation has no admissible state")
if len(_THIRD_ANSWER_BY_CARRIER) != len(InitialAssignmentCarrier):  # pragma: no cover
    raise RuntimeError("an initial-assignment carrier derives no third answer")
if len(_FOURTH_ANSWER_BY_CARRIER) != len(TransferFameCarrier):  # pragma: no cover
    raise RuntimeError("a transfer-fame carrier derives no fourth answer")
if len(_FIFTH_ANSWER_BY_CARRIER) != len(UsageIntentCarrier):  # pragma: no cover
    raise RuntimeError("a usage-intent carrier derives no fifth answer")


def _require_count(count: RelationCount, field_name: str) -> RelationCount:
    if not isinstance(count, RelationCount):
        raise LafzMadlulRelationError(
            f"{field_name} must come from the closed vocabulary"
        )
    return count


def _require_answer(answer: RelationAnswer, field_name: str) -> RelationAnswer:
    if not isinstance(answer, RelationAnswer):
        raise LafzMadlulRelationError(
            f"{field_name} must come from the closed vocabulary"
        )
    return answer


def _require_intended(meaning: IntendedMeaning, field_name: str) -> IntendedMeaning:
    if not isinstance(meaning, IntendedMeaning):
        raise LafzMadlulRelationError(
            f"{field_name} must come from the closed vocabulary"
        )
    return meaning


@dataclass(frozen=True, slots=True)
class FrozenRelationDomain:
    """المجال الصوري المجمَّد: أسئلته الخمسة، وشروطها، وحالاته السبع، ومصدره."""

    source: str = RELATION_SOURCE
    first_question: str = RELATION_FIRST_QUESTION
    second_question: str = RELATION_SECOND_QUESTION
    third_question: str = RELATION_THIRD_QUESTION
    fourth_question: str = RELATION_FOURTH_QUESTION
    fifth_question: str = RELATION_FIFTH_QUESTION
    third_question_condition: str = RELATION_THIRD_QUESTION_CONDITION
    fourth_question_condition: str = RELATION_FOURTH_QUESTION_CONDITION
    fifth_question_condition: str = RELATION_FIFTH_QUESTION_CONDITION
    admissible_states: tuple[RelationState, ...] = RELATION_ADMISSIBLE_STATES

    def __post_init__(self) -> None:
        for name in (
            "source",
            "first_question",
            "second_question",
            "third_question",
            "fourth_question",
            "fifth_question",
        ):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise LafzMadlulRelationError(f"{name} must be non-blank text")
        if set(self.admissible_states) != set(RELATION_ADMISSIBLE_STATES):
            raise LafzMadlulRelationError(
                "the frozen formal domain is exactly the seven admissible states"
            )

    @property
    def cardinality(self) -> int:
        """عدد الحالات المقبولة في المجال: سبع بالضبط."""

        return len(self.admissible_states)


FROZEN_RELATION_DOMAIN: Final = FrozenRelationDomain()


def canonical_relation_count(value: str) -> RelationCount:
    """أعِد العدد المسمّى في `value`؛ وأيّ لفظ آخر يُرَدّ ولا يُقرَّب."""

    if not isinstance(value, str) or not value.strip():
        raise LafzMadlulRelationError("العدد must be non-blank text")
    key = comparison_key(value)
    for count in RelationCount:
        if comparison_key(count.value) == key:
            return count
    raise LafzMadlulRelationError(
        "العدد must be one of: " + "، ".join(count.value for count in RelationCount)
    )


def canonical_relation_answer(value: str) -> RelationAnswer:
    """أعِد الإجابة المسمّاة في `value`؛ وأيّ لفظ آخر يُرَدّ ولا يُقرَّب."""

    if not isinstance(value, str) or not value.strip():
        raise LafzMadlulRelationError("الإجابة must be non-blank text")
    key = comparison_key(value)
    for answer in RelationAnswer:
        if comparison_key(answer.value) == key:
            return answer
    raise LafzMadlulRelationError(
        "الإجابة must be one of: "
        + "، ".join(answer.value for answer in RelationAnswer)
    )


def canonical_intended_meaning(value: str) -> IntendedMeaning:
    """أعِد المعنى المقصود المسمّى في `value`؛ وأيّ لفظ آخر يُرَدّ ولا يُقرَّب."""

    if not isinstance(value, str) or not value.strip():
        raise LafzMadlulRelationError("المعنى المقصود must be non-blank text")
    key = comparison_key(value)
    for meaning in IntendedMeaning:
        if comparison_key(meaning.value) == key:
            return meaning
    raise LafzMadlulRelationError(
        "المعنى المقصود must be one of: "
        + "، ".join(meaning.value for meaning in IntendedMeaning)
    )


def is_third_question_asked(first: RelationCount, second: RelationCount) -> bool:
    """هل تُطرَح س٣ أصلًا؟ تُطرَح إن وإن فقط كان اللفظ واحدًا والمعاني متعدّدة."""

    return (
        _require_count(first, "س١") is RelationCount.ONE
        and _require_count(second, "س٢") is RelationCount.MANY
    )


def is_fourth_question_asked(third: RelationAnswer) -> bool:
    """هل تُطرَح س٤ أصلًا؟ تُطرَح إن وإن فقط كانت إجابة س٣ = لا."""

    return _require_answer(third, "س٣") is RelationAnswer.NO


def is_fifth_question_asked(fourth: RelationAnswer) -> bool:
    """هل تُطرَح س٥ أصلًا؟ تُطرَح إن وإن فقط كانت إجابة س٤ = لا."""

    return _require_answer(fourth, "س٤") is RelationAnswer.NO


def classify_relation(
    first: RelationCount,
    second: RelationCount,
    third: RelationAnswer,
    fourth: RelationAnswer,
    fifth: IntendedMeaning,
) -> LafzMadlulRelation:
    """التصنيف المشتقّ من الإجابات اشتقاقًا مباشرًا، بلا تخمين ولا فرع افتراضي.

    واحد×واحد → منفرد. ومتعدّد×متعدّد → متباين. ومتعدّد×واحد → مترادف.
    وواحد×متعدّد مع س٣=نعم → مشترك، ومع س٣=لا وس٤=نعم → منقول، ومع س٤=لا
    وس٥=الأول → حقيقة، ومع س٤=لا وس٥=الثاني → مجاز. وأيّ حالة خارج هذه السبع
    — ومنها سؤالٌ أُجيب وهو غير مطروح، أو سؤالٌ مطروح تُرك `غير_مطروح` —
    تُرَدّ بخطأ ولا تُصنَّف.
    """

    state: RelationState = (
        _require_count(first, "س١"),
        _require_count(second, "س٢"),
        _require_answer(third, "س٣"),
        _require_answer(fourth, "س٤"),
        _require_intended(fifth, "س٥"),
    )
    third_asked = state[2] is not RelationAnswer.NOT_ASKED
    if is_third_question_asked(state[0], state[1]) != third_asked:
        raise LafzMadlulRelationError(RELATION_THIRD_QUESTION_CONDITION)
    fourth_asked = state[3] is not RelationAnswer.NOT_ASKED
    if (third_asked and is_fourth_question_asked(state[2])) != fourth_asked:
        raise LafzMadlulRelationError(RELATION_FOURTH_QUESTION_CONDITION)
    fifth_asked = state[4] is not IntendedMeaning.NOT_ASKED
    if (fourth_asked and is_fifth_question_asked(state[3])) != fifth_asked:
        raise LafzMadlulRelationError(RELATION_FIFTH_QUESTION_CONDITION)
    relation = _DECISION.get(state)
    if relation is None:  # pragma: no cover - guard
        raise LafzMadlulRelationError("حالة خارج المجال الصوري المجمَّد")
    return relation


@dataclass(frozen=True, slots=True)
class AttestedLexemeCluster:
    """عنقود لفظي مُثبَت نصًّا: ألفاظه ومعانيه وحوامله وأدلّته وتصنيفه المنصوص."""

    lexemes: tuple[str, ...]
    meanings: tuple[str, ...]
    tested_usage: str
    first_evidence: str
    second_evidence: str
    third_answer: RelationAnswer
    third_evidence: str
    fourth_answer: RelationAnswer
    fourth_evidence: str
    fifth_answer: IntendedMeaning
    fifth_evidence: str
    initial_assignment_carrier: InitialAssignmentCarrier
    transfer_fame_carrier: TransferFameCarrier
    usage_intent_carrier: UsageIntentCarrier
    majaz_relation: str
    attested_relation: LafzMadlulRelation
    source: str

    def __post_init__(self) -> None:
        for name in (
            "tested_usage",
            "first_evidence",
            "second_evidence",
            "third_evidence",
            "fourth_evidence",
            "fifth_evidence",
            "majaz_relation",
            "source",
        ):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise LafzMadlulRelationError(f"{name} must be non-blank text")
        for name in ("lexemes", "meanings"):
            values = getattr(self, name)
            if not isinstance(values, tuple) or not values:
                raise LafzMadlulRelationError(f"{name} must be a non-empty tuple")
            if any(not isinstance(item, str) or not item.strip() for item in values):
                raise LafzMadlulRelationError(f"{name} entries must be non-blank text")
            if len({comparison_key(item) for item in values}) != len(values):
                raise LafzMadlulRelationError(
                    f"{name} must not repeat the same entry twice"
                )
        _require_answer(self.third_answer, "س٣")
        _require_answer(self.fourth_answer, "س٤")
        _require_intended(self.fifth_answer, "س٥")
        if not isinstance(self.initial_assignment_carrier, InitialAssignmentCarrier):
            raise LafzMadlulRelationError(
                "حامل الوضع الابتدائي must come from the closed vocabulary"
            )
        if not isinstance(self.transfer_fame_carrier, TransferFameCarrier):
            raise LafzMadlulRelationError(
                "حامل الاشتهار والهجر must come from the closed vocabulary"
            )
        if not isinstance(self.usage_intent_carrier, UsageIntentCarrier):
            raise LafzMadlulRelationError(
                "حامل المعنى المقصود must come from the closed vocabulary"
            )
        if not isinstance(self.attested_relation, LafzMadlulRelation):
            raise LafzMadlulRelationError(
                "التصنيف المنصوص must come from the closed vocabulary"
            )
        if (
            self.third_answer
            is not _THIRD_ANSWER_BY_CARRIER[self.initial_assignment_carrier]
        ):
            raise LafzMadlulRelationError(
                "إجابة س٣ تُشتَقّ من حامل الوضع الابتدائي ولا تُكتَب اعتباطًا"
            )
        if (
            self.fourth_answer
            is not _FOURTH_ANSWER_BY_CARRIER[self.transfer_fame_carrier]
        ):
            raise LafzMadlulRelationError(
                "إجابة س٤ تُشتَقّ من حامل الاشتهار والهجر ولا تُكتَب اعتباطًا"
            )
        if self.fifth_answer is not _FIFTH_ANSWER_BY_CARRIER[self.usage_intent_carrier]:
            raise LafzMadlulRelationError(
                "إجابة س٥ تُشتَقّ من حامل المعنى المقصود ولا تُكتَب اعتباطًا"
            )
        if (
            self.second_answer is RelationCount.ONE
            and self.transfer_fame_carrier
            is TransferFameCarrier.FAMOUS_UNTIL_FIRST_ABANDONED
        ):
            raise LafzMadlulRelationError(
                "عنقودٌ بمعنى واحد لا يُقال فيه اشتهر في المعنى الثاني"
            )
        relation = self.derived_relation
        is_majaz = relation is LafzMadlulRelation.MAJAZ
        if is_majaz and comparison_key(self.majaz_relation) == comparison_key(
            NOT_APPLICABLE_TEXT
        ):
            raise LafzMadlulRelationError(
                "فرع المجاز يلزمه تصريحٌ بالعلاقة المعتبَرة عند العرب"
            )
        if not is_majaz and comparison_key(self.majaz_relation) != comparison_key(
            NOT_APPLICABLE_TEXT
        ):
            raise LafzMadlulRelationError(
                f"العلاقة تُصرَّح على فرع المجاز وحده، وعلى ما عداه تكون "
                f"{NOT_APPLICABLE_TEXT}"
            )

    @property
    def first_answer(self) -> RelationCount:
        """إجابة س١ مشتقّة من عدد الألفاظ الفعلي، لا مكتوبةً بيدٍ حرّة."""

        return RelationCount.ONE if len(self.lexemes) == 1 else RelationCount.MANY

    @property
    def second_answer(self) -> RelationCount:
        """إجابة س٢ مشتقّة من عدد المعاني الفعلي، لا مكتوبةً بيدٍ حرّة."""

        return RelationCount.ONE if len(self.meanings) == 1 else RelationCount.MANY

    @property
    def cluster_key(self) -> tuple[tuple[str, ...], str]:
        """هوية العنقود: ألفاظه مع الاستعمال المُختبَر، لا اللفظ المجرَّد وحده."""

        return (
            tuple(comparison_key(lexeme) for lexeme in self.lexemes),
            comparison_key(self.tested_usage),
        )

    @property
    def derived_relation(self) -> LafzMadlulRelation:
        """التصنيف المشتقّ من الدالة الصورية وحدها، لا من التصنيف المنصوص."""

        return classify_relation(
            self.first_answer,
            self.second_answer,
            self.third_answer,
            self.fourth_answer,
            self.fifth_answer,
        )


_SHAKHSIYYA: Final = RELATION_SOURCE

ATTESTED_CLUSTERS: Final = (
    AttestedLexemeCluster(
        lexemes=("الله",),
        meanings=("الذات الواجب الوجود",),
        tested_usage="إطلاق لفظ الجلالة على مدلوله الواحد",
        first_evidence=(
            "أن يتحد اللفظ والمعنى كلفظ الله، فإنه واحد ومدلوله واحد، وهو المنفرد."
        ),
        second_evidence="فإنه واحد ومدلوله واحد",
        third_answer=RelationAnswer.NOT_ASKED,
        third_evidence=(
            "لم تُطرَح س٣ لأن المعنى واحد، فلا يُسأل عن وضع اللفظ لكل معنى ابتداءً"
        ),
        fourth_answer=RelationAnswer.NOT_ASKED,
        fourth_evidence="لم تُطرَح س٤ لانقطاع السؤال عند س٣ غير المطروحة",
        fifth_answer=IntendedMeaning.NOT_ASKED,
        fifth_evidence="لم تُطرَح س٥ لانقطاع السؤال عند س٤ غير المطروحة",
        initial_assignment_carrier=InitialAssignmentCarrier.NOT_APPLICABLE,
        transfer_fame_carrier=TransferFameCarrier.NOT_APPLICABLE,
        usage_intent_carrier=UsageIntentCarrier.NOT_APPLICABLE,
        majaz_relation=NOT_APPLICABLE_TEXT,
        attested_relation=LafzMadlulRelation.MUNFARID,
        source=_SHAKHSIYYA,
    ),
    AttestedLexemeCluster(
        lexemes=("السواد", "البياض"),
        meanings=("اللون الأسود", "اللون الأبيض"),
        tested_usage="إطلاق كلٍّ من اللفظين على معناه المغاير لمعنى الآخر",
        first_evidence="أن يتكثر اللفظ ويتكثر المعنى كالسواد والبياض، وهو المتباين.",
        second_evidence="ويتكثر المعنى كالسواد والبياض",
        third_answer=RelationAnswer.NOT_ASKED,
        third_evidence=(
            "لم تُطرَح س٣ لأن الألفاظ متعدّدة، فلا يُسأل عن لفظٍ واحد وُضع لمعانٍ"
        ),
        fourth_answer=RelationAnswer.NOT_ASKED,
        fourth_evidence="لم تُطرَح س٤ لانقطاع السؤال عند س٣ غير المطروحة",
        fifth_answer=IntendedMeaning.NOT_ASKED,
        fifth_evidence="لم تُطرَح س٥ لانقطاع السؤال عند س٤ غير المطروحة",
        initial_assignment_carrier=InitialAssignmentCarrier.NOT_APPLICABLE,
        transfer_fame_carrier=TransferFameCarrier.NOT_APPLICABLE,
        usage_intent_carrier=UsageIntentCarrier.NOT_APPLICABLE,
        majaz_relation=NOT_APPLICABLE_TEXT,
        attested_relation=LafzMadlulRelation.MUTABAYIN,
        source=_SHAKHSIYYA,
    ),
    AttestedLexemeCluster(
        lexemes=("الأسد", "السبع"),
        meanings=("الحيوان المفترس المعروف",),
        tested_usage="إطلاق اللفظين معًا على المعنى الواحد نفسه",
        first_evidence="أن يتكثر اللفظ ويتحد المعنى مثل الأسد والسبع، وهو المترادف.",
        second_evidence="ويتحد المعنى مثل الأسد والسبع",
        third_answer=RelationAnswer.NOT_ASKED,
        third_evidence=(
            "لم تُطرَح س٣ لأن الألفاظ متعدّدة والمعنى واحد، فانقطع سؤال الوضع " "لكل معنى"
        ),
        fourth_answer=RelationAnswer.NOT_ASKED,
        fourth_evidence="لم تُطرَح س٤ لانقطاع السؤال عند س٣ غير المطروحة",
        fifth_answer=IntendedMeaning.NOT_ASKED,
        fifth_evidence="لم تُطرَح س٥ لانقطاع السؤال عند س٤ غير المطروحة",
        initial_assignment_carrier=InitialAssignmentCarrier.NOT_APPLICABLE,
        transfer_fame_carrier=TransferFameCarrier.NOT_APPLICABLE,
        usage_intent_carrier=UsageIntentCarrier.NOT_APPLICABLE,
        majaz_relation=NOT_APPLICABLE_TEXT,
        attested_relation=LafzMadlulRelation.MURADIF,
        source=_SHAKHSIYYA,
    ),
    AttestedLexemeCluster(
        lexemes=("العين",),
        meanings=("الباصرة", "الجارية"),
        tested_usage="إطلاق اللفظ الواحد على كلٍّ من معنييه الموضوع لهما ابتداءً",
        first_evidence=(
            "أن يتكثر المعنى ويتحد اللفظ... كالعين للباصرة والجارية، وهو " "المشترك."
        ),
        second_evidence="أن يتكثر المعنى... كالعين للباصرة والجارية",
        third_answer=RelationAnswer.YES,
        third_evidence="كالعين للباصرة والجارية: وُضع لكلٍّ منهما ابتداءً لا نقلًا",
        fourth_answer=RelationAnswer.NOT_ASKED,
        fourth_evidence="لم تُطرَح س٤ لأن إجابة س٣ = نعم، فلا نقل يُسأل عن اشتهاره",
        fifth_answer=IntendedMeaning.NOT_ASKED,
        fifth_evidence="لم تُطرَح س٥ لانقطاع السؤال عند س٤ غير المطروحة",
        initial_assignment_carrier=InitialAssignmentCarrier.FOR_EACH_MEANING,
        transfer_fame_carrier=TransferFameCarrier.NOT_APPLICABLE,
        usage_intent_carrier=UsageIntentCarrier.NOT_APPLICABLE,
        majaz_relation=NOT_APPLICABLE_TEXT,
        attested_relation=LafzMadlulRelation.MUSHTARAK,
        source=_SHAKHSIYYA,
    ),
    AttestedLexemeCluster(
        lexemes=("الصلاة",),
        meanings=("الدعاء", "الأفعال المخصوصة"),
        tested_usage="إطلاق اللفظ في نطاق الشرع بعد اشتهاره في المعنى الثاني",
        first_evidence=(
            "وُضع لمعنى ثم نُقل إلى غيره واشتهر في المعنى الثاني... كالصلاة... "
            "وهو المنقول."
        ),
        second_evidence="وُضع لمعنى ثم نُقل إلى غيره: فالمعاني اثنان لا واحد",
        third_answer=RelationAnswer.NO,
        third_evidence="وُضع لمعنى [الدعاء] ثم نُقل إلى غيره، فلم يُوضَع لكلٍّ ابتداءً",
        fourth_answer=RelationAnswer.YES,
        fourth_evidence="واشتهر في المعنى الثاني... كالصلاة",
        fifth_answer=IntendedMeaning.NOT_ASKED,
        fifth_evidence=(
            "لم تُطرَح س٥ لأن الاشتهار وقع حتى هُجر الأول، فلا يُسأل عن أيّ " "المعنيين قُصِد"
        ),
        initial_assignment_carrier=InitialAssignmentCarrier.FOR_ONE_MEANING,
        transfer_fame_carrier=TransferFameCarrier.FAMOUS_UNTIL_FIRST_ABANDONED,
        usage_intent_carrier=UsageIntentCarrier.NOT_APPLICABLE,
        majaz_relation=NOT_APPLICABLE_TEXT,
        attested_relation=LafzMadlulRelation.MANQUL,
        source=_SHAKHSIYYA,
    ),
    AttestedLexemeCluster(
        lexemes=("الأسد",),
        meanings=("الحيوان المفترس", "الرجل الشجاع"),
        tested_usage="إطلاق اللفظ على الحيوان المفترس، وهو المعنى الموضوع له ابتداءً",
        first_evidence=(
            "وُضع لمعنى ثم نُقل إلى غيره لعلاقة، ولكنه لم يشتهر في المعنى " "الثاني..."
        ),
        second_evidence="وُضع لمعنى ثم نُقل إلى غيره لعلاقة: فالمعاني اثنان",
        third_answer=RelationAnswer.NO,
        third_evidence="وُضع لمعنى ثم نُقل إلى غيره، فلم يُوضَع لكلٍّ منهما ابتداءً",
        fourth_answer=RelationAnswer.NO,
        fourth_evidence="ولكنه لم يشتهر في المعنى الثاني",
        fifth_answer=IntendedMeaning.FIRST,
        fifth_evidence="فإن أُطلق على المعنى الموضوع له فهو الحقيقة",
        initial_assignment_carrier=InitialAssignmentCarrier.FOR_ONE_MEANING,
        transfer_fame_carrier=TransferFameCarrier.NOT_FAMOUS,
        usage_intent_carrier=UsageIntentCarrier.ASSIGNED_MEANING,
        majaz_relation=NOT_APPLICABLE_TEXT,
        attested_relation=LafzMadlulRelation.HAQIQA,
        source=_SHAKHSIYYA,
    ),
    AttestedLexemeCluster(
        lexemes=("الأسد",),
        meanings=("الحيوان المفترس", "الرجل الشجاع"),
        tested_usage="إطلاق اللفظ على الرجل الشجاع، وهو المعنى المنقول إليه",
        first_evidence=(
            "وُضع لمعنى ثم نُقل إلى غيره لعلاقة، ولكنه لم يشتهر في المعنى " "الثاني..."
        ),
        second_evidence="وُضع لمعنى ثم نُقل إلى غيره لعلاقة: فالمعاني اثنان",
        third_answer=RelationAnswer.NO,
        third_evidence="وُضع لمعنى ثم نُقل إلى غيره، فلم يُوضَع لكلٍّ منهما ابتداءً",
        fourth_answer=RelationAnswer.NO,
        fourth_evidence="ولكنه لم يشتهر في المعنى الثاني",
        fifth_answer=IntendedMeaning.SECOND,
        fifth_evidence="وإن أُطلق على المعنى المنقول إليه فهو المجاز",
        initial_assignment_carrier=InitialAssignmentCarrier.FOR_ONE_MEANING,
        transfer_fame_carrier=TransferFameCarrier.NOT_FAMOUS,
        usage_intent_carrier=UsageIntentCarrier.TRANSFERRED_MEANING,
        majaz_relation=(
            "مشابهة الرجل الشجاع للأسد في الشجاعة، وهي علاقة معتبَرة عند العرب"
        ),
        attested_relation=LafzMadlulRelation.MAJAZ,
        source=_SHAKHSIYYA,
    ),
)

if len({cluster.cluster_key for cluster in ATTESTED_CLUSTERS}) != len(
    ATTESTED_CLUSTERS
):  # pragma: no cover - guard
    raise RuntimeError("two attested clusters carry the same identity")
if {cluster.attested_relation for cluster in ATTESTED_CLUSTERS} != set(
    LafzMadlulRelation
):  # pragma: no cover - guard
    raise RuntimeError("the attested corpus does not cover every declared relation")


@dataclass(frozen=True, slots=True)
class RelationProofRow:
    """صفّ برهانٍ واحد: عنقودٌ بإجاباته، وتصنيفه المشتقّ مقابل المنصوص."""

    lexemes: tuple[str, ...]
    tested_usage: str
    first_answer: RelationCount
    second_answer: RelationCount
    third_answer: RelationAnswer
    fourth_answer: RelationAnswer
    fifth_answer: IntendedMeaning
    derived_relation: LafzMadlulRelation
    attested_relation: LafzMadlulRelation

    @property
    def matches(self) -> bool:
        return self.derived_relation is self.attested_relation


@dataclass(frozen=True, slots=True)
class RelationProofReport:
    """تقرير البرهان الشامل: صفٌّ لكل عنقود، بلا توقّف عند أول فشل."""

    rows: tuple[RelationProofRow, ...]
    domain: FrozenRelationDomain
    source: str

    @property
    def is_complete_success(self) -> bool:
        """هل صُنِّف كل عنقود بلا استثناء واحد ولا حالة غموض؟"""

        return bool(self.rows) and all(row.matches for row in self.rows)

    @property
    def unmatched(self) -> tuple[RelationProofRow, ...]:
        """الصفوف التي خالف فيها المشتقّ المنصوص؛ تُبلَّغ ولا تُرمَّم."""

        return tuple(row for row in self.rows if not row.matches)

    @property
    def title(self) -> str | None:
        """التسمية الدقيقة عند النجاح التامّ وحده، و`None` عند غيره."""

        return RELATION_SUCCESS_TITLE if self.is_complete_success else None


def prove_relations_over_attested_corpus(
    clusters: tuple[AttestedLexemeCluster, ...] = ATTESTED_CLUSTERS,
) -> RelationProofReport:
    """برهِن على كل عنقود من الشواهد بالدالة الصورية وحدها، تغطيةً شاملة.

    لا يُقرأ `attested_relation` إلا للمقارنة بعد الاشتقاق، ولا يُستعمل في
    الاشتقاق نفسه. وعند عدم التطابق يُسجَّل الصفّ في `unmatched` كما هو: لا
    تُعدَّل الدالة الصورية ولا الشواهد لإخفاء الفشل.
    """

    if not clusters:
        raise LafzMadlulRelationError("البرهان الشامل لا يكون على مجموعة فارغة")
    rows = []
    for cluster in clusters:
        if not isinstance(cluster, AttestedLexemeCluster):
            raise LafzMadlulRelationError("البرهان يجري على شواهد مُثبَتة فقط")
        rows.append(
            RelationProofRow(
                lexemes=cluster.lexemes,
                tested_usage=cluster.tested_usage,
                first_answer=cluster.first_answer,
                second_answer=cluster.second_answer,
                third_answer=cluster.third_answer,
                fourth_answer=cluster.fourth_answer,
                fifth_answer=cluster.fifth_answer,
                derived_relation=cluster.derived_relation,
                attested_relation=cluster.attested_relation,
            )
        )
    return RelationProofReport(
        rows=tuple(rows), domain=FROZEN_RELATION_DOMAIN, source=RELATION_SOURCE
    )
