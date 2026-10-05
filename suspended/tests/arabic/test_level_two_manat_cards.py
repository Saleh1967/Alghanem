"""بطاقةُ «سائمة الغنم» الحقيقية: يُسجَّل ما صدر كما صدر، لا ما أُريد أن يصدر.

**وهذه أوّلُ مادّةٍ حديثيةٍ في الشجرة**: `SignifiedAspect` قائمٌ بتقسيمه
المجرَّد (`نوع_الحكم` / `قيد_جانبي`) بلا مثالٍ منصوصٍ فيه، فـ«الغنم السائمة»
شاهدٌ جديدٌ يُسمّى بنصّه ولا يُقرأ إعادةَ استعمالٍ لمثالٍ مُثبَتٍ من قبل. ولمّا
كان جنسُ مصدرها حديثًا مُسنَدًا لا آية، وُضِعت بطاقاتُها في
`examples/level_two_manat/` ولم تُدَسّ بين البطاقات القرآنية، ولم يُضَف لأجلها
عضوٌ إلى `BayanKind` ولا غُيّر فيها حرف.

**ولا يُقرأ من هذا الملفّ حكمٌ فقهيّ**: لا في زكاة المعلوفة، ولا في مفهوم
المخالفة، ولا ترجيحٌ بين مذاهب. المقروءُ موضعُ الوقوف في الأداة وحده.

**وترتيبُ القراءة محفوظ**: الضابطُ السالب في
`test_level_two_manat_negative_control.py` يُثبت أن الرابط الموازي **يقوم فعلًا**
حين يقوم طريقُ نقل القيد، فأيُّ وقوفٍ هنا يُقرأ وقوفًا مُشتَقًّا لا عطلَ أداة.
"""

import hashlib
import json
from pathlib import Path
from typing import Any, Final

from card_traversal import declares

from alghanem.arabic.level_two_manat import (
    CARD_COMPOSITION_RELATION_KEY,
    HADITH_SOURCE_DOES_NOT_WIDEN_THE_BAYAN_VOCABULARY_NOTE,
    NEW_WITNESS_IS_NOT_AN_ESTABLISHED_EXAMPLE_NOTE,
    ClosedLevelOneCard,
    CompositionGenus,
    CompositionRole,
    LevelTwoCompositionInput,
    LevelTwoStopGenus,
    QaydSignification,
    TaqyeedManatGate,
    tadmin_taqyid_certificate_is_constructible,
)
from alghanem.arabic.lexical_transmission import LexicalCitationStructure
from alghanem.arabic.manat_verification import BayanKind, assess_manat_from_card
from alghanem.arabic.transmission_standing import (
    TransmissionStanding,
    UnconstructibilityGenus,
)
from alghanem.encyclopedia.self_observation import (
    RepositoryArtifactRef,
    RepositoryObservationAuthority,
    RepositorySnapshotRef,
)
from alghanem.kernel import (
    ApplicabilityAssessmentStatus,
    AuthenticatedObservationBinding,
)

_CARDS: Final = Path(__file__).resolve().parents[2] / "examples" / "level_two_manat"
_GHANAM: Final = _CARDS / "ghanam_bukhari.yaml"
_SAIMA: Final = _CARDS / "saima_bukhari.yaml"
_COMPOSITION: Final = _CARDS / "ghanam_saima_composition.yaml"


class _CardFileProvider:
    """سلطةُ مصدرٍ تُوثِّق البطاقة ببايتاتها الفعلية؛ لا تمنح دليلًا ولا سلطة."""

    provider_identity = "level-two-card-file-provider"
    implementation_identity = "level-two-card-file-provider-sha256"
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


def test_both_level_one_cards_close_with_pass_on_the_gate() -> None:
    """الطرفان يُغلقان `PASS` بنيويًّا: لا قراءةَ منافسةً غير متعينةٍ فيهما."""

    ghanam = _closed(_GHANAM, CompositionRole.موصوف)
    saima = _closed(_SAIMA, CompositionRole.صفة)

    assert ghanam.status is ApplicabilityAssessmentStatus.PASS
    assert saima.status is ApplicabilityAssessmentStatus.PASS
    assert ghanam.scope_reference != saima.scope_reference


def test_the_emptiness_of_the_competing_readings_is_declared_not_silent() -> None:
    """خلوّ القراءات المنافسة ادّعاءٌ مكتوبٌ في البطاقتين، لا سكوتٌ يُطوى."""

    for path in (_GHANAM, _SAIMA):
        card = _card(path)
        assert card["القراءات_المنافسة"] == []
        assert "ادّعاءٌ مُعلَنٌ صريح" in card["بيان_انتفاء_الإجمال"]


def test_the_hadith_source_changed_no_letter_of_the_bayan_vocabulary() -> None:
    """النصّ الحديثيُّ قولٌ منصوص، ومفردةُ جنس البيان ثنائيةٌ كما كانت."""

    kinds = {
        qarina["جنس_البيان"]
        for path in (_GHANAM, _SAIMA)
        for qarina in _card(path)["قرائن_المناط"]
    }

    assert kinds == {kind.value for kind in BayanKind}
    assert len(BayanKind) == 2
    assert "لا يُضاف" in HADITH_SOURCE_DOES_NOT_WIDEN_THE_BAYAN_VOCABULARY_NOTE


def test_the_composition_genus_is_derived_from_its_named_source() -> None:
    """جنسُ التركيب مُشتَقٌّ من نسبةٍ مُعلَنةٍ في شرحٍ مُسمًّى، لا مكتوبٍ ابتداءً."""

    composition = _composition_input()

    assert composition.genus is CompositionGenus.تقييدية
    assert "فتح الباري" in composition.named_relation_source
    assert _card(_COMPOSITION)[CARD_COMPOSITION_RELATION_KEY]["نوع_النسبة"] == "تقييدية"


def test_the_parallel_link_stops_on_the_real_card_by_a_named_mechanism_genus() -> None:
    """يُسجَّل الوقوفُ كما صدر: طريقُ نقل القيد لم يقم، وجنسُ الوقوف مُسمًّى."""

    attempt = TaqyeedManatGate.assess(_composition_input())

    assert attempt.stood_up is False
    assert attempt.stop_genus is LevelTwoStopGenus.وقوف_آلة_لانقطاع_نقل_القيد
    assert attempt.standing is None
    assert LexicalCitationStructure.عنوان_واحد_مسطح.value in attempt.missing_declaration
    assert (
        UnconstructibilityGenus.REFUSED_BY_STRUCTURAL_CATEGORY_MISMATCH.value
        in attempt.missing_declaration
    )
    assert "ولا يُستعاض عنه بطريق الموصوف" in attempt.missing_declaration


def test_the_stop_is_not_read_as_an_input_stop_nor_as_a_settled_specification() -> None:
    """الوقوفُ وقوفُ آلةٍ لا وقوفُ مدخل، ودلالةُ القيد تبقى غيرَ محسومةٍ لا طرديّة."""

    composition = _composition_input()
    attempt = TaqyeedManatGate.assess(composition)

    assert attempt.stop_genus is not LevelTwoStopGenus.وقوف_مدخل_قبل_اختبار_الآلة
    assert composition.qayd_signification is (QaydSignification.دلالة_القيد_غير_محسومة)
    assert composition.qayd_signification is not QaydSignification.وصف_طردي


def test_the_single_attribution_is_a_property_of_the_text_not_a_choice() -> None:
    """الإسنادُ واحدٌ لأنّ النصَّ سمّى قائلًا واحدًا، ولا يُصنَع ثانٍ لبلوغ العتبة."""

    card = _card(_COMPOSITION)
    attributions = card["طريق_النقل_المعجمي"]["الإسنادات"]

    assert len(attributions) == 1
    assert attributions[0]["السلطة"] in attributions[0]["الاقتباس_المنقول"]
    assert "ابن حجر العسقلاني" not in attributions[0]["الاقتباس_المنقول"]
    assert "ابن حجر العسقلاني" in card["طريق_النقل_المعجمي"]["المصدر"]
    assert "تُنشئ لفظًا لم يقع في النصّ" in card["بيان_الإسناد_الواحد"]
    assert "لا يُقرأ من هذه البطاقة حكمٌ" in card["لا_حكم_فقهي"]


def test_the_print_edition_locus_residual_is_raised_only_in_part() -> None:
    """[ص: 372] ترقيمُ إحالةٍ مُتعارَف، ولكنّ المجلَّد والنسخةَ الورقية لم يُتحقَّقا."""

    card = _card(_COMPOSITION)

    assert "PRINT_EDITION_LOCUS_NOT_VERIFIED" in card["بيان_موضع_الطبعة"]
    assert "جزئيًّا لا كلّيًّا" in card["بيان_موضع_الطبعة"]
    assert "[ص: 372]" in card["طريق_النقل_المعجمي"]["الإسنادات"][0]["الموضع"]


def test_the_written_prediction_is_kept_beside_the_outcome_that_refuted_it() -> None:
    """التوقّعُ مكتوبٌ بجوار ما وقع: (متعارضة) انتُظِرت فوقعت (غير محسومة)."""

    card = _card(_COMPOSITION)
    attempt = TaqyeedManatGate.assess(_composition_input())

    assert "MarkerVocabularyIsFrozenBeforeItsText" in card["بيان_التوقع_قبل_التشغيل"]
    assert "ولم تُوسَّع المفردةُ" in card["بيان_التوقع_قبل_التشغيل"]
    assert attempt.qayd_signification is QaydSignification.دلالة_القيد_غير_محسومة


def test_no_standing_and_no_gate_status_is_written_in_any_real_card() -> None:
    """لا درجةَ مكتوبةً ولا حالَ إغلاقٍ مكتوبة: الأمران مُشتَقّان لا مقروءان."""

    for path in (_GHANAM, _SAIMA, _COMPOSITION):
        card = _card(path)
        assert not any(declares(card, member.value) for member in TransmissionStanding)
        assert not any(
            declares(card, member.name) for member in ApplicabilityAssessmentStatus
        )


def test_this_reading_neither_closes_the_frozen_stage_nor_claims_a_fractal() -> None:
    """لا شهادةَ لمرحلة التضمين والتقييد، ولا حكمَ بتوازٍ فركتاليّ من هنا."""

    assert tadmin_taqyid_certificate_is_constructible() is False
    assert "شاهدٌ جديد" in NEW_WITNESS_IS_NOT_AN_ESTABLISHED_EXAMPLE_NOTE
