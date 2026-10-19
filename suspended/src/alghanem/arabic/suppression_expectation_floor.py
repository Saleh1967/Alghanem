"""أرضيّةُ التوقُّع للكبت: `obs=0` بغير فرضيّةٍ وأرضيّةٍ ومساهمين خليّةٌ فارغة.

**أوّلًا: والغيابُ أقوى من الحضور، ولكن ليس بإطلاق.** دعوى الحضور تُضخَّم
بتكرار توكنٍ واحد، فأُغلِقت آليّتُها في `lexical_artifact_closure`. ودعوى
الغياب محصَّنةٌ من ذلك: تكرارُ كلمةٍ لا يملأ خليّةً فارغة. لكنّها **غيرُ
محصَّنةٍ من الخواء**: خليّةٌ توقُّعُها تحت الفرضية الصفريّة أقلُّ من واحدٍ
ليست كبتًا، بل خليّةٌ صغُرت عيّنتُها عن أن تملأها. فمن قرأ كلَّ صفرٍ كبتًا
استبدل بالأثر المعجميّ صورتَه المرآتيّة
(`A_ZERO_WITH_A_TINY_EXPECTATION_IS_AN_EMPTY_CELL_NOT_A_SUPPRESSION`).

**وثانيًا: وثلاثةٌ تُودَع قبل أيّ قراءةِ كبت.** لا واحدةَ ولا اثنتان:

\\[
\\text{Contract} = (\\ \\text{NullHypothesis},\\ E_{\\min},\\
\\text{TypeContributors}\\ )
\\]

فالفرضيّةُ الصفريّةُ تُعلَن لأنّ التوقُّعَ لا يُحسَب بغيرها؛ وأرضيّةُ
\\(E_{\\min}\\) تُعلَن لأنّ الصفرَ لا يُقرأ إلّا فوقها؛ وتوزيعُ مساهمي الخلايا
الصفريّة على **الأنماط** يُعلَن لأنّ خليّةً يملؤها جذرٌ واحدٌ ليست شاهدًا
كخليّةٍ يملؤها عشرون (`NO_SUPPRESSION_READING_WITHOUT_ALL_THREE_DEPOSITS`).

**وثالثًا: والأنماطُ لا التوكنات.** المساهمون يُعَدُّون أنماطًا، لأنّ عدَّهم
توكناتٍ يُعيد الآليّةَ التي أُغلِقت من جهة الغياب: تصير خليّةٌ «مدعومةً» لأنّ
كلمةً واحدةً تكرّرت فيها ألفَ مرّة. فحدُّ المساهمين حدُّ أنماطٍ، ويُقاس نصيبُ
أكبر مساهمٍ ويُنشَر مع كلّ قراءة
(`A_CELL_HELD_UP_BY_ONE_TYPE_IS_NOT_A_POPULATION`).

**ورابعًا: والاختبارُ المقصودُ مسمًّى وغيرُ مُودَع.** «اختبار CVC المُصفَّى»
بأربعةٍ وسبعمئةٍ وسبعةٍ وأربعين — 4,747 — **ليس في هذه الشجرة**: لا بايتاتُه،
ولا جدولُ خلاياه، ولا مساهموه. فسجلُّ العقود ههنا **فارغٌ**، وكلُّ طلب قراءةٍ
له يُرَدّ بالاسم، ولا يُنقَل رقمُه إلى هذا النثر ليُصدَّق بغير إيداع. وهذا
ليس إنكارًا للاختبار، بل امتناعٌ عن ترخيص قراءةٍ من مادّةٍ غائبة
(`THE_FILTERED_CVC_TEST_IS_NAMED_AND_NOT_DEPOSITED`).

**وخامسًا: والقراءةُ موسومةٌ بنوعها لا مُرسَلة.** مخرَجُ `read_zero_cell`
موقفٌ من ثلاثة: كبتٌ مقروء، أو خليّةٌ فارغةٌ لا تُقرأ كبتًا، أو امتناعٌ
لقصور العقد. ولا موقفَ رابعَ صامت، ولا يُقال «قريبٌ من صفر» بلا حدٍّ
مُعلَنٍ يُقاس عليه القرب (`NEAR_ZERO_IS_A_DECLARED_BAND_NOT_AN_IMPRESSION`).

ولا سلطةَ لهذه الوحدة: لا ولادةَ، ولا حكمَ ولادةٍ، ولا تجميدَ `E0`، ولا
تستورد من `kernel/` شيئًا، ولا فيها اسمُ ماركوف ولا انتروبيا.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, fields
from enum import Enum
from typing import Final

__all__ = [
    "A_CELL_HELD_UP_BY_ONE_TYPE_IS_NOT_A_POPULATION",
    "A_ZERO_WITH_A_TINY_EXPECTATION_IS_AN_EMPTY_CELL_NOT_A_SUPPRESSION",
    "NEAR_ZERO_IS_A_DECLARED_BAND_NOT_AN_IMPRESSION",
    "NO_SUPPRESSION_READING_WITHOUT_ALL_THREE_DEPOSITS",
    "SUPPRESSION_FLOOR_NAMED_RESIDUALS",
    "THE_CONTRACT_REGISTER",
    "THE_FILTERED_CVC_TEST_IS_NAMED_AND_NOT_DEPOSITED",
    "THE_NAMED_UNDEPOSITED_TESTS",
    "NullHypothesis",
    "SuppressionContract",
    "SuppressionFloorError",
    "SuppressionStanding",
    "TypeContributor",
    "ZeroCellReading",
    "contract_for",
    "read_zero_cell",
]


class SuppressionFloorError(ValueError):
    """رفضٌ عند القراءة: عقدٌ ناقصٌ، أو اختبارٌ غيرُ مُودَع، أو عددٌ لا يصحّ."""


class NullHypothesis(Enum):
    """الفرضيّاتُ الصفريّةُ المُعلَنة؛ ولا توقُّعَ يُحسَب بغير واحدةٍ منها."""

    INDEPENDENT_MARGINALS = "استقلالُ-الهوامش"
    UNIFORM_OVER_CELLS = "انتظامٌ-على-الخلايا"


class SuppressionStanding(Enum):
    """مواقفُ الخليّة الصفريّة الثلاثة؛ ولا رابعَ صامتٌ خارجها."""

    SUPPRESSION = "كبتٌ-مقروء"
    EMPTY_CELL = "خليّةٌ-فارغة"
    WITHHELD_FOR_AN_INCOMPLETE_CONTRACT = "امتناعٌ-لقصور-العقد"


# --- البقايا المسمّاة ------------------------------------------------------

A_ZERO_WITH_A_TINY_EXPECTATION_IS_AN_EMPTY_CELL_NOT_A_SUPPRESSION: Final[str] = (
    "A_ZERO_WITH_A_TINY_EXPECTATION_IS_AN_EMPTY_CELL_NOT_A_SUPPRESSION: الغيابُ "
    "محصَّنٌ من التضخُّم بتكرار التوكن وغيرُ محصَّنٍ من الخواء؛ فخليّةٌ توقُّعُها "
    "دون الأرضيّة المُعلَنة لم تُكبَت بل لم تُتَح لها فرصةُ الامتلاء، وقراءتُها "
    "كبتًا صورةٌ مرآتيّةٌ للأثر المعجميّ نفسِه"
)

NO_SUPPRESSION_READING_WITHOUT_ALL_THREE_DEPOSITS: Final[str] = (
    "NO_SUPPRESSION_READING_WITHOUT_ALL_THREE_DEPOSITS: لا تُقرأ خليّةٌ صفريّةٌ "
    "كبتًا إلّا بفرضيّةٍ صفريّةٍ مُعلَنةٍ يُحسَب عليها التوقُّع، وأرضيّةِ توقُّعٍ "
    "دنيا مُعلَنة، وتوزيعِ مساهمين على الأنماط منشور؛ ونقصُ واحدةٍ منها امتناعٌ "
    "لا تساهُل"
)

A_CELL_HELD_UP_BY_ONE_TYPE_IS_NOT_A_POPULATION: Final[str] = (
    "A_CELL_HELD_UP_BY_ONE_TYPE_IS_NOT_A_POPULATION: المساهمون يُعَدُّون "
    "أنماطًا لا توكناتٍ، وإلّا عادت آليّةُ التضخُّم من جهة الغياب فصارت خليّةٌ "
    "مدعومةً لأنّ نمطًا واحدًا تكرّر فيها كثيرًا؛ ونصيبُ أكبر مساهمٍ يُنشَر مع "
    "كلّ قراءة"
)

THE_FILTERED_CVC_TEST_IS_NAMED_AND_NOT_DEPOSITED: Final[str] = (
    "THE_FILTERED_CVC_TEST_IS_NAMED_AND_NOT_DEPOSITED: اختبارُ CVC المُصفَّى "
    "بأربعةٍ وسبعمئةٍ وسبعةٍ وأربعين ليس في هذه الشجرة: لا بايتاتُه ولا جدولُ "
    "خلاياه ولا مساهموه؛ فسجلُّ العقود فارغٌ وكلُّ طلب قراءةٍ له يُرَدّ بالاسم، "
    "وهذا امتناعٌ عن ترخيص قراءةٍ من مادّةٍ غائبةٍ لا إنكارٌ للاختبار"
)

NEAR_ZERO_IS_A_DECLARED_BAND_NOT_AN_IMPRESSION: Final[str] = (
    "NEAR_ZERO_IS_A_DECLARED_BAND_NOT_AN_IMPRESSION: «قريبٌ من صفر» لا يُقبَل "
    "انطباعًا؛ إن أُريد فحدُّه مُعلَنٌ في العقد يُقاس عليه القرب، وما جاوزه "
    "حضورٌ يُقاس بقواعد الحضور لا بقواعد الغياب"
)

SUPPRESSION_FLOOR_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "A_ZERO_WITH_A_TINY_EXPECTATION_IS_AN_EMPTY_CELL_NOT_A_SUPPRESSION": (
        A_ZERO_WITH_A_TINY_EXPECTATION_IS_AN_EMPTY_CELL_NOT_A_SUPPRESSION
    ),
    "NO_SUPPRESSION_READING_WITHOUT_ALL_THREE_DEPOSITS": (
        NO_SUPPRESSION_READING_WITHOUT_ALL_THREE_DEPOSITS
    ),
    "A_CELL_HELD_UP_BY_ONE_TYPE_IS_NOT_A_POPULATION": (
        A_CELL_HELD_UP_BY_ONE_TYPE_IS_NOT_A_POPULATION
    ),
    "THE_FILTERED_CVC_TEST_IS_NAMED_AND_NOT_DEPOSITED": (
        THE_FILTERED_CVC_TEST_IS_NAMED_AND_NOT_DEPOSITED
    ),
    "NEAR_ZERO_IS_A_DECLARED_BAND_NOT_AN_IMPRESSION": (
        NEAR_ZERO_IS_A_DECLARED_BAND_NOT_AN_IMPRESSION
    ),
}


# --- العقدُ ومساهموه -------------------------------------------------------


@dataclass(frozen=True)
class TypeContributor:
    """مساهمٌ في خليّةٍ معدودٌ نمطًا، ووقوعاتُه منشورةٌ ولا تُبدِّل عدَّه."""

    type_key: str
    occurrences: int

    def __post_init__(self) -> None:
        if not self.type_key.strip():
            raise SuppressionFloorError("مساهمٌ بلا مفتاحِ نمطٍ لا يُعَدّ.")
        if self.occurrences < 1:
            raise SuppressionFloorError("مساهمٌ بوقوعاتٍ دون الواحد لا يُسجَّل.")


@dataclass(frozen=True)
class SuppressionContract:
    """عقدُ قراءةِ الكبت: فرضيّةٌ، وأرضيّةُ توقُّعٍ، ومساهمون على الأنماط."""

    test_identity: str
    null_hypothesis: NullHypothesis
    minimum_expectation: float
    type_contributors: tuple[TypeContributor, ...]
    near_zero_band: int = 0

    def __post_init__(self) -> None:
        if not self.test_identity.strip():
            raise SuppressionFloorError("عقدٌ بلا هُويّةِ اختبارٍ لا يُودَع.")
        if self.minimum_expectation <= 0.0:
            raise SuppressionFloorError("أرضيّةُ توقُّعٍ غيرُ موجبةٍ لا تحرس شيئًا.")
        if not self.type_contributors:
            raise SuppressionFloorError(
                "عقدٌ بلا توزيعِ مساهمين على الأنماط عقدٌ ناقصٌ لا يُقرأ به."
            )
        if self.near_zero_band < 0:
            raise SuppressionFloorError("حدُّ «القرب من الصفر» لا يكون سالبًا.")
        keys = [contributor.type_key for contributor in self.type_contributors]
        if len(set(keys)) != len(keys):
            raise SuppressionFloorError("مفتاحُ نمطٍ مُكرَّرٌ بين المساهمين.")

    @property
    def contributing_types(self) -> int:
        """عددُ الأنماط المساهمة، وهو المقامُ في نصيب أكبرها."""

        return len(self.type_contributors)

    @property
    def largest_contributor_share(self) -> float:
        """نصيبُ أكبر مساهمٍ من وقوعات المساهمين، وهو يُنشَر مع كلّ قراءة."""

        total = sum(item.occurrences for item in self.type_contributors)
        return max(item.occurrences for item in self.type_contributors) / total


THE_CONTRACT_REGISTER: Final[tuple[SuppressionContract, ...]] = ()
"""سجلُّ العقود، وهو **فارغٌ** على هذه البيّنة؛ فلا قراءةَ كبتٍ تُصدَر بعدُ."""

THE_NAMED_UNDEPOSITED_TESTS: Final[tuple[str, ...]] = ("filtered-cvc-4747",)
"""اختباراتٌ مسمّاةٌ غيرُ مُودَعة؛ تُذكَر لتُرَدّ بالاسم لا لتُقرأ."""


def contract_for(test_identity: str) -> SuppressionContract:
    """عقدُ اختبارٍ بهُويّته، والمسمّى غيرُ المُودَعِ رفضٌ بالاسم لا فراغ."""

    for contract in THE_CONTRACT_REGISTER:
        if contract.test_identity == test_identity:
            return contract
    if test_identity in THE_NAMED_UNDEPOSITED_TESTS:
        raise SuppressionFloorError(
            f"اختبارٌ مسمًّى غيرُ مُودَع: {test_identity!r}؛ فلا عقدَ له ولا "
            "قراءةَ كبتٍ منه حتّى تُودَع خلاياه ومساهموه."
        )
    raise SuppressionFloorError(f"لا عقدَ لاختبارٍ بهذه الهُويّة: {test_identity!r}.")


# --- قراءةُ الخليّة الصفريّة -------------------------------------------------


@dataclass(frozen=True)
class ZeroCellReading:
    """قراءةُ خليّةٍ موسومةٌ بموقفها وسندِه، ونصيبُ أكبر مساهمٍ فيها منشور."""

    test_identity: str
    observed: int
    expected: float
    standing: SuppressionStanding
    ground: str
    largest_contributor_share: float

    def __post_init__(self) -> None:
        if self.observed < 0:
            raise SuppressionFloorError("مرصودٌ سالبٌ لا يُقرأ.")
        if self.expected < 0.0:
            raise SuppressionFloorError("توقُّعٌ سالبٌ لا يُحسَب.")
        if not self.ground.strip():
            raise SuppressionFloorError("قراءةٌ بلا سندٍ مكتوبٍ لا تُصدَر.")
        if not 0.0 < self.largest_contributor_share <= 1.0:
            raise SuppressionFloorError("نصيبُ أكبر مساهمٍ خارجَ حدِّه.")


def read_zero_cell(
    contract: SuppressionContract, observed: int, expected: float
) -> ZeroCellReading:
    """تقرأ خليّةً تحت عقدها: كبتٌ، أم خليّةٌ فارغة، أم امتناع.

    الترتيبُ مقصودٌ: يُفحَص التوقُّعُ قبل المرصود، لأنّ صفرًا تحت توقُّعٍ دون
    الأرضيّة لا يُقرأ كبتًا مهما صغُر المرصود.
    """

    share = contract.largest_contributor_share
    if expected < contract.minimum_expectation:
        return ZeroCellReading(
            test_identity=contract.test_identity,
            observed=observed,
            expected=expected,
            standing=SuppressionStanding.EMPTY_CELL,
            ground=A_ZERO_WITH_A_TINY_EXPECTATION_IS_AN_EMPTY_CELL_NOT_A_SUPPRESSION,
            largest_contributor_share=share,
        )
    if observed > contract.near_zero_band:
        return ZeroCellReading(
            test_identity=contract.test_identity,
            observed=observed,
            expected=expected,
            standing=SuppressionStanding.WITHHELD_FOR_AN_INCOMPLETE_CONTRACT,
            ground=NEAR_ZERO_IS_A_DECLARED_BAND_NOT_AN_IMPRESSION,
            largest_contributor_share=share,
        )
    return ZeroCellReading(
        test_identity=contract.test_identity,
        observed=observed,
        expected=expected,
        standing=SuppressionStanding.SUPPRESSION,
        ground=NO_SUPPRESSION_READING_WITHOUT_ALL_THREE_DEPOSITS,
        largest_contributor_share=share,
    )


# --- حرّاسُ الاستيراد ------------------------------------------------------


def _assert_no_authority_field() -> None:
    """حارسُ استيراد: لا حقلَ سلطةٍ في قراءةٍ لا سلطةَ فيها."""

    forbidden = {"verdict", "licensed", "born", "frozen", "authority", "rank"}
    for holder in (SuppressionContract, ZeroCellReading, TypeContributor):
        named = {field.name for field in fields(holder)}
        if named & forbidden:
            raise SuppressionFloorError(
                f"حقلُ سلطةٍ في {holder.__name__}: {sorted(named & forbidden)}."
            )


def _assert_the_register_is_empty_and_the_named_test_is_refused() -> None:
    """حارسُ استيراد: السجلُّ فارغٌ، والمسمّى غيرُ المُودَعِ يُرَدّ بالاسم."""

    if THE_CONTRACT_REGISTER:
        raise SuppressionFloorError(
            "سجلُّ العقود ليس فارغًا، والنثرُ يقول إنّه فارغٌ على هذه البيّنة."
        )
    for test_identity in THE_NAMED_UNDEPOSITED_TESTS:
        try:
            contract_for(test_identity)
        except SuppressionFloorError:
            continue
        raise SuppressionFloorError(  # pragma: no cover - الرفضُ فوقُ يمنعه
            f"اختبارٌ غيرُ مُودَعٍ أُخرِج له عقدٌ: {test_identity!r}."
        )


def _assert_a_contract_missing_any_of_the_three_is_refused() -> None:
    """حارسُ استيراد: نقصُ واحدةٍ من الثلاث رفضٌ عند البناء لا تساهُلٌ بعده."""

    contributors = (TypeContributor(type_key="نمط", occurrences=1),)
    builders: tuple[tuple[str, Callable[[], SuppressionContract]], ...] = (
        (
            "minimum_expectation",
            lambda: SuppressionContract(
                test_identity="حارس",
                null_hypothesis=NullHypothesis.INDEPENDENT_MARGINALS,
                minimum_expectation=0.0,
                type_contributors=contributors,
            ),
        ),
        (
            "type_contributors",
            lambda: SuppressionContract(
                test_identity="حارس",
                null_hypothesis=NullHypothesis.INDEPENDENT_MARGINALS,
                minimum_expectation=5.0,
                type_contributors=(),
            ),
        ),
        (
            "test_identity",
            lambda: SuppressionContract(
                test_identity="   ",
                null_hypothesis=NullHypothesis.INDEPENDENT_MARGINALS,
                minimum_expectation=5.0,
                type_contributors=contributors,
            ),
        ),
    )
    for field_name, build in builders:
        try:
            build()
        except SuppressionFloorError:
            continue
        raise SuppressionFloorError(  # pragma: no cover - الرفضُ فوقُ يمنعه
            f"عقدٌ ناقصٌ قُبِل عند {field_name!r}."
        )


def _assert_a_zero_under_the_floor_is_not_a_suppression() -> None:
    """حارسُ استيراد: صفرٌ تحت أرضيّةٍ خليّةٌ فارغةٌ، وفوقها كبتٌ مقروء."""

    contract = SuppressionContract(
        test_identity="حارس",
        null_hypothesis=NullHypothesis.INDEPENDENT_MARGINALS,
        minimum_expectation=5.0,
        type_contributors=(
            TypeContributor(type_key="أ", occurrences=3),
            TypeContributor(type_key="ب", occurrences=1),
        ),
    )
    below = read_zero_cell(contract, observed=0, expected=0.4)
    above = read_zero_cell(contract, observed=0, expected=9.0)
    if below.standing is not SuppressionStanding.EMPTY_CELL:
        raise SuppressionFloorError("صفرٌ تحت الأرضيّة قُرئ كبتًا.")
    if above.standing is not SuppressionStanding.SUPPRESSION:
        raise SuppressionFloorError("صفرٌ فوق الأرضيّة لم يُقرأ كبتًا.")
    if above.largest_contributor_share <= 0.0:
        raise SuppressionFloorError("قراءةٌ خرجت بلا نصيبِ أكبر مساهم.")


def _assert_no_probability_name_is_exported() -> None:
    """حارسُ استيراد: لا اسمَ سلسلةٍ ولا انتروبيا في واجهة أرضيّة التوقُّع."""

    banned = ("entropy", "markov", "nll", "likelihood", "transition_matrix")
    for name in __all__:
        if name in SUPPRESSION_FLOOR_NAMED_RESIDUALS:
            continue
        if any(word in name.lower() for word in banned):
            raise SuppressionFloorError(f"اسمُ احتمالٍ في واجهة الأرضيّة: {name}.")


def _assert_every_residual_is_named_by_its_key() -> None:
    """حارسُ استيراد: كلُّ بقيّةٍ تبدأ بمفتاحها فلا تُقتَبس منزوعةَ النسبة."""

    for key, text in SUPPRESSION_FLOOR_NAMED_RESIDUALS.items():
        if not text.startswith(f"{key}: "):
            raise SuppressionFloorError(f"بقيّةٌ لا تبدأ بمفتاحها: {key}.")


_assert_no_authority_field()
_assert_no_probability_name_is_exported()
_assert_the_register_is_empty_and_the_named_test_is_refused()
_assert_a_contract_missing_any_of_the_three_is_refused()
_assert_a_zero_under_the_floor_is_not_a_suppression()
_assert_every_residual_is_named_by_its_key()
