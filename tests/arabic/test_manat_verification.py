"""أول تشغيلٍ لبوّابة G0.EA.1 على كلمةٍ عربية: (قُرُوء) في البقرة:228.

`ExternalAuditor != KernelAuthority` محفوظ: البطاقة تُعلن قرائنها وعلاقات
قراءاتها، والبوّابة تشتقّ حالتها من النماذج المُسجَّلة وحدها. والنتيجة
المتوقَّعة `DEFER` بفضلةٍ مُسمّاة، وهي المقصودة لا نقصٌ يُصلَح.
"""

import hashlib
import json
from pathlib import Path
from typing import Any

import pytest

from alghanem.arabic.manat_verification import (
    FIL_MODEL_ID,
    ONE_SOUND_ELIMINATION_SUFFICES_NOTE,
    PREPONDERANCE_SOUGHT_IS_NOT_ELIMINATION_LICENSED_NOTE,
    QAWL_MODEL_ID,
    TAADUL_IS_NEVER_A_SETTLED_RESULT_NOTE,
    BayanKind,
    ManatVerificationError,
    assess_manat_from_card,
    build_manat_candidate,
    derive_bayan_models,
    manat_claim_scope,
    read_manat_qarain,
    seal_bayan_evaluators,
)
from alghanem.encyclopedia.self_observation import (
    RepositoryArtifactRef,
    RepositoryObservationAuthority,
    RepositorySnapshotRef,
)
from alghanem.kernel import (
    ApplicabilityAssessmentGate,
    ApplicabilityAssessmentSpecification,
    ApplicabilityAssessmentStatus,
    AuthenticatedObservationBinding,
    ClaimScopeRef,
)

_CARD_PATH = (
    Path(__file__).resolve().parents[2]
    / "examples"
    / "external_audit"
    / "quru_2_228.yaml"
)


class CardFileProvider:
    """سلطةُ مصدرٍ تُوثِّق البطاقة ببايتاتها الفعلية على القرص.

    ليست مزوّدَ `git`: عناوين اللقطة مشتقّة من بايتات الملف نفسه، والتوثيق
    الفعليّ هو مطابقة بصمة البايتات. وهي لا تمنح دليلًا ولا سلطة
    (`AuthenticatedObservationIsNotEvidence`).
    """

    provider_identity = "card-file-provider"
    implementation_identity = "card-file-provider-sha256"
    protocol_version = "1"

    def __init__(self, path: Path) -> None:
        self._path = path
        self._digest = hashlib.sha256(path.read_bytes()).hexdigest()

    def resolve_repository(self, repository_identity: str) -> object | None:
        return repository_identity if repository_identity == "Alghanem" else None

    def resolve_commit(self, repository: object, commit_sha: str) -> object | None:
        return commit_sha if commit_sha == self._digest else None

    def tree_for_commit(self, commit: object) -> str | None:
        return self._digest

    def blob_at_path(self, tree_sha: str, artifact_path: str) -> str | None:
        candidate = Path(artifact_path)
        if candidate.name != self._path.name:
            return None
        return self._digest

    def fragment_from_blob(self, blob_sha: str, fragment_locator: str) -> str | None:
        return f"{blob_sha}/{fragment_locator}"

    def is_ancestor(
        self, repository: object, from_commit_sha: str, to_commit_sha: str
    ) -> bool:
        return False


def _card() -> dict[str, Any]:
    payload = json.loads(_CARD_PATH.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def _binding() -> AuthenticatedObservationBinding:
    provider = CardFileProvider(_CARD_PATH)
    run = RepositoryObservationAuthority(provider).open_run()
    digest = hashlib.sha256(_CARD_PATH.read_bytes()).hexdigest()
    snapshot = run.observe_snapshot(RepositorySnapshotRef("Alghanem", digest, digest))
    artifact = run.observe_artifact(
        snapshot,
        RepositoryArtifactRef(
            snapshot.snapshot, "examples/external_audit/quru_2_228.yaml", digest
        ),
    )
    return run.bridge_authenticated_fragment(run.observe_fragment(artifact, "البطاقة"))


def test_quru_card_defers_with_named_residuals() -> None:
    assessment = assess_manat_from_card(_card(), _binding())

    assert assessment.status is ApplicabilityAssessmentStatus.DEFER
    assert assessment.residuals
    assert all("طهر" in residual.description for residual in assessment.residuals)
    assert assessment.scope == ClaimScopeRef("كلمة_في_آية", "البقرة:228:قُرُوء")


def test_qawl_holds_the_non_overridable_position_and_fil_never_overrides_it() -> None:
    card = _card()
    qarain = read_manat_qarain(card)
    models = derive_bayan_models(qarain)

    by_id = {model.model_id: model for model in models}
    assert by_id[QAWL_MODEL_ID].weaker_model_ids == ()
    assert by_id[FIL_MODEL_ID].weaker_model_ids == (QAWL_MODEL_ID,)

    assessment = assess_manat_from_card(card, _binding())
    decisive = dict(assessment.model_results)[QAWL_MODEL_ID]
    assert decisive.status is assessment.status
    assert all(residual in decisive.residuals for residual in assessment.residuals)


def test_a_lexical_indication_alone_cannot_build_a_card() -> None:
    card = _card()
    card["قرائن_المناط"] = [
        item
        for item in card["قرائن_المناط"]
        if item["جنس_البيان"] == BayanKind.FIL.value
    ]

    with pytest.raises(ManatVerificationError, match="FilNeverDecidesAlone"):
        read_manat_qarain(card)


def test_a_declared_rank_is_refused_rather_than_ignored() -> None:
    card = _card()
    card["قرائن_المناط"][0]["رتبة"] = "١"

    with pytest.raises(ManatVerificationError, match="لا تحمل رتبةً"):
        read_manat_qarain(card)


def test_an_invented_bayan_kind_is_refused() -> None:
    card = _card()
    card["قرائن_المناط"][0]["جنس_البيان"] = "بيان_مختلط"

    with pytest.raises(ManatVerificationError, match="جنس_البيان"):
        read_manat_qarain(card)


def test_evaluators_sealed_for_another_scope_are_refused_by_the_gate() -> None:
    card = _card()
    other = dict(card)
    other["الكلمة_المدروسة"] = "عسعس"
    qarain = read_manat_qarain(card)
    registry = seal_bayan_evaluators(other, qarain)
    specification = ApplicabilityAssessmentSpecification(derive_bayan_models(qarain))

    with pytest.raises(ValueError, match="not authorized"):
        ApplicabilityAssessmentGate.assess(
            build_manat_candidate(card, _binding()), specification, registry
        )


def test_a_declared_verdict_in_the_card_changes_nothing() -> None:
    card = _card()
    baseline = assess_manat_from_card(card, _binding())
    card["نتيجة_تحقيق_المناط"] = "PASS"

    assert assess_manat_from_card(card, _binding()).status is baseline.status


def test_resolving_every_competing_reading_closes_on_the_qawl_model() -> None:
    card = _card()
    for reading in card["القراءات_المنافسة"]:
        reading["علاقة_بالنموذج_المختبر"] = "أضعف_صوريًّا"

    assessment = assess_manat_from_card(card, _binding())

    assert assessment.status is ApplicabilityAssessmentStatus.PASS
    assert assessment.residuals == ()
    assert manat_claim_scope(card).reference == "البقرة:228:قُرُوء"


def test_a_defer_is_read_as_an_unfound_preponderance_not_as_a_settled_balance() -> None:
    """`DEFER` names what is still sought; it is never a closed conclusion."""

    assessment = assess_manat_from_card(_card(), _binding())

    assert assessment.status is ApplicabilityAssessmentStatus.DEFER
    assert assessment.residuals
    for residual in assessment.residuals:
        assert "ما زالت غير متعينة بعد هذه القرائن" in residual.description
        assert "البحث عن قرينةٍ مُرجِّحة إضافية باقٍ مطلوبًا" in residual.description
        assert TAADUL_IS_NEVER_A_SETTLED_RESULT_NOTE in residual.description

    assert "لم يُكتشَف المرجِّح" in TAADUL_IS_NEVER_A_SETTLED_RESULT_NOTE
    assert "التشهّي" in TAADUL_IS_NEVER_A_SETTLED_RESULT_NOTE


def test_the_open_research_marker_licenses_no_elimination() -> None:
    assert "أضعف من المُقصِية" in PREPONDERANCE_SOUGHT_IS_NOT_ELIMINATION_LICENSED_NOTE
    assert (
        "ONE_SOUND_ELIMINATION_SUFFICES_NOTE"
        in PREPONDERANCE_SOUGHT_IS_NOT_ELIMINATION_LICENSED_NOTE
    )
    assert "تراكمَ مؤيِّدات" in ONE_SOUND_ELIMINATION_SUFFICES_NOTE


def test_a_closed_assessment_carries_no_open_research_residual() -> None:
    card = _card()
    for reading in card["القراءات_المنافسة"]:
        reading["علاقة_بالنموذج_المختبر"] = "أضعف_صوريًّا"

    assessment = assess_manat_from_card(card, _binding())

    assert assessment.status is ApplicabilityAssessmentStatus.PASS
    assert assessment.residuals == ()
