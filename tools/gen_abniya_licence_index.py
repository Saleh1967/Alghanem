"""فهرسُ أبنية سيبويه على الترخيص الثلاثيّ (ABNIYA_LICENCE_INDEX.md؛ ADR ٣٦).

لكلّ هيكلٍ من الـ158 (`abniya_table.SKELETONS`): عددُ تشكيلاته (الألفُ ساكنةٌ أبدًا؛ والألفُ الأولى
همزةُ وصل بقاعدتها)، والمرخَّصُ منها وصلًا ووقفًا، والمرخَّصُ نفسُه بلا قاعدة الوصل — فالهياكلُ
التي لا يرخّصها شيءٌ إلّا بالقاعدة مسمّاةٌ بأعدادها. ويكتب `formal/Slge/AbniyaLicenceTable.lean`
و`src/slge/abniya_licence_table.py`: لكلّ هيكلٍ **شاهدٌ** — أوّلُ تشكيلٍ مرخَّصٍ وصلًا ووقفًا
بترتيب الحالات — يبرهن Lean ترخيصَه ومطابقتَه هيكلَه (`Slge.AbniyaLicence`). لا نصَّ هنا: حواملُ
وحالات.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from slge.abniya_licence import counts, is_wasl, vocalizations
from slge.abniya_table import SKELETONS
from slge.cells import ALPHABET, STATES
from slge.madd import continue_licensed, pause_licensed

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "ABNIYA_LICENCE_INDEX.md"
LEAN = ROOT / "formal" / "Slge" / "AbniyaLicenceTable.lean"
PY = ROOT / "src" / "slge" / "abniya_licence_table.py"
MARKS = {"فتح": "َ", "كسر": "ِ", "ضم": "ُ", "سكون": "ْ"}


def _name(sk: tuple[int, ...]) -> str:
    return "".join(ALPHABET[i] for i in sk)


def _witness(sk: tuple[int, ...]) -> tuple[tuple[str, str], ...] | None:
    for w in vocalizations(sk):
        if continue_licensed(w) and pause_licensed(w):
            return w
    return None


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
    }


def _vowelled(w: tuple[tuple[str, str], ...]) -> str:
    return "".join(k + MARKS[s] for k, s in w)


def render_tables() -> tuple[str, str]:
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
        "end Slge.AbniyaLicenceTable", "",
    ])
    py = "\n".join([
        '"""شواهدُ أبنية سيبويه على الترخيص الثلاثيّ — مولَّدٌ بـ`tools/gen_abniya_licence_index.py`؛',
        'لا يُحرَّر باليد. الخانةُ (فهرسُ الحامل، فهرسُ الحالة)."""', "",
        "from __future__ import annotations", "", "from typing import Final", "",
        "WITNESSES: Final[tuple[tuple[tuple[int, ...], tuple[tuple[int, int], ...]], ...]] = (",
        *(f"    ({sk!r},\n     {tuple((ALPHABET.index(k), STATES.index(s)) for k, s in w)!r}),"
          for sk, w in ws), ")", "",
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
        "الحالات، لا تشكيلُ سيبويه.",
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
    m = measure()
    lean, py = render_tables()
    text = render(m)
    if "--check" in argv:
        ok = (TARGET.read_text(encoding="utf-8") == text
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
