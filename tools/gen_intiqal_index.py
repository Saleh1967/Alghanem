"""حارسُ الانتقالات وفهرسُها (INTIQAL_INDEX.md) وجدولُه في Lean (`IntiqalTable.lean`): كلُّ دالّةٍ عامّة في
`src/slge` تنقل خاناتٍ إلى خانات (معلَمةٌ ‎Word → Word‎ أو ‎tuple[Cell, ...]‎ مدخلًا ومخرجًا) يجب أن تكون
في `slge.intiqal.REGISTRY`، وكلُّ صفٍّ فيه يجب أن تكون دالّتُه موجودةً، ومبرهنتُه — إن ذُكرت — مدقَّقةً في
`Audit.lean` (`formal/out/axioms.txt`)، وكلُّ دَينٍ بملاحظة. يرفض بالاسم: `TRANSITION_NOT_REGISTERED`،
`REGISTERED_FUNCTION_MISSING`، `THEOREM_NOT_AUDITED`، `DEBT_WITHOUT_NOTE`.
بـ`--check` يقارن الفهرسَ والجدولَ بما يولَّد الآن ويُسقط البناءَ على أيّ خرق.
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path

from slge.intiqal import KINDS, REGISTRY

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src" / "slge"
AXIOMS = ROOT / "formal" / "out" / "axioms.txt"
TARGET = ROOT / "INTIQAL_INDEX.md"
LEAN = ROOT / "formal" / "Slge" / "IntiqalTable.lean"
CELLISH = {"Word", "tuple[Cell, ...]"}
SKIP = {"intiqal", "shahada", "order", "status", "guard", "manifest", "gates"}


def transitions() -> list[tuple[str, str]]:
    """الدوالُّ العامّة التي مدخلُها ومخرجُها خانات، بترتيب الوحدات."""

    out: list[tuple[str, str]] = []
    for p in sorted(SRC.glob("*.py")):
        if p.stem in SKIP or p.stem.startswith("_"):
            continue
        tree = ast.parse(p.read_text(encoding="utf-8"))
        for n in tree.body:
            if not isinstance(n, ast.FunctionDef) or n.name.startswith("_"):
                continue
            ret = ast.unparse(n.returns) if n.returns else ""
            args = [ast.unparse(a.annotation) if a.annotation else "" for a in n.args.args]
            if ret in CELLISH and any(a in CELLISH for a in args):
                out.append((p.stem, n.name))
    return out


def audited() -> set[str]:
    names: set[str] = set()
    for line in AXIOMS.read_text(encoding="utf-8").splitlines():
        if line.startswith("'"):
            names.add(line[1:].split("'")[0])
    return names


def problems() -> list[str]:
    found = set(transitions())
    reg = {(r.module, r.function): r for r in REGISTRY}
    ax = audited()
    out = [f"TRANSITION_NOT_REGISTERED:{m}.{f}" for m, f in sorted(found - set(reg))]
    out += [f"REGISTERED_FUNCTION_MISSING:{m}.{f}" for m, f in sorted(set(reg) - found)]
    out += [f"THEOREM_NOT_AUDITED:{r.module}.{r.function}:{r.theorem}"
            for r in REGISTRY if r.theorem and r.theorem not in ax]
    out += [f"DEBT_WITHOUT_NOTE:{r.module}.{r.function}" for r in REGISTRY
            if not r.theorem and not r.note]
    return out


def _lean_str(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def render_lean() -> str:
    lines = [
        "import Slge.Categories", "",
        "/-! سجلُّ الانتقالات (‎Word → Word‎) في `src/slge` بأسماء مبرهناتها المدقَّقة — مولَّدٌ بـ",
        "`tools/gen_intiqal_index.py` من `slge.intiqal.REGISTRY` بعد فحص الشجرة و`Audit.lean`؛",
        "لا يُحرَّر باليد. الصفُّ: (الوحدة، الدالّة، المبرهنة أو فارغ، نوعُها: 0 إغلاق / 1 خاصّة / 2 دَين).",
        "-/", "",
        "namespace Slge.IntiqalTable", "",
        "def registry : List (String × String × String × Nat) := [",
    ]
    rows = [f"  ({_lean_str(r.module)}, {_lean_str(r.function)}, {_lean_str(r.theorem)}, "
            f"{KINDS.index(r.kind)})" for r in REGISTRY]
    lines += [",\n".join(rows), "]", "",
              f"theorem registry_length : registry.length = {len(REGISTRY)} := by rfl", "",
              "end Slge.IntiqalTable", ""]
    return "\n".join(lines)


def render() -> str:
    bad = problems()
    if bad:
        raise SystemExit("\n".join(bad))
    by_kind = {k: sum(1 for r in REGISTRY if r.kind == k) for k in KINDS}
    lines = [
        "# فهرسُ الانتقالات — لا انتقالَ على الـ116 إلّا مسجَّلًا باسمه ومبرهنته",
        "",
        "مولَّدٌ بـ`python tools/gen_intiqal_index.py` من `slge.intiqal.REGISTRY`؛ لا يُحرَّر باليد. "
        "الحارسُ يمشي على `src/slge` فيرفض دالّةَ انتقالٍ عامّةً (‎Word → Word‎) غيرَ مسجَّلة، وصفًّا "
        "بلا دالّة، ومبرهنةً غيرَ مدقَّقة في `Audit.lean`، ودَينًا بلا ملاحظة. السجلُّ **مفحوصٌ** لا "
        "مبرهَن: Lean (`IntiqalTable`) يحمل الأسماءَ لا الدوالَّ، والإغلاقُ حيث ذُكر مبرهنةٌ باسمها.",
        "",
        f"{len(REGISTRY)} انتقالًا: إغلاقٌ {by_kind['إغلاق']}، خاصّةٌ {by_kind['خاصّة']}، "
        f"دَينٌ باسمه {by_kind['—']}.",
        "",
        "| الوحدة | الدالّة | المبرهنة | النوع | ملاحظة |", "|---|---|---|---|---|",
        *(f"| `{r.module}` | `{r.function}` | {('`' + r.theorem + '`') if r.theorem else '—'} | "
          f"{r.kind} | {r.note} |" for r in REGISTRY),
        "",
        "## ما ليس هنا — باسمه", "",
        "- الديونُ أعلاه انتقالاتٌ بلا مبرهنةٍ باسمها؛ لا تُحذف الدالّةُ ولا تُزاد مبرهنةٌ من الذاكرة؛ "
        "تُبرهَن واحدةً واحدة أو تُعلَّق.",
        "- «خاصّة» ليست إغلاقًا: تُثبت حالةً أو علامةً لا حفظَ الترخيص؛ ترقيتُها إلى إغلاقٍ مبرهنةٌ جديدة.",
        "- الدوالُّ التي تنقل خاناتٍ عبر أنواعٍ وسيطة (قراءاتٌ، سجلّاتٌ) خارج هذا الحصر؛ حصرُها بالنوع "
        "الوسيط خطوةٌ لاحقة.",
        "",
    ]
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    text, lean = render(), render_lean()
    if "--check" in argv:
        ok = TARGET.read_text(encoding="utf-8") == text and LEAN.read_text(encoding="utf-8") == lean
        sys.stdout.write("INTIQAL_INDEX.md مطابق\n" if ok else "INTIQAL_INDEX.md غيرُ مطابق\n")
        return 0 if ok else 1
    TARGET.write_text(text, encoding="utf-8")
    LEAN.write_text(lean, encoding="utf-8")
    sys.stdout.write(f"كُتب INTIQAL_INDEX.md ({len(REGISTRY)} انتقالًا)\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
