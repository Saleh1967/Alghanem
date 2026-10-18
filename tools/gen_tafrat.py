"""سجلُّ طفرات Lean (ADR ١١١، الدستور م١٩).

كلُّ طفرةٍ في `docs/tafrat.json` نصٌّ `min` يقع **مرّةً واحدة** في ملفّ Lean، ويُبدَّل بـ`ila`. فيجب أن تُسقط
النواةُ الملفّ (`lake env lean`)، ثمّ يُعاد الملفّ بايتًا بايتًا. فالطفرةُ في CI لا «في الجلسة».

    python tools/gen_tafrat.py --check            # كلُّ الطفرات
    python tools/gen_tafrat.py --check NAME ...   # بعضُها

الرفضُ باسمه: `MUTANT_TEXT_NOT_UNIQUE`، `MUTANT_SURVIVED`، `MUTANT_FILE_NOT_RESTORED`،
`MUTANT_NAME_DUPLICATED`، `MUTANT_ROW_MALFORMED`، `MUTANT_ADR_MISSING`، `MUTANT_BASELINE_BROKEN`،
`LAKE_NOT_FOUND`، `MUTANT_TIMEOUT`. والملفُّ السليمُ يُبنى أوّلًا، فلا تُعدّ طفرةٌ مقتولةً على ملفٍّ معطوبٍ أصلًا.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
LEAN = ROOT / "formal" / "a116"
REGISTRY = ROOT / "docs" / "tafrat.json"
FIELDS = ("ism", "milaf", "adr", "min", "ila")


def load() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = json.loads(REGISTRY.read_text(encoding="utf-8"))
    return rows


def validate(rows: list[dict[str, Any]]) -> list[str]:
    """أخطاءُ السجلّ قبل التشغيل: حقولٌ ناقصة، واسمٌ مكرّر، ونصٌّ لا يقع مرّةً واحدة."""
    errs: list[str] = []
    names = [r.get("ism") for r in rows]
    for n in sorted({n for n in names if names.count(n) > 1}, key=str):
        errs.append(f"MUTANT_NAME_DUPLICATED {n}")
    for r in rows:
        if tuple(sorted(r)) != tuple(sorted(FIELDS)) or r["min"] == r["ila"]:
            errs.append(f"MUTANT_ROW_MALFORMED {r.get('ism')}")
            continue
        text = (LEAN / r["milaf"]).read_text(encoding="utf-8")
        if text.count(r["min"]) != 1:
            errs.append(f"MUTANT_TEXT_NOT_UNIQUE {r['ism']} ({text.count(r['min'])})")
        if not any((ROOT / "docs" / "adr").glob(f"{int(r['adr']):04d}-*.md")):
            errs.append(f"MUTANT_ADR_MISSING {r['ism']}")
    return errs


def lean(lake: str, milaf: str) -> int | None:
    """رمزُ خروج `lake env lean`، أو None إن جاوز المهلة (`MUTANT_TIMEOUT`)."""
    try:
        return subprocess.run([lake, "env", "lean", milaf], cwd=LEAN, capture_output=True,
                              text=True, timeout=1800).returncode
    except subprocess.TimeoutExpired:
        return None


def kills(r: dict[str, Any], lake: str) -> tuple[bool | None, bool]:
    """(قتلتها النواة، أُعيد الملفّ بعينه)؛ والأوّلُ None إن جاوز المهلة."""
    path = LEAN / r["milaf"]
    raw = path.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    try:
        path.write_bytes(raw.decode("utf-8").replace(r["min"], r["ila"], 1).encode("utf-8"))
        rc = lean(lake, r["milaf"])
        killed = None if rc is None else rc != 0
    finally:
        path.write_bytes(raw)
    return killed, hashlib.sha256(path.read_bytes()).hexdigest() == sha


def main(argv: list[str]) -> int:
    rows = load()
    errs = validate(rows)
    only = [a for a in argv if not a.startswith("--")]
    if only:
        rows = [r for r in rows if r["ism"] in only]
    lake = shutil.which("lake")
    if lake is None:
        sys.stderr.write("LAKE_NOT_FOUND\n")
        return 1
    if not errs:
        for milaf in sorted({r["milaf"] for r in rows}):
            rc = lean(lake, milaf)
            if rc is None:
                errs.append(f"MUTANT_TIMEOUT {milaf}")
            elif rc != 0:
                errs.append(f"MUTANT_BASELINE_BROKEN {milaf}")
    if not errs:
        for r in rows:
            killed, restored = kills(r, lake)
            if not restored:
                errs.append(f"MUTANT_FILE_NOT_RESTORED {r['ism']}")
            if killed is None:
                errs.append(f"MUTANT_TIMEOUT {r['ism']}")
            elif not killed:
                errs.append(f"MUTANT_SURVIVED {r['ism']}")
            hal = "جاوزت المهلة" if killed is None else ("قُتلت" if killed else "نجت")
            sys.stdout.write(f"{hal} {r['ism']} ({r['milaf']})\n")
    for e in errs:
        sys.stderr.write(e + "\n")
    if errs:
        return 1
    sys.stdout.write(f"طفراتُ Lean كلُّها مقتولة ({len(rows)})\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
