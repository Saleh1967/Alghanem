"""التدقيق: كيف وصل المحرّكُ إلى حكمه؟ سطورٌ مرتَّبةٌ مُشتَقّةٌ من الأثر وحدَه.

    ExecutionResultEnvelope  →  (str, …)

**والتدقيقُ قراءةٌ لا حكمٌ ثانٍ** (`AnAuditReadsTheTraceItDoesNotJudgeAgain`):
هذه الطبقةُ لا تُعيد تقييمَ قانونٍ ولا تُضيف منزلةً؛ إنّما تُظهِر ما في النواة
بترتيبه. فما لم يُسجَّل في الأثر لا يظهر في التدقيق، وما سُجِّل لا يُخفى.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

from typing import Final

from .outcome import CheckStanding
from .result import ExecutionResultEnvelope

__all__ = [
    "AN_AUDIT_READS_THE_TRACE_IT_DOES_NOT_JUDGE_AGAIN",
    "audit_lines",
]


AN_AUDIT_READS_THE_TRACE_IT_DOES_NOT_JUDGE_AGAIN: Final[str] = (
    "التدقيقُ قراءةُ الأثر لا حكمٌ ثانٍ: لا يُعيد تقييمَ قانونٍ ولا يُضيف منزلةً "
    "ولا يُخفي سطرًا؛ وما ليس في النواة ليس في التدقيق"
)


def _identity_line(label: str, identity: object) -> str:
    if identity is None:
        return f"{label}: —"
    content = getattr(identity, "as_canonical_content", None)
    if content is None:  # pragma: no cover - guard
        return f"{label}: —"
    fields = content()
    return f"{label}: {fields}"


def audit_lines(envelope: ExecutionResultEnvelope) -> tuple[str, ...]:
    """أظهِر الأثرَ سطرًا سطرًا؛ والترتيبُ ترتيبُ القوانين لا ترتيبَ الأهمّيّة."""

    if not isinstance(envelope, ExecutionResultEnvelope):
        raise TypeError("التدقيقُ يكون على غلافٍ قائمٍ لا على وصفٍ حرّ")
    core = envelope.core
    lines: list[str] = [
        f"outcome: {core.outcome.value}",
        f"input_digest: {core.input_digest}",
        f"law_set: {core.law_set_id}",
        f"law_set_digest: {core.law_set_digest}",
        f"execution_digest: {envelope.execution_digest}",
        _identity_line("lineage", core.lineage_identity),
        _identity_line("materialized", core.materialized_identity),
        "checks:",
    ]
    for entry in core.trace:
        suffix = "" if entry.blocked_by is None else f" (blocked_by={entry.blocked_by})"
        subject = "—" if entry.subject_id is None else entry.subject_id
        lines.append(f"  {entry.law} [{subject}] {entry.standing.value}{suffix}")
    lines.append("violations:")
    for violation in core.violations:
        subject = "—" if violation.subject_id is None else violation.subject_id
        lines.append(f"  {violation.law} [{subject}]")
    lines.append("residuals:")
    for residual in core.residuals:
        lines.append(
            f"  {residual.required_authority.value} [{residual.subject_id}] "
            f"{residual.standing.value}"
        )
    lines.append("not_evaluated:")
    for entry in core.trace:
        if entry.standing is not CheckStanding.NOT_EVALUATED_BY_PREREQUISITE:
            continue
        lines.append(f"  {entry.law} blocked_by={entry.blocked_by}")
    return tuple(lines)
