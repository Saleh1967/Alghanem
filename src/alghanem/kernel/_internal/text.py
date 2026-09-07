"""Shared internal text validation."""


def require_text(value: str, name: str) -> None:
    """Require an exact, non-blank text value."""

    if type(value) is not str or not value.strip():
        raise ValueError(f"{name} must be non-blank text")


def is_non_blank_text(value: object) -> bool:
    """Return whether a value is an exact, non-blank text value."""

    return type(value) is str and bool(value.strip())
