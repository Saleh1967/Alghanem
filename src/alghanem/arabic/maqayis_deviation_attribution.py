"""فصلُ ثلاثةِ تفاسيرَ للانحراف الموزَّع، بالبايتات القائمة لا بالترجيح.

أثبت `maqayis_chapter_census` أنّ فرقَ نصيبِ الشاهد الشعريّ موزَّعٌ على الأبواب
لا شاذٌّ ببابٍ منها، وسُمّي حينئذٍ أنّ ذلك ينفي تفسيرًا ولا يُثبِت بديلًا،
وأنّ ثلاثةً بقيت غيرَ مفصولة. وهذه الوحدة تفصلها بقياسٍ يُجرى لكلٍّ منها
على حدة، وتفصل معها::

    ASpreadDeviation      != AnExplainedDeviation
    ASmallChapterIsNoisy  != TheNoiseExplainsTheExcess
    AContaminantIsPresent != TheContaminantIsSufficient
    AResidualAccount      != AMeasuredCause

**والمقياسُ الثلاثةُ ليست متكافئةً في نوع دليلها، وذلك مُعلَنٌ قبل النتيجة.**
للعدّة نموذجُ عدمٍ يُبنى من الجدول نفسِه، فتُختبَر اختبارًا. وللاستخراج أثرٌ
يُقاس بمِسبارين لا يمسّان عمودَ الشاهد. وأمّا تفاوتُ التأليف فلا مِسبارَ له
ههنا البتّة: ليس في البايتات ما يشهد لعادةِ ابن فارس مستقلًّا عن هذا الاستخراج
نفسِه. فهو **بقيّةٌ تُسمّى بعد المِسبارين لا سببٌ يُقاس**، ومن قرأه مُثبَتًا
فقد رقّى بقيّةً إلى دعوى (`A_RESIDUAL_IS_NOT_A_MEASURED_CAUSE`).

**المِسبارُ الأوّل — العدّة.** لكلّ بابٍ عدّتُه `n`، فيُسحَب من الجدول كلِّه
`n` مدخلًا بلا إبدال مرارًا، ويُقرأ فرقُ نصيبِ الشاهد في كلّ سحبة. فما وقع
فرقُه المرصودُ فوق المئينِ الخامسِ والتسعين من سحباته فذلك فائضٌ لا تفسّره
العدّة. **والنتيجةُ تنقض العدّةَ تفسيرًا**: الفائضُ يتركّز في الأبواب الكبيرة
حيث نموذجُ العدم ضيّقٌ جدًّا، وأصغرُ الأبواب — حيث يُتوقَّع الضجيجُ أعلاه —
يكاد لا يتجاوزه. فالعدّةُ تُضخّم الفروقَ ولا تلد الفائض
(`SIZE_INFLATES_THE_GAPS_AND_DOES_NOT_PRODUCE_THE_EXCESS`).

**المِسبارُ الثاني — الاستخراج، بشاهدَين لا يمسّان عمودَ الشاهد الشعريّ.**
أوّلُهما صورةُ الترويسة: تُصنَّف بقاعدةٍ مُعلَنةٍ قبل القياس إلى كتابِ حرفٍ،
وبابٍ، وفاسدةٍ ليست ترويسةَ بابٍ أصلًا. وثانيهما نصيبُ الصفوف التي سكت فيها
عمودُ `axes_count` — وهو خللُ نقلٍ في عمودٍ آخرَ بالكلّيّة. **والنتيجةُ تُثبِت
ملوِّثًا ولا تُثبِته كافيًا**: الطبقةُ الفاسدةُ نصيبُها في الشاهد بعيدٌ جدًّا
عن نصيب الجدول، فهي ملوِّثٌ قائمٌ بالعدّ؛ ثمّ يُعاد القياسُ على المجال منقّى
منها فيبقى فائضٌ في أكثرِ صفوفه (`THE_CONTAMINANT_IS_REAL_AND_INSUFFICIENT`).

**والتنقيةُ ههنا ليست تفصيلًا على المقاس**، لأنّ قاعدةَ التصنيف تفحص **صورةَ
الترويسة** ولا تنظر إلى نصيبِ الشاهد فيها؛ فهي قاعدةٌ تُطبَّق على العمود الذي
تُصنّفه لا على العمود الذي يُقاس. ومع ذلك تخرج الطبقةُ الفاسدةُ معدودةً
مُسمّاةً، ويخرج القياسان معًا — على المجال كلِّه وعلى المنقّى — فلا يُقرأ
أحدُهما بلا الآخر.

**خمولٌ سلطويّ**: لا ولادةَ هنا ولا حكمَ ولادةٍ ولا تجميدَ `E0`، ولا استيرادَ
من `kernel/`.
"""

from __future__ import annotations

import random
from collections.abc import Sequence
from dataclasses import dataclass
from enum import Enum
from typing import Final

from .dal_alone_gloss import (
    THE_PROFILE_AXES,
    DalGlossEntry,
    ProfileAxis,
    profile_of,
    whole_table_entries,
)

__all__ = [
    "A_CORRELATION_ACROSS_FORTY_CHAPTERS_IS_NOT_A_POWERED_TEST",
    "A_RESIDUAL_IS_NOT_A_MEASURED_CAUSE",
    "AccountStanding",
    "AttributionReading",
    "CandidateAccount",
    "ChapterExcess",
    "HeaderForm",
    "MAQAYIS_DEVIATION_ATTRIBUTION_NAMED_RESIDUALS",
    "MaqayisDeviationAttributionError",
    "NullProfile",
    "SIZE_INFLATES_THE_GAPS_AND_DOES_NOT_PRODUCE_THE_EXCESS",
    "THE_CLEANING_RULE_READS_THE_HEADER_AND_NOT_THE_MEASURED_COLUMN",
    "THE_CONTAMINANT_IS_REAL_AND_INSUFFICIENT",
    "THE_DECLARED_NULL_PROFILE",
    "THE_MEASURED_AXIS",
    "THE_THREE_CANDIDATE_ACCOUNTS",
    "TWO_PROBES_DO_NOT_EXHAUST_THE_EXTRACTION_ACCOUNT",
    "classify_header",
    "excess_over_the_size_null",
    "extraction_defect_rate",
    "header_strata",
    "run_attribution",
    "spearman_rank_correlation",
]


class MaqayisDeviationAttributionError(ValueError):
    """خطأٌ في فصل تفاسير الانحراف أو في بناء نموذج عدمه."""


THE_MEASURED_AXIS: Final[ProfileAxis] = ProfileAxis.SHARE_WITH_POETRY
"""المحورُ المقيس: نصيبُ حامل الشاهد الشعريّ، وهو الذي خرج عن السماحيّة."""


# --- نموذجُ العدم ------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class NullProfile:
    """صفةُ نموذج العدم مُعلَنةً قبل تشغيله: عدد السحبات، والمئين، والبذرة."""

    replicates: int
    percentile: float
    seed: int

    def __post_init__(self) -> None:
        if self.replicates < 1:
            raise MaqayisDeviationAttributionError("نموذجُ عدمٍ بلا سحبةٍ لا يُقارَن به")
        if not 0.0 < self.percentile < 1.0:
            raise MaqayisDeviationAttributionError("مئينٌ خارجَ المجال ليس مئينًا")


THE_DECLARED_NULL_PROFILE: Final[NullProfile] = NullProfile(
    replicates=400, percentile=0.95, seed=20260920
)
"""نموذجُ العدم مُعلَنًا قبل القياس؛ والبذرةُ مكتوبةٌ فيُعاد الرقمُ عينُه."""


def excess_over_the_size_null(
    entries: Sequence[DalGlossEntry],
    domain: Sequence[DalGlossEntry],
    axis: ProfileAxis = THE_MEASURED_AXIS,
    profile: NullProfile = THE_DECLARED_NULL_PROFILE,
) -> tuple[float, float]:
    """`(الفرقُ المرصود، حدُّ نموذج العدم)` لبابٍ واحد عند عدّته.

    والسحبُ من المجال نفسِه بلا إبدالٍ وبعدّة الباب؛ فما زاد فرقُه على الحدّ
    فائضٌ لا تفسّره العدّةُ وحدَها.
    """

    if not entries:
        raise MaqayisDeviationAttributionError("بابٌ خالٍ لا يُقابَل بنموذج عدم")
    if len(entries) > len(domain):
        raise MaqayisDeviationAttributionError("بابٌ أوسعُ من مجاله؛ عدٌّ فاسد")
    whole_share = profile_of("المجال", domain).share(axis)
    observed = abs(profile_of("الباب", entries).share(axis) - whole_share)
    rng = random.Random(profile.seed)
    draws = sorted(
        abs(
            profile_of("سحبة", rng.sample(list(domain), len(entries))).share(axis)
            - whole_share
        )
        for _ in range(profile.replicates)
    )
    index = min(int(profile.percentile * profile.replicates), profile.replicates - 1)
    return observed, draws[index]


@dataclass(frozen=True, slots=True)
class ChapterExcess:
    """فائضُ بابٍ على نموذج عدمه؛ والحكمُ خاصّيّةٌ تُشتَقّ لا حقلٌ يُكتَب."""

    header: str
    size: int
    observed_gap: float
    null_threshold: float

    def __post_init__(self) -> None:
        if self.size < 1:
            raise MaqayisDeviationAttributionError("بابٌ بعدّةٍ غيرِ موجبةٍ لا يُقاس")

    @property
    def exceeds_the_null(self) -> bool:
        """أيتجاوز الفرقُ المرصودُ حدَّ نموذج العدم عند عدّة الباب؟"""

        return self.observed_gap > self.null_threshold


# --- تصنيفُ الترويسة --------------------------------------------------------------


class HeaderForm(Enum):
    """صورةُ الترويسة، مصنَّفةً بشكلها وحدَه لا بنتيجتها."""

    LETTER_BOOK = "كتابُ_حرف"
    SUB_CHAPTER = "بابٌ"
    MALFORMED = "ليست_ترويسةَ_باب"
    ABSENT = "لا_ترويسة"


def classify_header(header: str) -> HeaderForm:
    """صنِّف ترويسةً بصورتها؛ والقاعدةُ تقرأ الترويسةَ ولا تنظر إلى ما يُقاس.

    وهذا وحدَه ما يمنع أن تكون التنقيةُ تفصيلًا على المقاس: القاعدةُ مُطبَّقةٌ
    على العمود الذي تُصنّفه، لا على عمود الشاهد الشعريّ الذي يُقاس
    (`THE_CLEANING_RULE_READS_THE_HEADER_AND_NOT_THE_MEASURED_COLUMN`).
    """

    text = header.strip()
    if not text:
        return HeaderForm.ABSENT
    if text.startswith("كتاب ") and len(text.split()) <= 2:
        return HeaderForm.LETTER_BOOK
    if text.startswith("باب "):
        return HeaderForm.SUB_CHAPTER
    return HeaderForm.MALFORMED


def header_strata() -> dict[HeaderForm, tuple[DalGlossEntry, ...]]:
    """صفوفُ الجدول مقسومةً على صور الترويسة، بلا إسقاطِ صورةٍ ولا طيّها."""

    strata: dict[HeaderForm, list[DalGlossEntry]] = {form: [] for form in HeaderForm}
    for entry in whole_table_entries():
        strata[classify_header(entry.chapter_header)].append(entry)
    return {form: tuple(items) for form, items in strata.items()}


def extraction_defect_rate(entries: Sequence[DalGlossEntry]) -> float:
    """نصيبُ الصفوف التي سكت فيها عمودُ `axes_count`؛ خللُ نقلٍ في عمودٍ آخر.

    وإنّما صلح مِسبارًا لأنّه **لا يمسّ عمودَ الشاهد الشعريّ**؛ فارتباطُه به
    ارتباطُ شاهدين مستقلَّين على خللِ نقلٍ واحد، لا دورٌ في القياس.
    """

    if not entries:
        raise MaqayisDeviationAttributionError("مجموعةٌ خاليةٌ لا نصيبَ لها")
    return sum(1 for entry in entries if not entry.written_axis_count) / len(entries)


def spearman_rank_correlation(xs: Sequence[float], ys: Sequence[float]) -> float:
    """ارتباطُ الرتب؛ يُحسَب ههنا بالقائمة لا يُستورَد، إذ لا تبعيّةَ للتشغيل."""

    if len(xs) != len(ys):
        raise MaqayisDeviationAttributionError("متتاليتان مختلفتا الطول لا تُقرَنان")
    if len(xs) < 3:
        raise MaqayisDeviationAttributionError("ارتباطٌ على أقلَّ من ثلاثٍ لا يُقرَأ")

    def ranks(values: Sequence[float]) -> list[float]:
        """رتبٌ بمتوسّط المتساويات؛ فالتساوي لا يُفَضّ بترتيب الورود.

        ولولا ذلك لأخذت القيمُ المتساويةُ رتبًا متمايزةً بحسب موضعها في
        المدخل، فيخرج ارتباطٌ من ترتيبِ صفوفٍ لا من تفاوتِ قيم.
        """

        order = sorted(range(len(values)), key=lambda index: values[index])
        out = [0.0] * len(values)
        start = 0
        while start < len(order):
            stop = start
            while (
                stop + 1 < len(order)
                and values[order[stop + 1]] == values[order[start]]
            ):
                stop += 1
            shared = (start + stop) / 2 + 1
            for index in order[start : stop + 1]:
                out[index] = shared
            start = stop + 1
        return out

    rx, ry = ranks(xs), ranks(ys)
    count = len(rx)
    mx, my = sum(rx) / count, sum(ry) / count
    numerator = sum((a - mx) * (b - my) for a, b in zip(rx, ry, strict=True))
    spread_x = sum((a - mx) ** 2 for a in rx)
    spread_y = sum((b - my) ** 2 for b in ry)
    if spread_x == 0.0 or spread_y == 0.0:
        raise MaqayisDeviationAttributionError("متتاليةٌ بلا تفاوتٍ لا رتبةَ لها")
    return numerator / float((spread_x * spread_y) ** 0.5)


# --- الحكمُ على التفاسير الثلاثة ----------------------------------------------------


class CandidateAccount(Enum):
    """التفاسيرُ الثلاثةُ مُسمّاةً قبل القياس؛ ولا يُزاد رابعٌ بعد النتيجة."""

    CHAPTER_SIZE = "صِغَرُ_الأبواب"
    EXTRACTION_UNEVENNESS = "تفاوتُ_الاستخراج"
    AUTHORIAL_UNEVENNESS = "تفاوتُ_التأليف"


class AccountStanding(Enum):
    """منزلةُ تفسيرٍ واحد؛ أربعٌ لا اثنتان، والبقيّةُ ليست إثباتًا."""

    REFUTED_AS_THE_ACCOUNT = "منقوضٌ_تفسيرًا"
    A_REAL_BUT_INSUFFICIENT_CONTRIBUTOR = "مُسهِمٌ_قائمٌ_غيرُ_كافٍ"
    A_NAMED_RESIDUAL_WITH_NO_PROBE_OF_ITS_OWN = "بقيّةٌ_مُسمّاةٌ_بلا_مِسبار"
    NOT_ASSESSED = "لم_يُقَس"


@dataclass(frozen=True, slots=True)
class AttributionReading:
    """قراءةُ الفصل كاملةً؛ كلُّ حكمٍ فيها خاصّيّةٌ تُشتَقّ من أرقامها."""

    excesses: tuple[ChapterExcess, ...]
    cleaned_excesses: tuple[ChapterExcess, ...]
    malformed_share: float
    whole_share: float
    cleaned_whole_share: float
    malformed_rows: int
    defect_correlation: float
    correlated_chapters: int

    def __post_init__(self) -> None:
        if not self.excesses or not self.cleaned_excesses:
            raise MaqayisDeviationAttributionError("قراءةٌ بلا بابٍ مقيسٍ لا تُحكَم")
        if self.malformed_rows < 0:
            raise MaqayisDeviationAttributionError("صفوفٌ بعددٍ سالبٍ عدٌّ فاسد")

    @property
    def exceeding_chapters(self) -> tuple[ChapterExcess, ...]:
        """الأبوابُ التي فاض فرقُها على نموذج عدمها، قبل التنقية."""

        return tuple(item for item in self.excesses if item.exceeds_the_null)

    @property
    def cleaned_exceeding_chapters(self) -> tuple[ChapterExcess, ...]:
        """الأبوابُ الفائضةُ بعد نزع الطبقة الفاسدة من المجال."""

        return tuple(item for item in self.cleaned_excesses if item.exceeds_the_null)

    @property
    def median_size(self) -> float:
        """وسيطُ عدّة الأبواب؛ تُقسَم به الأبوابُ كبيرةً وصغيرة."""

        sizes = sorted(item.size for item in self.excesses)
        middle = len(sizes) // 2
        if len(sizes) % 2 == 1:
            return float(sizes[middle])
        return (sizes[middle - 1] + sizes[middle]) / 2

    @property
    def excess_among_the_large(self) -> int:
        """الفائضون من الأبواب التي عدّتُها فوق الوسيط."""

        return sum(
            1
            for item in self.excesses
            if item.exceeds_the_null and item.size > self.median_size
        )

    @property
    def excess_among_the_small(self) -> int:
        """الفائضون من الأبواب التي عدّتُها دون الوسيط أو عنده."""

        return sum(
            1
            for item in self.excesses
            if item.exceeds_the_null and item.size <= self.median_size
        )

    @property
    def rows_in_cleaned_exceeding_chapters(self) -> int:
        """كم صفًّا يقع في أبوابٍ فاضت بعد التنقية؟ سَعةُ ما بقي بلا تفسير."""

        return sum(item.size for item in self.cleaned_exceeding_chapters)

    @property
    def malformed_stratum_departs_from_the_whole(self) -> bool:
        """أنصيبُ الطبقة الفاسدة بعيدٌ عن نصيب الجدول بأكثرَ من الضعف العشريّ؟

        والحدُّ ههنا هو السماحيّةُ المُعلَنةُ سلفًا في `dal_alone_gloss`؛ فلا
        تُستحدَث عتبةٌ ثانيةٌ بعد رؤية الرقم.
        """

        return abs(self.malformed_share - self.whole_share) > 0.05

    def standing_of(self, account: CandidateAccount) -> AccountStanding:
        """منزلةُ تفسيرٍ واحد، مُشتقّةً من مِسباره لا مكتوبةً بجانبه.

        والعدّةُ تُنقَض تفسيرًا إذا تركّز فائضُها في الكبار لا في الصغار، إذ
        الضجيجُ عند الصغار أعلى فلو كان هو المُولِّدَ لظهر فيهم. والاستخراجُ
        يُثبَت مُسهِمًا بطبقةٍ فاسدةٍ نصيبُها بعيد، ولا يُثبَت كافيًا ما بقي
        فائضٌ بعد نزعها. وأمّا التأليفُ فلا مِسبارَ له، فمنزلتُه بقيّةٌ دائمًا.
        """

        if account is CandidateAccount.CHAPTER_SIZE:
            if self.excess_among_the_large > self.excess_among_the_small:
                return AccountStanding.REFUTED_AS_THE_ACCOUNT
            return AccountStanding.A_REAL_BUT_INSUFFICIENT_CONTRIBUTOR
        if account is CandidateAccount.EXTRACTION_UNEVENNESS:
            if not self.malformed_stratum_departs_from_the_whole:
                return AccountStanding.REFUTED_AS_THE_ACCOUNT
            if not self.cleaned_exceeding_chapters:
                return AccountStanding.NOT_ASSESSED
            return AccountStanding.A_REAL_BUT_INSUFFICIENT_CONTRIBUTOR
        return AccountStanding.A_NAMED_RESIDUAL_WITH_NO_PROBE_OF_ITS_OWN


THE_THREE_CANDIDATE_ACCOUNTS: Final[tuple[CandidateAccount, ...]] = tuple(
    CandidateAccount
)
"""التفاسيرُ الثلاثةُ كما سُمّيت حين سُجّلت البقيّة؛ لا يُزاد فيها ولا يُنقَص."""


def run_attribution(
    axis: ProfileAxis = THE_MEASURED_AXIS,
    profile: NullProfile = THE_DECLARED_NULL_PROFILE,
    minimum_size_for_correlation: int = 30,
) -> AttributionReading:
    """أجرِ المِسبارين وارفع البقيّة، في قراءةٍ واحدةٍ من البايتات المُودَعة."""

    if axis not in THE_PROFILE_AXES:
        raise MaqayisDeviationAttributionError("محورٌ غيرُ مُعلَنٍ لا يُقاس به")
    everything = whole_table_entries()
    strata = header_strata()
    malformed = strata[HeaderForm.MALFORMED]
    cleaned = tuple(
        entry
        for entry in everything
        if classify_header(entry.chapter_header)
        in (HeaderForm.LETTER_BOOK, HeaderForm.SUB_CHAPTER)
    )
    if not malformed or not cleaned:
        raise MaqayisDeviationAttributionError(
            "طبقةٌ خاليةٌ تجعل المقابلةَ بلا طرف؛ ولا تُقرَأ صفرًا"
        )

    def by_header(
        source: Sequence[DalGlossEntry],
    ) -> dict[str, tuple[DalGlossEntry, ...]]:
        grouped: dict[str, list[DalGlossEntry]] = {}
        for entry in source:
            if entry.chapter_header:
                grouped.setdefault(entry.chapter_header, []).append(entry)
        return {header: tuple(items) for header, items in grouped.items()}

    def measure(
        source: Sequence[DalGlossEntry],
    ) -> tuple[ChapterExcess, ...]:
        return tuple(
            ChapterExcess(
                header=header,
                size=len(items),
                observed_gap=observed,
                null_threshold=threshold,
            )
            for header, items in by_header(source).items()
            for observed, threshold in (
                excess_over_the_size_null(items, source, axis, profile),
            )
        )

    cleaned_groups = by_header(cleaned)
    cleaned_whole = profile_of("المنقّى", cleaned).share(axis)
    wide = [
        (header, items)
        for header, items in cleaned_groups.items()
        if len(items) >= minimum_size_for_correlation
    ]
    if len(wide) < 3:
        raise MaqayisDeviationAttributionError("أبوابٌ أقلُّ من ثلاثةٍ لا ارتباطَ لها")
    return AttributionReading(
        excesses=measure(everything),
        cleaned_excesses=measure(cleaned),
        malformed_share=profile_of("الفاسدة", malformed).share(axis),
        whole_share=profile_of("الجدول", everything).share(axis),
        cleaned_whole_share=cleaned_whole,
        malformed_rows=len(malformed),
        defect_correlation=spearman_rank_correlation(
            [extraction_defect_rate(items) for _, items in wide],
            [
                abs(profile_of(header, items).share(axis) - cleaned_whole)
                for header, items in wide
            ],
        ),
        correlated_chapters=len(wide),
    )


# --- البقايا المُسمّاة --------------------------------------------------------------


SIZE_INFLATES_THE_GAPS_AND_DOES_NOT_PRODUCE_THE_EXCESS: Final[str] = (
    "SIZE_INFLATES_THE_GAPS_AND_DOES_NOT_PRODUCE_THE_EXCESS: صِغَرُ الأبواب "
    "يوسّع فروقَها بلا ريب، وذلك مقروءٌ في نموذج العدم نفسِه: حدُّه عند البابِ "
    "الصغير أضعافُ حدِّه عند الكبير. لكنّ الفائضَ عليه يتركّز في الكبار، "
    "فالعدّةُ تفسّر سَعةَ الفرق ولا تفسّر تجاوزَه حدَّه."
)

THE_CONTAMINANT_IS_REAL_AND_INSUFFICIENT: Final[str] = (
    "THE_CONTAMINANT_IS_REAL_AND_INSUFFICIENT: الطبقةُ الفاسدةُ ملوِّثٌ مُثبَتٌ "
    "بالعدّ، نصيبُها في الشاهد بعيدٌ عن نصيب الجدول بأضعاف السماحيّة. ومع ذلك "
    "يبقى بعد نزعها فائضٌ في أكثر الأبواب سَعةً، فالاستخراجُ مُسهِمٌ لا مُستغرِق؛ "
    "ومن نزع الملوِّثَ ثمّ أعلن المسألةَ مُغلَقةً أغلقها على بقيّةٍ قائمة."
)

A_RESIDUAL_IS_NOT_A_MEASURED_CAUSE: Final[str] = (
    "A_RESIDUAL_IS_NOT_A_MEASURED_CAUSE: تفاوتُ تأليف ابن فارس لا مِسبارَ له في "
    "هذه البايتات، إذ ليس فيها شاهدٌ على عادته مستقلٌّ عن هذا الاستخراج نفسِه. "
    "فمنزلتُه بقيّةٌ مُسمّاةٌ لا تُرقَّى بارتفاع منافسَيها: نفيُ تفسيرين لا "
    "يُثبِت ثالثًا، وقد يكون المُفسِّرُ رابعًا لم يُسمَّ أصلًا."
)

THE_CLEANING_RULE_READS_THE_HEADER_AND_NOT_THE_MEASURED_COLUMN: Final[str] = (
    "THE_CLEANING_RULE_READS_THE_HEADER_AND_NOT_THE_MEASURED_COLUMN: قاعدةُ "
    "تصنيف الترويسة تفحص صورتَها وحدَها، فلا تنظر إلى نصيب الشاهد الشعريّ الذي "
    "يُقاس. وبذلك تخرج التنقيةُ من باب التفصيل على المقاس؛ ومع ذلك يخرج "
    "القياسان معًا — على المجال كلِّه وعلى المنقّى — فلا يُقرَأ أحدُهما وحدَه."
)

TWO_PROBES_DO_NOT_EXHAUST_THE_EXTRACTION_ACCOUNT: Final[str] = (
    "TWO_PROBES_DO_NOT_EXHAUST_THE_EXTRACTION_ACCOUNT: مِسبارا الاستخراج ههنا "
    "صورةُ الترويسة وسكوتُ عمود المحاور، وهما شاهدان لا استقصاء. فقد يكون في "
    "النقل خللٌ لا يظهر فيهما — كشاهدٍ شعريٍّ سقط من صفٍّ ترويستُه سليمةٌ "
    "وعمودُ محاوره ناطق — ونفيُ كفاية المِسبارين ليس نفيَ كفاية التفسير."
)

A_CORRELATION_ACROSS_FORTY_CHAPTERS_IS_NOT_A_POWERED_TEST: Final[str] = (
    "A_CORRELATION_ACROSS_FORTY_CHAPTERS_IS_NOT_A_POWERED_TEST: ارتباطُ الرتب "
    "بين خلل النقل وفرق الشاهد محسوبٌ على أبوابٍ عدّتُها عشراتٌ لا آلاف، فلا "
    "يُقرَأ حكمًا ولا يدخل في منزلة تفسير. وهو يخرج رقمًا يُقرَأ ويُنقَد، ولا "
    "يُبنى عليه حكمٌ في هذه الوحدة."
)

MAQAYIS_DEVIATION_ATTRIBUTION_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "SIZE_INFLATES_THE_GAPS_AND_DOES_NOT_PRODUCE_THE_EXCESS": (
        SIZE_INFLATES_THE_GAPS_AND_DOES_NOT_PRODUCE_THE_EXCESS
    ),
    "THE_CONTAMINANT_IS_REAL_AND_INSUFFICIENT": (
        THE_CONTAMINANT_IS_REAL_AND_INSUFFICIENT
    ),
    "A_RESIDUAL_IS_NOT_A_MEASURED_CAUSE": A_RESIDUAL_IS_NOT_A_MEASURED_CAUSE,
    "THE_CLEANING_RULE_READS_THE_HEADER_AND_NOT_THE_MEASURED_COLUMN": (
        THE_CLEANING_RULE_READS_THE_HEADER_AND_NOT_THE_MEASURED_COLUMN
    ),
    "TWO_PROBES_DO_NOT_EXHAUST_THE_EXTRACTION_ACCOUNT": (
        TWO_PROBES_DO_NOT_EXHAUST_THE_EXTRACTION_ACCOUNT
    ),
    "A_CORRELATION_ACROSS_FORTY_CHAPTERS_IS_NOT_A_POWERED_TEST": (
        A_CORRELATION_ACROSS_FORTY_CHAPTERS_IS_NOT_A_POWERED_TEST
    ),
}
"""ما لا يُثبِته هذا الفصلُ مُسمًّى باسمه، لا مطويًّا في حكمٍ عامّ."""
