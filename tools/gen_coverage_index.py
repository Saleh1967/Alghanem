"""فهرسُ التغطية (COVERAGE_INDEX.md): ما يشهد عليه مودَعا شهادات المصحف من الشبكة والقرّاء والجداول
والمقاييس والمخصّص — كلُّ مدخلٍ بشاهدٍ مسمًّى أو «معلومة» (ADR ٢٩). يقرأ
`corpus-certificates.json.gz` و`context-certificates.json.gz` ويقيس: (١) **الشبكة**: أيُّ خاناتٍ
من الـ116 تحملها صورةٌ من المودَعين — التوقّعُ 113 (المرخَّصُ بلا ألفٍ متحرّكة:
`Coverage.licensable`) ويودع المشهودَ في `CoverageTable.lean` فيبرهن Lean أنّه المرخَّصُ بعينه
(`attested_eq_licensable`)؛ (٢) **القرّاء**: كم صورةً وكم موقعًا يقرأ كلُّ بوّابةٍ قارئةٍ في
السُّلَّم؛ (٣) **صفوفُ الجداول** (الموزِّع، الأعلام، السوابق): لكلّ صفٍّ كم صورةً يقرؤها قارئُه
عليه — مفهومٌ بشاهد أو معلومةٌ بلا شاهد تبقى في جدولها؛ (٤) **المقاييس والمخصّص**: لكلّ جذرٍ
شواهدُه القاطعة والمحتملة من قراءات الجذع، ولكلّ عقدةٍ درجتُها بجذور عنوانها. يكتب أيضًا
`formal/Slge/CoverageTable.lean` و`src/slge/coverage_table.py`. لا نصَّ هنا: خاناتٌ وأعداد،
والصورُ تُطبع من خاناتها للعرض.
"""

from __future__ import annotations

import gzip
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from slge.alam import ilm
from slge.alam_table import ALAM
from slge.cells import ALPHABET, STATES, Cell
from slge.coverage import (
    ALIF_VOWELLED,
    MAFHUM,
    cell_witnesses,
    licensable_cells,
    node_grade,
    root_witnesses,
    row_grade,
)
from slge.entry import to_atoms
from slge.gates import LADDER, Pass, climb
from slge.jidh import jidh
from slge.maqayis import decode, roots_of
from slge.maqayis_table import ROOTS
from slge.mukhassas import NODES, code_of_root, title_of
from slge.sawabiq import sawabiq
from slge.sawabiq_table import TABLE as SAWABIQ_TABLE
from slge.tawzi import TABLE as TAWZI_TABLE
from slge.tawzi import tawzi

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "COVERAGE_INDEX.md"
LEAN = ROOT / "formal" / "Slge" / "CoverageTable.lean"
PY = ROOT / "src" / "slge" / "coverage_table.py"
DATA = ROOT / "tests" / "data"
Word = tuple[Cell, ...]
MARKS = {"فتح": "َ", "كسر": "ِ", "ضم": "ُ", "سكون": "ْ"}
GUARDS = ("الخانة", "الترخيص", "العدد")
CONTEXTUAL = ("الأدوات",)
"""بوّاباتٌ تقرأ الجارَ قبل الكلمة لا الكلمةَ المنفردة؛ قياسُها في فهرسها (`ADAWAT_INDEX.md`) لا هنا."""


def _load(name: str) -> dict[str, Any]:
    with gzip.open(DATA / name, "rt", encoding="utf-8") as f:
        d: dict[str, Any] = json.load(f)
    return d


def _forms(d: dict[str, Any]) -> list[Word]:
    return [tuple((a, b) for a, b in x["cells"]) for x in d["forms"]]


def vowelled(w: Word) -> str:
    return "".join(k + MARKS[s] for k, s in w)


def _root_name(code: int) -> str:
    return "".join(ALPHABET[i] if i < 29 else "ـ" for i in decode(code))


def measure() -> dict[str, Any]:
    start, ctx = _load("corpus-certificates.json.gz"), _load("context-certificates.json.gz")
    assert start["corpus_sha256"] == ctx["corpus_sha256"]
    sf, cf = _forms(start), _forms(ctx)
    freq: Counter[int] = Counter(i for i in start["stream"] if i >= 0)
    # (١) الشبكة
    wit = cell_witnesses([*sf, *cf])
    attested = tuple(x for x in licensable_cells() if wit[x])
    unattested = tuple(x for x in licensable_cells() if not wit[x])
    alif_seen = sum(wit[x] for x in ALIF_VOWELLED)
    # (٢) القرّاء و(٣) الجداول — على صور الابتداء بتكرارها مواقعَ
    read_forms: Counter[str] = Counter()
    read_tokens: Counter[str] = Counter()
    tawzi_hits: Counter[tuple[str, str, Word]] = Counter()
    alam_hits: Counter[str] = Counter()
    sawabiq_hits: Counter[tuple[str, Word]] = Counter()
    root_sets: list[frozenset[int]] = []
    for i, w in enumerate(sf):
        for p in climb(to_atoms(w)):
            if isinstance(p, Pass) and p.gate not in GUARDS and p.out:
                read_forms[p.gate] += 1
                read_tokens[p.gate] += freq[i]
        for m in tawzi(w):
            tawzi_hits[(m.kind, m.name, m.core)] += 1
        for a in ilm(w):
            if a.kind != "جلالة":
                alam_hits[a.rasm] += 1
        for s in sawabiq(w):
            sawabiq_hits[(s.kind, w)] += 1
        codes = {c for rd in jidh(w) for r in roots_of(rd) if (c := code_of_root(r)) is not None}
        if codes:
            root_sets.append(frozenset(codes))
    tawzi_rows = [(k, f"{n} {vowelled(c)}", row_grade(tawzi_hits[(k, n, c)]))
                  for k, n, c in TAWZI_TABLE]
    alam_rows = [(r, row_grade(alam_hits[r])) for r, *_ in ALAM]
    sawabiq_rows = [(k, line, sh, row_grade(sawabiq_hits[(k, form)]))
                    for k, _, line, sh, form, *_ in SAWABIQ_TABLE]
    # (٤) المقاييس والمخصّص
    qati, muhtamal = root_witnesses(root_sets)
    roots_qati = sum(1 for r in ROOTS if qati[r])
    roots_muhtamal_only = sum(1 for r in ROOTS if muhtamal[r] and not qati[r])
    nodes = [(n[0], node_grade(n[4], qati), any(muhtamal[r] for r in n[4]), bool(n[4]))
             for n in NODES]
    nodes_qati = sum(1 for _, g, _, _ in nodes if g[0] == MAFHUM)
    nodes_muhtamal_only = sum(1 for _, g, m, _ in nodes if g[0] != MAFHUM and m)
    nodes_no_roots = sum(1 for _, _, _, has in nodes if not has)
    readers = [g.name for g in LADDER if g.name not in GUARDS and g.name not in CONTEXTUAL]
    return {
        "forms": len(sf), "context_forms": len(cf), "tokens": len(start["stream"]),
        "cells": {"licensable": len(licensable_cells()), "attested": len(attested),
                  "unattested": [f"{k}{MARKS[s]}" for k, s in unattested],
                  "vowelled_alif_seen": alif_seen},
        "attested_cells": attested,
        "readers": {g: {"forms": read_forms[g], "tokens": read_tokens[g]} for g in readers},
        "tables": {
            "tawzi": {"rows": len(tawzi_rows),
                      "attested": sum(1 for _, _, g in tawzi_rows if g[0] == MAFHUM),
                      "unattested": [f"{k}:{n}" for k, n, g in tawzi_rows if g[0] != MAFHUM]},
            "alam": {"rows": len(alam_rows),
                     "attested": sum(1 for _, g in alam_rows if g[0] == MAFHUM),
                     "unattested": [r for r, g in alam_rows if g[0] != MAFHUM]},
            "sawabiq": {"rows": len(sawabiq_rows),
                        "attested": sum(1 for *_, g in sawabiq_rows if g[0] == MAFHUM),
                        "unattested": [f"{k}:{line}:{sh}" for k, line, sh, g in sawabiq_rows
                                       if g[0] != MAFHUM]},
        },
        "maqayis": {"roots": len(ROOTS), "forms_with_root": len(root_sets), "qati": roots_qati,
                    "muhtamal_only": roots_muhtamal_only,
                    "none": len(ROOTS) - roots_qati - roots_muhtamal_only,
                    "top_qati": [(_root_name(r), n) for r, n in qati.most_common(10)]},
        "mukhassas": {"nodes": len(NODES), "with_roots": len(NODES) - nodes_no_roots,
                      "qati": nodes_qati, "muhtamal_only": nodes_muhtamal_only,
                      "none": len(NODES) - nodes_no_roots - nodes_qati - nodes_muhtamal_only,
                      "no_roots": nodes_no_roots,
                      "sample_none": [f"{i} {title_of(i)}" for i, g, m, has in nodes
                                      if has and g[0] != MAFHUM and not m][:12]},
    }


def render_tables(m: dict[str, Any]) -> tuple[str, str]:
    cells = m["attested_cells"]
    rows = [", ".join(f"c {ALPHABET.index(k)} {STATES.index(s)}" for k, s in cells[j:j + 6])
            for j in range(0, len(cells), 6)]
    t, q, k = m["tables"], m["maqayis"], m["mukhassas"]
    axes = [(1, m["cells"]["licensable"], m["cells"]["attested"]),
            (2, t["tawzi"]["rows"], t["tawzi"]["attested"]),
            (3, t["alam"]["rows"], t["alam"]["attested"]),
            (4, t["sawabiq"]["rows"], t["sawabiq"]["attested"]),
            (5, q["roots"], q["qati"] + q["muhtamal_only"]),
            (6, k["with_roots"], k["qati"])]
    lean = "\n".join([
        "import Slge.Categories", "",
        "/-! التغطية على مودَعَي المصحف — مولَّدٌ بـ`tools/gen_coverage_index.py`؛ لا يُحرَّر باليد.",
        "`attestedCells` الخاناتُ التي تحملها صورةٌ من المودَعين بترتيب الشبكة؛ `axes` (المحور،",
        "المودَع، المشهود): ١ الشبكة، ٢ الموزِّع، ٣ الأعلام، ٤ السوابق، ٥ جذورُ المقاييس (قاطعًا أو",
        "محتملًا)، ٦ عقدُ المخصّص ذاتُ الجذور (قاطعًا). -/", "",
        "namespace Slge.CoverageTable", "",
        "open Slge.Categories (c)", "",
        "def attestedCells : List SCell := [",
        ",\n".join("  " + r for r in rows), "]", "",
        "def axes : List (Nat × Nat × Nat) := [",
        ",\n".join(f"  ({a}, {b}, {d})" for a, b, d in axes), "]", "",
        f"def rootsTotal : Nat := {q['roots']}",
        f"def rootsQati : Nat := {q['qati']}",
        f"def rootsMuhtamalOnly : Nat := {q['muhtamal_only']}",
        f"def rootsNone : Nat := {q['none']}", "",
        f"def nodesTotal : Nat := {k['nodes']}",
        f"def nodesQati : Nat := {k['qati']}",
        f"def nodesMuhtamalOnly : Nat := {k['muhtamal_only']}",
        f"def nodesNone : Nat := {k['none']}",
        f"def nodesNoRoots : Nat := {k['no_roots']}", "",
        f"theorem attestedCells_length : attestedCells.length = {len(cells)} := by decide", "",
        "end Slge.CoverageTable", "",
    ])
    py = "\n".join([
        '"""التغطية على مودَعَي المصحف — مولَّدٌ بـ`tools/gen_coverage_index.py`؛ لا يُحرَّر باليد."""', "",
        "from __future__ import annotations", "", "from typing import Final", "",
        "ATTESTED_CELLS: Final[tuple[tuple[str, str], ...]] = (",
        *(f"    {x!r}," for x in cells), ")", "",
        "AXES: Final[tuple[tuple[int, int, int], ...]] = (",
        *(f"    {a!r}," for a in axes), ")", "",
        f"ROOTS: Final[tuple[int, int, int, int]] = "
        f"{(q['roots'], q['qati'], q['muhtamal_only'], q['none'])!r}",
        f"NODES: Final[tuple[int, int, int, int, int]] = "
        f"{(k['nodes'], k['qati'], k['muhtamal_only'], k['none'], k['no_roots'])!r}", "",
    ])
    return lean, py


def _pct(a: int, b: int) -> str:
    return f"{a:,} من {b:,} ({100 * a / b:.1f}%)" if b else "—"


def render(m: dict[str, Any]) -> str:
    c, t, q, k = m["cells"], m["tables"], m["maqayis"], m["mukhassas"]
    lines = [
        "# فهرسُ التغطية — ما يشهد عليه المودَعُ، بشاهدٍ مسمًّى أو «معلومة»",
        "",
        "مولَّدٌ بـ`python tools/gen_coverage_index.py` من مودَعَي الغانم "
        "(`corpus-certificates.json.gz`، `context-certificates.json.gz`)؛ لا يُحرَّر باليد. تعريفُ "
        "الشاهد وخواصُّه في `formal/Slge/Coverage.lean` ومرآتُه `slge.coverage`؛ والأعدادُ المودَعة "
        "في `CoverageTable.lean` "
        "يبرهن Lean عليها قسمتَها وحدَّها (ADR ٢٩). **الغيابُ ليس امتناعًا**: ما لا شاهدَ له يبقى في "
        "جدوله «معلومة» (المادّة ١٥).",
        "",
        f"الصورُ: {m['forms']:,} ابتداءً، {m['context_forms']:,} في السياق؛ المواقعُ {m['tokens']:,}.",
        "",
        "## ١. الشبكة",
        "",
        f"المرخَّصُ من الـ116: **{c['licensable']}** (بلا الألف المتحرّكة — الكتاب: «لأن الألف لا تكون "
        f"أبدا إلا ساكنة»)؛ المشهودُ في المودَعين **{c['attested']}**"
        + (f"؛ بلا شاهد: {'، '.join(c['unattested'])}" if c["unattested"] else " — كلُّ مرخَّصٍ مشهود")
        + f"؛ الألفُ المتحرّكة في المصحف: {c['vowelled_alif_seen']}. مبرهَن: "
        "`Coverage.attested_eq_licensable` (المشهودُ هو المرخَّصُ بعينه).",
        "",
        "## ٢. القرّاء (بوّاباتُ السُّلَّم القارئة)",
        "",
        "| البوّابة | صورٌ تُقرأ | مواقع |", "|---|---|---|",
        *(f"| {g} | {_pct(v['forms'], m['forms'])} | {_pct(v['tokens'], m['tokens'])} |"
          for g, v in m["readers"].items()),
        "",
        "بوّابةُ «الأدوات» تقرأ الجارَ قبل الكلمة لا الكلمةَ المنفردة؛ قياسُها في `ADAWAT_INDEX.md`.",
        "",
        "## ٣. صفوفُ الجداول المودَعة",
        "",
        "شاهدُ الصفّ: صورةٌ من المودَع يقرؤها قارئُ الجدول على ذلك الصفّ.",
        "",
        "| الجدول | الصفوف | مفهوم (بشاهد) | معلومة (بلا شاهد) |", "|---|---|---|---|",
        f"| الموزِّع (`tawzi.TABLE`) | {t['tawzi']['rows']} | {t['tawzi']['attested']} | "
        f"{t['tawzi']['rows'] - t['tawzi']['attested']} |",
        f"| الأعلام (`alam_table.ALAM`) | {t['alam']['rows']} | {t['alam']['attested']} | "
        f"{t['alam']['rows'] - t['alam']['attested']} |",
        f"| السوابق (`sawabiq_table.TABLE`) | {t['sawabiq']['rows']} | "
        f"{t['sawabiq']['attested']} | "
        f"{t['sawabiq']['rows'] - t['sawabiq']['attested']} |",
        "",
        "صفوفُ الموزِّع بلا شاهد (من جداول النحو لا من المصحف؛ تبقى «معلومة»): "
        + ("، ".join(t["tawzi"]["unattested"]) or "—") + ".",
        "",
        "الأعلامُ بلا شاهد: " + ("، ".join(t["alam"]["unattested"]) or "— (كلُّ موقَّعٍ مشهود)") + ".",
        "",
        "السوابقُ بلا شاهد: " + ("، ".join(t["sawabiq"]["unattested"]) or "— (كلُّ صفٍّ مشهود)") + ".",
        "",
        "## ٤. جذورُ المقاييس وعقدُ المخصّص",
        "",
        "شاهدُ الجذر: صورةٌ يقرؤها الجذعُ عليه — **قاطعٌ** إن لم يقرأها على غيره، **محتملٌ** إن "
        "قرأها على غيره أيضًا (`Coverage.witnessOf`). شاهدُ العقدة: جذرٌ من جذور عنوانها له شاهدٌ قاطع "
        "(`Coverage.nodeGrade`).",
        "",
        f"الصورُ التي يقرؤها الجذعُ على جذرٍ من المقاييس: {_pct(q['forms_with_root'], m['forms'])}.",
        "",
        "| | المودَع | قاطع | محتملٌ فقط | بلا شاهد | بلا جذور |", "|---|---|---|---|---|---|",
        f"| جذورُ المقاييس | {q['roots']:,} | {q['qati']:,} | {q['muhtamal_only']:,} | "
        f"{q['none']:,} | — |",
        f"| عقدُ المخصّص | {k['nodes']:,} | {k['qati']:,} | {k['muhtamal_only']:,} | {k['none']:,} | "
        f"{k['no_roots']:,} |",
        "",
        "أكثرُ الجذور شواهدَ قاطعة: " + "، ".join(f"{r} {n}" for r, n in q["top_qati"]) + ".",
        "",
        "عقدٌ ذاتُ جذورٍ بلا شاهد (أوائلُها): " + "؛ ".join(k["sample_none"]) + ".",
        "",
        "## ما بقي باسمه",
        "",
        "- جذورُ المقاييس بلا شاهد ليست خطأً في الجدول ولا في الجذع: المصحفُ لا يستعمل كلَّ العربيّة؛ "
        "شاهدُها يأتي من مدوّنةٍ ثانيةٍ مختومة (قرارُ المالك).",
        "- شاهدُ الجذر من قراءات الجذع لا من قسمة MASAQ: القاطعُ قطعُ القارئ لا قطعُ المرجع "
        "(`JIDH_INDEX.md` للفرق).",
        "- عقدُ المخصّص بلا جذورٍ في عنوانها (العناوينُ الهيكليّة) لا تُحكم: لا شاهدَ ولا غياب.",
        "",
    ]
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    m = measure()
    lean, py = render_tables(m)
    text = render(m)
    if "--check" in argv:
        ok = (TARGET.read_text(encoding="utf-8") == text
              and LEAN.read_text(encoding="utf-8") == lean
              and PY.read_text(encoding="utf-8") == py)
        sys.stdout.write("COVERAGE_INDEX.md مطابق\n" if ok else "COVERAGE_INDEX.md غيرُ مطابق\n")
        return 0 if ok else 1
    LEAN.write_text(lean, encoding="utf-8")
    PY.write_text(py, encoding="utf-8")
    TARGET.write_text(text, encoding="utf-8")
    sys.stdout.write("كُتب COVERAGE_INDEX.md وجدولا التغطية\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
