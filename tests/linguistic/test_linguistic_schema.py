"""`Σ_L` مبنيّةٌ على بصمة `Σ_M`، ولا تشارك أصنافَها اسمًا، ولا تحمل نسبةً بعينها."""

from __future__ import annotations

import dataclasses

import pytest

from alghanem.linguistic.schema import (
    LINGUISTIC_NISBAH_SCHEMA,
    LINGUISTIC_SORT_IDS,
    LinguisticNisbahSchema,
    LinguisticNisbahSchemaError,
)
from alghanem.metaalgebra.schema import META_ALGEBRA_SCHEMA
from alghanem.metaalgebra.specification import SchemaRef


def test_the_nucleus_declares_the_seven_general_linguistic_sorts() -> None:
    assert LINGUISTIC_NISBAH_SCHEMA.sort_ids == LINGUISTIC_SORT_IDS
    assert len(LINGUISTIC_SORT_IDS) == 7


def test_no_linguistic_sort_shares_a_name_with_a_meta_sort() -> None:
    assert not set(LINGUISTIC_SORT_IDS) & set(META_ALGEBRA_SCHEMA.sort_ids)


def test_a_nucleus_built_on_another_language_digest_is_refused() -> None:
    with pytest.raises(LinguisticNisbahSchemaError):
        dataclasses.replace(
            LINGUISTIC_NISBAH_SCHEMA,
            meta_schema_ref=SchemaRef(
                schema_version=META_ALGEBRA_SCHEMA.schema_version,
                content_id="0" * len(META_ALGEBRA_SCHEMA.content_id),
            ),
        )


def test_a_nucleus_without_a_single_law_is_not_a_nucleus() -> None:
    with pytest.raises(LinguisticNisbahSchemaError):
        dataclasses.replace(LINGUISTIC_NISBAH_SCHEMA, laws=())


def test_an_absent_sort_is_refused_not_returned_as_silence() -> None:
    with pytest.raises(LinguisticNisbahSchemaError):
        LINGUISTIC_NISBAH_SCHEMA.sort("NoSuchSort")


def test_the_nucleus_is_the_single_declared_instance() -> None:
    assert isinstance(LINGUISTIC_NISBAH_SCHEMA, LinguisticNisbahSchema)
    assert LINGUISTIC_NISBAH_SCHEMA.meta_schema_ref.content_id == (
        META_ALGEBRA_SCHEMA.content_id
    )


def test_the_meta_algebra_keeps_exactly_its_own_four_sorts() -> None:
    assert len(META_ALGEBRA_SCHEMA.sort_ids) == 4
