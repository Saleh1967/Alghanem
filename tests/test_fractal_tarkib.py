"""فراكتالُ التركيب (`A116.FractalTarkib`، ADR ٨٠): أزواجُ الألفاظ بأقسامها على المصحف.

التوقّعاتُ مستقلّةٌ عن Lean وعن `gen_qac_pos.segments`: قارئٌ مكتوبٌ هنا لملفّ QAC المختوم (`gen_qac.QAC`،
ببصمته) سطرًا سطرًا، والقسمةُ مكتوبةٌ هنا من الألفيّة (الأسماءُ والضمائرُ والإشارةُ والموصولُ والظروف اسم،
والفعلُ فعل، وما سواهما حرف، و«أل» علامةُ الاسم لا كلمة):
١. المودَعُ (`FractalTarkibData.lean`) هو أقسامُ هذا القارئ آيةً آية.
٢. أعدادُ الأنواع التسعة في `FractalTarkibCount.lean` هي عدُّ هذا القارئ، وكلُّ نوعٍ واقع.
٣. أزواجُ كلّ آيةٍ كلماتُها ناقصًا واحدًا (`azwaj_length`).
٤. الآياتُ التي فيها إسنادٌ بين متجاورين (اسمٌ على اسم، أو فعلٌ على اسم) عددُها عددُ `isnad_mushaf`.
٥. الطفرتان: عدُّ «أل» كلمةً (`MUTANT_DET_IS_KALIMA`) والضميرُ حرفًا (`MUTANT_PRON_IS_HARF`)
   يغيّران الأعداد.
"""

from __future__ import annotations

import gzip
import hashlib
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QAC = ROOT / "corpora" / "qac" / "quranic-corpus-morphology-0.4.txt.gz"
DATA = ROOT / "formal" / "a116" / "A116" / "FractalTarkibData.lean"
COUNT = ROOT / "formal" / "a116" / "A116" / "FractalTarkibCount.lean"
LEAN = ROOT / "formal" / "a116" / "A116" / "FractalTarkib.lean"

ISM = {"N", "PN", "ADJ", "PRON", "DEM", "REL", "T", "LOC", "IMPN"}


def verses(skip: frozenset[str] = frozenset({"DET"}), ism: frozenset[str] = frozenset(ISM)
           ) -> list[list[int]]:
    raw = gzip.decompress(QAC.read_bytes()).decode("utf-8")
    out: dict[tuple[int, int], list[tuple[int, int, int]]] = {}
    for ln in raw.splitlines():
        if not ln.startswith("("):
            continue
        loc, _form, tag, _feats = ln.split("\t")
        s, v, w, g = (int(x) for x in loc.strip("()").split(":"))
        if tag in skip:
            continue
        q = 0 if tag in ism else 1 if tag == "V" else 2
        out.setdefault((s, v), []).append((w, g, q))
    return [[q for _w, _g, q in sorted(out[k])] for k in sorted(out)]


def pairs(vs: list[list[int]]) -> Counter[tuple[int, int]]:
    return Counter((a, b) for r in vs for a, b in zip(r, r[1:], strict=False))


def isnad(vs: list[list[int]]) -> int:
    return sum(1 for r in vs if any(p in ((0, 0), (1, 0)) for p in zip(r, r[1:], strict=False)))


VS = verses()


def test_qac_sealed() -> None:
    sha = hashlib.sha256(gzip.decompress(QAC.read_bytes())).hexdigest()
    seal = re.search(r'^QAC_SHA256 = "([0-9a-f]+)"', (ROOT / "tools" / "gen_qac.py").read_text(
        encoding="utf-8"), re.M)
    assert seal and sha == seal.group(1)


def test_deposit_is_reader() -> None:
    text = DATA.read_text(encoding="utf-8")
    found = re.findall(r"^  \[([0-9, ]*)\][,\]]?$", text, re.M)
    rows = [[int(x) for x in m.split(", ")] if m else [] for m in found]
    assert rows == VS


def test_nine_kinds_counted() -> None:
    p = pairs(VS)
    expected = [p[(a, b)] for a in range(3) for b in range(3)]
    assert all(expected)
    m = re.search(r"ayat\.foldl cntPairs \[0, 0, 0, 0, 0, 0, 0, 0, 0\] = \[([0-9, ]+)\]",
                  COUNT.read_text(encoding="utf-8"))
    assert m and [int(x) for x in m.group(1).split(", ")] == expected


def test_pairs_are_kalimat_minus_one() -> None:
    assert sum(pairs(VS).values()) == sum(len(r) - 1 for r in VS)


def test_isnad_count() -> None:
    m = re.search(r"lic isnadT \(aya r\)\)\.length = ([0-9]+)", LEAN.read_text(encoding="utf-8"))
    assert m and int(m.group(1)) == isnad(VS)


def test_mutants_rejected() -> None:
    assert pairs(verses(skip=frozenset())) != pairs(VS)
    assert isnad(verses(ism=frozenset(ISM - {"PRON"}))) != isnad(VS)
