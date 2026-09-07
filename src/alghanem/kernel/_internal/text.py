"""Shared internal text validation."""


def require_text(value: str, name: str) -> None:
    """Require an exact, non-blank text value."""

    if type(value) is not str or not value.strip():
        raise ValueError(f"{name} must be non-blank text")
