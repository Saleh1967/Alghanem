"""شواهدُ إيداع نواة النسبة: النصُّ أمينٌ، والمنافسةُ مُعلَنةٌ، ولا قراءةَ بعدُ."""

from __future__ import annotations

import ast
import pathlib

import pytest

from alghanem.arabic.flt1_qiyas_law import FLT1_QIYAS_TEXT, FLT1_QIYAS_TEXT_DIGEST
from alghanem.arabic.nisbah_nucleus_hypothesis import (
    COMPETING_STATEMENT_RECORD,
    NISBAH_NUCLEUS_NAMED_RESIDUALS,
    NISBAH_NUCLEUS_TEXT,
    NISBAH_NUCLEUS_TEXT_DIGEST,
    REQUIRED_NOTATION_SITES,
    CompetingStatementRecord,
    FidelityStanding,
    NisbahNucleusHypothesisError,
    derive_fidelity_report,
    nisbah_nucleus_text_digest,
)
from alghanem.metaalgebra.layer import CARRIER_IS_NOT_STATE
from alghanem.metaalgebra.schema import META_ALGEBRA_SCHEMA

_MODULE_PATH = (
    pathlib.Path(__file__).resolve().parents[2]
    / "src"
    / "alghanem"
    / "arabic"
    / "nisbah_nucleus_hypothesis.py"
)


def test_the_deposited_text_carries_every_decisive_site() -> None:
    report = derive_fidelity_report()

    assert report.absent_site_ids == ()
    assert report.standing is FidelityStanding.EVERY_DECISIVE_SITE_IS_PRESENT
    assert report.is_fit_to_be_read
    assert len(report.sites) == len(REQUIRED_NOTATION_SITES)
    assert report.text_digest == NISBAH_NUCLEUS_TEXT_DIGEST


def test_a_text_that_drops_the_minimal_triple_is_unfit_to_be_read() -> None:
    mutilated = NISBAH_NUCLEUS_TEXT.replace(
        r"\boxed{(Term,\ Predicate,\ Relation)}", r"\boxed{(Term,\ Predicate)}"
    )

    report = derive_fidelity_report(mutilated)

    assert not report.is_fit_to_be_read
    assert report.standing is FidelityStanding.A_DECISIVE_SITE_IS_ABSENT
    assert "the-minimal-linguistic-triple" in report.absent_site_ids


def test_a_text_that_drops_the_retained_representation_law_is_unfit() -> None:
    mutilated = NISBAH_NUCLEUS_TEXT.replace(
        "Representation(x)=(Carrier,State)", "Representation(x)"
    )

    report = derive_fidelity_report(mutilated)

    assert not report.is_fit_to_be_read
    assert "representation-stays" in report.absent_site_ids


def test_site_identifiers_are_distinct() -> None:
    ids = tuple(site.site_id for site in REQUIRED_NOTATION_SITES)

    assert len(ids) == len(set(ids))


def test_a_site_without_a_literal_is_refused() -> None:
    from alghanem.arabic.nisbah_nucleus_hypothesis import NotationSite

    with pytest.raises(NisbahNucleusHypothesisError):
        NotationSite(
            site_id="empty",
            literal="   ",
            what_it_decides="شيء",
            what_its_absence_invalidates="شيء",
        )


def test_an_empty_text_has_no_digest() -> None:
    with pytest.raises(NisbahNucleusHypothesisError):
        nisbah_nucleus_text_digest("   ")


def test_the_digest_is_derived_from_the_bytes_not_written_beside_them() -> None:
    assert nisbah_nucleus_text_digest(NISBAH_NUCLEUS_TEXT) == NISBAH_NUCLEUS_TEXT_DIGEST
    assert nisbah_nucleus_text_digest(NISBAH_NUCLEUS_TEXT + " ") != (
        NISBAH_NUCLEUS_TEXT_DIGEST
    )


def test_the_competing_record_binds_both_digests() -> None:
    assert COMPETING_STATEMENT_RECORD.competed_text_digest == FLT1_QIYAS_TEXT_DIGEST
    assert COMPETING_STATEMENT_RECORD.competing_text_digest == (
        NISBAH_NUCLEUS_TEXT_DIGEST
    )
    assert COMPETING_STATEMENT_RECORD.competed_text_digest != (
        COMPETING_STATEMENT_RECORD.competing_text_digest
    )


def test_a_statement_that_competes_with_itself_is_refused() -> None:
    with pytest.raises(NisbahNucleusHypothesisError):
        CompetingStatementRecord(
            competed_text_digest=NISBAH_NUCLEUS_TEXT_DIGEST,
            competing_text_digest=NISBAH_NUCLEUS_TEXT_DIGEST,
            what_the_competed_text_keeps="شيء",
            why_supersession_is_refused_here="شيء",
            what_would_invalidate_this_statement="شيء",
        )


def test_the_competed_text_keeps_its_own_letter() -> None:
    assert r"Q(O,F)" in FLT1_QIYAS_TEXT
    assert FLT1_QIYAS_TEXT_DIGEST == FLT1_QIYAS_TEXT_DIGEST


def test_the_carrier_state_law_is_untouched_by_this_deposit() -> None:
    assert "الحاملُ غيرُ الحالة" in CARRIER_IS_NOT_STATE
    assert "CarrierIsNotState" in META_ALGEBRA_SCHEMA.law_ids
    assert META_ALGEBRA_SCHEMA.sort_ids == (
        "Layer",
        "Transition",
        "AuditCertificate",
        "Realization",
    )


def test_no_nisbah_sort_entered_the_meta_algebra_schema() -> None:
    for forbidden in ("Term", "Predicate", "Operator", "Nisbah", "ArgumentRole"):
        assert forbidden not in META_ALGEBRA_SCHEMA.sort_ids


def _imported_module_names() -> tuple[str, ...]:
    tree = ast.parse(_MODULE_PATH.read_text(encoding="utf-8"))
    names: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            names.append("." * node.level + (node.module or ""))
    return tuple(names)


def test_the_deposit_imports_nothing_from_the_kernel() -> None:
    for imported in _imported_module_names():
        assert "kernel" not in imported


def test_the_deposit_duplicates_no_standing_vocabulary() -> None:
    for imported in _imported_module_names():
        assert "mantuq_mafhum_ifada" not in imported
        assert "compound_layer_preregistration" not in imported


def test_the_deposit_declares_no_reader_and_no_vocabulary_of_roles() -> None:
    tree = ast.parse(_MODULE_PATH.read_text(encoding="utf-8"))
    declared = {
        node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)
    }

    assert "RelationalRole" not in declared
    assert "NisbahRecord" not in declared
    assert "IfadaStanding" not in declared


def test_named_residuals_are_distinct_and_non_blank() -> None:
    assert len(set(NISBAH_NUCLEUS_NAMED_RESIDUALS)) == len(
        NISBAH_NUCLEUS_NAMED_RESIDUALS
    )
    for residual in NISBAH_NUCLEUS_NAMED_RESIDUALS:
        assert residual.strip()
