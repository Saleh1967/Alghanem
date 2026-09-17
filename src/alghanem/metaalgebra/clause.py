"""الفصلُ النوعيّ بين البند التصريحيّ والبند القابل للتنفيذ.

    DeclarativeClause  ≠  ExecutableClause

**والسببُ ليس تنظيميًّا:** مولِّدٌ يقرأ نصًّا نثريًّا ثمّ يُخرِج دالّةً يكون قد
اخترع دلالةً لم تُعطَ له؛ فإمّا أن يكون التوليدُ مكتوبًا يدويًّا خلف الستار،
وإمّا أن يكون توليدًا زائفًا. والفصلُ هنا **نوعيٌّ لا سمةٌ منطقيّةٌ في صنفٍ
واحد**، حتّى لا يُقرأ النثرُ تنفيذًا بالسهو (`NO_SEMANTICS_FROM_PROSE`).

فالبندُ التصريحيُّ التزامٌ يُقرأ ولا يُترجَم، ويصرّح **لماذا** لا يُترجَم؛
والبندُ القابلُ للتنفيذ شجرةُ تعبيرٍ من مفردةٍ مغلقة:

    And, Or, Not, Eq, MemberOf, FieldRef, Constant, PartialApply

ومن هذه وحدَها يجوز لمولِّدٍ أن يُخرِج محمولًا مُشغَّلًا؛ وما عداها يخرج عقدًا
مؤجَّلًا صريحًا، لا دالّةً مُخترَعة.

تسجيلٌ لا سلطة: لا حكمَ في صنفٍ هنا، ولا استيرادَ من `kernel/` ولا من `arabic/`
ولا من حزمة التوليد.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest

__all__ = [
    "AN_EXECUTABLE_CLAUSE_IS_NOT_A_PROMISE_OF_TRUTH",
    "EXECUTABLE_NODE_NAMES",
    "NO_SEMANTICS_FROM_PROSE",
    "And",
    "Clause",
    "ClauseError",
    "Constant",
    "DeclarativeClause",
    "Eq",
    "ExecutableClause",
    "Expression",
    "FieldRef",
    "MemberOf",
    "Not",
    "Or",
    "PartialApply",
    "require_clause",
]


class ClauseError(ValueError):
    """رفضٌ عند الإنشاء: نثرٌ يُقدَّم تعبيرًا، أو عقدةٌ خارج المفردة المغلقة."""


NO_SEMANTICS_FROM_PROSE: Final[str] = (
    "لا دلالةَ تنفيذيّةً تُشتَقّ من نثر: بندٌ بلا شجرةِ تعبيرٍ يخرج عقدًا مؤجَّلًا "
    "مُسمًّى، ولا يخترع المولِّدُ معناه"
)

AN_EXECUTABLE_CLAUSE_IS_NOT_A_PROMISE_OF_TRUTH: Final[str] = (
    "قابليّةُ البند للتنفيذ وصفٌ لصورته لا شهادةٌ بصحّته: تعبيرٌ مُترجَمٌ قد يكون "
    "خاطئًا، والترجمةُ لا تمنحه منزلةً"
)

EXECUTABLE_NODE_NAMES: Final[tuple[str, ...]] = (
    "And",
    "Or",
    "Not",
    "Eq",
    "MemberOf",
    "FieldRef",
    "Constant",
    "PartialApply",
)
"""مفردةُ عقد التعبير المغلقة؛ ولا تاسعَ لها إلّا بتعديلٍ في لغة الجبر نفسِها."""


def _require_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ClauseError(f"{label} نصٌّ غير فارغ")
    return value


@dataclass(frozen=True, slots=True)
class DeclarativeClause:
    """بندٌ تصريحيّ: التزامٌ يُقرأ ولا يُترجَم، ومعه سببُ عدم قابليّته للترجمة.

    و`why_not_executable` شرطُ إنشاءٍ لا زينة: بندٌ لا يقول لماذا بقي نثرًا
    يُقرأ يومًا نقصَ اجتهادٍ في المولِّد، لا حدًّا مُصرَّحًا به في المواصفة.
    """

    clause_id: str
    clause_text: str
    why_not_executable: str

    def __post_init__(self) -> None:
        _require_text(self.clause_id, "اسمُ البند")
        _require_text(self.clause_text, "نصُّ البند")
        _require_text(self.why_not_executable, "سببُ بقاء البند نثرًا")

    @property
    def is_executable(self) -> bool:
        """تصريحٌ مُشتَقٌّ لا حقلٌ يُكتَب؛ وهو هنا `False` دائمًا بالنوع."""

        return False

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى البند للبصمة."""

        return {
            "clause_kind": "declarative",
            "clause_id": self.clause_id,
            "clause_text": self.clause_text,
            "why_not_executable": self.why_not_executable,
        }


@dataclass(frozen=True, slots=True)
class Constant:
    """قيمةٌ ثابتةٌ في التعبير: نصٌّ أو عددٌ أو منطقيّةٌ لا غير."""

    value: str | int | bool

    def __post_init__(self) -> None:
        if not isinstance(self.value, str | int | bool):
            raise ClauseError("الثابتُ نصٌّ أو عددٌ صحيحٌ أو منطقيّة")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الثابت للبصمة."""

        return {"node": "Constant", "value": self.value}


@dataclass(frozen=True, slots=True)
class FieldRef:
    """إشارةٌ إلى موضعٍ في المُدخَل: مسارٌ من أسماءٍ لا تعبيرٌ نصّيٌّ يُفسَّر."""

    path: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.path, tuple) or not self.path:
            raise ClauseError("مسارُ الحقل مجموعةُ أسماءٍ غير فارغة")
        for part in self.path:
            _require_text(part, "جزءٌ في مسار الحقل")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الإشارة للبصمة."""

        return {"node": "FieldRef", "path": list(self.path)}


@dataclass(frozen=True, slots=True)
class Eq:
    """تساوي تعبيرين."""

    left: Expression
    right: Expression

    def __post_init__(self) -> None:
        _require_expression(self.left, "الطرفُ الأيسر")
        _require_expression(self.right, "الطرفُ الأيمن")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى التساوي للبصمة."""

        return {
            "node": "Eq",
            "left": self.left.as_canonical_content(),
            "right": self.right.as_canonical_content(),
        }


@dataclass(frozen=True, slots=True)
class MemberOf:
    """عضويّةُ تعبيرٍ في مجموعةِ ثوابتَ مُصرَّحٍ بها."""

    element: Expression
    members: tuple[Constant, ...]

    def __post_init__(self) -> None:
        _require_expression(self.element, "العنصرُ المفحوص")
        if not isinstance(self.members, tuple) or not self.members:
            raise ClauseError("مجموعةُ العضويّة غير فارغة")
        for member in self.members:
            if not isinstance(member, Constant):
                raise ClauseError("عضوٌ في مجموعة العضويّة ثابتٌ لا تعبيرٌ مركّب")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى العضويّة للبصمة."""

        return {
            "node": "MemberOf",
            "element": self.element.as_canonical_content(),
            "members": [member.as_canonical_content() for member in self.members],
        }


@dataclass(frozen=True, slots=True)
class Not:
    """نفيُ تعبير."""

    operand: Expression

    def __post_init__(self) -> None:
        _require_expression(self.operand, "معمولُ النفي")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى النفي للبصمة."""

        return {"node": "Not", "operand": self.operand.as_canonical_content()}


@dataclass(frozen=True, slots=True)
class And:
    """اقترانُ تعبيرين فأكثر."""

    operands: tuple[Expression, ...]

    def __post_init__(self) -> None:
        _require_operands(self.operands, "معمولاتُ الاقتران")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الاقتران للبصمة."""

        return {
            "node": "And",
            "operands": [item.as_canonical_content() for item in self.operands],
        }


@dataclass(frozen=True, slots=True)
class Or:
    """فصلُ تعبيرين فأكثر."""

    operands: tuple[Expression, ...]

    def __post_init__(self) -> None:
        _require_operands(self.operands, "معمولاتُ الفصل")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الفصل للبصمة."""

        return {
            "node": "Or",
            "operands": [item.as_canonical_content() for item in self.operands],
        }


@dataclass(frozen=True, slots=True)
class PartialApply:
    """تطبيقُ عمليةٍ جزئيّةٍ مُسمّاةٍ على وسائطَ مُصرَّحٍ بها.

    والاسمُ إشارةٌ إلى عمليةٍ مُعلَنةٍ في الطبقة، لا استدعاءُ دالّةٍ عشوائيّة؛
    فالمولِّدُ يربطه بما وُلِّد لتلك العملية، ولا يبحث عنه في فضاء الأسماء.
    """

    operation_id: str
    arguments: tuple[Expression, ...]

    def __post_init__(self) -> None:
        _require_text(self.operation_id, "اسمُ العملية المُطبَّقة")
        if not isinstance(self.arguments, tuple):
            raise ClauseError("وسائطُ التطبيق مجموعةٌ مُصرَّحٌ بها")
        for argument in self.arguments:
            _require_expression(argument, "وسيطٌ في التطبيق")

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى التطبيق للبصمة."""

        return {
            "node": "PartialApply",
            "operation_id": self.operation_id,
            "arguments": [item.as_canonical_content() for item in self.arguments],
        }


Expression = And | Constant | Eq | FieldRef | MemberOf | Not | Or | PartialApply
"""عقدُ التعبير مفردةً مغلقة؛ وما خرج عنها يُرفَض عند الإنشاء لا عند التوليد."""

_EXPRESSION_TYPES: Final[tuple[type, ...]] = (
    And,
    Constant,
    Eq,
    FieldRef,
    MemberOf,
    Not,
    Or,
    PartialApply,
)


def _require_expression(value: object, label: str) -> None:
    if not isinstance(value, _EXPRESSION_TYPES):
        raise ClauseError(
            f"{label} عقدةُ تعبيرٍ من المفردة المغلقة؛ و{NO_SEMANTICS_FROM_PROSE}"
        )


def _require_operands(value: object, label: str) -> None:
    if not isinstance(value, tuple) or len(value) < 2:
        raise ClauseError(f"{label} معمولان فأكثر؛ ومعمولٌ واحدٌ ليس تركيبًا")
    for item in value:
        _require_expression(item, f"عنصرٌ في {label}")


@dataclass(frozen=True, slots=True)
class ExecutableClause:
    """بندٌ قابلٌ للتنفيذ: شجرةُ تعبيرٍ تُترجَم، لا نصٌّ يُفسَّر.

    و`clause_text` وصفٌ عربيٌّ مرافقٌ للقراءة؛ **والتعبيرُ هو المصدر**، فإن
    اختلفا فالتعبيرُ هو المُنفَّذ، والوصفُ لا يُترجَم بحال.
    """

    clause_id: str
    clause_text: str
    expression: Expression

    def __post_init__(self) -> None:
        _require_text(self.clause_id, "اسمُ البند")
        _require_text(self.clause_text, "وصفُ البند")
        _require_expression(self.expression, "تعبيرُ البند")

    @property
    def is_executable(self) -> bool:
        """تصريحٌ مُشتَقٌّ لا حقلٌ يُكتَب؛ وهو هنا `True` دائمًا بالنوع."""

        return True

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى البند للبصمة؛ والتعبيرُ داخلٌ فيها لا الوصفُ وحدَه."""

        return {
            "clause_kind": "executable",
            "clause_id": self.clause_id,
            "clause_text": self.clause_text,
            "expression": self.expression.as_canonical_content(),
        }

    @property
    def content_id(self) -> str:
        """بصمةُ البند القابل للتنفيذ؛ وبها يُربَط المولَّدُ بمصدره."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))


Clause = DeclarativeClause | ExecutableClause
"""البندُ اتّحادُ نوعين، لا صنفٌ واحدٌ بسمةٍ منطقيّةٍ تُقلَب."""


def require_clause(value: object, label: str) -> Clause:
    """يرفض ما ليس بندًا من النوعين؛ ونصٌّ مرسَلٌ ليس بندًا."""

    if not isinstance(value, DeclarativeClause | ExecutableClause):
        raise ClauseError(
            f"{label} بندٌ تصريحيٌّ أو قابلٌ للتنفيذ؛ و{NO_SEMANTICS_FROM_PROSE}"
        )
    return value


_JUDGEMENT_FIELD_MARKERS: Final[tuple[str, ...]] = (
    "outcome",
    "verdict",
    "status",
    "standing",
    "birth",
    "proved",
)

_CLAUSE_TYPES: Final[tuple[type, ...]] = (
    DeclarativeClause,
    ExecutableClause,
) + _EXPRESSION_TYPES

for _declaring_type in _CLAUSE_TYPES:  # pragma: no cover - import guard
    for _field in fields(_declaring_type):
        if any(marker in _field.name for marker in _JUDGEMENT_FIELD_MARKERS):
            raise RuntimeError("البندُ يحمل صورتَه لا حكمَه؛ ولا حقلَ حكمٍ فيه")

if set(EXECUTABLE_NODE_NAMES) != {
    _type.__name__ for _type in _EXPRESSION_TYPES
}:  # pragma: no cover - import guard
    raise RuntimeError("مفردةُ عقد التعبير ونوعُها مصدرٌ واحدٌ لا نسختان تنحرفان")
