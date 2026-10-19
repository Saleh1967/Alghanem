"""هُويّةُ المولِّد: `digest(g)` من بايتات مصدره لا من رقمِ نسخةٍ مكتوبٍ باليد.

    determinism ⇔ (digest Σ_A, digest g)  ⇒  bytes

فرقمُ النسخةِ المكتوبُ يدويًّا يمكن أن يثبت بينما يتغيّر المولِّد، فيصير البيانُ
كاذبًا بلا خطأٍ ظاهر. وبصمةُ المصدرِ لا تحتمل هذا: أيُّ تغيُّرِ بايتٍ في وحدةٍ
مولِّدة يغيّر `generator_digest` ضرورةً.

والقائمةُ `GENERATOR_SOURCE_MODULES` مُعلَنةٌ صراحةً لا مُستنبَطةٌ بمسحِ المجلّد:
مسحُ المجلّد يجعل ملفًّا عارضًا جزءًا من الهُويّة، والإعلانُ يجعل توسيعَ
المولِّد فعلًا مقصودًا مُسجَّلًا.
"""

from __future__ import annotations

from pathlib import Path
from typing import Final

from ..canonical_content import canonical_bytes, canonical_digest

__all__ = [
    "GENERATOR_SOURCE_MODULES",
    "A_VERSION_STRING_IS_NOT_AN_IDENTITY",
    "GeneratorIdentityError",
    "generator_digest",
]

A_VERSION_STRING_IS_NOT_AN_IDENTITY: Final = (
    "هُويّةُ المولِّد بصمةُ بايتات مصدره؛ ورقمُ النسخةِ المكتوبُ يدويًّا "
    "قد يثبت بينما يتغيّر المولِّد"
)

GENERATOR_SOURCE_MODULES: Final[tuple[str, ...]] = (
    "artifact.py",
    "backend.py",
    "generator_identity.py",
    "manifest.py",
    "python_backend.py",
)


class GeneratorIdentityError(ValueError):
    """خطأُ هُويّةِ المولِّد: وحدةٌ مُعلَنةٌ غيرُ موجودة."""


def _package_directory() -> Path:
    return Path(__file__).resolve().parent


def generator_digest() -> str:
    """بصمةُ المولِّد `digest(g)` من بايتات وحداته المُعلَنة مرتّبةً بأسمائها."""

    directory = _package_directory()
    encoded: dict[str, str] = {}
    for module_name in sorted(GENERATOR_SOURCE_MODULES):
        path = directory / module_name
        if not path.is_file():
            raise GeneratorIdentityError(
                f"وحدةُ المولِّد المُعلَنة «{module_name}» غيرُ موجودة؛ "
                f"و{A_VERSION_STRING_IS_NOT_AN_IDENTITY}"
            )
        encoded[module_name] = canonical_digest(path.read_bytes())
    return canonical_digest(canonical_bytes(encoded))
