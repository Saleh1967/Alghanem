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

و**أعدادُ المبرهنات بوحداتها** (ADR ١٢): كلُّ مبرهنةٍ في `formal/a116/A116/*.lean` ينتهي نصُّها بـ‎= عدد‎
(عددٌ ≥ 2) تُسجَّل برقمها ووحدتها من قائمةٍ مغلقة (`UNITS`)، مدقَّقةً في `Audit.lean`. مبرهنةٌ عدديّة بلا
وحدة `CLAIM_WITHOUT_UNIT`، ووحدةٌ خارج القائمة `UNIT_NOT_IN_VOCABULARY`، ووحدةٌ لمبرهنةٍ لا توجد
`UNIT_FOR_MISSING_THEOREM`، ومبرهنةٌ عدديّة غيرُ مدقَّقة `COUNT_NOT_AUDITED`؛ والرقمُ الواحد بوحدتين
يُسمّى في السجلّ (375: متتالياتُ أصنافٍ بالوزن وسلاسلُ غلافٍ بالطول) — فلا يُقرأ رقمٌ بلا وحدته.
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
    "amr", "counts", "degrees", "degrees-pause", "hadd", "hadd-join", "hamza", "iltiqa", "ledger",
    "licensable", "need", "nizam", "numbers", "order", "neutral", "pairs", "roles", "syllables",
    "table", "utf8",
    "wazn", "wazn-body",
)
"""جداولُ Lean المسجَّلة في السجلّ بترتيب الاسم: المودَعةُ الثمانيةَ عشر (يطابقها CI بايتًا بايتًا)
والمولَّداتُ الأربع لحجمها (`syllables`، `hadd`، `hadd-join`، `iltiqa`: تُولَّد في وظيفة Lean وتُنزَّل
أثرًا إلى وظيفة البوّابة). جدولٌ جديد لا يدخل السجلَّ بوجوده على القرص بل بإضافته هنا وإلى الأثر في CI
— وإلّا اختلف السجلُّ محلّيًّا عنه في CI."""
FAN = 12  # أقصى ما يُفرد من مفاتيح؛ وما فوقه يُجمل عددًا ومجموعًا
LEAN_DIR = TABLES / "A116"
UNITS: dict[str, str] = {
    "خانة": "خانةٌ من شبكة الحوامل × الحالات",
    "حامل": "حرفٌ حاملٌ بلا حالة",
    "بايت": "بايتٌ في ترميز UTF-8",
    "سلسلة خانات مرخصة بالطول": "سلسلةُ خاناتٍ مرخَّصةٌ ثنائيًّا (‎U(n)‎) بطولها",
    "قلادة حوامل": "مدارُ سلاسل الحوامل تحت الدوران (عدُّ بيرنسايد)",
    "نمط متحرك/ساكن": "نمطُ M/S بطولٍ معيّن",
    "حالة آلة": "حالةٌ في آلة الترخيص المشبَّعة",
    "ضلع اشتقاق": "ضلعٌ بين أبواب الفعل في رسم الاشتقاق",
    "احتمال×6": "احتمالُ انتقالٍ مضروبًا في 6",
    "وزن التوزيع المستقر": "وزنٌ غيرُ مسوًّى في التوزيع المستقرّ على الأبواب",
    "قالب": "قالبُ صيغةٍ صرفيّة",
    "متتالية أصناف بالوزن": "متتاليةُ أصنافٍ (cv=2، v=c=1) بوزنها الصوتيّ",
    "سلسلة غلاف بالطول": "سلسلةُ C/V من الغلاف المقترَح بطولها",
    "دور خانة": "زوجُ (خانةٍ مرخَّصة، دورٍ تقبله: cv أو v أو c) — ADR ١٥",
    "حقل وظيفة": "حقلٌ من الوظائف السبع في صفّ درجة (ترميز … دلالة) — ADR ١٥",
    "زوج جوار": "زوجُ صنفين متجاورين (قبل، بعد) مأذونٌ وصلًا في نظام الجوار — ADR ٢٣",
}
"""القائمةُ المغلقة للوحدات: لا تُضاف وحدةٌ إلّا هنا وبـADR."""
LEAN_UNITS: dict[str, str] = {
    "Alif.alifVowelled_length": "خانة", "Alif.licensable_length": "خانة",
    "Cells.cells_length": "خانة", "Cells.cells112_length": "خانة",
    "Cells.hamzaRow_length": "خانة", "Numbering.orders_differ_only_in_two_rows": "خانة",
    "Field112.hamilField112_length": "خانة", "Field112.letters28_length": "حامل",
    "Unicode.arabic_is_two_bytes": "بايت",
    "Count.U_one": "سلسلة خانات مرخصة بالطول",
    "Junction.licensed_upto_4": "سلسلة خانات مرخصة بالطول",
    "Ladder.U3_by_pattern": "سلسلة خانات مرخصة بالطول",
    "Junction.burnside_4": "قلادة حوامل",
    "Ladder.admissible_patterns_3": "نمط متحرك/ساكن",
    "Model.saturation_rungs": "حالة آلة",
    "Derivation.edges_length": "ضلع اشتقاق", "Derivation.branching_nodes": "ضلع اشتقاق",
    "Derivation.rows_stochastic": "احتمال×6", "Derivation.w_total": "وزن التوزيع المستقر",
    "Ishtiqaq.soundTemplates_length": "قالب",
    "PauseCount.pause_count_375": "متتالية أصناف بالوزن",
    "ContinueCount.continue_count_304": "متتالية أصناف بالوزن",
    "Envelope.envelope_375": "سلسلة غلاف بالطول",
    "Envelope.envelope_licensed_75": "سلسلة غلاف بالطول",
    "Envelope.envelope_licensed_continue_59": "سلسلة غلاف بالطول",
    "Exhaust.role_count": "دور خانة", "Exhaust.current_qaim_count": "حقل وظيفة",
    "Zawaid.zawaid_length": "حامل", "Zawaid.zawaid_cells_licensable": "خانة",
    "Wazn.wasl_joined_waits": "قالب",
    "Ledger.filled_qaim_count": "حقل وظيفة",
    "Hajah.states_length": "حالة آلة",
    "Nizam.waslK_count": "زوج جوار",
}
"""كلُّ مبرهنةٍ عدديّة ووحدتُها؛ مبرهنةٌ عدديّةٌ جديدة لا تمرّ بلا سطرٍ هنا."""


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


def _hadith_tool() -> Any:
    import importlib.util

    spec = importlib.util.spec_from_file_location("gen_hadith_lines",
                                                  ROOT / "tools" / "gen_hadith_lines.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _mudari_comparison() -> Any:
    """`tests/test_mudari.py::corpus_comparison`: الأمرُ بالإزالة مقابلَ أوامر البوّابة (ADR ٢٤)."""

    import importlib.util

    path = ROOT / "tests" / "test_mudari.py"
    spec = importlib.util.spec_from_file_location("test_mudari", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.corpus_comparison()


def _neutral_comparison() -> Any:
    """`tests/test_neutral.py::corpus_comparison`: المطابَقُ بالوزن، والفجواتُ بأسمائها (ADR ١٧)."""

    import importlib.util

    path = ROOT / "tests" / "test_neutral.py"
    spec = importlib.util.spec_from_file_location("test_neutral", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    hits, misses = mod.corpus_comparison()
    gaps: dict[str, int] = {}
    for _, label, atoms, _ in misses:
        name = mod.gap_of(label, atoms)
        gaps[name] = gaps.get(name, 0) + 1
    return {"matched": sum(hits.values()), "matched_by_wazn": dict(hits), "gaps": gaps}


def generators() -> list[tuple[str, tuple[str, ...], Any]]:
    """(المولِّد، المودَعاتُ التي يقرؤها، دالّتُه) — الترتيبُ ترتيبُ السجلّ."""

    from gate import mabni_bridge
    from gate.degrees import attestation
    from gate.hamza import seat_census

    corpus, masaq = "corpora/quran-simple-enhanced.txt", "corpora/MASAQ.csv"
    hadith = tuple(f"corpora/hadith/{n}.gz" for n in _hadith_tool().HADITH_SOURCES)
    return [
        ("gate.audit.main", (corpus,), _audit),
        ("tools/gen_hadith_lines.py::stats", hadith, lambda: _hadith_tool().stats()),
        ("gate.hamza.seat_census", (corpus,), lambda: seat_census(_surfaces())),
        ("gate.degrees.attestation", (corpus,), lambda: attestation(_surfaces())),
        ("tests/test_neutral.py::corpus_comparison", (corpus,), _neutral_comparison),
        ("tests/test_mudari.py::corpus_comparison", (corpus,), _mudari_comparison),
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


_THEOREM = re.compile(r"^(?:theorem|lemma)\s+(\S+)(.*?):=", re.S | re.M)


def lean_counts() -> list[tuple[str, int]]:
    """(الوحدةُ.المبرهنة، عددُها) لكلّ مبرهنةٍ ينتهي نصُّها بـ‎= عدد ≥ 2‎، بترتيب الملفّ ثمّ الموضع."""

    out = []
    for f in sorted(LEAN_DIR.glob("*.lean")):
        for m in _THEOREM.finditer(f.read_text(encoding="utf-8")):
            tail = re.search(r"=\s*(\d+)\s*$", " ".join(m.group(2).split()))
            if tail and int(tail.group(1)) >= 2:
                out.append((f"{f.stem}.{m.group(1)}", int(tail.group(1))))
    return out


def unit_breaches(counts: list[tuple[str, int]]) -> list[str]:
    audit = (TABLES / "Audit.lean").read_text(encoding="utf-8")
    names = {n for n, _ in counts}
    out = [f"{n} — CLAIM_WITHOUT_UNIT" for n in sorted(names - set(LEAN_UNITS))]
    out += [f"{n} — UNIT_FOR_MISSING_THEOREM" for n in sorted(set(LEAN_UNITS) - names)]
    out += [f"{n}: {u} — UNIT_NOT_IN_VOCABULARY" for n, u in LEAN_UNITS.items() if u not in UNITS]
    out += [f"{n} — COUNT_NOT_AUDITED" for n in sorted(names)
            if not re.search(rf"#print axioms A116\.(?:\w+\.)*{re.escape(n.split('.')[1])}\s*$",
                             audit, re.M)]
    return out


def render_units(counts: list[tuple[str, int]]) -> list[str]:
    lines = ["", f"## أعدادُ المبرهنات بوحداتها ({len(counts)} مبرهنة)", "",
             "مستخرَجةٌ من نصوص Lean (`formal/a116/A116/*.lean`): كلُّ مبرهنةٍ مدقَّقة ينتهي نصُّها "
             "بـ‎= عدد‎؛ والوحدةُ من القائمة المغلقة أدناه (ADR ١٢). العددُ هو الثابتُ الأخير في نصّ "
             "المبرهنة.", "",
             "| الرقم | الوحدة | المبرهنة |", "|---|---|---|"]
    lines += [f"| {v:,} | {LEAN_UNITS.get(n, '—')} | `A116.{n}` |" for n, v in counts]
    by_value: dict[int, set[str]] = {}
    for n, v in counts:
        by_value.setdefault(v, set()).add(LEAN_UNITS.get(n, "—"))
    clash = sorted((v, us) for v, us in by_value.items() if len(us) > 1)
    lines += ["", "### رقمٌ واحدٌ بوحداتٍ مختلفة — لا يُقرأ بلا وحدته", ""]
    lines += [f"- {v:,}: " + "؛ ".join(sorted(us)) for v, us in clash] or ["- لا شيء"]
    lines += ["", "### القائمةُ المغلقة للوحدات", "", "| الوحدة | معناها |", "|---|---|"]
    lines += [f"| {u} | {d} |" for u, d in UNITS.items()]
    return lines


def _fmt(v: int | float) -> str:
    return f"{v:,}" if isinstance(v, int) else f"{v:.4f}"


def render(rows: list[dict[str, Any]]) -> str:
    from gate.api import ABNIYA_INTIQA_SHA256, CORPUS_SHA256

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
        *(f"| `corpora/hadith/{n}.gz` | واقع مختوم (ODbL 1.0؛ بايتاتُه بعد فكّ الضغط) | `{sha}` |"
          for n, sha in _hadith_tool().HADITH_SOURCES.items()),
        "| `corpora/abniya-intiqa-lines.txt` | مجالٌ مختومٌ ثالث: انتقاءُ الأبنية بيد المالك "
        f"(`ABNIYA_INTIQA_SHA256`، ADR ١٣) | `{ABNIYA_INTIQA_SHA256}` |",
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
    lines += render_units(lean_counts())
    lines.append("")
    return "\n".join(lines)


def unbacked(rows: list[dict[str, Any]]) -> list[str]:
    vals = {_fmt(v) for r in rows for _, v in r["numbers"] if isinstance(v, int)}
    vals |= {_fmt(v) for _, v in lean_counts()}
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
        for p in unbacked(rows) + unit_breaches(lean_counts()):
            sys.stderr.write(p + "\n")
            rc = 1
        sys.stdout.write("CLAIMS.md مطابق\n" if rc == 0 else "")
        return rc
    TARGET.write_text(text, encoding="utf-8")
    sys.stdout.write(f"كُتب CLAIMS.md ({sum(len(r['numbers']) for r in rows):,} رقمًا)\n")
    for p in unbacked(rows) + unit_breaches(lean_counts()):
        sys.stdout.write(p + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
