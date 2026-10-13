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

from slge.jidh import OBJECT_SUFFIXES, PROCLITICS
from slge.pipeline import GOLD_JIHA
from slge.tawzi import (
    _BABS,
    ANCHORS,
    GAP,
    HOSTS,
    KINDS,
    RULES,
    TABLE,
    Mabni,
    maana,
    maana_suffix,
    tawzi,
    wasm,
)

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


OPEN_EXCLUDED: tuple[str, ...] = ("ADV", "NOUN_ABSTRACT")
"""مجتمعُ الفصل الخاطئ: وسومُ `GOLD_JIHA` إلّا هذين، لأنّ الظروف فيهما وهي في جدولنا المغلق (ADR ٥٢)."""


def _split(r: dict[str, Any]) -> tuple[Word, Word]:
    pre = tuple((a, b) for t, cs in r["pre"] for a, b in cs if t not in PRE_IN_STEM and t != "DET")
    suf = tuple((a, b) for _, cs in r["suf"] for a, b in cs)
    return pre, suf


def _gold(m: Mabni, r: dict[str, Any]) -> bool:
    pre, suf = _split(r)
    return tuple(c for p in m.pre for c in p) == pre and m.suf == suf


def measure_rules(forms: list[Word], rows: list[dict[str, Any]],
                  rules: frozenset[str]) -> dict[str, int]:
    """مقاييسُ التسجيل المسبق (ADR ٥٢) بالقواعد `rules`: المبنيُّ عند المرجع (بقسمته، بغيرها، لا يُقرأ)،
    والفصلُ الخاطئ (مفتوحٌ عند المرجع يُقرأ مغلقًا)، وصورُ المصحف المقروءة."""

    cache: dict[Word, tuple[Mabni, ...]] = {}

    def t(w: Word) -> tuple[Mabni, ...]:
        if w not in cache:
            cache[w] = tawzi(w, rules)
        return cache[w]

    out = {"gold": 0, "wrong": 0, "none": 0, "open": 0, "false_closed": 0, "quran_read": 0}
    for r in rows:
        w = whole(r)
        if r["tag"] not in GOLD_JIHA:
            ms = t(w)
            key = "none" if not ms else "gold" if _gold(ms[0], r) else "wrong"
            out[key] += 1
        elif r["tag"] not in OPEN_EXCLUDED:
            out["open"] += 1
            out["false_closed"] += bool(t(w))
    out["quran_read"] = sum(1 for w in forms if t(w))
    return out


def decide(base: dict[str, int], new: dict[str, int]) -> bool:
    """قاعدةُ القرار المسجَّلة قبل القياس: نقص «لا يقرؤه»، وزاد «بقسمة المرجع»، وزيادةُ الفصل الخاطئ أقلُّ
    من نصف زيادة «بقسمة المرجع»."""

    dg = new["gold"] - base["gold"]
    df = new["false_closed"] - base["false_closed"]
    return new["none"] < base["none"] and dg > 0 and 2 * df < dg


def closure() -> dict[str, Any]:
    """الإغلاق: كلُّ صورةٍ في الجدول المغلق وكلُّ سابقةٍ ولاحقة لها بابٌ ومعنًى من المودَع أو فجوةٌ باسمها."""

    def has(b: str, w: Word, att: bool = False) -> bool:
        return maana(b, w, att)[1] != GAP

    cores = [w for _, _, w in (*TABLE, *HOSTS)]
    gaps: Counter[str] = Counter()
    for w in cores:
        if not any(has(b, w) for b, _ in _BABS[w]):
            gaps["/".join(b for b, _ in _BABS[w])] += 1
    pro_gap = [vowelled(p) for p in PROCLITICS if not has("حرف", p)]
    suf_gap = [vowelled(x) for x in OBJECT_SUFFIXES if maana_suffix(x)[1] == GAP]
    qisms: Counter[str] = Counter()
    for w in cores:
        qisms["+".join(dict.fromkeys(b for b, _ in _BABS[w]))] += 1
    return {"cores": len(cores), "core_gaps": dict(gaps), "pro": len(PROCLITICS),
            "pro_gap": pro_gap,
            "suf": len(OBJECT_SUFFIXES), "suf_gap": suf_gap, "babs": qisms.most_common(12)}


def closed_on(forms: list[Word]) -> tuple[int, int, int]:
    """على صور المصحف: (المقروءةُ بالموزِّع، وما لها قراءةٌ كلُّ أجزائها ذواتُ معنًى، وما كلُّ قراءاتها
    كذلك)."""

    read = some = every = 0
    for w in forms:
        tags = [wasm(m) for m in tawzi(w)]
        if not tags:
            continue
        ok = [all(any(src != GAP for *_, src in j.babs) for j in t.parts) for t in tags]
        read, some, every = read + 1, some + any(ok), every + all(ok)
    return read, some, every


def render() -> str:
    m = measure()
    forms, rows = corpus_forms(), masaq_rows()
    base = measure_rules(forms, rows, frozenset())
    full = measure_rules(forms, rows, RULES)
    ablate = {r: measure_rules(forms, rows, RULES - {r}) for r in sorted(RULES)}
    accepted = decide(base, full)
    cl = closure()
    cread, csome, cevery = closed_on(forms)
    src_n = Counter(a.source for a in ANCHORS)

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
        "## القواعدُ الخمس (ADR ٥٢) — على التسجيل المسبق", "",
        "المقاييسُ مسجَّلةٌ قبل القواعد (ADR ٥٢)، والقواعدُ مرساةٌ في الكتاب المختوم. **تلوّثٌ مسمًّى**: "
        "`REFERENCE_SEEN_BEFORE_RULES` — قائمةُ ما لا يُقرأ كانت "
        "منشورةً قبل اختيار القواعد، فالرقمُ على MASAQ "
        "«مفحوصٌ على مرجعٍ رآه الوكيل» لا قياسٌ أعمى.",
        "",
        "| المقياس | بلا القواعد | بالقواعد | الفرق |", "|---|---|---|---|",
        *(f"| {lab} | {base[k]:,} | {full[k]:,} | {full[k] - base[k]:+,} |" for lab, k in (
            ("المبنيُّ عند المرجع: بقسمته", "gold"), ("المبنيُّ عند المرجع: بغيرها", "wrong"),
            ("المبنيُّ عند المرجع: لا يُقرأ", "none"),
            (f"الفصلُ الخاطئ (من {base['open']:,} مفتوحًا)", "false_closed"),
            (f"صورُ المصحف المقروءة (من {len(forms):,})", "quran_read"))),
        "",
        f"**قاعدةُ القرار** (نقص «لا يُقرأ»، وزاد «بقسمته»، والفصلُ الخاطئ أقلُّ من نصف الزيادة): "
        f"{'مقبولة' if accepted else 'مرفوضة'}.",
        "",
        "### أثرُ كلّ قاعدةٍ بحذفها", "",
        "| القاعدة المحذوفة | بقسمته | لا يُقرأ | الفصلُ الخاطئ | "
        "المصحف | ما أصلحته (بقسمته) | ما أفسدته (فصلًا) |",
        "|---|---|---|---|---|---|---|",
        *(f"| `{r}` | {a['gold']:,} | {a['none']:,} | {a['false_closed']:,} | "
          f"{a['quran_read']:,} | "
          f"{full['gold'] - a['gold']:+,} | {full['false_closed'] - a['false_closed']:+,} |"
          for r, a in ablate.items()),
        "",
        "## الوسمُ المغلق — التعريفُ والمعنى (ADR ٥٢)", "",
        "كلُّ قراءةٍ من قراءات الموزِّع تحمل وسمًا (`tawzi.wasm`): "
        "القسمُ (حرف، اسمٌ مبنيّ، أو «أداة» قسمُها غيرُ "
        "مودَع)، والأجزاءُ بأدوارها (سابقة، نواة، لاحقة)، ولكلّ جزءٍ أبوابُه كلُّها ومعانيه من المودَع "
        "(`huruf`، `maani_table` من ج3، `rawabit`، `damair`، "
        "`ishara`، `istifham`، `zuruf`، `zaman`) أو الفجوةُ "
        f"`{GAP}` — لا يُكتب معنًى من الذاكرة.",
        "",
        f"**المرساةُ بنصّها (ADR ٥٥):** {len(ANCHORS)} معنًى عبارةً بعينها في سطرها من مختوم — "
        f"{src_n['ibn-aqil']} من شرح ابن عقيل (باب الموصول) و{src_n['kitab']} من الكتاب "
        "(لَ: لامُ الابتداء ولامُ اليمين)؛ وهاءُ الضمير المكسورة (س18128) ونِي (س8088) "
        "تُردّان إلى أصلهما في `damair` "
        "(`maana_suffix`). تُطابَق العبارةُ في سطرها حرفًا حرفًا (`test_tawzi.py`).",
        "",
        f"- على المصحف: {cread:,} صورةً يقرؤها الموزِّع؛ لـ{csome:,} منها قراءةٌ كلُّ أجزائها ذواتُ معنًى، "
        f"ولـ{cevery:,} كلُّ قراءاتها كذلك.",
        f"- النوى: {cl['cores']} صورةً؛ بلا معنًى مودَع: "
        + ("، ".join(f"{k} {v}" for k, v in cl["core_gaps"].items()) or "لا شيء") + ".",
        f"- السوابق: {cl['pro']}؛ بلا معنًى مودَع: " + ("، ".join(cl["pro_gap"]) or "لا شيء") + ".",
        f"- اللواحق: {cl['suf']}؛ بلا معنًى مودَع: " + ("، ".join(cl["suf_gap"]) or "لا شيء") + ".",
        "- أبوابُ النوى (والصورةُ في بابين تُعدّ بهما معًا): "
        + "، ".join(f"{k} {v}" for k, v in cl["babs"]) + ".",
        "",
        "## ما ليس هنا — باسمه", "",
        "- ما لا يُقرأ أعلاه غائبٌ من جداولنا أو مركَّبٌ لا يفكّه الموزِّع (أَنَّا = أَنَّ + نَا بإدغام؛ "
        "لفظُ الجلالة بأل)؛ لا يُزاد من الذاكرة بل من مودَعٍ مسمًّى.",
        "- اللاحقةُ هنا ضميرُ نصبٍ/جرٍّ متّصل فقط؛ والتعديلاتُ مسمّاةٌ كلُّها: الألفُ المقصورة ياءً، لامُ الجرّ "
        "مفتوحة، التقاءُ الساكنين، والقواعدُ الخمس أعلاه — لا غيرُها.",
        "- قراءاتُ الحكم (`qiraa.harf`) لا ترى القواعدَ الخمس "
        "(`is_base`، `Tawzi.base`) كما سُجّل قبلها.",
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
