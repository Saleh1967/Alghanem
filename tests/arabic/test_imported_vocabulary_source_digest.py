"""Tests for the byte-precise re-derivation of the declared source digest."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import pytest

from alghanem.arabic import (
    EXPECTED_DISTRIBUTION,
    EXPECTED_ROW_COUNT,
    SOURCE_CANONICALIZATION_VERSION,
    SOURCE_DECLARED_CONTENT_ID,
    SOURCE_DIGEST_COVERED_FIELDS,
    SOURCE_FIELD_SEPARATOR,
    SOURCE_LEDGER_ID,
    SOURCE_PROJECT,
    SOURCE_RECORD_SEPARATOR,
    SOURCE_VOCABULARY_ID,
    EvidenceGenus,
    ForeignFreezeScope,
    ImportedFeatureVocabulary,
    ImportedOriginType,
    ImportedVocabularyEntry,
    RederivedSourceContentIdentity,
    SourceDigestMismatchError,
    SourceDigestSchemaError,
    source_canonical_bytes,
    source_content_id,
    source_digest_pairs,
    verify_export_payload,
    verify_source_declared_content_id,
)

EXPORT_FIXTURE = Path(__file__).parent / "fixtures" / "origin_type_export_v1.json"

REFERENCE_PAIRS = (
    ("لزم", "ORIGIN_TYPE_EVENT"),
    ("زلف", "ORIGIN_TYPE_UNRESOLVED"),
)

REFERENCE_BYTES = ("زلف\x1fORIGIN_TYPE_UNRESOLVED\x1eلزم\x1fORIGIN_TYPE_EVENT").encode()


def entries(
    pairs: tuple[tuple[str, str], ...] = REFERENCE_PAIRS,
) -> tuple[ImportedVocabularyEntry, ...]:
    return tuple(
        ImportedVocabularyEntry(
            root=root,
            origin_type=ImportedOriginType(origin_type),
            raw_category="MASDAR",
            batch_note="batch_seed31415",
        )
        for root, origin_type in pairs
    )


def vocabulary(**overrides: Any) -> ImportedFeatureVocabulary:
    declared = overrides.pop("entries", entries())
    counts = {member: 0 for member in ImportedOriginType}
    for entry in declared:
        counts[entry.origin_type] += 1
    fields: dict[str, Any] = {
        "vocabulary_id": SOURCE_VOCABULARY_ID,
        "evidence_genus": EvidenceGenus.MORPHO_FUNCTIONAL,
        "source_project": SOURCE_PROJECT,
        "source_ledger_id": SOURCE_LEDGER_ID,
        "source_canonicalization_version": SOURCE_CANONICALIZATION_VERSION,
        "source_declared_content_id": source_content_id(
            (entry.root, entry.origin_type.value) for entry in declared
        ),
        "freeze_scope": ForeignFreezeScope.FROZEN_LOCAL,
        "declared_row_count": len(declared),
        "declared_distribution": tuple(
            (member, counts[member]) for member in ImportedOriginType
        ),
        "entries": declared,
    }
    fields.update(overrides)
    return ImportedFeatureVocabulary(**fields)


def test_reference_pairs_encode_to_the_declared_byte_layout() -> None:
    encoded = source_canonical_bytes(REFERENCE_PAIRS)

    assert encoded == REFERENCE_BYTES
    assert encoded.count(SOURCE_FIELD_SEPARATOR.encode("utf-8")) == 2
    assert encoded.count(SOURCE_RECORD_SEPARATOR.encode("utf-8")) == 1
    assert not encoded.startswith(b"\xef\xbb\xbf")
    assert (
        source_content_id(REFERENCE_PAIRS)
        == hashlib.sha256(REFERENCE_BYTES).hexdigest()
    )


def test_entry_order_does_not_change_the_source_digest() -> None:
    assert source_canonical_bytes(reversed(REFERENCE_PAIRS)) == REFERENCE_BYTES


def test_no_additional_unicode_normalization_is_applied() -> None:
    composed = source_canonical_bytes((("\u0622", "ORIGIN_TYPE_ENTITY"),))
    decomposed = source_canonical_bytes((("\u0627\u0653", "ORIGIN_TYPE_ENTITY"),))

    assert composed != decomposed


def test_separators_inside_a_field_are_refused() -> None:
    for injected in (SOURCE_FIELD_SEPARATOR, SOURCE_RECORD_SEPARATOR):
        with pytest.raises(SourceDigestSchemaError):
            source_canonical_bytes(((f"لز{injected}م", "ORIGIN_TYPE_EVENT"),))


def test_malformed_pairs_are_refused() -> None:
    with pytest.raises(SourceDigestSchemaError):
        source_canonical_bytes(((("لزم", "ORIGIN_TYPE_EVENT", "extra")),))  # type: ignore[arg-type]
    with pytest.raises(SourceDigestSchemaError):
        source_canonical_bytes((("  ", "ORIGIN_TYPE_EVENT"),))
    with pytest.raises(SourceDigestSchemaError):
        source_canonical_bytes((("لزم", "ORIGIN_TYPE_UNKNOWN"),))
    with pytest.raises(SourceDigestSchemaError):
        source_canonical_bytes(())


def test_duplicate_roots_are_refused() -> None:
    with pytest.raises(SourceDigestSchemaError):
        source_canonical_bytes(
            (("لزم", "ORIGIN_TYPE_EVENT"), ("لزم", "ORIGIN_TYPE_ENTITY"))
        )


def test_source_digest_pairs_cover_only_the_two_attested_fields() -> None:
    assert source_digest_pairs(vocabulary()) == REFERENCE_PAIRS
    assert SOURCE_DIGEST_COVERED_FIELDS == ("root", "origin_type")


def test_verification_rederives_the_declared_digest() -> None:
    identity = verify_source_declared_content_id(vocabulary())

    assert identity.digest == source_content_id(REFERENCE_PAIRS)
    assert identity.canonicalization_version == SOURCE_CANONICALIZATION_VERSION
    assert identity.covered_fields == SOURCE_DIGEST_COVERED_FIELDS
    assert identity.row_count == len(REFERENCE_PAIRS)


def test_a_rederived_identity_cannot_be_minted_outside_verification() -> None:
    with pytest.raises(SourceDigestSchemaError):
        RederivedSourceContentIdentity(
            algorithm="sha256",
            canonicalization_version=SOURCE_CANONICALIZATION_VERSION,
            digest=source_content_id(REFERENCE_PAIRS),
            covered_fields=SOURCE_DIGEST_COVERED_FIELDS,
            row_count=len(REFERENCE_PAIRS),
        )


def test_a_changed_payload_is_refused_with_both_causes_named() -> None:
    tampered = vocabulary(
        entries=entries(
            (("لزم", "ORIGIN_TYPE_ENTITY"), ("زلف", "ORIGIN_TYPE_UNRESOLVED"))
        ),
        source_declared_content_id=source_content_id(REFERENCE_PAIRS),
    )

    with pytest.raises(SourceDigestMismatchError) as error:
        verify_source_declared_content_id(tampered)

    message = str(error.value)
    assert tampered.source_declared_content_id in message
    assert "المخطَّط المُطبَّق مختلف" in message
    assert "ليست حمولة الإصدار المُثبَّت" in message


def test_an_unrecorded_canonicalization_version_is_refused() -> None:
    with pytest.raises(SourceDigestSchemaError):
        verify_source_declared_content_id(
            vocabulary(source_canonicalization_version="gflk.canonical.v2")
        )


def test_verification_requires_an_imported_vocabulary() -> None:
    with pytest.raises(SourceDigestSchemaError):
        verify_source_declared_content_id(object())  # type: ignore[arg-type]
    with pytest.raises(SourceDigestSchemaError):
        source_digest_pairs(object())  # type: ignore[arg-type]


def test_rederivation_grants_no_local_freeze_or_birth() -> None:
    identity = verify_source_declared_content_id(vocabulary())

    assert not hasattr(identity, "freeze_scope")
    assert not any(
        marker in name
        for name in identity.__dataclass_fields__
        for marker in ("freeze", "birth", "verdict", "authority")
    )


@pytest.mark.skipif(
    not EXPORT_FIXTURE.exists(),
    reason=(
        "the full 270-row source export payload is not deposited in this "
        "repository yet; drop it at tests/arabic/fixtures/"
        "origin_type_export_v1.json to run the independent re-derivation"
    ),
)
def test_recorded_release_digest_is_rederived_from_the_deposited_export() -> None:
    payload = json.loads(EXPORT_FIXTURE.read_text(encoding="utf-8"))

    identity = verify_export_payload(payload)

    assert identity.digest == SOURCE_DECLARED_CONTENT_ID
    assert identity.row_count == EXPECTED_ROW_COUNT
    assert sum(EXPECTED_DISTRIBUTION.values()) == EXPECTED_ROW_COUNT
