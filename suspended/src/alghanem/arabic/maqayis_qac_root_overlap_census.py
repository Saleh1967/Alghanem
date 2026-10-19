"""قياسُ تقاطع جذور «مقاييس» بجذور مدوَّنة القرآن، بمقاماته الستّة معًا.

**ما تفعله هذه الوحدة**: تقرأ جذورَ «مقاييس» من بايتاتٍ مُبصَّمةٍ في هذه
الشجرة، وجذورَ المدوَّنة الصرفية من بايتاتٍ يُمرِّرها حائزُها بعد مطابقة
بصمتها، ثمّ تُخرِج التقاطعَ وطرفيه **عند كلّ مقامٍ من مقامات
`OVERLAP_STAGES` دفعةً واحدة**. والقواعدُ كلُّها مُجمَّدةٌ قبلها في
`maqayis_qac_root_overlap_preregistration`، والتحويلُ والتطبيعُ في
`root_orthography_bridge`؛ فلا تُسَنّ هنا قاعدةٌ ولا يُخترَع مقام.

`BOTH_COUNTS_LEAVE_TOGETHER_OR_NEITHER_DOES`: لا دالّةَ في هذه الوحدة تُخرِج
مقامًا واحدًا: `overlap_readouts` تُخرِج الستّةَ مرتَّبةً، و`readout_at`
تختار من ناتجها ولا تحسب مفردًا. والعلّةُ مكتوبةٌ في
`NORMALISATION_IS_A_RULE_ENACTED_NOT_A_FACT_READ`: التطبيعُ يُغيّر الرقم،
فإخراجُ الرقم بعده وحدَه يُخفي **أنّ قاعدةً صنعته**.

`THE_ROOT_ALPHABET_IS_THE_DECIDING_OBSERVATION`: `qac_root_alphabet` تُخرِج
محارفَ خانة `ROOT` كما هي بعدد حاملي كلٍّ منها، وعليها وحدَها يفترق
تشخيصا الـ٣٢٨ المُجمَّدان في `HAMZA_DIAGNOSIS_HYPOTHESES`. وهي تُخرَج
**قبل** أيّ تحويل، إذ التحويلُ نفسُه هو المتّهَم.

`A_FUSION_IS_THE_PRICE_OF_A_STAGE`: مع كلّ مقامٍ تُخرَج الانصهاراتُ في كلّ
جانبٍ بأعيانها (`fusions_under` في وحدة الجسر): كم جذرًا متمايزًا في
البايتات صار جذرًا واحدًا، وأيُّها. فارتفاعُ التقاطع بالتطبيع ليس مكسبًا
صافيًا، وثمنُه يُعرَض معه لا بعده.

`THE_MAQAYIS_SIDE_IS_MEASURED_AND_THE_OTHER_IS_NOT_YET`: جانبُ «مقاييس»
يُقاس في هذه الشجرة الآن، وجانبُ المدوَّنة موقوفٌ على حائز بايتاتها؛ ولا
تُخمَّن لها قيمةٌ ولا تُنسَخ بايتاتُها — رخصتُها ورخصةُ نصّها تمنعان، كما
في `WITNESS_BYTES_ARE_STILL_NOT_VENDORED`.

`ABSENCE_IN_QAC_IS_ABSENCE_FROM_A_TAGGING`: كلُّ رقمٍ يخرج من هنا عن «غير
المغطّى» هو عددُ ما **لم يُوسَم** في هذا الإصدار، لا عددُ ما لم يرد في
القرآن؛ وخانةُ `ROOT` تبويبُ مُوسِّمين لا خاصّيّةٌ تُقاس.

`THE_3361_CARRY_NO_MORPHOLOGICAL_TAG`: ما تزيده «مقاييس» جذورٌ بلا وَسْمِ
وزنٍ ولا بابٍ ولا إعراب؛ فهي تُوسِّع فضاءَ الجذور لا فضاءَ القياس الصرفيّ،
ولا يخرج من هذه الوحدة وَسْمٌ لجذرٍ واحدٍ منها.

وهذه الوحدة قياسٌ لا سلطة: لا ولادةَ فيها، ولا حكمَ ولادة، ولا تجميدَ `E0`،
ولا تستورد من `kernel/` شيئًا، ولا تقرؤها وحدةٌ فيه.

المصدر: مدوَّنة القرآن الصرفية، http://corpus.quran.com — مبنيّةٌ على نصّ
تنزيل، http://tanzil.info. والإسنادُ إليهما شرطُ رخصةٍ لا لطفَ عبارة.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Final

from .hollow_root_root_census import (
    corpus_lines,
    parse_segment_line,
    root_of_features,
)
from .maqayis_qac_root_overlap_preregistration import (
    OVERLAP_STAGES,
    OverlapStage,
)
from .maqayis_root_table_deposit import TRILATERAL_ROOT_TYPE, root_table_rows
from .root_orthography_bridge import (
    HAMZA_CHARACTERS_IN_BUCKWALTER,
    FusionRecord,
    fusions_under,
    normalise_root,
    transliterate_root,
)

__all__ = [
    "A_FUSION_IS_THE_PRICE_OF_A_STAGE_NOTE",
    "BOTH_COUNTS_LEAVE_TOGETHER_OR_NEITHER_DOES_NOTE",
    "OVERLAP_CENSUS_NAMED_RESIDUALS",
    "THE_MAQAYIS_SIDE_IS_MEASURED_AND_THE_OTHER_IS_NOT_YET_NOTE",
    "THE_ROOT_ALPHABET_IS_THE_DECIDING_OBSERVATION_NOTE",
    "AlphabetReadout",
    "OverlapCensusError",
    "OverlapReadout",
    "StageFusions",
    "maqayis_roots",
    "maqayis_trilateral_roots",
    "overlap_readouts",
    "qac_root_alphabet",
    "qac_roots",
    "readout_at",
    "stage_fusions",
]


class OverlapCensusError(ValueError):
    """رفضٌ صريح: جانبٌ فارغ، أو مقامٌ غيرُ مُجمَّد، أو رقمٌ بلا مقامه."""


BOTH_COUNTS_LEAVE_TOGETHER_OR_NEITHER_DOES_NOTE: Final[str] = (
    "BothCountsLeaveTogetherOrNeitherDoes: لا دالّةَ هنا تُخرِج مقامًا مفردًا؛ "
    "التطبيعُ يُغيّر الرقمَ فإخراجُ ما بعده وحدَه يُخفي أنّ قاعدةً صنعته"
)

THE_ROOT_ALPHABET_IS_THE_DECIDING_OBSERVATION_NOTE: Final[str] = (
    "TheRootAlphabetIsTheDecidingObservation: محارفُ خانة `ROOT` كما هي قبل "
    "أيّ تحويلٍ هي الواقعةُ التي يفترق عندها تشخيصا الـ٣٢٨؛ وتُخرَج بأعدادها "
    "لا بحكمٍ عليها"
)

A_FUSION_IS_THE_PRICE_OF_A_STAGE_NOTE: Final[str] = (
    "AFusionIsThePriceOfAStage: ارتفاعُ التقاطع بالتطبيع ليس مكسبًا صافيًا؛ "
    "فتُخرَج مع كلّ مقامٍ الجذورُ المتمايزةُ التي انصهرت في كلّ جانبٍ بأعيانها"
)

THE_MAQAYIS_SIDE_IS_MEASURED_AND_THE_OTHER_IS_NOT_YET_NOTE: Final[str] = (
    "TheMaqayisSideIsMeasuredAndTheOtherIsNotYet: بايتاتُ «مقاييس» في الشجرة "
    "مُبصَّمةً فجانبُها مقيسٌ الآن، وبايتاتُ المدوَّنة خارجَها برخصتها فجانبُها "
    "موقوفٌ على حائزها؛ ولا تُخمَّن قيمةٌ ولا تُنسَخ بايتات"
)

OVERLAP_CENSUS_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "BothCountsLeaveTogetherOrNeitherDoes": (
        BOTH_COUNTS_LEAVE_TOGETHER_OR_NEITHER_DOES_NOTE
    ),
    "TheRootAlphabetIsTheDecidingObservation": (
        THE_ROOT_ALPHABET_IS_THE_DECIDING_OBSERVATION_NOTE
    ),
    "AFusionIsThePriceOfAStage": A_FUSION_IS_THE_PRICE_OF_A_STAGE_NOTE,
    "TheMaqayisSideIsMeasuredAndTheOtherIsNotYet": (
        THE_MAQAYIS_SIDE_IS_MEASURED_AND_THE_OTHER_IS_NOT_YET_NOTE
    ),
}


def maqayis_roots(root: Path | None = None) -> frozenset[str]:
    """جذورُ «مقاييس» المتمايزةُ على كلّ الأنواع، من البايتات المُبصَّمة.

    تحت `MAQAYIS_DISTINCT_ROOTS_ALL_TYPES`؛ والبايتاتُ تُقرأ عبر
    `maqayis_root_table_deposit` فتُطابَق بصمتُها وطولُها قبل أيّ قيمة، ولا
    يُفتَح الملفُّ هنا فتحًا ثانيًا ببصمةٍ منسوخة.
    """

    return frozenset(row["root_full"] for row in root_table_rows(root))


def maqayis_trilateral_roots(root: Path | None = None) -> frozenset[str]:
    """جذورُ «مقاييس» الثلاثيّةُ المتمايزة تحت قاعدة الملفّ لا تحت حكمٍ منّا."""

    return frozenset(
        row["root_full"]
        for row in root_table_rows(root)
        if row["root_type"] == TRILATERAL_ROOT_TYPE
    )


def qac_roots(path: Path) -> frozenset[str]:
    """جذورُ المدوَّنة المُوسَّمةُ المتمايزةُ بترميزها كما هي، بلا تحويل.

    تحت `QAC_DISTINCT_TAGGED_ROOTS`؛ والبايتاتُ تُطابَق بصمتُها وطولُها في
    `verified_corpus_bytes` قبل أن يخرج منها حرف. ومقطعٌ بلا سمة `ROOT` لا
    يُخمَّن له جذر: لا يدخل العدَّ ولا يُعَدُّ فراغًا فيه.
    """

    roots: set[str] = set()
    for line in corpus_lines(path):
        record = parse_segment_line(line)
        if record is None:
            continue
        root = root_of_features(record.features)
        if root is not None:
            roots.add(root)
    if not roots:
        raise OverlapCensusError(
            "لا جذرَ موسومًا في هذه البايتات؛ وصفرٌ هنا عطلُ قراءةٍ لا واقعةُ لغة."
        )
    return frozenset(roots)


@dataclass(frozen=True, slots=True)
class AlphabetReadout:
    """أبجديةُ خانةٍ كما هي: محارفُها بأعداد الجذور الحاملة لكلٍّ منها.

    وهذه **رصدٌ لا حكم**: تُخرِج ما في البايتات، ولا تقول أيَّ فرضيةٍ أصابت؛
    والحكمُ يُكتَب في `hamza_characters_present` قراءةً للواقعة لا تفسيرًا لها.
    """

    characters: tuple[tuple[str, int], ...]

    def __post_init__(self) -> None:
        if not self.characters:
            raise OverlapCensusError("أبجديةٌ فارغةٌ ليست رصدًا؛ ولا تُخرَج صامتةً.")
        seen = [character for character, _ in self.characters]
        if len(set(seen)) != len(seen):
            raise OverlapCensusError("محرفٌ مكرَّرٌ في أبجديةٍ واحدة.")
        for character, count in self.characters:
            if len(character) != 1:
                raise OverlapCensusError("مدخلُ الأبجدية محرفٌ واحد.")
            if not isinstance(count, int) or count <= 0:
                raise OverlapCensusError(
                    "محرفٌ في الأبجدية عددُ حامليه موجب؛ وصفرٌ يعني أنّه ليس فيها."
                )

    @property
    def hamza_characters_present(self) -> tuple[str, ...]:
        """محارفُ الهمزة الستّةُ الظاهرةُ فعلًا؛ وفراغُها هو الواقعةُ الفاصلة."""

        present = {character for character, _ in self.characters}
        return tuple(
            character
            for character in HAMZA_CHARACTERS_IN_BUCKWALTER
            if character in present
        )


def qac_root_alphabet(roots: Iterable[str]) -> AlphabetReadout:
    """محارفُ جذور المدوَّنة كما هي قبل أيّ تحويل، مرتَّبةً ترتيبًا واحدًا.

    والعدُّ على **الجذور** لا على الورودات: جذرٌ ورد ألفًا يُعَدّ واحدًا،
    فلا يُضخَّم حضورُ محرفٍ بتواتر حامله.
    """

    counter: Counter[str] = Counter()
    for root in roots:
        counter.update(set(root))
    return AlphabetReadout(
        characters=tuple(sorted(counter.items(), key=lambda item: (-item[1], item[0])))
    )


def _staged_forms(
    forms: Iterable[str], stage: OverlapStage, transliterate: bool
) -> dict[str, str]:
    staged: dict[str, str] = {}
    for form in forms:
        current = transliterate_root(form) if transliterate else form
        if stage.rules:
            current = normalise_root(current, stage.rules).after
        staged[form] = current
    return staged


@dataclass(frozen=True, slots=True)
class OverlapReadout:
    """تقاطعُ المعجمين عند مقامٍ واحد، بجانبيه وفجوتيه؛ ولا يُخرَج وحدَه.

    والأعدادُ كلُّها **بعد** إعمال المقام على الجانبين معًا: فالتطبيعُ يُنقِص
    حجمَ الجانب كما يزيد التقاطع، ونسبةٌ مقسومةٌ على حجمٍ قبل التطبيع تُخرِج
    كسرًا لا مقامَ له.
    """

    stage_name: str
    maqayis_size: int
    qac_size: int
    intersection: int
    maqayis_only: int
    qac_only: int

    def __post_init__(self) -> None:
        if not self.stage_name.strip():
            raise OverlapCensusError("قراءةٌ بلا اسم مقامٍ ليست عددًا.")
        for value, label in (
            (self.maqayis_size, "حجمُ جانب مقاييس"),
            (self.qac_size, "حجمُ جانب المدوَّنة"),
            (self.intersection, "التقاطع"),
            (self.maqayis_only, "غيرُ المغطّى"),
            (self.qac_only, "الفجوةُ العكسية"),
        ):
            if not isinstance(value, int) or value < 0:
                raise OverlapCensusError(f"{label} عددٌ صحيحٌ غيرُ سالب.")
        if self.intersection + self.maqayis_only != self.maqayis_size:
            raise OverlapCensusError(
                "تقاطعٌ وفجوةٌ لا يُجمَعان حجمَ جانبهما؛ وإحصاءٌ لا يُجمَع لا يُخرَج."
            )
        if self.intersection + self.qac_only != self.qac_size:
            raise OverlapCensusError(
                "تقاطعٌ وفجوةٌ عكسيّةٌ لا يُجمَعان حجمَ المدوَّنة بعد التطبيع."
            )

    @property
    def uncovered_share(self) -> float:
        """نسبةُ غير المغطّى إلى جانب «مقاييس» **عند هذا المقام** لا قبله."""

        return self.maqayis_only / self.maqayis_size if self.maqayis_size else 0.0

    @property
    def reverse_uncovered_share(self) -> float:
        """نسبةُ الفجوة العكسية إلى جانب المدوَّنة عند هذا المقام."""

        return self.qac_only / self.qac_size if self.qac_size else 0.0


@dataclass(frozen=True, slots=True)
class StageFusions:
    """ثمنُ مقامٍ في الجانبين: الانصهاراتُ بأعيانها لا عددُها وحدَه."""

    stage_name: str
    maqayis_fusions: tuple[FusionRecord, ...]
    qac_fusions: tuple[FusionRecord, ...]

    def __post_init__(self) -> None:
        if not self.stage_name.strip():
            raise OverlapCensusError("انصهاراتٌ بلا اسم مقامها لا تُنسَب إلى قاعدة.")

    @property
    def maqayis_distinctions_lost(self) -> int:
        """عددُ التمييزات المُتلَفة في جانب «مقاييس» عند هذا المقام."""

        return sum(fusion.lost_distinctions for fusion in self.maqayis_fusions)

    @property
    def qac_distinctions_lost(self) -> int:
        """عددُ التمييزات المُتلَفة في جانب المدوَّنة عند هذا المقام."""

        return sum(fusion.lost_distinctions for fusion in self.qac_fusions)


def overlap_readouts(
    maqayis: Iterable[str],
    qac: Iterable[str],
    stages: Iterable[OverlapStage] = OVERLAP_STAGES,
) -> tuple[OverlapReadout, ...]:
    """قراءاتُ المقامات كلِّها دفعةً واحدة، مرتَّبةً بترتيب تجميدها.

    ولا تُستدعى لمقامٍ واحد: الوسيطُ `stages` يُفحَص أن يكون المقاماتِ
    المُجمَّدةَ كلَّها، لأنّ إخراجَ رقمِ ما بعد التطبيع وحدَه يُخفي أنّ
    قاعدةً صنعته — وهو بعينه ما اشترط الطلبُ إظهارَه.
    """

    requested = tuple(stages)
    if requested != tuple(OVERLAP_STAGES):
        raise OverlapCensusError(
            "المقاماتُ تُقرأ كلُّها معًا بترتيبها المُجمَّد؛ ومقامٌ يخرج وحدَه "
            "يُقرأ رقمًا بلا قاعدةٍ صنعته."
        )
    maqayis_forms = tuple(maqayis)
    qac_forms = tuple(qac)
    if not maqayis_forms or not qac_forms:
        raise OverlapCensusError("جانبٌ فارغٌ لا يُقاس تقاطعُه؛ والصفرُ هنا عطلُ قراءة.")
    readouts: list[OverlapReadout] = []
    for stage in requested:
        left = set(_staged_forms(maqayis_forms, stage, transliterate=False).values())
        right = set(_staged_forms(qac_forms, stage, stage.transliterates_qac).values())
        shared = left & right
        readouts.append(
            OverlapReadout(
                stage_name=stage.name,
                maqayis_size=len(left),
                qac_size=len(right),
                intersection=len(shared),
                maqayis_only=len(left - right),
                qac_only=len(right - left),
            )
        )
    return tuple(readouts)


def readout_at(readouts: Iterable[OverlapReadout], stage_name: str) -> OverlapReadout:
    """يختار قراءةً من ناتجٍ كامل؛ ولا يحسب مقامًا مفردًا من البايتات."""

    for readout in readouts:
        if readout.stage_name == stage_name:
            return readout
    raise OverlapCensusError(f"لا قراءةَ بهذا المقام في الناتج: {stage_name}")


def stage_fusions(
    maqayis: Iterable[str],
    qac: Iterable[str],
    stages: Iterable[OverlapStage] = OVERLAP_STAGES,
) -> tuple[StageFusions, ...]:
    """انصهاراتُ كلِّ مقامٍ في الجانبين: ثمنُ التطبيع معروضًا بأعيانه."""

    maqayis_forms = tuple(maqayis)
    qac_forms = tuple(transliterate_root(form) for form in qac)
    records: list[StageFusions] = []
    for stage in stages:
        if not stage.rules:
            records.append(
                StageFusions(stage_name=stage.name, maqayis_fusions=(), qac_fusions=())
            )
            continue
        records.append(
            StageFusions(
                stage_name=stage.name,
                maqayis_fusions=fusions_under(maqayis_forms, stage.rules),
                qac_fusions=fusions_under(qac_forms, stage.rules),
            )
        )
    return tuple(records)
