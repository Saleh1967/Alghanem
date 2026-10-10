"""السلسلة (ADR ٣١): توقّعاتٌ مستقلّةٌ عن الشيفرة من نصّ النبهانيّ المختوم وقرار المالك
(2026-10-10) — ثلاثةُ سلالم، اليقينُ للوجود والحقائق وحدَهما («قطعية عن وجود الشيء… ظنية عن كنهه
وصفته»)، الجذرُ الأركانُ الأربعة لا «أوليات»، النسبُ إسنادٌ وتقييدٌ وإضافةٌ بلا «تضمين»، السببيّةُ
والمسببيّةُ علاقتا مجازٍ في الحكم، الفاعليّةُ والمفعوليّةُ نسبتان بعد الإسناد، وكلُّ ركنٍ بسطره من المختوم
أو معلَنٌ باسمه؛ وطفراتٌ مرفوضة."""

from __future__ import annotations

import gzip
import hashlib
import importlib.util
import sys
from pathlib import Path
from typing import Any

import pytest

from slge.salsala import ARKAN, DECLARED, ROWS, anchored, grade, ladder, salaf

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "tests" / "data"


def _tool() -> Any:
    spec = importlib.util.spec_from_file_location("deposit_salsala",
                                                  ROOT / "tools" / "deposit_salsala.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["deposit_salsala"] = mod
    spec.loader.exec_module(mod)
    return mod


def _lines(name: str, prefix: str) -> list[str]:
    raw = gzip.decompress((DATA / name).read_bytes())
    assert hashlib.sha256(raw).hexdigest().startswith(prefix)
    return raw.decode("utf-8").split("\n")


def test_every_rukn_is_anchored_in_the_sealed_text_or_declared_by_name() -> None:
    j3 = _lines("nabhani-shakhsiyya-3.txt.gz", "359bb553")
    tafkir = _lines("nabhani-tafkir.txt.gz", "b9b08eab")
    for rid, _, name, _, anchors, _, note in ROWS:
        if rid in DECLARED:
            assert not anchors and "معلَن" in note, name
            continue
        assert anchors, name
        for src, line, phrase in anchors:
            assert phrase in (j3 if src == "ج3" else tafkir)[line - 1], (name, src, line, phrase)
    assert {7, 10, 11} == DECLARED  # القابليّات، المكان، العدد — بقرار المالك لا من الذاكرة
    assert sum(1 for i in range(len(ROWS)) if anchored(i)) == 19


def test_three_ladders_with_the_ranked_tag() -> None:
    assert [ladder(i) for i in (0, 11, 12, 18, 19, 21)] == [
        "المعلومات السابقة", "المعلومات السابقة", "الوضع والنسب", "الوضع والنسب",
        "الحكم: علاقات المجاز", "الحكم: علاقات المجاز"]
    # التفكير 65 و123: اليقينُ في الوجود وحقائقه، والظنُّ في الكنه والصفات
    assert [i for i in range(len(ROWS)) if grade(i) == "يقين"] == [1, 2]
    assert all(grade(i) == "ظنّ" for i in range(3, 12))
    assert all(grade(i) == "—" for i in range(12, 22)) and grade(0) == "—"
    assert ROWS[0][2] == "الأركان الأربعة" and ARKAN == ("الواقع", "الإحساس", "الذهن",
                                                         "المعلومات السابقة")


def test_nisab_three_without_tadmin_and_majaz_in_the_judgement_ladder() -> None:
    names = [r[2] for r in ROWS]
    assert names[13:16] == ["الإسناد", "التقييد", "الإضافة"]  # ج3 393
    assert not any("التضمين" in n for n in names)
    assert names[16:18] == ["الفاعلية", "المفعولية"] and salaf(16) == ((13, True),)
    assert names[19:22] == ["العلاقة", "السببية", "المسببية"]  # ج3 432–434: علاقاتُ المجاز
    assert names[18].startswith("الإفادة") and all(s in (13, 14, 15, 16, 17) for s, _ in salaf(18))
    # الوضعُ فرعُ التصوّر: سوالفُه كلُّ المعلومات السابقة، منصوصةً
    assert salaf(12) == tuple((k, True) for k in range(1, 12))
    assert all(s < i for i in range(len(ROWS)) for s, _ in salaf(i))  # لا دور
    # ما ليس منصوصًا من السوالف رأيٌ من جدول المالك، يُوسَم كذلك
    assert salaf(9) == ((8, False),) and salaf(3) == ((2, False),)


def test_mutations_are_refused_by_name() -> None:
    m = _tool()
    j3 = _lines("nabhani-shakhsiyya-3.txt.gz", "359bb553")
    tafkir = _lines("nabhani-tafkir.txt.gz", "b9b08eab")
    m.verify(j3, tafkir)
    rows = list(m.ROWS)
    # عبارةٌ لا ترد في سطرها
    rid, lad, name, gr, anchors, sal, note = rows[1]
    m.ROWS = (*rows[:1], (rid, lad, name, gr, (("التفكير", 65, "الوجود يقيني بلا شك"),), sal, note),
              *rows[2:])
    with pytest.raises(SystemExit, match="PHRASE_NOT_IN_LINE"):
        m.verify(j3, tafkir)
    # ركنٌ بلا مرساةٍ ولا إعلان
    m.ROWS = (*rows[:1], (rid, lad, name, gr, (), sal, note), *rows[2:])
    with pytest.raises(SystemExit, match="ANCHOR_OR_DECLARATION_MISSING"):
        m.verify(j3, tafkir)
    # «التضمين» نسبةً
    rid, lad, name, gr, anchors, sal, note = rows[15]
    m.ROWS = (*rows[:15], (rid, lad, "التضمين", gr, anchors, sal, note), *rows[16:])
    with pytest.raises(SystemExit, match="TADMIN_IS_NOT_A_NISBA"):
        m.verify(j3, tafkir)
    # سالفٌ لاحق: دور
    rid, lad, name, gr, anchors, sal, note = rows[9]
    m.ROWS = (*rows[:9], (rid, lad, name, gr, anchors, (10,), note), *rows[10:])
    with pytest.raises(SystemExit, match="SALAF_NOT_EARLIER"):
        m.verify(j3, tafkir)
    m.ROWS = tuple(rows)
    m.verify(j3, tafkir)


def test_python_table_matches_the_lean_export() -> None:
    """`lake exe slge-table salsala` (formal/out/salsala.csv) يطبع الأركانَ من `SalsalaTable.lean`؛
    الجدولُ البايثونيُّ المولَّدُ من المودَع نفسِه يطابقه ركنًا ركنًا (السلّم، المرتبة، عددُ المراسي،
    السوالف)."""

    rows = (ROOT / "formal" / "out" / "salsala.csv").read_text(encoding="utf-8").splitlines()
    exported = [r.split(",") for r in rows if r.startswith("rukn,")]
    assert len(exported) == len(ROWS) == 22
    for (_, rid, lad, gr, n_anchors, sal), row in zip(exported, ROWS, strict=True):
        assert (int(rid), int(lad), int(gr), int(n_anchors)) == (row[0], row[1], row[3],
                                                                  len(row[4]))
        assert tuple(int(x) for x in sal.split("+") if x) == row[5]
    declared = next(r for r in rows if r.startswith("declared,")).split(",")[1:]
    assert sorted(int(d) for d in declared) == sorted(DECLARED)
