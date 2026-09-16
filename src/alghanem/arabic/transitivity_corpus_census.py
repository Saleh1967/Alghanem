"""قياسُ اللزوم والتعدّي على مدوَّنةٍ مُبصَّمة: تقسيمٌ بقواعده، واختبارٌ ببروتوكوله.

**ما تفعله هذه الوحدة**: تقرأ وسومَ الأفعال والمشتقّات في
`QURANIC_ARABIC_CORPUS_WITNESS` بعد مطابقة بصمتها وطولها، فتقسم الجذورَ ذواتِ
الماضي المجرَّد المعلوم قسمين بالقاعدة المُجمَّدة في
`transitivity_probe_preregistration`، ثمّ تُعيد اشتقاقَ أربع نتائجَ بأرقامها
واختبارَي تبديلٍ ببروتوكولهما. ولا أكثر: لا تُصدِر حكمًا نحويًّا على جذر، ولا
تُعرِّف اللزومَ في العربية.

`THE_ARRIVING_NUMBERS_DID_NOT_MATCH_AND_THE_RULE_WAS_NOT_TUNED`: الأرقامُ
الواردةُ في `ARRIVING_FIGURES` **خالفت** ما خرج من التشغيل على البايتات
المُبصَّمة: ١٬٦٤٢ جذرًا موسومًا لا ١٬٥٣٢، و٣٩٨ ذاتَ ماضٍ مجرَّدٍ معلومٍ لا ٣٧٩،
و٦٨/٣٣٠ لا ٦٧/٣١٢، و٤٨/٣٤ لا ٤٦/٣٥. والقاعدةُ **لم تُعدَّل حتى تُطابق**:
يُسجَّل الفرقُ في `ARRIVING_FIGURE_DIVERGENCES` ويُعرَض، على منوال ما يشترطه
`THE_NUMBERS_ARRIVED_BEFORE_THE_RUN` في `hollow_root_root_census` حين قال «ولو
لم تُطابق لوجب تسجيلُ الفرق». فالوارِدُ **غيرُ مُعادِ الاشتقاق** بهذه القواعد،
ولا تُقرأ أرقامُه من هذه الشجرة.

`THE_DIRECTION_SURVIVED_THE_NUMBERS`: ما طابق ليس الأعدادَ بل **اتّجاهَ
النتيجتين الثالثة والرابعة**: فارقُ اسم المفعول بقي كبيرًا ودالًّا (٢٧٫١٥ نقطةً،
`p = 1/5001`)، وفرضيةُ «اللازم يصير متعدّيًا بالتزيّد» بقيت مُفنَّدةً كقاعدةٍ
عامّة (١٣٫٣٪ مقابل ١٤٫٧٪، `p ≈ 0.85`). واتّفاقُ الاتّجاه مع اختلاف الأعداد
يُسمّى بحدّه: تأييدٌ نوعيٌّ لا إعادةُ اشتقاقٍ كمّيّة.

`THE_MAXIMUM_NULL_GAP_IS_NOT_THE_P_VALUE`: في اسم الفاعل خرج الفارقُ المرصود
٢١٫٠٧ نقطةً **دون** أقصى فارقٍ عدميٍّ (٢٤٫٦٢) ومع ذلك `p = 0.0012`. فمعيارُ
«تجاوزِ أقصى الفارق العدميّ» الذي جاء في النصّ الوارد يُسقِط فرقًا دالًّا،
وهذه واقعةٌ في هذا القياس بعينه لا اعتراضٌ نظريّ.

`THE_INDICATOR_AND_ITS_TEST_SHARE_A_PARENT`: المجموعتان عُرِّفتا بحضور المجهول
المجرَّد وغيابه، واسمُ المفعول صيغةٌ مجهولة؛ فدلالةُ فارقه **ليست شاهدًا
مستقلًّا** عن التعريف. وهذا التحفّظُ مكتوبٌ في التسجيل القبْليّ قبل الرقم.

`ONE_TENSE_IS_NOT_THE_VOICE_OF_THE_ROOT`: ثمانيةٌ وأربعون جذرًا لها مضارعٌ
مجهولٌ مجرَّدٌ بلا ماضٍ مجهولٍ مجرَّد، مقابل أربعةٍ وثلاثين لها الزمنان — فأكثرُ
من نصف ما يظهر فيه المجهولُ المجرَّد يظهر في زمنٍ واحد. ولذلك **تُقرأ مجموعةُ
«المرشَّح اللازم» بحدّها**: هي مُعرَّفةٌ بالماضي وحده كما وصلت الفرضية، وفيها
جذورٌ لها مضارعٌ مجهولٌ مجرَّدٌ فعلًا (`Elm` منها).

`A_TAGGED_ROOT_IS_A_HUMAN_JUDGEMENT_NOT_A_MEASUREMENT`: خانةُ `ROOT` ووسومُ
الوزن والبناء تبويبُ مُوسِّمين لا خواصُّ تُقاس من البايتات؛ فغيابُ وَسْمٍ غيابُ
تبويبٍ في هذه المدوَّنة لا غيابُ صيغةٍ في العربية.

`A_COUNT_IN_A_CORPUS_IS_NOT_A_COUNT_IN_ARABIC`: كلُّ عددٍ هنا دالّةٌ في هذه
المدوَّنة وإصدارها وقاعدة عدّها معًا؛ واستنفادُ مدوَّنةٍ ليس استنفادَ لغة.

`WITNESS_BYTES_ARE_STILL_NOT_VENDORED`: لم تُنسَخ بايتاتُ المدوَّنة إلى الشجرة؛
والقياسُ يقع عند حائزها بـ`examples/irab/measure_transitivity_census.py`، ولا
يمرّ رقمٌ قبل مطابقة البصمة والطول.

`THIS_IS_REGISTRATION_NOT_AUTHORITY`: لا ولادةَ هنا، ولا حكمَ ولادة، ولا تجميدَ
`E0`، ولا استيرادَ من `kernel/`.

المصدر: مدوَّنة القرآن الصرفية، http://corpus.quran.com — مبنيّةٌ على نصّ
تنزيل، http://tanzil.info. والإسنادُ إليهما شرطُ رخصةٍ لا لطفَ عبارة.
"""

from __future__ import annotations

import random
import re
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from enum import Enum
from typing import Final

from .hollow_root_root_census import (
    FEATURE_SEPARATOR,
    SegmentRecord,
    root_of_features,
)
from .transitivity_probe_preregistration import (
    ARRIVING_FIGURES,
    PERMUTATION_PROTOCOL,
    ArrivingFigure,
    TransitivityClass,
)

__all__ = [
    "ARRIVING_FIGURE_DIVERGENCES",
    "A_COUNT_IN_A_CORPUS_IS_NOT_A_COUNT_IN_ARABIC_NOTE",
    "A_TAGGED_ROOT_IS_A_HUMAN_JUDGEMENT_NOT_A_MEASUREMENT_NOTE",
    "AUGMENTED_PASSIVE_EXAMPLES",
    "FORM_TAG_PATTERN",
    "ONE_TENSE_IS_NOT_THE_VOICE_OF_THE_ROOT_NOTE",
    "REDERIVED_ACTIVE_PARTICIPLE_TEST",
    "REDERIVED_AUGMENTED_PASSIVE_TEST",
    "REDERIVED_BARE_PERFECT_ACTIVE_ROOTS",
    "REDERIVED_CONFIRMED_TRANSITIVE",
    "REDERIVED_INTRANSITIVE_CANDIDATES",
    "REDERIVED_PARTICIPLE_RATES",
    "REDERIVED_PASSIVE_PARTICIPLE_TEST",
    "REDERIVED_TAGGED_ROOTS",
    "REDERIVED_TENSE_SPLIT",
    "REDERIVED_VERB_TAGGED_ROOTS",
    "THE_ARRIVING_NUMBERS_DID_NOT_MATCH_AND_THE_RULE_WAS_NOT_TUNED_NOTE",
    "THE_DIRECTION_SURVIVED_THE_NUMBERS_NOTE",
    "THE_INDICATOR_AND_ITS_TEST_SHARE_A_PARENT_NOTE",
    "THE_MAXIMUM_NULL_GAP_IS_NOT_THE_P_VALUE_NOTE",
    "THIS_IS_REGISTRATION_NOT_AUTHORITY_NOTE",
    "TRANSITIVITY_CENSUS_NAMED_RESIDUALS",
    "WITNESS_BYTES_ARE_STILL_NOT_VENDORED_NOTE",
    "ArrivingFigureDivergence",
    "AugmentedPassiveExample",
    "ParticipleRates",
    "PermutationOutcome",
    "RootProfile",
    "SegmentReading",
    "TenseSplit",
    "Tense",
    "TransitivityCensusError",
    "TransitivityPartition",
    "Voice",
    "arriving_figure_divergences",
    "participle_rates",
    "partition_roots",
    "permutation_test",
    "read_segment",
    "root_profiles",
    "tense_split",
]


class TransitivityCensusError(ValueError):
    """رفضٌ صريح: سمةٌ خارج المخطَّط المُعلَن، أو مجموعةٌ فارغةٌ تُقسَّم إليها نسبة."""


FORM_TAG_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"^\((I|II|III|IV|V|VI|VII|VIII|IX|X|XI|XII)\)$"
)
"""وَسْمُ الوزن كما هو في السمات؛ والوزنُ الأوّل لا يُوسَم فيُقرأ من غيابه."""

_POS_PREFIX: Final[str] = "POS:"
_VERB_POS: Final[str] = "V"
_PARTICIPLE_FEATURE: Final[str] = "PCPL"
_PASSIVE_FEATURE: Final[str] = "PASS"
_ACTIVE_FEATURE: Final[str] = "ACT"


class Tense(Enum):
    """أزمنةُ الفعل الثلاثةُ كما تَسِمها المدوَّنة؛ ولا رابعَ لها فيها."""

    PERFECT = "PERF"
    IMPERFECT = "IMPF"
    IMPERATIVE = "IMPV"


class Voice(Enum):
    """بناءُ الفعل. والمعلومُ **غيابُ** `PASS` لا حضورُ `ACT` في خانة الأفعال."""

    ACTIVE = "ACT"
    PASSIVE = "PASS"


THE_ARRIVING_NUMBERS_DID_NOT_MATCH_AND_THE_RULE_WAS_NOT_TUNED_NOTE: Final[str] = (
    "TheArrivingNumbersDidNotMatchAndTheRuleWasNotTuned: خالفت الأرقامُ "
    "الواردةُ ما خرج من التشغيل على البايتات المُبصَّمة، فسُجِّل الفرقُ ولم "
    "تُعدَّل القاعدةُ حتى تُطابق؛ والوارِدُ غيرُ مُعادِ الاشتقاق بهذه القواعد"
)

THE_DIRECTION_SURVIVED_THE_NUMBERS_NOTE: Final[str] = (
    "TheDirectionSurvivedTheNumbers: طابق اتّجاهُ النتيجتين الثالثة والرابعة "
    "دون أعدادهما؛ وهذا تأييدٌ نوعيٌّ لا إعادةُ اشتقاقٍ كمّيّة، ولا يُقرأ "
    "تصديقًا للأرقام الواردة"
)

THE_MAXIMUM_NULL_GAP_IS_NOT_THE_P_VALUE_NOTE: Final[str] = (
    "TheMaximumNullGapIsNotThePValue: خرج فارقُ اسم الفاعل دون أقصى الفارق "
    "العدميّ وهو دالٌّ بـ p = 0.0012؛ فمعيارُ «تجاوز أقصى الفارق العدميّ» "
    "يُسقِط فرقًا دالًّا، وهذه واقعةٌ في هذا القياس لا اعتراضٌ نظريّ"
)

THE_INDICATOR_AND_ITS_TEST_SHARE_A_PARENT_NOTE: Final[str] = (
    "TheIndicatorAndItsTestShareAParent: اسمُ المفعول صيغةٌ مجهولة "
    "والمجموعتان عُرِّفتا بحضور المجهول وغيابه؛ فدلالةُ فارقه ليست شاهدًا "
    "مستقلًّا عن تعريف المجموعتين"
)

ONE_TENSE_IS_NOT_THE_VOICE_OF_THE_ROOT_NOTE: Final[str] = (
    "OneTenseIsNotTheVoiceOfTheRoot: أكثرُ ما يظهر فيه المجهولُ المجرَّدُ "
    "يظهر في زمنٍ واحدٍ لا في الزمنين، فمجموعةُ «المرشَّح اللازم» المُعرَّفةُ "
    "بالماضي وحده تضمّ جذورًا لها مضارعٌ مجهولٌ مجرَّدٌ فعلًا"
)

A_TAGGED_ROOT_IS_A_HUMAN_JUDGEMENT_NOT_A_MEASUREMENT_NOTE: Final[str] = (
    "ATaggedRootIsAHumanJudgementNotAMeasurement: خانةُ ROOT ووسومُ الوزن "
    "والبناء تبويبُ مُوسِّمين لا خواصُّ تُقاس؛ فغيابُ الوَسْم غيابُ تبويبٍ "
    "في هذه المدوَّنة لا غيابُ صيغةٍ في العربية"
)

A_COUNT_IN_A_CORPUS_IS_NOT_A_COUNT_IN_ARABIC_NOTE: Final[str] = (
    "ACountInACorpusIsNotACountInArabic: العددُ دالّةٌ في المدوَّنة وإصدارها "
    "وقاعدة عدّها معًا؛ واستنفادُ مدوَّنةٍ ليس استنفادَ لغة"
)

WITNESS_BYTES_ARE_STILL_NOT_VENDORED_NOTE: Final[str] = (
    "WitnessBytesAreStillNotVendored: بايتاتُ المدوَّنة لم تُنسَخ إلى الشجرة؛ "
    "والقياسُ يقع عند حائزها بعد مطابقة البصمة والطول، ولا يمرّ رقمٌ قبلها"
)

THIS_IS_REGISTRATION_NOT_AUTHORITY_NOTE: Final[str] = (
    "ThisIsRegistrationNotAuthority: لا ولادةَ هنا ولا حكمَ ولادة ولا تجميدَ "
    "E0 ولا استيرادَ من kernel؛ ولا يُصدَر بهذه الوحدة حكمٌ نحويٌّ على جذر"
)

TRANSITIVITY_CENSUS_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "TheArrivingNumbersDidNotMatchAndTheRuleWasNotTuned": (
        THE_ARRIVING_NUMBERS_DID_NOT_MATCH_AND_THE_RULE_WAS_NOT_TUNED_NOTE
    ),
    "TheDirectionSurvivedTheNumbers": THE_DIRECTION_SURVIVED_THE_NUMBERS_NOTE,
    "TheMaximumNullGapIsNotThePValue": THE_MAXIMUM_NULL_GAP_IS_NOT_THE_P_VALUE_NOTE,
    "TheIndicatorAndItsTestShareAParent": (
        THE_INDICATOR_AND_ITS_TEST_SHARE_A_PARENT_NOTE
    ),
    "OneTenseIsNotTheVoiceOfTheRoot": ONE_TENSE_IS_NOT_THE_VOICE_OF_THE_ROOT_NOTE,
    "ATaggedRootIsAHumanJudgementNotAMeasurement": (
        A_TAGGED_ROOT_IS_A_HUMAN_JUDGEMENT_NOT_A_MEASUREMENT_NOTE
    ),
    "ACountInACorpusIsNotACountInArabic": (
        A_COUNT_IN_A_CORPUS_IS_NOT_A_COUNT_IN_ARABIC_NOTE
    ),
    "WitnessBytesAreStillNotVendored": WITNESS_BYTES_ARE_STILL_NOT_VENDORED_NOTE,
    "ThisIsRegistrationNotAuthority": THIS_IS_REGISTRATION_NOT_AUTHORITY_NOTE,
}


@dataclass(frozen=True, slots=True)
class SegmentReading:
    """قراءةُ مقطعٍ موسومٍ بجذر: وَسْمُه ووزنُه وزمنُه وبناؤه، بلا تأويل."""

    root: str
    part_of_speech: str
    form: str | None
    tense: Tense | None
    voice: Voice
    is_participle: bool

    @property
    def is_bare(self) -> bool:
        """المجرَّدُ: غيابُ وَسْمِ الوزن. والوزنُ الأوّل لا يُوسَم في هذه المدوَّنة."""

        return self.form is None

    @property
    def is_verb(self) -> bool:
        return self.part_of_speech == _VERB_POS


def read_segment(record: SegmentRecord) -> SegmentReading | None:
    """يقرأ مقطعًا: `None` إن لم يُوسَم له جذر، ورفضٌ لوَسْمِ وزنٍ مكرَّر.

    والبناءُ يُقرأ بغياب `PASS` لا بحضور `ACT`: الأفعالُ المعلومةُ في هذه
    المدوَّنة لا تحمل `ACT` أصلًا، ومن اشترط حضورَه خرج بصفرٍ يُقرأ «لا فعلَ
    معلومًا في القرآن».
    """

    root = root_of_features(record.features)
    if root is None:
        return None
    part_of_speech = ""
    form: str | None = None
    tense: Tense | None = None
    voice = Voice.ACTIVE
    is_participle = False
    for feature in record.features.split(FEATURE_SEPARATOR):
        if feature.startswith(_POS_PREFIX):
            part_of_speech = feature[len(_POS_PREFIX) :]
        elif FORM_TAG_PATTERN.match(feature):
            if form is not None:
                raise TransitivityCensusError(
                    f"مقطعٌ بوَسْمَي وزنٍ في {record.location}؛ ولا يُرجَّح أحدُهما."
                )
            form = feature[1:-1]
        elif feature in (item.value for item in Tense):
            tense = Tense(feature)
        elif feature == _PASSIVE_FEATURE:
            voice = Voice.PASSIVE
        elif feature == _ACTIVE_FEATURE:
            voice = Voice.ACTIVE
        elif feature == _PARTICIPLE_FEATURE:
            is_participle = True
    if not part_of_speech:
        raise TransitivityCensusError(
            f"مقطعٌ بجذرٍ بلا وَسْمِ POS في {record.location}؛ ولا يُحمَل على أقربه."
        )
    return SegmentReading(
        root=root,
        part_of_speech=part_of_speech,
        form=form,
        tense=tense,
        voice=voice,
        is_participle=is_participle,
    )


@dataclass(frozen=True, slots=True)
class RootProfile:
    """ملفُّ جذرٍ واحد: أزمنتُه وأبنيتُه مجرَّدةً ومزيدة، ومشتقّاته الوصفية."""

    root: str
    bare_verb_shapes: frozenset[tuple[Tense, Voice]]
    augmented_verb_shapes: frozenset[tuple[Tense, Voice, str]]
    participle_voices: frozenset[Voice]

    def has_bare(self, tense: Tense, voice: Voice) -> bool:
        return (tense, voice) in self.bare_verb_shapes

    def has_augmented_passive(self) -> bool:
        """أله مجهولٌ في وزنٍ مزيد؟ وهو محكُّ فرضية «التعدّي بالتزيّد»."""

        return any(voice is Voice.PASSIVE for _, voice, _ in self.augmented_verb_shapes)

    def augmented_passive_forms(self) -> tuple[str, ...]:
        return tuple(
            sorted(
                {
                    form
                    for _, voice, form in self.augmented_verb_shapes
                    if voice is Voice.PASSIVE
                }
            )
        )

    def has_participle(self, voice: Voice) -> bool:
        return voice in self.participle_voices


def root_profiles(records: Iterable[SegmentRecord]) -> dict[str, RootProfile]:
    """يبني ملفَّ كلّ جذرٍ موسومٍ في المقاطع الممرَّرة، بقاعدة `TAGGED_ROOTS`."""

    bare: dict[str, set[tuple[Tense, Voice]]] = {}
    augmented: dict[str, set[tuple[Tense, Voice, str]]] = {}
    participles: dict[str, set[Voice]] = {}
    for record in records:
        reading = read_segment(record)
        if reading is None:
            continue
        bare.setdefault(reading.root, set())
        augmented.setdefault(reading.root, set())
        participles.setdefault(reading.root, set())
        if reading.is_verb and reading.tense is not None:
            if reading.form is None:
                bare[reading.root].add((reading.tense, reading.voice))
            else:
                augmented[reading.root].add(
                    (reading.tense, reading.voice, reading.form)
                )
        if reading.is_participle:
            participles[reading.root].add(reading.voice)
    return {
        root: RootProfile(
            root=root,
            bare_verb_shapes=frozenset(bare[root]),
            augmented_verb_shapes=frozenset(augmented[root]),
            participle_voices=frozenset(participles[root]),
        )
        for root in sorted(bare)
    }


@dataclass(frozen=True, slots=True)
class TransitivityPartition:
    """قسمَا المجال بأعيان جذورهما، مرتَّبَين ترتيبًا ثابتًا لا بترتيب القراءة."""

    confirmed_transitive: tuple[str, ...]
    intransitive_candidates: tuple[str, ...]

    def __post_init__(self) -> None:
        overlap = set(self.confirmed_transitive) & set(self.intransitive_candidates)
        if overlap:
            raise TransitivityCensusError(
                f"جذرٌ في القسمين معًا: {sorted(overlap)[0]}؛ والقسمان متمانعان."
            )

    def roots_of(self, transitivity_class: TransitivityClass) -> tuple[str, ...]:
        if transitivity_class is TransitivityClass.CONFIRMED_TRANSITIVE:
            return self.confirmed_transitive
        return self.intransitive_candidates


def partition_roots(profiles: Mapping[str, RootProfile]) -> TransitivityPartition:
    """يقسم الجذورَ ذواتِ الماضي المجرَّد المعلوم بالقاعدة المُجمَّدة قبل القياس."""

    transitive: list[str] = []
    intransitive: list[str] = []
    for root in sorted(profiles):
        profile = profiles[root]
        if not profile.has_bare(Tense.PERFECT, Voice.ACTIVE):
            continue
        if profile.has_bare(Tense.PERFECT, Voice.PASSIVE):
            transitive.append(root)
        else:
            intransitive.append(root)
    return TransitivityPartition(
        confirmed_transitive=tuple(transitive),
        intransitive_candidates=tuple(intransitive),
    )


@dataclass(frozen=True, slots=True)
class TenseSplit:
    """ربطُ المجهول المجرَّد بين الزمنين: أفي الزمنين معًا أم في أحدهما؟"""

    imperfect_passive_only: int
    both_tenses_passive: int
    perfect_passive_only: int

    def __post_init__(self) -> None:
        for count, label in (
            (self.imperfect_passive_only, "المضارعُ وحده"),
            (self.both_tenses_passive, "الزمنان معًا"),
            (self.perfect_passive_only, "الماضي وحده"),
        ):
            if count < 0:
                raise TransitivityCensusError(f"{label} عددٌ غيرُ سالب.")


def tense_split(profiles: Mapping[str, RootProfile]) -> TenseSplit:
    """يعدّ الجذورَ بحسب الزمن الذي وقع فيه المجهولُ المجرَّد، بقاعدة الجذور."""

    imperfect_only = 0
    both = 0
    perfect_only = 0
    for profile in profiles.values():
        has_perfect = profile.has_bare(Tense.PERFECT, Voice.PASSIVE)
        has_imperfect = profile.has_bare(Tense.IMPERFECT, Voice.PASSIVE)
        if has_imperfect and has_perfect:
            both += 1
        elif has_imperfect:
            imperfect_only += 1
        elif has_perfect:
            perfect_only += 1
    return TenseSplit(
        imperfect_passive_only=imperfect_only,
        both_tenses_passive=both,
        perfect_passive_only=perfect_only,
    )


@dataclass(frozen=True, slots=True)
class ParticipleRates:
    """نسبةُ حَمَلة اسم الفاعل واسم المفعول في مجموعةٍ مُسمّاة، مع عدديهما."""

    transitivity_class: TransitivityClass
    group_size: int
    active_participle_roots: int
    passive_participle_roots: int

    def __post_init__(self) -> None:
        if self.group_size < 1:
            raise TransitivityCensusError(
                "مجموعةٌ فارغةٌ لا تُقسَّم إليها نسبة؛ والقسمةُ على صفرٍ ليست صفرًا."
            )
        for count, label in (
            (self.active_participle_roots, "حَمَلةُ اسم الفاعل"),
            (self.passive_participle_roots, "حَمَلةُ اسم المفعول"),
        ):
            if not 0 <= count <= self.group_size:
                raise TransitivityCensusError(f"{label} عددٌ ضمن حجم المجموعة.")

    @property
    def active_percentage(self) -> float:
        return 100 * self.active_participle_roots / self.group_size

    @property
    def passive_percentage(self) -> float:
        return 100 * self.passive_participle_roots / self.group_size


def participle_rates(
    profiles: Mapping[str, RootProfile],
    roots: Iterable[str],
    transitivity_class: TransitivityClass,
) -> ParticipleRates:
    """نسبتا المشتقَّين في مجموعةٍ من الجذور، بقاعدة عدِّ الجذور لا المقاطع."""

    members = tuple(roots)
    active = sum(1 for root in members if profiles[root].has_participle(Voice.ACTIVE))
    passive = sum(1 for root in members if profiles[root].has_participle(Voice.PASSIVE))
    return ParticipleRates(
        transitivity_class=transitivity_class,
        group_size=len(members),
        active_participle_roots=active,
        passive_participle_roots=passive,
    )


@dataclass(frozen=True, slots=True)
class PermutationOutcome:
    """نتيجةُ اختبار تبديلٍ واحد ببروتوكوله كاملًا؛ ولا تُقرأ بمعزلٍ عنه."""

    label: str
    observed_gap_points: float
    maximum_null_gap_points: float
    at_least_as_extreme: int
    permutations: int
    seed: int

    def __post_init__(self) -> None:
        if not self.label.strip():
            raise TransitivityCensusError("لكلّ اختبارٍ اسمٌ يُميّزه.")
        if self.permutations < 1:
            raise TransitivityCensusError("عددُ التباديل عددٌ موجب.")
        if not 0 <= self.at_least_as_extreme <= self.permutations:
            raise TransitivityCensusError("عددُ المتجاوزات ضمن عدد التباديل.")

    @property
    def p_value(self) -> float:
        """`p` بصيغتها المُجمَّدة؛ ولا تبلغ صفرًا ولو لم يتجاوزها تبديلٌ واحد."""

        return (1 + self.at_least_as_extreme) / (1 + self.permutations)


def permutation_test(
    label: str,
    group_a: Iterable[bool],
    group_b: Iterable[bool],
    seed: int = PERMUTATION_PROTOCOL.seed,
    permutations: int = PERMUTATION_PROTOCOL.permutations,
) -> PermutationOutcome:
    """اختبارُ تبديلٍ حتميٌّ ببذرةٍ مُعلَنة؛ فتشغيلان ببذرةٍ واحدةٍ يتطابقان."""

    first = [1 if value else 0 for value in group_a]
    second = [1 if value else 0 for value in group_b]
    if not first or not second:
        raise TransitivityCensusError("مجموعةٌ فارغةٌ لا يقع عليها اختبارُ فرق.")
    size = len(first)
    observed = abs(sum(first) / size - sum(second) / len(second)) * 100
    pool = first + second
    generator = random.Random(seed)
    maximum = 0.0
    extreme = 0
    for _ in range(permutations):
        generator.shuffle(pool)
        gap = abs(sum(pool[:size]) / size - sum(pool[size:]) / (len(pool) - size)) * 100
        maximum = max(maximum, gap)
        if gap >= observed - 1e-12:
            extreme += 1
    return PermutationOutcome(
        label=label,
        observed_gap_points=round(observed, 2),
        maximum_null_gap_points=round(maximum, 2),
        at_least_as_extreme=extreme,
        permutations=permutations,
        seed=seed,
    )


REDERIVED_TAGGED_ROOTS: Final[int] = 1_642
"""جذورٌ موسومةٌ متمايزة، بقاعدة `TAGGED_ROOTS`؛ منها ٤٠ رباعيًّا و١٬٦٠٢ ثلاثيًّا."""

REDERIVED_VERB_TAGGED_ROOTS: Final[int] = 943
"""جذورٌ وردت في فعلٍ موسومٍ بزمن، بقاعدة `VERB_TAGGED_ROOTS`."""

REDERIVED_BARE_PERFECT_ACTIVE_ROOTS: Final[int] = 398
"""جذورٌ لها ماضٍ مجرَّدٌ معلوم؛ وهي مجالُ التقسيم كلِّه."""

REDERIVED_CONFIRMED_TRANSITIVE: Final[int] = 68
"""متعدٍّ مؤكَّد: له مجهولٌ مجرَّدٌ في الماضي أيضًا."""

REDERIVED_INTRANSITIVE_CANDIDATES: Final[int] = 330
"""مرشَّحٌ لازم: لا مجهولَ مجرَّدَ له في الماضي البتّة في هذه المدوَّنة."""

REDERIVED_TENSE_SPLIT: Final[TenseSplit] = TenseSplit(
    imperfect_passive_only=48,
    both_tenses_passive=34,
    perfect_passive_only=59,
)
"""النتيجةُ الثانيةُ بأعدادها: المضارعُ وحده ٤٨، والزمنان ٣٤، والماضي وحده ٥٩.

فأكثرُ من نصف ما يظهر فيه المجهولُ المجرَّدُ يظهر في زمنٍ واحد؛ والعددُ الثالث
(٥٩) لم يكن في الوارد أصلًا، وإيداعُه لازمٌ لأنّ عددين من ثلاثةٍ يُوهِمان
استيفاءَ التقسيم.
"""

REDERIVED_PARTICIPLE_RATES: Final[tuple[ParticipleRates, ...]] = (
    ParticipleRates(
        transitivity_class=TransitivityClass.CONFIRMED_TRANSITIVE,
        group_size=68,
        active_participle_roots=44,
        passive_participle_roots=30,
    ),
    ParticipleRates(
        transitivity_class=TransitivityClass.INTRANSITIVE_CANDIDATE,
        group_size=330,
        active_participle_roots=144,
        passive_participle_roots=56,
    ),
)
"""٦٤٫٧٪ و٤٤٫١٪ في المتعدّي، و٤٣٫٦٪ و١٧٫٠٪ في المرشَّح اللازم؛ بقاعدة الجذور."""

REDERIVED_PASSIVE_PARTICIPLE_TEST: Final[PermutationOutcome] = PermutationOutcome(
    label="فارقُ اسم المفعول بين القسمين",
    observed_gap_points=27.15,
    maximum_null_gap_points=20.05,
    at_least_as_extreme=0,
    permutations=5_000,
    seed=20_260_916,
)
"""دالٌّ بحدّ البروتوكول: `p = 1/5001`، ولم يبلغه تبديلٌ واحدٌ من خمسة آلاف.

و`TheIndicatorAndItsTestShareAParent` باقٍ: الدلالةُ دلالةُ تقاربِ مؤشّرين
مشتركَي الأصل، لا شاهدٌ مستقلٌّ عن تعريف المجموعتين.
"""

REDERIVED_ACTIVE_PARTICIPLE_TEST: Final[PermutationOutcome] = PermutationOutcome(
    label="فارقُ اسم الفاعل بين القسمين",
    observed_gap_points=21.07,
    maximum_null_gap_points=24.62,
    at_least_as_extreme=5,
    permutations=5_000,
    seed=20_260_916,
)
"""`p = 6/5001 ≈ 0.0012` مع بقاء الفارق **دون** أقصى الفارق العدميّ ٢٤٫٦٢.

وهذه هي الواقعةُ التي يُسمّيها `TheMaximumNullGapIsNotThePValue`.
"""

REDERIVED_AUGMENTED_PASSIVE_TEST: Final[PermutationOutcome] = PermutationOutcome(
    label="فارقُ المجهول المزيد بين القسمين",
    observed_gap_points=1.37,
    maximum_null_gap_points=15.56,
    at_least_as_extreme=4_248,
    permutations=5_000,
    seed=20_260_916,
)
"""`p ≈ 0.85`: لا فرقَ دالًّا. فالتزيّدُ لا يُحوِّل اللازمَ أكثرَ من المتعدّي.

٤٤ من ٣٣٠ في المرشَّح اللازم (١٣٫٣٪) مقابل ١٠ من ٦٨ في المتعدّي (١٤٫٧٪)؛
فالفرضيةُ مُفنَّدةٌ قاعدةً عامّةً من وجهين: لا هي الأغلبية، ولا هي فارقٌ بين
القسمين. وبقاؤها **إمكانًا** يُثبته وقوعُها في جذورٍ بأعيانها.
"""


@dataclass(frozen=True, slots=True)
class AugmentedPassiveExample:
    """مثالٌ مرصودٌ بموضعه: جذرٌ مرشَّحٌ لازمٌ له مجهولٌ في وزنٍ مزيد."""

    root_buckwalter: str
    root_arabic: str
    form: str
    location: str
    surface_buckwalter: str

    def __post_init__(self) -> None:
        for text, label in (
            (self.root_buckwalter, "الجذرُ بترميز Buckwalter"),
            (self.root_arabic, "الجذرُ بالعربية"),
            (self.form, "الوزن"),
            (self.location, "الموضع"),
            (self.surface_buckwalter, "الصورة"),
        ):
            if not text.strip():
                raise TransitivityCensusError(f"{label} نصٌّ غير فارغ.")


AUGMENTED_PASSIVE_EXAMPLES: Final[tuple[AugmentedPassiveExample, ...]] = (
    AugmentedPassiveExample(
        root_buckwalter="Elm",
        root_arabic="علم",
        form="II",
        location="(6:91:31:2)",
        surface_buckwalter="Eul~imo",
    ),
    AugmentedPassiveExample(
        root_buckwalter="Ewd",
        root_arabic="عود",
        form="IV",
        location="(22:22:8:1)",
        surface_buckwalter=">uEiydu",
    ),
    AugmentedPassiveExample(
        root_buckwalter="HfZ",
        root_arabic="حفظ",
        form="X",
        location="(5:44:17:1)",
        surface_buckwalter="{sotuHofiZu",
    ),
)
"""الأمثلةُ الثلاثةُ التي وصلت مُسمّاةً، مُعادةَ الاشتقاق بمواضعها من البايتات.

وهي **إمكانٌ مرصودٌ لا قاعدة**: الأربعةُ والأربعون كلُّها أقلّيةٌ في ثلاثمئةٍ
وثلاثين. و`Elm` منها شاهدٌ على `OneTenseIsNotTheVoiceOfTheRoot`: له مضارعٌ
مجهولٌ **مجرَّد** في هذه المدوَّنة، ومع ذلك وقع في «المرشَّح اللازم» لأنّ
التعريفَ الوارد بُني على الماضي وحده.
"""


@dataclass(frozen=True, slots=True)
class ArrivingFigureDivergence:
    """فرقٌ بين رقمٍ وارِدٍ ورقمٍ مُعادِ الاشتقاق، مُسجَّلًا بلا تعديلِ قاعدة."""

    figure: ArrivingFigure
    rederived_value: str

    def __post_init__(self) -> None:
        if not self.rederived_value.strip():
            raise TransitivityCensusError("القيمةُ المُعادُ اشتقاقُها نصٌّ غير فارغ.")

    @property
    def matched(self) -> bool:
        return self.figure.claimed_value == self.rederived_value


ARRIVING_FIGURE_DIVERGENCES: Final[tuple[ArrivingFigureDivergence, ...]] = (
    ArrivingFigureDivergence(figure=ARRIVING_FIGURES[0], rederived_value="1642"),
    ArrivingFigureDivergence(figure=ARRIVING_FIGURES[1], rederived_value="398"),
    ArrivingFigureDivergence(figure=ARRIVING_FIGURES[2], rederived_value="68"),
    ArrivingFigureDivergence(figure=ARRIVING_FIGURES[3], rederived_value="330"),
    ArrivingFigureDivergence(figure=ARRIVING_FIGURES[4], rederived_value="48"),
    ArrivingFigureDivergence(figure=ARRIVING_FIGURES[5], rederived_value="34"),
    ArrivingFigureDivergence(figure=ARRIVING_FIGURES[6], rederived_value="64.7"),
    ArrivingFigureDivergence(figure=ARRIVING_FIGURES[7], rederived_value="44.1"),
    ArrivingFigureDivergence(figure=ARRIVING_FIGURES[8], rederived_value="43.6"),
    ArrivingFigureDivergence(figure=ARRIVING_FIGURES[9], rederived_value="17.0"),
    ArrivingFigureDivergence(figure=ARRIVING_FIGURES[10], rederived_value="27.15"),
    ArrivingFigureDivergence(figure=ARRIVING_FIGURES[11], rederived_value="20.05"),
    ArrivingFigureDivergence(figure=ARRIVING_FIGURES[12], rederived_value="44"),
    ArrivingFigureDivergence(figure=ARRIVING_FIGURES[13], rederived_value="13.3"),
    ArrivingFigureDivergence(figure=ARRIVING_FIGURES[14], rederived_value="14.7"),
)
"""الخمسةَ عشرَ رقمًا الواردةَ بإزاء نظائرها المُعادةِ الاشتقاق: **ولا واحدَ طابق**.

فالنصُّ الوارد لا يُعاد اشتقاقُ أرقامه من هذه البايتات بهذه القواعد؛ وما بقي
منه هو الاتّجاهُ وحده (`TheDirectionSurvivedTheNumbers`). واحتمالُ أن يكون
الفرقُ ناشئًا عن قواعدَ أخرى غيرِ مُصرَّحٍ بها في الوارد قائمٌ ولا يُحسَم من
هنا: قاعدةٌ غيرُ مُعلَنةٍ لا تُعاد بالتخمين.
"""


def arriving_figure_divergences() -> tuple[ArrivingFigureDivergence, ...]:
    """الفروقُ المُودَعة؛ ودالّةٌ لا حقلٌ كي تُقرأ عرضًا لا سلطةً على رقم."""

    return ARRIVING_FIGURE_DIVERGENCES
