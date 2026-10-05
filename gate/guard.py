"""حارسُ عدم الخرق: لا يقرأ بايتًا ولا يكتبه ولا يفكّ ترميزًا إلّا `gate/`.

يمشي على كلّ `.py` في الشجرة (خارج `gate/` و`suspended/` و`formal/`) ويرفض:

* فتحَ ملفٍّ أو قراءتَه أو كتابتَه: `open`، `read_text`، `read_bytes`، `write_text`،
  `write_bytes`، `Path(...).open`، `gzip.open`، `json.load` من ملفّ، `csv.reader`.
* فكَّ الترميز أو تطبيعَه: `.decode(`، `.encode(`، `unicodedata.normalize`.
* استيرادَ ما عُلِّق: `suspended`، أو `gate._x` الداخليّ، أو `canonical116` مباشرةً.
* `print` و`sys.argv` و`input` (المخارجُ والمداخلُ غير الموسومة).

القائمةُ البيضاء: `gate/`، و`tests/`، و`tools/gen_registry.py`. وما سواها يكسر البناء.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXEMPT_DIRS = ("gate", "suspended", "formal", "tests", ".git", ".lake", "__pycache__")
EXEMPT_FILES = ("tools/gen_registry.py",)
IO_ATTRS = frozenset(
    {
        "read_text", "read_bytes", "write_text", "write_bytes", "open", "decode", "encode",
        "normalize", "load", "loads", "reader", "DictReader", "argv", "stdin", "stdout",
    }
)
IO_NAMES = frozenset({"open", "print", "input", "exec", "eval"})
FORBIDDEN_IMPORT_PREFIXES = (
    "suspended", "canonical116", "gate._", "gate.contextual", "gate.bridge",
                             "gate.audit", "gate.check_codebooks", "gate.rasm_consistency",
                             "gate.mabni_verbs", "gate.mabni_bridge", "gate.maqayis_root_table")


@dataclass(frozen=True)
class Breach:
    path: str
    line: int
    what: str


def _files() -> list[Path]:
    out = []
    for p in ROOT.rglob("*.py"):
        rel = p.relative_to(ROOT)
        if any(part in EXEMPT_DIRS for part in rel.parts[:-1]) or str(rel) in EXEMPT_FILES:
            continue
        out.append(p)
    return sorted(out)


def breaches() -> list[Breach]:
    found: list[Breach] = []
    for p in _files():
        rel = str(p.relative_to(ROOT))
        tree = ast.parse(p.read_text(encoding="utf-8"))
        for n in ast.walk(tree):
            if isinstance(n, (ast.Import, ast.ImportFrom)):
                names = [a.name for a in n.names] if isinstance(n, ast.Import) else [n.module or ""]
                for m in names:
                    if m.startswith(FORBIDDEN_IMPORT_PREFIXES):
                        found.append(Breach(rel, n.lineno, f"import {m}"))
            elif isinstance(n, ast.Call):
                f = n.func
                if isinstance(f, ast.Name) and f.id in IO_NAMES:
                    found.append(Breach(rel, n.lineno, f.id))
                elif isinstance(f, ast.Attribute) and f.attr in IO_ATTRS:
                    found.append(Breach(rel, n.lineno, f.attr))
            elif isinstance(n, ast.Attribute) and n.attr in ("argv", "stdin"):
                found.append(Breach(rel, n.lineno, n.attr))
    return found


def main() -> int:
    b = breaches()
    for x in b:
        print(f"خرق: {x.path}:{x.line} {x.what}")
    print("الحارس:", "لا خرق" if not b else f"{len(b)} خرقًا")
    return 1 if b else 0


if __name__ == "__main__":
    raise SystemExit(main())
