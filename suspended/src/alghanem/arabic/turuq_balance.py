"""موازنُ الطرق: ترتيبُ قوّةِ طرق المعرفة الثلاث بحارسٍ مقدَّمٍ عليها.

الاسمُ **موازنُ الطرق** لا «الدراية»، لأنّ «الدراية» محجوزةٌ في هذه الشجرة
لمعنًى آخر: نقدُ المتن مقابل نقد السند في `riwaya_diraya_registration`. فلو
سُمّي هذا الميزانُ بها لصار اللفظُ الواحدُ جنسَين، وهو عينُ الخطأ الذي أُغلق في
`dal_alone_bridge` حين فُصل بابُ حرف الدال عن ضلع الدالّ وحدَه
(`THE_BALANCE_IS_NOT_THE_DIRAYA_OF_THE_MATN`)::

    TuruqBalance   != RiwayaDirayaRegistration
    NamedIsCounted != CountedIsStrong
    Reserved       != Defeated
    RefusedOnce    != RefusedForever

**الطرقُ ثلاثٌ مرتَّبةٌ: عدٌّ، فبنيانٌ، فحجز.** والترتيبُ مسنونٌ ههنا لا مقروءٌ
من القرص، فلا يمرّ إلّا مُعلَنًا بنصِّه. ومعناه أنّ ما عارض عدًّا ببنيانٍ رُدَّ
بنيانُه (D1).

**والحارسُ الأوّلُ مقدَّمٌ على الترتيب كلِّه.** D0 يسأل قبل كلِّ شيء:
أالمعدودُ هو المُسمّى؟ فعدٌّ صحيحٌ تمامًا لغيرِ ما سُمّي به لا يُنقَذ بقوّة
طريقه، بل يسقط قبل أن يُوزَن. وهذا ليس تنظيرًا: في سجلّ
`exhibits/tawlid-algebra/ledger.json` جنسٌ مُودَعٌ اسمُه
`بصمةٌ_مقيسةٌ_والظاهرةُ_غيرُها`، وحلقاتُه تُقاس ههنا بمولّدٍ لا تُنقَل عددًا
(`A_CORRECT_COUNT_OF_THE_WRONG_NAME_IS_THE_STRONGEST_ROAD_TO_ERROR`).

**والحجزُ يمنع قبل القياس ولا يَرُدُّ بعده (D3).** فمن قاس محجوزًا ثمّ ردَّه
فقد رفع حجزَه بيده ثمّ حاكمه، وهذه مخالفةٌ لا نصرٌ
(`MEASURING_A_RESERVED_CLAIM_LIFTS_ITS_RESERVATION_BY_HAND`).

**وكلُّ قاعدةٍ من الخمس تحمل شاهدَها المُسقِط.** لا تُسَنُّ قاعدةٌ ههنا إلّا
ومعها الجملةُ التي تُسقطها باسمها إن صحّت يومًا، ويُقاس **عضُّ** كلِّ قاعدة —
كم حلقةً في السجلّ المُودَع تتناولها الآن — فقاعدةٌ لا تعضّ شيئًا تُعلَن
خاويةَ المستأجر ولا تُحسَب عاملة
(`A_RULE_THAT_BITES_NOTHING_IS_DECLARED_TENANTLESS`).
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Final

from alghanem.arabic.tawlid_algebra_ledger import (
    LinkGenus,
    LinkStanding,
    standings,
)

__all__ = [
    "A_CORRECT_COUNT_OF_THE_WRONG_NAME_IS_THE_STRONGEST_ROAD_TO_ERROR",
    "A_RULE_THAT_BITES_NOTHING_IS_DECLARED_TENANTLESS",
    "MEASURING_A_RESERVED_CLAIM_LIFTS_ITS_RESERVATION_BY_HAND",
    "THE_BALANCE_IS_NOT_THE_DIRAYA_OF_THE_MATN",
    "THE_ORDER_IS_ENACTED_HERE_NOT_READ",
    "BalanceError",
    "BalanceRule",
    "Claim",
    "RuleBite",
    "Tariqa",
    "Weighing",
    "rule_bites",
    "strength_of",
    "the_rules_in_order",
    "weigh",
]

THE_BALANCE_IS_NOT_THE_DIRAYA_OF_THE_MATN: Final[str] = (
    "THE_BALANCE_IS_NOT_THE_DIRAYA_OF_THE_MATN: موازنُ الطرق يرتّب قوّةَ "
    "طرقِ المعرفة، ودرايةُ الرواية تنقد المتنَ مقابلَ السند؛ جنسان لا "
    "يجمعهما اسمٌ واحد، ولذلك لم يُسَمَّ هذا الميزانُ درايةً."
)

THE_ORDER_IS_ENACTED_HERE_NOT_READ: Final[str] = (
    "THE_ORDER_IS_ENACTED_HERE_NOT_READ: ترتيبُ الطرق الثلاث مسنونٌ بيدٍ في "
    "هذه الوحدة، ليس مقيسًا من بايتاتٍ؛ فهو قاعدةٌ تُعلَن ويُحاجَج فيها، لا "
    "خاصّيّةٌ تُنسَب إلى القرص."
)

A_CORRECT_COUNT_OF_THE_WRONG_NAME_IS_THE_STRONGEST_ROAD_TO_ERROR: Final[str] = (
    "A_CORRECT_COUNT_OF_THE_WRONG_NAME_IS_THE_STRONGEST_ROAD_TO_ERROR: عدٌّ "
    "صحيحٌ لغير مُسمّاه يمرّ بأقوى الطرق فيحمل خطأَه بأقوى سند؛ ولذلك سُئل "
    "عن المُسمّى قبل أن يُوزَن، لا بعد أن يُرجَّح."
)

MEASURING_A_RESERVED_CLAIM_LIFTS_ITS_RESERVATION_BY_HAND: Final[str] = (
    "MEASURING_A_RESERVED_CLAIM_LIFTS_ITS_RESERVATION_BY_HAND: المحجوزُ "
    "يُمنَع قبل القياس؛ فمن قاسه ثمّ ردَّه فقد رفع حجزَه بيده ثمّ حاكمه، "
    "والردُّ حينئذٍ مخالفةٌ للحجز لا إعمالٌ له."
)

A_RULE_THAT_BITES_NOTHING_IS_DECLARED_TENANTLESS: Final[str] = (
    "A_RULE_THAT_BITES_NOTHING_IS_DECLARED_TENANTLESS: قاعدةٌ لا تتناول "
    "حلقةً واحدةً في المُودَع تُعلَن خاويةَ المستأجر؛ فالقاعدةُ تُسَنُّ "
    "بعضِّها المقيس لا بحُسن صياغتها."
)


class BalanceError(ValueError):
    """رفضٌ صريحٌ في موازن الطرق."""


class Tariqa(Enum):
    """طرقُ المعرفة الثلاث، مسمّاةً لا مرقَّمة."""

    COUNTING = "عدّ"
    STRUCTURE = "بنيان"
    RESERVATION = "حجز"


_STRENGTH: Final[dict[Tariqa, int]] = {
    Tariqa.COUNTING: 3,
    Tariqa.STRUCTURE: 2,
    Tariqa.RESERVATION: 1,
}


def strength_of(tariqa: Tariqa) -> int:
    """قوّةُ الطريق في الترتيب المسنون؛ الأكبرُ أقوى."""

    return _STRENGTH[tariqa]


class BalanceRule(Enum):
    """القواعدُ الخمس بترتيب إجرائها: D0 ثمّ D1 ثمّ D2 ثمّ D3 ثمّ D4."""

    D0_NAMED_IS_COUNTED = "المعدودُ_هو_المُسمّى"
    D1_ROAD_ORDER = "ترتيبُ_الطرق"
    D2_WHO_MAY_OPPOSE = "المعارضةُ_من_المختوم_والشهاديّ"
    D3_RESERVED_DOES_NOT_OPPOSE = "الحجزُ_لا_يُعارض"
    D4_REFUSAL_IS_ARCHIVED = "الردُّ_أمانةٌ_مؤرشفة"


_ORDER: Final[tuple[BalanceRule, ...]] = (
    BalanceRule.D0_NAMED_IS_COUNTED,
    BalanceRule.D1_ROAD_ORDER,
    BalanceRule.D2_WHO_MAY_OPPOSE,
    BalanceRule.D3_RESERVED_DOES_NOT_OPPOSE,
    BalanceRule.D4_REFUSAL_IS_ARCHIVED,
)


def the_rules_in_order() -> tuple[BalanceRule, ...]:
    """القواعدُ بترتيب إجرائها؛ والحارسُ الأوّلُ مقدَّمٌ على ترتيب الطرق."""

    return _ORDER


THE_FALSIFIERS: Final[dict[BalanceRule, str]] = {
    BalanceRule.D0_NAMED_IS_COUNTED: (
        "تسقط D0 إن أُبرز مثالٌ واحدٌ لبصمةٍ سُمّيت باسم ظاهرةٍ ليست هي ثمّ "
        "صحّ الاستدلالُ بها على تلك الظاهرة بعينها."
    ),
    BalanceRule.D1_ROAD_ORDER: (
        "تسقط D1 إن أُبرز بنيانٌ مرخَّصٌ ردَّ عدًّا مُعادَ اشتقاقِه فكان " "البنيانُ هو المصيب."
    ),
    BalanceRule.D2_WHO_MAY_OPPOSE: (
        "تسقط D2 إن عارض صوريٌّ لم تصل مادّتُه عدًّا فأُخذ بمعارضته."
    ),
    BalanceRule.D3_RESERVED_DOES_NOT_OPPOSE: (
        "تسقط D3 إن قيس محجوزٌ ثمّ رُدّ بعد قياسه فكان ذلك إعمالًا لحجزه " "لا رفعًا له."
    ),
    BalanceRule.D4_REFUSAL_IS_ARCHIVED: (
        "تسقط D4 إن وُجد ردٌّ في هذه الشجرة بلا معارضٍ مُعلَنٍ باسمه."
    ),
}


@dataclass(frozen=True)
class Claim:
    """دعوى تُوزَن: اسمُها، وطريقُها، وأمُسمّاها هو معدودُها، وأمحجوزةٌ هي."""

    name: str
    tariqa: Tariqa
    counted_is_the_named: bool
    is_reserved: bool = False
    is_rederived: bool = False

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise BalanceError("دعوى بلا اسمٍ لا تُوزَن.")
        if self.is_reserved and self.tariqa is not Tariqa.RESERVATION:
            raise BalanceError(
                f"{self.name}: المحجوزُ طريقُه الحجزُ؛ ولا يُحجَز عدٌّ " "ويُترَك مسمًّى عدًّا."
            )


@dataclass(frozen=True)
class Weighing:
    """حكمُ الميزان: القاعدةُ التي قطعت، والمرجَّحُ، وسببٌ مُعلَن."""

    deciding_rule: BalanceRule
    upheld: str | None
    reason: str


def weigh(contender: Claim, incumbent: Claim) -> Weighing:
    """يُجري القواعدَ بترتيبها ويقف عند أوّل قاعدةٍ تقطع.

    والوقوفُ عند الأولى مقصودٌ: قاعدةٌ لاحقةٌ لا تُراجع قطعَ سابقتها، وإلّا
    صار الترتيبُ زينةً لا سندًا.
    """

    for claim in (contender, incumbent):
        if not claim.counted_is_the_named:
            return Weighing(
                deciding_rule=BalanceRule.D0_NAMED_IS_COUNTED,
                upheld=None,
                reason=(
                    f"{claim.name}: معدودُه غيرُ مُسمّاه، فسقط قبل الوزن — "
                    f"{A_CORRECT_COUNT_OF_THE_WRONG_NAME_IS_THE_STRONGEST_ROAD_TO_ERROR}"
                ),
            )

    for claim in (contender, incumbent):
        if claim.is_reserved:
            return Weighing(
                deciding_rule=BalanceRule.D3_RESERVED_DOES_NOT_OPPOSE,
                upheld=None,
                reason=(
                    f"{claim.name}: محجوزٌ، فيُمنَع قبل القياس ولا يدخل "
                    f"خصمًا — {MEASURING_A_RESERVED_CLAIM_LIFTS_ITS_RESERVATION_BY_HAND}"
                ),
            )

    for claim in (contender, incumbent):
        if not claim.is_rederived:
            return Weighing(
                deciding_rule=BalanceRule.D2_WHO_MAY_OPPOSE,
                upheld=None,
                reason=(
                    f"{claim.name}: لم يُعَد اشتقاقُه، والمعارضةُ من المختوم "
                    "والشهاديّ وحدَهما، فليس طرفًا في الخصومة أصلًا."
                ),
            )

    here = strength_of(contender.tariqa)
    there = strength_of(incumbent.tariqa)
    if here == there:
        return Weighing(
            deciding_rule=BalanceRule.D4_REFUSAL_IS_ARCHIVED,
            upheld=None,
            reason=(
                f"{contender.name} و{incumbent.name}: طريقاهما في مرتبةٍ "
                "واحدة، فلا يرجّح الترتيبُ أحدَهما، ويُؤرشَف التعارضُ "
                "بطرفيه مُعلَنَين."
            ),
        )
    stronger, weaker = (
        (contender, incumbent) if here > there else (incumbent, contender)
    )
    return Weighing(
        deciding_rule=BalanceRule.D1_ROAD_ORDER,
        upheld=stronger.name,
        reason=(
            f"{stronger.name} بطريق {stronger.tariqa.value} أقوى من "
            f"{weaker.name} بطريق {weaker.tariqa.value}، فرُدَّ الأضعف."
        ),
    )


@dataclass(frozen=True)
class RuleBite:
    """عضُّ قاعدةٍ على المُودَع: كم حلقةً تتناولها الآن، ومِن كم."""

    rule: BalanceRule
    bitten: int
    out_of: int

    @property
    def is_tenantless(self) -> bool:
        """أقاعدةٌ لا تتناول حلقةً واحدة؟"""

        return self.bitten == 0


def rule_bites() -> tuple[RuleBite, ...]:
    """يقيس عضَّ كلِّ قاعدةٍ على سجلّ التوليد المُودَع، ولا ينقل عددًا."""

    read = standings()
    total = len(read)
    d0 = sum(1 for link, _ in read if link.genus is LinkGenus.PROXY_NOT_THE_PHENOMENON)
    d1 = sum(
        1
        for _, standing in read
        if standing
        in (
            LinkStanding.REDERIVED_AND_AGREES,
            LinkStanding.REDERIVED_AND_DIFFERS,
        )
    )
    d2 = sum(1 for _, standing in read if standing is LinkStanding.REDERIVED_AND_AGREES)
    d3 = sum(
        1
        for _, standing in read
        if standing
        in (
            LinkStanding.ITS_MATERIAL_HAS_NOT_ARRIVED,
            LinkStanding.NOT_FALSIFIABLE_AS_WORDED,
        )
    )
    d4 = sum(
        1 for _, standing in read if standing is LinkStanding.TWO_SIDES_NOT_LIFTED_HERE
    )
    counted = {
        BalanceRule.D0_NAMED_IS_COUNTED: d0,
        BalanceRule.D1_ROAD_ORDER: d1,
        BalanceRule.D2_WHO_MAY_OPPOSE: d2,
        BalanceRule.D3_RESERVED_DOES_NOT_OPPOSE: d3,
        BalanceRule.D4_REFUSAL_IS_ARCHIVED: d4,
    }
    return tuple(
        RuleBite(rule=rule, bitten=counted[rule], out_of=total) for rule in _ORDER
    )
