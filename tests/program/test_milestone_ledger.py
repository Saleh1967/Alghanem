"""Tests for the seventh AIM.1 milestone: milestone sections mapped to modules."""

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
    BOTH_DECLARATIONS_ARE_PROSE_NOT_TREE_DERIVED,
    FIRST_MILESTONE_NAMES_ITS_MODULE_IN_THE_PREAMBLE,
    INCIDENT_SECTIONS_CARRY_NO_MODULE_CLAIM,
    MILESTONE_LEDGER_AUTHORITY_NOTE,
    MILESTONE_LEDGER_DESIGN_SOURCE_CITATION_NOTE,
    MILESTONE_LEDGER_NAMED_RESIDUALS,
    MODULE_EXISTENCE_IS_NOT_MODULE_AUTHORSHIP,
    NO_INDICATOR_IN_THIS_LEDGER_NOTE,
    PROGRAMME_PACKAGE_RELATIVE_PATH,
    REOPENING_IS_DERIVED_BUT_ITS_REASON_IS_NOT,
    DeclaredModuleReference,
    DeclaredModuleShape,
    HeaderMilestoneDeclaration,
    MilestoneLedger,
    MilestoneLedgerError,
    MilestoneOrdinal,
    MilestoneRow,
    ModuleClaimStanding,
    ModuleNamingSite,
    ReadSeventhSection,
    SectionCensus,
    SeventhSectionKind,
    correspond_milestones_to_tree,
    programme_module_paths,
    read_milestone_ledger,
)
from alghanem.program import milestone_ledger as ledger_module
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

_LEDGER_TYPES = (
    DeclaredModuleReference,
    ReadSeventhSection,
    HeaderMilestoneDeclaration,
    SectionCensus,
    MilestoneRow,
    MilestoneLedger,
)


@pytest.fixture(scope="module")
def ledger() -> MilestoneLedger:
    return correspond_milestones_to_tree()


@pytest.fixture(scope="module")
def document_text() -> str:
    return ledger_module.aims_document_path().read_text(encoding="utf-8")


def module_reference(**overrides: object) -> DeclaredModuleReference:
    base: dict[str, object] = dict(
        token="src/alghanem/program/aims.py",
        shape=DeclaredModuleShape.FULL_PATH,
        document_line=10,
    )
    base.update(overrides)
    return DeclaredModuleReference(**base)  # type: ignore[arg-type]


def milestone_section(**overrides: object) -> ReadSeventhSection:
    base: dict[str, object] = dict(
        kind=SeventhSectionKind.MILESTONE_REVELATION,
        ordinal=MilestoneOrdinal.FIRST,
        heading="ما كشفته المرحلة الأولى (السجلّ وحده)",
        document_line=280,
        module=module_reference(),
        naming_site=ModuleNamingSite.NAMED_IN_SECTION_PREAMBLE,
    )
    base.update(overrides)
    return ReadSeventhSection(**base)  # type: ignore[arg-type]


def milestone_row(**overrides: object) -> MilestoneRow:
    base: dict[str, object] = dict(
        ordinal=MilestoneOrdinal.FIRST,
        relative_path="src/alghanem/program/aims.py",
        header_shape=DeclaredModuleShape.FULL_PATH,
        section_shape=DeclaredModuleShape.FULL_PATH,
        naming_site=ModuleNamingSite.NAMED_IN_SECTION_PREAMBLE,
        claim_standing=ModuleClaimStanding.FIRST_CODED_HERE,
        section_line=280,
    )
    base.update(overrides)
    return MilestoneRow(**base)  # type: ignore[arg-type]


# --- the document's own two declarations are read and corresponded ---


def test_every_declared_milestone_has_one_row_in_declaration_order(
    ledger: MilestoneLedger,
) -> None:
    ordinals = tuple(row.ordinal for row in ledger.rows)
    assert ordinals == tuple(MilestoneOrdinal)[: ledger.milestone_count]
    assert ledger.milestone_count == len(ledger.rows)


def test_the_seventh_milestone_claims_this_very_module(ledger: MilestoneLedger) -> None:
    row = ledger.row(MilestoneOrdinal.SEVENTH)
    assert row.relative_path == f"{PROGRAMME_PACKAGE_RELATIVE_PATH}/milestone_ledger.py"
    assert row.claim_standing is ModuleClaimStanding.FIRST_CODED_HERE


def test_every_claimed_module_exists_in_the_tree(ledger: MilestoneLedger) -> None:
    root = ledger_module.repository_root_path()
    for claimed in ledger.claimed_modules:
        assert (root / claimed).is_file()


def test_no_programme_module_is_left_unclaimed_by_a_milestone(
    ledger: MilestoneLedger,
) -> None:
    assert set(programme_module_paths()) == set(ledger.claimed_modules)


# --- the fifth milestone reopened the second's module, and that is not a duplicate ---


def test_the_reopened_module_is_derived_and_named_not_refused(
    ledger: MilestoneLedger,
) -> None:
    reopened = ledger.reopened_modules
    assert set(reopened) == {
        f"{PROGRAMME_PACKAGE_RELATIVE_PATH}/constitution_ledger.py"
    }
    assert reopened[f"{PROGRAMME_PACKAGE_RELATIVE_PATH}/constitution_ledger.py"] == (
        MilestoneOrdinal.SECOND,
        MilestoneOrdinal.FIFTH,
    )
    assert (
        ledger.row(MilestoneOrdinal.FIFTH).claim_standing
        is ModuleClaimStanding.REOPENED_BY_THIS_MILESTONE
    )
    assert (
        ledger.row(MilestoneOrdinal.SECOND).claim_standing
        is ModuleClaimStanding.FIRST_CODED_HERE
    )


def test_a_reopening_claimed_before_its_first_claimant_is_refused() -> None:
    with pytest.raises(MilestoneLedgerError, match="لم تُطالِب بها"):
        MilestoneLedger(
            rows=(
                milestone_row(
                    claim_standing=ModuleClaimStanding.REOPENED_BY_THIS_MILESTONE
                ),
            ),
            census=SectionCensus(sections=(milestone_section(),)),
        )


def test_a_second_claim_that_is_not_marked_as_a_reopening_is_refused() -> None:
    with pytest.raises(MilestoneLedgerError, match="ليست إعادةَ فتح"):
        MilestoneLedger(
            rows=(
                milestone_row(),
                milestone_row(ordinal=MilestoneOrdinal.SECOND, section_line=300),
            ),
            census=SectionCensus(sections=(milestone_section(),)),
        )


# --- the double landing is refused by structure, not caught by reading ---


def test_two_sections_for_one_milestone_are_refused(document_text: str) -> None:
    duplicated = document_text + (
        "\n### ما كشفته المرحلة السادسة (صيغةٌ ثانية)\n\n"
        "المرحلة السادسة قامت في `src/alghanem/program/aim_indicator.py`.\n"
    )
    with pytest.raises(MilestoneLedgerError, match="قسمان للمرحلة"):
        read_milestone_ledger(duplicated)


def test_a_duplicate_ordinal_row_is_refused() -> None:
    with pytest.raises(MilestoneLedgerError, match="مرحلةٌ مكرّرة"):
        MilestoneLedger(
            rows=(milestone_row(), milestone_row(section_line=300)),
            census=SectionCensus(sections=(milestone_section(),)),
        )


def test_rows_out_of_declaration_order_are_refused() -> None:
    with pytest.raises(MilestoneLedgerError, match="ترتيب الصفوف"):
        MilestoneLedger(
            rows=(
                milestone_row(ordinal=MilestoneOrdinal.SECOND),
                milestone_row(ordinal=MilestoneOrdinal.FIRST, section_line=300),
            ),
            census=SectionCensus(sections=(milestone_section(),)),
        )


def test_a_gap_in_the_milestone_sequence_is_refused() -> None:
    with pytest.raises(MilestoneLedgerError, match="تعاقبُ المراحل منقطع"):
        MilestoneLedger(
            rows=(milestone_row(ordinal=MilestoneOrdinal.SECOND),),
            census=SectionCensus(sections=(milestone_section(),)),
        )


# --- unknown headings stop the reading instead of being skipped ---


def test_an_unknown_subsection_heading_is_refused(document_text: str) -> None:
    altered = document_text + "\n### ملاحظةٌ عابرة\n\nنصٌّ.\n"
    with pytest.raises(MilestoneLedgerError, match="عنوانٌ فرعيّ خارج المفردة"):
        read_milestone_ledger(altered)


def test_an_unknown_ordinal_in_a_known_heading_is_refused(document_text: str) -> None:
    altered = document_text + (
        "\n### ما كشفته المرحلة العاشرة (لا رتبةَ لها)\n\n"
        "قامت في `src/alghanem/program/aims.py`.\n"
    )
    with pytest.raises(MilestoneLedgerError, match="رتبةُ مرحلةٍ خارج المفردة"):
        read_milestone_ledger(altered)


def test_a_section_naming_no_module_anywhere_is_refused() -> None:
    with pytest.raises(MilestoneLedgerError, match="بلا وحدةٍ مُسمّاة"):
        milestone_section(module=None, naming_site=None)


# --- the incident section is counted, and claims no module ---


def test_the_recorded_incident_is_counted_but_claims_no_module(
    ledger: MilestoneLedger,
) -> None:
    incidents = ledger.census.sections_of_kind(SeventhSectionKind.RECORDED_INCIDENT)
    assert ledger.incident_count == len(incidents) == 1
    for section in incidents:
        assert section.module is None
        assert section.naming_site is None
        assert section.ordinal is MilestoneOrdinal.SIXTH
    assert ledger.census.section_count == ledger.milestone_count + ledger.incident_count


def test_an_incident_that_claims_a_module_is_refused() -> None:
    with pytest.raises(MilestoneLedgerError, match="قسمُ واقعةٍ يُطالِب بوحدة"):
        milestone_section(
            kind=SeventhSectionKind.RECORDED_INCIDENT,
            ordinal=MilestoneOrdinal.SIXTH,
            heading="ما كشفه الهبوط المزدوج للمرحلة السادسة (تسجيلٌ لا طيّ)",
        )


def test_an_incident_for_a_milestone_without_a_section_is_refused(
    document_text: str,
) -> None:
    altered = document_text + (
        "\n### ما كشفه الهبوط المزدوج للمرحلة الثالثة (واقعةٌ مُختلَقة)\n\nنصٌّ.\n"
    )
    read_milestone_ledger(altered)
    stripped = document_text.replace(
        "### ما كشفته المرحلة السابعة (مقابلةُ المراحل بوحداتها)",
        "### ما كشفه الهبوط المزدوج للمرحلة السابعة (واقعةٌ بلا مرحلة)",
    )
    with pytest.raises(MilestoneLedgerError):
        read_milestone_ledger(stripped)


# --- the two declarations are corresponded, and neither outranks the other ---


def test_the_header_and_section_seven_must_name_the_same_module(
    document_text: str,
) -> None:
    altered = document_text.replace(
        "المرحلة السادسة قامت في `src/alghanem/program/aim_indicator.py`",
        "المرحلة السادسة قامت في `src/alghanem/program/aims.py`",
    )
    with pytest.raises(MilestoneLedgerError, match="الترويسة تُسمّي"):
        read_milestone_ledger(altered)


def test_a_header_milestone_without_a_section_is_refused(document_text: str) -> None:
    altered = document_text.replace(
        "### ما كشفته المرحلة السابعة (مقابلةُ المراحل بوحداتها)",
        "### ما كشفته المرحلة السادسة (عنوانٌ مُبدَل)",
    )
    with pytest.raises(MilestoneLedgerError):
        read_milestone_ledger(altered)


def test_the_first_milestone_is_named_in_the_preamble_not_in_its_body(
    ledger: MilestoneLedger,
) -> None:
    assert (
        ledger.row(MilestoneOrdinal.FIRST).naming_site
        is ModuleNamingSite.NAMED_IN_SECTION_PREAMBLE
    )
    for ordinal in tuple(MilestoneOrdinal)[1 : ledger.milestone_count]:
        assert ledger.row(ordinal).naming_site is ModuleNamingSite.NAMED_IN_SECTION_BODY


# --- the two naming shapes are kept apart, and their disagreement is not a refusal ---


def test_the_bare_filename_shape_resolves_inside_the_programme_layer(
    ledger: MilestoneLedger,
) -> None:
    fifth = ledger.row(MilestoneOrdinal.FIFTH)
    assert fifth.header_shape is DeclaredModuleShape.BARE_FILENAME
    assert fifth.relative_path.startswith(f"{PROGRAMME_PACKAGE_RELATIVE_PATH}/")
    assert all(row.shapes_agree for row in ledger.rows)


def test_a_shape_that_disagrees_with_its_own_text_is_refused() -> None:
    with pytest.raises(MilestoneLedgerError, match="شكلٌ مُعلَنٌ يخالف نصَّه"):
        module_reference(shape=DeclaredModuleShape.BARE_FILENAME)


def test_a_bare_filename_is_resolved_under_the_programme_package() -> None:
    bare = module_reference(
        token="constitution_ledger.py", shape=DeclaredModuleShape.BARE_FILENAME
    )
    assert bare.relative_path == (
        f"{PROGRAMME_PACKAGE_RELATIVE_PATH}/constitution_ledger.py"
    )


# --- a claimed module missing from the tree, and a module missing its claim ---


def test_a_module_named_but_absent_from_the_tree_is_refused(tmp_path: Path) -> None:
    with pytest.raises(MilestoneLedgerError, match="لا وجود لها في الشجرة"):
        correspond_milestones_to_tree(root=tmp_path)


def test_an_unclaimed_programme_module_is_refused(tmp_path: Path) -> None:
    root = ledger_module.repository_root_path()
    package = tmp_path / PROGRAMME_PACKAGE_RELATIVE_PATH
    package.mkdir(parents=True)
    for claimed in programme_module_paths(root):
        (tmp_path / claimed).write_text("", encoding="utf-8")
    (package / "unclaimed_reader.py").write_text("", encoding="utf-8")
    with pytest.raises(MilestoneLedgerError, match="لا تُطالِب بها مرحلة"):
        correspond_milestones_to_tree(root=tmp_path)


def test_a_missing_programme_package_is_refused_not_read_as_empty(
    tmp_path: Path,
) -> None:
    with pytest.raises(MilestoneLedgerError, match="غير موجودة"):
        programme_module_paths(tmp_path)


def test_a_missing_document_is_refused_not_read_as_no_milestones(
    tmp_path: Path,
) -> None:
    with pytest.raises(MilestoneLedgerError, match="تعذّرت قراءة"):
        correspond_milestones_to_tree(path=tmp_path / "absent.md")


# --- no written counts, no verdict, no attainment ---


def test_no_dataclass_here_writes_a_count_or_an_answer() -> None:
    for declared in _LEDGER_TYPES:
        for item in fields(declared):
            assert "count" not in item.name
            for marker in _ANSWER_MARKERS:
                assert marker not in item.name
    assert isinstance(MilestoneLedger.milestone_count, property)
    assert isinstance(MilestoneLedger.incident_count, property)
    assert isinstance(SectionCensus.section_count, property)


def test_the_module_imports_no_aim_identity_and_no_sibling_reader() -> None:
    tree = ast.parse(Path(ledger_module.__file__).read_text(encoding="utf-8"))
    imported = {
        (node.module, alias.name)
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
        for alias in node.names
    }
    assert ("aims", "DESIGN_SOURCE_OPEN_QUESTION") in {
        (module, name) for module, name in imported if module is not None
    }
    assert not any(name == "AimId" for _module, name in imported)
    for forbidden in (
        "constitution_ledger",
        "deferred_value_ledger",
        "aims_document_ledger",
        "aim_indicator",
    ):
        assert not any(
            module is not None and forbidden in module for module, _name in imported
        )


def test_the_ledger_issues_no_verdict_freeze_or_birth() -> None:
    tree = ast.parse(Path(ledger_module.__file__).read_text(encoding="utf-8"))
    imported = {
        node.module
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module is not None
    }
    assert not any(module.startswith("alghanem.kernel") for module in imported)
    assert not any(module.startswith("alghanem.arabic") for module in imported)
    assert not any(module.startswith("alghanem.encyclopedia") for module in imported)


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
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        assert "alghanem.program" not in alias.name


# --- named residuals and the cited design source ---


def test_named_residuals_are_recorded_in_code_not_prose_alone() -> None:
    assert set(MILESTONE_LEDGER_NAMED_RESIDUALS) == {
        MODULE_EXISTENCE_IS_NOT_MODULE_AUTHORSHIP,
        BOTH_DECLARATIONS_ARE_PROSE_NOT_TREE_DERIVED,
        FIRST_MILESTONE_NAMES_ITS_MODULE_IN_THE_PREAMBLE,
        REOPENING_IS_DERIVED_BUT_ITS_REASON_IS_NOT,
        INCIDENT_SECTIONS_CARRY_NO_MODULE_CLAIM,
    }
    for reason in MILESTONE_LEDGER_NAMED_RESIDUALS.values():
        assert reason.strip()


def test_the_design_source_open_question_is_cited_not_rederived() -> None:
    assert DESIGN_SOURCE_OPEN_QUESTION in MILESTONE_LEDGER_DESIGN_SOURCE_CITATION_NOTE
    assert MILESTONE_LEDGER_AUTHORITY_NOTE.strip()
    assert NO_INDICATOR_IN_THIS_LEDGER_NOTE.strip()


def test_rows_and_sections_are_frozen_against_quiet_mutation(
    ledger: MilestoneLedger,
) -> None:
    row = ledger.rows[0]
    with pytest.raises(MilestoneLedgerError):
        replace(row, relative_path="")
    with pytest.raises(AttributeError):
        row.relative_path = "other"  # type: ignore[misc]


def test_a_row_for_an_ordinal_without_one_is_refused(ledger: MilestoneLedger) -> None:
    with pytest.raises(MilestoneLedgerError):
        ledger.row("السابعة")  # type: ignore[arg-type]
