"""إحصاءُ الشواهد في جدول «مقاييس اللغة»، وعرضُ خلافِ عدٍّ صرّح به الملفُّ نفسُه.

**ما تفعله هذه الوحدة**: تُعيد اشتقاقَ أرقامٍ من البايتات المُبصَّمة الحاضرة
في الشجرة (`maqayis_by_root_csv_999.csv`)، لا من بايتاتٍ منتظَرة: عددَ
السجلّات الحاملة شاهدًا شعريًّا، وعددَ مقاطع الشواهد، وقسمةَ السجلّات على
قيم `root_type`، وموقفَ `axes_count` المُصرَّح به في الملفّ من محتوى
`semantic_axes` في السجلّ نفسِه.

`THE_BYTES_HERE_ARE_NOT_THE_WITHHELD_BYTES`: بايتاتُ MASAQ لم تصل بعدُ، وما
يتعلّق بها باقٍ على `skipped` بشرطِ البايتات لا بمتغيّر بيئة. وهذه الوحدةُ لا
تُعوّض عنها ولا تُقاس بها: مصدرُها ملفٌّ آخرُ مُبصَّمٌ في هذه الشجرة، وأرقامُها
أرقامُه وحدَه. فبلوغُ رقمٍ هنا لا يرفع تعذُّرَ رقمٍ هناك.

`NO_CLAIM_PRECEDED_THESE_NUMBERS`: أرقامُ `irab_column_preregistration` كان
يسبقها نصٌّ واردٌ يُسمّيها، فكانت المطابقةُ فيها اختبارًا لمُرسِل. وأرقامُ هذه
الوحدة **لم يسبقها مُدَّعٍ**: هي مقيسةٌ هنا أوّلَ مرّة. فليس في مطابقتها نصرٌ
على أحد، وليس في مخالفتها تكذيبُ أحد؛ المرفوعُ بها أنّ العددَ صار مشدودًا إلى
بصمةٍ وقاعدةٍ فيُعاد اشتقاقُه، لا أنّ دعوى صُدِّقت.

`THE_RULES_WERE_WRITTEN_AFTER_THESE_NUMBERS_WERE_SEEN`: قواعدُ العدّ هنا
صيغت **بعد** النظر في الملفّ، لا قبله؛ وهذا يُسجَّل لا يُطوى. ومقتضاه أنّ
القاعدةَ قد تكون فُصِّلت على مقاس رقمٍ مُستحسَن، فلا تُقرأ هذه الأرقامُ
تنبّؤًا تحقّق. وما يعصمها من ذلك شيءٌ واحد: أنّ كلَّ رقمٍ يُعاد اشتقاقُه من
بايتاتٍ مُبصَّمةٍ بقاعدةٍ مكتوبةٍ بحروفها، فمن خالف القاعدةَ ردّ الرقمَ بها.

`A_SEPARATOR_IS_THE_PRODUCERS_NOT_THE_POETS`: القضيبُ `|` فاصلٌ وضعه مُنتِجُ
الملفّ بين الشواهد، وليس علامةً في الشعر؛ والنقاطُ `…` علامةُ الفصل بين
الصدر والعجز عنده كذلك. فعدُّ المقاطع عدُّ فواصلِ مُنتِجٍ، وقضيبٌ يقع داخل
بيتٍ يزيد المقطعَ مقطعًا بلا شاهدٍ زائد. وليس هذا تخمينًا مُهمَلًا: يُقاس
معه `SEGMENTS_BEARING_THE_HEMISTICH_MARKER`، فإن ساوى عددَ المقاطع فليس في
الملفّ مقطعٌ بلا علامةِ فصل.

`A_WITNESS_SEGMENT_IS_NOT_A_VERSE`: المقطعُ وحدةُ نصٍّ بين فاصلين، وليس
«بيتًا» ولا «شاهدًا» بالمعنى النحويّ: لم يُحقَّق وزنُه ولا نسبتُه ولا أنّه
تامٌّ، ولا يُقرأ منه أنّ ابن فارس استشهد به. فـ٤٬١٧٦ عددُ مقاطعَ في ملفّ، لا
عددُ شواهدَ في العربية ولا عند ابن فارس.

`A_BLANK_IS_NOT_A_ZERO`: خليّةُ `axes_count` الفارغةُ ليست إعلانَ صفر، وخليّةُ
`semantic_axes` الفارغةُ ليست إعلانَ «لا محور له»؛ الفراغُ غيابُ تصريحٍ لا
تصريحٌ بغياب. ولذلك تُفرَز الفوارغُ صنفًا قائمًا بذاته، ولا تُجمَع إلى
المُخالِف ولا إلى المُطابِق.

`A_DECLARED_CELL_IS_CHECKED_AGAINST_ITS_OWN_FILE`: `axes_count` رقمٌ صرّح به
الملفُّ عن سجلٍّ من سجلّاته، فيُقابَل بمحتوى `semantic_axes` في السجلّ نفسِه.
والخلافُ إذا وقع يُعرَض بعدده وصنفه ولا يُطوى بترجيحِ أحد الطرفين: لا
يُعدَّل الرقمُ المُصرَّحُ به في الملفّ، ولا تُبدَّل قاعدةُ الفصل حتّى يستوي
العددان.

`THIS_IS_A_CENSUS_NOT_AN_INTERPRETATION`: لا تُقرأ بهذه الوحدة دلالةُ محورٍ،
ولا صحّةُ نسبةِ شاهد، ولا تصنيفُ جذرٍ؛ ولا استيرادَ من `kernel/`، ولا ولادةَ
ولا حكمَ ولادة.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Final

from .maqayis_root_table_deposit import (
    MaqayisRootTableError,
    root_table_rows,
)

__all__ = [
    "AXES_AGREEMENT_COUNTING_RULE",
    "A_BLANK_IS_NOT_A_ZERO_NOTE",
    "A_DECLARED_CELL_IS_CHECKED_AGAINST_ITS_OWN_FILE_NOTE",
    "A_SEPARATOR_IS_THE_PRODUCERS_NOT_THE_POETS_NOTE",
    "A_WITNESS_SEGMENT_IS_NOT_A_VERSE_NOTE",
    "BLANK_AXES_WITH_A_DECLARED_ONE",
    "FROZEN_AXES_AGREEMENT",
    "HEMISTICH_MARKER",
    "MAQAYIS_WITNESS_NAMED_RESIDUALS",
    "MEASURED_WITNESS_FIGURES",
    "NO_CLAIM_PRECEDED_THESE_NUMBERS_NOTE",
    "RECORDS_CARRYING_POETRY_EVIDENCE",
    "ROOT_TYPE_CENSUS",
    "ROOT_TYPE_COUNTING_RULE",
    "SEGMENTS_BEARING_THE_HEMISTICH_MARKER",
    "THE_BYTES_HERE_ARE_NOT_THE_WITHHELD_BYTES_NOTE",
    "THE_RULES_WERE_WRITTEN_AFTER_THESE_NUMBERS_WERE_SEEN_NOTE",
    "WITNESS_RECORD_COUNTING_RULE",
    "WITNESS_SEGMENTS",
    "WITNESS_SEGMENT_COUNTING_RULE",
    "WITNESS_SEPARATOR",
    "AxesAgreement",
    "AxesStanding",
    "MeasuredWitnessFigure",
    "count_blank_axes_with_a_declared_one",
    "count_records_carrying_poetry_evidence",
    "count_segments_bearing_the_hemistich_marker",
    "count_witness_segments",
    "measure_axes_agreement",
    "rederive_root_type_census",
    "split_witness_segments",
    "weigh_declared_axes_count",
]


WITNESS_SEPARATOR: Final[str] = "|"
"""الفاصلُ الذي وضعه مُنتِجُ الملفّ بين شاهدٍ وشاهد، لا علامةٌ في الشعر."""

HEMISTICH_MARKER: Final[str] = "…"
"""علامةُ الفصل بين الصدر والعجز عند مُنتِج الملفّ، تُقاس ولا تُفترَض."""


WITNESS_RECORD_COUNTING_RULE: Final[str] = (
    "السجلُّ حاملٌ لشاهدٍ إن كانت خليّةُ `poetry_evidence` فيه غيرَ فارغةٍ بعد "
    "حذف الفراغ من طرفيها؛ والفراغُ غيابُ تصريحٍ لا تصريحٌ بأن لا شاهدَ "
    "للجذر، فالعددُ عددُ سجلّاتٍ صرّحت لا عددُ جذورٍ لها شواهد"
)

WITNESS_SEGMENT_COUNTING_RULE: Final[str] = (
    "المقطعُ ما بين فاصلَي `|` في خليّة `poetry_evidence`، مُهمَلًا منه ما "
    "كان فراغًا خالصًا. والفاصلُ من وضع مُنتِج الملفّ لا من الشعر، فقضيبٌ "
    "وقع داخل بيتٍ يزيد المقطعَ مقطعًا؛ ولذلك يُقاس معه عددُ المقاطع الحاملة "
    "لعلامة الفصل `…`، فتساويهما قرينةٌ على أنّ الفصلَ وقع حيث يُتوقَّع"
)

ROOT_TYPE_COUNTING_RULE: Final[str] = (
    "القسمةُ على قيم `root_type` كما وردت في الملفّ بحروفها، بلا توحيدِ "
    "همزةٍ ولا حذفِ تشكيلٍ ولا ضمِّ قيمةٍ إلى أقربِ اسمٍ إليها؛ والصفوفُ تُعَدّ "
    "صفوفًا لا جذورًا متمايزة. ومجموعُ الأقسام يساوي عددَ السجلّات بالضرورة، "
    "فاختلافُه دليلُ خللٍ في القراءة لا في القسمة"
)

AXES_AGREEMENT_COUNTING_RULE: Final[str] = (
    "يُقابَل `axes_count` المُصرَّحُ به في السجلّ بعدد مقاطع `semantic_axes` "
    "في السجلّ نفسِه، والمقطعُ ما بين فاصلَي `|` مُهمَلًا منه الفراغُ الخالص. "
    "ثمّ يُصنَّف السجلُّ بواحدٍ من ثلاثة: فارغُ التصريح إن خلت خليّةُ العدد، "
    "أو مُطابِقٌ، أو مُخالِفٌ. والفارغُ لا يُجمَع إلى واحدٍ من الآخرين، ولا "
    "يُقرأ صفرًا"
)


def split_witness_segments(cell: str) -> tuple[str, ...]:
    """مقاطعُ خليّةٍ تحت قاعدة الفصل المكتوبة، بلا تطبيعِ حرفٍ ولا حركة."""

    return tuple(
        segment for segment in cell.split(WITNESS_SEPARATOR) if segment.strip()
    )


def count_records_carrying_poetry_evidence(root: Path | None = None) -> int:
    """عددُ السجلّات الحاملة شاهدًا تحت `WITNESS_RECORD_COUNTING_RULE`."""

    return sum(1 for row in root_table_rows(root) if row["poetry_evidence"].strip())


def count_witness_segments(root: Path | None = None) -> int:
    """عددُ مقاطع الشواهد تحت `WITNESS_SEGMENT_COUNTING_RULE`."""

    return sum(
        len(split_witness_segments(row["poetry_evidence"]))
        for row in root_table_rows(root)
    )


def count_segments_bearing_the_hemistich_marker(root: Path | None = None) -> int:
    """عددُ المقاطع الحاملة لعلامة الفصل `…`؛ قرينةٌ على قاعدة الفصل لا عليها."""

    return sum(
        1
        for row in root_table_rows(root)
        for segment in split_witness_segments(row["poetry_evidence"])
        if HEMISTICH_MARKER in segment
    )


def rederive_root_type_census(root: Path | None = None) -> tuple[tuple[str, int], ...]:
    """قسمةُ السجلّات على `root_type` تحت قاعدتها، مرتَّبةً بالعدد ثمّ بالاسم."""

    tally = Counter(row["root_type"] for row in root_table_rows(root))
    return tuple(
        sorted(tally.items(), key=lambda item: (-item[1], item[0])),
    )


class AxesStanding:
    """موقفُ سجلٍّ من عدده المُصرَّح به: فارغُ التصريح، أو مُطابِق، أو مُخالِف."""

    BLANK: Final[str] = "فارغُ التصريح"
    AGREES: Final[str] = "مُطابِق"
    DIFFERS: Final[str] = "مُخالِف"


def weigh_declared_axes_count(row: dict[str, str]) -> str:
    """موقفُ سجلٍّ واحدٍ تحت `AXES_AGREEMENT_COUNTING_RULE`، بلا ترجيحِ طرف."""

    declared = row["axes_count"].strip()
    if not declared:
        return AxesStanding.BLANK
    if not declared.isdecimal():
        return AxesStanding.DIFFERS
    segments = len(split_witness_segments(row["semantic_axes"]))
    return AxesStanding.AGREES if segments == int(declared) else AxesStanding.DIFFERS


@dataclass(frozen=True, slots=True)
class AxesAgreement:
    """موقفُ الملفّ من عدده المُصرَّح به: ثلاثةُ أصنافٍ لا يُدمَج أحدُها في آخر.

    `A_BLANK_IS_NOT_A_ZERO`: `blank` صنفٌ قائمٌ لا نصفُ مطابقةٍ ولا نصفُ
    مخالفة؛ ولذلك لا تُشتَقّ نسبةُ مطابقةٍ من `agreeing / total` في هذه
    الوحدة، فالمقامُ نفسُه محلُّ نزاع.
    """

    agreeing: int
    differing: int
    blank: int

    def __post_init__(self) -> None:
        for field_name in ("agreeing", "differing", "blank"):
            if int(getattr(self, field_name)) < 0:
                raise MaqayisRootTableError("صنفٌ في موقف الأعمدة لا يكون سالبًا")

    @property
    def declared_records(self) -> int:
        """السجلّاتُ التي صرّحت بعددٍ أصلًا: المُطابِقُ والمُخالِفُ دون الفارغ."""

        return self.agreeing + self.differing

    @property
    def total_records(self) -> int:
        """جملةُ السجلّات المقروءة؛ تُطابَق بعدد سجلّات الملفّ فلا يسقط سجلّ."""

        return self.declared_records + self.blank


def measure_axes_agreement(root: Path | None = None) -> AxesAgreement:
    """موقفُ الملفّ كلِّه من `axes_count`، مُعادَ الاشتقاق من البايتات المُبصَّمة."""

    tally = Counter(weigh_declared_axes_count(row) for row in root_table_rows(root))
    return AxesAgreement(
        agreeing=tally[AxesStanding.AGREES],
        differing=tally[AxesStanding.DIFFERS],
        blank=tally[AxesStanding.BLANK],
    )


def count_blank_axes_with_a_declared_one(root: Path | None = None) -> int:
    """سجلّاتٌ خليّةُ محاورها فارغةٌ وعددُها المُصرَّحُ به «1»؛ أغلبُ المُخالِف."""

    return sum(
        1
        for row in root_table_rows(root)
        if row["axes_count"].strip() == "1" and not row["semantic_axes"].strip()
    )


RECORDS_CARRYING_POETRY_EVIDENCE: Final[int] = 1_944
"""١٬٩٤٤: سجلّاتٌ خليّةُ `poetry_evidence` فيها غيرُ فارغة، من ٤٬٥٧٦ سجلًّا."""

WITNESS_SEGMENTS: Final[int] = 4_176
"""٤٬١٧٦: مقاطعُ الشواهد تحت قاعدة الفصل، لا «شواهدُ» بالمعنى النحويّ."""

SEGMENTS_BEARING_THE_HEMISTICH_MARKER: Final[int] = 4_176
"""٤٬١٧٦: المقاطعُ الحاملةُ لعلامة الفصل `…` — ساوت جملةَ المقاطع.

وهذه قرينةٌ على أنّ الفصلَ بالقضيب وقع حيث يُتوقَّع: ليس في الملفّ مقطعٌ
واحدٌ خلا من علامة الفصل بين الصدر والعجز. ولا تُثبت القرينةُ أنّ كلَّ مقطعٍ
بيتٌ تامٌّ، ولا تنفي أن يكون قضيبٌ داخلَ بيتٍ قد شطره شطرين كِلاهما يحمل
العلامة؛ فهي ترفع احتمالًا ولا تُغلق البابَ.
"""

ROOT_TYPE_CENSUS: Final[tuple[tuple[str, int], ...]] = (
    ("ثلاثي", 4_089),
    ("مضاعف", 428),
    ("ثلاثي معتل", 56),
    ("رباعي مكرر", 3),
)
"""قسمةُ ٤٬٥٧٦ سجلًّا على أربع قيمٍ لـ`root_type`، بحروفها كما في الملفّ.

ومجموعُها ٤٬٥٧٦ بالضبط، وهو شاهدٌ على القراءة نفسِها: لو انشقّ سجلٌّ بسطرٍ
مضمَّنٍ أو التُهم بفاصلٍ لاختلّ المجموعُ قبل أن تختلّ الأقسام. و«ثلاثي» هنا
٤٬٠٨٩ صفًّا لا ٤٬٠٨٧، والفرقُ جذران مكرَّران بصفّين كما في
`TRILATERAL_ROOT_COUNTING_RULE`، فالقاعدتان تُقرآن معًا ولا تُقابَل إحداهما
بالأخرى.
"""

FROZEN_AXES_AGREEMENT: Final[AxesAgreement] = AxesAgreement(
    agreeing=2_890,
    differing=822,
    blank=864,
)
"""موقفُ الملفّ من عدده المُصرَّح به تحت `AXES_AGREEMENT_COUNTING_RULE`.

٢٬٨٩٠ مُطابِقًا، و٨٢٢ مُخالِفًا، و٨٦٤ ساكتًا؛ ومجموعُها ٤٬٥٧٦ فلا يسقط سجلّ.
والمخالفةُ لا تُقرأ خطأً في الملفّ ولا خطأً في القاعدة حتّى يقوم على أحدهما
شاهد؛ والمُودَعُ هنا الفرقُ بعدده لا تسويتُه.
"""

BLANK_AXES_WITH_A_DECLARED_ONE: Final[int] = 597
"""٥٩٧: سجلّاتٌ محاورُها خاليةٌ وعددُها المُصرَّحُ به «1» — أغلبُ المُخالِف.

وهذا الصنفُ وحدَه يُفسِّر ٥٩٧ من ٨٢٢ مُخالِفًا. ولا يُرفَع الخلافُ بأن
يُقرأ الفراغُ محورًا واحدًا غيرَ مكتوب، ولا بأن يُقرأ «1» خطأً في الملفّ:
كلاهما ترجيحٌ بلا شاهد، والمُودَعُ هنا الفرقُ بعدده لا تسويتُه.
"""


@dataclass(frozen=True, slots=True)
class MeasuredWitnessFigure:
    """رقمٌ لم يسبقه مُدَّعٍ: قيمتُه وقاعدتُه وحدُّ ما لا يُثبته، وسندُه بايتات.

    `NO_CLAIM_PRECEDED_THESE_NUMBERS`: بخلاف `RederivedSpecificationFigure`
    لا حقلَ هنا لدعوى ولا لموضعِها، لأنّه لا دعوى. ومقتضى ذلك أنّ الرقمَ لا
    يُقرأ تصديقًا ولا تكذيبًا لأحد، فحقلُ `what_it_still_does_not_establish`
    ألزمُ هاهنا منه هناك.
    """

    figure: str
    measured_count: int
    counting_rule: str
    what_it_still_does_not_establish: str

    def __post_init__(self) -> None:
        for field_name in (
            "figure",
            "counting_rule",
            "what_it_still_does_not_establish",
        ):
            if not str(getattr(self, field_name)).strip():
                raise MaqayisRootTableError(
                    "رقمٌ مقيسٌ بلا قاعدةِ عدٍّ أو بلا حدٍّ مكتوبٍ لما لا "
                    "يُثبته يُقرأ بعد جلساتٍ حكمًا، وليس إيّاه"
                )
        if self.measured_count < 0:
            raise MaqayisRootTableError("عددٌ مقيسٌ لا يكون سالبًا")


MEASURED_WITNESS_FIGURES: Final[tuple[MeasuredWitnessFigure, ...]] = (
    MeasuredWitnessFigure(
        figure="1,944",
        measured_count=RECORDS_CARRYING_POETRY_EVIDENCE,
        counting_rule=WITNESS_RECORD_COUNTING_RULE,
        what_it_still_does_not_establish=(
            "أنّ الجذورَ الباقيةَ (٢٬٦٣٢ سجلًّا) لا شواهدَ لها: الخليّةُ "
            "الفارغةُ غيابُ تصريحٍ في هذا الملفّ، لا نفيٌ في المعجم. ولا "
            "يُقرأ منه أنّ ١٬٩٤٤ جذرًا متمايزًا حملت شاهدًا، فالعدُّ على "
            "السجلّات وفي الملفّ جذورٌ بصفّين"
        ),
    ),
    MeasuredWitnessFigure(
        figure="4,176",
        measured_count=WITNESS_SEGMENTS,
        counting_rule=WITNESS_SEGMENT_COUNTING_RULE,
        what_it_still_does_not_establish=(
            "أنّ في الملفّ ٤٬١٧٦ بيتًا أو شاهدًا نحويًّا: المقطعُ وحدةُ نصٍّ "
            "بين فاصلَي مُنتِجٍ، لم يُحقَّق وزنُه ولا نسبتُه ولا تمامُه، ولا "
            "يُقرأ منه أنّ ابن فارس استشهد به ولا أنّ الشاهدَ صحيحُ الرواية"
        ),
    ),
    MeasuredWitnessFigure(
        figure="4,576 = 4,089 + 428 + 56 + 3",
        measured_count=4_576,
        counting_rule=ROOT_TYPE_COUNTING_RULE,
        what_it_still_does_not_establish=(
            "أنّ هذه القسمةَ قسمةُ الجذور العربيّة على أبنيتها: هي قيمُ عمودٍ "
            "في ملفٍّ صنّفها مُنتِجُه، ولا تُقرأ منها صحّةُ تصنيفِ جذرٍ واحدٍ "
            "بعينه. واستواءُ المجموع بعدد السجلّات شاهدٌ على سلامة القراءة "
            "وحدَها، لا على سلامة التصنيف"
        ),
    ),
    MeasuredWitnessFigure(
        figure="2,890 / 822 / 864",
        measured_count=4_576,
        counting_rule=AXES_AGREEMENT_COUNTING_RULE,
        what_it_still_does_not_establish=(
            "أيَّ الطرفين أصوبُ عند الخلاف: ٨٢٢ سجلًّا خالف فيها عددُ الملفّ "
            "المُصرَّحُ به مقاطعَ محاوره تحت قاعدة الفصل، ولا يُرفَع الخلافُ "
            "بتعديل الرقم ولا بتبديل القاعدة. و٨٦٤ فارغةً ليست ٨٦٤ جذرًا بلا "
            "محاور، ولا ٨٦٤ صفرًا، بل ٨٦٤ موضعَ سكوت"
        ),
    ),
)


THE_BYTES_HERE_ARE_NOT_THE_WITHHELD_BYTES_NOTE: Final[str] = (
    "TheBytesHereAreNotTheWithheldBytes: مصدرُ هذه الأرقام "
    "`maqayis_by_root_csv_999.csv` المُبصَّمُ الحاضرُ في الشجرة، لا "
    "`corpora/MASAQ.csv` المنتظَر؛ فما تعذّر هناك باقٍ على تعذُّره، "
    "واختباراتُه باقيةٌ على `skipped` بشرطِ بايتاتها. وبلوغُ رقمٍ من ملفٍّ "
    "لا يُغني عن بايتات ملفٍّ آخر ولا يُقاس بها"
)

NO_CLAIM_PRECEDED_THESE_NUMBERS_NOTE: Final[str] = (
    "NoClaimPrecededTheseNumbers: لم يسبق هذه الأرقامَ نصٌّ واردٌ يُسمّيها، "
    "بخلاف أرقام `irab_column_preregistration`؛ فليست مطابقتُها اختبارًا "
    "لمُرسِل، ولا مخالفتُها تكذيبًا له. المرفوعُ بها أنّها صارت مشدودةً إلى "
    "بصمةٍ وقاعدةٍ فتُعاد اشتقاقًا، لا أنّ دعوى صُدِّقت"
)

THE_RULES_WERE_WRITTEN_AFTER_THESE_NUMBERS_WERE_SEEN_NOTE: Final[str] = (
    "TheRulesWereWrittenAfterTheseNumbersWereSeen: صيغت قواعدُ العدّ هنا بعد "
    "النظر في الملفّ لا قبله، فلا تُقرأ هذه الأرقامُ تنبّؤًا تحقّق. ويعصمها "
    "من التفصيل على مقاسٍ مُستحسَنٍ أنّ كلَّ قاعدةٍ مكتوبةٌ بحروفها وكلَّ رقمٍ "
    "يُعاد اشتقاقُه من بايتاتٍ مُبصَّمة، فمن خالف القاعدةَ ردّ الرقمَ بها"
)

A_SEPARATOR_IS_THE_PRODUCERS_NOT_THE_POETS_NOTE: Final[str] = (
    "ASeparatorIsTheProducersNotThePoets: `|` و`…` علامتان من وضع مُنتِج "
    "الملفّ لا من الشعر؛ فعدُّ المقاطع عدُّ فواصلِه. وقد قِيس معه عددُ "
    "المقاطع الحاملة لعلامة الفصل فساواه (٤٬١٧٦ = ٤٬١٧٦)، وهي قرينةٌ ترفع "
    "احتمالَ فاصلٍ في غير موضعه ولا تُغلق البابَ عليه"
)

A_WITNESS_SEGMENT_IS_NOT_A_VERSE_NOTE: Final[str] = (
    "AWitnessSegmentIsNotAVerse: المقطعُ وحدةُ نصٍّ بين فاصلين لا بيتٌ ولا "
    "شاهدٌ نحويّ؛ لم يُحقَّق وزنُه ولا نسبتُه ولا تمامُه. فـ٤٬١٧٦ عددُ مقاطعَ "
    "في ملفّ، لا عددُ شواهدَ في العربية ولا عند ابن فارس"
)

A_BLANK_IS_NOT_A_ZERO_NOTE: Final[str] = (
    "ABlankIsNotAZero: الخليّةُ الفارغةُ غيابُ تصريحٍ لا تصريحٌ بغياب؛ "
    "فـ٨٦٤ سجلًّا فارغَ `axes_count` صنفٌ ثالثٌ لا يُجمَع إلى المُطابِق ولا "
    "إلى المُخالِف، ولا تُشتَقّ نسبةُ مطابقةٍ على مقامٍ يضمّه"
)

A_DECLARED_CELL_IS_CHECKED_AGAINST_ITS_OWN_FILE_NOTE: Final[str] = (
    "ADeclaredCellIsCheckedAgainstItsOwnFile: `axes_count` رقمٌ صرّح به "
    "الملفُّ عن سجلٍّ من سجلّاته، فقوبل بمحتوى `semantic_axes` في السجلّ "
    "نفسِه: طابق في ٢٬٨٩٠ وخالف في ٨٢٢ وسكت في ٨٦٤. والفرقُ يُعرَض بعدده "
    "وصنفه (٥٩٧ منه محاورُها خاليةٌ وعددُها «1») ولا يُسوّى بترجيحِ طرف"
)

MAQAYIS_WITNESS_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "TheBytesHereAreNotTheWithheldBytes": (
        THE_BYTES_HERE_ARE_NOT_THE_WITHHELD_BYTES_NOTE
    ),
    "NoClaimPrecededTheseNumbers": NO_CLAIM_PRECEDED_THESE_NUMBERS_NOTE,
    "TheRulesWereWrittenAfterTheseNumbersWereSeen": (
        THE_RULES_WERE_WRITTEN_AFTER_THESE_NUMBERS_WERE_SEEN_NOTE
    ),
    "ASeparatorIsTheProducersNotThePoets": (
        A_SEPARATOR_IS_THE_PRODUCERS_NOT_THE_POETS_NOTE
    ),
    "AWitnessSegmentIsNotAVerse": A_WITNESS_SEGMENT_IS_NOT_A_VERSE_NOTE,
    "ABlankIsNotAZero": A_BLANK_IS_NOT_A_ZERO_NOTE,
    "ADeclaredCellIsCheckedAgainstItsOwnFile": (
        A_DECLARED_CELL_IS_CHECKED_AGAINST_ITS_OWN_FILE_NOTE
    ),
}
"""المخلَّفاتُ المسمّاةُ لهذه الوحدة، مفحوصةٌ في الاختبارات فلا تبقى زينةً."""
