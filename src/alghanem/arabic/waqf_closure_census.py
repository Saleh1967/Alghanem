"""قياسُ انغلاق الوحدات الإسنادية: ثلاثةُ أنماطٍ وثلاثُ منازلَ داخل الآية.

هذا تشغيلُ `waqf_closure_preregistration` لا تعديلٌ له: لا كاشفَ أُضيف بعد
رقم، ولا نمطٌ بُدِّل لتُطابِق نسبة، ولا رقمٌ يخرج من هنا إلّا وقاعدةُ عدِّه
مُجمَّدةٌ هناك وبصمتُها مربوطةٌ به.

`NoFigureWithoutTheFingerprintedBytes`: السجلّاتُ تأتي من `masaq_records` على
بايتاتٍ طُوبِق طولُها وبصمتُها؛ فإن غابت **لم يخرج رقم**.

`AClosureIsInferredFromNeighbourhoodNotTagged`: الإغلاقُ استنتاجٌ من حضور
الطرفين داخل الآية، و`AVerseBoundaryIsNotASentenceBoundary` حدُّ ذلك: المفتوحةُ
هنا قد تكون مُغلَقةً بطرفٍ في الآية التالية، ولا تُوصَل آيةٌ بآيةٍ ليكتمل عدد.

`APhraseIsNotAClause`: شبهُ الجملة **تابعةٌ في كلّ حال**، ولا تُرقَّى بحضور
متعلَّقٍ موسومٍ في آيتها؛ وحضورُه يُعَدُّ في حقلٍ باسمه لا في منزلتها.

`APartialScanForbidsATotalDenial`: النفيُ — «هذه القيمةُ ليست في العمود» —
لا يخرج من هذه الوحدة إلّا من `scan_column_values` الذي يمرّ على قيم العمود
كلِّها؛ ولا يُنفى شيءٌ من فحص بعضها.

`ANullifiedDenominatorIsNotAZero`: الحفظُ مسنونٌ — مُغلَقة + مفتوحة + تابعة =
المفاتيحُ بالضبط — ويُفحَص في `ClosureCensus.conserves_the_denominator`، فإن
اختلّ ظهر اختلالُه ولم يُصحَّح بجمعٍ يُعدَّل.

وهذه الوحدة قياسٌ لا سلطة: لا ولادةَ فيها، ولا حكمَ ولادة، ولا تجميدَ `E0`،
ولا تستورد من `kernel/` شيئًا، ولا تقرؤها وحدةٌ فيه.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Final

from .irab_column_census import value_counts
from .irab_column_preregistration import (
    ANCHOR_COLUMN_NAME,
    PHRASAL_FUNCTION_COLUMN,
    SEGMENT_INDEX_COLUMN_NAME,
    SYNTACTIC_ROLE_COLUMN,
    WORD_KEY_COLUMN_NAME,
)
from .irab_operator_census import (
    NO_FIGURE_WITHOUT_THE_FINGERPRINTED_BYTES_NOTE,
    VerseKey,
    verse_key_of,
)
from .irab_operator_preregistration import (
    STEM_MORPH_TYPE,
    DeclaredDenominator,
)
from .masaq_corpus_deposit import (
    MASAQ_SHA256,
    MasaqDepositError,
    masaq_records,
)
from .waqf_closure_preregistration import (
    A_PARTIAL_SCAN_FORBIDS_A_TOTAL_DENIAL_NOTE,
    A_PHRASE_IS_NOT_A_CLAUSE_NOTE,
    A_THIN_COLUMN_IS_NOT_A_THICK_ONE_NOTE,
    A_VALUE_WITHOUT_ITS_COLUMN_IS_TWO_VALUES_NOTE,
    A_VERSE_BOUNDARY_IS_NOT_A_SENTENCE_BOUNDARY_NOTE,
    CLOSURE_CENSUS_COLUMNS,
    CLOSURE_DETECTORS,
    KEY_DENOMINATOR,
    WAQF_CLOSURE_PREREGISTRATION_DIGEST,
    ClauseKind,
    ClosureStanding,
    TermSide,
    closing_detectors_for,
    detector_for,
)

__all__ = [
    "A_NULLIFIED_DENOMINATOR_IS_NOT_A_ZERO_NOTE",
    "CLAIMED_KEYS_BY_KIND",
    "CLOSURE_SCANNED_COLUMNS",
    "WAQF_CLOSURE_CENSUS_NAMED_RESIDUALS",
    "ClauseUnit",
    "ClosureCensus",
    "ColumnValueScan",
    "TaggedTerm",
    "WaqfClosureCensusError",
    "census_from_bytes",
    "clause_units",
    "closing_values_absent_from_their_columns",
    "measure_closure",
    "scan_column_values",
    "tagged_terms",
    "value_is_absent_from_the_column",
]


class WaqfClosureCensusError(ValueError):
    """تُرفَع حين يُطلَب عددٌ من عمودٍ غائبٍ أو من بايتاتٍ لم تُقرأ سجلّاتُها."""


A_NULLIFIED_DENOMINATOR_IS_NOT_A_ZERO_NOTE: Final[str] = (
    "ANullifiedDenominatorIsNotAZero: مجموعُ المنازل الثلاث يساوي المفاتيحَ "
    "بالضبط، ويُفحَص لا يُفترَض؛ فإن اختلّ الحفظُ ظهر اختلالُه ولم يُغطَّ "
    "بجمعٍ يُعدَّل ولا بمنزلةٍ رابعةٍ تُصطنَع"
)

WAQF_CLOSURE_CENSUS_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "NoFigureWithoutTheFingerprintedBytes": (
        NO_FIGURE_WITHOUT_THE_FINGERPRINTED_BYTES_NOTE
    ),
    "ANullifiedDenominatorIsNotAZero": A_NULLIFIED_DENOMINATOR_IS_NOT_A_ZERO_NOTE,
    "APartialScanForbidsATotalDenial": A_PARTIAL_SCAN_FORBIDS_A_TOTAL_DENIAL_NOTE,
    "AVerseBoundaryIsNotASentenceBoundary": (
        A_VERSE_BOUNDARY_IS_NOT_A_SENTENCE_BOUNDARY_NOTE
    ),
    "APhraseIsNotAClause": A_PHRASE_IS_NOT_A_CLAUSE_NOTE,
    "AThinColumnIsNotAThickOne": A_THIN_COLUMN_IS_NOT_A_THICK_ONE_NOTE,
    "AValueWithoutItsColumnIsTwoValues": A_VALUE_WITHOUT_ITS_COLUMN_IS_TWO_VALUES_NOTE,
}


CLOSURE_SCANNED_COLUMNS: Final[tuple[str, ...]] = (
    SYNTACTIC_ROLE_COLUMN,
    PHRASAL_FUNCTION_COLUMN,
)
"""العمودان اللذان تُقرأ منهما الأطراف؛ ولكلّ كاشفٍ عمودُه لا اسمُه وحدَه."""


def _require_columns(records: Sequence[Mapping[str, str]]) -> None:
    """احرسْ حضورَ الأعمدة السبعة؛ وغيابُ واحدٍ يُوقِف العدَّ ولا يُصفِّره."""

    if not records:
        raise WaqfClosureCensusError(
            "لا سجلَّ يُقرأ؛ ولا يُخرَج عددٌ من ملفٍّ بلا سجلّات. "
            + NO_FIGURE_WITHOUT_THE_FINGERPRINTED_BYTES_NOTE
        )
    for column in CLOSURE_CENSUS_COLUMNS:
        if column not in records[0]:
            raise WaqfClosureCensusError(
                f"العمودُ «{column}» غائبٌ عن الترويسة؛ ولا يُحمَل على أقرب "
                "اسمٍ إليه، فالعدُّ يقف."
            )


@dataclass(frozen=True, slots=True)
class TaggedTerm:
    """طرفٌ موسومٌ واحد: آيتُه، ومفتاحُ كلمته، ومقطعُه، وزوجُ عموده وقيمته."""

    verse: VerseKey
    word_number: int | None
    segment_index: str
    column: str
    value: str
    kind: ClauseKind
    side: TermSide


def _word_number(record: Mapping[str, str]) -> int | None:
    """مفتاحُ الكلمة عددًا؛ و`None` لِما لا يُقرأ عددًا، ولا يُسقَط الصفُّ به."""

    raw = record.get(WORD_KEY_COLUMN_NAME, "").strip()
    try:
        return int(raw)
    except ValueError:
        return None


def tagged_terms(records: Sequence[Mapping[str, str]]) -> tuple[TaggedTerm, ...]:
    """الأطرافُ الموسومةُ كلُّها في الجذوع وحدَها، بترتيب ورودها.

    والصفُّ الواحد قد يحمل طرفَين — في `Syntactic_Role` و`Phrasal_Function`
    معًا — فيخرج طرفان لا طرفٌ واحدٌ يُغلَّب على الآخر؛ وذلك نصُّ
    `AValueWithoutItsColumnIsTwoValues` مطبَّقًا على الصفّ نفسِه.
    """

    _require_columns(records)
    terms: list[TaggedTerm] = []
    for record in records:
        if record.get(ANCHOR_COLUMN_NAME, "").strip() != STEM_MORPH_TYPE:
            continue
        for column in CLOSURE_SCANNED_COLUMNS:
            value = record.get(column, "").strip()
            if not value:
                continue
            detector = detector_for(column, value)
            if detector is None:
                continue
            terms.append(
                TaggedTerm(
                    verse=verse_key_of(record),
                    word_number=_word_number(record),
                    segment_index=record.get(SEGMENT_INDEX_COLUMN_NAME, "").strip(),
                    column=column,
                    value=value,
                    kind=detector.kind,
                    side=detector.side,
                )
            )
    return tuple(terms)


@dataclass(frozen=True, slots=True)
class ClauseUnit:
    """وحدةٌ واحدة: مفتاحُها الفاتح، ونمطُها، ومنزلتُها من الثلاث.

    `AClosureIsInferredFromNeighbourhoodNotTagged`: `standing` مُستنتَجةٌ من
    حضور طرفٍ مُغلِقٍ من نمطها في آيتها، لا مقروءةٌ من عمودٍ يقولها.
    """

    key: TaggedTerm
    standing: ClosureStanding
    attachment_observed: bool

    def __post_init__(self) -> None:
        if self.key.side is not TermSide.OPENING:
            raise WaqfClosureCensusError(
                "لا تقوم وحدةٌ إلّا على طرفٍ فاتح؛ والمُغلِقُ لا يُفتَح به إسناد."
            )
        if (
            self.key.kind is ClauseKind.PHRASE
            and self.standing is not ClosureStanding.DEPENDENT
        ):
            raise WaqfClosureCensusError(
                "شبهُ الجملة تابعةٌ في كلّ حال. " + A_PHRASE_IS_NOT_A_CLAUSE_NOTE
            )
        if (
            self.key.kind is not ClauseKind.PHRASE
            and self.standing is ClosureStanding.DEPENDENT
        ):
            raise WaqfClosureCensusError(
                "«تابعة» منزلةُ شبه الجملة وحدَها؛ ولا تُدفَع إليها جملةٌ "
                "لم ينغلق طرفاها، فتلك «مفتوحة» باسمها."
            )


def clause_units(records: Sequence[Mapping[str, str]]) -> tuple[ClauseUnit, ...]:
    """كلُّ مفتاحٍ وحدةٌ، ومنزلتُها من حضور طرفٍ مُغلِقٍ من نمطها في آيتها.

    `AVerseBoundaryIsNotASentenceBoundary`: المجالُ الآيةُ الواحدة، ولا
    يُجاوَز بها حدُّها ولو كان الطرفُ المُغلِقُ في الآية التي تليها.
    """

    terms = tagged_terms(records)
    closing_kinds_by_verse: dict[VerseKey, set[ClauseKind]] = {}
    opening_kinds_by_verse: dict[VerseKey, set[ClauseKind]] = {}
    for term in terms:
        bucket = (
            closing_kinds_by_verse
            if term.side is TermSide.CLOSING
            else opening_kinds_by_verse
        )
        bucket.setdefault(term.verse, set()).add(term.kind)

    units: list[ClauseUnit] = []
    for term in terms:
        if term.side is not TermSide.OPENING:
            continue
        closing_kinds = closing_kinds_by_verse.get(term.verse, set())
        if term.kind is ClauseKind.PHRASE:
            # المتعلَّقُ المرصود: فاتحُ جملةٍ اسميةٍ أو فعليةٍ في الآية نفسِها.
            attachment = bool(
                (opening_kinds_by_verse.get(term.verse, set()) | closing_kinds)
                - {ClauseKind.PHRASE}
            )
            units.append(
                ClauseUnit(
                    key=term,
                    standing=ClosureStanding.DEPENDENT,
                    attachment_observed=attachment,
                )
            )
            continue
        closed = term.kind in closing_kinds
        units.append(
            ClauseUnit(
                key=term,
                standing=(ClosureStanding.CLOSED if closed else ClosureStanding.OPEN),
                attachment_observed=closed,
            )
        )
    return tuple(units)


@dataclass(frozen=True, slots=True)
class ColumnValueScan:
    """مسحٌ تامٌّ لقيم عمودٍ واحد؛ وبه وحدَه يجوز نفيُ وجود قيمة."""

    column: str
    distinct_values: int
    scanned_values: tuple[str, ...]

    def contains(self, value: str) -> bool:
        """أفي العمود هذه القيمةُ حرفيًّا؟ جوابٌ عن مسحٍ تامٍّ لا عن عيّنة."""

        return value.strip() in self.scanned_values


def scan_column_values(
    records: Sequence[Mapping[str, str]], column: str
) -> ColumnValueScan:
    """امسحْ قيمَ العمود كلَّها؛ ولا نفيَ إلّا بعد هذا المرور.

    `APartialScanForbidsATotalDenial`.
    """

    _require_columns(records)
    if column not in CLOSURE_SCANNED_COLUMNS:
        raise WaqfClosureCensusError(
            f"العمودُ «{column}» ليس من عمودَي الأطراف؛ ولا يُمسَح هنا عمودٌ "
            "لم يُجمَّد أنّه يحمل طرفًا. " + A_VALUE_WITHOUT_ITS_COLUMN_IS_TWO_VALUES_NOTE
        )
    counts = value_counts(records, column)
    scanned = tuple(sorted(counts))
    return ColumnValueScan(
        column=column,
        distinct_values=len(scanned),
        scanned_values=scanned,
    )


def value_is_absent_from_the_column(
    records: Sequence[Mapping[str, str]], column: str, value: str
) -> bool:
    """أغابت القيمةُ عن العمود؟ جوابٌ لا يخرج إلّا بعد مسحٍ تامّ."""

    return not scan_column_values(records, column).contains(value)


@dataclass(frozen=True, slots=True)
class ClosureCensus:
    """أعدادُ الوحدات بأنماطها ومنازلها، بمقامها المُعلَن لا بدونه."""

    denominator: DeclaredDenominator
    units_by_kind_and_standing: dict[str, dict[str, int]]
    attachments_observed: dict[str, int]
    unreadable_word_keys: int
    preregistration_digest: str
    corpus_digest: str

    @property
    def keys_total(self) -> int:
        """جملةُ المفاتيح: مقامُ هذه الأداة، معدودةً لا مشتقّةً من نسبة."""

        return sum(
            sum(standings.values())
            for standings in self.units_by_kind_and_standing.values()
        )

    def count(self, kind: ClauseKind, standing: ClosureStanding) -> int:
        """عددُ الوحدات في نمطٍ ومنزلة؛ والصفرُ هنا خبرٌ عن العدّ لا عن غيابه."""

        return self.units_by_kind_and_standing[kind.name][standing.name]

    def keys_of(self, kind: ClauseKind) -> int:
        """مفاتيحُ نمطٍ واحد بمنازله الثلاث."""

        return sum(self.units_by_kind_and_standing[kind.name].values())

    @property
    def conserves_the_denominator(self) -> bool:
        """أحُفِظ المقام: مُغلَقة + مفتوحة + تابعة = المفاتيحُ بالضبط؟"""

        total = sum(
            self.count(kind, standing)
            for kind in ClauseKind
            if kind is not ClauseKind.OUTSIDE_THE_DETECTORS
            for standing in ClosureStanding
        )
        return total == self.keys_total

    @property
    def no_phrase_is_closed(self) -> bool:
        """أبقيت شبهُ الجملة تابعةً كلَّها؟ `APhraseIsNotAClause` مقروءًا عدًّا."""

        return (
            self.count(ClauseKind.PHRASE, ClosureStanding.CLOSED) == 0
            and self.count(ClauseKind.PHRASE, ClosureStanding.OPEN) == 0
        )

    def open_share(self, kind: ClauseKind) -> float:
        """حصّةُ «المفتوحة» من مفاتيح النمط؛ و`0.0` حين لا مفتاحَ أصلًا.

        `AThinColumnIsNotAThickOne`: حصّةُ الاسمية تُقرأ أوّلًا خلوَّ عمود
        `Phrasal_Function` لا انفتاحَ جملةٍ في العربية.
        """

        keys = self.keys_of(kind)
        if keys == 0:
            return 0.0
        return self.count(kind, ClosureStanding.OPEN) / keys


def measure_closure(
    records: Sequence[Mapping[str, str]],
    *,
    corpus_digest: str = MASAQ_SHA256,
) -> ClosureCensus:
    """اقرأ منزلةَ كلّ مفتاحٍ داخل آيته، بأنماطٍ وثلاثِ منازلَ لا يجمعها صفر."""

    counts: dict[str, dict[str, int]] = {
        kind.name: {standing.name: 0 for standing in ClosureStanding}
        for kind in ClauseKind
        if kind is not ClauseKind.OUTSIDE_THE_DETECTORS
    }
    attachments = {
        kind.name: 0
        for kind in ClauseKind
        if kind is not ClauseKind.OUTSIDE_THE_DETECTORS
    }
    unreadable = 0
    for unit in clause_units(records):
        counts[unit.key.kind.name][unit.standing.name] += 1
        if unit.attachment_observed:
            attachments[unit.key.kind.name] += 1
        if unit.key.word_number is None:
            unreadable += 1
    return ClosureCensus(
        denominator=KEY_DENOMINATOR,
        units_by_kind_and_standing=counts,
        attachments_observed=attachments,
        unreadable_word_keys=unreadable,
        preregistration_digest=WAQF_CLOSURE_PREREGISTRATION_DIGEST,
        corpus_digest=corpus_digest,
    )


def closing_values_absent_from_their_columns(
    records: Sequence[Mapping[str, str]],
) -> tuple[tuple[str, str], ...]:
    """أزواجُ الكواشف المُغلِقة الغائبةُ عن أعمدتها بعد مسحٍ تامٍّ لكلٍّ منها.

    `AClaimedValueAbsentIsNotAZeroCount` معناه هنا: هذه أزواجٌ **غابت صياغتُها**
    عن العمود، لا أبوابٌ عُدِمت من العربية. `APartialScanForbidsATotalDenial`.
    """

    scans = {
        column: scan_column_values(records, column)
        for column in CLOSURE_SCANNED_COLUMNS
    }
    absent: list[tuple[str, str]] = []
    for kind in (ClauseKind.NOMINAL, ClauseKind.VERBAL):
        for detector in closing_detectors_for(kind):
            if not scans[detector.column].contains(detector.value):
                absent.append(detector.key)
    return tuple(absent)


def census_from_bytes(data: bytes) -> ClosureCensus:
    """اقرأ السجلّات من بايتاتٍ مُطابَقةٍ سلفًا، ثمّ أخرِج قياسَ الانغلاق.

    والبايتاتُ تأتي من `read_masaq_bytes` وحدَها: هي التي تُطابِق الطولَ
    والبصمةَ قبل القراءة. `NoFigureWithoutTheFingerprintedBytes`.
    """

    try:
        records = masaq_records(data)
    except MasaqDepositError as error:
        raise WaqfClosureCensusError(
            f"لم تُقرأ سجلّاتُ المدوَّنة: {error}. "
            + NO_FIGURE_WITHOUT_THE_FINGERPRINTED_BYTES_NOTE
        ) from error
    return measure_closure(records)


CLAIMED_KEYS_BY_KIND: Final[dict[str, int]] = {
    kind.name: sum(
        detector.claimed_segment_count
        for detector in CLOSURE_DETECTORS
        if detector.kind is kind and detector.side is TermSide.OPENING
    )
    for kind in ClauseKind
    if kind is not ClauseKind.OUTSIDE_THE_DETECTORS
}
"""مفاتيحُ كلّ نمطٍ مجموعةً من الأعداد المُجمَّدة؛ مجموعٌ مُشتَقٌّ لا رقمٌ رابع.

وهي **أعدادُ مقاطعَ في المدوَّنة كلِّها** لا أعدادُ وحداتٍ مقيسةٍ هنا: المقيسُ
يخرج من `measure_closure` على البايتات المُبصَّمة، وهذا مجموعُ ما جُمِّد قبلها؛
ومقامُ أحدهما ليس مقامَ الآخر، فلا يُقرأ هذا المجموعُ نتيجةَ قياس.
"""
