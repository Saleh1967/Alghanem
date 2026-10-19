"""تسجيلُ آلة الحالة (P-EXTRACTOR) قبل بنائها: قراءةُ حالاتها، وشرطُ قبولها.

المواصفةُ الواردة تُقدِّم «آلةَ حالةٍ» بحالاتٍ جديدة. وهذه الوحدةُ لا تبنيها،
بل تفعل ما يسبق البناءَ ولا يجوز أن يليه: تقرأ كلَّ حالةٍ مقترحةٍ وتسأل عنها
سؤالًا واحدًا، ثمّ تكتب شرطَ القبول **قبل** أيّ قياس.

`A_ROLE_IS_NOT_A_STATE`: السؤالُ عن كلّ حالةٍ مقترحة: أهي حالةُ حاملٍ فعلًا —
أي شيءٌ يحمله الحرفُ ويتغيّر به — أم **وصفُ دورٍ** تؤدّيه وحدةٌ قائمةٌ في سياقٍ
معيّن؟ فمفردةُ `CarrierState` مغلقةٌ بسبعة أعضاء، وإدخالُ وصفِ دورٍ فيها
يُضخِّمها بما ليس منها ويجعل الوحدةَ الواحدة عضوين. والدورُ يُعلَّق على
الوحدة القائمة ولا يزيد المفردة.

`REFUSAL_IS_NOT_A_MEMBER_OF_THE_VOCABULARY`: المواصفةُ تُعلن في بندها الأوّل
أنّ «القرارَ النهائيَّ دومًا ثنائيّ، وDEFER تأجيلٌ إجرائيٌّ لا قيمةٌ ثالثة»،
ثمّ تُدخل في بندها الثاني حالةَ غموضٍ **عضوًا في مفردة الحالات** وتسمّيها
«حالةَ DEFER صريحة». والبندان لا يجتمعان. والحفظُ للبند الأوّل يقتضي إخراجَ
الغموض في **حقلٍ منفصل** لا عضوًا؛ فيستقيم البندُ الثاني بلا نقضِ الأوّل.

`THE_ACCEPTANCE_FLOOR_IS_WRITTEN_BEFORE_THE_MEASUREMENT`: شرطُ القبول مكتوبٌ
هنا قبل بناء الآلة: مطابقةٌ على المدوّنة المُبصَّمة **لا تقلّ** عمّا يحقّقه
المرمازُ القائم اليوم. فتوسعةٌ تُنقص المطابقةَ تراجُعٌ مهما حسُنت بنيتُها؛
ومن قاس أوّلًا ثمّ كتب الشرطَ كتب الشرطَ على مقاسِ ما قاس.

`THIS_IS_REGISTRATION_NOT_AUTHORITY`: لا ولادةَ هنا، ولا حكمَ ولادة، ولا
استيرادَ من `kernel/`.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

from .encoding.carrier_state_candidate import CarrierState

__all__ = [
    "A_ROLE_IS_NOT_A_STATE_NOTE",
    "PROPOSED_STATE_READINGS",
    "P_EXTRACTOR_ACCEPTANCE_CONDITION",
    "REFUSAL_IS_NOT_A_MEMBER_OF_THE_VOCABULARY_NOTE",
    "THE_ACCEPTANCE_FLOOR_IS_WRITTEN_BEFORE_THE_MEASUREMENT_NOTE",
    "UNRESOLVABLE_PROPOSALS",
    "AcceptanceCondition",
    "ProposedStateReading",
    "ProposedStateVerdict",
    "StateMachineRegistrationError",
    "UnresolvableProposal",
    "existing_carrier_state_names",
]


class StateMachineRegistrationError(ValueError):
    """رفضٌ عند الإنشاء: قراءةٌ بلا مُبرِّر، أو غموضٌ أُقحِم في مفردة الحالات."""


class ProposedStateVerdict(Enum):
    """قراءةُ الحالة المقترحة. ليس فيها `مقبولةٌ بلا قياس`."""

    GENUINE_CARRIER_STATE = "حالةُ حاملٍ فعلًا"
    ROLE_OVER_AN_EXISTING_UNIT = "وصفُ دورٍ يُعلَّق على وحدةٍ قائمة"


@dataclass(frozen=True, slots=True)
class ProposedStateReading:
    """حالةٌ مقترحةٌ في المواصفة، وقراءتُها، ومُبرِّرُ القراءة."""

    proposed_name: str
    verdict: ProposedStateVerdict
    grounds: str
    existing_unit: str | None

    def __post_init__(self) -> None:
        if not self.proposed_name.strip() or not self.grounds.strip():
            raise StateMachineRegistrationError("قراءةٌ بلا اسمٍ أو بلا مُبرِّر")
        if (
            self.verdict is ProposedStateVerdict.ROLE_OVER_AN_EXISTING_UNIT
            and not (self.existing_unit or "").strip()
        ):
            raise StateMachineRegistrationError(
                "وصفُ دورٍ بلا وحدةٍ قائمةٍ يُعلَّق عليها ليس وصفَ دورٍ بل حالةً "
                "جديدةً سُمِّيت دورًا"
            )


@dataclass(frozen=True, slots=True)
class UnresolvableProposal:
    """مقترحٌ متعذّرٌ: يُسجَّل في حقلٍ منفصلٍ ولا يُجمَع مع مفردة الحالات.

    وفصلُه ليس ترتيبًا للعرض بل حفظٌ للبند الأوّل من المواصفة نفسها: من جعل
    الغموضَ عضوًا في المفردة صار عنده الغموضُ قيمةً تُرصَد كما تُرصَد الفتحةُ،
    فاختفى الفرقُ بين «لم يُميَّز» و«تميَّز غموضًا».
    """

    proposed_name: str
    why_it_cannot_be_a_member: str
    where_it_belongs_instead: str

    def __post_init__(self) -> None:
        if not self.why_it_cannot_be_a_member.strip():
            raise StateMachineRegistrationError("تعذّرٌ بلا سببٍ مُسمًّى")


@dataclass(frozen=True, slots=True)
class AcceptanceCondition:
    """شرطُ قبولِ التوسعة، مكتوبًا قبل القياس لا بعده."""

    floor_description: str
    floor_reference: str
    what_counts_as_regression: str
    explicit_test_cases: str


def existing_carrier_state_names() -> tuple[str, ...]:
    """أسماءُ حالات الحامل القائمة، مقروءةً من المفردة لا منسوخةً هنا."""

    return tuple(state.name for state in CarrierState)


PROPOSED_STATE_READINGS: Final[tuple[ProposedStateReading, ...]] = (
    ProposedStateReading(
        proposed_name="TANWEEN_ALIF_CARRIER",
        verdict=ProposedStateVerdict.ROLE_OVER_AN_EXISTING_UNIT,
        grounds=(
            "ألفُ التنوين لا تحمل حركةً تخصّها، وإنّما هي مَقعدُ كتابةٍ لتنوينِ "
            "الفتح المحمول على ما قبلها. والمرمازُ القائم يرصد المَقعدَ في "
            "`CarrierSeat.ON_ALEF` ويرصد التنوينَ في الوحدة نفسِها، فالمقترحُ "
            "يصف اجتماعَهما لا شيئًا ثالثًا"
        ),
        existing_unit="CarrierSeat.ON_ALEF مع حقلِ التنوين في CarrierStateUnit",
    ),
    ProposedStateReading(
        proposed_name="MADD_EXTENSION",
        verdict=ProposedStateVerdict.ROLE_OVER_AN_EXISTING_UNIT,
        grounds=(
            "المدُّ امتدادُ صائتٍ سابقٍ لا حالةٌ يحملها الحرفُ من جديد. "
            "و`CarrierSeat.MADD` قائمةٌ في المفردة، فالمقترحُ يُسمّي دورَها في "
            "السياق لا يُضيف محمولًا"
        ),
        existing_unit="CarrierSeat.MADD",
    ),
    ProposedStateReading(
        proposed_name="SHADDA_GEMINATION",
        verdict=ProposedStateVerdict.ROLE_OVER_AN_EXISTING_UNIT,
        grounds=(
            "التضعيفُ مرصودٌ أصلًا في `GeminationRole.PAIR_START`، والنصفُ "
            "الثاني لا يحمل دورًا. فإدخالُه حالةً يجعل الوحدةَ الواحدةَ عضوين"
        ),
        existing_unit="GeminationRole.PAIR_START",
    ),
)


UNRESOLVABLE_PROPOSALS: Final[tuple[UnresolvableProposal, ...]] = (
    UnresolvableProposal(
        proposed_name="AMBIGUOUS_MADD_OR_TANWEEN_ROOT",
        why_it_cannot_be_a_member=(
            "المواصفةُ نفسُها تُعلن في بندها الأوّل أنّ DEFER ليست قيمةً ثالثة، "
            "ثمّ تُدخلها عضوًا في مفردة الحالات في بندها الثاني. والعضويّةُ "
            "تجعل الغموضَ محمولًا يُرصَد كما تُرصَد الفتحة، فيستوي «لم يُميَّز» "
            "و«تميَّز غموضًا» في السجلّ"
        ),
        where_it_belongs_instead=(
            "حقلُ تعذّرٍ منفصلٌ لا يُجمَع مع مفردة الحالات ولا مع مفردة الفشل، "
            "على منوال `REFUSAL_IS_NOT_FAILURE_TO_DISCRIMINATE`؛ فيبقى البندان "
            "الأوّلُ والثاني قائمين بلا تعديلِ أيٍّ منهما"
        ),
    ),
)


P_EXTRACTOR_ACCEPTANCE_CONDITION: Final[AcceptanceCondition] = AcceptanceCondition(
    floor_description=(
        "مطابقةُ الذهاب والإياب على المدوّنة القرآنية المُبصَّمة **لا تقلّ** عن "
        "النسبة التي يحقّقها المرمازُ القائم اليوم على البايتات نفسِها "
        "(الوارِدُ: ٩٩٫٩٩٢٢٥١٪، ستُّ كلماتٍ تعود مغايرةً بصمت)"
    ),
    floor_reference=(
        "تُعاد النسبةُ اشتقاقًا من البايتات بـ"
        "`examples/irab/measure_carrier_state_invertibility.py`، ولا تُنسَخ "
        "رقمًا مكتوبًا؛ والمواضعُ الستّةُ بأعيانها في "
        "`gflk_codec_revision_audit.CORRUPTED_TOKENS`"
    ),
    what_counts_as_regression=(
        "أيُّ نقصٍ في النسبة، أو أيُّ كلمةٍ جديدةٍ تعود مغايرةً لم تكن كذلك — "
        "ولو ارتفعت النسبةُ إجمالًا. فبنيةٌ أحسنُ تُفسد كلمةً كانت سليمةً "
        "تراجُعٌ في موضعٍ وإن تقدّمت في غيره"
    ),
    explicit_test_cases=(
        "الكلماتُ الستُّ المعطوبة تصير حالاتِ اختبارٍ صريحةً بأعيانها، لا "
        "مشمولةً في نسبةٍ إجماليّة؛ فالنسبةُ تُخفي الكلمةَ الواحدة والاختبارُ "
        "المُسمَّى لا يُخفيها"
    ),
)


A_ROLE_IS_NOT_A_STATE_NOTE: Final[str] = (
    "ARoleIsNotAState: وصفُ الدور يُعلَّق على وحدةٍ قائمةٍ ولا يزيد مفردةَ "
    "الحالات؛ ومن أدخله عضوًا صيّر الوحدةَ الواحدةَ عضوين وضخّم المفردةَ بما "
    "ليس منها"
)

REFUSAL_IS_NOT_A_MEMBER_OF_THE_VOCABULARY_NOTE: Final[str] = (
    "RefusalIsNotAMemberOfTheVocabulary: الغموضُ يُخرَج في حقلِ تعذّرٍ منفصلٍ "
    "لا عضوًا في مفردة الحالات؛ وإلّا استوى «لم يُميَّز» و«تميَّز غموضًا» في "
    "السجلّ، ونقضَ البندُ الثاني البندَ الأوّل من المواصفة نفسِها"
)

THE_ACCEPTANCE_FLOOR_IS_WRITTEN_BEFORE_THE_MEASUREMENT_NOTE: Final[str] = (
    "TheAcceptanceFloorIsWrittenBeforeTheMeasurement: شرطُ القبول مكتوبٌ قبل "
    "بناء الآلة وقبل قياسها؛ ومن قاس أوّلًا ثمّ كتب الشرطَ كتبه على مقاسِ ما قاس"
)
