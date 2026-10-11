"""فهرسُ أبنية سيبويه على الترخيص الثلاثيّ (ABNIYA_LICENCE_INDEX.md؛ ADR ٣٦).

لكلّ هيكلٍ من الـ158 (`abniya_table.SKELETONS`): عددُ تشكيلاته (الألفُ ساكنةٌ أبدًا؛ والألفُ الأولى
همزةُ وصل بقاعدتها)، والمرخَّصُ منها وصلًا ووقفًا، والمرخَّصُ نفسُه بلا قاعدة الوصل — فالهياكلُ
التي لا يرخّصها شيءٌ إلّا بالقاعدة مسمّاةٌ بأعدادها. ويكتب `formal/Slge/AbniyaLicenceTable.lean`
و`src/slge/abniya_licence_table.py`: لكلّ هيكلٍ **شاهدٌ** — أوّلُ تشكيلٍ مرخَّصٍ وصلًا ووقفًا
بترتيب الحالات `STATES` (اختيارٌ مسمًّى لا تشكيلُ سيبويه) — يبرهن Lean ترخيصَه ومطابقتَه هيكلَه
(`Slge.AbniyaLicence`). لا نصَّ هنا: حواملُ وحالات.

و**المرجعُ المحجوب** (ADR ٣٧): الكتابُ المختوم بلا حركات، فتشكيلُ سيبويه ليس في مودَع. فالأداةُ تكتب
(إن غاب) إطارًا `tests/data/abniya-reference.tsv` — صفٌّ لكلّ هيكل: ثابتُه من المودَع (الهيكل، حروفه،
أسطرُه في الكتاب، رسمُه كما ورد) وأعمدةٌ فارغة يملؤها المالكُ بيده: `states` حالاتُ الحروف بالترتيب
(فتح/كسر/ضم/سكون، والألفُ الأولى همزةُ الوصل بحركتها)، و`source` الطبعةُ المشكولة وموضعُها، و`note`.
حالاتٌ لا نصّ: لا يدخل الشجرةَ لفظٌ مشكول. `--check` يطابق الثابتَ ولا يمسّ المملوء، ويرفض صفًّا مملوءًا
مخالفًا لشكله باسم `REFERENCE_ROW_MALFORMED`؛ ولا رقمَ في الفهرس قبل الملء.
"""

from __future__ import annotations

import csv
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

from slge.abniya_licence import HAMZA, counts, is_wasl, vocalizations
from slge.abniya_table import SKELETONS
from slge.cells import ALPHABET, STATES
from slge.madd import continue_licensed, pause_licensed

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "ABNIYA_LICENCE_INDEX.md"
LEAN = ROOT / "formal" / "Slge" / "AbniyaLicenceTable.lean"
PY = ROOT / "src" / "slge" / "abniya_licence_table.py"
SOURCE = ROOT / "tests" / "data" / "sibawayh-abniya.tsv"
REFERENCE = ROOT / "tests" / "data" / "abniya-reference.tsv"
INTIQA = ROOT / "tests" / "data" / "abniya-intiqa.json"
"""انتقاءُ الأبنية الموقَّع (الغانم ADR ١٣؛ هنا ADR ٣٨): مودَعٌ تطبعه أداةُ الغانم `gen_abniya_intiqa.py`
على `GATE_REV` — لكلّ صفٍّ مملوءٍ شهادةُ البوّابة وحالاتُ حروف الهيكل أو رفضُها المسمّى، والتوقيع."""
FIXED = ("id", "skeleton", "letters", "kitab_lines", "as_written")
OWNER = ("states", "source", "note")
MARKS = {"فتح": "َ", "كسر": "ِ", "ضم": "ُ", "سكون": "ْ"}


def _name(sk: tuple[int, ...]) -> str:
    return "".join(ALPHABET[i] for i in sk)


def _witness(sk: tuple[int, ...]) -> tuple[tuple[str, str], ...] | None:
    for w in vocalizations(sk):
        if continue_licensed(w) and pause_licensed(w):
            return w
    return None


def reference_fresh() -> list[dict[str, str]]:
    """الإطار: لكلّ هيكلٍ أسطرُه في الكتاب ورسمُه كما ورد من المودَع المختوم، والأعمدةُ للمالك فارغة."""

    lines: dict[str, set[int]] = defaultdict(set)
    written: dict[str, set[str]] = defaultdict(set)
    with SOURCE.open(encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            lines[r["skeleton"]].add(int(r["line"]))
            written[r["skeleton"]].add(r["token"])
    out = []
    for i, sk in enumerate(SKELETONS, 1):
        name = _name(sk)
        key = name
        out.append({"id": f"A{i:03d}", "skeleton": name, "letters": " ".join(name),
                    "kitab_lines": " ".join(str(n) for n in sorted(lines[key])),
                    "as_written": " ".join(sorted(written[key])),
                    **dict.fromkeys(OWNER, "")})
    return out


def reference_rows() -> list[dict[str, str]]:
    with REFERENCE.open(encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def _write_reference(rows: list[dict[str, str]]) -> None:
    with REFERENCE.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=(*FIXED, *OWNER), delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def owner_cells(row: dict[str, str]) -> tuple[tuple[str, str], ...] | None:
    """خاناتُ الصفّ المملوء: حواملُ الهيكل (والألفُ الأولى همزةُ الوصل) وحالاتُ المالك؛ أو لا شيء."""

    sk = next(s for s in SKELETONS if _name(s) == row["skeleton"])
    states = row["states"].split()
    if len(states) != len(sk) or any(x not in STATES for x in states):
        return None
    return tuple((HAMZA if i == 0 and is_wasl(sk) else ALPHABET[k], st)
                 for i, (k, st) in enumerate(zip(sk, states, strict=True)))


def check_reference() -> list[str]:
    """أسماءُ المخالفات: ثابتٌ تغيّر، أو صفٌّ مملوءٌ مخالفٌ لشكله."""

    rows, fresh = reference_rows(), reference_fresh()
    bad = []
    if [{k: r[k] for k in FIXED} for r in rows] != [{k: r[k] for k in FIXED} for r in fresh]:
        bad.append("REFERENCE_FIXED_COLUMNS_DRIFTED")
    bad += [f"REFERENCE_ROW_MALFORMED {r['id']}" for r in rows
            if r["states"].strip() and owner_cells(r) is None]
    return bad


def intiqa() -> dict[str, Any]:
    with INTIQA.open(encoding="utf-8") as f:
        d: dict[str, Any] = json.load(f)
    return d


def signed_rows() -> list[tuple[tuple[int, ...], tuple[tuple[str, str], ...]]]:
    """الصفوفُ الموقَّعة التي شهدت لها البوّابة: (الهيكل، خاناتُه بحالات الطبعة)؛ ولا شيء قبل التوقيع."""

    d = intiqa()
    if not d["signed"]:
        return []
    by_name = {_name(sk): sk for sk in SKELETONS}
    out = []
    for r in d["rows"]:
        if r["status"] == "CERTIFICATE" and r["states"]:
            sk = by_name[r["skeleton"]]
            out.append((sk, tuple((HAMZA if i == 0 and is_wasl(sk) else ALPHABET[k], st)
                                  for i, (k, st) in enumerate(zip(sk, r["states"], strict=True)))))
    return out


def intiqa_measure() -> dict[str, Any]:
    d = intiqa()
    rows = d["rows"]
    signed = signed_rows()
    ws = {sk: _witness(sk) for sk, _ in signed}
    return {
        "size": len(d["frame"]), "filled": len(rows), "signed": bool(d["signed"]),
        "refused": sum(r["status"] != "CERTIFICATE" for r in rows),
        "certified": len(signed),
        "continue": sum(continue_licensed(c) for _, c in signed),
        "pause": sum(pause_licensed(c) for _, c in signed),
        "licensed": sum(continue_licensed(c) and pause_licensed(c) for _, c in signed),
        "witness_equal": sum(ws[sk] == c for sk, c in signed),
    }


def reference_measure() -> dict[str, Any]:
    rows = [r for r in reference_rows() if r["states"].strip()]
    cells = [c for c in (owner_cells(r) for r in rows) if c is not None]
    ws = {_name(sk): w for sk, w in ((sk, _witness(sk)) for sk in SKELETONS)}
    by_name = {r["skeleton"]: owner_cells(r) for r in rows}
    return {
        "size": len(SKELETONS), "filled": len(rows),
        "continue": sum(continue_licensed(c) for c in cells),
        "pause": sum(pause_licensed(c) for c in cells),
        "witness_equal": sum(by_name[n] == ws[n] for n in by_name),
    }


def measure() -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for sk in SKELETONS:
        tot, cont, pause = counts(sk)
        _, cont0, pause0 = counts(sk, wasl_rule=False)
        rows.append({"skeleton": _name(sk), "letters": len(sk), "wasl": is_wasl(sk),
                     "vocalizations": tot, "continue": cont, "pause": pause,
                     "continue_without_wasl_rule": cont0, "pause_without_wasl_rule": pause0})
    tot = sum(r["vocalizations"] for r in rows)
    return {
        "skeletons": len(rows), "wasl_skeletons": sum(r["wasl"] for r in rows),
        "vocalizations": tot, "continue": sum(r["continue"] for r in rows),
        "pause": sum(r["pause"] for r in rows),
        "skeletons_with_continue": sum(r["continue"] > 0 for r in rows),
        "skeletons_with_pause": sum(r["pause"] > 0 for r in rows),
        "skeletons_without_rule_unlicensed": sum(r["continue_without_wasl_rule"] == 0
                                                 for r in rows),
        "rows": rows,
        "reference": reference_measure(),
        "intiqa": intiqa_measure(),
    }


def _vowelled(w: tuple[tuple[str, str], ...]) -> str:
    return "".join(k + MARKS[s] for k, s in w)


def render_tables() -> tuple[str, str]:
    signed = signed_rows()
    ws = []
    for sk in SKELETONS:
        w = _witness(sk)
        assert w is not None, _name(sk)
        ws.append((sk, w))
    lean_rows = []
    for sk, w in ws:
        cells = ", ".join(f"c {ALPHABET.index(k)} {STATES.index(s)}" for k, s in w)
        lean_rows.append(f"  ([{', '.join(str(i) for i in sk)}], [{cells}])")
    lean = "\n".join([
        "import Slge.Categories", "",
        "/-! شواهدُ أبنية سيبويه على الترخيص الثلاثيّ — مولَّدٌ بـ`tools/gen_abniya_licence_index.py`؛",
        "لا يُحرَّر باليد. لكلّ هيكلٍ (حواملُ بلا حركات، بترتيب `AbniyaTable.abniya`) أوّلُ تشكيلٍ",
        "مرخَّصٍ وصلًا ووقفًا؛",
        "والألفُ الأولى همزةُ وصلٍ ابتداءً (‎c 0 _‎). -/", "",
        "namespace Slge.AbniyaLicenceTable", "",
        "open Slge.Categories (c)", "",
        "set_option maxRecDepth 100000 in",
        "def witnesses : List (List Nat × List SCell) := [",
        ",\n".join(lean_rows), "]", "",
        f"theorem witnesses_length : witnesses.length = {len(ws)} := by rfl", "",
        "set_option maxRecDepth 100000 in",
        "/-- انتقاءُ الأبنية الموقَّع (ADR ٣٨): ما شهدت له البوّابةُ من صفوفه — الهيكلُ وخاناتُه بحالات "
        "الطبعة؛ فارغٌ قبل التوقيع. -/",
        "def signed : List (List Nat × List SCell) := [" + "".join(
            f"\n  ([{', '.join(str(i) for i in sk)}], "
            f"[{', '.join(f'c {ALPHABET.index(k)} {STATES.index(x)}' for k, x in c)}])"
            + ("," if j < len(signed) - 1 else "") for j, (sk, c) in enumerate(signed)) + "]", "",
        "/-- عددُ الموقَّع المرخَّص وصلًا ووقفًا، محسوبًا عند التوليد ومبرهنًا في `AbniyaLicence`. -/",
        "def signedLicensed : Nat := "
        f"{sum(continue_licensed(c) and pause_licensed(c) for _, c in signed)}",
        "",
        "end Slge.AbniyaLicenceTable", "",
    ])
    py = "\n".join([
        '"""شواهدُ أبنية سيبويه على الترخيص الثلاثيّ — مولَّدٌ بـ`tools/gen_abniya_licence_index.py`؛',
        'لا يُحرَّر باليد. الخانةُ (فهرسُ الحامل، فهرسُ الحالة)."""', "",
        "from __future__ import annotations", "", "from typing import Final", "",
        "WITNESSES: Final[tuple[tuple[tuple[int, ...], tuple[tuple[int, int], ...]], ...]] = (",
        *(f"    ({sk!r},\n     {tuple((ALPHABET.index(k), STATES.index(s)) for k, s in w)!r}),"
          for sk, w in ws), ")", "",
        "SIGNED: Final[tuple[tuple[tuple[int, ...], tuple[tuple[int, int], ...]], ...]] = (",
        *(f"    ({sk!r},\n     {tuple((ALPHABET.index(k), STATES.index(x)) for k, x in c)!r}),"
          for sk, c in signed), ")",
        '"""انتقاءُ الأبنية الموقَّع: ما شهدت له البوّابةُ من صفوفه (ADR ٣٨)؛ فارغٌ قبل التوقيع."""', "",
    ])
    return lean, py


def _pct(a: int, b: int) -> str:
    return f"{a:,} من {b:,} ({100 * a / b:.1f}%)" if b else "—"


def render(m: dict[str, Any]) -> str:
    rows = m["rows"]
    voc = m["vocalizations"]
    lines = [
        "# أبنيةُ سيبويه على الترخيص الثلاثيّ",
        "",
        "مولَّدٌ بـ`python tools/gen_abniya_licence_index.py` من هياكل أبنية سيبويه المودَعة "
        "(`sibawayh-abniya.tsv` ← `abniya_table`)؛ لا يُحرَّر باليد. الهيكلُ حروفٌ بلا حركات، "
        "فيُقاس بتشكيلاته: لكلّ حاملٍ حالةٌ من الأربع، والألفُ ساكنةٌ أبدًا (الكتاب س18101)، "
        "والألفُ الأولى همزةُ وصلٍ مكسورةٌ ابتداءً إلّا أن يُضمّ الثالث (`wasl_state_damm_iff`). "
        "الترخيصُ `Madd.continueLicensed`/`pauseLicensed` = `A116.Ternary.continueB`/`pauseB` "
        "على أصناف الخانات.",
        "",
        "## الحصيلة (محسوبةٌ على المودَع كلِّه)",
        "",
        f"- الهياكل: {m['skeletons']}، منها {m['wasl_skeletons']} أوّلُها همزةُ وصل.",
        f"- التشكيلات: {voc:,}؛ المرخَّصُ وصلًا {_pct(m['continue'], voc)}، "
        f"ووقفًا {_pct(m['pause'], voc)}.",
        f"- هياكلُ لها تشكيلٌ مرخَّصٌ وصلًا: {m['skeletons_with_continue']} من {m['skeletons']}؛ "
        f"ووقفًا: {m['skeletons_with_pause']} من {m['skeletons']}.",
        f"- **بلا قاعدة الوصل** (الألفُ الأولى ساكنةٌ كما رُسمت): "
        f"{m['skeletons_without_rule_unlicensed']} هيكلًا لا يُرخَّص له تشكيلٌ أصلًا — وهي هياكلُ همزة "
        "الوصل بعينها؛ فالقاعدةُ المبرهنة (لا ابتداءَ بساكن، والهمزةُ تُجتلب) هي الفارق، لا الهيكل.",
        "",
        "**ما لا يقيسه هذا الفهرس:** الهيكلُ بلا حركاتٍ لا يقول أيَّ تشكيلٍ أراد سيبويه؛ فالمرخَّصُ هنا "
        "**سقفٌ** لكلّ هيكل لا شهادةٌ بالبناء المشكول. والشاهدُ في Lean أوّلُ تشكيلٍ مرخَّصٍ بترتيب "
        "الحالات `STATES`، لا تشكيلُ سيبويه.",
        "",
        "## المرجعُ: انتقاءُ الأبنية الموقَّع (ADR ٣٨؛ الغانم ADR ١٣)",
        "",
        "الكتابُ المختوم بلا حركات، والمطابقةُ بالحروف على المصحف تُلبس («كانوا» على فاعل، «إنّهم» على "
        "انفعل)؛ فتشكيلُ البناء سماعٌ ينقله المالكُ من طبعةٍ مشكولةٍ بموضعها إلى إطار الغانم "
        "(`corpora/abniya-intiqa.tsv`)، ويمرّ على البوّابة **مجالًا مختومًا ثالثًا**، ويصل هنا مودَعًا "
        "(`abniya-intiqa.json`) خاناتٍ لا نصًّا. ولا يُعدّ صفٌّ قبل التوقيع؛ ورفضُ البوّابة لصفٍّ موقَّعٍ "
        "نقضٌ مسمًّى للترخيص لا يُخفى. (إطارُ الحالات السابق `abniya-reference.tsv`، ADR ٣٧، "
        "مستبدَلٌ بهذا ولا يُملأ.)",
        "",
        *([f"- **لا رقم**: المملوءُ {m['intiqa']['filled']} من {m['intiqa']['size']}، موقَّع: "
           f"{'نعم' if m['intiqa']['signed'] else 'لا'}."]
          if not (m["intiqa"]["signed"] and m["intiqa"]["filled"]) else [
            f"- موقَّع: {m['intiqa']['filled']} صفًّا من {m['intiqa']['size']}؛ شهدت البوّابةُ لـ"
            f"{m['intiqa']['certified']} ورفضت {m['intiqa']['refused']} بأسمائها في المودَع.",
            f"- من المشهود: المرخَّصُ وصلًا {m['intiqa']['continue']} ووقفًا {m['intiqa']['pause']}، "
            f"ومعًا {m['intiqa']['licensed']} (`signed_licensed_count`)؛ ويساوي شاهدَ Lean "
            f"{m['intiqa']['witness_equal']}."]),
        "",
        "## الهياكل",
        "",
        "| الهيكل | حروف | وصل؟ | تشكيلات | مرخَّصٌ وصلًا | مرخَّصٌ وقفًا | "
        "وصلًا بلا قاعدة الوصل |",
        "|---|---|---|---|---|---|---|",
        *(f"| {r['skeleton']} | {r['letters']} | {'نعم' if r['wasl'] else '—'} | "
          f"{r['vocalizations']:,} | {r['continue']:,} | {r['pause']:,} | "
          f"{r['continue_without_wasl_rule']:,} |" for r in rows),
        "",
    ]
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    if not REFERENCE.exists():
        _write_reference(reference_fresh())
    m = measure()
    lean, py = render_tables()
    text = render(m)
    if "--check" in argv:
        bad = check_reference()
        for b in bad:
            sys.stdout.write(b + "\n")
        ok = (not bad and TARGET.read_text(encoding="utf-8") == text
              and LEAN.read_text(encoding="utf-8") == lean
              and PY.read_text(encoding="utf-8") == py)
        sys.stdout.write("ABNIYA_LICENCE_INDEX.md مطابق\n" if ok
                         else "ABNIYA_LICENCE_INDEX.md غيرُ مطابق\n")
        return 0 if ok else 1
    LEAN.write_text(lean, encoding="utf-8")
    PY.write_text(py, encoding="utf-8")
    TARGET.write_text(text, encoding="utf-8")
    sys.stdout.write("كُتب ABNIYA_LICENCE_INDEX.md وجدولا الشواهد\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
