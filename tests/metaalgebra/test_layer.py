import pytest
from builders import layer

from alghanem.metaalgebra.layer import (
    CARRIER_IS_NOT_STATE,
    LAYER_COMPONENT_NAMES,
    CarrierSpecification,
    LayerSignature,
    LayerSignatureError,
    PartialOperationSpecification,
    StateSpaceSpecification,
)


def test_layer_signature_has_exactly_eight_components() -> None:
    assert LAYER_COMPONENT_NAMES == (
        "carrier",
        "state_space",
        "operations",
        "license_relations",
        "invariants",
        "closure",
        "trace",
        "residuals",
    )
    assert set(LAYER_COMPONENT_NAMES) <= set(LayerSignature.__dataclass_fields__)


def test_state_space_is_a_component_of_its_own() -> None:
    signature = layer()

    assert signature.carrier.carrier_id != signature.state_space.state_space_id


def test_a_carrier_that_is_also_the_state_space_is_refused() -> None:
    signature = layer()
    with pytest.raises(LayerSignatureError) as excinfo:
        LayerSignature(
            layer_id=signature.layer_id,
            carrier=CarrierSpecification(
                carrier_id="same",
                membership_condition="شرط",
                what_is_not_a_member="غيره",
            ),
            state_space=StateSpaceSpecification(
                state_space_id="same",
                state_condition="شرط",
                why_not_folded_into_carrier="سبب",
            ),
            operations=signature.operations,
            license_relations=signature.license_relations,
            invariants=signature.invariants,
            closure=signature.closure,
            trace=signature.trace,
            residuals=signature.residuals,
        )

    assert CARRIER_IS_NOT_STATE in str(excinfo.value)


def test_a_partial_operation_must_declare_where_it_is_undefined() -> None:
    with pytest.raises(LayerSignatureError):
        PartialOperationSpecification(
            operation_id="op",
            input_condition="لازمُ المُدخَل",
            result_condition="لازمُ المخرَج",
            undefined_when=(),
        )


def test_invariant_component_names_are_derived_not_written() -> None:
    signature = layer(invariant_names=("identity", "rank"))

    assert signature.invariant_component_names == frozenset({"identity", "rank"})
    assert "invariant_component_names" not in LayerSignature.__dataclass_fields__


def test_duplicate_invariant_components_are_refused() -> None:
    with pytest.raises(LayerSignatureError):
        layer(invariant_names=("identity", "identity"))


def test_layer_content_id_changes_with_any_component() -> None:
    first = layer()
    second = layer(invariant_names=("identity", "rank"))

    assert first.content_id != second.content_id
    assert layer().content_id == first.content_id


def test_no_layer_name_or_count_is_declared_in_this_module() -> None:
    import alghanem.metaalgebra.layer as layer_module

    enums = [
        value
        for name, value in vars(layer_module).items()
        if isinstance(value, type) and issubclass(value, __import__("enum").Enum)
    ]
    assert enums == []
    assert "layer_id" in LayerSignature.__dataclass_fields__
