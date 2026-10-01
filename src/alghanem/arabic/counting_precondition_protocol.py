"""بروتوكولُ شرط العدّ: الدالّةُ محفوظةٌ بموقعها، ومُلزِمةٌ قبل أيّ عدّ.

كانت دالّةُ التأسيس في `imla_founding_function` تُجيب سؤالَ «بأيّ حقٍّ يُعَدّ
موضعٌ من النصّ؟»، ثمّ **لا يلزم منها شيء**: تُستدعى إن شاء المستدعي، وتُهمَل
إن شاء، ويخرج العددُ في الحالين سواءً. فكانت شرطًا مُعلَنًا لا شرطًا نافذًا.
وهذه الوحدةُ تجعله نافذًا، وتفترق فيها ثلاثةٌ كانت تُقرأ واحدة::

    موقعٌ محفوظ   := مسارُ الدالّةِ وطولُها وبصمتُها، تُقرأ من القرص عند كلّ نداء
    أسبقيّةٌ نافذة := شرطُ الإمكان يُشتَقّ **قبل** أن يُستدعى العادّ، بالبناء
    إعلانٌ مُلزِم  := كلُّ عددٍ يخرج من الباب يحمل حالَه تحت الدالّة أو لا يخرج

**أوّلًا: الموقعُ محفوظٌ ومختوم.** مسارُ الدالّة مُعلَنٌ ههنا بطوله وبصمته،
ومقامُه يُشتَقّ من القرص عند كلّ نداءٍ ولا يُكتَب في حقل. فإن حُرّك موضعُها
أو حُرّر متنُها انكشف ذلك حالًا ووقف الباب، ولم يمرّ عددٌ واحد. وتحريرُ
الدالّة ليس ممنوعًا؛ إنّما هو **عملٌ مقصودٌ يُعاد ختمُه** في البوّابة الواحدة
(`EDITING_THE_FOUNDING_FUNCTION_IS_A_DELIBERATE_ACT_THAT_RESEALS_ITS_SITE`).

**وثانيًا: الأسبقيّةُ بالبناء لا بالوعد.** البابُ `count_under_the_protocol`
يأخذ العادَّ **دالّةً لا رقمًا**، فيثبِّت الموقعَ ويشتقّ شرطَ الإمكان، ثمّ
يستدعي العادَّ بعد ذلك. فلا يُنتَج رقمٌ قبل البروتوكول ولو أراد المستدعي،
وليست الأسبقيّةُ ترتيبَ سطورٍ يُوثَق به
(`AN_ORDER_ENFORCED_BY_CONSTRUCTION_IS_NOT_AN_ORDER_PROMISED_IN_PROSE`).

**وثالثًا: الإعلانُ مُلزِمٌ والترقيةُ ممنوعة.** شرطُ الإمكان **غيرُ مستوفًى
اليوم**، إذ نصفُ الدالّة الصوتيُّ موقوف. ولا يعني ذلك وقفَ العدّ في الشجرة —
ذلك شرطٌ لا يُطاق ولا يُعمَل به — بل يعني أنّ العددَ يخرج **معلَّقًا بأسماء
أنصافه غير المستوفاة**. والممنوعُ المرفوعُ خطأً أمران: عددٌ يخرج بلا إعلان
حالٍ ألبتّة، وعددٌ يُكتَب «مرخَّصًا» ونصفٌ موقوف.

**ورابعًا: إلزامُ البروتوكول غيرُ استيفاء شرطه.** هذه الوحدةُ مُلزِمةٌ اليوم،
وشرطُها غيرُ مستوفًى اليوم، ولا تناقضَ بينهما: الإلزامُ على **الإجراء**،
والاستيفاءُ على **المادّة**. فمن قرأ نفاذَ البروتوكول استيفاءً للشرط فقد
قرأ غيرَ ما كُتب (`A_BINDING_PROTOCOL_IS_NOT_A_MET_PRECONDITION`).

**وخامسًا: ولا رقمَ مُجمَّدٍ في هذه الوحدة سوى ختمِ الموقع.** لا عددَ
مستوردين، ولا نسبةَ امتثال؛ فالشجرةُ تنمو فتكذب الأرقامُ المُجمَّدةُ فيها.
والمستوردون يُقرأون من القرص شاهدًا يُنشَر، و**الاستيرادُ ليس مرورًا**: وحدةٌ
تستورد هذا البابَ وتعُدّ من غيره لم تمرّ به
(`AN_IMPORT_IS_NOT_A_PASSAGE_THROUGH_THE_DOOR`).

    ADeclaredPrecondition   != AnEnforcedPrecondition
    ABindingProcedure       != AMetCondition
    AnImportOfTheDoor       != APassageThroughIt
    AnOrderInProse          != AnOrderInConstruction

ولا سلطانَ لهذه الوحدة: لا ولادةَ، ولا رفعَ حظر، ولا فكَّ تجميد، ولا استيرادَ
من `kernel/` (`NO_PROTOCOL_HERE_LIFTS_A_BLOCK_OR_THAWS_A_FREEZE`).
"""

from __future__ import annotations

import hashlib
from collections.abc import Callable, Iterator
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Final

from .a116_bridge_licence import DeclaredMaterial, MaterialStanding
from .imla_founding_function import PossibilityCondition, possibility_condition
from .pipeline_stations import repository_root_path

__all__ = [
    "AN_IMPORT_IS_NOT_A_PASSAGE_THROUGH_THE_DOOR",
    "AN_ORDER_ENFORCED_BY_CONSTRUCTION_IS_NOT_AN_ORDER_PROMISED_IN_PROSE",
    "A_BINDING_PROTOCOL_IS_NOT_A_MET_PRECONDITION",
    "A_COUNT_WITHOUT_A_DECLARED_STANDING_IS_REFUSED_NOT_ASSUMED_LICENSED",
    "COUNTING_PROTOCOL_NAMED_RESIDUALS",
    "ClauseForce",
    "CountingProtocolError",
    "CountingStanding",
    "DeclaredCount",
    "EDITING_THE_FOUNDING_FUNCTION_IS_A_DELIBERATE_ACT_THAT_RESEALS_ITS_SITE",
    "NO_PROTOCOL_HERE_LIFTS_A_BLOCK_OR_THAWS_A_FREEZE",
    "ProtocolBinding",
    "ProtocolClause",
    "THE_FOUNDING_SITE",
    "THE_PROTOCOL_CLAUSES",
    "count_under_the_protocol",
    "importers_of_the_protocol",
    "protocol_binding",
    "require_the_protocol",
    "site_seal_renderings",
    "the_block_and_the_freeze_are_untouched",
]


class CountingProtocolError(RuntimeError):
    """خطأُ بروتوكولٍ يُرفَع ولا يُتخطّى؛ فالبابُ يقف ولا يمرّ عددٌ واحد."""


# ---------------------------------------------------------------------------
# أوّلًا: الموقعُ المحفوظُ المختوم
# ---------------------------------------------------------------------------

THE_FOUNDING_SITE: Final[DeclaredMaterial] = DeclaredMaterial(
    key="imla_founding_function",
    relative_path="src/alghanem/arabic/imla_founding_function.py",
    declared_byte_length=23090,
    declared_sha256=(
        "4b7e62fe6daf3e11b709dffef6f3cc0255da65e28747a090bdf882e9e55f5845"
    ),
)
"""موقعُ دالّة التأسيس محفوظًا بطوله وبصمته؛ ومقامُه يُقرأ من القرص لا يُكتَب."""

THE_PROTOCOL_MODULE: Final[str] = "counting_precondition_protocol"
"""اسمُ هذه الوحدة، تُعرَف به عند قراءة مستورديها من القرص."""


def site_seal_renderings(root: Path | None = None) -> dict[str, str]:
    """جانبا ختمِ الموقع: ما قاسه القرصُ الآن، ليُصادَم بما أُعلن ههنا."""

    path = THE_FOUNDING_SITE.resolved_path(root)
    if not path.is_file():
        return {
            "المسار": "موضعٌ غائبٌ عن الشجرة",
            "الطول": "موضعٌ غائبٌ عن الشجرة",
            "البصمة": "موضعٌ غائبٌ عن الشجرة",
        }
    raw = path.read_bytes()
    return {
        "المسار": THE_FOUNDING_SITE.relative_path,
        "الطول": str(len(raw)),
        "البصمة": hashlib.sha256(raw).hexdigest(),
    }


# ---------------------------------------------------------------------------
# ثانيًا: بنودُ البروتوكول وقوّةُ كلِّ بند
# ---------------------------------------------------------------------------


class ClauseForce(Enum):
    """قوّةُ البند: مُلزِمٌ يُرفَع خرقُه خطأً، أو شاهدٌ يُنشَر ولا يمنع."""

    BINDING = "مُلزِم"
    WITNESS = "شاهدٌ لا يمنع"


@dataclass(frozen=True, slots=True)
class ProtocolClause:
    """بندٌ واحدٌ برتبته وسؤاله وقوّته؛ والرتبةُ ترتيبُ نفاذٍ لا ترتيبُ عرض."""

    ordinal: int
    name: str
    question: str
    force: ClauseForce

    def __post_init__(self) -> None:
        if self.ordinal < 1:
            raise CountingProtocolError("بندٌ برتبةٍ دون الواحد لا يُسَنّ.")
        if not self.name.strip() or not self.question.strip():
            raise CountingProtocolError("بندٌ بلا اسمٍ أو بلا سؤالٍ لا يُقاس.")


THE_PROTOCOL_CLAUSES: Final[tuple[ProtocolClause, ...]] = (
    ProtocolClause(
        ordinal=1,
        name="الموقع",
        question="أمسارُ الدالّة حاضرٌ مطابقٌ لطوله وبصمته؟",
        force=ClauseForce.BINDING,
    ),
    ProtocolClause(
        ordinal=2,
        name="الأسبقيّة",
        question="أاشتُقَّ شرطُ الإمكان قبل أن يُستدعى العادّ؟",
        force=ClauseForce.BINDING,
    ),
    ProtocolClause(
        ordinal=3,
        name="الإعلان",
        question="أيحمل العددُ حالَه تحت الدالّة؟",
        force=ClauseForce.BINDING,
    ),
    ProtocolClause(
        ordinal=4,
        name="التسمية",
        question="أيحمل العددُ المعلَّقُ أسماءَ أنصافه غير المستوفاة؟",
        force=ClauseForce.BINDING,
    ),
    ProtocolClause(
        ordinal=5,
        name="منعُ الترقية",
        question="أخلا العددُ المرخَّصُ من كلّ نصفٍ موقوف؟",
        force=ClauseForce.BINDING,
    ),
    ProtocolClause(
        ordinal=6,
        name="المستوردون",
        question="كم وحدةً تستورد هذا الباب؟",
        force=ClauseForce.WITNESS,
    ),
)
"""بنودُ البروتوكول؛ خمسةٌ مُلزِمةٌ وسادسٌ شاهدٌ يُنشَر عددُه ولا يمنع."""


# ---------------------------------------------------------------------------
# ثالثًا: نفاذُ البروتوكول
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class ProtocolBinding:
    """قراءةُ نفاذٍ: مقامُ الموقع، وحالُ شرط الإمكان، وأنصافُه غير المستوفاة.

    و`holds` نفاذُ **الإجراء** لا استيفاءُ **الشرط**؛ فالأوّلُ قائمٌ اليوم
    والثاني غيرُ مستوفًى، ولا يُقرأ أحدُهما بالآخر
    (`A_BINDING_PROTOCOL_IS_NOT_A_MET_PRECONDITION`).
    """

    site_standing: MaterialStanding
    precondition_is_met: bool
    unmet_halves: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.precondition_is_met and self.unmet_halves:
            raise CountingProtocolError(
                "شرطٌ مستوفًى وفيه نصفٌ غيرُ مستوفًى؛ قراءةٌ متناقضة."
            )
        if not self.precondition_is_met and not self.unmet_halves:
            raise CountingProtocolError("شرطٌ غيرُ مستوفًى بلا تسميةِ ما لم يُستوفَ لا يُنشَر.")

    @property
    def holds(self) -> bool:
        """أينفُذ البروتوكول؟ ونفاذُه مقامُ موقعه، لا استيفاءُ شرطه."""

        return self.site_standing is MaterialStanding.DEPOSITED_AND_SEALED

    @property
    def binding_clauses(self) -> tuple[ProtocolClause, ...]:
        """البنودُ المُلزِمةُ وحدَها؛ والشاهدُ يُنشَر ولا يُحسَب فيها."""

        return tuple(
            clause
            for clause in THE_PROTOCOL_CLAUSES
            if clause.force is ClauseForce.BINDING
        )


def protocol_binding(root: Path | None = None) -> ProtocolBinding:
    """قراءةُ النفاذ **ولا تُرفَع منها خطأ**، ليُفحَص الموقعُ المكسورُ ويُسمّى."""

    condition: PossibilityCondition = possibility_condition()
    return ProtocolBinding(
        site_standing=THE_FOUNDING_SITE.standing(root),
        precondition_is_met=condition.is_met,
        unmet_halves=condition.unmet_halves,
    )


def require_the_protocol(root: Path | None = None) -> ProtocolBinding:
    """الإلزامُ بعينه: يُرفَع الخطأُ ويقف الباب، ولا يُتخطّى بوسمٍ ولا ببيئة."""

    binding = protocol_binding(root)
    if binding.holds:
        return binding
    raise CountingProtocolError(
        "بروتوكولُ شرط العدّ لا ينفُذ: موقعُ دالّة التأسيس "
        f"«{THE_FOUNDING_SITE.relative_path}» مقامُه {binding.site_standing.value}. "
        "ولا يمرّ عددٌ من هذا الباب حتّى يُعاد ختمُ الموقع في "
        "tools/regen_all.py وفي THE_FOUNDING_SITE: "
        f"{EDITING_THE_FOUNDING_FUNCTION_IS_A_DELIBERATE_ACT_THAT_RESEALS_ITS_SITE}"
    )


# ---------------------------------------------------------------------------
# رابعًا: العددُ المُعلَنُ حالُه
# ---------------------------------------------------------------------------


class CountingStanding(Enum):
    """حالُ العدّ تحت الدالّة؛ ويُشتَقّ من شرط الإمكان ولا يُكتَب في حقل."""

    LICENSED_BY_A_MET_PRECONDITION = "مرخَّصٌ بشرطٍ مستوفًى"
    CONDITIONAL_ON_A_NAMED_SUSPENSION = "معلَّقٌ بأنصافٍ مُسمّاة"


@dataclass(frozen=True, slots=True)
class DeclaredCount:
    """عددٌ يحمل حالَه تحت الدالّة؛ وعددٌ بلا حالٍ لا يُبنى أصلًا.

    والقيمةُ محمولةٌ صحيحةَ الحساب كما قاسها عادُّها؛ وليس الإعلانُ تشكيكًا
    في حسابها، بل تسميةً للقسمة التي حُسبت عليها
    (`A_COUNT_WITHOUT_A_DECLARED_STANDING_IS_REFUSED_NOT_ASSUMED_LICENSED`).
    """

    name: str
    value: int
    standing: CountingStanding
    unmet_halves: tuple[str, ...]
    site_standing: MaterialStanding

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise CountingProtocolError("عددٌ بلا اسمٍ لا يُعلَن.")
        if self.value < 0:
            raise CountingProtocolError("عددٌ سالبٌ لا يُعلَن عدًّا.")
        if self.site_standing is not MaterialStanding.DEPOSITED_AND_SEALED:
            raise CountingProtocolError(
                "عددٌ يخرج وموقعُ دالّة التأسيس غيرُ مختوم؛ البابُ واقف."
            )
        if (
            self.standing is CountingStanding.CONDITIONAL_ON_A_NAMED_SUSPENSION
            and not self.unmet_halves
        ):
            raise CountingProtocolError(
                "عددٌ معلَّقٌ بلا تسميةِ أنصافه غير المستوفاة لا يُنشَر."
            )
        if (
            self.standing is CountingStanding.LICENSED_BY_A_MET_PRECONDITION
            and self.unmet_halves
        ):
            raise CountingProtocolError("عددٌ يُكتَب مرخَّصًا ونصفٌ موقوف؛ ترقيةٌ ممنوعة.")

    @property
    def is_licensed(self) -> bool:
        """أمرخَّصٌ هذا العدّ؟ ويُقرأ من حاله لا من صحّة حسابه."""

        return self.standing is CountingStanding.LICENSED_BY_A_MET_PRECONDITION


def count_under_the_protocol(
    name: str,
    count: Callable[[], int],
    root: Path | None = None,
) -> DeclaredCount:
    """البابُ الوحيد: يُثبَّت الموقعُ ويُشتَقّ الشرطُ **ثمّ** يُستدعى العادّ.

    والعادُّ يُؤخَذ دالّةً لا رقمًا عمدًا: فلو أُخِذ رقمًا لكان قد حُسب قبل
    البروتوكول، ولصار البابُ ختمًا يُلصَق على عددٍ سابقٍ لا شرطًا سابقًا عليه
    (`AN_ORDER_ENFORCED_BY_CONSTRUCTION_IS_NOT_AN_ORDER_PROMISED_IN_PROSE`).
    """

    if not callable(count):
        raise CountingProtocolError(
            "العادُّ يُؤخَذ دالّةً تُستدعى بعد البروتوكول، لا رقمًا سبقه."
        )
    binding = require_the_protocol(root)
    value = count()
    if not isinstance(value, int) or isinstance(value, bool):
        raise CountingProtocolError("عادٌّ لا يُخرِج عددًا صحيحًا لا يمرّ.")
    standing = (
        CountingStanding.LICENSED_BY_A_MET_PRECONDITION
        if binding.precondition_is_met
        else CountingStanding.CONDITIONAL_ON_A_NAMED_SUSPENSION
    )
    return DeclaredCount(
        name=name,
        value=value,
        standing=standing,
        unmet_halves=binding.unmet_halves,
        site_standing=binding.site_standing,
    )


# ---------------------------------------------------------------------------
# خامسًا: شاهدُ المستوردين، يُقرأ من القرص ولا يُجمَّد
# ---------------------------------------------------------------------------


def _source_modules(root: Path | None = None) -> Iterator[Path]:
    package = (root or repository_root_path()) / "src" / "alghanem"
    yield from sorted(package.rglob("*.py"))


def importers_of_the_protocol(root: Path | None = None) -> tuple[str, ...]:
    """الوحداتُ التي تذكر هذا الباب، مقروءةً من القرص عند كلّ نداء.

    وهذا **شاهدٌ لا مقياسُ امتثال**: ذِكرُ الباب ليس مرورًا به، ووحدةٌ تستورده
    ثمّ تعُدّ من غيره لم تمرّ (`AN_IMPORT_IS_NOT_A_PASSAGE_THROUGH_THE_DOOR`).
    """

    found: list[str] = []
    for path in _source_modules(root):
        if path.stem == THE_PROTOCOL_MODULE:
            continue
        if THE_PROTOCOL_MODULE in path.read_text(encoding="utf-8"):
            found.append(path.stem)
    return tuple(found)


# ---------------------------------------------------------------------------
# البقايا المُسمّاة
# ---------------------------------------------------------------------------

A_BINDING_PROTOCOL_IS_NOT_A_MET_PRECONDITION: Final[str] = (
    "A_BINDING_PROTOCOL_IS_NOT_A_MET_PRECONDITION: نفاذُ الإجراء غيرُ استيفاء "
    "المادّة؛ فالبروتوكولُ مُلزِمٌ اليوم وشرطُه غيرُ مستوفًى اليوم، ولا يُقرأ "
    "نفاذُه استيفاءً."
)

AN_ORDER_ENFORCED_BY_CONSTRUCTION_IS_NOT_AN_ORDER_PROMISED_IN_PROSE: Final[str] = (
    "AN_ORDER_ENFORCED_BY_CONSTRUCTION_IS_NOT_AN_ORDER_PROMISED_IN_PROSE: العادُّ "
    "يُؤخَذ دالّةً فيُستدعى بعد الشرط؛ ولو أُخِذ رقمًا لكان البابُ ختمًا على "
    "عددٍ سابقٍ لا شرطًا سابقًا عليه."
)

A_COUNT_WITHOUT_A_DECLARED_STANDING_IS_REFUSED_NOT_ASSUMED_LICENSED: Final[str] = (
    "A_COUNT_WITHOUT_A_DECLARED_STANDING_IS_REFUSED_NOT_ASSUMED_LICENSED: عددٌ "
    "بلا إعلانِ حالِه تحت الدالّة يُرَدّ؛ ولا يُفترَض مرخَّصًا بسكوته."
)

AN_IMPORT_IS_NOT_A_PASSAGE_THROUGH_THE_DOOR: Final[str] = (
    "AN_IMPORT_IS_NOT_A_PASSAGE_THROUGH_THE_DOOR: ذِكرُ هذا الباب في وحدةٍ شاهدٌ "
    "يُنشَر، وليس شهادةً أنّ عددَها مرّ به؛ فلا يُقرأ عددُ المستوردين امتثالًا."
)

EDITING_THE_FOUNDING_FUNCTION_IS_A_DELIBERATE_ACT_THAT_RESEALS_ITS_SITE: Final[str] = (
    "EDITING_THE_FOUNDING_FUNCTION_IS_A_DELIBERATE_ACT_THAT_RESEALS_ITS_SITE: "
    "تحريرُ الدالّة مباحٌ ويقف له البابُ حتّى يُعاد ختمُ الموقع؛ فالختمُ يمنع "
    "الانزياحَ الصامت ولا يمنع العمل."
)

NO_PROTOCOL_HERE_LIFTS_A_BLOCK_OR_THAWS_A_FREEZE: Final[str] = (
    "NO_PROTOCOL_HERE_LIFTS_A_BLOCK_OR_THAWS_A_FREEZE: لا ولادةَ ههنا، ولا حكمَ "
    "ولادة، ولا رفعَ حظرٍ، ولا فكَّ تجميد، ولا استيرادَ من kernel/."
)

COUNTING_PROTOCOL_NAMED_RESIDUALS: Final[tuple[str, ...]] = (
    A_BINDING_PROTOCOL_IS_NOT_A_MET_PRECONDITION,
    AN_ORDER_ENFORCED_BY_CONSTRUCTION_IS_NOT_AN_ORDER_PROMISED_IN_PROSE,
    A_COUNT_WITHOUT_A_DECLARED_STANDING_IS_REFUSED_NOT_ASSUMED_LICENSED,
    AN_IMPORT_IS_NOT_A_PASSAGE_THROUGH_THE_DOOR,
    EDITING_THE_FOUNDING_FUNCTION_IS_A_DELIBERATE_ACT_THAT_RESEALS_ITS_SITE,
    NO_PROTOCOL_HERE_LIFTS_A_BLOCK_OR_THAWS_A_FREEZE,
)
"""البقايا بأسمائها؛ وكلُّ واحدةٍ منها فرقٌ يُحتَجّ به لا شعارٌ يُردَّد."""


def the_block_and_the_freeze_are_untouched() -> str:
    """تصريحُ الخمول: لا تمسّ هذه الوحدةُ حظرًا ولا تجميدًا ولا ولادة."""

    return NO_PROTOCOL_HERE_LIFTS_A_BLOCK_OR_THAWS_A_FREEZE


# ---------------------------------------------------------------------------
# حرّاسُ الاستيراد
# ---------------------------------------------------------------------------


def _assert_the_clauses_are_ordered_and_named() -> None:
    """رتبُ البنود متتاليةٌ من الواحد، وأسماؤها متمايزة، وفيها مُلزِمٌ خمسة."""

    ordinals = [clause.ordinal for clause in THE_PROTOCOL_CLAUSES]
    if ordinals != list(range(1, len(THE_PROTOCOL_CLAUSES) + 1)):
        raise CountingProtocolError("رتبُ البنود غيرُ متتاليةٍ من الواحد.")
    names = {clause.name for clause in THE_PROTOCOL_CLAUSES}
    if len(names) != len(THE_PROTOCOL_CLAUSES):
        raise CountingProtocolError("بندان باسمٍ واحدٍ لا يفترقان عند الاحتجاج.")
    binding = [
        clause for clause in THE_PROTOCOL_CLAUSES if clause.force is ClauseForce.BINDING
    ]
    if not binding:
        raise CountingProtocolError("بروتوكولٌ بلا بندٍ مُلزِمٍ ليس بروتوكولًا.")


def _assert_the_site_is_sealed_at_import() -> None:
    """الإلزامُ من أوّل نفَس: استيرادُ هذه الوحدة نفسُه يقف على ختم الموقع."""

    require_the_protocol()


_assert_the_clauses_are_ordered_and_named()
_assert_the_site_is_sealed_at_import()
