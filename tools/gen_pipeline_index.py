"""فهرسُ السُّلَّم رقمًا واحدًا (PIPELINE_INDEX.md): كم كلمةً من MASAQ تعبر المراحلَ كلَّها — الشهادة،
الجذعُ قراءةً واحدةً صحيحة، الجهة، الحالة، النسبة — بقراءةٍ واحدةٍ توافق المرجعَ المحجوب في كلّ مرحلة.

القياسُ على `masaq-shibh.json.gz` (40,731 كلمةً بشهادات البوّابة) و`corpus-certificates.json.gz`.
القمعُ: العابرون بعد كلّ مرحلة (`funnel`)، والتوقّفُ باسمه (`stops`)، مرّتين: الصارمُ (قسمةٌ واحدة محسومة
بـ`hasm`) والمرتَّب (الأولى بعد الترتيب هي الذهبيّة). يكتب أيضًا `formal/Slge/PipelineTable.lean` و
`src/slge/pipeline_table.py` (القمعان أعدادًا) ويفحصهما بـ`--check`؛ Lean يثبت أنّهما متناقصان.
"""

from __future__ import annotations

import gzip
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from slge.pipeline import GOLD_CASE, GOLD_JIHA, GOLD_NISBA, STAGES, STOPS, Gold, run, stages_passed

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "PIPELINE_INDEX.md"
LEAN = ROOT / "formal" / "Slge" / "PipelineTable.lean"
PY = ROOT / "src" / "slge" / "pipeline_table.py"
DATA = ROOT / "tests" / "data"
Word = tuple[tuple[str, str], ...]
PRE_IN_STEM = ("IMPERF_PREF", "CV_PREF", "IV1S", "IV1P", "IV2MP", "IV3MS", "IV3MP", "IV3FS")
"""سوابقُ MASAQ التي تُعدّ من الجذع (كما في فهرس الجذع)."""


def corpus_forms() -> set[Word]:
    with gzip.open(DATA / "corpus-certificates.json.gz", "rt", encoding="utf-8") as f:
        d: dict[str, Any] = json.load(f)
    return {tuple((a, b) for a, b in x["cells"]) for x in d["forms"]}


def masaq_rows() -> list[dict[str, Any]]:
    with gzip.open(DATA / "masaq-shibh.json.gz", "rt", encoding="utf-8") as f:
        rows: list[dict[str, Any]] = json.load(f)["rows"]
    return rows


def whole(r: dict[str, Any]) -> Word:
    return (*((a, b) for _, cs in r["pre"] for a, b in cs), *((a, b) for a, b in r["stem"]),
            *((a, b) for _, cs in r["suf"] for a, b in cs))


def stem_with_al(r: dict[str, Any]) -> Word:
    return (*((a, b) for t, cs in r["pre"] for a, b in cs if t == "DET"),
            *((a, b) for a, b in r["stem"]))


def gold_of(r: dict[str, Any]) -> Gold:
    pre = tuple((a, b) for t, cs in r["pre"] for a, b in cs if t not in PRE_IN_STEM and t != "DET")
    return Gold(pre=pre, det=any(t == "DET" for t, _ in r["pre"]),
                suf=tuple((a, b) for _, cs in r["suf"] for a, b in cs),
                tag=str(r["tag"]), case=str(r["case"]), role=str(r["role"]))


def measure() -> dict[str, Any]:
    forms = corpus_forms()
    rows = masaq_rows()
    idx = {(r["ref"], r["pos"]): r for r in rows}
    def asked(r: dict[str, Any]) -> bool:
        """هل يسأل المرجعُ هذه الكلمةَ عن المراحل الخمس كلِّها؟"""

        return (r["tag"] in GOLD_JIHA and r["case"] in GOLD_CASE and r["role"] in GOLD_NISBA
                and (r["ref"], r["pos"] - 1) in idx)

    out: dict[str, Any] = {"masaq": len(rows), "stages": list(STAGES),
                           "content": sum(1 for r in rows if r["tag"] in GOLD_JIHA),
                           "asked": sum(1 for r in rows if asked(r))}
    for mode, strict in (("strict", True), ("ranked", False)):
        stops: Counter[str] = Counter()
        content_passed = 0
        for r in rows:
            w = whole(r)
            prev = idx.get((r["ref"], r["pos"] - 1))
            stop = run(w, stem_with_al(r), whole(prev) if prev else None, gold_of(r), w in forms,
                       strict=strict)
            stops[stop] += 1
            if stop == "PASSED" and r["tag"] in GOLD_JIHA:
                content_passed += 1
        funnel = [sum(v for s, v in stops.items() if stages_passed(s) >= k) for k in range(6)]
        out[mode] = {"funnel": funnel, "stops": {s: stops[s] for s in STOPS},
                     "content_passed": content_passed}
    return out


def render_lean(m: dict[str, Any]) -> str:
    s, r = m["strict"]["funnel"], m["ranked"]["funnel"]
    return "\n".join([
        "import Slge.Pipeline", "",
        "/-! قمعُ السُّلَّم على MASAQ: العابرون قبل المراحل وبعد كلٍّ منها — مولَّدٌ بـ",
        "`tools/gen_pipeline_index.py` من `masaq-shibh.json.gz` و`corpus-certificates.json.gz`؛",
        "لا يُحرَّر باليد. الصارمُ: قسمةٌ واحدة محسومة (Hasm)؛ المرتَّبُ: الأولى بعد الترتيب ذهبيّة. -/",
        "", "namespace Slge.PipelineTable", "",
        f"/-- {m['masaq']} كلمةً؛ العابرون بعد 0..5 مراحل (الصارم). -/",
        "def strict : List Nat := [" + ", ".join(str(n) for n in s) + "]", "",
        "/-- العابرون بعد 0..5 مراحل (المرتَّب). -/",
        "def ranked : List Nat := [" + ", ".join(str(n) for n in r) + "]", "",
        "/-- القمعان سلسلتان متناقصتان على خمس مراحل. -/",
        "theorem funnels : Pipeline.Antitone strict ∧ Pipeline.Antitone ranked ∧",
        "    strict.length = 6 ∧ ranked.length = 6 := by decide",
        "", "end Slge.PipelineTable", "",
    ])


def render_py(m: dict[str, Any]) -> str:
    s, r = m["strict"]["funnel"], m["ranked"]["funnel"]
    return "\n".join([
        '"""قمعُ السُّلَّم على MASAQ أعدادًا — مولَّدٌ بـ`tools/gen_pipeline_index.py`؛ لا يُحرَّر باليد."""',
        "", "from __future__ import annotations", "", "from typing import Final", "",
        f"MASAQ: Final[int] = {m['masaq']}",
        f"STRICT: Final[tuple[int, ...]] = ({', '.join(str(n) for n in s)})",
        f"RANKED: Final[tuple[int, ...]] = ({', '.join(str(n) for n in r)})", "",
    ])


def render(m: dict[str, Any]) -> str:
    n, c, a = m["masaq"], m["content"], m["asked"]
    st, rk = m["strict"], m["ranked"]

    def pct(k: int, d: int = n) -> str:
        return f"{100 * k / d:.1f}%"

    lines = [
        "# فهرسُ السُّلَّم — رقمٌ واحد من الشهادة إلى النسبة",
        "",
        "مولَّدٌ بـ`python tools/gen_pipeline_index.py` من `src/slge/pipeline.py`؛ لا يُحرَّر باليد. "
        "البرهانُ `formal/Slge/Pipeline.lean` (لا تقفز كلمةٌ مرحلة)، والقمعُ أعدادًا في "
        "`formal/Slge/PipelineTable.lean` مولَّدًا ومبرهَنًا متناقصًا.",
        "",
        "## الرقم", "",
        f"على **{n:,}** كلمةً من MASAQ (مرجعٌ محجوب) بشهادات البوّابة: تعبر المراحلَ الخمس بقراءةٍ "
        f"واحدةٍ محسومة (`hasm`) توافق المرجعَ في كلّ مرحلة **{st['funnel'][5]:,} "
        f"({pct(st['funnel'][5])})**؛ ولو قُبلت القراءةُ الأولى بعد الترتيب بدل المحسومة: "
        f"{rk['funnel'][5]:,} "
        f"({pct(rk['funnel'][5])}). ومن الكلمات التي للمرجع فيها جهةٌ (أسماءٌ وأفعالٌ وأوصاف "
        f"ومصادر: {c:,}): {st['content_passed']:,} ({pct(st['content_passed'], c)}) صارمًا، "
        f"{rk['content_passed']:,} ({pct(rk['content_passed'], c)}) مرتَّبًا. ومن الكلمات التي "
        f"يسألها المرجعُ عن المراحل الخمس كلِّها (جهةٌ وحالةٌ معربة ودورٌ ذو نسبة وجارٌ سابق: {a:,}): "
        f"**{st['funnel'][5]:,} ({pct(st['funnel'][5], a)})** صارمًا، {rk['funnel'][5]:,} "
        f"({pct(rk['funnel'][5], a)}) مرتَّبًا — هذا رقمُ الدقّة الخالص؛ والأوّلُ رقمُ التغطية.",
        "",
        "الكلمةُ تعبر المرحلةَ إن عبرت ما قبلها، وتقف باسمٍ واحد؛ الحرفُ والضميرُ يقفان باسم «لا جهةَ "
        "في المرجع» لا خطأً، والمبنيُّ باسم «الحالةُ لا تُقرأ»: المرجعُ لا يسألهما، فهما خارج القمع "
        "باسمهما لا داخلَه بالصفر.",
        "",
        "## القمع", "",
        "| بعد المرحلة | الصارم | % | المرتَّب | % |", "|---|---|---|---|---|",
        f"| (٠) الكلّ | {st['funnel'][0]:,} | {pct(st['funnel'][0])} | {rk['funnel'][0]:,} | "
        f"{pct(rk['funnel'][0])} |",
        *(f"| ({'١٢٣٤٥'[k - 1]}) {STAGES[k - 1]} | {st['funnel'][k]:,} | {pct(st['funnel'][k])} | "
          f"{rk['funnel'][k]:,} | {pct(rk['funnel'][k])} |" for k in range(1, 6)),
        "",
        "## التوقّفُ باسمه", "",
        "| الاسم | المرحلة | الصارم | المرتَّب |", "|---|---|---|---|",
        *(f"| `{s}` | {STAGES[stages_passed(s)] if stages_passed(s) < 5 else '—'} | "
          f"{st['stops'][s]:,} | {rk['stops'][s]:,} |" for s in STOPS),
        "",
        "## ما يقوله الرقم — باسمه", "",
        "- الرقمُ الصارم هو رقمُ الإدارة: ما دونه ليس «فهمًا» بل ترخيصًا متعدّدَ القراءات أو مخالفًا "
        "للمرجع في مرحلةٍ ما.",
        "- الصارمُ يحسم القسمةَ (`hasm`: واحدةٌ بلا قرينة أو الأعلى الوحيدةُ بالجوار والمعجم والتكرار؛ "
        "التعادلُ يقف باسمه)؛ والمرتَّبُ يأخذ الأولى بعد الترتيب ولو تعادلت — فقد يعلو أحدُهما الآخر "
        "في مرحلةٍ ويسفل في أخرى، ولا يهيمن أحدُهما.",
        "- بعد الحسم صار التوقّفُ الأكبر في الجهة (القسمةُ ذهبيّةٌ والجهةُ مخالفة) لا في الجذع؛ كلُّ ما "
        "فوق مرحلةٍ يُقاس على ما بلغها لا على اللغة.",
        "- المرجعُ MASAQ لا الصواب: ما يخالفه بوسمٍ متعارض (تاءُ الفاعل/التأنيث، الضميرُ المفعول "
        "فاعلًا) يُعدّ هنا مخالفةً حتى يُفصل باسمه.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    m = measure()
    md, lean, py = render(m), render_lean(m), render_py(m)
    if "--check" in sys.argv:
        ok = (TARGET.read_text(encoding="utf-8") == md and LEAN.read_text(encoding="utf-8") == lean
              and PY.read_text(encoding="utf-8") == py)
        sys.stdout.write("PIPELINE_INDEX.md مطابق\n" if ok else "PIPELINE_INDEX.md غيرُ مطابق؛ "
                         "شغّل tools/gen_pipeline_index.py\n")
        return 0 if ok else 1
    TARGET.write_text(md, encoding="utf-8")
    LEAN.write_text(lean, encoding="utf-8")
    PY.write_text(py, encoding="utf-8")
    sys.stdout.write(f"كُتب PIPELINE_INDEX.md: {m['strict']['funnel']} / {m['ranked']['funnel']}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
