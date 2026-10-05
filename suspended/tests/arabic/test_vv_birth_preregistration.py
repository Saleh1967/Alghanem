"""اختباراتُ التسجيل القبليّ G0.VV-BIRTH-1: تجميدُ الشروط، وانعدامُ القراءة."""

from __future__ import annotations

import importlib.util
import pkgutil
from dataclasses import fields, replace
from pathlib import Path

import pytest

import alghanem.kernel as kernel_package
from alghanem.arabic.vv_birth_hypothesis import (
    BANNED_IDENTITY_PROXIES,
    BEHAVIOURAL_CLOSURE_LAW,
    COMPETING_TYPE_HYPOTHESES,
    HYPOTHESES,
    IDENTITY_PROJECTION,
    LICENSED_JOIN_SPECIFICATION,
    QUANTITY_PROJECTION,
    SEPARATED_CLAIMS,
    TRACE_MINIMALITY_CRITERION,
    TYPED_SPACES,
    WEAKER_MODELS,
    ExperimentOutcome,
    Hypothesis,
    HypothesisIdentifier,
    TypedSpaceIdentifier,
    VvBirthHypothesisError,
    WeakerModelRole,
    hypothesis_named,
    weaker_model_named,
)
from alghanem.arabic.vv_birth_preregistration import (
    ADVERSE_TREE_FACTS,
    EXPERIMENT_ID,
    OUTCOME_CEILINGS,
    PREREGISTRATION_DIGEST,
    READOUT_MODULE_NAME,
    READOUT_SEAL_CONTRACT,
    RECONSTRUCTION_TARGET_ASSESSMENTS,
    REQUIRED_NOTATION_SITES,
    VV_BIRTH_PREREGISTRATION_NAMED_RESIDUALS,
    OutcomeCeiling,
    TargetIndependence,
    VvBirthPreregistrationError,
    ceiling_for,
    missing_notation_sites,
    preregistration_digest,
    readout_module_is_absent,
    target_assessment_named,
)

_SOURCE_ROOT = Path(__file__).resolve().parents[2] / "src" / "alghanem"


class TestNoJudgementIsFrozenOnlyItsConditions:
    def test_born_is_not_an_issuable_state(self) -> None:
        names = {outcome.name for outcome in ExperimentOutcome}
        values = {outcome.value for outcome in ExperimentOutcome}
        assert "BORN" not in names
        assert "BORN" not in values
        assert "FULL_CONSTITUTIONAL_BIRTH" not in values

    def test_every_hypothesis_admits_its_own_refutation(self) -> None:
        for hypothesis in HYPOTHESES:
            assert ExperimentOutcome.REFUTED in hypothesis.admissible_outcomes
            assert len(hypothesis.admissible_outcomes) >= 2

    def test_a_hypothesis_with_one_admissible_outcome_is_refused(self) -> None:
        with pytest.raises(VvBirthHypothesisError):
            Hypothesis(
                identifier=HypothesisIdentifier.H_E,
                statement="نصٌّ مفترض",
                independent_falsifier="مُفنِّدٌ مفترض",
                precondition="شرطٌ مفترض",
                admissible_outcomes=(ExperimentOutcome.PASS,),
            )

    def test_a_hypothesis_that_cannot_be_refuted_is_refused(self) -> None:
        with pytest.raises(VvBirthHypothesisError):
            Hypothesis(
                identifier=HypothesisIdentifier.H_E,
                statement="نصٌّ مفترض",
                independent_falsifier="مُفنِّدٌ مفترض",
                precondition="شرطٌ مفترض",
                admissible_outcomes=(
                    ExperimentOutcome.PASS,
                    ExperimentOutcome.UNDERPOWERED,
                ),
            )

    def test_every_hypothesis_carries_a_non_blank_falsifier(self) -> None:
        for hypothesis in HYPOTHESES:
            assert hypothesis.independent_falsifier.strip()
            assert hypothesis.precondition.strip()

    def test_no_declared_field_carries_a_judgement(self) -> None:
        markers = ("verdict", "born", "score", "result", "measured")
        for declaring_type in (
            Hypothesis,
            OutcomeCeiling,
        ):
            declared = {item.name for item in fields(declaring_type)}
            for marker in markers:
                assert not any(marker in name for name in declared), marker


class TestNeutralityNeedsAnOperationAndAnEquivalence:
    def test_h_e_and_h_n_are_two_hypotheses_not_one(self) -> None:
        assert hypothesis_named(HypothesisIdentifier.H_E) is not hypothesis_named(
            HypothesisIdentifier.H_N
        )
        assert "⊗" not in hypothesis_named(HypothesisIdentifier.H_E).statement
        assert "⊗" in hypothesis_named(HypothesisIdentifier.H_N).statement

    def test_a_neutral_element_outcome_is_not_in_the_vocabulary(self) -> None:
        assert "NEUTRAL_ELEMENT_SUPPORTED" not in {
            outcome.value for outcome in ExperimentOutcome
        }

    def test_h_n_is_capped_at_undefined_while_the_operation_is_undefined(
        self,
    ) -> None:
        ceiling = ceiling_for(HypothesisIdentifier.H_N)
        assert ceiling is not None
        assert ceiling.ceiling is ExperimentOutcome.UNDEFINED
        assert ceiling.what_would_raise_it.strip()


class TestTheProjectionsAreDefinedBeforeAnyReadout:
    def test_the_three_typed_spaces_are_all_defined(self) -> None:
        assert {space.identifier for space in TYPED_SPACES} == set(TypedSpaceIdentifier)

    def test_a_program_index_cannot_be_a_phonetic_identity(self) -> None:
        assert "letter_index" in BANNED_IDENTITY_PROXIES
        assert "letter_index" in IDENTITY_PROJECTION.banned_proxies

    def test_a_projection_with_no_banned_proxy_is_refused(self) -> None:
        with pytest.raises(VvBirthHypothesisError):
            replace(IDENTITY_PROJECTION, banned_proxies=())

    def test_a_banned_proxy_outside_the_named_list_is_refused(self) -> None:
        with pytest.raises(VvBirthHypothesisError):
            replace(IDENTITY_PROJECTION, banned_proxies=("something_else",))

    def test_the_quantity_codomain_is_counting_not_physical_time(self) -> None:
        assert "{1, 2}" in QUANTITY_PROJECTION.codomain
        assert "وليس زمنًا" in QUANTITY_PROJECTION.codomain

    def test_each_projection_names_what_would_make_it_vacuous(self) -> None:
        for projection in (IDENTITY_PROJECTION, QUANTITY_PROJECTION):
            assert projection.what_would_make_it_vacuous.strip()
            assert projection.what_it_forgets.strip()


class TestTheTypeQuestionIsNotDecidedHere:
    def test_both_competing_hypotheses_are_frozen(self) -> None:
        assert COMPETING_TYPE_HYPOTHESES == (
            HypothesisIdentifier.H_SAME_TYPE,
            HypothesisIdentifier.H_DIFFERENT_TYPE,
        )
        for identifier in COMPETING_TYPE_HYPOTHESES:
            assert hypothesis_named(identifier).independent_falsifier.strip()

    def test_neither_competitor_carries_a_ceiling_that_decides_it(self) -> None:
        for identifier in COMPETING_TYPE_HYPOTHESES:
            assert ceiling_for(identifier) is None


class TestClosureIsAQuotientLawNotTemplateMembership:
    def test_the_law_quantifies_over_licensed_outer_contexts(self) -> None:
        assert "Obs(k[g]) = Obs(k[π(g)])" in BEHAVIOURAL_CLOSURE_LAW.quotient_law
        assert (
            "NoCrossBoundaryActiveResidual"
            in BEHAVIOURAL_CLOSURE_LAW.residual_condition
        )

    def test_template_membership_is_named_as_no_substitute(self) -> None:
        assert (
            "SyllableTemplate"
            in BEHAVIOURAL_CLOSURE_LAW.what_does_not_substitute_for_it
        )

    def test_untestable_contexts_yield_an_underpowered_outcome(self) -> None:
        assert BEHAVIOURAL_CLOSURE_LAW.underpowered_outcome is (
            ExperimentOutcome.BEHAVIOURAL_CLOSURE_UNDERPOWERED
        )
        with pytest.raises(VvBirthHypothesisError):
            replace(
                BEHAVIOURAL_CLOSURE_LAW,
                underpowered_outcome=ExperimentOutcome.PASS,
            )


class TestTheJoinIsAPartialTypedOperation:
    def test_it_names_both_its_definedness_and_its_impediments(self) -> None:
        assert LICENSED_JOIN_SPECIFICATION.definedness_conditions
        assert LICENSED_JOIN_SPECIFICATION.undefinedness_conditions

    def test_a_join_without_impediments_is_refused(self) -> None:
        with pytest.raises(VvBirthHypothesisError):
            replace(LICENSED_JOIN_SPECIFICATION, undefinedness_conditions=())

    def test_totality_is_named_as_what_would_make_closure_vacuous(self) -> None:
        assert "كلّيّة" in LICENSED_JOIN_SPECIFICATION.why_partiality_is_not_a_defect


class TestTraceMinimality:
    def test_a_strict_subset_of_the_trace_must_fail(self) -> None:
        assert "T' ⊊ T" in TRACE_MINIMALITY_CRITERION.minimality_law

    def test_a_trace_carrying_the_answer_yields_a_tautology_outcome(self) -> None:
        assert TRACE_MINIMALITY_CRITERION.tautology_outcome is (
            ExperimentOutcome.TRACE_TAUTOLOGY
        )
        with pytest.raises(VvBirthHypothesisError):
            replace(
                TRACE_MINIMALITY_CRITERION,
                tautology_outcome=ExperimentOutcome.PASS,
            )


class TestTheWeakerModels:
    def test_four_rivals_and_one_leakage_baseline_are_frozen(self) -> None:
        rivals = [model for model in WEAKER_MODELS if model.counts_as_evidence]
        baselines = [
            model
            for model in WEAKER_MODELS
            if model.role is WeakerModelRole.LEAKAGE_BASELINE
        ]
        assert len(rivals) == 4
        assert len(baselines) == 1
        assert {model.name for model in rivals} == {
            "M_drop",
            "M_consonant",
            "M_second_vowel",
            "M_no_join",
        }

    def test_the_leakage_baseline_is_not_evidence(self) -> None:
        baseline = weaker_model_named("M_identity_lookup")
        assert not baseline.counts_as_evidence
        assert "اسمَ الحرف" in baseline.what_it_sees

    def test_an_unknown_weaker_model_is_refused_by_name(self) -> None:
        with pytest.raises(VvBirthHypothesisError):
            weaker_model_named("M_unknown")

    def test_a_rival_reconstructing_the_target_is_an_admissible_outcome(
        self,
    ) -> None:
        assert (
            ExperimentOutcome.WEAKER_MODEL_RECONSTRUCTS
            in hypothesis_named(HypothesisIdentifier.H_S).admissible_outcomes
        )


class TestTheThreeClaimsAreSeparated:
    def test_they_are_three_and_named_in_order(self) -> None:
        assert [claim.name for claim in SEPARATED_CLAIMS] == [
            "IDENTITY_PRESERVATION",
            "QUANTITY_TRANSFORMATION",
            "HISTORICAL_RECOVERABILITY",
        ]

    def test_each_names_what_its_success_does_not_prove(self) -> None:
        for claim in SEPARATED_CLAIMS:
            assert claim.what_its_success_does_not_prove.strip()


class TestTheAdverseFactsAreDepositedBeforeTheRun:
    def test_the_four_adverse_facts_are_named(self) -> None:
        assert {fact.name for fact in ADVERSE_TREE_FACTS} == {
            "NO_BIRTH_CERTIFICATE_FOR_C_OR_V",
            "NO_RECORDED_SOUND_IN_THIS_TREE",
            "NO_INDEPENDENT_RECONSTRUCTION_TARGET",
            "THE_MADD_LABEL_IS_A_RULE_OUTPUT",
        }

    def test_every_adverse_fact_carries_grounds_and_a_prohibition(self) -> None:
        for fact in ADVERSE_TREE_FACTS:
            assert fact.grounds.strip()
            assert fact.what_it_forbids.strip()

    def test_the_syllable_hypothesis_is_capped_at_conditional_birth(self) -> None:
        ceiling = ceiling_for(HypothesisIdentifier.H_S)
        assert ceiling is not None
        assert ceiling.ceiling is ExperimentOutcome.CONDITIONAL_STRUCTURAL_BIRTH

    def test_at_most_one_ceiling_is_frozen_per_hypothesis(self) -> None:
        capped = [ceiling.hypothesis for ceiling in OUTCOME_CEILINGS]
        assert len(set(capped)) == len(capped)

    def test_a_ceiling_outside_its_hypothesis_outcomes_is_refused(self) -> None:
        with pytest.raises(VvBirthPreregistrationError):
            OutcomeCeiling(
                hypothesis=HypothesisIdentifier.H_E,
                ceiling=ExperimentOutcome.CONDITIONAL_STRUCTURAL_BIRTH,
                grounds="سندٌ مفترض",
                what_would_raise_it="رفعٌ مفترض",
            )


class TestNoIndependentTargetExistsToday:
    def test_no_assessed_target_is_usable(self) -> None:
        assert RECONSTRUCTION_TARGET_ASSESSMENTS
        assert not any(
            assessment.is_usable for assessment in RECONSTRUCTION_TARGET_ASSESSMENTS
        )

    def test_the_syllabifier_is_disqualified_for_sharing_the_model_rules(
        self,
    ) -> None:
        assessment = target_assessment_named("alghanem.arabic.syllabifier")
        assert assessment.independence is (
            TargetIndependence.DISQUALIFIED_SHARES_THE_MODEL_RULES
        )
        assert "syllable_preregistration" in assessment.grounds

    def test_the_missing_target_outcome_is_admissible_for_the_syllable_claim(
        self,
    ) -> None:
        admissible = hypothesis_named(HypothesisIdentifier.H_S).admissible_outcomes
        assert ExperimentOutcome.INDEPENDENT_TARGET_MISSING in admissible
        assert ExperimentOutcome.CIRCULAR_TARGET in admissible

    def test_an_unknown_target_is_refused_by_name(self) -> None:
        with pytest.raises(VvBirthPreregistrationError):
            target_assessment_named("لا_هدف")


class TestTheFidelityCheckIsNotATautology:
    def test_the_site_list_is_written_by_hand_not_read_from_the_text(self) -> None:
        source = (_SOURCE_ROOT / "arabic" / "vv_birth_preregistration.py").read_text(
            encoding="utf-8"
        )
        head, _, _ = source.partition("def missing_notation_sites")
        declaration = head.rpartition("REQUIRED_NOTATION_SITES")[2]
        for forbidden in ("__all__", "dir(", "splitlines", "read_text", "getmembers"):
            assert forbidden not in declaration, forbidden

    def test_no_required_site_is_missing_today(self) -> None:
        assert missing_notation_sites() == ()

    def test_a_removed_site_is_actually_detected(self, monkeypatch) -> None:
        import alghanem.arabic.vv_birth_hypothesis as hypothesis_module

        monkeypatch.delattr(hypothesis_module, "WEAKER_MODELS")
        assert ("vv_birth_hypothesis", "WEAKER_MODELS") in missing_notation_sites()

    def test_every_required_site_is_distinct(self) -> None:
        assert len(set(REQUIRED_NOTATION_SITES)) == len(REQUIRED_NOTATION_SITES)


class TestTheSealIsHistoricalNotSelfReferential:
    def test_the_readout_module_does_not_exist_in_this_commit(self) -> None:
        assert readout_module_is_absent()
        assert importlib.util.find_spec(READOUT_MODULE_NAME) is None
        assert not (_SOURCE_ROOT / "arabic" / "vv_birth_readout.py").exists()

    def test_no_test_module_for_the_readout_exists_either(self) -> None:
        assert not (
            Path(__file__).resolve().parent / "test_vv_birth_readout.py"
        ).exists()

    def test_the_contract_binds_the_readout_to_a_prior_commit(self) -> None:
        assert READOUT_SEAL_CONTRACT.required_readout_fields == (
            "prereg_commit_sha",
            "expected_preregistration_digest",
        )
        assert READOUT_SEAL_CONTRACT.refusal_condition.strip()

    def test_the_contract_states_what_the_digest_cannot_detect(self) -> None:
        assert "التزامٍ واحد" in READOUT_SEAL_CONTRACT.what_this_digest_does_not_detect

    def test_this_module_carries_no_commit_sha_of_its_own(self) -> None:
        source = (_SOURCE_ROOT / "arabic" / "vv_birth_preregistration.py").read_text(
            encoding="utf-8"
        )
        assert "prereg_commit_sha=" not in source
        assert READOUT_SEAL_CONTRACT.why_this_module_carries_no_commit_sha.strip()

    def test_a_contract_with_fewer_than_two_bound_fields_is_refused(self) -> None:
        with pytest.raises(VvBirthPreregistrationError):
            replace(READOUT_SEAL_CONTRACT, required_readout_fields=("only_one",))


class TestRegistrationNotAuthority:
    def test_the_experiment_is_named(self) -> None:
        assert EXPERIMENT_ID == "G0.VV-BIRTH-1"

    def test_the_digest_is_rederived_at_import(self) -> None:
        assert PREREGISTRATION_DIGEST == preregistration_digest()
        assert len(PREREGISTRATION_DIGEST) == 64

    def test_the_named_residuals_are_sorted_and_distinct(self) -> None:
        assert list(VV_BIRTH_PREREGISTRATION_NAMED_RESIDUALS) == sorted(
            VV_BIRTH_PREREGISTRATION_NAMED_RESIDUALS
        )
        assert len(set(VV_BIRTH_PREREGISTRATION_NAMED_RESIDUALS)) == len(
            VV_BIRTH_PREREGISTRATION_NAMED_RESIDUALS
        )

    def test_the_cited_freeze_is_absent_from_this_tree(self) -> None:
        assert not (_SOURCE_ROOT / "arabic" / "vv_neutral_birth_freeze.py").exists()
        joined = " ".join(VV_BIRTH_PREREGISTRATION_NAMED_RESIDUALS)
        assert "TheCitedFreezeIsAbsentFromThisTree" in joined

    @pytest.mark.parametrize(
        "module_name",
        ("vv_birth_hypothesis", "vv_birth_preregistration"),
    )
    def test_neither_module_reads_kernel_authority(self, module_name: str) -> None:
        source = (_SOURCE_ROOT / "arabic" / f"{module_name}.py").read_text(
            encoding="utf-8"
        )
        imports = tuple(
            line
            for line in source.splitlines()
            if line.startswith(("import ", "from "))
        )
        assert imports
        assert not any("kernel" in line for line in imports)

    def test_no_kernel_module_reads_this_experiment(self) -> None:
        for module in pkgutil.walk_packages(
            kernel_package.__path__, prefix="alghanem.kernel."
        ):
            spec = module.module_finder.find_spec(module.name)  # type: ignore[union-attr]
            assert spec is not None and spec.origin is not None
            text = Path(spec.origin).read_text(encoding="utf-8")
            assert "vv_birth" not in text, module.name
