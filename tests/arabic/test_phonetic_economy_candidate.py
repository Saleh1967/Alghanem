"""المرشّحُ الصوتيُّ: الحكمُ محسوبٌ، والبقايا شرطُ وجود، والتصديقُ ممنوعٌ بنيويًّا.

يُثبِت هذا الاختبارُ خمسةَ أشياء: أنّ الحكمَ المُسجَّل `DEFER_IN_SCOPE` وفحصَه
`FAIL` على المحاور الثلاثة، وأنّ الفحصَ محسوبٌ حقًّا فينقلب `PASS` بانفكاك أيِّ
محورٍ واحد، وأنّ فارقَ الأداة المُرفَقة يُحسَب حيًّا ولا تُبنى بطاقةٌ به بلا
بقيّتِه، وأنّ التصديقَ يُرَدُّ ما دامت بقيّةُ منعِ الإغلاق قائمة، وأنّ تعميمَ
نتائج الجلسة مُسجَّلٌ بقيّةً بمداها لا تعليقًا.
"""

from __future__ import annotations

import pytest

from alghanem.arabic.phonetic_economy_candidate import (
    CLOSURE_BLOCKING_RESIDUAL_CODE,
    GFLK_SESSION_FINDINGS_SHARE_ONE_ORIGIN,
    INDEPENDENT_CLOSURE_NOT_MET,
    LAM_TARIF_EVIDENCE,
    NUN_SAKIN_EVIDENCE,
    PHONETIC_ECONOMY_CANDIDATE,
    TOOL_IS_APPROXIMATE_RECONSTRUCTION,
    TOOL_RECONSTRUCTION_RESIDUAL_CODE,
    CertifiedPhoneticEconomyFinding,
    ChainVerdict,
    ClosureOutcome,
    IndependenceAxis,
    IndependentClosureCheck,
    LicensedWeakerExhaustion,
    PhoneticEconomyCandidate,
    PhoneticEconomyRegistrationError,
    PhoneticEvidenceItem,
    RegisteredResidual,
    ResidualScope,
    ToolReconstructionReading,
    WeakerModelAttempt,
    WeakerModelOutcome,
    certify_phonetic_economy_candidate,
    registered_residual_for,
)
from alghanem.arabic.phonetic_economy_tool import (
    TOOL_MODULE_PATH,
    compute_lam_f,
    compute_nun_f,
)


def _evidence(**changes: object) -> PhoneticEvidenceItem:
    base: dict[str, object] = {
        "key": "K",
        "phenomenon": "ظاهرةٌ مقيسة",
        "statistic_name": "F",
        "statistic_value": 1.0,
        "corpus_identity": "كوربصٌ مُسمًّى",
        "tool_identity": "أداةٌ مُسمّاة",
        "metric_definition": "تعريفُ مقياس",
    }
    base.update(changes)
    return PhoneticEvidenceItem(**base)  # type: ignore[arg-type]


def _exhaustion() -> LicensedWeakerExhaustion:
    return LicensedWeakerExhaustion(
        attempts=(
            WeakerModelAttempt(model_name="عشوائيّ", outcome=WeakerModelOutcome.فشل),
        )
    )


def _candidate(**changes: object) -> PhoneticEconomyCandidate:
    base: dict[str, object] = {
        "claim": "دعوى",
        "session_identity": "جلسة",
        "closure_check": IndependentClosureCheck(
            evidence=(_evidence(key="A"), _evidence(key="B"))
        ),
        "weaker_exhaustion": _exhaustion(),
        "tool_readings": (),
        "residuals": (INDEPENDENT_CLOSURE_NOT_MET,),
    }
    base.update(changes)
    return PhoneticEconomyCandidate(**base)  # type: ignore[arg-type]


def test_registered_candidate_is_defer_in_scope_on_all_three_axes() -> None:
    check = PHONETIC_ECONOMY_CANDIDATE.closure_check
    assert check.outcome is ClosureOutcome.FAIL
    assert check.same_corpus and check.same_tool and check.same_metric_definition
    assert set(check.collapsed_axes) == set(IndependenceAxis)
    assert PHONETIC_ECONOMY_CANDIDATE.verdict is ChainVerdict.DEFER_IN_SCOPE
    assert PHONETIC_ECONOMY_CANDIDATE.is_closure_blocked


def test_registered_evidence_keeps_its_independence_fields_populated() -> None:
    for item in (NUN_SAKIN_EVIDENCE, LAM_TARIF_EVIDENCE):
        assert item.corpus_identity.strip()
        assert item.metric_definition.strip()
        assert item.tool_identity == TOOL_MODULE_PATH
    assert NUN_SAKIN_EVIDENCE.statistic_value == 4.0
    assert LAM_TARIF_EVIDENCE.statistic_value == 9.5


@pytest.mark.parametrize(
    ("changed_field", "axis"),
    [
        ("corpus_identity", IndependenceAxis.كوربص),
        ("tool_identity", IndependenceAxis.أداة),
        ("metric_definition", IndependenceAxis.تعريف_المقياس),
    ],
)
def test_closure_outcome_is_computed_not_hardcoded(
    changed_field: str, axis: IndependenceAxis
) -> None:
    check = IndependentClosureCheck(
        evidence=(
            _evidence(key="A"),
            _evidence(key="B", **{changed_field: "مصدرٌ منفصلٌ حقًّا"}),
        )
    )
    assert check.outcome is ClosureOutcome.PASS
    assert axis not in check.collapsed_axes


def test_closure_check_requires_two_evidence_lines() -> None:
    with pytest.raises(PhoneticEconomyRegistrationError):
        IndependentClosureCheck(evidence=(_evidence(key="A"),))
    with pytest.raises(PhoneticEconomyRegistrationError):
        IndependentClosureCheck(evidence=(_evidence(key="A"), _evidence(key="A")))


@pytest.mark.parametrize(
    "omitted", ["corpus_identity", "tool_identity", "metric_definition"]
)
def test_evidence_refuses_omitted_provenance(omitted: str) -> None:
    with pytest.raises(PhoneticEconomyRegistrationError):
        _evidence(**{omitted: "   "})


def test_residual_survives_only_when_every_weaker_model_failed() -> None:
    survived = LicensedWeakerExhaustion(
        attempts=(
            WeakerModelAttempt(
                model_name="خطُّ أساسٍ عشوائيّ", outcome=WeakerModelOutcome.فشل
            ),
            WeakerModelAttempt(model_name="الثِّقَلُ وحدَه", outcome=WeakerModelOutcome.فشل),
        )
    )
    assert survived.residual_survives
    explained = LicensedWeakerExhaustion(
        attempts=(
            WeakerModelAttempt(
                model_name="الثِّقَلُ وحدَه", outcome=WeakerModelOutcome.فسّر_البقيّة
            ),
        )
    )
    assert not explained.residual_survives
    with pytest.raises(PhoneticEconomyRegistrationError):
        LicensedWeakerExhaustion(attempts=())


def test_registered_exhaustion_tried_both_weaker_models_and_both_failed() -> None:
    attempts = PHONETIC_ECONOMY_CANDIDATE.weaker_exhaustion.attempts
    assert len(attempts) == 2
    assert all(attempt.outcome is WeakerModelOutcome.فشل for attempt in attempts)
    assert PHONETIC_ECONOMY_CANDIDATE.weaker_exhaustion.residual_survives


def test_tool_discrepancy_is_computed_live_and_is_not_papered_over() -> None:
    readings = {
        reading.evidence_key: reading
        for reading in PHONETIC_ECONOMY_CANDIDATE.tool_readings
    }
    assert readings["NUN_SAKIN"].session_value == 4.0
    assert readings["LAM_TARIF"].session_value == 9.5
    assert readings["NUN_SAKIN"].reconstructed_value == compute_nun_f()
    assert readings["LAM_TARIF"].reconstructed_value == compute_lam_f()
    assert round(compute_nun_f(), 2) == 3.43
    assert round(compute_lam_f(), 2) == 9.96
    assert not any(
        reading.reproduces_session_value
        for reading in PHONETIC_ECONOMY_CANDIDATE.tool_readings
    )
    assert len(PHONETIC_ECONOMY_CANDIDATE.unreproduced_tool_readings) == 2
    assert (
        TOOL_RECONSTRUCTION_RESIDUAL_CODE in PHONETIC_ECONOMY_CANDIDATE.residual_codes
    )


def test_candidate_refuses_a_tool_discrepancy_without_its_residual() -> None:
    readings = (
        ToolReconstructionReading(
            evidence_key="NUN_SAKIN", session_value=4.0, reconstruction="compute_nun_f"
        ),
    )
    with pytest.raises(PhoneticEconomyRegistrationError):
        _candidate(tool_readings=readings)
    accepted = _candidate(
        tool_readings=readings,
        residuals=(INDEPENDENT_CLOSURE_NOT_MET, TOOL_IS_APPROXIMATE_RECONSTRUCTION),
    )
    assert accepted.unreproduced_tool_readings == readings


def test_tool_reading_refuses_an_unregistered_computation() -> None:
    with pytest.raises(PhoneticEconomyRegistrationError):
        ToolReconstructionReading(
            evidence_key="NUN_SAKIN", session_value=4.0, reconstruction="compute_x_f"
        )


def test_candidate_refuses_a_failed_check_without_its_residual() -> None:
    with pytest.raises(PhoneticEconomyRegistrationError):
        _candidate(residuals=(GFLK_SESSION_FINDINGS_SHARE_ONE_ORIGIN,))
    with pytest.raises(PhoneticEconomyRegistrationError):
        _candidate(residuals=())


def test_candidate_refuses_a_blocking_residual_the_check_does_not_support() -> None:
    passing = IndependentClosureCheck(
        evidence=(_evidence(key="A"), _evidence(key="B", corpus_identity="كوربصٌ آخر"))
    )
    with pytest.raises(PhoneticEconomyRegistrationError):
        _candidate(closure_check=passing)


def test_certification_is_refused_while_the_blocking_residual_stands() -> None:
    with pytest.raises(PhoneticEconomyRegistrationError):
        certify_phonetic_economy_candidate(PHONETIC_ECONOMY_CANDIDATE)


def test_certified_type_cannot_be_built_directly() -> None:
    with pytest.raises(PhoneticEconomyRegistrationError):
        CertifiedPhoneticEconomyFinding(candidate=PHONETIC_ECONOMY_CANDIDATE)


def test_certification_succeeds_only_on_a_genuinely_independent_candidate() -> None:
    independent = _candidate(
        closure_check=IndependentClosureCheck(
            evidence=(
                _evidence(key="A"),
                _evidence(
                    key="B",
                    corpus_identity="كوربصٌ منفصلٌ حقًّا",
                    tool_identity="أداةٌ منفصلةٌ حقًّا",
                    metric_definition="تعريفُ مقياسٍ منفصلٌ حقًّا",
                ),
            )
        ),
        residuals=(GFLK_SESSION_FINDINGS_SHARE_ONE_ORIGIN,),
    )
    assert independent.verdict is ChainVerdict.CLOSURE_MET_PENDING_AUTHORITY
    certified = certify_phonetic_economy_candidate(independent)
    assert isinstance(certified, CertifiedPhoneticEconomyFinding)
    assert certified.candidate is independent


def test_the_session_generalization_is_a_residual_object_not_a_comment() -> None:
    residual = registered_residual_for("GFLK_SESSION_FINDINGS_SHARE_ONE_ORIGIN")
    assert residual is GFLK_SESSION_FINDINGS_SHARE_ONE_ORIGIN
    assert residual.scope is ResidualScope.كل_نتائج_الجلسة
    assert "١٣٠" in residual.statement
    assert INDEPENDENT_CLOSURE_NOT_MET.scope is ResidualScope.هذا_المرشّح
    statement = INDEPENDENT_CLOSURE_NOT_MET.statement
    assert "NoBedrockWithoutRecurringDirayaSurvival" in statement
    with pytest.raises(PhoneticEconomyRegistrationError):
        registered_residual_for("NO_SUCH_RESIDUAL")


def test_registered_residuals_are_exactly_the_three_named_ones() -> None:
    assert PHONETIC_ECONOMY_CANDIDATE.residual_codes == (
        CLOSURE_BLOCKING_RESIDUAL_CODE,
        TOOL_RECONSTRUCTION_RESIDUAL_CODE,
        "GFLK_SESSION_FINDINGS_SHARE_ONE_ORIGIN",
    )
    with pytest.raises(PhoneticEconomyRegistrationError):
        _candidate(residuals=(INDEPENDENT_CLOSURE_NOT_MET, INDEPENDENT_CLOSURE_NOT_MET))
    with pytest.raises(PhoneticEconomyRegistrationError):
        RegisteredResidual(code=" ", statement="نصّ", scope=ResidualScope.هذا_المرشّح)


def test_the_module_declares_no_success_title_and_no_birth_member() -> None:
    from alghanem.arabic import phonetic_economy_candidate as module

    assert not [name for name in dir(module) if "SUCCESS" in name]
    assert {member.name for member in ChainVerdict} == {
        "DEFER_IN_SCOPE",
        "CLOSURE_MET_PENDING_AUTHORITY",
    }
