"""`G0.EXEC-0.AUTHORITY`: سلطةُ التنفيذ المربوط؛ وحدَها تُصدِر إيصالًا.

    FrozenSystemIdentity
            ↓
    BoundEvaluationRequest
            ↓
    BlindPayload (bytes)
            ↓
    ExecutionAuthority
            ↓
    BoundExecutionReceipt
            ↓
    FrozenRunReport

قبل التشغيل تُعاد مكوّناتُ الهويّة الأربعةُ قياسًا من الصفر، وتُركَّب بصمةً
تُقارَن بالهويّة المُجمَّدة: `ExecutedReaderIdentity == FrozenReaderIdentity`.
وبعد التشغيل يُعاد قياسُ المصدر، فإن تغيّر لم يُعرَف أيُّ البايتات أنتج المخرجات:
`ImplementationChangedDuringExecution -> NoReferenceRunReport`.

والقارئُ لا يستلم كائنًا: يستلم بايتاتِ الحمولة على `stdin` في عمليّةٍ منفصلةٍ
ببيئةٍ مُقلَّمةٍ ومساحةِ عملٍ مؤقّتةٍ خارج الشجرة، وتُلتقَط بايتاتُ `stdout`
و`stderr` وحالُ الخروج. وليس هذا حبسًا: `SeparateProcess != Sandbox`.

وما بدأ تنفيذُه يُوصَل به إيصالٌ وإن فشل، ولا يُرقّى غيرُ التامِّ إلى تشغيلٍ
مرجعيّ: `FailureIsReceiptedButNotPromotedToReferenceRun`.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..canonical_content import canonical_digest
from ..evaluation import (
    BoundExecutionReceipt,
    EvaluationBinding,
    ExecutionExitStatus,
    ExecutionMode,
    FrozenSystemIdentity,
    ProcessConfinementStanding,
    ResidualCode,
    RunResidual,
    compose_system_content_id,
    measure_configuration_digest,
    measure_dependency_boundary_digest,
    measure_implementation_digest,
    reader_import_audit,
)
from ..evaluation.receipt import _issue_receipt
from ..import_boundary import displayed_path
from .laws import (
    EXECUTED_READER_IDENTITY_EQUALS_FROZEN_READER_IDENTITY,
    IMPLEMENTATION_CHANGED_DURING_EXECUTION_MEANS_NO_REFERENCE_RUN,
    SEPARATE_PROCESS_IS_NOT_A_SANDBOX,
    ExecutionError,
)
from .runner import (
    EXIT_COMPLETED,
    EXIT_READER_RAISED,
    EXIT_UNUSABLE_RESULT,
    READER_ENTRYPOINT_NAME,
    RUNNER_WIRE_PROTOCOL,
)
from .workspace import (
    EXECUTION_WORKSPACE_PREFIX,
    RUNNER_FILE_NAME,
    execution_entrypoint_digest,
    materialize_measured_bytes,
)

__all__ = [
    "DEFAULT_EXECUTION_TIMEOUT_SECONDS",
    "ExecutionAuthority",
    "ReaderExecutionRequest",
    "SeparateProcessConfinementDeclaration",
]

DEFAULT_EXECUTION_TIMEOUT_SECONDS = 60
"""سقفُ زمنِ تشغيلٍ مُعلَن؛ تجاوزُه حالُ خروجٍ مُسمّاةٌ لا تعليقٌ صامت."""


@dataclass(frozen=True, slots=True)
class SeparateProcessConfinementDeclaration:
    """تصريحٌ بآليّة التشغيل وحدِّها؛ منفصلةٌ مُعلَنة، لا حبسَ مُثبَت."""

    standing: ProcessConfinementStanding = (
        ProcessConfinementStanding.SEPARATE_PROCESS_DECLARED
    )

    def __post_init__(self) -> None:
        if not isinstance(self.standing, ProcessConfinementStanding):
            raise ExecutionError("حالُ حبس العمليّة عضوٌ في مفردته المغلقة")

    @property
    def is_proven(self) -> bool:
        """أمُثبَتٌ حبسُ العمليّة؟ ولا إثباتَ في هذا الطور بالبناء."""

        return self.standing.is_proven

    @property
    def ceiling(self) -> str:
        """سقفُ ما يُدَّعى بآليّة العمليّة المنفصلة."""

        return SEPARATE_PROCESS_IS_NOT_A_SANDBOX

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى التصريح للسجلّ."""

        return {
            "standing": self.standing.value,
            "is_proven": self.is_proven,
            "ceiling": self.ceiling,
        }


@dataclass(frozen=True, slots=True)
class ReaderExecutionRequest:
    """ما تحتاجه السلطةُ لتُعيد القياسَ ثمّ تُشغِّل: هويّةٌ، ومصدرٌ، وإعداد."""

    identity: FrozenSystemIdentity
    implementation_files: tuple[Path, ...]
    entry_file: Path
    configuration: Mapping[str, str]

    def __post_init__(self) -> None:
        if not isinstance(self.identity, FrozenSystemIdentity):
            raise ExecutionError("التنفيذُ يقع على هويّةٍ مُجمَّدةٍ من نوعها")
        if not isinstance(self.implementation_files, tuple):
            raise ExecutionError("ملفّاتُ التنفيذ صفٌّ مُجمَّد لا قائمة")
        if not self.implementation_files:
            raise ExecutionError("لا تنفيذَ بلا ملفِّ تنفيذٍ مُسمًّى")
        if self.entry_file.resolve() not in {
            path.resolve() for path in self.implementation_files
        }:
            raise ExecutionError("ملفُّ المدخل ليس من ملفّات التنفيذ المُصرَّحة")
        if not isinstance(self.configuration, Mapping):
            raise ExecutionError("إعدادُ القارئ مطابقةٌ مُعلَنة")


class _OutputShapeError(ExecutionError):
    """شكلُ ناتجٍ مرفوض؛ يُسمّى ولا يُحمَل على أقرب حالة."""


class _UnknownMemberError(ExecutionError):
    """عضوٌ خارج المجال في الناتج؛ يُسمّى ولا يُطوى."""


def _residual_from_wire(entry: Mapping[str, Any]) -> RunResidual:
    return RunResidual(
        member_id=str(entry["member_id"]),
        residual_code=ResidualCode(str(entry["residual_code"])),
        blocking=bool(entry["blocking"]),
        reason=str(entry["reason"]),
        evidence_ref=str(entry["evidence_ref"]),
    )


class ExecutionAuthority:
    """السلطةُ التي تُعيد القياسَ، وتُشغِّل المقيس، وتُصدِر الإيصالَ وحدَها."""

    execution_mode = ExecutionMode.SEPARATE_PROCESS

    def __init__(
        self,
        binding: EvaluationBinding,
        *,
        timeout_seconds: int = DEFAULT_EXECUTION_TIMEOUT_SECONDS,
    ) -> None:
        if not isinstance(binding, EvaluationBinding):
            raise ExecutionError("سلطةُ التنفيذ تقوم على ربطٍ مُجمَّدٍ من نوعه")
        if not isinstance(timeout_seconds, int) or timeout_seconds < 1:
            raise ExecutionError("سقفُ الزمن عددٌ صحيحٌ موجب")
        self._binding = binding
        self._timeout_seconds = timeout_seconds
        self._member_ids = frozenset(binding.contract.body.member_ids)

    @property
    def binding(self) -> EvaluationBinding:
        """الربطُ الذي يُشتَقُّ منه الطلبُ والحمولة."""

        return self._binding

    @property
    def confinement(self) -> SeparateProcessConfinementDeclaration:
        """تصريحُ الآليّة؛ منفصلةٌ مُعلَنة، لا حبسَ مُثبَت."""

        return SeparateProcessConfinementDeclaration()

    def execute(self, request: ReaderExecutionRequest) -> BoundExecutionReceipt:
        """أعِد قياسَ الهويّة، شغِّل بايتاتِها المقيسة، وأصدِر إيصالَ ما جرى."""

        if not isinstance(request, ReaderExecutionRequest):
            raise ExecutionError("التنفيذُ يقع على طلبِ تشغيلٍ من نوعه")
        bound_request = self._binding.request_for(request.identity)
        payload = self._binding.payload
        trace: list[str] = [
            "execution.mode=" + self.execution_mode.value,
            "execution.confinement=" + self.confinement.standing.value,
            "request.id=" + bound_request.request_id,
            "payload.digest=" + payload.payload_digest,
        ]
        identity = request.identity
        entrypoint_digest = execution_entrypoint_digest(
            contract_interface_version=identity.contract_interface_version
        )

        implementation_digest, displayed, measured = measure_implementation_digest(
            request.implementation_files
        )
        trace.append("implementation.remeasured=" + implementation_digest)
        boundary_report = reader_import_audit(request.implementation_files)
        dependency_boundary_digest = measure_dependency_boundary_digest(boundary_report)
        configuration_digest = measure_configuration_digest(request.configuration)
        composed = compose_system_content_id(
            implementation_digest=implementation_digest,
            configuration_digest=configuration_digest,
            dependency_boundary_digest=dependency_boundary_digest,
            contract_interface_version=identity.contract_interface_version,
        )

        def receipt(
            status: ExecutionExitStatus,
            *,
            outputs: tuple[tuple[str, str], ...] = (),
            residuals: tuple[RunResidual, ...] = (),
        ) -> BoundExecutionReceipt:
            return _issue_receipt(
                system_content_id=identity.content_id,
                request_id=bound_request.request_id,
                implementation_digest=implementation_digest,
                configuration_digest=configuration_digest,
                dependency_boundary_digest=dependency_boundary_digest,
                payload_digest=payload.payload_digest,
                execution_entrypoint_digest=entrypoint_digest,
                exit_status=status,
                execution_mode=self.execution_mode,
                outputs=outputs,
                residuals=residuals,
                trace=tuple(trace),
            )

        if not boundary_report.is_isolated:
            trace.append(
                "boundary.violations=" + ";".join(sorted(boundary_report.violations))
            )
            trace.append(
                "boundary.dynamic=" + ";".join(sorted(boundary_report.dynamic_accesses))
            )
            return receipt(ExecutionExitStatus.BOUNDARY_VIOLATION)
        trace.append("boundary.digest=" + dependency_boundary_digest)

        if composed != identity.content_id:
            trace.append("identity.composed=" + composed)
            trace.append("identity.frozen=" + identity.content_id)
            trace.append(
                "identity.law=" + EXECUTED_READER_IDENTITY_EQUALS_FROZEN_READER_IDENTITY
            )
            return receipt(ExecutionExitStatus.IDENTITY_MISMATCH)
        trace.append("identity.confirmed=" + identity.content_id)

        entry_displayed = displayed_path(request.entry_file.resolve())
        if entry_displayed not in displayed:
            raise ExecutionError("ملفُّ المدخل ليس من ملفّات التنفيذ المقيسة")
        completed = self._run_in_a_separate_process(
            measured, entry_displayed, payload.payload_bytes
        )
        return_code, stdout, stderr = completed
        trace.append("process.return_code=" + str(return_code))
        trace.append("process.stdout_digest=" + canonical_digest(stdout))
        trace.append("process.stderr_digest=" + canonical_digest(stderr))

        after_digest, _, _ = measure_implementation_digest(request.implementation_files)
        trace.append("implementation.post_execution=" + after_digest)
        if after_digest != implementation_digest:
            trace.append(
                "implementation.law="
                + IMPLEMENTATION_CHANGED_DURING_EXECUTION_MEANS_NO_REFERENCE_RUN
            )
            return receipt(ExecutionExitStatus.IMPLEMENTATION_CHANGED_DURING_EXECUTION)

        if return_code == EXIT_READER_RAISED:
            return receipt(ExecutionExitStatus.RAISED)
        if return_code == EXIT_UNUSABLE_RESULT:
            return receipt(ExecutionExitStatus.REFUSED_OUTPUT_SHAPE)
        if return_code != EXIT_COMPLETED:
            return receipt(ExecutionExitStatus.NONZERO_EXIT)

        try:
            outputs, residuals = self._validated_result(stdout)
        except _UnknownMemberError as error:
            trace.append("outputs.refused=" + str(error))
            return receipt(ExecutionExitStatus.REFUSED_UNKNOWN_MEMBER)
        except _OutputShapeError as error:
            trace.append("outputs.refused=" + str(error))
            return receipt(ExecutionExitStatus.REFUSED_OUTPUT_SHAPE)
        trace.append("outputs.classified=" + str(len(outputs)))
        trace.append("outputs.residuals=" + str(len(residuals)))
        return receipt(
            ExecutionExitStatus.COMPLETED, outputs=outputs, residuals=residuals
        )

    def _run_in_a_separate_process(
        self, measured: Mapping[str, bytes], entry_displayed: str, payload: bytes
    ) -> tuple[int, bytes, bytes]:
        with tempfile.TemporaryDirectory(
            prefix=EXECUTION_WORKSPACE_PREFIX
        ) as workspace:
            root = Path(workspace)
            module_name = materialize_measured_bytes(
                root, measured, entry_displayed_name=entry_displayed
            )
            environment = {
                "PATH": os.environ.get("PATH", ""),
                "LC_ALL": "C.UTF-8",
                "LANG": "C.UTF-8",
                "PYTHONIOENCODING": "utf-8",
                "PYTHONHASHSEED": "0",
            }
            try:
                completed = subprocess.run(
                    [
                        sys.executable,
                        "-I",
                        "-S",
                        str(root / RUNNER_FILE_NAME),
                        module_name,
                        READER_ENTRYPOINT_NAME,
                    ],
                    input=payload,
                    cwd=str(root),
                    env=environment,
                    capture_output=True,
                    timeout=self._timeout_seconds,
                    check=False,
                )
            except subprocess.TimeoutExpired:
                return -1, b"", b"timeout"
            return completed.returncode, completed.stdout, completed.stderr

    def _validated_result(
        self, stdout: bytes
    ) -> tuple[tuple[tuple[str, str], ...], tuple[RunResidual, ...]]:
        try:
            decoded = json.loads(stdout.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise _OutputShapeError(f"قناةٌ غيرُ قانونيّة: {error}") from error
        if not isinstance(decoded, dict):
            raise _OutputShapeError("ناتجُ القناة بنيةٌ مغلقةٌ لا قيمةٌ حرّة")
        if decoded.get("protocol") != RUNNER_WIRE_PROTOCOL:
            raise _OutputShapeError("ناتجٌ بإصدارِ قناةٍ غيرِ المُعلَن")
        raw_outputs = decoded.get("outputs")
        raw_residuals = decoded.get("residuals")
        if not isinstance(raw_outputs, list) or not isinstance(raw_residuals, list):
            raise _OutputShapeError("التصنيفاتُ والبقايا قائمتان مُعلَنتان")
        outputs: list[tuple[str, str]] = []
        for entry in raw_outputs:
            if not isinstance(entry, list) or len(entry) != 2:
                raise _OutputShapeError("المخرَجُ زوجٌ: عضوٌ وتصنيفُه")
            member_id, label = entry
            if not isinstance(member_id, str) or not isinstance(label, str):
                raise _OutputShapeError("العضوُ وتصنيفُه نصّان")
            if not label.strip():
                raise _OutputShapeError(f"تصنيفٌ فارغٌ للعضو `{member_id}`")
            if member_id not in self._member_ids:
                raise _UnknownMemberError(f"عضوٌ خارج المجال: {member_id}")
            outputs.append((member_id, label))
        residuals: list[RunResidual] = []
        for entry in raw_residuals:
            if not isinstance(entry, dict):
                raise _OutputShapeError("البقيّةُ بنيةٌ مُسمّاةٌ لا نصّ")
            try:
                residual = _residual_from_wire(entry)
            except (KeyError, ValueError) as error:
                raise _OutputShapeError(f"بقيّةٌ غيرُ مُصنَّفة: {error}") from error
            if residual.member_id not in self._member_ids:
                raise _UnknownMemberError(
                    f"بقيّةٌ لعضوٍ خارج المجال: {residual.member_id}"
                )
            residuals.append(residual)
        classified = [member_id for member_id, _ in outputs]
        if len(set(classified)) != len(classified):
            raise _OutputShapeError("عضوٌ مُصنَّفٌ مرّتين؛ والمكرّرُ يُرفَض لا يُطوى")
        left = [residual.member_id for residual in residuals]
        if len(set(left)) != len(left):
            raise _OutputShapeError("بقيّةٌ مُكرَّرة؛ والمكرّرُ يُرفَض لا يُطوى")
        overlap = set(classified) & set(left)
        if overlap:
            raise _OutputShapeError("عضوٌ مُصنَّفٌ وبقيّةٌ معًا: " + "، ".join(sorted(overlap)))
        missing = self._member_ids - set(classified) - set(left)
        if missing:
            raise _OutputShapeError(
                "التغطيةُ تامّةٌ لا أحسنَ جهد؛ والأعضاءُ المتروكون بلا بقيّة: "
                + "، ".join(sorted(missing))
            )
        return tuple(outputs), tuple(residuals)
