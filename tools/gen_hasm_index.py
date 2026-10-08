"""فهرسُ الحسم (HASM_INDEX.md) وجدولُ تكرار الجذور: (١) من `corpus-certificates.json.gz` يُولَّد
`src/slge/hasm_table.py` و`formal/Slge/HasmTable.lean` — لكلّ جذرٍ كم صورةً **وحيدةَ القسمة** في
المصحف تُقرأ عليه (شهادةٌ من غير المتعدّد، فلا دورَ في الحسم)؛ (٢) على `masaq-shibh.json.gz` (مرجعٌ
محجوب): كم كلمةً قسمتُها واحدةٌ بلا قرينة، وكم تُحسم بالقرائن صوابًا وخطأً، وكم تتعادل باسمها.
`--check` يقارن الثلاثة بما يولَّد الآن.
"""

from __future__ import annotations

import gzip
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from slge.adawat import of_cells
from slge.jidh import Reading, jidh
from slge.maqayis import _code, roots_of

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "HASM_INDEX.md"
LEAN = ROOT / "formal" / "Slge" / "HasmTable.lean"
PY = ROOT / "src" / "slge" / "hasm_table.py"
DATA = ROOT / "tests" / "data"
Word = tuple[tuple[str, str], ...]
PRE_IN_STEM = ("IMPERF_PREF", "CV_PREF", "IV1S", "IV1P", "IV2MP", "IV3MS", "IV3MP", "IV3FS")


def corpus_forms() -> list[Word]:
    with gzip.open(DATA / "corpus-certificates.json.gz", "rt", encoding="utf-8") as f:
        d: dict[str, Any] = json.load(f)
    return [tuple((a, b) for a, b in x["cells"]) for x in d["forms"]]


def masaq_rows() -> list[dict[str, Any]]:
    with gzip.open(DATA / "masaq-shibh.json.gz", "rt", encoding="utf-8") as f:
        rows: list[dict[str, Any]] = json.load(f)["rows"]
    return rows


def whole(r: dict[str, Any]) -> Word:
    return (*((a, b) for _, cs in r["pre"] for a, b in cs), *((a, b) for a, b in r["stem"]),
            *((a, b) for _, cs in r["suf"] for a, b in cs))


def _seg(rd: Reading) -> tuple[Any, ...]:
    return (rd.pre, rd.al, rd.stem, rd.suf)


def root_freq(forms: list[Word]) -> tuple[dict[int, int], int]:
    """تكرارُ كلّ جذرٍ في الصور وحيدةِ القسمة، وعددُ تلك الصور."""

    freq: Counter[int] = Counter()
    unique = 0
    for w in forms:
        rs = jidh(w)
        if rs and len({_seg(rd) for rd in rs}) == 1:
            unique += 1
            for r in {x for rd in rs for x in roots_of(rd)}:
                a, b, d = _code(r)
                freq[a * 900 + b * 30 + d] += 1
    return dict(sorted(freq.items())), unique


def render_tables(freq: dict[int, int], unique: int, forms: int) -> tuple[str, str]:
    bound = max(freq.values()) + 1
    pairs = list(freq.items())
    chunks = [pairs[i:i + 400] for i in range(0, len(pairs), 400)]
    parts: list[str] = []
    for i, ch in enumerate(chunks):
        rows = [", ".join(f"({k}, {v})" for k, v in ch[j:j + 8]) for j in range(0, len(ch), 8)]
        parts += [f"def t{i} : List (Nat × Nat) := [", ",\n".join("  " + r for r in rows), "]", ""]
    lean = "\n".join([
        "import Slge.Categories", "",
        "/-! تكرارُ الجذور في مودَع المصحف: لكلّ جذرٍ (رمزُه a·900+b·30+d) كم صورةً وحيدةَ القسمة تُقرأ",
        f"عليه ({unique} صورةً من {forms}) — مولَّدٌ بـ`tools/gen_hasm_index.py` من",
        "`corpus-certificates.json.gz`؛ لا يُحرَّر باليد. القطعُ أجزاءً لحدّ التعمّق في المحرّر. -/", "",
        "namespace Slge.HasmTable", "",
        *parts,
        "/-- (رمزُ الجذر، تكرارُه) مرتَّبًا بالرمز. -/",
        "def table : List (Nat × Nat) := " + " ++ ".join(f"t{i}" for i in range(len(chunks))), "",
        "/-- حدٌّ فوق كلّ تكرار؛ الدرجةُ المعجميّةُ تُبنى عليه. -/",
        f"def bound : Nat := {bound}", "",
        f"theorem table_length : table.length = {len(freq)} := by decide +kernel", "",
        "theorem freq_lt_bound : table.all (fun p => p.2 < bound) = true := by decide +kernel", "",
        "theorem freq_pos : table.all (fun p => 0 < p.2) = true := by decide +kernel", "",
        "end Slge.HasmTable", "",
    ])
    py = "\n".join([
        '"""تكرارُ الجذور في مودَع المصحف (الصورُ وحيدةُ القسمة) — مولَّدٌ بـ`tools/gen_hasm_index.py`؛',
        'لا يُحرَّر باليد."""', "",
        "from __future__ import annotations", "", "from typing import Final", "",
        f"UNIQUE_FORMS: Final[int] = {unique}",
        f"BOUND: Final[int] = {bound}",
        "ROOT_FREQ: Final[dict[int, int]] = {",
        *(f"    {k}: {v}," for k, v in freq.items()),
        "}", "",
    ])
    return lean, py


def measure_masaq() -> dict[str, Any]:
    from slge.hasm import hasm, seg_of

    rows = masaq_rows()
    idx = {(r["ref"], r["pos"]): r for r in rows}
    out: Counter[str] = Counter()
    cache: dict[Word, tuple[Reading, ...]] = {}
    for r in rows:
        w = whole(r)
        if w not in cache:
            cache[w] = jidh(w)
        rs = cache[w]
        prev = idx.get((r["ref"], r["pos"] - 1))
        a = of_cells(whole(prev)) if prev else None
        h = hasm(a, rs)
        pre = tuple((x, y) for t, cs in r["pre"] for x, y in cs
                    if t not in PRE_IN_STEM and t != "DET")
        det = any(t == "DET" for t, _ in r["pre"])
        suf = tuple((x, y) for _, cs in r["suf"] for x, y in cs)
        gold = next((seg_of(rd) for rd in rs if tuple(c for p in rd.pre for c in p) == pre
                     and (rd.al != 0) == det and rd.suf == suf), None)
        if h.name in ("NO_READING", "TIE"):
            out[h.name + ("_GOLD_IN" if gold is not None and h.name == "TIE" else "")] += 1
        else:
            out[h.name + ("_GOLD" if h.seg == gold else "_WRONG")] += 1
    return {"masaq": len(rows), **dict(out)}


def measure() -> dict[str, Any]:
    forms = corpus_forms()
    freq, unique = root_freq(forms)
    m = measure_masaq()
    return {"forms": len(forms), "unique_forms": unique, "roots": len(freq),
            "bound": max(freq.values()) + 1, "masaq": m}


def render(m: dict[str, Any]) -> str:
    q = m["masaq"]
    n = q["masaq"]
    one = q.get("UNIQUE_GOLD", 0) + q.get("DECIDED_GOLD", 0)
    dec = q.get("DECIDED_GOLD", 0) + q.get("DECIDED_WRONG", 0)

    def pct(k: int, d: int = n) -> str:
        return f"{100 * k / d:.1f}%" if d else "—"

    return "\n".join([
        "# فهرسُ الحسم — قسمةٌ واحدة بقرينتين",
        "",
        "مولَّدٌ بـ`python tools/gen_hasm_index.py` من `src/slge/hasm.py`؛ لا يُحرَّر باليد. البرهانُ "
        "`formal/Slge/Hasm.lean`، وجدولُ التكرار `formal/Slge/HasmTable.lean` مولَّدٌ من مودَع المصحف.",
        "",
        "## ما يُحسم", "",
        "ما يسأله المرجعُ عن الكلمة قسمتُها (سوابق، أل، جذع، لواحق) لا قالبُها؛ فالقراءاتُ المتّفقةُ "
        "قسمةً المختلفةُ قالبًا قسمةٌ واحدة. وإن تعدّدت القسماتُ حُسم بينها بالدرجة: الجوارُ (الأداةُ قبلها "
        "توافق القراءة) ثمّ المعجمُ (الجذرُ في المقاييس) ثمّ تكرارُ الجذر في المودَع — والحسمُ الأعلى "
        "الوحيد؛ التعادلُ باسمه (`TIE`) ولا قراءةَ تُحذف (`hasm_mem`، `best_strict`).",
        "",
        "## جدولُ التكرار", "",
        f"{m['roots']:,} جذرًا من {m['unique_forms']:,} صورةً وحيدةَ القسمة (من {m['forms']:,}): "
        "الشهادةُ من غير المتعدّد فلا دورَ في الحسم؛ الحدُّ فوق كلّ تكرار "
        f"{m['bound']:,} (`freq_lt_bound`).",
        "",
        "## على MASAQ (مرجعٌ محجوب)", "",
        f"{n:,} كلمةً بشهادات البوّابة:", "",
        "| الحال | العدد | % |", "|---|---|---|",
        f"| قسمةٌ واحدة بلا قرينة، وهي الذهبيّة | {q.get('UNIQUE_GOLD', 0):,} | "
        f"{pct(q.get('UNIQUE_GOLD', 0))} |",
        f"| قسمةٌ واحدة بلا قرينة، وليست الذهبيّة | {q.get('UNIQUE_WRONG', 0):,} | "
        f"{pct(q.get('UNIQUE_WRONG', 0))} |",
        f"| حُسمت بالقرائن صوابًا | {q.get('DECIDED_GOLD', 0):,} | {pct(q.get('DECIDED_GOLD', 0))} |",
        f"| حُسمت بالقرائن خطأً | {q.get('DECIDED_WRONG', 0):,} | {pct(q.get('DECIDED_WRONG', 0))} |",
        f"| تعادلٌ والذهبيّةُ بين القسمات | {q.get('TIE_GOLD_IN', 0):,} | "
        f"{pct(q.get('TIE_GOLD_IN', 0))} |",
        f"| تعادلٌ ولا ذهبيّة | {q.get('TIE', 0):,} | {pct(q.get('TIE', 0))} |",
        f"| لا قراءة | {q.get('NO_READING', 0):,} | {pct(q.get('NO_READING', 0))} |",
        "",
        f"**قسمةٌ واحدة صحيحة: {one:,} ({pct(one)})** — كانت 15,583 (38.3%) حين عُدّ القالبُ قسمة. "
        f"دقّةُ الحسم بالقرائن: {q.get('DECIDED_GOLD', 0):,} من {dec:,} "
        f"({pct(q.get('DECIDED_GOLD', 0), dec)}).",
        "",
        "## ما يقوله الرقم — باسمه", "",
        "- أكثرُ الرفع من تعريف السؤال لا من القرينة: القالبُ ليس قسمة.",
        "- الحسمُ بالقرائن يخطئ في نحو أربعة من عشرة؛ تكرارُ الجذر أقوى القرائن عددًا وأضعفُها دقّةً.",
        "- التعادلُ الباقي يحتاج قرينةً جديدة (الجوارُ بعد الكلمة، أو التركيب) لا قراءةً جديدة.",
        "",
    ])


def main() -> int:
    forms = corpus_forms()
    freq, unique = root_freq(forms)
    lean, py = render_tables(freq, unique, len(forms))
    if "--check" in sys.argv:
        if LEAN.read_text(encoding="utf-8") != lean or PY.read_text(encoding="utf-8") != py:
            sys.stdout.write("جدولُ التكرار غيرُ مطابق؛ شغّل tools/gen_hasm_index.py\n")
            return 1
    else:
        LEAN.write_text(lean, encoding="utf-8")
        PY.write_text(py, encoding="utf-8")
    m = {"forms": len(forms), "unique_forms": unique, "roots": len(freq),
         "bound": max(freq.values()) + 1, "masaq": measure_masaq()}
    text = render(m)
    if "--check" in sys.argv:
        if TARGET.read_text(encoding="utf-8") != text:
            sys.stdout.write("HASM_INDEX.md غيرُ مطابق؛ شغّل tools/gen_hasm_index.py\n")
            return 1
        sys.stdout.write("HASM_INDEX.md مطابق\n")
        return 0
    TARGET.write_text(text, encoding="utf-8")
    sys.stdout.write(f"كُتب HASM_INDEX.md: {m['masaq']}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
