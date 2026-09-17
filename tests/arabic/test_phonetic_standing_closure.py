"""اختباراتُ إغلاق ملفّ الأصوات: منزلةٌ مُشتَقّة، وحجزٌ بشرطِ رفعٍ لا عصمة."""

from __future__ import annotations

import pkgutil
from pathlib import Path

import pytest

import alghanem.kernel as kernel_package
from alghanem.arabic.encoding.sakin_adjacency import MEASURED_SAKIN_CLASH_SOURCES
from alghanem.arabic.phonetic_standing_closure import (
    CLOSED_PHONETIC_FINDINGS,
    CLOSURE_REGISTRATION_DIGEST,
    EXTERNAL_SOURCE_SEARCH_RECORDS,
    PHONETIC_CLOSURE_NAMED_RESIDUALS,
    PHONETIC_FILE_CLOSURE,
    PROMOTION_CONDITION,
    ClosedPhoneticFinding,
    ExternalSourceSearchRecord,
    PhoneticFileClosure,
    PhoneticStanding,
    PhoneticStandingError,
    PhoneticStandingGate,
    PhoneticStandingRecord,
    RuleIndependence,
    SourceDeposit,
    TaggingSource,
    closure_registration_digest,
    finding_named,
    search_record_named,
)
from alghanem.arabic.transmission_standing import UnconstructibilityGenus


class TestTheStandingIsDerivedNotWritten:
    def test_the_standing_is_rule_derived_today(self) -> None:
        assert PHONETIC_FILE_CLOSURE.standing is (
            PhoneticStanding.RULE_DERIVED_BY_DECLARED_RULE
        )

    def test_the_record_cannot_be_built_outside_its_gate(self) -> None:
        with pytest.raises(PhoneticStandingError):
            PhoneticStandingRecord(
                tagging_source=TaggingSource.RULE_APPLIED_AUTOMATICALLY,
                source_deposit=SourceDeposit.NOT_DEPOSITED,
                rule_independence=RuleIndependence.DERIVED_BY_OUR_OWN_RULE,
            )

    def test_independent_verification_is_declared_but_unissuable(self) -> None:
        assert PhoneticStanding.INDEPENDENTLY_VERIFIED in PhoneticStanding
        with pytest.raises(PhoneticStandingError) as excinfo:
            PhoneticStandingGate.issue(
                tagging_source=TaggingSource.HUMAN_LETTER_BY_LETTER,
                source_deposit=SourceDeposit.DIGESTED_AND_DEPOSITED,
                rule_independence=(RuleIndependence.INDEPENDENT_OF_OUR_DERIVATION_RULE),
            )
        assert PROMOTION_CONDITION in str(excinfo.value)

    @pytest.mark.parametrize(
        ("tagging_source", "source_deposit", "rule_independence"),
        (
            (
                TaggingSource.HUMAN_LETTER_BY_LETTER,
                SourceDeposit.DIGESTED_AND_DEPOSITED,
                RuleIndependence.DERIVED_BY_OUR_OWN_RULE,
            ),
            (
                TaggingSource.HUMAN_LETTER_BY_LETTER,
                SourceDeposit.NOT_DEPOSITED,
                RuleIndependence.INDEPENDENT_OF_OUR_DERIVATION_RULE,
            ),
            (
                TaggingSource.RULE_APPLIED_AUTOMATICALLY,
                SourceDeposit.DIGESTED_AND_DEPOSITED,
                RuleIndependence.INDEPENDENT_OF_OUR_DERIVATION_RULE,
            ),
        ),
    )
    def test_any_missing_carrier_yields_the_rule_derived_standing(
        self,
        tagging_source: TaggingSource,
        source_deposit: SourceDeposit,
        rule_independence: RuleIndependence,
    ) -> None:
        record = PhoneticStandingGate.issue(
            tagging_source=tagging_source,
            source_deposit=source_deposit,
            rule_independence=rule_independence,
        )
        assert record.standing is PhoneticStanding.RULE_DERIVED_BY_DECLARED_RULE


class TestTheClosureIsHeldNotRefusedByCategory:
    def test_the_genus_is_a_hold_not_a_category_mismatch(self) -> None:
        assert PHONETIC_FILE_CLOSURE.unconstructibility_genus is (
            UnconstructibilityGenus.HELD_BY_MISSING_AUTHORITY_TODAY
        )
        assert PHONETIC_FILE_CLOSURE.unconstructibility_genus is not (
            UnconstructibilityGenus.REFUSED_BY_STRUCTURAL_CATEGORY_MISMATCH
        )

    def test_the_promotion_condition_names_its_four_requirements(self) -> None:
        assert PROMOTION_CONDITION.strip()
        assert PHONETIC_FILE_CLOSURE.promotion_condition == PROMOTION_CONDITION
        for requirement in ("بيدٍ بشريّةٍ حرفًا بحرف", "ترخيص", "بروتوكول", "اتّفاق"):
            assert requirement in PROMOTION_CONDITION

    def test_a_closure_without_a_promotion_condition_is_refused(self) -> None:
        with pytest.raises(PhoneticStandingError):
            PhoneticFileClosure(
                standing_record=PHONETIC_FILE_CLOSURE.standing_record,
                promotion_condition="   ",
                findings=CLOSED_PHONETIC_FINDINGS,
                search_records=EXTERNAL_SOURCE_SEARCH_RECORDS,
            )


class TestTheSearchRecordIsDepositedNotSummarised:
    def test_the_search_record_is_not_empty(self) -> None:
        assert EXTERNAL_SOURCE_SEARCH_RECORDS

    def test_a_closure_without_a_search_record_is_refused(self) -> None:
        with pytest.raises(PhoneticStandingError):
            PhoneticFileClosure(
                standing_record=PHONETIC_FILE_CLOSURE.standing_record,
                promotion_condition=PROMOTION_CONDITION,
                findings=CLOSED_PHONETIC_FINDINGS,
                search_records=(),
            )

    def test_quran_tajweed_is_refused_with_four_named_reasons(self) -> None:
        record = search_record_named("cpfair/quran-tajweed")
        assert record.license_text == "CC BY 4.0"
        assert len(record.refusal_reasons) == 4
        assert record.refusal_is_final
        joined = " ".join(record.refusal_reasons)
        assert "٢٠١٧" in joined
        assert "كوميتات" in joined
        assert "أشجار قرار" in joined
        assert "الكوربص" in joined

    def test_a_source_refused_without_a_reason_is_refused(self) -> None:
        with pytest.raises(PhoneticStandingError):
            ExternalSourceSearchRecord(
                source_id="مصدرٌ مفترض",
                license_text="رخصةٌ مفترضة",
                tagging_method="طريقةٌ مفترضة",
                refusal_reasons=(),
                refusal_is_final=False,
                why_the_refusal_stands_or_lifts="نصٌّ غير فارغ",
            )

    def test_an_unknown_source_is_refused_by_name(self) -> None:
        with pytest.raises(PhoneticStandingError):
            search_record_named("لا_مصدر")


class TestTheClosedFindings:
    def test_the_six_findings_are_named(self) -> None:
        assert {finding.identifier for finding in CLOSED_PHONETIC_FINDINGS} == {
            "IDGHAM_NUN_SAKINA_YARMALUN",
            "IDGHAM_LAM_SHAMSI",
            "IDGHAM_MITHLAN_MUTAQARIBAN_ACROSS_WORD_BOUNDARY",
            "MADD_MARKING",
            "HAMZAT_AL_WASL_MARKING",
            "SILENT_ALIF_MARKING",
        }

    def test_every_finding_carries_its_rule_and_its_impediment(self) -> None:
        for finding in CLOSED_PHONETIC_FINDINGS:
            assert finding.declared_rule.strip()
            assert finding.not_rederivable_because.strip()

    def test_the_third_class_stays_residue_defined_and_dependent(self) -> None:
        third = finding_named("IDGHAM_MITHLAN_MUTAQARIBAN_ACROSS_WORD_BOUNDARY")
        assert third.is_residue_defined
        assert third.depends_on_finding == "IDGHAM_NUN_SAKINA_YARMALUN"
        assert PHONETIC_FILE_CLOSURE.residue_defined_identifiers == (
            "IDGHAM_MITHLAN_MUTAQARIBAN_ACROSS_WORD_BOUNDARY",
        )

    def test_a_residue_defined_finding_without_a_dependency_is_refused(self) -> None:
        with pytest.raises(PhoneticStandingError):
            ClosedPhoneticFinding(
                identifier="X",
                phenomenon="ظاهرةٌ مفترضة",
                declared_rule="قاعدةٌ مفترضة",
                not_rederivable_because="سببٌ مفترض",
                is_residue_defined=True,
            )

    def test_a_dependency_on_an_unlisted_finding_is_refused(self) -> None:
        with pytest.raises(PhoneticStandingError):
            PhoneticFileClosure(
                standing_record=PHONETIC_FILE_CLOSURE.standing_record,
                promotion_condition=PROMOTION_CONDITION,
                findings=(
                    ClosedPhoneticFinding(
                        identifier="X",
                        phenomenon="ظاهرةٌ مفترضة",
                        declared_rule="قاعدةٌ مفترضة",
                        not_rederivable_because="سببٌ مفترض",
                        depends_on_finding="Y",
                    ),
                ),
                search_records=EXTERNAL_SOURCE_SEARCH_RECORDS,
            )

    def test_an_unknown_finding_is_refused_by_name(self) -> None:
        with pytest.raises(PhoneticStandingError):
            finding_named("لا_نتيجة")

    def test_no_finding_carries_a_figure_bearing_field(self) -> None:
        declared = set(ClosedPhoneticFinding.__dataclass_fields__)
        for marker in ("percent", "figure", "count", "value", "rate"):
            assert not any(marker in name for name in declared), marker


class TestRegistrationNotAuthority:
    def test_no_corpus_reached_the_tree(self) -> None:
        assert MEASURED_SAKIN_CLASH_SOURCES == ()

    def test_the_digest_is_rederived_at_import(self) -> None:
        assert CLOSURE_REGISTRATION_DIGEST == closure_registration_digest()
        assert len(CLOSURE_REGISTRATION_DIGEST) == 64

    def test_the_named_residuals_are_sorted_and_distinct(self) -> None:
        assert list(PHONETIC_CLOSURE_NAMED_RESIDUALS) == sorted(
            PHONETIC_CLOSURE_NAMED_RESIDUALS
        )
        assert len(set(PHONETIC_CLOSURE_NAMED_RESIDUALS)) == len(
            PHONETIC_CLOSURE_NAMED_RESIDUALS
        )

    def test_coverage_and_correctness_are_kept_apart_by_name(self) -> None:
        joined = " ".join(PHONETIC_CLOSURE_NAMED_RESIDUALS)
        assert "CoverageIsNotVerification" in joined
        assert "AHundredPercentIsNotCorrectness" in joined
        assert "ImportingAForeignRuleSetDoesNotRaiseStanding" in joined

    def test_the_module_reads_no_kernel_authority(self) -> None:
        source = (
            Path(__file__).resolve().parents[2]
            / "src"
            / "alghanem"
            / "arabic"
            / "phonetic_standing_closure.py"
        ).read_text(encoding="utf-8")
        imports = tuple(
            line
            for line in source.splitlines()
            if line.startswith(("import ", "from "))
        )
        assert imports
        assert not any("kernel" in line for line in imports)

    def test_no_kernel_module_reads_this_closure(self) -> None:
        for module in pkgutil.walk_packages(
            kernel_package.__path__, prefix="alghanem.kernel."
        ):
            spec = module.module_finder.find_spec(module.name)  # type: ignore[union-attr]
            assert spec is not None and spec.origin is not None
            text = Path(spec.origin).read_text(encoding="utf-8")
            assert "phonetic_standing_closure" not in text, module.name
            assert "PhoneticStanding" not in text, module.name
