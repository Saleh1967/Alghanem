"""جنس القرينة المُقصِية مطبَّقًا على «أنّى» في البقرة:223.

هذا امتدادٌ لقانون `G0.EA.1` القائم لا قانونٌ جديد: جنس البيان وترتيبه
المُشتقّ لم يتغيّرا، وأُضيفت بجانبهما وظيفةُ القرينة (مؤيِّدة/مُقصِية). والإقصاء
نوعٌ لا درجة، ولا يُقصي بيانُ الفعل وحده، ولا يتراكم المؤيِّد حتى يصير مُقصيًا.
"""

import hashlib
import json
from pathlib import Path
from typing import Any

import pytest

from alghanem.arabic.manat_verification import (
    QAWL_MODEL_ID,
    BayanKind,
    ManatVerificationError,
    QarinaFunction,
    assess_manat_from_card,
    eliminated_competing_readings,
    manat_claim_scope,
    read_manat_qarain,
    undetermined_competing_readings,
)
from alghanem.encyclopedia.self_observation import (
    RepositoryArtifactRef,
    RepositoryObservationAuthority,
    RepositorySnapshotRef,
)
from alghanem.kernel import (
    ApplicabilityAssessmentStatus,
    AuthenticatedObservationBinding,
    ClaimScopeRef,
)

_EXAMPLES = Path(__file__).resolve().parents[2] / "examples" / "external_audit"
_CARD_PATH = _EXAMPLES / "anna_2_223.yaml"
_QURU_PATH = _EXAMPLES / "quru_2_228.yaml"


class CardFileProvider:
    """سلطةُ مصدرٍ تُوثِّق البطاقة ببايتاتها الفعلية على القرص."""

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


def _card(path: Path = _CARD_PATH) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def _binding(path: Path = _CARD_PATH) -> AuthenticatedObservationBinding:
    provider = CardFileProvider(path)
    run = RepositoryObservationAuthority(provider).open_run()
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    snapshot = run.observe_snapshot(RepositorySnapshotRef("Alghanem", digest, digest))
    artifact = run.observe_artifact(
        snapshot,
        RepositoryArtifactRef(
            snapshot.snapshot, f"examples/external_audit/{path.name}", digest
        ),
    )
    return run.bridge_authenticated_fragment(run.observe_fragment(artifact, "البطاقة"))


def _negating(card: dict[str, Any]) -> dict[str, Any]:
    (entry,) = (
        item
        for item in card["قرائن_المناط"]
        if item.get("وظيفة_القرينة") == QarinaFunction.NEGATING.value
    )
    assert isinstance(entry, dict)
    return entry


def test_one_negating_qarina_closes_the_gate_on_the_qawl_model() -> None:
    card = _card()
    assessment = assess_manat_from_card(card, _binding())

    assert assessment.status is ApplicabilityAssessmentStatus.PASS
    assert assessment.residuals == ()
    assert assessment.scope == ClaimScopeRef("كلمة_في_آية", "البقرة:223:أنّى")
    assert manat_claim_scope(card).reference == "البقرة:223:أنّى"
    assert dict(assessment.model_results)[QAWL_MODEL_ID].status is assessment.status


def test_the_excluded_reading_was_undetermined_before_the_elimination() -> None:
    """الإقصاء وحده هو ما أغلق البطاقة، لا تعيينُ العلاقة في البطاقة."""

    card = _card()
    qarain = read_manat_qarain(card)

    assert undetermined_competing_readings(card) == ("من_أين",)
    assert eliminated_competing_readings(card, qarain) == ("من_أين",)


def test_the_elimination_needs_no_supporting_qarina_to_reinforce_it() -> None:
    card = _card()
    card["قرائن_المناط"] = [_negating(card)]

    assert (
        assess_manat_from_card(card, _binding()).status
        is ApplicabilityAssessmentStatus.PASS
    )


def test_repeating_a_supporting_qarina_never_becomes_an_elimination() -> None:
    card = _card()
    negating = _negating(card)
    supporting = next(item for item in card["قرائن_المناط"] if item is not negating)
    card["قرائن_المناط"] = [
        {**supporting, "معرف": f"{supporting['معرف']}-{index}"} for index in range(5)
    ]

    assessment = assess_manat_from_card(card, _binding())

    assert assessment.status is ApplicabilityAssessmentStatus.DEFER
    assert [residual for residual in assessment.residuals]


def test_a_preferred_reading_described_as_negating_is_refused_at_construction() -> None:
    card = _card()
    _negating(card)["القرينة"] = (
        "قراءة (أنّى) بمعنى (كيف) أرجح من قراءة (من أين) في هذا الموضع"
    )

    with pytest.raises(ManatVerificationError, match="EliminationIsAKindNotADegree"):
        read_manat_qarain(card)


def test_a_negating_statement_without_any_impossibility_is_refused() -> None:
    card = _card()
    _negating(card)["القرينة"] = "قوله (فَأْتُوا حَرْثَكُمْ) يدلّ على موضع الحرث"

    with pytest.raises(ManatVerificationError, match="EliminationIsAKindNotADegree"):
        read_manat_qarain(card)


def test_a_lexical_negation_alone_cannot_build_a_card() -> None:
    card = _card()
    negating = _negating(card)
    negating["جنس_البيان"] = BayanKind.FIL.value
    card["قرائن_المناط"] = [negating]

    with pytest.raises(ManatVerificationError, match="FilNeverDecidesAlone"):
        read_manat_qarain(card)


def test_a_lexical_negation_beside_a_qawl_qarina_eliminates_nothing() -> None:
    card = _card()
    _negating(card)["جنس_البيان"] = BayanKind.FIL.value
    qarain = read_manat_qarain(card)

    assert eliminated_competing_readings(card, qarain) == ()
    assert (
        assess_manat_from_card(card, _binding()).status
        is ApplicabilityAssessmentStatus.DEFER
    )


def test_two_unelimated_rivals_still_defer_with_their_own_residuals() -> None:
    card = _card()
    card["القراءات_المنافسة"].extend(
        [
            {
                "قراءة": "متى",
                "علاقة_بالنموذج_المختبر": "غير_متعينة",
                "سبب_الإخلال_بالفهم": "اشتراك",
            },
            {
                "قراءة": "حيث",
                "علاقة_بالنموذج_المختبر": "غير_متعينة",
                "سبب_الإخلال_بالفهم": "اشتراك",
            },
        ]
    )

    assessment = assess_manat_from_card(card, _binding())

    assert assessment.status is ApplicabilityAssessmentStatus.DEFER
    descriptions = [residual.description for residual in assessment.residuals]
    assert len(descriptions) == 2
    assert any("متى" in text for text in descriptions)
    assert any("حيث" in text for text in descriptions)
    assert not any("من_أين" in text for text in descriptions)


def test_an_invented_qarina_function_is_refused() -> None:
    card = _card()
    _negating(card)["وظيفة_القرينة"] = "قرينة_مختلطة"

    with pytest.raises(ManatVerificationError, match="وظيفة_القرينة"):
        read_manat_qarain(card)


def test_an_excluded_reading_that_names_no_declared_rival_is_refused() -> None:
    card = _card()
    _negating(card)["القراءة_المُقصاة"] = "قراءة_غير_مُعلَنة"

    with pytest.raises(ManatVerificationError, match="القراءة_المُقصاة"):
        read_manat_qarain(card)


def test_a_supporting_qarina_may_not_carry_an_excluded_reading() -> None:
    card = _card()
    negating = _negating(card)
    negating["وظيفة_القرينة"] = QarinaFunction.SUPPORTING.value

    with pytest.raises(ManatVerificationError, match="القراءة_المُقصاة"):
        read_manat_qarain(card)


def test_a_declared_rank_is_still_refused_on_this_card() -> None:
    card = _card()
    _negating(card)["رتبة"] = "١"

    with pytest.raises(ManatVerificationError, match="لا تحمل رتبةً"):
        read_manat_qarain(card)


def test_an_undeclared_function_reads_as_supporting_and_quru_is_unchanged() -> None:
    """البطاقة القديمة بلا تصريح وظيفةٍ تبقى على حالها: DEFER بفضلةٍ مُسمّاة."""

    card = _card(_QURU_PATH)
    qarain = read_manat_qarain(card)

    assert all(item.function is QarinaFunction.SUPPORTING for item in qarain)
    assert all(item.excluded_reading is None for item in qarain)
    assert eliminated_competing_readings(card, qarain) == ()

    assessment = assess_manat_from_card(card, _binding(_QURU_PATH))
    assert assessment.status is ApplicabilityAssessmentStatus.DEFER
    assert all("طهر" in residual.description for residual in assessment.residuals)
