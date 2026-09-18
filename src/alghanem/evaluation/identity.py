"""`G0.EVAL-0.IDENTITY`: هويّةُ النظام القارئ بصمةَ محتوًى لا اسمًا نصّيًّا.

    SystemIdentity
      =  implementation_digest
       + configuration_digest
       + dependency_boundary_digest
       + contract_interface_version

الاسمُ ينتحله برنامجٌ آخر؛ أمّا بايتاتُ مصدره وإعدادُه وحدُّ اعتماده المقيس
وإصدارُ واجهته فلا تُنتحَل. وأيُّ بايتٍ يتغيّر في مصدر قارئٍ بعد رؤية الامتحان
يُغيِّر هويّتَه، فيُكشَف التغيّرُ ولا يمرّ باسمٍ ثابت.

ولا تُجمَّد هويّةُ قارئٍ خرق حدَّ مصدره المُصرَّح: من بلغ مادّةَ الجواب أو سلطةَ
فتحه ليس قارئًا محجوبًا عنه، وسقفُ هذا الحدّ مُعلَنٌ لا مُدَّعًى.
"""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

from ..canonical_content import canonical_bytes, canonical_digest, is_canonical_digest
from ..import_boundary import ImportBoundaryReport, displayed_path
from .laws import (
    A_SYSTEM_NAME_IS_NOT_A_SYSTEM_IDENTITY,
    STATIC_IMPORT_AUDIT_IS_NOT_PROCESS_ISOLATION,
    EvaluationError,
)

__all__ = [
    "FrozenSystemIdentity",
    "SYSTEM_IDENTITY_COMPONENTS",
    "compose_system_content_id",
    "freeze_system_identity",
    "measure_configuration_digest",
    "measure_dependency_boundary_digest",
    "measure_implementation_digest",
]

SYSTEM_IDENTITY_COMPONENTS: tuple[str, ...] = (
    "implementation_digest",
    "configuration_digest",
    "dependency_boundary_digest",
    "contract_interface_version",
)
"""مكوّناتُ الهويّة الأربعة؛ تُشتَقُّ منها البصمةُ ولا يدخلها اسمٌ ولا وصف."""


def _require_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise EvaluationError(f"{label} نصٌّ غير فارغ")
    return value


def _require_digest(value: object, label: str) -> str:
    if not is_canonical_digest(value):
        raise EvaluationError(f"{label} بصمةٌ قانونيّةٌ لا نصٌّ حرّ")
    assert isinstance(value, str)
    return value


@dataclass(frozen=True, slots=True)
class FrozenSystemIdentity:
    """هويّةُ قارئٍ مُجمَّدة: أربعُ بصماتٍ، ولا اسمَ فيها يُنتحَل."""

    implementation_digest: str
    configuration_digest: str
    dependency_boundary_digest: str
    contract_interface_version: str
    implementation_files: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_digest(self.implementation_digest, "بصمةُ التنفيذ")
        _require_digest(self.configuration_digest, "بصمةُ الإعداد")
        _require_digest(self.dependency_boundary_digest, "بصمةُ حدّ الاعتماد")
        _require_text(self.contract_interface_version, "إصدارُ واجهة العقد")
        if not isinstance(self.implementation_files, tuple):
            raise EvaluationError("ملفّاتُ التنفيذ صفٌّ مُجمَّد لا قائمة")
        if not self.implementation_files:
            raise EvaluationError("هويّةُ قارئٍ بلا ملفِّ تنفيذٍ لا تُقاس")
        if len(set(self.implementation_files)) != len(self.implementation_files):
            raise EvaluationError("ملفُّ تنفيذٍ مُكرَّر؛ والمكرّرُ يُرفَض لا يُطوى")

    @property
    def identity_law(self) -> str:
        """قانونُ الهويّة: الاسمُ ليس هويّة."""

        return A_SYSTEM_NAME_IS_NOT_A_SYSTEM_IDENTITY

    @property
    def confinement_ceiling(self) -> str:
        """ما لا يجوز أن يُقرَأ حدُّ الاعتماد إثباتًا له."""

        return STATIC_IMPORT_AUDIT_IS_NOT_PROCESS_ISOLATION

    @property
    def carries_no_system_name(self) -> bool:
        """أتخلو الهويّةُ من حقل اسمٍ أو وصف؟ يُفحَص على الحقول لا بالدعوى."""

        declared = tuple(FrozenSystemIdentity.__dataclass_fields__)
        return not any(
            name in declared for name in ("system_name", "name", "label", "title")
        )

    def as_identity_content(self) -> dict[str, object]:
        """محتوى الهويّة: المكوّناتُ الأربعة وحدَها، لا ملفّاتُها ولا اسمُها."""

        return {
            "implementation_digest": self.implementation_digest,
            "configuration_digest": self.configuration_digest,
            "dependency_boundary_digest": self.dependency_boundary_digest,
            "contract_interface_version": self.contract_interface_version,
        }

    @property
    def content_id(self) -> str:
        """بصمةُ الهويّة؛ مُشتَقّةٌ من المكوّنات الأربعة لا مكتوبةً ولا مُسمّاة."""

        return compose_system_content_id(
            implementation_digest=self.implementation_digest,
            configuration_digest=self.configuration_digest,
            dependency_boundary_digest=self.dependency_boundary_digest,
            contract_interface_version=self.contract_interface_version,
        )

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الهويّة للعرض والسجلّ."""

        return {
            **self.as_identity_content(),
            "implementation_files": list(self.implementation_files),
            "content_id": self.content_id,
        }


def measure_implementation_digest(
    files: tuple[Path, ...],
) -> tuple[str, tuple[str, ...], dict[str, bytes]]:
    """اقرأ بايتاتِ ملفّات التنفيذ الآن، وأعِد بصمتَها وأسماءَها وبايتاتِها.

    هذه هي بدائيّةُ القياس الوحيدة: يُجمِّد بها التجميدُ الهويّةَ، وتُعيد بها
    سلطةُ التنفيذ القياسَ قبل التشغيل وبعده. ونسختان من خوارزميّة قياسٍ واحدة
    قياسان ينحرفان بصمت.
    """

    if not isinstance(files, tuple) or not files:
        raise EvaluationError("هويّةُ قارئٍ تُقاس على ملفّاتٍ مُسمّاةٍ غيرِ فارغة")
    rows: list[list[str]] = []
    displayed: list[str] = []
    measured: dict[str, bytes] = {}
    for path in files:
        resolved = path.resolve()
        if not resolved.is_file():
            raise EvaluationError(f"ملفُّ تنفيذٍ غيرُ موجود: {path}")
        name = displayed_path(resolved)
        content = resolved.read_bytes()
        rows.append([name, hashlib.sha256(content).hexdigest()])
        displayed.append(name)
        measured[name] = content
    if len(set(displayed)) != len(displayed):
        raise EvaluationError("ملفُّ تنفيذٍ مُكرَّرُ الاسم؛ والمكرّرُ يُرفَض لا يُطوى")
    rows.sort()
    return (
        canonical_digest(canonical_bytes(rows)),
        tuple(sorted(displayed)),
        measured,
    )


def measure_configuration_digest(configuration: Mapping[str, str]) -> str:
    """اشتقَّ بصمةَ الإعداد من مطابقةٍ مُعلَنة؛ بدائيّةٌ واحدةٌ لا تُنسَخ."""

    if not isinstance(configuration, Mapping):
        raise EvaluationError("إعدادُ القارئ مطابقةٌ مُعلَنة")
    for key, value in configuration.items():
        _require_text(key, "مفتاحُ الإعداد")
        _require_text(value, f"قيمةُ الإعداد `{key}`")
    return canonical_digest(
        canonical_bytes([[key, configuration[key]] for key in sorted(configuration)])
    )


def measure_dependency_boundary_digest(report: ImportBoundaryReport) -> str:
    """اشتقَّ بصمةَ حدِّ الاعتماد من تقريرٍ مقيسٍ؛ بدائيّةٌ واحدةٌ لا تُنسَخ."""

    if not isinstance(report, ImportBoundaryReport):
        raise EvaluationError("حدُّ الاعتماد تقريرٌ مقيسٌ من نوعه لا دعوى")
    return canonical_digest(
        canonical_bytes(
            {
                "policy_id": report.policy_id,
                "reached_modules": list(report.reached_modules),
                "violations": list(report.violations),
                "dynamic_accesses": list(report.dynamic_accesses),
            }
        )
    )


def compose_system_content_id(
    *,
    implementation_digest: str,
    configuration_digest: str,
    dependency_boundary_digest: str,
    contract_interface_version: str,
) -> str:
    """ركِّب بصمةَ الهويّة من مكوّناتها الأربعة، بلا اسمٍ ولا ملفّات."""

    return canonical_digest(
        canonical_bytes(
            {
                "implementation_digest": _require_digest(
                    implementation_digest, "بصمةُ التنفيذ"
                ),
                "configuration_digest": _require_digest(
                    configuration_digest, "بصمةُ الإعداد"
                ),
                "dependency_boundary_digest": _require_digest(
                    dependency_boundary_digest, "بصمةُ حدّ الاعتماد"
                ),
                "contract_interface_version": _require_text(
                    contract_interface_version, "إصدارُ واجهة العقد"
                ),
            }
        )
    )


def _implementation_digest(files: tuple[Path, ...]) -> tuple[str, tuple[str, ...]]:
    if not isinstance(files, tuple) or not files:
        raise EvaluationError("هويّةُ قارئٍ تُقاس على ملفّاتٍ مُسمّاةٍ غيرِ فارغة")
    digest, displayed, _ = measure_implementation_digest(files)
    return digest, displayed


def freeze_system_identity(
    *,
    implementation_files: tuple[Path, ...],
    configuration: Mapping[str, str],
    boundary_report: ImportBoundaryReport,
    contract_interface_version: str,
) -> FrozenSystemIdentity:
    """جمِّد هويّةَ قارئٍ من مصدره وإعداده وحدِّ اعتماده المقيس وإصدار واجهته."""

    if not isinstance(boundary_report, ImportBoundaryReport):
        raise EvaluationError("حدُّ الاعتماد تقريرٌ مقيسٌ من نوعه لا دعوى")
    if not boundary_report.is_isolated:
        raise EvaluationError(
            "لا تُجمَّد هويّةُ قارئٍ خرق حدَّ مصدره المُصرَّح؛ والمخالفات: "
            + "، ".join(boundary_report.violations + boundary_report.dynamic_accesses)
        )
    implementation_digest, displayed = _implementation_digest(implementation_files)
    return FrozenSystemIdentity(
        implementation_digest=implementation_digest,
        configuration_digest=measure_configuration_digest(configuration),
        dependency_boundary_digest=measure_dependency_boundary_digest(boundary_report),
        contract_interface_version=_require_text(
            contract_interface_version, "إصدارُ واجهة العقد"
        ),
        implementation_files=displayed,
    )
