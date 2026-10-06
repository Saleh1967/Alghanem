"""فحصُ السجلّ: كلُّ وحدةٍ في `slge.manifest` موصولةٌ في كلّ موضعٍ من الشجرة، وكلُّ موضعٍ في السجلّ.

المواضع: `src/slge/<name>.py`؛ `formal/Slge/<Lean>.lean` و`import Slge.<Lean>` في `Slge.lean` وتدقيقُ
مبرهناته في `Audit.lean`؛ `| ["<table>"] =>` في `Main.lean` و`formal/out/<table>.csv`؛ أداةُ الفهرس
في `tools/` وفي `guard.EXEMPT_FILES` وفهرسُها `<NAME>_INDEX.md` مذكورٌ في `CLAUDE.md`؛ والاختبارُ في
`tests/`.
بـ`--tables` يطبع قائمةَ الجداول لـCI، وبـ`--indexes` يشغّل كلَّ أداةِ فهرسٍ بـ`--check`.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

from slge.guard import EXEMPT_FILES
from slge.manifest import MODULES, index_tools, tables

ROOT = Path(__file__).resolve().parent.parent


def problems() -> list[str]:
    out: list[str] = []
    slge_lean = (ROOT / "formal" / "Slge.lean").read_text(encoding="utf-8")
    audit = (ROOT / "formal" / "Audit.lean").read_text(encoding="utf-8")
    main = (ROOT / "formal" / "Main.lean").read_text(encoding="utf-8")
    claude = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")
    for m in MODULES:
        if m.name != "bits" and not (ROOT / "src" / "slge" / f"{m.name}.py").exists():
            out.append(f"{m.name}: لا وحدةَ src/slge/{m.name}.py")
        for lean in m.lean:
            path = ROOT / "formal" / "Slge" / f"{lean}.lean"
            if not path.exists():
                out.append(f"{m.name}: لا ملفَّ formal/Slge/{lean}.lean")
                continue
            if f"import Slge.{lean}\n" not in slge_lean:
                out.append(f"{m.name}: Slge.lean لا يستورد Slge.{lean}")
            thms = re.findall(r"^theorem (\w+)", path.read_text(encoding="utf-8"), re.M)
            if not any(re.search(rf"#print axioms [\w.]*\.{t}\n", audit) for t in thms):
                out.append(f"{m.name}: Audit.lean لا يدقّق شيئًا من Slge/{lean}.lean")
        for t in m.tables:
            if f'| ["{t}"] =>' not in main:
                out.append(f"{m.name}: Main.lean لا يصدّر الجدول {t}")
            if not (ROOT / "formal" / "out" / f"{t}.csv").exists():
                out.append(f"{m.name}: لا جدولَ formal/out/{t}.csv")
        if m.index:
            if not (ROOT / "tools" / m.index).exists():
                out.append(f"{m.name}: لا أداةَ tools/{m.index}")
            if f"tools/{m.index}" not in EXEMPT_FILES:
                out.append(f"{m.name}: tools/{m.index} ليست في guard.EXEMPT_FILES")
            idx = f"{m.name.upper()}_INDEX.md"
            if not (ROOT / idx).exists():
                out.append(f"{m.name}: لا فهرسَ {idx}")
            if idx not in claude:
                out.append(f"{m.name}: CLAUDE.md لا يذكر {idx}")
        if m.test and not (ROOT / "tests" / m.test).exists():
            out.append(f"{m.name}: لا اختبارَ tests/{m.test}")
    # العكس: كلُّ جدولٍ في Main وكلُّ ملفِّ Lean وكلُّ أداةِ فهرسٍ في السجلّ
    for t in re.findall(r'\| \["(\w+)"\] =>', main):
        if t not in tables():
            out.append(f"الجدول {t} في Main.lean ليس في السجلّ")
    for p in (ROOT / "formal" / "Slge").glob("*.lean"):
        if p.stem not in {lean for m in MODULES for lean in m.lean}:
            out.append(f"الملفّ formal/Slge/{p.name} ليس في السجلّ")
    for p in (ROOT / "tools").glob("gen_*_index.py"):
        if p.name not in index_tools() and p.name != "gen_lean_index.py":
            out.append(f"الأداة tools/{p.name} ليست في السجلّ")
    return out


def main() -> int:
    if "--tables" in sys.argv:
        sys.stdout.write(" ".join(tables()) + "\n")
        return 0
    if "--indexes" in sys.argv:
        rc = 0
        for tool in index_tools():
            res = subprocess.run([sys.executable, str(ROOT / "tools" / tool), "--check"], cwd=ROOT,
                                 capture_output=True, text=True)
            sys.stdout.write(res.stdout)
            if res.returncode != 0:
                sys.stderr.write(res.stderr)
                rc = 1
        return rc
    ps = problems()
    for p in ps:
        sys.stderr.write(p + "\n")
    head = f"السجلّ: {len(MODULES)} وحدة، {len(tables())} جدولًا، {len(index_tools())} فهرسًا — "
    sys.stdout.write(head + ("مطابق\n" if not ps else f"{len(ps)} خللًا\n"))
    return 1 if ps else 0


if __name__ == "__main__":
    raise SystemExit(main())
