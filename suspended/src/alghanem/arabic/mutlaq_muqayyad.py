"""المطلقُ والمقيَّد: حملُ المطلق على المقيَّد بشرطين معًا، لا بأحدهما.

المطلقُ لفظٌ دالٌّ على فردٍ شائعٍ في جنسه بلا قيد، والمقيَّدُ ما زِيد عليه وصفٌ
يُضيّق ذلك الشيوع. والمسألةُ عمليًّا مسألةُ **حملٍ**: متى يُحمَل المطلقُ على
المقيَّد فيُقرأ مُقيَّدًا، ومتى يبقى كلٌّ منهما على حاله؟

**والشرطان مجتمعان لا مفترقان** (`BothUnitiesOrNoCarrying`): اتّحادُ الحكم
**واتّحادُ سببه معًا**. فإن اختلف أحدُهما فلا حمل. وهذا هو موضعُ الخطأ الذي
تُبنى الوحدةُ لمنعه: من اكتفى باتّحاد الحكم حَمَل نصوصًا لا تُحمَل، ومن اكتفى
باتّحاد السبب فعل مثلَه. ولذلك **يُشتَقّ** الحملُ من الشرطين ولا يُكتَب في حقل،
وتُرفَض عند الإنشاء كلُّ قراءةٍ مكتوبةٍ تخالف المُشتَقّ.

**والشاهدُ المُسجَّل شاهدُ عدمِ حمل، لا شاهدُ حمل** (`ZIHAR_QATL_PAIR`): عتقُ
الرقبة في الظهار مطلقٌ، وعتقُها في القتل الخطأ مقيَّدٌ بالإيمان؛ والحكمُ الجنسيُّ
واحدٌ في ظاهره (عتقُ رقبة) ومع ذلك **لا يُحمَل** أحدُهما على الآخر لاختلاف سبب
الحكم. وهو أنفعُ من شاهد الحمل بعينه لهذا: شاهدُ الحمل يُرضي الشرطين معًا فلا
يكشف أيَّهما كان العامل، وهذا يفصل أحدَهما عن الآخر فيمنع اختزالَهما في واحد.

**وقناةُ الدلالة مستوردةٌ لا منسوخة**: `DalalaChannel` من `mantuq_mafhum_ifada`،
وسعةُ الدليل `DalilScope` ونصُّ `TAKHSIS_IS_NOT_IHMAL_NOTE` من `umum_khusus` —
استيرادًا لا نسخًا، على سابقة `umum_khusus` نفسها في استيرادها للقناة. فالحملُ
كالتخصيص في أنّه **إعمالُ الدليلين معًا**: المقيَّدُ يعمل في موضعه، والمطلقُ لا
يسقط ولا يُهمَل، ولا حقلَ في هذه الوحدة يُكتَب فيه «المُهمَل».

**والإطلاقُ ليس عمومًا** (`ItlaqIsNotUmum`): العامُّ يستغرق أفرادَه كلَّها،
والمطلقُ يدلُّ على فردٍ شائعٍ بلا استغراق. فلا تُستورَد `DalilScope` لتُقرأ
مفردةَ إطلاقٍ، ولا يُقرأ المطلقُ عامًّا وإن اشتركا في آليّة القرار؛ ولذلك
مفردةُ `ItlaqStanding` مستقلّةٌ هنا، ويُفحَص عند الاستيراد أنّها ليست
`DalilScope` نفسها.

**ومفردةُ هذه الوحدة مطلوبةٌ لا مُثبَتة**: القاعدةُ وشاهدُها منقولان في **طلبٍ**
يُحيل إلى الشخصية الإسلامية ج٣، ولم يُنقَل نصُّهما بحروفه في هذا المستودع؛
فالمُخرَجُ «تسجيل» لا «شهادة»، وبقيّتُه في `MUTLAQ_WORDING_NOT_TRANSCRIBED`.

**وهذه الوحدة تسجيلٌ لا سلطة**: لا ولادة، ولا تجميد، ولا `E0`، ولا تستورد من
`kernel/` شيئًا، ولا تقرؤها وحدةٌ فيه.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from typing import Final

from .mantuq_mafhum_ifada import DalalaChannel
from .umum_khusus import TAKHSIS_IS_NOT_IHMAL_NOTE, DalilScope

__all__ = [
    "BOTH_UNITIES_ARE_REQUIRED_NOTE",
    "CARRYING_IS_NOT_IHMAL_NOTE",
    "ITLAQ_IS_NOT_UMUM_NOTE",
    "MUTLAQ_IS_NOT_A_GATE_NOTE",
    "MUTLAQ_WORDING_NOT_TRANSCRIBED",
    "NON_CARRYING_WITNESS_IS_THE_SHARPER_ONE_NOTE",
    "ZIHAR_QATL_PAIR",
    "CarryingOutcome",
    "ItlaqStanding",
    "MutlaqMuqayyadError",
    "NassRegistration",
    "MutlaqMuqayyadPair",
    "derive_carrying",
]


class MutlaqMuqayyadError(ValueError):
    """رفضٌ صريحٌ في تسجيل المطلق والمقيَّد؛ لا يُحمَل على أقرب حالةٍ مقبولة."""


class ItlaqStanding(Enum):
    """حالُ النصّ في لفظه: مطلقٌ أم مقيَّد؛ ثنائيةٌ مغلقةٌ لا درجةَ بينهما.

    وهي **غيرُ** `DalilScope`: تلك سعةُ استغراقٍ (عامٌّ/خاصّ)، وهذه وجودُ قيدٍ
    من عدمه. والمطلقُ يدلُّ على فردٍ شائعٍ بلا استغراق، فليس عامًّا بحال.
    """

    مطلق = "مطلق"
    مقيد = "مقيد"


class CarryingOutcome(Enum):
    """نتيجةُ عرضِ الشرطين؛ ثنائيةٌ مغلقة، والامتناعُ تصريحٌ لا صمت."""

    يحمل = "يحمل"
    لا_يحمل = "لا_يحمل"


BOTH_UNITIES_ARE_REQUIRED_NOTE: Final[str] = (
    "BothUnitiesOrNoCarrying: الحملُ مشروطٌ باتّحاد الحكم واتّحاد سببه معًا، "
    "فإن اختلف أحدُهما فلا حمل. والاكتفاءُ بأحد الشرطين يحمل نصوصًا لا تُحمَل، "
    "ولذلك تُشتَقّ النتيجةُ من الشرطين ولا تُكتَب في حقلٍ يُخالَف به المُشتَقّ"
)

NON_CARRYING_WITNESS_IS_THE_SHARPER_ONE_NOTE: Final[str] = (
    "الشاهدُ المُسجَّل شاهدُ عدمِ حملٍ لا شاهدُ حمل: شاهدُ الحمل يُرضي الشرطين "
    "معًا فلا يكشف أيَّهما كان العامل، وشاهدُ الامتناع مع اتّحاد الحكم الجنسيّ "
    "يفصل الشرطين فيمنع اختزالَهما في واحد"
)

ITLAQ_IS_NOT_UMUM_NOTE: Final[str] = (
    "ItlaqIsNotUmum: العامُّ يستغرق أفرادَه، والمطلقُ يدلُّ على فردٍ شائعٍ في "
    "جنسه بلا استغراق؛ فمفردةُ الإطلاق مستقلّةٌ عن `DalilScope` وإن اشترك "
    "البابان في آليّة القرار، وحملُ إحداهما على الأخرى يُسوّي بين الاستغراق "
    "وعدم التقييد وهما مختلفان"
)

CARRYING_IS_NOT_IHMAL_NOTE: Final[str] = (
    "الحملُ كالتخصيص إعمالُ الدليلين معًا لا إسقاطُ أحدهما، على نصّ "
    "`umum_khusus` بعينه مستورَدًا لا منسوخًا: " + TAKHSIS_IS_NOT_IHMAL_NOTE
)

MUTLAQ_WORDING_NOT_TRANSCRIBED: Final[str] = (
    "MUTLAQ_WORDING_NOT_TRANSCRIBED: القاعدةُ وشاهدُها منقولان في طلبٍ يُحيل "
    "إلى الشخصية الإسلامية ج٣، لا في نصٍّ مُثبَتٍ بحروفه في هذا المستودع؛ "
    "فالمفردةُ مطلوبةٌ لا مُثبَتة، والمُخرَجُ تسجيلٌ لا شهادة"
)

MUTLAQ_IS_NOT_A_GATE_NOTE: Final[str] = (
    "تسجيلٌ لا سلطة: لا تُصدر هذه الوحدة ولادةً ولا حكمَ ولادة ولا تجميدًا ولا "
    "`E0`، ولا تستورد من `kernel/` شيئًا، ولا تقرؤها وحدةٌ فيه"
)

_FORBIDDEN_FIELD_MARKERS: Final[tuple[str, ...]] = (
    "count",
    "total",
    "score",
    "rank",
    "verdict",
    "birth",
    "freeze",
    "dropped",
    "ignored",
    "مهمل",
    "مُهمَل",
)


def _require_non_blank(value: str, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise MutlaqMuqayyadError(f"{label} نصٌّ غير فارغ.")
    return value


def derive_carrying(same_ruling: bool, same_cause: bool) -> CarryingOutcome:
    """اشتقّ الحملَ من الشرطين معًا؛ ولا يكفي أحدُهما بحال."""

    for value, label in ((same_ruling, "اتّحادُ الحكم"), (same_cause, "اتّحادُ السبب")):
        if not isinstance(value, bool):
            raise MutlaqMuqayyadError(f"{label} جوابٌ ثنائيٌّ صريح، لا قيمةٌ تُحمَل.")
    if same_ruling and same_cause:
        return CarryingOutcome.يحمل
    return CarryingOutcome.لا_يحمل


@dataclass(frozen=True, slots=True)
class NassRegistration:
    """نصٌّ مُسجَّل: موضعُه، ولفظُه المقروء، وحكمُه، وسببُ حكمه، وحالُ إطلاقه."""

    reference: str
    wording: str
    ruling: str
    ruling_cause: str
    standing: ItlaqStanding
    qayd: str = ""

    def __post_init__(self) -> None:
        for value, label in (
            (self.reference, "موضعُ النصّ"),
            (self.wording, "لفظُ النصّ المقروء"),
            (self.ruling, "الحكم"),
            (self.ruling_cause, "سببُ الحكم"),
        ):
            _require_non_blank(value, label)
        if not isinstance(self.standing, ItlaqStanding):
            raise MutlaqMuqayyadError("حالُ الإطلاق من مفردتها المغلقة الثنائية.")
        if not isinstance(self.qayd, str):
            raise MutlaqMuqayyadError("القيدُ نصّ.")
        if self.standing is ItlaqStanding.مقيد and not self.qayd.strip():
            raise MutlaqMuqayyadError(
                "المقيَّدُ يلزمه تسميةُ قيده؛ ومقيَّدٌ بلا قيدٍ مُسمًّى دعوى تقييد."
            )
        if self.standing is ItlaqStanding.مطلق and self.qayd.strip():
            raise MutlaqMuqayyadError(
                "المطلقُ لا قيدَ له؛ وكتابةُ قيدٍ له تصريحان متناقضان في تسجيلٍ واحد."
            )

    @property
    def is_qualified(self) -> bool:
        return self.standing is ItlaqStanding.مقيد


@dataclass(frozen=True, slots=True)
class MutlaqMuqayyadPair:
    """نصّان يُعرَضان على الشرطين: مطلقٌ ومقيَّد، والحملُ مُشتَقٌّ لا مكتوب.

    ولا حقلَ هنا لنصٍّ ساقطٍ ولا راجح: النصّان يبقيان معًا في التسجيل، سواءٌ
    وقع الحملُ أم امتنع. و`declared_outcome` تُكتَب ليُقابَل بها المُشتَقّ
    فتُرَدّ المخالفةُ عند الإنشاء، لا لتقوم مقامَه.
    """

    mutlaq: NassRegistration
    muqayyad: NassRegistration
    declared_outcome: CarryingOutcome

    def __post_init__(self) -> None:
        for value, label in (
            (self.mutlaq, "النصُّ المطلق"),
            (self.muqayyad, "النصُّ المقيَّد"),
        ):
            if not isinstance(value, NassRegistration):
                raise MutlaqMuqayyadError(f"{label} نصٌّ مُسجَّلٌ مُصاغ، لا نصٌّ حرّ.")
        if self.mutlaq.standing is not ItlaqStanding.مطلق:
            raise MutlaqMuqayyadError(
                "الطرفُ الأوّل مطلقٌ في لفظه؛ ومقيَّدان لا حملَ بينهما."
            )
        if self.muqayyad.standing is not ItlaqStanding.مقيد:
            raise MutlaqMuqayyadError(
                "الطرفُ الثاني مقيَّدٌ في لفظه؛ ومطلقان لا حملَ بينهما."
            )
        if self.mutlaq.reference == self.muqayyad.reference:
            raise MutlaqMuqayyadError(
                "نصٌّ يُحمَل على نفسه ليس حملًا بل إعادةَ قراءةٍ لنصٍّ واحد."
            )
        if not isinstance(self.declared_outcome, CarryingOutcome):
            raise MutlaqMuqayyadError("النتيجةُ المكتوبة من مفردتها المغلقة الثنائية.")
        if self.declared_outcome is not self.outcome:
            raise MutlaqMuqayyadError(
                "النتيجةُ المكتوبة تخالف المُشتَقّ من الشرطين: "
                f"{BOTH_UNITIES_ARE_REQUIRED_NOTE}"
            )

    @property
    def same_ruling(self) -> bool:
        """اتّحادُ الحكم، مقروءًا من النصّين لا مكتوبًا في حقلٍ ثالث."""

        return self.mutlaq.ruling == self.muqayyad.ruling

    @property
    def same_cause(self) -> bool:
        """اتّحادُ سبب الحكم، مقروءًا من النصّين لا مكتوبًا في حقلٍ ثالث."""

        return self.mutlaq.ruling_cause == self.muqayyad.ruling_cause

    @property
    def outcome(self) -> CarryingOutcome:
        """الحملُ مُشتَقًّا من الشرطين معًا."""

        return derive_carrying(self.same_ruling, self.same_cause)

    @property
    def retained(self) -> tuple[NassRegistration, NassRegistration]:
        """النصّان معًا؛ فالحملُ إعمالٌ لا إسقاط، ولا يسقط أحدُهما بالتسجيل."""

        return (self.mutlaq, self.muqayyad)

    @property
    def blocked_by_cause_alone(self) -> bool:
        """امتنع الحملُ مع اتّحاد الحكم؛ وهذا موضعُ الشاهد المُسجَّل بعينه."""

        return self.same_ruling and not self.same_cause


ZIHAR_QATL_PAIR: Final[MutlaqMuqayyadPair] = MutlaqMuqayyadPair(
    mutlaq=NassRegistration(
        reference="كفّارةُ الظهار",
        wording="تحريرُ رقبةٍ من غير وصفٍ زائد",
        ruling="عتقُ رقبة",
        ruling_cause="الظهار",
        standing=ItlaqStanding.مطلق,
    ),
    muqayyad=NassRegistration(
        reference="كفّارةُ القتل الخطأ",
        wording="تحريرُ رقبةٍ موصوفةٍ بالإيمان",
        ruling="عتقُ رقبة",
        ruling_cause="القتلُ الخطأ",
        standing=ItlaqStanding.مقيد,
        qayd="الإيمان",
    ),
    declared_outcome=CarryingOutcome.لا_يحمل,
)


def _assert_no_fields_matching(markers: tuple[str, ...]) -> None:
    for declaring_type in (NassRegistration, MutlaqMuqayyadPair):
        for field in fields(declaring_type):
            for marker in markers:
                if marker in field.name.lower():
                    raise RuntimeError(
                        f"{declaring_type.__name__} يحمل حقلاً محظورًا: {field.name}"
                    )


if len(ItlaqStanding) != 2:  # pragma: no cover - guard
    raise RuntimeError("حالُ الإطلاق ثنائيةٌ مغلقة: مطلقٌ أو مقيَّد.")
if len(CarryingOutcome) != 2:  # pragma: no cover - guard
    raise RuntimeError("نتيجةُ الحمل ثنائيةٌ مغلقة، والامتناعُ عضوٌ مُصرَّحٌ فيها.")
if {standing.value for standing in ItlaqStanding} & {  # pragma: no cover - guard
    scope.value for scope in DalilScope
}:
    raise RuntimeError(ITLAQ_IS_NOT_UMUM_NOTE)
if len(DalalaChannel) != 2:  # pragma: no cover - guard
    raise RuntimeError("قناةُ الدلالة ثنائيةٌ مغلقة، مستورَدةً لا منسوخة.")
if ZIHAR_QATL_PAIR.outcome is not CarryingOutcome.لا_يحمل:  # pragma: no cover - guard
    raise RuntimeError(
        "الشاهدُ المُسجَّل شاهدُ عدمِ حمل: " + NON_CARRYING_WITNESS_IS_THE_SHARPER_ONE_NOTE
    )
if not ZIHAR_QATL_PAIR.blocked_by_cause_alone:  # pragma: no cover - guard
    raise RuntimeError(
        "الشاهدُ يمتنع لاختلاف السبب وحده مع اتّحاد الحكم؛ وشاهدٌ يختلف فيه "
        "الحكمُ أيضًا لا يفصل الشرطين."
    )
_assert_no_fields_matching(_FORBIDDEN_FIELD_MARKERS)
