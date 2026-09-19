"""معايير تصنيفٍ أربعةٌ تُقاس مفصولةً، ونتيجةُ الاسترجاع لا تُقرأ تحليلًا.

ثبت لـ`ArabicRoundTripV1` على إيداع الفاتحة تسعٌ وعشرون من تسعٍ وعشرين. وهذا
**عددٌ كتابيٌّ يبقى أساسًا** ولا يُبنى عليه حكمٌ صرفيٌّ ولا إعرابيّ. وما يُضاف
ههنا جدولُ **تغطيةٍ** بأربعة محاور، لكلّ فئةٍ فيه عددُ كلماتٍ، ونتيجةُ استرجاعٍ،
وموضعُ فشلٍ مستقلّ.

`THE_AXES_ARE_MEASURED_APART_NOT_MERGED`: المحاورُ أربعةٌ لا تُخلَط: أصلُ
الكلمة وبنيتُها الصرفيّة، وحالتُها الإعرابيّة العامّة، وأبنيةُ الفعل المبنيّ،
وحالاتُ الفعل المُعرَب. ولا تُنسَب كلمةٌ إلى فئتَين من محورٍ واحد، فلا يُخلَط
البناءُ بالإعراب، ولا حالُ الفعل بحال الاسم.

`ROOT_IS_NOT_A_CATEGORY_BESIDE_JAMID_AND_MASDAR_AND_MUSHTAQQ`: الجذرُ **أصلٌ
صرفيٌّ محتمَل**، والجامدُ والمصدرُ والمشتقُّ أوصافٌ لبنية الكلمة؛ فليسا من بابٍ
واحد. ولذلك لا عضوَ باسم الجذر في `ClassificationCategory`، وإنّما يُسجَّل
الجذرُ في `RootRecord` إلى جانب وصف البنية. ولا يُستخرَج جذرٌ قسرًا من كلّ
كلمة: الحروفُ والأدواتُ والأسماءُ المبنيّةُ تُسجَّل
`غير_مُرخَّصٍ_لهذه_الكلمة` ولا يُفتعَل لها تحليلٌ جذريّ.

`A_MASDAR_IS_ITS_OWN_CATEGORY_WITHOUT_A_PRESUPPOSED_DERIVATION`: المصدرُ فئةُ
قياسٍ مستقلّة، ولا يُفترَض ههنا أنّ كلَّ مصدرٍ مشتقٌّ من فعل، ولا أنّ العلاقةَ
بينهما محسومةٌ في كلّ حال.

`A_DECLARED_TARGET_IS_NOT_A_RESULT`: ما يُكتَب في `COVERAGE_ITEMS` من تصنيفٍ
وعلامةٍ ودليلٍ هو **ما يُراد اختبارُه**، لا ما أثبته المحرّك. ولا حقلَ في هذه
الوحدة يحمل تصنيفًا أخرجه الخطُّ، لأنّ الخطَّ لا يُخرِج تصنيفًا: الصرفُ والنحوُ
خارجُ طبقاته كما يُقرأ في `LAYERS_NOT_IN_THIS_PIPELINE`.

`AN_UNRESOLVED_ANALYSIS_IS_NOT_A_CORRECT_ONE`: الفحصُ غيرُ المحسوم لا يُحسَب
صحيحًا. ولذلك `AnalysisAccuracy` ليست صفرًا ولا واحدًا بل **ممتنعةٌ** لانعدام
مقسومٍ عليه، وتُعرَض شرطةً باسم سببها. وغيرُ المحسوم ههنا **يُسمّى بعلّته**
واحدةً واحدة: لا وَسْمَ مُثبَتًا لهذه الفئة، أو لا عمودَ في المرجع لهذا
السؤال، أو بايتاتُ المرجع غيرُ محلولة، أو لم تُوجَد الكلمةُ في المرجع.

`THE_ANALYTIC_REFERENCE_IS_MASAQ_AND_ITS_STANDING_IS_RUN_NOT_WRITTEN`: المرجعُ
`MASAQ`، وبصمتُه مقروءةٌ من `masaq_corpus_deposit`، ومنزلتُه تُشتَقُّ بتشغيل
`masaq_reference()` لا تُكتَب في حقل. وقد كان اسمُ المرجع ههنا `MAQSAD`،
فصُحِّح إلى المرجع الموجود فعلًا في هذه الشجرة.

`THE_REFERENCE_ANSWERS_ONE_QUESTION_OF_THREE`: MASAQ تَسِم البنيةَ في عمود
`Morph_Tag`، ولا عمودَ فيها لعلامة الإعراب على وجهها المطلوب ههنا ولا لدليلها؛
فسؤالُ الفئة وحدَه قابلٌ للحسم، وسؤالا العلامة والدليل يخرجان بعلّةٍ في المرجع
نفسِه تُقال قبل أن تُطلَب بايتاتُه.

`A_TAGGED_SEGMENT_COUNT_IS_NOT_A_WORD_COUNT_NOR_AN_ACCURACY`: ٤٬٢١٦ بوَسْم
`GERUND` و٣٬١٥٦ بوَسْم `NOUN_ACTIVE_PART` أعدادُ **سجلّاتٍ موسومة**، والسجلُّ
مقطعٌ لا كلمة؛ فليست أعدادَ كلماتٍ فريدة ولا نتيجةَ دقّةٍ للغانم.

`AN_EMPTY_CATEGORY_HAS_NO_RATE`: الفئةُ التي لا كلمةَ لها في هذا الإيداع تبقى
في الجدول صفًّا بصفرٍ ولا تُحذَف، ونسبتُها ممتنعةٌ لا مئةٌ بالمئة. وخلوُّ
أربعِ فئاتٍ من أصل إحدى عشرة هو **الدليلُ المقيس** على أنّ مجتمع الفاتحة أضيقُ
من هذه المعايير، وأنّ المطلوب توسيعُ المدوّنة لا رفعُ نسبةٍ بلغت تمامها.
"""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Final

from .arabic_round_trip_v1 import (
    LayerOutcome,
    RoundTripLayer,
    RoundTripRefusal,
    run_token,
    tokens_from_text,
)
from .fatiha_source_text import FATIHA_SOURCE_TEXT
from .masaq_corpus_deposit import (
    DERIVED_NOUN_TAGS,
    MASAQ_SHA256,
    MORPH_TAG_COLUMN,
    WORD_KEY_COLUMN,
    MasaqDepositError,
    masaq_bytes_are_resolvable,
    masaq_records,
    read_masaq_bytes,
)
from .masaq_fractal_experiment import (
    SEGMENTED_WORD_COLUMN,
    SURA_COLUMN,
    VERSE_COLUMN,
)

__all__ = [
    "ANALYSIS_REFERENCE",
    "AN_EMPTY_CATEGORY_HAS_NO_RATE_NOTE",
    "AN_UNRESOLVED_ANALYSIS_IS_NOT_A_CORRECT_ONE_NOTE",
    "A_DECLARED_TARGET_IS_NOT_A_RESULT_NOTE",
    "A_MASDAR_IS_ITS_OWN_CATEGORY_WITHOUT_A_PRESUPPOSED_DERIVATION_NOTE",
    "A_TAGGED_SEGMENT_COUNT_IS_NOT_A_WORD_COUNT_NOR_AN_ACCURACY_NOTE",
    "AXIS_REFERENCE_REQUIREMENTS",
    "CATEGORY_TAGS",
    "COVERAGE_ITEMS",
    "ROOT_IS_NOT_A_CATEGORY_BESIDE_JAMID_AND_MASDAR_AND_MUSHTAQQ_NOTE",
    "TAGS_NOT_ASSIGNED_TO_A_CATEGORY",
    "THE_ANALYTIC_REFERENCE_IS_MASAQ_AND_ITS_STANDING_IS_RUN_NOT_WRITTEN_NOTE",
    "THE_AXES_ARE_MEASURED_APART_NOT_MERGED_NOTE",
    "THE_REFERENCE_ANSWERS_ONE_QUESTION_OF_THREE_NOTE",
    "AnalysisCheck",
    "AnalysisOutcome",
    "AnalysisQuestion",
    "AnalysisReference",
    "AxisReferenceRequirement",
    "CategoryClaim",
    "CategoryCoverage",
    "ClassificationAxis",
    "ClassificationCategory",
    "ClassificationCoverageError",
    "CoverageItem",
    "CoverageReport",
    "CoverageRow",
    "ReferenceAddress",
    "ReferenceStanding",
    "RootRecord",
    "RootStanding",
    "axis_of",
    "deposit_tokens",
    "letters_only",
    "masaq_reference",
    "render_coverage",
    "run_coverage",
    "settle_question",
    "word_tags",
]


class ClassificationCoverageError(ValueError):
    """رُوجِع الجدولُ بما لا يقوم به؛ ولا يُحمَل على أقربِ حالةٍ مقبولة."""


class ClassificationAxis(Enum):
    """محاورُ القياس الأربعة؛ مفردةٌ مغلقةٌ، ولكلّ محورٍ سؤالُه وعدادُه."""

    ORIGIN_AND_MORPHOLOGICAL_STRUCTURE = "ORIGIN_AND_MORPHOLOGICAL_STRUCTURE"
    GENERAL_IRAB_STANDING = "GENERAL_IRAB_STANDING"
    BUILT_VERB_FORM = "BUILT_VERB_FORM"
    INFLECTED_VERB_CASE = "INFLECTED_VERB_CASE"


class ClassificationCategory(Enum):
    """فئاتُ القياس؛ ولا عضوَ فيها باسم الجذر، فالجذرُ ليس وصفَ بنية."""

    JAMID = "JAMID"
    MASDAR = "MASDAR"
    MUSHTAQQ = "MUSHTAQQ"
    MABNI = "MABNI"
    MURAB = "MURAB"
    PAST_VERB = "PAST_VERB"
    IMPERATIVE_VERB = "IMPERATIVE_VERB"
    BUILT_PRESENT_VERB = "BUILT_PRESENT_VERB"
    PRESENT_MARFU = "PRESENT_MARFU"
    PRESENT_MANSUB = "PRESENT_MANSUB"
    PRESENT_MAJZUM = "PRESENT_MAJZUM"


_CATEGORY_AXIS: Final[dict[ClassificationCategory, ClassificationAxis]] = {
    ClassificationCategory.JAMID: (
        ClassificationAxis.ORIGIN_AND_MORPHOLOGICAL_STRUCTURE
    ),
    ClassificationCategory.MASDAR: (
        ClassificationAxis.ORIGIN_AND_MORPHOLOGICAL_STRUCTURE
    ),
    ClassificationCategory.MUSHTAQQ: (
        ClassificationAxis.ORIGIN_AND_MORPHOLOGICAL_STRUCTURE
    ),
    ClassificationCategory.MABNI: ClassificationAxis.GENERAL_IRAB_STANDING,
    ClassificationCategory.MURAB: ClassificationAxis.GENERAL_IRAB_STANDING,
    ClassificationCategory.PAST_VERB: ClassificationAxis.BUILT_VERB_FORM,
    ClassificationCategory.IMPERATIVE_VERB: ClassificationAxis.BUILT_VERB_FORM,
    ClassificationCategory.BUILT_PRESENT_VERB: ClassificationAxis.BUILT_VERB_FORM,
    ClassificationCategory.PRESENT_MARFU: ClassificationAxis.INFLECTED_VERB_CASE,
    ClassificationCategory.PRESENT_MANSUB: ClassificationAxis.INFLECTED_VERB_CASE,
    ClassificationCategory.PRESENT_MAJZUM: ClassificationAxis.INFLECTED_VERB_CASE,
}


def axis_of(category: ClassificationCategory) -> ClassificationAxis:
    """محورُ هذه الفئة؛ ولا فئةَ بلا محورٍ مُسمًّى، فالخلطُ يبدأ من ههنا."""

    if not isinstance(category, ClassificationCategory):
        raise ClassificationCoverageError("الفئةُ عضوٌ في مفردتها المغلقة لا نصٌّ حُرّ")
    try:
        return _CATEGORY_AXIS[category]
    except KeyError as error:  # pragma: no cover - يُمنَع ببناء المفردة
        raise ClassificationCoverageError(
            f"الفئةُ {category.value} بلا محورٍ مُسنَد"
        ) from error


_MARKER_BEARING_AXES: Final[frozenset[ClassificationAxis]] = frozenset(
    {
        ClassificationAxis.GENERAL_IRAB_STANDING,
        ClassificationAxis.BUILT_VERB_FORM,
        ClassificationAxis.INFLECTED_VERB_CASE,
    }
)
"""المحاورُ التي يسأل سؤالُها عن علامةٍ ودليل؛ ومحورُ البنية ليس منها."""


_ATTESTED_TAGS: Final[frozenset[str]] = frozenset(
    item.tag for item in DERIVED_NOUN_TAGS
)
"""الوسومُ المُثبَتةُ في هذه الشجرة؛ ولا يُكتَب وَسْمٌ لم يُقرأ في إيداعٍ."""


CATEGORY_TAGS: Final[dict[ClassificationCategory, frozenset[str]]] = {
    ClassificationCategory.MASDAR: frozenset(
        {
            "GERUND",
            "GERUND_MEEM",
            "GERUND_INSTANT",
            "GERUND_PROFESSION",
            "GERUND_STATE",
        }
    ),
    ClassificationCategory.MUSHTAQQ: frozenset(
        {
            "NOUN_ACTIVE_PART",
            "NOUN_PASSIVE_PART",
            "ADJ_QUALIT",
            "ADJ_INTENS",
            "ADJ_COMP",
            "NOUN_TIME_PLACE",
            "NOUN_INSTRUMENT",
        }
    ),
}
"""ربطُ الفئة بوسوم MASAQ؛ وما لا وَسْمَ له ليس له مدخلٌ ههنا فيُقال بعلّته.

ولا يُكتَب في هذا الجدول وَسْمٌ لم يُقرأ في هذه الشجرة: تسعٌ من إحدى عشرة
فئةً بلا مدخل، لا لأنّ MASAQ لا تسمها، بل لأنّ أسماءَ وسومها لتلك الأبواب
**لم تُقرأ ههنا**، وكتابتُها تخمينًا وَسْمٌ مُفتعَلٌ لا قراءةٌ من مرجع.
"""

TAGS_NOT_ASSIGNED_TO_A_CATEGORY: Final[dict[str, str]] = {
    "NOUN_RELATIVE": "المنسوبُ ليس من المشتقّات السبعة، فلا يُضَمُّ إليها تكثيرًا للمطابقة",
    "NOUN_DIMINUTIVE": "المصغَّرُ ليس من المشتقّات السبعة، وإلحاقُه بها توسيعٌ بلا دليل",
}
"""وسومٌ مُثبَتةٌ تُرِكت بلا فئة عمدًا، وسببُ تركها مكتوبٌ لا مطويّ."""


def _tags_are_attested() -> None:
    unknown = sorted(
        tag
        for tags in CATEGORY_TAGS.values()
        for tag in tags
        if tag not in _ATTESTED_TAGS
    ) + sorted(
        tag for tag in TAGS_NOT_ASSIGNED_TO_A_CATEGORY if tag not in _ATTESTED_TAGS
    )
    if unknown:
        raise ClassificationCoverageError(
            f"وسومٌ غيرُ مُثبَتةٍ في الإيداع كُتِبت ههنا: {unknown}"
        )


_tags_are_attested()


def letters_only(surface: str) -> str:
    """الحروفُ وحدَها بلا حركةٍ ولا تطويل؛ محاذاةُ الموضع لا تُقاس بالشكل.

    وهذا تحويلٌ **للمقارنة** لا للاسترجاع: خطُّ `ArabicRoundTripV1` يُعيد
    البايتات كما دخلت، وهذه الدالّةُ لا تمسّه ولا تدخل فيه.
    """

    return "".join(
        character
        for character in unicodedata.normalize("NFC", surface)
        if unicodedata.category(character) != "Mn" and character != "\u0640"
    )


@dataclass(frozen=True, slots=True)
class ReferenceAddress:
    """موضعُ الكلمة في المرجع: سورةٌ وآية؛ والكلمةُ تُلتَمس بحروفها لا برقمها.

    وترقيمُ الآي في MASAQ لم يُقرأ ههنا، فهذا العنوانُ **مُرشَّحٌ مُعلَن**:
    إن لم تُوجَد الكلمةُ في موضعه خرج الفحصُ
    `UNRESOLVED_WORD_NOT_FOUND_IN_THE_REFERENCE` ولم يُحمَل على أقرب موضع.
    """

    sura: str
    verse: str

    def __post_init__(self) -> None:
        for value, label in ((self.sura, "رقمُ السورة"), (self.verse, "رقمُ الآية")):
            if not value.strip():
                raise ClassificationCoverageError(f"{label} يُكتَب ولا يُترَك فارغًا")


def word_tags(
    records: tuple[dict[str, str], ...],
    address: ReferenceAddress,
    surface: str,
) -> tuple[str, ...] | None:
    """وسومُ مقاطع كلمةٍ واحدةٍ في المرجع، أو `None` إن لم تُوجَد الكلمة.

    المقاطعُ تُجمَع بمفتاح الكلمة `Column5` — لا بـ`Word_No` فهو فهرسُ مقطع —
    ثمّ تُقارَن صورتُها المجموعةُ بحروف الكلمة. ولا تُلتَمس كلمةٌ بالتقريب:
    مجموعةٌ لا تطابق حروفَها ليست هي.
    """

    groups: dict[str, list[str]] = {}
    tags: dict[str, list[str]] = {}
    for record in records:
        if record.get(SURA_COLUMN) != address.sura:
            continue
        if record.get(VERSE_COLUMN) != address.verse:
            continue
        key = record.get(WORD_KEY_COLUMN, "")
        groups.setdefault(key, []).append(record.get(SEGMENTED_WORD_COLUMN, ""))
        tags.setdefault(key, []).append(record.get(MORPH_TAG_COLUMN, ""))
    wanted = letters_only(surface)
    for key, segments in groups.items():
        if letters_only("".join(segments)) == wanted:
            return tuple(tags[key])
    return None


class RootStanding(Enum):
    """منزلةُ الجذر؛ والعليا بلا مدخلٍ حتى يُودَع مرجعٌ يُقرأ منه."""

    READ_FROM_A_DEPOSITED_REFERENCE = "مقروء_من_مرجعٍ_مُودَع"
    AWAITING_THE_REFERENCE = "مُرخَّص_ينتظر_المرجع"
    NOT_LICENSED_FOR_THIS_WORD = "غير_مُرخَّصٍ_لهذه_الكلمة"


class ReferenceStanding(Enum):
    """منزلةُ المرجع التحليليّ؛ وتُشتَقُّ بالتشغيل على البايتات لا تُكتَب."""

    DEPOSITED_AND_FINGERPRINTED = "مُودَع_مُبصَّم"
    FINGERPRINTED_BUT_BYTES_NOT_RESOLVED = "مُبصَّم_بايتاتُه_غيرُ_محلولة"
    BYTES_PRESENT_BUT_DIGEST_MISMATCHED = "بايتاتٌ_حاضرةٌ_خالفت_البصمة"
    BEING_TRANSCRIBED_BY_HAND = "يُطبَع_يدويًّا"
    NAMED_ONLY = "مُسمًّى_فقط"


class AnalysisQuestion(Enum):
    """ما يُسأل عنه في كلّ دعوى: الفئةُ، ثمّ علامتُها، ثمّ دليلُها."""

    CATEGORY = "CATEGORY"
    MARKER = "MARKER"
    EVIDENCE = "EVIDENCE"


class AnalysisOutcome(Enum):
    """حكمُ الفحص التحليليّ؛ وغيرُ المحسوم يُسمّى بعلّته لا بعلّةٍ واحدةٍ جامعة."""

    MATCHED_THE_REFERENCE = "طابق_المرجع"
    CONTRADICTED_THE_REFERENCE = "خالف_المرجع"
    UNRESOLVED_NO_ATTESTED_TAG_FOR_THIS_CATEGORY = "غير_محسوم_لا_وَسْمَ_مُثبَتًا_لهذه_الفئة"
    UNRESOLVED_THE_REFERENCE_HAS_NO_COLUMN_FOR_THIS_QUESTION = (
        "غير_محسوم_لا_عمودَ_في_المرجع_لهذا_السؤال"
    )
    UNRESOLVED_REFERENCE_BYTES_NOT_RESOLVED = "غير_محسوم_بايتاتُ_المرجع_غيرُ_محلولة"
    UNRESOLVED_WORD_NOT_FOUND_IN_THE_REFERENCE = "غير_محسوم_لم_تُوجَد_الكلمةُ_في_المرجع"


_FINGERPRINTED_STANDINGS: Final[frozenset[ReferenceStanding]] = frozenset(
    {
        ReferenceStanding.DEPOSITED_AND_FINGERPRINTED,
        ReferenceStanding.FINGERPRINTED_BUT_BYTES_NOT_RESOLVED,
        ReferenceStanding.BYTES_PRESENT_BUT_DIGEST_MISMATCHED,
    }
)
"""المنازلُ التي تحمل بصمةً مكتوبة؛ والبصمةُ هويّةٌ لا حضورُ بايتات."""


@dataclass(frozen=True, slots=True)
class RootRecord:
    """سجلُّ الجذر إلى جانب وصف البنية؛ ولا يُكتَب جذرٌ بلا مرجعٍ مُودَع."""

    standing: RootStanding
    root: str | None
    why: str

    def __post_init__(self) -> None:
        if not isinstance(self.standing, RootStanding):
            raise ClassificationCoverageError("منزلةُ الجذر عضوٌ في مفردتها المغلقة")
        if self.standing is RootStanding.READ_FROM_A_DEPOSITED_REFERENCE:
            raise ClassificationCoverageError(
                "لا مرجعَ جذريٌّ مُودَعٌ في هذه الشجرة، فلا تُرفَع منزلةُ الجذر بالكتابة"
            )
        if self.root is not None:
            raise ClassificationCoverageError(
                "لا يُكتَب جذرٌ إلّا مقروءًا من مرجعٍ مُودَع، ولا يُستخرَج قسرًا"
            )
        if not self.why.strip():
            raise ClassificationCoverageError("منزلةُ الجذر تُعلَّل ولا تُترَك بلا سبب")


@dataclass(frozen=True, slots=True)
class CategoryClaim:
    """دعوى تصنيفٍ واحدةٌ مُعلَنةٌ للاختبار: فئةٌ، ومعها علامتُها ودليلُها."""

    category: ClassificationCategory
    declared_marker: str | None
    declared_evidence: str | None

    def __post_init__(self) -> None:
        axis = axis_of(self.category)
        wants_marker = axis in _MARKER_BEARING_AXES
        has_marker = bool(self.declared_marker and self.declared_marker.strip())
        has_evidence = bool(self.declared_evidence and self.declared_evidence.strip())
        if wants_marker and not (has_marker and has_evidence):
            raise ClassificationCoverageError(
                f"سؤالُ محور {axis.value} يطلب علامةً ودليلًا، فلا تُعلَن فئتُه بدونهما"
            )
        if not wants_marker and (has_marker or has_evidence):
            raise ClassificationCoverageError(
                "محورُ البنية الصرفيّة لا علامةَ إعرابٍ فيه؛ ولا يُخلَط البناءُ بالإعراب"
            )

    @property
    def questions(self) -> tuple[AnalysisQuestion, ...]:
        """ما يُفحَص في هذه الدعوى؛ مشتقٌّ من محورها لا مكتوبٌ إلى جانبها."""

        if axis_of(self.category) in _MARKER_BEARING_AXES:
            return (
                AnalysisQuestion.CATEGORY,
                AnalysisQuestion.MARKER,
                AnalysisQuestion.EVIDENCE,
            )
        return (AnalysisQuestion.CATEGORY,)


def deposit_tokens() -> tuple[bytes, ...]:
    """كلماتُ الإيداع كما يقرؤها الخطّ؛ لا تُعاد كتابتُها في هذه الوحدة."""

    return tokens_from_text(FATIHA_SOURCE_TEXT)


@dataclass(frozen=True, slots=True)
class CoverageItem:
    """كلمةٌ من الإيداع بدعاواها المُعلَنة؛ وسطحُها مأخوذٌ لا مُعاد كتابته."""

    key: str
    token_index: int
    claims: tuple[CategoryClaim, ...]
    root_record: RootRecord
    why_it_is_here: str
    reference_address: ReferenceAddress

    def __post_init__(self) -> None:
        if not self.key.strip():
            raise ClassificationCoverageError("لكلّ كلمةٍ مفتاحٌ غيرُ فارغ")
        tokens = deposit_tokens()
        if not 0 <= self.token_index < len(tokens):
            raise ClassificationCoverageError(
                "موضعُ الكلمة يُحيل إلى الإيداع نفسِه، ولا يُكتَب سطحٌ من خارجه"
            )
        if not self.claims:
            raise ClassificationCoverageError("لا تدخل كلمةٌ الجدولَ بلا دعوى واحدة")
        axes = [axis_of(claim.category) for claim in self.claims]
        if len(set(axes)) != len(axes):
            raise ClassificationCoverageError(
                "لا تُنسَب كلمةٌ إلى فئتَين من محورٍ واحد؛ والمحاورُ تُقاس مفصولة"
            )
        if not self.why_it_is_here.strip():
            raise ClassificationCoverageError("لا تدخل كلمةٌ الجدولَ بلا سببٍ مكتوب")
        if not isinstance(self.reference_address, ReferenceAddress):
            raise ClassificationCoverageError(
                "لكلّ كلمةٍ عنوانٌ مُعلَنٌ في المرجع، ولا يُلتَمس موضعُها بالتخمين"
            )

    @property
    def raw_bytes(self) -> bytes:
        """بايتاتُ هذه الكلمة من الإيداع؛ مشتقّةٌ بالموضع لا منسوخةٌ باليد."""

        return deposit_tokens()[self.token_index]

    @property
    def surface(self) -> str:
        """سطحُ الكلمة؛ يُقرأ من بايتات الإيداع ولا يُكتَب إلى جانبها."""

        return self.raw_bytes.decode("utf-8")

    @property
    def categories(self) -> tuple[ClassificationCategory, ...]:
        return tuple(claim.category for claim in self.claims)


@dataclass(frozen=True, slots=True)
class AnalysisCheck:
    """فحصٌ تحليليٌّ واحد: أيُّ سؤالٍ، وفي أيّ فئة، وبأيّ حكم."""

    category: ClassificationCategory
    question: AnalysisQuestion
    outcome: AnalysisOutcome

    def __post_init__(self) -> None:
        if not isinstance(self.outcome, AnalysisOutcome):
            raise ClassificationCoverageError("حكمُ الفحص عضوٌ في مفردته المغلقة")
        if not isinstance(self.question, AnalysisQuestion):
            raise ClassificationCoverageError("سؤالُ الفحص عضوٌ في مفردته المغلقة")

    @property
    def is_resolved(self) -> bool:
        """أحُسِم الفحصُ؟ وغيرُ المحسوم لا يُعَدّ صحيحًا ولا يدخل المقسومَ عليه."""

        return self.outcome in (
            AnalysisOutcome.MATCHED_THE_REFERENCE,
            AnalysisOutcome.CONTRADICTED_THE_REFERENCE,
        )


@dataclass(frozen=True, slots=True)
class CoverageRow:
    """صفُّ كلمةٍ واحدة: أين وقفت كتابيًّا، وما فُحص من دعاواها تحليليًّا."""

    item: CoverageItem
    reached: RoundTripLayer
    outcome: LayerOutcome
    refusal: RoundTripRefusal | None
    checks: tuple[AnalysisCheck, ...]

    def __post_init__(self) -> None:
        if not self.checks:
            raise ClassificationCoverageError("صفٌّ بلا فحصٍ واحدٍ ليس صفَّ تغطية")

    @property
    def bytes_returned(self) -> bool:
        """أعادت الكلمةُ بايتاتها كما دخلت؟ مقروءٌ من التشغيل لا من دعوى."""

        return (
            self.reached is RoundTripLayer.FINAL_BYTES
            and self.outcome is LayerOutcome.RECONSTRUCTED
        )

    @property
    def failure_position(self) -> str:
        """موضعُ الفشل مستقلًّا: الطبقةُ التي وقفت عندها، وحكمُها، وسببُه."""

        if self.bytes_returned:
            return "—"
        reason = "" if self.refusal is None else f"/{self.refusal.value}"
        return f"{self.reached.value}/{self.outcome.value}{reason}"


@dataclass(frozen=True, slots=True)
class CategoryCoverage:
    """تغطيةُ فئةٍ واحدة: عددُ كلماتها، واسترجاعُها، وفحوصُها، وفشلُها."""

    category: ClassificationCategory
    rows: tuple[CoverageRow, ...]

    @property
    def axis(self) -> ClassificationAxis:
        return axis_of(self.category)

    @property
    def word_total(self) -> int:
        return len(self.rows)

    @property
    def returned_total(self) -> int:
        return sum(1 for row in self.rows if row.bytes_returned)

    @property
    def refused_total(self) -> int:
        return sum(1 for row in self.rows if row.outcome is LayerOutcome.REFUSED)

    @property
    def mismatched_total(self) -> int:
        return sum(1 for row in self.rows if row.outcome is LayerOutcome.MISMATCHED)

    @property
    def checks(self) -> tuple[AnalysisCheck, ...]:
        """فحوصُ هذه الفئة وحدَها؛ فحصُ فئةٍ أخرى لا يُحسَب ههنا."""

        return tuple(
            check
            for row in self.rows
            for check in row.checks
            if check.category is self.category
        )

    @property
    def resolved_total(self) -> int:
        return sum(1 for check in self.checks if check.is_resolved)

    @property
    def matched_total(self) -> int:
        return sum(
            1
            for check in self.checks
            if check.outcome is AnalysisOutcome.MATCHED_THE_REFERENCE
        )

    @property
    def unresolved_total(self) -> int:
        """الفحوصُ التي لم تُحسَم؛ تُعرَض ولا تُحسَب تصنيفًا صحيحًا."""

        return len(self.checks) - self.resolved_total

    @property
    def round_trip(self) -> float | None:
        """نسبةُ الاسترجاع؛ ممتنعةٌ في فئةٍ خاليةٍ ولا تُكتَب مئةً بالمئة."""

        if self.word_total == 0:
            return None
        return self.returned_total / self.word_total

    @property
    def analysis_accuracy(self) -> float | None:
        """دقّةُ التحليل؛ ممتنعةٌ ما لم يُحسَم فحصٌ واحدٌ بمرجعٍ مُودَع."""

        if self.resolved_total == 0:
            return None
        return self.matched_total / self.resolved_total

    @property
    def failure_positions(self) -> tuple[str, ...]:
        """مواضعُ الفشل في هذه الفئة؛ لكلّ فئةٍ موضعُها مستقلًّا."""

        return tuple(
            row.failure_position for row in self.rows if not row.bytes_returned
        )


@dataclass(frozen=True, slots=True)
class AxisReferenceRequirement:
    """ما يلزم من مرجعٍ مستقلٍّ ليُقاس محورٌ من المحاور الأربعة."""

    axis: ClassificationAxis
    question_the_axis_asks: str
    what_the_reference_must_supply: str

    def __post_init__(self) -> None:
        if not isinstance(self.axis, ClassificationAxis):
            raise ClassificationCoverageError("المحورُ عضوٌ في مفردته المغلقة")
        if not self.question_the_axis_asks.strip():
            raise ClassificationCoverageError("سؤالُ المحور يُكتَب ولا يُطوى")
        if not self.what_the_reference_must_supply.strip():
            raise ClassificationCoverageError("شرطُ المرجع يُكتَب ولا يُترَك فارغًا")


@dataclass(frozen=True, slots=True)
class AnalysisReference:
    """المرجعُ التحليليُّ المُسمّى: اسمُه، ومنزلتُه، وبصمتُه إن بُصِّم."""

    name: str
    standing: ReferenceStanding
    digest: str | None
    how_it_is_being_obtained: str

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ClassificationCoverageError("المرجعُ يُسمّى باسمه لا بوصفه")
        if not isinstance(self.standing, ReferenceStanding):
            raise ClassificationCoverageError("منزلةُ المرجع عضوٌ في مفردتها المغلقة")
        fingerprinted = self.standing in _FINGERPRINTED_STANDINGS
        if fingerprinted and not (self.digest and self.digest.strip()):
            raise ClassificationCoverageError("لا يُقال مُبصَّمٌ بلا بصمةٍ مكتوبة")
        if not fingerprinted and self.digest is not None:
            raise ClassificationCoverageError("بصمةٌ بلا بايتاتٍ مُبصَّمةٍ دعوى لم تقع")
        if not self.how_it_is_being_obtained.strip():
            raise ClassificationCoverageError("طريقُ تحصيل المرجع يُكتَب ولا يُطوى")

    @property
    def can_settle_an_analysis(self) -> bool:
        """أيصلح هذا المرجعُ لحسم فحص؟ لا يصلح حتى تُحَلَّ بايتاتُه وتُطابِق."""

        return self.standing is ReferenceStanding.DEPOSITED_AND_FINGERPRINTED


@dataclass(frozen=True, slots=True)
class CoverageReport:
    """تقريرُ التغطية: صفوفُ الكلمات، وتغطيةُ كلِّ فئةٍ من الإحدى عشرة."""

    rows: tuple[CoverageRow, ...]
    coverages: tuple[CategoryCoverage, ...]
    reference: AnalysisReference

    def __post_init__(self) -> None:
        if not self.rows:
            raise ClassificationCoverageError("تقريرٌ بلا صفٍّ واحدٍ ليس تقريرًا")
        keys = [row.item.key for row in self.rows]
        if len(set(keys)) != len(keys):
            raise ClassificationCoverageError("مفاتيحُ الجدول لا تتكرّر")
        listed = [coverage.category for coverage in self.coverages]
        if set(listed) != set(ClassificationCategory) or len(listed) != len(
            set(listed)
        ):
            raise ClassificationCoverageError(
                "كلُّ فئةٍ تُعرَض ولو خلت من الكلمات؛ والخاليةُ لا تُحذَف من الجدول"
            )

    def coverage(self, category: ClassificationCategory) -> CategoryCoverage:
        """تغطيةُ فئةٍ بعينها؛ وتُطلَب بعضوٍ مغلقٍ لا بنصٍّ حُرّ."""

        for coverage in self.coverages:
            if coverage.category is category:
                return coverage
        raise ClassificationCoverageError(f"لا صفَّ للفئة {category!r}")

    def axis_coverages(self, axis: ClassificationAxis) -> tuple[CategoryCoverage, ...]:
        """تغطياتُ محورٍ واحد؛ ولا تُخلَط بتغطيات محورٍ آخر."""

        if not isinstance(axis, ClassificationAxis):
            raise ClassificationCoverageError("المحورُ عضوٌ في مفردته المغلقة")
        return tuple(coverage for coverage in self.coverages if coverage.axis is axis)

    @property
    def word_total(self) -> int:
        return len(self.rows)

    @property
    def returned_total(self) -> int:
        return sum(1 for row in self.rows if row.bytes_returned)

    @property
    def unresolved_total(self) -> int:
        """كلُّ فحصٍ لم يُحسَم في التقرير؛ مشتقٌّ بالعدّ لا مكتوب."""

        return sum(
            1 for row in self.rows for check in row.checks if not check.is_resolved
        )

    @property
    def unresolved_by_cause(self) -> dict[AnalysisOutcome, int]:
        """الفحوصُ غيرُ المحسومة موزَّعةً على عللها؛ فالعلّةُ الواحدةُ لا تجمعها."""

        counts: dict[AnalysisOutcome, int] = {}
        for row in self.rows:
            for check in row.checks:
                if check.is_resolved:
                    continue
                counts[check.outcome] = counts.get(check.outcome, 0) + 1
        return counts

    @property
    def empty_categories(self) -> tuple[ClassificationCategory, ...]:
        """الفئاتُ الخاليةُ من الكلمات؛ وهي قياسُ ضيقِ هذا المجتمع لا عيبُه."""

        return tuple(
            coverage.category for coverage in self.coverages if coverage.word_total == 0
        )


ANALYSIS_REFERENCE: Final[AnalysisReference] = AnalysisReference(
    name="MASAQ",
    standing=ReferenceStanding.FINGERPRINTED_BUT_BYTES_NOT_RESOLVED,
    digest=MASAQ_SHA256,
    how_it_is_being_obtained=(
        "بصمةُ `MASAQ.csv` وطولُها مُودَعان في `masaq_corpus_deposit`، "
        "والبايتاتُ خارجَ الشجرة تُحَلُّ بـ`corpora/MASAQ.csv` أو "
        "بـ`ALGHANEM_MASAQ_PATH`؛ ولا يُقرأ منها رقمٌ قبل مطابقة الطول والبصمة"
    ),
)
"""المرجعُ التحليليُّ المكتوب؛ والمُعوَّلُ عليه ما تُخرِجه `masaq_reference()`."""


def masaq_reference(path: Path | str | None = None) -> AnalysisReference:
    """منزلةُ MASAQ **مشتقّةً بالتشغيل** على البايتات، لا مكتوبةً في حقل.

    ثلاثُ حالاتٍ تُفرَّق ولا تُجمَع: بايتاتٌ لا تُحَلّ، وبايتاتٌ حاضرةٌ خالفت
    البصمةَ أو الطول، وبايتاتٌ طابقت فصار حسمُ الفحص ممكنًا.
    """

    if not masaq_bytes_are_resolvable(path):
        return ANALYSIS_REFERENCE
    try:
        read_masaq_bytes(path)
    except MasaqDepositError as error:
        return AnalysisReference(
            name="MASAQ",
            standing=ReferenceStanding.BYTES_PRESENT_BUT_DIGEST_MISMATCHED,
            digest=MASAQ_SHA256,
            how_it_is_being_obtained=(f"حُلَّ مسارٌ إلى ملفٍّ موجودٍ وخالف المُودَع: {error}"),
        )
    return AnalysisReference(
        name="MASAQ",
        standing=ReferenceStanding.DEPOSITED_AND_FINGERPRINTED,
        digest=MASAQ_SHA256,
        how_it_is_being_obtained=(
            "حُلَّت البايتاتُ وطابقت الطولَ والبصمةَ المُودَعَين، فتُقرأ منها " "الوسومُ بقاعدتها"
        ),
    )


def settle_question(
    claim: CategoryClaim,
    question: AnalysisQuestion,
    item: CoverageItem,
    reference: AnalysisReference,
    records: tuple[dict[str, str], ...] | None,
) -> AnalysisOutcome:
    """احسم فحصًا واحدًا بالقراءة من المرجع، أو سمِّ علّةَ تعذُّرِ حسمه.

    والترتيبُ مقصود: ما يعجز عنه المرجعُ **في ذاته** يُقال قبل أن تُطلَب
    بايتاتُه، فلا يُحمَل عجزُ عمودٍ غائبٍ على غيابٍ عارضٍ للملفّ.
    """

    if question is AnalysisQuestion.MARKER:
        return AnalysisOutcome.UNRESOLVED_THE_REFERENCE_HAS_NO_COLUMN_FOR_THIS_QUESTION
    if question is AnalysisQuestion.EVIDENCE:
        return AnalysisOutcome.UNRESOLVED_THE_REFERENCE_HAS_NO_COLUMN_FOR_THIS_QUESTION
    tags = CATEGORY_TAGS.get(claim.category)
    if not tags:
        return AnalysisOutcome.UNRESOLVED_NO_ATTESTED_TAG_FOR_THIS_CATEGORY
    if not reference.can_settle_an_analysis or records is None:
        return AnalysisOutcome.UNRESOLVED_REFERENCE_BYTES_NOT_RESOLVED
    found = word_tags(records, item.reference_address, item.surface)
    if found is None:
        return AnalysisOutcome.UNRESOLVED_WORD_NOT_FOUND_IN_THE_REFERENCE
    if any(tag in tags for tag in found):
        return AnalysisOutcome.MATCHED_THE_REFERENCE
    return AnalysisOutcome.CONTRADICTED_THE_REFERENCE


AXIS_REFERENCE_REQUIREMENTS: Final[tuple[AxisReferenceRequirement, ...]] = (
    AxisReferenceRequirement(
        axis=ClassificationAxis.ORIGIN_AND_MORPHOLOGICAL_STRUCTURE,
        question_the_axis_asks=(
            "ما أصلُ الكلمة؟ وما نوعُ بنيتها؟ وهل الاشتقاقُ ثابتٌ بدليل؟"
        ),
        what_the_reference_must_supply=(
            "وصفُ بنيةٍ لكلّ كلمةٍ (جامدٌ أو مصدرٌ أو مشتقّ)، ومعه — حيث يُرخَّص — "
            "جذرٌ مُصرَّحٌ به، وتصريحٌ بما لا جذرَ له؛ ولا يُقبَل جذرٌ مُستنبَطٌ من "
            "الشكل المقيس نفسِه"
        ),
    ),
    AxisReferenceRequirement(
        axis=ClassificationAxis.GENERAL_IRAB_STANDING,
        question_the_axis_asks=("هل يلزم آخرُ الكلمة صورةً واحدة، أم يتغيّر بحسب العامل؟"),
        what_the_reference_must_supply=(
            "حكمُ بناءٍ أو إعرابٍ لكلّ كلمةٍ موضعًا موضعًا، لا قاعدةٌ عامّةٌ "
            "تُطبَّق، لأنّ الحكمَ ههنا سياقيٌّ لا صُوَريّ"
        ),
    ),
    AxisReferenceRequirement(
        axis=ClassificationAxis.BUILT_VERB_FORM,
        question_the_axis_asks="هل حدّد النظامُ نوعَ الفعل وعلامةَ بنائه؟",
        what_the_reference_must_supply=(
            "نوعُ الفعل المبنيّ وعلامةُ بنائه وسببُها، ومنها بناءُ المضارع في "
            "مواضعه؛ ولا يُقبَل حكمٌ بلا علامةٍ مُسمّاة"
        ),
    ),
    AxisReferenceRequirement(
        axis=ClassificationAxis.INFLECTED_VERB_CASE,
        question_the_axis_asks="هل حدّد النظامُ حالةَ الإعراب وعلامتَها ودليلَها؟",
        what_the_reference_must_supply=(
            "حالةُ المضارع (رفعٌ أو نصبٌ أو جزم) وعلامتُها والعاملُ الدالُّ "
            "عليها؛ والعاملُ دليلٌ لا زينةٌ في العبارة"
        ),
    ),
)
"""شرطُ القياس، محورًا محورًا؛ ولا يُقاس محورٌ بمرجعٍ لمحورٍ آخر."""


COVERAGE_ITEMS: Final[tuple[CoverageItem, ...]] = (
    CoverageItem(
        key="allathina",
        reference_address=ReferenceAddress(sura="1", verse="7"),
        token_index=21,
        claims=(
            CategoryClaim(
                category=ClassificationCategory.JAMID,
                declared_marker=None,
                declared_evidence=None,
            ),
            CategoryClaim(
                category=ClassificationCategory.MABNI,
                declared_marker="مبنيٌّ على الفتح",
                declared_evidence="اسمٌ موصولٌ يلزم آخرُه صورةً واحدة",
            ),
        ),
        root_record=RootRecord(
            standing=RootStanding.NOT_LICENSED_FOR_THIS_WORD,
            root=None,
            why="اسمٌ مبنيٌّ لا يُتاح له تحليلٌ جذريٌّ مُرخَّص، فلا يُنتزَع منه جذرٌ قسرًا",
        ),
        why_it_is_here=(
            "الموضعُ المطلوبُ اختبارُه: أتُحفَظ هويّتُها اسمًا موصولًا فلا تُقرأ "
            "«أل تعريف + ذين»؟"
        ),
    ),
    CoverageItem(
        key="ad_dallina",
        reference_address=ReferenceAddress(sura="1", verse="7"),
        token_index=28,
        claims=(
            CategoryClaim(
                category=ClassificationCategory.MUSHTAQQ,
                declared_marker=None,
                declared_evidence=None,
            ),
            CategoryClaim(
                category=ClassificationCategory.MURAB,
                declared_marker="مجرورٌ بالياء",
                declared_evidence="جمعُ مذكّرٍ سالمٌ مجرورٌ في هذا السياق",
            ),
        ),
        root_record=RootRecord(
            standing=RootStanding.AWAITING_THE_REFERENCE,
            root=None,
            why="مشتقٌّ يُتاح له تحليلٌ جذريّ، ولم يُقرأ جذرُه من مرجعٍ مُودَع",
        ),
        why_it_is_here="لامُها من لام التعريف، وهي الطرفُ الآخرُ في موضع الخلط",
    ),
    CoverageItem(
        key="ihdina",
        reference_address=ReferenceAddress(sura="1", verse="6"),
        token_index=17,
        claims=(
            CategoryClaim(
                category=ClassificationCategory.IMPERATIVE_VERB,
                declared_marker="مبنيٌّ على حذف حرف العلّة",
                declared_evidence="فعلُ أمرٍ معتلُّ الآخر، متّصلٌ بضمير",
            ),
            CategoryClaim(
                category=ClassificationCategory.MABNI,
                declared_marker="مبنيٌّ على حذف حرف العلّة",
                declared_evidence="الأمرُ مبنيٌّ لا يتغيّر آخرُه بالعامل",
            ),
        ),
        root_record=RootRecord(
            standing=RootStanding.AWAITING_THE_REFERENCE,
            root=None,
            why="فعلٌ يُتاح له تحليلٌ جذريّ، ولم يُقرأ جذرُه من مرجعٍ مُودَع",
        ),
        why_it_is_here="أمرٌ معتلٌّ متّصلٌ بضمير: نوعُ الفعل وعلامةُ بنائه معًا",
    ),
    CoverageItem(
        key="nabudu",
        reference_address=ReferenceAddress(sura="1", verse="5"),
        token_index=14,
        claims=(
            CategoryClaim(
                category=ClassificationCategory.PRESENT_MARFU,
                declared_marker="مرفوعٌ بالضمّة",
                declared_evidence="مضارعٌ لم يسبقه ناصبٌ ولا جازم",
            ),
            CategoryClaim(
                category=ClassificationCategory.MURAB,
                declared_marker="مرفوعٌ بالضمّة",
                declared_evidence="يتغيّر آخرُه بحسب العامل الداخل عليه",
            ),
        ),
        root_record=RootRecord(
            standing=RootStanding.AWAITING_THE_REFERENCE,
            root=None,
            why="فعلٌ يُتاح له تحليلٌ جذريّ، ولم يُقرأ جذرُه من مرجعٍ مُودَع",
        ),
        why_it_is_here="مضارعٌ مُعرَب: الحالةُ وعلامتُها ودليلُها ثلاثةُ فحوصٍ لا واحد",
    ),
    CoverageItem(
        key="anamta",
        reference_address=ReferenceAddress(sura="1", verse="7"),
        token_index=22,
        claims=(
            CategoryClaim(
                category=ClassificationCategory.PAST_VERB,
                declared_marker="مبنيٌّ على السكون",
                declared_evidence="اتّصلت به تاءُ الفاعل",
            ),
            CategoryClaim(
                category=ClassificationCategory.MABNI,
                declared_marker="مبنيٌّ على السكون",
                declared_evidence="الماضي مبنيٌّ لا يدخله عاملُ إعراب",
            ),
        ),
        root_record=RootRecord(
            standing=RootStanding.AWAITING_THE_REFERENCE,
            root=None,
            why="فعلٌ يُتاح له تحليلٌ جذريّ، ولم يُقرأ جذرُه من مرجعٍ مُودَع",
        ),
        why_it_is_here="ماضٍ اتّصلت به تاءُ الفاعل: البناءُ وعلامتُه وسببُها",
    ),
)
"""كلماتُ الجدول: خمسٌ من الإيداع، ودعاواها **أهدافُ اختبارٍ لا نتائج**."""


def run_coverage(
    items: tuple[CoverageItem, ...] = COVERAGE_ITEMS,
    reference: AnalysisReference | None = None,
    records: tuple[dict[str, str], ...] | None = None,
    path: Path | str | None = None,
) -> CoverageReport:
    """شغِّل التغطية: استرجاعٌ بالتشغيل، وفحوصٌ تُقرأ من MASAQ أو تُسمّى علّتُها.

    والمرجعُ إن لم يُمرَّر اشتُقَّت منزلتُه بالتشغيل على البايتات؛ والسجلّاتُ
    لا تُقرأ إلّا إذا صار المرجعُ حاسمًا، فلا تُفتَح بايتاتٌ لم تُطابَق.
    """

    if not items:
        raise ClassificationCoverageError("جدولٌ بلا كلمةٍ واحدةٍ لا يُشغَّل")
    resolved_reference = masaq_reference(path) if reference is None else reference
    resolved_records = records
    if resolved_reference.can_settle_an_analysis and resolved_records is None:
        resolved_records = masaq_records(read_masaq_bytes(path))
    rows: list[CoverageRow] = []
    for item in items:
        trace = run_token(item.raw_bytes)
        checks = tuple(
            AnalysisCheck(
                category=claim.category,
                question=question,
                outcome=settle_question(
                    claim, question, item, resolved_reference, resolved_records
                ),
            )
            for claim in item.claims
            for question in claim.questions
        )
        rows.append(
            CoverageRow(
                item=item,
                reached=trace.reached,
                outcome=trace.outcome,
                refusal=trace.refusal,
                checks=checks,
            )
        )
    coverages = tuple(
        CategoryCoverage(
            category=category,
            rows=tuple(row for row in rows if category in row.item.categories),
        )
        for category in ClassificationCategory
    )
    return CoverageReport(
        rows=tuple(rows), coverages=coverages, reference=resolved_reference
    )


def _rate(value: float | None) -> str:
    return "—" if value is None else f"{value * 100:.4f}%"


def render_coverage(report: CoverageReport) -> str:
    """اعرض التغطيةَ محورًا محورًا؛ ولا يُدمَج عمودُ الاسترجاع بعمود التحليل."""

    lines: list[str] = []
    for axis in ClassificationAxis:
        lines.append(axis.value)
        lines.append(
            f"  {'category':<20}{'words':>6}{'returned':>10}{'RoundTrip':>12}"
            f"{'REFUSED':>9}{'MISMATCH':>10}{'UNRESOLVED':>12}{'Accuracy':>10}"
        )
        for coverage in report.axis_coverages(axis):
            lines.append(
                f"  {coverage.category.value:<20}{coverage.word_total:>6}"
                f"{coverage.returned_total:>10}{_rate(coverage.round_trip):>12}"
                f"{coverage.refused_total:>9}{coverage.mismatched_total:>10}"
                f"{coverage.unresolved_total:>12}"
                f"{_rate(coverage.analysis_accuracy):>10}"
            )
        lines.append("")
    lines.append("failure positions, per category and independent:")
    for coverage in report.coverages:
        positions = coverage.failure_positions
        shown = "—" if not positions else " ".join(positions)
        lines.append(f"  {coverage.category.value:<20}{shown}")
    lines.append("")
    lines.append(
        f"words: {report.word_total}; bytes returned: {report.returned_total}"
        f"/{report.word_total}; unresolved analyses: {report.unresolved_total}"
    )
    lines.append(
        f"empty categories: {len(report.empty_categories)}/"
        f"{len(ClassificationCategory)} — مجتمعُ الفاتحة أضيقُ من هذه المعايير"
    )
    lines.append("unresolved analyses, by named cause:")
    for outcome, count in sorted(
        report.unresolved_by_cause.items(), key=lambda pair: pair[0].name
    ):
        lines.append(f"  {outcome.name:<52}{count:>4}")
    lines.append(
        f"analytic reference: {report.reference.name} "
        f"({report.reference.standing.value}) — "
        "ولا تُحسَب دقّةُ تحليلٍ قبل أن تُحَلَّ بايتاتُه وتُطابِق بصمتَه"
    )
    return "\n".join(lines)


THE_AXES_ARE_MEASURED_APART_NOT_MERGED_NOTE: Final[str] = (
    "TheAxesAreMeasuredApartNotMerged: المحاورُ أربعةٌ لكلٍّ منها عدّادُه وسؤالُه "
    "وموضعُ فشله، ولا تُنسَب كلمةٌ إلى فئتَين من محورٍ واحد؛ فلا يُخلَط أصلُ "
    "الكلمة ببنيتها، ولا البناءُ بالإعراب، ولا حالُ الفعل بحال الاسم"
)

ROOT_IS_NOT_A_CATEGORY_BESIDE_JAMID_AND_MASDAR_AND_MUSHTAQQ_NOTE: Final[str] = (
    "RootIsNotACategoryBesideJamidAndMasdarAndMushtaqq: الجذرُ أصلٌ صرفيٌّ "
    "محتمَل، والجامدُ والمصدرُ والمشتقُّ أوصافُ بنية؛ فلا عضوَ للجذر في مفردة "
    "الفئات، ويُسجَّل في `RootRecord` إلى جانب الوصف، ولا يُنتزَع من الحروف "
    "والأدوات والأسماء المبنيّة قسرًا"
)

A_MASDAR_IS_ITS_OWN_CATEGORY_WITHOUT_A_PRESUPPOSED_DERIVATION_NOTE: Final[str] = (
    "AMasdarIsItsOwnCategoryWithoutAPresupposedDerivation: المصدرُ فئةُ قياسٍ "
    "مستقلّة، ولا يُفترَض أنّ كلَّ مصدرٍ مشتقٌّ من فعل، ولا أنّ العلاقةَ بينهما "
    "محسومةٌ في كلّ حال"
)

A_DECLARED_TARGET_IS_NOT_A_RESULT_NOTE: Final[str] = (
    "ADeclaredTargetIsNotAResult: ما في `COVERAGE_ITEMS` من فئةٍ وعلامةٍ ودليلٍ "
    "هو المطلوبُ اختبارُه لا المُثبَت؛ ولا يُخرِج هذا الخطُّ تصنيفًا أصلًا، "
    "فالصرفُ والنحوُ خارجُ طبقاته"
)

AN_UNRESOLVED_ANALYSIS_IS_NOT_A_CORRECT_ONE_NOTE: Final[str] = (
    "AnUnresolvedAnalysisIsNotACorrectOne: الفحصُ غيرُ المحسوم لا يُعَدّ صحيحًا "
    "ولا يدخل مقسومَ `AnalysisAccuracy` عليه؛ فالدقّةُ ممتنعةٌ لا صفرٌ ولا واحد، "
    "وتُعرَض شرطةً باسم سببها"
)

THE_ANALYTIC_REFERENCE_IS_MASAQ_AND_ITS_STANDING_IS_RUN_NOT_WRITTEN_NOTE: Final[str] = (
    "TheAnalyticReferenceIsMasaqAndItsStandingIsRunNotWritten: المرجعُ "
    "التحليليُّ `MASAQ`، وبصمتُه مقروءةٌ من `masaq_corpus_deposit` لا منسوخةً "
    "باليد؛ ومنزلتُه تُشتَقُّ بتشغيل `masaq_reference()` على البايتات، فتُفرَّق "
    "ثلاثُ حالاتٍ لا تُجمَع: بايتاتٌ لا تُحَلّ، وبايتاتٌ حاضرةٌ خالفت البصمةَ، "
    "وبايتاتٌ طابقت فصار الحسمُ ممكنًا"
)

THE_REFERENCE_ANSWERS_ONE_QUESTION_OF_THREE_NOTE: Final[str] = (
    "TheReferenceAnswersOneQuestionOfThree: MASAQ تَسِم البنيةَ في عمود "
    f"«{MORPH_TAG_COLUMN}»، فتحسم سؤالَ الفئة حيث لها وَسْمٌ مُثبَتٌ ههنا. ولا "
    "عمودَ فيها لعلامة الإعراب على وجهها المطلوب ههنا ولا لدليلها، فسؤالا "
    "العلامة والدليل يخرجان `لا_عمودَ_في_المرجع_لهذا_السؤال` — وهي علّةٌ في "
    "المرجع لا في البايتات، فتُقال قبل أن تُطلَب البايتاتُ أصلًا"
)

A_TAGGED_SEGMENT_COUNT_IS_NOT_A_WORD_COUNT_NOR_AN_ACCURACY_NOTE: Final[str] = (
    "ATaggedSegmentCountIsNotAWordCountNorAnAccuracy: ٤٬٢١٦ بوَسْم `GERUND` "
    "و٣٬١٥٦ بوَسْم `NOUN_ACTIVE_PART` أعدادُ **سجلّاتٍ موسومة** في بايتات "
    "MASAQ تحت قاعدة عدّها؛ والسجلُّ مقطعٌ لا كلمة، فليست أعدادَ كلماتٍ "
    "فريدة، وليست بحالٍ نتيجةَ دقّةٍ للغانم: الغانمُ لم يُخرِج منها تصنيفًا "
    "واحدًا، وإنّما تُقارَن دعاواه بها"
)

AN_EMPTY_CATEGORY_HAS_NO_RATE_NOTE: Final[str] = (
    "AnEmptyCategoryHasNoRate: الفئةُ الخاليةُ تبقى صفًّا بصفرٍ ونسبتُها ممتنعة، "
    "ولا تُحذَف ولا تُكتَب مئةً بالمئة؛ وعددُ الفئات الخالية قياسٌ على أنّ "
    "المطلوب توسيعُ المدوّنة لا رفعُ نسبةٍ بلغت تمامها"
)
