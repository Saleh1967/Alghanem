"""فهرسُ الأعلام ولفظِ الجلالة (ALAM_INDEX.md): لفظٌ منفردٌ بلا قياس، بتوقيع المالك. (١) على
`corpus-certificates.json.gz` أوّلًا (قانونُ القارئ): كم صورةً من المصحف يقرؤها القارئُ علمًا أو لفظَ
جلالة، بأبوابها وصرفها وصور الجلالة. (٢) ثمّ على `masaq-shibh.json.gz` (مرجعٌ محجوب): صفوفُ
`NOUN_PROP`/`NOUN_PROP_FOREIGN`: كم يقرؤها، وكم توافق قسمتُها المرجعَ وكم تخالفه باسم الخلاف (أل في
لفظ الجلالة — فصلُه توقيعُ المالك)، وكم توافق حالتُها حالةَ المرجع، وأكثرُ ما لا يُقرأ بصوره.

تنبيه: قائمةُ الأعلام استُخرجت من صفوف MASAQ نفسها ثمّ وُقِّعت؛ فالقياسُ عليها **ليس مستقلًّا** عن المرجع
في اختيار الألفاظ، وهو مستقلٌّ في القسمة والحالة فقط.
"""

from __future__ import annotations

import gzip
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from slge.alam import ALAM, JALALA_FORMS, ilm
from slge.alam_table import SIGNED_BY
from slge.pipeline import GOLD_CASE
from slge.tawabi import compatible

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "ALAM_INDEX.md"
DATA = ROOT / "tests" / "data"
Word = tuple[tuple[str, str], ...]
MARKS = {"فتح": "َ", "كسر": "ِ", "ضم": "ُ", "سكون": "ْ"}
PROP = ("NOUN_PROP", "NOUN_PROP_FOREIGN")


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
    sarfs: Counter[str] = Counter()
    jforms: Counter[str] = Counter()
    read = with_pre = multi = 0
    for w in forms:
        ms = ilm(w)
        if not ms:
            continue
        read += 1
        m = ms[0]
        kinds[m.kind] += 1
        sarfs[m.sarf] += 1
        if m.kind == "جلالة":
            jforms[m.form] += 1
        with_pre += bool(m.pre)
        multi += len({x.pre for x in ms}) > 1
    rows = masaq_rows()
    props = [r for r in rows if r["tag"] in PROP]
    none = gold = det_jalala = wrong = 0
    case_asked = case_ok = 0
    unread: Counter[str] = Counter()
    for r in props:
        w = whole(r)
        ms = ilm(w)
        if not ms:
            none += 1
            unread[vowelled(w)] += 1
            continue
        m = ms[0]
        pre = tuple((a, b) for t, cs in r["pre"] for a, b in cs if t != "DET")
        det = any(t == "DET" for t, _ in r["pre"])
        suf = tuple((a, b) for _, cs in r["suf"] for a, b in cs)
        if tuple(c for p in m.pre for c in p) == pre and not suf:
            if det and m.kind == "جلالة":
                det_jalala += 1  # أل في لفظ الجلالة: المرجعُ يعدّها سابقةً والموقَّعُ لا — خلافٌ مفصول
            elif det:
                wrong += 1
            else:
                gold += 1
        else:
            wrong += 1
            continue
        c = GOLD_CASE.get(str(r["case"]))
        if c is not None:
            case_asked += 1
            case_ok += compatible(m.case, c)
    return {"signed_by": SIGNED_BY, "table": len(ALAM), "jalala_forms": len(JALALA_FORMS),
            "table_kinds": Counter(k for *_, k, _ in ALAM),
            "table_sarfs": Counter(s for *_, s in ALAM),
            "forms": len(forms), "read": read, "kinds": dict(kinds), "sarfs": dict(sarfs),
            "jforms": dict(jforms), "with_pre": with_pre, "multi": multi,
            "props": len(props), "gold": gold, "det_jalala": det_jalala, "wrong": wrong,
            "none": none, "case_asked": case_asked, "case_ok": case_ok,
            "unread_top": unread.most_common(15)}


def render() -> str:
    m = measure()

    def pct(k: int, d: int) -> str:
        return f"{100 * k / d:.1f}%" if d else "—"

    def kv(c: dict[str, int]) -> str:
        return "، ".join(f"{k} {v:,}" for k, v in sorted(c.items(), key=lambda x: -x[1]))

    lines = [
        "# فهرسُ الأعلام ولفظِ الجلالة — لفظٌ منفردٌ بلا قياس (بتوقيع المالك)",
        "",
        "مولَّدٌ بـ`python tools/gen_alam_index.py` من `src/slge/alam.py`؛ لا يُحرَّر باليد. المودَعُ "
        "`tests/data/owner-alam.json` موقَّعٌ: " + m["signed_by"] + ". البرهانُ "
        "`formal/Slge/Alam.lean`: كلُّ قراءةٍ تُردّ إلى الكلمة بعينها (`ilm_restores`)، وصورُ الجلالة "
        "عشرٌ (`jalala_forms_count`)، وجرُّ الممنوع بالفتح صورتُه المنصوبةُ بعينها "
        "(`mamnu_jarr_is_fatha`)، "
        "وشواهدُ على المودَع (`witness_jalala`، `witness_alam`).",
        "",
        "## المودَع", "",
        f"لفظُ الجلالة منفردٌ لا شبيهَ له: {m['jalala_forms']} صورٍ مسمّاة (ثلاثُ حالاتٍ × ابتداءً/بعد "
        "سابقة/مدًّا بعد تاء القسم أو همزة الاستفهام، واللهمّ). ثمّ "
        f"{m['table']} علمًا: " + kv(m["table_kinds"]) + "؛ صرفُها: " + kv(m["table_sarfs"]) +
        ". لا قالبَ ولا قياسَ على شيءٍ منها؛ ما ليس فيها لا يُزاد من الذاكرة.",
        "",
        "## على مودَع المصحف أوّلًا (قانونُ القارئ)", "",
        f"من {m['forms']:,} صورةً يقرأ القارئُ **{m['read']:,} ({pct(m['read'], m['forms'])})** علمًا "
        "أو لفظَ جلالة: " + kv(m["kinds"]) + "؛ صرفًا: " + kv(m["sarfs"]) +
        "؛ صورُ الجلالة: " + kv(m["jforms"]) +
        f"؛ منها بسابقة {m['with_pre']:,}، وتتعدّد قسمتُها في {m['multi']:,}.",
        "",
        "## على MASAQ (مرجعٌ محجوب في القسمة والحالة لا في اختيار الألفاظ)", "",
        f"صفوفُ العلم عند المرجع (`NOUN_PROP`، `NOUN_PROP_FOREIGN`): {m['props']:,}. يقرؤها القارئُ "
        f"بقسمة المرجع **{m['gold']:,} ({pct(m['gold'], m['props'])})**، وبقسمة الموقَّع خلافًا "
        "للمرجع "
        f"في أل لفظِ الجلالة {m['det_jalala']:,} (المرجعُ يعدّها سابقةً `DET` والموقَّعُ لفظًا منفردًا — "
        f"خلافٌ مفصولٌ بتوقيع المالك لا بالقياس)، وبغير ذلك {m['wrong']:,}، ولا يقرؤها {m['none']:,} "
        f"({pct(m['none'], m['props'])}).",
        "",
        f"الحالةُ: ممّا قُرئ بقسمةٍ مقبولة وسأل المرجعُ عن حالته {m['case_asked']:,}، توافق الحالةُ "
        f"المقروءةُ من الآخر حالةَ المرجع في **{m['case_ok']:,} "
        f"({pct(m['case_ok'], m['case_asked'])})** "
        "(الممنوعُ بالفتح «نصب/جرّ» يوافق النصبَ والجرّ؛ والمقصورُ لا تُقرأ حالتُه فيُعدّ خلافًا).",
        "",
        "### أكثرُ ما لا يُقرأ — بصوره", "",
        "| الصورة | العدد |", "|---|---|",
        *(f"| {w} | {n:,} |" for w, n in m["unread_top"]),
        "",
        "## ما ليس هنا — باسمه", "",
        "- قائمةُ الأعلام من صفوف المرجع نفسها ثمّ وُقِّعت؛ فاختيارُ الألفاظ غيرُ مستقلٍّ عن المرجع، "
        "والقسمةُ والحالةُ مستقلّتان.",
        "- ما لا يُقرأ أعلاه: أعلامٌ بأل (الْمَسِيح…) أو مضافة أو منوَّنة على غير ما شُهد، أو مستثناةٌ "
        "بالاسم (`excluded_by_name`)؛ لا تُزاد إلّا بتوقيعٍ جديد.",
        "- الأعجميُّ/العربيُّ من وسم المرجع (`NOUN_PROP_FOREIGN`) لا من المعجم؛ وصرفُ كلّ علمٍ من صوره "
        "المشهودة فقط («غيرُ مشهود الجرّ» حيث لم تُشهد صورةُ جرّ).",
        "",
    ]
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    text = render()
    if "--check" in argv:
        ok = TARGET.read_text(encoding="utf-8") == text
        sys.stdout.write("ALAM_INDEX.md مطابق\n" if ok else "ALAM_INDEX.md غيرُ مطابق\n")
        return 0 if ok else 1
    TARGET.write_text(text, encoding="utf-8")
    sys.stdout.write("كُتب ALAM_INDEX.md\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
