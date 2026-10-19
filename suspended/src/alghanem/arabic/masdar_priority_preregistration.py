"""تجميدُ فرضية «المصدر أوّلًا» قبل قياسها، وإيداعُ أرقامها الواردة كما وصلت.

**السؤالُ الذي وُضِعت له هذه الوحدة**: وصلت دعوى ثلاثيةٌ مؤدّاها أنّ المصدر
(أ) يُحدِّد الوزنَ بيقينٍ حيث يشترك الفعل، و(ب) يفصل معانيَ تخلطها هويّةُ
الجذر وحدَها، و(ج) يكشف تعدّيًا يفشل المجهولُ في كشفه — وشاهدُها المذكورُ
جذرٌ واحدٌ هو «قوم» بأربعة مصادرَ موسومةٍ في مدوَّنة MASAQ. والدعوى لا تُقرأ
قياسًا ما لم تحمل **قاعدةَ عدِّها** و**بروتوكولَ اختبارها** و**حدَّ ما
تُثبِته**؛ فتُجمَّد هنا، ويقع القياسُ في `masdar_priority_census`.

`THIS_REGISTRATION_IS_NOT_PRIOR_TO_THE_NUMBER`: وصلت الأرقامُ قبل هذه القواعد،
فمنزلةُ التسجيل `مُصاغ_بعد_الرقم` كما صُرِّح في `imperative_wasla_specification`.
ومن قرأ قواعدَه تنبّؤًا تحقّق قرأ ما لم يقع.

`THE_THREE_CLAIMS_ARE_FALSIFIED_SEPARATELY`: الدعاوى الثلاثُ **مفردةٌ**، لكلٍّ
شرطُ تكذيبها بنصّه؛ فسقوطُ واحدةٍ لا يُسقِط أختَها، وثبوتُ واحدةٍ لا يُثبِتها.
وقد وصلت الثلاثُ مجموعةً في حكمٍ واحد، وجمعُها يُخفي أنّ أضعفَها أضعفُ.

`THE_JOIN_BETWEEN_TWO_CORPORA_IS_LEGISLATED_NOT_READ`: الدعوى (ج) تَصِل مجهولًا
مقيسًا في مدوَّنة القرآن الصرفية بمصدرٍ موسومٍ في MASAQ. ووصلُ جذورِ مدوَّنتين
يستلزم جدولَ تحويلٍ وقرارَ توحيدِ همزة، وكلاهما **قاعدةٌ تُسَنّ** لا قراءةٌ
تُقرأ — وهو بعينه ما أوقف `TheJoinWasNotTaken` في `transitivity_lexicon_witness`
حين خرج التقاطعُ الحرفيُّ صفرًا مقيسًا. فالمانعُ قائمٌ هنا بنصّه، ولا يمرّ
رقمٌ عابرٌ للمدوَّنتين قبل رفعه.

`A_MASDAR_IS_NOT_A_MEASURED_TRANSITIVITY`: الانتقالُ من «مصدرٌ موسوم» إلى
«تعدٍّ مُثبَت» **استنتاجٌ لا قياس** ما لم تُنطَق قاعدةُ الربط بينهما وتُجمَّد.
ولم تصل هذه القاعدة؛ فالدعوى (ج) موقوفةٌ عند حدِّها: شاهدُ **وَسْمِ مصدرٍ
حاضر**، لا شاهدُ تعدٍّ.

`THE_ORDERING_OBJECTION_IS_RECORDED_NOT_EXECUTED`: وصل مع النتيجة حكمٌ بأنّ
بنية «فعل ← لزوم/تعدٍّ ← مشتقّات» معيبةُ الترتيب وأنّ المصدر يجب أن يسبق.
ويُسجَّل الاعتراضُ بنصّه ومقدارِ ما يحمله، **ولا يُنفَّذ** في هذه الجولة:
شاهدُه جذرٌ واحد، ومحطّاتُ `pipeline_stations` تُشتَقّ من الشجرة فتُنتِج
`محطة_غير_مُرمَّزة` لِما لم يُرمَّز بعد.

وهذه الوحدة تجميدٌ لا سلطة: لا ولادةَ فيها، ولا حكمَ ولادة، ولا تجميدَ `E0`،
ولا تستورد من `kernel/` شيئًا، ولا تقرؤها وحدةٌ فيه. ولا حقلَ نتيجةٍ فيها،
وحارسٌ في آخرها يرفض إضافتَه.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest

__all__ = [
    "ARRIVING_MASDAR_FIGURES",
    "A_MASDAR_IS_NOT_A_MEASURED_TRANSITIVITY_NOTE",
    "LEGISLATION_BARRIERS",
    "MASDAR_CLAIMS",
    "MASDAR_PERMUTATION_PROTOCOL",
    "MASDAR_PRIORITY_NAMED_RESIDUALS",
    "MASDAR_PRIORITY_PREREGISTRATION_DIGEST",
    "ORDERING_OBJECTION",
    "PRE_REGISTERED_EXPECTATION",
    "STANDING",
    "THE_JOIN_BETWEEN_TWO_CORPORA_IS_LEGISLATED_NOT_READ_NOTE",
    "THE_ORDERING_OBJECTION_IS_RECORDED_NOT_EXECUTED_NOTE",
    "THE_THREE_CLAIMS_ARE_FALSIFIED_SEPARATELY_NOTE",
    "THIS_REGISTRATION_IS_NOT_PRIOR_TO_THE_NUMBER_NOTE",
    "ArrivingMasdarFigure",
    "LegislationBarrier",
    "MasdarClaim",
    "MasdarCountingRule",
    "MasdarPermutationProtocol",
    "MasdarPriorityPreregistrationError",
    "OrderingObjection",
    "RegistrationStanding",
    "claim_by_label",
    "preregistration_digest",
]


class MasdarPriorityPreregistrationError(ValueError):
    """تُرفَع حين تُوصَف دعوى أو قاعدةُ عدٍّ وصفًا لا يُعاد به اشتقاقُ رقمها."""


class RegistrationStanding(Enum):
    """منزلةُ التسجيل؛ والقيمةُ الأقوى معلنةٌ ليُرى أنّ هذا ليس إيّاها."""

    PRIOR_TO_THE_NUMBER = "سابق_للرقم"
    FORMULATED_AFTER_THE_NUMBER = "مُصاغ_بعد_الرقم"


STANDING: Final[RegistrationStanding] = RegistrationStanding.FORMULATED_AFTER_THE_NUMBER
"""منزلةُ هذا التسجيل بعينه؛ وهي الأضعف، مُعلَنةً لا مُؤوَّلة."""


THIS_REGISTRATION_IS_NOT_PRIOR_TO_THE_NUMBER_NOTE: Final[str] = (
    "ThisRegistrationIsNotPriorToTheNumber: وصلت أرقامُ «قوم» قبل صوغ هذه "
    "القواعد، فمنزلةُ التسجيل `مُصاغ_بعد_الرقم`؛ ومن قرأه تنبّؤًا تحقّق قرأ "
    "ما لم يقع"
)

THE_THREE_CLAIMS_ARE_FALSIFIED_SEPARATELY_NOTE: Final[str] = (
    "TheThreeClaimsAreFalsifiedSeparately: لكلِّ دعوى شرطُ تكذيبها بنصّه؛ "
    "فسقوطُ واحدةٍ لا يُسقِط أختَها، وثبوتُ واحدةٍ لا يُثبِتها، وجمعُها في "
    "حكمٍ واحدٍ يُخفي أنّ أضعفَها أضعف"
)

THE_JOIN_BETWEEN_TWO_CORPORA_IS_LEGISLATED_NOT_READ_NOTE: Final[str] = (
    "TheJoinBetweenTwoCorporaIsLegislatedNotRead: وصلُ جذورِ MASAQ بجذور "
    "مدوَّنة القرآن الصرفية يستلزم جدولَ تحويلٍ وقرارَ توحيدِ همزة، وكلاهما "
    "قاعدةٌ تُسَنّ وتُجمَّد قبل القياس لا قراءةٌ تُقرأ"
)

A_MASDAR_IS_NOT_A_MEASURED_TRANSITIVITY_NOTE: Final[str] = (
    "AMasdarIsNotAMeasuredTransitivity: حضورُ «إقامة» يُثبِت أنّ المُوسِّم "
    "وَسَم مصدرًا، ولا يُثبِت تعدّيًا إلّا بقاعدةِ ربطٍ بين المصدر والتعدّي "
    "تُنطَق وتُجمَّد؛ ولم تصل، فالدعوى موقوفةٌ عند حدِّها"
)

THE_ORDERING_OBJECTION_IS_RECORDED_NOT_EXECUTED_NOTE: Final[str] = (
    "TheOrderingObjectionIsRecordedNotExecuted: الاعتراضُ على ترتيب «فعل ← "
    "لزوم/تعدٍّ ← مشتقّات» مُسجَّلٌ بنصّه وشاهدِه، ولا يُعاد به ترتيبُ الشجرة "
    "على جذرٍ واحد"
)

MASDAR_PRIORITY_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "ThisRegistrationIsNotPriorToTheNumber": (
        THIS_REGISTRATION_IS_NOT_PRIOR_TO_THE_NUMBER_NOTE
    ),
    "TheThreeClaimsAreFalsifiedSeparately": (
        THE_THREE_CLAIMS_ARE_FALSIFIED_SEPARATELY_NOTE
    ),
    "TheJoinBetweenTwoCorporaIsLegislatedNotRead": (
        THE_JOIN_BETWEEN_TWO_CORPORA_IS_LEGISLATED_NOT_READ_NOTE
    ),
    "AMasdarIsNotAMeasuredTransitivity": (A_MASDAR_IS_NOT_A_MEASURED_TRANSITIVITY_NOTE),
    "TheOrderingObjectionIsRecordedNotExecuted": (
        THE_ORDERING_OBJECTION_IS_RECORDED_NOT_EXECUTED_NOTE
    ),
}


class MasdarCountingRule(Enum):
    """قواعدُ العدّ بنصّها؛ ورقمٌ بلا واحدةٍ منها ليس عددًا."""

    MASDAR_SEGMENTS = (
        "المقطعُ الموسومُ مصدرًا: صفٌّ وَسْمُه الصرفيُّ أحدُ وسوم المصدر "
        "المُصرَّح بها في `MasaqColumnBinding`، مجرَّدًا كان أو ميميًّا؛ "
        "ويُعَدُّ كما وُسِم لا كما تُقرأ صورتُه"
    )
    MASDAR_ROOTS = (
        "الجذرُ ذو المصدر: جذرٌ موسومٌ ورد له مقطعٌ واحدٌ فأكثرُ موسومٌ مصدرًا؛ "
        "وجذرٌ بلا وَسْمِ جذرٍ لا يدخل في العدّ ولا يُخمَّن له جذر"
    )
    DISTINCT_MASDAR_LEMMAS = (
        "المصدرُ المتمايز: قيمةُ المدخل المعجميّ (lemma) متمايزةً بين المقاطع "
        "الموسومة مصدرًا؛ والصورةُ المشكولةُ لا تُعَدُّ مُمَيِّزًا لأنّ السياق "
        "يُبدِّل آخرَها"
    )
    MASDAR_FORM_PAIRS = (
        "زوجُ المصدر والوزن: مصدرٌ متمايزٌ مقرونًا بوَسْمِ وزنٍ واحد؛ ومصدرٌ "
        "بلا وَسْمِ وزنٍ يُعَدُّ في بابه `بلا_وزنٍ_موسوم` ولا يُنسَب إلى وزن"
    )


@dataclass(frozen=True, slots=True)
class MasdarClaim:
    """دعوى واحدةٌ من الثلاث، بنصّها وشرطِ تكذيبها وحدِّ ما لا تدّعيه."""

    label: str
    statement: str
    counting_rule: MasdarCountingRule
    what_would_falsify_it: str
    what_it_does_not_claim: str

    def __post_init__(self) -> None:
        for value, label in (
            (self.label, "اسمُ الدعوى"),
            (self.statement, "نصُّ الدعوى"),
            (self.what_would_falsify_it, "شرطُ التكذيب"),
            (self.what_it_does_not_claim, "حدُّ الدعوى"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise MasdarPriorityPreregistrationError(f"{label} نصٌّ غير فارغ.")
        if not isinstance(self.counting_rule, MasdarCountingRule):
            raise MasdarPriorityPreregistrationError("لكلِّ دعوى قاعدةُ عدٍّ مُسمّاة.")


MASDAR_CLAIMS: Final[tuple[MasdarClaim, ...]] = (
    MasdarClaim(
        label="أ_المصدر_يُميِّز_الوزن",
        statement=(
            "المصدرُ المتمايزُ يُحدِّد وزنَ فعله تحديدًا يقينيًّا حيث يشترك "
            "الفعلُ نفسُه بين وزنين: «تقويم» ⟸ الوزن II، و«إقامة» ⟸ الوزن IV"
        ),
        counting_rule=MasdarCountingRule.MASDAR_FORM_PAIRS,
        what_would_falsify_it=(
            "أن يَرِد مصدرٌ متمايزٌ واحدٌ فأكثرُ موسومًا بوزنين مختلفين في هذه "
            "المدوَّنة؛ فالتحديدُ حينئذٍ غالبٌ لا يقينيّ، ويُعرَض عدَدُ الفاصل "
            "وعدَدُ المشترَك معًا لا الفاصلُ وحدَه"
        ),
        what_it_does_not_claim=(
            "لا تدّعي أنّ لكلِّ وزنٍ مصدرًا في هذه المدوَّنة، ولا أنّ المصدرَ "
            "يُميِّز وزنًا لم يَرِد فيها"
        ),
    ),
    MasdarClaim(
        label="ب_المصدر_يفصل_ما_يخلطه_الجذر",
        statement=(
            "هويّةُ الجذر وحدَها تجمع «قيام» و«إقامة» و«تقويم» و«مقام» في خانةٍ "
            "واحدة، والمصدرُ يفصلها مداخلَ متمايزةً موسومةً"
        ),
        counting_rule=MasdarCountingRule.DISTINCT_MASDAR_LEMMAS,
        what_would_falsify_it=(
            "أن يكون لكلِّ جذرٍ ذي مصدرٍ مصدرٌ متمايزٌ واحدٌ لا غير؛ فلا فصلَ "
            "حينئذٍ يزيد على ما يفصله الجذر"
        ),
        what_it_does_not_claim=(
            "لا تدّعي أنّ المصادرَ المتمايزةَ مختلفةُ المعاني: التمايزُ "
            "المقيسُ تمايزُ مداخلَ موسومةٍ لا تمايزُ دلالة، ولا تُقاس الدلالةُ "
            "من وَسْمٍ صرفيّ"
        ),
    ),
    MasdarClaim(
        label="ج_المصدر_يكشف_تعدّيًا_يفشل_فيه_المجهول",
        statement=(
            "جذرٌ مجهولُ وزنِه المزيد صفرٌ في مدوَّنة القرآن الصرفية يَرِد له "
            "مصدرٌ موسومٌ في MASAQ، فيُقرأ المصدرُ كاشفًا لتعدٍّ فشل المجهولُ "
            "في كشفه"
        ),
        counting_rule=MasdarCountingRule.MASDAR_ROOTS,
        what_would_falsify_it=(
            "لا شرطَ تكذيبٍ قابلًا للتشغيل اليوم: الدعوى موقوفةٌ بمانعين "
            "قائمين — وصلُ المدوَّنتين غيرُ مُشرَّع، وقاعدةُ «المصدر ⟸ تعدٍّ» "
            "غيرُ منطوقة. ودعوى بلا شرطِ تكذيبٍ قابلٍ للتشغيل تُسجَّل ولا تُقاس"
        ),
        what_it_does_not_claim=(
            "لا تدّعي أنّ صفرَ المجهول امتناعٌ في العربية: هو غيابٌ في مدوَّنةٍ "
            "محدودة، وهو التحفّظُ نفسُه المقبولُ في نتيجة المضارع والأمر"
        ),
    ),
)
"""الدعاوى الثلاثُ مفردةً؛ ولا تُقرأ واحدةٌ منها حكمًا على أختيها."""


def claim_by_label(label: str) -> MasdarClaim:
    """الدعوى باسمها؛ ولا تُختلَق دعوى ليُقابَل بها رقم."""

    for claim in MASDAR_CLAIMS:
        if claim.label == label:
            return claim
    raise MasdarPriorityPreregistrationError(
        f"لا دعوى بهذا الاسم: {label}؛ ولا تُصاغ بعد رؤية رقمها."
    )


@dataclass(frozen=True, slots=True)
class MasdarPermutationProtocol:
    """بروتوكولُ التبديل ببذرته وعدده وصيغة احتماله؛ ولا يُبدَّل بعد التجميد."""

    statistic: str
    permutations: int
    seed: int
    generator: str
    p_value_formula: str
    p_value_floor_numerator: int

    def __post_init__(self) -> None:
        for value, label in (
            (self.statistic, "نصُّ الإحصاءة"),
            (self.generator, "المولِّدُ العشوائيّ"),
            (self.p_value_formula, "صيغةُ p"),
        ):
            if not value.strip():
                raise MasdarPriorityPreregistrationError(f"{label} نصٌّ غير فارغ.")
        if self.permutations < 1000:
            raise MasdarPriorityPreregistrationError(
                "عددُ التبديلات دون الألف يُضيّق أرضيةَ الاحتمال؛ فلا يُقبَل."
            )
        if self.p_value_floor_numerator != 1:
            raise MasdarPriorityPreregistrationError(
                "بسطُ حدِّ p واحدٌ بحكم صيغته (1 + المتجاوزات) عند صفر متجاوز."
            )

    @property
    def p_value_floor(self) -> float:
        """أصغرُ `p` يُخرِجها هذا البروتوكول؛ ولا يُخرِج صفرًا البتّة."""

        return self.p_value_floor_numerator / (1 + self.permutations)


MASDAR_PERMUTATION_PROTOCOL: Final[MasdarPermutationProtocol] = (
    MasdarPermutationProtocol(
        statistic=(
            "نسبةُ المصادر المتمايزة التي تقابل وزنًا واحدًا لا غير، من جملة "
            "المصادر المتمايزة الموسومة بوزنٍ واحدٍ فأكثر"
        ),
        permutations=5_000,
        seed=20_260_916,
        generator="random.Random(seed).shuffle على قائمة الأوزان مرتَّبةً",
        p_value_formula=(
            "(1 + عددُ التباديل التي بلغت نسبتُها النسبةَ المرصودة) / (1 + 5000)"
        ),
        p_value_floor_numerator=1,
    )
)
"""البروتوكولُ بأرقامه؛ وتبديلُ البذرة بعد رؤية `p` يجعل الاختيارَ نتيجةً."""


@dataclass(frozen=True, slots=True)
class ArrivingMasdarFigure:
    """رقمٌ وصل مُصرَّحًا به في النصّ الوارد، مُجمَّدًا بنصّه قبل إعادة الاشتقاق.

    وإيداعُه ليس تصديقًا له: هو تثبيتُ المُدَّعى كي يكون الفرقُ — إن وقع —
    قابلًا للعرض بدل أن تُعدَّل القاعدةُ حتى تُطابق.
    """

    label: str
    claimed_value: str
    counting_rule: MasdarCountingRule
    corpus: str

    def __post_init__(self) -> None:
        for value, label in (
            (self.label, "اسمُ الرقم"),
            (self.claimed_value, "قيمتُه كما وصلت"),
            (self.corpus, "المدوَّنةُ التي نُسِب إليها"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise MasdarPriorityPreregistrationError(f"{label} نصٌّ غير فارغ.")
        if not isinstance(self.counting_rule, MasdarCountingRule):
            raise MasdarPriorityPreregistrationError("لكلِّ رقمٍ قاعدةُ عدٍّ مُسمّاة.")


ARRIVING_MASDAR_FIGURES: Final[tuple[ArrivingMasdarFigure, ...]] = (
    ArrivingMasdarFigure(
        label="مصادرُ جذر «قوم» المتمايزة",
        claimed_value="4",
        counting_rule=MasdarCountingRule.DISTINCT_MASDAR_LEMMAS,
        corpus="MASAQ",
    ),
    ArrivingMasdarFigure(
        label="«قِيَام» مصدرًا للمجرَّد",
        claimed_value="GERUND",
        counting_rule=MasdarCountingRule.MASDAR_SEGMENTS,
        corpus="MASAQ",
    ),
    ArrivingMasdarFigure(
        label="«إقَامَة / إقَام» مصدرًا للوزن IV",
        claimed_value="GERUND",
        counting_rule=MasdarCountingRule.MASDAR_FORM_PAIRS,
        corpus="MASAQ",
    ),
    ArrivingMasdarFigure(
        label="«تَقْوِيم» مصدرًا للوزن II",
        claimed_value="GERUND",
        counting_rule=MasdarCountingRule.MASDAR_FORM_PAIRS,
        corpus="MASAQ",
    ),
    ArrivingMasdarFigure(
        label="«مَقَام» مصدرًا ميميًّا",
        claimed_value="GERUND_MEEM",
        counting_rule=MasdarCountingRule.MASDAR_SEGMENTS,
        corpus="MASAQ",
    ),
    ArrivingMasdarFigure(
        label="مجهولُ «أقام» في المدوَّنة",
        claimed_value="0",
        counting_rule=MasdarCountingRule.MASDAR_ROOTS,
        corpus="Quranic Arabic Corpus 0.4",
    ),
)
"""الأرقامُ الواردةُ بنصّها ومدوَّنةِ كلٍّ منها؛ ولا يُجمَع رقمُ هذه إلى رقم تلك."""


@dataclass(frozen=True, slots=True)
class LegislationBarrier:
    """قاعدةٌ لازمةٌ لم تُسَنّ بعد، وما تمنعه، وما يرفع منعَها."""

    what_is_blocked: str
    the_rule_that_is_missing: str
    why_it_is_not_a_reading: str
    what_lifts_it: str

    def __post_init__(self) -> None:
        for value, label in (
            (self.what_is_blocked, "الممنوع"),
            (self.the_rule_that_is_missing, "القاعدةُ الناقصة"),
            (self.why_it_is_not_a_reading, "سببُ أنّها تُسَنّ لا تُقرأ"),
            (self.what_lifts_it, "شرطُ الرفع"),
        ):
            if not isinstance(value, str) or not value.strip():
                raise MasdarPriorityPreregistrationError(f"{label} نصٌّ غير فارغ.")


LEGISLATION_BARRIERS: Final[tuple[LegislationBarrier, ...]] = (
    LegislationBarrier(
        what_is_blocked="كلُّ رقمٍ يَصِل وَسْمًا في MASAQ بوَسْمٍ في مدوَّنة القرآن الصرفية",
        the_rule_that_is_missing=(
            "جدولُ تحويل جذور MASAQ إلى ترميز Buckwalter، وقرارُ توحيد الهمزة "
            "المحمولة والمفردة"
        ),
        why_it_is_not_a_reading=(
            "التقاطعُ الحرفيُّ بين ترميزٍ لاتينيٍّ بثمانيةٍ وعشرين محرفًا "
            "وكتابةٍ عربيةٍ بتسعةٍ وعشرين صفرٌ مقيسٌ لا مُقدَّر، كما خرج في "
            "`transitivity_lexicon_witness`؛ فالوصلُ قرارٌ يُتَّخذ. "
            + THE_JOIN_BETWEEN_TWO_CORPORA_IS_LEGISLATED_NOT_READ_NOTE
        ),
        what_lifts_it=(
            "تجميدُ جدول التحويل وقرارِ الهمزة في تسجيلٍ قبْليٍّ مستقلٍّ قبل "
            "القياس، ثمّ عرضُ الأرقام تحته باسمه"
        ),
    ),
    LegislationBarrier(
        what_is_blocked="قراءةُ حضورِ مصدرٍ موسومٍ إثباتًا لتعدّي فعله",
        the_rule_that_is_missing=(
            "قاعدةٌ تقول أيُّ مصدرٍ يستلزم تعدّيًا وأيُّه لا يستلزمه، وبأيّ "
            "قرينةٍ في هذه المدوَّنة"
        ),
        why_it_is_not_a_reading=(
            "وَسْمُ المصدر خبرٌ عن صيغة، والتعدّي خبرٌ عن عملٍ في مفعول؛ "
            "والانتقالُ بينهما استنتاجٌ لا قياس. "
            + A_MASDAR_IS_NOT_A_MEASURED_TRANSITIVITY_NOTE
        ),
        what_lifts_it=(
            "نطقُ القاعدة وتجميدُها، أو الوقوفُ بالدعوى (ج) عند حدِّها: شاهدُ "
            "وَسْمِ مصدرٍ حاضرٍ لا شاهدُ تعدٍّ"
        ),
    ),
)
"""ما لم يُسَنّ بعدُ فيمنع رقمًا؛ ولا يُسَنّ منه شيءٌ في وحدة القياس."""


@dataclass(frozen=True, slots=True)
class OrderingObjection:
    """اعتراضٌ على ترتيبٍ قائمٍ في الشجرة، مُسجَّلٌ بشاهده وحدِّ ما يحمله."""

    objection: str
    the_order_it_objects_to: str
    the_order_it_proposes: str
    evidence_borne: str
    why_it_is_not_executed_now: str
    what_would_let_it_be_executed: str

    def __post_init__(self) -> None:
        for field in fields(self):
            value = getattr(self, field.name)
            if not isinstance(value, str) or not value.strip():
                raise MasdarPriorityPreregistrationError(
                    f"{field.name} نصٌّ غير فارغ؛ واعتراضٌ بلا شاهدٍ مكتوبٍ رأيٌ."
                )


ORDERING_OBJECTION: Final[OrderingObjection] = OrderingObjection(
    objection=(
        "بنيةُ «فعل ← لزوم/تعدٍّ ← مشتقّات» معيبةُ الترتيب؛ والمصدرُ يجب أن "
        "يسبق لأنّه المميِّزُ الوحيدُ الذي يفصل الأوزانَ ويكشف تعدّيًا لا "
        "يظهر في المجهول"
    ),
    the_order_it_objects_to="فعل ← لزوم/تعدٍّ ← مشتقّات",
    the_order_it_proposes="مصدر ← فعل ← لزوم/تعدٍّ ← سائرُ المشتقّات",
    evidence_borne=(
        "جذرٌ واحدٌ هو «قوم» بأربعة مصادرَ موسومةٍ كما وصلت؛ ولم يُعَد اشتقاقُ "
        "هذا من بايتاتٍ مُبصَّمةٍ في هذه الشجرة بعد"
    ),
    why_it_is_not_executed_now=(
        "شاهدُ الاعتراض جذرٌ واحد، ودعوى ترتيبٍ عامّةٌ لا تُبنى على جذر؛ "
        "ومحطّاتُ `pipeline_stations` تُشتَقّ من الشجرة، فتقديمُ محطّةٍ قبل "
        "ترميزها يُنتِج `محطة_غير_مُرمَّزة` لا ترتيبًا جديدًا. "
        + THE_ORDERING_OBJECTION_IS_RECORDED_NOT_EXECUTED_NOTE
    ),
    what_would_let_it_be_executed=(
        "قياسُ الدعوى (أ) على جذور MASAQ كلِّها من بايتاتٍ مُبصَّمةٍ مُودَعةٍ "
        "تامّةً، ورفعُ مانعَي `LEGISLATION_BARRIERS`؛ فيُنظَر حينئذٍ في "
        "الترتيب بشاهدٍ لا بجذر"
    ),
)


PRE_REGISTERED_EXPECTATION: Final[str] = (
    "PreRegisteredExpectation: المُصرَّحُ به — وقد رُئي رقمُ «قوم» قبل الصوغ، "
    "فليس تنبّؤًا — ثلاثةُ أمور. **أوّلًا**: تُتوقَّع الدعوى (ب) ثابتةً بيسر، "
    "فوجودُ جذرٍ واحدٍ بمصدرين متمايزين يكفي لإثباتها، وثبوتُها بهذا الثمن "
    "يُقرأ بقدره لا أكثر. **ثانيًا**: تُتوقَّع الدعوى (أ) **ساقطةً كقاعدةٍ "
    "مطلقة** وقائمةً كغالبٍ مقيس: «إقام» و«إقامة» صيغتان لمصدرٍ واحد، "
    "والمصدرُ الميميُّ يشترك بابُه مع اسم المكان والزمان، فيُنتظَر مصدرٌ "
    "متمايزٌ بوزنين. **ثالثًا**: تبقى الدعوى (ج) بلا رقمٍ ما بقي مانعاها، "
    "ولا يُخرَج لها رقمٌ بقاعدةٍ تُسَنّ أثناء القياس"
)


def preregistration_digest() -> str:
    """بصمةُ محتوى التسجيل؛ فزيادةُ دعوى أو تبديلُ بذرةٍ تُغيّرها."""

    return canonical_digest(
        canonical_bytes(
            {
                "standing": STANDING.value,
                "counting_rules": {
                    rule.name: rule.value for rule in MasdarCountingRule
                },
                "claims": [
                    [
                        claim.label,
                        claim.statement,
                        claim.counting_rule.name,
                        claim.what_would_falsify_it,
                        claim.what_it_does_not_claim,
                    ]
                    for claim in MASDAR_CLAIMS
                ],
                "permutation_protocol": {
                    "statistic": MASDAR_PERMUTATION_PROTOCOL.statistic,
                    "permutations": MASDAR_PERMUTATION_PROTOCOL.permutations,
                    "seed": MASDAR_PERMUTATION_PROTOCOL.seed,
                    "generator": MASDAR_PERMUTATION_PROTOCOL.generator,
                    "p_value_formula": MASDAR_PERMUTATION_PROTOCOL.p_value_formula,
                },
                "arriving_figures": [
                    [
                        figure.label,
                        figure.claimed_value,
                        figure.counting_rule.name,
                        figure.corpus,
                    ]
                    for figure in ARRIVING_MASDAR_FIGURES
                ],
                "barriers": [
                    [barrier.what_is_blocked, barrier.the_rule_that_is_missing]
                    for barrier in LEGISLATION_BARRIERS
                ],
                "ordering_objection": ORDERING_OBJECTION.objection,
                "expectation": PRE_REGISTERED_EXPECTATION,
            }
        )
    )


MASDAR_PRIORITY_PREREGISTRATION_DIGEST: Final[str] = (
    "6e042d755160741e92efe1e1b774e644c259d74179007359cd1e8057ab5e213c"
)
"""البصمةُ المُجمَّدة؛ وحارسُ الاستيراد يرفض أيّ تبديلٍ صامتٍ بعد التجميد."""


_FORBIDDEN_FIELD_MARKERS: Final[tuple[str, ...]] = (
    "outcome",
    "result",
    "observed",
    "measured",
    "rederived",
    "verdict",
    "birth",
)


def _assert_no_outcome_field() -> None:
    """احرسْ خلوَّ وحدة التجميد من حقلِ نتيجةٍ أو مُخرَجٍ مقيس."""

    for dataclass_type in (
        MasdarClaim,
        MasdarPermutationProtocol,
        ArrivingMasdarFigure,
        LegislationBarrier,
        OrderingObjection,
    ):
        for field in fields(dataclass_type):
            lowered = field.name.lower()
            for marker in _FORBIDDEN_FIELD_MARKERS:
                if marker in lowered:
                    raise RuntimeError(
                        f"{dataclass_type.__name__}.{field.name} حقلٌ ممنوع: "
                        "هذه وحدةُ تجميدٍ قبل القياس. "
                        + THIS_REGISTRATION_IS_NOT_PRIOR_TO_THE_NUMBER_NOTE
                    )


def _assert_each_claim_has_its_own_falsifier() -> None:
    """احرسْ إفرادَ الدعاوى: دعويان بشرطِ تكذيبٍ واحدٍ دعوى واحدةٌ مكرَّرة."""

    labels = [claim.label for claim in MASDAR_CLAIMS]
    if len(set(labels)) != len(labels):
        raise RuntimeError(
            "دعوى مكرّرةُ الاسم؛ والتكرارُ يُوهِم تعدُّدَ شواهد. "
            + THE_THREE_CLAIMS_ARE_FALSIFIED_SEPARATELY_NOTE
        )
    falsifiers = [claim.what_would_falsify_it for claim in MASDAR_CLAIMS]
    if len(set(falsifiers)) != len(falsifiers):
        raise RuntimeError(
            "دعويان بشرطِ تكذيبٍ واحد؛ فهما دعوى واحدةٌ قُرِئت اثنتين. "
            + THE_THREE_CLAIMS_ARE_FALSIFIED_SEPARATELY_NOTE
        )


def _assert_the_registration_is_frozen() -> None:
    """احرسْ ثباتَ المُجمَّد ببصمةٍ مُعادةِ الاشتقاق من محتواه."""

    recomputed = preregistration_digest()
    if recomputed != MASDAR_PRIORITY_PREREGISTRATION_DIGEST:
        raise RuntimeError(
            "محتوى التسجيل القبْليّ تغيّر بعد تجميده: البصمةُ المُعادُ "
            f"اشتقاقُها {recomputed} تخالف المُجمَّدة "
            f"{MASDAR_PRIORITY_PREREGISTRATION_DIGEST}. "
            + THIS_REGISTRATION_IS_NOT_PRIOR_TO_THE_NUMBER_NOTE
        )


_assert_no_outcome_field()
_assert_each_claim_has_its_own_falsifier()
_assert_the_registration_is_frozen()
