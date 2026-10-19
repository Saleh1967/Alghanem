"""Measurement protocol authority for raw surface observations."""

from __future__ import annotations

from dataclasses import dataclass
from unicodedata import unidata_version


def _require_non_empty_string(value: object, field_name: str) -> None:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{field_name} must be a non-empty string")


@dataclass(frozen=True, order=True)
class MeasurementProtocolSpec:
    """Frozen description of how observation occurrence identities are issued."""

    protocol_id: str
    protocol_version: str
    source_scope: str
    normalization_policy: str
    occurrence_scheme: str

    def __post_init__(self) -> None:
        _require_non_empty_string(self.protocol_id, "protocol id")
        _require_non_empty_string(self.protocol_version, "protocol version")
        _require_non_empty_string(self.source_scope, "source scope")
        _require_non_empty_string(self.normalization_policy, "normalization policy")
        _require_non_empty_string(self.occurrence_scheme, "occurrence scheme")


@dataclass(frozen=True, order=True)
class MeasurementRunIdentity:
    """A concrete run of a frozen measurement protocol."""

    protocol: MeasurementProtocolSpec
    run_id: str

    def __post_init__(self) -> None:
        if not isinstance(self.protocol, MeasurementProtocolSpec):
            raise ValueError(
                "measurement run protocol must be a MeasurementProtocolSpec"
            )
        _require_non_empty_string(self.run_id, "measurement run id")


@dataclass(frozen=True, order=True)
class MeasurementRunManifest:
    """The measurement-run metadata required before cross-run comparison."""

    run_identity: MeasurementRunIdentity
    normalization_form: str
    unicode_database_version: str

    def __post_init__(self) -> None:
        if not isinstance(self.run_identity, MeasurementRunIdentity):
            raise ValueError(
                "measurement run manifest must include a measurement run identity"
            )
        _require_non_empty_string(self.normalization_form, "normalization form")
        _require_non_empty_string(
            self.unicode_database_version, "unicode database version"
        )
        if self.normalization_form != self.run_identity.protocol.normalization_policy:
            raise ValueError(
                "measurement run manifest normalization must match protocol policy"
            )

    @classmethod
    def current(cls, run_identity: MeasurementRunIdentity) -> MeasurementRunManifest:
        """Issue a manifest for the runtime Unicode database and run policy."""
        return cls(
            run_identity,
            normalization_form=run_identity.protocol.normalization_policy,
            unicode_database_version=unidata_version,
        )
