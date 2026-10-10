"""السلسلة (ADR ٣١، ٣٢): توقّعاتٌ مستقلّةٌ عن الشيفرة من نصّ النبهانيّ المختوم وقرار المالك
(2026-10-10) — ثلاثةُ سلالم، اليقينُ للوجود والحقائق وحدَهما («قطعية عن وجود الشيء… ظنية عن كنهه
وصفته»)، الجذرُ الأركانُ الأربعة لا «أوليات»، النسبُ إسنادٌ وتقييدٌ وإضافةٌ بلا «تضمين»، السببيّةُ
والمسببيّةُ علاقتا مجازٍ في الحكم، الفاعليّةُ والمفعوليّةُ نسبتان بعد الإسناد، وكلُّ ركنٍ بسطره من المختوم
أو معلَنٌ باسمه؛ ثمّ سُلَّما الغزاليّ خارج العمود («نختم وفق النبهاني»): مصادرُ اليقين السبعة من المستصفى
بسطرها، وأوليّاتُه خلافًا مسجَّلًا بلا سالفٍ في العمود؛ وشواهدُ الغزاليّ الثانية على العمود لا تُرسي
(ADR ٣٣)؛ وطفراتٌ مرفوضة."""

from __future__ import annotations

import gzip
import hashlib
import importlib.util
import sys
from pathlib import Path
from typing import Any

import pytest

from slge.salsala import (
    ARKAN,
    DECLARED,
    LADDERS,
    ROWS,
    SHAWAHID,
    anchored,
    grade,
    ladder,
    salaf,
    shahid,
)

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "tests" / "data"
SEALED = {"ج3": ("nabhani-shakhsiyya-3.txt.gz", "359bb553"),
          "التفكير": ("nabhani-tafkir.txt.gz", "b9b08eab"),
          "المستصفى": ("openiti-ghazali-mustasfa.txt.gz", "59cda7d5"),
          "محك النظر": ("openiti-ghazali-mihakk.txt.gz", "9e54d050"),
          "معيار العلم": ("openiti-ghazali-micyar.txt.gz", "2ddf9165")}


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


def _texts() -> dict[str, list[str]]:
    return {src: _lines(name, prefix) for src, (name, prefix) in SEALED.items()}


def test_every_rukn_is_anchored_in_the_sealed_text_or_declared_by_name() -> None:
    texts = _texts()
    for rid, _, name, _, anchors, _, note in ROWS:
        if rid in DECLARED:
            assert not anchors and "معلَن" in note, name
            continue
        assert anchors, name
        for src, line, phrase in anchors:
            assert phrase in texts[src][line - 1], (name, src, line, phrase)
    assert {7, 10, 11} == DECLARED  # القابليّات، المكان، العدد — بقرار المالك لا من الذاكرة
    assert sum(1 for i in range(len(ROWS)) if anchored(i)) == 31


def test_three_ladders_with_the_ranked_tag() -> None:
    assert [ladder(i) for i in (0, 11, 12, 18, 19, 21)] == [
        "المعلومات السابقة", "المعلومات السابقة", "الوضع والنسب", "الوضع والنسب",
        "الحكم: علاقات المجاز", "الحكم: علاقات المجاز"]
    # التفكير 65 و123: اليقينُ في الوجود وحقائقه، والظنُّ في الكنه والصفات
    assert [i for i in range(len(ROWS)) if grade(i) == "يقين"] == [1, 2]
    assert all(grade(i) == "ظنّ" for i in range(3, 12))
    assert all(grade(i) == "—" for i in range(12, len(ROWS))) and grade(0) == "—"
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


def test_ghazali_ladders_are_outside_the_spine_and_sourced_by_name() -> None:
    """ADR ٣٢: (د) مصادرُ اليقين السبعة من المستصفى 1351–1460 بترتيب الغزاليّ نفسِه، و(هـ) أوليّاتُه
    G1–G4 والكمّ؛ كلاهما مرسًى في مودَع الغزاليّ باسمه، بلا مرتبةٍ ولا سالفٍ في العمود؛ والعمودُ (أ–ج)
    لا يُرسى إلّا في النبهانيّ."""

    assert len(LADDERS) == 5 and len(ROWS) == 34
    seven = [r for r in ROWS if r[1] == 3]
    assert [r[2] for r in seven] == ["الأوليات (مصدرًا)", "المشاهدات الباطنة", "المحسوسات الظاهرة",
                                     "التجريبيات", "المتواترات", "الوهميات", "المشهورات"]
    assert [r[4][0][1] for r in seven] == [1351, 1363, 1367, 1376, 1405, 1414, 1458]
    assert all(r[4][0][0] == "المستصفى" for r in seven)
    outside = [r for r in ROWS if r[1] == 4]
    assert [r[2][-4:-1] for r in outside[:4]] == ["(G1", "(G2", "(G3", "(G4"]
    assert outside[-1][2].endswith("(الكمّ)")
    # خارج العمود: لا سالفَ ولا مرتبة، ومرساةٌ عند الغزاليّ لا غير
    for r in [*seven, *outside]:
        assert not r[5] and grade(r[0]) == "—" and anchored(r[0])
        assert all(src != "ج3" or r[2] == "المتواترات" for src, _, _ in r[4])
    # ملتقيا المصدرين: الحسّ (التفكير 22) والتواترُ بلا عدد (ج3 308 مع المستصفى 1408)
    sources = {r[2]: {a[0] for a in r[4]} for r in seven}
    assert sources["المحسوسات الظاهرة"] == {"المستصفى", "التفكير"}
    assert sources["المتواترات"] == {"المستصفى", "ج3"}
    # العمودُ لا يُرسى في الغزاليّ
    assert all(src in ("ج3", "التفكير") for r in ROWS if r[1] < 3 for src, _, _ in r[4])


def test_second_witnesses_from_ghazali_do_not_anchor_or_undeclare() -> None:
    """ADR ٣٣ (إذنُ المالك «كشاهدٍ أو رأيٍ ثانٍ»): شواهدُ الغزاليّ على أركان العمود — المكانُ (محكّ النظر
    329 «لا يكون في مكانين»، معيار العلم «في الأين») والعددُ (المستصفى 619، «في الكم») والزمانُ («في
    المتى») والأجناسُ («الجنس والنوع») — بسطرها، من خارج العمود، ولا تُرسي: المعلَناتُ الثلاث تبقى
    معلَنة."""

    texts = _texts()
    assert len(SHAWAHID) == 6
    for rid, src, line, phrase, _ in SHAWAHID:
        assert src in ("المستصفى", "محك النظر", "معيار العلم") and ROWS[rid][1] < 3
        assert phrase in texts[src][line - 1], (rid, src, line, phrase)
    assert {s[0] for s in SHAWAHID} == {4, 9, 10, 11}
    assert ("محك النظر", 329) in {(s[1], s[2]) for s in shahid(10)}
    assert ("المستصفى", 619) in {(s[1], s[2]) for s in shahid(11)}
    assert shahid(7) == () and shahid(0) == ()
    assert {7, 10, 11} == DECLARED and all(not anchored(i) for i in DECLARED)


def test_mutations_are_refused_by_name() -> None:
    m = _tool()
    texts = _texts()
    m.verify(texts)
    rows = list(m.ROWS)
    # عبارةٌ لا ترد في سطرها
    rid, lad, name, gr, anchors, sal, note = rows[1]
    m.ROWS = (*rows[:1], (rid, lad, name, gr, (("التفكير", 65, "الوجود يقيني بلا شك"),), sal, note),
              *rows[2:])
    with pytest.raises(SystemExit, match="PHRASE_NOT_IN_LINE"):
        m.verify(texts)
    # ركنٌ بلا مرساةٍ ولا إعلان
    m.ROWS = (*rows[:1], (rid, lad, name, gr, (), sal, note), *rows[2:])
    with pytest.raises(SystemExit, match="ANCHOR_OR_DECLARATION_MISSING"):
        m.verify(texts)
    # «التضمين» نسبةً
    rid, lad, name, gr, anchors, sal, note = rows[15]
    m.ROWS = (*rows[:15], (rid, lad, "التضمين", gr, anchors, sal, note), *rows[16:])
    with pytest.raises(SystemExit, match="TADMIN_IS_NOT_A_NISBA"):
        m.verify(texts)
    # سالفٌ لاحق: دور
    rid, lad, name, gr, anchors, sal, note = rows[9]
    m.ROWS = (*rows[:9], (rid, lad, name, gr, anchors, (10,), note), *rows[10:])
    with pytest.raises(SystemExit, match="SALAF_NOT_EARLIER"):
        m.verify(texts)
    # مودَعٌ غيرُ مختوم باسمه
    rid, lad, name, gr, anchors, sal, note = rows[29]
    m.ROWS = (*rows[:29], (rid, lad, name, gr, (("الإحياء", 1, "x"),), sal, note), *rows[30:])
    with pytest.raises(SystemExit, match="UNKNOWN_SOURCE"):
        m.verify(texts)
    # أوليّةُ الغزاليّ تُبنى على ركنٍ من العمود: دمجٌ مرفوض
    m.ROWS = (*rows[:29], (rid, lad, name, gr, anchors, (1,), note), *rows[30:])
    with pytest.raises(SystemExit, match="OUTSIDE_SPINE_HAS_SALAF"):
        m.verify(texts)
    m.ROWS = tuple(rows)
    # شاهدٌ ثانٍ من العمود نفسِه: ليس شاهدًا ثانيًا بل مرساةٌ مدّعاة
    shawahid = m.SHAWAHID
    m.SHAWAHID = (*shawahid, (10, "ج3", 393, "نقل الواقع", ""))
    with pytest.raises(SystemExit, match="SHAHID_NOT_FROM_SECOND_SOURCE"):
        m.verify(texts)
    # شاهدٌ على ركنٍ خارج العمود
    m.SHAWAHID = (*shawahid, (29, "المستصفى", 1353, "علم الإنسان بوجود نفسه", ""))
    with pytest.raises(SystemExit, match="SHAHID_TARGET_OUTSIDE_SPINE"):
        m.verify(texts)
    m.SHAWAHID = shawahid
    m.verify(texts)


def test_python_table_matches_the_lean_export() -> None:
    """`lake exe slge-table salsala` (formal/out/salsala.csv) يطبع الأركانَ من `SalsalaTable.lean`؛
    الجدولُ البايثونيُّ المولَّدُ من المودَع نفسِه يطابقه ركنًا ركنًا (السلّم، المرتبة، عددُ المراسي،
    السوالف)."""

    rows = (ROOT / "formal" / "out" / "salsala.csv").read_text(encoding="utf-8").splitlines()
    exported = [r.split(",") for r in rows if r.startswith("rukn,")]
    assert len(exported) == len(ROWS) == 34
    for (_, rid, lad, gr, n_anchors, sal), row in zip(exported, ROWS, strict=True):
        assert (int(rid), int(lad), int(gr), int(n_anchors)) == (row[0], row[1], row[3],
                                                                  len(row[4]))
        assert tuple(int(x) for x in sal.split("+") if x) == row[5]
    declared = next(r for r in rows if r.startswith("declared,")).split(",")[1:]
    assert sorted(int(d) for d in declared) == sorted(DECLARED)
