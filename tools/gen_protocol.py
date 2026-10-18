"""توثيقُ كلّ خطوة (الدستور م٢٠، ADR ١١١).

السجلّ `docs/protocol/khutuwat.tsv`: لكلّ خطوةٍ معرِّفُها `STEP-NNNN` وتاريخُها وعنوانُها وADR الذي
يحكمها والفحوصُ التي شُغّلت قبل إيداعها من قائمةٍ مغلقة (`CHECKS`). وكلُّ إيداعٍ بعد اعتماد
البروتوكول يحمل في رسالته سطرَ «خطوة: STEP-NNNN» لخطوةٍ في السجلّ.

    python tools/gen_protocol.py --check   # السجلُّ وإيداعُ HEAD
    python tools/gen_protocol.py --all     # السجلُّ وكلُّ إيداعٍ منذ الاعتماد (يلزمه التاريخ كاملًا)

**حدُّه (معلن):** يفحص أنّ الخطوة موثَّقةٌ بفحوصٍ مسمّاة، لا أنّ الفحوص شُغّلت فعلًا؛
فتشغيلُها يشهد له CI.
الرفضُ باسمه: `STEP_UNDOCUMENTED`، `STEP_UNKNOWN`، `STEP_ROW_MALFORMED`، `STEP_ADR_MISSING`،
`STEP_CHECK_UNKNOWN`، `STEP_ORDER_BROKEN`.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOG = ROOT / "docs" / "protocol" / "khutuwat.tsv"
HEADER = ("khutwa", "tarikh", "unwan", "adr", "fuhus")
CHECKS = frozenset({
    "lake_build", "audit", "tafrat", "ruff", "mypy", "registry", "glossary", "refusals", "guard",
    "claims", "pytest_fast", "gen_check", "murajii", "protocol",
})
STEP_RE = re.compile(r"^خطوة: (STEP-\d{4})$", re.M)
ADOPTION = "STEP-0001"


def parse(text: str) -> tuple[dict[str, list[str]], list[str]]:
    rows: dict[str, list[str]] = {}
    errs: list[str] = []
    lines = text.splitlines()
    if not lines or tuple(lines[0].split("\t")) != HEADER:
        return rows, ["STEP_ROW_MALFORMED header"]
    prev = 0
    for ln in lines[1:]:
        cols = ln.split("\t")
        if len(cols) != len(HEADER) or not re.fullmatch(r"STEP-\d{4}", cols[0]):
            errs.append(f"STEP_ROW_MALFORMED {ln[:40]}")
            continue
        k, _date, _title, adr, checks = cols
        num = int(k[5:])
        if num != prev + 1:
            errs.append(f"STEP_ORDER_BROKEN {k}")
        prev = num
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", cols[1]):
            errs.append(f"STEP_ROW_MALFORMED {k} date")
        if not adr.isdigit() or not any((ROOT / "docs" / "adr").glob(f"{int(adr):04d}-*.md")):
            errs.append(f"STEP_ADR_MISSING {k} {adr}")
        names = checks.split(";")
        for c in names:
            if c not in CHECKS:
                errs.append(f"STEP_CHECK_UNKNOWN {k} {c}")
        rows[k] = names
    return rows, errs


def message_errors(msg: str, rows: dict[str, list[str]]) -> list[str]:
    found = STEP_RE.findall(msg)
    if not found:
        return ["STEP_UNDOCUMENTED"]
    return [f"STEP_UNKNOWN {s}" for s in found if s not in rows]


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True,
                          check=True).stdout


def commits_since_adoption() -> list[str]:
    shas = git("log", "--format=%H", "--no-merges").split()
    out: list[str] = []
    for sha in shas:
        out.append(sha)
        if f"خطوة: {ADOPTION}" in git("log", "-1", "--format=%B", sha):
            return out
    return []


def main(argv: list[str]) -> int:
    rows, errs = parse(LOG.read_text(encoding="utf-8"))
    targets: list[str] = []
    if "--all" in argv:
        targets = commits_since_adoption()
        if not targets:
            errs.append(f"STEP_UNDOCUMENTED no commit carries {ADOPTION}")
    elif len(git("log", "-1", "--format=%P").split()) == 1:
        targets = ["HEAD"]
    for sha in targets:
        msg = git("log", "-1", "--format=%B", sha)
        errs += [f"{e} {sha[:8]}" for e in message_errors(msg, rows)]
    for e in errs:
        sys.stderr.write(e + "\n")
    if errs:
        return 1
    sys.stdout.write(f"الخطواتُ موثَّقة ({len(rows)} خطوةً، {len(targets)} إيداعًا)\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
