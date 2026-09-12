"""تطبيقٌ كاملٌ واحد على بطاقة (مَلِك) في الناس:2، مُشغَّلًا على حلقات ٤–١٣.

هذا **اختبارُ تشغيل، لا وحدةُ قياسٍ جديدة**: لا يُنشئ سلطةً ولا مفردةً ولا
دفترًا، ولا يُصدر ولادةً ولا تجميدًا ولا `E0`، ولا تقرؤه وحدةٌ في الشجرة. وكلُّ
ما يفعله أن يسوق بطاقةً واحدة على الحلقات بترتيبها، ويُسجّل أين وقفت ولماذا
بالاسم.

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
import re
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Final

import pytest

from alghanem.arabic.comprehension_defect import (
    ComprehensionDefectCause,
    canonical_defect_classification,
)
from alghanem.arabic.maluma_mafhum import SanadOrigin, SemanticTarget
from alghanem.arabic.manat_verification import (
    FIL_MODEL_ID,
    QAWL_MODEL_ID,
    assess_manat_from_card,
    derive_bayan_models,
    manat_claim_scope,
    read_manat_qarain,
)
from alghanem.arabic.mantuq_mafhum_ifada import DalalaChannel, MafhumKind
from alghanem.arabic.qiyas_rabt_registration import (
    IllaApplication,
    frozen_asl_references,
)
from alghanem.arabic.riwaya_diraya_registration import DirayaBranch, RiwayaStanding
from alghanem.arabic.text_key import comparison_key
from alghanem.arabic.transmission_standing import (
    KnowledgeBasis,
    RepetitionPattern,
    SourceIndependence,
    TransmissionStanding,
)
from alghanem.arabic.umum_khusus import DalilScope, RuleGenus
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


def _texts(payload: Any) -> tuple[str, ...]:
    """كلُّ نصوص البطاقة، مفاتيحَ وقيَمًا، مسرودةً بلا تأويل."""

    if isinstance(payload, str):
        return (payload,)
    if isinstance(payload, dict):
        collected: list[str] = []
        for key, value in payload.items():
            collected.extend(_texts(key))
            collected.extend(_texts(value))
        return tuple(collected)
    if isinstance(payload, list):
        collected = []
        for item in payload:
            collected.extend(_texts(item))
        return tuple(collected)
    return ()


def _declares(card: dict[str, Any], term: str) -> bool:
    """أيرِد المصطلحُ في البطاقة كلمةً قائمةً بنفسها، لا جزءًا من كلمةٍ أخرى؟"""

    boundary = r"[\w\u0621-\u064a]"
    pattern = re.compile(
        f"(?<!{boundary})" + re.escape(comparison_key(term)) + f"(?!{boundary})"
    )
    return any(pattern.search(comparison_key(text)) for text in _texts(card))


def _declared_members(card: dict[str, Any], vocabulary: type[Enum]) -> tuple[Enum, ...]:
    """أعضاءُ المفردة المغلقة التي تُصرّح بها البطاقة نصًّا، وقد تكون فارغة."""

    return tuple(member for member in vocabulary if _declares(card, str(member.value)))


@dataclass(frozen=True, slots=True)
class LinkAttempt:
    """محاولةُ حلقةٍ واحدة على هذه البطاقة: أقامت، أم وقفت ولأيّ إعلانٍ غائب."""

    label: str
    module_relative_path: str
    stood_up: bool
    missing_declaration: str


def _link_four(card: dict[str, Any]) -> LinkAttempt:
    """٤ الوضع بالنقل: يلزمه طريقُ معرفةٍ من `TransmissionStanding` وحدها."""

    declared = _declared_members(card, TransmissionStanding)
    return LinkAttempt(
        label="٤",
        module_relative_path="wad_naql.py",
        stood_up=bool(declared),
        missing_declaration=(
            ""
            if declared
            else "درجةُ النقل من `TransmissionStanding` (متواتر/آحاد/فرض): "
            "بطاقةُ المناط تُعلن قرائنَ موضعٍ ومصادرَها المُسمّاة، ولا تُعلن "
            "طريقَ معرفة الوضع؛ فـ`WadRecord` غيرُ قابلٍ للتسجيل منها، "
            "و`DistributionalCorroboration` لا تقوم إلا على منقولٍ سابق."
        ),
    )


def _link_five(card: dict[str, Any]) -> LinkAttempt:
    """٥ تحقيقُ المناط: البطاقةُ مصوغةٌ لهذه الحلقة بعينها."""

    read_manat_qarain(card)
    return LinkAttempt(
        label="٥",
        module_relative_path="manat_verification.py",
        stood_up=True,
        missing_declaration="",
    )


def _link_six(card: dict[str, Any]) -> LinkAttempt:
    """٦ ما يخلّ بالفهم: البطاقةُ تُصنّف كلَّ قراءةٍ منافسةٍ بسببٍ من المفردة."""

    declared = tuple(
        canonical_defect_classification(reading["سبب_الإخلال_بالفهم"])
        for reading in card["القراءات_المنافسة"]
        if "سبب_الإخلال_بالفهم" in reading
    )
    return LinkAttempt(
        label="٦",
        module_relative_path="comprehension_defect.py",
        stood_up=len(declared) == len(card["القراءات_المنافسة"]),
        missing_declaration=(
            ""
            if len(declared) == len(card["القراءات_المنافسة"])
            else "سبب_الإخلال_بالفهم لكلّ قراءةٍ منافسة"
        ),
    )


def _link_seven(card: dict[str, Any]) -> LinkAttempt:
    """٧ البيانُ بالقول مقدَّمًا على البيان بالفعل: الترتيبُ مُشتَقٌّ من القرائن."""

    derived = derive_bayan_models(read_manat_qarain(card))
    models = {model.model_id: model for model in derived}
    ordered = models[QAWL_MODEL_ID].weaker_model_ids == () and models[
        FIL_MODEL_ID
    ].weaker_model_ids == (QAWL_MODEL_ID,)
    return LinkAttempt(
        label="٧",
        module_relative_path="manat_verification.py",
        stood_up=ordered,
        missing_declaration="" if ordered else "قرينتا قولٍ وفعلٍ معًا في البطاقة",
    )


def _link_eight(card: dict[str, Any]) -> LinkAttempt:
    """٨ المنطوقُ والمفهوم: يلزمه قناةُ دلالةٍ وجنسُ مفهومٍ مُعلَنان."""

    declared = _declared_members(card, DalalaChannel) and _declared_members(
        card, MafhumKind
    )
    return LinkAttempt(
        label="٨",
        module_relative_path="mantuq_mafhum_ifada.py",
        stood_up=bool(declared),
        missing_declaration=(
            ""
            if declared
            else "قناةُ الدلالة (`DalalaChannel`) وجنسُ المفهوم (`MafhumKind`): "
            "البطاقةُ تُعلن مدلولَ اللفظ ولا تُعلن دلالةً ثانيةً يُحمَل عليها."
        ),
    )


def _link_nine(card: dict[str, Any]) -> LinkAttempt:
    """٩ القياسُ بعلّةٍ منطبقة: يلزمه أصلٌ مُجمَّدٌ مُسمًّى وعلّةٌ مُعلَنة."""

    declared = any(
        _declares(card, reference) for reference in frozen_asl_references()
    ) and bool(_declared_members(card, IllaApplication))
    return LinkAttempt(
        label="٩",
        module_relative_path="qiyas_rabt_registration.py",
        stood_up=declared,
        missing_declaration=(
            ""
            if declared
            else "أصلٌ من `frozen_asl_references()` وانطباقُ علّةٍ من "
            "`IllaApplication`: البطاقةُ موضعٌ واحد بلا فرعٍ مقيسٍ عليه."
        ),
    )


def _link_ten(card: dict[str, Any]) -> LinkAttempt:
    """١٠ العمومُ والخصوص: يلزمه دليلان بنطاقَيهما، أو جنسُ قاعدةٍ للتفريع."""

    declared = bool(_declared_members(card, DalilScope)) or bool(
        _declared_members(card, RuleGenus)
    )
    return LinkAttempt(
        label="١٠",
        module_relative_path="umum_khusus.py",
        stood_up=declared,
        missing_declaration=(
            ""
            if declared
            else "نطاقُ الدليل (`DalilScope`) أو جنسُ القاعدة (`RuleGenus`): "
            "لا عامَّ في البطاقة ولا مخصِّصَ له ولا موضعَ تعارضٍ مُسمًّى."
        ),
    )


def _link_eleven(card: dict[str, Any]) -> LinkAttempt:
    """١١ الروايةُ والدراية: يلزمها قناةُ نقلٍ مُعرَّفةٌ ببصمتها، أو فرعُ درايةٍ."""

    declared = bool(_declared_members(card, RiwayaStanding)) or bool(
        _declared_members(card, DirayaBranch)
    )
    return LinkAttempt(
        label="١١",
        module_relative_path="riwaya_diraya_registration.py",
        stood_up=declared,
        missing_declaration=(
            ""
            if declared
            else "حالُ الرواية (`RiwayaStanding`) أو فرعُ الدراية "
            "(`DirayaBranch`): البطاقةُ نصٌّ مقروء لا تشغيلُ أداةٍ بهويةٍ وبصمة."
        ),
    )


def _link_twelve(card: dict[str, Any]) -> LinkAttempt:
    """١٢ درجةُ اليقين: تُشتَقّ من أساسٍ واستقلالٍ وتكرارٍ مُعلَنة."""

    declared = (
        bool(_declared_members(card, KnowledgeBasis))
        and bool(_declared_members(card, SourceIndependence))
        and bool(_declared_members(card, RepetitionPattern))
    )
    return LinkAttempt(
        label="١٢",
        module_relative_path="transmission_standing.py",
        stood_up=declared,
        missing_declaration=(
            ""
            if declared
            else "أساسُ المعرفة واستقلالُ المصادر ونمطُ التكرار، وهي عينُ ما "
            "تفتقده الحلقةُ ٤: البطاقةُ تُسمّي مصادرَها ولا تصف طريقَ ورودها."
        ),
    )


def _link_thirteen(card: dict[str, Any]) -> LinkAttempt:
    """١٣ المعلومةُ والمفهوم: يلزمها هدفٌ دلاليٌّ وسندٌ ينتهي إلى حسٍّ مباشر."""

    declared = bool(_declared_members(card, SemanticTarget)) and bool(
        _declared_members(card, SanadOrigin)
    )
    return LinkAttempt(
        label="١٣",
        module_relative_path="maluma_mafhum.py",
        stood_up=declared,
        missing_declaration=(
            ""
            if declared
            else "هدفُ الفهم (`SemanticTarget`) وأصلُ السند (`SanadOrigin`): "
            "لا سلسلةَ تسليمٍ في البطاقة تنتهي إلى حسٍّ مباشر."
        ),
    )


def _traverse(card: dict[str, Any]) -> tuple[LinkAttempt, ...]:
    """سَوقُ البطاقة على الحلقات ٤–١٣ بترتيبها، بلا تقديمٍ ولا تأخير."""

    return (
        _link_four(card),
        _link_five(card),
        _link_six(card),
        _link_seven(card),
        _link_eight(card),
        _link_nine(card),
        _link_ten(card),
        _link_eleven(card),
        _link_twelve(card),
        _link_thirteen(card),
    )


def _first_stop(attempts: tuple[LinkAttempt, ...]) -> LinkAttempt | None:
    """أوّلُ حلقةٍ وقفت؛ وما بعدها لا يُقرأ بالغًا وإن قام بذاته."""

    for attempt in attempts:
        if not attempt.stood_up:
            return attempt
    return None


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

    attempts = _traverse(_card())
    stop = _first_stop(attempts)

    assert stop is not None
    assert stop.label == "٤"
    assert stop.module_relative_path == "wad_naql.py"
    assert "TransmissionStanding" in stop.missing_declaration


def test_the_fourth_and_twelfth_links_stop_for_the_same_absent_declaration() -> None:
    """وقوفُ ٤ و١٢ غيابُ إعلانٍ واحد، لا غيابان: طريقُ ورود النقل."""

    by_label = {attempt.label: attempt for attempt in _traverse(_card())}

    assert by_label["٤"].stood_up is False
    assert by_label["١٢"].stood_up is False
    assert "عينُ ما تفتقده الحلقةُ ٤" in by_label["١٢"].missing_declaration
    assert _declared_members(_card(), TransmissionStanding) == ()
    assert _declared_members(_card(), KnowledgeBasis) == ()


def test_links_that_stand_up_after_the_stop_are_not_read_as_reached() -> None:
    """٥ و٦ و٧ تقوم بذاتها على هذه البطاقة، ولا تُقرأ بالغةً بعد وقوف ٤."""

    attempts = _traverse(_card())
    by_label = {attempt.label: attempt for attempt in attempts}
    stop = _first_stop(attempts)

    stood = [attempt.label for attempt in attempts if attempt.stood_up]

    assert stood == ["٥", "٦", "٧"]
    assert stop is not None
    assert attempts.index(stop) < attempts.index(by_label["٥"])


def test_the_traversal_is_not_complete_so_the_application_test_is_unmet() -> None:
    """الاختبارُ الذي يطلبه القيدُ (ب) تطبيقٌ كاملٌ ناجز، وهذا لم يكتمل."""

    attempts = _traverse(_card())

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
    assert _declared_members(_card(), TransmissionStanding) == ()


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
