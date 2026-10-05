"""برهان صوري شامل على نطاق محدود: تصنيف المدلول وحده خمسةَ أقسام.

المصدر النصّي — يُذكَر بالاسم لا إحالةً مبهمة — كتاب "الشخصية الإسلامية" الجزء
الثالث، في تقسيم المدلول:

    "أن يكون المدلول معنى، أي شيئًا ليس بلفظ، كالحيوان وكزيد علمًا على رجل."
    "أن يكون المدلول لفظًا مفردًا مستعملًا، مثل لفظ الكلمة، فإن مدلولها لفظ
    وضع لمعنى مفرد، وهو الاسم والفعل والحرف."
    "أن يكون المدلول لفظًا مفردًا مهملًا، كأسماء حروف الهجاء... فللأول الضاد."
    "أن يكون المدلول لفظًا مركّبًا مستعملًا، نحو الخبر، فإن مدلوله لفظ مركّب
    موضوع، مثل زيد قائم."
    "أن يكون المدلول لفظًا مركّبًا مهملًا، وهو الهذيان."

هذه الوحدة تبني — بنفس نمط `word_class_formal.py` و`lafz_madlul_relation_formal.py`،
وعلى معيار `NoBirthWithoutResidualOrFormalNecessity` في وضعه الصوري (`FORMAL`)
وصفًا لا تفعيلًا — مجالًا صوريًّا مجمَّدًا، ودالةَ قرارٍ كلّيةً عليه، ثم برهانًا
شاملًا على خمسة شواهد مُثبَتة بأعيانها في المصدر نفسه، واحدٍ لكل فرع بالضبط.

الفارق البنيوي عن الشهادتين السابقتين — تصريحٌ لا تفصيل لاحق: الوحدة المُصنَّفة
هنا **لفظ واحد يُختبَر مدلوله هو**، لا عنقودُ علاقةٍ بين لفظ ومعنى آخر كالوحدة
السابقة. فالسؤال هنا عن جنس المدلول نفسه — أمعنى هو أم لفظ، وإن كان لفظًا فما
تركيبه وما حالُ وضعه — لا عن نسبة اللفظ إلى معناه ولا عن تعدّد الطرفين. فلفظ
"الكلمة" يُصنَّف بمدلوله وحده، بصرف النظر عن كونه مشتركًا أو منفردًا في العلاقة.

بنية المجال — `card(Ω) = 5` بالضبط، لا أكثر ولا أقل، وثلاثة أسئلة ثنائية فقط:

* س١ = "نوع مدلول اللفظ؟" (معنى / لفظ)، تُطرَح دائمًا.
* س٢ = "تركيب اللفظ المدلول؟" (مفرد / مركّب)، ولا تُطرَح إلا إذا كانت س١ = لفظ.
* س٣ = "حالة وضعه؟" (مستعمَل / مهمَل)، ولا تُطرَح إلا إذا كانت س١ = لفظ.

فالحالات المقبولة خمس لا غير، وقيمة `غير_مطروح` قيمةٌ مصرَّح بها في المفردات
المغلقة، لا `None` صامتة ولا غياب حقل: التصريح بأن السؤال لم يُطرَح أصلًا جزءٌ من
البنية، وبه تُغلَق كل حالة خارج الخمس بنيويًّا بدل أن تتسلّل بصمت.

ولا تُكتَب إجابةٌ اعتباطًا: كلٌّ منها تُشتَقّ من حقل بيانات مُدخَل، بنفس انضباط
"حامل الدلالة الزمنية" في الشهادة الأولى وحوامل العلاقة في الثانية. فس١ تُشتَقّ من
**حامل جنس المدلول**، وس٢ من **حامل تركيب اللفظ المدلول**، وس٣ من **حامل حال
الوضع**؛ ويُرفَض أي شاهد كُتبت فيه إجابةٌ مخالفةً لحاملها.

ملاحظة نطاقٍ خاصّة بالفرع الخامس — تُسجَّل صراحةً ولا تُخفى: القسم الخامس
(الهذيان) حالةٌ شاذّة موثَّقة في المصدر نفسه، إذ يقول: "هذا القسم غير موضوع، أي
لم تضعه العرب؛ لأن الغرض من التركيب الإفادة، وهذا لا يفيد؛ ولكنه موجود." فهذا
الفرع صحيحٌ بنيويًّا ويجب أن يُصنَّف كسائر الفروع، لكنه **يقع خارج نطاق الوضع
اللغوي** بخلاف الأربعة الأخرى. وهذه الملاحظة مسجَّلة بنيويًّا — على غرار ملاحظة
"العلاقة" التوثيقية في فرع المجاز من الشهادة الثانية — بحقلٍ مُلزَم على فرع
الهذيان وحده، ومرفوضٍ على ما عداه، لا بتعليقٍ يُنسى.

نطاق الوحدة وحدودها — تسجيل صريح، لا اعتذار لاحق:

* النطاق خمسة شواهد مُثبَتة من نصّ واحد بعينه، وخمسة أقسام لا سادس لها هنا.
  ولا تتناول هذه الوحدة تقسيم اللفظ المدلول نفسه إلى اسم وفعل وحرف، ولا أقسام
  المركّب (إسنادي وغير إسنادي)، ولا مراتب الإهمال: تلك تحتاج شواهد لكل قيمة ليكون
  المجال مكتمل الفروع بالبناء، ولا نملكها هنا، وإدخالها الآن ادّعاءُ نطاقٍ غير
  مبرهَن.
* سلطويًّا: `FormalClassification != BirthVerdict`، و
  `DeclaredSignifiedKind != BornOntology`. هذا توثيق وتصنيف صوري فقط: لا نوع في
  `kernel/`، ولا `Freeze`، ولا `E0`، ولا بوّابة نواة تقرأ هذه المخرجات. لا تدخل
  نتيجة هذه الوحدة في `BirthExperimentSpecification`، ولا يقرأها
  `IndependentClosureGate` ولا `BirthVerdictGate`، ولا تغيّر نتيجة التدقيق
  الخارجي، ويبقى كل حقل فيه مطابقًا بايتيًّا.
* عند نجاح البرهان الشامل تُستعمل التسمية الدقيقة وحدها: "شهادة صورية شاملة
  ناجحة على نطاق محدود" — لا "ولادة"، فتلك تسمية لاحقة تحتاج `Freeze` و`E0` لم
  يُبنَيا بعد.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

from .text_key import comparison_key


class MadlulAloneError(ValueError):
    """رُفض مدخلٌ خارج المجال الصوري المجمَّد؛ لا يُحمَل على أقرب حالة."""


class SignifiedKind(Enum):
    """مفردة جنس المدلول المغلقة: معنى أو لفظ، لا ثالث لهما، وس١ تُطرَح دائمًا."""

    MEANING = "معنى"
    UTTERANCE = "لفظ"


class SignifiedComposition(Enum):
    """مفردة تركيب اللفظ المدلول؛ `غير_مطروح` تصريحٌ لا صمت."""

    SIMPLE = "مفرد"
    COMPOUND = "مركّب"
    NOT_ASKED = "غير_مطروح"


class SignifiedUsageState(Enum):
    """مفردة حال وضع اللفظ المدلول؛ `غير_مطروح` تصريحٌ لا صمت."""

    USED = "مستعمَل"
    NEGLECTED = "مهمَل"
    NOT_ASKED = "غير_مطروح"


class MadlulSection(Enum):
    """الأقسام الخمسة المغلقة بترتيب المصدر؛ لا سادس لها في هذا النطاق."""

    MEANING = "معنى"
    SIMPLE_USED_UTTERANCE = "لفظ_مفرد_مستعمَل"
    SIMPLE_NEGLECTED_UTTERANCE = "لفظ_مفرد_مهمَل"
    COMPOUND_USED_UTTERANCE = "لفظ_مركّب_مستعمَل"
    HADHAYAN = "هذيان"


class SignifiedNatureCarrier(Enum):
    """حامل جنس المدلول؛ منه تُشتَقّ إجابة س١ ولا تُكتَب اعتباطًا."""

    NOT_AN_UTTERANCE = "شيء_ليس_بلفظ"
    AN_UTTERANCE = "لفظ_مدلول"


class SignifiedStructureCarrier(Enum):
    """حامل تركيب اللفظ المدلول؛ منه تُشتَقّ إجابة س٢ ولا تُكتَب اعتباطًا."""

    SIMPLE_STRUCTURE = "تركيب_مفرد"
    COMPOUND_STRUCTURE = "تركيب_مركّب"
    NOT_APPLICABLE = "لا_ينطبق"


class SignifiedAssignmentCarrier(Enum):
    """حامل حال الوضع؛ منه تُشتَقّ إجابة س٣ ولا تُكتَب اعتباطًا."""

    ASSIGNED_AND_USED = "موضوع_مستعمَل"
    UNASSIGNED_AND_NEGLECTED = "غير_موضوع_مهمَل"
    NOT_APPLICABLE = "لا_ينطبق"


MADLUL_SOURCE: Final = "الشخصية الإسلامية، الجزء الثالث، في تقسيم المدلول"

MADLUL_FIRST_QUESTION: Final = "نوع مدلول اللفظ؟"

MADLUL_SECOND_QUESTION: Final = "تركيب اللفظ المدلول؟"

MADLUL_THIRD_QUESTION: Final = "حالة وضعه؟"

MADLUL_SECOND_QUESTION_CONDITION: Final = "لا تُطرَح س٢ إلا إذا كانت س١ = لفظ"

MADLUL_THIRD_QUESTION_CONDITION: Final = "لا تُطرَح س٣ إلا إذا كانت س١ = لفظ"

MADLUL_SUCCESS_TITLE: Final = "شهادة صورية شاملة ناجحة على نطاق محدود"

MADLUL_SCOPE_NOTE: Final = (
    "نطاق هذا البرهان خمسة شواهد مُثبَتة من مصدر واحد بعينه وخمسة أقسام مغلقة؛ "
    "فتقسيم اللفظ المدلول إلى اسم وفعل وحرف، وأقسام المركّب، ومراتب الإهمال "
    "خارجه بالتصريح لا بالسهو، لافتقارها إلى شاهد لكل قيمة يجعل المجال مكتمل "
    "الفروع بالبناء"
)

MADLUL_AUTHORITY_NOTE: Final = (
    "تصنيف صوري وتوثيق فقط: لا يُنتج ولادةً ولا حكم ولادة، ولا يُجمَّد، ولا "
    "تقرأه أيّ بوّابة في النواة"
)

MADLUL_FIFTH_SECTION_SCOPE_NOTE: Final = (
    "القسم الخامس حالة شاذّة موثَّقة في المصدر نفسه: هذا القسم غير موضوع، أي لم "
    "تضعه العرب؛ لأن الغرض من التركيب الإفادة، وهذا لا يفيد؛ ولكنه موجود. فهو "
    "صحيح بنيويًّا ويجب أن يُصنَّف، لكنه يقع خارج نطاق الوضع اللغوي بخلاف "
    "الأقسام الأربعة الأخرى"
)

MADLUL_NOT_APPLICABLE_TEXT: Final = "لا_ينطبق"

MadlulState = tuple[SignifiedKind, SignifiedComposition, SignifiedUsageState]

MADLUL_ADMISSIBLE_STATES: Final[tuple[MadlulState, ...]] = (
    (
        SignifiedKind.MEANING,
        SignifiedComposition.NOT_ASKED,
        SignifiedUsageState.NOT_ASKED,
    ),
    (
        SignifiedKind.UTTERANCE,
        SignifiedComposition.SIMPLE,
        SignifiedUsageState.USED,
    ),
    (
        SignifiedKind.UTTERANCE,
        SignifiedComposition.SIMPLE,
        SignifiedUsageState.NEGLECTED,
    ),
    (
        SignifiedKind.UTTERANCE,
        SignifiedComposition.COMPOUND,
        SignifiedUsageState.USED,
    ),
    (
        SignifiedKind.UTTERANCE,
        SignifiedComposition.COMPOUND,
        SignifiedUsageState.NEGLECTED,
    ),
)

_DECISION: Final[dict[MadlulState, MadlulSection]] = {
    MADLUL_ADMISSIBLE_STATES[0]: MadlulSection.MEANING,
    MADLUL_ADMISSIBLE_STATES[1]: MadlulSection.SIMPLE_USED_UTTERANCE,
    MADLUL_ADMISSIBLE_STATES[2]: MadlulSection.SIMPLE_NEGLECTED_UTTERANCE,
    MADLUL_ADMISSIBLE_STATES[3]: MadlulSection.COMPOUND_USED_UTTERANCE,
    MADLUL_ADMISSIBLE_STATES[4]: MadlulSection.HADHAYAN,
}

_FIRST_ANSWER_BY_CARRIER: Final = {
    SignifiedNatureCarrier.NOT_AN_UTTERANCE: SignifiedKind.MEANING,
    SignifiedNatureCarrier.AN_UTTERANCE: SignifiedKind.UTTERANCE,
}

_SECOND_ANSWER_BY_CARRIER: Final = {
    SignifiedStructureCarrier.SIMPLE_STRUCTURE: SignifiedComposition.SIMPLE,
    SignifiedStructureCarrier.COMPOUND_STRUCTURE: SignifiedComposition.COMPOUND,
    SignifiedStructureCarrier.NOT_APPLICABLE: SignifiedComposition.NOT_ASKED,
}

_THIRD_ANSWER_BY_CARRIER: Final = {
    SignifiedAssignmentCarrier.ASSIGNED_AND_USED: SignifiedUsageState.USED,
    SignifiedAssignmentCarrier.UNASSIGNED_AND_NEGLECTED: SignifiedUsageState.NEGLECTED,
    SignifiedAssignmentCarrier.NOT_APPLICABLE: SignifiedUsageState.NOT_ASKED,
}

if len(MADLUL_ADMISSIBLE_STATES) != len(
    set(MADLUL_ADMISSIBLE_STATES)
):  # pragma: no cover - guard
    raise RuntimeError("the admissible states are not five distinct states")
if set(_DECISION) != set(MADLUL_ADMISSIBLE_STATES):  # pragma: no cover - guard
    raise RuntimeError("the decision function does not cover the admissible domain")
if set(_DECISION.values()) != set(MadlulSection):  # pragma: no cover - guard
    raise RuntimeError("a declared section has no admissible state")
if len(_FIRST_ANSWER_BY_CARRIER) != len(SignifiedNatureCarrier):  # pragma: no cover
    raise RuntimeError("a signified-nature carrier derives no first answer")
if len(_SECOND_ANSWER_BY_CARRIER) != len(SignifiedStructureCarrier):  # pragma: no cover
    raise RuntimeError("a signified-structure carrier derives no second answer")
if len(_THIRD_ANSWER_BY_CARRIER) != len(
    SignifiedAssignmentCarrier
):  # pragma: no cover - guard
    raise RuntimeError("a signified-assignment carrier derives no third answer")


def _require_kind(kind: SignifiedKind, field_name: str) -> SignifiedKind:
    if not isinstance(kind, SignifiedKind):
        raise MadlulAloneError(f"{field_name} must come from the closed vocabulary")
    return kind


def _require_composition(
    composition: SignifiedComposition, field_name: str
) -> SignifiedComposition:
    if not isinstance(composition, SignifiedComposition):
        raise MadlulAloneError(f"{field_name} must come from the closed vocabulary")
    return composition


def _require_usage_state(
    usage: SignifiedUsageState, field_name: str
) -> SignifiedUsageState:
    if not isinstance(usage, SignifiedUsageState):
        raise MadlulAloneError(f"{field_name} must come from the closed vocabulary")
    return usage


@dataclass(frozen=True, slots=True)
class FrozenMadlulDomain:
    """المجال الصوري المجمَّد: أسئلته الثلاثة، وشرطاها، وحالاته الخمس، ومصدره."""

    source: str = MADLUL_SOURCE
    first_question: str = MADLUL_FIRST_QUESTION
    second_question: str = MADLUL_SECOND_QUESTION
    third_question: str = MADLUL_THIRD_QUESTION
    second_question_condition: str = MADLUL_SECOND_QUESTION_CONDITION
    third_question_condition: str = MADLUL_THIRD_QUESTION_CONDITION
    admissible_states: tuple[MadlulState, ...] = MADLUL_ADMISSIBLE_STATES

    def __post_init__(self) -> None:
        for name in (
            "source",
            "first_question",
            "second_question",
            "third_question",
            "second_question_condition",
            "third_question_condition",
        ):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise MadlulAloneError(f"{name} must be non-blank text")
        if set(self.admissible_states) != set(MADLUL_ADMISSIBLE_STATES):
            raise MadlulAloneError(
                "the frozen formal domain is exactly the five admissible states"
            )

    @property
    def cardinality(self) -> int:
        """عدد الحالات المقبولة في المجال: خمس بالضبط."""

        return len(self.admissible_states)


FROZEN_MADLUL_DOMAIN: Final = FrozenMadlulDomain()


def canonical_signified_kind(value: str) -> SignifiedKind:
    """أعِد جنس المدلول المسمّى في `value`؛ وأيّ لفظ آخر يُرَدّ ولا يُقرَّب."""

    if not isinstance(value, str) or not value.strip():
        raise MadlulAloneError("جنس المدلول must be non-blank text")
    key = comparison_key(value)
    for kind in SignifiedKind:
        if comparison_key(kind.value) == key:
            return kind
    raise MadlulAloneError(
        "جنس المدلول must be one of: " + "، ".join(kind.value for kind in SignifiedKind)
    )


def canonical_signified_composition(value: str) -> SignifiedComposition:
    """أعِد التركيب المسمّى في `value`؛ وأيّ لفظ آخر يُرَدّ ولا يُقرَّب."""

    if not isinstance(value, str) or not value.strip():
        raise MadlulAloneError("التركيب must be non-blank text")
    key = comparison_key(value)
    for composition in SignifiedComposition:
        if comparison_key(composition.value) == key:
            return composition
    raise MadlulAloneError(
        "التركيب must be one of: "
        + "، ".join(composition.value for composition in SignifiedComposition)
    )


def canonical_signified_usage_state(value: str) -> SignifiedUsageState:
    """أعِد حال الوضع المسمّى في `value`؛ وأيّ لفظ آخر يُرَدّ ولا يُقرَّب."""

    if not isinstance(value, str) or not value.strip():
        raise MadlulAloneError("حالة الوضع must be non-blank text")
    key = comparison_key(value)
    for usage in SignifiedUsageState:
        if comparison_key(usage.value) == key:
            return usage
    raise MadlulAloneError(
        "حالة الوضع must be one of: "
        + "، ".join(usage.value for usage in SignifiedUsageState)
    )


def is_second_question_asked(kind: SignifiedKind) -> bool:
    """هل تُطرَح س٢ أصلًا؟ تُطرَح إن وإن فقط كان مدلول اللفظ لفظًا."""

    return _require_kind(kind, "س١") is SignifiedKind.UTTERANCE


def is_third_question_asked(kind: SignifiedKind) -> bool:
    """هل تُطرَح س٣ أصلًا؟ تُطرَح إن وإن فقط كان مدلول اللفظ لفظًا."""

    return _require_kind(kind, "س١") is SignifiedKind.UTTERANCE


def classify_madlul(
    kind: SignifiedKind,
    composition: SignifiedComposition,
    usage: SignifiedUsageState,
) -> MadlulSection:
    """التصنيف المشتقّ من الإجابات اشتقاقًا مباشرًا، بلا تخمين ولا فرع افتراضي.

    س١=معنى → القسم الأول. وس١=لفظ مع مفرد×مستعمَل → القسم الثاني، ومع
    مفرد×مهمَل → القسم الثالث، ومع مركّب×مستعمَل → القسم الرابع، ومع
    مركّب×مهمَل → القسم الخامس وهو الهذيان. وأيّ حالة خارج هذه الخمس — ومنها
    سؤالٌ أُجيب وهو غير مطروح، أو سؤالٌ مطروح تُرك `غير_مطروح` — تُرَدّ بخطأ ولا
    تُصنَّف.
    """

    state: MadlulState = (
        _require_kind(kind, "س١"),
        _require_composition(composition, "س٢"),
        _require_usage_state(usage, "س٣"),
    )
    second_asked = state[1] is not SignifiedComposition.NOT_ASKED
    if is_second_question_asked(state[0]) != second_asked:
        raise MadlulAloneError(MADLUL_SECOND_QUESTION_CONDITION)
    third_asked = state[2] is not SignifiedUsageState.NOT_ASKED
    if is_third_question_asked(state[0]) != third_asked:
        raise MadlulAloneError(MADLUL_THIRD_QUESTION_CONDITION)
    section = _DECISION.get(state)
    if section is None:  # pragma: no cover - guard
        raise MadlulAloneError("حالة خارج المجال الصوري المجمَّد")
    return section


@dataclass(frozen=True, slots=True)
class AttestedSignifiedWitness:
    """لفظٌ مُثبَت نصًّا يُختبَر مدلوله: حوامله وأدلّته وقسمه المنصوص."""

    lexeme: str
    signified_description: str
    first_answer: SignifiedKind
    first_evidence: str
    second_answer: SignifiedComposition
    second_evidence: str
    third_answer: SignifiedUsageState
    third_evidence: str
    signified_nature_carrier: SignifiedNatureCarrier
    signified_structure_carrier: SignifiedStructureCarrier
    signified_assignment_carrier: SignifiedAssignmentCarrier
    outside_assignment_note: str
    attested_section: MadlulSection
    source: str

    def __post_init__(self) -> None:
        for name in (
            "lexeme",
            "signified_description",
            "first_evidence",
            "second_evidence",
            "third_evidence",
            "outside_assignment_note",
            "source",
        ):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise MadlulAloneError(f"{name} must be non-blank text")
        _require_kind(self.first_answer, "س١")
        _require_composition(self.second_answer, "س٢")
        _require_usage_state(self.third_answer, "س٣")
        if not isinstance(self.signified_nature_carrier, SignifiedNatureCarrier):
            raise MadlulAloneError(
                "حامل جنس المدلول must come from the closed vocabulary"
            )
        if not isinstance(self.signified_structure_carrier, SignifiedStructureCarrier):
            raise MadlulAloneError(
                "حامل تركيب اللفظ المدلول must come from the closed vocabulary"
            )
        if not isinstance(
            self.signified_assignment_carrier, SignifiedAssignmentCarrier
        ):
            raise MadlulAloneError("حامل الوضع must come from the closed vocabulary")
        if not isinstance(self.attested_section, MadlulSection):
            raise MadlulAloneError("القسم المنصوص must come from the closed vocabulary")
        if (
            self.first_answer
            is not _FIRST_ANSWER_BY_CARRIER[self.signified_nature_carrier]
        ):
            raise MadlulAloneError("إجابة س١ تُشتَقّ من حامل جنس المدلول ولا تُكتَب اعتباطًا")
        if (
            self.second_answer
            is not _SECOND_ANSWER_BY_CARRIER[self.signified_structure_carrier]
        ):
            raise MadlulAloneError(
                "إجابة س٢ تُشتَقّ من حامل تركيب اللفظ المدلول ولا تُكتَب اعتباطًا"
            )
        if (
            self.third_answer
            is not _THIRD_ANSWER_BY_CARRIER[self.signified_assignment_carrier]
        ):
            raise MadlulAloneError("إجابة س٣ تُشتَقّ من حامل حال الوضع ولا تُكتَب اعتباطًا")
        section = self.derived_section
        is_hadhayan = section is MadlulSection.HADHAYAN
        declared_note_key = comparison_key(self.outside_assignment_note)
        not_applicable_key = comparison_key(MADLUL_NOT_APPLICABLE_TEXT)
        if is_hadhayan and declared_note_key == not_applicable_key:
            raise MadlulAloneError(
                "فرع الهذيان يلزمه تصريحٌ بخروجه عن نطاق الوضع اللغوي"
            )
        if not is_hadhayan and declared_note_key != not_applicable_key:
            raise MadlulAloneError(
                f"ملاحظة الخروج عن الوضع تُصرَّح على فرع الهذيان وحده، وعلى ما "
                f"عداه تكون {MADLUL_NOT_APPLICABLE_TEXT}"
            )

    @property
    def witness_key(self) -> tuple[str, str]:
        """هوية الشاهد: لفظه مع مدلوله المُختبَر، لا اللفظ المجرَّد وحده."""

        return (
            comparison_key(self.lexeme),
            comparison_key(self.signified_description),
        )

    @property
    def derived_section(self) -> MadlulSection:
        """القسم المشتقّ من الدالة الصورية وحدها، لا من القسم المنصوص."""

        return classify_madlul(
            self.first_answer,
            self.second_answer,
            self.third_answer,
        )


_SHAKHSIYYA: Final = MADLUL_SOURCE

ATTESTED_SIGNIFIED_WITNESSES: Final = (
    AttestedSignifiedWitness(
        lexeme="الحيوان",
        signified_description="الجسم النامي الحسّاس المتحرّك بالإرادة، وهو معنى لا لفظ",
        first_answer=SignifiedKind.MEANING,
        first_evidence=(
            "أن يكون المدلول معنى، أي شيئًا ليس بلفظ، كالحيوان وكزيد علمًا على رجل."
        ),
        second_answer=SignifiedComposition.NOT_ASKED,
        second_evidence=(
            "لم تُطرَح س٢ لأن المدلول معنى لا لفظ، فلا يُسأل عن تركيب لفظٍ مدلول"
        ),
        third_answer=SignifiedUsageState.NOT_ASKED,
        third_evidence=(
            "لم تُطرَح س٣ لأن المدلول معنى لا لفظ، فلا يُسأل عن حال وضع لفظٍ مدلول"
        ),
        signified_nature_carrier=SignifiedNatureCarrier.NOT_AN_UTTERANCE,
        signified_structure_carrier=SignifiedStructureCarrier.NOT_APPLICABLE,
        signified_assignment_carrier=SignifiedAssignmentCarrier.NOT_APPLICABLE,
        outside_assignment_note=MADLUL_NOT_APPLICABLE_TEXT,
        attested_section=MadlulSection.MEANING,
        source=_SHAKHSIYYA,
    ),
    AttestedSignifiedWitness(
        lexeme="الكلمة",
        signified_description="لفظ وضع لمعنى مفرد، وهو الاسم والفعل والحرف",
        first_answer=SignifiedKind.UTTERANCE,
        first_evidence=(
            "أن يكون المدلول لفظًا مفردًا مستعملًا، مثل لفظ الكلمة، فإن مدلولها "
            "لفظ وضع لمعنى مفرد، وهو الاسم والفعل والحرف."
        ),
        second_answer=SignifiedComposition.SIMPLE,
        second_evidence="أن يكون المدلول لفظًا مفردًا... فإن مدلولها لفظ وضع لمعنى مفرد",
        third_answer=SignifiedUsageState.USED,
        third_evidence="أن يكون المدلول لفظًا مفردًا مستعملًا... فإن مدلولها لفظ وضع",
        signified_nature_carrier=SignifiedNatureCarrier.AN_UTTERANCE,
        signified_structure_carrier=SignifiedStructureCarrier.SIMPLE_STRUCTURE,
        signified_assignment_carrier=SignifiedAssignmentCarrier.ASSIGNED_AND_USED,
        outside_assignment_note=MADLUL_NOT_APPLICABLE_TEXT,
        attested_section=MadlulSection.SIMPLE_USED_UTTERANCE,
        source=_SHAKHSIYYA,
    ),
    AttestedSignifiedWitness(
        lexeme="الضاد",
        signified_description="حرف الهجاء المسمّى بهذا الاسم، وهو لفظ مفرد مهمل",
        first_answer=SignifiedKind.UTTERANCE,
        first_evidence=(
            "أن يكون المدلول لفظًا مفردًا مهملًا، كأسماء حروف الهجاء... فللأول الضاد."
        ),
        second_answer=SignifiedComposition.SIMPLE,
        second_evidence="أن يكون المدلول لفظًا مفردًا... كأسماء حروف الهجاء",
        third_answer=SignifiedUsageState.NEGLECTED,
        third_evidence="أن يكون المدلول لفظًا مفردًا مهملًا... فللأول الضاد",
        signified_nature_carrier=SignifiedNatureCarrier.AN_UTTERANCE,
        signified_structure_carrier=SignifiedStructureCarrier.SIMPLE_STRUCTURE,
        signified_assignment_carrier=(
            SignifiedAssignmentCarrier.UNASSIGNED_AND_NEGLECTED
        ),
        outside_assignment_note=MADLUL_NOT_APPLICABLE_TEXT,
        attested_section=MadlulSection.SIMPLE_NEGLECTED_UTTERANCE,
        source=_SHAKHSIYYA,
    ),
    AttestedSignifiedWitness(
        lexeme="الخبر",
        signified_description="لفظ مركّب موضوع، مثل زيد قائم",
        first_answer=SignifiedKind.UTTERANCE,
        first_evidence=(
            "أن يكون المدلول لفظًا مركّبًا مستعملًا، نحو الخبر، فإن مدلوله لفظ "
            "مركّب موضوع، مثل زيد قائم."
        ),
        second_answer=SignifiedComposition.COMPOUND,
        second_evidence="أن يكون المدلول لفظًا مركّبًا... فإن مدلوله لفظ مركّب موضوع",
        third_answer=SignifiedUsageState.USED,
        third_evidence="أن يكون المدلول لفظًا مركّبًا مستعملًا... لفظ مركّب موضوع",
        signified_nature_carrier=SignifiedNatureCarrier.AN_UTTERANCE,
        signified_structure_carrier=SignifiedStructureCarrier.COMPOUND_STRUCTURE,
        signified_assignment_carrier=SignifiedAssignmentCarrier.ASSIGNED_AND_USED,
        outside_assignment_note=MADLUL_NOT_APPLICABLE_TEXT,
        attested_section=MadlulSection.COMPOUND_USED_UTTERANCE,
        source=_SHAKHSIYYA,
    ),
    AttestedSignifiedWitness(
        lexeme="الهذيان",
        signified_description="لفظ مركّب مهمل لم تضعه العرب",
        first_answer=SignifiedKind.UTTERANCE,
        first_evidence="أن يكون المدلول لفظًا مركّبًا مهملًا، وهو الهذيان.",
        second_answer=SignifiedComposition.COMPOUND,
        second_evidence="أن يكون المدلول لفظًا مركّبًا... وهو الهذيان",
        third_answer=SignifiedUsageState.NEGLECTED,
        third_evidence="أن يكون المدلول لفظًا مركّبًا مهملًا، وهو الهذيان",
        signified_nature_carrier=SignifiedNatureCarrier.AN_UTTERANCE,
        signified_structure_carrier=SignifiedStructureCarrier.COMPOUND_STRUCTURE,
        signified_assignment_carrier=(
            SignifiedAssignmentCarrier.UNASSIGNED_AND_NEGLECTED
        ),
        outside_assignment_note=MADLUL_FIFTH_SECTION_SCOPE_NOTE,
        attested_section=MadlulSection.HADHAYAN,
        source=_SHAKHSIYYA,
    ),
)

if len({witness.witness_key for witness in ATTESTED_SIGNIFIED_WITNESSES}) != len(
    ATTESTED_SIGNIFIED_WITNESSES
):  # pragma: no cover - guard
    raise RuntimeError("two attested witnesses carry the same identity")
if {witness.attested_section for witness in ATTESTED_SIGNIFIED_WITNESSES} != set(
    MadlulSection
):  # pragma: no cover - guard
    raise RuntimeError("the attested corpus does not cover every declared section")


@dataclass(frozen=True, slots=True)
class MadlulProofRow:
    """صفّ برهانٍ واحد: لفظٌ بإجاباته، وقسمه المشتقّ مقابل المنصوص."""

    lexeme: str
    signified_description: str
    first_answer: SignifiedKind
    second_answer: SignifiedComposition
    third_answer: SignifiedUsageState
    derived_section: MadlulSection
    attested_section: MadlulSection

    @property
    def matches(self) -> bool:
        return self.derived_section is self.attested_section


@dataclass(frozen=True, slots=True)
class MadlulProofReport:
    """تقرير البرهان الشامل: صفٌّ لكل شاهد، بلا توقّف عند أول فشل."""

    rows: tuple[MadlulProofRow, ...]
    domain: FrozenMadlulDomain
    source: str

    @property
    def is_complete_success(self) -> bool:
        """هل صُنِّف كل شاهد بلا استثناء واحد ولا حالة غموض؟"""

        return bool(self.rows) and all(row.matches for row in self.rows)

    @property
    def unmatched(self) -> tuple[MadlulProofRow, ...]:
        """الصفوف التي خالف فيها المشتقّ المنصوص؛ تُبلَّغ ولا تُرمَّم."""

        return tuple(row for row in self.rows if not row.matches)

    @property
    def title(self) -> str | None:
        """التسمية الدقيقة عند النجاح التامّ وحده، و`None` عند غيره."""

        return MADLUL_SUCCESS_TITLE if self.is_complete_success else None


def prove_madlul_over_attested_corpus(
    witnesses: tuple[AttestedSignifiedWitness, ...] = ATTESTED_SIGNIFIED_WITNESSES,
) -> MadlulProofReport:
    """برهِن على كل شاهد من الشواهد بالدالة الصورية وحدها، تغطيةً شاملة.

    لا يُقرأ `attested_section` إلا للمقارنة بعد الاشتقاق، ولا يُستعمل في
    الاشتقاق نفسه. وعند عدم التطابق يُسجَّل الصفّ في `unmatched` كما هو: لا
    تُعدَّل الدالة الصورية ولا الشواهد لإخفاء الفشل.
    """

    if not witnesses:
        raise MadlulAloneError("البرهان الشامل لا يكون على مجموعة فارغة")
    rows = []
    for witness in witnesses:
        if not isinstance(witness, AttestedSignifiedWitness):
            raise MadlulAloneError("البرهان يجري على شواهد مُثبَتة فقط")
        rows.append(
            MadlulProofRow(
                lexeme=witness.lexeme,
                signified_description=witness.signified_description,
                first_answer=witness.first_answer,
                second_answer=witness.second_answer,
                third_answer=witness.third_answer,
                derived_section=witness.derived_section,
                attested_section=witness.attested_section,
            )
        )
    return MadlulProofReport(
        rows=tuple(rows), domain=FROZEN_MADLUL_DOMAIN, source=MADLUL_SOURCE
    )
