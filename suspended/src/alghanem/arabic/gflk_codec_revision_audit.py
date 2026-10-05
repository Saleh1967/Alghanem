"""تدقيقُ مراجعةٍ خارجيةٍ لمِرمازِ الحامل/الحالة، وحكمُها محسوبٌ لا مكتوب.

وصلت من محادثةٍ خارجية دالّتا توليدٍ واسترجاعٍ للحامل/الحالة، معهما ادّعاءُ
`Close(Open(x)) ≅ x` بنسبة **100.0000%** على «٧٨٬٢٤٥ كلمة» قرآنية وعلى «مصدرٍ
عربيٍّ حديثٍ مستقلّ». وحُمِلت كما يُحمَل كلُّ نصٍّ من محادثةٍ أخرى:
`PROSE_FROM_ANOTHER_CONVERSATION` — لا يُصدَّق رقمٌ حتى يُعاد اشتقاقُه هنا، على
منوال مرشّح الاقتصاد الصوتيّ.

وأُعيد اشتقاقُه فعلًا على المدوَّنة المُبصَّمة نفسِها
(`QURANIC_ARABIC_CORPUS_WITNESS`)، فكان:

* **٩٩٫٩٩٢٢٥١٪ لا ١٠٠٪**: ستُّ كلماتٍ حقيقيةٍ تُفسَد صامتًا، لا حالةٌ نظرية.
  و`فَٱدَّٰرَْٰٔتُمْ` تخرج `فَٱدَّٰرْٰٔتُمْ`: فتحةٌ تسقط بلا تحذير.
* **والعطبُ مُغلَقٌ في هذه الشجرة سلفًا**: حلقةُ `while` في المراجعة تكتب فوق
  حالةٍ مكتوبةٍ سلفًا، وهو بعينه العطبُ الأوّل المُسمَّى في
  `carrier_state_candidate` ومردودٌ هناك عند الإنشاء. فالمراجعةُ تُعيد عطبًا
  حُلَّ قبلها.
* **و`madd_self` ما زال يُسقِط كلَّ حقلٍ سواه**: `آً` تعود `آ`، و`آّ` تعود
  `ءّ`. ولم تقع هذه الصورُ في المدوَّنة القرآنية، فبدا الرقمُ مئةً وهو ليس
  كذلك — وهذا وحدَه يكفي لإبطال «١٠٠٪» بوصفه شهادةَ سلامة.

والإنصافُ جزءٌ من التدقيق لا زينةٌ فيه: **عطبُ إسقاطِ الرموز غير الحرفية
مُصلَحٌ فعلًا في هذه المراجعة** — `العربية!` و`hello` تعودان كما دخلتا. فليست
المراجعةُ كلُّها خطأً، والتدقيقُ الذي لا يُسمّي ما نجح تدقيقٌ ناقص.

`الحكمُ محسوبٌ لا مكتوب`: لا حقلَ في `CodecRevisionAudit` اسمُه حكم. بل
`outcome` خاصّيةٌ تُشتقُّ من مقارنةِ المُدّعى بالمقيس — `ADOPTION_REFUSED` ما
دامت بقيّةٌ حاجزةٌ قائمة، و`CLAIM_REPRODUCED_PENDING_AUTHORITY` لو زال الحاجزُ
كلُّه. فمن بدّل رقمًا ليُجمّل النتيجة بدّل المُدخَل لا الحكم، وظهر التبديل.

`ولا سلطةَ لهذه الوحدة`: لا ولادةَ، ولا حكمَ ولادة، ولا تجميدَ `E0`، ولا
ترقيةَ رتبة؛ ولا تستورد من `kernel/` شيئًا، ولا تقرؤها وحدةٌ فيه. ويبقى
`ROUND_TRIP_IS_INVERTIBILITY_NOT_ATOMICITY` قائمًا على حاله: لو صحّت المئةُ
تامّةً لما دلّت على أنّ الزوجَ (حامل، حالة) ذرّةٌ ولا وحدةٌ وحيدة.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from typing import Final

from .encoding.carrier_state_candidate import (
    QURANIC_CORPUS_INVERTIBILITY,
    InvertibilityMeasurement,
)
from .irab_corpus_witness import QURANIC_ARABIC_CORPUS_WITNESS, IrabCorpusWitness

__all__ = [
    "A_CORPUS_RATE_DOES_NOT_COVER_THE_UNATTESTED",
    "CLAIMED_ROUND_TRIP_FRACTION",
    "CLAIMED_TOKEN_TOTAL",
    "DEPOSITED_REVISION_ORIGIN",
    "DOCSTRING_CONTRADICTS_ITS_OWN_CODE",
    "GFLK_CODEC_REVISION_AUDIT",
    "GFLK_REVISION_AUDIT_RESIDUALS",
    "MADD_SELF_STILL_DROPS_EVERY_OTHER_FIELD",
    "PASSTHROUGH_DEFECT_IS_GENUINELY_CLOSED_IN_THE_DEPOSIT",
    "REVISION_AUDIT_AUTHORITY_NOTE",
    "ROUND_TRIP_IS_NOT_100_PERCENT_ON_THIS_CORPUS",
    "SECOND_SOURCE_IS_NOT_AN_INDEPENDENT_LINE",
    "SILENT_OVERWRITE_DEFECT_REINSTATED",
    "SILENT_OVERWRITE_LOCATIONS",
    "THE_CLAIMED_CORPUS_IS_UNIDENTIFIED",
    "AdoptionOutcome",
    "CodecRevisionAudit",
    "CorruptedToken",
    "GflkCodecRevisionAuditError",
]


class GflkCodecRevisionAuditError(ValueError):
    """رُفض مدخلٌ لا يُعاد به اشتقاقُ التدقيق؛ ولا يُحمَل على أقرب حالة."""


class AdoptionOutcome(Enum):
    """حكمُ التدقيق؛ ثنائيٌّ مغلق، وكلا فرعَيه قابلٌ للبلوغ بالحساب.

    ولا عضوَ فيه اسمُه «وُلِد» ولا «مُصدَّق»: حتى على الفرع الموافق يبقى
    الحكمُ موقوفًا على سلطةٍ لم تُبنَ في هذا المستودع.
    """

    ADOPTION_REFUSED = "ADOPTION_REFUSED"
    CLAIM_REPRODUCED_PENDING_AUTHORITY = "CLAIM_REPRODUCED_PENDING_AUTHORITY"


# --- البقايا المُسمّاة -------------------------------------------------------

ROUND_TRIP_IS_NOT_100_PERCENT_ON_THIS_CORPUS: Final[str] = (
    "أُعيد اشتقاقُ الادّعاء على المدوَّنة المُبصَّمة فخرج ٩٩٫٩٩٢٢٥١٪ لا ١٠٠٪: "
    "ستُّ كلماتٍ تعود مغايرةً لما دخلت، بلا استثناءٍ ولا تحذير"
)

SILENT_OVERWRITE_DEFECT_REINSTATED: Final[str] = (
    "الكلماتُ الستُّ كلُّها من جنسٍ واحد: كتابةٌ فوق حالةٍ مكتوبةٍ سلفًا في "
    "حلقةِ قراءةِ العلامات، وهو العطبُ الأوّلُ المُسمَّى في "
    "carrier_state_candidate والمردودُ فيه عند الإنشاء؛ فالمراجعةُ تُعيده لا "
    "تُصلحه، والفرقُ بين صفرٍ وستٍّ فرقُ ردٍّ صريحٍ من فقدٍ صامت"
)

MADD_SELF_STILL_DROPS_EVERY_OTHER_FIELD: Final[str] = (
    "حالةُ madd_self تعود من الاسترجاع قبل قراءةِ التنوين والتضعيف والمقعد، "
    "فتصير آً هي آ وتصير آّ هي ءّ؛ وهو العطبُ الثاني المُسمَّى سلفًا، مُعادًا"
)

A_CORPUS_RATE_DOES_NOT_COVER_THE_UNATTESTED: Final[str] = (
    "صورُ الألف الممدودة الموسومةِ بتنوينٍ أو تضعيفٍ لا ترد في المدوَّنة "
    "القرآنية، فعطبُها لا يظهر في نسبةٍ محسوبةٍ عليها؛ ونسبةٌ عاليةٌ على نصٍّ "
    "مغلقٍ لا تشهد لما لم يرد فيه"
)

THE_CLAIMED_CORPUS_IS_UNIDENTIFIED: Final[str] = (
    "لم تصحب الادّعاءَ بصمةٌ ولا طولُ بايتاتٍ ولا قاعدةُ تقطيعٍ ولا صورةُ "
    "تنميط، فالفجوةُ بين ٧٨٬٢٤٥ المُدّعاة و٧٧٬٤٢٩ المقيسة لا تُنسَب إلى سبب؛ "
    "ونسبةٌ على مجتمعٍ غيرِ مُعرَّفٍ لا يُعيد اشتقاقَها أحد"
)

SECOND_SOURCE_IS_NOT_AN_INDEPENDENT_LINE: Final[str] = (
    "المصدرُ الحديثُ الثاني غيرُ مُسمًّى ولا مُبصَّم، وأُجري بالأداةِ نفسِها "
    "ومعيارِ النجاحِ نفسِه؛ فهو تشغيلٌ ثانٍ لأداةٍ واحدة لا خطُّ دليلٍ ثانٍ، "
    "وهو بعينه شرطُ IndependentClosureCheck الذي لا ينفكّ باختلافِ الكوربصِ "
    "وحدَه"
)

DOCSTRING_CONTRADICTS_ITS_OWN_CODE: Final[str] = (
    "تُعلن ترويسةُ المراجعة ذرّةً بأربعةِ حقول، والكودُ يُصدِر ستّة؛ ومفرداتُ "
    "الحالة والتضعيف تعليقٌ لا يُلزِم شيئًا، فوصفُ المراجعة لنفسها ليس "
    "مواصفةً لها"
)

PASSTHROUGH_DEFECT_IS_GENUINELY_CLOSED_IN_THE_DEPOSIT: Final[str] = (
    "وهذا حقٌّ للمراجعة لا يُطوى: عطبُ إسقاطِ الرموز غير الحرفية مُصلَحٌ فيها "
    "فعلًا، فتعود العربية! وhello كما دخلتا؛ وتدقيقٌ لا يُسمّي ما نجح ناقص"
)

REVISION_AUDIT_AUTHORITY_NOTE: Final[str] = (
    "REVISION_AUDIT_IS_A_RECORD_NOT_A_GATE: تسجيلٌ لا سلطة؛ لا ولادةَ ولا "
    "حكمَ ولادةٍ ولا تجميدَ E0 ولا ترقيةَ رتبة، ولا تقرؤه بوّابةٌ في kernel/"
)

GFLK_REVISION_AUDIT_RESIDUALS: Final[dict[str, str]] = {
    "ROUND_TRIP_IS_NOT_100_PERCENT_ON_THIS_CORPUS": (
        ROUND_TRIP_IS_NOT_100_PERCENT_ON_THIS_CORPUS
    ),
    "SILENT_OVERWRITE_DEFECT_REINSTATED": SILENT_OVERWRITE_DEFECT_REINSTATED,
    "MADD_SELF_STILL_DROPS_EVERY_OTHER_FIELD": (
        MADD_SELF_STILL_DROPS_EVERY_OTHER_FIELD
    ),
    "A_CORPUS_RATE_DOES_NOT_COVER_THE_UNATTESTED": (
        A_CORPUS_RATE_DOES_NOT_COVER_THE_UNATTESTED
    ),
    "THE_CLAIMED_CORPUS_IS_UNIDENTIFIED": THE_CLAIMED_CORPUS_IS_UNIDENTIFIED,
    "SECOND_SOURCE_IS_NOT_AN_INDEPENDENT_LINE": (
        SECOND_SOURCE_IS_NOT_AN_INDEPENDENT_LINE
    ),
    "DOCSTRING_CONTRADICTS_ITS_OWN_CODE": DOCSTRING_CONTRADICTS_ITS_OWN_CODE,
    "PASSTHROUGH_DEFECT_IS_GENUINELY_CLOSED_IN_THE_DEPOSIT": (
        PASSTHROUGH_DEFECT_IS_GENUINELY_CLOSED_IN_THE_DEPOSIT
    ),
}

_BLOCKING_RESIDUAL_CODES: Final[frozenset[str]] = frozenset(
    {
        "ROUND_TRIP_IS_NOT_100_PERCENT_ON_THIS_CORPUS",
        "SILENT_OVERWRITE_DEFECT_REINSTATED",
        "MADD_SELF_STILL_DROPS_EVERY_OTHER_FIELD",
        "THE_CLAIMED_CORPUS_IS_UNIDENTIFIED",
        "SECOND_SOURCE_IS_NOT_AN_INDEPENDENT_LINE",
    }
)

DEPOSITED_REVISION_ORIGIN: Final[str] = (
    "محادثةُ GFLK خارجَ هذه الشجرة: دالّتا generate_carrier_state و"
    "retrieve_state_carrier، وُصِفتا الصيغةَ النهائيةَ ولم يصحبهما سجلٌّ "
    "مُجمَّدٌ ولا بصمةُ مصدرٍ ولا قاعدةُ تقطيع"
)

CLAIMED_ROUND_TRIP_FRACTION: Final[float] = 1.0
CLAIMED_TOKEN_TOTAL: Final[int] = 78_245


@dataclass(frozen=True, slots=True)
class CorruptedToken:
    """كلمةٌ واحدةٌ عادت مغايرة، بموضعها من المدوَّنة وصورتَيها.

    والموضعُ شرطٌ لا زينة: بلا (سورة:آية:كلمة) لا يُعيد حائزُ البايتات نفسِها
    فتحَ الكلمةِ بعينها والنظرَ فيها.
    """

    sura: int
    aya: int
    word: int
    surface_in: str
    surface_out: str

    def __post_init__(self) -> None:
        for number, label in (
            (self.sura, "رقمُ السورة"),
            (self.aya, "رقمُ الآية"),
            (self.word, "رقمُ الكلمة"),
        ):
            if isinstance(number, bool) or not isinstance(number, int) or number < 1:
                raise GflkCodecRevisionAuditError(f"{label} عددٌ صحيحٌ موجب.")
        for surface, label in (
            (self.surface_in, "الصورةُ الداخلة"),
            (self.surface_out, "الصورةُ الخارجة"),
        ):
            if not isinstance(surface, str) or not surface.strip():
                raise GflkCodecRevisionAuditError(f"{label} نصٌّ غير فارغ.")
        if self.surface_in == self.surface_out:
            raise GflkCodecRevisionAuditError(
                "كلمةٌ عادت كما دخلت ليست كلمةً مُفسَدة؛ ولا تُدرَج في جدول "
                "الإفساد الصامت."
            )

    @property
    def location(self) -> tuple[int, int, int]:
        """موضعُ الكلمة من المدوَّنة: (سورة، آية، كلمة)."""

        return (self.sura, self.aya, self.word)


SILENT_OVERWRITE_LOCATIONS: Final[tuple[CorruptedToken, ...]] = (
    CorruptedToken(
        sura=2,
        aya=72,
        word=4,
        surface_in="\u0641\u064e\u0671\u062f\u064e\u0651\u0670\u0631\u064e"
        "\u0652\u0670\u0654\u062a\u064f\u0645\u0652",
        surface_out="\u0641\u064e\u0671\u062f\u0651\u064e\u0670\u0631\u0652"
        "\u0670\u0654\u062a\u064f\u0645\u0652",
    ),
    CorruptedToken(
        sura=7,
        aya=196,
        word=2,
        surface_in="\u0648\u064e\u0644\u0650\u0650\u0651\u06d7\u0649\u064e",
        surface_out="\u0648\u064e\u0644\u0651\u0650\u06d7\u0649\u064e",
    ),
    CorruptedToken(
        sura=25,
        aya=49,
        word=1,
        surface_in="\u0644\u0650\u0651\u0646\u064f\u062d\u0650\u0652\u06d7"
        "\u0649\u064e",
        surface_out="\u0644\u0651\u0650\u0646\u064f\u062d\u0652\u06d7\u0649" "\u064e",
    ),
    CorruptedToken(
        sura=27,
        aya=36,
        word=8,
        surface_in="\u0621\u064e\u0627\u062a\u064e\u0649\u0670\u0646\u064e"
        "\u0650\u06d7",
        surface_out="\u0621\u064e\u0627\u062a\u064e\u0649\u0670\u0646\u0650" "\u06d7",
    ),
    CorruptedToken(
        sura=46,
        aya=33,
        word=15,
        surface_in="\u064a\u064f\u062d\u0650\u0652\u06d7\u0649\u064e",
        surface_out="\u064a\u064f\u062d\u0652\u06d7\u0649\u064e",
    ),
    CorruptedToken(
        sura=75,
        aya=40,
        word=6,
        surface_in="\u064a\u064f\u062d\u0650\u0652\u06d7\u0649\u064e",
        surface_out="\u064a\u064f\u062d\u0652\u06d7\u0649\u064e",
    ),
)
"""المواضعُ الستّةُ بأعيانها، يُعيد اشتقاقَها سكربتُ القياس من البايتات نفسِها."""


_RESULT_BEARING_FIELD_MARKERS: Final[tuple[str, ...]] = (
    "outcome",
    "verdict",
    "adopted",
    "birth",
    "freeze",
    "rank",
    "aim",
)


@dataclass(frozen=True, slots=True)
class CodecRevisionAudit:
    """تدقيقُ مراجعةٍ خارجيةٍ واحدة: مُدّعًى مُسمًّى، ومقيسٌ مُشتقّ، وحكمٌ محسوب.

    ولا حقلَ حكمٍ فيها بحال: `outcome` خاصّيةٌ تُشتقُّ من المقارنة، فمن أراد
    حكمًا آخر لزمه تبديلُ المقيس أو البقايا، وكلاهما ظاهر.
    """

    origin: str
    claimed_round_trip_fraction: float
    claimed_token_total: int
    tree_codec_measurement: InvertibilityMeasurement
    witness: IrabCorpusWitness
    corrupted_tokens: tuple[CorruptedToken, ...]
    blocking_residual_codes: frozenset[str]

    def __post_init__(self) -> None:
        if not isinstance(self.origin, str) or not self.origin.strip():
            raise GflkCodecRevisionAuditError("منشأُ المراجعة نصٌّ غير فارغ.")
        if not isinstance(self.tree_codec_measurement, InvertibilityMeasurement):
            raise GflkCodecRevisionAuditError(
                "المقيسُ قياسٌ مُشتقٌّ من تشغيلِ مِرمازِ هذه الشجرة، لا رقمٌ " "مكتوب."
            )
        if not isinstance(self.witness, IrabCorpusWitness):
            raise GflkCodecRevisionAuditError(
                "التدقيقُ مربوطٌ بشاهدٍ خارجيٍّ مُبصَّم؛ وبلا شاهدٍ لا يُعاد " "اشتقاقُه."
            )
        if (
            self.tree_codec_measurement.source_sha256 != self.witness.sha256
            or self.tree_codec_measurement.source_byte_length
            != self.witness.byte_length
        ):
            raise GflkCodecRevisionAuditError(
                "بصمةُ القياس وطولُه يطابقان الشاهدَ المُسمّى؛ وقياسٌ على "
                "بايتاتٍ أخرى لا يُدقِّق هذا الادّعاء."
            )
        if (
            isinstance(self.claimed_round_trip_fraction, bool)
            or not isinstance(self.claimed_round_trip_fraction, int | float)
            or not 0.0 <= float(self.claimed_round_trip_fraction) <= 1.0
        ):
            raise GflkCodecRevisionAuditError(
                "النسبةُ المُدّعاة كسرٌ بين الصفر والواحد؛ تُسجَّل كما ادُّعيت."
            )
        if (
            isinstance(self.claimed_token_total, bool)
            or not isinstance(self.claimed_token_total, int)
            or self.claimed_token_total < 1
        ):
            raise GflkCodecRevisionAuditError("عددُ الكلماتِ المُدّعى عددٌ صحيحٌ موجب.")
        if not isinstance(self.corrupted_tokens, tuple) or any(
            not isinstance(item, CorruptedToken) for item in self.corrupted_tokens
        ):
            raise GflkCodecRevisionAuditError(
                "جدولُ الإفسادِ الصامت كلماتٌ مُسمّاةٌ بمواضعها، لا عددٌ مجرَّد."
            )
        locations = [token.location for token in self.corrupted_tokens]
        if len(set(locations)) != len(locations):
            raise GflkCodecRevisionAuditError(
                "موضعٌ مكرَّرٌ في جدول الإفساد يُوهِم تعدُّدَ شواهد."
            )
        if not isinstance(self.blocking_residual_codes, frozenset):
            raise GflkCodecRevisionAuditError(
                "رموزُ البقايا الحاجزة مجموعةٌ مجمَّدةٌ من رموزٍ مُسجَّلة."
            )
        unknown = sorted(
            self.blocking_residual_codes - set(GFLK_REVISION_AUDIT_RESIDUALS)
        )
        if unknown:
            raise GflkCodecRevisionAuditError(
                "بقيّةٌ حاجزةٌ غيرُ مُسجَّلةٍ في جدول البقايا: " + ", ".join(unknown)
            )

    @property
    def measured_token_total(self) -> int:
        """مجتمعُ القياس: كلماتُ المدوَّنة نفسِها التي قيس عليها الطرفان."""

        return self.tree_codec_measurement.token_total

    @property
    def measured_round_trip_fraction(self) -> float:
        """نسبةُ المراجعةِ المُودَعة، مُشتقّةً من عدّ كلماتِها المُفسَدة.

        وهي نسبةُ المِرمازِ المُودَع لا نسبةَ مِرمازِ هذه الشجرة: ذاك يَرُدُّ
        الكلماتِ الستَّ عند الإنشاء ولا يُفسِدها، وقياسُه مسجَّلٌ على حِدَةٍ في
        `tree_codec_measurement` كي لا يُقرأ أحدُهما مكانَ الآخر.
        """

        total = self.measured_token_total
        return (total - len(self.corrupted_tokens)) / total

    @property
    def claim_reproduced(self) -> bool:
        """هل أُعيد اشتقاقُ الادّعاء نسبةً ومجتمعًا؟ محسوبٌ لا مكتوب."""

        return (
            not self.corrupted_tokens
            and float(self.claimed_round_trip_fraction)
            == self.measured_round_trip_fraction
            and self.claimed_token_total == self.measured_token_total
        )

    @property
    def token_total_gap(self) -> int:
        """الفجوةُ بين المجتمعِ المُدّعى والمجتمعِ المقيس، موجبةً كانت أو سالبة."""

        return self.claimed_token_total - self.measured_token_total

    @property
    def outcome(self) -> AdoptionOutcome:
        """الحكم، مُشتقًّا من المقارنةِ والبقايا؛ ولا يُكتَب في حقل."""

        if self.blocking_residual_codes or not self.claim_reproduced:
            return AdoptionOutcome.ADOPTION_REFUSED
        return AdoptionOutcome.CLAIM_REPRODUCED_PENDING_AUTHORITY


def _refuse_result_bearing_fields() -> None:
    """يمنع تسلُّلَ حقلِ حكمٍ إلى التدقيق لاحقًا، لا حين كُتِب فحسب."""

    declared = {item.name for item in fields(CodecRevisionAudit)}
    for marker in _RESULT_BEARING_FIELD_MARKERS:
        offending = sorted(name for name in declared if marker in name.split("_"))
        if offending:
            raise GflkCodecRevisionAuditError(
                "حكمُ التدقيق مُشتقٌّ لا مكتوب؛ وحقلٌ كهذا يُبطِل الاشتقاق: "
                + ", ".join(offending)
            )


_refuse_result_bearing_fields()


GFLK_CODEC_REVISION_AUDIT: Final[CodecRevisionAudit] = CodecRevisionAudit(
    origin=DEPOSITED_REVISION_ORIGIN,
    claimed_round_trip_fraction=CLAIMED_ROUND_TRIP_FRACTION,
    claimed_token_total=CLAIMED_TOKEN_TOTAL,
    tree_codec_measurement=QURANIC_CORPUS_INVERTIBILITY,
    witness=QURANIC_ARABIC_CORPUS_WITNESS,
    corrupted_tokens=SILENT_OVERWRITE_LOCATIONS,
    blocking_residual_codes=_BLOCKING_RESIDUAL_CODES,
)
"""التدقيقُ الواحد، وحكمُه `ADOPTION_REFUSED` مُشتقًّا لا مكتوبًا."""
