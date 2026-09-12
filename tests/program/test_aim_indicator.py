"""Tests for the sixth AIM.1 milestone: the derived aim-to-source indicator."""

from __future__ import annotations

import pkgutil
from dataclasses import fields, replace
from types import MappingProxyType

import pytest

import alghanem.kernel as kernel_package
from alghanem.program import (
    AIM_INDICATOR_AUTHORITY_NOTE,
    AIM_INDICATOR_NAMED_RESIDUALS,
    AIM_RECORDS,
    CITATION_LINK_IS_NOT_ATTAINMENT,
    CITATION_PROSE_IS_NOT_A_TOKEN_STREAM,
    DEFERRED_VALUE_READER_IS_NOT_REACHED_BY_ANY_CITATION,
    LEDGER_COUNT_MOVEMENT_IS_NOT_AIM_MOVEMENT,
    AimCitationLink,
    AimId,
    AimIndicator,
    AimIndicatorError,
    AttainmentStanding,
    CitationCensus,
    CitedSourceGenus,
    CitedTokenShape,
    ReadCitation,
    derive_aim_indicator,
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
    "result",
    "outcome",
    "birth",
    "promotion",
    "indicator",
    "score",
    "percent",
    "estimate",
    "priority",
    "attainment",
)


def test_every_recorded_aim_is_linked_to_its_own_citation() -> None:
    indicator = derive_aim_indicator()
    assert indicator.linked_aim_count == len(AIM_RECORDS)
    assert tuple(link.aim_id for link in indicator.links) == tuple(AIM_RECORDS)
    for link in indicator.links:
        assert link.tokens
        for token in link.tokens:
            assert token.aim_id is link.aim_id


def test_the_census_holds_every_token_of_every_link() -> None:
    indicator = derive_aim_indicator()
    linked = tuple(token for link in indicator.links for token in link.tokens)
    assert indicator.citations.tokens == linked
    assert indicator.citations.token_count == len(linked)
    read = indicator.citations.read_tokens
    excluded = indicator.citations.excluded_tokens
    assert len(read) + len(excluded) == indicator.citations.token_count
    assert all(token.is_read_in_a_ledger for token in read)
    assert not any(token.is_read_in_a_ledger for token in excluded)


def test_every_declared_genus_and_shape_is_counted_even_at_zero() -> None:
    indicator = derive_aim_indicator()
    genus_counts = indicator.citations.genus_counts
    assert set(genus_counts) == set(CitedSourceGenus) - {
        CitedSourceGenus.NO_LEDGER_READABLE_SOURCE
    }
    assert genus_counts[CitedSourceGenus.DEFERRED_VALUE_SITE] == 0
    assert set(indicator.citations.shape_counts) == set(CitedTokenShape)
    assert sum(genus_counts.values()) == indicator.citations.token_count
    assert (
        sum(indicator.citations.shape_counts.values())
        == indicator.citations.token_count
    )


def test_the_third_reader_is_read_and_its_absence_is_a_named_residual() -> None:
    indicator = derive_aim_indicator()
    assert indicator.reached_references(CitedSourceGenus.DEFERRED_VALUE_SITE) == ()
    assert (
        DEFERRED_VALUE_READER_IS_NOT_REACHED_BY_ANY_CITATION
        in AIM_INDICATOR_NAMED_RESIDUALS
    )


def test_an_aim_without_a_ledger_readable_source_carries_the_ignorance_member() -> None:
    indicator = derive_aim_indicator()
    unbacked = indicator.aims_without_ledger_readable_source
    assert unbacked == (AimId.A1, AimId.E2)
    for aim_id in unbacked:
        link = indicator.link(aim_id)
        assert link.ledger_backed_genera == (
            CitedSourceGenus.NO_LEDGER_READABLE_SOURCE,
        )
        assert link.has_ledger_readable_source is False
        assert link.law_row_count == 0
        assert link.audit_question_count == 0
        assert link.deferred_value_count == 0


def test_reader_counts_stay_separate_and_are_never_summed() -> None:
    indicator = derive_aim_indicator()
    link = indicator.link(AimId.T1)
    assert link.audit_question_count == 3
    assert link.law_row_count == 0
    assert not hasattr(link, "total_count")
    assert not hasattr(indicator, "total_count")
    field_names = {item.name for item in fields(AimCitationLink)}
    assert not any("count" in name for name in field_names)


def test_a_row_identifier_resolves_to_its_own_row_and_not_to_its_sibling() -> None:
    indicator = derive_aim_indicator()
    assert indicator.link(AimId.K2).law_rows == (
        "G0.BV.1 authority-issued birth verdict",
        "G0.BV.1a gate-derived scoped deferral",
    )


def test_a_section_citation_is_excluded_by_a_declared_genus_not_read_as_a_row() -> None:
    indicator = derive_aim_indicator()
    sections = [
        token
        for token in indicator.link(AimId.K4).tokens
        if token.genus is CitedSourceGenus.CONSTITUTION_SECTION
    ]
    assert [token.text for token in sections] == ["G0.F.1"]
    assert sections[0].is_read_in_a_ledger is False
    assert sections[0].reference.startswith("G0.F.1 —")


def test_a_name_written_without_its_backticks_still_reaches_its_row() -> None:
    indicator = derive_aim_indicator()
    assert indicator.link(AimId.E1).law_rows == (
        "`DeferPreservesOpenQuestion`",
        "`NoIndexFeedbackIntoDiscovery`",
    )


def test_a_token_joined_to_arabic_prose_is_read_and_not_skipped() -> None:
    record = replace(AIM_RECORDS[AimId.K2], citation="صفّا G0.BV.1 وG0.BV.1a")
    indicator = derive_aim_indicator(records=MappingProxyType({AimId.K2: record}))
    assert indicator.link(AimId.K2).law_rows == (
        "G0.BV.1 authority-issued birth verdict",
        "G0.BV.1a gate-derived scoped deferral",
    )


def test_a_token_without_a_reference_is_refused_by_name_and_position() -> None:
    record = replace(AIM_RECORDS[AimId.K2], citation="docs/CONSTITUTION.md، صفّ G0.ZZ.9")
    with pytest.raises(AimIndicatorError) as error:
        derive_aim_indicator(records=MappingProxyType({AimId.K2: record}))
    assert "G0.ZZ.9" in str(error.value)
    assert "AIM-K2" in str(error.value)


def test_an_unknown_name_is_refused_rather_than_read_as_an_absent_source() -> None:
    record = replace(
        AIM_RECORDS[AimId.T2], citation="docs/CONSTITUTION.md، `NoSuchAuditQuestion`"
    )
    with pytest.raises(AimIndicatorError):
        derive_aim_indicator(records=MappingProxyType({AimId.T2: record}))


def test_a_path_that_does_not_exist_is_refused_not_excluded_in_silence() -> None:
    record = replace(AIM_RECORDS[AimId.A1], citation="src/alghanem/arabic/nowhere/")
    with pytest.raises(AimIndicatorError):
        derive_aim_indicator(records=MappingProxyType({AimId.A1: record}))


def test_a_citation_with_no_declared_token_shape_is_refused() -> None:
    record = replace(AIM_RECORDS[AimId.A1], citation="صفوف الدستور كلُّها")
    with pytest.raises(AimIndicatorError):
        derive_aim_indicator(records=MappingProxyType({AimId.A1: record}))


def test_the_ignorance_member_is_not_a_token_genus() -> None:
    indicator = derive_aim_indicator()
    token = indicator.citations.tokens[0]
    with pytest.raises(AimIndicatorError):
        replace(token, genus=CitedSourceGenus.NO_LEDGER_READABLE_SOURCE)
    with pytest.raises(AimIndicatorError):
        indicator.link(AimId.A1).references_of_genus(
            CitedSourceGenus.NO_LEDGER_READABLE_SOURCE
        )
    with pytest.raises(AimIndicatorError):
        indicator.reached_references(CitedSourceGenus.NO_LEDGER_READABLE_SOURCE)


def test_a_token_is_not_attributed_to_another_aim() -> None:
    indicator = derive_aim_indicator()
    link = indicator.link(AimId.K2)
    stranger = replace(link.tokens[0], aim_id=AimId.K3)
    with pytest.raises(AimIndicatorError):
        AimCitationLink(aim_id=AimId.K2, tokens=(stranger,))


def test_tokens_keep_the_order_in_which_the_citation_wrote_them() -> None:
    indicator = derive_aim_indicator()
    link = indicator.link(AimId.K2)
    with pytest.raises(AimIndicatorError):
        AimCitationLink(aim_id=AimId.K2, tokens=tuple(reversed(link.tokens)))


def test_a_census_that_disagrees_with_its_links_is_refused() -> None:
    indicator = derive_aim_indicator()
    with pytest.raises(AimIndicatorError):
        AimIndicator(
            links=indicator.links,
            citations=CitationCensus(tokens=indicator.citations.tokens[1:]),
        )


def test_an_aim_is_not_linked_twice() -> None:
    indicator = derive_aim_indicator()
    link = indicator.link(AimId.K2)
    with pytest.raises(AimIndicatorError):
        AimIndicator(
            links=(link, link),
            citations=CitationCensus(tokens=link.tokens + link.tokens),
        )


def test_a_missing_link_is_refused_by_name_and_not_returned_as_none() -> None:
    record = AIM_RECORDS[AimId.K2]
    indicator = derive_aim_indicator(records=MappingProxyType({AimId.K2: record}))
    with pytest.raises(AimIndicatorError):
        indicator.link(AimId.T1)


def test_a_record_filed_under_another_key_is_refused() -> None:
    with pytest.raises(AimIndicatorError):
        derive_aim_indicator(
            records=MappingProxyType({AimId.K3: AIM_RECORDS[AimId.K2]})
        )


def test_no_indicator_type_carries_a_result_or_attainment_field() -> None:
    for declaring_type in (ReadCitation, CitationCensus, AimCitationLink, AimIndicator):
        for item in fields(declaring_type):
            assert not any(marker in item.name for marker in _ANSWER_MARKERS), item.name


def test_the_indicator_neither_promotes_nor_writes_attainment() -> None:
    indicator = derive_aim_indicator()
    text = "".join(
        value
        for value in (indicator_module.__doc__, AIM_INDICATOR_AUTHORITY_NOTE)
        if value is not None
    )
    assert "AttainmentStanding" not in [
        type(getattr(link, "attainment", None)).__name__ for link in indicator.links
    ]
    assert AttainmentStanding.REACHED not in tuple(
        getattr(link, "attainment", None) for link in indicator.links
    )
    assert "لا ترقية" in text or "لا يرفع غايةً إلى بلوغ" in text
    for name in dir(indicator_module):
        assert "freeze" not in name.lower()
        assert "verdict" not in name.lower()


def test_the_aims_keep_their_recorded_order_and_are_not_ranked_by_count() -> None:
    indicator = derive_aim_indicator()
    counts = [link.law_row_count for link in indicator.links]
    assert counts != sorted(counts, reverse=True) or len(set(counts)) == 1


def test_the_module_cites_its_direct_design_source() -> None:
    assert indicator_module.__doc__ is not None
    assert DESIGN_SOURCE_OPEN_QUESTION in indicator_module.__doc__


def test_named_residuals_are_recorded_in_code_not_prose_alone() -> None:
    assert set(AIM_INDICATOR_NAMED_RESIDUALS) == {
        CITATION_LINK_IS_NOT_ATTAINMENT,
        CITATION_PROSE_IS_NOT_A_TOKEN_STREAM,
        LEDGER_COUNT_MOVEMENT_IS_NOT_AIM_MOVEMENT,
        DEFERRED_VALUE_READER_IS_NOT_REACHED_BY_ANY_CITATION,
    }
    for text in AIM_INDICATOR_NAMED_RESIDUALS.values():
        assert text.strip()


def test_no_kernel_module_reads_the_programme_layer() -> None:
    for module in pkgutil.walk_packages(
        kernel_package.__path__, prefix="alghanem.kernel."
    ):
        source = module.module_finder.find_spec(  # type: ignore[union-attr]
            module.name
        )
        assert source is not None and source.origin is not None
        with open(source.origin, encoding="utf-8") as handle:
            text = handle.read()
        assert "alghanem.program" not in text, module.name
        assert "AimIndicator" not in text, module.name
        assert "derive_aim_indicator" not in text, module.name
