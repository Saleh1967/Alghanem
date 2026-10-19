"""حصرُ مرشَّحي الإحالة لكلّ ضميرٍ مُقيَّد، وإحصاءُ حجمِ المجموعة لا اختيارُ واحد.

هذا تشغيلُ `referent_candidate_preregistration` لا تعديلٌ له: لا نافذةَ وُسِّعت
بعد الرقم، ولا وسمٌ أُضيف إلى المقام حتّى تَحسُنَ نسبةٌ، ولا لاحقةٌ سُنَّت بعد
رؤية ما تُخرجه.

**الأداةُ تُخرِج مجموعةَ مرشَّحين لكلّ ضمير، ولا تختار منها واحدًا أبدًا.**
ولا رقمَ دقّةٍ ولا استدعاءٍ هنا — لا لضعفِ قاعدةٍ بل لأنّ **المرجعَ الصحيح غير
موسومٍ في أيّ مصدرٍ بين أيدينا**، فلا ذهبَ يُقاس عليه. والمخرَجُ المشروعُ:
**حجمُ المجموعة، ونسبةُ ما يُحصَر لمرشَّحٍ واحد، ومواضعُ العجز مسرودةً**.

`NoFigureWithoutTheFingerprintedBytes`: السجلّاتُ تأتي من `masaq_records` على
بايتاتٍ طُوبِق طولُها وبصمتُها؛ فإن غابت **لم يخرج رقم**.

`AnUnreadablePositionIsCountedNotDropped`: صفٌّ لا تُقرأ سورتُه أو آيتُه أو
مفتاحُ كلمته أو فهرسُ مقطعه عددًا صحيحًا لا يدخل نافذةً ولا ترتيبًا، ويُعَدُّ
في حقلٍ باسمه؛ فإسقاطُه صامتًا يُنقِص مقامًا بلا أثرٍ يُرى.

`FourStandingsAndNoZeroGathersThem`: لكلّ ضميرٍ منزلةٌ مُسمّاة — مرشَّحٌ واحدٌ،
أو مرشَّحون متعدّدون، أو **صفرُ مرشَّح**، أو **طرفُ خطابٍ** لا يُحال لاسمٍ سابق
أصلًا. والثالثةُ والرابعةُ تُسمَّيان ولا تُبتلَعان في صفرٍ واحد.

`APrecisionFieldIsRefusedNotIgnored`: بنيةُ المخرَج ترفع خطأً إن حُقِن فيها حقلُ
دقّةٍ أو استدعاءٍ أو صوابٍ؛ فالرفضُ في البنية أبقى من تنبيهٍ في وثيقة.

وهذه الوحدة تسجيلٌ لا سلطة: لا ولادةَ فيها، ولا حكمَ ولادة، ولا تجميدَ `E0`،
ولا تستورد من `kernel/` شيئًا، ولا تقرؤها وحدةٌ فيه.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Final

from .irab_column_census import SURA_COLUMN, VERSE_COLUMN
from .irab_column_preregistration import (
    ANCHOR_COLUMN_NAME,
    SEGMENT_INDEX_COLUMN_NAME,
    WORD_KEY_COLUMN_NAME,
)
from .masaq_corpus_deposit import MASAQ_SHA256, MORPH_TAG_COLUMN
from .referent_candidate_preregistration import (
    A_CANDIDATE_SET_IS_NOT_AN_ANSWER_NOTE,
    A_WINDOW_IS_DECLARED_NOT_OPTIMISED_NOTE,
    AN_UNDETERMINED_INFERENCE_IS_NOT_A_MATCH_NOTE,
    AN_UNPARSED_TAG_YIELDS_NO_CONSTRAINT_NOTE,
    DECLARED_DENOMINATOR_COUNT,
    ELEVEN_PERCENT_IS_THE_REAL_DENOMINATOR_NOTE,
    GENDER_AND_NUMBER_ARE_INFERRED_NOT_TAGGED_NOTE,
    NO_FIGURE_WITHOUT_THE_FINGERPRINTED_BYTES_NOTE,
    REFERENT_CANDIDATE_PREREGISTRATION_DIGEST,
    SEARCH_WINDOW,
    SEGMENTED_WORD_COLUMN,
    STEM_MORPH_TYPE,
    THE_HOST_WORD_IS_NOT_ITS_OWN_CANDIDATE_NOTE,
    THE_REFERENT_IS_NOT_ANNOTATED_ANYWHERE_NOTE,
    Gender,
    PronounConstraint,
    SurfaceInference,
    constraints_of,
    infer_surface,
    is_nominal_tag,
)

__all__ = [
    "A_PRECISION_FIELD_IS_REFUSED_NOT_IGNORED_NOTE",
    "DECLARED_DENOMINATOR_NOTE",
    "AN_UNREADABLE_POSITION_IS_COUNTED_NOT_DROPPED_NOTE",
    "FOUR_STANDINGS_AND_NO_ZERO_GATHERS_THEM_NOTE",
    "REFUSED_FIELD_STEMS",
    "REFERENT_CANDIDATE_CENSUS_NAMED_RESIDUALS",
    "CandidateSet",
    "CandidateSetCensus",
    "CandidateStanding",
    "NominalPosition",
    "PronounPosition",
    "ReferentCandidateCensusError",
    "SegmentPosition",
    "candidates_for",
    "enumerate_candidate_sets",
    "matches",
    "measure_candidates",
    "nominal_positions",
    "pronoun_positions",
    "refuse_gold_fields",
    "size_by_constraint",
]


class ReferentCandidateCensusError(ValueError):
    """تُرفَع حين يُطلَب عددٌ من عمودٍ غائب، أو يُحقَن حقلُ دقّةٍ في مخرَج."""


AN_UNREADABLE_POSITION_IS_COUNTED_NOT_DROPPED_NOTE: Final[str] = (
    "AnUnreadablePositionIsCountedNotDropped: صفٌّ لا يُقرأ موضعُه عددًا "
    "صحيحًا لا يدخل نافذةً ولا ترتيبًا، ويُعَدُّ في حقلٍ باسمه؛ فإسقاطُه "
    "صامتًا يُنقِص مقامًا بلا أثرٍ يُرى"
)

FOUR_STANDINGS_AND_NO_ZERO_GATHERS_THEM_NOTE: Final[str] = (
    "FourStandingsAndNoZeroGathersThem: مرشَّحٌ واحدٌ، أو متعدّدون، أو صفرُ "
    "مرشَّحٍ، أو طرفُ خطابٍ لا يُطلَب له اسمٌ سابق؛ أربعُ منازلَ مُسمّاةٍ لا "
    "يجمعها صفرٌ واحدٌ ولا تُخفى إحداها في أخرى"
)

A_PRECISION_FIELD_IS_REFUSED_NOT_IGNORED_NOTE: Final[str] = (
    "APrecisionFieldIsRefusedNotIgnored: حقلُ دقّةٍ أو استدعاءٍ أو صوابٍ في "
    "مخرَج هذه الأداة يُرفَع به خطأٌ في البنية نفسها، لا يُهمَل؛ فلا ذهبَ "
    "يُقاس عليه. " + THE_REFERENT_IS_NOT_ANNOTATED_ANYWHERE_NOTE
)

REFERENT_CANDIDATE_CENSUS_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "NoFigureWithoutTheFingerprintedBytes": (
        NO_FIGURE_WITHOUT_THE_FINGERPRINTED_BYTES_NOTE
    ),
    "AnUnreadablePositionIsCountedNotDropped": (
        AN_UNREADABLE_POSITION_IS_COUNTED_NOT_DROPPED_NOTE
    ),
    "FourStandingsAndNoZeroGathersThem": FOUR_STANDINGS_AND_NO_ZERO_GATHERS_THEM_NOTE,
    "APrecisionFieldIsRefusedNotIgnored": A_PRECISION_FIELD_IS_REFUSED_NOT_IGNORED_NOTE,
    "TheReferentIsNotAnnotatedAnywhere": THE_REFERENT_IS_NOT_ANNOTATED_ANYWHERE_NOTE,
    "ACandidateSetIsNotAnAnswer": A_CANDIDATE_SET_IS_NOT_AN_ANSWER_NOTE,
    "ElevenPercentIsTheRealDenominator": ELEVEN_PERCENT_IS_THE_REAL_DENOMINATOR_NOTE,
    "GenderAndNumberAreInferredNotTagged": (
        GENDER_AND_NUMBER_ARE_INFERRED_NOT_TAGGED_NOTE
    ),
    "AnUnparsedTagYieldsNoConstraint": AN_UNPARSED_TAG_YIELDS_NO_CONSTRAINT_NOTE,
    "AWindowIsDeclaredNotOptimised": A_WINDOW_IS_DECLARED_NOT_OPTIMISED_NOTE,
    "AnUndeterminedInferenceIsNotAMatch": (
        AN_UNDETERMINED_INFERENCE_IS_NOT_A_MATCH_NOTE
    ),
    "TheHostWordIsNotItsOwnCandidate": THE_HOST_WORD_IS_NOT_ITS_OWN_CANDIDATE_NOTE,
}


REFUSED_FIELD_STEMS: Final[tuple[str, ...]] = (
    "precision",
    "recall",
    "f1",
    "fscore",
    "f_score",
    "accuracy",
    "gold",
    "truth",
    "correct",
    "referent",
)
"""جذورُ الأسماء المرفوضةِ في مخرَج هذه الأداة؛ مرفوضةً لا مُهمَلة."""


def refuse_gold_fields(payload: Mapping[str, Any]) -> None:
    """ارفضْ أيَّ حقلٍ يدّعي ذهبًا أو دقّةً؛ والرفضُ في البنية لا في وثيقة."""

    for name in payload:
        lowered = name.lower()
        for stem in REFUSED_FIELD_STEMS:
            if stem in lowered:
                raise ReferentCandidateCensusError(
                    f"الحقلُ «{name}» يدّعي قياسًا إلى مرجعٍ موسوم. "
                    + A_PRECISION_FIELD_IS_REFUSED_NOT_IGNORED_NOTE
                )


def _require_columns(records: Sequence[Mapping[str, str]]) -> None:
    """احرسْ حضورَ الأعمدة السبعة؛ وغيابُ واحدٍ يُوقِف العدَّ ولا يُصفِّره."""

    if not records:
        raise ReferentCandidateCensusError(
            "لا سجلَّ يُقرأ؛ ولا يُخرَج عددٌ من ملفٍّ بلا سجلّات. "
            + NO_FIGURE_WITHOUT_THE_FINGERPRINTED_BYTES_NOTE
        )
    for column in (
        SURA_COLUMN,
        VERSE_COLUMN,
        ANCHOR_COLUMN_NAME,
        MORPH_TAG_COLUMN,
        WORD_KEY_COLUMN_NAME,
        SEGMENT_INDEX_COLUMN_NAME,
        SEGMENTED_WORD_COLUMN,
    ):
        if column not in records[0]:
            raise ReferentCandidateCensusError(
                f"العمودُ «{column}» غائبٌ عن الترويسة؛ ولا يُحمَل على أقرب "
                "اسمٍ إليه، فالعدُّ يقف."
            )


@dataclass(frozen=True, slots=True)
class SegmentPosition:
    """موضعُ مقطعٍ واحدٍ عددًا: سورةٌ وآيةٌ ومفتاحُ كلمةٍ وفهرسُ مقطع."""

    sura: int
    verse: int
    word_number: int
    segment_index: int

    @property
    def order_key(self) -> tuple[int, int, int, int]:
        """مفتاحُ الترتيب الموضعيّ وحدَه؛ ولا أفضليّةَ في هذه الأداة البتّة."""

        return (self.sura, self.verse, self.word_number, self.segment_index)

    def precedes(self, other: SegmentPosition) -> bool:
        """أيقع هذا قبل ذاك في ترتيب الكلمات؟ مقارنةَ مواضعَ لا مقارنةَ قوّة."""

        return self.order_key < other.order_key

    def in_window_of(self, other: SegmentPosition) -> bool:
        """أيقع في نافذةِ ذاك المُعلَنة: آيتُه أو سابقتُها، في سورته وحدَها؟"""

        if self.sura != other.sura:
            return False
        return 0 <= other.verse - self.verse <= SEARCH_WINDOW.preceding_verses


def _integer(record: Mapping[str, str], column: str) -> int | None:
    """قيمةُ عمودٍ عددًا صحيحًا، و`None` لما لا يُقرأ — يُعَدُّ ولا يُسقَط."""

    try:
        return int(record.get(column, "").strip())
    except ValueError:
        return None


def _position_of(record: Mapping[str, str]) -> SegmentPosition | None:
    """موضعُ الصفّ إن قُرِئت أعدادُه الأربعة كلُّها، وإلّا `None` مُسمًّى."""

    values = [
        _integer(record, column)
        for column in (
            SURA_COLUMN,
            VERSE_COLUMN,
            WORD_KEY_COLUMN_NAME,
            SEGMENT_INDEX_COLUMN_NAME,
        )
    ]
    if any(value is None for value in values):
        return None
    sura, verse, word_number, segment_index = (int(value or 0) for value in values)
    return SegmentPosition(
        sura=sura, verse=verse, word_number=word_number, segment_index=segment_index
    )


@dataclass(frozen=True, slots=True)
class PronounPosition:
    """ضميرٌ مُقيَّدٌ في موضعه، بوسمه وثلاثيّتِه المُشتقّة من وسمه بالقاعدة."""

    position: SegmentPosition
    tag: str
    constraint: PronounConstraint


@dataclass(frozen=True, slots=True)
class NominalPosition:
    """اسمٌ في موضعه، بصورته وباستنتاج القاعدة عنه — استنتاجًا لا وَسْمًا."""

    position: SegmentPosition
    tag: str
    surface: str
    inference: SurfaceInference


def pronoun_positions(
    records: Sequence[Mapping[str, str]],
) -> tuple[tuple[PronounPosition, ...], int, int]:
    """الضمائرُ المُقيَّدةُ مرتَّبةً موضعيًّا، ومعها عدَّا المستبعَدَين بعلّتيهما.

    تُعيد ثلاثيّةً: المواضعُ، وعددُ الوسوم التي لم تُحلَّل إلى ثلاثية، وعددُ
    الصفوف التي لم يُقرأ موضعُها — وكلاهما يُعَدُّ ولا يُبتلَع في صفر.
    """

    _require_columns(records)
    positions: list[PronounPosition] = []
    unparsed = 0
    unreadable = 0
    for record in records:
        tag = record.get(MORPH_TAG_COLUMN, "").strip()
        if "PRON" not in tag:
            continue
        constraint = constraints_of(tag)
        if constraint is None:
            unparsed += 1
            continue
        position = _position_of(record)
        if position is None:
            unreadable += 1
            continue
        positions.append(
            PronounPosition(position=position, tag=tag, constraint=constraint)
        )
    positions.sort(key=lambda item: item.position.order_key)
    return tuple(positions), unparsed, unreadable


def nominal_positions(
    records: Sequence[Mapping[str, str]],
) -> tuple[tuple[NominalPosition, ...], int, int]:
    """الأسماءُ المُعلَنةُ مرتَّبةً موضعيًّا، وعددُ ما عجزت عنه القاعدةُ ومواضعُه.

    تُعيد ثلاثيّةً: المواضعُ، وعددُ الأسماء التي عجزت عنها قاعدةُ الاستنتاج،
    وعددُ الصفوف التي لم يُقرأ موضعُها.
    """

    _require_columns(records)
    positions: list[NominalPosition] = []
    undetermined = 0
    unreadable = 0
    for record in records:
        if record.get(ANCHOR_COLUMN_NAME, "").strip() != STEM_MORPH_TYPE:
            continue
        tag = record.get(MORPH_TAG_COLUMN, "").strip()
        if not is_nominal_tag(tag):
            continue
        position = _position_of(record)
        if position is None:
            unreadable += 1
            continue
        surface = record.get(SEGMENTED_WORD_COLUMN, "")
        inference = infer_surface(surface)
        if not inference.is_determined:
            undetermined += 1
        positions.append(
            NominalPosition(
                position=position, tag=tag, surface=surface, inference=inference
            )
        )
    positions.sort(key=lambda item: item.position.order_key)
    return tuple(positions), undetermined, unreadable


def matches(constraint: PronounConstraint, inference: SurfaceInference) -> bool:
    """أيوافق الاسمُ الضميرَ في العدد والجنس؟ والعجزُ لا يُقرأ موافقةً."""

    if not inference.is_determined:
        return False
    if inference.number is not constraint.number:
        return False
    if constraint.gender is Gender.UNSPECIFIED:
        return True
    return inference.gender is constraint.gender


class CandidateStanding(Enum):
    """منازلُ الضمير الأربعُ مُسمّاةً؛ ولا يجمع اثنتين منها صفرٌ واحد."""

    SINGLE = "مرشَّح_واحد"
    MULTIPLE = "مرشَّحون_متعدّدون"
    NONE = "صفر_مرشَّح"
    DISCOURSE_PARTICIPANT = "طرف_خطاب"


def candidates_for(
    pronoun: PronounPosition,
    nominals: Sequence[NominalPosition],
) -> tuple[NominalPosition, ...]:
    """مرشَّحو ضميرٍ واحدٍ تحت النافذة والقاعدة المُعلَنتين، بترتيبٍ موضعيّ.

    وضميرُ المتكلّم والمخاطَب يخرج من المطابقة الاسمية **قبل أيّ بحث**؛ فهو
    لأطراف الخطاب لا لاسمٍ سابق، فلا تُبنى له مجموعةٌ أصلًا.
    """

    if pronoun.constraint.is_discourse_participant:
        return ()
    return tuple(
        nominal
        for nominal in nominals
        if nominal.position.in_window_of(pronoun.position)
        and nominal.position.precedes(pronoun.position)
        and not (
            nominal.position.sura == pronoun.position.sura
            and nominal.position.verse == pronoun.position.verse
            and nominal.position.word_number == pronoun.position.word_number
        )
        and matches(pronoun.constraint, nominal.inference)
    )


@dataclass(frozen=True, slots=True)
class CandidateSet:
    """مجموعةُ مرشَّحي ضميرٍ واحدٍ بمنزلتها؛ ولا اسمَ فيها يُسمّى مرجعًا."""

    pronoun: PronounPosition
    candidates: tuple[NominalPosition, ...]

    @property
    def size(self) -> int:
        """حجمُ المجموعة عدًّا؛ وهو المخرَجُ المشروعُ لا اسمُ أحدِ أفرادها."""

        return len(self.candidates)

    @property
    def standing(self) -> CandidateStanding:
        """منزلةُ الضمير من المنازل الأربع المُسمّاة، بلا رابعٍ يبتلع ثالثًا."""

        if self.pronoun.constraint.is_discourse_participant:
            return CandidateStanding.DISCOURSE_PARTICIPANT
        if self.size == 0:
            return CandidateStanding.NONE
        if self.size == 1:
            return CandidateStanding.SINGLE
        return CandidateStanding.MULTIPLE


def enumerate_candidate_sets(
    records: Sequence[Mapping[str, str]],
) -> tuple[tuple[CandidateSet, ...], int, int, int]:
    """مجموعاتُ المرشَّحين كلُّها، ومعها الأعدادُ الثلاثةُ المُستبعَدةُ بعللها."""

    pronouns, unparsed, unreadable_pronouns = pronoun_positions(records)
    nominals, undetermined, _unreadable_nominals = nominal_positions(records)
    sets = tuple(
        CandidateSet(pronoun=pronoun, candidates=candidates_for(pronoun, nominals))
        for pronoun in pronouns
    )
    return sets, unparsed, unreadable_pronouns, undetermined


@dataclass(frozen=True, slots=True)
class CandidateSetCensus:
    """إحصاءُ الحصر: مقامٌ ومنازلُ ومتوسّطٌ بمقامه ومواضعُ عجزٍ مسرودة.

    ولا حقلَ دقّةٍ فيها ولا استدعاءٍ ولا مرجعٍ مُسمًّى — يُرفَع بها خطأٌ في
    `__post_init__` لا تُهمَل.
    """

    denominator: int
    standings: dict[str, int]
    candidate_total: int
    zero_candidate_positions: tuple[tuple[int, int, int, int], ...]
    unparsed_tags: int
    unreadable_pronoun_positions: int
    undetermined_nominals: int
    preregistration_digest: str
    corpus_digest: str
    extra_fields: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        refuse_gold_fields(self.extra_fields)
        for name in type(self).__dataclass_fields__:
            lowered = name.lower()
            for stem in REFUSED_FIELD_STEMS:
                if stem in lowered:  # pragma: no cover - يمنعه اسمُ الحقل نفسُه
                    raise ReferentCandidateCensusError(
                        f"حقلُ «{name}» في بنية المخرَج. "
                        + A_PRECISION_FIELD_IS_REFUSED_NOT_IGNORED_NOTE
                    )
        missing = [
            standing.value
            for standing in CandidateStanding
            if standing.value not in self.standings
        ]
        if missing:
            raise ReferentCandidateCensusError(
                f"منازلُ لم تُسمَّ في المخرَج: {missing}. "
                + FOUR_STANDINGS_AND_NO_ZERO_GATHERS_THEM_NOTE
            )
        if sum(self.standings.values()) != self.denominator:
            raise ReferentCandidateCensusError(
                "مجموعُ المنازل خالف المقام؛ ولا يُطوى الفرقُ في منزلةٍ. "
                + FOUR_STANDINGS_AND_NO_ZERO_GATHERS_THEM_NOTE
            )
        if self.nominal_denominator != (
            self.standings[CandidateStanding.SINGLE.value]
            + self.standings[CandidateStanding.MULTIPLE.value]
            + self.standings[CandidateStanding.NONE.value]
        ):
            raise ReferentCandidateCensusError(
                "واحدٌ + متعدّدٌ + صفرٌ لا يساوي مقامَ المطابقة الاسمية. "
                + FOUR_STANDINGS_AND_NO_ZERO_GATHERS_THEM_NOTE
            )
        if (
            len(self.zero_candidate_positions)
            != self.standings[CandidateStanding.NONE.value]
        ):
            raise ReferentCandidateCensusError(
                "مواضعُ «صفر مرشَّح» تُسرَد كلُّها أو لا يُخرَج عددُها. "
                + FOUR_STANDINGS_AND_NO_ZERO_GATHERS_THEM_NOTE
            )

    @property
    def nominal_denominator(self) -> int:
        """المقامُ بعد إخراج أطراف الخطاب؛ وهو مقامُ نسبةِ الحصر وحدَه."""

        return (
            self.denominator
            - self.standings[CandidateStanding.DISCOURSE_PARTICIPANT.value]
        )

    @property
    def mean_candidate_set_size(self) -> float:
        """متوسّطُ حجمِ المجموعة على مقامه المُعلَن؛ ولا متوسّطَ بمقامٍ صفر."""

        if self.nominal_denominator == 0:
            raise ReferentCandidateCensusError(
                "لا ضميرَ تُطلَب له أسماءٌ، فلا متوسّطَ يُقسَم. "
                + ELEVEN_PERCENT_IS_THE_REAL_DENOMINATOR_NOTE
            )
        return self.candidate_total / self.nominal_denominator

    @property
    def single_candidate_share(self) -> float:
        """نسبةُ ما حُصِر لمرشَّحٍ واحدٍ من مقام المطابقة الاسمية وحدَه."""

        if self.nominal_denominator == 0:
            raise ReferentCandidateCensusError(
                "نسبةٌ بمقامٍ صفر. " + ELEVEN_PERCENT_IS_THE_REAL_DENOMINATOR_NOTE
            )
        return (
            100.0
            * self.standings[CandidateStanding.SINGLE.value]
            / self.nominal_denominator
        )


def measure_candidates(
    records: Sequence[Mapping[str, str]],
    *,
    corpus_digest: str = MASAQ_SHA256,
) -> CandidateSetCensus:
    """أخرِجْ حجمَ الحصر ونسبتَه ومواضعَ عجزه؛ ولا تُسمِّ مرجعًا ولا تُرجِّح."""

    sets, unparsed, unreadable, undetermined = enumerate_candidate_sets(records)
    standings = {standing.value: 0 for standing in CandidateStanding}
    zero_positions: list[tuple[int, int, int, int]] = []
    candidate_total = 0
    for candidate_set in sets:
        standings[candidate_set.standing.value] += 1
        if candidate_set.standing is CandidateStanding.NONE:
            zero_positions.append(candidate_set.pronoun.position.order_key)
        if candidate_set.standing is not CandidateStanding.DISCOURSE_PARTICIPANT:
            candidate_total += candidate_set.size
    return CandidateSetCensus(
        denominator=len(sets),
        standings=standings,
        candidate_total=candidate_total,
        zero_candidate_positions=tuple(zero_positions),
        unparsed_tags=unparsed,
        unreadable_pronoun_positions=unreadable,
        undetermined_nominals=undetermined,
        preregistration_digest=REFERENT_CANDIDATE_PREREGISTRATION_DIGEST,
        corpus_digest=corpus_digest,
    )


def size_by_constraint(
    sets: Sequence[CandidateSet],
) -> dict[tuple[str, str, str], tuple[int, int]]:
    """توزيعُ الحجم حسب الثلاثية: لكلّ (شخصٍ وعددٍ وجنسٍ) عددُ ضمائرَ وجملةُ حجم.

    وأطرافُ الخطاب تدخل بعددها وبحجمٍ صفرٍ **لأنّها لم تُطلَب لها أسماءٌ**، لا
    لأنّها طُلِبت فلم تُوجَد؛ والفرقُ مكتوبٌ في `CandidateStanding`.
    """

    table: dict[tuple[str, str, str], tuple[int, int]] = {}
    for candidate_set in sets:
        constraint = candidate_set.pronoun.constraint
        key = (
            constraint.person.value,
            constraint.number.value,
            constraint.gender.value,
        )
        count, total = table.get(key, (0, 0))
        table[key] = (count + 1, total + candidate_set.size)
    return table


DECLARED_DENOMINATOR_NOTE: Final[str] = (
    f"المقامُ المُعلَنُ قبل القياس {DECLARED_DENOMINATOR_COUNT} ضميرًا. "
    + ELEVEN_PERCENT_IS_THE_REAL_DENOMINATOR_NOTE
)
"""يُقرأ مع كلّ مخرَجٍ: المقيسُ يُقارَن بالمُعلَن ولا يُعدَّل المُعلَنُ ليُطابِقه."""
