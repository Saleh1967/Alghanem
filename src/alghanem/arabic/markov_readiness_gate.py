"""بوّابةُ جاهزيّةِ ماركوف: تراخيصُ فضاءِ الحالات، وهي اثنان لا واحد.

**أوّلًا: والبوّابةُ لا تحسب شيئًا.** لا مصفوفةَ انتقالٍ ههنا، ولا احتمالَ،
ولا انتروبيا؛ وإنّما سلسلةُ شروطٍ مرتَّبةٍ تُقرأ عند القراءة فتقول: أين وقف
البناءُ، وبأيّ شرطٍ بعينه وقف. والوقوفُ الموسومُ ليس عجزًا، بل هو الفرقُ بين
«لم نحسب» و«لا يجوز أن نحسب بعدُ»
(`A_GATE_THAT_NAMES_ITS_FIRST_UNMET_PREREQUISITE_IS_NOT_A_FAILURE`).

**وثانيًا: والشروطُ مرتَّبةٌ لا مجموعة.** أوّلُ شرطٍ غيرُ مستوفًى يوقف
السلسلةَ، ولا يُنظَر فيما بعده؛ لأنّ استيفاءَ شرطٍ متأخّرٍ لا يعوّض عن سابقه،
ولأنّ إعلانَ «ستّةُ شروطٍ ناقصة» يخفي أنّ أوّلَها وحدَه هو الباب.

| الترتيب | الشرط | الحال |
|---|---|---|
| ١ | إغلاقُ الأثر المعجميّ | مستوفًى |
| ٢ | عقدُ حالةِ السكون | مستوفًى |
| ٣ | بايتاتُ المدوّنة | **غيرُ مستوفًى** |
| ٤ | شهادةُ إسقاطِ المدوّنة | غيرُ منظورٍ فيه |
| ٥ | قانونُ ترتيبِ تركيبها | غيرُ منظورٍ فيه |

**وثالثًا: وماركوف التوكنز موقوفٌ بالشرط الثالث.** `word_total` ترفض لأنّ
البايتات ليست في الشجرة ولا مصرَّحًا بمسارها؛ فكلُّ رقمٍ قرآنيٍّ اليومَ حسابٌ
بلا مرجِع. ولو أُودِعت غدًا لم يُفتَح البابُ وحدَه، بل انتقل الوقوفُ إلى
الشرط الذي يليه (`THE_CORPUS_BYTES_ARE_THE_THIRD_RUNG_AND_THEY_ARE_ABSENT`).

**ورابعًا: وماركوف الوظيفيُّ موقوفٌ لا محجوب.**

\\[
\\text{SUSPENDED} \\;\\neq\\; \\text{BLOCKED}
\\]

فالمحجوبُ ينتظر شرطًا معلومَ الطريق، والموقوفُ ينتظر **وديعةَ قسمةٍ وظيفيّةٍ
مرخّصة** لا وجودَ لها؛ والمحاولةُ التوزيعيّةُ الوحيدةُ نتيجتُها سالبةٌ
ومسجَّلة: أفضلُ عنقودٍ اثنان لا ثلاثة، وقسمةٌ ٢٬١٥٩/٣٤ خلطت حروفَ المعاني
بكلماتِ المحتوى فائقةِ التكرار. فاستيفاءُ الشروط الخمسةِ كلِّها لا يرفع
الوقفَ (`A_NEGATIVE_PROBE_SUSPENDS_THE_FUNCTIONAL_SPLIT_UNTIL_IT_IS_DEPOSITED`).

**وخامسًا: ولا رقمَ توكنٍ بغير مقياس هيمنة.** كلُّ مقدارٍ يخرج من التوكنات
يُصدَر ومعه نصيبُ أعلى نمطٍ وحصّةُ المكرَّر، وإلّا أعاد الأثرَ المعجميَّ
المُغلَقَ نفسَه على مقياسٍ أكبر؛ و`TokenFigure` لا تُبنى بغير قراءة هيمنة
(`NO_TOKEN_FIGURE_IS_ISSUED_WITHOUT_ITS_DOMINANCE_READING`).

**وسادسًا: والبوّابةُ الإحصائيّةُ تبقى سارية.** أيُّ انتظامٍ يُقاس يُقابَل بما
يصنعه الإسقاطُ وحدَه: ثلاثةُ أنماطٍ مكرَّرةٍ مكتوبةً صارت خمسةً مُسقَطةً على
آية الفتح، وبقيت ثلاثةً على الفاتحة. فالفائضُ اثنان صنعهما الطَّيُّ لا النصُّ
(`AN_INVARIANCE_THE_PROJECTION_MADE_IS_NOT_A_STATISTICAL_FINDING`).

ولا سلطةَ لهذه الوحدة: لا ولادةَ، ولا تجميدَ، ولا استيرادَ من `kernel/`،
ولا تُصدِر مقدارًا احتماليًّا واحدًا.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, fields
from enum import Enum
from functools import cache
from typing import Final

from alghanem.arabic.carrier_projection_deposit import (
    THE_DEPOSITS_PROJECTED,
    WordBoundary,
    deposited_text,
    project_word,
    words_of,
)
from alghanem.arabic.lexical_artifact_closure import (
    THE_CLOSED_CLAIMS,
    DominanceReading,
    dominance_of,
)
from alghanem.arabic.projection_composition_order import the_composition_table
from alghanem.arabic.quran_corpus_word_total import (
    QURAN_CORPUS_RELATIVE_PATH,
    quran_corpus_bytes_are_resolvable,
)
from alghanem.arabic.sukun_state_contract import the_sukun_splits

__all__ = [
    "AN_INVARIANCE_THE_PROJECTION_MADE_IS_NOT_A_STATISTICAL_FINDING",
    "A_GATE_THAT_NAMES_ITS_FIRST_UNMET_PREREQUISITE_IS_NOT_A_FAILURE",
    "A_NEGATIVE_PROBE_SUSPENDS_THE_FUNCTIONAL_SPLIT_UNTIL_IT_IS_DEPOSITED",
    "MARKOV_READINESS_NAMED_RESIDUALS",
    "NO_TOKEN_FIGURE_IS_ISSUED_WITHOUT_ITS_DOMINANCE_READING",
    "THE_CORPUS_BYTES_ARE_THE_THIRD_RUNG_AND_THEY_ARE_ABSENT",
    "THE_PREREQUISITE_ORDER",
    "ChainReading",
    "ChainStanding",
    "MarkovReadinessError",
    "Prerequisite",
    "PrerequisiteReading",
    "ProjectionMadeRegularity",
    "TokenFigure",
    "functional_markov_standing",
    "projection_made_regularity_on",
    "the_prerequisite_chain",
    "token_markov_standing",
]


class MarkovReadinessError(ValueError):
    """رفضٌ عند البوّابة: رقمُ توكنٍ بلا هيمنة، أو رفعُ وقفٍ بلا وديعة."""


class Prerequisite(Enum):
    """شروطُ فضاء الحالات مسمّاةً؛ وترتيبُها في `THE_PREREQUISITE_ORDER`."""

    LEXICAL_ARTIFACT_CLOSED = "إغلاقُ الأثر المعجميّ"
    SUKUN_COLUMN_SPLIT = "فصلُ عمود السكون"
    CORPUS_BYTES_PRESENT = "حضورُ بايتات المدوّنة"
    CORPUS_PROJECTION_CERTIFIED = "شهادةُ إسقاط المدوّنة"
    COMPOSITION_ORDER_KNOWN = "عِلمُ ترتيب التركيب"


THE_PREREQUISITE_ORDER: Final[tuple[Prerequisite, ...]] = (
    Prerequisite.LEXICAL_ARTIFACT_CLOSED,
    Prerequisite.SUKUN_COLUMN_SPLIT,
    Prerequisite.CORPUS_BYTES_PRESENT,
    Prerequisite.CORPUS_PROJECTION_CERTIFIED,
    Prerequisite.COMPOSITION_ORDER_KNOWN,
)
"""ترتيبُ الشروط؛ وأوّلُ غيرِ مستوفًى يوقف النظرَ فيما بعده."""


class ChainStanding(Enum):
    """مواقفُ السلسلة؛ والموقوفُ غيرُ المحجوب، ولا يُحمَل أحدُهما على الآخر."""

    OPEN = "مفتوح"
    BLOCKED = "محجوبٌ بشرطٍ مسمًّى"
    SUSPENDED = "موقوفٌ حتّى تُودَع قسمتُه"


# --- البقايا المسمّاة ------------------------------------------------------

A_GATE_THAT_NAMES_ITS_FIRST_UNMET_PREREQUISITE_IS_NOT_A_FAILURE: Final[str] = (
    "A_GATE_THAT_NAMES_ITS_FIRST_UNMET_PREREQUISITE_IS_NOT_A_FAILURE: الوقوفُ "
    "الموسومُ يفرّق بين «لم نحسب» و«لا يجوز أن نحسب بعدُ»؛ والشروطُ مرتَّبةٌ "
    "لا مجموعة، فأوّلُ غيرِ مستوفًى هو البابُ، وما بعده غيرُ منظورٍ فيه"
)

THE_CORPUS_BYTES_ARE_THE_THIRD_RUNG_AND_THEY_ARE_ABSENT: Final[str] = (
    "THE_CORPUS_BYTES_ARE_THE_THIRD_RUNG_AND_THEY_ARE_ABSENT: المدوّنةُ ليست "
    f"في `{QURAN_CORPUS_RELATIVE_PATH}` ولا مصرَّحًا بمسارها، فكلُّ رقمٍ قرآنيٍّ "
    "اليومَ حسابٌ بلا مرجِع؛ وإيداعُها لا يفتح البابَ بل ينقل الوقوفَ إلى "
    "الشرط الذي يليه"
)

A_NEGATIVE_PROBE_SUSPENDS_THE_FUNCTIONAL_SPLIT_UNTIL_IT_IS_DEPOSITED: Final[str] = (
    "A_NEGATIVE_PROBE_SUSPENDS_THE_FUNCTIONAL_SPLIT_UNTIL_IT_IS_DEPOSITED: "
    "المحاولةُ التوزيعيّةُ الوحيدةُ نتيجتُها سالبةٌ ومسجَّلة — أفضلُ عنقودٍ "
    "اثنان لا ثلاثة، وقسمةٌ خلطت حروفَ المعاني بكلماتِ المحتوى فائقةِ التكرار — "
    "فلا تُبنى القسمةُ الوظيفيّةُ حتّى تُودَع من مصدرٍ مُبصَّمٍ أو تُقاس بنجاح"
)

NO_TOKEN_FIGURE_IS_ISSUED_WITHOUT_ITS_DOMINANCE_READING: Final[str] = (
    "NO_TOKEN_FIGURE_IS_ISSUED_WITHOUT_ITS_DOMINANCE_READING: مقدارُ التوكنات "
    "يُصدَر ومعه نصيبُ أعلى نمطٍ وحصّةُ المكرَّر؛ وإلّا أعاد على مقياسٍ أكبرَ "
    "الأثرَ المعجميَّ الذي أُغلِق: تضخُّمًا بتكرار توكنٍ لا شاهدًا صوتيًّا"
)

AN_INVARIANCE_THE_PROJECTION_MADE_IS_NOT_A_STATISTICAL_FINDING: Final[str] = (
    "AN_INVARIANCE_THE_PROJECTION_MADE_IS_NOT_A_STATISTICAL_FINDING: ثلاثةُ "
    "أنماطٍ مكرَّرةٍ مكتوبةً صارت خمسةً مُسقَطةً على آية الفتح وبقيت ثلاثةً على "
    "الفاتحة؛ فالفائضُ صنعه الطَّيُّ لا النصّ، ويُطرَح من كلّ انتظامٍ يُدَّعى"
)

MARKOV_READINESS_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "A_GATE_THAT_NAMES_ITS_FIRST_UNMET_PREREQUISITE_IS_NOT_A_FAILURE": (
        A_GATE_THAT_NAMES_ITS_FIRST_UNMET_PREREQUISITE_IS_NOT_A_FAILURE
    ),
    "THE_CORPUS_BYTES_ARE_THE_THIRD_RUNG_AND_THEY_ARE_ABSENT": (
        THE_CORPUS_BYTES_ARE_THE_THIRD_RUNG_AND_THEY_ARE_ABSENT
    ),
    "A_NEGATIVE_PROBE_SUSPENDS_THE_FUNCTIONAL_SPLIT_UNTIL_IT_IS_DEPOSITED": (
        A_NEGATIVE_PROBE_SUSPENDS_THE_FUNCTIONAL_SPLIT_UNTIL_IT_IS_DEPOSITED
    ),
    "NO_TOKEN_FIGURE_IS_ISSUED_WITHOUT_ITS_DOMINANCE_READING": (
        NO_TOKEN_FIGURE_IS_ISSUED_WITHOUT_ITS_DOMINANCE_READING
    ),
    "AN_INVARIANCE_THE_PROJECTION_MADE_IS_NOT_A_STATISTICAL_FINDING": (
        AN_INVARIANCE_THE_PROJECTION_MADE_IS_NOT_A_STATISTICAL_FINDING
    ),
}


# --- سلسلةُ الشروط --------------------------------------------------------


@dataclass(frozen=True)
class PrerequisiteReading:
    """قراءةُ شرطٍ واحد: أمستوفًى، وبأيّ سندٍ مقيسٍ استُوفِي أو لم يُستوفَ."""

    prerequisite: Prerequisite
    met: bool
    ground: str

    def __post_init__(self) -> None:
        if not self.ground.strip():
            raise MarkovReadinessError("قراءةُ شرطٍ بلا سندٍ مكتوب.")


def _lexical_closure_reading() -> PrerequisiteReading:
    closed = len(THE_CLOSED_CLAIMS)
    return PrerequisiteReading(
        prerequisite=Prerequisite.LEXICAL_ARTIFACT_CLOSED,
        met=closed > 0,
        ground=f"دعاوى مُغلَقةٌ كأثرٍ معجميٍّ مُشخَّص: {closed}.",
    )


def _sukun_split_reading() -> PrerequisiteReading:
    splits = the_sukun_splits()
    met = all(split.in_state_space < split.raw_column for split in splits)
    return PrerequisiteReading(
        prerequisite=Prerequisite.SUKUN_COLUMN_SPLIT,
        met=met,
        ground="عمودُ السكون مقسومٌ إلى حالتَين ومُخرَجٍ على " f"{len(splits)} وديعة.",
    )


def _corpus_bytes_reading() -> PrerequisiteReading:
    resolvable = quran_corpus_bytes_are_resolvable()
    return PrerequisiteReading(
        prerequisite=Prerequisite.CORPUS_BYTES_PRESENT,
        met=resolvable,
        ground=(
            f"بايتاتُ المدوّنة تُحَلّ إلى ملفٍّ حاضر: {resolvable}. "
            f"{THE_CORPUS_BYTES_ARE_THE_THIRD_RUNG_AND_THEY_ARE_ABSENT}"
        ),
    )


def _corpus_certificate_reading() -> PrerequisiteReading:
    certified = tuple(THE_DEPOSITS_PROJECTED)
    return PrerequisiteReading(
        prerequisite=Prerequisite.CORPUS_PROJECTION_CERTIFIED,
        met=False,
        ground=(
            "الشهاداتُ المُصدَرةُ على الوديعتَين الصغيرتَين لا على المدوّنة: "
            f"{len(certified)}؛ ولا شهادةَ لمدوّنةٍ غائبةِ البايتات."
        ),
    )


def _composition_order_reading() -> PrerequisiteReading:
    unusable = tuple(
        finding for finding in the_composition_table() if not finding.is_usable
    )
    return PrerequisiteReading(
        prerequisite=Prerequisite.COMPOSITION_ORDER_KNOWN,
        met=False,
        ground=(
            "المدوّنةُ متعدّدةُ الأسطر ولم تُصنَّف؛ والتصنيفُ المقيسُ يُظهر "
            f"{len(unusable)} تركيبًا غيرَ محلولٍ على نصٍّ متعدّد الأسطر."
        ),
    )


@cache
def the_prerequisite_chain() -> tuple[PrerequisiteReading, ...]:
    """قراءةُ الشروط الخمسة بترتيبها، مشتقّةً عند القراءة لا منسوخة."""

    readers = {
        Prerequisite.LEXICAL_ARTIFACT_CLOSED: _lexical_closure_reading,
        Prerequisite.SUKUN_COLUMN_SPLIT: _sukun_split_reading,
        Prerequisite.CORPUS_BYTES_PRESENT: _corpus_bytes_reading,
        Prerequisite.CORPUS_PROJECTION_CERTIFIED: _corpus_certificate_reading,
        Prerequisite.COMPOSITION_ORDER_KNOWN: _composition_order_reading,
    }
    return tuple(readers[name]() for name in THE_PREREQUISITE_ORDER)


def _first_unmet() -> PrerequisiteReading | None:
    for reading in the_prerequisite_chain():
        if not reading.met:
            return reading
    return None


# --- التراخيص، وهي اثنان --------------------------------------------------


@dataclass(frozen=True)
class ChainReading:
    """موقفُ سلسلةٍ: مفتوحٌ، أو محجوبٌ بشرطٍ مسمًّى، أو موقوفٌ حتّى تُودَع قسمتُه."""

    chain_name: str
    standing: ChainStanding
    ground: str
    blocking_prerequisite: Prerequisite | None = None

    def __post_init__(self) -> None:
        if not self.ground.strip():
            raise MarkovReadinessError("موقفُ سلسلةٍ بلا سندٍ مكتوب.")
        if (self.blocking_prerequisite is None) is (
            self.standing is ChainStanding.BLOCKED
        ):
            raise MarkovReadinessError("الشرطُ الحاجبُ يلزم المحجوبَ وحدَه ويُمنَع على سواه.")


def token_markov_standing() -> ChainReading:
    """موقفُ ماركوف التوكنز: مفتوحٌ إن استُوفِيت الشروطُ، وإلّا محجوبٌ بأوّلها."""

    unmet = _first_unmet()
    if unmet is None:
        return ChainReading(
            chain_name="ماركوف التوكنز",
            standing=ChainStanding.OPEN,
            ground=(
                "الشروطُ الخمسةُ مستوفاة؛ ولا يُصدَر رقمٌ إلّا بقراءة هيمنةٍ. "
                f"{NO_TOKEN_FIGURE_IS_ISSUED_WITHOUT_ITS_DOMINANCE_READING}"
            ),
        )
    return ChainReading(
        chain_name="ماركوف التوكنز",
        standing=ChainStanding.BLOCKED,
        ground=f"{unmet.prerequisite.value}: {unmet.ground}",
        blocking_prerequisite=unmet.prerequisite,
    )


def functional_markov_standing() -> ChainReading:
    """موقفُ ماركوف الوظيفيّ: **موقوفٌ دائمًا**؛ ولا يرفعه استيفاءُ الشروط."""

    return ChainReading(
        chain_name="ماركوف الوظيفيّ",
        standing=ChainStanding.SUSPENDED,
        ground=A_NEGATIVE_PROBE_SUSPENDS_THE_FUNCTIONAL_SPLIT_UNTIL_IT_IS_DEPOSITED,
    )


# --- مقياسُ الهيمنة لازمٌ لكلّ رقم -----------------------------------------


@dataclass(frozen=True)
class TokenFigure:
    """مقدارٌ من التوكنات لا يُبنى إلّا مصحوبًا بقراءة هيمنته."""

    name: str
    value: int
    dominance: DominanceReading

    def __post_init__(self) -> None:
        if not isinstance(self.dominance, DominanceReading):
            raise MarkovReadinessError(
                NO_TOKEN_FIGURE_IS_ISSUED_WITHOUT_ITS_DOMINANCE_READING
            )
        if self.value < 0:
            raise MarkovReadinessError("مقدارٌ سالبٌ لا يُصدَر.")

    @property
    def leading_share(self) -> float:
        """نصيبُ أعلى نمطٍ من التوكنات؛ ويُنشَر مع المقدار لا بعده."""

        return self.dominance.leading_occurrences / self.dominance.tokens


# --- البوّابةُ الإحصائيّة ---------------------------------------------------


@dataclass(frozen=True)
class ProjectionMadeRegularity:
    """ما صنعه الطَّيُّ من تكرارٍ لم يكن في الكتابة؛ يُطرَح من كلّ انتظام."""

    source_identity: str
    repeated_written: int
    repeated_projected: int

    @property
    def made_by_the_projection(self) -> int:
        """الفائضُ المصنوع؛ وهو صفرٌ حيث لم يصنع الطَّيُّ شيئًا."""

        return self.repeated_projected - self.repeated_written


def _repeated_types(sequence: tuple[str, ...]) -> int:
    return sum(1 for count in Counter(sequence).values() if count > 1)


@cache
def projection_made_regularity_on(source_id: str) -> ProjectionMadeRegularity:
    """يقيس الأنماطَ المكرَّرةَ كتابةً وإسقاطًا على وديعةٍ، عند القراءة."""

    if source_id not in THE_DEPOSITS_PROJECTED:
        raise MarkovReadinessError(f"وديعةٌ خارج النطاق: {source_id!r}.")
    written = words_of(deposited_text(source_id), WordBoundary.ANY_WHITESPACE)
    projected = tuple("".join(project_word(word)) for word in written)
    return ProjectionMadeRegularity(
        source_identity=source_id,
        repeated_written=_repeated_types(written),
        repeated_projected=_repeated_types(projected),
    )


# --- حرّاسُ الاستيراد ------------------------------------------------------


def _assert_no_authority_field() -> None:
    """حارسُ استيراد: لا حقلَ سلطةٍ في بوّابةٍ تقف ولا تحكم."""

    forbidden = {"verdict", "licensed", "born", "frozen", "authority", "rank"}
    for holder in (PrerequisiteReading, ChainReading, TokenFigure):
        named = {field.name for field in fields(holder)}
        if named & forbidden:
            raise MarkovReadinessError(
                f"حقلُ سلطةٍ في {holder.__name__}: {sorted(named & forbidden)}."
            )


def _assert_this_module_issues_no_probability() -> None:
    """حارسُ استيراد: لا اسمَ احتمالٍ ولا انتروبيا في واجهة البوّابة."""

    banned = ("entropy", "nll", "likelihood", "transition_matrix", "probability")
    for exported in __all__:
        lowered = exported.lower()
        if any(word in lowered for word in banned):
            raise MarkovReadinessError(f"اسمٌ احتماليٌّ مُصدَّر: {exported}.")


def _assert_the_chain_is_ordered_and_complete() -> None:
    """حارسُ استيراد: الشروطُ كلُّها مقروءةٌ مرّةً واحدةً وبترتيبها المنشور."""

    read = tuple(reading.prerequisite for reading in the_prerequisite_chain())
    if read != THE_PREREQUISITE_ORDER:
        raise MarkovReadinessError("سلسلةُ الشروط ليست بترتيبها المنشور.")
    if len(set(read)) != len(Prerequisite):
        raise MarkovReadinessError("شرطٌ مسمًّى لم يُقرَأ في السلسلة.")


def _assert_the_token_chain_is_blocked_at_the_corpus_bytes() -> None:
    """حارسُ استيراد: الوقوفُ اليومَ عند البايتات، لا قبلها ولا بعدها."""

    reading = token_markov_standing()
    if reading.standing is not ChainStanding.BLOCKED:
        raise MarkovReadinessError("ماركوف التوكنز ليس محجوبًا والبايتاتُ غائبة.")
    if reading.blocking_prerequisite is not Prerequisite.CORPUS_BYTES_PRESENT:
        raise MarkovReadinessError(
            f"الحاجبُ غيرُ المنشور: {reading.blocking_prerequisite}."
        )


def _assert_the_functional_chain_is_suspended_and_not_blocked() -> None:
    """حارسُ استيراد: الوظيفيُّ موقوفٌ، والموقوفُ لا يُحمَل على المحجوب."""

    reading = functional_markov_standing()
    if reading.standing is not ChainStanding.SUSPENDED:
        raise MarkovReadinessError("ماركوف الوظيفيّ ليس موقوفًا.")
    if reading.blocking_prerequisite is not None:
        raise MarkovReadinessError("وقفٌ عُلِّل بشرطٍ حاجبٍ فصار محجوبًا.")


def _assert_a_token_figure_refuses_a_missing_dominance() -> None:
    """حارسُ استيراد: رقمُ توكنٍ بلا قراءة هيمنةٍ مرفوضٌ عند البناء."""

    try:
        TokenFigure(name="مقدار", value=1, dominance=None)  # type: ignore[arg-type]
    except MarkovReadinessError:
        return
    raise MarkovReadinessError(  # pragma: no cover - الرفضُ فوقُ يمنعه
        "رقمُ توكنٍ قُبِل بلا هيمنة."
    )


def _assert_the_projection_makes_regularity_where_it_was_measured() -> None:
    """حارسُ استيراد: الفائضُ المصنوعُ مقيسٌ ومطابقٌ للمنشور على الوديعتَين."""

    published = {
        "fatiha-transcription-in-tree": (3, 3),
        "fath-48-29-simplified-transcription-in-tree": (3, 5),
    }
    for source_id, (written, projected) in published.items():
        measured = projection_made_regularity_on(source_id)
        if (measured.repeated_written, measured.repeated_projected) != (
            written,
            projected,
        ):
            raise MarkovReadinessError(f"الفائضُ المقيسُ خالف المنشورَ: {source_id}.")
    dominance = dominance_of("fath-48-29-simplified-transcription-in-tree", True)
    if dominance.tokens <= dominance.types:
        raise MarkovReadinessError("لا مكرَّرَ حيث نشر النثرُ مكرَّرًا.")


def _assert_every_residual_is_named_by_its_key() -> None:
    """حارسُ استيراد: كلُّ بقيّةٍ تبدأ بمفتاحها فلا تُقتَبس منزوعةَ النسبة."""

    for key, text in MARKOV_READINESS_NAMED_RESIDUALS.items():
        if not text.startswith(f"{key}: "):
            raise MarkovReadinessError(f"بقيّةٌ لا تبدأ بمفتاحها: {key}.")


_assert_no_authority_field()
_assert_this_module_issues_no_probability()
_assert_the_chain_is_ordered_and_complete()
_assert_the_token_chain_is_blocked_at_the_corpus_bytes()
_assert_the_functional_chain_is_suspended_and_not_blocked()
_assert_a_token_figure_refuses_a_missing_dominance()
_assert_the_projection_makes_regularity_where_it_was_measured()
_assert_every_residual_is_named_by_its_key()
