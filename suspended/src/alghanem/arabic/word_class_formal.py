"""برهان صوري شامل على نطاق محدود: تقسيم اللفظ المفرد إلى اسم وفعل وحرف.

المصدر النصّي — يُذكَر بالاسم لا إحالةً مبهمة — كتاب "الشخصية الإسلامية" الجزء
الثالث، في تقسيم اللفظ المفرد:

    "اللفظ المفرد إما أن لا يستقلّ بمعناه [فهو الحرف]. وإما أن يستقلّ
    بمعناه... فإن دلّ بهيئته على أحد الأزمنة الثلاثة [فهو الفعل]، وإن لم
    يدلّ بهيئته على أحد الأزمنة [فهو الاسم]."

هذه الوحدة تبني — على معيار `NoBirthWithoutResidualOrFormalNecessity` في وضعه
الصوري (`FORMAL`) وصفًا لا تفعيلًا — مجالًا صوريًّا مجمَّدًا سؤالاه ثنائيّان،
ودالةَ قرارٍ كلّيةً عليه، ثم برهانًا شاملًا على أربعة ألفاظ مُثبَتة بأعيانها في
المصدر نفسه.

بنية المجال — `card(Ω) = 3` بالضبط، لا أربع:

* س١ = "هل يستقلّ اللفظ بمعناه بلا حاجة للفظ آخر؟"
* س٢ = "هل يدلّ اللفظ بهيئته الصرفية (لا بذاته) على أحد الأزمنة الثلاثة؟"،
  ولا تُطرَح إلا إذا كانت إجابة س١ = نعم.

فالحالات المقبولة ثلاث لا غير: `(لا، غير_مطروح)`، و`(نعم، نعم)`،
و`(نعم، لا)`. وقيمة `غير_مطروح` قيمةٌ مصرَّح بها في المفردة، لا `None` صامتة
ولا غياب حقل: التصريح بأن السؤال لم يُطرَح أصلًا جزءٌ من البنية، وبه تُغلَق
الحالة الرابعة (`لا` مع س٢ مطروحة) بنيويًّا بدل أن تتسلّل بصمت.

والفارق الدقيق الذي يمنع خلط "أمس" بالفعل مبنيٌّ في البيانات نفسها لا مشروحٌ
في تعليق: لكل شاهد حقلٌ مغلق هو **حامل الدلالة الزمنية**
(`بالهيئة` / `بالذات` / `لا_دلالة_زمنية`)، ومنه تُشتَقّ إجابة س٢ اشتقاقًا،
ويُرفَض أي شاهد كُتبت فيه إجابة س٢ مخالفةً لحامله. فـ"أمس" يدلّ على الزمن
`بالذات` لا `بالهيئة`، فإجابته عن س٢ = لا، فهو اسم رغم دلالته الزمنية — كما
صُرِّح به نصًّا: "يدلّ عليه لكن لا بهيئته بل بذاته".

نطاق الوحدة وحدودها — تسجيل صريح، لا اعتذار لاحق:

* النطاق أربعة ألفاظ مُثبَتة من نصّ واحد بعينه، وثلاثة تصنيفات لا رابع لها
  هنا. ولا تتناول هذه الوحدة المصدر ولا المضارع ولا اللازم والمتعدي: تلك تحتاج
  مصدرًا صرفيًّا لم يُوفَّر بعد، وإدخالها الآن ادّعاءُ نطاقٍ غير مبرهَن.
* سلطويًّا: `FormalClassification != BirthVerdict`، و
  `DeclaredWordClass != BornOntology`. هذا توثيق وتصنيف صوري فقط: لا نوع في
  `kernel/`، ولا `Freeze`، ولا `E0`، ولا بوّابة نواة تقرأ هذه المخرجات. لا
  تدخل نتيجة هذه الوحدة في `BirthExperimentSpecification`، ولا يقرأها
  `IndependentClosureGate` ولا `BirthVerdictGate`، ولا تغيّر نتيجة التدقيق
  الخارجي.
* عند نجاح البرهان الشامل تُستعمل التسمية الدقيقة وحدها:
  "أول شهادة صورية شاملة ناجحة على نطاق محدود" — لا "ولادة"، فتلك تسمية لاحقة
  تحتاج `Freeze` و`E0` لم يُبنَيا بعد.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

from .text_key import comparison_key


class WordClassFormalError(ValueError):
    """رُفض مدخلٌ خارج المجال الصوري المجمَّد؛ لا يُحمَل على أقرب حالة."""


class FormalAnswer(Enum):
    """مفردة الإجابات المغلقة؛ `غير_مطروح` تصريحٌ لا صمت."""

    YES = "نعم"
    NO = "لا"
    NOT_ASKED = "غير_مطروح"


class WordClass(Enum):
    """التصنيفات الثلاثة المغلقة؛ لا رابع لها في هذا النطاق."""

    HARF = "حرف"
    FIL = "فعل"
    ISM = "اسم"


class TemporalSignifierCarrier(Enum):
    """حامل الدلالة الزمنية؛ منه تُشتَقّ إجابة س٢ ولا تُكتَب اعتباطًا."""

    BY_FORM = "بالهيئة"
    BY_ESSENCE = "بالذات"
    NONE = "لا_دلالة_زمنية"


SOURCE: Final = "الشخصية الإسلامية، الجزء الثالث، في تقسيم اللفظ المفرد"

FIRST_QUESTION: Final = "هل يستقلّ اللفظ بمعناه بلا حاجة للفظ آخر؟"

SECOND_QUESTION: Final = (
    "هل يدلّ اللفظ بهيئته الصرفية (لا بذاته) على أحد الأزمنة الثلاثة؟"
)

SECOND_QUESTION_CONDITION: Final = "لا تُطرَح س٢ إلا إذا كانت إجابة س١ = نعم"

SUCCESS_TITLE: Final = "أول شهادة صورية شاملة ناجحة على نطاق محدود"

SCOPE_NOTE: Final = (
    "نطاق هذا البرهان أربعة ألفاظ مُثبَتة من مصدر واحد بعينه وثلاثة تصنيفات "
    "مغلقة؛ فالمصدر والمضارع واللازم والمتعدي خارجه بالتصريح لا بالسهو، "
    "لافتقارها إلى مصدر صرفي لم يُوفَّر بعد"
)

AUTHORITY_NOTE: Final = (
    "تصنيف صوري وتوثيق فقط: لا يُنتج ولادةً ولا حكم ولادة، ولا يُجمَّد، ولا "
    "تقرأه أيّ بوّابة في النواة"
)

ADMISSIBLE_STATES: Final = (
    (FormalAnswer.NO, FormalAnswer.NOT_ASKED),
    (FormalAnswer.YES, FormalAnswer.YES),
    (FormalAnswer.YES, FormalAnswer.NO),
)

_DECISION: Final = {
    (FormalAnswer.NO, FormalAnswer.NOT_ASKED): WordClass.HARF,
    (FormalAnswer.YES, FormalAnswer.YES): WordClass.FIL,
    (FormalAnswer.YES, FormalAnswer.NO): WordClass.ISM,
}

_SECOND_ANSWER_BY_CARRIER: Final = {
    TemporalSignifierCarrier.BY_FORM: FormalAnswer.YES,
    TemporalSignifierCarrier.BY_ESSENCE: FormalAnswer.NO,
    TemporalSignifierCarrier.NONE: FormalAnswer.NO,
}

if set(_DECISION) != set(ADMISSIBLE_STATES):  # pragma: no cover - guard
    raise RuntimeError("the decision function does not cover the admissible domain")
if len(_SECOND_ANSWER_BY_CARRIER) != len(TemporalSignifierCarrier):  # pragma: no cover
    raise RuntimeError("a temporal-signifier carrier derives no second answer")


def _require_answer(answer: FormalAnswer, field_name: str) -> FormalAnswer:
    if not isinstance(answer, FormalAnswer):
        raise WordClassFormalError(f"{field_name} must come from the closed vocabulary")
    return answer


@dataclass(frozen=True, slots=True)
class FrozenFormalDomain:
    """المجال الصوري المجمَّد: سؤالاه، وشرط الثاني، وحالاته المقبولة، ومصدره."""

    source: str = SOURCE
    first_question: str = FIRST_QUESTION
    second_question: str = SECOND_QUESTION
    second_question_condition: str = SECOND_QUESTION_CONDITION
    admissible_states: tuple[tuple[FormalAnswer, FormalAnswer], ...] = ADMISSIBLE_STATES

    def __post_init__(self) -> None:
        for name in ("source", "first_question", "second_question"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise WordClassFormalError(f"{name} must be non-blank text")
        if set(self.admissible_states) != set(ADMISSIBLE_STATES):
            raise WordClassFormalError(
                "the frozen formal domain is exactly the three admissible states"
            )

    @property
    def cardinality(self) -> int:
        """عدد الحالات المقبولة في المجال: ثلاث بالضبط."""

        return len(self.admissible_states)


FROZEN_FORMAL_DOMAIN: Final = FrozenFormalDomain()


def canonical_answer(value: str) -> FormalAnswer:
    """أعِد الإجابة المسمّاة في `value`؛ وأيّ لفظ آخر يُرَدّ ولا يُقرَّب."""

    if not isinstance(value, str) or not value.strip():
        raise WordClassFormalError("الإجابة must be non-blank text")
    key = comparison_key(value)
    for answer in FormalAnswer:
        if comparison_key(answer.value) == key:
            return answer
    raise WordClassFormalError(
        "الإجابة must be one of: " + "، ".join(answer.value for answer in FormalAnswer)
    )


def is_second_question_asked(first: FormalAnswer) -> bool:
    """هل تُطرَح س٢ أصلًا؟ تُطرَح إن وإن فقط كانت إجابة س١ = نعم."""

    return _require_answer(first, "س١") is FormalAnswer.YES


def classify(first: FormalAnswer, second: FormalAnswer) -> WordClass:
    """التصنيف المشتقّ من الإجابتين اشتقاقًا مباشرًا، بلا تخمين ولا فرع افتراضي.

    س١=لا (وس٢ غير مطروحة) → حرف. وس١=نعم وس٢=نعم → فعل. وس١=نعم وس٢=لا →
    اسم. وأيّ حالة خارج هذه الثلاث — ومنها `لا` مع س٢ مطروحة — تُرَدّ بخطأ ولا
    تُصنَّف.
    """

    state = (_require_answer(first, "س١"), _require_answer(second, "س٢"))
    if state[0] is FormalAnswer.NOT_ASKED:
        raise WordClassFormalError("س١ تُطرَح دائمًا، فلا تكون غير_مطروح")
    if is_second_question_asked(state[0]) != (state[1] is not FormalAnswer.NOT_ASKED):
        raise WordClassFormalError(SECOND_QUESTION_CONDITION)
    word_class = _DECISION.get(state)
    if word_class is None:  # pragma: no cover - guard
        raise WordClassFormalError("حالة خارج المجال الصوري المجمَّد")
    return word_class


@dataclass(frozen=True, slots=True)
class AttestedLexeme:
    """لفظ مُثبَت نصًّا بإجابتيه الصريحتين ودليل كلٍّ منهما وتصنيفه المنصوص."""

    lexeme: str
    first_answer: FormalAnswer
    first_evidence: str
    second_answer: FormalAnswer
    second_evidence: str
    temporal_carrier: TemporalSignifierCarrier
    attested_class: WordClass
    source: str

    def __post_init__(self) -> None:
        for name in ("lexeme", "first_evidence", "second_evidence", "source"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise WordClassFormalError(f"{name} must be non-blank text")
        _require_answer(self.first_answer, "س١")
        _require_answer(self.second_answer, "س٢")
        if not isinstance(self.temporal_carrier, TemporalSignifierCarrier):
            raise WordClassFormalError(
                "حامل الدلالة الزمنية must come from the closed vocabulary"
            )
        if not isinstance(self.attested_class, WordClass):
            raise WordClassFormalError(
                "التصنيف المنصوص must come from the closed vocabulary"
            )
        if self.first_answer is FormalAnswer.NOT_ASKED:
            raise WordClassFormalError("س١ تُطرَح دائمًا، فلا تكون غير_مطروح")
        if not is_second_question_asked(self.first_answer):
            if self.second_answer is not FormalAnswer.NOT_ASKED:
                raise WordClassFormalError(SECOND_QUESTION_CONDITION)
            if self.temporal_carrier is TemporalSignifierCarrier.BY_FORM:
                raise WordClassFormalError("لفظٌ لا يستقلّ بمعناه لا يدلّ بهيئته على زمن")
            return
        if self.second_answer is not _SECOND_ANSWER_BY_CARRIER[self.temporal_carrier]:
            raise WordClassFormalError(
                "إجابة س٢ تُشتَقّ من حامل الدلالة الزمنية ولا تُكتَب اعتباطًا"
            )

    @property
    def derived_class(self) -> WordClass:
        """التصنيف المشتقّ من الدالة الصورية وحدها، لا من التصنيف المنصوص."""

        return classify(self.first_answer, self.second_answer)


_SHAKHSIYYA: Final = SOURCE

ATTESTED_LEXEMES: Final = (
    AttestedLexeme(
        lexeme="مِن",
        first_answer=FormalAnswer.NO,
        first_evidence=(
            "لا يُفهَم معناه الذي وضع له إلا باعتبار لفظ آخر... كقولك قبضت من " "الدراهم"
        ),
        second_answer=FormalAnswer.NOT_ASKED,
        second_evidence=(
            "لم تُطرَح س٢ لأن اللفظ لم يستقلّ بمعناه، فانقطع السؤال عن دلالة "
            "الهيئة على الزمن"
        ),
        temporal_carrier=TemporalSignifierCarrier.NONE,
        attested_class=WordClass.HARF,
        source=_SHAKHSIYYA,
    ),
    AttestedLexeme(
        lexeme="قام",
        first_answer=FormalAnswer.YES,
        first_evidence="يستقلّ بمعناه، فيُفهَم منه الحدث بلا حاجة إلى لفظ آخر",
        second_answer=FormalAnswer.YES,
        second_evidence="دلّ بهيئته الصرفية على الزمن الماضي",
        temporal_carrier=TemporalSignifierCarrier.BY_FORM,
        attested_class=WordClass.FIL,
        source=_SHAKHSIYYA,
    ),
    AttestedLexeme(
        lexeme="زيد",
        first_answer=FormalAnswer.YES,
        first_evidence="يستقلّ بمعناه، فيُفهَم منه المسمّى بلا حاجة إلى لفظ آخر",
        second_answer=FormalAnswer.NO,
        second_evidence="لا يدلّ على أحد الأزمنة الثلاثة أصلًا، لا بهيئته ولا بذاته",
        temporal_carrier=TemporalSignifierCarrier.NONE,
        attested_class=WordClass.ISM,
        source=_SHAKHSIYYA,
    ),
    AttestedLexeme(
        lexeme="أمس",
        first_answer=FormalAnswer.YES,
        first_evidence="يستقلّ بمعناه، فيُفهَم منه اليوم الماضي بلا حاجة إلى لفظ آخر",
        second_answer=FormalAnswer.NO,
        second_evidence="يدلّ عليه لكن لا بهيئته بل بذاته",
        temporal_carrier=TemporalSignifierCarrier.BY_ESSENCE,
        attested_class=WordClass.ISM,
        source=_SHAKHSIYYA,
    ),
)

if len({lexeme.lexeme for lexeme in ATTESTED_LEXEMES}) != len(
    ATTESTED_LEXEMES
):  # pragma: no cover - guard
    raise RuntimeError("two attested lexemes carry the same surface")


@dataclass(frozen=True, slots=True)
class FormalProofRow:
    """صفّ برهانٍ واحد: لفظٌ بإجابتيه، وتصنيفه المشتقّ مقابل المنصوص."""

    lexeme: str
    first_answer: FormalAnswer
    second_answer: FormalAnswer
    derived_class: WordClass
    attested_class: WordClass

    @property
    def matches(self) -> bool:
        return self.derived_class is self.attested_class


@dataclass(frozen=True, slots=True)
class FormalProofReport:
    """تقرير البرهان الشامل: صفٌّ لكل لفظ، بلا توقّف عند أول فشل."""

    rows: tuple[FormalProofRow, ...]
    domain: FrozenFormalDomain
    source: str

    @property
    def is_complete_success(self) -> bool:
        """هل صُنِّف كل لفظ بلا استثناء واحد ولا حالة غموض؟"""

        return bool(self.rows) and all(row.matches for row in self.rows)

    @property
    def unmatched(self) -> tuple[FormalProofRow, ...]:
        """الصفوف التي خالف فيها المشتقّ المنصوص؛ تُبلَّغ ولا تُرمَّم."""

        return tuple(row for row in self.rows if not row.matches)

    @property
    def title(self) -> str | None:
        """التسمية الدقيقة عند النجاح التامّ وحده، و`None` عند غيره."""

        return SUCCESS_TITLE if self.is_complete_success else None


def prove_over_attested_corpus(
    lexemes: tuple[AttestedLexeme, ...] = ATTESTED_LEXEMES,
) -> FormalProofReport:
    """برهِن على كل لفظ من الشواهد بالدالة الصورية وحدها، تغطيةً شاملة.

    لا يُقرأ `attested_class` إلا للمقارنة بعد الاشتقاق، ولا يُستعمل في
    الاشتقاق نفسه. وعند عدم التطابق يُسجَّل الصفّ في `unmatched` كما هو: لا
    تُعدَّل الدالة الصورية ولا الإجابات لإخفاء الفشل.
    """

    if not lexemes:
        raise WordClassFormalError("البرهان الشامل لا يكون على مجموعة فارغة")
    rows = []
    for lexeme in lexemes:
        if not isinstance(lexeme, AttestedLexeme):
            raise WordClassFormalError("البرهان يجري على شواهد مُثبَتة فقط")
        rows.append(
            FormalProofRow(
                lexeme=lexeme.lexeme,
                first_answer=lexeme.first_answer,
                second_answer=lexeme.second_answer,
                derived_class=lexeme.derived_class,
                attested_class=lexeme.attested_class,
            )
        )
    return FormalProofReport(
        rows=tuple(rows), domain=FROZEN_FORMAL_DOMAIN, source=SOURCE
    )
