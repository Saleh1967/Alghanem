"""قياسُ دعوى المفعولية على طبقةِ علاقاتٍ خارجية، بالمواصفة المُجمَّدة قبله.

هذا تشغيلُ `ud_objecthood_preregistration` لا تعديلٌ له: لا عتبةَ غُيِّرت، ولا
قاعدةَ أُضيفت، ولا عمودَ بُدِّل. وكلُّ قياسٍ هنا مربوطٌ ببصمةِ تلك المواصفة،
فمن حرّك فيها حرفًا بعد التجميد فشل عنده **إنشاءُ** القياس لا صدر عنه تحذير.

**والجواب: الدعوى ساقطة** (`ObjecthoodDecision.CLAIM_REFUTED`). على القسم
المحجوب `ar_padt-ud-test`: من ٤١٩ موضعًا حسمتها الدعوى أصابت ١٥٠ — **٣٥٫٨٪**؛
وعلى قسم التطوير `ar_padt-ud-dev` ثلاثون بالمئة من ٤٤٩. والعتبةُ المُعلَنة قبل
القراءة كانت ٦٠٪ للسقوط، فالسقوطُ بالعتبة لا بانطباعٍ عن الرقم. وهذه أوّلُ مرّةٍ
تُقاس فيها الدعوى الأصلية على وَسْم **وظيفة** لا على وَسْم **حالة**؛ وقد بقيت
غيرَ مقيسةٍ على الوظيفة منذ سُمّي `ACCUSATIVE_IS_NOT_OBJECTHOOD`.

**ولا يُنقَل هذا السقوطُ إلى قراءة الحالة**: ٩٧٫١٪ في `irab_case_readout` قراءةُ
علامةِ إعرابٍ، وهي قائمةٌ كما هي. والمُبطَلُ هنا الخطوةُ الثانيةُ وحدَها —
الانتقالُ من العلامة إلى الوظيفة.

**وأكثرُ الخطأ ليس خطأَ قراءةِ حركةٍ بل خطأُ مجتمعٍ**
(`FUNCTION_WORDS_ARE_IN_THE_POPULATION_AS_STATED`): ١٨٨ من ٢٦٩ خطأً في القسم
المحجوب كلماتٌ وظيفية — «إِلَى» و«أَنَّ» و«وَ» و«لَ» — آخرُها فتحةٌ وليست
أسماءً أصلًا. والدعوى كما نُطِق بها لا تستثنيها، فتُحسَب عليها؛ ومن استثناها
فقد بدّل الدعوى المقيسة لا قاسها.

**وثغرةٌ في المواصفة نفسِها تُسمّى ولا تُصحَّح صمتًا**
(`PREREGISTERED_VOCABULARY_COVERS_PREDICTED_POSITIONS_ONLY`): مفردةُ المنازل
الثلاث المُجمَّدة تغطّي المواضع التي تنبّأت بها الدعوى والمتعذّرَ منها، ولا
منزلةَ فيها للموضع المقروءِ الذي لم تتنبّأ به. فعُدَّ هذا الصنفُ في حقلٍ رابعٍ
باسمه ولم يُدسَّ في منزلةٍ من الثلاث، ويبقى نقصُ المفردة مُسجَّلًا على المواصفة.

وهذه الوحدة تسجيلٌ لا سلطة: لا ولادةَ فيها، ولا حكمَ ولادة، ولا تجميدَ `E0`،
ولا تستورد من `kernel/` شيئًا، ولا تقرؤها وحدةٌ فيه. وبايتاتُ المدوَّنة غيرُ
منسوخةٍ إلى الشجرة؛ والشاهدان مُودَعان في `ud_relation_layer_step0`.
"""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass, fields
from typing import Final, Literal

from .irab_corpus_witness import IrabCorpusWitness
from .ud_objecthood_preregistration import (
    OBJ_IS_UD_OBJECTHOOD_NOT_CLASSICAL_MAFUL_NOTE,
    OBJECTHOOD_PREREGISTRATION,
    VFORM_IS_AN_ANNOTATORS_VOCALIZATION_NOTE,
    ObjecthoodDecision,
    ObjecthoodPositionOutcome,
)
from .ud_relation_layer_step0 import (
    REGISTER_IS_NEWSWIRE_NOT_QURANIC_NOTE,
    UD_ARABIC_PADT_DEV_CENSUS,
    UD_ARABIC_PADT_TEST_CENSUS,
)

__all__ = [
    "ADJACENCY_IS_NOT_GOVERNMENT_NOTE",
    "DEVELOPMENT_SPLIT_OBJECTHOOD_MEASUREMENT",
    "FUNCTION_WORD_UPOS_TAGS",
    "FUNCTION_WORDS_ARE_IN_THE_POPULATION_AS_STATED_NOTE",
    "HELD_OUT_SPLIT_OBJECTHOOD_MEASUREMENT",
    "NORMALIZATION_FORM",
    "NO_RULE_DEVELOPMENT_HAPPENED_THIS_ROUND_NOTE",
    "OBJECTHOOD_MEASUREMENT_NAMED_RESIDUALS",
    "ObjecthoodMeasurement",
    "ObjecthoodMeasurementError",
    "PREREGISTERED_VOCABULARY_COVERS_PREDICTED_POSITIONS_ONLY_NOTE",
    "UNICODE_DATABASE_VERSION",
    "classify_position",
    "predicts_object",
    "read_final_short_vowel",
]


class ObjecthoodMeasurementError(ValueError):
    """رُفض قياسٌ لا يُعاد اشتقاقُه من أعداده أو لا يُطابق مواصفتَه المُجمَّدة."""


NORMALIZATION_FORM: Final[Literal["NFC"]] = "NFC"

UNICODE_DATABASE_VERSION: Final[str] = "15.0.0"

_FATHA: Final[str] = "\u064e"
_DAMMA: Final[str] = "\u064f"
_KASRA: Final[str] = "\u0650"
_FATHATAN: Final[str] = "\u064b"
_DAMMATAN: Final[str] = "\u064c"
_KASRATAN: Final[str] = "\u064d"
_SUKUN: Final[str] = "\u0652"

_CASE_VOWELS: Final[frozenset[str]] = frozenset(
    {_FATHA, _DAMMA, _KASRA, _FATHATAN, _DAMMATAN, _KASRATAN}
)

_FATHA_FORMS: Final[frozenset[str]] = frozenset({_FATHA, _FATHATAN})

FUNCTION_WORD_UPOS_TAGS: Final[frozenset[str]] = frozenset(
    {"ADP", "CCONJ", "SCONJ", "PART", "PUNCT", "DET", "AUX"}
)

FUNCTION_WORDS_ARE_IN_THE_POPULATION_AS_STATED_NOTE: Final[str] = (
    "FunctionWordsAreInThePopulationAsStated: أكثرُ ما تُخطئ فيه الدعوى كلماتٌ "
    "وظيفيةٌ تلي الفعلَ الماضيَ وآخرُها فتحة — حروفُ جرٍّ ونواصبُ وعواطف — لا "
    "أسماءٌ أُسيءَ إعرابُها. والدعوى كما نُطِق بها لا تستثني صنفًا، فتُحسَب "
    "عليها؛ ومن استثناها بدّل الدعوى ولم يقسها، ولذلك يُعَدُّ هذا الصنفُ بحقلٍ "
    "مستقلٍّ ولا يُطرَح من المقام"
)

PREREGISTERED_VOCABULARY_COVERS_PREDICTED_POSITIONS_ONLY_NOTE: Final[str] = (
    "PreregisteredVocabularyCoversPredictedPositionsOnly: المنازلُ الثلاثُ "
    "المُجمَّدةُ في المواصفة تغطّي ما تنبّأت به الدعوى وما تعذّرت قراءتُه، ولا "
    "منزلةَ فيها لموضعٍ مقروءٍ لم تتنبّأ به. فحُفِظ هذا الصنفُ في حقلٍ رابعٍ "
    "باسمه، ولم يُدسَّ في `أخطأ` ولا في `متعذّر_القياس`، ويبقى النقصُ مُسجَّلًا "
    "على المواصفة لا مُصحَّحًا فيها بعد رؤية الأرقام"
)

NO_RULE_DEVELOPMENT_HAPPENED_THIS_ROUND_NOTE: Final[str] = (
    "NoRuleDevelopmentHappenedThisRound: القاعدةُ المُشغَّلةُ على القسمين واحدةٌ "
    "بحروفها، ولم تُطوَّر على قسم التطوير ولا سُطر منها بعد رؤية خطأٍ. ففرقُ "
    "الرقمين ليس مقدارَ ملاءمةٍ بل اختلافَ قسمين، وقسمُ التطوير محفوظٌ لجولةٍ "
    "تُطوَّر فيها قاعدةٌ إن طُوِّرت"
)

ADJACENCY_IS_NOT_GOVERNMENT_NOTE: Final[str] = (
    "AdjacencyIsNotGovernment: «التالية للفعل» في الدعوى مجاورةٌ خطّيةٌ في سطور "
    "الملفّ، وليست عملًا نحويًّا؛ فقد يكون الفعلُ غيرَ رأسِ الكلمة التالية "
    "أصلًا. والمقيسُ ما نُطِقت به الدعوى، وتبديلُه بشرط رأسٍ دعوى أخرى تحتاج "
    "تسجيلًا قَبْليًّا خاصًّا بها"
)

OBJECTHOOD_MEASUREMENT_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "FunctionWordsAreInThePopulationAsStated": (
        FUNCTION_WORDS_ARE_IN_THE_POPULATION_AS_STATED_NOTE
    ),
    "PreregisteredVocabularyCoversPredictedPositionsOnly": (
        PREREGISTERED_VOCABULARY_COVERS_PREDICTED_POSITIONS_ONLY_NOTE
    ),
    "NoRuleDevelopmentHappenedThisRound": NO_RULE_DEVELOPMENT_HAPPENED_THIS_ROUND_NOTE,
    "AdjacencyIsNotGovernment": ADJACENCY_IS_NOT_GOVERNMENT_NOTE,
    "ObjIsUdObjecthoodNotClassicalMaful": OBJ_IS_UD_OBJECTHOOD_NOT_CLASSICAL_MAFUL_NOTE,
    "VformIsAnAnnotatorsVocalization": VFORM_IS_AN_ANNOTATORS_VOCALIZATION_NOTE,
    "RegisterIsNewswireNotQuranic": REGISTER_IS_NEWSWIRE_NOT_QURANIC_NOTE,
}

_RESULT_BEARING_WORDS: Final[frozenset[str]] = frozenset(
    {"decision", "verdict", "precision", "recall", "accuracy", "share", "upheld"}
)


def read_final_short_vowel(vocalized: str) -> str | None:
    """آخرُ حركةٍ قصيرةٍ أو تنوينٍ في الصورة المشكولة، أو `None` إن لم تُقرأ.

    والمسحُ من آخر الحروف إلى أوّلها كما في `irab_case_readout`: السكونُ يقطع
    المسحَ لأنّه إعلانُ ألّا حركةَ هناك، فلا تُقرأ حركةُ ما قبله حركةَ آخرٍ.
    """

    if not isinstance(vocalized, str):
        raise ObjecthoodMeasurementError("الصورةُ المشكولةُ نصٌّ؛ ولا تُقرَأ من غيره.")
    normalized = unicodedata.normalize(NORMALIZATION_FORM, vocalized)
    for character in reversed(normalized):
        if character in _CASE_VOWELS:
            return character
        if character == _SUKUN:
            return None
    return None


def predicts_object(vocalized: str) -> bool | None:
    """أتتنبّأ الدعوى كما نُطِق بها بمفعوليةِ هذه الصورة؟ و`None` إن تعذّرت."""

    vowel = read_final_short_vowel(vocalized)
    if vowel is None:
        return None
    return vowel in _FATHA_FORMS


def classify_position(vocalized: str, gold_relation: str) -> ObjecthoodPositionOutcome:
    """منزلةُ موضعٍ تنبّأت به الدعوى، أو تعذّر قياسُه.

    ويُرفَع الخطأُ على الموضع المقروءِ الذي لم تتنبّأ به الدعوى بدل أن يُعطى
    منزلةً ليست له؛ فالمفردةُ المُجمَّدة لا تحمل له منزلة، وذاك نقصُها المُسجَّل
    في `PREREGISTERED_VOCABULARY_COVERS_PREDICTED_POSITIONS_ONLY`.
    """

    if not isinstance(gold_relation, str) or not gold_relation.strip():
        raise ObjecthoodMeasurementError("العلاقةُ المرجعيةُ نصٌّ غير فارغ.")
    predicted = predicts_object(vocalized)
    if predicted is None:
        return ObjecthoodPositionOutcome.UNREADABLE_SURFACE
    if not predicted:
        raise ObjecthoodMeasurementError(
            "لا منزلةَ في المفردة المُجمَّدة لموضعٍ مقروءٍ لم تتنبّأ به الدعوى؛ "
            "ويُعَدّ في حقله الرابع ولا يُدَسّ في منزلةٍ من الثلاث."
        )
    base = gold_relation.split(":")[0]
    if base == OBJECTHOOD_PREREGISTRATION.gold_relation:
        return ObjecthoodPositionOutcome.PREDICTED_AND_IS_OBJECT
    return ObjecthoodPositionOutcome.PREDICTED_AND_IS_NOT_OBJECT


@dataclass(frozen=True, slots=True)
class ObjecthoodMeasurement:
    """قياسٌ مُجمَّدٌ مربوطٌ ببصمة مواصفته؛ وحكمُه مُشتقٌّ بعتبتها لا مكتوب."""

    witness: IrabCorpusWitness
    split: str
    preregistration_digest: str
    normalization_form: str
    unicode_database_version: str
    population: int
    predicted_and_is_object: int
    predicted_and_is_not_object: int
    unreadable_positions: int
    readable_but_not_predicted: int
    objects_in_population: int
    function_word_errors: int
    content_word_errors: int

    def __post_init__(self) -> None:
        if not isinstance(self.witness, IrabCorpusWitness):
            raise ObjecthoodMeasurementError("الشاهدُ عضوٌ في نوعه لا نصٌّ حرّ.")
        if not isinstance(self.split, str) or not self.split.strip():
            raise ObjecthoodMeasurementError(
                "اسمُ القسم نصٌّ غير فارغ؛ وقياسٌ بلا قسمٍ مُبهَم."
            )
        if self.preregistration_digest != OBJECTHOOD_PREREGISTRATION.content_digest:
            raise ObjecthoodMeasurementError(
                "بصمةُ المواصفة المربوطةُ بالقياس تُطابق بصمةَ المواصفة الحيّة؛ "
                "واختلافُهما يعني أنّ المواصفةَ بُدِّلت بعد تجميدها أو أنّ هذا "
                "القياسَ لم يجرِ بها."
            )
        if self.normalization_form != NORMALIZATION_FORM:
            raise ObjecthoodMeasurementError(
                "صيغةُ التطبيع تُطابق صيغةَ الوحدة؛ وقياسٌ بصيغةٍ أخرى قياسٌ على حروفٍ أخرى."
            )
        if (
            not isinstance(self.unicode_database_version, str)
            or not self.unicode_database_version.strip()
        ):
            raise ObjecthoodMeasurementError("إصدارُ قاعدة Unicode نصٌّ غير فارغ.")
        counts = {
            "المجتمع": self.population,
            "المُصاب": self.predicted_and_is_object,
            "المُخطأ": self.predicted_and_is_not_object,
            "المتعذّر": self.unreadable_positions,
            "المقروءُ غيرُ المتنبَّأ به": self.readable_but_not_predicted,
            "المفاعيلُ في المجتمع": self.objects_in_population,
            "خطأُ الكلمات الوظيفية": self.function_word_errors,
            "خطأُ الكلمات المعجمية": self.content_word_errors,
        }
        for label, number in counts.items():
            if not isinstance(number, int) or number < 0:
                raise ObjecthoodMeasurementError(f"{label} عددٌ صحيحٌ غيرُ سالب.")
        if (
            self.predicted_and_is_object
            + self.predicted_and_is_not_object
            + self.unreadable_positions
            + self.readable_but_not_predicted
            != self.population
        ):
            raise ObjecthoodMeasurementError(
                "المنازلُ الأربعُ تستغرق المجتمعَ كلَّه؛ وفرقٌ بينها وبينه يعني "
                "موضعًا سقط من العدّ بلا منزلة."
            )
        if self.predicted_and_is_object + self.predicted_and_is_not_object == 0:
            raise ObjecthoodMeasurementError(
                "دعوى لم تحسم موضعًا واحدًا لا تُشتقّ منها نسبة؛ ونسبةٌ من صفرٍ رقمٌ مصنوع."
            )
        if (
            self.function_word_errors + self.content_word_errors
            != self.predicted_and_is_not_object
        ):
            raise ObjecthoodMeasurementError(
                "صنفا الخطأ يستغرقان الخطأَ كلَّه؛ وفرقٌ بينهما وبينه يعني خطأً "
                "بلا صنفٍ مُسمّى."
            )
        if self.objects_in_population > self.population:
            raise ObjecthoodMeasurementError(
                "المفاعيلُ في المجتمع جزءٌ منه؛ وجزءٌ أكبرُ من كلٍّ خطأُ عدّ."
            )
        if self.predicted_and_is_object > self.objects_in_population:
            raise ObjecthoodMeasurementError(
                "المُصابُ جزءٌ من مفاعيل المجتمع؛ ولا يزيد الجزءُ على كلِّه."
            )

    @property
    def decided_positions(self) -> int:
        """المواضعُ التي حسمتها الدعوى؛ والمتعذّرُ وغيرُ المتنبَّأ به ليسا منها."""

        return self.predicted_and_is_object + self.predicted_and_is_not_object

    @property
    def precision_on_decided(self) -> float:
        """نسبةُ الإصابة من المحسوم وحده؛ مُشتَقّةٌ لا مكتوبة."""

        return self.predicted_and_is_object / self.decided_positions

    @property
    def recall_over_objects(self) -> float:
        """حصّةُ ما بلغته الدعوى من مفاعيل المجتمع؛ فدقّةٌ بلا بلوغٍ نصفُ خبر."""

        if self.objects_in_population == 0:
            raise ObjecthoodMeasurementError(
                "لا مفعولَ في المجتمع، فلا تُشتقّ حصّةُ بلوغٍ من صفر."
            )
        return self.predicted_and_is_object / self.objects_in_population

    @property
    def unreadable_share(self) -> float:
        """حصّةُ المتعذّر من المجتمع؛ تُعلَن مع النسبة ولا تُطوى تحتها."""

        return self.unreadable_positions / self.population

    @property
    def function_word_error_share(self) -> float:
        """حصّةُ الكلمات الوظيفية من الخطأ؛ تُبيِّن أنّ الخلل في المجتمع لا في الحركة."""

        if self.predicted_and_is_not_object == 0:
            raise ObjecthoodMeasurementError("لا خطأَ هنا، فلا تُقسَّم حصصُ خطأٍ معدوم.")
        return self.function_word_errors / self.predicted_and_is_not_object

    @property
    def decision(self) -> ObjecthoodDecision:
        """الحكمُ بعتبةِ المواصفة المُجمَّدة قبل القراءة، لا بعتبةٍ تُختار الآن."""

        return OBJECTHOOD_PREREGISTRATION.decide(self.precision_on_decided)


def _refuse_result_bearing_fields() -> None:
    """يمنع عند الاستيراد إيداعَ حكمٍ أو نسبةٍ حقلًا بدل اشتقاقها من الأعداد."""

    for field in fields(ObjecthoodMeasurement):
        for word in field.name.split("_"):
            if word in _RESULT_BEARING_WORDS:
                raise ObjecthoodMeasurementError(
                    f"`{field.name}` حقلٌ يحمل حكمًا أو نسبة؛ وكلاهما يُشتقّ من "
                    f"الأعداد ولا يُودَع."
                )


_refuse_result_bearing_fields()


DEVELOPMENT_SPLIT_OBJECTHOOD_MEASUREMENT: Final[ObjecthoodMeasurement] = (
    ObjecthoodMeasurement(
        witness=UD_ARABIC_PADT_DEV_CENSUS.witness,
        split="ar_padt-ud-dev (قسم التطوير المُعلَن، ولم تُطوَّر عليه قاعدة)",
        preregistration_digest=OBJECTHOOD_PREREGISTRATION.content_digest,
        normalization_form=NORMALIZATION_FORM,
        unicode_database_version=UNICODE_DATABASE_VERSION,
        population=1_267,
        predicted_and_is_object=135,
        predicted_and_is_not_object=314,
        unreadable_positions=149,
        readable_but_not_predicted=669,
        objects_in_population=190,
        function_word_errors=202,
        content_word_errors=112,
    )
)

HELD_OUT_SPLIT_OBJECTHOOD_MEASUREMENT: Final[ObjecthoodMeasurement] = (
    ObjecthoodMeasurement(
        witness=UD_ARABIC_PADT_TEST_CENSUS.witness,
        split="ar_padt-ud-test (القسم المحجوب، وهو الرقم المُعلَن)",
        preregistration_digest=OBJECTHOOD_PREREGISTRATION.content_digest,
        normalization_form=NORMALIZATION_FORM,
        unicode_database_version=UNICODE_DATABASE_VERSION,
        population=1_192,
        predicted_and_is_object=150,
        predicted_and_is_not_object=269,
        unreadable_positions=120,
        readable_but_not_predicted=653,
        objects_in_population=220,
        function_word_errors=188,
        content_word_errors=81,
    )
)
