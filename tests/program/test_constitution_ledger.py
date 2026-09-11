"""Tests for the AIM.1 derivation readers over the constitution document."""

from __future__ import annotations

import pkgutil
from dataclasses import fields, replace
from pathlib import Path

import pytest

import alghanem.kernel as kernel_package
from alghanem.program import (
    NO_STATUS_DECLARED_IN_RECORD,
    AuditQuestionLedger,
    AuditQuestionRow,
    AuditQuestionStanding,
    ConstitutionLedgerError,
    DeclaredLawStatus,
    LawRow,
    LawRowLedger,
    constitution_document_path,
    load_constitution_ledger,
    read_constitution_ledger,
)
from alghanem.program import constitution_ledger as ledger_module
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
)

_MINIMAL_DOCUMENT = """# Title

| Law | Status | Scope |
| --- | --- | --- |
| `FirstLaw` | ENFORCED | scope one |
| `SecondLaw` | DECLARED_DEFERRED | scope with an escaped \\| pipe |

| Explanatory candidate | Piercing question |
| --- | --- |
| Repetition-only candidate | Can mere repetition explain it? |

### OpenAuditQuestions

- `AnOpenQuestionWithoutStatus`: the boundary is not yet derived.
- `AnOpenQuestionWithStatus`
  - Status: `OPEN`

### ResolvedAuditQuestions (lineage preserved)

- `AResolvedQuestion`
  - Previous audit label: `ClosedResiduals`
  - Status: `RESOLVED_BY_G_MINUS_1_1`
  - Closure law: `SomeLaw`

## Next section
"""


def law_row(**overrides: object) -> LawRow:
    base: dict[str, object] = dict(
        law="`FirstLaw`",
        status=DeclaredLawStatus.ENFORCED,
        document_line=5,
    )
    base.update(overrides)
    return LawRow(**base)  # type: ignore[arg-type]


def question_row(**overrides: object) -> AuditQuestionRow:
    base: dict[str, object] = dict(
        name="AnOpenQuestion",
        standing=AuditQuestionStanding.OPEN,
        declared_status="OPEN",
        document_line=12,
    )
    base.update(overrides)
    return AuditQuestionRow(**base)  # type: ignore[arg-type]


def test_the_minimal_document_is_read_into_two_separate_ledgers() -> None:
    ledger = read_constitution_ledger(_MINIMAL_DOCUMENT)
    assert ledger.laws.row_count == 2
    assert [row.law for row in ledger.laws.rows] == ["`FirstLaw`", "`SecondLaw`"]
    assert ledger.audit_questions.open_count == 2
    assert ledger.audit_questions.resolved_count == 1


def test_only_law_tables_are_counted() -> None:
    ledger = read_constitution_ledger(_MINIMAL_DOCUMENT)
    counted = {row.law for row in ledger.laws.rows}
    assert "Repetition-only candidate" not in counted


def test_an_escaped_pipe_does_not_split_a_row() -> None:
    ledger = read_constitution_ledger(_MINIMAL_DOCUMENT)
    second = ledger.laws.rows[1]
    assert second.status is DeclaredLawStatus.DECLARED_DEFERRED
    assert second.law == "`SecondLaw`"


def test_an_undeclared_status_is_refused_and_never_skipped() -> None:
    document = _MINIMAL_DOCUMENT.replace("| ENFORCED |", "| MOSTLY_ENFORCED |")
    with pytest.raises(ConstitutionLedgerError, match="خارج المفردة المغلقة"):
        read_constitution_ledger(document)


def test_a_missing_audit_section_is_refused_not_read_as_empty() -> None:
    document = _MINIMAL_DOCUMENT.replace("### OpenAuditQuestions", "### Something")
    with pytest.raises(ConstitutionLedgerError, match="قسمٌ مفقود"):
        read_constitution_ledger(document)


def test_a_missing_document_is_a_named_refusal_not_an_empty_ledger(
    tmp_path: Path,
) -> None:
    with pytest.raises(ConstitutionLedgerError, match="تعذّرت قراءة"):
        load_constitution_ledger(tmp_path / "absent.md")


def test_ignorance_of_a_declared_status_is_a_value_not_a_blank() -> None:
    ledger = read_constitution_ledger(_MINIMAL_DOCUMENT)
    by_name = {question.name: question for question in ledger.audit_questions.questions}
    without = by_name["AnOpenQuestionWithoutStatus"]
    assert without.declared_status == NO_STATUS_DECLARED_IN_RECORD
    assert without.status_is_declared_in_record is False
    assert by_name["AnOpenQuestionWithStatus"].status_is_declared_in_record is True


def test_a_resolved_question_keeps_its_lineage_and_closure_law() -> None:
    ledger = read_constitution_ledger(_MINIMAL_DOCUMENT)
    resolved = ledger.audit_questions.resolved_questions[0]
    assert resolved.previous_audit_label == "ClosedResiduals"
    assert resolved.closure_law == "SomeLaw"
    assert resolved.remains_open is False


def test_lineage_fields_are_required_exactly_when_resolved() -> None:
    with pytest.raises(ConstitutionLedgerError, match="الوسم السابق"):
        question_row(standing=AuditQuestionStanding.RESOLVED, closure_law="SomeLaw")
    with pytest.raises(ConstitutionLedgerError, match="قانون الإغلاق"):
        question_row(
            standing=AuditQuestionStanding.RESOLVED,
            previous_audit_label="ClosedResiduals",
        )
    with pytest.raises(ConstitutionLedgerError, match="يبقى فارغًا"):
        question_row(previous_audit_label="ClosedResiduals")
    with pytest.raises(ConstitutionLedgerError, match="يبقى فارغًا"):
        question_row(closure_law="SomeLaw")


def test_a_resolved_question_without_a_declared_status_is_refused() -> None:
    with pytest.raises(ConstitutionLedgerError, match="بلا حالةٍ مُعلَنة"):
        question_row(
            standing=AuditQuestionStanding.RESOLVED,
            declared_status=NO_STATUS_DECLARED_IN_RECORD,
            previous_audit_label="ClosedResiduals",
            closure_law="SomeLaw",
        )


def test_closed_vocabularies_reject_foreign_values() -> None:
    with pytest.raises(ConstitutionLedgerError, match="حالة الصفّ"):
        law_row(status="ENFORCED")
    with pytest.raises(ConstitutionLedgerError, match="موقف السؤال"):
        question_row(standing="OPEN")
    with pytest.raises(ConstitutionLedgerError, match="اسم الصفّ"):
        law_row(law="   ")
    with pytest.raises(ConstitutionLedgerError, match="موضع الصفّ"):
        law_row(document_line=0)


def test_a_law_name_is_never_counted_twice() -> None:
    with pytest.raises(ConstitutionLedgerError, match="اسم صفٍّ مكرّر"):
        LawRowLedger(rows=(law_row(), law_row(document_line=6)))


def test_law_rows_keep_the_document_order() -> None:
    with pytest.raises(ConstitutionLedgerError, match="ورودها"):
        LawRowLedger(
            rows=(law_row(document_line=6), law_row(law="`Other`", document_line=5))
        )


def test_one_question_is_never_both_open_and_resolved() -> None:
    with pytest.raises(ConstitutionLedgerError, match="سؤالٌ مكرّر"):
        AuditQuestionLedger(
            questions=(
                question_row(),
                question_row(
                    standing=AuditQuestionStanding.RESOLVED,
                    previous_audit_label="ClosedResiduals",
                    closure_law="SomeLaw",
                ),
            )
        )


def test_an_empty_ledger_is_refused() -> None:
    with pytest.raises(ConstitutionLedgerError, match="غير فارغة"):
        LawRowLedger(rows=())
    with pytest.raises(ConstitutionLedgerError, match="غير فارغة"):
        AuditQuestionLedger(questions=())
    with pytest.raises(ConstitutionLedgerError, match="نصٌّ غير فارغ"):
        read_constitution_ledger("   ")


def test_counts_are_derived_properties_and_never_written_fields() -> None:
    declared = {item.name for item in fields(LawRowLedger)}
    declared |= {item.name for item in fields(AuditQuestionLedger)}
    assert not any("count" in name for name in declared)
    ledger = read_constitution_ledger(_MINIMAL_DOCUMENT)
    assert sum(ledger.laws.status_counts.values()) == ledger.laws.row_count
    with pytest.raises(TypeError):
        ledger.laws.status_counts[DeclaredLawStatus.ENFORCED] = 99  # type: ignore[index]


def test_every_status_member_is_present_in_the_counts_even_at_zero() -> None:
    ledger = read_constitution_ledger(_MINIMAL_DOCUMENT)
    counts = ledger.laws.status_counts
    assert set(counts) == set(DeclaredLawStatus)
    assert counts[DeclaredLawStatus.DECLARED_LAW_ONLY] == 0


def test_rows_with_status_requires_the_closed_vocabulary() -> None:
    ledger = read_constitution_ledger(_MINIMAL_DOCUMENT)
    assert len(ledger.laws.rows_with_status(DeclaredLawStatus.ENFORCED)) == 1
    with pytest.raises(ConstitutionLedgerError, match="حالة الصفّ"):
        ledger.laws.rows_with_status("ENFORCED")  # type: ignore[arg-type]


def test_a_read_row_is_frozen_and_replacement_is_revalidated() -> None:
    with pytest.raises(ConstitutionLedgerError, match="حالة الصفّ"):
        replace(law_row(), status="ENFORCED")


@pytest.mark.parametrize("marker", _ANSWER_MARKERS)
def test_no_reader_type_carries_an_answer_bearing_field(marker: str) -> None:
    for declaring_type in (LawRow, AuditQuestionRow, LawRowLedger, AuditQuestionLedger):
        declared = {item.name for item in fields(declaring_type)}
        assert not any(marker in name for name in declared), declaring_type


def test_the_reader_is_not_bound_to_any_aim() -> None:
    bound = set(vars(ledger_module)) & {
        "AimId",
        "AIM_RECORDS",
        "AimRecord",
        "AttainmentStanding",
        "ForeignDeclaredAim",
    }
    assert bound == set()
    for declaring_type in (LawRow, AuditQuestionRow, LawRowLedger, AuditQuestionLedger):
        declared = {item.name for item in fields(declaring_type)}
        assert not any("aim" in name for name in declared), declaring_type


def test_the_module_cites_its_direct_design_source() -> None:
    assert ledger_module.__doc__ is not None
    assert DESIGN_SOURCE_OPEN_QUESTION in ledger_module.__doc__
    assert DESIGN_SOURCE_OPEN_QUESTION in ledger_module.DESIGN_SOURCE_CITATION_NOTE


def test_the_repository_document_is_read_without_refusal() -> None:
    assert constitution_document_path().name == "CONSTITUTION.md"
    ledger = load_constitution_ledger()
    assert ledger.laws.row_count == sum(ledger.laws.status_counts.values())
    assert ledger.laws.row_count > 100
    assert ledger.laws.status_counts[DeclaredLawStatus.DECLARED_DEFERRED] > 0
    assert ledger.laws.status_counts[DeclaredLawStatus.ENFORCED_AT_AIM_RECORD] == 1
    open_names = {question.name for question in ledger.audit_questions.open_questions}
    assert DESIGN_SOURCE_OPEN_QUESTION in open_names
    assert ledger.audit_questions.resolved_count > 0
    for question in ledger.audit_questions.resolved_questions:
        assert question.previous_audit_label
        assert question.closure_law


def test_no_kernel_module_reads_the_derivation_readers() -> None:
    for module in pkgutil.walk_packages(
        kernel_package.__path__, prefix="alghanem.kernel."
    ):
        source = module.module_finder.find_spec(  # type: ignore[union-attr]
            module.name
        )
        assert source is not None and source.origin is not None
        text = Path(source.origin).read_text(encoding="utf-8")
        assert "alghanem.program" not in text, module.name
        assert "ConstitutionLedger" not in text, module.name
        assert "LawRowLedger" not in text, module.name
        assert "AuditQuestionLedger" not in text, module.name
