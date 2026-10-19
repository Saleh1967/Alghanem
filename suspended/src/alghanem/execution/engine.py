"""المحرّك: من وثيقةٍ مُصرَّحٍ بها إلى حكمٍ مختومٍ قابلٍ للتدقيق وإعادة التشغيل.

    Declaration → Validation → PartialDerivation → LawEvaluation
                      ↘ INVALID_INPUT (ليس حكمًا)
    BLOCK | DEFER
    PASS → Materialization → MaterializedIdentity

**والحكمُ يسبق الإنشاء** (`JudgmentPrecedesConstruction`): لا تُنشَأ
`AnchoredNisbahSignatureV3` إلّا بعد `PASS` مبدئيّ؛ لأنّ بانيها يرفض اختلاطَ
الأصل، فلو أُنشئت قبل الحكم لأصدر الباني الحكمَ بدل المحرّك ولَما بقي أثر.

**وبطلانُ الإدخال ليس حجبًا** (`InvalidInputIsNotABlock`): الوثيقةُ التي لا تقوم
منها قضيّةٌ لا تُصدِر `BLOCK`؛ إنّما تُصدِر `InputValidation` لا حكمَ معها.

**وفشلُ التشييد بعد النجاح ليس حجبًا** (`AMaterializationFailureIsNotABlock`):
إن أجازت القوانينُ كلُّها القضيّةَ ثمّ تعذّر تشييدُ النسبة، فذلك عطبُ محرّكٍ أو
نقصٌ في قائمة القوانين؛ فيُرفَع `ExecutionInvariantError` ولا يُختَم غلاف. وهو
الاستثناءُ الوحيدُ الذي يخرج من هذا الباب، وليس حكمًا.

تسجيلٌ لا سلطة: لا ولادةَ ولا حكمَ ولادةٍ ولا تجميدَ `E0`.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from ..linguistic.anchored_v3 import (
    AnchoredArgumentSlotV3,
    AnchoredNisbahSignatureV3,
    AnchoredPredicateSignatureV3,
    AnchoredTermAnchorV3,
    AnchoredV3Error,
)
from ..linguistic.nisbah import ArityLicenseGenus
from .contract import decode_document
from .declaration import CaseDeclaration
from .derivation import (
    PartialAuthorityDerivation,
    SiteKey,
    SiteOwnerKind,
    derive_partial_authority,
)
from .invariant import (
    A_MATERIALIZATION_FAILURE_IS_NOT_A_BLOCK,
    ExecutionInvariantError,
)
from .laws import aggregate_outcome, evaluate_laws, residuals_of, violations_of
from .lawset import LAW_SET_DIGEST, LAW_SET_ID, ExecutionLaw
from .outcome import CheckStanding, ExecutionOutcome, Identity, LawCheckEntry
from .result import (
    EXECUTION_RESULT_SCHEMA,
    ExecutionResultCore,
    ExecutionResultEnvelope,
    LineageIdentity,
)
from .standing import InputValidation
from .validation import validate_declaration

__all__ = [
    "ExecutionReport",
    "execute_declaration",
    "execute_document",
]


@dataclass(frozen=True, slots=True)
class ExecutionReport:
    """ناتجُ تشغيلٍ واحد: قيامُ الإدخال، ثمّ الحكمُ إن قامت القضيّةُ أصلًا."""

    validation: InputValidation
    envelope: ExecutionResultEnvelope | None

    def __post_init__(self) -> None:
        if not isinstance(self.validation, InputValidation):
            raise TypeError("قيامُ الإدخال من نوعه")
        if self.validation.is_valid != (self.envelope is not None):
            raise TypeError(
                "إدخالٌ باطلُ التكوين لا حكمَ معه، وإدخالٌ قائمٌ لا يخلو من حكم؛ "
                "وبطلانُ الإدخال ليس حجبًا"
            )


def _lineage_identity(
    derivation: PartialAuthorityDerivation,
) -> LineageIdentity | None:
    lineage = derivation.lineage.subject
    if lineage is None:
        return None
    return LineageIdentity(
        base=Identity(id=lineage.base_id, content_id=lineage.base_content_id),
        general_ontology=Identity(
            id=lineage.general_ontology_id, content_id=lineage.general_content_id
        ),
        linguistic_ontology=Identity(
            id=lineage.linguistic_ontology_id,
            content_id=lineage.linguistic_content_id,
        ),
        content_id=lineage.content_id,
    )


def _materialize(
    declaration: CaseDeclaration, derivation: PartialAuthorityDerivation
) -> AnchoredNisbahSignatureV3:
    """أنشئ النسبةَ السلطويّةَ بعد النجاح؛ وتعذُّرُ الإنشاء عطبُ محرّكٍ لا حجب."""

    lineage = derivation.lineage.subject
    declared_predicate = declaration.nisbah.predicate
    predicate_role = derivation.role_sites.get(
        SiteKey(SiteOwnerKind.PREDICATE, declared_predicate.predicate_id)
    )
    if lineage is None:
        raise ExecutionInvariantError(
            "نجاحٌ مبدئيٌّ بلا سلسلةٍ مُشتَقّة؛ و" + A_MATERIALIZATION_FAILURE_IS_NOT_A_BLOCK
        )
    if predicate_role is None or predicate_role.subject is None:
        raise ExecutionInvariantError(
            f"نجاحٌ مبدئيٌّ بلا دورٍ مُرخَّصٍ للمحمول `{declared_predicate.predicate_id}`؛ و"
            + A_MATERIALIZATION_FAILURE_IS_NOT_A_BLOCK
        )
    slots: list[AnchoredArgumentSlotV3] = []
    for declared_slot in declared_predicate.slots:
        site = derivation.condition_sites.get(
            SiteKey(SiteOwnerKind.SLOT, declared_slot.slot_id)
        )
        if site is None or site.subject is None:
            raise ExecutionInvariantError(
                f"نجاحٌ مبدئيٌّ بلا شرطِ قبولٍ للخانة `{declared_slot.slot_id}`؛ و"
                + A_MATERIALIZATION_FAILURE_IS_NOT_A_BLOCK
            )
        slots.append(
            AnchoredArgumentSlotV3(
                slot_id=declared_slot.slot_id,
                position=declared_slot.position,
                admissibility_condition_ref=site.subject,
            )
        )
    anchors: list[AnchoredTermAnchorV3] = []
    for declared_anchor in declaration.nisbah.anchors:
        key = SiteKey(SiteOwnerKind.ANCHOR, declared_anchor.anchor_id)
        role = derivation.role_sites.get(key)
        condition = derivation.condition_sites.get(key)
        if role is None or role.subject is None:
            raise ExecutionInvariantError(
                f"نجاحٌ مبدئيٌّ بلا دورٍ مُرخَّصٍ للمرتكز `{declared_anchor.anchor_id}`؛ و"
                + A_MATERIALIZATION_FAILURE_IS_NOT_A_BLOCK
            )
        if condition is None or condition.subject is None:
            raise ExecutionInvariantError(
                f"نجاحٌ مبدئيٌّ بلا شرطِ هويّةٍ للمرتكز `{declared_anchor.anchor_id}`؛ و"
                + A_MATERIALIZATION_FAILURE_IS_NOT_A_BLOCK
            )
        anchors.append(
            AnchoredTermAnchorV3(
                anchor_id=declared_anchor.anchor_id,
                role_ref=role.subject,
                identity_condition_ref=condition.subject,
            )
        )
    predicate = AnchoredPredicateSignatureV3(
        predicate_id=declared_predicate.predicate_id,
        role_ref=predicate_role.subject,
        arity=declared_predicate.arity,
        arity_license=ArityLicenseGenus(declared_predicate.arity_license_name),
        slots=tuple(slots),
    )
    try:
        return AnchoredNisbahSignatureV3.in_lineage(
            nisbah_id=declaration.nisbah.nisbah_id,
            lineage=lineage,
            predicate=predicate,
            anchors=tuple(anchors),
        )
    except AnchoredV3Error as refusal:
        raise ExecutionInvariantError(
            f"بابُ `v3` ردّ ما أجازته القوانينُ كلُّها: {refusal}؛ و"
            + A_MATERIALIZATION_FAILURE_IS_NOT_A_BLOCK
        ) from refusal


def _first_law_with(
    trace: tuple[LawCheckEntry, ...], standing: CheckStanding
) -> str | None:
    for entry in trace:
        if entry.standing is standing:
            return entry.law
    return None


def _materialized_identity_entry(
    declaration: CaseDeclaration,
    derivation: PartialAuthorityDerivation,
    provisional: ExecutionOutcome,
    trace: tuple[LawCheckEntry, ...],
) -> tuple[LawCheckEntry, AnchoredNisbahSignatureV3 | None]:
    """القانونُ الثامنَ عشرَ: لا يُقيَّم إلّا بعد النجاح، ولا يُطوى من الأثر."""

    law = ExecutionLaw.MATERIALIZED_IDENTITY_AGREES
    subject = declaration.nisbah.nisbah_id
    claimed = declaration.nisbah.declared_content_id
    expected = None if claimed is None else Identity(id=subject, content_id=claimed)
    materialized: AnchoredNisbahSignatureV3 | None = None
    if provisional is ExecutionOutcome.PASS:
        materialized = _materialize(declaration, derivation)
    observed = (
        None
        if materialized is None
        else Identity(id=subject, content_id=materialized.content_id)
    )
    standing = CheckStanding.SATISFIED
    blocked_by: str | None = None
    if claimed is None:
        standing = CheckStanding.NOT_APPLICABLE_NO_CLAIM
    elif provisional is ExecutionOutcome.BLOCK:
        standing = CheckStanding.NOT_EVALUATED_BY_PREREQUISITE
        blocked_by = _first_law_with(trace, CheckStanding.VIOLATED)
    elif provisional is ExecutionOutcome.DEFER:
        standing = CheckStanding.NOT_EVALUATED_BY_PREREQUISITE
        blocked_by = _first_law_with(trace, CheckStanding.UNRESOLVED)
    elif observed != expected:
        standing = CheckStanding.VIOLATED
    entry = LawCheckEntry(
        law=law.value,
        standing=standing,
        subject_id=subject,
        expected=None
        if standing is CheckStanding.NOT_APPLICABLE_NO_CLAIM
        else expected,
        observed=observed,
        blocked_by=blocked_by,
    )
    return entry, materialized


def execute_declaration(declaration: CaseDeclaration) -> ExecutionReport:
    """نفِّذ تصريحًا قائمًا؛ ولا يخرج من هنا استثناءٌ من أبواب المستويات."""

    validation, levels = validate_declaration(declaration)
    if not validation.is_valid:
        return ExecutionReport(validation=validation, envelope=None)
    derivation = derive_partial_authority(declaration, levels)
    trace = evaluate_laws(declaration, derivation)
    provisional = aggregate_outcome(trace)
    final_entry, materialized = _materialized_identity_entry(
        declaration, derivation, provisional, trace
    )
    trace = trace + (final_entry,)
    outcome = aggregate_outcome(trace)
    core = ExecutionResultCore(
        schema=EXECUTION_RESULT_SCHEMA,
        nisbah_schema=declaration.nisbah_schema,
        input_digest=declaration.input_digest,
        law_set_id=LAW_SET_ID,
        law_set_digest=LAW_SET_DIGEST,
        outcome=outcome,
        trace=trace,
        violations=violations_of(trace),
        residuals=residuals_of(declaration, trace),
        lineage_identity=_lineage_identity(derivation),
        materialized_identity=(
            None
            if outcome is not ExecutionOutcome.PASS or materialized is None
            else Identity(id=materialized.nisbah_id, content_id=materialized.content_id)
        ),
    )
    envelope = ExecutionResultEnvelope.sealing(declaration=declaration, core=core)
    return ExecutionReport(validation=validation, envelope=envelope)


def execute_document(document: Mapping[str, object]) -> ExecutionReport:
    """نفِّذ وثيقةً خامًا؛ وعيوبُ القراءة عيوبُ إدخالٍ لا أحكامًا."""

    decoded = decode_document(document)
    if decoded.declaration is None:
        from .standing import InputStanding

        return ExecutionReport(
            validation=InputValidation(
                standing=InputStanding.INVALID, faults=decoded.faults
            ),
            envelope=None,
        )
    return execute_declaration(decoded.declaration)
