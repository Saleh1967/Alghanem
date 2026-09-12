"""الاختبارُ الفارق للمستوى الثاني: يُسجَّل ما يقع كما يقع، ولا يُدَّعى ما لم يقع.

**والمقروءُ هنا شيئان لا ثالثَ لهما**: (١) أنّ الاختبار الفارق **لم يُجرَ بعد**
لأنّ تعدادَ الإسنادات في بطاقة التركيب الحقيقية ما زال خاليًا؛ (٢) أنّ تطابقَ
أجناس الوقوف عبر المستويين تطابقُ روايةٍ لا تطابقُ دراية، فلا يُبنى عليه ادّعاءٌ
فركتاليّ.

**ولا حكمَ فقهيًّا هنا ولا حكمَ فركتاليًّا**: الوحدةُ المفحوصة تُسمّي جنسَ
التطابق المؤهَّل للقراءة ولا تُصدر حكمًا بوقوع فركتاليّةٍ ولا بانتفائها.
"""

import hashlib
import json
from pathlib import Path
from typing import Any, Final

import pytest

from alghanem.arabic.level_two_discrimination import (
    ARITY_IS_NOT_A_LINGUISTIC_STRUCTURE_NOTE,
    IDENTICAL_STOP_GENUS_IS_NOT_FRACTAL_EVIDENCE_NOTE,
    LEVEL_TWO_DISCRIMINATION_PREREGISTRATION,
    SINGLE_ATTRIBUTION_STOP_IS_AN_ARITY_ARTIFACT_NOTE,
    STRUCTURALLY_UNFALSIFIABLE_NEGATIVE_IS_A_RECURRING_PATTERN_NOTE,
    DiscriminationBranch,
    LevelTwoDiscriminationError,
    StopDataStanding,
    StopMatchGenus,
    StopReading,
    card_stop_data_standing,
    card_stop_reading,
    discrimination_branch,
    stop_match_genus,
)
from alghanem.arabic.level_two_manat import (
    ClosedLevelOneCard,
    CompositionGenus,
    CompositionRole,
    LevelTwoCompositionInput,
    LevelTwoStopGenus,
    TaqyeedManatGate,
)
from alghanem.arabic.lexical_transmission import LEXICAL_CHAIN_MINIMUM_ATTRIBUTIONS
from alghanem.arabic.manat_verification import assess_manat_from_card
from alghanem.arabic.transmission_standing import UnconstructibilityGenus
from alghanem.encyclopedia.self_observation import (
    RepositoryArtifactRef,
    RepositoryObservationAuthority,
    RepositorySnapshotRef,
)
from alghanem.kernel import AuthenticatedObservationBinding

_ROOT: Final = Path(__file__).resolve().parents[2]
_LEVEL_TWO: Final = _ROOT / "examples" / "level_two_manat"
_EXTERNAL: Final = _ROOT / "examples" / "external_audit"
_GHANAM: Final = _LEVEL_TWO / "ghanam_bukhari.yaml"
_SAIMA: Final = _LEVEL_TWO / "saima_bukhari.yaml"
_COMPOSITION: Final = _LEVEL_TWO / "ghanam_saima_composition.yaml"
_LEVEL_ONE_CARDS: Final = (
    "quru_2_228.yaml",
    "anna_2_223.yaml",
    "malik_114_2.yaml",
    "assa_81_17.yaml",
)


class _CardFileProvider:
    """سلطةُ مصدرٍ تُوثِّق البطاقة ببايتاتها الفعلية؛ لا تمنح دليلًا ولا سلطة."""

    provider_identity = "level-two-discrimination-card-file-provider"
    implementation_identity = "level-two-discrimination-card-file-provider-sha256"
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


def _card(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(payload, dict)
    return payload


def _binding(path: Path) -> AuthenticatedObservationBinding:
    provider = _CardFileProvider(path)
    run = RepositoryObservationAuthority(provider).open_run()
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    snapshot = run.observe_snapshot(RepositorySnapshotRef("Alghanem", digest, digest))
    artifact = run.observe_artifact(
        snapshot,
        RepositoryArtifactRef(
            snapshot.snapshot, f"examples/level_two_manat/{path.name}", digest
        ),
    )
    return run.bridge_authenticated_fragment(run.observe_fragment(artifact, "البطاقة"))


def _closed(path: Path, role: CompositionRole) -> ClosedLevelOneCard:
    card = _card(path)
    return ClosedLevelOneCard(
        role=role, card=card, assessment=assess_manat_from_card(card, _binding(path))
    )


def _composition_input() -> LevelTwoCompositionInput:
    return LevelTwoCompositionInput(
        described=_closed(_GHANAM, CompositionRole.موصوف),
        descriptor=_closed(_SAIMA, CompositionRole.صفة),
        composition_card=_card(_COMPOSITION),
        declared_genus=CompositionGenus.تقييدية,
    )


def test_every_branch_is_registered_with_what_it_licenses_and_what_it_refuses() -> None:
    """التغطيةُ تسبق القراءة: كلُّ فرعٍ مُسمًّى بنصَّيه قبل نقل أيّ إسناد."""

    registration = LEVEL_TWO_DISCRIMINATION_PREREGISTRATION

    assert set(registration.registered_branches) == set(DiscriminationBranch)
    for branch in DiscriminationBranch:
        entry = registration.registration_for(branch)
        assert entry.licensed_reading.strip()
        assert entry.refused_reading.strip()
    assert "تعدادُ `الإسنادات`" in registration.controlled_variable
    assert len(registration.fixed_elements) >= 2
    assert {refusal.name for refusal in registration.refusals} >= {
        "SingleAttributionStopIsAnArityArtifact",
        "IdenticalStopGenusIsNotFractalEvidenceWhileDataIsAbsent",
        "ArityIsNotALinguisticStructure",
        "StructurallyUnfalsifiableNegativeIsARecurringPattern",
    }


def test_the_recurring_pattern_is_named_with_its_prospective_question() -> None:
    """النمطُ المتكرّر يُسمّى بسؤاله الاستباقيّ، لا يُنتظَر اكتشافُه بعد كلّ بناء."""

    assert (
        "أيُّ مدخلٍ واقعيٍّ يُفنّد وقوفَها؟"
        in STRUCTURALLY_UNFALSIFIABLE_NEGATIVE_IS_A_RECURRING_PATTERN_NOTE
    )
    assert "متواتر" in STRUCTURALLY_UNFALSIFIABLE_NEGATIVE_IS_A_RECURRING_PATTERN_NOTE
    assert str(LEXICAL_CHAIN_MINIMUM_ATTRIBUTIONS) in (
        SINGLE_ATTRIBUTION_STOP_IS_AN_ARITY_ARTIFACT_NOTE
    )


def test_the_real_composition_card_has_not_been_supplied_with_any_attribution() -> None:
    """بطاقةُ التركيب الحقيقية اليوم: لا إسنادَ منقولًا، فالاختبارُ لم يُجرَ."""

    composition_card = _card(_COMPOSITION)
    attempt = TaqyeedManatGate.assess(_composition_input())

    assert composition_card["طريق_النقل_المعجمي"]["الإسنادات"] == []
    assert card_stop_data_standing(composition_card) is StopDataStanding.لا_إسناد_منقول
    assert attempt.stood_up is False
    assert attempt.stop_genus is LevelTwoStopGenus.وقوف_آلة_لانقطاع_نقل_القيد
    assert (
        discrimination_branch(attempt, composition_card)
        is DiscriminationBranch.لم_يُزوَّد_بإسناد_بعد
    )


def test_the_branch_reading_of_today_forbids_any_cross_level_match_claim() -> None:
    """الفرعُ القائم اليوم يمنع ادّعاءَ التطابق بنصّه المُسجَّل قبل القراءة."""

    entry = LEVEL_TWO_DISCRIMINATION_PREREGISTRATION.registration_for(
        DiscriminationBranch.لم_يُزوَّد_بإسناد_بعد
    )

    assert "لم يُجرَ" in entry.licensed_reading
    assert IDENTICAL_STOP_GENUS_IS_NOT_FRACTAL_EVIDENCE_NOTE in entry.refused_reading


def test_the_four_level_one_cards_and_the_composition_match_only_as_riwaya() -> None:
    """الأجناسُ الأربعة وبطاقةُ التركيب: تطابقُ روايةٍ لا تطابقُ دراية."""

    readings = tuple(
        card_stop_reading(name, _card(_EXTERNAL / name)) for name in _LEVEL_ONE_CARDS
    ) + (card_stop_reading("ghanam_saima_composition", _card(_COMPOSITION)),)

    assert all(
        reading.genus is UnconstructibilityGenus.REFUSED_BY_STRUCTURAL_CATEGORY_MISMATCH
        for reading in readings
    )
    assert all(reading.data is StopDataStanding.لا_إسناد_منقول for reading in readings)
    assert stop_match_genus(readings) is StopMatchGenus.تطابق_رواية
    assert stop_match_genus(readings) is not StopMatchGenus.تطابق_دراية_مرشح


def test_a_single_attribution_reading_is_never_read_as_a_match() -> None:
    """قراءةٌ بإسنادٍ واحدٍ تُبقي التطابقَ غيرَ محسوم، ولو اتّحد الجنسان."""

    flat = UnconstructibilityGenus.REFUSED_BY_STRUCTURAL_CATEGORY_MISMATCH
    readings = (
        StopReading("أوّل", flat, StopDataStanding.إسناد_واحد_منقول),
        StopReading("ثانٍ", flat, StopDataStanding.إسناد_واحد_منقول),
    )

    assert stop_match_genus(readings) is StopMatchGenus.تطابق_غير_محسوم
    assert "لا بنيةٌ لغويةٌ" in ARITY_IS_NOT_A_LINGUISTIC_STRUCTURE_NOTE


def test_a_candidate_diraya_match_needs_every_side_above_the_threshold() -> None:
    """تطابقُ الدراية المرشَّح لا يقوم إلّا ببلوغ كلِّ طرفٍ عتبةَ التعاقب."""

    held = UnconstructibilityGenus.HELD_BY_MISSING_AUTHORITY_TODAY
    chained = (
        StopReading("أوّل", held, StopDataStanding.إسناد_متعاقب_منقول),
        StopReading("ثانٍ", held, StopDataStanding.إسناد_متعاقب_منقول),
    )
    mixed = (
        chained[0],
        StopReading("ثالث", held, StopDataStanding.لا_إسناد_منقول),
    )

    assert stop_match_genus(chained) is StopMatchGenus.تطابق_دراية_مرشح
    assert stop_match_genus(mixed) is StopMatchGenus.تطابق_رواية


def test_differing_genera_are_not_a_match_at_all() -> None:
    """اختلافُ الجنسين لا تطابقَ فيه، ولا يُحمَل على أحد طرفيه."""

    readings = (
        StopReading(
            "أوّل",
            UnconstructibilityGenus.REFUSED_BY_STRUCTURAL_CATEGORY_MISMATCH,
            StopDataStanding.لا_إسناد_منقول,
        ),
        StopReading(
            "ثانٍ",
            UnconstructibilityGenus.HELD_BY_MISSING_AUTHORITY_TODAY,
            StopDataStanding.إسناد_متعاقب_منقول,
        ),
    )

    assert stop_match_genus(readings) is StopMatchGenus.لا_تطابق


def test_one_reading_alone_does_not_match_itself() -> None:
    """قراءةٌ واحدةٌ لا تُطابق نفسها، فالتطابقُ نسبةٌ بين طرفين فأكثر."""

    single = (
        StopReading(
            "وحيدة",
            UnconstructibilityGenus.GENUS_NOT_SETTLED,
            StopDataStanding.لا_إسناد_منقول,
        ),
    )

    with pytest.raises(LevelTwoDiscriminationError, match="قراءتين"):
        stop_match_genus(single)
