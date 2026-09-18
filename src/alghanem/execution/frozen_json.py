"""`G0.CASE-0.DATA-H`: تجميدٌ عميقٌ لوثائق المدوّنة، وفرقٌ بنيويٌّ بين نصّين.

    FrozenData  ≺  Readout

**والوثيقةُ المجمَّدةُ لا تُحوَّر** (`AFrozenDocumentIsDeeplyImmutable`): تجميدُ
`dataclass` لا يجمّد قاموسًا داخله ولا قوائمَه المتداخلة؛ فمن أمسك بالقاموس
بعد بناء المدوّنة غيَّرها وهي «مجمَّدةٌ» بالاسم. ولذلك تُحفَظ الوثيقةُ محتوًى
مجمَّدًا تجميدًا متعدِّيًا — كائنٌ لا يُكتَب فيه، وقائمةٌ صارت `tuple` — وتُشتَقّ
نسخةٌ جديدةٌ عند كلّ قراءة، كما يفعل غلافُ النتيجة بتصريحه.

**والفرقُ عمليّةٌ لا موضع** (`ADifferenceIsAnOperationNotAPath`):

    StructuralDiff  =  operation ∈ {ADD, REMOVE, REPLACE}  ×  path
                       ×  before  ×  after

فزيادةُ مرتكزٍ `ADD nisbah.anchors[1]`، وحذفُه `REMOVE nisbah.anchors[1]`،
وتغيُّرُ قائمٍ `REPLACE nisbah.predicate.arity`؛ ولا يُقال «طولُ القائمة تغيَّر»
فيُضغَط فرقان في موضعٍ أبٍ غامض. وإن تغيَّر عنصرٌ قائمٌ وزِيد آخرُ فهما فرقان
مستقلّان لا فرقٌ واحد.

**وهذا الفرقُ يُقاس بين نصّين مؤلَّفين** لا يُنتِجه المحرّك؛ فلا يخرق
`DATA ≺ READOUT` ولا يفتح بابًا إلى بصمة تنفيذ.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from enum import Enum
from types import MappingProxyType
from typing import Any, Final, TypeAlias

__all__ = [
    "A_DIFFERENCE_IS_AN_OPERATION_NOT_A_PATH",
    "A_FROZEN_DOCUMENT_IS_DEEPLY_IMMUTABLE",
    "DiffOperation",
    "FrozenJson",
    "FrozenJsonError",
    "StructuralDiff",
    "freeze_json",
    "frozen_equal",
    "join_path",
    "structural_diff",
    "thaw_json",
]


FrozenJson: TypeAlias = (
    "None | bool | int | float | str "
    "| tuple[FrozenJson, ...] | Mapping[str, FrozenJson]"
)
"""قيمةٌ مجمَّدةٌ تجميدًا متعدِّيًا: قياسٌ، أو `tuple`، أو كائنٌ لا يُكتَب فيه."""


A_FROZEN_DOCUMENT_IS_DEEPLY_IMMUTABLE: Final[str] = (
    "الوثيقةُ المجمَّدةُ لا تُحوَّر: تجميدُ الكائن لا يجمّد قاموسًا داخله، "
    "فتُحفَظ الوثيقةُ محتوًى مجمَّدًا متعدِّيًا وتُشتَقّ نسخةٌ جديدةٌ عند كلّ قراءة؛ "
    "ومن أمسك بقاموسٍ مشترَكٍ غيَّر البياناتِ بعد تجميدها"
)

A_DIFFERENCE_IS_AN_OPERATION_NOT_A_PATH: Final[str] = (
    "الفرقُ عمليّةٌ لا موضع: زيادةٌ أو حذفٌ أو إبدالٌ في موضعٍ مُسمًّى، بحالته "
    "قبلَه وبعدَه؛ ومن اكتفى بالموضع وصف تغييرًا غيرَ الذي وقع"
)


class FrozenJsonError(ValueError):
    """رفضٌ عند تجميد قيمةٍ خارج عقد `JSON`؛ لا حملَ على أقرب صورةٍ مقبولة."""


class DiffOperation(Enum):
    """أجناسُ الفرق البنيويّ؛ مفردةٌ مغلقةٌ لا رابعَ لها."""

    ADD = "add"
    REMOVE = "remove"
    REPLACE = "replace"


def freeze_json(value: object, label: str) -> FrozenJson:
    """جمّدْ قيمةَ `JSON` تجميدًا متعدِّيًا؛ وما خرج عن العقد يُردّ لا يُحمَل."""

    if value is None:
        return None
    if isinstance(value, bool | int | float | str):
        return value
    if isinstance(value, Mapping):
        frozen: dict[str, FrozenJson] = {}
        for key, nested in value.items():
            if not isinstance(key, str):
                raise FrozenJsonError(f"{label}: مفتاحُ الكائن نصٌّ لا غير")
            frozen[key] = freeze_json(nested, f"{label}.{key}")
        return MappingProxyType(frozen)
    if isinstance(value, Sequence) and not isinstance(value, str | bytes):
        return tuple(
            freeze_json(item, f"{label}[{index}]") for index, item in enumerate(value)
        )
    raise FrozenJsonError(
        f"{label}: قيمةٌ خارج عقد `JSON`: {type(value).__name__}؛ و"
        + A_FROZEN_DOCUMENT_IS_DEEPLY_IMMUTABLE
    )


def thaw_json(value: FrozenJson) -> Any:
    """اشتُقَّ نسخةً جديدةً قابلةً للقراءة؛ فلا نسخةَ مشتركةٌ تُعدَّل عند القارئ."""

    if isinstance(value, Mapping):
        return {key: thaw_json(nested) for key, nested in value.items()}
    if isinstance(value, tuple):
        return [thaw_json(item) for item in value]
    return value


def frozen_equal(left: FrozenJson, right: FrozenJson) -> bool:
    """أهما قيمةٌ واحدة؟ والنوعُ من المطابقة، فلا يُقرَأ `True` عددًا ولا العكس."""

    if isinstance(left, Mapping) or isinstance(right, Mapping):
        if not (isinstance(left, Mapping) and isinstance(right, Mapping)):
            return False
        if set(left) != set(right):
            return False
        return all(frozen_equal(left[key], right[key]) for key in left)
    if isinstance(left, tuple) or isinstance(right, tuple):
        if not (isinstance(left, tuple) and isinstance(right, tuple)):
            return False
        if len(left) != len(right):
            return False
        return all(frozen_equal(first, second) for first, second in zip(left, right))
    if left is None or right is None:
        return left is None and right is None
    if type(left) is not type(right):
        return False
    return bool(left == right)


def join_path(path: str, step: str) -> str:
    """اسمُ الموضع: مفاتيحُ منقوطةٌ، ومواضعُ القوائم بين قوسين."""

    if step.startswith("["):
        return f"{path}{step}"
    return step if not path else f"{path}.{step}"


@dataclass(frozen=True, slots=True)
class StructuralDiff:
    """فرقٌ بنيويٌّ واحد: عمليّتُه، وموضعُه، وما كان، وما صار."""

    operation: DiffOperation
    path: str
    before: FrozenJson
    after: FrozenJson

    def __post_init__(self) -> None:
        if not isinstance(self.operation, DiffOperation):
            raise FrozenJsonError("عمليّةُ الفرق عضوٌ في مفردتها المغلقة")
        if not isinstance(self.path, str) or not self.path.strip():
            raise FrozenJsonError("موضعُ الفرق نصٌّ غير فارغ")


def structural_diff(
    before: FrozenJson, after: FrozenJson, path: str = ""
) -> tuple[StructuralDiff, ...]:
    """الفرقُ الحقيقيُّ بين نصّين مؤلَّفين، عمليّاتٍ مرتَّبةً لا مواضعَ مجرَّدة."""

    if isinstance(before, Mapping) and isinstance(after, Mapping):
        return _mapping_diff(before, after, path)
    if isinstance(before, tuple) and isinstance(after, tuple):
        return _sequence_diff(before, after, path)
    if frozen_equal(before, after):
        return ()
    return (
        StructuralDiff(
            operation=DiffOperation.REPLACE,
            path=path or _ROOT_PATH,
            before=before,
            after=after,
        ),
    )


_ROOT_PATH: Final[str] = "."
"""موضعُ الجذر حين يختلف النصّان في أصلهما لا في موضعٍ منهما."""


def _mapping_diff(
    before: Mapping[str, FrozenJson], after: Mapping[str, FrozenJson], path: str
) -> tuple[StructuralDiff, ...]:
    differences: list[StructuralDiff] = []
    for key in sorted(set(before) | set(after)):
        here = join_path(path, key)
        if key not in after:
            differences.append(
                StructuralDiff(
                    operation=DiffOperation.REMOVE,
                    path=here,
                    before=before[key],
                    after=None,
                )
            )
        elif key not in before:
            differences.append(
                StructuralDiff(
                    operation=DiffOperation.ADD,
                    path=here,
                    before=None,
                    after=after[key],
                )
            )
        else:
            differences.extend(structural_diff(before[key], after[key], here))
    return tuple(differences)


def _sequence_diff(
    before: tuple[FrozenJson, ...], after: tuple[FrozenJson, ...], path: str
) -> tuple[StructuralDiff, ...]:
    differences: list[StructuralDiff] = []
    shared = min(len(before), len(after))
    for index in range(shared):
        differences.extend(
            structural_diff(before[index], after[index], f"{path}[{index}]")
        )
    for index in range(shared, len(before)):
        differences.append(
            StructuralDiff(
                operation=DiffOperation.REMOVE,
                path=f"{path}[{index}]",
                before=before[index],
                after=None,
            )
        )
    for index in range(shared, len(after)):
        differences.append(
            StructuralDiff(
                operation=DiffOperation.ADD,
                path=f"{path}[{index}]",
                before=None,
                after=after[index],
            )
        )
    return tuple(differences)
