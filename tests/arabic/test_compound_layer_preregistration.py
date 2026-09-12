"""اختبارات التسجيل المسبق لطبقة المركّب.

تحرس هذه الاختبارات ما يحرسه نظائرها في الشهادات الصورية الثلاث: المفردات
مغلقة، والتغطية تسبق الحكم، والتبعية مُشتَقّة لا مكتوبة، ولا سلطةَ نواةٍ
تُقرَأ ولا تتغيّر نتيجة التدقيق الخارجي.
"""

from __future__ import annotations

import json
from dataclasses import fields, replace
from pathlib import Path

import pytest

from alghanem.arabic.compound_layer_preregistration import (
    COMPOUND_AUTHORITY_NOTE,
    COMPOUND_LAYER_PREREGISTRATION,
    COMPOUND_REQUESTED_NOT_ATTESTED_NOTE,
    COMPOUND_SCOPE_NOTE,
    COMPOUND_SOURCE_REQUIREMENT,
    COMPOUND_SUCCESS_TITLE_IS_WITHHELD,
    COMPOUND_UNDECIDED_TEXT,
    AttestationStanding,
    CompoundLayerPreregistration,
    CompoundLayerPreregistrationError,
    CompoundStage,
    CompoundStageRegistration,
    NamedRefusal,
    derived_prerequisites,
)
from alghanem.arabic.external_audit import audit_card

_EXAMPLES = Path(__file__).resolve().parents[2] / "examples" / "external_audit"

_CARDS = (
    "hadhan_20_63.yaml",
    "imran_3_33.yaml",
    "maa_2_197.yaml",
    "man_2_255.yaml",
)


def _registration(stage: CompoundStage) -> CompoundStageRegistration:
    return COMPOUND_LAYER_PREREGISTRATION.registration_for(stage)


def test_the_stage_vocabulary_is_exactly_the_four_declared_values() -> None:
    assert tuple(stage.value for stage in CompoundStage) == (
        "العامل_والمعمول",
        "النسب_الإسنادية",
        "التضمين_والتقييد",
        "قيم_النسبة",
    )


def test_the_attestation_vocabulary_is_exactly_the_three_declared_values() -> None:
    assert tuple(standing.value for standing in AttestationStanding) == (
        "مصدر_غير_مُقدَّم",
        "مصدر_مُقدَّم_غير_متحقَّق",
        "شاهد_لكل_فرع",
    )


def test_every_stage_is_registered_exactly_once_in_dependency_order() -> None:
    assert COMPOUND_LAYER_PREREGISTRATION.stages == tuple(CompoundStage)
    assert len(COMPOUND_LAYER_PREREGISTRATION.registrations) == len(CompoundStage)


def test_each_stage_declares_the_requested_outcome_vocabulary() -> None:
    assert _registration(CompoundStage.AMIL_MAMUL).declared_outcomes == (
        "عامل",
        "معمول",
        COMPOUND_UNDECIDED_TEXT,
    )
    assert _registration(CompoundStage.NISBA_ISNADIYYA).declared_outcomes == (
        "مركّب_إسنادي",
        "مركّب_غير_إسنادي",
        COMPOUND_UNDECIDED_TEXT,
    )
    assert _registration(CompoundStage.TADMIN_TAQYID).declared_outcomes == (
        "تضمين",
        "تقييد",
        COMPOUND_UNDECIDED_TEXT,
    )
    assert _registration(CompoundStage.NISBA_ROLE).declared_outcomes == (
        "فاعلية",
        "مفعولية",
        "مسببية",
        COMPOUND_UNDECIDED_TEXT,
    )


def test_the_undecided_value_is_a_member_of_every_vocabulary() -> None:
    for registration in COMPOUND_LAYER_PREREGISTRATION.registrations:
        assert registration.undecided_outcome in registration.declared_outcomes


def test_an_undecided_value_outside_its_own_vocabulary_is_refused() -> None:
    with pytest.raises(CompoundLayerPreregistrationError, match="ليست عضوًا"):
        replace(
            _registration(CompoundStage.AMIL_MAMUL),
            undecided_outcome="قيمة_لم_تُسجَّل",
        )


def test_each_stage_names_the_refusals_the_request_states() -> None:
    named = {
        stage: tuple(refusal.name for refusal in _registration(stage).refusals)
        for stage in CompoundStage
    }
    assert named[CompoundStage.AMIL_MAMUL] == (
        "GovernanceRelationIsNotBornOntology",
        "DeclaredAmil != BornOperator",
        "FormalClassification != BirthVerdict",
        "SurfaceEffectIsNotSemanticRole",
    )
    assert named[CompoundStage.NISBA_ISNADIYYA] == (
        "IsnadiyyaIsNotTruth",
        "DeclaredNisba != BornRelation",
    )
    assert named[CompoundStage.TADMIN_TAQYID] == (
        "TadminIsNotLogicalEntailment",
        "TaqyidIsNotQuantification",
        "DeclaredMode != BornOntology",
    )
    assert named[CompoundStage.NISBA_ROLE] == (
        "MusabbibiyyaIsNotCausation",
        "RoleIsNotAgencyOfAnAgent",
        "SemanticRoleIsNotSurfaceGovernance",
    )


def test_every_refusal_carries_a_statement_not_a_bare_name() -> None:
    for registration in COMPOUND_LAYER_PREREGISTRATION.registrations:
        for refusal in registration.refusals:
            assert refusal.statement.strip()
    with pytest.raises(CompoundLayerPreregistrationError, match="بيان الرفض"):
        NamedRefusal(name="SomeRefusal", statement="   ")


def test_a_stage_with_no_named_refusal_is_refused() -> None:
    with pytest.raises(CompoundLayerPreregistrationError, match="بلا رفضٍ مُسمّى"):
        replace(_registration(CompoundStage.AMIL_MAMUL), refusals=())


def test_a_duplicate_refusal_name_is_refused() -> None:
    only = _registration(CompoundStage.NISBA_ISNADIYYA).refusals[0]
    with pytest.raises(CompoundLayerPreregistrationError, match="رفضٌ مكرّر"):
        replace(_registration(CompoundStage.NISBA_ISNADIYYA), refusals=(only, only))


def test_a_duplicate_outcome_value_is_refused() -> None:
    with pytest.raises(CompoundLayerPreregistrationError, match="قيمةٌ مكرّرة"):
        replace(
            _registration(CompoundStage.AMIL_MAMUL),
            declared_outcomes=("عامل", "عامل", COMPOUND_UNDECIDED_TEXT),
        )


def test_a_vocabulary_with_fewer_than_two_values_is_refused() -> None:
    with pytest.raises(CompoundLayerPreregistrationError, match="قيمتين فأكثر"):
        replace(
            _registration(CompoundStage.AMIL_MAMUL),
            declared_outcomes=(COMPOUND_UNDECIDED_TEXT,),
        )


def test_a_blank_outcome_value_is_refused() -> None:
    with pytest.raises(CompoundLayerPreregistrationError, match="غير فارغ"):
        replace(
            _registration(CompoundStage.AMIL_MAMUL),
            declared_outcomes=("عامل", "   ", COMPOUND_UNDECIDED_TEXT),
        )


def test_the_dependency_order_is_derived_and_a_written_one_is_checked() -> None:
    assert derived_prerequisites(CompoundStage.AMIL_MAMUL) == ()
    assert derived_prerequisites(CompoundStage.NISBA_ISNADIYYA) == ()
    assert derived_prerequisites(CompoundStage.TADMIN_TAQYID) == (
        CompoundStage.AMIL_MAMUL,
    )
    assert derived_prerequisites(CompoundStage.NISBA_ROLE) == (
        CompoundStage.NISBA_ISNADIYYA,
    )
    with pytest.raises(CompoundLayerPreregistrationError, match="على خلاف المُشتَقّ"):
        replace(_registration(CompoundStage.TADMIN_TAQYID), prerequisites=())
    with pytest.raises(CompoundLayerPreregistrationError, match="على خلاف المُشتَقّ"):
        replace(
            _registration(CompoundStage.NISBA_ROLE),
            prerequisites=(CompoundStage.AMIL_MAMUL,),
        )


def test_a_stage_placed_before_its_prerequisite_is_refused() -> None:
    with pytest.raises(CompoundLayerPreregistrationError, match="سبقت شرطها"):
        CompoundLayerPreregistration(
            registrations=(
                _registration(CompoundStage.TADMIN_TAQYID),
                _registration(CompoundStage.AMIL_MAMUL),
                _registration(CompoundStage.NISBA_ISNADIYYA),
                _registration(CompoundStage.NISBA_ROLE),
            )
        )


def test_a_missing_stage_is_refused_rather_than_silently_shortened() -> None:
    with pytest.raises(CompoundLayerPreregistrationError, match="مرحلةٌ مفقودة"):
        CompoundLayerPreregistration(
            registrations=(
                _registration(CompoundStage.AMIL_MAMUL),
                _registration(CompoundStage.NISBA_ISNADIYYA),
            )
        )


def test_a_duplicate_stage_is_refused() -> None:
    with pytest.raises(CompoundLayerPreregistrationError, match="مرحلةٌ مكرّرة"):
        CompoundLayerPreregistration(
            registrations=(
                _registration(CompoundStage.AMIL_MAMUL),
                _registration(CompoundStage.AMIL_MAMUL),
                _registration(CompoundStage.NISBA_ISNADIYYA),
                _registration(CompoundStage.TADMIN_TAQYID),
                _registration(CompoundStage.NISBA_ROLE),
            )
        )


def test_attested_per_branch_is_declared_but_unconstructible_today() -> None:
    with pytest.raises(CompoundLayerPreregistrationError, match="لا سلطة"):
        replace(
            _registration(CompoundStage.AMIL_MAMUL),
            attestation=AttestationStanding.ATTESTED_PER_BRANCH,
        )


def test_a_supplied_but_unverified_source_is_refused_with_its_own_reason() -> None:
    with pytest.raises(CompoundLayerPreregistrationError, match="لم يُقدَّم"):
        replace(
            _registration(CompoundStage.AMIL_MAMUL),
            attestation=AttestationStanding.SOURCE_SUPPLIED_NOT_VERIFIED,
        )


def test_every_stage_stands_at_source_not_supplied_with_a_reason() -> None:
    for registration in COMPOUND_LAYER_PREREGISTRATION.registrations:
        assert registration.attestation is AttestationStanding.SOURCE_NOT_SUPPLIED
        assert registration.missing_source_note.strip()


def test_no_certificate_is_constructible_on_any_branch() -> None:
    assert COMPOUND_LAYER_PREREGISTRATION.certificate_is_constructible is False
    assert COMPOUND_SUCCESS_TITLE_IS_WITHHELD.strip()
    assert COMPOUND_SOURCE_REQUIREMENT.strip()
    assert COMPOUND_SCOPE_NOTE.strip()
    assert COMPOUND_AUTHORITY_NOTE.strip()
    assert COMPOUND_REQUESTED_NOT_ATTESTED_NOTE.strip()


def test_no_type_here_carries_a_result_field() -> None:
    forbidden = ("result", "verdict", "birth", "certificate", "proof")
    for dataclass_type in (
        NamedRefusal,
        CompoundStageRegistration,
        CompoundLayerPreregistration,
    ):
        for declared in fields(dataclass_type):
            lowered = declared.name.lower()
            assert not any(token in lowered for token in forbidden)


def test_the_module_reads_no_kernel_authority() -> None:
    source = (
        Path(__file__).resolve().parents[2]
        / "src"
        / "alghanem"
        / "arabic"
        / "compound_layer_preregistration.py"
    ).read_text(encoding="utf-8")

    imports = tuple(
        line for line in source.splitlines() if line.startswith(("import ", "from "))
    )

    assert imports
    assert not any("kernel" in line for line in imports)


@pytest.mark.parametrize("card", _CARDS)
def test_the_preregistration_changes_no_external_audit_field(card: str) -> None:
    before = json.dumps(
        audit_card(_EXAMPLES / card).to_dict(), ensure_ascii=False, sort_keys=True
    )

    assert COMPOUND_LAYER_PREREGISTRATION.certificate_is_constructible is False

    after = json.dumps(
        audit_card(_EXAMPLES / card).to_dict(), ensure_ascii=False, sort_keys=True
    )
    assert before == after
