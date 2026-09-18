"""اختباراتُ تطبيق `G0.LEX-0` على معجم المقاييس المُجمَّد."""

from __future__ import annotations

import pkgutil
from dataclasses import fields
from pathlib import Path

import pytest

import alghanem.kernel as kernel_package
from alghanem.arabic import (
    DerivedMorphologicalCandidate,
    LexicalComparativeStanding,
    LexicalEvidenceSpecificationError,
    LexicalNormalizationTrace,
    NormalizationBranch,
    SignifierCandidate,
    SurfaceOccurrence,
    derive_comparative_standing,
    refuse_numeric_or_verdict_fields,
)
from alghanem.arabic.maqayis_lexical_evidence import (
    BRANCH_RULE_CHAINS,
    MAQAYIS_INDEXING_UNIT,
    MAQAYIS_LEXICON_ID,
    QUOTED_NUMBER_IS_NOT_DERIVED_MEASURE_NOTE,
    REPORTED_RECORD_IS_NOT_CORE_CANDIDATE_NOTE,
    SURFACE_IS_NOT_ROOT_NOTE,
    MaqayisLexicalEvidenceError,
    MaqayisRootEvidence,
    build_root_index,
    evidence_for_match,
    match_derived_root,
    read_root_evidence,
)
from alghanem.arabic.maqayis_root_table_deposit import FROZEN_ROOT_TABLE

_MODULE = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "alghanem"
    / "arabic"
    / "maqayis_lexical_evidence.py"
)


def _derived(
    raw_form: str, proposed_root: str, branch: NormalizationBranch
) -> DerivedMorphologicalCandidate:
    chain = BRANCH_RULE_CHAINS[branch]
    normalized = raw_form
    destroys = ""
    if chain:
        from alghanem.arabic.root_orthography_bridge import normalise_root

        normalized = normalise_root(raw_form, chain).after
        destroys = chain[0].what_it_destroys
    return DerivedMorphologicalCandidate(
        signifier=SignifierCandidate(
            occurrence=SurfaceOccurrence(
                source_id="test",
                occurrence_id=raw_form,
                raw_form=raw_form,
                source_position="1",
                local_position=0,
            ),
            trace=LexicalNormalizationTrace(
                branch=branch,
                raw_form=raw_form,
                normalized_form=normalized,
                what_it_destroys=destroys,
            ),
        ),
        proposed_root=proposed_root,
        derivation_basis="جذرٌ مُصرَّحٌ به في الاختبار",
    )


def test_the_entries_come_from_the_fingerprinted_deposit_not_a_second_reader() -> None:
    source = _MODULE.read_text(encoding="utf-8")
    assert "from .maqayis_root_table_deposit import" in source
    assert "import csv" not in source
    assert "read_bytes" not in source
    assert "open(" not in source
    entries = read_root_evidence()
    assert entries
    assert len({entry.entry_ref for entry in entries}) == len(entries)


def test_a_quoted_number_is_kept_as_source_text_and_never_parsed() -> None:
    entries = read_root_evidence()
    assert all(isinstance(entry.axes_count_as_reported, str) for entry in entries[:50])
    field_types = {field.name: field.type for field in fields(MaqayisRootEvidence)}
    assert all(declared == "str" for declared in field_types.values())
    assert all(name.endswith("_as_reported") for name in field_types)
    assert "QuotedNumberIsNotDerivedMeasure" in (
        QUOTED_NUMBER_IS_NOT_DERIVED_MEASURE_NOTE
    )
    assert "int(" not in _MODULE.read_text(encoding="utf-8")


def test_the_reported_record_is_deliberately_outside_the_core_candidates() -> None:
    with pytest.raises(LexicalEvidenceSpecificationError):
        refuse_numeric_or_verdict_fields(MaqayisRootEvidence)
    assert "ReportedRecordIsNotCoreCandidate" in (
        REPORTED_RECORD_IS_NOT_CORE_CANDIDATE_NOTE
    )


def test_matching_passes_through_a_derived_root_and_never_the_raw_surface() -> None:
    index = build_root_index(NormalizationBranch.EXACT)
    matches = match_derived_root(
        _derived("كَتَبَ", "كتب", NormalizationBranch.EXACT), index
    )
    assert matches
    assert all(match.indexing_unit == MAQAYIS_INDEXING_UNIT for match in matches)
    assert all(match.lexicon_id == MAQAYIS_LEXICON_ID for match in matches)
    assert all(match.exact_form == "كَتَبَ" for match in matches)
    with pytest.raises(MaqayisLexicalEvidenceError) as error:
        match_derived_root("كتب", index)  # type: ignore[arg-type]
    assert "SurfaceIsNotRoot" in str(error.value)
    assert "SurfaceIsNotRoot" in SURFACE_IS_NOT_ROOT_NOTE


def test_a_signifier_normalized_under_one_branch_never_matches_another() -> None:
    index = build_root_index(NormalizationBranch.EXACT)
    with pytest.raises(MaqayisLexicalEvidenceError):
        match_derived_root(
            _derived("حَدَأَة", "حدأ", NormalizationBranch.NORMALIZE_TO_ALIF), index
        )


def test_each_branch_keeps_its_own_index_and_shows_its_own_price() -> None:
    prices = {}
    for branch in NormalizationBranch:
        index = build_root_index(branch)
        assert index.branch is branch
        prices[branch] = index.fusions
        if branch is NormalizationBranch.EXACT:
            assert index.rule_chain == ()
            assert index.what_it_destroys == ()
            assert index.fusions == ()
        else:
            assert index.rule_chain
            assert all(text for text in index.what_it_destroys)
    bare = dict(prices[NormalizationBranch.NORMALIZE_TO_ALIF])
    assert bare, "القاعدةُ الأوسعُ إتلافًا لا بدّ أن تُظهر ثمنَها بأعيانه"
    assert all(len(sources) >= 2 for sources in bare.values())


def test_the_bare_alif_branch_produces_a_recordable_ambiguity() -> None:
    index = build_root_index(NormalizationBranch.NORMALIZE_TO_ALIF)
    matches = match_derived_root(
        _derived("حَدَأَة", "حدأ", NormalizationBranch.NORMALIZE_TO_ALIF), index
    )
    exact = build_root_index(NormalizationBranch.EXACT)
    exact_matches = match_derived_root(
        _derived("حَدَأَة", "حدأ", NormalizationBranch.EXACT), exact
    )
    assert len(matches) > len(exact_matches)


def test_the_evidence_carries_its_bytes_digest_and_is_not_a_meaning() -> None:
    index = build_root_index(NormalizationBranch.EXACT)
    entries = {entry.entry_ref: entry for entry in read_root_evidence()}
    match = match_derived_root(
        _derived("كَتَبَ", "كتب", NormalizationBranch.EXACT), index
    )[0]
    evidence = evidence_for_match(match, entries[match.matched_entry_ref])
    assert evidence.is_a_meaning is False
    assert FROZEN_ROOT_TABLE.sha256_hex in evidence.source_trace
    assert "ALexiconIsAWitnessNotAnAuthority" in evidence.source_trace
    assert "RootEvidenceIsNotSurfaceMeaning" in evidence.source_trace
    assert "NoRetroactivePreregistrationOfMaqayis" in evidence.source_trace


def test_evidence_is_never_raised_over_an_entry_other_than_the_matched_one() -> None:
    index = build_root_index(NormalizationBranch.EXACT)
    entries = read_root_evidence()
    match = match_derived_root(
        _derived("كَتَبَ", "كتب", NormalizationBranch.EXACT), index
    )[0]
    other = next(
        entry for entry in entries if entry.entry_ref != match.matched_entry_ref
    )
    with pytest.raises(MaqayisLexicalEvidenceError):
        evidence_for_match(match, other)


def test_a_root_indexed_lexicon_is_not_comparable_to_a_surface_comparator() -> None:
    standing = derive_comparative_standing(
        lexicon_indexing_unit=MAQAYIS_INDEXING_UNIT,
        comparator_indexing_unit="surface",
        lexical_reached=True,
        comparator_reached=False,
    )
    assert standing is LexicalComparativeStanding.NOT_COMPARABLE


def test_the_module_is_named_a_specification_never_a_preregistration() -> None:
    assert "preregistration" not in _MODULE.read_text(encoding="utf-8")


def test_the_core_layer_does_not_import_this_adapter() -> None:
    arabic = _MODULE.parent
    for name in ("lexical_evidence_layer", "lexical_evidence_specification"):
        source = (arabic / f"{name}.py").read_text(encoding="utf-8")
        imports = tuple(
            line
            for line in source.splitlines()
            if line.startswith(("import ", "from "))
        )
        assert imports
        assert not any("maqayis" in line.lower() for line in imports), name


def test_the_adapter_imports_no_kernel_authority() -> None:
    imports = tuple(
        line
        for line in _MODULE.read_text(encoding="utf-8").splitlines()
        if line.startswith(("import ", "from "))
    )
    assert imports
    assert not any("kernel" in line for line in imports)


def test_no_kernel_module_reads_this_adapter() -> None:
    for module in pkgutil.walk_packages(
        kernel_package.__path__, prefix="alghanem.kernel."
    ):
        spec = module.module_finder.find_spec(module.name)  # type: ignore[union-attr]
        assert spec is not None and spec.origin is not None
        text = Path(spec.origin).read_text(encoding="utf-8")
        for name in ("maqayis_lexical_evidence", "MaqayisRootEvidence"):
            assert name not in text, (module.name, name)


def test_the_module_declares_it_is_a_registration_not_an_authority() -> None:
    assert "تسجيلٌ لا سلطة" in _MODULE.read_text(encoding="utf-8")
