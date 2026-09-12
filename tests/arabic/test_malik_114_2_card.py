"""تطبيقٌ كاملٌ واحد على بطاقة (مَلِك) في الناس:2، مُشغَّلًا على حلقات ٤–١٣.

هذا **اختبارُ تشغيل، لا وحدةُ قياسٍ جديدة**: لا يُنشئ سلطةً ولا مفردةً ولا
دفترًا، ولا يُصدر ولادةً ولا تجميدًا ولا `E0`، ولا تقرؤه وحدةٌ في الشجرة. وكلُّ
ما يفعله أن يسوق بطاقةً واحدة على الحلقات بترتيبها، ويُسجّل أين وقفت ولماذا
بالاسم.

**وسَوقُ الحلقات مُخرَجٌ إلى `card_traversal`** ليُساق عليه أكثرُ من بطاقة
بالمنهج نفسه، فلا يُعمَّم حكمُ بطاقةٍ واحدة على غيرها.

**والوقوفُ مُشتَقٌّ من البطاقة لا مكتوبٌ هنا**: لكلّ حلقةٍ إعلانٌ تحتاجه من
مفرداتها المغلقة، ويُفحَص نصُّ البطاقة كلُّه عن أعضاء تلك المفردات؛ فإن لم
يَرِد منها عضوٌ فالحلقةُ واقفةٌ لغياب إعلانٍ مُسمًّى، لا لحكمٍ كُتِب في هذا
الملف. وهذا هو المعطى الذي تدور عليه المسألة: أيُّ حلقةٍ أوقفت التطبيق الفعليّ
الأوّل، ولأيّ إعلانٍ غائبٍ بعينه.

**والبلوغُ يُشتَقّ بالتتابع كما في `decision_chain`**: حلقةٌ قامت وقد سبقتها
واقفةٌ لا تُقرأ بالغة، وإلا ظهر التطبيقُ تامًّا وهو منقطعٌ عند موضعٍ سابق.

وموضعُ الناس:2 مقصودٌ لنظافته: رسمُ الكلمة فيه غيرُ مختلَفٍ فيه، وخلافُ
القراءتين (مالك/مَلِك) في الفاتحة:4 خلافُ قراءةٍ لا خلافُ مدلول، وقد استُبعِد
في البطاقة نفسها بالتصريح لا بالسكوت.
"""

import hashlib
import json
from pathlib import Path
from typing import Any, Final

import pytest
from card_traversal import (
    LinkAttempt,
    declared_members,
    first_stop,
    lexical_citation_genus,
    traverse,
)

from alghanem.arabic.comprehension_defect import (
    ComprehensionDefectCause,
    canonical_defect_classification,
)
from alghanem.arabic.lexical_transmission import (
    FLAT_TITLE_CITATION_IS_NOT_A_TRANSMISSION_CHAIN_NOTE,
    LexicalCitationStructure,
    card_lexical_citation_structure,
    card_transmission_standing,
)
from alghanem.arabic.manat_verification import assess_manat_from_card, manat_claim_scope
from alghanem.arabic.transmission_standing import (
    KnowledgeBasis,
    TransmissionStanding,
    UnconstructibilityGenus,
)
from alghanem.arabic.wad_naql import (
    DistributionalCorroboration,
    WadNaqlError,
    WadRecord,
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

_CARD_RELATIVE_PATH: Final = "examples/external_audit/malik_114_2.yaml"
_CARD_PATH: Final = Path(__file__).resolve().parents[2] / _CARD_RELATIVE_PATH


class CardFileProvider:
    """سلطةُ مصدرٍ تُوثِّق البطاقة ببايتاتها الفعلية، كما في `test_manat_verification`."""

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
        snapshot, RepositoryArtifactRef(snapshot.snapshot, _CARD_RELATIVE_PATH, digest)
    )
    return run.bridge_authenticated_fragment(run.observe_fragment(artifact, "البطاقة"))


def test_the_card_is_admitted_and_defers_with_named_residuals() -> None:
    """الحلقةُ ٥ تقوم على هذه البطاقة، و`DEFER` بفضلةٍ مُسمّاة نتيجةٌ مقبولة."""

    assessment = assess_manat_from_card(_card(), _binding())

    assert assessment.status is ApplicabilityAssessmentStatus.DEFER
    assert assessment.residuals
    assert all("مالك" in residual.description for residual in assessment.residuals)
    assert manat_claim_scope(_card()) == ClaimScopeRef("كلمة_في_آية", "الناس:2:مَلِك")


def test_the_competing_reading_is_classified_as_a_shared_wording() -> None:
    card = _card()
    (reading,) = card["القراءات_المنافسة"]

    assert reading["قراءة"] == "مالك"
    assert (
        canonical_defect_classification(reading["سبب_الإخلال_بالفهم"])
        is ComprehensionDefectCause.ISHTIRAK
    )


def test_the_neighbouring_qiraat_dispute_is_excluded_by_name_not_by_silence() -> None:
    """استبعادُ خلاف الفاتحة:4 مكتوبٌ في البطاقة، فلا يُقرأ سكوتًا عنه."""

    criterion = _card()["تعريف_التجربة"]["closure_criterion"]

    assert "الفاتحة:4" in criterion
    assert "خلافٌ في القراءة لا في المدلول" in criterion
    assert "لا سلطة لهذا المستودع على القراءات" in criterion


def test_the_first_application_stops_at_the_fourth_link_for_a_named_absence() -> None:
    """المعطى الذي تدور عليه المسألة: أيُّ حلقةٍ أوقفت التطبيق، ولأيّ غياب."""

    attempts = traverse(_card())
    stop = first_stop(attempts)

    assert stop is not None
    assert stop.label == "٤"
    assert stop.module_relative_path == "wad_naql.py"
    assert "TransmissionStanding" in stop.missing_declaration


def test_the_fourth_link_stops_by_a_derived_category_error_not_by_waiting() -> None:
    """الوقوفُ عند ٤ صار مُعلَّلًا ببنيةٍ مُشتَقّة: خطأٌ فئويٌّ دائم لا انتظار."""

    card = _card()

    assert (
        card_lexical_citation_structure(card)
        is LexicalCitationStructure.عنوان_واحد_مسطح
    )
    assert lexical_citation_genus(card) is (
        UnconstructibilityGenus.REFUSED_BY_STRUCTURAL_CATEGORY_MISMATCH
    )
    assert card_transmission_standing(card) is None
    assert "عنوان_واحد_مسطح" in first_stop(traverse(card)).missing_declaration  # type: ignore[union-attr]
    assert "FlatTitleCitationIsNotATransmissionChain" in (
        FLAT_TITLE_CITATION_IS_NOT_A_TRANSMISSION_CHAIN_NOTE
    )


def test_the_fourth_and_twelfth_links_stop_for_the_same_absent_declaration() -> None:
    """وقوفُ ٤ و١٢ غيابُ إعلانٍ واحد، لا غيابان: طريقُ ورود النقل."""

    by_label = {attempt.label: attempt for attempt in traverse(_card())}

    assert by_label["٤"].stood_up is False
    assert by_label["١٢"].stood_up is False
    assert "عينُ ما تفتقده الحلقةُ ٤" in by_label["١٢"].missing_declaration
    assert declared_members(_card(), TransmissionStanding) == ()
    assert declared_members(_card(), KnowledgeBasis) == ()


def test_links_that_stand_up_after_the_stop_are_not_read_as_reached() -> None:
    """٥ و٦ و٧ تقوم بذاتها على هذه البطاقة، ولا تُقرأ بالغةً بعد وقوف ٤."""

    attempts = traverse(_card())
    by_label = {attempt.label: attempt for attempt in attempts}
    stop = first_stop(attempts)

    stood = [attempt.label for attempt in attempts if attempt.stood_up]

    assert stood == ["٥", "٦", "٧"]
    assert stop is not None
    assert attempts.index(stop) < attempts.index(by_label["٥"])


def test_the_traversal_is_not_complete_so_the_application_test_is_unmet() -> None:
    """الاختبارُ الذي يطلبه القيدُ (ب) تطبيقٌ كاملٌ ناجز، وهذا لم يكتمل."""

    attempts = traverse(_card())

    assert not all(attempt.stood_up for attempt in attempts)
    assert [attempt.label for attempt in attempts if not attempt.stood_up] == [
        "٤",
        "٨",
        "٩",
        "١٠",
        "١١",
        "١٢",
        "١٣",
    ]
    assert all(
        attempt.missing_declaration.strip()
        for attempt in attempts
        if not attempt.stood_up
    )


def test_a_corroboration_without_a_prior_transmitted_record_is_refused() -> None:
    """المصادقةُ التوزيعية لا تقوم إلا على منقولٍ سابق، فهي هنا غيرُ ممكنة."""

    with pytest.raises(WadNaqlError):
        DistributionalCorroboration(
            wad=None,  # type: ignore[arg-type]
            probe_reference="مسبارٌ توزيعيّ",
            observed_regularity="انتظامٌ مرصود",
        )

    transmitted = WadRecord(
        lafz="مَلِك",
        madlul="ذو سلطان",
        naql_source="لسان العرب لابن منظور، مادة (م ل ك)",
        transmission=TransmissionStanding.AHAD,
    )
    corroboration = DistributionalCorroboration(
        wad=transmitted,
        probe_reference="مسبارٌ توزيعيّ",
        observed_regularity="انتظامٌ مرصود",
    )

    assert corroboration.transmission_after_corroboration is transmitted.transmission
    assert declared_members(_card(), TransmissionStanding) == ()


def test_the_traversal_issues_no_verdict_and_writes_nothing_into_the_tree() -> None:
    """الاختبارُ قراءةٌ لا سلطة: لا حقلَ حكمٍ في سجلّه، ولا وحدةَ جديدةً له."""

    forbidden = ("verdict", "birth", "freeze", "rank", "score", "count")

    assert all(
        marker not in field for field in LinkAttempt.__slots__ for marker in forbidden
    )
    assert not (
        Path(__file__).resolve().parents[2]
        / "src"
        / "alghanem"
        / "arabic"
        / "jiddiya_ifada.py"
    ).exists()
