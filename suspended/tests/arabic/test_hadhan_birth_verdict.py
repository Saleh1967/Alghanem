"""The first end-to-end run of the G0.BV.1a verdict authority on a real card.

`ExternalAuditor != KernelAuthority` is preserved throughout: the card
supplies only a `BirthExperimentSpecification` (through the existing,
non-authoritative `build_birth_spec_from_card`), and its external audit
result never enters the kernel. The gate derives its own status from the
frozen projection poset alone.
"""

import json
from pathlib import Path

from alghanem.arabic.external_audit import audit_card, build_birth_spec_from_card
from alghanem.kernel.birth import BirthAssessmentRequest, BirthVerdictStatus
from alghanem.kernel.birth_verdict import (
    BirthVerdictGate,
    BirthVerdictScopeRegistry,
)
from alghanem.kernel.evidence_acquisition import EvidenceAcquisitionAuthority
from alghanem.kernel.experiment_spec_content_identity import (
    BirthExperimentSpecificationContentBinding,
    CanonicalBirthExperimentSpecificationEncoder,
    PreEvidenceSpecificationRegistry,
)

_CARD = (
    Path(__file__).resolve().parents[2]
    / "examples"
    / "external_audit"
    / "hadhan_20_63.yaml"
)


def _hadhan_request() -> BirthAssessmentRequest:
    card = json.loads(_CARD.read_text(encoding="utf-8"))
    specification = build_birth_spec_from_card(card)
    frozen = PreEvidenceSpecificationRegistry().freeze(
        CanonicalBirthExperimentSpecificationEncoder.encode(specification)
    )
    binding = BirthExperimentSpecificationContentBinding(specification, frozen)
    authorization = EvidenceAcquisitionAuthority().authorize(
        authorization_id="auth-hadhan-20-63", binding=binding
    )
    run = authorization.open_run("run-hadhan-20-63")
    snapshot = run.ingest(
        snapshot_id="snapshot-hadhan-20-63",
        payload=json.dumps(card["الأدلة"], ensure_ascii=False),
        trace="declared-witnesses-of-hadhan-20-63",
    )
    return BirthAssessmentRequest(
        experiment_binding=binding, evidence_snapshot=snapshot
    )


def test_hadhan_card_defers_in_scope_through_the_verdict_gate() -> None:
    request = _hadhan_request()
    registry = BirthVerdictScopeRegistry()
    registry.register(scope_id="scope-hadhan-20-63", binding=request.experiment_binding)

    decision = BirthVerdictGate.assess(
        registry=registry.seal("registry-hadhan-20-63"), request=request
    )

    assert decision.status is BirthVerdictStatus.DEFER_IN_SCOPE
    assert decision.is_birth is False
    assert decision.scope.test_model == "لغة_بلحارث_ألف_ثابتة"
    assert decision.open_prerequisite_models == ()
    assert decision.unresolved_competing_models == (
        "تصحيح_لفظي_هذين",
        "تخفيف_إن_وضمير_شأن",
        "مذهب_كنانة_قلب_الألف_ياء",
        "شاذ_آحاد_ما_هذان_إلا_ساحران",
    )
    assert "MultipleIncomparableMinimalFactorizationsDefer" in decision.reason


def test_kernel_verdict_is_derived_independently_of_the_external_audit() -> None:
    external = audit_card(_CARD)
    scope_request = _hadhan_request()
    registry = BirthVerdictScopeRegistry()
    registry.register(scope_id="scope", binding=scope_request.experiment_binding)
    sealed = registry.seal("registry")

    decision = BirthVerdictGate.assess(registry=sealed, request=_hadhan_request())

    assert external.نتيجة_التدقيق_الخارجي == "DEFER_التدقيق"
    assert decision.status is BirthVerdictStatus.DEFER_IN_SCOPE
    assert decision.unresolved_competing_models == tuple(
        external.الإسقاطات_المنافسة_المشتقة
    )
