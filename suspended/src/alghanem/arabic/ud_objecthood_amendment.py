"""تصحيحُ عيبَين مُسمَّيَين، بمواصفةٍ مُعدَّلةٍ لا بتحريرِ المواصفة المُجمَّدة.

سُمِّي في الجولة الماضية عيبان ولم يُلطَّفا:

* **عيبُ المجتمع** (`FUNCTION_WORDS_ARE_IN_THE_POPULATION_AS_STATED`): ١٨٨ من
  ٢٦٩ خطأً في القسم المحجوب كلماتٌ وظيفية — «إِلَى» و«أَنَّ» و«وَ» و«لَ» —
  آخرُها فتحةٌ وليست أسماءً أصلًا.
* **عيبُ المفردة** (`PREREGISTERED_VOCABULARY_COVERS_PREDICTED_POSITIONS_ONLY`):
  منازلُ الموضع الثلاثُ المُجمَّدة لا منزلةَ فيها لموضعٍ مقروءٍ لم تتنبّأ به
  الدعوى، فكان `classify_position` يرفع خطأً بدل أن يُصنِّف.

**وتصحيحُهما هنا إلى الأمام لا بالرجوع** (`THE_FROZEN_SPECIFICATION_IS_NOT_EDITED`):
لم يُمَسّ `ud_objecthood_preregistration` ولا `ud_objecthood_measurement` بحرف،
وبصمةُ المواصفة الأولى كما هي، وقياسُ الدعوى كما نُطِق بها قائمٌ عند ٣٥٫٨٪.
فتحريرُ مواصفةٍ بعد رؤية رقمها هو عينُ ما تمنعه هذه الشجرة، ولو كان التحرير
إصلاحًا صادقًا: من حرّر مواصفتَه بعد الرقم لم يَعُد يملك مواصفةً سابقةً للدليل.

**وهذه المواصفةُ المُعدَّلةُ أضعفُ منزلةً من الأولى، ويُصرَّح بذلك في بنيتها**
(`AN_AMENDMENT_AFTER_THE_NUMBER_IS_WEAKER_THAN_A_PREREGISTRATION`): كُتِبت بعد
رؤية أرقام القسمين، فحقلُ `standing` فيها مُلزَمٌ بقيمة `معدَّلة_بعد_الرقم`،
ولا سبيلَ إلى بنائها بمنزلة `سابقة_للدليل` البتّة.

**والعتبتان لم تُحرَّكا**: القيامُ عند ٩٠٪ والسقوطُ عند ٦٠٪، مأخوذتان من
المواصفة الأولى استيرادًا لا نسخًا، لأنّ تحريكَ عتبةٍ بعد رقمٍ منظورٍ تفصيلُ
حكمٍ على مقاس النتيجة.

**والنتيجة: التصحيحُ لا يُنقِذ الدعوى**. على القسم المحجوب ترتفع الإصابةُ من
٣٥٫٨٪ إلى **٦٤٫٥٪** — وهي في نطاق عدم الحسم لا فوق عتبة القيام — وعلى قسم
التطوير ٥٤٫٧٪ وهي دون عتبة السقوط. فالقسمان يختلفان في الحكم بعد التعديل
(`THE_TWO_SPLITS_DISAGREE_UNDER_THE_AMENDMENT`)، واختلافُهما نفسُه دليلٌ على
أنّ الدعوى لم تبلغ حدًّا يُقال عنده «قامت».

**وللتصحيح ثمنٌ يُسمّى** (`THE_AMENDED_POPULATION_IS_DEFINED_BY_THE_ANNOTATION`):
استثناءُ الكلمات الوظيفية يقرأ عمودَ `UPOS` من المدوَّنة نفسِها، فالقارئُ
المُعدَّل لم يعد قارئًا سطحيًّا خالصًا: صار يستهلك عمودًا مُوسَّمًا ليُعرِّف
مجتمعَه، ثمّ يُقاس على عمودٍ مُوسَّمٍ آخر. ومن أراد تشغيلَ هذه الدعوى على نصٍّ
غيرِ مُوسَّمٍ لزِمَه مُصنِّفُ أقسامٍ لم يُبنَ هنا، ودقّتُه تدخل في الرقم.

وهذه الوحدة تسجيلٌ لا سلطة: لا ولادةَ فيها، ولا حكمَ ولادة، ولا تجميدَ `E0`،
ولا تستورد من `kernel/` شيئًا، ولا تقرؤها وحدةٌ فيه.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from typing import Final

from alghanem.canonical_content import canonical_bytes, canonical_digest

from .irab_corpus_witness import IrabCorpusWitness
from .ud_objecthood_measurement import (
    FUNCTION_WORD_UPOS_TAGS,
    NORMALIZATION_FORM,
    UNICODE_DATABASE_VERSION,
    ObjecthoodMeasurementError,
    predicts_object,
)
from .ud_objecthood_preregistration import (
    OBJECTHOOD_PREREGISTRATION,
    ObjecthoodDecision,
)
from .ud_relation_layer_step0 import (
    UD_ARABIC_PADT_DEV_CENSUS,
    UD_ARABIC_PADT_TEST_CENSUS,
)

__all__ = [
    "AN_AMENDMENT_AFTER_THE_NUMBER_IS_WEAKER_THAN_A_PREREGISTRATION_NOTE",
    "AMENDED_OBJECTHOOD_SPECIFICATION",
    "AMENDED_DEVELOPMENT_SPLIT_MEASUREMENT",
    "AMENDED_HELD_OUT_SPLIT_MEASUREMENT",
    "AMENDMENT_NAMED_RESIDUALS",
    "AmendedObjecthoodMeasurement",
    "AmendedObjecthoodSpecification",
    "AmendedPositionOutcome",
    "AmendmentStanding",
    "THE_AMENDED_POPULATION_IS_DEFINED_BY_THE_ANNOTATION_NOTE",
    "THE_FROZEN_SPECIFICATION_IS_NOT_EDITED_NOTE",
    "THE_TWO_SPLITS_DISAGREE_UNDER_THE_AMENDMENT_NOTE",
    "classify_amended_position",
    "is_function_word",
]


class AmendmentStanding(Enum):
    """منزلةُ المواصفة؛ والقيمةُ الأقوى معلنةٌ ليُرى أنّ هذه ليست إيّاها."""

    PRIOR_TO_EVIDENCE = "سابقة_للدليل"
    AMENDED_AFTER_THE_NUMBER = "معدَّلة_بعد_الرقم"


class AmendedPositionOutcome(Enum):
    """منازلُ الموضع أربعٌ بعد التصحيح؛ والرابعةُ هي التي كان نقصُها العيب."""

    PREDICTED_AND_IS_OBJECT = "أصاب"
    PREDICTED_AND_IS_NOT_OBJECT = "أخطأ"
    UNREADABLE_SURFACE = "متعذّر_القياس"
    READABLE_BUT_NOT_PREDICTED = "مقروء_لم_تتنبّأ_به"


THE_FROZEN_SPECIFICATION_IS_NOT_EDITED_NOTE: Final[str] = (
    "TheFrozenSpecificationIsNotEdited: لم يُمَسَّ نصُّ المواصفة الأولى ولا "
    "بصمتُها ولا قياسُها؛ والتصحيحُ مواصفةٌ ثانيةٌ ببصمةٍ أخرى. فمن صحّح داخلَ "
    "مواصفةٍ مُجمَّدةٍ بعد رؤية رقمها أتلف الترتيبَ الذي جمّدها من أجله، ولو "
    "كان تصحيحُه صوابًا في نفسه"
)

AN_AMENDMENT_AFTER_THE_NUMBER_IS_WEAKER_THAN_A_PREREGISTRATION_NOTE: Final[str] = (
    "AnAmendmentAfterTheNumberIsWeakerThanAPreregistration: هذه المواصفةُ كُتِبت "
    "بعد رؤية أرقام القسمين، فلا تُساوي مواصفةً سبقت دليلَها. ومنزلتُها حقلٌ "
    "مُلزَمٌ في بنيتها لا تصريحٌ في نثرٍ يُقرأ أو يُهمَل، ولا تُبنى بالمنزلة "
    "الأقوى البتّة"
)

THE_AMENDED_POPULATION_IS_DEFINED_BY_THE_ANNOTATION_NOTE: Final[str] = (
    "TheAmendedPopulationIsDefinedByTheAnnotation: استثناءُ الكلمات الوظيفية "
    "يقرأ عمودَ `UPOS` من المدوَّنة، فمجتمعُ القياس صار مُعرَّفًا بوَسْمٍ لا "
    "بسطحٍ. فالقارئُ المُعدَّل يستهلك عمودًا مُوسَّمًا ثمّ يُقاس على عمودٍ "
    "مُوسَّمٍ آخر، ونقلُه إلى نصٍّ غيرِ مُوسَّمٍ يحتاج مُصنِّفَ أقسامٍ لم يُبنَ "
    "هنا وتدخل دقّتُه في الرقم"
)

THE_TWO_SPLITS_DISAGREE_UNDER_THE_AMENDMENT_NOTE: Final[str] = (
    "TheTwoSplitsDisagreeUnderTheAmendment: بعد التصحيح يقع القسمُ المحجوب في "
    "نطاق عدم الحسم ويبقى قسمُ التطوير دون عتبة السقوط، فالحكمان مختلفان على "
    "مدوَّنةٍ واحدةٍ وقاعدةٍ واحدة. ولا يُؤخَذ أعلى الرقمين ويُترَك أدناهما: "
    "اختلافُهما نفسُه يمنع أن يُقال «قامت الدعوى»"
)

AMENDMENT_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "TheFrozenSpecificationIsNotEdited": THE_FROZEN_SPECIFICATION_IS_NOT_EDITED_NOTE,
    "AnAmendmentAfterTheNumberIsWeakerThanAPreregistration": (
        AN_AMENDMENT_AFTER_THE_NUMBER_IS_WEAKER_THAN_A_PREREGISTRATION_NOTE
    ),
    "TheAmendedPopulationIsDefinedByTheAnnotation": (
        THE_AMENDED_POPULATION_IS_DEFINED_BY_THE_ANNOTATION_NOTE
    ),
    "TheTwoSplitsDisagreeUnderTheAmendment": (
        THE_TWO_SPLITS_DISAGREE_UNDER_THE_AMENDMENT_NOTE
    ),
}

_RESULT_BEARING_WORDS: Final[frozenset[str]] = frozenset(
    {"decision", "verdict", "precision", "recall", "accuracy", "share", "upheld"}
)


def is_function_word(upos: str) -> bool:
    """أكلمةٌ وظيفيةٌ هي؟ والقائمةُ مكتوبةٌ مرّةً واحدةً في وحدة القياس الأولى."""

    if not isinstance(upos, str) or not upos.strip():
        raise ObjecthoodMeasurementError("وَسْمُ القسم نصٌّ غير فارغ.")
    return upos in FUNCTION_WORD_UPOS_TAGS


def classify_amended_position(
    vocalized: str, gold_relation: str
) -> AmendedPositionOutcome:
    """منزلةُ الموضع بالمفردة الرباعية؛ ولا موضعَ يُرفَع عليه خطأٌ بعد اليوم.

    وهذا هو تصحيحُ العيب الثاني بعينه: كان الموضعُ المقروءُ الذي لم تتنبّأ به
    الدعوى يرفع خطأً لأنّ المفردةَ لا تحمل له منزلة، فصارت له منزلةٌ باسمه.
    """

    if not isinstance(gold_relation, str) or not gold_relation.strip():
        raise ObjecthoodMeasurementError("العلاقةُ المرجعيةُ نصٌّ غير فارغ.")
    predicted = predicts_object(vocalized)
    if predicted is None:
        return AmendedPositionOutcome.UNREADABLE_SURFACE
    if not predicted:
        return AmendedPositionOutcome.READABLE_BUT_NOT_PREDICTED
    base = gold_relation.split(":")[0]
    if base == OBJECTHOOD_PREREGISTRATION.gold_relation:
        return AmendedPositionOutcome.PREDICTED_AND_IS_OBJECT
    return AmendedPositionOutcome.PREDICTED_AND_IS_NOT_OBJECT


@dataclass(frozen=True, slots=True)
class AmendedObjecthoodSpecification:
    """مواصفةٌ تُصحِّح عيبَين مُسمَّيَين، ومنزلتُها الأضعفُ مُلزَمةٌ في بنيتها."""

    amends_digest: str
    standing: AmendmentStanding
    corrected_defects: tuple[str, ...]
    excluded_upos: frozenset[str]
    population_definition: str
    inherited_threshold_source: str

    def __post_init__(self) -> None:
        if self.amends_digest != OBJECTHOOD_PREREGISTRATION.content_digest:
            raise ObjecthoodMeasurementError(
                "المواصفةُ المُعدَّلةُ مربوطةٌ ببصمة المواصفة التي تُعدِّلها؛ "
                "وتعديلٌ لا يُسمّي أصلَه تعديلٌ بلا أصل."
            )
        if self.standing is not AmendmentStanding.AMENDED_AFTER_THE_NUMBER:
            raise ObjecthoodMeasurementError(
                "هذه المواصفةُ كُتِبت بعد رؤية الرقم، فلا تُبنى بمنزلة السابق "
                "للدليل؛ ومنزلةٌ تُدّعى أعلى من حالها ادّعاءُ ترتيبٍ لم يحصل."
            )
        if (
            not isinstance(self.corrected_defects, tuple)
            or len(self.corrected_defects) < 2
        ):
            raise ObjecthoodMeasurementError(
                "العيوبُ المُصحَّحةُ تُسمّى بأسمائها المُودَعة، وهي اثنان على الأقلّ."
            )
        for defect in self.corrected_defects:
            if not isinstance(defect, str) or not defect.strip():
                raise ObjecthoodMeasurementError("اسمُ العيب نصٌّ غير فارغ.")
        if not isinstance(self.excluded_upos, frozenset) or not self.excluded_upos:
            raise ObjecthoodMeasurementError(
                "الأقسامُ المستثناةُ مُسمّاةٌ مُجمَّدة؛ واستثناءٌ فارغٌ ليس تصحيحًا."
            )
        if self.excluded_upos != FUNCTION_WORD_UPOS_TAGS:
            raise ObjecthoodMeasurementError(
                "الأقسامُ المستثناةُ هي عينُ القائمة التي صُنِّف بها خطأُ القياس "
                "الأوّل؛ وقائمةٌ ثانيةٌ تختار ما يُستثنى بعد الرقم."
            )
        for label, text in (
            ("تعريفُ المجتمع", self.population_definition),
            ("مصدرُ العتبتين", self.inherited_threshold_source),
        ):
            if not isinstance(text, str) or not text.strip():
                raise ObjecthoodMeasurementError(f"{label} نصٌّ غير فارغ.")

    @property
    def claim_stands_at_or_above(self) -> float:
        """عتبةُ القيام موروثةٌ من المواصفة الأولى، لا مكتوبةٌ هنا من جديد."""

        return OBJECTHOOD_PREREGISTRATION.claim_stands_at_or_above

    @property
    def claim_falls_at_or_below(self) -> float:
        """عتبةُ السقوط موروثةٌ كذلك؛ فلا تتحرّك عتبةٌ بعد رقمٍ منظور."""

        return OBJECTHOOD_PREREGISTRATION.claim_falls_at_or_below

    @property
    def content_digest(self) -> str:
        """بصمةُ المواصفة المُعدَّلة، وهي غيرُ بصمة المواصفة التي تُعدِّلها."""

        return canonical_digest(
            canonical_bytes(
                {
                    "amends_digest": self.amends_digest,
                    "standing": self.standing.value,
                    "corrected_defects": list(self.corrected_defects),
                    "excluded_upos": sorted(self.excluded_upos),
                    "population_definition": self.population_definition,
                    "inherited_threshold_source": self.inherited_threshold_source,
                }
            )
        )

    def decide(self, precision_on_decided: float) -> ObjecthoodDecision:
        """الحسمُ بعتبتَي المواصفة الأولى نفسِهما، بلا تحريكٍ ولا استثناء."""

        return OBJECTHOOD_PREREGISTRATION.decide(precision_on_decided)


AMENDED_OBJECTHOOD_SPECIFICATION: Final[AmendedObjecthoodSpecification] = (
    AmendedObjecthoodSpecification(
        amends_digest=OBJECTHOOD_PREREGISTRATION.content_digest,
        standing=AmendmentStanding.AMENDED_AFTER_THE_NUMBER,
        corrected_defects=(
            "FunctionWordsAreInThePopulationAsStated",
            "PreregisteredVocabularyCoversPredictedPositionsOnly",
        ),
        excluded_upos=FUNCTION_WORD_UPOS_TAGS,
        population_definition=(
            "مجتمعُ المواصفة الأولى نفسُه — كلمةٌ نحويةٌ تسبقها مباشرةً كلمةٌ "
            "عمودُ `UPOS` فيها `VERB` وسماتُها تحمل `Aspect=Perf` — مطروحًا منه "
            "كلُّ كلمةٍ وَسْمُها في `UPOS` من الأقسام الوظيفية المُجمَّدة. "
            "والطرحُ يُخرِج معه ما كان منها موسومًا `obj` فعلًا، فلا يُنتقى "
            "الطرحُ لصالح الدعوى"
        ),
        inherited_threshold_source=(
            "العتبتان مستوردتان من `OBJECTHOOD_PREREGISTRATION` لا منسوختان، "
            "فلا تتحرّك واحدةٌ منهما بعد رؤية الرقم ولو حُرِّرت هنا"
        ),
    )
)


@dataclass(frozen=True, slots=True)
class AmendedObjecthoodMeasurement:
    """قياسٌ بالمواصفة المُعدَّلة، مربوطٌ ببصمتها وببصمة أصلها معًا."""

    witness: IrabCorpusWitness
    split: str
    amended_specification_digest: str
    normalization_form: str
    unicode_database_version: str
    population: int
    predicted_and_is_object: int
    predicted_and_is_not_object: int
    unreadable_positions: int
    readable_but_not_predicted: int
    objects_in_population: int
    objects_lost_to_the_exclusion: int

    def __post_init__(self) -> None:
        if not isinstance(self.witness, IrabCorpusWitness):
            raise ObjecthoodMeasurementError("الشاهدُ عضوٌ في نوعه لا نصٌّ حرّ.")
        if not isinstance(self.split, str) or not self.split.strip():
            raise ObjecthoodMeasurementError("اسمُ القسم نصٌّ غير فارغ.")
        if self.amended_specification_digest != (
            AMENDED_OBJECTHOOD_SPECIFICATION.content_digest
        ):
            raise ObjecthoodMeasurementError(
                "بصمةُ المواصفة المُعدَّلة المربوطةُ بالقياس تُطابق بصمتَها "
                "الحيّة؛ واختلافُهما يعني أنّها بُدِّلت بعد هذا القياس."
            )
        if self.normalization_form != NORMALIZATION_FORM:
            raise ObjecthoodMeasurementError(
                "صيغةُ التطبيع تُطابق صيغةَ وحدة القياس؛ وقياسٌ بصيغةٍ أخرى "
                "قياسٌ على حروفٍ أخرى."
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
            "المفاعيلُ التي أخرجها الاستثناء": self.objects_lost_to_the_exclusion,
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
                "دعوى لم تحسم موضعًا واحدًا لا تُشتقّ منها نسبة."
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
        """المواضعُ التي حسمتها الدعوى بعد التصحيح."""

        return self.predicted_and_is_object + self.predicted_and_is_not_object

    @property
    def precision_on_decided(self) -> float:
        """نسبةُ الإصابة من المحسوم؛ مُشتَقّةٌ لا مكتوبة."""

        return self.predicted_and_is_object / self.decided_positions

    @property
    def recall_over_objects(self) -> float:
        """حصّةُ ما بلغته الدعوى من مفاعيل المجتمع المُعدَّل."""

        if self.objects_in_population == 0:
            raise ObjecthoodMeasurementError("لا مفعولَ في المجتمع، فلا تُشتقّ حصّةُ بلوغ.")
        return self.predicted_and_is_object / self.objects_in_population

    @property
    def unreadable_share(self) -> float:
        """حصّةُ المتعذّر من المجتمع؛ تُعلَن مع النسبة ولا تُطوى تحتها."""

        return self.unreadable_positions / self.population

    @property
    def decision(self) -> ObjecthoodDecision:
        """الحكمُ بعتبتَي المواصفة الأولى؛ ولم تُحرَّك واحدةٌ منهما."""

        return AMENDED_OBJECTHOOD_SPECIFICATION.decide(self.precision_on_decided)


def _refuse_result_bearing_fields() -> None:
    """يمنع عند الاستيراد إيداعَ حكمٍ أو نسبةٍ حقلًا بدل اشتقاقها من الأعداد."""

    for field in fields(AmendedObjecthoodMeasurement):
        for word in field.name.split("_"):
            if word in _RESULT_BEARING_WORDS:
                raise ObjecthoodMeasurementError(
                    f"`{field.name}` حقلٌ يحمل حكمًا أو نسبة؛ وكلاهما يُشتقّ من "
                    f"الأعداد ولا يُودَع."
                )


_refuse_result_bearing_fields()


AMENDED_DEVELOPMENT_SPLIT_MEASUREMENT: Final[AmendedObjecthoodMeasurement] = (
    AmendedObjecthoodMeasurement(
        witness=UD_ARABIC_PADT_DEV_CENSUS.witness,
        split="ar_padt-ud-dev (بالمواصفة المُعدَّلة)",
        amended_specification_digest=AMENDED_OBJECTHOOD_SPECIFICATION.content_digest,
        normalization_form=NORMALIZATION_FORM,
        unicode_database_version=UNICODE_DATABASE_VERSION,
        population=847,
        predicted_and_is_object=135,
        predicted_and_is_not_object=112,
        unreadable_positions=104,
        readable_but_not_predicted=496,
        objects_in_population=190,
        objects_lost_to_the_exclusion=0,
    )
)

AMENDED_HELD_OUT_SPLIT_MEASUREMENT: Final[AmendedObjecthoodMeasurement] = (
    AmendedObjecthoodMeasurement(
        witness=UD_ARABIC_PADT_TEST_CENSUS.witness,
        split="ar_padt-ud-test (بالمواصفة المُعدَّلة، وهو الرقم المُعلَن)",
        amended_specification_digest=AMENDED_OBJECTHOOD_SPECIFICATION.content_digest,
        normalization_form=NORMALIZATION_FORM,
        unicode_database_version=UNICODE_DATABASE_VERSION,
        population=815,
        predicted_and_is_object=147,
        predicted_and_is_not_object=81,
        unreadable_positions=81,
        readable_but_not_predicted=506,
        objects_in_population=216,
        objects_lost_to_the_exclusion=4,
    )
)
