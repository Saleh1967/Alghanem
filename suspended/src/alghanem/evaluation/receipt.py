"""`G0.EXEC-0.RECEIPT`: إيصالُ تنفيذٍ مربوط، لا يصدُر إلّا عن سلطة تنفيذ.

    NoRunReportWithoutBoundExecution
    OnlyExecutionAuthorityIssuesExecutionReceipts

هذه الوحدةُ نوعٌ لا آليّة: تصف ما يجب أن يُشهَد به، ولا تُشغِّل عمليّةً ولا تفتح
ملفًّا ولا تُنشئ مساحةَ عمل. فالآليّةُ في حزمةٍ أخرى تستورد هذه، ولا تستوردها هذه:

    EvaluationBoundary != ExecutionMechanism

والإيصالُ لا يُبنى من الواجهة العامّة. فـ`frozen=True` يمنع التعديلَ بعد الإنشاء
ولا يمنع تزويرَ الإنشاء، والدعوى المطلوبة هنا دعوى إصدارٍ لا دعوى ثبات. فالبناءُ
مشروطٌ بختمٍ خاصٍّ بهذه الوحدة، تبلغه سلطةُ التنفيذ وحدَها عبر مصنعٍ خاصّ.

ولا يقف الأمرُ عند الختم: `ReceiptIssuanceIsKeyedNotMerelySealed`. فالختمُ حيازةٌ
لا تترك أثرًا في المتن، والإيصالُ يحمل مُعرِّفَ مفتاح سلطته وتوقيعَها على محتواه
فيُقارَن. وسقفُ ذلك مُعلَنٌ لا مُدَّعًى:
`AnInProcessSealIsNotUnforgeableProvenance`.

والإيصالُ يشهد بما جرى وإن فشل:

    FailureIsReceiptedButNotPromotedToReferenceRun
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import Enum

from ..canonical_content import canonical_bytes, canonical_digest, is_canonical_digest
from .laws import (
    AN_IN_PROCESS_SEAL_IS_NOT_UNFORGEABLE_PROVENANCE,
    FAILURE_IS_RECEIPTED_BUT_NOT_PROMOTED_TO_REFERENCE_RUN,
    ONLY_EXECUTION_AUTHORITY_ISSUES_EXECUTION_RECEIPTS,
    RECEIPT_ISSUANCE_IS_KEYED_NOT_MERELY_SEALED,
    EvaluationError,
)
from .provenance import (
    IssuanceProvenanceStanding,
    ReceiptIssuanceKey,
    issuance_signature,
    verify_issuance_signature,
)
from .residual import RunResidual

__all__ = [
    "BoundExecutionReceipt",
    "ExecutionExitStatus",
    "ExecutionMode",
    "verify_receipt_issuance",
]


class ExecutionMode(Enum):
    """آليّةُ التشغيل المُعلَنة؛ تدخل الإيصالَ فلا يُنسَب ناتجُ آليّةٍ إلى أخرى."""

    SEPARATE_PROCESS = "separate_process"

    @property
    def is_a_sandbox(self) -> bool:
        """أهذه الآليّةُ حبسٌ مُثبَت؟ ولا عضوَ كذلك فيها بالبناء."""

        return False


class ExecutionExitStatus(Enum):
    """حالُ انتهاء التنفيذ؛ مفردةٌ مغلقةٌ تُسمّي الفشلَ ولا تطويه."""

    COMPLETED = "completed"
    RAISED = "raised"
    NONZERO_EXIT = "nonzero_exit"
    SIGNALLED = "signalled"
    TIMEOUT = "timeout"
    REFUSED_OUTPUT_SHAPE = "refused_output_shape"
    REFUSED_UNKNOWN_MEMBER = "refused_unknown_member"
    REFUSED_ENTRYPOINT_SIGNATURE = "refused_entrypoint_signature"
    CONFIGURATION_DELIVERY_MISMATCH = "configuration_delivery_mismatch"
    IDENTITY_MISMATCH = "identity_mismatch"
    BOUNDARY_VIOLATION = "boundary_violation"
    IMPLEMENTATION_CHANGED_DURING_EXECUTION = "implementation_changed_during_execution"

    @property
    def is_a_reference_run(self) -> bool:
        """أيُرقَّى هذا الحالُ إلى تشغيلٍ مرجعيّ؟ والتامُّ وحدَه يُرقَّى."""

        return self is ExecutionExitStatus.COMPLETED

    @property
    def promotion_law(self) -> str:
        """قانونُ توصيل الفشل دون ترقيته."""

        return FAILURE_IS_RECEIPTED_BUT_NOT_PROMOTED_TO_REFERENCE_RUN


_AUTHORITY_SEAL: object = object()
"""ختمُ الإصدار؛ خاصٌّ بهذه الوحدة، لا يبلغه بناءٌ من الواجهة العامّة."""


def _require_digest(value: object, label: str) -> str:
    if not is_canonical_digest(value):
        raise EvaluationError(f"{label} بصمةٌ قانونيّةٌ لا نصٌّ حرّ")
    assert isinstance(value, str)
    return value


def _require_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise EvaluationError(f"{label} نصٌّ غير فارغ")
    return value


def executed_result_digest(
    outputs: tuple[tuple[str, str], ...], residuals: tuple[RunResidual, ...]
) -> str:
    """بصمةُ ما خرج فعلًا: التصنيفاتُ والبقايا معًا، قانونيّةً مُرتَّبة."""

    return canonical_digest(
        canonical_bytes(
            {
                "outputs": [list(entry) for entry in sorted(outputs)],
                "residuals": [
                    residual.as_canonical_content()
                    for residual in sorted(residuals, key=lambda item: item.member_id)
                ],
            }
        )
    )


def execution_trace_digest(trace: tuple[str, ...]) -> str:
    """بصمةُ أثرِ السلطة؛ الأثرُ الذي تملكه هي لا الذي يرويه المُمتحَن عن نفسه."""

    return canonical_digest(canonical_bytes(list(trace)))


@dataclass(frozen=True, slots=True)
class BoundExecutionReceipt:
    """شهادةُ سلطةٍ: هذه الهويّةُ المُعاد قياسُها استلمت هذه الحمولةَ فأخرجت هذه."""

    system_content_id: str
    request_id: str
    implementation_digest: str
    configuration_digest: str
    dependency_boundary_digest: str
    payload_digest: str
    execution_entrypoint_digest: str
    execution_envelope_digest: str
    output_digest: str
    exit_status: ExecutionExitStatus
    trace_digest: str
    execution_mode: ExecutionMode
    issuer_key_id: str
    issuance_signature: str
    outputs: tuple[tuple[str, str], ...]
    residuals: tuple[RunResidual, ...]
    trace: tuple[str, ...]
    seal: object

    def __post_init__(self) -> None:
        if self.seal is not _AUTHORITY_SEAL:
            raise EvaluationError(ONLY_EXECUTION_AUTHORITY_ISSUES_EXECUTION_RECEIPTS)
        for label, value in (
            ("بصمةُ هويّة القارئ", self.system_content_id),
            ("بصمةُ الطلب", self.request_id),
            ("بصمةُ التنفيذ المُعاد قياسها", self.implementation_digest),
            ("بصمةُ الإعداد المُعاد قياسها", self.configuration_digest),
            ("بصمةُ حدّ الاعتماد المُعاد قياسها", self.dependency_boundary_digest),
            ("بصمةُ الحمولة المُسلَّمة", self.payload_digest),
            ("بصمةُ مدخل التنفيذ", self.execution_entrypoint_digest),
            ("بصمةُ مغلّف التنفيذ المُسلَّم", self.execution_envelope_digest),
            ("مُعرِّفُ مفتاح الإصدار", self.issuer_key_id),
            ("توقيعُ الإصدار", self.issuance_signature),
            ("بصمةُ المخرجات المُلتقَطة", self.output_digest),
            ("بصمةُ أثر السلطة", self.trace_digest),
        ):
            _require_digest(value, label)
        if not isinstance(self.exit_status, ExecutionExitStatus):
            raise EvaluationError("حالُ الانتهاء عضوٌ في مفردته المغلقة")
        if not isinstance(self.execution_mode, ExecutionMode):
            raise EvaluationError("آليّةُ التشغيل عضوٌ في مفردتها المغلقة")
        if not isinstance(self.outputs, tuple):
            raise EvaluationError("المخرجاتُ صفٌّ مُجمَّد لا قائمة")
        member_ids = []
        for entry in self.outputs:
            if not isinstance(entry, tuple) or len(entry) != 2:
                raise EvaluationError("المخرَجُ زوجٌ: عضوٌ وتصنيفُه")
            _require_text(entry[0], "مُعرِّفُ العضو في المخرَج")
            _require_text(entry[1], f"تصنيفُ `{entry[0]}`")
            member_ids.append(entry[0])
        if len(set(member_ids)) != len(member_ids):
            raise EvaluationError("عضوٌ مُصنَّفٌ مرّتين؛ والمكرّرُ يُرفَض لا يُطوى")
        if not isinstance(self.residuals, tuple):
            raise EvaluationError("البقايا صفٌّ مُجمَّد لا قائمة")
        residual_members = []
        for residual in self.residuals:
            if not isinstance(residual, RunResidual):
                raise EvaluationError("البقيّةُ مُسمّاةٌ من نوعها لا نصٌّ حرّ")
            residual_members.append(residual.member_id)
        if len(set(residual_members)) != len(residual_members):
            raise EvaluationError("بقيّةٌ مُكرَّرة؛ والمكرّرُ يُرفَض لا يُطوى")
        overlap = set(member_ids) & set(residual_members)
        if overlap:
            raise EvaluationError("عضوٌ مُصنَّفٌ وبقيّةٌ معًا: " + "، ".join(sorted(overlap)))
        if not isinstance(self.trace, tuple) or not self.trace:
            raise EvaluationError("إيصالٌ بلا أثرِ سلطةٍ لا يُدقَّق")
        for line in self.trace:
            _require_text(line, "سطرٌ في أثر السلطة")
        if self.output_digest != executed_result_digest(self.outputs, self.residuals):
            raise EvaluationError(
                "بصمةُ المخرجات لا تُطابق المخرجاتِ المحمولة؛ فالإيصالُ عن غيرها"
            )
        if self.trace_digest != execution_trace_digest(self.trace):
            raise EvaluationError("بصمةُ الأثر لا تُطابق الأثرَ المحمول")

    @property
    def is_a_reference_run(self) -> bool:
        """أيُرقَّى هذا الإيصالُ إلى تشغيلٍ مرجعيّ؟ والتامُّ وحدَه يُرقَّى."""

        return self.exit_status.is_a_reference_run

    @property
    def issuance_law(self) -> str:
        """قانونُ الإصدار: لا إيصالَ إلّا عن سلطة تنفيذ."""

        return ONLY_EXECUTION_AUTHORITY_ISSUES_EXECUTION_RECEIPTS

    @property
    def issuance_provenance_law(self) -> str:
        """قانونُ نسبِ الإصدار: مفتاحٌ يُوقِّع، لا ختمُ حيازةٍ وحدَه."""

        return RECEIPT_ISSUANCE_IS_KEYED_NOT_MERELY_SEALED

    @property
    def issuance_provenance_standing(self) -> IssuanceProvenanceStanding:
        """حالُ نسبِ الإصدار؛ مُعلَنٌ داخل عمليّة السلطة لا مُثبَتٌ عبر حدِّ ثقة."""

        return IssuanceProvenanceStanding.IN_PROCESS_KEYED_DECLARED

    @property
    def issuance_provenance_ceiling(self) -> str:
        """سقفُ ما يُدَّعى بتوقيعٍ بمفتاحٍ يعيش في عمليّة السلطة نفسِها."""

        return AN_IN_PROCESS_SEAL_IS_NOT_UNFORGEABLE_PROVENANCE

    @property
    def residual_member_ids(self) -> tuple[str, ...]:
        """أعضاءُ المجال المتروكون في هذا التنفيذ."""

        return tuple(sorted(residual.member_id for residual in self.residuals))

    def as_canonical_content(self) -> dict[str, object]:
        """محتوى الإيصال للبصمة والسجلّ؛ بلا ختمه، فالختمُ سلطةٌ لا محتوى."""

        return {
            "system_content_id": self.system_content_id,
            "request_id": self.request_id,
            "implementation_digest": self.implementation_digest,
            "configuration_digest": self.configuration_digest,
            "dependency_boundary_digest": self.dependency_boundary_digest,
            "payload_digest": self.payload_digest,
            "execution_entrypoint_digest": self.execution_entrypoint_digest,
            "execution_envelope_digest": self.execution_envelope_digest,
            "output_digest": self.output_digest,
            "exit_status": self.exit_status.value,
            "trace_digest": self.trace_digest,
            "execution_mode": self.execution_mode.value,
            "issuer_key_id": self.issuer_key_id,
        }

    @property
    def receipt_digest(self) -> str:
        """بصمةُ الإيصال؛ مُشتَقّةٌ لا مكتوبة."""

        return canonical_digest(canonical_bytes(self.as_canonical_content()))


def verify_receipt_issuance(
    receipt: BoundExecutionReceipt, key: ReceiptIssuanceKey
) -> bool:
    """أتَشهدُ هذه السلطةُ بهذا الإيصال؟ يُقرأ الأثرُ في المتن ولا تُصدَّق حيازة.

    والتحقّقُ سقفُه مُعلَن: `AnInProcessSealIsNotUnforgeableProvenance`.
    """

    if not isinstance(receipt, BoundExecutionReceipt):
        raise EvaluationError("التحقّقُ يقع على إيصالٍ من نوعه")
    if receipt.issuer_key_id != key.key_id:
        return False
    return verify_issuance_signature(
        key, receipt.as_canonical_content(), receipt.issuance_signature
    )


def _issue_receipt(
    *,
    issuance_key: ReceiptIssuanceKey,
    system_content_id: str,
    request_id: str,
    implementation_digest: str,
    configuration_digest: str,
    dependency_boundary_digest: str,
    payload_digest: str,
    execution_entrypoint_digest: str,
    execution_envelope_digest: str,
    exit_status: ExecutionExitStatus,
    execution_mode: ExecutionMode,
    outputs: tuple[tuple[str, str], ...],
    residuals: tuple[RunResidual, ...],
    trace: tuple[str, ...],
) -> BoundExecutionReceipt:
    """أصدِر إيصالًا بختم هذه الوحدة وتوقيعِ مفتاح سلطته؛ ولا تبلغهما غيرُها.

    والتوقيعُ يقع على محتوى الإيصال بعد اشتقاق بصماته، ولا يدخل هو ذلك المحتوى؛
    فمن وقّع على توقيعه لم يوقّع على شيء.
    """

    if not isinstance(issuance_key, ReceiptIssuanceKey):
        raise EvaluationError(ONLY_EXECUTION_AUTHORITY_ISSUES_EXECUTION_RECEIPTS)
    content: dict[str, object] = {
        "system_content_id": system_content_id,
        "request_id": request_id,
        "implementation_digest": implementation_digest,
        "configuration_digest": configuration_digest,
        "dependency_boundary_digest": dependency_boundary_digest,
        "payload_digest": payload_digest,
        "execution_entrypoint_digest": execution_entrypoint_digest,
        "execution_envelope_digest": execution_envelope_digest,
        "output_digest": executed_result_digest(outputs, residuals),
        "exit_status": exit_status.value,
        "trace_digest": execution_trace_digest(trace),
        "execution_mode": execution_mode.value,
        "issuer_key_id": issuance_key.key_id,
    }
    return BoundExecutionReceipt(
        system_content_id=system_content_id,
        request_id=request_id,
        implementation_digest=implementation_digest,
        configuration_digest=configuration_digest,
        dependency_boundary_digest=dependency_boundary_digest,
        payload_digest=payload_digest,
        execution_entrypoint_digest=execution_entrypoint_digest,
        execution_envelope_digest=execution_envelope_digest,
        output_digest=executed_result_digest(outputs, residuals),
        exit_status=exit_status,
        trace_digest=execution_trace_digest(trace),
        execution_mode=execution_mode,
        issuer_key_id=issuance_key.key_id,
        issuance_signature=issuance_signature(issuance_key, content),
        outputs=outputs,
        residuals=residuals,
        trace=trace,
        seal=_AUTHORITY_SEAL,
    )


def _refuse_a_public_construction_path(names: Mapping[str, object]) -> None:
    """ارفض عند الاستيراد تصديرَ مصنعٍ عامٍّ للإيصال."""

    for name in names:
        if name.startswith("_"):
            continue
        if "issue" in name and "receipt" in name.lower():
            raise EvaluationError(ONLY_EXECUTION_AUTHORITY_ISSUES_EXECUTION_RECEIPTS)


_refuse_a_public_construction_path({name: None for name in __all__})
