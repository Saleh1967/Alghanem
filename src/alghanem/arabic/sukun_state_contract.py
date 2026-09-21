"""عقدُ حالةِ السكون: مكتوبٌ ومستنتَجٌ حالتان، وأوّلُ زوجِ الشدّة ليس منهما.

**أوّلًا: وما كان تقريرًا يصير عقدًا.** قاس `implicit_sukun_treatment`
عمودَ السكون بأربعة مصادر وسمّاها ولم يحكم بينها، وزاده `sukun_second_scope`
وديعةً ثانية. وههنا يُحوَّل المقيسُ إلى **عقد حالة**: أيُّ المصادر يدخل فضاءَ
الحالات، وبأيّ اسمٍ يدخل، وأيُّها يُخرَج منه رأسًا
(`A_CENSUS_IS_NOT_A_STATE_SPACE_UNTIL_ITS_COLUMN_IS_SPLIT`).

**وثانيًا: والسكونُ حالتان لا حالة.**

\\[
\\text{WRITTEN\\_SUKUN} \\;\\neq\\; \\text{INFERRED\\_SUKUN}
\\]

فالمكتوبُ شاهدُه في المِداد، والمستنتَجُ شاهدُه في قاعدةٍ لنا. وجمعُهما في
حالةٍ واحدةٍ يجعل قرارَنا نحن بيّنةً من النصّ، وهو بعينه الخلطُ الذي أُغلِق
فرعُ الأثر المعجميّ لأجله (`THE_WRITTEN_AND_THE_INFERRED_ARE_NOT_ONE_STATE`).

**وثالثًا: وأوّلُ زوجِ الشدّة يُخرَج بالكامل.** ليس سكونًا مكتوبًا ولا
مستنتَجًا، بل نصفُ حرفٍ مضعَّفٍ؛ فمقولتُه غيرُ مقولةِ السكون، ويُنقَل إلى
`NonSukunCategory` لا إلى قسمٍ ثالثٍ من السكون
(`THE_FIRST_HALF_OF_A_GEMINATE_IS_EVICTED_NOT_SUBCLASSED`).

| الوديعة | مكتوب | مستنتَج | مُخرَج | العمودُ الخام |
|---|---|---|---|---|
| الفاتحة | ٢١ | ٤٠ | ١٤ | ٧٥ |
| آيةُ الفتح | ٢٧ | ٦١ | ١٦ | ١٠٤ |

والمستنتَجُ هو الألفُ بلا علامةٍ والحاملُ العاري مجموعَين:
\\(23+17=40\\) و\\(33+28=61\\)؛ وهو المقدارُ الذي سمّاه ما سبق «الضمنيَّ ناقصَ
أوائلِ الأزواج».

**ورابعًا: والعمودُ الخامُ لا يُصدَر رقمًا واحدًا.** `refuse_a_merged_total`
ترفض دائمًا، لأنّ ٧٥ و١٠٤ مجموعُ ثلاثِ مقولاتٍ لا مقدارُ حالةٍ واحدة؛ ومن
حمَلها على «عدد السكون» فقد أدخل المضعَّفَ والقرارَ والمِدادَ في خانةٍ واحدة
(`NO_SINGLE_SUKUN_TOTAL_IS_ISSUED_FROM_A_THREE_WAY_COLUMN`).

**وخامسًا: ولا حالةَ قبل هذا الفصل.** `the_state_space_of` لا تُصدِر إلّا
الحالتَين، وحارسُ الاستيراد يمنع دخولَ المُخرَج فيهما؛ فأيُّ بناءٍ يطلب
«السكونَ» حالةً يجد حالتَين مفصولتَين أو لا يجد شيئًا
(`NOTHING_ENTERS_A_STATE_SPACE_AS_SUKUN_BEFORE_THIS_SPLIT`).

ولا سلطةَ لهذه الوحدة: لا ولادةَ، ولا تجميدَ، ولا استيرادَ من `kernel/`،
ولا اسمَ احتمالٍ ولا انتقالٍ ولا انتروبيا فيها.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from functools import cache
from typing import Final

from alghanem.arabic.implicit_sukun_treatment import (
    SukunCensus,
    SukunSource,
    measured_text_census,
)
from alghanem.arabic.sukun_second_scope import second_text_census

__all__ = [
    "A_CENSUS_IS_NOT_A_STATE_SPACE_UNTIL_ITS_COLUMN_IS_SPLIT",
    "NOTHING_ENTERS_A_STATE_SPACE_AS_SUKUN_BEFORE_THIS_SPLIT",
    "NO_SINGLE_SUKUN_TOTAL_IS_ISSUED_FROM_A_THREE_WAY_COLUMN",
    "SUKUN_STATE_NAMED_RESIDUALS",
    "THE_FIRST_HALF_OF_A_GEMINATE_IS_EVICTED_NOT_SUBCLASSED",
    "THE_WRITTEN_AND_THE_INFERRED_ARE_NOT_ONE_STATE",
    "NonSukunCategory",
    "SukunState",
    "SukunStateContractError",
    "SukunStateSplit",
    "the_state_space_of",
    "the_sukun_splits",
    "split_of",
    "refuse_a_merged_total",
]


class SukunStateContractError(ValueError):
    """رفضٌ عند عقد الحالة: دمجُ عمودٍ، أو إدخالُ مُخرَجٍ في فضاء الحالات."""


class SukunState(Enum):
    """حالتا السكون؛ ولا ثالثةَ لهما، ولا تُجمَعان في واحدة."""

    WRITTEN_SUKUN = "سكونٌ مكتوب"
    INFERRED_SUKUN = "سكونٌ مستنتَج"


class NonSukunCategory(Enum):
    """ما خرج من العمود إلى مقولته؛ لا يدخل فضاءَ حالات السكون بحال."""

    GEMINATION_FIRST_HALF = "النصفُ الأوّلُ من مضعَّف"


# --- البقايا المسمّاة ------------------------------------------------------

A_CENSUS_IS_NOT_A_STATE_SPACE_UNTIL_ITS_COLUMN_IS_SPLIT: Final[str] = (
    "A_CENSUS_IS_NOT_A_STATE_SPACE_UNTIL_ITS_COLUMN_IS_SPLIT: الإحصاءُ يسمّي "
    "المصادرَ ولا يقسم فضاءَ الحالات؛ وما لم يُقَل أيُّ مصدرٍ حالةٌ وأيُّه "
    "مُخرَجٌ بقي العمودُ تقريرًا لا عقدًا، ولا يُبنى على تقريرٍ فضاءُ حالات"
)

THE_WRITTEN_AND_THE_INFERRED_ARE_NOT_ONE_STATE: Final[str] = (
    "THE_WRITTEN_AND_THE_INFERRED_ARE_NOT_ONE_STATE: شاهدُ المكتوب في المِداد "
    "وشاهدُ المستنتَج في قاعدةٍ لنا؛ فجمعُهما في حالةٍ واحدةٍ يحوّل قرارَنا "
    "إلى بيّنةٍ من النصّ، وهو الخلطُ الذي أُغلِق لأجله فرعُ الأثر المعجميّ"
)

THE_FIRST_HALF_OF_A_GEMINATE_IS_EVICTED_NOT_SUBCLASSED: Final[str] = (
    "THE_FIRST_HALF_OF_A_GEMINATE_IS_EVICTED_NOT_SUBCLASSED: أوّلُ زوج الشدّة "
    "نصفُ حرفٍ مضعَّفٍ لا سكونٌ مكتوبٌ ولا مستنتَج؛ فيُنقَل إلى مقولته خارج "
    "العمود، ولا يُجعَل قسمًا ثالثًا من السكون يدخل معه حيث يدخل"
)

NO_SINGLE_SUKUN_TOTAL_IS_ISSUED_FROM_A_THREE_WAY_COLUMN: Final[str] = (
    "NO_SINGLE_SUKUN_TOTAL_IS_ISSUED_FROM_A_THREE_WAY_COLUMN: خمسةٌ وسبعون "
    "ومئةٌ وأربعةٌ مجموعُ ثلاثِ مقولاتٍ لا مقدارُ حالةٍ واحدة؛ فمن أصدرها رقمًا "
    "واحدًا باسم «عدد السكون» جمع المضعَّفَ والقرارَ والمِدادَ في خانة"
)

NOTHING_ENTERS_A_STATE_SPACE_AS_SUKUN_BEFORE_THIS_SPLIT: Final[str] = (
    "NOTHING_ENTERS_A_STATE_SPACE_AS_SUKUN_BEFORE_THIS_SPLIT: فضاءُ الحالات "
    "المُصدَرُ ههنا حالتان مفصولتان لا غير؛ فأيُّ بناءٍ لاحقٍ يطلب «السكونَ» "
    "حالةً يأخذهما مفصولتَين أو لا يأخذ شيئًا"
)

SUKUN_STATE_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "A_CENSUS_IS_NOT_A_STATE_SPACE_UNTIL_ITS_COLUMN_IS_SPLIT": (
        A_CENSUS_IS_NOT_A_STATE_SPACE_UNTIL_ITS_COLUMN_IS_SPLIT
    ),
    "THE_WRITTEN_AND_THE_INFERRED_ARE_NOT_ONE_STATE": (
        THE_WRITTEN_AND_THE_INFERRED_ARE_NOT_ONE_STATE
    ),
    "THE_FIRST_HALF_OF_A_GEMINATE_IS_EVICTED_NOT_SUBCLASSED": (
        THE_FIRST_HALF_OF_A_GEMINATE_IS_EVICTED_NOT_SUBCLASSED
    ),
    "NO_SINGLE_SUKUN_TOTAL_IS_ISSUED_FROM_A_THREE_WAY_COLUMN": (
        NO_SINGLE_SUKUN_TOTAL_IS_ISSUED_FROM_A_THREE_WAY_COLUMN
    ),
    "NOTHING_ENTERS_A_STATE_SPACE_AS_SUKUN_BEFORE_THIS_SPLIT": (
        NOTHING_ENTERS_A_STATE_SPACE_AS_SUKUN_BEFORE_THIS_SPLIT
    ),
}


# --- القسمة --------------------------------------------------------------

_THE_INFERRING_SOURCES: Final[tuple[SukunSource, ...]] = (
    SukunSource.ALIF_WITHOUT_A_MARK,
    SukunSource.BARE_CARRIER,
)


@dataclass(frozen=True)
class SukunStateSplit:
    """قسمةُ عمودٍ مقيسٍ إلى حالتَين ومُخرَجٍ واحد، مع عمودها الخامِ للمراجعة."""

    scope: str
    written: int
    inferred: int
    evicted: int
    raw_column: int

    def __post_init__(self) -> None:
        if min(self.written, self.inferred, self.evicted) < 0:
            raise SukunStateContractError("مقدارٌ سالبٌ في قسمةِ عمود.")
        if self.written + self.inferred + self.evicted != self.raw_column:
            raise SukunStateContractError(
                "القسمةُ لا تستوعب العمودَ الخامَ كلَّه؛ ولا بقيّةَ صامتة."
            )

    @property
    def states(self) -> dict[SukunState, int]:
        """فضاءُ الحالات وحدَه: حالتان، والمُخرَجُ ليس فيه."""

        return {
            SukunState.WRITTEN_SUKUN: self.written,
            SukunState.INFERRED_SUKUN: self.inferred,
        }

    @property
    def in_state_space(self) -> int:
        """ما دخل فضاءَ الحالات فعلًا؛ وهو دون العمود الخامِ بمقدار المُخرَج."""

        return self.written + self.inferred


def _split_a_census(census: SukunCensus) -> SukunStateSplit:
    counted = dict(census.by_source)
    written = counted.get(SukunSource.EXPLICIT_MARK, 0)
    inferred = sum(counted.get(source, 0) for source in _THE_INFERRING_SOURCES)
    evicted = counted.get(SukunSource.GEMINATION_PAIR_START, 0)
    return SukunStateSplit(
        scope=census.scope,
        written=written,
        inferred=inferred,
        evicted=evicted,
        raw_column=sum(counted.values()),
    )


@cache
def the_sukun_splits() -> tuple[SukunStateSplit, ...]:
    """قسمتا الوديعتَين، مشتقّتان عند القراءة من الإحصاءَين لا منسوختَين."""

    return (
        _split_a_census(measured_text_census()),
        _split_a_census(second_text_census()),
    )


def split_of(scope: str) -> SukunStateSplit:
    """قسمةُ نطاقٍ بعينه؛ وترفض ما لم يُقَس."""

    for split in the_sukun_splits():
        if split.scope == scope:
            return split
    raise SukunStateContractError(f"نطاقٌ غيرُ مقيسٍ: {scope!r}.")


def the_state_space_of(scope: str) -> dict[SukunState, int]:
    """فضاءُ حالاتِ السكون لنطاقٍ: حالتان، والمضعَّفُ خارجَهما."""

    return split_of(scope).states


def refuse_a_merged_total(scope: str) -> None:
    """طلبُ «عدد السكون» رقمًا واحدًا؛ وترفض دائمًا وتسمّي مقاديرَه الثلاثة."""

    split = split_of(scope)
    raise SukunStateContractError(
        f"{NO_SINGLE_SUKUN_TOTAL_IS_ISSUED_FROM_A_THREE_WAY_COLUMN} — "
        f"{scope}: مكتوبٌ {split.written}، مستنتَجٌ {split.inferred}، "
        f"مُخرَجٌ {split.evicted}."
    )


# --- حرّاسُ الاستيراد ------------------------------------------------------


def _assert_no_authority_field() -> None:
    """حارسُ استيراد: لا حقلَ سلطةٍ في عقدٍ يقسم ولا يحكم."""

    forbidden = {"verdict", "licensed", "born", "frozen", "authority", "rank"}
    named = {field.name for field in fields(SukunStateSplit)}
    if named & forbidden:
        raise SukunStateContractError(f"حقلُ سلطة: {sorted(named & forbidden)}.")


def _assert_the_state_space_holds_two_states_only() -> None:
    """حارسُ استيراد: فضاءُ الحالات حالتان، ولا يسع المُخرَجَ ولا اسمَه."""

    for split in the_sukun_splits():
        states = split.states
        if set(states) != set(SukunState):
            raise SukunStateContractError("فضاءُ الحالات ليس الحالتَين بعينهما.")
        if len(states) != 2:
            raise SukunStateContractError("فضاءُ الحالات ليس اثنَين.")
        if split.in_state_space + split.evicted != split.raw_column:
            raise SukunStateContractError("المُخرَجُ لم يُطرَح من الداخل.")


def _assert_the_evicted_is_never_a_sukun_state() -> None:
    """حارسُ استيراد: لا اسمَ للمضعَّف في مقولةِ السكون ولا العكس."""

    if {member.name for member in NonSukunCategory} & {
        member.name for member in SukunState
    }:
        raise SukunStateContractError("مقولةُ المضعَّف تسرّبت إلى حالات السكون.")


def _assert_the_split_matches_what_the_censuses_measure() -> None:
    """حارسُ استيراد: القسمةُ هي المقيسُ نفسُه معادَ توزيعِه لا رقمًا منسوخًا."""

    for split, census in zip(
        the_sukun_splits(),
        (measured_text_census(), second_text_census()),
        strict=True,
    ):
        counted = dict(census.by_source)
        if split.written != counted[SukunSource.EXPLICIT_MARK]:
            raise SukunStateContractError("المكتوبُ لا يطابق العلامةَ المقيسة.")
        if split.evicted != counted[SukunSource.GEMINATION_PAIR_START]:
            raise SukunStateContractError("المُخرَجُ لا يطابق أوائلَ الأزواج.")
        if split.inferred != sum(counted[s] for s in _THE_INFERRING_SOURCES):
            raise SukunStateContractError("المستنتَجُ لا يطابق مصدرَيه.")


def _assert_a_merged_total_is_always_refused() -> None:
    """حارسُ استيراد: طلبُ رقمٍ واحدٍ للعمود مرفوضٌ على كلّ نطاقٍ مقيس."""

    for split in the_sukun_splits():
        try:
            refuse_a_merged_total(split.scope)
        except SukunStateContractError:
            continue
        raise SukunStateContractError(  # pragma: no cover - الرفضُ يمنعه
            "عمودٌ خامٌ صدَر رقمًا واحدًا."
        )


def _assert_every_residual_is_named_by_its_key() -> None:
    """حارسُ استيراد: كلُّ بقيّةٍ تبدأ بمفتاحها فلا تُقتَبس منزوعةَ النسبة."""

    for key, text in SUKUN_STATE_NAMED_RESIDUALS.items():
        if not text.startswith(f"{key}: "):
            raise SukunStateContractError(f"بقيّةٌ لا تبدأ بمفتاحها: {key}.")


_assert_no_authority_field()
_assert_the_state_space_holds_two_states_only()
_assert_the_evicted_is_never_a_sukun_state()
_assert_the_split_matches_what_the_censuses_measure()
_assert_a_merged_total_is_always_refused()
_assert_every_residual_is_named_by_its_key()
