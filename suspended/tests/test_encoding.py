"""طبقة يونيكود."""

from __future__ import annotations

from conftest import ROOT
from slge.encoding import SUBSTITUTIONS, audit_text, conflicts, normalize


def test_normalize_idempotent_on_every_char() -> None:
    chars = [chr(c) for c in range(0x0600, 0x0700)] + list(SUBSTITUTIONS)
    for ch in chars:
        once = normalize(ch)
        assert normalize(once) == once, hex(ord(ch))
    assert not any(bad in normalize("".join(chars)) for bad in SUBSTITUTIONS)


def test_conflicts_catch_every_substitution() -> None:
    text = "".join(SUBSTITUTIONS) * 2
    found = conflicts(text)
    assert len(found) == len(SUBSTITUTIONS) and all(n == 2 for _, n in found)


def test_sources_are_clean() -> None:
    for path in sorted((ROOT / "src" / "slge").glob("*.py")):
        assert audit_text(path.read_text(encoding="utf-8")) == [], path.name
