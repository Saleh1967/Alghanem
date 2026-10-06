"""حارسُ عدم الخرق: لا قارئَ للنصّ ولا كاتبَ له في SLGE؛ المدخلُ شهادةُ بوّابة الغانم
(`slge.entry`).

يمشي على كلّ `.py` في الشجرة (خارج `suspended/` و`formal/` و`tests/`) ويرفض:

* فتحَ ملفٍّ أو قراءتَه أو كتابتَه: `open`، `read_text`، `read_bytes`، `write_text`،
  `write_bytes`، `Path(...).open`، `gzip.open`، `json.load` من ملفّ، `csv.reader`.
* فكَّ الترميز أو تطبيعَه: `.decode(`، `.encode(`، `unicodedata.normalize`.
* استيرادَ ما عُلِّق: `suspended`، أو `gate._x` الداخليّ، أو `canonical116` مباشرةً.
* `print` و`sys.argv` و`input` (المخارجُ والمداخلُ غير الموسومة).

القائمةُ البيضاء: `tests/`، و`tools/gen_*.py`، و`order.py` (يبصم خاناتٍ لا نصًّا).
وما سواها يكسر البناء.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXEMPT_DIRS = ("suspended", "formal", "tests", ".git", ".lake", "__pycache__", ".venv")
EXEMPT_FILES = (
    "src/slge/guard.py", "tools/gen_status.py", "tools/gen_registry.py", "tools/gen_lean_index.py",
    "tools/gen_rawabit_index.py", "tools/gen_damair_index.py",
    "tools/gen_ishara_index.py", "tools/gen_istifham_index.py",
    "tools/gen_nida_index.py", "tools/gen_zuruf_index.py",
    "tools/gen_zaman_index.py", "tools/gen_adad_index.py",
    "tools/gen_marifa_index.py", "tools/gen_sarf_index.py",
    "tools/gen_tawabi_index.py", "tools/gen_nawasikh_index.py", "tools/gen_jazm_index.py",
    "tools/gen_mansubat_index.py", "tools/gen_majrurat_index.py",
    "tools/gen_wasl_index.py", "tools/gen_ism_index.py", "tools/gen_fil_index.py",
    "tools/gen_huruf_index.py",
    "src/slge/order.py",  # يبصم خاناتٍ لا نصًّا
)
IO_ATTRS = frozenset(
    {
        "read_text", "read_bytes", "write_text", "write_bytes", "open", "decode", "encode",
        "normalize", "load", "loads", "reader", "DictReader", "argv", "stdin", "stdout",
    }
)
IO_NAMES = frozenset({"open", "print", "input", "exec", "eval"})
FORBIDDEN_IMPORT_PREFIXES = (
    "suspended", "slge.orthography", "slge.lexicon", "slge.morphology", "slge.encoding",
)


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
