"""`Σ_M` لغةٌ لا نظريّة: أصنافٌ نحويّةٌ وقوانين، بصفر طبقاتٍ وانتقالات."""

from __future__ import annotations

from dataclasses import fields

import pytest

from alghanem.metaalgebra.layer import LAYER_COMPONENT_NAMES, LayerSignature
from alghanem.metaalgebra.schema import (
    META_ALGEBRA_SCHEMA,
    SCHEMA_VERSION,
    MetaAlgebraSchema,
    MetaAlgebraSchemaError,
    SchemaLaw,
    SortDeclaration,
)
from alghanem.metaalgebra.transition import (
    TRANSITION_COMPONENT_NAMES,
    TransitionSignature,
)


def test_the_schema_carries_no_concrete_structure() -> None:
    field_types = {field.name: field.type for field in fields(MetaAlgebraSchema)}
    assert "layers" not in field_types
    assert "transitions" not in field_types
    for sort in META_ALGEBRA_SCHEMA.sorts:
        assert not isinstance(sort, LayerSignature | TransitionSignature)


def test_component_names_come_from_one_source_not_a_second_copy() -> None:
    assert META_ALGEBRA_SCHEMA.sort("Layer").component_names == LAYER_COMPONENT_NAMES
    assert META_ALGEBRA_SCHEMA.sort(
        "Transition"
    ).component_names == TRANSITION_COMPONENT_NAMES + ("handoff",)


def test_the_schema_declares_realization_as_a_sort() -> None:
    assert "Realization" in META_ALGEBRA_SCHEMA.sort_ids
    assert "SchemaIsNotSpecification" in META_ALGEBRA_SCHEMA.law_ids


def test_an_absent_sort_is_refused_not_returned_as_none() -> None:
    with pytest.raises(MetaAlgebraSchemaError):
        META_ALGEBRA_SCHEMA.sort("Syllable")


def test_the_schema_digest_is_stable_and_version_bound() -> None:
    assert META_ALGEBRA_SCHEMA.schema_version == SCHEMA_VERSION
    rebuilt = MetaAlgebraSchema(
        schema_version=META_ALGEBRA_SCHEMA.schema_version,
        sorts=META_ALGEBRA_SCHEMA.sorts,
        laws=META_ALGEBRA_SCHEMA.laws,
    )
    assert rebuilt.content_id == META_ALGEBRA_SCHEMA.content_id


def test_a_language_without_a_law_is_not_an_algebra() -> None:
    with pytest.raises(MetaAlgebraSchemaError):
        MetaAlgebraSchema(
            schema_version="x",
            sorts=(
                SortDeclaration(sort_id="S", component_names=("a",), meaning="معنًى"),
            ),
            laws=(),
        )


def test_a_sort_without_components_is_refused() -> None:
    with pytest.raises(MetaAlgebraSchemaError):
        SortDeclaration(sort_id="S", component_names=(), meaning="معنًى")


def test_a_law_declares_what_it_forbids() -> None:
    with pytest.raises(MetaAlgebraSchemaError):
        SchemaLaw(law_id="L", statement="نصّ", what_it_forbids="  ")
