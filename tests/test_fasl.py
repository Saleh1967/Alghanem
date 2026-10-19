"""قانونُ الفصل (`A116.Fasl`، ADR ٧٤) مقروءًا من الجدول المولَّد لا من Lean.

التوقّعاتُ مكتوبةٌ هنا باليد من صفوف سيبويه في «الكتاب» المختوم
(المخارجُ الستّةَ عشر بحروفها، واللامُ من السيرافيّ)،
ثمّ يُعاد الحسابُ على أعمدة `formal/a116/huruf.csv` بشيفرةٍ مستقلّة:

١. **المانعُ بالمخرج وحدَه**: أزواجُ الحروف المختلفة من مخرجٍ واحد؛
   مجموعاتُها مجموعاتُ اليد، وعددُها المرتّب ‎Σ s(s−1) = 40‎ (`makhraj_mani_count`).
٢. **الفصلُ بالمخرج وأربع صفات** (الهمس، الشدّة، التوسّط، الاستعلاء):
   29 مفتاحًا مختلفًا (`nutq_fasl`)، ولا يفصل إن أُسقطت واحدة (`nutq_mukhtamal`)،
   ولا تفصل ثلاثُ صفاتٍ أو أقلّ مع المخرج.
٣. **الاستنفادُ بالشرط**: حرفا الغنّة من مخرجين (`ghunna_shart`).
٤. **الدور**: الخاناتُ المتحرّكة المرخَّصة 84 دورُها واحد، ومنها بَ وتَ (`dawr_mani`).

الطفرات: `MUTANT_HAND_GROUP`، `MUTANT_CSV_MAKHRAJ_MERGE`، `MUTANT_CSV_HAMS_FLIP`.
"""

from __future__ import annotations

import csv
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "formal" / "a116" / "huruf.csv"
LEAN = ROOT / "formal" / "a116" / "A116" / "Fasl.lean"
AUDIT = ROOT / "formal" / "a116" / "Audit.lean"

# من صفوف سيبويه باليد (ترتيبُها لا يدخل الحساب).
HAND_GROUPS = [
    "ءها", "عح", "غخ", "ق", "ك", "جشي", "ض", "ل", "ن", "ر", "طدت", "زسص", "ظذث", "ف", "بمو",
]
FOUR = ["hams", "shidda", "tawassut", "istila"]
SIFAT = ["hams", "shidda", "tawassut", "istila", "itbaq", "idhlaq", "safir", "qalqala", "lin",
         "inhiraf", "takrir", "tafashi", "istitala", "ghunna"]
THEOREMS = ["fasl_iff_no_mani", "tayin_sound", "tayin_of_fasl", "fasl_of_tayin",
            "mani_blocks_tayin",
            "istinfad_sabab", "sabab_mono", "sabab_coarse", "istinfad_shart", "shart_mono",
            "thalatha_la_tafsil", "mawdi_fasl", "khana_mani", "makhraj_mani", "makhraj_mani_count",
            "nutq_fasl", "nutq_tayin", "nutq_mukhtamal", "ghunna_shart", "dawr_mani",
            "ternary_la_tafsil",
            "dal_mani", "dal_la_tayin"]


def letters(rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {r["harf"]: r for r in rows if r["haraka"] == "fatha"}


def load() -> list[dict[str, str]]:
    with TABLE.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def mani(rows: dict[str, dict[str, str]], cols: list[str]) -> set[tuple[str, str]]:
    key = {c: tuple(r[k] for k in ["makhraj16", *cols]) for c, r in rows.items()}
    return {(a, b) for a in key for b in key if a != b and key[a] == key[b]}


def hand_mani(groups: list[str]) -> set[tuple[str, str]]:
    return {(a, b) for g in groups for a in g for b in g if a != b}


def check(rows_all: list[dict[str, str]], groups: list[str]) -> list[str]:
    bad: list[str] = []
    rows = letters(rows_all)
    if len(rows) != 29 or sorted("".join(groups)) != sorted(rows):
        bad.append("LETTERS")
    m0 = mani(rows, [])
    if m0 != hand_mani(groups):
        bad.append("MAKHRAJ_MANI_GROUPS")
    if len(m0) != sum(len(g) * (len(g) - 1) for g in HAND_GROUPS) or len(m0) != 40:
        bad.append("MAKHRAJ_MANI_COUNT")
    if mani(rows, FOUR):
        bad.append("NUTQ_FASL")
    if any(not mani(rows, [s for s in FOUR if s != d]) for d in FOUR):
        bad.append("NUTQ_MUKHTAMAL")
    if any(not mani(rows, list(ss)) for k in range(4) for ss in combinations(SIFAT, k)):
        bad.append("NO_THREE")
    ghunna = {c: r for c, r in rows.items() if r["ghunna"] == "1"}
    if sorted(ghunna) != sorted("نم") or mani(ghunna, []):
        bad.append("GHUNNA_SHART")
    moving = [r for r in rows_all if r["licensable"] == "true" and r["haraka"] != "sukun"]
    harf = {r["harf"] for r in moving}
    if len(moving) != 84 or not {"ب", "ت"} <= harf:
        bad.append("DAWR")
    return bad


def test_fasl_table() -> None:
    assert check(load(), HAND_GROUPS) == []


def test_theorems_named_and_audited() -> None:
    src = LEAN.read_text(encoding="utf-8")
    audit = AUDIT.read_text(encoding="utf-8")
    for t in THEOREMS:
        assert f"theorem {t}" in src, t
        assert f"#print axioms A116.Fasl.{t}\n" in audit, t
    assert "sorry" not in src and "native_decide" not in src and "\naxiom " not in src


def test_mutants_rejected() -> None:
    rows = load()
    assert check(rows, ["ءه", "ا", *HAND_GROUPS[1:]]), "MUTANT_HAND_GROUP"
    merged = [dict(r, makhraj16="10") if r["makhraj16"] == "11" else r for r in rows]
    assert check(merged, HAND_GROUPS), "MUTANT_CSV_MAKHRAJ_MERGE"
    flipped = [dict(r, hams="0") if r["harf"] == "ت" else r for r in rows]
    assert "NUTQ_FASL" in check(flipped, HAND_GROUPS), "MUTANT_CSV_HAMS_FLIP"


if __name__ == "__main__":
    test_fasl_table()
    test_theorems_named_and_audited()
    test_mutants_rejected()
    print("3/3")
