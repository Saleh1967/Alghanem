"""خريطةُ المفاهيم الكلاسيكية ببنى الكيرنل (§8 من G0.N).

كلّ صفٍّ يحمل سندَه من مفردةٍ مغلقة، ووجودُ البنية المُسمّاة في الشيفرة يُقرأ
من الشجرة لا يُكتَب؛ فالصفُّ الذي لا بنيةَ له يُرفَض إن ادّعى سندًا أعلى من
`مُصرَّح_غير_مُتحقَّق`.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, fields
from enum import Enum
from pathlib import Path
from typing import Final

__all__ = [
    "ABSENT_STRUCTURE_NOTE",
    "CLASSICAL_KERNEL_MAP_IS_NOT_A_GATE_NOTE",
    "KERNEL_PACKAGE_RELATIVE_PATH",
    "TRANSLATION_IS_NOT_TRANSMISSION_NOTE",
    "ClassicalKernelMapError",
    "MapRow",
    "MapRowReading",
    "MapSanad",
    "kernel_symbol_names",
    "read_map",
]


class ClassicalKernelMapError(ValueError):
    """رفضٌ صريحٌ في خريطة المفاهيم الكلاسيكية."""


class MapSanad(Enum):
    """سندُ الصفّ؛ مفردةٌ مغلقةٌ ثلاثية لا رابعَ لها."""

    مُشتقّ_من_الشيفرة = "مُشتقّ_من_الشيفرة"
    اجتهاد_ترجمة = "اجتهاد_ترجمة"
    مُصرَّح_غير_مُتحقَّق = "مُصرَّح_غير_مُتحقَّق"


KERNEL_PACKAGE_RELATIVE_PATH: Final[str] = "src/alghanem/kernel"

TRANSLATION_IS_NOT_TRANSMISSION_NOTE: Final[str] = (
    "مقابلةُ مفهومٍ كلاسيكيٍّ ببنيةٍ في الشيفرة اجتهادُ ترجمةٍ لا نقلٌ عن "
    "أحد: تسميةُ الصفّ `مُشتقّ_من_الشيفرة` لا تعني أن القدماء قصدوا هذه "
    "البنية، بل أن البنيةَ المُسمّاة قائمةٌ في الشجرة فعلاً."
)

ABSENT_STRUCTURE_NOTE: Final[str] = (
    "بنيةٌ غيرُ قائمةٍ في الشجرة لا تُسنِد صفًّا: سندُها `مُصرَّح_غير_مُتحقَّق` "
    "لا غير، وادّعاءُ الاشتقاق من شيفرةٍ لا وجودَ لها ادّعاءُ قراءةٍ لم تجرِ."
)

CLASSICAL_KERNEL_MAP_IS_NOT_A_GATE_NOTE: Final[str] = (
    "الخريطةُ قراءةٌ لا سلطة: لا تُصدر ولادةً ولا تجميدًا ولا `E0`، ولا "
    "تستورد من `kernel/` شيئًا، ولا تقرؤها وحدةٌ فيه."
)

_DECLARED_ROWS: Final[tuple[tuple[str, str, MapSanad], ...]] = (
    ("الحامل", "Carrier", MapSanad.مُصرَّح_غير_مُتحقَّق),
    ("الحال", "State", MapSanad.اجتهاد_ترجمة),
    ("الوجود", "StructuralDecisionStatus", MapSanad.مُشتقّ_من_الشيفرة),
    ("الكنه والصفة", "InvariantSpec", MapSanad.اجتهاد_ترجمة),
    ("الرتبة", "InvariantVerificationDecision", MapSanad.اجتهاد_ترجمة),
    ("العلة", "WeakerModelSpec", MapSanad.اجتهاد_ترجمة),
    ("البقيةُ الناجية", "ResidualSurvivalCertificate", MapSanad.مُشتقّ_من_الشيفرة),
    (
        "التجميد",
        "FrozenPreEvidenceExperimentManifest",
        MapSanad.مُشتقّ_من_الشيفرة,
    ),
    ("سلسلةُ السند", "SealedInvariantExtractorRegistry", MapSanad.مُشتقّ_من_الشيفرة),
    ("بصمةُ تعريف الظاهرة", "TransitionContentIdentity", MapSanad.مُشتقّ_من_الشيفرة),
    (
        "استنفادُ الأضعف",
        "WeakerModelExhaustionAssessment",
        MapSanad.اجتهاد_ترجمة,
    ),
    ("الحكم", "BirthVerdictGate", MapSanad.مُشتقّ_من_الشيفرة),
)

_DEFINITION_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"^(?:class|def)\s+([A-Za-z_][A-Za-z0-9_]*)", re.MULTILINE
)


def repository_root_path() -> Path:
    """جذرُ المستودع، مُشتقًّا من موضع هذه الوحدة لا مكتوبًا."""

    return Path(__file__).resolve().parents[3]


def kernel_symbol_names(root: Path | None = None) -> frozenset[str]:
    """أسماءُ البنى المُعرَّفة في `kernel/`، مقروءةً من الشجرة لا مستورَدة."""

    base = repository_root_path() if root is None else root
    if not isinstance(base, Path):
        raise ClassicalKernelMapError("جذرُ المستودع مسار.")
    package = base / KERNEL_PACKAGE_RELATIVE_PATH
    if not package.is_dir():
        raise ClassicalKernelMapError(
            f"طبقةُ الكيرنل غير موجودة عند {package}: شجرةٌ غائبةٌ تُقرأ «لا "
            "بنى» وهو ادّعاءٌ لم تُقرأ الشجرة لأجله."
        )
    names: set[str] = set()
    for item in sorted(package.iterdir()):
        if item.is_file() and item.suffix == ".py":
            names.update(_DEFINITION_PATTERN.findall(item.read_text(encoding="utf-8")))
    return frozenset(names)


@dataclass(frozen=True, slots=True)
class MapRow:
    """صفٌّ واحد: مفهومٌ كلاسيكيّ، وبنيةٌ مُسمّاة، وسندُ المقابلة."""

    classical_concept: str
    kernel_symbol: str
    sanad: MapSanad

    def __post_init__(self) -> None:
        for name in ("classical_concept", "kernel_symbol"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ClassicalKernelMapError(f"{name} نصٌّ غير فارغ.")
        if not isinstance(self.sanad, MapSanad):
            raise ClassicalKernelMapError("سندُ الصفّ من مفردته المغلقة الثلاثية.")


@dataclass(frozen=True, slots=True)
class MapRowReading:
    """قراءةُ صفٍّ: إعلانُه، ووجودُ بنيته في الشجرة، ومطابقةُ سنده لذلك."""

    row: MapRow
    structure_present: bool

    def __post_init__(self) -> None:
        if not isinstance(self.row, MapRow):
            raise ClassicalKernelMapError("الصفُّ صفٌّ مُصاغ.")
        if not isinstance(self.structure_present, bool):
            raise ClassicalKernelMapError("وجودُ البنية قيمةٌ ثنائيةٌ مُشتقّة.")
        if not self.structure_present and self.row.sanad is not (
            MapSanad.مُصرَّح_غير_مُتحقَّق
        ):
            raise ClassicalKernelMapError(ABSENT_STRUCTURE_NOTE)
        if self.structure_present and self.row.sanad is MapSanad.مُصرَّح_غير_مُتحقَّق:
            raise ClassicalKernelMapError(
                "بنيةٌ قائمةٌ في الشجرة لا تُسجَّل «مُصرَّحًا غير مُتحقَّق»: "
                "التحقّقُ من وجودها جرى فعلاً."
            )

    @property
    def is_verified_against_the_tree(self) -> bool:
        return self.structure_present


def read_map(root: Path | None = None) -> tuple[MapRowReading, ...]:
    """اقرأ صفوفَ الخريطة الاثني عشر، مُشتقًّا وجودَ كلّ بنيةٍ من الشجرة."""

    present = kernel_symbol_names(root)
    return tuple(
        MapRowReading(
            row=MapRow(
                classical_concept=concept,
                kernel_symbol=symbol,
                sanad=sanad,
            ),
            structure_present=symbol in present,
        )
        for concept, symbol, sanad in _DECLARED_ROWS
    )


def _assert_no_fields_matching(markers: tuple[str, ...]) -> None:
    for declaring_type in (MapRow, MapRowReading):
        for field in fields(declaring_type):
            for marker in markers:
                if marker in field.name:
                    raise RuntimeError(
                        f"{declaring_type.__name__} يحمل حقلاً محظورًا: {field.name}"
                    )


if len(MapSanad) != 3:
    raise RuntimeError("سندُ الصفّ ثلاثيٌّ مغلق.")
if len(_DECLARED_ROWS) != 12:
    raise RuntimeError("صفوفُ الخريطة اثنا عشرَ صفًّا.")
if len({row[0] for row in _DECLARED_ROWS}) != len(_DECLARED_ROWS):
    raise RuntimeError("مفهومٌ كلاسيكيٌّ مُعادٌ ليس صفًّا ثانيًا.")
if len({row[1] for row in _DECLARED_ROWS}) != len(_DECLARED_ROWS):
    raise RuntimeError("بنيةٌ مُعادةٌ ليست صفًّا ثانيًا.")
_assert_no_fields_matching(("count", "number", "total", "verdict", "birth"))
