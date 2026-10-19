"""The first end-to-end run of the G0.IC.1a closure gate on a real card.

`ExternalAuditor != KernelAuthority` is preserved throughout: the card
supplies only a `BirthExperimentSpecification` (through the existing,
non-authoritative `build_birth_spec_from_card`), and neither its external
audit result nor its Arabic `علاقة_بالنموذج_المختبر` declarations enter the
kernel. The gate derives its own status from the frozen projection poset
alone.
"""

import json
from pathlib import Path

from alghanem.arabic.external_audit import build_birth_spec_from_card
from alghanem.kernel.birth import BirthAssessmentRequest
from alghanem.kernel.evidence_acquisition import EvidenceAcquisitionAuthority
from alghanem.kernel.experiment_spec_content_identity import (
    BirthExperimentSpecificationContentBinding,
    CanonicalBirthExperimentSpecificationEncoder,
    PreEvidenceSpecificationRegistry,
)
from alghanem.kernel.independent_closure import (
    ClosureScopeRegistry,
    ComparabilityClosureStatus,
    IndependentClosureGate,
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


def test_hadhan_card_leaves_competition_unresolved_through_the_closure_gate() -> None:
    request = _hadhan_request()
    registry = ClosureScopeRegistry()
    registry.register(scope_id="scope-hadhan-20-63", binding=request.experiment_binding)

    assessment = IndependentClosureGate.assess(
        registry=registry.seal("registry-hadhan-20-63"), request=request
    )

    assert (
        assessment.status is ComparabilityClosureStatus.COMPETITION_UNRESOLVED_IN_POSET
    )
    assert assessment.is_independent_closure is False
    assert assessment.scope.test_model == "لغة_بلحارث_ألف_ثابتة"
    assert assessment.open_prerequisite_models == ()
    assert assessment.incomparable_competitors == (
        "تصحيح_لفظي_هذين",
        "تخفيف_إن_وضمير_شأن",
        "مذهب_كنانة_قلب_الألف_ياء",
        "شاذ_آحاد_ما_هذان_إلا_ساحران",
    )
    assert "MultipleIncomparableMinimalFactorizationsDefer" in assessment.reason


def test_the_card_declares_every_relation_undetermined_not_incomparable() -> None:
    """The card says `غير_متعينة`; the kernel reads only the frozen poset.

    The two are not the same claim. The gate never reads this Arabic field,
    and its conservative treatment of an absent strict relation is what makes
    the two agree here rather than any coupling between them.
    """

    card = json.loads(_CARD.read_text(encoding="utf-8"))

    assert card["تعريف_التجربة"]["strict_relations"] == []
    assert [
        reading["علاقة_بالنموذج_المختبر"] for reading in card["القراءات_المنافسة"]
    ] == ["غير_متعينة"] * 4
