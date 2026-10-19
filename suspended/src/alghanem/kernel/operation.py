"""Operations and their explicitly separate results."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Operation:
    """A declared operation; execution and reversibility are not assumed.

    ``target_domain`` is declared metadata only at Kernel v0.1.
    """

    name: str
    declared_change: str
    source_domain: str | None = None
    target_domain: str | None = None

    def __post_init__(self) -> None:
        if not self.name.strip() or not self.declared_change.strip():
            raise ValueError("an operation requires a name and declared change")
        if self.source_domain is not None and not self.source_domain.strip():
            raise ValueError("an operation source domain cannot be blank")
        if self.target_domain is not None and not self.target_domain.strip():
            raise ValueError("an operation target domain cannot be blank")

    @property
    def change(self) -> str:
        """Compatibility view of the operation's declared change."""
        return self.declared_change


@dataclass(frozen=True, slots=True)
class OperationResult:
    """The result of an operation, kept distinct from the operation itself.

    The container is frozen, but payload immutability is not enforced.
    """

    value: object
