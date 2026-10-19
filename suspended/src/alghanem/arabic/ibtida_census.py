"""قياسُ مقام الابتداء وفئاتِه ومنازلِ المبتدأ من بايتاتٍ مُبصَّمة.

هذا تشغيلُ `ibtida_preregistration` لا تعديلٌ له: لا قيمةَ أُضيفت بعد الرقم،
ولا مقامَ بُدِّل حتّى تُطابِق نسبةٌ، ولا رقمٌ يخرج من هنا إلّا وقاعدةُ عدِّه
مُجمَّدةٌ هناك وبصمتُها مربوطةٌ به.

`NoFigureWithoutTheFingerprintedBytes`: السجلّاتُ تأتي من `masaq_records` على
بايتاتٍ طُوبِق طولُها وبصمتُها في `read_masaq_bytes`؛ فإن غابت **لم يخرج رقم**.

`ADenominatorIsDeclaredNotAssumed`: كلُّ نسبةٍ هنا تحمل مقامَها في بنيتها —
`InchoativeDenominatorReading.denominator` — والمقامُ **مواضعُ الابتداء** لا
الجذوعُ ولا المقاطع؛ ويُعاد في البنية نفسِها عددُ الجذوع وعددُ المقاطع كي
يُرى أنّ الثلاثةَ ثلاثةُ مقاماتٍ لا رقمٌ واحدٌ اختُلِف فيه.

`ARoleTagIsNotALink`: منازلُ المبتدأ أدناه أعدادُ **جوارٍ داخل الآية** تحت
قاعدةٍ مُجمَّدة، لا أعدادُ إسنادٍ مُثبَتٍ بين مبتدأٍ وخبره بعينه. ولذلك ليس في
بنى هذه الوحدة حقلُ دقّةٍ ولا استرجاعٍ ولا ضبط، وحارسٌ في آخرها يرفض إضافتَه:
لا ذهبَ يُقاس إليه.

`ARelationNeedsTwoPresentTerms`: مجالُ كلّ علاقةٍ الآيةُ الواحدة، ولا يُربَط
مبتدأ في آيةٍ بخبرٍ في أخرى ليكتمل عدد.

`AnUnreadableWordKeyIsCountedNotDropped`: صفٌّ لا يُقرأ مفتاحُ كلمته عددًا
صحيحًا يُعَدُّ في حقلٍ باسمه ولا يُسقَط صامتًا.

وهذه الوحدة تسجيلٌ لا سلطة: لا ولادةَ فيها، ولا حكمَ ولادة، ولا تجميدَ `E0`،
ولا تستورد من `kernel/` شيئًا، ولا تقرؤها وحدةٌ فيه.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, fields
from enum import Enum
from typing import Final

from .ibtida_preregistration import (
    A_ROLE_TAG_IS_NOT_A_LINK_NOTE,
    DECLARED_GOVERNOR_VALUES,
    IBTIDA_CENSUS_COLUMNS,
    IBTIDA_PREREGISTRATION_DIGEST,
    INCHOATIVE_POSITION_DENOMINATOR,
    INCHOATIVE_POSITION_TOTAL,
    INCHOATIVE_POSITION_VALUES,
    NAMED_RESIDUES,
    PositionSide,
    SentenceClass,
    class_of_value,
    figure_for_value,
    figures_of_class,
    side_of_value,
)
from .irab_column_census import SURA_COLUMN, VERSE_COLUMN
from .irab_column_preregistration import (
    ANCHOR_COLUMN_NAME,
    CASE_MOOD_COLUMN,
    CASE_MOOD_MARKER_COLUMN,
    SEGMENT_INDEX_COLUMN_NAME,
    SYNTACTIC_ROLE_COLUMN,
    WORD_KEY_COLUMN_NAME,
)
from .irab_operator_census import (
    AN_UNREADABLE_WORD_KEY_IS_COUNTED_NOT_DROPPED_NOTE,
    NO_FIGURE_WITHOUT_THE_FINGERPRINTED_BYTES_NOTE,
)
from .irab_operator_preregistration import (
    A_DENOMINATOR_IS_DECLARED_NOT_ASSUMED_NOTE,
    A_RELATION_NEEDS_TWO_PRESENT_TERMS_NOTE,
    STEM_MORPH_TYPE,
    DeclaredDenominator,
)
from .masaq_corpus_deposit import (
    MASAQ_SHA256,
    MasaqDepositError,
    masaq_records,
)

__all__ = [
    "ACCUSATIVE_CASE_VALUE",
    "ARRIVING_INCHOATIVE_TOTAL",
    "ARRIVING_NAMED_RESIDUE_NAMES",
    "IBTIDA_CENSUS_NAMED_RESIDUALS",
    "NO_GOLD_FOR_THE_INCHOATIVE_LINK_NOTE",
    "AccusativeMubtadaCensus",
    "GovernorCensus",
    "GovernorStanding",
    "IbtidaCensusError",
    "InchoativeDenominatorReading",
    "InchoativePosition",
    "InchoativeRelationCensus",
    "MubtadaStanding",
    "SentenceClassCensus",
    "census_from_bytes",
    "classify_positions",
    "inchoative_positions",
    "measure_accusative_mubtada",
    "measure_governors",
    "measure_inchoative_relations",
    "read_inchoative_denominator",
    "stem_records",
    "verse_key_of",
]


class IbtidaCensusError(ValueError):
    """تُرفَع حين يُطلَب عددٌ من عمودٍ غائبٍ أو من بايتاتٍ لم تُقرأ سجلّاتُها."""


NO_GOLD_FOR_THE_INCHOATIVE_LINK_NOTE: Final[str] = (
    "NoGoldForTheInchoativeLink: لا عمودَ في المدوَّنة يربط مبتدأً بخبره "
    "بعينه، فلا مرجعَ تُقاس إليه دقّةُ ربطٍ ولا استرجاعُه؛ وحقلُ دقّةٍ في "
    "مُخرَجِ هذه الوحدة دعوى مرجعٍ لا وجودَ له، وحارسٌ يرفضه. "
    + A_ROLE_TAG_IS_NOT_A_LINK_NOTE
)

IBTIDA_CENSUS_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "NoFigureWithoutTheFingerprintedBytes": (
        NO_FIGURE_WITHOUT_THE_FINGERPRINTED_BYTES_NOTE
    ),
    "ADenominatorIsDeclaredNotAssumed": A_DENOMINATOR_IS_DECLARED_NOT_ASSUMED_NOTE,
    "ARelationNeedsTwoPresentTerms": A_RELATION_NEEDS_TWO_PRESENT_TERMS_NOTE,
    "ARoleTagIsNotALink": A_ROLE_TAG_IS_NOT_A_LINK_NOTE,
    "NoGoldForTheInchoativeLink": NO_GOLD_FOR_THE_INCHOATIVE_LINK_NOTE,
    "AnUnreadableWordKeyIsCountedNotDropped": (
        AN_UNREADABLE_WORD_KEY_IS_COUNTED_NOT_DROPPED_NOTE
    ),
}


ACCUSATIVE_CASE_VALUE: Final[str] = "منصوب"
"""قيمةُ `Case_Mood` التي يُفحَص بها المبتدأُ المنصوب؛ مطابقةً حرفيّةً."""


VerseKey = tuple[str, str]


def _require_columns(records: Sequence[Mapping[str, str]]) -> None:
    """احرسْ حضورَ الأعمدة الثمانية؛ وغيابُ واحدٍ يُوقِف العدَّ ولا يُصفِّره."""

    if not records:
        raise IbtidaCensusError(
            "لا سجلَّ يُقرأ؛ ولا يُخرَج عددٌ من ملفٍّ بلا سجلّات. "
            + NO_FIGURE_WITHOUT_THE_FINGERPRINTED_BYTES_NOTE
        )
    for column in IBTIDA_CENSUS_COLUMNS:
        if column not in records[0]:
            raise IbtidaCensusError(
                f"العمودُ «{column}» غائبٌ عن الترويسة؛ ولا يُحمَل على أقرب "
                "اسمٍ إليه، فالعدُّ يقف."
            )


def stem_records(
    records: Sequence[Mapping[str, str]],
) -> tuple[Mapping[str, str], ...]:
    """الجذوعُ وحدَها؛ وغيرُ الجذع لا موضعَ له في الابتداء فلا يُعَدُّ هنا."""

    _require_columns(records)
    return tuple(
        record
        for record in records
        if record.get(ANCHOR_COLUMN_NAME, "").strip() == STEM_MORPH_TYPE
    )


def verse_key_of(record: Mapping[str, str]) -> VerseKey:
    """مفتاحُ الآية: `(Sura_No، Verse_No)`؛ وبه يُحَدُّ مجالُ كلّ علاقة."""

    return (
        record.get(SURA_COLUMN, "").strip(),
        record.get(VERSE_COLUMN, "").strip(),
    )


def _word_number(record: Mapping[str, str]) -> int | None:
    """مفتاحُ الكلمة عددًا؛ و`None` لِما لا يُقرأ عددًا، ويُعَدُّ لا يُسقَط."""

    try:
        return int(record.get(WORD_KEY_COLUMN_NAME, "").strip())
    except ValueError:
        return None


@dataclass(frozen=True, slots=True)
class InchoativePosition:
    """موضعُ ابتداءٍ واحد: آيتُه، وكلمتُه، وقيمتُه، وفئتُه، وطرفُه، وحالُه."""

    verse: VerseKey
    word_number: int | None
    segment_index: str
    value: str
    sentence_class: SentenceClass
    side: PositionSide
    case_mood: str
    case_marker: str

    @property
    def reference(self) -> str:
        """موضعُه منطوقًا «سورة:آية:كلمة»؛ وبه تُسمّى البقيّةُ لا بعددها."""

        word = self.word_number if self.word_number is not None else "؟"
        return f"{self.verse[0]}:{self.verse[1]}:{word}"


def inchoative_positions(
    records: Sequence[Mapping[str, str]],
) -> tuple[InchoativePosition, ...]:
    """مواضعُ الابتداء وحدَها بترتيب ورودها؛ وما سواها خارجَ المقام لا صفرٌ فيه."""

    positions: list[InchoativePosition] = []
    for record in stem_records(records):
        value = record.get(SYNTACTIC_ROLE_COLUMN, "").strip()
        sentence_class = class_of_value(value)
        side = side_of_value(value)
        if sentence_class is None or side is None:
            continue
        positions.append(
            InchoativePosition(
                verse=verse_key_of(record),
                word_number=_word_number(record),
                segment_index=record.get(SEGMENT_INDEX_COLUMN_NAME, "").strip(),
                value=value,
                sentence_class=sentence_class,
                side=side,
                case_mood=record.get(CASE_MOOD_COLUMN, "").strip(),
                case_marker=record.get(CASE_MOOD_MARKER_COLUMN, "").strip(),
            )
        )
    return tuple(positions)


@dataclass(frozen=True, slots=True)
class InchoativeDenominatorReading:
    """قراءةُ المقام المُعلَن، ومعه مقاما الجذوع والمقاطع كي يُرى أنّها ثلاثة."""

    denominator: DeclaredDenominator
    denominator_count: int
    counts_by_value: dict[str, int]
    stem_count: int
    segment_count: int
    preregistration_digest: str
    corpus_digest: str

    def share_of_the_denominator(self, count: int) -> float:
        """نسبةُ عددٍ إلى مقام الابتداء وحدَه؛ ولا تُخرَج نسبةٌ بلا مقامها."""

        if self.denominator_count == 0:
            raise IbtidaCensusError(
                "لا موضعَ يُقسَم عليه؛ ولا نسبةَ بمقامٍ صفر. "
                + A_DENOMINATOR_IS_DECLARED_NOT_ASSUMED_NOTE
            )
        return count / self.denominator_count

    @property
    def absent_values(self) -> tuple[str, ...]:
        """قيمٌ مُجمَّدةٌ لم تَرِد في العمود البتّة؛ وذلك «ليست منه» لا «صفر»."""

        return tuple(
            value
            for value in INCHOATIVE_POSITION_VALUES
            if value not in self.counts_by_value
        )

    @property
    def agrees_with_the_declared_total(self) -> bool:
        """أطابق المقامُ المقيسُ المُدَّعى؟ ولا يُعدَّل المُدَّعى إن خالف."""

        return self.denominator_count == INCHOATIVE_POSITION_TOTAL


def read_inchoative_denominator(
    records: Sequence[Mapping[str, str]],
    *,
    corpus_digest: str = MASAQ_SHA256,
) -> InchoativeDenominatorReading:
    """اقرأ مقامَ الابتداء عدًّا، ومعه مقاما الجذوع والمقاطع للمقابلة."""

    stems = stem_records(records)
    counts: dict[str, int] = {}
    for position in inchoative_positions(records):
        counts[position.value] = counts.get(position.value, 0) + 1
    return InchoativeDenominatorReading(
        denominator=INCHOATIVE_POSITION_DENOMINATOR,
        denominator_count=sum(counts.values()),
        counts_by_value=counts,
        stem_count=len(stems),
        segment_count=len(records),
        preregistration_digest=IBTIDA_PREREGISTRATION_DIGEST,
        corpus_digest=corpus_digest,
    )


@dataclass(frozen=True, slots=True)
class SentenceClassCensus:
    """الفئاتُ الأربعُ معدودةً، ومعها الجذوعُ الخارجةُ عن المقام مُسمّاةً."""

    positions_by_class: dict[str, int]
    denominator_count: int
    stems_outside_the_denominator: int
    preregistration_digest: str
    corpus_digest: str

    @property
    def positions_in_the_four_classes(self) -> int:
        """مجموعُ الفئات الأربع؛ وهو المقامُ بعينه إن كانت مانعةً جامعة."""

        return sum(self.positions_by_class.values())

    @property
    def conserves_the_denominator(self) -> bool:
        """اختبارُ الحفظ: الفئاتُ الأربعُ مجموعةً تساوي المقامَ بالضبط."""

        return self.positions_in_the_four_classes == self.denominator_count


def classify_positions(
    records: Sequence[Mapping[str, str]],
    *,
    corpus_digest: str = MASAQ_SHA256,
) -> SentenceClassCensus:
    """صنِّف كلَّ موضعٍ في فئةٍ واحدةٍ من الأربع؛ ولا موضعَ في اثنتين.

    والجذعُ الذي ليس من مواضع الابتداء **ليس فئةً خامسة**: هو خارجَ المقام
    أصلًا، ويُعَدُّ في حقلٍ باسمه كي لا يُقرأ غيابُه صفرًا في فئة.
    """

    by_class = {sentence_class.name: 0 for sentence_class in SentenceClass}
    positions = inchoative_positions(records)
    for position in positions:
        by_class[position.sentence_class.name] += 1
    return SentenceClassCensus(
        positions_by_class=by_class,
        denominator_count=len(positions),
        stems_outside_the_denominator=len(stem_records(records)) - len(positions),
        preregistration_digest=IBTIDA_PREREGISTRATION_DIGEST,
        corpus_digest=corpus_digest,
    )


class MubtadaStanding(Enum):
    """منزلةُ المبتدأ في آيته؛ وثلاثتُها لا يجمعها صفرٌ واحد."""

    HAS_ONE_TAGGED_PREDICATE = "له_خبرٌ_موسومٌ_في_آيته"
    NO_TAGGED_PREDICATE = "لا_خبرَ_موسومٌ_في_آيته"
    MORE_THAN_ONE_CANDIDATE = "له_أكثرُ_من_خبرٍ_مرشَّح"


def _predicate_value_of_class(sentence_class: SentenceClass) -> str | None:
    """قيمةُ الخبر لفئةٍ بعينها؛ و`None` لفئةٍ لا قيمةَ خبرٍ لها في العمود."""

    for figure in figures_of_class(sentence_class):
        if figure.side is PositionSide.PREDICATE:
            return figure.value
    return None


@dataclass(frozen=True, slots=True)
class InchoativeRelationCensus:
    """منازلُ المبتدأ بقاعدة الجوار داخل الآية؛ أعدادُ جوارٍ لا أعدادُ إسناد.

    `NoGoldForTheInchoativeLink`: لا حقلَ دقّةٍ هنا ولا استرجاعٍ، لأنّ
    المدوَّنةَ لا تحمل رابطةً تُقاس إليها.
    """

    standings: dict[str, int]
    inchoatives: int
    predicates: int
    unreadable_word_keys: int
    positions_without_a_predicate: tuple[str, ...]
    inchoatives_whose_class_has_no_predicate_value: int
    preregistration_digest: str
    corpus_digest: str

    @property
    def counted_inchoatives(self) -> int:
        """المبتدآتُ التي دخلت المنازلَ الثلاث؛ وما سواها مُسمًّى في حقله."""

        return sum(self.standings.values())


def measure_inchoative_relations(
    records: Sequence[Mapping[str, str]],
    *,
    corpus_digest: str = MASAQ_SHA256,
) -> InchoativeRelationCensus:
    """اقرأ منزلةَ كلّ مبتدأٍ من خبر فئته **داخل آيته وحدَها**.

    `ARelationNeedsTwoPresentTerms`: لا يُربَط مبتدأ في آيةٍ بخبرٍ في أخرى.
    و«لا خبرَ موسوم» تُسمّى بمواضعها لا بعددها المجمل.
    """

    positions = inchoative_positions(records)
    predicates_by_verse: dict[tuple[VerseKey, str], int] = {}
    for position in positions:
        if position.side is PositionSide.PREDICATE:
            key = (position.verse, position.value)
            predicates_by_verse[key] = predicates_by_verse.get(key, 0) + 1

    standings = {standing.name: 0 for standing in MubtadaStanding}
    without: list[str] = []
    unreadable = 0
    inchoatives = 0
    no_predicate_value = 0
    for position in positions:
        if position.word_number is None:
            unreadable += 1
        if position.side is not PositionSide.INCHOATIVE:
            continue
        inchoatives += 1
        predicate_value = _predicate_value_of_class(position.sentence_class)
        if predicate_value is None:
            no_predicate_value += 1
            continue
        count = predicates_by_verse.get((position.verse, predicate_value), 0)
        if count == 0:
            standings[MubtadaStanding.NO_TAGGED_PREDICATE.name] += 1
            without.append(f"{position.reference} — {position.value}")
        elif count == 1:
            standings[MubtadaStanding.HAS_ONE_TAGGED_PREDICATE.name] += 1
        else:
            standings[MubtadaStanding.MORE_THAN_ONE_CANDIDATE.name] += 1
    return InchoativeRelationCensus(
        standings=standings,
        inchoatives=inchoatives,
        predicates=sum(predicates_by_verse.values()),
        unreadable_word_keys=unreadable,
        positions_without_a_predicate=tuple(without),
        inchoatives_whose_class_has_no_predicate_value=no_predicate_value,
        preregistration_digest=IBTIDA_PREREGISTRATION_DIGEST,
        corpus_digest=corpus_digest,
    )


class GovernorStanding(Enum):
    """منزلةُ الناسخ الموسوم؛ و«ليست من قيم العمود» غيرُ «لا اسمَ له»."""

    HAS_A_TAGGED_NAME = "له_اسمٌ_موسومٌ_في_آيته"
    NO_TAGGED_NAME = "لا_اسمَ_موسومٌ_في_آيته"


@dataclass(frozen=True, slots=True)
class GovernorCensus:
    """النواسخُ الموسومةُ بأسمائها؛ وقيمةٌ لم تَرِد تُسمّى ولا تُعَدُّ صفرًا."""

    standings: dict[str, int]
    governors_by_value: dict[str, int]
    absent_values: tuple[str, ...]
    governors_without_a_name: tuple[str, ...]
    preregistration_digest: str
    corpus_digest: str


_NAME_VALUE_OF_GOVERNOR: Final[dict[str, str]] = {
    "حرف ناسخ": "اسم حرف ناسخ",
    "فعل ناسخ": "اسم فعل ناسخ",
}


def measure_governors(
    records: Sequence[Mapping[str, str]],
    *,
    corpus_digest: str = MASAQ_SHA256,
) -> GovernorCensus:
    """اقرأ كلَّ ناسخٍ موسومٍ ومعه اسمُه في آيته؛ تكذيبًا للتوقّع الثالث.

    `AClaimedValueAbsentIsNotAZeroCount`: قيمةُ الناسخ إن لم تَرِد في العمود
    البتّة خرجت في `absent_values` ولم تُعَدَّ صفرًا في المنازل.
    """

    stems = stem_records(records)
    names_by_verse: dict[tuple[VerseKey, str], int] = {}
    governors: list[tuple[VerseKey, int | None, str]] = []
    by_value: dict[str, int] = {}
    for record in stems:
        value = record.get(SYNTACTIC_ROLE_COLUMN, "").strip()
        verse = verse_key_of(record)
        if figure_for_value(value) is not None:
            key = (verse, value)
            names_by_verse[key] = names_by_verse.get(key, 0) + 1
        if value in DECLARED_GOVERNOR_VALUES:
            governors.append((verse, _word_number(record), value))
            by_value[value] = by_value.get(value, 0) + 1

    standings = {standing.name: 0 for standing in GovernorStanding}
    without: list[str] = []
    for verse, word, value in governors:
        name_value = _NAME_VALUE_OF_GOVERNOR[value]
        if names_by_verse.get((verse, name_value), 0) > 0:
            standings[GovernorStanding.HAS_A_TAGGED_NAME.name] += 1
        else:
            standings[GovernorStanding.NO_TAGGED_NAME.name] += 1
            reference = f"{verse[0]}:{verse[1]}:{word if word is not None else '؟'}"
            without.append(f"{reference} — {value}")
    return GovernorCensus(
        standings=standings,
        governors_by_value=by_value,
        absent_values=tuple(
            value for value in DECLARED_GOVERNOR_VALUES if value not in by_value
        ),
        governors_without_a_name=tuple(without),
        preregistration_digest=IBTIDA_PREREGISTRATION_DIGEST,
        corpus_digest=corpus_digest,
    )


@dataclass(frozen=True, slots=True)
class AccusativeMubtadaCensus:
    """المبتدأُ المنصوبُ **بمواضعه**؛ وثلاثةٌ عددٌ يُفحَص لا يُلخَّص نسبةً."""

    references: tuple[str, ...]
    markers: tuple[str, ...]
    preregistration_digest: str
    corpus_digest: str

    @property
    def count(self) -> int:
        """عددُها مُشتَقًّا من مواضعها لا مكتوبًا رقمًا بجانبها."""

        return len(self.references)


def measure_accusative_mubtada(
    records: Sequence[Mapping[str, str]],
    *,
    corpus_digest: str = MASAQ_SHA256,
) -> AccusativeMubtadaCensus:
    """أخرِج كلَّ موضعِ «مبتدأ» حالُه «منصوب»، موضعًا موضعًا لا عددًا مجملًا."""

    references: list[str] = []
    markers: list[str] = []
    for position in inchoative_positions(records):
        if position.value != "مبتدأ":
            continue
        if position.case_mood != ACCUSATIVE_CASE_VALUE:
            continue
        references.append(position.reference)
        markers.append(position.case_marker)
    return AccusativeMubtadaCensus(
        references=tuple(references),
        markers=tuple(markers),
        preregistration_digest=IBTIDA_PREREGISTRATION_DIGEST,
        corpus_digest=corpus_digest,
    )


def census_from_bytes(
    data: bytes,
) -> tuple[
    InchoativeDenominatorReading,
    SentenceClassCensus,
    InchoativeRelationCensus,
    GovernorCensus,
    AccusativeMubtadaCensus,
]:
    """اقرأ السجلّات من بايتاتٍ مُطابَقةٍ سلفًا، ثمّ أخرِج القياسات الخمسة.

    والبايتاتُ تأتي من `read_masaq_bytes` وحدَها: هي التي تُطابِق الطولَ
    والبصمةَ قبل القراءة. `NoFigureWithoutTheFingerprintedBytes`.
    """

    try:
        records = masaq_records(data)
    except MasaqDepositError as error:
        raise IbtidaCensusError(
            f"لم تُقرأ سجلّاتُ المدوَّنة: {error}. "
            + NO_FIGURE_WITHOUT_THE_FINGERPRINTED_BYTES_NOTE
        ) from error
    return (
        read_inchoative_denominator(records),
        classify_positions(records),
        measure_inchoative_relations(records),
        measure_governors(records),
        measure_accusative_mubtada(records),
    )


ARRIVING_INCHOATIVE_TOTAL: Final[int] = INCHOATIVE_POSITION_TOTAL
"""١١٬٣٤٩ موضعًا كما وصلت، مجموعةً في التسجيل لا مكتوبةً هنا رقمًا ثانيًا."""


ARRIVING_NAMED_RESIDUE_NAMES: Final[tuple[str, ...]] = tuple(
    residue.name for residue in NAMED_RESIDUES
)
"""أسماءُ البقايا كما سُمِّيت قبل القياس؛ ولا تُسمّى بقيّةٌ بعد رؤية عددها."""


_FORBIDDEN_OUTPUT_FIELD_MARKERS: Final[tuple[str, ...]] = (
    "accuracy",
    "precision",
    "recall",
    "f1",
    "gold",
    "score",
)


def _assert_no_accuracy_field() -> None:
    """احرسْ خلوَّ بنى المخرَج من حقل دقّةٍ؛ فلا ذهبَ تُقاس إليه رابطة."""

    for dataclass_type in (
        InchoativePosition,
        InchoativeDenominatorReading,
        SentenceClassCensus,
        InchoativeRelationCensus,
        GovernorCensus,
        AccusativeMubtadaCensus,
    ):
        for field in fields(dataclass_type):
            lowered = field.name.lower()
            for marker in _FORBIDDEN_OUTPUT_FIELD_MARKERS:
                if marker in lowered:
                    raise IbtidaCensusError(
                        f"حقلُ دقّةٍ في بنية مخرَج: {dataclass_type.__name__}."
                        f"{field.name}. " + NO_GOLD_FOR_THE_INCHOATIVE_LINK_NOTE
                    )


_assert_no_accuracy_field()
