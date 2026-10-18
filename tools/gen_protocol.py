"""توثيقُ كلّ خطوة (الدستور م٢٠، ADR ١١١، ومصحَّحٌ في الخطوة STEP-0002).

السجلّ `docs/protocol/khutuwat.tsv`: لكلّ خطوةٍ معرِّفُها `STEP-NNNN` وتاريخُها وعنوانُها وADR الذي
يحكمها والفحوصُ التي شُغّلت قبل إيداعها: اسمٌ من القائمة المغلقة (`CHECKS`). وكلُّ إيداعٍ بعد اعتماد
البروتوكول يحمل في رسالته سطرَ «خطوة: STEP-NNNN» لخطوةٍ في السجلّ.

    python tools/gen_protocol.py --check   # السجلُّ وHEAD، أو رأسُ الفرع في pull_request
    python tools/gen_protocol.py --all     # السجلُّ وكلُّ إيداعٍ منذ الاعتماد (يلزمه التاريخ كاملًا)

**حدُّه (معلن):** يفحص أنّ الخطوة موثَّقةٌ بفحوصٍ مسمّاة، لا أنّ الفحوص شُغّلت فعلًا؛
فتشغيلُها يشهد له CI. والمفحوصُ في `pull_request` رأسُ الفرع، وفي غيره HEAD نفسُه (ودمجُ `push` يُقبل
بخطوةٍ في رسالته أو في رأس الفرع المدموج). ويفحص رأسَ الدفعة وحدَه لا ما بينه وبين الأساس؛
وذلك `--all`.
الرفضُ باسمه: `STEP_UNDOCUMENTED`، `STEP_UNKNOWN`، `STEP_ROW_MALFORMED`، `STEP_ADR_MISSING`،
`STEP_CHECK_UNKNOWN`، `STEP_ORDER_BROKEN`، `STEP_HISTORY_MISSING` (استنساخٌ ضحلٌ لا أبَ فيه ظاهرًا)،
`STEP_ADOPTION_MISSING` (`--all` ولا إيداعَ يحمل خطوةَ الاعتماد).
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOG = ROOT / "docs" / "protocol" / "khutuwat.tsv"
HEADER = ("khutwa", "tarikh", "unwan", "adr", "fuhus")
CHECKS = frozenset({
    "lake_build", "audit", "tafrat", "ruff", "mypy", "registry", "glossary", "refusals", "guard",
    "claims", "pytest_fast", "murajii", "protocol",
})


def check_known(c: str) -> bool:
    """اسمٌ من القائمة المغلقة، أو `gen:<x>` لمولِّدٍ موجود `tools/gen_<x>.py` شُغّل بـ`--check`."""
    if c in CHECKS:
        return True
    if not c.startswith("gen:") or c[4:] in CHECKS:      # لا يكرّر اسمًا من القائمة المغلقة
        return False
    tool = ROOT / "tools" / f"gen_{c[4:]}.py"
    return tool.is_file() and '"--check"' in tool.read_text(encoding="utf-8")
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
            if not check_known(c):
                errs.append(f"STEP_CHECK_UNKNOWN {k} {c}")
        rows[k] = names
    return rows, errs


def message_errors(msg: str, rows: dict[str, list[str]]) -> list[str]:
    found = STEP_RE.findall(msg)
    if not found:
        return ["STEP_UNDOCUMENTED"]
    return [f"STEP_UNKNOWN {s}" for s in found if s not in rows]


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True,
                          check=True).stdout


def checked_commit(repo: Path, event: str) -> list[str]:
    """الإيداعُ المفحوص: HEAD نفسُه، إلّا في حدث `pull_request` فإيداعُ الدمج الذي يصنعه GitHub
    ورأسُ الفرع أبوه الثاني. والاستنساخُ الضحلُ لا أبَ فيه ظاهرًا: قائمةٌ فارغة، فيُرفض باسمه."""
    head = git(repo, "rev-parse", "HEAD").strip()
    parents = git(repo, "log", "-1", "--format=%P").split()
    if git(repo, "rev-parse", "--is-shallow-repository").strip() == "true" and not parents:
        return []
    if event == "pull_request" and len(parents) == 2:
        return [parents[1]]
    return [head]


def commits_since_adoption(repo: Path) -> list[str]:
    shas = git(repo, "log", "--format=%H", "--no-merges").split()
    out: list[str] = []
    for sha in shas:
        out.append(sha)
        if f"خطوة: {ADOPTION}" in git(repo, "log", "-1", "--format=%B", sha):
            return out
    return []


def run(repo: Path, log_text: str, all_commits: bool,
        event: str = "") -> tuple[list[str], int, int]:
    rows, errs = parse(log_text)
    if all_commits:
        targets = commits_since_adoption(repo)
        if not targets:
            errs.append(f"STEP_ADOPTION_MISSING {ADOPTION}")
    else:
        targets = checked_commit(repo, event)
        if not targets:
            errs.append("STEP_HISTORY_MISSING")
    for sha in targets:
        errs += commit_errors(repo, sha, rows, merge_either=not all_commits)
    return errs, len(rows), len(targets)


def commit_errors(repo: Path, sha: str, rows: dict[str, list[str]],
                  merge_either: bool) -> list[str]:
    """أخطاءُ إيداعٍ واحد. وإيداعُ الدمج في `push` (دمجُ المالك بزرّ GitHub رسالتُه بلا خطوة) يُقبل إن
    حملت رسالتُه خطوةً أو حملها رأسُ الفرع المدموج (أبوه الثاني)."""
    errs = message_errors(git(repo, "log", "-1", "--format=%B", sha), rows)
    parents = git(repo, "log", "-1", "--format=%P", sha).split()
    if errs and merge_either and len(parents) == 2:
        alt = message_errors(git(repo, "log", "-1", "--format=%B", parents[1]), rows)
        if not alt:
            return []
    return [f"{e} {sha[:8]}" for e in errs]


def main(argv: list[str]) -> int:
    errs, nrows, ntargets = run(ROOT, LOG.read_text(encoding="utf-8"), "--all" in argv,
                                os.environ.get("GITHUB_EVENT_NAME", ""))
    for e in errs:
        sys.stderr.write(e + "\n")
    if errs:
        return 1
    sys.stdout.write(f"الخطواتُ موثَّقة ({nrows} خطوةً، {ntargets} إيداعًا)\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
