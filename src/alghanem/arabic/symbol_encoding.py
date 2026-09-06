"""Discovery and freezing of a symbolic Arabic surface encoding."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from unicodedata import combining, normalize


@dataclass(frozen=True)
class CarrierIdentity:
    """A discovered carrier, identified without linguistic naming."""

    identifier: str
    surface: str


@dataclass(frozen=True)
class StateIdentity:
    """A discovered combining state, identified without linguistic naming."""

    identifier: str
    surface: str


@dataclass(frozen=True)
class CarrierStateAssignment:
    """A separately discovered assignment of a state to a carrier."""

    carrier: CarrierIdentity
    state: StateIdentity


@dataclass(frozen=True)
class CanonicalSurfaceEncoding:
    """The normalized surface and its born symbolic assignment."""

    normalized_surface: str
    assignment: CarrierStateAssignment


@dataclass(frozen=True)
class FrozenSymbolicEncoding:
    """A closed 29-carrier, 4-state symbolic encoding."""

    carriers: tuple[CarrierIdentity, ...]
    states: tuple[StateIdentity, ...]
    assignments: tuple[CarrierStateAssignment, ...]
    surfaces: tuple[CanonicalSurfaceEncoding, ...]

    def __post_init__(self) -> None:
        if len(self.carriers) != 29:
            raise ValueError("a frozen Arabic encoding requires exactly 29 carriers")
        if len(self.states) != 4:
            raise ValueError("a frozen Arabic encoding requires exactly 4 states")
        if len({carrier.identifier for carrier in self.carriers}) != len(self.carriers):
            raise ValueError("carrier identities must be unique")
        if len({state.identifier for state in self.states}) != len(self.states):
            raise ValueError("state identities must be unique")
        expected_bindings = {
            (carrier.identifier, state.identifier)
            for carrier in self.carriers
            for state in self.states
        }
        actual_bindings = {
            (assignment.carrier.identifier, assignment.state.identifier)
            for assignment in self.assignments
        }
        if actual_bindings != expected_bindings:
            raise ValueError(
                "a frozen Arabic encoding requires every carrier-state binding"
            )


class ArabicSymbolEncodingV1:
    """Birth protocol for symbolic carrier/state encodings.

    Inputs are normalized before identities are born.  The protocol intentionally
    exposes no linguistic labels: identities follow discovery order and become
    meaningful only in the independently frozen result.
    """

    def __init__(self) -> None:
        self._carriers: dict[str, CarrierIdentity] = {}
        self._states: dict[str, StateIdentity] = {}
        self._assignments: dict[tuple[str, str], CarrierStateAssignment] = {}
        self._surfaces: dict[str, CanonicalSurfaceEncoding] = {}

    def discover(self, raw_unicode: Iterable[str]) -> None:
        """Perform normalization, identity birth, and binding birth in order."""
        for raw_surface in raw_unicode:
            normalized_surface = self.orthographic_normalize(raw_surface)
            carrier_surface, state_surface = self._split_surface(normalized_surface)
            carrier = self._carriers.setdefault(
                carrier_surface,
                CarrierIdentity(f"C_{len(self._carriers)}", carrier_surface),
            )
            state = self._states.setdefault(
                state_surface,
                StateIdentity(f"S_{len(self._states)}", state_surface),
            )
            assignment = self._assignments.setdefault(
                (carrier.identifier, state.identifier),
                CarrierStateAssignment(carrier, state),
            )
            encoding = CanonicalSurfaceEncoding(normalized_surface, assignment)
            prior = self._surfaces.setdefault(normalized_surface, encoding)
            if prior.assignment != assignment:
                raise ValueError(
                    "a canonical surface cannot collide across assignments"
                )

    @staticmethod
    def orthographic_normalize(raw_unicode: str) -> str:
        """Return the canonical Unicode surface used for discovery."""
        if not isinstance(raw_unicode, str) or not raw_unicode:
            raise ValueError("a raw Unicode surface must be a non-empty string")
        return normalize("NFD", normalize("NFC", raw_unicode))

    @staticmethod
    def _split_surface(normalized_surface: str) -> tuple[str, str]:
        bases = [
            character for character in normalized_surface if not combining(character)
        ]
        states = [character for character in normalized_surface if combining(character)]
        if len(bases) != 1 or len(states) != 1:
            raise ValueError(
                "each surface must contain exactly one carrier and one combining state"
            )
        return bases[0], states[0]

    @property
    def carrier_identities(self) -> tuple[CarrierIdentity, ...]:
        return tuple(self._carriers.values())

    @property
    def state_identities(self) -> tuple[StateIdentity, ...]:
        return tuple(self._states.values())

    @property
    def carrier_state_assignments(self) -> tuple[CarrierStateAssignment, ...]:
        return tuple(self._assignments.values())

    @property
    def canonical_surface_encodings(self) -> tuple[CanonicalSurfaceEncoding, ...]:
        return tuple(self._surfaces.values())

    def freeze(self) -> FrozenSymbolicEncoding:
        """Close discovery after identities and all bindings are born."""
        return FrozenSymbolicEncoding(
            self.carrier_identities,
            self.state_identities,
            self.carrier_state_assignments,
            self.canonical_surface_encodings,
        )
