"""شجرةُ الأجناس من «المخصَّص» (`A116.AjnasMukhassas`، `corpora/mukhassas/ajnas.tsv`، ADR ١٠٤).

التوقّعاتُ مستقلّةٌ عن Lean:
١. كلُّ صفٍّ عقدتُه في `nodes.tsv` بعنوانها وكتابها وسطرها، وسطرُها في المخصَّص المختوم رأسُ الباب بعنوانه.
٢. صفوفُ Lean هي صفوفُ المودَع بأعيانها.
٣. نصُّ التفكير س23 في سطره.
الطفرة: `MUTANT_TITLE_NOT_IN_LINE` (عنوانٌ في غير سطره يُلتقط).
"""

from __future__ import annotations

import gzip
import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
M = ROOT / "corpora" / "mukhassas"


def rows() -> list[list[str]]:
    return [ln.split("\t") for ln in (M / "ajnas.tsv").read_text(encoding="utf-8").splitlines()[1:]]


def mukhassas() -> list[str]:
    raw = gzip.decompress((M / "0458IbnSidaMursi.Mukhassas.Shamela0003590-ara1.gz").read_bytes())
    assert hashlib.sha256(raw).hexdigest() == (
        "936c68e0c2c62ddbfb881c573487c7b37650ef69117bca364c219b6d1bf8e76c")
    return raw.decode("utf-8").splitlines()


def in_line(title: str, line: str) -> bool:
    return line.startswith("### ") and title in line


def test_rows_anchored() -> None:
    nodes = {r.split("\t")[0]: r.split("\t")
             for r in (M / "nodes.tsv").read_text(encoding="utf-8").splitlines()[1:]}
    text = mukhassas()
    for jins, node, line, title, book in rows():
        n = nodes[node]
        assert (n[1], n[3], n[4]) == (line, book, title), jins
        assert in_line(title, text[int(line) - 1]), jins
        # MUTANT_TITLE_NOT_IN_LINE
        assert not in_line(title, text[int(line)])


def test_lean_rows_are_deposit() -> None:
    src = (ROOT / "formal" / "a116" / "A116" / "AjnasMukhassas.lean").read_text(encoding="utf-8")
    lean = re.findall(r'⟨"([^"]+)", (\d+), (\d+), "([^"]+)"⟩', src)
    assert lean == [(j, n, s, b) for j, n, s, _, b in rows()]


def test_tafkir_anchor() -> None:
    path = ROOT / "corpora" / "nabhani" / "tafkir.txt.gz"
    raw = gzip.decompress(path.read_bytes()).decode("utf-8")
    assert "العقل غير موجود إلا عند الإنسان" in raw.splitlines()[22]
