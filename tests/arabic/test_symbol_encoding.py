"""Tests for the symbolic Arabic encoding foundation."""

from __future__ import annotations

import pytest

from alghanem.arabic import ArabicSymbolEncodingV1

_CARRIERS = (
    "\u0621\u0627\u0628\u062a\u062b\u062c\u062d\u062e\u062f\u0630\u0631\u0632\u0633"
    "\u0634\u0635\u0636\u0637\u0638\u0639\u063a\u0641\u0642\u0643\u0644\u0645\u0646"
    "\u0647\u0648\u064a"
)
_STATES = ("\u064e", "\u064f", "\u0650", "\u0652")


def surfaces() -> list[str]:
    return [carrier + state for carrier in _CARRIERS for state in _STATES]


def test_discovery_births_independent_identities_bindings_and_surfaces() -> None:
    encoding = ArabicSymbolEncodingV1()
    encoding.discover(surfaces())

    assert [carrier.identifier for carrier in encoding.carrier_identities] == [
        f"C_{index}" for index in range(29)
    ]
    assert [state.identifier for state in encoding.state_identities] == [
        f"S_{index}" for index in range(4)
    ]
    assert len(encoding.carrier_state_assignments) == 116
    assert len(encoding.canonical_surface_encodings) == 116
    assert len(encoding.freeze().assignments) == 116


def test_normalization_precedes_canonical_surface_birth() -> None:
    encoding = ArabicSymbolEncodingV1()
    encoding.discover(["\u0628\u064e", "\u0628\u064e"])

    assert len(encoding.canonical_surface_encodings) == 1
    assert encoding.canonical_surface_encodings[0].normalized_surface == "\u0628\u064e"


def test_freeze_requires_the_declared_symbolic_cardinalities() -> None:
    encoding = ArabicSymbolEncodingV1()
    encoding.discover(["\u0628\u064e"])

    with pytest.raises(ValueError, match="exactly 29 carriers"):
        encoding.freeze()


def test_freeze_rejects_identity_counts_without_complete_bindings() -> None:
    encoding = ArabicSymbolEncodingV1()
    encoding.discover(
        [
            carrier + _STATES[index % len(_STATES)]
            for index, carrier in enumerate(_CARRIERS)
        ]
    )

    with pytest.raises(ValueError, match="every carrier-state binding"):
        encoding.freeze()


@pytest.mark.parametrize(
    "surface",
    ["\u0628", "\u064e", "\u0628\u064e\u064f", "\u0628\u062a\u064e"],
)
def test_discovery_rejects_surfaces_without_one_carrier_and_one_state(
    surface: str,
) -> None:
    with pytest.raises(ValueError, match="exactly one carrier and one combining state"):
        ArabicSymbolEncodingV1().discover([surface])
