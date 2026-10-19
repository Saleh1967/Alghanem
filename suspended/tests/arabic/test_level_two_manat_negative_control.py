"""ضابطٌ سالب: أيقوم الرابطُ الموازي فعلًا حين يقوم طريقُ نقل القيد؟

**هذا ضابطُ أداةٍ لا بطاقةُ بحث**: بطاقاتُه مصنوعةٌ لهذا الغرض وحده
(`test_only`)، وموصوفُها وصفتُها وقيدُها مخترعةٌ بالتصريح، ولا تُقرأ منها شهادةٌ
على نصٍّ قائمٍ ولا على قيدٍ فقهيّ. ولذلك تبقى في ملفّ الاختبار ولا تُكتَب في
`examples/`: تلك البطاقاتُ يجري عليها التدقيقُ بالكامل، فوضعُ بطاقةٍ اصطناعيةٍ
بينها يمنحها شهادةً إنتاجيةً هي عينُ ما يمنعه غرضُها. وهو نصُّ التعليل نفسِه
الوارد في `test_fourth_link_negative_control.py`، مُطبَّقًا على المستوى الثاني.

**ومعيارُ النجاح واحد**: أن يقوم الرابطُ الموازي على هذا المدخل بعينه. فإن لم
يقم فأيُّ وقوفٍ على بطاقةٍ حقيقيةٍ لاحقًا يُقرأ بأثرٍ رجعيّ «عطلَ أداة» لا
«وقوفًا مُشتَقًّا صحيحًا». ولذلك يسبق هذا الضابطُ كلَّ قراءةٍ لبطاقةٍ حقيقية.

**والوقوفُ مُشتَقٌّ أيضًا لا مُثبَّتٌ في الأداة**: حذفُ إسنادٍ واحدٍ يُوقف
الرابطَ نفسَه بجنس آلةٍ مُسمًّى، وحذفُ التخصيص المنقول يُوقفه بجنسٍ آخر،
وإسقاطُ نسبة التركيب يُوقفه **وقوفَ مدخلٍ** لا وقوفَ آلة.
"""

import hashlib
import json
from pathlib import Path
from typing import Any, Final

import pytest

from alghanem.arabic.level_two_manat import (
    CARD_COMPOSITION_RELATION_KEY,
    INPUT_STOP_IS_NOT_A_MECHANISM_FAILURE_NOTE,
    LEVEL_ONE_CLOSURE_IS_READ_NOT_REPEATED_NOTE,
    SPECIFICATION_IS_A_KIND_NOT_A_DEGREE_NOTE,
    TRANSMITTED_CONFLICT_IS_A_CASE_NOT_A_CRASH_NOTE,
    ClosedLevelOneCard,
    CompositionGenus,
    CompositionRole,
    LevelTwoCompositionInput,
    LevelTwoManatError,
    LevelTwoStopGenus,
    QaydSignification,
    TaqyeedManatGate,
    tadmin_taqyid_certificate_is_constructible,
)
from alghanem.arabic.lexical_transmission import (
    LEXICAL_CHAIN_MINIMUM_ATTRIBUTIONS,
    LexicalCitationStructure,
)
from alghanem.arabic.manat_verification import assess_manat_from_card
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

_TEST_ONLY_MARKER: Final = "test_only"


class _CardFileProvider:
    """سلطةُ مصدرٍ تُوثِّق بطاقةً ببايتاتها الفعلية، بلا دليلٍ ولا سلطةٍ تمنحها."""

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


def _binding(path: Path) -> AuthenticatedObservationBinding:
    provider = _CardFileProvider(path)
    run = RepositoryObservationAuthority(provider).open_run()
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    snapshot = run.observe_snapshot(RepositorySnapshotRef("Alghanem", digest, digest))
    artifact = run.observe_artifact(
        snapshot, RepositoryArtifactRef(snapshot.snapshot, path.name, digest)
    )
    return run.bridge_authenticated_fragment(run.observe_fragment(artifact, "البطاقة"))


def _level_one_card(word: str, position: str, identifier: str) -> dict[str, Any]:
    """بطاقةُ مستوًى أوّلٍ اصطناعية، بلا قراءةٍ منافسةٍ غير متعينة."""

    return {
        "النص": f"نصٌّ مخترعٌ لهذا الضابط فيه ({word})",
        "الموضع": position,
        "الكلمة_المدروسة": word,
        "معرف_السؤال": identifier,
        "الغرض": (
            f"{_TEST_ONLY_MARKER}: ضبطُ الأداة وحدها، فلا شهادةَ إنتاجيةً في هذه "
            "البطاقة ولا حكمَ منها على لفظٍ قائم"
        ),
        "النموذج_المختبر": f"مدلولٌ_مخترعٌ_لـ{word}",
        "قرائن_المناط": [
            {
                "معرف": f"qar-qawl-{identifier}",
                "القرينة": (f"نصٌّ مخترعٌ لهذا الضابط يُبيِّن مدلول ({word}) في موضعه"),
                "جنس_البيان": "بيان_بالقول",
                "المصدر_المُسمّى": "مصدرٌ قوليٌّ مخترعٌ لهذا الضابط",
            }
        ],
        "القراءات_المنافسة": [],
        "تعريف_التجربة": {"domain": "level-two-control"},
    }


def _composition_card() -> dict[str, Any]:
    """بطاقةُ تركيبٍ اصطناعية: نسبةٌ تقييديةٌ مُسمّاة، وطريقُ نقلٍ للقيد بعينه."""

    return {
        "معرف_السؤال": f"q-{_TEST_ONLY_MARKER}-level-two-control",
        "الكلمة_المدروسة": "تركيبٌ مخترعٌ لهذا الضابط",
        "الغرض": (
            f"{_TEST_ONLY_MARKER}: ضبطُ الرابط الموازي وحده، فلا حكمَ من هذه "
            "البطاقة على قيدٍ قائمٍ في نصّ"
        ),
        CARD_COMPOSITION_RELATION_KEY: {
            "نوع_النسبة": "تقييدية",
            "المصدر_المُسمّى": "شارحٌ مخترعٌ لهذا الضابط، موضعٌ مخترع",
        },
        "طريق_النقل_المعجمي": {
            "المصدر": "مُجمِّعٌ مخترعٌ لهذا الضابط",
            "المادة": "قيدٌ مخترعٌ لهذا الضابط",
            "الإسنادات": [
                {
                    "السلطة": "سلطةٌ أولى مخترعة",
                    "الاقتباس_المنقول": (
                        "قالت سلطةٌ أولى مخترعة: هذا القيدُ أخرج ما عداه من الحكم"
                    ),
                    "الموضع": "موضعٌ مخترعٌ أوّل",
                    "جنس_المحتوى": "نقل_قول_منسوب",
                },
                {
                    "السلطة": "سلطةٌ ثانية مخترعة",
                    "الاقتباس_المنقول": (
                        "وقالت سلطةٌ ثانية مخترعة: إخراج ما عدا هذا القيد مرادٌ به"
                    ),
                    "الموضع": "موضعٌ مخترعٌ ثانٍ",
                    "جنس_المحتوى": "نقل_قول_منسوب",
                },
            ],
        },
    }


def _closed(
    card: dict[str, Any], role: CompositionRole, tmp_path: Path, name: str
) -> ClosedLevelOneCard:
    """يُغلِق بطاقة المستوى الأول ببوّابة G0.EA.1 نفسها، لا بإعلانٍ مكتوب."""

    path = tmp_path / name
    path.write_text(json.dumps(card, ensure_ascii=False), encoding="utf-8")
    return ClosedLevelOneCard(
        role=role, card=card, assessment=assess_manat_from_card(card, _binding(path))
    )


def _input(tmp_path: Path, composition: dict[str, Any]) -> LevelTwoCompositionInput:
    described = _closed(
        _level_one_card("موصوفٌ مخترع", "موضعٌ مخترعٌ أوّل", "q-control-mawsuf"),
        CompositionRole.موصوف,
        tmp_path,
        "mawsuf.json",
    )
    descriptor = _closed(
        _level_one_card("صفةٌ مخترعة", "موضعٌ مخترعٌ ثانٍ", "q-control-sifa"),
        CompositionRole.صفة,
        tmp_path,
        "sifa.json",
    )
    return LevelTwoCompositionInput(
        described=described,
        descriptor=descriptor,
        composition_card=composition,
        declared_genus=CompositionGenus.تقييدية,
    )


def test_the_cards_declare_themselves_controls_without_production_witness() -> None:
    """غرضُ البطاقات مكتوبٌ فيها، فلا تُقرأ شهادةً على نصٍّ قائم."""

    composition = _composition_card()

    assert _TEST_ONLY_MARKER in composition["معرف_السؤال"]
    assert _TEST_ONLY_MARKER in composition["الغرض"]
    assert "الأدلة" not in composition
    assert "تعريف_التجربة" not in composition


def test_both_level_one_cards_close_on_the_gate_before_any_composition(
    tmp_path: Path,
) -> None:
    """المدخلُ حالُ إغلاقٍ صادرةٌ عن البوّابة، لا إعلانٌ مكتوبٌ في البطاقة."""

    composition = _input(tmp_path, _composition_card())

    assert composition.described.status is ApplicabilityAssessmentStatus.PASS
    assert composition.descriptor.status is ApplicabilityAssessmentStatus.PASS
    assert (
        composition.described.scope_reference != composition.descriptor.scope_reference
    )


def test_the_tool_actually_stands_the_parallel_link_on_this_input(
    tmp_path: Path,
) -> None:
    """معيارُ النجاح الوحيد: الرابطُ الموازي يقوم فعلًا على هذا المدخل."""

    attempt = TaqyeedManatGate.assess(_input(tmp_path, _composition_card()))

    assert attempt.stood_up is True
    assert attempt.stop_genus is LevelTwoStopGenus.الرابط_قائم
    assert attempt.missing_declaration == ""
    assert attempt.standing is TransmissionStanding.AHAD
    assert attempt.qayd_signification is QaydSignification.قيد_مخصص


def test_the_standing_is_derived_from_the_qayd_path_and_never_written(
    tmp_path: Path,
) -> None:
    """الدرجةُ مُشتَقّةٌ من طريق نقل القيد بعينه، ولم تُكتَب في البطاقة نصًّا."""

    composition = _composition_card()
    attempt = TaqyeedManatGate.assess(_input(tmp_path, composition))

    assert attempt.standing is not TransmissionStanding.MUTAWATIR
    assert not any(
        member.value in str(composition) for member in TransmissionStanding
    ), "الدرجةُ لم تُكتَب في البطاقة، فقيامُ الرابط اشتقاقٌ لا قراءة"


def test_removing_one_attribution_stops_the_same_link_as_a_mechanism_stop(
    tmp_path: Path,
) -> None:
    """حذفُ إسنادٍ واحد يُوقف الرابطَ نفسَه بجنس آلةٍ مُسمًّى لا بصمت."""

    composition = _composition_card()
    composition["طريق_النقل_المعجمي"]["الإسنادات"] = composition["طريق_النقل_المعجمي"][
        "الإسنادات"
    ][:1]
    attempt = TaqyeedManatGate.assess(_input(tmp_path, composition))

    assert attempt.stood_up is False
    assert attempt.stop_genus is LevelTwoStopGenus.وقوف_آلة_لانقطاع_نقل_القيد
    assert attempt.standing is None
    assert LexicalCitationStructure.عنوان_واحد_مسطح.value in attempt.missing_declaration
    assert (
        UnconstructibilityGenus.REFUSED_BY_STRUCTURAL_CATEGORY_MISMATCH.value
        in attempt.missing_declaration
    )


def test_removing_the_transmitted_specification_stops_the_link_by_its_own_genus(
    tmp_path: Path,
) -> None:
    """طريقٌ قائمٌ بلا تخصيصٍ منقول: وقوفٌ بجنسٍ آخر، ولا يُقرأ وصفًا طرديًّا."""

    composition = _composition_card()
    for index, attribution in enumerate(
        composition["طريق_النقل_المعجمي"]["الإسنادات"], start=1
    ):
        attribution["الاقتباس_المنقول"] = (
            f"{attribution['السلطة']}: وصفٌ مخترعٌ لهذا الضابط بلا نقلٍ في "
            f"دلالته، الموضع {index}"
        )
    attempt = TaqyeedManatGate.assess(_input(tmp_path, composition))

    assert attempt.stood_up is False
    assert attempt.stop_genus is LevelTwoStopGenus.وقوف_آلة_لغياب_تخصيص_منقول
    assert attempt.standing is TransmissionStanding.AHAD
    assert attempt.qayd_signification is QaydSignification.دلالة_القيد_غير_محسومة
    assert SPECIFICATION_IS_A_KIND_NOT_A_DEGREE_NOTE in attempt.missing_declaration


def test_an_unsettled_composition_genus_is_an_input_stop_not_a_mechanism_failure(
    tmp_path: Path,
) -> None:
    """جنسٌ غيرُ محسومٍ يُوقف الرابطَ قبل أن تُختبَر الآلةُ أصلًا."""

    composition = _composition_card()
    del composition[CARD_COMPOSITION_RELATION_KEY]
    described = _closed(
        _level_one_card("موصوفٌ مخترع", "موضعٌ مخترعٌ أوّل", "q-control-mawsuf"),
        CompositionRole.موصوف,
        tmp_path,
        "mawsuf.json",
    )
    descriptor = _closed(
        _level_one_card("صفةٌ مخترعة", "موضعٌ مخترعٌ ثانٍ", "q-control-sifa"),
        CompositionRole.صفة,
        tmp_path,
        "sifa.json",
    )
    attempt = TaqyeedManatGate.assess(
        LevelTwoCompositionInput(
            described=described,
            descriptor=descriptor,
            composition_card=composition,
            declared_genus=CompositionGenus.غير_محسوم,
        )
    )

    assert attempt.stood_up is False
    assert attempt.stop_genus is LevelTwoStopGenus.وقوف_مدخل_قبل_اختبار_الآلة
    assert INPUT_STOP_IS_NOT_A_MECHANISM_FAILURE_NOTE in attempt.missing_declaration


def test_a_written_genus_that_contradicts_the_derived_one_is_refused(
    tmp_path: Path,
) -> None:
    """الجنسُ المكتوبُ المخالفُ للمُشتَقّ يُرفَض عند الإنشاء ولا يُقرَّر."""

    described = _closed(
        _level_one_card("موصوفٌ مخترع", "موضعٌ مخترعٌ أوّل", "q-control-mawsuf"),
        CompositionRole.موصوف,
        tmp_path,
        "mawsuf.json",
    )
    descriptor = _closed(
        _level_one_card("صفةٌ مخترعة", "موضعٌ مخترعٌ ثانٍ", "q-control-sifa"),
        CompositionRole.صفة,
        tmp_path,
        "sifa.json",
    )

    with pytest.raises(LevelTwoManatError, match="يخالف المُشتَقّ"):
        LevelTwoCompositionInput(
            described=described,
            descriptor=descriptor,
            composition_card=_composition_card(),
            declared_genus=CompositionGenus.إضافية,
        )


def test_an_unclosed_level_one_card_does_not_enter_the_second_level() -> None:
    """بطاقةٌ لم تُغلَق لا تدخل المستوى الثاني، ولا يُعاد تحليلُ نصّها هنا."""

    with pytest.raises(LevelTwoManatError, match="لم تُغلَق"):
        ClosedLevelOneCard(
            role=CompositionRole.موصوف,
            card=_level_one_card("موصوفٌ مخترع", "موضعٌ مخترعٌ أوّل", "q-control-mawsuf"),
            assessment=None,
        )

    assert "لا يُعاد تحليلُ نصّها الخام" in LEVEL_ONE_CLOSURE_IS_READ_NOT_REPEATED_NOTE


def test_a_borrowed_closure_from_another_scope_is_refused(tmp_path: Path) -> None:
    """إغلاقُ بطاقةٍ لا يُستعار لأخرى، فالنطاقُ يُقابَل ولا يُتجاوَز."""

    other = _level_one_card("موصوفٌ مخترع", "موضعٌ مخترعٌ أوّل", "q-control-mawsuf")
    path = tmp_path / "other.json"
    path.write_text(json.dumps(other, ensure_ascii=False), encoding="utf-8")
    assessment = assess_manat_from_card(other, _binding(path))

    with pytest.raises(LevelTwoManatError, match="نطاقٍ غير نطاق"):
        ClosedLevelOneCard(
            role=CompositionRole.صفة,
            card=_level_one_card("صفةٌ مخترعة", "موضعٌ مخترعٌ ثانٍ", "q-control-sifa"),
            assessment=assessment,
        )


def test_the_frozen_tadmin_taqyid_stage_is_left_exactly_as_it_was() -> None:
    """قيامُ الرابط لا يُقدِّم نصَّ المرحلة المُجمَّدة ولا يُصيّر شهادتَها ممكنة."""

    assert tadmin_taqyid_certificate_is_constructible() is False


def test_one_genuinely_transmitted_attribution_stops_by_the_arity_threshold_alone(
    tmp_path: Path,
) -> None:
    """إسنادٌ واحدٌ يَنقُل التخصيصَ صراحةً يقف بجنس من لم يَنقُل شيئًا.

    وهذا هو الضابطُ الفارق: لو كان الوقوفُ الحاصلُ على البطاقة الحقيقية شهادةً
    على بنيةٍ لغويةٍ لاختلف جنسُه هنا، إذ نُقِل التخصيصُ بنصّه؛ فلمّا اتّحد
    الجنسان ثبت أنّ الوقوفَ أثرُ عتبة العدد لا نتيجةَ فحصٍ بنيويّ.
    """

    composition = _composition_card()
    composition["طريق_النقل_المعجمي"]["الإسنادات"] = composition["طريق_النقل_المعجمي"][
        "الإسنادات"
    ][:1]
    single = TaqyeedManatGate.assess(_input(tmp_path, composition))

    empty = _composition_card()
    empty["طريق_النقل_المعجمي"]["الإسنادات"] = []
    none_at_all = TaqyeedManatGate.assess(_input(tmp_path, empty))

    assert LEXICAL_CHAIN_MINIMUM_ATTRIBUTIONS == 2
    assert (
        "أخرج" in composition["طريق_النقل_المعجمي"]["الإسنادات"][0]["الاقتباس_المنقول"]
    )
    assert single.stood_up is False
    assert single.stop_genus is none_at_all.stop_genus
    assert single.stop_genus is LevelTwoStopGenus.وقوف_آلة_لانقطاع_نقل_القيد
    assert single.standing is none_at_all.standing is None


def test_a_transmitted_conflict_is_read_as_a_named_stop_not_a_raised_error(
    tmp_path: Path,
) -> None:
    """طريقٌ يَنقُل التخصيصَ والطرديّة معًا حالٌ تُقرأ، ولا تُسقِط الأداة."""

    composition = _composition_card()
    composition["طريق_النقل_المعجمي"]["الإسنادات"][1]["الاقتباس_المنقول"] = (
        "وقالت سلطةٌ ثانية مخترعة: هذا وصف طردي لا مفهوم له"
    )
    attempt = TaqyeedManatGate.assess(_input(tmp_path, composition))

    assert attempt.stood_up is False
    assert attempt.stop_genus is LevelTwoStopGenus.وقوف_آلة_لتعارض_منقول_في_دلالة_القيد
    assert attempt.qayd_signification is QaydSignification.دلالة_القيد_متعارضة
    assert attempt.standing is TransmissionStanding.AHAD
    assert (
        TRANSMITTED_CONFLICT_IS_A_CASE_NOT_A_CRASH_NOTE in attempt.missing_declaration
    )
