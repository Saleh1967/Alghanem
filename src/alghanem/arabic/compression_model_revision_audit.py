"""تدقيقُ مراجعةٍ لأرقامٍ سابقةٍ: ما بطل، ولماذا بطل، وما الذي يمنع عودته.

الرقمُ الخاطئُ يُسجَّل ولا يُمحى. المحوُ يُخفي الدرسَ ويُبقي البابَ الذي دخل
منه الخطأُ مفتوحًا؛ والتسجيلُ يجعل القاعدةَ التي سدّته مقروءةً مع سببها.

`ASupersededNumberIsRecordedNotErased`: لكلّ روايةٍ باطلةٍ صفٌّ يحمل الرقمَ
كما قيل، وسببَ بطلانه، والقاعدةَ البنيويّة التي تمنع تكرارَه — لا اعتذارًا.

`TheDefectIsInTheDeclarationNotAlwaysInTheArithmetic`: روايتان من الثلاث كان
حسابُهما صحيحًا وإنّما كان **المُصرَّحُ به** ناقصًا: الأولى قِيست على تمثيلٍ
أسقط الحركات فكانت صحيحةً عن نصفِ المعلومة، والثانية ذكرت الحمولةَ وحدها
وقُدِّمت كأنّها حجمُ الملفّ القابل لفكّ الترميز. فالتدقيقُ يلاحق التصريحَ لا
العمليّةَ الحسابيّة وحدها.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

__all__ = [
    "ADAPTIVE_CODING_DISSOLVES_THE_TABLE_QUESTION_NOTE",
    "AN_UNISSUED_FIGURE_IS_NOT_A_RESULT_NOTE",
    "A_SUPERSEDED_NUMBER_IS_RECORDED_NOT_ERASED_NOTE",
    "REPORTED_PILOT_LINEAGE",
    "SUPERSEDED_COMPRESSION_CLAIMS",
    "IssuanceStanding",
    "ReportedPilotFigure",
    "SupersededCompressionClaim",
]


@dataclass(frozen=True, slots=True)
class SupersededCompressionClaim:
    """روايةٌ باطلةٌ: ما قيل، وما صار، ولمَ بطل، وما يمنع عودته."""

    superseded_figure: str
    corrected_figure: str
    defect: str
    structural_closure: str


SUPERSEDED_COMPRESSION_CLAIMS: Final[tuple[SupersededCompressionClaim, ...]] = (
    SupersededCompressionClaim(
        superseded_figure="44.85% / 50.03% (ARABIC-COMPRESSION-MODEL-PILOT-1)",
        corrected_figure="68.8837% رتبةَ صفرٍ و78.7818% رتبةً أولى، حمولةً",
        defect=(
            "قِيس على تمثيلٍ مُعاد بناؤه من `units.json` أسقط الحركات، فأُحصيت "
            "٣٦ رمزًا لا ٥١؛ فكان الحسابُ صحيحًا على نصف المعلومة وخاطئًا عن الكلّ"
        ),
        structural_closure=(
            "مدخلُ القياس صار بايتاتٍ خامًّا يُتحقَّق من طولها وبصمتها قبل فكّ "
            "ترميزها، ولا تقبل دالّةُ قياسٍ واحدةٌ تمثيلًا وسيطًا"
        ),
    ),
    SupersededCompressionClaim(
        superseded_figure="78.78% مذكورًا مجرَّدًا كأنّه حجمُ الملفّ",
        corrected_figure="78.7818% حمولةً، و78.5774% كلّيًّا شاملًا الجداول",
        defect=(
            "رقمُ الحمولة المرمَّزة قُدِّم بلا التصريح بأنّه لا يُفَكّ إلا بمعرفةٍ "
            "مسبقةٍ بالشفرة لم تُحسَب في الحجم"
        ),
        structural_closure=(
            "`ModelMeasurement` يحمل الحمولةَ والجدولَ معًا، و`as_two_sizes` "
            "لا يُخرج أحدَهما دون الآخر"
        ),
    ),
    SupersededCompressionClaim(
        superseded_figure="78.45% حجمًا كلّيًّا لرتبةٍ أولى",
        corrected_figure="78.5774% (جدولٌ 21,589 بت لا ~35,342)",
        defect=(
            "قُدِّر الجدولُ تقديرًا بتمثيلٍ غير قانونيٍّ للشفرة بدل اشتقاقه من "
            "الشفرة القانونيّة المستعملة في القياس نفسه"
        ),
        structural_closure=(
            "حجمُ الجدول يُشتَقّ من `code_lengths` عينِها التي رُمِّزت بها "
            "الحمولة، فلا يبقى تقديرٌ مستقلٌّ يخالف ما رُمِّز فعلًا"
        ),
    ),
    SupersededCompressionClaim(
        superseded_figure="«حسمُ التعادل أضعفُ نقطةٍ في أرقام الحمولة»",
        corrected_figure=(
            "الحمولةُ ثابتةٌ تحت أيّ قاعدةِ تعادل (3,285,636 و2,240,471 مقيسَين "
            "بقاعدتين متعاكستين)، والمتحرّكُ هو الجدولُ وحده (21,589 مقابل 21,587)"
        ),
        defect=(
            "نُسِبت عدمُ القطعيّة إلى الرقم الخطأ: كلفةُ هفمان أمثلُ فهي وحيدةٌ "
            "عدديًّا مهما تعدّدت الأشجارُ المثلى، ومجموعُ الأطوال هو المتعدّد"
        ),
        structural_closure=(
            "قاعدةُ `MINIMAL_TABLE` (التردّد، ثمّ أقلُّ عمق، ثمّ أقلُّ عددِ "
            "أوراق، ثمّ أصغرُ نقطةِ كود) كليّةٌ ولا تترك تعادلًا، وتفضيلُ الأقلّ "
            "عمقًا يُصغِّر مجموعَ الأطوال فيبلغ الجدولُ أصغرَ ما يبلغه بين "
            "الأشجار المثلى"
        ),
    ),
)


A_SUPERSEDED_NUMBER_IS_RECORDED_NOT_ERASED_NOTE: Final[str] = (
    "ASupersededNumberIsRecordedNotErased: الرقمُ الباطلُ يبقى مكتوبًا بسببه "
    "وبالقاعدة التي سدّته؛ فمحوُه يُخفي الدرسَ ويُبقي بابَه مفتوحًا"
)


class IssuanceStanding(Enum):
    """منزلةُ الإصدار. `ISSUED` وحدها تعني رقمًا يجوز الاستشهادُ به نتيجةً."""

    ISSUED = "مُصدَر"
    NOT_ISSUED_NO_DECLARED_ROUND_TRIP = "غيرُ مُصدَر: لا مطابقةَ مُصرَّحٌ بها"
    NOT_ISSUED_NO_CORPUS_DIGEST = "غيرُ مُصدَر: لا بصمةَ للبايتات المقيسة"


@dataclass(frozen=True, slots=True)
class ReportedPilotFigure:
    """رقمٌ وارِدٌ في نصٍّ خارجيّ: منزلتُه في الإصدار، وما ينقصه لِيُصدَر."""

    pilot: str
    model: str
    reported_ratio: str
    standing: IssuanceStanding
    what_is_missing: str


REPORTED_PILOT_LINEAGE: Final[tuple[ReportedPilotFigure, ...]] = (
    ReportedPilotFigure(
        pilot="PILOT-1",
        model="هفمان رتبة صفر/أولى على تمثيلٍ مُعادِ بناءٍ أسقط الحركات",
        reported_ratio="44.85% / 50.03%",
        standing=IssuanceStanding.NOT_ISSUED_NO_CORPUS_DIGEST,
        what_is_missing=(
            "قِيست على نصفِ المعلومة؛ وسببُ بطلانها مُسجَّلٌ في "
            "`SUPERSEDED_COMPRESSION_CLAIMS`"
        ),
    ),
    ReportedPilotFigure(
        pilot="PILOT-2",
        model="هفمان رتبة صفر على النصّ الحرفيّ الكامل",
        reported_ratio="68.8837% حمولةً / 68.8674% كلّيًّا",
        standing=IssuanceStanding.ISSUED,
        what_is_missing="لا شيء: البصمةُ مُجمَّدةٌ والمطابقةُ محقَّقة",
    ),
    ReportedPilotFigure(
        pilot="PILOT-2",
        model="هفمان رتبة أولى بالجوار الحرفيّ",
        reported_ratio="78.7818% حمولةً / 78.5774% كلّيًّا",
        standing=IssuanceStanding.ISSUED,
        what_is_missing="لا شيء: البصمةُ مُجمَّدةٌ والمطابقةُ محقَّقة",
    ),
    ReportedPilotFigure(
        pilot="PILOT-3",
        model="ترميزٌ حسابيٌّ تكيّفيّ، سياقُ رتبةٍ أولى",
        reported_ratio="85.11%",
        standing=IssuanceStanding.NOT_ISSUED_NO_DECLARED_ROUND_TRIP,
        what_is_missing="مطابقةٌ محقّقةٌ مُصرَّحٌ بها، وبصمةُ البايتات المقيسة",
    ),
    ReportedPilotFigure(
        pilot="PILOT-4",
        model="ترميزٌ حسابيٌّ تكيّفيّ، مزجُ رتبتين",
        reported_ratio="87.67%",
        standing=IssuanceStanding.NOT_ISSUED_NO_DECLARED_ROUND_TRIP,
        what_is_missing="مطابقةٌ محقّقةٌ مُصرَّحٌ بها، وبصمةُ البايتات المقيسة",
    ),
    ReportedPilotFigure(
        pilot="PILOT-5",
        model="مزجُ ثلاث رتبٍ، تشكيلةٌ غيرُ (7,4,1)",
        reported_ratio="88.01%",
        standing=IssuanceStanding.NOT_ISSUED_NO_DECLARED_ROUND_TRIP,
        what_is_missing="مطابقةٌ محقّقةٌ مُصرَّحٌ بها، وبصمةُ البايتات المقيسة",
    ),
    ReportedPilotFigure(
        pilot="PILOT-5",
        model="مزجُ ثلاث رتبٍ، ترتيب (7,4,1)، K=5",
        reported_ratio="88.34%",
        standing=IssuanceStanding.NOT_ISSUED_NO_CORPUS_DIGEST,
        what_is_missing=(
            "المطابقةُ مُصرَّحٌ بتحقّقها لهذه التشكيلة وحدها، لكنّ بصمةَ "
            "البايتات المقيسة لم تُذكَر؛ فلا يُعرَف أهي بايتاتُ `FROZEN_CORPUS` "
            "نفسُها أم غيرُها. ولا يُقاس رقمٌ على نصٍّ لا بصمةَ له"
        ),
    ),
)


AN_UNISSUED_FIGURE_IS_NOT_A_RESULT_NOTE: Final[str] = (
    "AnUnissuedFigureIsNotAResult: الرقمُ بلا مطابقةٍ محقّقةٍ أو بلا بصمةِ "
    "بايتاتٍ يُسجَّل بوصفه **ما وَرَد**، لا بوصفه ما قِيس؛ فالفرقُ بين "
    "«٨٨٪» و«قيل ٨٨٪» هو الفرقُ كلُّه"
)

ADAPTIVE_CODING_DISSOLVES_THE_TABLE_QUESTION_NOTE: Final[str] = (
    "AdaptiveCodingDissolvesTheTableQuestion: الترميزُ التكيّفيُّ يُلغي سؤالَ "
    "الجدول **بنيويًّا** لا التفافًا: لا نموذجَ يُنقَل أصلًا، إذ يُعاد بناؤه "
    "أثناء فكّ الترميز من البايتات المفكوكة نفسها، فيسقط الفرقُ بين الحمولة "
    "والكلّيّ لانعدام أحد طرفيه. لكنّه ينقل القطعيّةَ إلى موضعٍ آخر: إلى "
    "الحساب. فأيُّ عائمٍ في تحديث الاحتمالات يجعل فكَّ الترميز تابعًا لمنصّةِ "
    "التنفيذ، ولا يُصدَر رقمٌ من حسابٍ غيرِ صحيحٍ بالكامل. ويلزم تجميدُ K "
    "وترتيبِ المزج وSCALE بندًا مُجمَّدًا قبل القياس لا بعده"
)
