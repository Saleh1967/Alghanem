"""فراكتالُ التركيب: أزواجُ الألفاظ بأقسامها على المصحف (ADR ٨٠) — `A116/FractalTarkibData.lean`.

لكلّ آيةٍ متتاليةُ أقسام كلماتها بالترتيب من وسم QAC 0.4 المختوم (`gen_qac.QAC_SHA256`، ADR ٤١):
كلُّ قطعةٍ كلمة (السابقةُ والجذعُ واللاحقة)، وقسمُها من وسمها بقسمةٍ معلَنة (`ISM`، `FIL`، وما سواهما
حرف) على تقسيم الألفيّة «واسمٌ وفعلٌ ثمّ حرفٌ الكلم»؛ و«أل» ليست كلمةً بل علامةُ الاسم («بالجرّ
والتنوين والندا وأل»)، فوسمُ `DET` لا يُعدّ (`DET_IS_ISM_SIGN`). والقسمُ مرجعٌ لا تقرؤه البوّابة
(`TARKIB_QISM_IS_INPUT`، `QISM_ORACLE`).

`--check` يُسقط البناءَ بـ`FRACTAL_TARKIB_LEAN_DRIFTED` أو `FRACTAL_TARKIB_COUNT_DRIFTED`
(`A116/FractalTarkibCount.lean`: عدُّ الأزواج قطعةً قطعة). معفاةٌ في الحارس لأنّها أداةُ إيداع.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

LEAN = ROOT / "formal" / "a116" / "A116" / "FractalTarkibData.lean"
COUNT = ROOT / "formal" / "a116" / "A116" / "FractalTarkibCount.lean"
CHUNK = 400

ISM = frozenset({"N", "PN", "ADJ", "PRON", "DEM", "REL", "T", "LOC", "IMPN"})
"""الاسم: الاسمُ والعلَمُ والصفةُ والضميرُ والإشارةُ والموصولُ والظرفان واسمُ الفعل."""
FIL = frozenset({"V"})
SKIP = frozenset({"DET"})


def _load(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


Q = _load("gen_qac", ROOT / "tools" / "gen_qac.py")
P = _load("gen_qac_pos", ROOT / "tools" / "gen_qac_pos.py")


def code(tag: str) -> int:
    return 0 if tag in ISM else 1 if tag in FIL else 2


def rows() -> list[list[int]]:
    """لكلّ آيةٍ أقسامُ كلماتها بالترتيب (0 اسم، 1 فعل، 2 حرف)."""
    segs = P.segments(Q.source())
    out = []
    for key in sorted(segs):
        out.append([code(x.split(":", 1)[1]) for _w, ss in segs[key] for x in ss
                    if x.split(":", 1)[1] not in SKIP])
    return out


def render_lean(rs: list[list[int]]) -> str:
    lines = ["  [" + ", ".join(map(str, r)) + "]" for r in rs]
    chunks = [lines[i:i + CHUNK] for i in range(0, len(lines), CHUNK)]
    defs = "".join(f"def ayat{j} : List (List Nat) := [\n" + ",\n".join(ch) + "]\n\n"
                   for j, ch in enumerate(chunks))
    joined = " ++ ".join(f"ayat{j}" for j in range(len(chunks)))
    return (
        "/-! مولَّدٌ بـ`tools/gen_fractal_tarkib.py` من وسم QAC 0.4 المختوم (ADR ٨٠)؛ "
        "لا يُحرَّر باليد. -/\n\n"
        "set_option maxRecDepth 100000\n\n"
        "namespace A116.FractalTarkib\n\n" + defs +
        "/-- أقسامُ كلمات كلّ آية بالترتيب: 0 اسم، 1 فعل، 2 حرف. -/\n"
        "def ayat : List (List Nat) := " + joined + "\n\nend A116.FractalTarkib\n"
    )


def accumulators(rs: list[list[int]]) -> list[list[int]]:
    """عدّادُ الأزواج التسعة (رمزُ ‎3a + b‎) قبل كلّ قطعةٍ وبعد الأخيرة."""
    v = [0] * 9
    out = [list(v)]
    for i in range(0, len(rs), CHUNK):
        for r in rs[i:i + CHUNK]:
            for a, b in zip(r, r[1:], strict=False):
                v[3 * a + b] += 1
        out.append(list(v))
    return out


def render_count(rs: list[list[int]]) -> str:
    acc = accumulators(rs)
    n = len(acc) - 1
    rows_ = ",\n".join("  [" + ", ".join(map(str, v)) + "]" for v in acc)
    accs = "def accs : List (List Nat) := [\n" + rows_ + "]\n\n"
    lemmas = "".join(
        f"theorem qitaa{j} : ayat{j}.foldl cntPairs (accs.getD {j} []) = "
        f"accs.getD {j + 1} [] := by\n"
        "  decide +kernel\n\n" for j in range(n))
    chain = ", ".join(f"qitaa{j}" for j in range(n))
    return (
        "import A116.FractalTarkib\n\n"
        "/-! مولَّدٌ بـ`tools/gen_fractal_tarkib.py` (ADR ٨٠)؛ لا يُحرَّر باليد. عدُّ الأزواج على المصحف "
        "قطعةً قطعة، كلُّ قطعةٍ تفحصها النواة، ثمّ تُوصل بالطيّ (`List.foldl_append`). -/\n\n"
        "set_option maxRecDepth 200000\n\n"
        "namespace A116.FractalTarkib\n\n" + accs + lemmas +
        "/-- **الأنواعُ التسعة كلُّها واقعةٌ بأعدادها** برمز ‎3a + b‎ (0 اسم، 1 فعل، 2 حرف). -/\n"
        "theorem azwaj_mushaf :\n    ayat.foldl cntPairs [0, 0, 0, 0, 0, 0, 0, 0, 0] = ["
        + ", ".join(map(str, acc[-1])) + "] := by\n"
        f"  rw [show [0, 0, 0, 0, 0, 0, 0, 0, 0] = accs.getD 0 [] from rfl]\n"
        f"  simp only [ayat, List.foldl_append, {chain}]\n  rfl\n\n"
        "end A116.FractalTarkib\n"
    )


def breaches() -> list[str]:
    rs = rows()
    bad = []
    if not LEAN.exists() or LEAN.read_text(encoding="utf-8") != render_lean(rs):
        bad.append("FRACTAL_TARKIB_LEAN_DRIFTED")
    if not COUNT.exists() or COUNT.read_text(encoding="utf-8") != render_count(rs):
        bad.append("FRACTAL_TARKIB_COUNT_DRIFTED")
    return bad


def main(argv: list[str]) -> int:
    if "--check" not in argv:
        rs = rows()
        LEAN.write_text(render_lean(rs), encoding="utf-8")
        COUNT.write_text(render_count(rs), encoding="utf-8")
        return 0
    bad = breaches()
    print("\n".join(bad) if bad else "فراكتالُ التركيب مطابق")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
