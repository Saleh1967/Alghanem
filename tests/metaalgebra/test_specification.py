"""`Σ_A` نظريّةٌ بعينها مكتوبةٌ بلغةٍ مُسمّاة؛ والسلسلةُ عضوٌ فيها لا بديلٌ عنها."""

from __future__ import annotations

import pytest
from builders import layer, specification, transition

from alghanem.metaalgebra.composition import CompositionChain
from alghanem.metaalgebra.schema import META_ALGEBRA_SCHEMA
from alghanem.metaalgebra.specification import (
    AbstractSystemSpecification,
    AbstractSystemSpecificationError,
    SchemaRef,
)
from alghanem.metaalgebra.standing import SpecificationSetRef


def test_a_specification_is_written_in_the_current_schema() -> None:
    spec = specification()
    assert spec.schema_ref.content_id == META_ALGEBRA_SCHEMA.content_id


def test_a_specification_built_on_another_schema_digest_is_refused() -> None:
    with pytest.raises(AbstractSystemSpecificationError):
        AbstractSystemSpecification(
            spec_id="SIGMA_A.other",
            schema_ref=SchemaRef(schema_version="other.v0", content_id="0" * 64),
            layers=(layer("L0"), layer("L1")),
            transitions=(transition("alpha"),),
        )


def test_an_orphan_transition_is_refused() -> None:
    with pytest.raises(AbstractSystemSpecificationError):
        AbstractSystemSpecification(
            spec_id="SIGMA_A.orphan",
            schema_ref=SchemaRef.of(),
            layers=(layer("L0"),),
            transitions=(transition("alpha"),),
        )


def test_a_duplicate_layer_name_hides_one_under_another() -> None:
    with pytest.raises(AbstractSystemSpecificationError):
        AbstractSystemSpecification(
            spec_id="SIGMA_A.dup",
            schema_ref=SchemaRef.of(),
            layers=(layer("L0"), layer("L0")),
            transitions=(),
        )


def test_a_chain_is_a_member_of_the_specification_not_a_substitute() -> None:
    first = layer("L0")
    second = layer("L1")
    step = transition("alpha")
    spec = AbstractSystemSpecification(
        spec_id="SIGMA_A.chained",
        schema_ref=SchemaRef.of(),
        layers=(first, second, layer("L2")),
        transitions=(step,),
        chains=(
            CompositionChain(
                chain_id="chain0", layers=(first, second), transitions=(step,)
            ),
        ),
    )
    assert spec.layer_ids == ("L0", "L1", "L2")
    assert spec.chains[0].instantiation_coverage == 1


def test_a_chain_over_a_foreign_layer_is_refused() -> None:
    outsider = layer("X0")
    other = layer("X1")
    step = transition("beta", source_layer_id="X0", target_layer_id="X1")
    with pytest.raises(AbstractSystemSpecificationError):
        AbstractSystemSpecification(
            spec_id="SIGMA_A.foreign",
            schema_ref=SchemaRef.of(),
            layers=(layer("L0"), layer("L1")),
            transitions=(transition("alpha"),),
            chains=(
                CompositionChain(
                    chain_id="chain0",
                    layers=(outsider, other),
                    transitions=(step,),
                ),
            ),
        )


def test_lookup_of_an_absent_member_is_refused_not_silent() -> None:
    spec = specification()
    assert spec.layer("L0").layer_id == "L0"
    assert spec.transition("alpha").transition_id == "alpha"
    with pytest.raises(AbstractSystemSpecificationError):
        spec.layer("L9")
    with pytest.raises(AbstractSystemSpecificationError):
        spec.transition("omega")


def test_the_specification_digest_excludes_realizations_entirely() -> None:
    spec = specification()
    content = spec.as_canonical_content()
    assert "realizations" not in content
    assert spec.content_id == specification().content_id


def test_the_specification_exposes_a_standing_reference() -> None:
    reference = specification().as_specification_ref(scope="نطاقُ الاختبار")
    assert isinstance(reference, SpecificationSetRef)
    assert reference.content_id == specification().content_id
