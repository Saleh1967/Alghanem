"""Operations and their explicitly separate results."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Operation:
    """A declared operation; execution and reversibility are not assumed."""

    name: str
    change: str

    def __post_init__(self) -> None:
        if not self.name or not self.change:
            raise ValueError("an operation requires a name and declared change")


@dataclass(frozen=True, slots=True)
class OperationResult:
    """The result of an operation, kept distinct from the operation itself."""

    value: object
