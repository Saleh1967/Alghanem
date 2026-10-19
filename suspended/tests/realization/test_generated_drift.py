"""الشجرةُ المُودَعة أثرٌ مطابقٌ لإعادة التوليد، لا نسخةٌ تنحرف بصمت."""

from __future__ import annotations

import json
from pathlib import Path

from alghanem.realization.generator_identity import (
    GENERATOR_SOURCE_MODULES,
    generator_digest,
)
from alghanem.realization.python_backend import PythonBackend
from alghanem.realization.reference_specification import REFERENCE_SPECIFICATION

_GENERATED_ROOT = (
    Path(__file__).resolve().parents[2]
    / "src"
    / "alghanem"
    / "realization"
    / "generated"
)


def _manifest_path() -> Path:
    return _GENERATED_ROOT / "manifest.json"


def test_the_committed_tree_is_byte_identical_to_regeneration() -> None:
    generated = PythonBackend().generate(REFERENCE_SPECIFICATION)
    for artifact in generated.artifacts:
        committed = _GENERATED_ROOT / artifact.relative_path
        assert committed.is_file(), artifact.relative_path
        assert committed.read_bytes() == artifact.encoded


def test_the_committed_manifest_matches_the_regenerated_manifest() -> None:
    manifest = PythonBackend().manifest(REFERENCE_SPECIFICATION)
    committed = json.loads(_manifest_path().read_text(encoding="utf-8"))
    assert committed == manifest.as_canonical_content()


def test_the_committed_manifest_names_both_digests_and_the_backend() -> None:
    committed = json.loads(_manifest_path().read_text(encoding="utf-8"))
    assert committed["sigma_digest"] == REFERENCE_SPECIFICATION.content_id
    assert committed["generator_digest"] == generator_digest()
    assert committed["backend_id"] == "g_py"
    assert committed["target_language"] == "python"
    assert committed["schema_digest"] == REFERENCE_SPECIFICATION.schema_ref.content_id


def test_the_generated_tree_contains_no_undeclared_artifact() -> None:
    manifest = PythonBackend().manifest(REFERENCE_SPECIFICATION)
    declared = set(manifest.artifact_paths) | {"manifest.json"}
    present = {
        path.name
        for path in _GENERATED_ROOT.iterdir()
        if path.is_file() and not path.name.startswith(".")
    }
    assert present == declared


def test_a_changed_generator_source_changes_the_generator_digest() -> None:
    directory = Path(__file__).resolve().parents[2] / "src" / "alghanem" / "realization"
    baseline = generator_digest()
    target = directory / "python_backend.py"
    original = target.read_bytes()
    try:
        target.write_bytes(original + b"\n# drift\n")
        assert generator_digest() != baseline
    finally:
        target.write_bytes(original)
    assert generator_digest() == baseline


def test_every_declared_generator_module_exists() -> None:
    directory = Path(__file__).resolve().parents[2] / "src" / "alghanem" / "realization"
    for module_name in GENERATOR_SOURCE_MODULES:
        assert (directory / module_name).is_file(), module_name


def test_the_generated_header_carries_the_current_generator_digest() -> None:
    manifest = PythonBackend().manifest(REFERENCE_SPECIFICATION)
    for relative_path in manifest.artifact_paths:
        text = (_GENERATED_ROOT / relative_path).read_text(encoding="utf-8")
        assert f"# generator_digest: {generator_digest()}" in text
        assert f"# sigma_digest: {REFERENCE_SPECIFICATION.content_id}" in text
