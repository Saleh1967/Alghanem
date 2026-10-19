"""شواهدُ وديعةِ الخطّ: البتاتُ حاضرةٌ، والقارئُ يرفض ما لا يفهم."""

from __future__ import annotations

import hashlib

import pytest

from alghanem.arabic.font_deposit import (
    AMIRI,
    FONT_DEPOSIT,
    FONT_DEPOSIT_NAMED_RESIDUALS,
    NOTO_KUFI,
    SCHEHERAZADE,
    FontDepositError,
    FontManifest,
    deposit_bytes,
    deposit_path,
    every_deposit_matches_its_manifest,
    load_font,
    measured_manifest_of,
)

_ALL = (AMIRI, SCHEHERAZADE, NOTO_KUFI)


@pytest.mark.parametrize("filename", _ALL)
def test_every_deposit_is_present_in_the_tree(filename: str) -> None:
    assert deposit_path(filename).is_file()


@pytest.mark.parametrize("filename", _ALL)
def test_the_frozen_digest_is_the_digest_of_the_deposited_bytes(
    filename: str,
) -> None:
    frozen = {entry.filename: entry for entry in FONT_DEPOSIT}[filename]
    assert hashlib.sha256(deposit_bytes(filename)).hexdigest() == frozen.sha256


@pytest.mark.parametrize("filename", _ALL)
def test_the_measured_manifest_equals_the_frozen_one(filename: str) -> None:
    frozen = {entry.filename: entry for entry in FONT_DEPOSIT}[filename]
    assert measured_manifest_of(filename) == frozen


def test_the_whole_deposit_matches_at_read_time() -> None:
    assert every_deposit_matches_its_manifest() is True


def test_the_three_deposits_are_distinct_files() -> None:
    digests = {entry.sha256 for entry in FONT_DEPOSIT}
    assert len(digests) == len(FONT_DEPOSIT) == 3


def test_a_font_with_no_frozen_manifest_is_refused() -> None:
    with pytest.raises(FontDepositError):
        load_font("DejaVuSans.ttf")


def test_an_absent_deposit_is_refused_and_the_system_font_is_not_used() -> None:
    with pytest.raises(FontDepositError):
        deposit_bytes("NoSuchFont-Regular.ttf")


def test_a_manifest_without_the_glyf_table_is_refused() -> None:
    with pytest.raises(FontDepositError):
        FontManifest(
            filename="x.ttf",
            sha256="0" * 64,
            byte_length=1,
            glyph_count=1,
            units_per_em=1000,
            tables=("cmap", "head", "loca", "maxp"),
        )


def test_a_manifest_with_unsorted_tables_is_refused() -> None:
    with pytest.raises(FontDepositError):
        FontManifest(
            filename="x.ttf",
            sha256="0" * 64,
            byte_length=1,
            glyph_count=1,
            units_per_em=1000,
            tables=("maxp", "cmap", "glyf", "head", "loca"),
        )


def test_a_digest_that_is_not_sha256_is_refused() -> None:
    with pytest.raises(FontDepositError):
        FontManifest(
            filename="x.ttf",
            sha256="short",
            byte_length=1,
            glyph_count=1,
            units_per_em=1000,
            tables=("cmap", "glyf", "head", "loca", "maxp"),
        )


@pytest.mark.parametrize("filename", _ALL)
def test_the_deposit_covers_the_arabic_letters_it_is_read_for(filename: str) -> None:
    font = load_font(filename)
    assert font.glyph_for("\u0628") != 0
    assert font.glyph_for("\u0627") != 0


def test_cmap_is_asked_about_one_character_only() -> None:
    font = load_font(AMIRI)
    with pytest.raises(FontDepositError):
        font.glyph_for("\u0628\u062a")


def test_a_glyph_beyond_the_deposit_is_refused() -> None:
    font = load_font(NOTO_KUFI)
    with pytest.raises(FontDepositError):
        font.outline_of(font.glyph_count)


def test_components_are_refused_for_a_simple_glyph() -> None:
    font = load_font(NOTO_KUFI)
    glyph = font.glyph_for("\u0628")
    assert font.is_composite(glyph) is False
    with pytest.raises(FontDepositError):
        font.components_of(glyph)


def test_contours_are_refused_for_a_composite_glyph() -> None:
    font = load_font(AMIRI)
    glyph = font.glyph_for("\u0628")
    assert font.is_composite(glyph) is True
    with pytest.raises(FontDepositError):
        font.contours_of(glyph)


def test_the_naskh_deposit_declares_a_decomposition_and_the_kufi_does_not() -> None:
    amiri = load_font(AMIRI)
    kufi = load_font(NOTO_KUFI)
    assert amiri.is_composite(amiri.glyph_for("\u0628")) is True
    assert kufi.is_composite(kufi.glyph_for("\u0628")) is False


def test_a_composite_outline_is_flattened_to_its_component_contours() -> None:
    font = load_font(AMIRI)
    glyph = font.glyph_for("\u0628")
    components = font.components_of(glyph)
    spread = sum(len(font.outline_of(index)) for index, _x, _y in components)
    assert len(font.outline_of(glyph)) == spread


def test_a_component_shift_moves_the_contour_by_exactly_that_shift() -> None:
    font = load_font(AMIRI)
    glyph = font.glyph_for("\u0628")
    (base, _bx, _by), (extra, shift_x, shift_y) = font.components_of(glyph)
    raw = font.outline_of(extra)[0]
    placed = font.outline_of(glyph)[len(font.outline_of(base))]
    assert placed[0][0] - raw[0][0] == shift_x
    assert placed[0][1] - raw[0][1] == shift_y


@pytest.mark.parametrize("filename", _ALL)
def test_the_outline_hash_is_stable_across_reads(filename: str) -> None:
    font = load_font(filename)
    glyph = font.glyph_for("\u0628")
    assert font.outline_hash(glyph) == font.outline_hash(glyph)


def test_different_letters_get_different_outline_hashes() -> None:
    font = load_font(AMIRI)
    assert font.outline_hash(font.glyph_for("\u0628")) != font.outline_hash(
        font.glyph_for("\u062a")
    )


@pytest.mark.parametrize("filename", _ALL)
def test_the_units_per_em_is_read_from_the_bytes_not_assumed(filename: str) -> None:
    assert load_font(filename).manifest.units_per_em in (1000, 2048)


def test_the_deposits_do_not_share_a_units_per_em() -> None:
    grid = {entry.units_per_em for entry in FONT_DEPOSIT}
    assert len(grid) > 1


def test_every_residual_is_named_by_its_own_key() -> None:
    for key, text in FONT_DEPOSIT_NAMED_RESIDUALS.items():
        assert text.startswith(f"{key}: ")


def test_the_residuals_name_the_reader_limits_and_the_missing_shaper() -> None:
    assert "WHAT_THIS_READER_CANNOT_PARSE_IT_REFUSES_AND_DOES_NOT_GUESS" in (
        FONT_DEPOSIT_NAMED_RESIDUALS
    )
    assert "THERE_IS_NO_SHAPING_ENGINE_HERE_ONLY_ISOLATED_GLYPHS" in (
        FONT_DEPOSIT_NAMED_RESIDUALS
    )
