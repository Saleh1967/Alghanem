"""فهرسُ قوالب الاسم على أبنية سيبويه (ABNIYA_INDEX.md): الهيكلُ المودَع، والقوالبُ المضافة بأثرها
على المودَع.

القياسُ على `tests/data/corpus-certificates.json.gz` (18,179 صورةً مشهودةً من المصحف): لكلّ قالبٍ مضاف كم
صورةً له قراءةٌ عليه، وكم صورةً لا تُقرأ إلّا عليه (كلُّ قراءاتها عليه وحدَه)؛ وعلى قسمة MASAQ المحجوبة:
كم كلمةً قراءتُها الموافقةُ للقسمة على القالب المضاف. والأزواجُ غيرُ المفصولة في الجدول بأسمائها.
"""

from __future__ import annotations

import gzip
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from slge.abniya import AMBIGUOUS, ISM, OUTSIDE, SHA256, SKELETONS, in_abniya, separated
from slge.jidh import jidh
from slge.wazn import AWZAN

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "ABNIYA_INDEX.md"
DATA = ROOT / "tests" / "data"
Word = tuple[tuple[str, str], ...]
PRE_IN_STEM = ("IMPERF_PREF", "CV_PREF", "IV1S", "IV1P", "IV2MP", "IV3MS", "IV3MP", "IV3FS")


def corpus_forms() -> list[Word]:
    with gzip.open(DATA / "corpus-certificates.json.gz", "rt", encoding="utf-8") as f:
        d: dict[str, Any] = json.load(f)
    return [tuple((a, b) for a, b in x["cells"]) for x in d["forms"]]


def masaq_rows() -> list[tuple[Word, Word, bool, Word]]:
    with gzip.open(DATA / "masaq-shibh.json.gz", "rt", encoding="utf-8") as f:
        rows: list[dict[str, Any]] = json.load(f)["rows"]
    out = []
    for r in rows:
        allpre = tuple((a, b) for _, cs in r["pre"] for a, b in cs)
        pre = tuple((a, b) for t, cs in r["pre"] for a, b in cs
                    if t not in PRE_IN_STEM and t != "DET")
        det = any(t == "DET" for t, _ in r["pre"])
        stem = tuple((a, b) for a, b in r["stem"])
        suf = tuple((a, b) for _, cs in r["suf"] for a, b in cs)
        if stem:
            out.append((allpre + stem + suf, pre, det, suf))
    return out


def measure() -> dict[str, Any]:
    forms = corpus_forms()
    with_k: Counter[int] = Counter()
    only_k: Counter[int] = Counter()
    read = 0
    for w in forms:
        rs = jidh(w)
        if not rs:
            continue
        read += 1
        used = {k for r in rs for k in r.templates}
        for k in ISM:
            if k in used:
                with_k[k] += 1
            if all(r.templates == (k,) for r in rs):
                only_k[k] += 1
    gold_k: Counter[int] = Counter()
    rows = masaq_rows()
    for w, pre, det, suf in rows:
        for r in jidh(w):
            if tuple(c for p in r.pre for c in p) == pre and (r.al != 0) == det and r.suf == suf:
                for k in r.templates:
                    if k in ISM:
                        gold_k[k] += 1
    pairs = sum(1 for k in range(len(AWZAN)) for q in range(k + 1, len(AWZAN))
                if separated(AWZAN[k].template, AWZAN[q].template))
    sys.path.insert(0, str(ROOT / "tools"))
    from gen_jidh_index import measure as jidh_measure

    j = jidh_measure()
    return {"forms": len(forms), "read": read, "with": with_k, "only": only_k, "gold": gold_k,
            "masaq": len(rows), "separated_pairs": pairs, "n": len(AWZAN),
            "in_abniya": sum(in_abniya(w.template) for w in AWZAN), "step2": j["step2"],
            "none": j["none"], "match": j["gold_match"]}


def render() -> str:
    m = measure()
    n = m["n"]
    lines = [
        "# فهرسُ قوالب الاسم على أبنية سيبويه",
        "",
        "مولَّدٌ بـ`python tools/gen_abniya_index.py` من `src/slge/abniya.py`؛ لا يُحرَّر باليد. "
        "البرهانُ: "
        "`formal/Slge/Abniya.lean`؛ الجدولُ `formal/Slge/AbniyaTable.lean` مولَّدٌ من المودَع "
        f"`tests/data/sibawayh-abniya.tsv` (SHA-256 `{SHA256}`، 749 صفًّا، {len(SKELETONS)} هيكلًا).",
        "",
        "## الهيكلُ والعضويّة", "",
        "هيكلُ القالب حروفُه بلا حركات (الأصولُ ف ع ل، الزوائدُ بحواملها، الشدّةُ حرفٌ واحد، التاءُ "
        "الأخيرةُ تاءُ تأنيثٍ تُسقط)، والعضويّةُ في الأبنية تقبل الهمزةَ الأولى وصلًا أو قطعًا لأنّ "
        f"الخانةَ لا تميّزهما. {m['in_abniya']} من {n} قالبًا هياكلُها عند سيبويه؛ والباقي "
        f"{len(OUTSIDE)} بأرقامها "
        f"(`outside_abniya`): {', '.join(AWZAN[k].name for k in OUTSIDE)}.",
        "",
        "## القوالبُ المضافة (أ2) — الرقمُ على المودَع نفسه", "",
        "كلُّ قالبٍ هيكلُه عند سيبويه (`ism_in_abniya`)، وحافّتُه من أبيه في الشبكة بعمليّات `Shabaka` "
        "(`edges_apply`)، وأُدخل لأنّه رفع الرقمَ على المودَع ولم يُنزل الموافقةَ على MASAQ؛ وما لم "
        "يستوفِ "
        "ذلك معلَّقٌ باسمه أدناه.",
        "",
        f"{m['forms']:,} صورةً من المصحف، يقرأ الجذعُ منها {m['read']:,}:",
        "",
        "| القالب | صورٌ لها قراءةٌ عليه | لا تُقرأ إلّا عليه | قراءةٌ موافقةٌ لقسمة MASAQ عليه |",
        "|---|---|---|---|",
    ]
    for k in ISM:
        lines.append(f"| {AWZAN[k].name} ({k}) | {m['with'][k]:,} | {m['only'][k]:,} "
                     f"| {m['gold'][k]:,} |")
    lines += [
        "",
        f"الرقمُ قبلُ وبعدُ على المودَع نفسه (فهرسُ الجذع): الجذعُ يقرأ {m['step2']:,} من {m['forms']:,} "
        "(كانت 14,912 قبل القوالب الأربعة)، ولا قراءةَ على MASAQ "
        f"{100 * m['none'] / m['masaq']:.1f}% "
        f"(كانت 15.9%)، وقراءةٌ واحدةٌ موافقة {100 * m['match'] / m['masaq']:.1f}% (كانت 35.5%).",
        "",
        "## المعلَّقُ باسمه", "",
        "- فَعِلٌ: لا يضيف صورةً — يتساوى مع فَعِلَ بعد تسوية الآخر (لو أُدخل لكان زوجًا غيرَ مفصول).",
        "- فَيْعِلٌ، فُعْلَةٌ، فَعِيلَةٌ، مَفْعِلَةٌ، فَعْلِيٌّ (النسبة)، فَعَلِيٌّ، فُعَالَةٌ: قيست خارج الشجرة "
        "(ADR ١٠) فلم ترفع الموافقةَ على MASAQ أو أنزلتها — تاءُ التأنيث والنسبةُ لاحقتان قبل أن "
        "تكونا "
        "قالبًا (أ3)، لا قالبَ لهما هنا.",
        "- الرباعيُّ (فعلل وما بُني عليه: 35 بناءً عند سيبويه) خارج الأصل الثلاثيّ: دَين.",
        "",
        "## التمايز", "",
        f"الأزواجُ المفصولة {m['separated_pairs']:,} من {n * (n - 1) // 2:,} (`awzan_separated`)؛ "
        "وغيرُ "
        f"المفصولة {len(AMBIGUOUS)} بأسمائها (`ambiguous_sound`): "
        + "، ".join(f"{AWZAN[k].name}/{AWZAN[q].name}" for k, q in AMBIGUOUS) + " — وهي بعينها ما "
        "يعيده الجذعُ قراءاتٍ متعدّدةً على جذرٍ واحد؛ والمفصولُ لا يقرأ ملءً واحدًا على أصلين نظيفين "
        "(`awzan_disjoint`).",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    text = render()
    if "--check" in sys.argv:
        if TARGET.read_text(encoding="utf-8") != text:
            sys.stderr.write("ABNIYA_INDEX.md غيرُ مطابق؛ شغّل tools/gen_abniya_index.py\n")
            return 1
        sys.stdout.write("ABNIYA_INDEX.md مطابق\n")
        return 0
    TARGET.write_text(text, encoding="utf-8")
    sys.stdout.write("كُتب ABNIYA_INDEX.md\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
