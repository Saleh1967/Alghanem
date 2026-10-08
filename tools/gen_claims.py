"""سجلُّ الأرقام (CLAIMS.md): لا رقمَ منشورًا بلا مولِّدٍ ومودَعٍ وبصمةِ مخرَج.

كلُّ أداةِ فهرسٍ في `tools/gen_*_index.py` لها `measure()` تحسب أرقامَها من المودَعات ثمّ تُنشئ
فهرسَها نثرًا. هذه الأداةُ تستدعي `measure()` نفسَها لكلّ أداة، وتكتب لكلّ رقمٍ عدديٍّ في مخرَجها
سطرًا من أربعة لا خامسَ لها: (الرقم، المولِّد، المودَعاتُ التي يقرؤها ببصماتها، بصمةُ المخرَج
كاملًا). الأرقامُ لا تُكتب باليد: ما تطبعه الآلةُ هنا هو ما يُنشر، و`--check` يعيد الحسابَ كلَّه
ويُسقط البناءَ على أيّ فرق — فالسطرُ في السجلّ شهادةُ تشغيلٍ لا دعوى.

«المراجعة» (rev): بصمةُ كلّ مودَعٍ من `manifest.DEPOSITS` (أو sha256 الملفّ حين لم يُختم بعد) وإيداعُ
الـ116 المثبَّتُ في `formal/lakefile.toml`؛ أمّا مراجعةُ هذا المستودع فهي الإيداعُ الذي يحمل هذا
الملفّ، وشاهدُها تشغيلُ CI الذي أعاد توليدَه — لا تُكتب هنا لأنّها لا تُعرف قبل الإيداع.

وبـ`--check` أيضًا: كلُّ عددٍ بفاصلة الآلاف في `CLAUDE.md` (خارج سطرٍ يحيل إلى ADR، فتلك أرقامٌ
تاريخيّة مسجَّلة بتاريخها) يجب أن يكون قيمةً في هذا السجلّ، وإلّا سقط البناءُ باسم
`NUMBER_WITHOUT_GENERATOR`.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any

from slge.manifest import DEPOSITS

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "CLAIMS.md"
TOOLS = ROOT / "tools"
DATA = ROOT / "tests" / "data"
LAKEFILE = ROOT / "formal" / "lakefile.toml"
FAN = 12  # أقصى ما يُفرد من مفاتيح؛ وما فوقه يُجمل عددًا ومجموعًا


def _canon(x: Any) -> Any:
    """صورةٌ قانونيّةٌ للمخرَج تصلح للبصمة: ترتيبُ المفاتيح، والمجموعاتُ قوائمَ مرتّبة."""

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
    """الأرقامُ العدديّة في المخرَج بمساراتها؛ الكبيرُ يُجمل: `len` (ومعه `sum` إن كانت قيمُه أعدادًا)."""

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


def deposit_shas() -> dict[str, str]:
    """بصمةُ كلّ مودَع: المختومةُ من السجلّ، وغيرُها من الملفّ كما هو على القرص."""

    out: dict[str, str] = {}
    for d in DEPOSITS:
        p = DATA / d.path
        out[d.path] = d.sha256 or (_sha(p) if p.exists() else "—")
    return out


def a116_rev() -> str:
    m = re.search(r'^rev = "([0-9a-f]+)"', LAKEFILE.read_text(encoding="utf-8"), re.M)
    return m.group(1) if m else "—"


def _reads(tool: Path) -> list[str]:
    src = tool.read_text(encoding="utf-8")
    return [d.path for d in DEPOSITS if f'"{d.path}"' in src]


def _measure(tool: Path) -> Any:
    spec = importlib.util.spec_from_file_location(tool.stem, tool)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.measure()


def ledger() -> list[dict[str, Any]]:
    """لكلّ أداةٍ: مولِّدُها، مودَعاتُها، بصمةُ مخرَجها، وأرقامُه."""

    rows: list[dict[str, Any]] = []
    for tool in sorted(TOOLS.glob("gen_*_index.py")):
        if "\ndef measure(" not in tool.read_text(encoding="utf-8"):
            continue
        out = _canon(_measure(tool))
        blob = json.dumps(out, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        nums: list[tuple[str, int | float]] = []
        _numbers(out, "", nums)
        rows.append({"generator": f"tools/{tool.name}::measure", "reads": _reads(tool),
                     "fingerprint": hashlib.sha256(blob.encode("utf-8")).hexdigest()[:16],
                     "numbers": nums})
    return rows


def _fmt(v: int | float) -> str:
    return f"{v:,}" if isinstance(v, int) else f"{v:.4f}"


def render(rows: list[dict[str, Any]]) -> str:
    shas = deposit_shas()
    lines = [
        "# سجلُّ الأرقام — لا رقمَ بلا مولِّد",
        "",
        "مولَّدٌ بـ`python tools/gen_claims.py` من `measure()` في كلّ أداةِ فهرس؛ لا يُحرَّر باليد، "
        "و`--check` يعيد الحسابَ كلَّه في CI ويُسقط البناءَ على أيّ فرق. السطرُ أربعةٌ لا خامسَ "
        "لها: الرقم، المولِّد، المودَعاتُ المقروءة (ببصمتها أدناه)، بصمةُ المخرَج كاملًا. "
        "مراجعةُ هذا المستودع هي الإيداعُ الحاملُ لهذا الملفّ وشاهدُها تشغيلُ CI؛ "
        f"وبرهانُ الـ116 مثبَّتٌ على الإيداع `{a116_rev()}` (`formal/lakefile.toml`).",
        "",
        "## المودَعات ببصماتها", "",
        "| المودَع | النوع | sha256 |", "|---|---|---|",
    ]
    for d in DEPOSITS:
        lines.append(f"| `{d.path}` | {d.kind} | `{shas[d.path]}` |")
    total = sum(len(r["numbers"]) for r in rows)
    lines += ["", f"## الأرقام ({total:,} رقمًا من {len(rows)} مولِّدًا)", ""]
    for r in rows:
        reads = "، ".join(f"`{p}`" for p in r["reads"]) or "— (جداولُ الوحدة وحدَها)"
        lines += [f"### `{r['generator']}`", "",
                  f"يقرأ: {reads}. بصمةُ المخرَج: `{r['fingerprint']}`.", "",
                  "| المسار في المخرَج | الرقم |", "|---|---|"]
        lines += [f"| `{k}` | {_fmt(v)} |" for k, v in r["numbers"]]
        lines.append("")
    return "\n".join(lines)


def _values(rows: list[dict[str, Any]]) -> set[str]:
    return {_fmt(v) for r in rows for _, v in r["numbers"] if isinstance(v, int)}


def unbacked(rows: list[dict[str, Any]]) -> list[str]:
    """أعدادُ `CLAUDE.md` بفاصلة الآلاف التي لا قيمةَ لها في السجلّ؛ أسطرُ ADR تاريخٌ مستثنًى."""

    vals = _values(rows)
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
