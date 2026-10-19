"""واجهةُ سطر الأوامر: `python -m canonical116 input.txt --context-json c.json --count`.

ويخرج برمز 2 إذا لم تكن النتيجةُ جاهزة؛ فالعدُّ محظورٌ في كلِّ حالٍ سواها.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .bridge import BridgeStatus, bridge, count_atoms


def _load_context(path: str | None) -> dict[str, Any]:
    if path is None:
        return {}
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise SystemExit("ملفُّ الحدود كائنٌ فيه contexts و/أو annotations.")
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="canonical116")
    parser.add_argument("input", help="مسارُ ملفِّ المصدر؛ يُقرأ بايتاتٍ لا نصًّا")
    parser.add_argument("--context-json", default=None)
    parser.add_argument("--profile", default="modern-vocalized")
    parser.add_argument("--encoding", default=None)
    parser.add_argument("--count", action="store_true")
    arguments = parser.parse_args(argv)

    payload = _load_context(arguments.context_json)
    record = bridge(
        Path(arguments.input).read_bytes(),
        encoding=arguments.encoding,
        profile=arguments.profile,
        contexts=payload.get("contexts"),
        annotations=payload.get("annotations"),
    )
    output: dict[str, Any] = {"record": record}
    if arguments.count and record["status"] == BridgeStatus.READY.value:
        output["counts"] = count_atoms(record)
    json.dump(output, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0 if record["status"] == BridgeStatus.READY.value else 2


if __name__ == "__main__":
    raise SystemExit(main())
