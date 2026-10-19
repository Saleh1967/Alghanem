"""قانونُ ترتيب التركيب: متبادلٌ، أم مشروطُ ترتيبٍ، أم غيرُ محلول.

**أوّلًا: وما فتحته شهادةُ الهُويّة يُغلَق ههنا.** أودعت
`projection_identity_certificate` أنّ التبادلَ شرطُ **ذلك العقد** لا شرطُ كلّ
مسقط، وسمّت بقيّتَه `NO_CERTIFICATE_UNDER_AN_UNORDERED_COMPOSITION`، وأجّلت
جبرَ الترتيب صراحةً. وهذا هو الجبرُ المؤجَّل: تصنيفٌ موسومٌ لكلّ تركيب
طَيٍّ وحدٍّ، لا رفضٌ واحدٌ لكلّ ما لا يتبادل
(`THE_DEFERRED_ORDERING_ALGEBRA_IS_DEPOSITED_HERE_NOT_ASSUMED`).

**وثانيًا: والمواقفُ ثلاثةٌ لا اثنان.**

\\[
\\text{COMMUTES}\\ \\mid\\ \\text{ORDER\\_REQUIRED}\\ \\mid\\ \\text{UNRESOLVED}
\\]

فـ`COMMUTES` يُقاس: \\(B(F_s(T)) = \\operatorname{map}(F_w, B(T))\\). و
`ORDER_REQUIRED` **لا يُقاس بل يُودَع**: تركيبٌ لا يتبادل ولكن لترتيبه وديعةٌ
مكتوبةٌ تقول أيُّ الطرفَين هو القانونيُّ ولِمَ. و`UNRESOLVED` هو الباقي: لا
تبادلَ ولا وديعةَ ترتيب. ولا يُحمَل الثالثُ على الثاني بحالٍ، فإنّ عدمَ
التبادل لا يُنشئ ترتيبًا، وإنّما يُظهِر الحاجةَ إليه
(`A_FAILURE_TO_COMMUTE_DOES_NOT_ITSELF_DEPOSIT_AN_ORDER`).

**وثالثًا: وسجلُّ الترتيب فارغٌ على هذه البيّنة.** الخليّةُ المكسورةُ الوحيدةُ
— الفاتحةُ بحدِّ الفراغ وحدَه — تخرج `UNRESOLVED` لا `ORDER_REQUIRED`، لأنّه
لم يُودَع لها ترتيبٌ قانونيٌّ بعد. وهذا خبرٌ عن وديعتنا لا عن اللغة، ولو
أُودِع لها ترتيبٌ غدًا لانتقلت بلا تعديلٍ في القانون
(`THE_ORDER_REGISTER_IS_EMPTY_SO_THE_BROKEN_CELL_STAYS_UNRESOLVED`).

| الوديعة | الحدّ | الموقف |
|---|---|---|
| الفاتحة | كلُّ بياض | متبادل |
| الفاتحة | فراغٌ وحدَه | **غيرُ محلول** |
| آيةُ الفتح | كلُّ بياض | متبادل |
| آيةُ الفتح | فراغٌ وحدَه | متبادل |

**ورابعًا: والصالحُ للاستعمال اثنان من ثلاثة.** `usable_for_composition`
تقبل المتبادلَ والمُودَعَ ترتيبُه وترفض غيرَ المحلول. فالقانونُ لا يشترط
التبادل، بل يشترط **أن يكون الترتيب معلومًا**: إمّا لأنّه لا يهمّ، وإمّا لأنّه
مكتوب (`WHAT_IS_REQUIRED_IS_A_KNOWN_ORDER_NOT_A_COMMUTING_ONE`).

**وخامسًا: وهذا شرطُ كلِّ نصٍّ متعدّد الأسطر.** الكسرُ المقيسُ علّتُه سطرٌ
جديدٌ يُسقِطه الطَّيُّ ولا يأكله الحدّ. وكلُّ مدوَّنةٍ قرآنيّةٍ متعدّدةُ
الأسطر بالضرورة، فهذا الموقفُ حيٌّ فيها لا نظريّ؛ ولا يُقاس ههنا نصٌّ غيرُ
الوديعتَين، لأنّ التصنيفَ يُقاس ولا يُعمَّم
(`THE_TABLE_IS_MEASURED_ON_TWO_DEPOSITS_AND_NOT_GENERALIZED`).

ولا سلطةَ لهذه الوحدة: لا ولادةَ، ولا حكمَ ولادةٍ، ولا تجميدَ `E0`، ولا
تستورد من `kernel/` شيئًا، ولا فيها اسمُ ماركوف ولا انتروبيا.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from functools import cache
from typing import Final

from alghanem.arabic.carrier_projection_deposit import (
    THE_DEPOSITS_PROJECTED,
    WordBoundary,
)
from alghanem.arabic.fatiha_source_text import FATIHA_SOURCE_ID
from alghanem.arabic.projection_identity_certificate import (
    the_fold_and_the_boundary_commute_on,
)

__all__ = [
    "A_FAILURE_TO_COMMUTE_DOES_NOT_ITSELF_DEPOSIT_AN_ORDER",
    "COMPOSITION_ORDER_NAMED_RESIDUALS",
    "THE_DEFERRED_ORDERING_ALGEBRA_IS_DEPOSITED_HERE_NOT_ASSUMED",
    "THE_ORDER_REGISTER",
    "THE_ORDER_REGISTER_IS_EMPTY_SO_THE_BROKEN_CELL_STAYS_UNRESOLVED",
    "THE_TABLE_IS_MEASURED_ON_TWO_DEPOSITS_AND_NOT_GENERALIZED",
    "WHAT_IS_REQUIRED_IS_A_KNOWN_ORDER_NOT_A_COMMUTING_ONE",
    "CompositionOrderError",
    "CompositionStanding",
    "DepositedOrder",
    "LegalSide",
    "OrderFinding",
    "classify_composition",
    "the_composition_table",
    "usable_for_composition",
]


class CompositionOrderError(ValueError):
    """رفضٌ عند التصنيف: تركيبٌ خارج النطاق، أو ترتيبٌ بلا سندٍ مكتوب."""


class CompositionStanding(Enum):
    """مواقفُ التركيب الثلاثة؛ ولا رابعَ، ولا يُحمَل ثالثُها على ثانيها."""

    COMMUTES = "متبادل"
    ORDER_REQUIRED = "مشروطُ-ترتيب"
    UNRESOLVED = "غيرُ-محلول"


class LegalSide(Enum):
    """أيُّ الطرفَين هو القانونيُّ حين لا يتبادلان؛ يُودَع ولا يُستنتَج."""

    BOUNDARY_THEN_FOLD = "الحدُّ-ثمّ-الطَّيّ"
    FOLD_THEN_BOUNDARY = "الطَّيُّ-ثمّ-الحدّ"


# --- البقايا المسمّاة ------------------------------------------------------

THE_DEFERRED_ORDERING_ALGEBRA_IS_DEPOSITED_HERE_NOT_ASSUMED: Final[str] = (
    "THE_DEFERRED_ORDERING_ALGEBRA_IS_DEPOSITED_HERE_NOT_ASSUMED: أجّلت شهادةُ "
    "الهُويّة جبرَ الترتيب صراحةً وأصدرت رفضَ الالتباس وحدَه؛ وههنا يُودَع "
    "الجبرُ تصنيفًا موسومًا بثلاثة مواقف، فلا يبقى كلُّ ما لا يتبادل مرفوضًا "
    "رفضًا واحدًا لا تمييزَ فيه"
)

A_FAILURE_TO_COMMUTE_DOES_NOT_ITSELF_DEPOSIT_AN_ORDER: Final[str] = (
    "A_FAILURE_TO_COMMUTE_DOES_NOT_ITSELF_DEPOSIT_AN_ORDER: انكسارُ التبادل "
    "يُظهِر الحاجةَ إلى ترتيبٍ ولا يُنشئه؛ فلا يُرفَع تركيبٌ إلى مشروط الترتيب "
    "إلّا بوديعةٍ مكتوبةٍ تقول أيُّ الطرفَين قانونيٌّ ولِمَ، وإلّا بقي غيرَ "
    "محلول"
)

THE_ORDER_REGISTER_IS_EMPTY_SO_THE_BROKEN_CELL_STAYS_UNRESOLVED: Final[str] = (
    "THE_ORDER_REGISTER_IS_EMPTY_SO_THE_BROKEN_CELL_STAYS_UNRESOLVED: الخليّةُ "
    "المكسورةُ الوحيدةُ — الفاتحةُ بحدِّ الفراغ وحدَه — غيرُ محلولةٍ لا مشروطةَ "
    "ترتيب، لأنّ سجلَّ التراتيب فارغٌ؛ وهذا خبرٌ عن وديعتنا لا عن اللغة، "
    "وانتقالُها غدًا لا يحتاج تعديلًا في القانون"
)

WHAT_IS_REQUIRED_IS_A_KNOWN_ORDER_NOT_A_COMMUTING_ONE: Final[str] = (
    "WHAT_IS_REQUIRED_IS_A_KNOWN_ORDER_NOT_A_COMMUTING_ONE: الصالحُ للاستعمال "
    "ما كان ترتيبُه معلومًا: إمّا لأنّه لا يهمّ فيتبادل، وإمّا لأنّه مكتوبٌ "
    "فيُودَع؛ والمرفوضُ التباسُ الترتيب لا اختلافُ الطرفَين في ذاته"
)

THE_TABLE_IS_MEASURED_ON_TWO_DEPOSITS_AND_NOT_GENERALIZED: Final[str] = (
    "THE_TABLE_IS_MEASURED_ON_TWO_DEPOSITS_AND_NOT_GENERALIZED: التصنيفُ يُقاس "
    "على الوديعتَين بالحدَّين ولا يُعمَّم على نصٍّ لم يُقَس؛ وعلّةُ الكسر — سطرٌ "
    "يُسقِطه الطَّيُّ ولا يأكله الحدُّ — حيّةٌ في كلّ نصٍّ متعدّد الأسطر، "
    "فيُصنَّف كلُّ نصٍّ بنفسه قبل أن يُبنى عليه"
)

COMPOSITION_ORDER_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "THE_DEFERRED_ORDERING_ALGEBRA_IS_DEPOSITED_HERE_NOT_ASSUMED": (
        THE_DEFERRED_ORDERING_ALGEBRA_IS_DEPOSITED_HERE_NOT_ASSUMED
    ),
    "A_FAILURE_TO_COMMUTE_DOES_NOT_ITSELF_DEPOSIT_AN_ORDER": (
        A_FAILURE_TO_COMMUTE_DOES_NOT_ITSELF_DEPOSIT_AN_ORDER
    ),
    "THE_ORDER_REGISTER_IS_EMPTY_SO_THE_BROKEN_CELL_STAYS_UNRESOLVED": (
        THE_ORDER_REGISTER_IS_EMPTY_SO_THE_BROKEN_CELL_STAYS_UNRESOLVED
    ),
    "WHAT_IS_REQUIRED_IS_A_KNOWN_ORDER_NOT_A_COMMUTING_ONE": (
        WHAT_IS_REQUIRED_IS_A_KNOWN_ORDER_NOT_A_COMMUTING_ONE
    ),
    "THE_TABLE_IS_MEASURED_ON_TWO_DEPOSITS_AND_NOT_GENERALIZED": (
        THE_TABLE_IS_MEASURED_ON_TWO_DEPOSITS_AND_NOT_GENERALIZED
    ),
}


# --- سجلُّ التراتيب المُودَعة ------------------------------------------------


@dataclass(frozen=True)
class DepositedOrder:
    """ترتيبٌ قانونيٌّ مُودَعٌ لتركيبٍ لا يتبادل: أيُّ طرفٍ، وبأيّ سند."""

    source_identity: str
    boundary_rule: WordBoundary
    legal_side: LegalSide
    ground: str

    def __post_init__(self) -> None:
        if self.source_identity not in THE_DEPOSITS_PROJECTED:
            raise CompositionOrderError(
                f"ترتيبٌ لوديعةٍ خارج النطاق: {self.source_identity!r}."
            )
        if not self.ground.strip():
            raise CompositionOrderError("ترتيبٌ بلا سندٍ مكتوبٍ لا يُودَع.")


THE_ORDER_REGISTER: Final[tuple[DepositedOrder, ...]] = ()
"""سجلُّ التراتيب المُودَعة، وهو **فارغٌ** ههنا؛ فلا تركيبَ مشروطَ ترتيبٍ بعدُ."""


def _deposited_order_for(
    source_id: str, boundary: WordBoundary
) -> DepositedOrder | None:
    for order in THE_ORDER_REGISTER:
        if order.source_identity == source_id and order.boundary_rule is boundary:
            return order
    return None


# --- التصنيف --------------------------------------------------------------


@dataclass(frozen=True)
class OrderFinding:
    """تصنيفُ تركيبٍ موسومًا بموقفه وسندِه، وبطرفه القانونيِّ إن وُجد."""

    source_identity: str
    boundary_rule: WordBoundary
    standing: CompositionStanding
    ground: str
    legal_side: LegalSide | None = None

    def __post_init__(self) -> None:
        if not self.ground.strip():
            raise CompositionOrderError("تصنيفٌ بلا سندٍ مكتوبٍ لا يُصدَر.")
        if (self.legal_side is None) is (
            self.standing is CompositionStanding.ORDER_REQUIRED
        ):
            raise CompositionOrderError(
                "الطرفُ القانونيُّ يلزم مشروطَ الترتيب وحدَه ويُمنَع على سواه."
            )

    @property
    def is_usable(self) -> bool:
        """أصالحٌ للاستعمال؟ متبادلٌ أو مُودَعُ الترتيب، لا غيرُ المحلول."""

        return self.standing is not CompositionStanding.UNRESOLVED


@cache
def classify_composition(source_id: str, boundary: WordBoundary) -> OrderFinding:
    """تصنيفُ تركيبِ الطَّيّ والحدّ على وديعةٍ، مقيسًا ثمّ مقروءًا من السجلّ."""

    if source_id not in THE_DEPOSITS_PROJECTED:
        raise CompositionOrderError(f"لا تصنيفَ لوديعةٍ خارج النطاق: {source_id!r}.")
    if the_fold_and_the_boundary_commute_on(source_id, boundary):
        return OrderFinding(
            source_identity=source_id,
            boundary_rule=boundary,
            standing=CompositionStanding.COMMUTES,
            ground=WHAT_IS_REQUIRED_IS_A_KNOWN_ORDER_NOT_A_COMMUTING_ONE,
        )
    order = _deposited_order_for(source_id, boundary)
    if order is None:
        return OrderFinding(
            source_identity=source_id,
            boundary_rule=boundary,
            standing=CompositionStanding.UNRESOLVED,
            ground=A_FAILURE_TO_COMMUTE_DOES_NOT_ITSELF_DEPOSIT_AN_ORDER,
        )
    return OrderFinding(
        source_identity=source_id,
        boundary_rule=boundary,
        standing=CompositionStanding.ORDER_REQUIRED,
        ground=order.ground,
        legal_side=order.legal_side,
    )


@cache
def the_composition_table() -> tuple[OrderFinding, ...]:
    """جدولُ التصنيف على الوديعتَين بالحدَّين، مشتقًّا عند القراءة."""

    return tuple(
        classify_composition(source_id, boundary)
        for source_id in THE_DEPOSITS_PROJECTED
        for boundary in WordBoundary
    )


def usable_for_composition(source_id: str, boundary: WordBoundary) -> bool:
    """أيُبنى على هذا التركيب؟ نعم إن عُلِم ترتيبُه، ولا إن التبس."""

    return classify_composition(source_id, boundary).is_usable


# --- حرّاسُ الاستيراد ------------------------------------------------------


def _assert_no_authority_field() -> None:
    """حارسُ استيراد: لا حقلَ سلطةٍ في تصنيفٍ لا سلطةَ فيه."""

    forbidden = {"verdict", "licensed", "born", "frozen", "authority", "rank"}
    for holder in (OrderFinding, DepositedOrder):
        named = {field.name for field in fields(holder)}
        if named & forbidden:
            raise CompositionOrderError(
                f"حقلُ سلطةٍ في {holder.__name__}: {sorted(named & forbidden)}."
            )


def _assert_the_three_standings_are_distinct() -> None:
    """حارسُ استيراد: المواقفُ ثلاثةٌ متمايزةُ القيم، ولا رابعَ لها."""

    values = {member.value for member in CompositionStanding}
    if len(values) != 3:
        raise CompositionOrderError("المواقفُ ليست ثلاثةً متمايزة.")


def _assert_the_register_is_empty_and_the_broken_cell_is_unresolved() -> None:
    """حارسُ استيراد: الكسرُ الوحيدُ غيرُ محلولٍ ما دام السجلُّ فارغًا."""

    if THE_ORDER_REGISTER:
        raise CompositionOrderError(
            "سجلُّ التراتيب ليس فارغًا، والنثرُ يقول إنّه فارغٌ على هذه البيّنة."
        )
    broken = tuple(
        finding
        for finding in the_composition_table()
        if finding.standing is not CompositionStanding.COMMUTES
    )
    expected = (FATIHA_SOURCE_ID, WordBoundary.SPACE_ONLY)
    if len(broken) != 1:
        raise CompositionOrderError(f"غيرُ المتبادل ليس واحدًا: {len(broken)}.")
    if (broken[0].source_identity, broken[0].boundary_rule) != expected:
        raise CompositionOrderError("الكسرُ في غير الموضع المنشور.")
    if broken[0].standing is not CompositionStanding.UNRESOLVED:
        raise CompositionOrderError("كسرٌ رُفِع إلى مشروط الترتيب بلا وديعة.")


def _assert_no_order_required_finding_lacks_its_legal_side() -> None:
    """حارسُ استيراد: مشروطُ الترتيب بلا طرفٍ قانونيٍّ مرفوضٌ عند البناء."""

    try:
        OrderFinding(
            source_identity=FATIHA_SOURCE_ID,
            boundary_rule=WordBoundary.SPACE_ONLY,
            standing=CompositionStanding.ORDER_REQUIRED,
            ground="سند",
        )
    except CompositionOrderError:
        return
    raise CompositionOrderError(  # pragma: no cover - الرفضُ فوقُ يمنعه
        "مشروطُ ترتيبٍ قُبِل بلا طرفٍ قانونيّ."
    )


def _assert_the_unusable_is_exactly_the_unresolved() -> None:
    """حارسُ استيراد: المرفوضُ للاستعمال هو غيرُ المحلولِ وحدَه لا كلُّ كسر."""

    for finding in the_composition_table():
        unusable = not usable_for_composition(
            finding.source_identity, finding.boundary_rule
        )
        if unusable != (finding.standing is CompositionStanding.UNRESOLVED):
            raise CompositionOrderError("الصلاحيّةُ لا تطابق الموقفَ المُصدَر.")


def _assert_every_residual_is_named_by_its_key() -> None:
    """حارسُ استيراد: كلُّ بقيّةٍ تبدأ بمفتاحها فلا تُقتَبس منزوعةَ النسبة."""

    for key, text in COMPOSITION_ORDER_NAMED_RESIDUALS.items():
        if not text.startswith(f"{key}: "):
            raise CompositionOrderError(f"بقيّةٌ لا تبدأ بمفتاحها: {key}.")


_assert_no_authority_field()
_assert_the_three_standings_are_distinct()
_assert_no_order_required_finding_lacks_its_legal_side()
_assert_the_register_is_empty_and_the_broken_cell_is_unresolved()
_assert_the_unusable_is_exactly_the_unresolved()
_assert_every_residual_is_named_by_its_key()
