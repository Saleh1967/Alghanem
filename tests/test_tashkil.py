"""تشكيلُ النصّ غير المشكول بمرشَّحي الوضع (`A116.Tashkil`، `tools/gen_tashkil.py`، ADR ١٠٣).

التوقّعاتُ مستقلّةٌ عن الأداة وعن Lean:
١. صورُ «قال» و«كتب» تُجمع هنا من المدوّنتين المختومتين بقراءةٍ مستقلّة، وتُطوى الناقصةُ في التامّة
   بقاعدةٍ هنا.
٢. المرجعُ المحجوب (Fadel) ليس مصدرًا للمعجم: لا يقرؤه بناءُ المعجم.
٣. شاهدٌ باليد: «قَالَ» صورةٌ واحدة، و«كتب» خمسُ صور منها «كَتَبَ» و«كُتِبَ».
الطفرات: `MUTANT_NO_TAMAM`، `MUTANT_FADEL_IN_MUJAM`.
"""

from __future__ import annotations

import gzip
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKS = set("ًٌٍَُِّْ")


def mujam() -> dict[str, list[str]]:
    path = ROOT / "corpora" / "tashkil" / "mujam.tsv.gz"
    text = gzip.decompress(path.read_bytes()).decode("utf-8")
    return {k: v.split(" ") for k, v in (ln.split("\t") for ln in text.splitlines())}


def raw_forms(skel: str) -> set[str]:
    texts = [(ROOT / "corpora" / "quran-simple-enhanced.txt").read_text(encoding="utf-8"),
             gzip.decompress((ROOT / "corpora" / "hadith" / "sahihain-lines.txt.gz").read_bytes())
             .decode("utf-8")]
    out = set()
    for t in texts:
        for tok in re.findall(r"[ء-يً-ْ]+", re.sub(r"<[^>]*>", " ", t)):
            f = unicodedata.normalize("NFC", tok)
            if "".join(c for c in f if c not in MARKS) == skel and any(c in MARKS for c in f):
                out.add(f)
    return out


def marks(f: str) -> list[set[str]]:
    out: list[set[str]] = []
    for c in f:
        if c in MARKS:
            out[-1].add(c)
        else:
            out.append(set())
    return out


def maximal(fs: set[str]) -> list[str]:
    return sorted(f for f in fs
                  if not any(g != f and all(a <= b for a, b in zip(marks(f), marks(g), strict=True))
                             for g in fs))


def test_qala_and_kataba() -> None:
    mj = mujam()
    raw = raw_forms("قال")
    assert len(raw) >= 2  # MUTANT_NO_TAMAM: بلا طيّ الناقصة تكون «قال» محتمَلة
    assert mj["قال"] == maximal(raw) == ["قَالَ"]
    kt = mj["كتب"]
    assert kt == maximal(raw_forms("كتب")) and len(kt) == 5 and "كَتَبَ" in kt and "كُتِبَ" in kt


def test_fadel_not_a_source() -> None:
    src = (ROOT / "tools" / "gen_tashkil.py").read_text(encoding="utf-8")
    body = src[src.index("def sources()"):src.index("def mujam()")]
    assert "FADEL" not in body  # MUTANT_FADEL_IN_MUJAM


def test_lean_names() -> None:
    lean = (ROOT / "formal" / "a116" / "A116" / "Tashkil.lean").read_text(encoding="utf-8")
    names = ("la_tashkil_bila_wad", "muayyan_min_mujam", "la_takhmin", "qayd_la_yazid", "shawahid",
             "mujam_count")
    assert all(f"theorem {n}" in lean for n in names)
    audit = (ROOT / "formal" / "a116" / "Audit.lean").read_text(encoding="utf-8")
    assert all(f"A116.Tashkil.{n}" in audit for n in names)
