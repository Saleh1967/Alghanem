"""التأكّدُ من الإنجازات المُعلَنة في `README.md` اشتقاقًا، لا قراءةً بالعين.

هذه **المرحلة الخامسة عشرة من الطور الثاني** لـ AIM.1، وهي إخضاعُ آخرِ مستندٍ
مُعلِنٍ في المستودع لما أُخضِعت له وثيقتا الدستور والغايات. صار في الشجرة دفترٌ
يقرأ `docs/CONSTITUTION.md`، وآخرُ يقرأ `docs/AIMS.md`، وثالثٌ يقابل مراحل §٧
بوحداتها؛ وبقي `README.md` — وهو الواجهةُ التي تُقرأ أوّلًا وتُعلن فيها
الإنجازات — **لا يقرؤه شيء**. فكلُّ ما فيه مقبولٌ لأنّه مكتوب::

    AnnouncedAchievement != DerivedAchievement
    ModuleNamedInProse   != ModuleThatImports
    TestFileExists       != AchievementWitnessed
    Readme               != Authority

**المصدر التصميميّ المباشر، مُستشهَدًا به لا مُعادًا اشتقاقه.** شكلُ «الوثيقة
تُعلن، والقارئ لا يقبل إلا من مفردةٍ مغلقة يملكها هو، والمخالفة تُرفَض عند
الإنشاء» مأخوذٌ من سؤال التدقيق المفتوح
`DeclaredVersusDerivedRecurrenceNotExplained` بوصفه **مصدرًا مباشرًا** (إلزام §٥
من `docs/AIMS.md`)، لا بوصفه بديهةً تُعاد هنا صامتةً. وذلك السؤال مرصودٌ غير
مفسَّر، فلا يُستحدَث له اسمٌ عامّ ولا صنفُ أساسٍ مشترك يوحّد الشكل بين القرّاء
السبعة؛ يُستعمل في موضعه ويُنسَب إلى سؤاله.

**ما يُقرَأ مطالبةً بالإنجاز شكلٌ واحد لا تقديرُ معنى.** المستودع يكتب مطالبةَ
البوّابة بوحدتها بشكلٍ واحدٍ ثابت: معرّفُ بوّابةٍ، ثم نثرٌ لا يحمل علامةَ ترميزٍ
ولا قوسًا، ثم مسارُ وحدةٍ بين قوسين في علامة ترميز. فهذا وحده يُقرَأ **مطالبةً**
(`AchievementClaim`)، وما عداه من ذِكرِ معرّفٍ يُقرَأ **ذِكرًا** لا مطالبة. ولو
قُدِّرت المطالبةُ من قرب المسار للمعرّف لأُلحِقت بـ`G0` وحدةُ تدخّلٍ سطحيّ
ذكرها النثرُ بعدها بعشرات الأسطر، ولأُلحِقت بـ`G0.F.1` وحدةُ هويةِ محتوًى
يذكرها سياقٌ آخر. وهذا الحدُّ مُسمًّى في `NAMED_RESIDUALS` لا مطويّ.

**الوجودُ في الشجرة لا يكفي، والاستيرادُ هو الاشتقاق.** مطابقةُ نصِّ مسارٍ
بملفٍّ قائم تُثبت أن اسمًا كُتب مرّتين، لا أن وحدةً تقوم. فالمطالبةُ هنا
تُستورَد استيرادًا فعليًّا (`importlib`)، ثم تُقابَل الرموزُ التي سمّاها النثرُ
في مدى المطالبة بما تحمله الوحدةُ فعلًا. ومطالبةٌ لا يقوم لها رمزٌ واحدٌ في
وحدتها نثرٌ غيرُ مربوطٍ بالشجرة، فتُرفَض باسمها وموضع سطرها.

**والحضورُ صفةً ليس تأليفًا**: رمزٌ مستورَدٌ إلى الوحدة يحمله `getattr` كما
يحمل ما عُرِّف فيها، فالمقروءُ «قائمٌ من هذه الوحدة» لا «مُعرَّفٌ فيها»، وهو
مُسمًّى في `NAMED_RESIDUALS`.

**المقابلةُ ثلاثيةٌ والرفضُ في جهةٍ واحدة، وذلك مُشتَقٌّ لا مُجامَلة.**
معرّفاتُ البوّابات تُقرأ من المستندات الثلاثة خارج علامات الترميز. فمعرّفٌ
يُطالِب بوحدةٍ في `README.md` ولا يُسمّيه الدستور **يُرفَض عند الإنشاء**: إنجازٌ
مُعلَنٌ بلا قانونٍ يحكمه. أمّا معرّفٌ يُذكَر في `README.md` بلا مطالبةٍ ولا
يُسمّيه الدستور فيُسجَّل بحالٍ مُسمّاة `ANNOUNCED_IN_README_ONLY` ولا يُرفَع إلى
الرفض: رفعُه كان يُلزِم هذا الدفترَ بتعديل صفٍّ في الدستور، وهو ما لا سلطةَ له
عليه. وهذه الحالُ ليست فارغةً اليوم: `P0.1` مُعلَنٌ في `README.md` ولا يَرِد في
`docs/CONSTITUTION.md` أصلًا، وهو ما كشفته هذه القراءةُ لا نثرٌ على هامشها.
ومعرّفٌ يُصدِّر قسمًا في الدستور ولا يُذكَر في `README.md` يُسجَّل
`DECLARED_IN_CONSTITUTION_ONLY`؛ فالحالاتُ ثلاثٌ لا حالان، والصمتُ ليس إحداها.

**الشاهدُ مُشتَقٌّ بعُرف الشجرة نفسِه، لا بسجلٍّ مكتوب.** `tests/` يقابل `src/`
بعُرفٍ واحد: `src/alghanem/X/Y.py` شاهدُه `tests/X/test_Y.py`. فيُشتَقّ موضعُ
الشاهد من مسار الوحدة، ثم يُقرَأ الملفُّ ويُشتَقّ أنه يحمل دوالَّ اختبارٍ فعلًا.
**وثلاثةُ أحوالٍ لا حالان**، اقتداءً بـ`step_reproducers`: شاهدٌ مُشتَقٌّ قائم،
أو شاهدٌ مُسجَّلٌ في موضعٍ آخر، أو **غيرُ مُسجَّلٍ أصلًا** — والثالثةُ ليست
رفضًا، لأن هذا الدفتر مكتوبُ العُرف لا مُستقصي الشجرة كلِّها.

**و«الشاهد يُجمَع» ليس «الشاهد يفحص هذا الإنجاز»**: وجودُ دوالِّ اختبارٍ في
الملفّ المُشتَقّ لا يشتقّ أنها تفحص ما يصفه النثر، وهو مُسمًّى في
`NAMED_RESIDUALS` لا مطويّ.

**والفجوتان الظاهرتان تُسجَّلان ولا تبقيان صمتًا.** سكربتاتُ `examples/` التي لا
يستدعيها اختبارٌ تُحصى بحالها `DECLARED_NOT_REPRODUCED`، فتُقرَأ «مُعلَنةٌ غيرُ
مُعادةِ الإنتاج» لا «مُثبَتة». والاختباراتُ المتخطّاة تُحصى بجنسَين مُصرَّح
بهما — تخطٍّ مشروطٌ بمُدخَلٍ غير مودَع، وتخطٍّ لحالةٍ لا تنطبق بالبناء — وما خرج
عن الجنسين يُرفَض باسمه وموضعه؛ فالتخطّي الذي لا يُسمّى جنسُه يُعَدّ نجاحًا في
العدّ العامّ وهو ليس نجاحًا.

**التعداد خاصّيةٌ تُحسَب لا حقلٌ يُكتَب** (§٤): لا حقلَ عددٍ في أيّ صنفٍ هنا.

**لا مؤشرَ هنا**: المؤشر ربطُ عددٍ مُشتَقّ **بغايةٍ بعينها**، وهذا الدفتر يربط
بوّابةً مُعلَنة بوحدةِ شيفرةٍ وشاهدٍ؛ فلا يستورد `AimId` ولا أيًّا من الدفاتر،
ولا يُحصي غايةً، ويُفحَص ذلك آليًّا.

**خمولٌ سلطويّ**: `AchievementLedger != BirthVerdict`؛ لا تُصدر هذه الوحدة
ولادةً ولا حكمًا ولا تجميدًا ولا `E0`، ولا تُصدر بلوغَ غايةٍ ولا تُرقّيه، ولا
تُعدّل حالةَ صفٍّ في الدستور، ولا تقرؤها أيّ وحدةٍ في `kernel/`. وترتيبُ الصفوف
ترتيبُ ورودها في المستندات، لا ترتيبَ أولويةٍ ولا أهمّية (§٦)، وقيامُ الدفتر
ليس بلوغَ غاية.
"""

from __future__ import annotations

import importlib
import re
from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from types import MappingProxyType
from typing import Final

from .aims import DESIGN_SOURCE_OPEN_QUESTION

README_RELATIVE_PATH: Final = "README.md"

CONSTITUTION_DOCUMENT_RELATIVE_PATH: Final = "docs/CONSTITUTION.md"

AIMS_DOCUMENT_RELATIVE_PATH: Final = "docs/AIMS.md"

SOURCE_PACKAGE_RELATIVE_PATH: Final = "src/alghanem"

TESTS_RELATIVE_PATH: Final = "tests"

EXAMPLES_RELATIVE_PATH: Final = "examples"

ACHIEVEMENT_LEDGER_AUTHORITY_NOTE: Final = (
    "قراءةٌ ومقابلةٌ فقط: لا يُنتج هذا الدفتر ولادةً ولا حكمًا ولا تجميدًا ولا "
    "`E0`، ولا يُصدر بلوغَ غايةٍ ولا يُرقّيه، ولا يُعدّل حالةَ صفٍّ في الدستور، "
    "ولا تقرؤه بوّابةٌ في النواة"
)

NO_INDICATOR_IN_THIS_ACHIEVEMENT_LEDGER_NOTE: Final = (
    "لا مؤشر هنا: المؤشر ربطُ عددٍ مُشتَقّ بغايةٍ بعينها، وهذا الدفتر يربط "
    "بوّابةً مُعلَنة بوحدةِ شيفرةٍ وشاهدٍ؛ فلا يستورد `AimId` ولا أيًّا من "
    "الدفاتر، ولا يُحصي غايةً، ويُفحَص ذلك آليًّا"
)

DESIGN_SOURCE_CITATION_NOTE: Final = (
    "شكلُ «الوثيقة تُعلن، والقارئ لا يقبل إلا من مفردةٍ مغلقة يملكها، "
    f"والمخالفة تُرفَض» مأخوذٌ من `{DESIGN_SOURCE_OPEN_QUESTION}` مصدرًا "
    "مباشرًا، لا بديهةً تُعاد هنا صامتةً"
)

CLAIMED_MODULE_MUST_IMPORT_NOTE: Final = (
    "وحدةٌ مُطالَبٌ بها في `README.md` لا تُستورَد تُرفَض ولا تُقبَل بمطابقة "
    "اسمِ مسارٍ: المطابقةُ النصّية تُثبت أن اسمًا كُتب مرّتين، لا أن وحدةً تقوم"
)

CLAIM_WITHOUT_A_RESIDENT_SYMBOL_IS_REFUSED_NOTE: Final = (
    "مطالبةٌ تُسمّي وحدةً ولا يقوم لها في تلك الوحدة رمزٌ واحد نثرٌ غيرُ مربوطٍ "
    "بالشجرة، فتُرفَض باسمها وموضع سطرها لا تُقبَل بوجود الملفّ وحده"
)

README_CLAIM_WITHOUT_A_CONSTITUTIONAL_GATE_IS_REFUSED_NOTE: Final = (
    "بوّابةٌ تُطالِب بوحدةٍ في `README.md` ولا يُسمّيها `docs/CONSTITUTION.md` "
    "تُرفَض: إنجازٌ مُعلَنٌ بلا قانونٍ يحكمه يُقرَأ لاحقًا «هكذا صرّح الدستور»"
)

UNKNOWN_SKIP_FORM_IS_REFUSED_NOTE: Final = (
    "تخطٍّ في `tests/` خارج الجنسين المُصرَّح بهما يُوقف القراءة ولا يُتخطّى: "
    "التخطّي الذي لا يُسمّى جنسُه يُعَدّ نجاحًا في العدّ العامّ وهو ليس نجاحًا"
)

CLAIM_SHAPE_IS_A_FORM_NOT_A_MEANING: Final = "CLAIM_SHAPE_IS_A_FORM_NOT_A_MEANING"

SYMBOL_PRESENCE_IS_NOT_SYMBOL_AUTHORSHIP: Final = (
    "SYMBOL_PRESENCE_IS_NOT_SYMBOL_AUTHORSHIP"
)

WITNESS_COLLECTS_IS_NOT_WITNESS_CHECKS_THIS: Final = (
    "WITNESS_COLLECTS_IS_NOT_WITNESS_CHECKS_THIS"
)

README_ONLY_GATE_IS_RECORDED_NOT_REFUSED: Final = (
    "README_ONLY_GATE_IS_RECORDED_NOT_REFUSED"
)

EXAMPLE_SCRIPT_REFERENCE_IS_NOT_EXECUTION: Final = (
    "EXAMPLE_SCRIPT_REFERENCE_IS_NOT_EXECUTION"
)

NAMED_RESIDUALS: Final[Mapping[str, str]] = MappingProxyType(
    {
        CLAIM_SHAPE_IS_A_FORM_NOT_A_MEANING: (
            "المطالبةُ مقروءةٌ بشكلٍ واحد: معرّفٌ، ثم نثرٌ بلا علامة ترميزٍ ولا "
            "قوس، ثم مسارٌ بين قوسين. فبوّابةٌ رُمِّزت فعلًا وكُتبت مطالبتُها "
            "بشكلٍ آخر تُقرَأ ذِكرًا لا مطالبة، ولا يشتقّ هذا الدفتر ذلك؛ "
            "والشكلُ اختيرَ لأنّ تقديرَ المطالبة من قُربِ المسار يُلحِق بـ`G0` "
            "وحدةَ تدخّلٍ سطحيّ وبـ`G0.F.1` وحدةَ هويةِ محتوًى، وكلاهما خطأ"
        ),
        SYMBOL_PRESENCE_IS_NOT_SYMBOL_AUTHORSHIP: (
            "قيامُ الرمز مُشتَقٌّ بالاستيراد ثم `getattr`، وهذا يحمل الرمزَ "
            "المستورَدَ إلى الوحدة كما يحمل المُعرَّفَ فيها؛ فالمقروءُ «قائمٌ "
            "من هذه الوحدة» لا «مُعرَّفٌ فيها»، وفجوةُ نسبةِ التأليف باقية"
        ),
        WITNESS_COLLECTS_IS_NOT_WITNESS_CHECKS_THIS: (
            "أن ملفّ الشاهد قائمٌ ويحمل دوالَّ اختبارٍ مُشتَقٌّ، وأنّ تلك "
            "الدوالَّ تفحص ما يصفه نثرُ `README.md` ليس مُشتَقًّا من شيءٍ هنا: "
            "شاهدٌ كاملُ الشكل يفحص غيرَ ما وُصف يجتاز هذه المقابلة كاملةً"
        ),
        README_ONLY_GATE_IS_RECORDED_NOT_REFUSED: (
            "بوّابةٌ تُذكَر في `README.md` بلا مطالبةٍ ولا يُسمّيها الدستور "
            "تُسجَّل ولا تُرفَض: رفعُها إلى الرفض يُلزِم هذا الدفترَ بتعديل "
            "الدستور، وهو ما لا سلطةَ له عليه. والحالُ قائمةٌ اليوم بـ`P0.1`، "
            "فالتسجيلُ يُبقيها مرئيّةً بدل أن تُسوّى بغيرها أو تسقط صامتة"
        ),
        EXAMPLE_SCRIPT_REFERENCE_IS_NOT_EXECUTION: (
            "«يستدعيه اختبارٌ» مُشتَقٌّ هنا من ذِكرِ اسم الملفّ في شجرة "
            "`tests/`، وذِكرُ الاسم ليس تشغيلًا: اختبارٌ يذكر السكربت في نصٍّ "
            "ولا يُشغّله يُقرَأ هنا مُعادَ الإنتاج، وهو حدٌّ مكتوبٌ لا مطويّ"
        ),
    }
)

_GATE_IDENTIFIER: Final = r"(?:G−1|G[0-9]+|P[0-9]+|E[0-9]+)(?:\.[A-Za-z0-9]+)*"

_GATE_OCCURRENCE: Final = re.compile(
    rf"(?<![A-Za-z0-9._−]){_GATE_IDENTIFIER}(?![A-Za-z0-9._])"
)

_CODE_SPAN: Final = re.compile(r"`[^`\n]*`")

_FENCED_BLOCK: Final = re.compile(r"^```", re.MULTILINE)

_CLAIM_TAIL: Final = re.compile(r"[^`()]{0,200}?\(`(?P<module>[^`]+\.py)`\)")

_BACKTICKED: Final = re.compile(r"`(?P<content>[^`\n]+)`")

_PYTHON_IDENTIFIER: Final = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")

_HEADING_GATE: Final = re.compile(
    rf"^#+\s+(?P<gate>{_GATE_IDENTIFIER})(?![A-Za-z0-9._])"
)

_TEST_FUNCTION: Final = re.compile(r"^\s*(?:async\s+)?def\s+(test_[A-Za-z0-9_]*)\s*\(")

_SKIP_CONSTRUCT: Final = re.compile(r"pytest\.(?:mark\.)?(?:skip|xfail)[A-Za-z_]*")

_CONDITIONAL_SKIP: Final = re.compile(r"@pytest\.mark\.skipif\s*\(")

_INLINE_SKIP: Final = re.compile(r"(?<![A-Za-z0-9_.])pytest\.skip\s*\(")


class AchievementLedgerError(ValueError):
    """قراءةٌ أو مقابلةٌ مرفوضة؛ لا يُحمَل المستند على أقرب شكلٍ مقبول."""


class GateCorrespondenceStanding(Enum):
    """أحوالُ معرّف البوّابة بين `README.md` والدستور، ثلاثًا لا اثنتين."""

    ANNOUNCED_IN_BOTH = "مُعلَنٌ في الواجهة والدستور"
    ANNOUNCED_IN_README_ONLY = "مُعلَنٌ في الواجهة وحدها"
    DECLARED_IN_CONSTITUTION_ONLY = "مُصرَّحٌ به في الدستور وحده"

    @property
    def is_named_in_the_constitution(self) -> bool:
        """أيُسمّي الدستورُ هذه البوّابة؟"""

        return self is not GateCorrespondenceStanding.ANNOUNCED_IN_README_ONLY


class ConstitutionNamingSite(Enum):
    """موضعُ تسمية البوّابة في الدستور: عنوانُ قسمٍ، أو متنٌ بلا عنوان."""

    NAMED_IN_A_SECTION_HEADING = "عنوانُ قسمٍ"
    NAMED_IN_THE_BODY_ONLY = "متنٌ بلا عنوان"


class WitnessStanding(Enum):
    """رتبةُ شاهدِ الإنجاز، ثلاثًا لا اثنتين؛ والثالثةُ ليست رفضًا."""

    WITNESS_DERIVED_AND_PRESENT = "شاهدٌ مُشتَقٌّ قائم"
    WITNESS_REGISTERED_ELSEWHERE = "شاهدٌ مُسجَّلٌ في موضعٍ آخر"
    WITNESS_NOT_REGISTERED = "لم يُسجَّل له شاهد"

    @property
    def is_a_refusal(self) -> bool:
        """هل هذه الرتبةُ رفضٌ؟ لا: غيابُ التسجيل ليس ردًّا."""

        return False


class ExampleScriptStanding(Enum):
    """رتبةُ سكربت المثال: يستدعيه شاهدٌ، أو مُعلَنٌ غيرُ مُعادِ الإنتاج."""

    REPRODUCED_BY_A_WITNESS = "يستدعيه شاهد"
    DECLARED_NOT_REPRODUCED = "مُعلَنٌ غيرُ مُعادِ الإنتاج"


class SkipGenus(Enum):
    """جنسا التخطّي المُصرَّح بهما، ولا ثالثَ يُفترَض."""

    CONDITIONAL_ON_UNDEPOSITED_INPUT = "مشروطٌ بمُدخَلٍ غير مودَع"
    CASE_INAPPLICABLE_BY_CONSTRUCTION = "حالةٌ لا تنطبق بالبناء"


def _require_non_blank(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise AchievementLedgerError(f"{field_name} نصٌّ غير فارغ")
    return value


def _require_positive_line(value: int, field_name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        raise AchievementLedgerError(f"{field_name} رقم سطرٍ موجب")
    return value


def _mask_code_spans(text: str) -> str:
    """استبدِل ما بين علامتَي ترميزٍ بفراغٍ مساوٍ في الطول، فتبقى المواضع.

    معرّفاتُ البوّابات تُقرَأ من النثر لا من أمثلة الشيفرة: `PageV05P240…P245`
    يحمل شكلَ معرّفٍ ولا يُعلن بوّابة.
    """

    masked = _FENCED_BLOCK.sub("   ", text)
    return _CODE_SPAN.sub(lambda match: " " * (match.end() - match.start()), masked)


def _line_of(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def _module_dotted_name(relative_path: str) -> str:
    """اسمُ الوحدة المنقوط، مُشتَقًّا من مسارها لا مكتوبًا معه."""

    _require_non_blank(relative_path, "مسار الوحدة")
    if not relative_path.endswith(".py"):
        raise AchievementLedgerError(f"مسارُ وحدةٍ بلا لاحقةٍ بايثونية: {relative_path}")
    parts = relative_path[: -len(".py")].split("/")
    if len(parts) < 2 or parts[0] != "src":
        raise AchievementLedgerError(
            f"مسارُ وحدةٍ خارج شجرة المصدر: {relative_path} — المسارُ يُحَلّ من "
            "`src/` لا يُخمَّن"
        )
    return ".".join(parts[1:])


def _witness_relative_path(relative_path: str) -> str:
    """موضعُ الشاهد، مُشتَقًّا بعُرف الشجرة نفسِه لا بسجلٍّ مكتوب."""

    parts = _module_dotted_name(relative_path).split(".")
    if len(parts) < 2:
        raise AchievementLedgerError(
            f"وحدةٌ بلا حزمةٍ حاضنة: {relative_path} — عُرفُ الشاهد يقابل الحزمة"
        )
    return "/".join((TESTS_RELATIVE_PATH, *parts[1:-1], f"test_{parts[-1]}.py"))


@dataclass(frozen=True, slots=True)
class ReadmeAchievementClaim:
    """مطالبةُ بوّابةٍ واحدة بوحدةٍ في الشجرة، كما وردت في `README.md`."""

    gate_id: str
    relative_path: str
    document_line: int
    declared_symbols: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_non_blank(self.gate_id, "معرّف البوّابة")
        _require_non_blank(self.relative_path, "مسار الوحدة")
        _require_positive_line(self.document_line, "موضع المطالبة")
        if not isinstance(self.declared_symbols, tuple):
            raise AchievementLedgerError("الرموز المُسمّاة مجموعةٌ مرتَّبة")
        seen: set[str] = set()
        for symbol in self.declared_symbols:
            _require_non_blank(symbol, "الرمز المُسمّى")
            if symbol in seen:
                raise AchievementLedgerError(f"رمزٌ مكرّر في المطالبة: {symbol}")
            seen.add(symbol)
        _module_dotted_name(self.relative_path)

    @property
    def dotted_module_name(self) -> str:
        """اسمُ وحدة المطالبة المنقوط، محسوبًا لا مكتوبًا."""

        return _module_dotted_name(self.relative_path)

    @property
    def witness_relative_path(self) -> str:
        """موضعُ شاهد المطالبة المُشتَقّ بعُرف الشجرة."""

        return _witness_relative_path(self.relative_path)


@dataclass(frozen=True, slots=True)
class AchievementRow:
    """صفُّ إنجازٍ واحد: مطالبتُه، ورموزُه القائمة، ورتبةُ شاهده.

    لا حقلَ «مطابق/غير مطابق» هنا: قيامُ الصفّ **هو** المطابقة، وانحرافُها
    استثناءٌ مُسمّى عند الإنشاء (§٤: «المخالفة تُرفَض لا تُقرَّر»).
    """

    claim: ReadmeAchievementClaim
    resident_symbols: tuple[str, ...]
    witness_relative_path: str
    witness_standing: WitnessStanding

    def __post_init__(self) -> None:
        if not isinstance(self.claim, ReadmeAchievementClaim):
            raise AchievementLedgerError("المطالبة من نوعها")
        if not isinstance(self.resident_symbols, tuple):
            raise AchievementLedgerError("الرموز القائمة مجموعةٌ مرتَّبة")
        declared = set(self.claim.declared_symbols)
        for symbol in self.resident_symbols:
            if symbol not in declared:
                raise AchievementLedgerError(
                    f"رمزٌ قائمٌ لم تُسمّه المطالبة: {symbol} — الرموزُ القائمة "
                    "جزءٌ ممّا سمّاه النثر لا زيادةٌ عليه"
                )
        if not self.resident_symbols:
            raise AchievementLedgerError(
                f"{self.claim.gate_id}: مطالبةٌ بلا رمزٍ قائمٍ في وحدتها عند "
                f"السطر {self.claim.document_line} — "
                f"{CLAIM_WITHOUT_A_RESIDENT_SYMBOL_IS_REFUSED_NOTE}"
            )
        _require_non_blank(self.witness_relative_path, "موضع الشاهد")
        if not isinstance(self.witness_standing, WitnessStanding):
            raise AchievementLedgerError("رتبة الشاهد من مفردتها المغلقة")
        if (
            self.witness_standing is WitnessStanding.WITNESS_DERIVED_AND_PRESENT
            and self.witness_relative_path != self.claim.witness_relative_path
        ):
            raise AchievementLedgerError(
                f"{self.claim.gate_id}: شاهدٌ يُقرَأ مُشتَقًّا وموضعُه ليس "
                f"الموضعَ الذي يشتقّه العُرف: {self.witness_relative_path}"
            )

    @property
    def foreign_symbols(self) -> tuple[str, ...]:
        """الرموزُ التي سمّاها النثرُ ولا تقوم من هذه الوحدة، بترتيب ورودها."""

        resident = set(self.resident_symbols)
        return tuple(
            symbol for symbol in self.claim.declared_symbols if symbol not in resident
        )


@dataclass(frozen=True, slots=True)
class GateCorrespondenceRow:
    """صفُّ مقابلةٍ لمعرّف بوّابةٍ واحد بين `README.md` و`docs/CONSTITUTION.md`."""

    gate_id: str
    standing: GateCorrespondenceStanding
    readme_line: int | None = None
    constitution_line: int | None = None
    constitution_site: ConstitutionNamingSite | None = None

    def __post_init__(self) -> None:
        _require_non_blank(self.gate_id, "معرّف البوّابة")
        if not isinstance(self.standing, GateCorrespondenceStanding):
            raise AchievementLedgerError("حال المقابلة من مفردتها المغلقة")

        constitution_only = GateCorrespondenceStanding.DECLARED_IN_CONSTITUTION_ONLY
        names_readme = self.standing is not constitution_only
        if names_readme:
            if self.readme_line is None:
                raise AchievementLedgerError(
                    f"{self.gate_id}: حالٌ تُعلن الواجهةَ بلا موضعِ ذِكرٍ فيها"
                )
            _require_positive_line(self.readme_line, "موضع الذِكر في الواجهة")
        elif self.readme_line is not None:
            raise AchievementLedgerError(
                f"{self.gate_id}: حالٌ لا تُعلن الواجهةَ ومعها موضعُ ذِكرٍ فيها"
            )

        if self.standing.is_named_in_the_constitution:
            if self.constitution_line is None or self.constitution_site is None:
                raise AchievementLedgerError(
                    f"{self.gate_id}: حالٌ تُسمّي الدستورَ بلا موضعٍ فيه"
                )
            _require_positive_line(self.constitution_line, "موضع الذِكر في الدستور")
            if not isinstance(self.constitution_site, ConstitutionNamingSite):
                raise AchievementLedgerError("موضع التسمية من مفردته المغلقة")
        elif self.constitution_line is not None or self.constitution_site is not None:
            raise AchievementLedgerError(
                f"{self.gate_id}: حالٌ لا يُسمّيها الدستور ومعها موضعٌ فيه — "
                f"{README_ONLY_GATE_IS_RECORDED_NOT_REFUSED}"
            )


@dataclass(frozen=True, slots=True)
class ExampleScriptRow:
    """صفُّ سكربتِ مثالٍ واحد ورتبةُ إعادة إنتاجه."""

    relative_path: str
    standing: ExampleScriptStanding

    def __post_init__(self) -> None:
        _require_non_blank(self.relative_path, "مسار السكربت")
        if not self.relative_path.startswith(f"{EXAMPLES_RELATIVE_PATH}/"):
            raise AchievementLedgerError(
                f"سكربتٌ خارج شجرة الأمثلة: {self.relative_path}"
            )
        if not isinstance(self.standing, ExampleScriptStanding):
            raise AchievementLedgerError("رتبة السكربت من مفردتها المغلقة")


@dataclass(frozen=True, slots=True)
class SkippedWitnessRow:
    """صفُّ تخطٍّ واحد في شجرة الشواهد: موضعُه وجنسُه المُصرَّح به."""

    relative_path: str
    document_line: int
    genus: SkipGenus

    def __post_init__(self) -> None:
        _require_non_blank(self.relative_path, "مسار ملفّ الشاهد")
        _require_positive_line(self.document_line, "موضع التخطّي")
        if not isinstance(self.genus, SkipGenus):
            raise AchievementLedgerError("جنس التخطّي من مفردته المغلقة")


@dataclass(frozen=True, slots=True)
class AchievementLedger:
    """دفترُ الإنجازات: مطالباتُ الواجهة مُقابَلةً بالدستور وبالشجرة وبشواهدها."""

    rows: tuple[AchievementRow, ...]
    correspondence: tuple[GateCorrespondenceRow, ...]
    example_scripts: tuple[ExampleScriptRow, ...]
    skipped_witnesses: tuple[SkippedWitnessRow, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.rows, tuple) or not self.rows:
            raise AchievementLedgerError("صفوف الإنجازات مجموعةٌ غير فارغة")
        if not isinstance(self.correspondence, tuple) or not self.correspondence:
            raise AchievementLedgerError("صفوف المقابلة مجموعةٌ غير فارغة")
        if not isinstance(self.example_scripts, tuple):
            raise AchievementLedgerError("صفوف الأمثلة مجموعةٌ مرتَّبة")
        if not isinstance(self.skipped_witnesses, tuple):
            raise AchievementLedgerError("صفوف التخطّي مجموعةٌ مرتَّبة")

        seen_gates: set[str] = set()
        previous_line = 0
        for row in self.rows:
            if not isinstance(row, AchievementRow):
                raise AchievementLedgerError("كل عنصرٍ صفُّ إنجازٍ")
            if row.claim.gate_id in seen_gates:
                raise AchievementLedgerError(
                    f"بوّابةٌ تُطالِب بوحدتها مرّتين: {row.claim.gate_id} — "
                    "مطالبتان لبوّابةٍ واحدة تُقرَآن إنجازين"
                )
            seen_gates.add(row.claim.gate_id)
            if row.claim.document_line <= previous_line:
                raise AchievementLedgerError("ترتيب الصفوف ترتيبُ ورودها في `README.md`")
            previous_line = row.claim.document_line

        seen_correspondence: set[str] = set()
        for entry in self.correspondence:
            if not isinstance(entry, GateCorrespondenceRow):
                raise AchievementLedgerError("كل عنصرٍ صفُّ مقابلةٍ")
            if entry.gate_id in seen_correspondence:
                raise AchievementLedgerError(f"معرّفٌ مُقابَلٌ مرّتين: {entry.gate_id}")
            seen_correspondence.add(entry.gate_id)

        for gate_id in seen_gates:
            claimed_entry = self._correspondence_of(gate_id)
            if claimed_entry is None:
                raise AchievementLedgerError(
                    f"مطالبةٌ بلا صفِّ مقابلةٍ: {gate_id} — المقابلةُ تشمل كلّ "
                    "معرّفٍ مذكورٍ في الواجهة، والمطالبةُ ذِكرٌ أوّلًا"
                )
            if not claimed_entry.standing.is_named_in_the_constitution:
                raise AchievementLedgerError(
                    f"{gate_id}: مطالبةٌ بوحدةٍ بلا تسميةٍ في الدستور — "
                    f"{README_CLAIM_WITHOUT_A_CONSTITUTIONAL_GATE_IS_REFUSED_NOTE}"
                )

        for row_example in self.example_scripts:
            if not isinstance(row_example, ExampleScriptRow):
                raise AchievementLedgerError("كل عنصرٍ صفُّ سكربتٍ")
        for row_skip in self.skipped_witnesses:
            if not isinstance(row_skip, SkippedWitnessRow):
                raise AchievementLedgerError("كل عنصرٍ صفُّ تخطٍّ")

    def _correspondence_of(self, gate_id: str) -> GateCorrespondenceRow | None:
        for entry in self.correspondence:
            if entry.gate_id == gate_id:
                return entry
        return None

    @property
    def achievement_count(self) -> int:
        """عدد الإنجازات المُطالَب بها، محسوبًا لا مكتوبًا."""

        return len(self.rows)

    @property
    def correspondence_count(self) -> int:
        """عدد معرّفات البوّابات المُقابَلة، محسوبًا لا مكتوبًا."""

        return len(self.correspondence)

    @property
    def example_script_count(self) -> int:
        """عدد سكربتات الأمثلة المرصودة، محسوبًا لا مكتوبًا."""

        return len(self.example_scripts)

    @property
    def skipped_witness_count(self) -> int:
        """عدد مواضع التخطّي المرصودة، محسوبًا لا مكتوبًا."""

        return len(self.skipped_witnesses)

    @property
    def claimed_modules(self) -> tuple[str, ...]:
        """وحداتُ الإنجازات بترتيب مطالباتها، بلا تكرار."""

        return tuple(dict.fromkeys(row.claim.relative_path for row in self.rows))

    def rows_by_witness_standing(
        self, standing: WitnessStanding
    ) -> tuple[AchievementRow, ...]:
        """صفوفُ رتبةِ شاهدٍ بعينها، بترتيب ورودها."""

        if not isinstance(standing, WitnessStanding):
            raise AchievementLedgerError("رتبة الشاهد من مفردتها المغلقة")
        return tuple(row for row in self.rows if row.witness_standing is standing)

    def correspondence_by_standing(
        self, standing: GateCorrespondenceStanding
    ) -> tuple[GateCorrespondenceRow, ...]:
        """صفوفُ حالِ مقابلةٍ بعينها، بترتيب ورودها."""

        if not isinstance(standing, GateCorrespondenceStanding):
            raise AchievementLedgerError("حال المقابلة من مفردتها المغلقة")
        return tuple(
            entry for entry in self.correspondence if entry.standing is standing
        )

    def example_scripts_by_standing(
        self, standing: ExampleScriptStanding
    ) -> tuple[ExampleScriptRow, ...]:
        """صفوفُ رتبةِ إعادةِ إنتاجٍ بعينها، بترتيب ورودها."""

        if not isinstance(standing, ExampleScriptStanding):
            raise AchievementLedgerError("رتبة السكربت من مفردتها المغلقة")
        return tuple(
            entry for entry in self.example_scripts if entry.standing is standing
        )

    def skipped_witnesses_by_genus(
        self, genus: SkipGenus
    ) -> tuple[SkippedWitnessRow, ...]:
        """مواضعُ تخطٍّ من جنسٍ بعينه، بترتيب ورودها."""

        if not isinstance(genus, SkipGenus):
            raise AchievementLedgerError("جنس التخطّي من مفردته المغلقة")
        return tuple(entry for entry in self.skipped_witnesses if entry.genus is genus)

    def row(self, gate_id: str) -> AchievementRow:
        """صفُّ إنجازٍ بعينه؛ وغيابُه رفضٌ مُسمّى لا `None` يُطوى."""

        _require_non_blank(gate_id, "معرّف البوّابة")
        for row in self.rows:
            if row.claim.gate_id == gate_id:
                return row
        raise AchievementLedgerError(f"لا صفَّ إنجازٍ للبوّابة: {gate_id}")

    def correspondence_row(self, gate_id: str) -> GateCorrespondenceRow:
        """صفُّ مقابلةٍ بعينه؛ وغيابُه رفضٌ مُسمّى لا `None` يُطوى."""

        _require_non_blank(gate_id, "معرّف البوّابة")
        entry = self._correspondence_of(gate_id)
        if entry is None:
            raise AchievementLedgerError(f"لا صفَّ مقابلةٍ للمعرّف: {gate_id}")
        return entry


def read_readme_claims(document_text: str) -> tuple[ReadmeAchievementClaim, ...]:
    """اقرأ مطالبات `README.md` بشكلها الواحد؛ وما خرج عنه ذِكرٌ لا مطالبة."""

    if not isinstance(document_text, str) or not document_text.strip():
        raise AchievementLedgerError("نصّ الواجهة نصٌّ غير فارغ")
    masked = _mask_code_spans(document_text)

    offsets = [match.start() for match in _GATE_OCCURRENCE.finditer(masked)]
    sites: list[tuple[int, str, str, int]] = []
    for match in _GATE_OCCURRENCE.finditer(masked):
        tail = _CLAIM_TAIL.match(document_text, match.end())
        if tail is None:
            continue
        if any(match.end() < other < tail.start("module") for other in offsets):
            continue
        sites.append((match.start(), match.group(0), tail.group("module"), tail.end()))

    claims: list[ReadmeAchievementClaim] = []
    for order, (start, gate_id, module_path, tail_end) in enumerate(sites):
        paragraph_end = document_text.find("\n\n", tail_end)
        if paragraph_end < 0:
            paragraph_end = len(document_text)
        stop = sites[order + 1][0] if order + 1 < len(sites) else paragraph_end
        declared = tuple(
            dict.fromkeys(
                found.group("content")
                for found in _BACKTICKED.finditer(
                    document_text, start, max(stop, tail_end)
                )
                if _PYTHON_IDENTIFIER.match(found.group("content"))
            )
        )
        claims.append(
            ReadmeAchievementClaim(
                gate_id=gate_id,
                relative_path=module_path,
                document_line=_line_of(document_text, start),
                declared_symbols=declared,
            )
        )
    if not claims:
        raise AchievementLedgerError(
            "لم تُقرَأ أيّ مطالبةٍ من الواجهة: واجهةٌ بلا مطالبةٍ تُقرَأ «لا "
            "إنجاز» وهو ادّعاءٌ لم يُقرَأ النصّ لأجله"
        )
    return tuple(claims)


def read_gate_mentions(document_text: str) -> Mapping[str, int]:
    """معرّفاتُ البوّابات المذكورة في نصٍّ، بأوّل موضعِ ذِكرٍ لكلٍّ منها."""

    if not isinstance(document_text, str) or not document_text.strip():
        raise AchievementLedgerError("نصّ المستند نصٌّ غير فارغ")
    masked = _mask_code_spans(document_text)
    gathered: dict[str, int] = {}
    for match in _GATE_OCCURRENCE.finditer(masked):
        gathered.setdefault(match.group(0), _line_of(document_text, match.start()))
    return MappingProxyType(gathered)


def read_constitution_heading_gates(document_text: str) -> Mapping[str, int]:
    """معرّفاتُ البوّابات التي تُصدِّر أقسامًا في الدستور، بمواضع عناوينها."""

    if not isinstance(document_text, str) or not document_text.strip():
        raise AchievementLedgerError("نصّ الدستور نصٌّ غير فارغ")
    gathered: dict[str, int] = {}
    for number, line in enumerate(document_text.splitlines(), start=1):
        match = _HEADING_GATE.match(line)
        if match is not None:
            gathered.setdefault(match.group("gate"), number)
    if not gathered:
        raise AchievementLedgerError(
            "لم يُقرَأ أيّ عنوانِ بوّابةٍ من الدستور: دستورٌ بلا عناوين يُقرَأ "
            "«لا قوانين» وهو ادّعاءٌ لم يُقرَأ النصّ لأجله"
        )
    return MappingProxyType(gathered)


def correspond_gates(
    readme_text: str, constitution_text: str
) -> tuple[GateCorrespondenceRow, ...]:
    """قابِل معرّفات الواجهة بمعرّفات الدستور؛ والحالاتُ ثلاثٌ لا حالان."""

    readme_mentions = read_gate_mentions(readme_text)
    constitution_mentions = read_gate_mentions(constitution_text)
    heading_gates = read_constitution_heading_gates(constitution_text)

    rows: list[GateCorrespondenceRow] = []
    for gate_id, readme_line in readme_mentions.items():
        constitution_line = constitution_mentions.get(gate_id)
        if constitution_line is None:
            rows.append(
                GateCorrespondenceRow(
                    gate_id=gate_id,
                    standing=GateCorrespondenceStanding.ANNOUNCED_IN_README_ONLY,
                    readme_line=readme_line,
                )
            )
            continue
        heading_line = heading_gates.get(gate_id)
        rows.append(
            GateCorrespondenceRow(
                gate_id=gate_id,
                standing=GateCorrespondenceStanding.ANNOUNCED_IN_BOTH,
                readme_line=readme_line,
                constitution_line=(
                    heading_line if heading_line is not None else constitution_line
                ),
                constitution_site=(
                    ConstitutionNamingSite.NAMED_IN_A_SECTION_HEADING
                    if heading_line is not None
                    else ConstitutionNamingSite.NAMED_IN_THE_BODY_ONLY
                ),
            )
        )

    for gate_id, heading_line in heading_gates.items():
        if gate_id in readme_mentions:
            continue
        rows.append(
            GateCorrespondenceRow(
                gate_id=gate_id,
                standing=GateCorrespondenceStanding.DECLARED_IN_CONSTITUTION_ONLY,
                constitution_line=heading_line,
                constitution_site=ConstitutionNamingSite.NAMED_IN_A_SECTION_HEADING,
            )
        )
    return tuple(rows)


def repository_root_path() -> Path:
    """جذرُ المستودع، مشتقًّا من موضع هذه الوحدة لا مكتوبًا."""

    return Path(__file__).resolve().parents[3]


def _read_document(path: Path, name: str) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as error:
        raise AchievementLedgerError(
            f"تعذّرت قراءة {name} عند {path}: دفترٌ فارغ يُقرَأ «لا إنجاز» وهو "
            "ادّعاءٌ لم يُقرَأ المستند لأجله"
        ) from error


def derive_resident_symbols(claim: ReadmeAchievementClaim) -> tuple[str, ...]:
    """استورِد وحدةَ المطالبة، ثم اقرأ أيُّ رموزها المُسمّاة تقوم منها فعلًا."""

    if not isinstance(claim, ReadmeAchievementClaim):
        raise AchievementLedgerError("المطالبة من نوعها")
    try:
        module = importlib.import_module(claim.dotted_module_name)
    except ImportError as error:
        raise AchievementLedgerError(
            f"{claim.gate_id}: وحدةٌ مُطالَبٌ بها لا تُستورَد "
            f"({claim.relative_path}) — {CLAIMED_MODULE_MUST_IMPORT_NOTE}"
        ) from error
    return tuple(symbol for symbol in claim.declared_symbols if hasattr(module, symbol))


def derive_witness_standing(
    claim: ReadmeAchievementClaim,
    root: Path,
    registered_witnesses: Mapping[str, str] | None = None,
) -> tuple[str, WitnessStanding]:
    """اشتقّ موضعَ الشاهد ورتبتَه؛ وغيابُ التسجيل حالٌ ثالثة لا رفض."""

    if not isinstance(claim, ReadmeAchievementClaim):
        raise AchievementLedgerError("المطالبة من نوعها")
    if not isinstance(root, Path):
        raise AchievementLedgerError("جذر المستودع مسارٌ")

    derived = claim.witness_relative_path
    if _defines_test_functions(root / derived):
        return derived, WitnessStanding.WITNESS_DERIVED_AND_PRESENT

    registered = (registered_witnesses or {}).get(claim.gate_id)
    if registered is not None and _defines_test_functions(root / registered):
        return registered, WitnessStanding.WITNESS_REGISTERED_ELSEWHERE
    return derived, WitnessStanding.WITNESS_NOT_REGISTERED


def _defines_test_functions(path: Path) -> bool:
    if not path.is_file():
        return False
    text = path.read_text(encoding="utf-8")
    return any(_TEST_FUNCTION.match(line) for line in text.splitlines())


def census_example_scripts(root: Path) -> tuple[ExampleScriptRow, ...]:
    """أحصِ سكربتات الأمثلة، ورتبةَ إعادة إنتاج كلٍّ منها، بترتيب مساراتها."""

    if not isinstance(root, Path):
        raise AchievementLedgerError("جذر المستودع مسارٌ")
    examples = root / EXAMPLES_RELATIVE_PATH
    if not examples.is_dir():
        raise AchievementLedgerError(
            f"شجرة الأمثلة غير موجودة عند {examples}: شجرةٌ غائبة تُقرَأ «لا "
            "أمثلة» وهو ادّعاءٌ لم تُقرَأ الشجرة لأجله"
        )
    witness_texts = _witness_texts(root)
    rows: list[ExampleScriptRow] = []
    for script in sorted(examples.rglob("*.py")):
        name = script.name
        reproduced = any(name in text for text in witness_texts)
        rows.append(
            ExampleScriptRow(
                relative_path=script.relative_to(root).as_posix(),
                standing=(
                    ExampleScriptStanding.REPRODUCED_BY_A_WITNESS
                    if reproduced
                    else ExampleScriptStanding.DECLARED_NOT_REPRODUCED
                ),
            )
        )
    return tuple(rows)


def _witness_paths(root: Path) -> tuple[Path, ...]:
    tests = root / TESTS_RELATIVE_PATH
    if not tests.is_dir():
        raise AchievementLedgerError(
            f"شجرة الشواهد غير موجودة عند {tests}: شجرةٌ غائبة تُقرَأ «لا "
            "شواهد» وهو ادّعاءٌ لم تُقرَأ الشجرة لأجله"
        )
    return tuple(sorted(tests.rglob("*.py")))


def _witness_texts(root: Path) -> tuple[str, ...]:
    return tuple(path.read_text(encoding="utf-8") for path in _witness_paths(root))


def census_skipped_witnesses(root: Path) -> tuple[SkippedWitnessRow, ...]:
    """أحصِ مواضع التخطّي في شجرة الشواهد بجنسَيها؛ وما خرج عنهما مرفوض."""

    if not isinstance(root, Path):
        raise AchievementLedgerError("جذر المستودع مسارٌ")
    rows: list[SkippedWitnessRow] = []
    for path in _witness_paths(root):
        relative = path.relative_to(root).as_posix()
        for number, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), start=1
        ):
            if _SKIP_CONSTRUCT.search(line) is None:
                continue
            if _CONDITIONAL_SKIP.search(line):
                genus = SkipGenus.CONDITIONAL_ON_UNDEPOSITED_INPUT
            elif _INLINE_SKIP.search(line):
                genus = SkipGenus.CASE_INAPPLICABLE_BY_CONSTRUCTION
            else:
                raise AchievementLedgerError(
                    f"تخطٍّ خارج الجنسين عند {relative}:{number} — "
                    f"{UNKNOWN_SKIP_FORM_IS_REFUSED_NOTE}"
                )
            rows.append(
                SkippedWitnessRow(
                    relative_path=relative, document_line=number, genus=genus
                )
            )
    return tuple(rows)


def correspond_achievements_to_tree(
    root: Path | None = None,
    registered_witnesses: Mapping[str, str] | None = None,
) -> AchievementLedger:
    """قابِل إنجازات الواجهة بالدستور وبالشجرة وبشواهدها؛ وقيامُ الدفتر هو المقابلة."""

    base = repository_root_path() if root is None else root
    if not isinstance(base, Path):
        raise AchievementLedgerError("جذر المستودع مسارٌ")

    readme_text = _read_document(base / README_RELATIVE_PATH, "الواجهة")
    constitution_text = _read_document(
        base / CONSTITUTION_DOCUMENT_RELATIVE_PATH, "وثيقة الدستور"
    )

    claims = read_readme_claims(readme_text)
    rows: list[AchievementRow] = []
    for claim in claims:
        if not (base / claim.relative_path).is_file():
            raise AchievementLedgerError(
                f"{claim.gate_id}: وحدةٌ مُطالَبٌ بها لا وجود لها في الشجرة: "
                f"{claim.relative_path} — {CLAIMED_MODULE_MUST_IMPORT_NOTE}"
            )
        witness_path, standing = derive_witness_standing(
            claim, base, registered_witnesses
        )
        rows.append(
            AchievementRow(
                claim=claim,
                resident_symbols=derive_resident_symbols(claim),
                witness_relative_path=witness_path,
                witness_standing=standing,
            )
        )

    return AchievementLedger(
        rows=tuple(rows),
        correspondence=correspond_gates(readme_text, constitution_text),
        example_scripts=census_example_scripts(base),
        skipped_witnesses=census_skipped_witnesses(base),
    )


__all__ = [
    "ACHIEVEMENT_LEDGER_AUTHORITY_NOTE",
    "AIMS_DOCUMENT_RELATIVE_PATH",
    "CLAIMED_MODULE_MUST_IMPORT_NOTE",
    "CLAIM_SHAPE_IS_A_FORM_NOT_A_MEANING",
    "CLAIM_WITHOUT_A_RESIDENT_SYMBOL_IS_REFUSED_NOTE",
    "CONSTITUTION_DOCUMENT_RELATIVE_PATH",
    "DESIGN_SOURCE_CITATION_NOTE",
    "EXAMPLES_RELATIVE_PATH",
    "EXAMPLE_SCRIPT_REFERENCE_IS_NOT_EXECUTION",
    "NAMED_RESIDUALS",
    "NO_INDICATOR_IN_THIS_ACHIEVEMENT_LEDGER_NOTE",
    "README_CLAIM_WITHOUT_A_CONSTITUTIONAL_GATE_IS_REFUSED_NOTE",
    "README_ONLY_GATE_IS_RECORDED_NOT_REFUSED",
    "README_RELATIVE_PATH",
    "SOURCE_PACKAGE_RELATIVE_PATH",
    "SYMBOL_PRESENCE_IS_NOT_SYMBOL_AUTHORSHIP",
    "TESTS_RELATIVE_PATH",
    "UNKNOWN_SKIP_FORM_IS_REFUSED_NOTE",
    "WITNESS_COLLECTS_IS_NOT_WITNESS_CHECKS_THIS",
    "AchievementLedger",
    "AchievementLedgerError",
    "AchievementRow",
    "ConstitutionNamingSite",
    "ExampleScriptRow",
    "ExampleScriptStanding",
    "GateCorrespondenceRow",
    "GateCorrespondenceStanding",
    "ReadmeAchievementClaim",
    "SkipGenus",
    "SkippedWitnessRow",
    "WitnessStanding",
    "census_example_scripts",
    "census_skipped_witnesses",
    "correspond_achievements_to_tree",
    "correspond_gates",
    "derive_resident_symbols",
    "derive_witness_standing",
    "read_constitution_heading_gates",
    "read_gate_mentions",
    "read_readme_claims",
    "repository_root_path",
]
