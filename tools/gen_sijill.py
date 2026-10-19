"""سجلُّ التراخيص محسوبًا لا مكتوبًا (ADR ٢٩): الحالةُ دليلٌ
بمحتوى الملفّ، والترخيصُ `A116.Exhaust.Murakhkhas`.

المودَعات:

* `docs/sijill/ledger.json` — «الشجرة المرخَّصة — سجلّ التراخيص»
كما أرفقه المالك، بلا تحرير (`LEDGER_SHA256`).
* `docs/sijill/evidence.tsv` — صفٌّ لكلّ مدخلٍ بترتيبه: بصمتُه،
ومن أين قُرئ (مستودعٌ ونقطةُ git)، وصنفُ محتواه
  بقواعد `content_kind` (على البايتات لا على الاسم)، ودليلُه
  (`burhan:N` أو `muallaq:<سبب>`)، ووظيفتُه.
  يُبنى بـ`--build --repos DIR…` من نُسَخ git الكاملة (كلُّ blob
  في التاريخ يُبصَم بـsha256)؛ ولا يُبنى في CI.
* `formal/a116/A116/SijillData.lean` — يُولَّد من المودَعين، و`--check` يطابقه بايتًا بايتًا ويطابق
  الصفوفَ بالسجلّ (المعرّف، الدرجة، البصمة، المرخِّص) ويطابق بصمةَ السجلّ.

الدليلُ: ما لم يُقرأ بايتُه `muallaq:NOT_FOUND_BY_HASH`، والنصُّ والبياناتُ والشيفرةُ والاختبارُ غيرُ المشغَّل
معلَّقةٌ بأسمائها؛ و`burhan:N` لوحدة Lean بُنيت وطُبعت مسلّماتُ مبرهناتها في جلسة ADR ٢٩ (`BUILT`، معلن:
بناءٌ في الجلسة، أوامرُه في الـADR). والوظيفةُ تُسند لما دليلُه قائمٌ وحده (`ASSIGN`، معلن)، إذ لا تغيّر
الوظيفةُ خانةً دليلُها معلَّق. الأداةُ معفاةٌ في الحارس لأنّها أداةُ إيداع.
"""

from __future__ import annotations

import ast
import csv
import hashlib
import io
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "docs" / "sijill" / "ledger.json"
EVIDENCE = ROOT / "docs" / "sijill" / "evidence.tsv"
LEAN = ROOT / "formal" / "a116" / "A116" / "SijillData.lean"
LEDGER_SHA256 = "436b8adfd50aec4c05b99791c14ec90e27b92ed7623380f46dbc48d816d11cc1"
FIELDS = ("id", "degree", "sha256", "licensed_by", "source", "kind", "daleel", "wazifa")
WAZAIF = ("tarmiz", "imla", "sawt", "ishtiqaq", "sarf", "nahw", "dalala")
"""بترتيب `A116.Exhaust.Wazifa`."""

BUILT: dict[str, tuple[str, int]] = {
    "f1021": ("Slge.Bridge", 8), "f1022": ("Slge.Categories", 3),
    "f1023": ("Slge.Consistency", 3), "f1024": ("Slge.Ghazali", 4),
    "f1025": ("Slge.Rank", 11), "f1026": ("Slge.Rasm", 3), "f1027": ("Slge.Sequence", 6),
}
"""وحداتُ Lean التي بُنيت في الجلسة على A116 بلا خطأ ولا
تحذير، وعددُ مبرهناتها في `Audit.lean` الخاصّ بها
(مسلّماتُها propext/Classical.choice/Quot.sound فحسب). معلن: البناءُ خارج CI."""
FAILED: dict[str, str] = {"f0051": "LEAN_BUILD_FAILED"}
"""بُني على Mathlib المحلّي فخطآن، و7 مبرهناتٍ على `sorryAx`؛ ومستودعُه لا يعلن إصدارَ Mathlib."""
ASSIGN: dict[str, str] = {
    "f1021": "tarmiz", "f1023": "tarmiz", "f1027": "tarmiz", "f1026": "imla", "f1022": "nahw",
}
"""الوظيفةُ من موضوع الوحدة كما تعلنه هي في رأسها (معلن):
الجسرُ والاتّساقُ والتسلسلُ ترميز، والرسمُ إملاء،
والضمائرُ نحو؛ والغزاليُّ والرتبةُ منطقٌ وحكمٌ فوق الترخيص لا من الوظائف السبع (`-`)."""


def content_kind(b: bytes) -> str:
    """صنفُ المحتوى بقواعدَ مرتّبة على البايتات؛ لا ينظر في الاسم ولا في الامتداد."""

    if b[:2] == b"\x1f\x8b":
        return "GZIP"
    if b[:4] == b"PK\x03\x04":
        return "ZIP"
    if b[:8] == b"\x89PNG\r\n\x1a\n":
        return "PNG"
    if b.startswith((b"# v2 git bundle", b"# v3 git bundle")):
        return "GIT_BUNDLE"
    try:
        t = b.decode("utf-8")
    except UnicodeDecodeError:
        return "BINARY"
    if not t.strip():
        return "EMPTY"
    try:
        json.loads(t)
        return "JSON"
    except ValueError:
        pass
    ls = [ln for ln in t.splitlines() if ln.strip()]
    if all(ln.lstrip().startswith("{") for ln in ls):
        try:
            for ln in ls:
                json.loads(ln)
            return "JSONL"
        except ValueError:
            pass
    if all(re.fullmatch(r"import\s+[\w.]+\s*", ln) for ln in ls):
        return "IMPORTS_ONLY"  # نحوُ Lean ونحوُ Python سواء: لا يفصل المحتوى بينهما
    has_thm = re.search(r"^\s*(theorem|lemma)\s", t, re.M)
    has_head = re.search(r"^(import|namespace|open)\s", t, re.M)
    if has_thm and has_head and ":=" in t:
        return "LEAN"
    if re.search(r"^jobs:", t, re.M) and "runs-on" in t:
        return "CI"
    if re.match(r"#!.*\b(ba)?sh\b", t):
        return "SHELL"
    try:
        tree = ast.parse(t)
    except (SyntaxError, ValueError):
        tree = None
    stmt = ast.FunctionDef | ast.Import | ast.ImportFrom | ast.ClassDef | ast.Assign
    if tree is not None and any(isinstance(n, stmt) for n in ast.walk(tree)):
        tests = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
        if any(n.name.startswith("test_") for n in tests):
            return "PY_TEST"
        return "PY"
    for d in (",", "\t"):
        counts = {ln.count(d) for ln in ls[:200]}
        if len(ls) >= 3 and len(counts) == 1 and counts.pop() > 0:
            return "TABLE"
    return "TEXT"


REASON = {
    "TEXT": "NASS", "EMPTY": "NASS",
    "JSON": "DATA_WITHOUT_MEASURE", "JSONL": "DATA_WITHOUT_MEASURE",
    "TABLE": "DATA_WITHOUT_MEASURE",
    "PY": "CODE_NOT_RUN", "SHELL": "CODE_NOT_RUN", "CI": "CODE_NOT_RUN",
    "PY_TEST": "TEST_NOT_RUN", "LEAN": "LEAN_NOT_BUILT", "IMPORTS_ONLY": "NO_THEOREMS",
    "ZIP": "ARCHIVE", "GZIP": "ARCHIVE", "GIT_BUNDLE": "ARCHIVE", "PNG": "ARCHIVE",
    "BINARY": "ARCHIVE",
}


def daleel(eid: str, kind: str) -> str:
    if eid in BUILT:
        return f"burhan:{BUILT[eid][1]}"
    if eid in FAILED:
        return f"muallaq:{FAILED[eid]}"
    if kind == "UNREAD":
        return "muallaq:NOT_FOUND_BY_HASH"
    return f"muallaq:{REASON[kind]}"


def ledger() -> dict:
    return json.loads(LEDGER.read_text(encoding="utf-8"))


def _cat(repo: str, b: str) -> bytes:
    return subprocess.run(["git", "-C", repo, "cat-file", "blob", b], capture_output=True,
                          check=True).stdout


def blob_index(repos: list[str]) -> dict[str, tuple[str, str]]:
    """sha256 ← (المستودع، blob) لكلّ blob في كلّ تاريخ git المعطى."""

    out: dict[str, tuple[str, str]] = {}
    for repo in repos:
        lines = subprocess.run(["git", "-C", repo, "cat-file", "--batch-all-objects",
                                "--batch-check=%(objectname) %(objecttype)"],
                               capture_output=True, text=True, check=True).stdout.split()
        blobs = [lines[i] for i in range(0, len(lines), 2) if lines[i + 1] == "blob"]
        for b in blobs:
            out.setdefault(hashlib.sha256(_cat(repo, b)).hexdigest(), (repo, b))
    return out


def build(repos: list[str]) -> list[dict[str, str]]:
    idx = blob_index(repos)
    rows = []
    for e in ledger()["entries"]:
        hit = idx.get(e["sha256"])
        kind = content_kind(_cat(*hit)) if hit else "UNREAD"
        rows.append({"id": e["id"], "degree": e["degree"], "sha256": e["sha256"],
                     "licensed_by": e["licensed_by"] or "-",
                     "source": f"{Path(hit[0]).name.removesuffix('.git')}@{hit[1]}" if hit else "-",
                     "kind": kind,
                     "daleel": daleel(e["id"], kind), "wazifa": ASSIGN.get(e["id"], "-")})
    return rows


def render_tsv(rows: list[dict[str, str]]) -> str:
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=FIELDS, delimiter="\t", lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    return buf.getvalue()


def read_tsv() -> list[dict[str, str]]:
    with EVIDENCE.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def render_lean(led: dict, rows: list[dict[str, str]]) -> str:
    deg = {g["key"]: g["num"] for g in led["degrees"]}
    pos = {r["id"]: i for i, r in enumerate(rows)}
    items = []
    for r in rows:
        lvl = int(r["daleel"].split(":")[1]) if r["daleel"].startswith("burhan:") else 0
        w = f"some .{r['wazifa']}" if r["wazifa"] != "-" else "none"
        p = f"some {pos[r['licensed_by']]}" if r["licensed_by"] != "-" else "none"
        items.append(f"  ⟨{deg[r['degree']]}, {lvl}, {w}, {p}⟩")
    return (
        "import A116.Exhaust\n\n"
        "/-! مولَّدٌ بـ`tools/gen_sijill.py` من `docs/sijill/ledger.json` (sha256 "
        f"{LEDGER_SHA256}) و`docs/sijill/evidence.tsv`؛ لا يُحرَّر باليد (ADR ٢٩).\n\n"
        "صفٌّ لكلّ مدخلٍ بترتيب السجلّ: الدرجة، وعددُ المبرهنات المدقَّقة (0 = معلَّق)، "
        "والوظيفة، وفهرسُ المرخِّص. -/\n\n"
        "namespace A116.SijillData\n\n"
        "structure Row where\n  daraja : Nat\n  audited : Nat\n"
        "  wazifa : Option A116.Exhaust.Wazifa\n"
        "  licensedBy : Option Nat\n  deriving DecidableEq, Repr\n\n"
        "open A116.Exhaust in\n"
        "def rows : List Row := [\n" + ",\n".join(items) + "]\n\nend A116.SijillData\n"
    )


def check() -> list[str]:
    out = []
    raw = LEDGER.read_bytes()
    if hashlib.sha256(raw).hexdigest() != LEDGER_SHA256:
        out.append("LEDGER_DRIFTED: بصمةُ السجلّ المودَع تغيّرت")
    led = ledger()
    rows = read_tsv()
    ents = led["entries"]
    if [(r["id"], r["degree"], r["sha256"], r["licensed_by"]) for r in rows] != [
            (e["id"], e["degree"], e["sha256"], e["licensed_by"] or "-") for e in ents]:
        out.append("EVIDENCE_ROWS_DRIFTED: صفوفُ الدليل لا تطابق مدخلاتِ السجلّ بترتيبها")
    for r in rows:
        if r["daleel"] != daleel(r["id"], r["kind"]):
            out.append(f"DALEEL_NOT_DERIVED: {r['id']}")
        if r["wazifa"] != ASSIGN.get(r["id"], "-"):
            out.append(f"WAZIFA_NOT_DECLARED: {r['id']}")
        if (r["kind"] == "UNREAD") != (r["source"] == "-"):
            out.append(f"SOURCE_KIND_MISMATCH: {r['id']}")
    if LEAN.read_text(encoding="utf-8") != render_lean(led, rows):
        out.append("LEAN_DATA_DRIFTED: SijillData.lean ليس ما يولّده المودَعان")
    return out


def main(argv: list[str]) -> int:
    if "--check" in argv:
        bad = check()
        for b in bad:
            sys.stderr.write(b + "\n")
        if not bad:
            rows = read_tsv()
            read = sum(1 for r in rows if r["kind"] != "UNREAD")
            sys.stdout.write(f"سجلُّ التراخيص مطابق: {len(rows)} مدخلًا، المقروءُ بالبصمة {read}\n")
        return 1 if bad else 0
    if "--build" in argv:
        repos = argv[argv.index("--repos") + 1:]
        EVIDENCE.write_text(render_tsv(build(repos)), encoding="utf-8")
    LEAN.write_text(render_lean(ledger(), read_tsv()), encoding="utf-8")
    sys.stdout.write(f"كُتب {LEAN.name}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
