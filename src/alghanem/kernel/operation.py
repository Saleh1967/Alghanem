"""Operations and their explicitly separate results."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Operation:
    """A declared operation; execution and reversibility are not assumed."""

    name: str
    declared_change: str
    source_domain: str | None = None
    target_domain: str | None = None

    def __post_init__(self) -> None:
        if not self.name or not self.declared_change:
            raise ValueError("an operation requires a name and declared change")

    @property
    def change(self) -> str:
        """Compatibility view of the operation's declared change."""
        return self.declared_change


@dataclass(frozen=True, slots=True)
class OperationResult:
    """The result of an operation, kept distinct from the operation itself."""

    value: object
