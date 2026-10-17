"""جدولُ اللزوم من شبكة المعاجم (`A116.Lazim`، `corpora/naql/lawazim.tsv`، ADR ١٠١).

التوقّعاتُ مستقلّةٌ عن `tools/gen_naql.py` وعن Lean:
١. جملُ الشواهد في نصّ ابن فارس المختوم بعينها (بلا حركات)، مكتوبةً هنا باليد.
٢. الأصنافُ على جملٍ مكتوبةٍ هنا: «لأنّه» تعليل، و«كأنّه» حملٌ ولو جاء معه «لأنّه»، و«مجاز» حمل،
   و«مجازاة» في «جزي» ليست حملًا، والشعرُ لا يدخل.
٣. اتّساقُ `LazimData.lean` مع الجدول بشيفرةٍ هنا.
الطفرات: `MUTANT_JAZA_AS_MAJAZ`، `MUTANT_TAALIL_BEFORE_HAML`، `MUTANT_POETRY_INCLUDED`.
"""

from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TSV = ROOT / "corpora" / "naql" / "lawazim.tsv"
DATA = ROOT / "formal" / "a116" / "A116" / "LazimData.lean"
MARKS = re.compile(r"[ً-ْٰـ]")
LEAN_NAMES = ("taalil_iltizam", "haml_la_iltizam", "la_lazim_bila_shahada", "lazim_muayyan",
              "haml_maluma_mashhuda", "jumal_count", "shawahid", "midad_iltizam")


def rows() -> list[list[str]]:
    return [ln.split("\t") for ln in TSV.read_text(encoding="utf-8").splitlines()]


def bare(s: str) -> str:
    return MARKS.sub("", s)


def body(root: str) -> str:
    with (ROOT / "maqayis_by_root_csv_999.csv").open(encoding="utf-8") as f:
        return "\n".join(bare(" ".join(r["body_text"].split("\n")))
                         for r in csv.DictReader(f) if r["root_full"].replace("ى", "ي") == root)


def test_witness_sentences_in_ibn_faris() -> None:
    hand = {"مدد": "والمداد: ما يكتب به، لأنه يمد بالماء",
            "تلو": "ومنه تلاوة القرآن، لأنه يتبع آية بعد آية",
            "خشي": "والمجاز قولهم خشيت بمعنى علمت",
            "طرف": "هذا هو الأصل ثم يسمون العين الطرف مجازا"}
    shurb = "ثم يحمل عليه ما يقاربه مجازا وتشبيها"
    assert shurb in body("شرب") and any(r[0] == "شرب" and shurb in bare(r[5]) for r in rows())
    rs = rows()
    for root, sent in hand.items():
        assert sent in body(root), root
        assert any(r[0] == root and bare(r[5]) == sent for r in rs), root


def test_kinds() -> None:
    rs = rows()
    kind = {(r[0], bare(r[5])): r[2] for r in rs}
    assert kind[("مدد", "والمداد: ما يكتب به، لأنه يمد بالماء")] == "taalil"
    assert kind[("خشي", "والمجاز قولهم خشيت بمعنى علمت")] == "haml"
    # MUTANT_TAALIL_BEFORE_HAML: فيها «لأنّه» و«كأنّه» معًا، فهي حمل
    both = next(k for k in kind if k[0] == "مرد" and "لأنه كأنه" in k[1])
    assert kind[both] == "haml"
    # MUTANT_JAZA_AS_MAJAZ: «وجازيته مجازاة» ليست حملًا ولا تعليلًا
    assert not any(r[0] == "جزي" and "مجازاة" in bare(r[5]) for r in rs)
    # MUTANT_POETRY_INCLUDED
    assert not any("…" in r[5] or "*" in r[5] or bare(r[5]).startswith("قال") for r in rs)


def test_data_consistent() -> None:
    rs = rows()
    src = DATA.read_text(encoding="utf-8")
    kinds = [sum(1 for r in rs if r[2] == k) for k in ("taalil", "haml")]
    wahid = [sum(1 for r in rs if r[2] == k and r[1] in ("wahid", "kalima"))
             for k in ("taalil", "haml")]
    assert f"def bisinf : List Nat := {kinds}" in src
    assert f"def biAslWahid : List Nat := {wahid}" in src
    lean = (ROOT / "formal" / "a116" / "A116" / "Lazim.lean").read_text(encoding="utf-8")
    assert f"LazimData.bisinf = {kinds}".replace(", ", ", ") in lean
    assert all(f"theorem {n}" in lean for n in LEAN_NAMES)
    audit = (ROOT / "formal" / "a116" / "Audit.lean").read_text(encoding="utf-8")
    assert all(f"A116.Lazim.{n}" in audit for n in LEAN_NAMES)
