"""Tests for the sixth AIM.1 milestone: the indicator binding aims to supports."""

from __future__ import annotations

import ast
import pkgutil
from dataclasses import fields, replace
from pathlib import Path

import pytest

import alghanem.arabic as arabic_package
import alghanem.encyclopedia as encyclopedia_package
import alghanem.kernel as kernel_package
from alghanem.program import (
    AIM_INDICATOR_AUTHORITY_NOTE,
    AIM_INDICATOR_DESIGN_SOURCE_CITATION_NOTE,
    AIM_INDICATOR_NAMED_RESIDUALS,
    AIM_RECORDS,
    CITATION_SUPPORT_IS_DECLARED_BY_THE_RECORD_NOT_BY_THE_CONSTITUTION,
    COUNT_IS_DERIVED_NOT_WRITTEN_NOTE,
    NO_DECLARED_SUPPORT_TOTAL_TO_CROSS_CHECK,
    SECTION_HEADING_CARRIES_NO_DECLARED_STATUS,
    SUPPORT_COUNT_IS_NOT_PROGRESS,
    THIRD_READER_IS_CITED_BY_NO_AIM,
    AimId,
    AimIndicatorError,
    AimIndicatorLedger,
    AimIndicatorRow,
    AimSupportStanding,
    AttainmentStanding,
    AuditQuestionStanding,
    CitationReferenceCensus,
    CitedSupportKind,
    DeclaredCitationFiller,
    DeclaredCitationShape,
    DeclaredLawStatus,
    DeclaredUnresolvableReference,
    DeferredValueSite,
    ReadCitationReference,
    constitution_document_path,
    load_aim_indicator_ledger,
    load_constitution_ledger,
    read_aim_indicator_row,
    repository_root_path,
)
from alghanem.program import aim_indicator as indicator_module
from alghanem.program.aims import DESIGN_SOURCE_OPEN_QUESTION

_ANSWER_MARKERS = (
    "answer",
    "verdict",
    "conclusion",
    "resolution",
    "decision",
    "outcome",
    "birth",
    "promotion",
    "indicator",
    "score",
    "percent",
    "estimate",
    "priority",
    "progress",
    "share",
    "ratio",
    "rank",
    "closeness",
    "attainment",
)

_INDICATOR_TYPES = (
    ReadCitationReference,
    CitationReferenceCensus,
    AimIndicatorRow,
    AimIndicatorLedger,
)


@pytest.fixture(scope="module")
def ledger() -> AimIndicatorLedger:
    return load_aim_indicator_ledger()


def law_reference(**overrides: object) -> ReadCitationReference:
    base: dict[str, object] = dict(
        aim_id=AimId.K2,
        shape=DeclaredCitationShape.ROW,
        reference_name="G0.BV.1",
        kind=CitedSupportKind.LAW_ROW,
        citation_offset=21,
        resolved_target="G0.BV.1",
        derived_status=DeclaredLawStatus.DECLARED_DEFERRED_CONTRACT_ONLY.value,
    )
    base.update(overrides)
    return ReadCitationReference(**base)  # type: ignore[arg-type]


def question_reference(**overrides: object) -> ReadCitationReference:
    base: dict[str, object] = dict(
        aim_id=AimId.T3,
        shape=DeclaredCitationShape.BACKTICKED_NAME,
        reference_name="ThirdTransmittedEvidenceModeNotDecided",
        kind=CitedSupportKind.AUDIT_QUESTION,
        citation_offset=23,
        resolved_target="ThirdTransmittedEvidenceModeNotDecided",
        derived_status="OPEN",
        question_standing=AuditQuestionStanding.OPEN,
    )
    base.update(overrides)
    return ReadCitationReference(**base)  # type: ignore[arg-type]


def excluded_reference(**overrides: object) -> ReadCitationReference:
    base: dict[str, object] = dict(
        aim_id=AimId.A1,
        shape=DeclaredCitationShape.ROW_GROUP,
        reference_name="G0",
        kind=CitedSupportKind.DECLARED_UNRESOLVABLE,
        citation_offset=31,
    )
    base.update(overrides)
    return ReadCitationReference(**base)  # type: ignore[arg-type]


# --- the record's own document is read, and every aim gets exactly one row ---


def test_ledger_carries_one_row_per_aim_in_record_order(
    ledger: AimIndicatorLedger,
) -> None:
    assert ledger.row_count == len(AIM_RECORDS)
    assert tuple(row.aim_id for row in ledger.rows) == tuple(AIM_RECORDS)


def test_every_aim_citation_yields_at_least_one_reference(
    ledger: AimIndicatorLedger,
) -> None:
    for row in ledger.rows:
        assert row.reference_count >= 1


def test_a_missing_aim_row_is_refused_not_read_as_absent_support(
    ledger: AimIndicatorLedger,
) -> None:
    with pytest.raises(AimIndicatorError):
        AimIndicatorLedger(rows=ledger.rows[1:])


def test_reordering_rows_is_refused_because_order_is_not_priority(
    ledger: AimIndicatorLedger,
) -> None:
    with pytest.raises(AimIndicatorError):
        AimIndicatorLedger(rows=tuple(reversed(ledger.rows)))


# --- resolution against the three readers' artefacts ---


def test_law_rows_resolve_by_identifier_and_by_full_name(
    ledger: AimIndicatorLedger,
) -> None:
    rows = ledger.rows_by_aim
    by_identifier = {
        reference.reference_name
        for reference in rows[AimId.K2].references_of_kind(CitedSupportKind.LAW_ROW)
    }
    by_name = {
        reference.reference_name
        for reference in rows[AimId.K1].references_of_kind(CitedSupportKind.LAW_ROW)
    }
    assert by_identifier == {"G0.BV.1", "G0.BV.1a"}
    assert by_name == {"Structural admission boundary", "No epistemic promotion"}


def test_audit_questions_resolve_and_keep_their_declared_status(
    ledger: AimIndicatorLedger,
) -> None:
    row = ledger.rows_by_aim[AimId.T1]
    questions = row.references_of_kind(CitedSupportKind.AUDIT_QUESTION)
    assert len(questions) == 3
    assert row.questions_without_declared_status_count == 2
    assert row.question_standing_counts[AuditQuestionStanding.OPEN] == 3
    assert row.question_standing_counts[AuditQuestionStanding.RESOLVED] == 0


def test_sections_and_paths_resolve_without_a_declared_status(
    ledger: AimIndicatorLedger,
) -> None:
    row = ledger.rows_by_aim[AimId.E2]
    sections = row.references_of_kind(CitedSupportKind.DOCUMENT_SECTION)
    assert [reference.reference_name for reference in sections] == [
        "Encyclopedia Self-Observation"
    ]
    for reference in sections:
        assert reference.derived_status == ""
    for reference in row.references_of_kind(CitedSupportKind.REPOSITORY_PATH):
        assert (repository_root_path() / reference.reference_name).exists()


def test_a_cited_path_that_does_not_exist_is_refused() -> None:
    record = replace(
        AIM_RECORDS[AimId.A1], citation="src/alghanem/arabic/no_such_module.py"
    )
    with pytest.raises(AimIndicatorError, match="مسارًا لا وجود له"):
        read_aim_indicator_row(
            record=record,
            ledger=load_constitution_ledger(),
            document_text=constitution_document_path().read_text(encoding="utf-8"),
            repository_root=repository_root_path(),
        )


def test_a_cited_law_row_that_does_not_exist_is_refused_by_aim_and_offset() -> None:
    record = replace(AIM_RECORDS[AimId.K2], citation="صفّ G0.ZZ.9")
    with pytest.raises(AimIndicatorError, match="AIM-K2"):
        read_aim_indicator_row(
            record=record,
            ledger=load_constitution_ledger(),
            document_text=constitution_document_path().read_text(encoding="utf-8"),
            repository_root=repository_root_path(),
        )


def test_a_cited_section_that_has_no_heading_is_refused() -> None:
    record = replace(AIM_RECORDS[AimId.E2], citation="قسم «No Such Section»")
    with pytest.raises(AimIndicatorError, match="قسمًا لا عنوانَ له"):
        read_aim_indicator_row(
            record=record,
            ledger=load_constitution_ledger(),
            document_text=constitution_document_path().read_text(encoding="utf-8"),
            repository_root=repository_root_path(),
        )


# --- refusal, not silent skipping, raised to the citation reference ---


def test_uncovered_citation_text_is_refused_not_skipped() -> None:
    record = replace(AIM_RECORDS[AimId.T3], citation="صفّ G0.BV.1 ثم شيءٌ لم يُقرَأ")
    with pytest.raises(AimIndicatorError, match="نصٌّ غير مقروءٍ في الاستشهاد"):
        read_aim_indicator_row(
            record=record,
            ledger=load_constitution_ledger(),
            document_text=constitution_document_path().read_text(encoding="utf-8"),
            repository_root=repository_root_path(),
        )


def test_excluded_references_are_counted_not_dropped(
    ledger: AimIndicatorLedger,
) -> None:
    excluded = ledger.census.excluded_references
    assert {reference.reference_name for reference in excluded} == {
        member.reference_name for member in DeclaredUnresolvableReference
    }
    for reference in excluded:
        assert not reference.is_resolved
        assert reference.resolved_target == ""


def test_census_counts_every_member_of_every_vocabulary_even_at_zero(
    ledger: AimIndicatorLedger,
) -> None:
    census = ledger.census
    assert set(census.kind_counts) == set(CitedSupportKind)
    assert set(census.shape_counts) == set(DeclaredCitationShape)
    assert census.reference_count == sum(census.kind_counts.values())
    assert census.reference_count == sum(row.reference_count for row in ledger.rows)


def test_every_row_counts_every_law_status_and_question_standing(
    ledger: AimIndicatorLedger,
) -> None:
    for row in ledger.rows:
        assert set(row.law_status_counts) == set(DeclaredLawStatus)
        assert set(row.question_standing_counts) == set(AuditQuestionStanding)
        assert sum(row.law_status_counts.values()) == len(
            row.references_of_kind(CitedSupportKind.LAW_ROW)
        )


def test_declared_filler_is_stripped_longest_first(
    ledger: AimIndicatorLedger,
) -> None:
    lengths = [len(filler.value) for filler in indicator_module._FILLERS_LONGEST_FIRST]
    assert lengths == sorted(lengths, reverse=True)
    assert set(indicator_module._FILLERS_LONGEST_FIRST) == set(DeclaredCitationFiller)


# --- the declared status parenthetical is matched against derived statuses ---


def test_declared_status_matches_at_least_one_derived_support(
    ledger: AimIndicatorLedger,
) -> None:
    declaring = [row for row in ledger.rows if row.status_is_declared_in_citation]
    assert {row.aim_id for row in declaring} == {AimId.K1, AimId.A2, AimId.T2, AimId.T3}
    for row in declaring:
        assert row.declared_status_in_citation in {
            reference.derived_status
            for reference in row.references
            if reference.derived_status
        }


def test_a_declared_status_matching_no_support_is_refused() -> None:
    references = (law_reference(),)
    with pytest.raises(AimIndicatorError, match="لا تُطابق أيّ"):
        AimIndicatorRow(
            aim_id=AimId.K2,
            references=references,
            declared_status_in_citation="ENFORCED",
        )


def test_a_declared_status_need_not_match_every_support(
    ledger: AimIndicatorLedger,
) -> None:
    row = ledger.rows_by_aim[AimId.K1]
    statuses = {
        reference.derived_status
        for reference in row.references_of_kind(CitedSupportKind.LAW_ROW)
    }
    assert row.declared_status_in_citation == "DECLARED_DEFERRED"
    assert statuses == {"DECLARED_DEFERRED", "ENFORCED"}


# --- support standing describes homogeneity, never distance to attainment ---


def test_support_standing_reads_status_homogeneity(ledger: AimIndicatorLedger) -> None:
    rows = ledger.rows_by_aim
    assert rows[AimId.K1].support_standing is (
        AimSupportStanding.DIFFERENT_DECLARED_STATUSES
    )
    assert rows[AimId.A2].support_standing is AimSupportStanding.ONE_DECLARED_STATUS
    assert rows[AimId.E2].support_standing is (
        AimSupportStanding.NO_STATUS_BEARING_SUPPORT
    )


def test_no_status_bearing_support_is_not_no_support(
    ledger: AimIndicatorLedger,
) -> None:
    row = ledger.rows_by_aim[AimId.E2]
    assert row.support_standing is AimSupportStanding.NO_STATUS_BEARING_SUPPORT
    assert row.resolved_support_count >= 1


def test_standing_counts_cover_every_member(ledger: AimIndicatorLedger) -> None:
    counts = ledger.support_standing_counts
    assert set(counts) == set(AimSupportStanding)
    assert sum(counts.values()) == ledger.row_count


# --- the third reader of section 4 is reached by no citation, derived not assumed ---


def test_no_aim_citation_names_a_deferred_value_site(
    ledger: AimIndicatorLedger,
) -> None:
    assert {site.member_name for site in DeferredValueSite}
    assert all(row.deferred_value_site_count == 0 for row in ledger.rows)
    assert THIRD_READER_IS_CITED_BY_NO_AIM in AIM_INDICATOR_NAMED_RESIDUALS


# --- no written answer, no attainment, no ranking ---


def test_no_indicator_type_carries_an_answer_or_ranking_field() -> None:
    for declaring_type in _INDICATOR_TYPES:
        for item in fields(declaring_type):
            assert not any(marker in item.name for marker in _ANSWER_MARKERS)


def test_no_count_is_a_field_and_every_count_is_a_property() -> None:
    for declaring_type in _INDICATOR_TYPES:
        for item in fields(declaring_type):
            assert "count" not in item.name
    assert isinstance(AimIndicatorRow.reference_count, property)
    assert isinstance(AimIndicatorLedger.row_count, property)
    assert isinstance(CitationReferenceCensus.reference_count, property)


def test_the_module_never_writes_an_attainment_standing() -> None:
    source = Path(indicator_module.__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)
    written = {
        node.attr
        for node in ast.walk(tree)
        if isinstance(node, ast.Attribute)
        and isinstance(node.value, ast.Name)
        and node.value.id == "AttainmentStanding"
    }
    assert written == set()
    assert "AttainmentStanding" not in {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
        for alias in node.names
    }
    assert AttainmentStanding.REACHED.value


def test_the_ledger_issues_no_verdict_freeze_or_birth() -> None:
    source = Path(indicator_module.__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported = {
        node.module
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    }
    assert not any(module.startswith("alghanem.kernel") for module in imported)
    assert not any(module.startswith("alghanem.arabic") for module in imported)


# --- authority inertness across the tree ---


def test_no_kernel_arabic_or_encyclopedia_module_imports_the_programme_layer() -> None:
    for package in (kernel_package, arabic_package, encyclopedia_package):
        for module_info in pkgutil.walk_packages(
            package.__path__, prefix=f"{package.__name__}."
        ):
            path = Path(
                str(module_info.module_finder.path),  # type: ignore[union-attr]
                f"{module_info.name.rsplit('.', 1)[-1]}.py",
            )
            if not path.exists():
                continue
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom) and node.module is not None:
                    assert "alghanem.program" not in node.module
                    assert "program" not in node.module.split(".")
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        assert "alghanem.program" not in alias.name


# --- named residuals and the cited design source ---


def test_named_residuals_are_recorded_in_code_not_prose_alone() -> None:
    assert set(AIM_INDICATOR_NAMED_RESIDUALS) == {
        CITATION_SUPPORT_IS_DECLARED_BY_THE_RECORD_NOT_BY_THE_CONSTITUTION,
        SUPPORT_COUNT_IS_NOT_PROGRESS,
        NO_DECLARED_SUPPORT_TOTAL_TO_CROSS_CHECK,
        THIRD_READER_IS_CITED_BY_NO_AIM,
        SECTION_HEADING_CARRIES_NO_DECLARED_STATUS,
    }
    for reason in AIM_INDICATOR_NAMED_RESIDUALS.values():
        assert reason.strip()


def test_the_design_source_open_question_is_cited_not_rederived() -> None:
    assert DESIGN_SOURCE_OPEN_QUESTION in AIM_INDICATOR_DESIGN_SOURCE_CITATION_NOTE
    assert AIM_INDICATOR_AUTHORITY_NOTE.strip()
    assert COUNT_IS_DERIVED_NOT_WRITTEN_NOTE.strip()


# --- reference construction laws ---


def test_an_excluded_reference_may_not_carry_a_resolved_target() -> None:
    with pytest.raises(AimIndicatorError):
        excluded_reference(resolved_target="G0.BV.1")


def test_a_resolved_support_must_name_its_target() -> None:
    with pytest.raises(AimIndicatorError):
        law_reference(resolved_target="")


def test_only_law_rows_and_questions_carry_a_derived_status() -> None:
    with pytest.raises(AimIndicatorError):
        ReadCitationReference(
            aim_id=AimId.E2,
            shape=DeclaredCitationShape.SECTION,
            reference_name="Encyclopedia Self-Observation",
            kind=CitedSupportKind.DOCUMENT_SECTION,
            citation_offset=3,
            resolved_target="Encyclopedia Self-Observation",
            derived_status="ENFORCED",
        )


def test_only_audit_questions_carry_a_standing() -> None:
    with pytest.raises(AimIndicatorError):
        law_reference(question_standing=AuditQuestionStanding.OPEN)
    with pytest.raises(AimIndicatorError):
        question_reference(question_standing=None)


def test_a_reference_from_another_aim_is_not_counted_for_this_one() -> None:
    with pytest.raises(AimIndicatorError, match="غايةٍ أخرى"):
        AimIndicatorRow(aim_id=AimId.K3, references=(law_reference(),))


def test_references_keep_the_order_of_their_citation() -> None:
    with pytest.raises(AimIndicatorError, match="ترتيب الإشارات"):
        AimIndicatorRow(
            aim_id=AimId.K2,
            references=(
                law_reference(citation_offset=40),
                law_reference(reference_name="G0.BV.1a", citation_offset=10),
            ),
        )


def test_an_empty_row_is_refused_as_a_claim_of_absence() -> None:
    with pytest.raises(AimIndicatorError, match="بلا إشارةٍ مقروءة"):
        AimIndicatorRow(aim_id=AimId.K2, references=())
