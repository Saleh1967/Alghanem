"""قياسُ التغطية على مقام الجذوع، وبقيّتِها بأنماطها، وأزواجِ العامل والمعمول.

هذا تشغيلُ `irab_operator_preregistration` لا تعديلٌ له: لا كاشفَ أُضيف بعد
الرقم، ولا مقامَ بُدِّل حتّى تُطابِق نسبةٌ، ولا رقمٌ يخرج من هنا إلّا وقاعدةُ
عدِّه مُجمَّدةٌ هناك وبصمتُها مربوطةٌ به.

`NoFigureWithoutTheFingerprintedBytes`: السجلّاتُ تأتي من `masaq_records` على
بايتاتٍ طُوبِق طولُها وبصمتُها في `read_masaq_bytes`؛ فإن غابت **لم يخرج رقم**.

`ADenominatorIsDeclaredNotAssumed`: كلُّ نسبةٍ هنا تحمل مقامَها في بنيتها —
`StemCoverageReading.denominator` — ولا تُخرَج نسبةٌ من دالّةٍ لا تُعيد مقامَها
معها.

`ARelationNeedsTwoPresentTerms`: العاملُ والمعمولُ يُطلَبان داخل الآية الواحدة،
ولا يُوصَل معمولٌ بعاملٍ من آيةٍ أخرى ليكتمل عددٌ. ولكلّ معمولٍ ثلاثُ منازلَ لا
يجمعها صفر: له عاملٌ سابقٌ في آيته، أو له عاملٌ لاحقٌ فيها، أو **لا عامل مرصود**
— والثالثةُ تُسمّى ولا تُبتلَع.

`AnOperatorTagIsNotAProvenGovernment`: المسافةُ والسبقُ يُقاسان من ترتيب
الكلمات، وهما قياسٌ لقاعدة الجوار المُجمَّدة لا إثباتٌ لعملٍ في معمولٍ بعينه.

`AnUnreadableWordKeyIsCountedNotDropped`: صفٌّ لا يُقرأ مفتاحُ كلمته عددًا
صحيحًا لا يدخل في ترتيبٍ ولا في مسافة، ويُعَدُّ في حقلٍ باسمه؛ فإسقاطُه صامتًا
يُنقِص مقامًا بلا أثر.

وهذه الوحدة تسجيلٌ لا سلطة: لا ولادةَ فيها، ولا حكمَ ولادة، ولا تجميدَ `E0`،
ولا تستورد من `kernel/` شيئًا، ولا تقرؤها وحدةٌ فيه.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from enum import Enum
from typing import Final

from .irab_column_census import SURA_COLUMN, VERSE_COLUMN
from .irab_column_preregistration import (
    ANCHOR_COLUMN_NAME,
    SEGMENT_INDEX_COLUMN_NAME,
    SYNTACTIC_ROLE_COLUMN,
    WORD_KEY_COLUMN_NAME,
)
from .irab_operator_preregistration import (
    A_DENOMINATOR_IS_DECLARED_NOT_ASSUMED_NOTE,
    A_RELATION_NEEDS_TWO_PRESENT_TERMS_NOTE,
    ACCEPTANCE_THRESHOLD_PERCENTAGE,
    AN_OPERATOR_TAG_IS_NOT_A_PROVEN_GOVERNMENT_NOTE,
    ARRIVING_RESIDUE_ACCOUNT,
    ARRIVING_ROLE_COVERAGE_ON_STEMS,
    IRAB_OPERATOR_PREREGISTRATION_DIGEST,
    OPERATOR_CENSUS_COLUMNS,
    STEM_DENOMINATOR,
    STEM_MORPH_TYPE,
    DeclaredDenominator,
    ResiduePattern,
    RoleSide,
    role_side_of,
)
from .masaq_corpus_deposit import (
    MASAQ_SHA256,
    MasaqDepositError,
    masaq_records,
)

__all__ = [
    "AN_UNREADABLE_WORD_KEY_IS_COUNTED_NOT_DROPPED_NOTE",
    "ARRIVING_RESIDUE_STEMS",
    "ARRIVING_RESIDUE_VERSES",
    "IRAB_OPERATOR_CENSUS_NAMED_RESIDUALS",
    "NO_FIGURE_WITHOUT_THE_FINGERPRINTED_BYTES_NOTE",
    "DependentStanding",
    "IrabOperatorCensusError",
    "RelationCensus",
    "ResidueCensus",
    "StemCoverageReading",
    "StemPosition",
    "census_from_bytes",
    "measure_relations",
    "measure_residue",
    "read_stem_coverage",
    "stem_positions",
    "stem_records",
    "unroled_stem_positions",
    "verse_key_of",
]


class IrabOperatorCensusError(ValueError):
    """تُرفَع حين يُطلَب عددٌ من عمودٍ غائبٍ أو من بايتاتٍ لم تُقرأ سجلّاتُها."""


NO_FIGURE_WITHOUT_THE_FINGERPRINTED_BYTES_NOTE: Final[str] = (
    "NoFigureWithoutTheFingerprintedBytes: كلُّ عددٍ هنا مُشتَقٌّ من بايتاتٍ "
    "طُوبِق طولُها وبصمتُها قبل قراءتها؛ فإن غابت لم يخرج رقمٌ ولم يُوضَع "
    "مكانَه تقديرٌ ولا قيمةٌ محفوظة"
)

AN_UNREADABLE_WORD_KEY_IS_COUNTED_NOT_DROPPED_NOTE: Final[str] = (
    "AnUnreadableWordKeyIsCountedNotDropped: صفٌّ لا يُقرأ مفتاحُ كلمته عددًا "
    "صحيحًا لا يدخل ترتيبًا ولا مسافةً، ويُعَدُّ في حقلٍ باسمه؛ فإسقاطُه "
    "صامتًا يُنقِص مقامًا بلا أثرٍ يُرى"
)

IRAB_OPERATOR_CENSUS_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "NoFigureWithoutTheFingerprintedBytes": (
        NO_FIGURE_WITHOUT_THE_FINGERPRINTED_BYTES_NOTE
    ),
    "AnUnreadableWordKeyIsCountedNotDropped": (
        AN_UNREADABLE_WORD_KEY_IS_COUNTED_NOT_DROPPED_NOTE
    ),
    "ADenominatorIsDeclaredNotAssumed": A_DENOMINATOR_IS_DECLARED_NOT_ASSUMED_NOTE,
    "ARelationNeedsTwoPresentTerms": A_RELATION_NEEDS_TWO_PRESENT_TERMS_NOTE,
    "AnOperatorTagIsNotAProvenGovernment": (
        AN_OPERATOR_TAG_IS_NOT_A_PROVEN_GOVERNMENT_NOTE
    ),
}


VerseKey = tuple[str, str]


def _require_columns(records: Sequence[Mapping[str, str]]) -> None:
    """احرسْ حضورَ الأعمدة الستّة؛ وغيابُ واحدٍ يُوقِف العدَّ ولا يُصفِّره."""

    if not records:
        raise IrabOperatorCensusError(
            "لا سجلَّ يُقرأ؛ ولا يُخرَج عددٌ من ملفٍّ بلا سجلّات. "
            + NO_FIGURE_WITHOUT_THE_FINGERPRINTED_BYTES_NOTE
        )
    for column in OPERATOR_CENSUS_COLUMNS:
        if column not in records[0]:
            raise IrabOperatorCensusError(
                f"العمودُ «{column}» غائبٌ عن الترويسة؛ ولا يُحمَل على أقرب "
                "اسمٍ إليه، فالعدُّ يقف."
            )


def stem_records(
    records: Sequence[Mapping[str, str]],
) -> tuple[Mapping[str, str], ...]:
    """الجذوعُ وحدَها تحت قاعدة `STEM_DENOMINATOR`؛ مطابقةً حرفيّةً لا احتواءً."""

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


@dataclass(frozen=True, slots=True)
class StemPosition:
    """موضعُ جذعٍ واحد: آيتُه، ومفتاحُ كلمته، وفهرسُ مقطعه، ودورُه وطرفُه."""

    verse: VerseKey
    word_number: int | None
    segment_index: str
    role: str
    side: RoleSide

    @property
    def has_role(self) -> bool:
        """أحمل الجذعُ دورًا نحويًّا؟ والفراغُ غيابُ وَسْمٍ لا نفيُ دور."""

        return bool(self.role)


def _word_number(record: Mapping[str, str]) -> int | None:
    """مفتاحُ الكلمة عددًا؛ و`None` لِما لا يُقرأ عددًا، ويُعَدُّ لا يُسقَط."""

    raw = record.get(WORD_KEY_COLUMN_NAME, "").strip()
    try:
        return int(raw)
    except ValueError:
        return None


def stem_positions(
    records: Sequence[Mapping[str, str]],
) -> tuple[StemPosition, ...]:
    """مواضعُ الجذوع كلِّها بترتيب ورودها؛ ولا يُعاد ترتيبُ المدوَّنة هنا."""

    positions: list[StemPosition] = []
    for record in stem_records(records):
        role = record.get(SYNTACTIC_ROLE_COLUMN, "").strip()
        positions.append(
            StemPosition(
                verse=verse_key_of(record),
                word_number=_word_number(record),
                segment_index=record.get(SEGMENT_INDEX_COLUMN_NAME, "").strip(),
                role=role,
                side=role_side_of(role) if role else RoleSide.OUTSIDE_THE_DETECTORS,
            )
        )
    return tuple(positions)


def unroled_stem_positions(
    records: Sequence[Mapping[str, str]],
) -> tuple[StemPosition, ...]:
    """الجذوعُ التي خلا فيها `Syntactic_Role`؛ وهي البقيّةُ بعينها."""

    return tuple(
        position for position in stem_positions(records) if not position.has_role
    )


@dataclass(frozen=True, slots=True)
class StemCoverageReading:
    """قراءةُ التغطية على مقامٍ مُعلَن؛ ولا تُفارِق النسبةُ مقامَها هنا."""

    column: str
    denominator: DeclaredDenominator
    denominator_count: int
    covered_count: int
    declared_percentage: str
    threshold_percentage: str
    preregistration_digest: str
    corpus_digest: str

    @property
    def residue_count(self) -> int:
        """ما لم يُوسَم: المقامُ ناقصَ المُغطّى، عدًّا لا اشتقاقًا من نسبة."""

        return self.denominator_count - self.covered_count

    @property
    def measured_percentage(self) -> float:
        """النسبةُ المقيسةُ كاملةً؛ ولا تُقارَن بها بل بمُقرَّبِها."""

        if self.denominator_count == 0:
            raise IrabOperatorCensusError(
                "لا جذعَ يُقسَم عليه؛ ولا نسبةَ بمقامٍ صفر. "
                + A_DENOMINATOR_IS_DECLARED_NOT_ASSUMED_NOTE
            )
        return 100.0 * self.covered_count / self.denominator_count

    @property
    def agrees_with_the_declared(self) -> bool:
        """أطابقت المُدَّعى عند منازله المُصرَّح بها وحدَها؟"""

        places = len(self.declared_percentage.split(".")[1])
        return f"{self.measured_percentage:.{places}f}" == self.declared_percentage

    @property
    def meets_threshold(self) -> bool:
        """أبلغت العتبةَ المُعلَنة؟ والعتبةُ على مقام الجذوع وحدَه."""

        return self.measured_percentage >= float(self.threshold_percentage)


def read_stem_coverage(
    records: Sequence[Mapping[str, str]],
    *,
    corpus_digest: str = MASAQ_SHA256,
) -> StemCoverageReading:
    """تغطيةُ `Syntactic_Role` على الجذوع وحدَها، بمقامها منطوقًا معها."""

    stems = stem_records(records)
    covered = sum(
        1 for record in stems if record.get(SYNTACTIC_ROLE_COLUMN, "").strip()
    )
    return StemCoverageReading(
        column=SYNTACTIC_ROLE_COLUMN,
        denominator=STEM_DENOMINATOR,
        denominator_count=len(stems),
        covered_count=covered,
        declared_percentage=ARRIVING_ROLE_COVERAGE_ON_STEMS.declared_percentage,
        threshold_percentage=ACCEPTANCE_THRESHOLD_PERCENTAGE,
        preregistration_digest=IRAB_OPERATOR_PREREGISTRATION_DIGEST,
        corpus_digest=corpus_digest,
    )


@dataclass(frozen=True, slots=True)
class ResidueCensus:
    """البقيّةُ مقيسةً بأنماطها المُجمَّدة: آياتٍ وجذوعًا لكلّ نمطٍ منها."""

    verses_by_pattern: dict[str, int]
    stems_by_pattern: dict[str, int]
    preregistration_digest: str
    corpus_digest: str

    @property
    def residue_stems(self) -> int:
        """جملةُ الجذوع بلا دور؛ وهي مجموعُ الأنماط الثلاثة لا غيرُه."""

        return sum(self.stems_by_pattern.values())

    @property
    def residue_verses(self) -> int:
        """جملةُ الآيات التي فيها جذعٌ بلا دورٍ واحدٌ فأكثر."""

        return sum(self.verses_by_pattern.values())

    @property
    def stems_per_verse(self) -> float:
        """معدّلُ الجذوع للآية؛ و`0.0` حين لا بقيّةَ أصلًا لا قسمةٌ على صفر."""

        if self.residue_verses == 0:
            return 0.0
        return self.residue_stems / self.residue_verses


def measure_residue(
    records: Sequence[Mapping[str, str]],
    *,
    corpus_digest: str = MASAQ_SHA256,
) -> ResidueCensus:
    """صنِّف البقيّةَ بأنماط `ResiduePattern` المسنونةِ قبل رؤيتها.

    والآيةُ تُصنَّف مرّةً واحدة: مُهمَلةٌ بأكملها إن لم يحمل جذعٌ فيها دورًا،
    وسهوٌ موضعيٌّ إن كان الخالي من الدور جذعًا واحدًا وفيها مُغطًّى، وإلّا
    فـ«لا هذا ولا ذاك» — وهو بابٌ مُعلَنٌ لا مَعذِرة.
    """

    unroled: dict[VerseKey, int] = {}
    roled: dict[VerseKey, int] = {}
    for position in stem_positions(records):
        bucket = roled if position.has_role else unroled
        bucket[position.verse] = bucket.get(position.verse, 0) + 1

    verses = {pattern.name: 0 for pattern in ResiduePattern}
    stems = {pattern.name: 0 for pattern in ResiduePattern}
    for verse, count in unroled.items():
        if roled.get(verse, 0) == 0:
            pattern = ResiduePattern.WHOLLY_UNANNOTATED_VERSE
        elif count == 1:
            pattern = ResiduePattern.SINGLE_UNROLED_STEM_IN_VERSE
        else:
            pattern = ResiduePattern.NEITHER_PATTERN
        verses[pattern.name] += 1
        stems[pattern.name] += count
    return ResidueCensus(
        verses_by_pattern=verses,
        stems_by_pattern=stems,
        preregistration_digest=IRAB_OPERATOR_PREREGISTRATION_DIGEST,
        corpus_digest=corpus_digest,
    )


class DependentStanding(Enum):
    """منزلةُ المعمول في آيته؛ وثلاثتُها لا يجمعها صفرٌ واحد."""

    HAS_PRECEDING_OPERATOR = "له_عاملٌ_سابقٌ_في_آيته"
    HAS_FOLLOWING_OPERATOR = "له_عاملٌ_لاحقٌ_في_آيته"
    NO_OPERATOR_OBSERVED = "لا_عاملَ_مرصودٌ_في_آيته"


@dataclass(frozen=True, slots=True)
class RelationCensus:
    """أزواجُ العامل والمعمول بقاعدة الجوار: منازلُ المعمولات، ومسافاتُها.

    `AnOperatorTagIsNotAProvenGovernment`: هذه أعدادُ جوارٍ داخل الآية، لا
    أعدادُ عملٍ مُثبَتٍ في معمولٍ بعينه.
    """

    standings: dict[str, int]
    distances: dict[int, int]
    operators: int
    dependents: int
    unreadable_word_keys: int
    preregistration_digest: str
    corpus_digest: str

    @property
    def decided(self) -> int:
        """المعمولاتُ التي وُجِد لها عاملٌ في آيتها، سابقًا كان أو لاحقًا."""

        return (
            self.standings[DependentStanding.HAS_PRECEDING_OPERATOR.name]
            + self.standings[DependentStanding.HAS_FOLLOWING_OPERATOR.name]
        )

    @property
    def preceding_share_of_decided(self) -> float:
        """حصّةُ «العاملُ سابقٌ» من المحسوم؛ و`0.0` حين لا محسومَ أصلًا."""

        if self.decided == 0:
            return 0.0
        return (
            self.standings[DependentStanding.HAS_PRECEDING_OPERATOR.name] / self.decided
        )

    @property
    def most_common_distance(self) -> int | None:
        """المسافةُ الأشيعُ بالكلمات؛ و`None` حين لا مسافةَ رُصِدت البتّة."""

        if not self.distances:
            return None
        return max(
            sorted(self.distances), key=lambda distance: self.distances[distance]
        )


def measure_relations(
    records: Sequence[Mapping[str, str]],
    *,
    corpus_digest: str = MASAQ_SHA256,
) -> RelationCensus:
    """اقرأ منزلةَ كلّ معمولٍ داخل آيته، ومسافةَ أقربِ عاملٍ إليه بالكلمات.

    `ARelationNeedsTwoPresentTerms`: المجالُ الآيةُ الواحدة، ولا يُجاوَز بها
    حدُّها. والأقربُ سابقًا مُقدَّمٌ على الأقرب لاحقًا، لأنّ التوقّعَ المُجمَّد
    في السبق فيُقاس عليه لا يُصاغ بعده.
    """

    positions = stem_positions(records)
    by_verse: dict[VerseKey, list[StemPosition]] = {}
    unreadable = 0
    for position in positions:
        if position.word_number is None:
            unreadable += 1
            continue
        by_verse.setdefault(position.verse, []).append(position)

    standings = {standing.name: 0 for standing in DependentStanding}
    distances: dict[int, int] = {}
    operators = 0
    dependents = 0
    for verse_positions in by_verse.values():
        operator_words = sorted(
            {
                position.word_number
                for position in verse_positions
                if position.side is RoleSide.OPERATOR
                and position.word_number is not None
            }
        )
        operators += sum(
            1 for position in verse_positions if position.side is RoleSide.OPERATOR
        )
        for position in verse_positions:
            if position.side is not RoleSide.DEPENDENT:
                continue
            dependents += 1
            word = position.word_number
            if word is None:
                continue
            preceding = [other for other in operator_words if other < word]
            following = [other for other in operator_words if other > word]
            if preceding:
                standing = DependentStanding.HAS_PRECEDING_OPERATOR
                distance = word - preceding[-1]
            elif following:
                standing = DependentStanding.HAS_FOLLOWING_OPERATOR
                distance = following[0] - word
            else:
                standings[DependentStanding.NO_OPERATOR_OBSERVED.name] += 1
                continue
            standings[standing.name] += 1
            distances[distance] = distances.get(distance, 0) + 1
    return RelationCensus(
        standings=standings,
        distances=distances,
        operators=operators,
        dependents=dependents,
        unreadable_word_keys=unreadable,
        preregistration_digest=IRAB_OPERATOR_PREREGISTRATION_DIGEST,
        corpus_digest=corpus_digest,
    )


def census_from_bytes(
    data: bytes,
) -> tuple[StemCoverageReading, ResidueCensus, RelationCensus]:
    """اقرأ السجلّات من بايتاتٍ مُطابَقةٍ سلفًا، ثمّ أخرِج القياسات الثلاثة.

    والبايتاتُ تأتي من `read_masaq_bytes` وحدَها: هي التي تُطابِق الطولَ
    والبصمةَ قبل القراءة. `NoFigureWithoutTheFingerprintedBytes`.
    """

    try:
        records = masaq_records(data)
    except MasaqDepositError as error:
        raise IrabOperatorCensusError(
            f"لم تُقرأ سجلّاتُ المدوَّنة: {error}. "
            + NO_FIGURE_WITHOUT_THE_FINGERPRINTED_BYTES_NOTE
        ) from error
    return (
        read_stem_coverage(records),
        measure_residue(records),
        measure_relations(records),
    )


ARRIVING_RESIDUE_STEMS: Final[int] = ARRIVING_ROLE_COVERAGE_ON_STEMS.residue_count
"""٢٤٦ جذعًا؛ مُشتقّةً من المقام والمُغطّى لا مكتوبةً رقمًا ثالثًا يفترق عنهما."""


ARRIVING_RESIDUE_VERSES: Final[int] = sum(
    account.verses for account in ARRIVING_RESIDUE_ACCOUNT
)
"""١٩٠ آيةً؛ مجموعَ الأنماط الثلاثة لا عددًا رابعًا يُكتَب بيد."""
