"""قياسُ فرضية «المصدر أوّلًا» على صفوفٍ مقروءةٍ بربطٍ مُصرَّحٍ به، لا على ظنّ.

هذا تشغيلُ `masdar_priority_preregistration` لا تعديلٌ له: لا دعوى حُذفت، ولا
بذرةَ بُدِّلت، ولا وَسْمَ مصدرٍ أُضيف بعد الرقم. وكلُّ رقمٍ يخرج من هنا مربوطٌ
ببصمة التسجيل وببصمة ربط الأعمدة الذي خرج منه.

`THE_BYTES_WERE_NOT_OPENED_IN_THIS_TREE`: لم تُفتَح بايتاتُ `MASAQ.csv` في هذه
الشجرة ولم تُنسَخ إليها، ولم يصل طولُها ولا مسارُها ولا ربطُ أعمدتها. فليس في
هذه الوحدة **رقمٌ مُعادُ الاشتقاقِ واحد**: فيها أنبوبُ الاشتقاق وحارِسُه،
ومنزلتُها `لم_تُفتَح_البايتات` مُعلَنةً لا مطويّة. ومن قرأ منها رقمًا قرأ ما
لم يُقَس.

`A_HUMAN_TAG_IS_NOT_A_MEASUREMENT`: وَسْمُ `GERUND` و`GERUND_MEEM` تبويبُ
مُوسِّمين بشرٍ لا خاصّيّةٌ تُقاس من البايتات؛ فغيابُ وَسْمٍ غيابُ تبويبٍ في
هذه المدوَّنة لا غيابُ صيغةٍ في العربية، على منوال
`A_TAGGED_ROOT_IS_A_HUMAN_JUDGEMENT_NOT_A_MEASUREMENT` في
`transitivity_corpus_census`.

`ONE_ROOT_IS_NOT_A_CORPUS`: «قوم» جذرٌ واحد، والنتيجةُ الواردةُ مبنيّةٌ عليه
وحدَه؛ فهي **شاهدُ إمكانٍ** لا معدَّلُ مدوَّنة. ودعوى «المصدر يُميِّز الوزن»
تُقاس على الجذور كلِّها أو لا تُقاس، ولذلك يُخرِج هذا الأنبوبُ جدولَ الجذور
كلِّها ويُفرِد «قوم» شاهدًا مُسمًّى لا رقمًا عامًّا.

`A_PRESENT_MASDAR_IS_NOT_A_MEASURED_TRANSITIVITY`: الدعوى (ج) موقوفةٌ بمانعَي
`LEGISLATION_BARRIERS`؛ وكلُّ دالّةٍ هنا تُفضي إليها ترفع خطأً باسم المانع ولا
تُخرِج رقمًا. ورفعُ المانع تسجيلٌ قبْليٌّ آخرُ لا سطرٌ يُكتَب في وحدة قياس.

`ABSENCE_IN_A_CORPUS_IS_NOT_IMPOSSIBILITY`: صفرُ مجهولِ «أقام» غيابٌ في مدوَّنةٍ
محدودة لا امتناعٌ في العربية؛ وهو التحفّظُ نفسُه المقبولُ في نتيجة الأمر
والمضارع، فيُطبَّق هنا بالسويّة لا بانتقاء.

وهذه الوحدة تسجيلٌ لا سلطة: لا ولادةَ فيها، ولا حكمَ ولادة، ولا تجميدَ `E0`،
ولا تستورد من `kernel/` شيئًا، ولا تقرؤها وحدةٌ فيه.
"""

from __future__ import annotations

import random
from collections.abc import Iterable
from dataclasses import dataclass
from enum import Enum
from typing import Final, NoReturn

from .masaq_corpus_witness import (
    MasaqColumnBinding,
    MasaqSegmentRow,
    binding_digest,
)
from .masdar_priority_preregistration import (
    ARRIVING_MASDAR_FIGURES,
    LEGISLATION_BARRIERS,
    MASDAR_PERMUTATION_PROTOCOL,
    MASDAR_PRIORITY_PREREGISTRATION_DIGEST,
    ArrivingMasdarFigure,
    MasdarCountingRule,
    preregistration_digest,
)

__all__ = [
    "ABSENCE_IN_A_CORPUS_IS_NOT_IMPOSSIBILITY_NOTE",
    "A_HUMAN_TAG_IS_NOT_A_MEASUREMENT_NOTE",
    "A_PRESENT_MASDAR_IS_NOT_A_MEASURED_TRANSITIVITY_NOTE",
    "CENSUS_STANDING",
    "MASDAR_CENSUS_NAMED_RESIDUALS",
    "ONE_ROOT_IS_NOT_A_CORPUS_NOTE",
    "REDERIVED_FIGURES",
    "THE_BYTES_WERE_NOT_OPENED_IN_THIS_TREE_NOTE",
    "UNTAGGED_FORM_LABEL",
    "CensusStanding",
    "DiscriminationTable",
    "MasdarPriorityCensusError",
    "MasdarRecord",
    "PermutationOutcome",
    "RootMasdarProfile",
    "arriving_figures_without_a_rederivation",
    "discrimination_table",
    "masdar_records",
    "permutation_test",
    "root_profiles",
    "single_root_witness",
    "transitivity_from_masdar",
]


class MasdarPriorityCensusError(ValueError):
    """تُرفَع حين يُقرأ صفٌّ أو يُطلَب رقمٌ قراءةً لا يُعاد بها اشتقاقُه."""


THE_BYTES_WERE_NOT_OPENED_IN_THIS_TREE_NOTE: Final[str] = (
    "TheBytesWereNotOpenedInThisTree: لم تُفتَح بايتاتُ MASAQ في هذه الشجرة، "
    "فليس في هذه الوحدة رقمٌ مُعادُ الاشتقاق؛ فيها أنبوبُه وحارسُه، ومن قرأ "
    "منها رقمًا قرأ ما لم يُقَس"
)

A_HUMAN_TAG_IS_NOT_A_MEASUREMENT_NOTE: Final[str] = (
    "AHumanTagIsNotAMeasurement: `GERUND` و`GERUND_MEEM` تبويبُ مُوسِّمين "
    "بشرٍ لا خاصّيّةٌ تُقاس من البايتات؛ فغيابُ الوَسْم غيابُ تبويبٍ في هذه "
    "المدوَّنة لا غيابُ صيغةٍ في العربية"
)

ONE_ROOT_IS_NOT_A_CORPUS_NOTE: Final[str] = (
    "OneRootIsNotACorpus: «قوم» جذرٌ واحدٌ والنتيجةُ الواردةُ مبنيّةٌ عليه "
    "وحدَه، فهي شاهدُ إمكانٍ لا معدَّلُ مدوَّنة؛ ودعوى التمييز تُقاس على "
    "الجذور كلِّها أو لا تُقاس"
)

A_PRESENT_MASDAR_IS_NOT_A_MEASURED_TRANSITIVITY_NOTE: Final[str] = (
    "APresentMasdarIsNotAMeasuredTransitivity: وجودُ «إقامة» يُثبِت وَسْمَ "
    "مصدرٍ لا تعدّيًا؛ والانتقالُ بينهما استنتاجٌ لا قياس ما لم تُجمَّد قاعدةُ "
    "الربط، فالدعوى (ج) بلا رقمٍ هنا"
)

ABSENCE_IN_A_CORPUS_IS_NOT_IMPOSSIBILITY_NOTE: Final[str] = (
    "AbsenceInACorpusIsNotImpossibility: صفرُ مجهولِ «أقام» غيابٌ في مدوَّنةٍ "
    "محدودةٍ لا امتناعٌ في العربية؛ وهو التحفّظُ نفسُه المقبولُ في نتيجة "
    "المضارع والأمر، فيُطبَّق بالسويّة"
)

MASDAR_CENSUS_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "TheBytesWereNotOpenedInThisTree": THE_BYTES_WERE_NOT_OPENED_IN_THIS_TREE_NOTE,
    "AHumanTagIsNotAMeasurement": A_HUMAN_TAG_IS_NOT_A_MEASUREMENT_NOTE,
    "OneRootIsNotACorpus": ONE_ROOT_IS_NOT_A_CORPUS_NOTE,
    "APresentMasdarIsNotAMeasuredTransitivity": (
        A_PRESENT_MASDAR_IS_NOT_A_MEASURED_TRANSITIVITY_NOTE
    ),
    "AbsenceInACorpusIsNotImpossibility": (
        ABSENCE_IN_A_CORPUS_IS_NOT_IMPOSSIBILITY_NOTE
    ),
}


class CensusStanding(Enum):
    """منزلةُ هذا القياس؛ والقيمةُ الأقوى معلنةٌ ليُرى أنّ هذه ليست إيّاها."""

    REDERIVED_FROM_FINGERPRINTED_BYTES = "مُعادُ_الاشتقاق_من_بايتاتٍ_مُبصَّمة"
    BYTES_NOT_OPENED = "لم_تُفتَح_البايتات"


CENSUS_STANDING: Final[CensusStanding] = CensusStanding.BYTES_NOT_OPENED
"""منزلةُ هذا القياس اليوم؛ وتبديلُها لا يقع إلّا بفتح البايتات وإيداع الشاهد."""


UNTAGGED_FORM_LABEL: Final[str] = "بلا_وزنٍ_موسوم"
"""بابُ ما لم يُوسَم له وزن؛ ولا يُنسَب إلى وزنٍ ولا يُطرَح ليستقيم رقم."""


@dataclass(frozen=True, slots=True)
class MasdarRecord:
    """مقطعٌ موسومٌ مصدرًا: جذرُه ومدخلُه ووزنُه ووَسْمُه، كما وُسِمت لا كما تُقرأ."""

    location: str
    root: str
    lemma: str
    form: str
    verb_form: str
    morphological_tag: str

    def __post_init__(self) -> None:
        for value, label in (
            (self.location, "موضعُ المقطع"),
            (self.root, "جذرُ المقطع"),
            (self.lemma, "مدخلُ المقطع"),
            (self.morphological_tag, "وَسْمُ المقطع"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise MasdarPriorityCensusError(
                    f"{label} نصٌّ غير فارغ؛ ولا يُخمَّن ولا يُتخطّى صامتًا."
                )


def masdar_records(
    rows: Iterable[MasaqSegmentRow], binding: MasaqColumnBinding
) -> tuple[MasdarRecord, ...]:
    """المقاطعُ الموسومةُ مصدرًا وحدَها، بالوسوم المُصرَّح بها في الربط.

    وصفٌّ موسومٌ مصدرًا بلا وَسْمِ جذرٍ **يُترَك خارج العدّ ويُسمّى**: لا
    يُخمَّن له جذر، ولا يُحمَل على أقرب جذرٍ إليه.
    """

    records: list[MasdarRecord] = []
    for row in rows:
        if not row.is_masdar(binding):
            continue
        if not row.root.strip():
            continue
        records.append(
            MasdarRecord(
                location=row.location,
                root=row.root,
                lemma=row.lemma if row.lemma.strip() else row.form,
                form=row.form,
                verb_form=(
                    row.verb_form if row.verb_form.strip() else UNTAGGED_FORM_LABEL
                ),
                morphological_tag=row.morphological_tag,
            )
        )
    return tuple(records)


@dataclass(frozen=True, slots=True)
class RootMasdarProfile:
    """ملفُّ جذرٍ واحد: مصادرُه المتمايزة، وأوزانُ كلِّ مصدرٍ كما وُسِمت."""

    root: str
    lemmas: tuple[str, ...]
    forms_by_lemma: tuple[tuple[str, tuple[str, ...]], ...]

    @property
    def distinct_masdar_count(self) -> int:
        """عددُ المصادر المتمايزة في هذا الجذر؛ والقاعدةُ `DISTINCT_MASDAR_LEMMAS`."""

        return len(self.lemmas)


def root_profiles(
    records: Iterable[MasdarRecord],
) -> tuple[RootMasdarProfile, ...]:
    """ملفُّ كلِّ جذرٍ ذي مصدر، مرتَّبًا بترتيب نقاط يونيكود لا بترتيب ورودٍ."""

    by_root: dict[str, dict[str, set[str]]] = {}
    for record in records:
        lemmas = by_root.setdefault(record.root, {})
        lemmas.setdefault(record.lemma, set()).add(record.verb_form)
    profiles: list[RootMasdarProfile] = []
    for root in sorted(by_root):
        lemmas = by_root[root]
        ordered = tuple(sorted(lemmas))
        profiles.append(
            RootMasdarProfile(
                root=root,
                lemmas=ordered,
                forms_by_lemma=tuple(
                    (lemma, tuple(sorted(lemmas[lemma]))) for lemma in ordered
                ),
            )
        )
    return tuple(profiles)


@dataclass(frozen=True, slots=True)
class DiscriminationTable:
    """قوّةُ تمييز المصدر للوزن: الفاصلُ والمشترَكُ معًا، لا الفاصلُ وحدَه."""

    masdar_roots: int
    roots_with_more_than_one_masdar: int
    distinct_masdars: int
    masdars_with_a_tagged_form: int
    masdars_separating_one_form: int
    masdars_shared_between_forms: int
    binding_digest: str
    preregistration_digest: str

    def __post_init__(self) -> None:
        if (
            self.masdars_separating_one_form + self.masdars_shared_between_forms
            != self.masdars_with_a_tagged_form
        ):
            raise MasdarPriorityCensusError(
                "الفاصلُ والمشترَكُ يستوعبان كلَّ مصدرٍ موسومِ الوزن؛ وتركُ "
                "مصدرٍ خارجَهما انتقاء."
            )
        if self.masdars_with_a_tagged_form > self.distinct_masdars:
            raise MasdarPriorityCensusError(
                "موسومُ الوزن لا يزيد على المصادر المتمايزة؛ والزيادةُ عدٌّ مكرَّر."
            )
        if self.roots_with_more_than_one_masdar > self.masdar_roots:
            raise MasdarPriorityCensusError(
                "ذواتُ المصدرين لا تزيد على ذوات المصدر؛ والزيادةُ عدٌّ مكرَّر."
            )

    @property
    def separation_rate(self) -> float:
        """نسبةُ ما فصل وزنًا واحدًا؛ ومقامُها موسومُ الوزن لا كلُّ المصادر."""

        if self.masdars_with_a_tagged_form == 0:
            return 0.0
        return (
            100.0 * self.masdars_separating_one_form / self.masdars_with_a_tagged_form
        )


def discrimination_table(
    records: Iterable[MasdarRecord], binding: MasaqColumnBinding
) -> DiscriminationTable:
    """جدولُ الدعوى (أ): كم مصدرًا فصل وزنًا واحدًا، وكم اشترك بين وزنين.

    والمصدرُ الذي لم يُوسَم له وزنٌ البتّة يخرج من مقام النسبة ولا يُعَدّ
    فاصلًا ولا مشترَكًا: عدُّه في أحدهما يجعل غيابَ الوَسْم نتيجةً.
    """

    materialised = tuple(records)
    forms_by_lemma: dict[str, set[str]] = {}
    roots: set[str] = set()
    lemmas_by_root: dict[str, set[str]] = {}
    for record in materialised:
        roots.add(record.root)
        lemmas_by_root.setdefault(record.root, set()).add(record.lemma)
        forms_by_lemma.setdefault(record.lemma, set()).add(record.verb_form)
    tagged = 0
    separating = 0
    shared = 0
    for forms in forms_by_lemma.values():
        declared = {form for form in forms if form != UNTAGGED_FORM_LABEL}
        if not declared:
            continue
        tagged += 1
        if len(declared) == 1:
            separating += 1
        else:
            shared += 1
    return DiscriminationTable(
        masdar_roots=len(roots),
        roots_with_more_than_one_masdar=sum(
            1 for lemmas in lemmas_by_root.values() if len(lemmas) > 1
        ),
        distinct_masdars=len(forms_by_lemma),
        masdars_with_a_tagged_form=tagged,
        masdars_separating_one_form=separating,
        masdars_shared_between_forms=shared,
        binding_digest=binding_digest(binding),
        preregistration_digest=MASDAR_PRIORITY_PREREGISTRATION_DIGEST,
    )


@dataclass(frozen=True, slots=True)
class PermutationOutcome:
    """مُخرَجُ اختبار التبديل كاملًا: الإحصاءةُ والمتجاوزاتُ والاحتمالُ وأقصى العدميّ."""

    label: str
    sample_size: int
    observed_rate: float
    at_least_as_extreme: int
    p_value: float
    maximum_null_rate: float

    def __post_init__(self) -> None:
        if self.p_value <= 0.0:
            raise MasdarPriorityCensusError(
                "احتمالُ التبديل لا يبلغ صفرًا بحكم صيغته؛ وأرضيتُه "
                f"{MASDAR_PERMUTATION_PROTOCOL.p_value_floor:.4f}."
            )


def permutation_test(records: Iterable[MasdarRecord], label: str) -> PermutationOutcome:
    """اختبارُ الدعوى (أ) تحت البروتوكول المُجمَّد ببذرته وعدد تبديلاته.

    والعدميُّ يُبنى بتبديل **أوزانِ المقاطع** بينها مع تثبيت المصادر
    وتوزيعِ المقاطع عليها؛ فالمقيسُ هو أنّ اقترانَ المصدر بوزنه ليس توزيعًا
    عشوائيًّا على المصادر بالأحجام نفسِها.
    """

    materialised = [
        record for record in records if record.verb_form != UNTAGGED_FORM_LABEL
    ]
    if not materialised:
        raise MasdarPriorityCensusError(
            "لا مقطعَ موسومَ الوزن؛ ولا يُشغَّل اختبارٌ على مجموعةٍ خالية."
        )
    lemmas = [record.lemma for record in materialised]
    forms = [record.verb_form for record in materialised]

    def separation_rate(assignment: list[str]) -> float:
        grouped: dict[str, set[str]] = {}
        for lemma, form in zip(lemmas, assignment, strict=True):
            grouped.setdefault(lemma, set()).add(form)
        separating = sum(1 for values in grouped.values() if len(values) == 1)
        return 100.0 * separating / len(grouped)

    observed = separation_rate(forms)
    generator = random.Random(MASDAR_PERMUTATION_PROTOCOL.seed)
    shuffled = list(forms)
    at_least_as_extreme = 0
    maximum_null = 0.0
    for _ in range(MASDAR_PERMUTATION_PROTOCOL.permutations):
        generator.shuffle(shuffled)
        rate = separation_rate(shuffled)
        maximum_null = max(maximum_null, rate)
        if rate >= observed:
            at_least_as_extreme += 1
    p_value = (1 + at_least_as_extreme) / (1 + MASDAR_PERMUTATION_PROTOCOL.permutations)
    return PermutationOutcome(
        label=label,
        sample_size=len(materialised),
        observed_rate=observed,
        at_least_as_extreme=at_least_as_extreme,
        p_value=p_value,
        maximum_null_rate=maximum_null,
    )


def single_root_witness(
    records: Iterable[MasdarRecord], root: str
) -> RootMasdarProfile:
    """شاهدُ جذرٍ واحدٍ مُسمًّى — «قوم» في النصّ الوارد — لا رقمٌ عامّ.

    ويُقرأ بحدِّه المكتوب في `ONE_ROOT_IS_NOT_A_CORPUS_NOTE`: شاهدُ إمكانٍ
    لا معدَّلُ مدوَّنة.
    """

    for profile in root_profiles(records):
        if profile.root == root:
            return profile
    raise MasdarPriorityCensusError(
        f"لا مصدرَ موسومًا لجذر «{root}» في الصفوف المقروءة؛ ولا يُختلَق شاهدٌ له. "
        + A_HUMAN_TAG_IS_NOT_A_MEASUREMENT_NOTE
    )


def transitivity_from_masdar(root: str) -> NoReturn:
    """الدعوى (ج) لا رقمَ لها هنا: ترفع هذه الدالّةُ خطأً باسم مانعها.

    وهي مكتوبةٌ لتُرفَع لا لتُحسَب: من طلب الرقمَ وجد المانعَ بنصّه بدل أن
    يجد صمتًا يملؤه بتقدير.
    """

    barrier = LEGISLATION_BARRIERS[1]
    raise MasdarPriorityCensusError(
        f"لا يُخرَج رقمُ تعدٍّ لجذر «{root}» من وَسْمِ مصدر: "
        f"{barrier.the_rule_that_is_missing}. "
        + A_PRESENT_MASDAR_IS_NOT_A_MEASURED_TRANSITIVITY_NOTE
        + " "
        + ABSENCE_IN_A_CORPUS_IS_NOT_IMPOSSIBILITY_NOTE
    )


REDERIVED_FIGURES: Final[tuple[str, ...]] = ()
"""لا رقمَ مُعادَ الاشتقاقِ واحدًا؛ والفراغُ مُصرَّحٌ به لا مُستنتَج.

والبقاءُ على الفراغ حتّى تُفتَح البايتاتُ المُبصَّمة هو عينُ
`THE_BYTES_WERE_NOT_OPENED_IN_THIS_TREE_NOTE`.
"""


def arriving_figures_without_a_rederivation() -> tuple[ArrivingMasdarFigure, ...]:
    """الأرقامُ الواردةُ التي لم يُعَد اشتقاقُ واحدٍ منها بعد؛ وهي كلُّها."""

    return ARRIVING_MASDAR_FIGURES


def _assert_the_preregistration_is_the_frozen_one() -> None:
    current = preregistration_digest()
    if current != MASDAR_PRIORITY_PREREGISTRATION_DIGEST:
        raise MasdarPriorityCensusError(
            f"بصمةُ التسجيل {current} لا تطابق المُجمَّدة "
            f"{MASDAR_PRIORITY_PREREGISTRATION_DIGEST}؛ فلا يُبنى قياسٌ على "
            "تسجيلٍ بُدِّل بعد تجميده."
        )


def _assert_every_arriving_figure_names_its_rule() -> None:
    for figure in ARRIVING_MASDAR_FIGURES:
        if not isinstance(figure.counting_rule, MasdarCountingRule):
            raise MasdarPriorityCensusError(
                f"الرقمُ الوارِدُ «{figure.label}» بلا قاعدةِ عدٍّ مُسمّاة."
            )


_assert_the_preregistration_is_the_frozen_one()
_assert_every_arriving_figure_names_its_rule()
