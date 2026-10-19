"""الضميرُ والإحالةُ والموصولُ والإشارة (`A116.Ihala`، ADR ٨٣).

التوقّعاتُ مستقلّةٌ عن Lean:
١. كلُّ مرساةٍ في `Ihala.marasi` نصٌّ في سطرها بعينه من شرح ابن عقيل المختوم (ببصمته).
٢. الحضورُ الثلاثيّ (`Hudur`) يستوفي ضمائرَ المصحف كلَّها: كلُّ قطعةٍ وسمُها `PRON` في QAC المختوم لها شخصٌ
   واحدٌ من 1 (متكلّم) و2 (مخاطب) و3 (غائب)، والأقسامُ الثلاثة واقعة.
الطفرات: `MUTANT_LINE_SHIFTED`، `MUTANT_HUDUR_TWO` (حضورٌ ثنائيٌّ بلا المتكلّم يترك ضمائر بلا قسم).
"""

from __future__ import annotations

import gzip
import hashlib
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHARH = ROOT / "corpora" / "ibn-aqil" / "sharh-alfiyya.txt.gz"
QAC = ROOT / "corpora" / "qac" / "quranic-corpus-morphology-0.4.txt.gz"
LEAN = ROOT / "formal" / "a116" / "A116" / "Ihala.lean"
SHA = "661e43ea265eca8c72b9e4ab7a46cd9182b34e834105b595241bc7787b471f09"


def lines() -> list[str]:
    raw = gzip.decompress(SHARH.read_bytes())
    assert hashlib.sha256(raw).hexdigest() == SHA
    return raw.decode("utf-8").splitlines()


def marasi() -> list[tuple[int, str]]:
    text = LEAN.read_text(encoding="utf-8")
    return [(int(n), q) for n, q in re.findall(r'\((\d+), "([^"]+)"\)', text)]


def anchored(ms: list[tuple[int, str]], ls: list[str]) -> bool:
    return all(q in ls[n] for n, q in ms)


def persons(classes: tuple[str, ...]) -> Counter[str]:
    out: Counter[str] = Counter()
    for ln in gzip.decompress(QAC.read_bytes()).decode("utf-8").splitlines():
        if ln.startswith("("):
            _loc, _form, tag, feats = ln.split("\t")
            if tag == "PRON":
                hit = [c for f in feats.split("|") for c in classes
                       if f.removeprefix("PRON:").startswith(c)]
                out[hit[0] if len(hit) == 1 else "NONE"] += 1
    return out


def test_marasi_in_sealed_lines() -> None:
    ms = marasi()
    assert len(ms) == 12 and anchored(ms, lines())


def test_hudur_exhausts_mushaf_pronouns() -> None:
    c = persons(("1", "2", "3"))
    assert c["NONE"] == 0 and all(c[k] > 0 for k in ("1", "2", "3"))


def test_mutants_rejected() -> None:
    assert not anchored([(n + 1, q) for n, q in marasi()], lines())
    assert persons(("2", "3"))["NONE"] > 0
