"""حروفُ العطف (`A116.Atf`، ADR ٨٢): مراسي Lean أسطرٌ بأعيانها في شرح ابن عقيل المختوم.

التوقّعاتُ مستقلّةٌ عن Lean: القسمةُ مقروءةٌ هنا من نصّ الشرح نفسه (س6446–6453) لا من `ishrak`.
١. الشرحُ المختوم ببصمته (`gen_lane_khatm.IBN_AQIL_SHA`، منسوخةً هنا باليد).
٢. كلُّ مرساةٍ في `Atf.marasi` نصٌّ في سطرها بعينه.
٣. الحروفُ التي «تُشرك لفظًا وحكمًا» في س6446–6449 ستّةٌ باليد، و«لفظًا فقط» في س6451 ثلاثة — وهي عددا
   `ishrak_count` في Lean.
الطفرات: `MUTANT_LINE_SHIFTED` (المرساةُ في السطر التالي)،
`MUTANT_QUOTE_ALTERED` (التخيير ↔ الإباحة).
"""

from __future__ import annotations

import gzip
import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHARH = ROOT / "corpora" / "ibn-aqil" / "sharh-alfiyya.txt.gz"
LEAN = ROOT / "formal" / "a116" / "A116" / "Atf.lean"
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


def test_marasi_in_sealed_lines() -> None:
    ms, ls = marasi(), lines()
    assert len(ms) == 12 and anchored(ms, ls)


def test_ishrak_from_text() -> None:
    ls = lines()
    both = " ".join(ls[6446:6450])
    six = ["الواو", "وثم", "والفاء", "وحتى", "وأم", "وأو"]
    assert all(w in both for w in six)
    assert "بل ولا" in ls[6451] and "لكن" in ls[6451]
    text = LEAN.read_text(encoding="utf-8")
    assert "= 6 ∧" in text and "= 3 ∧" in text


def test_mutants_rejected() -> None:
    ms, ls = marasi(), lines()
    assert not anchored([(n + 1, q) for n, q in ms], ls)
    swapped = [(n, q.replace("للتخيير", "للإباحة")) for n, q in ms]
    assert not anchored(swapped, ls)
