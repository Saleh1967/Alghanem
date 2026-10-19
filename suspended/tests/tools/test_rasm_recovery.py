"""جسرُ الرسم السياقيّ (`tools/rasm_recovery`): استعادةٌ نسبيّة، وفحصُ اتّساقٍ مستقلّ."""

from __future__ import annotations

import gzip
import hashlib
import json
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parents[2] / "tools" / "rasm_recovery"
sys.path.insert(0, str(HERE))

from check_codebooks import check  # noqa: E402
from contextual import Codebook, Context, project, transport  # noqa: E402
from rasm_consistency import consistent  # noqa: E402

WORDS = ["رَحْمَةِ", "رَحْمَتِ", "قَالَ", "فَاتَّبِعْ", "عَلَا", "عَلَى", "دَابَّةٍ"]


def _write(rows: list[dict[str, object]], path: Path) -> None:
    with gzip.open(path, "wt", encoding="utf-8") as out:
        for row in rows:
            out.write(json.dumps(row, ensure_ascii=False) + "\n")


def _digest(book: dict[str, object]) -> str:
    raw = json.dumps(book, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode()).hexdigest()


def test_the_wasl_alif_after_a_prefix_gets_no_certificate() -> None:
    decision = project("فَاتَّبِعْ", Context())
    assert decision["status"] == "DEFER"
    assert (
        decision["reasons"][0]["reason"] == "ALIF_AFTER_A_POSSIBLE_PREFIX_MAY_BE_WASL"
    )


def test_rasm_distinctions_lost_by_the_projection_form_fibers() -> None:
    book = Codebook(WORDS, Context())
    sizes = sorted(len(f) for f in book.fibers.values())
    assert sizes.count(2) == 2  # رحمة/رحمت و علا/على
    for word in ("رَحْمَةِ", "رَحْمَتِ", "عَلَا", "عَلَى"):
        assert book.decode(book.encode(word)) == word
        assert book.decode_integer(book.encode(word).integer) == word


def test_a_certificate_is_re_evaluated_not_inherited_across_a_boundary() -> None:
    start = Codebook(WORDS, Context())
    pause = Codebook(WORDS, Context(exit="pause"))
    moved = transport(start.encode("دَابَّةٍ"), start, pause)
    assert pause.decode(moved) == "دَابَّةٍ"
    assert moved.atoms[-1] == "هْ"  # التاءُ المربوطةُ هاءٌ ساكنةٌ في الوقف


def test_consistency_accepts_the_declared_expansions() -> None:
    assert consistent("قَالَ", ["قَ", "اْ", "لَ"])
    assert consistent("دَابَّةٍ", ["دَ", "اْ", "بْ", "بَ", "تِ", "نْ"])
    assert consistent("آبَاؤُكُمْ", ["ءَ", "اْ", "بَ", "اْ", "ءُ", "كُ", "مْ"])


def test_consistency_refuses_atoms_with_no_source_in_the_rasm() -> None:
    assert not consistent("فَاتَّبِعْ", ["بَ"])
    assert not consistent("قَالَ", ["قِ", "اْ", "لَ"])  # كسرةٌ لم تُكتب
    assert not consistent("قَالَ", ["كَ", "اْ", "لَ"])  # حاملٌ ليس في الرسم


def test_the_checker_now_refuses_wrong_atoms_even_when_re_digested(
    tmp_path: Path,
) -> None:
    book = Codebook(WORDS, Context())
    row = json.loads(
        json.dumps(
            {"book_digest": book.digest, "book": book.payload}, ensure_ascii=False
        )
    )
    good = tmp_path / "good.gz"
    _write([row], good)
    assert check(good)["ready_cases"] == len(
        [d for d in book.decisions.values() if d["status"] == "READY"]
    )
    row["book"]["decisions"]["قَالَ"]["atoms"] = ["بَ"]
    row["book_digest"] = _digest(row["book"])
    bad = tmp_path / "bad.gz"
    _write([row], bad)
    with pytest.raises(ValueError, match="RASM_ATOMS_INCONSISTENT"):
        check(bad)
