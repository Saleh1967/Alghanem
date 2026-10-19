"""جاهزيّةُ امتحان التخرّج: شروطُ غيابه آليّةً لا توكيدًا في تعليق.

القرارُ `٧` في `decision_chain` أعلن غيابَه بثلاثة شروط، وأعلن أنّها تُشغَّل
ولا تُقال. وهذه الوحدةُ موضعُ تشغيلها. **ولا تبني الامتحانَ ولا تدّعي بناءه**:
الحلقةُ تبقى `حلقة_غير_مُرمَّزة` بعلامة الوصل الخارجيّ، ولا يرفع هذه الوحدةَ
شيءٌ من ذلك (`THIS_MODULE_IS_THE_ABSENCE_GUARD_NOT_THE_BUILDER`).

**أوّلًا: والشروطُ مرتَّبةٌ لا مجموعة.** أوّلُ شرطٍ غيرِ مستوفًى هو البابُ،
وما بعده غيرُ منظورٍ فيه؛ فإعلانُ «ثلاثةُ شروطٍ ناقصة» يُخفي أنّ أوّلَها وحدَه
هو الذي يقف عنده البناء.

| الترتيب | الشرط | الحال |
|---|---|---|
| ١ | حضورُ المُصدِّر في موضعه | **غيرُ مستوفًى** |
| ٢ | حارسُ غيابٍ يجري على البانِي | غيرُ منظورٍ فيه |
| ٣ | نتيجةٌ لم تُكتَب في طرفٍ منهما | غيرُ منظورٍ فيه |

**وثانيًا: والنسخةُ المودَعةُ ليست المادّة، والفرقُ مُشتَقٌّ لا مُدَّعًى.**
مادّةُ الامتحان أختامُ صنفِ `[بوّابة]` — بقوسَيها — تُقرأ من مواضعها في
المستودع المُخرِج. والمودَعُ في `exhibits/hamil-induction/` لا يحمل من ذلك
الصنف ختمًا واحدًا: أختامُه صنفُها `بوّابة` بلا قوسَين، وحقولُها ليست حقولَه.
فامتناعُه عن أن يكون المادّةَ مقروءٌ من بنيته لا من تاريخ أخذه
(`THE_DEPOSITED_COPY_IS_REFUSED_BY_ITS_OWN_SHAPE_NOT_BY_ITS_DATE`). وهذا
بعينه الشرطُ الثاني من شروط الغياب وقد صار جارياً: النسخةُ الثانيةُ تتخلّف،
فتُرفَض مادّةً وتبقى معروضَ تدقيقٍ كما أُعلِن يومَ أُودِعت.

**وثالثًا: والبانِي ممنوعٌ من نصّ المصدر.** الشرطُ الأوّل يقول: إن مسّ البانِي
بايتةً من نصّ المُصدِّر سقط البابُ بتمامه. فههنا حارسُ `ast` يقرأ نصَّ أيّ
بانٍ ويُسمّي ما مسّ به المصدرَ: قراءةَ ملفٍّ بامتدادِ `.py`، أو استخراجَ
شيفرةٍ بـ`inspect`، أو تحليلَها بـ`ast`. والحارسُ يجري اليومَ على العدم
فيُصدِر فراغًا؛ ووجودُه قبل البانِي مقصودٌ: حارسٌ يُكتَب بعد المحروس يُفصَّل
على مقاسه (`A_GUARD_WRITTEN_AFTER_ITS_BUILDER_IS_CUT_TO_ITS_SHAPE`).

**ورابعًا: والشرطُ الثالث لا يُغلَق ههنا ولا في غيرها.** سلسلةُ الشهادة
مفتوحةُ الطرف: الدالُّ مسنودٌ إلى البايتات وحدَها، ولا يُصادِق عقدٌ على اللغة
فيدور الدور. فهو مُصرَّحٌ بحدّه لا مُشغَّل، وتصريحُه بحدّه أصدقُ من حارسٍ
يُوهِم إغلاقَ ما لا يُغلَق (`THE_OPEN_ENDED_WITNESS_CHAIN_IS_DECLARED_NOT_CLOSED`).

**وخامسًا: ولا مقدارَ يخرج من ههنا.** لا عددَ أختامٍ ولا عددَ فواتير ولا نسبة:
رقمٌ يُنقَل من ذاك المستودع إلى هذا مكتوبًا هو عينُ ما يُسقِط القرارَ بالشرط
الثاني. فالأحكامُ ههنا أسماءٌ ومواضعُ وحالٌ، وليس فيها رقمٌ واحد
(`NO_FIGURE_CROSSES_FROM_THE_EXPORTER_INTO_THIS_TREE`).

ولا سلطةَ لهذه الوحدة: لا ولادةَ، ولا تجميدَ، ولا `E0`، ولا استيرادَ من
`kernel/`.
"""

from __future__ import annotations

import ast
import json
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Final

__all__ = [
    "A_GUARD_WRITTEN_AFTER_ITS_BUILDER_IS_CUT_TO_ITS_SHAPE",
    "EXAM_MATERIAL_SEAL_CLASS",
    "GRADUATION_EXAM_NAMED_RESIDUALS",
    "NO_FIGURE_CROSSES_FROM_THE_EXPORTER_INTO_THIS_TREE",
    "THE_DEPOSITED_COPY_IS_REFUSED_BY_ITS_OWN_SHAPE_NOT_BY_ITS_DATE",
    "THE_EXPORTER_OUTPUT_RELATIVE_PATH",
    "THE_EXPORTING_REPOSITORY",
    "THE_OPEN_ENDED_WITNESS_CHAIN_IS_DECLARED_NOT_CLOSED",
    "THE_RUNG_ORDER",
    "THIS_MODULE_IS_THE_ABSENCE_GUARD_NOT_THE_BUILDER",
    "DepositedCopyReading",
    "ExamRung",
    "GraduationExamReadinessError",
    "RungStanding",
    "SourceTouch",
    "exporter_is_present_at_its_place",
    "read_deposited_copy",
    "source_touches_in",
    "the_first_unmet_rung",
    "repository_root_path",
    "the_rung_readings",
]


class GraduationExamReadinessError(ValueError):
    """رفضٌ مُسمًّى في حراسة الامتحان؛ ولا يُبتلَع خللٌ ههنا صمتًا."""


THE_EXPORTING_REPOSITORY: Final[str] = "Saleh1967/hamil-hala-zaman-program"
"""المستودعُ المُخرِج؛ يُسمّى ولا يُنسَخ، والارتباطُ بمخرجه لا بمسارٍ ههنا."""

EXAM_MATERIAL_SEAL_CLASS: Final[str] = "[بوّابة]"
"""صنفُ أختام المادّة بقوسَيه؛ وهو وحدَه الفارقُ عن `بوّابة` المودَعة."""

THE_EXPORTER_OUTPUT_RELATIVE_PATH: Final[str] = "induction/seals.json"
"""مخرجُ المُصدِّر في موضعه من المستودع المُخرِج؛ لا في هذه الشجرة."""

_THE_DEPOSITED_COPY_PATH: Final[str] = "exhibits/hamil-induction/seals.json"

_THE_REGISTER_KEY: Final[str] = "سجلُّ_الأختام"
_THE_SEALS_KEY: Final[str] = "أختام"
_THE_CLASS_KEY: Final[str] = "صنف"

_SOURCE_READING_SUFFIX: Final[str] = ".py"

_SOURCE_EXTRACTING_NAMES: Final[frozenset[str]] = frozenset(
    {"getsource", "getsourcelines", "getsourcefile", "parse", "unparse"}
)

_FILE_READING_NAMES: Final[frozenset[str]] = frozenset(
    {"open", "read_text", "read_bytes"}
)


class RungStanding(Enum):
    """حالُ الدرجة؛ وما بعد أوّلِ غيرِ مستوفًى غيرُ منظورٍ فيه لا مستوفًى."""

    مستوفاة = "مستوفاة"
    غير_مستوفاة = "غيرُ مستوفاة"
    غير_منظور_فيها = "غيرُ منظورٍ فيها"


class ExamRung(Enum):
    """درجاتُ الامتحان مسمّاةً؛ وترتيبُها في `THE_RUNG_ORDER`."""

    EXPORTER_PRESENT_AT_ITS_PLACE = "حضورُ المُصدِّر في موضعه"
    ABSENCE_GUARD_RUNS_OVER_THE_BUILDER = "جريانُ حارس الغياب على البانِي"
    A_RESULT_IN_NEITHER_SIDE = "نتيجةٌ لم تُكتَب في طرفٍ منهما"


THE_RUNG_ORDER: Final[tuple[ExamRung, ...]] = (
    ExamRung.EXPORTER_PRESENT_AT_ITS_PLACE,
    ExamRung.ABSENCE_GUARD_RUNS_OVER_THE_BUILDER,
    ExamRung.A_RESULT_IN_NEITHER_SIDE,
)
"""ترتيبُ الدرجات؛ وأوّلُ غيرِ مستوفاةٍ يوقف النظرَ فيما بعدها."""


# --- البقايا المسمّاة ------------------------------------------------------

THIS_MODULE_IS_THE_ABSENCE_GUARD_NOT_THE_BUILDER: Final[str] = (
    "THIS_MODULE_IS_THE_ABSENCE_GUARD_NOT_THE_BUILDER: ههنا تُشغَّل شروطُ "
    "غياب القرار `٧` ولا يُبنى الامتحان. والحلقةُ تبقى `حلقة_غير_مُرمَّزة` "
    "بعلامة الوصل الخارجيّ، فلا يرفعها وجودُ هذه الوحدة ولا وجودُ شواهدها"
)

THE_DEPOSITED_COPY_IS_REFUSED_BY_ITS_OWN_SHAPE_NOT_BY_ITS_DATE: Final[str] = (
    "THE_DEPOSITED_COPY_IS_REFUSED_BY_ITS_OWN_SHAPE_NOT_BY_ITS_DATE: المودَعُ "
    f"في `{_THE_DEPOSITED_COPY_PATH}` لا يحمل ختمًا واحدًا من صنف "
    f"`{EXAM_MATERIAL_SEAL_CLASS}`، فامتناعُه عن أن يكون المادّةَ مقروءٌ من "
    "بنيته لا من تاريخ أخذه؛ ولو حُدِّث لبقي نسخةً، والنسخةُ لا تُقرأ موضعًا"
)

A_GUARD_WRITTEN_AFTER_ITS_BUILDER_IS_CUT_TO_ITS_SHAPE: Final[str] = (
    "A_GUARD_WRITTEN_AFTER_ITS_BUILDER_IS_CUT_TO_ITS_SHAPE: حارسُ الغياب "
    "مكتوبٌ قبل البانِي عمدًا، فيجري اليومَ على العدم ويُصدِر فراغًا؛ وحارسٌ "
    "يُكتَب بعد محروسه يُفصَّل على مقاسه فيُجيز ما وقع لا ما يجوز"
)

THE_OPEN_ENDED_WITNESS_CHAIN_IS_DECLARED_NOT_CLOSED: Final[str] = (
    "THE_OPEN_ENDED_WITNESS_CHAIN_IS_DECLARED_NOT_CLOSED: الدالُّ مسنودٌ إلى "
    "البايتات وحدَها، ولا يُصادِق عقدٌ على اللغة فيدور الدور؛ فالدرجةُ الثالثة "
    "مُصرَّحةٌ بحدّها لا مُشغَّلة، ولا يُصطنَع لها حارسٌ يُوهِم إغلاقَ ما لا يُغلَق"
)

NO_FIGURE_CROSSES_FROM_THE_EXPORTER_INTO_THIS_TREE: Final[str] = (
    "NO_FIGURE_CROSSES_FROM_THE_EXPORTER_INTO_THIS_TREE: لا عددَ أختامٍ ولا "
    "عددَ فواتيرَ ولا نسبةَ تُكتَب ههنا؛ فرقمٌ يُنقَل مكتوبًا بدل موضعه هو "
    "عينُ ما يُسقِط القرارَ لا الرقم، والأحكامُ ههنا أسماءٌ ومواضعُ وحال"
)

GRADUATION_EXAM_NAMED_RESIDUALS: Final[dict[str, str]] = {
    "THIS_MODULE_IS_THE_ABSENCE_GUARD_NOT_THE_BUILDER": (
        THIS_MODULE_IS_THE_ABSENCE_GUARD_NOT_THE_BUILDER
    ),
    "THE_DEPOSITED_COPY_IS_REFUSED_BY_ITS_OWN_SHAPE_NOT_BY_ITS_DATE": (
        THE_DEPOSITED_COPY_IS_REFUSED_BY_ITS_OWN_SHAPE_NOT_BY_ITS_DATE
    ),
    "A_GUARD_WRITTEN_AFTER_ITS_BUILDER_IS_CUT_TO_ITS_SHAPE": (
        A_GUARD_WRITTEN_AFTER_ITS_BUILDER_IS_CUT_TO_ITS_SHAPE
    ),
    "THE_OPEN_ENDED_WITNESS_CHAIN_IS_DECLARED_NOT_CLOSED": (
        THE_OPEN_ENDED_WITNESS_CHAIN_IS_DECLARED_NOT_CLOSED
    ),
    "NO_FIGURE_CROSSES_FROM_THE_EXPORTER_INTO_THIS_TREE": (
        NO_FIGURE_CROSSES_FROM_THE_EXPORTER_INTO_THIS_TREE
    ),
}
"""البقايا المسمّاةُ لهذه الوحدة، تُقرأ بأسمائها ولا تُطوى في نثر."""


# --- الشرطُ الثاني: النسخةُ المودَعةُ ليست المادّة -------------------------


@dataclass(frozen=True, slots=True)
class DepositedCopyReading:
    """قراءةُ النسخة المودَعة: أتحمل صنفَ المادّة أم لا، وبأيّ أصنافٍ جاءت."""

    relative_path: str
    classes_present: tuple[str, ...]
    carries_the_material_class: bool

    @property
    def is_refused_as_material(self) -> bool:
        """امتناعُها مادّةً مقروءٌ من بنيتها: لا ختمَ من صنف المادّة فيها."""

        return not self.carries_the_material_class


def repository_root_path() -> Path:
    """جذرُ المستودع، مُشتقًّا من موضع هذه الوحدة لا مكتوبًا."""

    return Path(__file__).resolve().parents[3]


def read_deposited_copy(root: Path | None = None) -> DepositedCopyReading:
    """قراءةُ المودَع من القرص؛ أصنافُ أختامه تُشتَقّ ولا تُكتَب ههنا."""

    base = repository_root_path() if root is None else root
    path = base / _THE_DEPOSITED_COPY_PATH
    if not path.is_file():
        raise GraduationExamReadinessError(
            f"المعروضُ المُسمّى غائبٌ عن القرص: {_THE_DEPOSITED_COPY_PATH}"
        )
    loaded = json.loads(path.read_text(encoding="utf-8"))
    register = loaded.get(_THE_REGISTER_KEY)
    if not isinstance(register, dict):
        raise GraduationExamReadinessError("سجلُّ الأختام لا يُقرأ خريطةً مسمّاة.")
    seals = register.get(_THE_SEALS_KEY)
    if not isinstance(seals, list):
        raise GraduationExamReadinessError("أختامُ المعروض لا تُقرأ قائمةً.")
    classes = tuple(
        sorted(
            {
                str(seal.get(_THE_CLASS_KEY))
                for seal in seals
                if isinstance(seal, dict) and seal.get(_THE_CLASS_KEY) is not None
            }
        )
    )
    return DepositedCopyReading(
        relative_path=_THE_DEPOSITED_COPY_PATH,
        classes_present=classes,
        carries_the_material_class=EXAM_MATERIAL_SEAL_CLASS in classes,
    )


# --- الشرطُ الأوّل: حارسُ الغياب على البانِي --------------------------------


@dataclass(frozen=True, slots=True)
class SourceTouch:
    """مسَّةٌ واحدةٌ لنصّ المصدر، مُسمّاةً بموضعها في نصّ البانِي."""

    call_name: str
    line: int
    reason: str


def source_touches_in(builder_source: str) -> tuple[SourceTouch, ...]:
    """مسّاتُ البانِي لنصّ المصدر، مُشتَقّةً من شجرته لا من بحثٍ نصّيّ."""

    try:
        tree = ast.parse(builder_source)
    except SyntaxError as error:  # pragma: no cover - نصٌّ لا يُحلَّل
        raise GraduationExamReadinessError("نصُّ البانِي لا يُحلَّل شجرةً.") from error

    touches: list[SourceTouch] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = _called_name(node.func)
        if name is None:
            continue
        if name in _SOURCE_EXTRACTING_NAMES:
            touches.append(
                SourceTouch(
                    call_name=name,
                    line=node.lineno,
                    reason="استخراجُ شيفرةٍ أو تحليلُها شجرةً مسٌّ لنصّ المصدر",
                )
            )
            continue
        if name in _FILE_READING_NAMES and _reads_a_source_file(node):
            touches.append(
                SourceTouch(
                    call_name=name,
                    line=node.lineno,
                    reason=f"فتحُ ملفٍّ بامتداد `{_SOURCE_READING_SUFFIX}` قراءةً",
                )
            )
    return tuple(touches)


def _called_name(func: ast.expr) -> str | None:
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        return func.attr
    return None


def _reads_a_source_file(node: ast.Call) -> bool:
    for literal in _string_literals_under(node):
        if literal.endswith(_SOURCE_READING_SUFFIX):
            return True
    return False


def _string_literals_under(node: ast.AST) -> tuple[str, ...]:
    return tuple(
        child.value
        for child in ast.walk(node)
        if isinstance(child, ast.Constant) and isinstance(child.value, str)
    )


def exporter_is_present_at_its_place(checkout: Path | None = None) -> bool:
    """أحاضرٌ المُصدِّرُ في موضعه؟ ولا يُقبَل موضعٌ داخلَ هذه الشجرة أصلًا."""

    if checkout is None:
        return False
    resolved = checkout.resolve()
    if resolved.is_relative_to(repository_root_path()):
        raise GraduationExamReadinessError(
            "موضعُ المُصدِّر لا يقع داخلَ هذه الشجرة: ما ههنا نسخةٌ لا موضع."
        )
    return (resolved / THE_EXPORTER_OUTPUT_RELATIVE_PATH).is_file()


# --- الدرجاتُ وأوّلُ غيرِ مستوفاة -------------------------------------------


def the_rung_readings(
    checkout: Path | None = None,
) -> tuple[tuple[ExamRung, RungStanding], ...]:
    """حالُ كلّ درجة؛ وما بعد أوّلِ غيرِ مستوفاةٍ `غيرُ منظورٍ فيها` لا مستوفاة."""

    readings: list[tuple[ExamRung, RungStanding]] = []
    stopped = False
    for rung in THE_RUNG_ORDER:
        if stopped:
            readings.append((rung, RungStanding.غير_منظور_فيها))
            continue
        if _is_met(rung, checkout):
            readings.append((rung, RungStanding.مستوفاة))
            continue
        readings.append((rung, RungStanding.غير_مستوفاة))
        stopped = True
    return tuple(readings)


def _is_met(rung: ExamRung, checkout: Path | None) -> bool:
    if rung is ExamRung.EXPORTER_PRESENT_AT_ITS_PLACE:
        return exporter_is_present_at_its_place(checkout)
    return False


def the_first_unmet_rung(checkout: Path | None = None) -> ExamRung | None:
    """أوّلُ درجةٍ غيرِ مستوفاة، وهي بابُ الامتحان؛ و`None` إن استُوفِيت كلُّها."""

    for rung, standing in the_rung_readings(checkout):
        if standing is RungStanding.غير_مستوفاة:
            return rung
    return None


if len(ExamRung) != 3:  # pragma: no cover - guard
    raise RuntimeError("شروطُ غياب القرار `٧` ثلاثةٌ كما أُعلِنت، لا تزيد ولا تنقص.")
if len(THE_RUNG_ORDER) != len(ExamRung):  # pragma: no cover - guard
    raise RuntimeError("كلُّ درجةٍ مُعلَنةٍ لها موضعٌ في الترتيب، ولا درجةَ مهمَلة.")
if len(RungStanding) != 3:  # pragma: no cover - guard
    raise RuntimeError("حالُ الدرجة ثلاثيةٌ مغلقة: مستوفاة، وغيرُها، وغيرُ منظورٍ فيها.")
