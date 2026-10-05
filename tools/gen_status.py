"""ولّد `STATUS.md` من `slge.status.LEDGER`؛ و‎--check‎ يفشل إن كان الملفُّ قديمًا."""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

from slge.status import LEDGER, Status

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "STATUS.md"


def render() -> str:
    counts = Counter(c.status for c in LEDGER)
    lines = [
        "# سجلُّ الدعاوى",
        "",
        "مولَّدٌ من `src/slge/status.py` بـ`python tools/gen_status.py`؛ لا يُحرَّر باليد.",
        "",
        "| الوسم | العدد |",
        "|---|---|",
        *[f"| {s.name} | {counts[s]} |" for s in Status],
        "",
        "| المعرّف | الدعوى | الوسم | السند | ملاحظة |",
        "|---|---|---|---|---|",
    ]
    for c in sorted(LEDGER, key=lambda c: (c.status.value, c.claim_id)):
        support = "<br>".join(f"`{x}`" for x in c.support) or "—"
        lines.append(f"| {c.claim_id} | {c.statement} | {c.status.name} | {support} | {c.note} |")
    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    text = render()
    if "--check" in argv:
        if not TARGET.exists() or TARGET.read_text(encoding="utf-8") != text:
            print("STATUS.md قديم: شغّل python tools/gen_status.py", file=sys.stderr)
            return 1
        return 0
    TARGET.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
