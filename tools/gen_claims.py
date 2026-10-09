"""سجلُّ الأرقام (CLAIMS.md): لا رقمَ منشورًا بلا مولِّدٍ ومودَعٍ وبصمةِ مخرَج.

كلُّ رقمٍ يُنشر عن البوّابة له مولِّدٌ مسمًّى في الشجرة: `gate.audit.main` على المدوّنة المختومة،
قراءاتُ `gate.mabni_bridge` على المرجع المحجوب (MASAQ)، `gate.hamza.seat_census` على الرسوم المختومة،
وجداولُ Lean المولَّدة (`formal/a116/*.csv`). هذه الأداةُ تستدعي كلَّ مولِّدٍ وتكتب لكلّ رقمٍ عدديٍّ
في مخرَجه سطرًا من أربعة لا خامسَ لها: (الرقم، المولِّد، المودَعاتُ التي يقرؤها ببصماتها، بصمةُ المخرَج
كاملًا). الأرقامُ لا تُكتب باليد؛ `--check` يعيد الحسابَ كلَّه ويُسقط البناءَ على أيّ فرق.

«المراجعة» (rev): بصماتُ المودَعات (المدوّنةُ المختومة `CORPUS_SHA256`، والمرجعُ المحجوب، وجداولُ
Lean كما هي على القرص)؛ أمّا مراجعةُ هذا المستودع فهي الإيداعُ الحاملُ لهذا الملفّ وشاهدُها تشغيلُ CI.

وبـ`--check` أيضًا: كلُّ عددٍ بفاصلة الآلاف في `CLAUDE.md` (خارج سطرٍ يحيل إلى ADR) يجب أن يكون قيمةً
في هذا السجلّ، وإلّا سقط البناءُ باسم `NUMBER_WITHOUT_GENERATOR`.
"""

from __future__ import annotations

import contextlib
import hashlib
import io
import json
import re
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "CLAIMS.md"
CORPUS = ROOT / "corpora" / "quran-simple-enhanced.txt"
MASAQ = ROOT / "corpora" / "MASAQ.csv"
TABLES = ROOT / "formal" / "a116"
TABLE_NAMES = (
    "counts", "hadd", "hadd-join", "hamza", "iltiqa", "licensable", "numbers", "order", "pairs",
    "syllables", "table", "utf8",
)
"""جداولُ Lean المسجَّلة في السجلّ بترتيب الاسم: المودَعةُ الثمانية (يطابقها CI بايتًا بايتًا)
والمولَّداتُ الأربع لحجمها (`syllables`، `hadd`، `hadd-join`، `iltiqa`: تُولَّد في وظيفة Lean وتُنزَّل
أثرًا إلى وظيفة البوّابة). جدولٌ جديد لا يدخل السجلَّ بوجوده على القرص بل بإضافته هنا وإلى الأثر في CI
— وإلّا اختلف السجلُّ محلّيًّا عنه في CI."""
FAN = 12  # أقصى ما يُفرد من مفاتيح؛ وما فوقه يُجمل عددًا ومجموعًا


def _canon(x: Any) -> Any:
    if isinstance(x, bool | int | float | str) or x is None:
        return x
    if isinstance(x, dict):
        return {str(k): _canon(v) for k, v in sorted(x.items(), key=lambda kv: str(kv[0]))}
    if isinstance(x, list | tuple):
        return [_canon(v) for v in x]
    if isinstance(x, set | frozenset):
        return sorted((_canon(v) for v in x), key=lambda v: json.dumps(v, ensure_ascii=False))
    return repr(x)


def _numbers(x: Any, path: str, out: list[tuple[str, int | float]]) -> None:
    if isinstance(x, bool):
        out.append((path, int(x)))
    elif isinstance(x, int | float):
        out.append((path, x))
    elif isinstance(x, dict):
        if len(x) <= FAN or not path:  # الجذرُ يُفرد كلُّه؛ والتفريعُ تحته بحدّ FAN
            for k, v in x.items():
                _numbers(v, f"{path}.{k}" if path else str(k), out)
        else:
            out.append((f"{path}.len", len(x)))
            if all(isinstance(v, int | float) and not isinstance(v, bool) for v in x.values()):
                out.append((f"{path}.sum", sum(x.values())))
    elif isinstance(x, list | tuple | set | frozenset):
        if isinstance(x, set | frozenset) or len(x) > FAN:
            out.append((f"{path}.len", len(x)))
        else:
            for i, v in enumerate(x):
                _numbers(v, f"{path}[{i}]", out)


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _surfaces() -> list[str]:
    text = CORPUS.read_text(encoding="utf-8")
    return sorted({w for w in text.split() if w != "<sel>" and any("ء" <= c <= "ي" for c in w)})


def _audit() -> Any:
    from gate import audit

    with tempfile.TemporaryDirectory() as out, contextlib.redirect_stdout(io.StringIO()):
        audit.main(str(CORPUS), out)
    return json.loads((ROOT / "gate" / "audit_results.json").read_text(encoding="utf-8"))


def generators() -> list[tuple[str, tuple[str, ...], Any]]:
    """(المولِّد، المودَعاتُ التي يقرؤها، دالّتُه) — الترتيبُ ترتيبُ السجلّ."""

    from gate import mabni_bridge
    from gate.hamza import seat_census

    corpus, masaq = "corpora/quran-simple-enhanced.txt", "corpora/MASAQ.csv"
    return [
        ("gate.audit.main", (corpus,), _audit),
        ("gate.hamza.seat_census", (corpus,), lambda: seat_census(_surfaces())),
        ("gate.mabni_bridge.verb_readings", (masaq,), mabni_bridge.verb_readings),
        ("gate.mabni_bridge.verb_generation_reading", (masaq,),
         mabni_bridge.verb_generation_reading),
        ("gate.mabni_bridge.lexical_generation_reading", (masaq,),
         mabni_bridge.lexical_generation_reading),
        ("gate.mabni_bridge.lexical_recognition_reading", (masaq,),
         mabni_bridge.lexical_recognition_reading),
    ]


def ledger() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for name, reads, fn in generators():
        out = _canon(fn())
        blob = json.dumps(out, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        nums: list[tuple[str, int | float]] = []
        _numbers(out, "", nums)
        rows.append({"generator": name, "reads": list(reads),
                     "fingerprint": hashlib.sha256(blob.encode("utf-8")).hexdigest()[:16],
                     "numbers": nums})
    for name in TABLE_NAMES:
        csv = TABLES / f"{name}.csv"
        if not csv.exists():
            raise FileNotFoundError(
                f"{csv.name}: جدولُ Lean غيرُ مولَّد — شغّل lake exe a116-table {name}")
        n = sum(1 for _ in csv.open(encoding="utf-8"))
        rows.append({"generator": f"lake exe a116-table {csv.stem}", "reads": [],
                     "fingerprint": _sha(csv)[:16], "numbers": [(f"{csv.name}.rows", n)]})
    return rows


def _fmt(v: int | float) -> str:
    return f"{v:,}" if isinstance(v, int) else f"{v:.4f}"


def render(rows: list[dict[str, Any]]) -> str:
    from gate.api import CORPUS_SHA256

    lines = [
        "# سجلُّ الأرقام — لا رقمَ بلا مولِّد",
        "",
        "مولَّدٌ بـ`python tools/gen_claims.py` باستدعاء كلّ مولِّدٍ مسمًّى في الشجرة؛ لا يُحرَّر "
        "باليد، و`--check` يعيد الحسابَ كلَّه في CI ويُسقط البناءَ على أيّ فرق. السطرُ أربعةٌ لا "
        "خامسَ لها: الرقم، المولِّد، المودَعاتُ المقروءة (ببصمتها أدناه)، بصمةُ المخرَج كاملًا. "
        "مراجعةُ هذا المستودع هي الإيداعُ الحاملُ لهذا الملفّ وشاهدُها تشغيلُ CI. جداولُ Lean "
        "يولّدها `lake exe a116-table` في CI وتُطابَق بايتًا بايتًا بالإيداع المسجَّل هنا.",
        "",
        "## المودَعات ببصماتها", "",
        "| المودَع | النوع | sha256 |", "|---|---|---|",
        "| `corpora/quran-simple-enhanced.txt` | واقع مختوم (`CORPUS_SHA256`) | "
        f"`{CORPUS_SHA256}` |",
        f"| `corpora/MASAQ.csv` | مرجع محجوب | `{_sha(MASAQ)}` |",
    ]
    total = sum(len(r["numbers"]) for r in rows)
    lines += ["", f"## الأرقام ({total:,} رقمًا من {len(rows)} مولِّدًا)", ""]
    for r in rows:
        reads = "، ".join(f"`{p}`" for p in r["reads"]) or "— (نواةُ Lean؛ لا مودَع)"
        lines += [f"### `{r['generator']}`", "",
                  f"يقرأ: {reads}. بصمةُ المخرَج: `{r['fingerprint']}`.", "",
                  "| المسار في المخرَج | الرقم |", "|---|---|"]
        lines += [f"| `{k}` | {_fmt(v)} |" for k, v in r["numbers"]]
        lines.append("")
    return "\n".join(lines)


def unbacked(rows: list[dict[str, Any]]) -> list[str]:
    vals = {_fmt(v) for r in rows for _, v in r["numbers"] if isinstance(v, int)}
    out: list[str] = []
    for i, line in enumerate((ROOT / "CLAUDE.md").read_text(encoding="utf-8").splitlines(), 1):
        if "ADR" in line:
            continue
        for n in re.findall(r"\d{1,3}(?:,\d{3})+", line):
            if n not in vals:
                out.append(f"CLAUDE.md:{i}: {n} — NUMBER_WITHOUT_GENERATOR")
    return out


def main() -> int:
    rows = ledger()
    text = render(rows)
    if "--check" in sys.argv:
        rc = 0
        if TARGET.read_text(encoding="utf-8") != text:
            sys.stderr.write("CLAIMS.md غيرُ مطابق؛ شغّل tools/gen_claims.py\n")
            rc = 1
        for p in unbacked(rows):
            sys.stderr.write(p + "\n")
            rc = 1
        sys.stdout.write("CLAIMS.md مطابق\n" if rc == 0 else "")
        return rc
    TARGET.write_text(text, encoding="utf-8")
    sys.stdout.write(f"كُتب CLAIMS.md ({sum(len(r['numbers']) for r in rows):,} رقمًا)\n")
    for p in unbacked(rows):
        sys.stdout.write(p + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
