"""فهرسُ الموزِّع (TAWZI_INDEX.md): المبنيّاتُ المودَعة قراءةً قبل القوالب. (١) على
`corpus-certificates.json.gz` أوّلًا (قانونُ القارئ): كم صورةً من المصحف يقرؤها الموزِّع، بأبوابها، وكم
منها بسابقةٍ أو لاحقة. (٢) ثمّ على `masaq-shibh.json.gz` (مرجعٌ محجوب): الكلماتُ التي يعدّها المرجعُ
حرفًا أو ضميرًا أو موصولًا (لا جهةَ لها): كم يقرؤها الموزِّع بقسمة المرجع، وكم بغيرها، وكم لا يقرؤها
(`PARTICLE_NOT_IN_TABLE`) — وأكثرُ ما لا يُقرأ بصوره.
"""

from __future__ import annotations

import gzip
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from slge.pipeline import GOLD_JIHA
from slge.tawzi import KINDS, TABLE, tawzi

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "TAWZI_INDEX.md"
DATA = ROOT / "tests" / "data"
Word = tuple[tuple[str, str], ...]
PRE_IN_STEM = ("IMPERF_PREF", "CV_PREF", "IV1S", "IV1P", "IV2MP", "IV3MS", "IV3MP", "IV3FS")
MARKS = {"فتح": "َ", "كسر": "ِ", "ضم": "ُ", "سكون": "ْ"}


def corpus_forms() -> list[Word]:
    with gzip.open(DATA / "corpus-certificates.json.gz", "rt", encoding="utf-8") as f:
        d: dict[str, Any] = json.load(f)
    return [tuple((a, b) for a, b in x["cells"]) for x in d["forms"]]


def masaq_rows() -> list[dict[str, Any]]:
    with gzip.open(DATA / "masaq-shibh.json.gz", "rt", encoding="utf-8") as f:
        rows: list[dict[str, Any]] = json.load(f)["rows"]
    return rows


def whole(r: dict[str, Any]) -> Word:
    return (*((a, b) for _, cs in r["pre"] for a, b in cs), *((a, b) for a, b in r["stem"]),
            *((a, b) for _, cs in r["suf"] for a, b in cs))


def vowelled(w: Word) -> str:
    return "".join(k + MARKS[s] for k, s in w)


def measure() -> dict[str, Any]:
    forms = corpus_forms()
    kinds: Counter[str] = Counter()
    read = with_pre = with_suf = multi = 0
    for w in forms:
        ms = tawzi(w)
        if not ms:
            continue
        read += 1
        kinds[ms[0].kind] += 1
        with_pre += bool(ms[0].pre)
        with_suf += bool(ms[0].suf)
        multi += len({(m.pre, m.suf) for m in ms}) > 1
    rows = masaq_rows()
    particles = [r for r in rows if r["tag"] not in GOLD_JIHA]
    gold = wrong = none = 0
    unread: Counter[str] = Counter()
    by_tag_unread: Counter[str] = Counter()
    for r in particles:
        w = whole(r)
        ms = tawzi(w)
        if not ms:
            none += 1
            unread[vowelled(w)] += 1
            by_tag_unread[str(r["tag"])] += 1
            continue
        pre = tuple((a, b) for t, cs in r["pre"] for a, b in cs
                    if t not in PRE_IN_STEM and t != "DET")
        suf = tuple((a, b) for _, cs in r["suf"] for a, b in cs)
        m = ms[0]
        if tuple(c for p in m.pre for c in p) == pre and m.suf == suf:
            gold += 1
        else:
            wrong += 1
    return {"table": len(TABLE), "kinds_table": {k: sum(1 for kk, _, _ in TABLE if kk == k)
                                                 for k in KINDS},
            "forms": len(forms), "read": read, "kinds": dict(kinds), "with_pre": with_pre,
            "with_suf": with_suf, "multi": multi,
            "masaq_particles": len(particles), "gold": gold, "wrong": wrong, "none": none,
            "unread_top": unread.most_common(12), "unread_by_tag": by_tag_unread.most_common(8)}


def render() -> str:
    m = measure()

    def pct(k: int, d: int) -> str:
        return f"{100 * k / d:.1f}%" if d else "—"

    lines = [
        "# فهرسُ الموزِّع — المبنيّاتُ تُقرأ من جدولها قبل القوالب",
        "",
        "مولَّدٌ بـ`python tools/gen_tawzi_index.py` من `src/slge/tawzi.py`؛ لا يُحرَّر باليد. البرهانُ "
        "`formal/Slge/Tawzi.lean`: كلُّ قراءةٍ تُردّ إلى الكلمة بعينها (`tawzi_restores`)، ومبنيُّها من "
        "الجدول (`tawzi_core_mem`)، ولاحقتُها من جدول الضمائر (`tawzi_suf_mem`)، والجدولُ مرخَّص "
        "(`table_licensed`).",
        "",
        "## الجدول", "",
        f"{m['table']} صورةً من الجداول القائمة بلا تكرار: " +
        "، ".join(f"{k} {v}" for k, v in m["kinds_table"].items()) +
        ". ما ليس فيها لا يُزاد من الذاكرة؛ يبقى باسمه أدناه.",
        "",
        "## على مودَع المصحف أوّلًا (قانونُ القارئ)", "",
        f"من {m['forms']:,} صورةً يقرأ الموزِّعُ **{m['read']:,} ({pct(m['read'], m['forms'])})** "
        "مبنيًّا من جدوله: "
        + "، ".join(f"{k} {v:,}" for k, v in sorted(m["kinds"].items(), key=lambda kv: -kv[1]))
        + f"؛ منها بسابقة {m['with_pre']:,} وبلاحقةِ ضمير {m['with_suf']:,}، وتتعدّد قسمتُها في "
        f"{m['multi']:,}.",
        "",
        "## على MASAQ (مرجعٌ محجوب)", "",
        f"الكلماتُ التي لا جهةَ لها عند المرجع (حروفٌ وضمائرُ وموصولات…): {m['masaq_particles']:,}. "
        f"يقرؤها الموزِّعُ بقسمة المرجع **{m['gold']:,} ({pct(m['gold'], m['masaq_particles'])})**، "
        f"وبغير قسمته {m['wrong']:,}، ولا يقرؤها {m['none']:,} "
        f"({pct(m['none'], m['masaq_particles'])}) — `PARTICLE_NOT_IN_TABLE`.",
        "",
        "### أكثرُ ما لا يُقرأ — بصوره وأوسامه", "",
        "| الصورة | العدد |", "|---|---|",
        *(f"| {w} | {n:,} |" for w, n in m["unread_top"]),
        "",
        "| وسمُ المرجع | غيرُ مقروء |", "|---|---|",
        *(f"| `{t}` | {n:,} |" for t, n in m["unread_by_tag"]),
        "",
        "## ما ليس هنا — باسمه", "",
        "- ما لا يُقرأ أعلاه غائبٌ من جداولنا أو مركَّبٌ لا يفكّه الموزِّع (أَنَّا = أَنَّ + نَا بإدغام؛ "
        "لفظُ الجلالة بأل)؛ لا يُزاد من الذاكرة بل من مودَعٍ مسمًّى.",
        "- اللاحقةُ هنا ضميرُ نصبٍ/جرٍّ متّصل فقط؛ التعديلُ الوحيدُ الألفُ المقصورة ياءً (`alifToYa`).",
        "- خلافُ أوسمة المرجع (تاءُ التأنيث لاحقةً، بِ/لِ سابقتين، لفظُ الجلالة) يُحصى في فهرس السُّلَّم "
        "ولا يُفصل هنا.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    text = render()
    if "--check" in sys.argv:
        if TARGET.read_text(encoding="utf-8") != text:
            sys.stderr.write("TAWZI_INDEX.md غيرُ مطابق؛ شغّل tools/gen_tawzi_index.py\n")
            return 1
        sys.stdout.write("TAWZI_INDEX.md مطابق\n")
        return 0
    TARGET.write_text(text, encoding="utf-8")
    sys.stdout.write("كُتب TAWZI_INDEX.md\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
