"""اختبارُ فحص المصدر النحويّ المقترَح: الإذنُ يسبق البنية، والحصيلةُ مُشتقّة.

والمقصودُ حسمُ ثلاثة أشياء: أنّ قيمةَ الفحص تُحسَب من الصفوف لا تُكتَب ثابتًا،
وأنّ صفحةً لم تُفتَح لا يُدَّعى عليها إذنٌ ولا بنيةٌ ولا بصمة، وأنّ الكتابَ
المردودَ لا يقوم مقامَ المقصود.
"""

from __future__ import annotations

import pkgutil
from dataclasses import fields
from pathlib import Path

import pytest

import alghanem.kernel as kernel_package
from alghanem.arabic import (
    MAANI_AL_NAHW_IS_NOT_NAHW_WADIH,
    MAANI_AL_NAHW_REJECTED_WORK,
    NAHW_WADIH_PROBE_NAMED_RESIDUALS,
    NAHW_WADIH_WORK,
    PROBED_CANDIDATES,
    GrammarSourceCandidate,
    GrammarSourceProbeError,
    GrammarSourceProbeOutcome,
    GrammarSourceProbeReport,
    LicenceStanding,
    ProposedWork,
    SourceReachability,
    StructureStanding,
    TextLayerStanding,
    derive_probe_outcome,
    run_nahw_wadih_source_probe,
)
from alghanem.arabic import nahw_wadih_source_probe as probe_module
from alghanem.program import REPORTED_UNVERIFIED_FIGURES

_OPEN_LICENCE_TEXT = "Creative Commons Attribution 4.0 International (CC BY 4.0)"
_RIGHTS_RESERVED_TEXT = "الملكية الفكرية محفوظة لأصحابها"


def _opened_candidate(
    *,
    licence_standing: LicenceStanding = LicenceStanding.EXPLICIT_OPEN_LICENCE_NAMED,
    verbatim_licence_text: str | None = _OPEN_LICENCE_TEXT,
    text_layer: TextLayerStanding = (
        TextLayerStanding.MACHINE_READABLE_TEXT_LAYER_FOUND
    ),
    numbered_rule_headings_found: bool | None = True,
    **overrides: object,
) -> GrammarSourceCandidate:
    """مُرشَّحٌ مُفترَضٌ للاختبار وحده؛ ولا يُقرأ خبرًا عن موضعٍ حقيقيّ."""
    fields_: dict[str, object] = {
        "work": NAHW_WADIH_WORK,
        "mirror": "example.test",
        "requested_url": "https://example.test/book",
        "declared_print_edition": None,
        "reachability": SourceReachability.OPENED_IN_THIS_SANDBOX,
        "licence_standing": licence_standing,
        "verbatim_licence_text": verbatim_licence_text,
        "text_layer": text_layer,
        "numbered_rule_headings_found": numbered_rule_headings_found,
        "note": "مُرشَّحٌ اصطناعيٌّ في الاختبار",
    }
    fields_.update(overrides)
    return GrammarSourceCandidate(**fields_)  # type: ignore[arg-type]


# --- الحصيلةُ مُشتقّةٌ لا مكتوبة -------------------------------------------------


def test_the_probe_outcome_is_derived_from_the_recorded_rows() -> None:
    report = run_nahw_wadih_source_probe()
    assert report == derive_probe_outcome(PROBED_CANDIDATES)
    assert isinstance(report, GrammarSourceProbeReport)
    source = Path(probe_module.__file__).read_text(encoding="utf-8")
    assert "PROBE_OUTCOME: Final" not in source


def test_what_this_environment_actually_found_is_licence_unresolved() -> None:
    report = run_nahw_wadih_source_probe()
    assert report.outcome is GrammarSourceProbeOutcome.SOURCE_LICENCE_UNRESOLVED
    assert (
        report.structure_standing
        is StructureStanding.NOT_INSPECTED_LICENCE_BLOCKED_FIRST
    )
    assert report.licence_unblocked_candidates == ()
    assert all(not candidate.reachability.was_opened for candidate in PROBED_CANDIDATES)


def test_an_open_licence_with_numbered_headings_derives_the_extractable_value() -> None:
    report = derive_probe_outcome((_opened_candidate(),))
    assert (
        report.outcome
        is GrammarSourceProbeOutcome.SOURCE_AVAILABLE_STRUCTURE_EXTRACTABLE
    )
    assert (
        report.structure_standing
        is StructureStanding.NUMBERED_RULE_STRUCTURE_EXTRACTABLE
    )


def test_ocr_over_scan_is_not_extractable_however_open_the_licence_is() -> None:
    report = derive_probe_outcome(
        (_opened_candidate(text_layer=TextLayerStanding.OCR_OVER_SCAN),)
    )
    assert (
        report.outcome
        is GrammarSourceProbeOutcome.SOURCE_AVAILABLE_STRUCTURE_NOT_EXTRACTABLE
    )
    assert report.structure_standing is StructureStanding.PROSE_OR_SCAN_ONLY


# --- الإذنُ يسبق البنية ---------------------------------------------------------


def test_a_rights_reserved_source_blocks_before_its_structure_is_read() -> None:
    report = derive_probe_outcome(
        (
            _opened_candidate(
                licence_standing=LicenceStanding.RIGHTS_RESERVED_STATED,
                verbatim_licence_text=_RIGHTS_RESERVED_TEXT,
            ),
        )
    )
    assert report.outcome is GrammarSourceProbeOutcome.SOURCE_LICENCE_UNRESOLVED
    assert (
        report.structure_standing
        is StructureStanding.NOT_INSPECTED_LICENCE_BLOCKED_FIRST
    )


def test_silence_blocks_exactly_as_rights_reserved_does() -> None:
    silent = derive_probe_outcome(
        (
            _opened_candidate(
                licence_standing=LicenceStanding.NO_STATEMENT_FOUND,
                verbatim_licence_text=None,
            ),
        )
    )
    assert silent.outcome is GrammarSourceProbeOutcome.SOURCE_LICENCE_UNRESOLVED


def test_only_one_licence_standing_unblocks_and_none_means_probably_permitted() -> None:
    unblocking = [standing for standing in LicenceStanding if standing.unblocks]
    assert unblocking == [LicenceStanding.EXPLICIT_OPEN_LICENCE_NAMED]


def test_a_blocked_report_may_not_carry_an_unblocked_candidate() -> None:
    with pytest.raises(GrammarSourceProbeError, match="لا يجتمع إذنٌ غيرُ محسوم"):
        GrammarSourceProbeReport(
            outcome=GrammarSourceProbeOutcome.SOURCE_LICENCE_UNRESOLVED,
            structure_standing=(StructureStanding.NOT_INSPECTED_LICENCE_BLOCKED_FIRST),
            licence_unblocked_candidates=(_opened_candidate(),),
            reason="علّةٌ مكتوبة",
        )


def test_an_unresolved_licence_may_not_be_reported_with_a_read_structure() -> None:
    with pytest.raises(GrammarSourceProbeError, match="الإذنُ يسبق البنية"):
        GrammarSourceProbeReport(
            outcome=GrammarSourceProbeOutcome.SOURCE_LICENCE_UNRESOLVED,
            structure_standing=(StructureStanding.NUMBERED_RULE_STRUCTURE_EXTRACTABLE),
            licence_unblocked_candidates=(),
            reason="علّةٌ مكتوبة",
        )


# --- صفحةٌ لم تُفتَح لا يُدَّعى عليها شيء ------------------------------------------


def test_a_digest_without_opened_bytes_is_refused() -> None:
    with pytest.raises(GrammarSourceProbeError, match="بصمةٌ لملفٍّ لم يُفتَح"):
        GrammarSourceCandidate(
            work=NAHW_WADIH_WORK,
            mirror="example.test",
            requested_url="https://example.test/book",
            declared_print_edition=None,
            reachability=SourceReachability.UNREACHABLE_FROM_THIS_SANDBOX,
            licence_standing=(LicenceStanding.NOT_READ_BECAUSE_PAGE_WAS_NOT_OPENED),
            verbatim_licence_text=None,
            text_layer=(TextLayerStanding.NOT_INSPECTED_BECAUSE_PAGE_WAS_NOT_OPENED),
            numbered_rule_headings_found=None,
            note="مُرشَّحٌ اصطناعيٌّ في الاختبار",
            sha256="a" * 64,
            byte_length=17,
        )


def test_an_unopened_page_may_not_be_read_as_silent_about_its_licence() -> None:
    with pytest.raises(GrammarSourceProbeError, match="لا تُقرأ رخصتُها"):
        GrammarSourceCandidate(
            work=NAHW_WADIH_WORK,
            mirror="example.test",
            requested_url="https://example.test/book",
            declared_print_edition=None,
            reachability=SourceReachability.UNREACHABLE_FROM_THIS_SANDBOX,
            licence_standing=LicenceStanding.NO_STATEMENT_FOUND,
            verbatim_licence_text=None,
            text_layer=(TextLayerStanding.NOT_INSPECTED_BECAUSE_PAGE_WAS_NOT_OPENED),
            numbered_rule_headings_found=None,
            note="مُرشَّحٌ اصطناعيٌّ في الاختبار",
        )


def test_a_structure_claim_over_an_unopened_page_is_refused() -> None:
    with pytest.raises(GrammarSourceProbeError, match="صفحةٍ لم تُفتَح دعوى بلا نظر"):
        GrammarSourceCandidate(
            work=NAHW_WADIH_WORK,
            mirror="example.test",
            requested_url="https://example.test/book",
            declared_print_edition=None,
            reachability=SourceReachability.UNREACHABLE_FROM_THIS_SANDBOX,
            licence_standing=(LicenceStanding.NOT_READ_BECAUSE_PAGE_WAS_NOT_OPENED),
            verbatim_licence_text=None,
            text_layer=(TextLayerStanding.NOT_INSPECTED_BECAUSE_PAGE_WAS_NOT_OPENED),
            numbered_rule_headings_found=True,
            note="مُرشَّحٌ اصطناعيٌّ في الاختبار",
        )


def test_a_read_licence_standing_deposits_its_verbatim_text() -> None:
    with pytest.raises(GrammarSourceProbeError, match="تُودِع نصَّه بحروفه"):
        _opened_candidate(verbatim_licence_text=None)


# --- الكتابُ المقصودُ وحدَه ------------------------------------------------------


def test_the_rejected_work_may_not_be_probed_in_place_of_the_intended_one() -> None:
    assert MAANI_AL_NAHW_REJECTED_WORK.is_rejected
    assert not NAHW_WADIH_WORK.is_rejected
    with pytest.raises(GrammarSourceProbeError, match="كتابٌ مردودٌ بعلّته"):
        _opened_candidate(work=MAANI_AL_NAHW_REJECTED_WORK)


def test_a_different_unrejected_work_is_still_refused_by_the_probe() -> None:
    other = ProposedWork(
        title="كتابٌ آخرُ لم يُردَّ بعد",
        authors=("مؤلّفٌ ما",),
        rejection_ground=None,
    )
    with pytest.raises(GrammarSourceProbeError, match="للنحو الواضح وحدَه"):
        derive_probe_outcome((_opened_candidate(work=other),))


def test_the_two_books_are_distinguished_by_title_and_authors() -> None:
    assert NAHW_WADIH_WORK.title != MAANI_AL_NAHW_REJECTED_WORK.title
    assert set(NAHW_WADIH_WORK.authors).isdisjoint(MAANI_AL_NAHW_REJECTED_WORK.authors)
    assert "معاني النحو" in MAANI_AL_NAHW_IS_NOT_NAHW_WADIH


# --- ما لا يحسمه الفحص، مُسمًّى ---------------------------------------------------


def test_the_named_residuals_are_carried_and_each_names_itself() -> None:
    assert "A_RULE_STATEMENT_IS_NOT_A_DECISION_PROCEDURE" in (
        NAHW_WADIH_PROBE_NAMED_RESIDUALS
    )
    assert "A_DIGEST_IS_NOT_A_PERMISSION" in NAHW_WADIH_PROBE_NAMED_RESIDUALS
    for name, note in NAHW_WADIH_PROBE_NAMED_RESIDUALS.items():
        assert note.startswith(f"{name}:")


def test_the_reported_rule_and_part_counts_are_filed_as_prose_not_measurement() -> None:
    figures = {record.figure_text: record for record in REPORTED_UNVERIFIED_FIGURES}
    assert "٤٢١ قاعدة" in figures
    assert "٣ أجزاء" in figures
    for figure in ("٤٢١ قاعدة", "٣ أجزاء"):
        assert not figures[figure].source_genus.supports_freeze


# --- السلطة: هذا الفحصُ خامل ------------------------------------------------------


def test_the_probe_has_exactly_three_outcome_members() -> None:
    assert len(GrammarSourceProbeOutcome) == 3
    names = {member.name for member in GrammarSourceProbeOutcome}
    assert names == {
        "SOURCE_AVAILABLE_STRUCTURE_EXTRACTABLE",
        "SOURCE_AVAILABLE_STRUCTURE_NOT_EXTRACTABLE",
        "SOURCE_LICENCE_UNRESOLVED",
    }


def test_the_probe_imports_nothing_from_the_kernel() -> None:
    source = Path(probe_module.__file__).read_text(encoding="utf-8")
    assert "alghanem.kernel" not in source
    assert "from ..kernel" not in source
    imported = [
        line
        for line in source.splitlines()
        if line.startswith(("import ", "from ")) and "__future__" not in line
    ]
    assert imported == [
        "from dataclasses import dataclass",
        "from enum import Enum",
        "from typing import Final",
    ]
    assert "DirectCertaintyStep." not in source


def test_no_kernel_module_reads_this_probe() -> None:
    for module in pkgutil.walk_packages(
        kernel_package.__path__, prefix="alghanem.kernel."
    ):
        spec = module.module_finder.find_spec(module.name)  # type: ignore[union-attr]
        assert spec is not None and spec.origin is not None
        text = Path(spec.origin).read_text(encoding="utf-8")
        assert "nahw_wadih_source_probe" not in text, module.name


def test_no_type_here_carries_a_verdict_pass_or_fail_field() -> None:
    for declaring in (
        ProposedWork,
        GrammarSourceCandidate,
        GrammarSourceProbeReport,
    ):
        for field in fields(declaring):
            lowered = field.name.lower()
            assert "verdict" not in lowered
            assert "pass" not in lowered
            assert "fail" not in lowered
            assert "birth" not in lowered
            assert "freeze" not in lowered


def test_the_probe_deposits_no_rule_text_and_no_extraction_machinery() -> None:
    source = Path(probe_module.__file__).read_text(encoding="utf-8")
    for forbidden in ("RuleNode", "extract_rules", "PreRegistration", "RULE_TEXTS"):
        assert forbidden not in source


def test_an_empty_probe_is_refused() -> None:
    with pytest.raises(GrammarSourceProbeError, match="ليس فحصًا"):
        derive_probe_outcome(())
