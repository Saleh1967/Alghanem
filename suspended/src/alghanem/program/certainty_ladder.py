"""سُلَّمُ اليقين: أين ينتهي المُبرهَن، مُشتَقًّا من الشجرة لا مُعلَنًا في جدول.

الدعوى المعروضة سُلَّمٌ من خمس درجات، من الثنائيّ إلى الدلالة، عليه علامتان
فقط: «نعم بيقين ١٠٠٪» لأوّل ثلاث، و«لا» لآخر اثنتين. وهذه الوحدة تقرأ السُّلَّم
نفسَه بقاعدة الشجرة::

    DeclaredCeiling  != DerivedCeiling
    CleanCorpusPass  != ProvenLaw
    RelativeCertainty != AbsoluteCertainty

**وما كشفه الترميز أنّ الحدَّ رُسم درجةً أعلى من موضعه.** ليس في `RungStanding`
عضوٌ اسمُه «يقينٌ مطلق»، ولا يُسنَد إلى درجةٍ ما ليس في المفردة؛ فكلُّ درجةٍ
مما سُمّي «١٠٠٪» تنزل إلى واحدةٍ من ثلاث: يقينٌ **نسبيٌّ إلى إعلان**، أو
استقراءٌ **محدودٌ بمُدوَّنته**، أو درجةٌ لم تُبلَغ. وليست هذه الثلاثُ سُلَّمَ
قوّةٍ فيما بينها، بل أجناسٌ متمايزةُ العلّة (`STANDINGS_ARE_GENERA_NOT_A_SCALE`).

**والدرجةُ الثالثة بعينها هي موضعُ التصحيح.** «حامل/حالة ↔ نصّ مُشكَّل» دعوى
انعكاسٍ (round trip)، ودعوى الانعكاس على مُدوَّنةٍ مغلقةٍ يحكمها صفٌّ مكتوبٌ في
الدستور باسمه: `CompleteInductionIsCorpusBounded` — الاستقصاءُ على مجموعةٍ
منتهيةٍ مغلقة يقينٌ **داخلها وحدها**، وظنٌّ فيما وراءها حتى تُستقصى مُدوَّنةٌ
ثانيةٌ مستقلّة. فمرورُ ٧٨٬٢٤٥ كلمةً بلا استثناء ليس نقضًا لهذا الصفّ بل هو
الحالةُ التي كُتب لها. وقد سبق أن سُمّي هذا في شجرة الترميز نفسِها
(`THREE_SOURCES_ARE_CORPUS_BOUNDED`)، وسُمّي معه أنّ الانعكاس **قابليةُ ردٍّ لا
ذرّية** (`ROUND_TRIP_IS_INVERTIBILITY_NOT_ATOMICITY`).

**والدرجتان الأوليان يقينيّتان نسبةً إلى إعلانٍ لا مطلقًا.** مجموعةُ الحوامل
مكتوبةٌ في الوحدة لا مُشتَقّةٌ من خاصّةٍ للعربية
(`CARRIER_SET_IS_DECLARED_NOT_DERIVED`)، فترقيمُها تقابلٌ تامٌّ **مع** هذا
الإعلان وينتقض بانتقاضه؛ وكذلك «٠/١ ↔ رقم» تقابلٌ مع عرضٍ وترميزٍ مُعلَنَين،
وبدونهما لا يقوم التقابل أصلًا (`BIT_WIDTH_IS_A_CONVENTION_NOT_A_THEOREM`).

**ولا رقمَ من أرقام الدعوى مقبولٌ هنا.** ١٣١/١٣١ و٧٨٬٢٤٥ و٢٨/٢٨ و١٠٠٫٠٠٠٠٪
وصلت سردًا من محادثةٍ أخرى، ولا كودَ في هذه الشجرة يُعيد اشتقاقَها؛ فسُجِّلت في
`alghanem.program.direct_certainty.REPORTED_UNVERIFIED_FIGURES` خبرًا بقيده لا
قياسًا. و`derive_declared_carrier_state_product` يُخرج الجداءَ القائم فعلًا في
هذه الشجرة، فيُقابَل بالرقم المنقول ولا يُستبدَل به.

**وموافقةُ الدعوى في نفيها لا تُقرأ تصديقًا لإثباتها.** وقوفُ الدعوى عند
الدلالة صوابٌ، لكنّ صوابَ حدٍّ أعلى لا يُصحِّح ما تحته؛ ولذلك تُشتَقّ كلُّ
درجةٍ على حدة (`AGREEING_ON_THE_CEILING_IS_NOT_AGREEING_ON_THE_RUNGS`).

ولا سلطةَ لهذه الوحدة: لا تقرؤها بوّابةٌ في `kernel/`، ولا تُجمِّد ولا تُولِد
(`NO_KERNEL_MODULE_CONSUMES_THE_LADDER`).
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

from ..arabic.encoding.carrier_state_candidate import (
    DECLARED_CARRIERS,
    EMBEDDED_ROUND_TRIP_CASES,
    CarrierState,
    round_trip_holds,
)

__all__ = [
    "AGREEING_ON_THE_CEILING_IS_NOT_AGREEING_ON_THE_RUNGS",
    "BIT_WIDTH_IS_A_CONVENTION_NOT_A_THEOREM",
    "CERTAINTY_LADDER_NAMED_RESIDUALS",
    "CORPUS_BOUNDED_LAW_NAME",
    "LADDER_RUNGS",
    "NO_KERNEL_MODULE_CONSUMES_THE_LADDER",
    "STANDINGS_ARE_GENERA_NOT_A_SCALE",
    "CertaintyLadderError",
    "LadderRung",
    "RungAssessment",
    "RungStanding",
    "derive_declared_carrier_state_product",
    "derive_embedded_round_trip_span",
    "derive_ladder_ceiling",
    "rung_assessment",
]


class CertaintyLadderError(ValueError):
    """رُوجِع السُّلَّمُ بما لا يقوم به: درجةٌ بلا علّة، أو يقينٌ بلا إعلانه."""


CORPUS_BOUNDED_LAW_NAME: Final[str] = "CompleteInductionIsCorpusBounded"
"""اسمُ الصفّ الدستوريّ الحاكم للدرجة الثالثة، مذكورٌ ليُراجَع في موضعه."""


# --- الدرجات الخمس، بترتيب الدعوى نفسِه --------------------------------------


class LadderRung(Enum):
    """درجاتُ السُّلَّم الخمس كما عُرضت، لا يُزاد عليها ولا يُدمَج منها اثنتان."""

    BITS_TO_NUMBER = "bits_to_number"
    NUMBER_TO_CARRIER_STATE = "number_to_carrier_state"
    CARRIER_STATE_TO_VOCALIZED_TEXT = "carrier_state_to_vocalized_text"
    VOCALIZED_TEXT_TO_SYNTAX = "vocalized_text_to_syntax"
    TEXT_TO_MEANING = "text_to_meaning"

    @property
    def position(self) -> int:
        """موضعُ الدرجة في السُّلَّم، صفرًا فما فوق."""
        return LADDER_RUNGS.index(self)


LADDER_RUNGS: Final[tuple[LadderRung, ...]] = tuple(LadderRung)


class RungStanding(Enum):
    """رتبةُ الدرجة؛ **ولا عضوَ هنا اسمُه يقينٌ مطلق**، وذلك أصلُ التصحيح.

    وهذه الثلاثُ أجناسٌ لا درجاتٌ في سُلَّم: النسبيُّ إلى إعلانٍ لا يقع «فوق»
    المحدودِ بمُدوَّنته ولا «تحته»؛ علّةُ قصورِ كلٍّ منهما غيرُ علّة الآخر،
    وترتيبُهما في سُلَّمٍ واحد يُخفي ذلك الفرق.
    """

    CERTAIN_RELATIVE_TO_A_DECLARATION = "certain_relative_to_a_declaration"
    CORPUS_BOUNDED_INDUCTION = "corpus_bounded_induction"
    NOT_REACHED_WITH_A_COUNTEREXAMPLE_IN_HAND = "not_reached_with_a_counterexample"

    @property
    def supports_an_unqualified_claim(self) -> bool:
        """أتحمل هذه الرتبةُ دعوى «١٠٠٪» بلا قيدٍ مكتوبٍ معها؟

        لا واحدةَ منها تحملها؛ والدالّةُ مكتوبةٌ لتُقرأ صراحةً لا لتُفترَض.
        """
        return False


@dataclass(frozen=True)
class RungAssessment:
    """رتبةُ درجةٍ واحدة، ومعها علّتُها والقيدُ المُسمّى الذي تُقرأ تحته."""

    rung: LadderRung
    standing: RungStanding
    reason: str
    named_constraint: str

    def __post_init__(self) -> None:
        if not isinstance(self.rung, LadderRung):
            raise CertaintyLadderError("الدرجةُ عضوٌ في `LadderRung`.")
        if not isinstance(self.standing, RungStanding):
            raise CertaintyLadderError("الرتبةُ عضوٌ في `RungStanding`.")
        if not self.reason.strip():
            raise CertaintyLadderError("رتبةٌ بلا علّةٍ مكتوبةٍ لا تُراجَع ولا تُردّ.")
        if not self.named_constraint.strip():
            raise CertaintyLadderError(
                "كلُّ درجةٍ تُقرأ تحت قيدٍ مُسمًّى؛ ودرجةٌ بلا قيدٍ تُقرأ مطلقةً."
            )


_ASSESSMENTS: Final[dict[LadderRung, RungAssessment]] = {
    LadderRung.BITS_TO_NUMBER: RungAssessment(
        rung=LadderRung.BITS_TO_NUMBER,
        standing=RungStanding.CERTAIN_RELATIVE_TO_A_DECLARATION,
        reason=(
            "التقابلُ تامٌّ متى أُعلن العرضُ وترتيبُ البتّات واتّجاهُ الترميز؛ "
            "وبدون هذا الإعلان لا يقوم تقابلٌ أصلًا، فاليقينُ نسبةٌ إليه"
        ),
        named_constraint="BIT_WIDTH_IS_A_CONVENTION_NOT_A_THEOREM",
    ),
    LadderRung.NUMBER_TO_CARRIER_STATE: RungAssessment(
        rung=LadderRung.NUMBER_TO_CARRIER_STATE,
        standing=RungStanding.CERTAIN_RELATIVE_TO_A_DECLARATION,
        reason=(
            "ترقيمُ مجموعةٍ منتهيةٍ تقابلٌ تامٌّ لا مِراءَ فيه؛ غير أنّ المجموعةَ "
            "نفسَها مكتوبةٌ في الوحدة لا مُشتَقّةٌ من خاصّةٍ للعربية، فينتقض "
            "التقابلُ بانتقاض الإعلان لا بخطأٍ في الترقيم"
        ),
        named_constraint="CARRIER_SET_IS_DECLARED_NOT_DERIVED",
    ),
    LadderRung.CARRIER_STATE_TO_VOCALIZED_TEXT: RungAssessment(
        rung=LadderRung.CARRIER_STATE_TO_VOCALIZED_TEXT,
        standing=RungStanding.CORPUS_BOUNDED_INDUCTION,
        reason=(
            "دعوى انعكاسٍ نظيفٍ على مُدوَّنةٍ مغلقة هي بعينها الحالةُ التي كُتب "
            f"لها {CORPUS_BOUNDED_LAW_NAME} في الدستور: يقينٌ داخل المُدوَّنة "
            "وظنٌّ وراءها حتى تُستقصى ثانيةٌ مستقلّة؛ ولا يرفع عددُ الكلمات هذا "
            "الحدَّ لأنه حدُّ جنسِ الاستدلال لا حدُّ حجم العيّنة. والانعكاسُ "
            "قابليةُ ردٍّ لا ذرّية"
        ),
        named_constraint="THREE_SOURCES_ARE_CORPUS_BOUNDED",
    ),
    LadderRung.VOCALIZED_TEXT_TO_SYNTAX: RungAssessment(
        rung=LadderRung.VOCALIZED_TEXT_TO_SYNTAX,
        standing=RungStanding.NOT_REACHED_WITH_A_COUNTEREXAMPLE_IN_HAND,
        reason=(
            "الإعرابُ السياقيُّ لم يُبلَغ، والنقضُ في اليد لا في الاحتمال: "
            "مواضعُ لا تحسمها قرينةٌ مباشرة"
        ),
        named_constraint="SYNTAX_RUNG_IS_NOT_REACHED",
    ),
    LadderRung.TEXT_TO_MEANING: RungAssessment(
        rung=LadderRung.TEXT_TO_MEANING,
        standing=RungStanding.NOT_REACHED_WITH_A_COUNTEREXAMPLE_IN_HAND,
        reason=(
            "الدلالةُ لم تُبلَغ، والنقضُ في اليد: التجانسُ اللفظيُّ غيرُ محلول، "
            "وأبوابٌ صرفيةٌ مؤجَّلةٌ لغياب معلومةٍ معجمية، والتأنيثُ المعنويُّ "
            "بلا مُنبِّئٍ سطحيّ"
        ),
        named_constraint="MEANING_RUNG_IS_NOT_REACHED",
    ),
}


def rung_assessment(rung: LadderRung) -> RungAssessment:
    """رُدَّ رتبةَ درجةٍ بعينها وعلّتَها؛ ولا درجةَ بلا رتبةٍ مكتوبة."""
    if not isinstance(rung, LadderRung):
        raise CertaintyLadderError("الدرجةُ عضوٌ في `LadderRung`.")
    return _ASSESSMENTS[rung]


def derive_ladder_ceiling() -> LadderRung:
    """اشتقّ أعلى درجةٍ بُلغت، لا الدرجةَ المُعلَنة سقفًا.

    والسقفُ مُشتَقٌّ بالمرور على الدرجات بترتيبها والوقوف عند أوّل درجةٍ رتبتُها
    «لم تُبلَغ»؛ فلو غُيِّرت رتبةُ درجةٍ تغيَّر السقفُ معها ولم يبقَ رقمًا مكتوبًا
    في موضعٍ آخر.
    """
    reached: LadderRung | None = None
    for rung in LADDER_RUNGS:
        standing = rung_assessment(rung).standing
        if standing is RungStanding.NOT_REACHED_WITH_A_COUNTEREXAMPLE_IN_HAND:
            break
        reached = rung
    if reached is None:  # pragma: no cover - الدرجةُ الأولى مبلوغةٌ بالإنشاء
        raise CertaintyLadderError("سُلَّمٌ لم تُبلَغ أولى درجاته ليس سُلَّمًا.")
    return reached


# --- ما تُخرجه الشجرة فعلًا، ليُقابَل بالمنقول ولا يُستبدَل به ------------------


def derive_declared_carrier_state_product() -> tuple[int, int, int]:
    """رُدَّ (عددَ الحوامل، عددَ الحالات، جداءَهما) كما هي في هذه الشجرة الآن.

    وهذا جداءُ المفردتين المُعلَنتين لا تعدادُ ما يقع منهما فعلًا في نصّ: ليس
    كلُّ حاملٍ يقبل كلَّ حالة، فالجداءُ حدٌّ أعلى لا إحصاءُ مواضع. ويُقابَل به
    أيُّ رقمٍ يَرِد سردًا فيُرى الفرقُ بدل أن يُسوّى.
    """
    carriers = len(DECLARED_CARRIERS)
    states = len(CarrierState)
    return carriers, states, carriers * states


def derive_embedded_round_trip_span() -> tuple[int, bool]:
    """رُدَّ (عددَ الحالات المُضمَّنة، أتنعكس كلُّها) بتشغيل المُرمِّز الآن.

    وهذا هو كلُّ ما تُثبته هذه الشجرةُ بنفسها عن الدرجة الثالثة: عددٌ صغيرٌ
    مُضمَّنٌ يُعاد تشغيلُه، لا مُدوَّنةٌ محسوبة. والفرقُ بينه وبين أيّ رقمٍ منقولٍ
    ليس فرقَ تقريبٍ بل فرقُ ما يملك المرءُ كودَه.
    """
    cases = EMBEDDED_ROUND_TRIP_CASES
    return len(cases), all(round_trip_holds(surface) for surface in cases)


# --- ما يتركه هذا السُّلَّم مفتوحًا، مُسمًّى -------------------------------------


STANDINGS_ARE_GENERA_NOT_A_SCALE: Final[str] = (
    "STANDINGS_ARE_GENERA_NOT_A_SCALE: اليقينُ النسبيُّ إلى إعلانٍ والاستقراءُ "
    "المحدودُ بمُدوَّنته جنسانِ مختلفا العلّة لا درجتانِ في سُلَّمِ قوّة؛ فلا "
    "يُقرَأ تقدُّمُ أحدهما في التعداد تفضيلًا لدليله"
)

BIT_WIDTH_IS_A_CONVENTION_NOT_A_THEOREM: Final[str] = (
    "BIT_WIDTH_IS_A_CONVENTION_NOT_A_THEOREM: تقابلُ ٠/١ مع الرقم قائمٌ على "
    "عرضٍ وترتيبٍ واتّجاهِ ترميزٍ مُعلَنة؛ وهي اصطلاحٌ يُكتَب لا مبرهنةٌ تُستنتَج، "
    "فاليقينُ فيها نسبةٌ إلى الاصطلاح لا مطلق"
)

AGREEING_ON_THE_CEILING_IS_NOT_AGREEING_ON_THE_RUNGS: Final[str] = (
    "AGREEING_ON_THE_CEILING_IS_NOT_AGREEING_ON_THE_RUNGS: وقوفُ الدعوى عند "
    "الدلالة صوابٌ، وصوابُ الحدّ الأعلى لا يُصحِّح ما تحته؛ ولذلك تُشتَقّ رتبةُ "
    "كلّ درجةٍ على حدة ولا تُقبَل جملةً"
)

NO_KERNEL_MODULE_CONSUMES_THE_LADDER: Final[str] = (
    "NO_KERNEL_MODULE_CONSUMES_THE_LADDER: لا تقرأ هذا السُّلَّمَ أيُّ بوّابةٍ في "
    "`kernel/`، ولا يُجمِّد ولا يُولِد ولا يُرخِّص انتقالًا؛ فهو قراءةٌ لدعوى "
    "لا سلطةٌ عليها"
)

CERTAINTY_LADDER_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "STANDINGS_ARE_GENERA_NOT_A_SCALE": STANDINGS_ARE_GENERA_NOT_A_SCALE,
    "BIT_WIDTH_IS_A_CONVENTION_NOT_A_THEOREM": BIT_WIDTH_IS_A_CONVENTION_NOT_A_THEOREM,
    "AGREEING_ON_THE_CEILING_IS_NOT_AGREEING_ON_THE_RUNGS": (
        AGREEING_ON_THE_CEILING_IS_NOT_AGREEING_ON_THE_RUNGS
    ),
    "NO_KERNEL_MODULE_CONSUMES_THE_LADDER": NO_KERNEL_MODULE_CONSUMES_THE_LADDER,
}
"""ما لا يحسمه هذا السُّلَّم، مُسمًّى هنا لا متروكًا ليُفترَض."""
