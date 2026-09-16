"""Tests for the fifteenth AIM.1 milestone: announced achievements, derived."""

from __future__ import annotations

import ast
import pkgutil
from dataclasses import FrozenInstanceError, fields, replace
from pathlib import Path

import pytest

import alghanem.arabic as arabic_package
import alghanem.encyclopedia as encyclopedia_package
import alghanem.kernel as kernel_package
from alghanem.program import (
    ACHIEVEMENT_LEDGER_AUTHORITY_NOTE,
    ACHIEVEMENT_LEDGER_DESIGN_SOURCE_CITATION_NOTE,
    ACHIEVEMENT_LEDGER_NAMED_RESIDUALS,
    CLAIM_SHAPE_IS_A_FORM_NOT_A_MEANING,
    CLAIMED_MODULE_MUST_IMPORT_NOTE,
    CONSTITUTION_DOCUMENT_RELATIVE_PATH,
    EXAMPLE_SCRIPT_REFERENCE_IS_NOT_EXECUTION,
    EXAMPLES_RELATIVE_PATH,
    NO_INDICATOR_IN_THIS_ACHIEVEMENT_LEDGER_NOTE,
    README_ONLY_GATE_IS_RECORDED_NOT_REFUSED,
    README_RELATIVE_PATH,
    SYMBOL_PRESENCE_IS_NOT_SYMBOL_AUTHORSHIP,
    TESTS_RELATIVE_PATH,
    WITNESS_COLLECTS_IS_NOT_WITNESS_CHECKS_THIS,
    AchievementLedger,
    AchievementLedgerError,
    AchievementRow,
    ConstitutionNamingSite,
    ExampleScriptRow,
    ExampleScriptStanding,
    GateCorrespondenceRow,
    GateCorrespondenceStanding,
    ReadmeAchievementClaim,
    SkipGenus,
    SkippedWitnessRow,
    WitnessStanding,
    census_example_scripts,
    census_skipped_witnesses,
    correspond_achievements_to_tree,
    correspond_gates,
    derive_resident_symbols,
    derive_witness_standing,
    read_constitution_heading_gates,
    read_gate_mentions,
    read_readme_claims,
)
from alghanem.program import achievement_ledger as ledger_module
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
    "attainment",
)

_LEDGER_TYPES = (
    ReadmeAchievementClaim,
    AchievementRow,
    GateCorrespondenceRow,
    ExampleScriptRow,
    SkippedWitnessRow,
    AchievementLedger,
)

# The two skip forms are written by concatenation so that fixtures inside this
# file are not themselves read as skip constructs by the census under test.
_CONDITIONAL_SKIP_SOURCE = "@pytest.mark." + "skipif(condition)"
_INLINE_SKIP_SOURCE = "    pytest." + "skip('no case here')"
_UNKNOWN_SKIP_SOURCE = "@pytest.mark." + "skipwhenever(condition)"


def repository_root() -> Path:
    return Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def readme_text() -> str:
    return (repository_root() / README_RELATIVE_PATH).read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def constitution_text() -> str:
    return (repository_root() / CONSTITUTION_DOCUMENT_RELATIVE_PATH).read_text(
        encoding="utf-8"
    )


@pytest.fixture(scope="module")
def ledger() -> AchievementLedger:
    return correspond_achievements_to_tree()


def claim(
    *,
    gate_id: str = "G0.IC.1a",
    relative_path: str = "src/alghanem/kernel/independent_closure.py",
    document_line: int = 87,
    declared_symbols: tuple[str, ...] = ("ClosureScopeRegistry",),
) -> ReadmeAchievementClaim:
    return ReadmeAchievementClaim(
        gate_id=gate_id,
        relative_path=relative_path,
        document_line=document_line,
        declared_symbols=declared_symbols,
    )


# --- the claim is read by one written shape, never by estimated meaning ---


def test_every_claim_read_from_the_readme_names_an_existing_module(
    readme_text: str,
) -> None:
    claims = read_readme_claims(readme_text)
    assert claims
    root = repository_root()
    for read in claims:
        assert (root / read.relative_path).is_file()
        assert read.relative_path.startswith("src/alghanem/")


def test_claims_are_ordered_by_their_position_in_the_readme(
    readme_text: str,
) -> None:
    lines = [read.document_line for read in read_readme_claims(readme_text)]
    assert lines == sorted(lines)
    assert len(set(lines)) == len(lines)


def test_a_path_separated_from_its_gate_by_another_gate_is_not_its_claim() -> None:
    document = (
        "G0.AA.1 introduces a thing. G0.BB.1 does something else\n"
        "(`src/alghanem/kernel/transition.py`).\n"
    )
    claims = read_readme_claims(document)
    assert [read.gate_id for read in claims] == ["G0.BB.1"]


def test_a_path_reached_only_through_a_code_span_is_a_mention_not_a_claim() -> None:
    document = (
        "G0.AA.1 declares law only, and a `SurfaceAtomIntervention` runtime\n"
        "does exist (`src/alghanem/kernel/transition.py`).\n"
    )
    with pytest.raises(AchievementLedgerError, match="لم تُقرَأ أيّ مطالبة"):
        read_readme_claims(document)


def test_a_gate_shaped_token_inside_a_code_span_announces_nothing() -> None:
    document = (
        "The markers `PageV05P240…P245` bound the material, and\n"
        "G0.AA.1 (`src/alghanem/kernel/transition.py`) is the only claim.\n"
    )
    claims = read_readme_claims(document)
    assert [read.gate_id for read in claims] == ["G0.AA.1"]
    assert "P245" not in read_gate_mentions(document)


def test_the_claim_shape_limit_is_named_not_folded() -> None:
    assert CLAIM_SHAPE_IS_A_FORM_NOT_A_MEANING in ACHIEVEMENT_LEDGER_NAMED_RESIDUALS


def test_an_empty_readme_is_refused_not_read_as_no_achievements() -> None:
    with pytest.raises(AchievementLedgerError, match="نصٌّ غير فارغ"):
        read_readme_claims("   ")


def test_a_readme_without_a_single_claim_is_refused() -> None:
    with pytest.raises(AchievementLedgerError, match="لم تُقرَأ أيّ مطالبة"):
        read_readme_claims("prose with no gate identifier at all\n")


# --- the module is imported, not string-matched ---


def test_every_claimed_module_carries_at_least_one_symbol_the_prose_named(
    ledger: AchievementLedger,
) -> None:
    for row in ledger.rows:
        assert row.resident_symbols
        assert set(row.resident_symbols) <= set(row.claim.declared_symbols)


def test_a_claimed_module_outside_the_source_tree_is_refused() -> None:
    with pytest.raises(AchievementLedgerError, match="خارج شجرة المصدر"):
        claim(relative_path="docs/CONSTITUTION.py")


def test_a_claimed_path_without_a_python_suffix_is_refused() -> None:
    with pytest.raises(AchievementLedgerError, match="بلا لاحقةٍ بايثونية"):
        claim(relative_path="src/alghanem/kernel/transition")


def test_a_claimed_module_that_does_not_import_is_refused_not_matched() -> None:
    absent = claim(relative_path="src/alghanem/kernel/no_such_module.py")
    with pytest.raises(AchievementLedgerError, match="لا تُستورَد"):
        derive_resident_symbols(absent)


def test_a_claim_naming_no_resident_symbol_is_refused_at_construction() -> None:
    with pytest.raises(AchievementLedgerError, match="بلا رمزٍ قائم"):
        AchievementRow(
            claim=claim(declared_symbols=("NotASymbolInThatModule",)),
            resident_symbols=(),
            witness_relative_path="tests/kernel/test_independent_closure.py",
            witness_standing=WitnessStanding.WITNESS_DERIVED_AND_PRESENT,
        )


def test_a_resident_symbol_the_claim_never_named_is_refused() -> None:
    with pytest.raises(AchievementLedgerError, match="لم تُسمّه المطالبة"):
        AchievementRow(
            claim=claim(),
            resident_symbols=("ClosureScopeRegistry", "SomethingElse"),
            witness_relative_path="tests/kernel/test_independent_closure.py",
            witness_standing=WitnessStanding.WITNESS_DERIVED_AND_PRESENT,
        )


def test_symbols_the_prose_named_from_elsewhere_are_derived_not_dropped() -> None:
    row = AchievementRow(
        claim=claim(declared_symbols=("ClosureScopeRegistry", "ForeignName")),
        resident_symbols=("ClosureScopeRegistry",),
        witness_relative_path="tests/kernel/test_independent_closure.py",
        witness_standing=WitnessStanding.WITNESS_DERIVED_AND_PRESENT,
    )
    assert row.foreign_symbols == ("ForeignName",)


def test_symbol_presence_is_not_symbol_authorship_and_is_named() -> None:
    residuals = ACHIEVEMENT_LEDGER_NAMED_RESIDUALS
    assert SYMBOL_PRESENCE_IS_NOT_SYMBOL_AUTHORSHIP in residuals


# --- the three-way correspondence, refusing in one derived direction ---


def test_every_gate_mentioned_in_the_readme_has_exactly_one_correspondence_row(
    ledger: AchievementLedger,
) -> None:
    gates = [entry.gate_id for entry in ledger.correspondence]
    assert len(gates) == len(set(gates))
    for row in ledger.rows:
        assert ledger.correspondence_row(row.claim.gate_id)


def test_all_three_correspondence_standings_are_occupied_by_the_real_tree(
    ledger: AchievementLedger,
) -> None:
    for standing in GateCorrespondenceStanding:
        assert ledger.correspondence_by_standing(standing)


def test_the_readme_only_gate_found_by_this_milestone_is_recorded_not_refused(
    ledger: AchievementLedger,
) -> None:
    readme_only = ledger.correspondence_by_standing(
        GateCorrespondenceStanding.ANNOUNCED_IN_README_ONLY
    )
    assert [entry.gate_id for entry in readme_only] == ["P0.1"]
    residuals = ACHIEVEMENT_LEDGER_NAMED_RESIDUALS
    assert README_ONLY_GATE_IS_RECORDED_NOT_REFUSED in residuals


def test_a_claim_whose_gate_the_constitution_never_names_is_refused() -> None:
    readme = (
        "G0.ZZ.9 does a thing (`src/alghanem/kernel/transition.py`)\n"
        "and issues an `Operation`.\n"
    )
    constitution = "# Constitution\n\n### G0.C.1 — something else\n\ntext\n"
    claims = read_readme_claims(readme)
    row = AchievementRow(
        claim=claims[0],
        resident_symbols=derive_resident_symbols(claims[0]),
        witness_relative_path="tests/kernel/test_transition.py",
        witness_standing=WitnessStanding.WITNESS_NOT_REGISTERED,
    )
    with pytest.raises(AchievementLedgerError, match="بلا تسميةٍ في الدستور"):
        AchievementLedger(
            rows=(row,),
            correspondence=correspond_gates(readme, constitution),
            example_scripts=(),
            skipped_witnesses=(),
        )


def test_a_gate_heading_a_constitution_section_is_read_from_its_heading(
    constitution_text: str,
) -> None:
    headings = read_constitution_heading_gates(constitution_text)
    assert "G0.C.1" in headings
    assert "G0.EA.1" in headings
    assert all(line > 0 for line in headings.values())


def test_a_body_only_mention_is_distinguished_from_a_section_heading() -> None:
    readme = "G0.AA.1 and G0.BB.1 are announced here.\n"
    constitution = "# Doc\n\n### G0.AA.1 — heading\n\nthe body mentions G0.BB.1 too\n"
    rows = {entry.gate_id: entry for entry in correspond_gates(readme, constitution)}
    assert (
        rows["G0.AA.1"].constitution_site
        is ConstitutionNamingSite.NAMED_IN_A_SECTION_HEADING
    )
    assert (
        rows["G0.BB.1"].constitution_site
        is ConstitutionNamingSite.NAMED_IN_THE_BODY_ONLY
    )


def test_a_constitution_without_a_single_gate_heading_is_refused() -> None:
    with pytest.raises(AchievementLedgerError, match="لم يُقرَأ أيّ عنوانِ بوّابة"):
        read_constitution_heading_gates("# Doc\n\nprose only\n")


def test_a_readme_only_standing_carrying_a_constitution_line_is_refused() -> None:
    with pytest.raises(AchievementLedgerError, match="ومعها موضعٌ فيه"):
        GateCorrespondenceRow(
            gate_id="P0.1",
            standing=GateCorrespondenceStanding.ANNOUNCED_IN_README_ONLY,
            readme_line=45,
            constitution_line=10,
            constitution_site=ConstitutionNamingSite.NAMED_IN_THE_BODY_ONLY,
        )


def test_a_constitution_only_standing_carrying_a_readme_line_is_refused() -> None:
    with pytest.raises(AchievementLedgerError, match="ومعه موضعُ ذِكرٍ فيها|ومعها"):
        GateCorrespondenceRow(
            gate_id="G0.MA",
            standing=GateCorrespondenceStanding.DECLARED_IN_CONSTITUTION_ONLY,
            readme_line=12,
            constitution_line=1338,
            constitution_site=ConstitutionNamingSite.NAMED_IN_A_SECTION_HEADING,
        )


def test_a_both_sided_standing_without_a_constitution_position_is_refused() -> None:
    with pytest.raises(AchievementLedgerError, match="بلا موضعٍ فيه"):
        GateCorrespondenceRow(
            gate_id="G0.EA.1",
            standing=GateCorrespondenceStanding.ANNOUNCED_IN_BOTH,
            readme_line=28,
        )


# --- the witness is derived by the tree's own convention, in three standings ---


def test_the_witness_path_is_derived_from_the_module_path_not_written() -> None:
    assert claim().witness_relative_path == "tests/kernel/test_independent_closure.py"


def test_every_achievement_in_this_tree_has_its_derived_witness_present(
    ledger: AchievementLedger,
) -> None:
    present = ledger.rows_by_witness_standing(
        WitnessStanding.WITNESS_DERIVED_AND_PRESENT
    )
    assert len(present) == ledger.achievement_count
    root = repository_root()
    for row in present:
        assert (root / row.witness_relative_path).is_file()


def test_an_absent_derived_witness_reads_as_unregistered_not_as_a_refusal(
    tmp_path: Path,
) -> None:
    witness_path, standing = derive_witness_standing(claim(), tmp_path)
    assert standing is WitnessStanding.WITNESS_NOT_REGISTERED
    assert standing.is_a_refusal is False
    assert witness_path == claim().witness_relative_path


def test_a_witness_registered_elsewhere_is_a_third_standing_not_the_first(
    tmp_path: Path,
) -> None:
    elsewhere = tmp_path / "tests" / "elsewhere" / "test_other.py"
    elsewhere.parent.mkdir(parents=True)
    elsewhere.write_text("def test_it() -> None:\n    pass\n", encoding="utf-8")
    witness_path, standing = derive_witness_standing(
        claim(),
        tmp_path,
        {"G0.IC.1a": "tests/elsewhere/test_other.py"},
    )
    assert standing is WitnessStanding.WITNESS_REGISTERED_ELSEWHERE
    assert witness_path == "tests/elsewhere/test_other.py"


def test_a_witness_file_without_a_test_function_is_not_a_present_witness(
    tmp_path: Path,
) -> None:
    empty = tmp_path / "tests" / "kernel" / "test_independent_closure.py"
    empty.parent.mkdir(parents=True)
    empty.write_text("def helper() -> None:\n    pass\n", encoding="utf-8")
    _witness_path, standing = derive_witness_standing(claim(), tmp_path)
    assert standing is WitnessStanding.WITNESS_NOT_REGISTERED


def test_a_derived_standing_pointing_somewhere_else_is_refused() -> None:
    with pytest.raises(AchievementLedgerError, match="ليس الموضعَ الذي يشتقّه"):
        AchievementRow(
            claim=claim(),
            resident_symbols=("ClosureScopeRegistry",),
            witness_relative_path="tests/kernel/test_kernel.py",
            witness_standing=WitnessStanding.WITNESS_DERIVED_AND_PRESENT,
        )


def test_that_a_witness_collects_is_not_that_it_checks_this_claim() -> None:
    residuals = ACHIEVEMENT_LEDGER_NAMED_RESIDUALS
    assert WITNESS_COLLECTS_IS_NOT_WITNESS_CHECKS_THIS in residuals


# --- the two standing gaps are counted, never assumed away ---


def test_every_example_script_carries_a_declared_reproduction_standing(
    ledger: AchievementLedger,
) -> None:
    assert ledger.example_script_count == len(
        list((repository_root() / EXAMPLES_RELATIVE_PATH).rglob("*.py"))
    )
    for entry in ledger.example_scripts:
        assert entry.relative_path.startswith(f"{EXAMPLES_RELATIVE_PATH}/")
        assert isinstance(entry.standing, ExampleScriptStanding)


def test_one_example_script_in_this_tree_is_reproduced_and_the_rest_are_not(
    ledger: AchievementLedger,
) -> None:
    """الرتبتان معًا مسكونتان، والمذكورُ في شاهدٍ ليس بذلك مُشغَّلًا فيه."""

    reproduced = ledger.example_scripts_by_standing(
        ExampleScriptStanding.REPRODUCED_BY_A_WITNESS
    )
    unreproduced = ledger.example_scripts_by_standing(
        ExampleScriptStanding.DECLARED_NOT_REPRODUCED
    )
    assert [entry.relative_path for entry in reproduced] == [
        "examples/kernel/license_transitions.py"
    ]
    assert len(reproduced) + len(unreproduced) == ledger.example_script_count
    assert (
        EXAMPLE_SCRIPT_REFERENCE_IS_NOT_EXECUTION in ACHIEVEMENT_LEDGER_NAMED_RESIDUALS
    )


def test_a_script_named_inside_a_witness_reads_as_reproduced(
    tmp_path: Path,
) -> None:
    script = tmp_path / EXAMPLES_RELATIVE_PATH / "run_me.py"
    script.parent.mkdir(parents=True)
    script.write_text("print(1)\n", encoding="utf-8")
    witness = tmp_path / TESTS_RELATIVE_PATH / "test_examples.py"
    witness.parent.mkdir(parents=True)
    witness.write_text('PATH = "examples/run_me.py"\n', encoding="utf-8")
    rows = census_example_scripts(tmp_path)
    assert rows == (
        ExampleScriptRow(
            relative_path="examples/run_me.py",
            standing=ExampleScriptStanding.REPRODUCED_BY_A_WITNESS,
        ),
    )


def test_an_absent_examples_tree_is_refused_not_read_as_no_examples(
    tmp_path: Path,
) -> None:
    with pytest.raises(AchievementLedgerError, match="شجرة الأمثلة غير موجودة"):
        census_example_scripts(tmp_path)


def test_a_script_outside_the_examples_tree_is_refused() -> None:
    with pytest.raises(AchievementLedgerError, match="خارج شجرة الأمثلة"):
        ExampleScriptRow(
            relative_path="src/alghanem/kernel/transition.py",
            standing=ExampleScriptStanding.DECLARED_NOT_REPRODUCED,
        )


def test_both_skip_genera_are_occupied_by_the_arabic_witnesses(
    ledger: AchievementLedger,
) -> None:
    arabic = [
        entry
        for entry in ledger.skipped_witnesses
        if entry.relative_path.startswith("tests/arabic/")
    ]
    assert {entry.genus for entry in arabic} == set(SkipGenus)
    for entry in arabic:
        assert entry.document_line > 0


def test_every_skip_in_the_witness_tree_carries_a_declared_genus(
    ledger: AchievementLedger,
) -> None:
    for entry in ledger.skipped_witnesses:
        assert isinstance(entry.genus, SkipGenus)
        assert entry.relative_path.startswith(f"{TESTS_RELATIVE_PATH}/")


def test_a_skip_form_outside_the_two_genera_stops_the_reading(
    tmp_path: Path,
) -> None:
    witness = tmp_path / TESTS_RELATIVE_PATH / "test_odd.py"
    witness.parent.mkdir(parents=True)
    witness.write_text(f"{_UNKNOWN_SKIP_SOURCE}\ndef test_x():\n    pass\n", "utf-8")
    with pytest.raises(AchievementLedgerError, match="تخطٍّ خارج الجنسين"):
        census_skipped_witnesses(tmp_path)


def test_the_two_declared_skip_forms_are_classified_by_their_own_genus(
    tmp_path: Path,
) -> None:
    witness = tmp_path / TESTS_RELATIVE_PATH / "test_two.py"
    witness.parent.mkdir(parents=True)
    witness.write_text(
        f"{_CONDITIONAL_SKIP_SOURCE}\ndef test_a():\n{_INLINE_SKIP_SOURCE}\n",
        encoding="utf-8",
    )
    rows = census_skipped_witnesses(tmp_path)
    assert [entry.genus for entry in rows] == [
        SkipGenus.CONDITIONAL_ON_UNDEPOSITED_INPUT,
        SkipGenus.CASE_INAPPLICABLE_BY_CONSTRUCTION,
    ]


def test_an_absent_witness_tree_is_refused_not_read_as_no_witnesses(
    tmp_path: Path,
) -> None:
    with pytest.raises(AchievementLedgerError, match="شجرة الشواهد غير موجودة"):
        census_skipped_witnesses(tmp_path)


# --- the ledger refuses malformed assemblies rather than repairing them ---


def test_two_claims_for_one_gate_are_refused_at_construction() -> None:
    first = AchievementRow(
        claim=claim(),
        resident_symbols=("ClosureScopeRegistry",),
        witness_relative_path="tests/kernel/test_independent_closure.py",
        witness_standing=WitnessStanding.WITNESS_DERIVED_AND_PRESENT,
    )
    second = replace(first, claim=replace(first.claim, document_line=99))
    with pytest.raises(AchievementLedgerError, match="تُطالِب بوحدتها مرّتين"):
        AchievementLedger(
            rows=(first, second),
            correspondence=(
                GateCorrespondenceRow(
                    gate_id="G0.IC.1a",
                    standing=GateCorrespondenceStanding.ANNOUNCED_IN_BOTH,
                    readme_line=87,
                    constitution_line=1000,
                    constitution_site=(
                        ConstitutionNamingSite.NAMED_IN_A_SECTION_HEADING
                    ),
                ),
            ),
            example_scripts=(),
            skipped_witnesses=(),
        )


def test_rows_out_of_document_order_are_refused() -> None:
    later = AchievementRow(
        claim=claim(gate_id="G0.IC.1b", document_line=200),
        resident_symbols=("ClosureScopeRegistry",),
        witness_relative_path="tests/kernel/test_independent_closure.py",
        witness_standing=WitnessStanding.WITNESS_DERIVED_AND_PRESENT,
    )
    earlier = AchievementRow(
        claim=claim(gate_id="G0.IC.1a", document_line=87),
        resident_symbols=("ClosureScopeRegistry",),
        witness_relative_path="tests/kernel/test_independent_closure.py",
        witness_standing=WitnessStanding.WITNESS_DERIVED_AND_PRESENT,
    )
    with pytest.raises(AchievementLedgerError, match="ترتيبُ ورودها"):
        AchievementLedger(
            rows=(later, earlier),
            correspondence=(
                GateCorrespondenceRow(
                    gate_id="G0.IC.1a",
                    standing=GateCorrespondenceStanding.ANNOUNCED_IN_BOTH,
                    readme_line=87,
                    constitution_line=1000,
                    constitution_site=(
                        ConstitutionNamingSite.NAMED_IN_A_SECTION_HEADING
                    ),
                ),
            ),
            example_scripts=(),
            skipped_witnesses=(),
        )


def test_a_lookup_without_a_row_is_refused_not_returned_as_none(
    ledger: AchievementLedger,
) -> None:
    with pytest.raises(AchievementLedgerError, match="لا صفَّ إنجازٍ للبوّابة"):
        ledger.row("G0.NOPE.1")
    with pytest.raises(AchievementLedgerError, match="لا صفَّ مقابلةٍ للمعرّف"):
        ledger.correspondence_row("G0.NOPE.1")


def test_rows_are_frozen_against_quiet_mutation(ledger: AchievementLedger) -> None:
    with pytest.raises(FrozenInstanceError):
        ledger.rows[0].claim.gate_id = "G0.OTHER"  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        ledger.correspondence[0].gate_id = "G0.OTHER"  # type: ignore[misc]


def test_a_missing_readme_is_refused_not_read_as_no_achievements(
    tmp_path: Path,
) -> None:
    with pytest.raises(AchievementLedgerError, match="تعذّرت قراءة الواجهة"):
        correspond_achievements_to_tree(root=tmp_path)


def test_a_vocabulary_member_from_outside_its_enum_is_refused() -> None:
    with pytest.raises(AchievementLedgerError, match="من مفردته المغلقة"):
        SkippedWitnessRow(
            relative_path="tests/x/test_y.py",
            document_line=1,
            genus="conditional",  # type: ignore[arg-type]
        )


# --- no written counts, no verdict, no attainment ---


def test_no_dataclass_here_writes_a_count_or_an_answer() -> None:
    for declared in _LEDGER_TYPES:
        for item in fields(declared):
            assert "count" not in item.name
            for marker in _ANSWER_MARKERS:
                assert marker not in item.name
    assert isinstance(AchievementLedger.achievement_count, property)
    assert isinstance(AchievementLedger.correspondence_count, property)
    assert isinstance(AchievementLedger.example_script_count, property)
    assert isinstance(AchievementLedger.skipped_witness_count, property)


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
        "milestone_ledger",
        "step_reproducers",
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


def test_no_kernel_arabic_or_encyclopedia_module_imports_this_ledger() -> None:
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
                    assert "achievement_ledger" not in node.module
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        assert "achievement_ledger" not in alias.name


# --- named residuals and the cited design source ---


def test_named_residuals_are_recorded_in_code_not_prose_alone() -> None:
    assert set(ACHIEVEMENT_LEDGER_NAMED_RESIDUALS) == {
        CLAIM_SHAPE_IS_A_FORM_NOT_A_MEANING,
        SYMBOL_PRESENCE_IS_NOT_SYMBOL_AUTHORSHIP,
        WITNESS_COLLECTS_IS_NOT_WITNESS_CHECKS_THIS,
        README_ONLY_GATE_IS_RECORDED_NOT_REFUSED,
        EXAMPLE_SCRIPT_REFERENCE_IS_NOT_EXECUTION,
    }
    for reason in ACHIEVEMENT_LEDGER_NAMED_RESIDUALS.values():
        assert reason.strip()


def test_the_design_source_open_question_is_cited_not_rederived() -> None:
    assert DESIGN_SOURCE_OPEN_QUESTION in ACHIEVEMENT_LEDGER_DESIGN_SOURCE_CITATION_NOTE
    assert ACHIEVEMENT_LEDGER_AUTHORITY_NOTE.strip()
    assert NO_INDICATOR_IN_THIS_ACHIEVEMENT_LEDGER_NOTE.strip()
    assert CLAIMED_MODULE_MUST_IMPORT_NOTE.strip()
