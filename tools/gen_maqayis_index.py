"""فهرسُ القرينة المعجميّة (MAQAYIS_INDEX.md): كم قراءةً من قراءات الجذع المتعدّدة تفصلها العضويّةُ في
المقاييس — الرقمُ قبلَ القرينة وبعدَها على المودَع نفسه.

القياسُ على `tests/data/corpus-certificates.json.gz` (18,179 صورةً مشهودةً من المصحف): لكلّ صورةٍ
قراءاتُ `jidh` ثمّ المشهودُ منها في المقاييس (`attested`)؛ التعدّدُ قبلُ وبعدُ، وما لا شاهدَ له أصلًا.
ثمّ على `masaq-shibh.json.gz` بقسمته المحجوبة: هل القسمةُ الذهبيّةُ في القراءة المشهودة الوحيدة؟ وهل
أسقطتها القرينةُ (ذهبيّةٌ غيرُ مشهودة وأختُها مشهودة)؟ — الخسارةُ تُذكر كما يُذكر الربح.
"""

from __future__ import annotations

import gzip
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from slge.jidh import Reading, jidh
from slge.maqayis import ROOTS, SHA256, attested, member, rank, roots_of

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "MAQAYIS_INDEX.md"
DATA = ROOT / "tests" / "data"
Word = tuple[tuple[str, str], ...]
PRE_IN_STEM = ("IMPERF_PREF", "CV_PREF", "IV1S", "IV1P", "IV2MP", "IV3MS", "IV3MP", "IV3FS")


def corpus_forms() -> list[Word]:
    with gzip.open(DATA / "corpus-certificates.json.gz", "rt", encoding="utf-8") as f:
        d: dict[str, Any] = json.load(f)
    return [tuple((a, b) for a, b in x["cells"]) for x in d["forms"]]


def masaq_rows() -> list[tuple[Word, Word, bool, Word]]:
    """(الكلمة، سوابقُ المرجع بلا أل، أفيها أل؟، لواحقُه) — كما في فهرس الجذع."""

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


def _gold(r: Reading, pre: Word, det: bool, suf: Word) -> bool:
    """قراءةٌ على قسمة المرجع: السوابقُ نفسُها، وأل كما عنده، واللاحقةُ نفسُها."""

    return tuple(c for p in r.pre for c in p) == pre and (r.al != 0) == det and r.suf == suf


def kept(rs: tuple[Reading, ...]) -> tuple[Reading, ...]:
    """ما تُبقيه القرينة: المشهودُ إن وُجد، وإلّا القراءاتُ كلُّها (لا تُسقط القرينةُ ما لا بديلَ له)."""

    seen = tuple(r for r in rs if attested(r))
    return seen or rs


def measure() -> dict[str, Any]:
    forms = corpus_forms()
    before: Counter[str] = Counter()
    after: Counter[str] = Counter()
    none_attested = total_readings = attested_readings = 0
    for w in forms:
        rs = jidh(w)
        if not rs:
            continue
        total_readings += len(rs)
        seen = [r for r in rs if attested(r)]
        attested_readings += len(seen)
        if not seen:
            none_attested += 1
        k = len(kept(rs))
        before["1" if len(rs) == 1 else "2" if len(rs) == 2 else "3+"] += 1
        after["1" if k == 1 else "2" if k == 2 else "3+"] += 1
    rows = masaq_rows()
    b: Counter[str] = Counter()
    a: Counter[str] = Counter()
    dropped: Counter[str] = Counter()
    for w, pre, det, suf in rows:
        rs = jidh(w)
        if not rs:
            b["none"] += 1
            a["none"] += 1
            continue

        hits = [r for r in rs if _gold(r, pre, det, suf)]
        b["match" if hits and len(rs) == 1 else "among" if hits else "wrong"] += 1
        ks = kept(rs)
        khits = [r for r in ks if _gold(r, pre, det, suf)]
        if khits and len(ks) == 1:
            a["match"] += 1
        elif khits:
            a["among"] += 1
        elif hits:
            a["dropped"] += 1  # الخسارةُ: الذهبيّةُ غيرُ مشهودة وأختُها مشهودة
            dropped[_text(w)] += 1
        else:
            a["wrong"] += 1
    return {"forms": len(forms), "roots": len(ROOTS), "before": before, "after": after,
            "none_attested": none_attested, "total_readings": total_readings,
            "attested_readings": attested_readings, "masaq": len(rows), "b": b, "a": a,
            "dropped": dropped.most_common(8)}


def _text(w: Word) -> str:
    marks = {"فتح": "\u064e", "كسر": "\u0650", "ضم": "\u064f", "سكون": "\u0652"}
    return "".join(a + marks[b] for a, b in w)


def _witness_lines() -> list[str]:
    from slge.rawabit import cells_of

    out = []
    for text in ("كَذَّبُوا", "قَالَ", "دَعَوْا", "جَاءَ", "كُنْتُمْ"):
        w = cells_of(text)
        w = w[:-1] if text.endswith("ا") else w  # صورةُ الشهادة بلا الفارقة
        rs = rank(jidh(w))
        parts = []
        for r in rs:
            roots = "/".join("".join(ro) for ro in roots_of(r)) or "—"
            parts.append(f"{roots}{'✓' if attested(r) else '✗'}")
        out.append(f"- {text}: " + "، ".join(parts))
    return out


def render() -> str:
    m = measure()
    b, a, mb, ma = m["before"], m["after"], m["b"], m["a"]
    n, k = m["forms"], m["masaq"]
    multi_b, multi_a = b["2"] + b["3+"], a["2"] + a["3+"]
    lines = [
        "# فهرسُ القرينة المعجميّة — عضويّةُ الجذر في مقاييس اللغة",
        "",
        "مولَّدٌ بـ`python tools/gen_maqayis_index.py` من `src/slge/maqayis.py`؛ لا يُحرَّر باليد. "
        "البرهانُ: `formal/Slge/Maqayis.lean`؛ الجدولُ `formal/Slge/MaqayisTable.lean` مولَّدٌ من "
        "المودَع `tests/data/maqayis-roots.json.gz` (المصدرُ `maqayis_by_root_csv_999.csv`، "
        f"SHA-256 `{SHA256}`).",
        "",
        "## القانون", "",
        f"الجذرُ ثلاثةُ حوامل، والجدولُ {m['roots']:,} جذرًا ثلاثيًّا من مقاييس اللغة لابن فارس (الرباعيُّ "
        "الثلاثةُ أُسقط باسمه؛ والعينُ أو اللامُ المعتلّةُ في الطبعة — ا/ى — تطابق الواوَ أو الياءَ "
        "لا غير: "
        "`matchesL_weak`). العضويّةُ دالّةٌ على الخانات لا بحثَ خارج الجدول (`member_sound`)، وقراءةٌ "
        "أصلُها على قالبٍ سليم بجذرٍ مشهود مشهودةٌ (`attested_of_member`)، والترتيبُ بالقرينة — المشهودُ "
        "أوّلًا — لا يُسقط قراءةً ولا يزيدها لكلّ قائمة (`mem_rank`، `length_rank`). "
        "الشواهدُ `member_witnesses`، `rank_kadhdhabu`، `rank_qala` بالحساب.",
        "",
        "القرينةُ تفصل ما لم يُشهَد ولا تختار بين مشهودَين: قَالَ أصلاه قول وقيل كلاهما في المقاييس، "
        "فيبقيان "
        "(`rank_qala`). وفي هذا الفهرس «ما تُبقيه القرينة» = المشهودُ إن وُجد وإلّا القراءاتُ كلُّها.",
        "",
        "## الرقمُ قبلُ وبعدُ — على المودَع نفسه", "",
        f"{n:,} صورةً مشهودةً من المصحف؛ منها {sum(b.values()):,} يقرؤها الجذع "
        f"({m['total_readings']:,} قراءةً، المشهودُ منها في المقاييس {m['attested_readings']:,}):",
        "",
        "| عددُ القراءات | قبل القرينة | بعدها |", "|---|---|---|",
        f"| واحدة | {b['1']:,} | {a['1']:,} |",
        f"| اثنتان | {b['2']:,} | {a['2']:,} |",
        f"| ثلاثٌ فأكثر | {b['3+']:,} | {a['3+']:,} |",
        "",
        f"المتعدّدُ قبل القرينة {b['2'] + b['3+']:,}، وبعدها {a['2'] + a['3+']:,} — فصلت القرينةُ "
        f"{(b['2'] + b['3+']) - (a['2'] + a['3+']):,} "
        f"({100 * (multi_b - multi_a) / multi_b:.1f}% من المتعدّد). "
        f"وصورٌ لا قراءةَ مشهودةً لها أصلًا: {m['none_attested']:,} (تبقى كما هي).",
        "",
        "## القياس على قسمة MASAQ المحجوبة", "",
        f"على {k:,} كلمةً قسمها المرجعُ سوابقَ وجذعًا ولواحقَ:",
        "",
        "| الحكم | قبل القرينة | بعدها |", "|---|---|---|",
        f"| قراءةٌ واحدةٌ توافق القسمة | {mb['match']:,} ({100 * mb['match'] / k:.1f}%) "
        f"| {ma['match']:,} ({100 * ma['match'] / k:.1f}%) |",
        f"| القسمةُ بين قراءاتٍ متعدّدة | {mb['among']:,} ({100 * mb['among'] / k:.1f}%) "
        f"| {ma['among']:,} ({100 * ma['among'] / k:.1f}%) |",
        f"| القرينةُ أسقطت القسمةَ الذهبيّة | — | {ma['dropped']:,} "
        f"({100 * ma['dropped'] / k:.1f}%) |",
        f"| قراءاتٌ كلُّها على غير القسمة | {mb['wrong']:,} ({100 * mb['wrong'] / k:.1f}%) "
        f"| {ma['wrong']:,} ({100 * ma['wrong'] / k:.1f}%) |",
        f"| لا قراءة | {mb['none']:,} ({100 * mb['none'] / k:.1f}%) "
        f"| {ma['none']:,} ({100 * ma['none'] / k:.1f}%) |",
        "",
        "الخسارةُ باسمها: «أسقطت القسمةَ الذهبيّة» قراءةٌ ذهبيّةٌ جذرُها غيرُ مشهود وأختُها مشهودة — "
        "القرينةُ ترتّب ولا تُسقط (`mem_rank`)، والإسقاطُ هنا قياسٌ لما لو اختير المشهودُ وحدَه. "
        "أكثرُ ما يُسقَط: " + "، ".join(f"{t} ({c})" for t, c in m["dropped"]) + " — القسمةُ الذهبيّةُ "
        "قسمةُ زوائدَ لا قراءةُ قالب: ما تقرؤه الجداول (إنّي، في، منّي) يُقرأ هنا على قالبٍ بجذرٍ غيرِ "
        "مشهود، والمضارعُ الأجوف (يَكُونَ) يُقرأ اسمًا على فَعُول بجذرٍ غيرِ مشهود (يكن) قبل النزول "
        "بالإعلال؛ فالإسقاطُ هنا يُسقط قراءةً خاطئةً على قسمةٍ صحيحة. والجذرُ لا مرجعَ محجوبًا له في "
        "MASAQ.",
        "",
        "## الشواهد", "",
        *_witness_lines(),
        "",
        "## ما لا تفصله القرينةُ — باسمه", "",
        "- الأصلان الواويُّ واليائيُّ إذا كان كلاهما في المقاييس (قول/قيل، كون/كين…): يفصلهما المعنى "
        "لا الجدول.",
        "- الدلالةُ: محاورُ المعاني في المقاييس لم تُودَع؛ الجدولُ عضويّةٌ لا معنًى.",
        "- الرباعيُّ (ثأثأ، جأجأ، جهجه) أُسقط من الإيداع؛ والقوالبُ ثلاثيّة.",
        "- جذرٌ مشهودٌ في قراءةٍ على غير القسمة الذهبيّة (كَ + الذَّبُو تُفصل لأنّ ذبو ليست جذرًا، لا لأنّ "
        "القسمةَ خطأ).",
        "",
    ]
    assert member(("ق", "و", "ل")) and not member(("ذ", "ب", "و"))
    return "\n".join(lines)


def main() -> int:
    text = render()
    if "--check" in sys.argv:
        if TARGET.read_text(encoding="utf-8") != text:
            sys.stderr.write("MAQAYIS_INDEX.md غيرُ مطابق؛ شغّل tools/gen_maqayis_index.py\n")
            return 1
        sys.stdout.write("MAQAYIS_INDEX.md مطابق\n")
        return 0
    TARGET.write_text(text, encoding="utf-8")
    sys.stdout.write("كُتب MAQAYIS_INDEX.md\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
