"""قياسُ وظائف المغلق بأبواب الحاجة على وسوم QAC، بالتسجيل المسبق `docs/haja/PREREG.md`
(ADR ٥٨).

لكلّ موقعٍ محاذًى في `qac-pos.tsv.gz`: أبوابُ قراءاته المغلقة (`haja.core_babs` لكلّ نواةٍ من
`mughlaq.closed`) مقابلَ وسم جذعه في QAC بالتعيين المسجَّل (`TAGS`). يكتب
`docs/haja/qac-result.json`، وبـ`--check` يعيد الحساب ويقارن.
لا يُحرَّر الناتجُ باليد.
"""

from __future__ import annotations

import gzip
import json
import math
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from slge.haja import core_babs
from slge.mughlaq import closed

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "tests" / "data"
OUT = ROOT / "docs" / "haja" / "qac-result.json"
Word = tuple[tuple[str, str], ...]

TAGS: dict[str, frozenset[str]] = {
    "jarr": frozenset({"P"}), "mushabbaha": frozenset({"ACC"}), "atf": frozenset({"CONJ"}),
    "istithna": frozenset({"EXP", "RES"}), "shart": frozenset({"COND"}), "nafy": frozenset({"NEG"}),
    "amilFil": frozenset({"NEG", "FUT", "CERT", "PRO", "SUB"}), "tanbih": frozenset({"INC"}),
    "jawab": frozenset({"ANS"}), "rad": frozenset({"AVR"}), "istifham": frozenset({"INTG"}),
    "nida": frozenset({"VOC"}), "damir": frozenset({"PRON"}), "mawsul": frozenset({"REL"}),
}
"""التعيينُ المسجَّل (PREREG §٢): البابُ ← وسومُ جذع QAC."""

GOLD: frozenset[str] = frozenset().union(*TAGS.values())


def wilson(k: int, n: int, z: float = 1.959963984540054) -> tuple[float, float]:
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    r = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - r) / d, (c + r) / d)


def babs_of(w: Word) -> tuple[str, ...]:
    out: list[str] = []
    for m in closed(w):
        for b in core_babs(m.core):
            if b in TAGS and b not in out:
                out.append(b)
    return tuple(out)


def judge(gold: str, babs: tuple[str, ...]) -> tuple[bool, bool, bool, bool]:
    """(ذهبيٌّ وظيفيّ، له أبواب، أبوابُه تحمل وسمَه، بابٌ واحدٌ صحيح)."""

    hit = any(gold in TAGS[b] for b in babs)
    return (gold in GOLD, bool(babs), hit, hit and len(babs) == 1)


def verdict(m1_low: float, m2_low: float) -> str:
    jami, mani = m1_low >= 0.95, m2_low >= 0.90
    if jami and mani:
        return "HAJA_JAMI_MANI"
    if jami:
        return "HAJA_JAMI"
    if mani:
        return "HAJA_MANI"
    return "HAJA_GAPS"


def _load() -> list[tuple[Word, str]]:
    with gzip.open(DATA / "corpus-certificates.json.gz", "rt", encoding="utf-8") as f:
        d: dict[str, Any] = json.load(f)
    forms = [tuple((a, b) for a, b in x["cells"]) for x in d["forms"]]
    stream: list[int] = d["stream"]
    rows: list[tuple[Word, str]] = []
    with gzip.open(DATA / "qac-pos.tsv.gz", "rt", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i == 0:
                continue
            tok, _loc, _segs, stem = line.rstrip("\n").split("\t")
            rows.append((forms[stream[int(tok)]], stem))
    return rows


def measure() -> dict[str, Any]:
    cache: dict[Word, tuple[str, ...]] = {}
    n_gold = n_has = k1 = k2 = k3 = 0
    miss: Counter[str] = Counter()
    wrong: Counter[str] = Counter()
    for w, gold in _load():
        if w not in cache:
            cache[w] = babs_of(w)
        babs = cache[w]
        is_gold, has, hit, single = judge(gold, babs)
        if is_gold:
            n_gold += 1
            k1 += hit
            k3 += single
            if not hit:
                miss[f"{gold}|{'+'.join(babs) or '—'}"] += 1
        if has:
            n_has += 1
            k2 += hit
            if not hit:
                wrong[f"{gold}|{'+'.join(babs)}"] += 1
    m1, m2, m3 = wilson(k1, n_gold), wilson(k2, n_has), wilson(k3, n_gold)
    def row(k: int, n: int, ci: tuple[float, float]) -> dict[str, Any]:
        return {"k": k, "n": n, "p": round(k / n, 6), "ci": [round(x, 6) for x in ci]}

    return {
        "prereg": "docs/haja/PREREG.md",
        "m1_jami": row(k1, n_gold, m1),
        "m2_mani": row(k2, n_has, m2),
        "m3_hasm": row(k3, n_gold, m3),
        "verdict": verdict(m1[0], m2[0]),
        "gaps_jami": dict(miss.most_common(10)),
        "gaps_mani": dict(wrong.most_common(10)),
    }


def main(argv: list[str]) -> int:
    got = measure()
    text = json.dumps(got, ensure_ascii=False, indent=1, sort_keys=True) + "\n"
    if "--check" in argv:
        ok = OUT.read_text(encoding="utf-8") == text
        sys.stdout.write("qac-result.json مطابق\n" if ok else "qac-result.json غيرُ مطابق\n")
        return 0 if ok else 1
    OUT.write_text(text, encoding="utf-8")
    sys.stdout.write(f"كُتب {OUT.name}: {got['verdict']}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
