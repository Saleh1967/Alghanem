"""Tests for the enforced cross-project OriginType import contract."""

from __future__ import annotations

import pkgutil
from dataclasses import fields, replace
from typing import Any

import pytest

import alghanem.kernel as kernel_package
from alghanem.arabic import (
    EXPECTED_DISTRIBUTION,
    EXPECTED_ROW_COUNT,
    LOCAL_CANONICALIZATION_VERSION,
    SOURCE_CANONICALIZATION_VERSION,
    SOURCE_DECLARED_CONTENT_ID,
    SOURCE_DIGEST_COVERED_FIELDS,
    SOURCE_LEDGER_ID,
    SOURCE_PROJECT,
    SOURCE_VOCABULARY_ID,
    EvidenceGenus,
    ForeignFreezeScope,
    ImportedFeatureVocabulary,
    ImportedFeatureVocabularyError,
    ImportedOriginType,
    ImportedVocabularyContentVerifier,
    ImportedVocabularyEntry,
    LocalVocabularyContentIdentity,
    SpecificationFreeze,
    VerifiedVocabularyImport,
    assert_matches_recorded_release,
    canonical_origin_type,
    vocabulary_from_export_mapping,
)

_ROOTS = ("لزم", "زلف", "كتب")
_TYPES = (
    ImportedOriginType.EVENT,
    ImportedOriginType.UNRESOLVED,
    ImportedOriginType.ENTITY,
)


def entries(count: int = 3) -> tuple[ImportedVocabularyEntry, ...]:
    return tuple(
        ImportedVocabularyEntry(
            root=_ROOTS[index],
            origin_type=_TYPES[index],
            raw_category="MASDAR",
            batch_note="batch_seed31415",
        )
        for index in range(count)
    )


def vocabulary(**overrides: Any) -> ImportedFeatureVocabulary:
    declared = entries() if "entries" not in overrides else overrides["entries"]
    counts = {member: 0 for member in ImportedOriginType}
    for entry in declared:
        counts[entry.origin_type] += 1
    base: dict[str, Any] = dict(
        vocabulary_id=SOURCE_VOCABULARY_ID,
        evidence_genus=EvidenceGenus.MORPHO_FUNCTIONAL,
        source_project=SOURCE_PROJECT,
        source_ledger_id=SOURCE_LEDGER_ID,
        source_canonicalization_version=SOURCE_CANONICALIZATION_VERSION,
        source_declared_content_id=SOURCE_DECLARED_CONTENT_ID,
        freeze_scope=ForeignFreezeScope.FROZEN_LOCAL,
        declared_row_count=len(declared),
        declared_distribution=tuple(
            (member, counts[member]) for member in ImportedOriginType
        ),
        entries=declared,
    )
    base.update(overrides)
    return ImportedFeatureVocabulary(**base)


def payload(**overrides: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "vocabulary_id": SOURCE_VOCABULARY_ID,
        "genus": "MORPHO_FUNCTIONAL",
        "source_project": SOURCE_PROJECT,
        "source_ledger_id": SOURCE_LEDGER_ID,
        "row_count": 3,
        "content_id": SOURCE_DECLARED_CONTENT_ID,
        "canonicalization_version": SOURCE_CANONICALIZATION_VERSION,
        "freeze_scope": "FROZEN_LOCAL",
        "declared_distribution": {
            "ORIGIN_TYPE_EVENT": 1,
            "ORIGIN_TYPE_UNRESOLVED": 1,
            "ORIGIN_TYPE_ENTITY": 1,
        },
        "entries": [
            {
                "root": _ROOTS[index],
                "origin_type": _TYPES[index].value,
                "raw_category": "MASDAR",
                "batch_note": "batch_seed31415",
            }
            for index in range(3)
        ],
    }
    base.update(overrides)
    return base


def test_the_import_is_bound_to_the_morpho_functional_genus() -> None:
    assert vocabulary().evidence_genus is EvidenceGenus.MORPHO_FUNCTIONAL
    with pytest.raises(ImportedFeatureVocabularyError):
        vocabulary(evidence_genus=EvidenceGenus.DISTRIBUTIONAL)


def test_the_local_digest_is_rederived_and_deterministic() -> None:
    first = ImportedVocabularyContentVerifier.verify(vocabulary())
    second = ImportedVocabularyContentVerifier.verify(vocabulary())
    assert first.local_content_id.digest == second.local_content_id.digest
    assert first.content_bytes == second.content_bytes
    assert (
        first.local_content_id.canonicalization_version
        == LOCAL_CANONICALIZATION_VERSION
    )


def test_a_tampered_entry_changes_the_rederived_digest() -> None:
    original = ImportedVocabularyContentVerifier.verify(vocabulary())
    tampered_entries = (
        replace(entries()[0], origin_type=ImportedOriginType.ENTITY),
    ) + entries()[1:]
    tampered = ImportedVocabularyContentVerifier.verify(
        vocabulary(entries=tampered_entries)
    )
    assert tampered.local_content_id.digest != original.local_content_id.digest


def test_the_source_digest_alone_never_stands_for_the_local_one() -> None:
    verified = ImportedVocabularyContentVerifier.verify(vocabulary())
    assert verified.source_declared_content_id == SOURCE_DECLARED_CONTENT_ID
    assert verified.local_content_id.digest != SOURCE_DECLARED_CONTENT_ID


def test_a_verified_import_is_unconstructible_outside_the_verifier() -> None:
    verified = ImportedVocabularyContentVerifier.verify(vocabulary())
    with pytest.raises(ImportedFeatureVocabularyError):
        VerifiedVocabularyImport(
            vocabulary=verified.vocabulary,
            content_bytes=verified.content_bytes,
            local_content_id=verified.local_content_id,
        )
    with pytest.raises(ImportedFeatureVocabularyError):
        LocalVocabularyContentIdentity(
            algorithm="sha256",
            canonicalization_version=LOCAL_CANONICALIZATION_VERSION,
            digest=verified.local_content_id.digest,
        )


def test_the_distribution_is_derived_and_a_declared_mismatch_is_refused() -> None:
    imported = vocabulary()
    assert dict(imported.derived_distribution) == {
        ImportedOriginType.EVENT: 1,
        ImportedOriginType.ENTITY: 1,
        ImportedOriginType.UNRESOLVED: 1,
    }
    with pytest.raises(ImportedFeatureVocabularyError):
        vocabulary(
            declared_distribution=(
                (ImportedOriginType.EVENT, 3),
                (ImportedOriginType.ENTITY, 0),
                (ImportedOriginType.UNRESOLVED, 0),
            )
        )
    with pytest.raises(ImportedFeatureVocabularyError):
        vocabulary(declared_row_count=270)


def test_an_unknown_origin_type_is_refused_not_folded_into_unresolved() -> None:
    with pytest.raises(ImportedFeatureVocabularyError):
        canonical_origin_type("ORIGIN_TYPE_PROCESS")
    assert canonical_origin_type("ORIGIN_TYPE_UNRESOLVED") is (
        ImportedOriginType.UNRESOLVED
    )
    with pytest.raises(ImportedFeatureVocabularyError):
        vocabulary_from_export_mapping(
            payload(
                entries=[
                    {
                        "root": "لزم",
                        "origin_type": "ORIGIN_TYPE_PROCESS",
                        "raw_category": "MASDAR",
                        "batch_note": "batch_seed31415",
                    }
                ]
            )
        )


def test_a_duplicate_root_is_refused() -> None:
    duplicated = entries()[:1] * 2
    with pytest.raises(ImportedFeatureVocabularyError):
        vocabulary(entries=duplicated)


def test_an_export_mapping_round_trips_through_the_closed_vocabularies() -> None:
    imported = vocabulary_from_export_mapping(payload())
    assert imported.freeze_scope is ForeignFreezeScope.FROZEN_LOCAL
    assert imported.row_count == 3
    with pytest.raises(ImportedFeatureVocabularyError):
        vocabulary_from_export_mapping(payload(freeze_scope="FROZEN"))
    with pytest.raises(ImportedFeatureVocabularyError):
        vocabulary_from_export_mapping(payload(genus="DISTRIBUTIONAL"))
    incomplete = payload()
    del incomplete["content_id"]
    with pytest.raises(ImportedFeatureVocabularyError):
        vocabulary_from_export_mapping(incomplete)


def test_the_recorded_release_counts_are_pinned() -> None:
    assert EXPECTED_ROW_COUNT == 270
    assert EXPECTED_DISTRIBUTION == {
        ImportedOriginType.EVENT: 126,
        ImportedOriginType.ENTITY: 56,
        ImportedOriginType.UNRESOLVED: 88,
    }
    with pytest.raises(ImportedFeatureVocabularyError):
        assert_matches_recorded_release(vocabulary())
    with pytest.raises(ImportedFeatureVocabularyError):
        assert_matches_recorded_release(vocabulary(vocabulary_id="other.v1"))


def test_the_foreign_scope_is_not_a_local_freeze() -> None:
    assert {member.name for member in ForeignFreezeScope} == {"FROZEN_LOCAL"}
    assert ForeignFreezeScope.FROZEN_LOCAL.name not in {
        member.name for member in SpecificationFreeze
    }
    assert ForeignFreezeScope.FROZEN_LOCAL is not SpecificationFreeze.FROZEN


def test_no_imported_type_carries_a_result_or_birth_field() -> None:
    markers = ("result", "outcome", "answer", "verdict", "birth", "promotion")
    for declaring in (ImportedFeatureVocabulary, ImportedVocabularyEntry):
        for item in fields(declaring):
            assert not any(marker in item.name for marker in markers)


def test_no_kernel_module_reads_the_import_contract() -> None:
    for module in pkgutil.walk_packages(
        kernel_package.__path__, prefix=f"{kernel_package.__name__}."
    ):
        source = module.module_finder.find_spec(  # type: ignore[union-attr]
            module.name
        )
        assert source is not None and source.origin is not None
        with open(source.origin, encoding="utf-8") as handle:
            assert "imported_feature_vocabulary" not in handle.read()


def test_the_local_identity_covers_strictly_more_than_the_source_digest() -> None:
    assert set(SOURCE_DIGEST_COVERED_FIELDS) == {"root", "origin_type"}
    entry_fields = {item.name for item in fields(ImportedVocabularyEntry)}
    assert set(SOURCE_DIGEST_COVERED_FIELDS) < entry_fields
    original = ImportedVocabularyContentVerifier.verify(vocabulary())
    uncovered = (replace(entries()[0], raw_category="JAMID"),) + entries()[1:]
    changed = ImportedVocabularyContentVerifier.verify(vocabulary(entries=uncovered))
    assert changed.local_content_id.digest != original.local_content_id.digest
    assert changed.source_declared_content_id == original.source_declared_content_id
