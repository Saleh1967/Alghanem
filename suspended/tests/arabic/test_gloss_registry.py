"""شهودٌ على سجلّ الوسم: موضعٌ يُحَلّ، وقارئٌ يردُّ ما لا يعرفه."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from alghanem.arabic import gloss_registry as gloss_module
from alghanem.arabic.fatiha_source_text import FATIHA_LINES, FATIHA_SOURCE_ID
from alghanem.arabic.gloss_registry import (
    DEPOSITED_GLOSS_REGISTRY_SHA256,
    GLOSS_REGISTRY_NAMED_RESIDUALS,
    GLOSS_REGISTRY_RELATIVE_PATH,
    NORMALIZATION_FORM,
    SANCTIONED_GLOSS_DATA_FILENAMES,
    GlossEntry,
    GlossRegistry,
    GlossRegistryError,
    SourceLocator,
    an_empty_registry,
    in_tree_gloss_registry,
    normalize,
    read_gloss_registry,
    registered_source_ids,
    registered_source_text,
    resolve_locator,
    unsanctioned_gloss_data_files,
)
from alghanem.import_boundary import ImportBoundaryPolicy, audit_import_boundary


def _document(**overrides: object) -> dict[str, object]:
    document: dict[str, object] = {
        "registry_id": "سجلُّ اختبار",
        "authority_id": "جهةٌ أخرى",
        "authority_note": "جهةٌ مكتوبةٌ لهذا الاختبار",
        "version": "v1",
        "normalization_form": NORMALIZATION_FORM,
        "entries": [],
    }
    document.update(overrides)
    return document


def _bytes_of(document: dict[str, object]) -> bytes:
    return json.dumps(document, ensure_ascii=False).encode("utf-8")


# --- الحدودُ البنيويّة --------------------------------------------------------


def test_the_gloss_registry_module_reaches_no_kernel_module() -> None:
    report = audit_import_boundary(
        (Path(str(gloss_module.__file__)),),
        ImportBoundaryPolicy(
            policy_id="gloss-registry",
            permitted_modules=(),
            forbidden_packages=("alghanem.kernel",),
        ),
    )
    assert not [
        name for name in report.reached_modules if name.startswith("alghanem.kernel")
    ]


def test_there_are_four_named_residuals_all_distinct_and_non_blank() -> None:
    assert len(GLOSS_REGISTRY_NAMED_RESIDUALS) == 4
    assert len(set(GLOSS_REGISTRY_NAMED_RESIDUALS)) == 4
    assert all(note.strip() for note in GLOSS_REGISTRY_NAMED_RESIDUALS)


# --- محدِّدُ الموضع ------------------------------------------------------------


def test_a_locator_resolves_to_the_surface_that_really_sits_there() -> None:
    line = normalize(FATIHA_LINES[3])
    locator = SourceLocator(line=4, start=0, end=len(line.split(" ")[0]), word_number=1)
    assert resolve_locator(FATIHA_SOURCE_ID, locator) == line.split(" ")[0]


def test_a_locator_beyond_the_line_or_the_text_does_not_resolve() -> None:
    assert resolve_locator(FATIHA_SOURCE_ID, SourceLocator(99, 0, 3)) is None
    assert resolve_locator(FATIHA_SOURCE_ID, SourceLocator(1, 0, 10_000)) is None


def test_a_locator_into_an_unregistered_source_does_not_resolve() -> None:
    assert resolve_locator("مصدرٌ ليس في الشجرة", SourceLocator(1, 0, 3)) is None
    assert registered_source_text("مصدرٌ ليس في الشجرة") is None
    assert registered_source_ids() == (FATIHA_SOURCE_ID,)


def test_a_malformed_locator_is_refused_outright() -> None:
    for line, start, end in ((0, 0, 3), (1, -1, 3), (1, 3, 3), (1, 4, 3)):
        with pytest.raises(GlossRegistryError):
            SourceLocator(line=line, start=start, end=end)
    with pytest.raises(GlossRegistryError):
        SourceLocator(line=1, start=0, end=3, word_number=0)


def test_a_word_number_is_written_for_reading_and_never_resolves_a_place() -> None:
    plain = SourceLocator(line=4, start=0, end=4)
    numbered = SourceLocator(line=4, start=0, end=4, word_number=7)
    assert resolve_locator(FATIHA_SOURCE_ID, plain) == resolve_locator(
        FATIHA_SOURCE_ID, numbered
    )
    assert "#w7" in numbered.rendered
    registry = read_gloss_registry(
        _bytes_of(
            _document(
                entries=[
                    {
                        "source_id": FATIHA_SOURCE_ID,
                        "line": 4,
                        "start": 0,
                        "end": 4,
                        "word_number": 7,
                        "genus": "جنس",
                        "predicate": "محمول",
                        "content": "مضمون",
                    }
                ]
            )
        )
    )
    assert registry.lookup(FATIHA_SOURCE_ID, plain) is not None
    joined = "\n".join(GLOSS_REGISTRY_NAMED_RESIDUALS)
    assert "AWordNumberIsForReadingNotForResolution" in joined


# --- القارئُ الصارم -----------------------------------------------------------


def test_an_unknown_field_is_refused_in_the_header_and_in_an_entry() -> None:
    with pytest.raises(GlossRegistryError):
        read_gloss_registry(_bytes_of(_document(surprise="حقلٌ طارئ")))
    with pytest.raises(GlossRegistryError):
        read_gloss_registry(
            _bytes_of(
                _document(
                    entries=[
                        {
                            "source_id": FATIHA_SOURCE_ID,
                            "line": 1,
                            "start": 0,
                            "end": 3,
                            "genus": "جنس",
                            "predicate": "محمول",
                            "content": "مضمون",
                            "surprise": "حقلٌ طارئ",
                        }
                    ]
                )
            )
        )


def test_a_missing_required_field_is_refused() -> None:
    document = _document()
    del document["version"]
    with pytest.raises(GlossRegistryError):
        read_gloss_registry(_bytes_of(document))


def test_a_registry_without_an_authority_is_not_read_as_a_warrant() -> None:
    with pytest.raises(GlossRegistryError):
        read_gloss_registry(_bytes_of(_document(authority_id="   ")))
    with pytest.raises(GlossRegistryError):
        read_gloss_registry(_bytes_of(_document(authority_note="  ")))


def test_a_registry_declaring_another_normalization_is_refused() -> None:
    with pytest.raises(GlossRegistryError):
        read_gloss_registry(_bytes_of(_document(normalization_form="NFD")))


def test_bytes_that_are_not_json_are_refused_rather_than_read_empty() -> None:
    with pytest.raises(GlossRegistryError):
        read_gloss_registry(b"\xff\xfe not json")
    with pytest.raises(GlossRegistryError):
        read_gloss_registry(b"[]")


def test_a_field_of_the_wrong_type_is_refused() -> None:
    for key, value in (("line", "1"), ("start", True), ("word_number", "1")):
        entry = {
            "source_id": FATIHA_SOURCE_ID,
            "line": 1,
            "start": 0,
            "end": 3,
            "genus": "جنس",
            "predicate": "محمول",
            "content": "مضمون",
        }
        entry[key] = value
        with pytest.raises(GlossRegistryError):
            read_gloss_registry(_bytes_of(_document(entries=[entry])))


def test_one_place_glossed_twice_in_one_registry_is_refused() -> None:
    entry = GlossEntry(
        source_id=FATIHA_SOURCE_ID,
        locator=SourceLocator(1, 0, 3),
        genus="جنس",
        predicate="محمول",
        content="مضمون",
    )
    with pytest.raises(GlossRegistryError):
        GlossRegistry(
            registry_id="سجل",
            authority_id="جهة",
            authority_note="بيان",
            version="v1",
            payload_sha256="0" * 64,
            entries=(entry, entry),
        )


def test_the_digest_is_computed_from_the_bytes_and_not_written_in_the_document() -> (
    None
):
    payload = _bytes_of(_document())
    registry = read_gloss_registry(payload)
    import hashlib

    assert registry.payload_sha256 == hashlib.sha256(payload).hexdigest()


# --- المُودَعُ في الشجرة ---------------------------------------------------------


def test_the_deposited_registry_is_read_and_its_digest_matches() -> None:
    registry = in_tree_gloss_registry()
    assert registry.payload_sha256 == DEPOSITED_GLOSS_REGISTRY_SHA256
    assert registry.authority_id.strip()
    assert registry.version.strip()


def test_the_deposited_registry_carries_no_entry_yet_and_that_is_read_as_absence() -> (
    None
):
    assert in_tree_gloss_registry().entry_count == 0
    assert an_empty_registry().entry_count == 0


def test_the_deposited_place_is_sanctioned_and_holds_no_stray_file() -> None:
    assert GLOSS_REGISTRY_RELATIVE_PATH == "gloss_data/arabic_glosses_v1.json"
    assert SANCTIONED_GLOSS_DATA_FILENAMES == ("README.md", "arabic_glosses_v1.json")
    assert unsanctioned_gloss_data_files() == ()


def test_bytes_that_drift_from_the_deposited_digest_are_refused(tmp_path: Path) -> None:
    drifted = tmp_path / "arabic_glosses_v1.json"
    drifted.write_bytes(_bytes_of(_document()))
    original = gloss_module.gloss_registry_path
    gloss_module.gloss_registry_path = lambda: drifted
    try:
        with pytest.raises(GlossRegistryError):
            in_tree_gloss_registry()
    finally:
        gloss_module.gloss_registry_path = original
