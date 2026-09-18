"""`G0.EXEC-0`: تنفيذُ قارئٍ مربوطٌ بهويّته المُعاد قياسُها وبحمولته المُجمَّدة.

    NoRunReportWithoutBoundExecution

    FrozenSystemIdentity
            ↓
    BoundEvaluationRequest
            ↓
    BlindPayload (bytes)
            ↓
    ExecutionAuthority        ← تُعيد القياسَ، وتنسخ المقيس، وتُشغِّله منفصلًا
            ↓
    BoundExecutionReceipt     ← لا يصدُر إلّا عنها
            ↓
    FrozenRunReport           ← لا يُبنى إلّا منه
            ↓
    RunLedger
            ↓
    GoldRevealRecord

ولا مقارنةَ هنا، ولا نظامَ ثانٍ، ولا `Ω_M`، ولا حكم. والسقفُ إيصالُ تنفيذٍ
وتقريرٌ مُشتَقٌّ منه: `NoComparisonBeforeBoundExecution`.

وهذه الحزمةُ تستورد `evaluation` ولا تُستورَد منها:
`EvaluationBoundary != ExecutionMechanism`. وآليّتُها عمليّةٌ منفصلةٌ مُعلَنةٌ لا
حبسٌ مُثبَت: `SeparateProcess != Sandbox`.
"""

from __future__ import annotations

from .audit import (
    EXECUTION_DECLARED_ACCESSES,
    EXECUTION_FORBIDDEN_PACKAGES,
    EXECUTION_IMPORT_POLICY,
    EXECUTION_PERMITTED_MODULES,
    ExecutionIsolationReport,
    execution_import_isolation_audit,
)
from .authority import (
    DEFAULT_EXECUTION_TIMEOUT_SECONDS,
    ExecutionAuthority,
    ReaderExecutionRequest,
    SeparateProcessConfinementDeclaration,
)
from .laws import (
    EVALUATION_BOUNDARY_IS_NOT_THE_EXECUTION_MECHANISM,
    EXECUTED_READER_IDENTITY_EQUALS_FROZEN_READER_IDENTITY,
    EXECUTION_LAWS,
    IMPLEMENTATION_CHANGED_DURING_EXECUTION_MEANS_NO_REFERENCE_RUN,
    MEASURED_BYTES_ARE_EXECUTED_BYTES,
    NO_COMPARISON_BEFORE_BOUND_EXECUTION,
    SEPARATE_PROCESS_IS_NOT_A_SANDBOX,
    ExecutionError,
)
from .runner import READER_ENTRYPOINT_NAME, RUNNER_WIRE_PROTOCOL
from .workspace import (
    EXECUTION_WORKSPACE_PREFIX,
    RUNNER_FILE_NAME,
    execution_entrypoint_digest,
)

__all__ = [
    "DEFAULT_EXECUTION_TIMEOUT_SECONDS",
    "EVALUATION_BOUNDARY_IS_NOT_THE_EXECUTION_MECHANISM",
    "EXECUTED_READER_IDENTITY_EQUALS_FROZEN_READER_IDENTITY",
    "EXECUTION_DECLARED_ACCESSES",
    "EXECUTION_FORBIDDEN_PACKAGES",
    "EXECUTION_IMPORT_POLICY",
    "EXECUTION_LAWS",
    "EXECUTION_PERMITTED_MODULES",
    "EXECUTION_WORKSPACE_PREFIX",
    "IMPLEMENTATION_CHANGED_DURING_EXECUTION_MEANS_NO_REFERENCE_RUN",
    "MEASURED_BYTES_ARE_EXECUTED_BYTES",
    "NO_COMPARISON_BEFORE_BOUND_EXECUTION",
    "READER_ENTRYPOINT_NAME",
    "RUNNER_FILE_NAME",
    "RUNNER_WIRE_PROTOCOL",
    "SEPARATE_PROCESS_IS_NOT_A_SANDBOX",
    "ExecutionAuthority",
    "ExecutionError",
    "ExecutionIsolationReport",
    "ReaderExecutionRequest",
    "SeparateProcessConfinementDeclaration",
    "execution_entrypoint_digest",
    "execution_import_isolation_audit",
]
