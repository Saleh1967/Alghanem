"""الحكمُ الموحَّد من القابليّة الموروثة (`A116.HukmMuwahhad`، ADR ١٠٢).

التوقّعاتُ مستقلّةٌ عن Lean:
١. صفوفُ `Khawass.sufuf` تُقرأ من نصّ Lean، والوراثةُ والحكمُ بقاعدةٍ مكتوبةٍ هنا.
٢. أحكامٌ مكتوبةٌ باليد على الشواهد: «سجد القمر» بالتشبيه مجاز وبلا علاقة «لا حكم»؛
   «الكلبُ يُخاطَب» مجازٌ بالوراثة؛ «الإنسانُ يتكلّم» حقيقة؛ «الغول» «لا حكم».
الطفرات: `MUTANT_NO_INHERITANCE`، `MUTANT_NEGATION_IS_MAJAZ`، `MUTANT_ABSENCE_IS_NEGATION`.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
A = ROOT / "formal" / "a116" / "A116"
LEAN_NAMES = ("khass_yaghlib", "yarith", "la_saff", "haqiqa_iff", "majaz_iff",
              "la_majaz_bila_alaqa", "la_majaz_bila_wad", "la_hukm_bila_saff", "majaz_mithal",
              "qabil_mithal", "khawass_mithal", "shawahid", "dimagh_la_majaz")
# شرطُ المصدر في دوره، من نصّ السيرافيّ س23550–23552 كما في ADR ٩٦ (مكتوبٌ هنا).
SHART = {("khitab", "faail"): True, ("khitab", "mafool"): True, ("sujud", "faail"): True,
         ("ikhbar", "mafool"): False}


def rows() -> dict[str, tuple[bool, str | None]]:
    src = (A / "Khawass.lean").read_text(encoding="utf-8")
    out: dict[str, tuple[bool, str | None]] = {}
    pat = r'⟨"([^"]+)", (true|false), (\.nass|\.hasr|\.isa "[^"]+")'
    for jins, aqil, asl in re.findall(pat, src):
        parent = asl.split('"')[1] if asl.startswith(".isa") else None
        out[jins] = (aqil == "true", parent)
    return out


def verdict(jins: str, masdar: str, dawr: str, alaqa: bool, *, inherit: bool = True,
            neg_is_majaz: bool = False, absent_is_neg: bool = False) -> str:
    rs = rows()
    shart = SHART.get((masdar, dawr))
    q: bool | None = None
    if shart is not None and jins in rs:
        aqil, parent = rs[jins]
        if parent is not None:
            q = (rs[parent][0] if shart else True) if inherit else None
        else:
            q = aqil if shart else True
    if q is None:
        return "majaz" if absent_is_neg else "laHukm"
    if q:
        return "haqiqa"
    return "majaz" if (alaqa or neg_is_majaz) else "laHukm"


EXPECTED = {("القمر", "sujud", "faail", True): "majaz",
            ("القمر", "sujud", "faail", False): "laHukm",
            ("الكلب", "khitab", "mafool", True): "majaz",
            ("الإنسان", "khitab", "faail", True): "haqiqa",
            ("الغول", "khitab", "faail", True): "laHukm"}


def test_rows_read() -> None:
    rs = rows()
    assert rs["الكلب"] == (False, "ذوات الأربع") and rs["ذوات الأربع"] == (False, None)
    assert rs["الإنسان"] == (True, None) and "الغول" not in rs


def test_verdicts() -> None:
    for (j, m, d, a), v in EXPECTED.items():
        assert verdict(j, m, d, a) == v, (j, m, d, a)


def test_mutants_rejected() -> None:
    assert verdict("الكلب", "khitab", "mafool", True, inherit=False) != "majaz"
    assert verdict("القمر", "sujud", "faail", False, neg_is_majaz=True) != "laHukm"
    assert verdict("الغول", "khitab", "faail", True, absent_is_neg=True) != "laHukm"


def test_lean_names() -> None:
    src = (A / "HukmMuwahhad.lean").read_text(encoding="utf-8")
    assert all(f"theorem {n}" in src for n in LEAN_NAMES)
    audit = (ROOT / "formal" / "a116" / "Audit.lean").read_text(encoding="utf-8")
    assert all(f"A116.HukmMuwahhad.{n}" in audit for n in LEAN_NAMES)
