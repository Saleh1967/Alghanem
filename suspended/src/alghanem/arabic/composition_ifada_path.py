"""مسارٌ رأسيٌّ واحدٌ من البايتات إلى مرشَّح الإفادة، موصولٌ لا مجموع.

مخرجُ كلّ طبقةٍ هنا مدخلُ التي تليها فعلًا: لا تقريرَ مستقلٌّ يُضَمّ إلى تقرير،
ولا جوابَ مرجعيٌّ يُمرَّر من خارج الخطّ. والطبقاتُ الخمسُ الأولى ليست مُعادَ
بناؤها: `arabic_round_trip_v1.run_token` هو مَن يُشغّلها، وهذه الوحدةُ تقرأ أثرَه
وتستأنف من حيث وقف.

**نطاقٌ مُعلَنٌ قبل التشغيل** (`SCOPE_IS_DECLARED_BEFORE_ANY_INPUT`): تركيبُ
كلمتين مشكولتَي الآخِر. وما خرج عنه يقف بجنسٍ مُسمًّى لا يُقرَأ نفيًا، على منوال
`IfadaStanding.غير_مقروء` نفسِها.

**الإفادةُ مُشتَقّةٌ من التركيب لا مكتوبةٌ من المتّصل** (`BENEFIT_IS_DERIVED_FROM
_THE_COMPOSITION_NOT_SUPPLIED`): `composition_benefits` في `DalalaRecord` حاملٌ
يُملأ هنا من قراءةِ علامتَي الإعراب المكتوبتين على اللفظين، وشاهدُه يذكر
العلامتين بأعيانهما. فإن لم تُقرأ إحداهما، لم يُبنَ سجلٌّ أصلًا، والحالُ
`غير_مقروء` بسببٍ مُسمًّى — لا `True` تُكتَب لإنهاء التجربة.

**ثلاثُ نتائجَ لكلّ انتقال لا اثنتان**: `ADVANCED` لمن استوفى مدخلَه وشرطَه،
و`DEFERRED` لغموضٍ أو دليلٍ ناقص، و`BLOCKED` لمانعٍ مُحدَّد. والفرقُ بينهما
مقصود: التأجيلُ ليس منعًا، والمنعُ ليس تأجيلًا.

**ما لا تدّعيه هذه الوحدة، مُسمًّى لا مطويًّا:**

* `CASE_MARK != I'RAB`: المقروءُ علامةٌ مكتوبةٌ في آخر اللفظ، لا حكمٌ إعرابيٌّ
  مُسنَدٌ إلى عاملٍ مقروء. فـ«ضمّةٌ مكتوبة» ليست «رفعًا بالابتداء».
* `NO_LEXICON_IS_CONSULTED`: لا معجمَ هنا ولا جذرَ ولا وزن. ولو استُدعي معجمٌ
  لَجاز أن يُبنى على جواب الاختبار، وهو عينُ ما يُمنَع.
* `DEFINITENESS_IS_NOT_READ`: التعريفُ والتنكيرُ خارج المقروء، فلا تُشترَط
  معرفةُ المبتدأ ولا تُقاس.
* `THE_READING_IS_NOT_A_BIRTH`: سجلُّ هذا المسار ليس شهادةَ ولادة، ومرشَّحُ
  الإفادة ليس حكمًا بمطابقة الواقع.
"""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass
from enum import Enum
from typing import Final

from alghanem.canonical_content import canonical_bytes, canonical_digest
from alghanem.kernel.trace import Trace

from .arabic_round_trip_v1 import (
    LayerOutcome,
    RoundTripLayer,
    TokenTrace,
    run_token,
)
from .encoding.carrier_state_candidate import (
    CarrierState,
    CarrierStateCodec,
    CarrierStateUnit,
)
from .mantuq_mafhum_ifada import (
    DalalaChannel,
    DalalaRecord,
    IfadaStanding,
    MafhumKind,
)

__all__ = [
    "BENEFIT_IS_DERIVED_NOT_SUPPLIED_NOTE",
    "THE_ENTRY_IS_BYTES_NOT_A_STRING_NOTE",
    "CASE_MARK_IS_NOT_IRAB_NOTE",
    "COMPOSITION_IFADA_PATH_NAMED_LAWS",
    "DECLARED_SCOPE",
    "NO_LEXICON_IS_CONSULTED_NOTE",
    "CaseMark",
    "CompositionIfadaPathError",
    "CompositionReading",
    "PathRun",
    "PathStage",
    "PathStop",
    "StageOutcome",
    "StageRecord",
    "WordReading",
    "run_text",
]


class CompositionIfadaPathError(ValueError):
    """رفضٌ بنيويٌّ في بناء سجلّ المسار نفسِه، لا في النصّ المقيس."""


DECLARED_SCOPE: Final[str] = (
    "تركيبٌ من كلمتين اثنتين، كلٌّ منهما تعبر الطبقاتِ الخمسَ المكتوبة كما "
    "تدخلها، وتحمل في آخرها علامةً مكتوبةً واحدةً من ضمّةٍ أو كسرةٍ أو فتحةٍ "
    "(منوّنةً أو غيرَ منوّنة). وما خرج عن هذا النطاق يقف بجنسٍ مُسمًّى."
)


class PathStage(Enum):
    """طبقاتُ المسار الثماني بترتيب التنفيذ؛ مفردةٌ مغلقةٌ لا تاسعةَ لها."""

    UTF8_BYTES = "UTF8_BYTES"
    UNICODE_NFC = "UNICODE_NFC"
    WORD_SPLIT = "WORD_SPLIT"
    CARRIER_STATE = "CARRIER_STATE"
    SYLLABLE = "SYLLABLE"
    WORD_STRUCTURE = "WORD_STRUCTURE"
    CASE_MARK = "CASE_MARK"
    COMPOSITION = "COMPOSITION"
    IFADA = "IFADA"

    @property
    def rank(self) -> int:
        """رتبةُ الطبقة في المسار، مُشتقّةً من ترتيب المفردة لا مكتوبة."""

        return tuple(PathStage).index(self) + 1


class StageOutcome(Enum):
    """نتيجةُ انتقالٍ واحد: ثلاثةٌ لا رابعَ لها، ولا «نجحَ تقريبًا»."""

    ADVANCED = "ADVANCED"
    DEFERRED = "DEFERRED"
    BLOCKED = "BLOCKED"


class PathStop(Enum):
    """أجناسُ التوقّف؛ كلٌّ يُرفَع بعينه ولا تُطوى في «لم يُقرأ»."""

    BYTES_ARE_NOT_UTF8 = "BYTES_ARE_NOT_UTF8"
    NOT_TWO_WORDS = "NOT_TWO_WORDS"
    WORD_HALTED_IN_THE_WRITTEN_CHAIN = "WORD_HALTED_IN_THE_WRITTEN_CHAIN"
    FINAL_MARK_NOT_WRITTEN = "FINAL_MARK_NOT_WRITTEN"
    FIRST_MARK_IS_NOT_RAF = "FIRST_MARK_IS_NOT_RAF"
    SECOND_MARK_IS_NASB = "SECOND_MARK_IS_NASB"
    PROCLITIC_JARR_UNDECIDED = "PROCLITIC_JARR_UNDECIDED"
    MUDAF_CARRIES_TANWIN = "MUDAF_CARRIES_TANWIN"


class CaseMark(Enum):
    """العلامةُ المكتوبةُ في آخر اللفظ؛ و`غير_مكتوبة` عضوٌ مصرَّحٌ به لا فراغ."""

    ضمّة = "ضمّة"
    كسرة = "كسرة"
    فتحة = "فتحة"
    غير_مكتوبة = "غير_مكتوبة"

    @property
    def is_written(self) -> bool:
        return self is not CaseMark.غير_مكتوبة


class CompositionReading(Enum):
    """قراءةُ التركيب من علامتَي الطرفين؛ قسمةٌ في النطاق المُعلَن وحده."""

    إسناد = "إسناد"
    إضافة = "إضافة"


_CODEC: Final = CarrierStateCodec()

_MARK_OF_STATE: Final[dict[CarrierState, CaseMark]] = {
    CarrierState.DAMMA: CaseMark.ضمّة,
    CarrierState.KASRA: CaseMark.كسرة,
    CarrierState.FATHA: CaseMark.فتحة,
}

_JARR_PROCLITICS: Final[dict[str, CarrierState]] = {
    "\u0644": CarrierState.KASRA,
    "\u0628": CarrierState.KASRA,
    "\u0643": CarrierState.FATHA,
}
"""حروفُ جرٍّ قد تُلصَق بأوّل الكلمة، كلٌّ بحركته المكتوبة.

والاختبارُ خطّيٌّ لا معجميّ، فهو يَشمل كلمةً أصليّةُ أوّلِها أحدُ هذه الحروف
بحركته (`THE_PROCLITIC_TEST_OVER_TRIGGERS`). ولذلك مخرجُه تأجيلٌ مُسمًّى لا
قراءةُ إضافةٍ ولا نفيُها.
"""

_IFADA_SECTION_FIVE_WITNESS: Final[str] = (
    "الغرضُ من التركيب الإفادة، وهذا لا يفيد؛ ولكنه موجود "
    "(madlul_alone_formal، القسم الخامس)"
)

CASE_MARK_IS_NOT_IRAB_NOTE: Final[str] = (
    "CaseMarkIsNotIrab: المقروءُ حركةٌ مكتوبةٌ على آخر حرفٍ من اللفظ، تُقرأ من "
    "وحدات الحامل/الحالة نفسِها. وليست حكمًا إعرابيًّا مُسنَدًا إلى عامل، فلا "
    "يُقرأ «ضمّةٌ مكتوبة» رفعًا بالابتداء ولا «كسرةٌ مكتوبة» جرًّا بمُضافٍ مقروء."
)

NO_LEXICON_IS_CONSULTED_NOTE: Final[str] = (
    "NoLexiconIsConsulted: لا يُستدعى في هذا المسار معجمٌ ولا جذرٌ ولا وزنٌ ولا "
    "مدوّنةٌ مُعلَّمة. والقراءةُ كلُّها من الحركات المكتوبة في النصّ الداخل، فلا "
    "يمكن أن تُبنى قاعدةٌ معجميةٌ لتطابق جوابَ اختبار."
)

BENEFIT_IS_DERIVED_NOT_SUPPLIED_NOTE: Final[str] = (
    "BenefitIsDerivedFromTheCompositionNotSupplied: `composition_benefits` "
    "يُملأ من قراءة التركيب وحدها، وشاهدُه يذكر العلامتين المقروءتين بأعيانهما. "
    "وما لم تُقرأ قراءةُ تركيبٍ لم يُبنَ سجلٌّ أصلًا، فالحالُ `غير_مقروء` بسببٍ "
    "مُسمًّى لا `True` تُكتَب لإنهاء التجربة."
)

THE_ENTRY_IS_BYTES_NOT_A_STRING_NOTE: Final[str] = (
    "TheEntryIsBytesNotAString: مدخلُ المسار بايتاتٌ، وفكُّ ترميزها انتقالٌ "
    "مقيسٌ له شرطُه ومانعُه وبصمتا طرفيه، لا شرطٌ صامتٌ يقع قبل القياس. "
    "و`run_text` تيسيرٌ يُرمِّز ثمّ يُسلِّم إلى `run_bytes`، فلا تُتخطّى بها "
    "طبقةُ الترميز ولا تُقرأ نصًّا بلا بايتات."
)

COMPOSITION_IFADA_PATH_NAMED_LAWS: Final[dict[str, str]] = {
    "TheEntryIsBytesNotAString": THE_ENTRY_IS_BYTES_NOT_A_STRING_NOTE,
    "CaseMarkIsNotIrab": CASE_MARK_IS_NOT_IRAB_NOTE,
    "NoLexiconIsConsulted": NO_LEXICON_IS_CONSULTED_NOTE,
    "BenefitIsDerivedFromTheCompositionNotSupplied": (
        BENEFIT_IS_DERIVED_NOT_SUPPLIED_NOTE
    ),
    "ARunRecordIsNotABirthCertificate": (
        "ARunRecordIsNotABirthCertificate: سجلُّ هذا المسار وصفُ ما جرى لنصٍّ "
        "بعينه عبر طبقاتٍ مُعلَنة. ولا يُصدِر ولادةً ولا حكمَ ولادة، ولا "
        "يقرؤه شيءٌ في `kernel/`، ومرشَّحُ الإفادة ليس حكمًا بمطابقة الواقع"
    ),
    "ADeferralIsNotABlock": (
        "ADeferralIsNotABlock: `DEFERRED` غموضٌ أو دليلٌ ناقص، و`BLOCKED` مانعٌ "
        "مُحدَّدٌ مقروء. ولا تُطوى إحداهما في الأخرى، ولا تخرج كلتاهما من "
        "المقام الإحصائيّ"
    ),
    "TheProcliticTestOverTriggers": (
        "TheProcliticTestOverTriggers: اختبارُ حرف الجرّ المُلصَق خطّيٌّ لا "
        "معجميّ، فيَشمل كلمةً أصليّةُ أوّلِها لامٌ أو باءٌ مكسورةٌ أو كافٌ "
        "مفتوحة. ولذلك لا يُخرِج قراءةً ولا نفيَها، بل تأجيلًا مُسمًّى يُعَدّ "
        "في مقامه"
    ),
    "AMarkReadingIsNotAProofOfBenefit": (
        "AMarkReadingIsNotAProofOfBenefit: المقروءُ علامتان مكتوبتان على آخِرَي "
        "لفظين، ومنهما تُقرأ صورةُ التركيب. والانتقالُ من صورة التركيب المكتوبة "
        "إلى كون الكلام مُفيدًا في نفس الأمر انتقالٌ لا يقطعه هذا الشاهد: فهو "
        "لا يقرأ قصدًا ولا سياقًا ولا مقامًا ولا صدقًا، ولا يميّز مُفيدًا من "
        "مُحاكٍ لصورته. فالمخرجُ `IfadaStanding` مرشَّحٌ على القناة المكتوبة "
        "وحدها، لا برهانَ إفادة"
    ),
    "NoLaterLayerRepairsAnEarlierLoss": (
        "NoLaterLayerRepairsAnEarlierLoss: كلمةٌ وقفت في الطبقات المكتوبة لا "
        "تُستأنَف من طبقةٍ أعلى بتقديرٍ يسدّ فقدَها، بل يقف المسارُ كلُّه عند "
        "`WORD_HALTED_IN_THE_WRITTEN_CHAIN`"
    ),
}
"""القيودُ المُسمّاةُ التي تُجمّدها هذه الوحدة؛ كلُّ نصٍّ يفتتح باسم قانونه."""

_WHAT_A_MARK_READING_DOES_NOT_PROVE: Final[tuple[str, ...]] = (
    "AMarkReadingIsNotAProofOfBenefit",
    "CaseMarkIsNotIrab",
    "NoLexiconIsConsulted",
    "ARunRecordIsNotABirthCertificate",
)
"""أسماءُ القوانين التي تحدّ قراءةَ العلامتين عن أن تُسمّى برهانَ إفادة."""


def _digest_of(content: object) -> str:
    return canonical_digest(canonical_bytes(content))


def _digest_of_bytes(content: bytes) -> str:
    """بصمةُ بايتاتٍ كما وردت، بلا ترميزٍ وسيطٍ ولا تحويلٍ إلى نصّ."""

    return canonical_digest(content)


@dataclass(frozen=True, slots=True)
class StageRecord:
    """سجلُّ انتقالٍ واحد: هويّةُ طرفيه، وعمليتُه، وشرطُه، ومانعُه، ودليلُه."""

    stage: PathStage
    outcome: StageOutcome
    operation: str
    condition: str
    preventer: PathStop | None
    evidence: str
    input_digest: str
    output_digest: str | None
    trace: Trace
    residuals: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.stage, PathStage):
            raise CompositionIfadaPathError("طبقةُ السجلّ عضوٌ في مفردتها المغلقة.")
        if not isinstance(self.outcome, StageOutcome):
            raise CompositionIfadaPathError("نتيجةُ السجلّ عضوٌ في مفردتها المغلقة.")
        for name in ("operation", "condition", "evidence", "input_digest"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise CompositionIfadaPathError(f"{name} نصٌّ غير فارغ.")
        if (self.outcome is StageOutcome.ADVANCED) != (self.preventer is None):
            raise CompositionIfadaPathError(
                "المتقدِّمُ لا مانعَ له، وغيرُ المتقدِّم يحمل مانعَه المُسمّى."
            )
        if (self.outcome is StageOutcome.ADVANCED) != (self.output_digest is not None):
            raise CompositionIfadaPathError(
                "هويّةُ المخرج تُكتَب لمن تقدَّم وحدَه؛ فالواقفُ لا مخرجَ له يُبصَم."
            )
        if type(self.trace) is not Trace:
            raise CompositionIfadaPathError("أثرُ السجلّ أثرٌ مُصاغ.")
        if type(self.residuals) is not tuple or any(
            not isinstance(item, str) or not item.strip() for item in self.residuals
        ):
            raise CompositionIfadaPathError("البقايا نصوصٌ غيرُ فارغة.")

    @property
    def rank(self) -> int:
        """رتبةُ الانتقال، مُشتقّةً من رتبة طبقته."""

        return self.stage.rank


@dataclass(frozen=True, slots=True)
class WordReading:
    """قراءةُ كلمةٍ واحدة: أثرُها في الطبقات المكتوبة، وعلامتُها المقروءة."""

    index: int
    surface: str
    token_trace: TokenTrace
    final_mark: CaseMark
    final_is_tanwin: bool
    has_jarr_proclitic: bool

    def __post_init__(self) -> None:
        if type(self.token_trace) is not TokenTrace:
            raise CompositionIfadaPathError("أثرُ الكلمة أثرُ الخطّ المكتوب نفسِه.")
        if not isinstance(self.final_mark, CaseMark):
            raise CompositionIfadaPathError("علامةُ الآخِر عضوٌ في مفردتها المغلقة.")
        if not self.final_mark.is_written and self.final_is_tanwin:
            raise CompositionIfadaPathError("تنوينٌ على علامةٍ لم تُكتَب دعوَيان.")

    @property
    def crossed_the_written_chain(self) -> bool:
        """أعبرَت الكلمةُ الطبقاتِ المكتوبةَ كلَّها ورجعت كما دخلت؟"""

        return (
            self.token_trace.outcome is LayerOutcome.RECONSTRUCTED
            and self.token_trace.reached is RoundTripLayer.FINAL_BYTES
        )


@dataclass(frozen=True, slots=True)
class PathRun:
    """سَوقُ نصٍّ واحدٍ في المسار كلِّه: سجلّاتُه، وقراءاتُه، وأين وقف."""

    source: bytes
    text: str
    stages: tuple[StageRecord, ...]
    words: tuple[WordReading, ...]
    composition: CompositionReading | None
    record: DalalaRecord | None

    def __post_init__(self) -> None:
        if type(self.source) is not bytes or not self.source:
            raise CompositionIfadaPathError("مدخلُ السَّوق بايتاتٌ غيرُ فارغة.")
        if not isinstance(self.text, str):
            raise CompositionIfadaPathError("نصُّ السَّوق نصٌّ مقروء.")
        if self.text and self.text.encode("utf-8") != self.source:
            raise CompositionIfadaPathError(
                "نصُّ السَّوق هو فكُّ ترميز بايتاته نفسِها، لا نصٌّ آخر."
            )
        if type(self.stages) is not tuple or not self.stages:
            raise CompositionIfadaPathError("سَوقٌ بلا سجلٍّ واحدٍ لا يُقرأ.")
        ranks = tuple(record.rank for record in self.stages)
        if ranks != tuple(range(1, len(ranks) + 1)):
            raise CompositionIfadaPathError(
                "رتبُ الانتقالات متعاقبةٌ من الأولى؛ وطبقةٌ مقفوزةٌ ليست مسارًا."
            )
        for record in self.stages[:-1]:
            if record.outcome is not StageOutcome.ADVANCED:
                raise CompositionIfadaPathError(
                    "لا انتقالَ بعد وقوف: آخرُ سجلٍّ وحدَه يجوز أن يكون واقفًا."
                )
        if (self.record is not None) != (self.composition is not None):
            raise CompositionIfadaPathError(
                "سجلُّ الدلالة يُبنى على قراءة تركيبٍ مقروءة، ولا يُبنى بدونها."
            )

    @property
    def reached(self) -> PathStage:
        """الطبقةُ التي بلغها السَّوق، مُشتقّةً من آخر سجلّ."""

        return self.stages[-1].stage

    @property
    def outcome(self) -> StageOutcome:
        """حكمُ السَّوق، مُشتقًّا من آخر سجلّ."""

        return self.stages[-1].outcome

    @property
    def stop(self) -> PathStop | None:
        """جنسُ التوقّف، و`None` لمن بلغ الإفادة."""

        return self.stages[-1].preventer

    @property
    def ifada(self) -> IfadaStanding:
        """حالُ الإفادة مُشتقّةً من السجلّ، و`غير_مقروء` حيث لا سجلّ."""

        if self.record is None:
            return IfadaStanding.غير_مقروء
        return self.record.ifada

    @property
    def reached_ifada(self) -> bool:
        """أبلغ السَّوقُ إفادةً مقروءة؟ فبلوغُ الطبقة ليس قراءةَ الفائدة."""

        return self.ifada.is_read

    @property
    def what_the_benefit_reading_does_not_prove(self) -> tuple[str, ...]:
        """ما لا تقطعه قراءةُ العلامتين؛ مُشتقٌّ من القوانين المُسمّاة لا مُنشَأ.

        فمن سمّى هذا المخرجَ برهانَ إفادةٍ فقد عبَر انتقالًا لم يُقَس هنا.
        """

        return tuple(
            COMPOSITION_IFADA_PATH_NAMED_LAWS[name]
            for name in _WHAT_A_MARK_READING_DOES_NOT_PROVE
        )

    @property
    def the_benefit_is_a_candidate_not_a_proof(self) -> bool:
        """أمرشَّحٌ هذا المخرجُ لا برهان؟ وهو ثابتٌ لكلِّ سَوقٍ بلا استثناء."""

        return True

    @property
    def trace(self) -> Trace:
        """أثرُ السَّوق كلِّه، مجموعًا من آثار انتقالاته بترتيبها."""

        events: list[str] = [f"source_bytes:{_digest_of_bytes(self.source)}"]
        for record in self.stages:
            events.extend(record.trace.events)
        return Trace(tuple(events))

    @property
    def residuals(self) -> tuple[str, ...]:
        """بقايا السَّوق كلِّه، بلا تكرارٍ وبترتيب أوّل ورودها."""

        seen: list[str] = []
        for record in self.stages:
            for residual in record.residuals:
                if residual not in seen:
                    seen.append(residual)
        return tuple(seen)


def _stage(
    stage: PathStage,
    outcome: StageOutcome,
    *,
    operation: str,
    condition: str,
    evidence: str,
    input_digest: str,
    output_digest: str | None = None,
    preventer: PathStop | None = None,
    residuals: tuple[str, ...] = (),
) -> StageRecord:
    return StageRecord(
        stage=stage,
        outcome=outcome,
        operation=operation,
        condition=condition,
        preventer=preventer,
        evidence=evidence,
        input_digest=input_digest,
        output_digest=output_digest,
        trace=Trace(
            (
                f"stage:{stage.value}",
                f"outcome:{outcome.value}",
                f"path_operation:{operation}",
                f"in:{input_digest}",
                f"out:{output_digest}" if output_digest else "out:none",
                f"preventer:{preventer.value}" if preventer else "preventer:none",
            )
        ),
        residuals=residuals,
    )


def _final_unit(units: tuple[CarrierStateUnit, ...]) -> CarrierStateUnit | None:
    for unit in reversed(units):
        if unit.state is not CarrierState.PASSTHROUGH:
            return unit
    return None


def _opens_with_a_jarr_proclitic(surface: str) -> bool:
    """أيفتتح اللفظُ بحرفٍ قد يكون جارًّا مُلصَقًا، بحركته المكتوبة؟"""

    units = _CODEC.generate(surface)
    if not units:
        return False
    first = units[0]
    return _JARR_PROCLITICS.get(first.carrier) is first.state


def _read_word(index: int, surface: str) -> WordReading:
    """اقرأ كلمةً واحدة: سُقها في الخطّ المكتوب، ثم اقرأ علامةَ آخِرها."""

    trace = run_token(surface.encode("utf-8"), token_index=index)
    mark = CaseMark.غير_مكتوبة
    tanwin = False
    if (
        trace.outcome is LayerOutcome.RECONSTRUCTED
        and trace.reached is RoundTripLayer.FINAL_BYTES
    ):
        unit = _final_unit(_CODEC.generate(surface))
        if unit is not None:
            mark = _MARK_OF_STATE.get(unit.state, CaseMark.غير_مكتوبة)
            tanwin = unit.tanwin and mark.is_written
    return WordReading(
        index=index,
        surface=surface,
        token_trace=trace,
        final_mark=mark,
        final_is_tanwin=tanwin,
        has_jarr_proclitic=_opens_with_a_jarr_proclitic(surface),
    )


def _read_composition(
    first: WordReading, second: WordReading
) -> tuple[CompositionReading | None, PathStop | None, str]:
    """اقرأ التركيبَ من علامتَي الطرفين وحدَهما، أو قف بجنسٍ مُسمًّى."""

    marks = (
        f"{first.surface}:{first.final_mark.value}"
        f"/{second.surface}:{second.final_mark.value}"
    )
    if not first.final_mark.is_written or not second.final_mark.is_written:
        return None, PathStop.FINAL_MARK_NOT_WRITTEN, marks
    if second.has_jarr_proclitic:
        return None, PathStop.PROCLITIC_JARR_UNDECIDED, marks
    if second.final_mark is CaseMark.فتحة:
        return None, PathStop.SECOND_MARK_IS_NASB, marks
    if first.final_mark is not CaseMark.ضمّة:
        return None, PathStop.FIRST_MARK_IS_NOT_RAF, marks
    if second.final_mark is CaseMark.ضمّة:
        return CompositionReading.إسناد, None, marks
    if first.final_is_tanwin:
        return None, PathStop.MUDAF_CARRIES_TANWIN, marks
    return CompositionReading.إضافة, None, marks


def _benefit_of(reading: CompositionReading, witness_marks: str) -> tuple[bool, str]:
    """حاملُ الإفادة وشاهدُه، مُشتقَّين من قراءة التركيب وحدها."""

    if reading is CompositionReading.إسناد:
        return True, f"رفعُ الطرفين المقروء في العلامتين: {witness_marks}"
    return False, f"{_IFADA_SECTION_FIVE_WITNESS}؛ والعلامتان: {witness_marks}"


def run_text(text: str) -> PathRun:
    """سُق نصًّا مقروءًا بترميزه: يُرمَّز بـUTF-8 ثمّ يُساق من بايتاته.

    والمدخلُ الأصليُّ للمسار بايتاتٌ لا نصّ (`TheEntryIsBytesNotAString`)؛
    وهذه الدالّةُ تيسيرٌ لمن بيده نصٌّ مفكوكُ الترميز، فتُرمِّزه ثمّ تُسلِّمه
    إلى `run_bytes`، ولا تتخطّى بها طبقةُ الترميز.
    """

    if not isinstance(text, str) or not text.strip():
        raise CompositionIfadaPathError("مدخلُ المسار نصٌّ غير فارغ.")
    return run_bytes(text.encode("utf-8"))


def run_bytes(source: bytes) -> PathRun:
    """سُق بايتاتٍ في المسار كلِّه، من فكِّ الترميز إلى مرشّح الإفادة.

    وفكُّ الترميز انتقالٌ مقيسٌ له حكمُه ومانعُه، لا شرطًا صامتًا قبل المسار؛
    فبايتاتٌ ليست UTF-8 تقف عند `BYTES_ARE_NOT_UTF8` ولا تُصلَح ولا تُتخطّى.
    """

    if type(source) is not bytes or not source.strip():
        raise CompositionIfadaPathError("مدخلُ المسار بايتاتٌ غيرُ فارغة.")

    source_digest = _digest_of_bytes(source)
    stages: list[StageRecord] = []
    decode_condition = "بايتاتُ المدخل UTF-8 صحيحةٌ تُفَكّ بلا إبدالٍ ولا إسقاط"
    try:
        text = source.decode("utf-8")
    except UnicodeDecodeError as error:
        stages.append(
            _stage(
                PathStage.UTF8_BYTES,
                StageOutcome.BLOCKED,
                operation="decode the declared bytes as strict UTF-8",
                condition=decode_condition,
                evidence=f"utf8_decode_error:{error.reason}@{error.start}",
                input_digest=source_digest,
                output_digest=None,
                preventer=PathStop.BYTES_ARE_NOT_UTF8,
            )
        )
        return PathRun(
            source=source,
            text="",
            stages=tuple(stages),
            words=(),
            composition=None,
            record=None,
        )

    stages.append(
        _stage(
            PathStage.UTF8_BYTES,
            StageOutcome.ADVANCED,
            operation="decode the declared bytes as strict UTF-8",
            condition=decode_condition,
            evidence=f"decoded_characters:{len(text)}",
            input_digest=source_digest,
            output_digest=_digest_of(text),
        )
    )

    normalized = unicodedata.normalize("NFC", text)
    stages.append(
        _stage(
            PathStage.UNICODE_NFC,
            StageOutcome.ADVANCED,
            operation="normalize the decoded text to NFC before any reading",
            condition="التسويةُ تسبق كلَّ قراءةٍ، ولا تُقرأ صورتان لنصٍّ واحد",
            evidence=f"nfc_identical:{normalized == text}",
            input_digest=_digest_of(text),
            output_digest=_digest_of(normalized),
        )
    )

    words: tuple[str, ...] = tuple(normalized.split())
    stages.append(
        _stage(
            PathStage.WORD_SPLIT,
            StageOutcome.ADVANCED if len(words) == 2 else StageOutcome.DEFERRED,
            operation="split the normalized text into whitespace-separated words",
            condition=DECLARED_SCOPE,
            evidence=f"words:{len(words)}",
            input_digest=_digest_of(normalized),
            output_digest=_digest_of(words) if len(words) == 2 else None,
            preventer=None if len(words) == 2 else PathStop.NOT_TWO_WORDS,
        )
    )
    if len(words) != 2:
        return PathRun(
            source=source,
            text=text,
            stages=tuple(stages),
            words=(),
            composition=None,
            record=None,
        )

    readings = tuple(_read_word(index, surface) for index, surface in enumerate(words))
    halted = tuple(
        reading for reading in readings if not reading.crossed_the_written_chain
    )
    written_evidence = "; ".join(
        f"{reading.surface}:{reading.token_trace.reached.value}"
        f"/{reading.token_trace.outcome.value}"
        for reading in readings
    )
    for stage in (
        PathStage.CARRIER_STATE,
        PathStage.SYLLABLE,
        PathStage.WORD_STRUCTURE,
    ):
        if halted:
            stages.append(
                _stage(
                    stage,
                    StageOutcome.BLOCKED,
                    operation="arabic_round_trip_v1.run_token over each word",
                    condition="كلُّ كلمةٍ تعبر الطبقاتِ المكتوبة وترجع كما دخلت",
                    evidence=written_evidence,
                    input_digest=_digest_of(words),
                    preventer=PathStop.WORD_HALTED_IN_THE_WRITTEN_CHAIN,
                    residuals=(
                        COMPOSITION_IFADA_PATH_NAMED_LAWS[
                            "NoLaterLayerRepairsAnEarlierLoss"
                        ],
                    ),
                )
            )
            return PathRun(
                source=source,
                text=text,
                stages=tuple(stages),
                words=readings,
                composition=None,
                record=None,
            )
        stages.append(
            _stage(
                stage,
                StageOutcome.ADVANCED,
                operation="arabic_round_trip_v1.run_token over each word",
                condition="كلُّ كلمةٍ تعبر الطبقاتِ المكتوبة وترجع كما دخلت",
                evidence=written_evidence,
                input_digest=_digest_of(words),
                output_digest=_digest_of(
                    tuple(reading.token_trace.reached.value for reading in readings)
                ),
            )
        )

    marks = tuple(
        (reading.surface, reading.final_mark.value, reading.final_is_tanwin)
        for reading in readings
    )
    unwritten = tuple(
        reading for reading in readings if not reading.final_mark.is_written
    )
    stages.append(
        _stage(
            PathStage.CASE_MARK,
            StageOutcome.ADVANCED if not unwritten else StageOutcome.DEFERRED,
            operation="read the last non-passthrough carrier state of each word",
            condition="لكلّ كلمةٍ علامةٌ مكتوبةٌ في آخرها من الثلاث",
            evidence=f"marks:{marks}",
            input_digest=_digest_of(words),
            output_digest=_digest_of(marks) if not unwritten else None,
            preventer=None if not unwritten else PathStop.FINAL_MARK_NOT_WRITTEN,
            residuals=(CASE_MARK_IS_NOT_IRAB_NOTE,),
        )
    )
    if unwritten:
        return PathRun(
            source=source,
            text=text,
            stages=tuple(stages),
            words=readings,
            composition=None,
            record=None,
        )

    reading, stop, witness_marks = _read_composition(readings[0], readings[1])
    stages.append(
        _stage(
            PathStage.COMPOSITION,
            StageOutcome.ADVANCED
            if reading is not None
            else (
                StageOutcome.BLOCKED
                if stop is PathStop.MUDAF_CARRIES_TANWIN
                else StageOutcome.DEFERRED
            ),
            operation="read the composition from the two written final marks",
            condition="قراءةُ التركيب من العلامتين وحدَهما، بلا معجمٍ ولا جذر",
            evidence=witness_marks,
            input_digest=_digest_of(marks),
            output_digest=_digest_of(reading.value) if reading is not None else None,
            preventer=stop,
            residuals=(
                NO_LEXICON_IS_CONSULTED_NOTE,
                COMPOSITION_IFADA_PATH_NAMED_LAWS["TheProcliticTestOverTriggers"],
            ),
        )
    )
    if reading is None:
        return PathRun(
            source=source,
            text=text,
            stages=tuple(stages),
            words=readings,
            composition=None,
            record=None,
        )

    benefits, benefit_witness = _benefit_of(reading, witness_marks)
    record = DalalaRecord(
        lafz=text,
        madlul=f"تركيبٌ مقروءٌ: {reading.value}",
        carried_by_the_wording=True,
        agrees_with_the_uttered_ruling=None,
        composition_benefits=benefits,
        benefit_witness=benefit_witness,
        declared_channel=DalalaChannel.منطوق,
        declared_mafhum_kind=MafhumKind.لا_ينطبق,
        declared_ifada=(IfadaStanding.مُفيد if benefits else IfadaStanding.غير_مُفيد),
    )
    stages.append(
        _stage(
            PathStage.IFADA,
            StageOutcome.ADVANCED,
            operation="derive composition_benefits from the composition reading",
            condition="حاملُ الإفادة يأتي من قراءة التركيب، وشاهدُه يذكر العلامتين",
            evidence=benefit_witness,
            input_digest=_digest_of(reading.value),
            output_digest=_digest_of(record.ifada.value),
            residuals=(BENEFIT_IS_DERIVED_NOT_SUPPLIED_NOTE,),
        )
    )
    return PathRun(
        source=source,
        text=text,
        stages=tuple(stages),
        words=readings,
        composition=reading,
        record=record,
    )


if len(PathStage) != 9:
    raise RuntimeError("طبقاتُ المسار تسعٌ مُعلَنة.")
if tuple(PathStage)[0] is not PathStage.UTF8_BYTES:
    raise RuntimeError("أوّلُ الطبقات بايتاتُ المدخل، فالمسارُ يبدأ منها.")
if len(StageOutcome) != 3:
    raise RuntimeError("نتائجُ الانتقال ثلاثٌ لا رابعَ لها.")
for _law_name, _law_text in COMPOSITION_IFADA_PATH_NAMED_LAWS.items():
    if not _law_text.startswith(f"{_law_name}:"):
        raise RuntimeError("كلُّ نصِّ قانونٍ يفتتح باسم قانونه.")
