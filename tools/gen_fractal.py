"""الفراكتالُ على المصحف كلِّه من التشغيل إلى Lean (ADR ٧٨): `A116/FractalData.lean` تفحصه النواة.

لكلّ آيةٍ صفٌّ واحد، بمرحلتي التشابه الذاتيّ:
* **الأصناف** (ADR ٧٧): كلُّ كلمةٍ تدخل `gate.enter` بلا سياق؛ عددُ الجاهز والمرفوض، وأثرُ
  الآية على الأصناف الثلاثيّة صفًّا من أربع قيم: صورةُ كلّ حالةٍ (ابتداء، cv، v، c)، و4 انقطاع.
* **الحدّ والإصلاح**: كلُّ كلمةٍ في سياقها كما في `tools/gen_context_certificates.py` (الأولى
  ابتداءً، وما بعدها موصولٌ بما قبلها، والأخيرةُ وقفًا)؛ فإن جهزت الآيةُ كلُّها أُصلحت كلُّ يسرى
  بيمناها (`gate.licence.repair_junction`) وطُويت الآيةُ بآلة الحرف وقفًا بحدّها بين الكلمات
  (`gate.mizan`، جدولُ `A116.Harf`، أي `Harf.lineWaqfB`)؛ ويُعدّ الإصلاحُ، والحدودُ التي
  يحرّكها الحدّ، وما حرّكه منها بعد إصلاح.

`--check` يُسقط البناءَ بـ`FRACTAL_LEAN_DRIFTED`. معفاةٌ في الحارس لأنّها أداةُ إيداع.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from gate import Refusal, enter  # noqa: E402
from gate.licence import kind_of, repair_junction  # noqa: E402
from gate.mizan import BAD, HADD, QABIL_WAQF, WAQF, run  # noqa: E402

CORPUS = ROOT / "corpora" / "quran-simple-enhanced.txt"
LEAN = ROOT / "formal" / "a116" / "A116" / "FractalData.lean"
CHUNK = 400

_SPEC = importlib.util.spec_from_file_location("gen_context_certificates",
                                               ROOT / "tools" / "gen_context_certificates.py")
assert _SPEC and _SPEC.loader
C: Any = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(C)

Row = tuple[tuple[int, int, int, int], int, int, bool, bool, int, int, int, int]
"""صفُّ الآية: الأثر، الجاهز، المرفوض، جهوزُ السياق، القبول، الحدود، الإصلاح، ما حرّكه الحدّ."""

STATES = ("start", "cv", "v", "c")
DEAD = 4
WASL = {("cv", "cv"), ("cv", "v"), ("cv", "c"), ("v", "cv"), ("v", "c"), ("c", "cv")}


def _step(s: int, x: str) -> int:
    if s == DEAD:
        return DEAD
    if s == 0:
        return STATES.index(x) if x == "cv" else DEAD
    return STATES.index(x) if (STATES[s], x) in WASL else DEAD


def athar_of(kinds: list[str]) -> tuple[int, int, int, int]:
    """الأثرُ: صورةُ كلّ حالةٍ من الأربع (4 انقطاع)."""
    out = []
    for i in range(4):
        s = i
        for x in kinds:
            s = _step(s, x)
        out.append(s)
    return (out[0], out[1], out[2], out[3])


def rows() -> list[Row]:
    raw = CORPUS.read_bytes()
    lines = C.lines_of(raw)
    joined = C.gates_for(lines, CORPUS)
    start = {"continue": C.gate(), "pause": C.Gate(C.Context(exit="pause"), corpus=CORPUS)}
    out = []
    for tokens in lines:
        ready = refused = 0
        kinds: list[str] = []
        for w in tokens:
            cert = enter(w.encode("utf-8"))
            if isinstance(cert, Refusal):
                refused += 1
            else:
                ready += 1
                kinds += list(kind_of(cert.atoms))
        atoms: list[tuple[str, ...]] = []
        ok = True
        for i, w in enumerate(tokens):
            exit_ = C.EXITS[i == len(tokens) - 1]
            g = start[exit_] if i == 0 else joined[(C.repair(tokens[i - 1])[0], exit_)]
            cert = g.enter(w.encode("utf-8"))
            if isinstance(cert, Refusal):
                ok = False
                break
            atoms.append(tuple(cert.atoms))
        accepted = False
        repairs = moved = moved_repaired = 0
        if ok:
            fixed = []
            tagged = []
            for i, a in enumerate(atoms):
                if i + 1 < len(atoms):
                    a2, tag = repair_junction(a, atoms[i + 1])
                    fixed.append(a2)
                    tagged.append(tag is not None)
                    repairs += tag is not None
                else:
                    fixed.append(a)
                    tagged.append(False)
            s = BAD
            for i, a in enumerate(fixed):
                if i > 0:
                    if HADD[s] != s:
                        moved += 1
                        moved_repaired += tagged[i - 1]
                    s = HADD[s]
                s = run(WAQF, s, a)
            accepted = QABIL_WAQF[s]
        out.append((athar_of(kinds), ready, refused, ok, accepted, max(len(tokens) - 1, 0), repairs,
                    moved, moved_repaired))
    return out


def render_lean(rs: list[Row]) -> str:
    def b(x: bool) -> str:
        return "true" if x else "false"
    lines = [f"  ⟨[{a[0]}, {a[1]}, {a[2]}, {a[3]}], {r}, {f}, {b(o)}, {b(c)}, {s}, {p}, {m}, {mr}⟩"
             for a, r, f, o, c, s, p, m, mr in rs]
    chunks = [lines[i:i + CHUNK] for i in range(0, len(lines), CHUNK)]
    defs = "".join(f"def ayat{j} : List Aya := [\n" + ",\n".join(ch) + "]\n\n"
                   for j, ch in enumerate(chunks))
    joined = " ++ ".join(f"ayat{j}" for j in range(len(chunks)))
    return (
        "import A116.FractalMushafDef\n\n"
        "/-! مولَّدٌ بـ`tools/gen_fractal.py` من تشغيل البوّابة على المصحف المختوم (ADR ٧٨)؛ "
        "لا يُحرَّر باليد. -/\n\n"
        "set_option maxRecDepth 100000\n\n"
        "namespace A116.FractalMushaf\n\n" + defs +
        "/-- صفٌّ لكلّ آية بترتيب المصحف. -/\n"
        "def ayat : List Aya := " + joined + "\n\nend A116.FractalMushaf\n"
    )


def breaches() -> list[str]:
    if not LEAN.exists() or LEAN.read_text(encoding="utf-8") != render_lean(rows()):
        return ["FRACTAL_LEAN_DRIFTED"]
    return []


def main(argv: list[str]) -> int:
    if "--check" not in argv:
        LEAN.write_text(render_lean(rows()), encoding="utf-8")
        return 0
    bad = breaches()
    print("\n".join(bad) if bad else "الفراكتالُ على المصحف مطابق")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
