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

والقارئُ لا يستلم كائنًا: يستلم مغلّفًا مؤطَّرًا على `stdin` في عمليّةٍ منفصلةٍ
ببيئةٍ مُقلَّمةٍ ومساحةِ عملٍ مؤقّتةٍ خارج الشجرة، وتُلتقَط بايتاتُ `stdout`
و`stderr` وحالُ الخروج. وليس هذا حبسًا: `SeparateProcess != Sandbox`.

والإعدادُ الذي ركّب الهويّةَ يعبُر ذلك المغلّفَ إلى نداء القارئ، ويشهد المُشغِّلُ
ببصمة ما استلم فتُقارَن ببصمة ما كُتِب:
`ConfigurationIsExecutedNotOnlyIdentified`.

وكلُّ إيصالٍ يحمل مُعرِّفَ مفتاح سلطته وتوقيعَها على محتواه:
`ReceiptIssuanceIsKeyedNotMerelySealed`، وسقفُه مُعلَنٌ لا مُدَّعًى:
`AnInProcessSealIsNotUnforgeableProvenance`.

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
    IssuanceProvenanceStanding,
    ProcessConfinementStanding,
    ReceiptIssuanceKey,
    ResidualCode,
    RunResidual,
    compose_system_content_id,
    measure_configuration_digest,
    measure_dependency_boundary_digest,
    measure_implementation_digest,
    reader_import_audit,
    verify_receipt_issuance,
)
from ..evaluation.receipt import _issue_receipt
from ..import_boundary import displayed_path
from .envelope import ExecutionEnvelope, build_execution_envelope
from .laws import (
    A_TIMEOUT_IS_NAMED_NOT_FOLDED_INTO_A_NONZERO_EXIT,
    A_WIRE_VALUE_IS_REFUSED_NOT_COERCED,
    AN_IN_PROCESS_SEAL_IS_NOT_UNFORGEABLE_PROVENANCE,
    CONFIGURATION_IS_EXECUTED_NOT_ONLY_IDENTIFIED,
    EXECUTED_READER_IDENTITY_EQUALS_FROZEN_READER_IDENTITY,
    IMPLEMENTATION_CHANGED_DURING_EXECUTION_MEANS_NO_REFERENCE_RUN,
    SEPARATE_PROCESS_IS_NOT_A_SANDBOX,
    ExecutionError,
)
from .runner import (
    EXIT_COMPLETED,
    EXIT_READER_RAISED,
    EXIT_REFUSED_ENTRYPOINT_SIGNATURE,
    EXIT_UNUSABLE_ENVELOPE,
    EXIT_UNUSABLE_RESULT,
    READER_ENTRYPOINT_NAME,
    RESIDUAL_WIRE_FIELDS,
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
    "SeparateProcessOutcome",
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


@dataclass(frozen=True, slots=True)
class SeparateProcessOutcome:
    """ما انتهت إليه العمليّةُ المنفصلة، مُسمًّى لا مطويًّا في رمزٍ حارس.

    تجاوزُ السقف الزمنيّ حدثٌ غيرُ الخروج برمزٍ غيرِ صفر، والقتلُ بإشارةٍ غيرُهما؛
    ورمزٌ حارسٌ مُصطنَعٌ مثل `-1` يتصادم برمزِ عمليّةٍ قُتلت بإشارة، فيُسمّى الحالُ
    هنا ولا يُستدَلّ عليه من رقم: `ATimeoutIsNamedNotFoldedIntoANonzeroExit`.
    """

    timed_out: bool
    return_code: int | None
    stdout: bytes
    stderr: bytes

    def __post_init__(self) -> None:
        if type(self.timed_out) is not bool:
            raise ExecutionError("صفةُ تجاوز السقف قيمةٌ ثنائيّةٌ مُعلَنة")
        if self.timed_out:
            if self.return_code is not None:
                raise ExecutionError("ما تجاوز السقفَ لا يُنسَب إليه رمزُ خروج")
        elif not isinstance(self.return_code, int):
            raise ExecutionError("رمزُ الخروج عددٌ صحيحٌ مقيس")

    @property
    def was_signalled(self) -> bool:
        """أقُتِلت العمليّةُ بإشارة؟ يُقرَأ من رمزٍ سالبٍ مقيسٍ لا من حارس."""

        return self.return_code is not None and self.return_code < 0

    @property
    def timeout_law(self) -> str:
        """قانونُ تسمية المهلة والإشارة."""

        return A_TIMEOUT_IS_NAMED_NOT_FOLDED_INTO_A_NONZERO_EXIT


class _OutputShapeError(ExecutionError):
    """شكلُ ناتجٍ مرفوض؛ يُسمّى ولا يُحمَل على أقرب حالة."""


class _UnknownMemberError(ExecutionError):
    """عضوٌ خارج المجال في الناتج؛ يُسمّى ولا يُطوى."""


class _ConfigurationDeliveryError(ExecutionError):
    """إعدادٌ لم يبلغ القارئَ كما كُتِب؛ يُسمّى ولا يُقرَأ ناتجُه."""


def _require_wire_text(value: object, label: str) -> str:
    """اقبل نصًّا غيرَ فارغٍ ولا تُحوِّل نوعًا خاطئًا: `AWireValueIsRefusedNotCoerced`."""

    if type(value) is not str or not value.strip():
        raise _OutputShapeError(f"{label}: {A_WIRE_VALUE_IS_REFUSED_NOT_COERCED}")
    return value


def _residual_from_wire(entry: Mapping[str, Any]) -> RunResidual:
    """اقرأ بقيّةً من القناة رفضًا للنوع الخاطئ، لا تطويعًا له."""

    if tuple(sorted(entry)) != RESIDUAL_WIRE_FIELDS:
        raise _OutputShapeError("حقولُ البقيّة مجموعةٌ مطابقة؛ ولا ناقصَ ولا زائد")
    if type(entry["blocking"]) is not bool:
        raise _OutputShapeError("صفةُ الإعاقة: " + A_WIRE_VALUE_IS_REFUSED_NOT_COERCED)
    code = _require_wire_text(entry["residual_code"], "رمزُ البقيّة")
    try:
        residual_code = ResidualCode(code)
    except ValueError as error:
        raise _OutputShapeError(f"رمزُ بقيّةٍ خارج مفردته المغلقة: {code}") from error
    return RunResidual(
        member_id=_require_wire_text(entry["member_id"], "عضوُ البقيّة"),
        residual_code=residual_code,
        blocking=entry["blocking"],
        reason=_require_wire_text(entry["reason"], "سببُ البقيّة"),
        evidence_ref=_require_wire_text(entry["evidence_ref"], "إحالةُ شاهد البقيّة"),
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
        self._issuance_key = ReceiptIssuanceKey()

    @property
    def issuer_key_id(self) -> str:
        """مُعرِّفُ مفتاح إصدار هذه السلطة؛ يدخل كلَّ إيصالٍ تُصدِره ويُقارَن."""

        return self._issuance_key.key_id

    @property
    def issuance_provenance_standing(self) -> IssuanceProvenanceStanding:
        """حالُ نسبِ الإصدار؛ مفتاحٌ داخل العمليّة، ولا ثقةَ عابرةً للجلسات."""

        return self._issuance_key.standing

    @property
    def issuance_provenance_ceiling(self) -> str:
        """سقفُ ما يُدَّعى بمفتاحٍ يعيش في عمليّة السلطة نفسِها."""

        return AN_IN_PROCESS_SEAL_IS_NOT_UNFORGEABLE_PROVENANCE

    def verify_issuance(self, receipt: BoundExecutionReceipt) -> bool:
        """أصدَرَت هذه السلطةُ هذا الإيصال؟ يُقرَأ التوقيعُ في متنه لا في حيازته."""

        return verify_receipt_issuance(receipt, self._issuance_key)

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
        envelope = build_execution_envelope(
            configuration=request.configuration,
            payload_bytes=payload.payload_bytes,
            payload_digest=payload.payload_digest,
        )
        trace.append("envelope.digest=" + envelope.envelope_digest)
        trace.append("envelope.configuration_digest=" + configuration_digest)
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
                issuance_key=self._issuance_key,
                system_content_id=identity.content_id,
                request_id=bound_request.request_id,
                implementation_digest=implementation_digest,
                configuration_digest=configuration_digest,
                dependency_boundary_digest=dependency_boundary_digest,
                payload_digest=payload.payload_digest,
                execution_entrypoint_digest=entrypoint_digest,
                execution_envelope_digest=envelope.envelope_digest,
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
        outcome = self._run_in_a_separate_process(measured, entry_displayed, envelope)
        trace.append("process.timed_out=" + ("true" if outcome.timed_out else "false"))
        trace.append("process.timeout_seconds=" + str(self._timeout_seconds))
        trace.append("process.return_code=" + str(outcome.return_code))
        trace.append("process.stdout_digest=" + canonical_digest(outcome.stdout))
        trace.append("process.stderr_digest=" + canonical_digest(outcome.stderr))

        after_digest, _, _ = measure_implementation_digest(request.implementation_files)
        trace.append("implementation.post_execution=" + after_digest)
        if after_digest != implementation_digest:
            trace.append(
                "implementation.law="
                + IMPLEMENTATION_CHANGED_DURING_EXECUTION_MEANS_NO_REFERENCE_RUN
            )
            return receipt(ExecutionExitStatus.IMPLEMENTATION_CHANGED_DURING_EXECUTION)

        if outcome.timed_out:
            trace.append("process.law=" + outcome.timeout_law)
            return receipt(ExecutionExitStatus.TIMEOUT)
        if outcome.was_signalled:
            trace.append("process.law=" + outcome.timeout_law)
            return receipt(ExecutionExitStatus.SIGNALLED)
        return_code = outcome.return_code
        if return_code == EXIT_READER_RAISED:
            return receipt(ExecutionExitStatus.RAISED)
        if return_code == EXIT_REFUSED_ENTRYPOINT_SIGNATURE:
            return receipt(ExecutionExitStatus.REFUSED_ENTRYPOINT_SIGNATURE)
        if return_code == EXIT_UNUSABLE_ENVELOPE:
            trace.append(
                "envelope.law=" + CONFIGURATION_IS_EXECUTED_NOT_ONLY_IDENTIFIED
            )
            return receipt(ExecutionExitStatus.CONFIGURATION_DELIVERY_MISMATCH)
        if return_code == EXIT_UNUSABLE_RESULT:
            return receipt(ExecutionExitStatus.REFUSED_OUTPUT_SHAPE)
        if return_code != EXIT_COMPLETED:
            return receipt(ExecutionExitStatus.NONZERO_EXIT)

        try:
            outputs, residuals = self._validated_result(
                outcome.stdout, envelope_digest=envelope.envelope_digest
            )
        except _ConfigurationDeliveryError as error:
            trace.append("envelope.refused=" + str(error))
            trace.append(
                "envelope.law=" + CONFIGURATION_IS_EXECUTED_NOT_ONLY_IDENTIFIED
            )
            return receipt(ExecutionExitStatus.CONFIGURATION_DELIVERY_MISMATCH)
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
        self,
        measured: Mapping[str, bytes],
        entry_displayed: str,
        envelope: ExecutionEnvelope,
    ) -> SeparateProcessOutcome:
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
                    input=envelope.framed_bytes,
                    cwd=str(root),
                    env=environment,
                    capture_output=True,
                    timeout=self._timeout_seconds,
                    check=False,
                )
            except subprocess.TimeoutExpired as expired:
                return SeparateProcessOutcome(
                    timed_out=True,
                    return_code=None,
                    stdout=expired.stdout or b"",
                    stderr=expired.stderr or b"",
                )
            return SeparateProcessOutcome(
                timed_out=False,
                return_code=completed.returncode,
                stdout=completed.stdout,
                stderr=completed.stderr,
            )

    def _validated_result(
        self, stdout: bytes, *, envelope_digest: str
    ) -> tuple[tuple[tuple[str, str], ...], tuple[RunResidual, ...]]:
        try:
            decoded = json.loads(stdout.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise _OutputShapeError(f"قناةٌ غيرُ قانونيّة: {error}") from error
        if not isinstance(decoded, dict):
            raise _OutputShapeError("ناتجُ القناة بنيةٌ مغلقةٌ لا قيمةٌ حرّة")
        if decoded.get("protocol") != RUNNER_WIRE_PROTOCOL:
            raise _OutputShapeError("ناتجٌ بإصدارِ قناةٍ غيرِ المُعلَن")
        if decoded.get("envelope_digest") != envelope_digest:
            raise _ConfigurationDeliveryError(
                "بصمةُ المغلّف المشهودُ باستلامه غيرُ بصمة ما كُتِب؛ "
                "فالإعدادُ لم يبلغ القارئَ كما قيس"
            )
        raw_outputs = decoded.get("outputs")
        raw_residuals = decoded.get("residuals")
        if not isinstance(raw_outputs, list) or not isinstance(raw_residuals, list):
            raise _OutputShapeError("التصنيفاتُ والبقايا قائمتان مُعلَنتان")
        outputs: list[tuple[str, str]] = []
        for entry in raw_outputs:
            if not isinstance(entry, list) or len(entry) != 2:
                raise _OutputShapeError("المخرَجُ زوجٌ: عضوٌ وتصنيفُه")
            member_id = _require_wire_text(entry[0], "مُعرِّفُ العضو في المخرَج")
            label = _require_wire_text(entry[1], f"تصنيفُ `{entry[0]}`")
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
