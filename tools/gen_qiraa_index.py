"""فهرسُ القراءة الموحَّدة (QIRAA_INDEX.md): الحرفُ أوّلًا، والجذعُ على الصورة وعلى أصلها المردود (ADR ٤١).

(١) على `corpus-certificates.json.gz` أوّلًا (قانونُ القارئ): كم صورةً (وموضعًا) يقرؤها الموزِّعُ حرفًا
من حروف المعاني فيُحجب جذرُها عن الحكم، وكم منها كان للجذع عليها قراءةٌ مشهودةٌ في المقاييس (ما حُجب ولم
يُحذف)؛ وكم
صورةً ردّت السابقةُ الموصولةُ أصلَها فقرأه الجذعُ على جذرٍ مشهود، وكم منها لم يكن لها جذرٌ مشهودٌ قبل.
(٢) ثمّ على `masaq-shibh.json.gz` (مرجعٌ محجوب): من الكلمات التي يقرؤها الموزِّعُ حرفًا، كم يعدّها المرجعُ
بلا جهة (حرفًا أو ضميرًا أو موصولًا) وكم يعدّها اسمًا أو فعلًا أو وصفًا (حجبٌ على غير المرجع) — بصورها.
"""

from __future__ import annotations

import gzip
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from slge.maqayis import attested
from slge.pipeline import GOLD_JIHA
from slge.qiraa import harf, lifted, qiraa, restored

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "QIRAA_INDEX.md"
DATA = ROOT / "tests" / "data"
Word = tuple[tuple[str, str], ...]
MARKS = {"فتح": "َ", "كسر": "ِ", "ضم": "ُ", "سكون": "ْ"}


def corpus() -> tuple[list[Word], Counter[int]]:
    with gzip.open(DATA / "corpus-certificates.json.gz", "rt", encoding="utf-8") as f:
        d: dict[str, Any] = json.load(f)
    return [tuple((a, b) for a, b in x["cells"]) for x in d["forms"]], Counter(d["stream"])


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
    forms, cnt = corpus()
    n = Counter[str]()
    kinds: Counter[str] = Counter()
    for k, w in enumerate(forms):
        q = qiraa(w)
        direct = [x for x in q if x.via is None]
        if harf(w):
            n["harf"] += 1
            n["harf_pos"] += cnt[k]
            if direct:
                n["harf_jidh"] += 1
                n["harf_jidh_pos"] += cnt[k]
                if any(attested(x.r) for x in direct):
                    n["harf_att"] += 1
                    n["harf_att_pos"] += cnt[k]
        if lifted(w):
            n["lifted"] += 1
        rs = restored(w)
        n["restored_readings"] += len(rs)
        if any(attested(x.r) for x in rs):
            n["gain"] += 1
            n["gain_pos"] += cnt[k]
            kinds.update({str(x.via.kind) for x in rs if x.via is not None and attested(x.r)})
            if not any(attested(x.r) for x in direct):
                n["new"] += 1
                n["new_pos"] += cnt[k]
    masaq: Counter[str] = Counter()
    against: Counter[str] = Counter()
    for r in masaq_rows():
        w = whole(r)
        if not harf(w):
            continue
        masaq["harf"] += 1
        if r["tag"] in GOLD_JIHA:
            masaq["against"] += 1
            against[f"{vowelled(w)} ({r['tag']})"] += 1
        else:
            masaq["with"] += 1
    return {"forms": len(forms), "positions": sum(cnt.values()), **n, "kinds": dict(kinds),
            "masaq": dict(masaq), "against": against.most_common(12)}


def pct(a: int, b: int) -> str:
    return f"{100 * a / b:.1f}%" if b else "—"


def render() -> str:
    m = measure()
    mq = m["masaq"]
    kinds = "، ".join(f"`{k}` {v:,}" for k, v in sorted(m["kinds"].items()))
    against = "؛ ".join(f"{w} {c:,}" for w, c in m["against"])
    lines = [
        "# فهرسُ القراءة الموحَّدة — الحرفُ أوّلًا، والجذعُ على الصورة وعلى أصلها المردود",
        "",
        "مولَّدٌ بـ`python tools/gen_qiraa_index.py`؛ لا يُحرَّر باليد. المبرهَن في `Slge.Qiraa` "
        "(ADR ٤١): ما قرأه الموزِّعُ حرفًا فلا قراءةَ للحكم (`harf_no_hukm`) ولا تُحذف قراءةُ جذع "
        "(`jidh_sub_qiraa`)؛ "
        "وكلُّ قراءةٍ تُردّ — سابقتُها إلى الكلمة بعينها وجذعُها إلى الأصل المردود (`qiraa_restores`) — "
        "وأصلُها يصعد إلى جذعها (`qiraa_ascends`).",
        "",
        "## (١) على مودَع المصحف (قانونُ القارئ)",
        "",
        f"{m['forms']:,} صورةً مشهودةً ({m['positions']:,} موضعًا):",
        "",
        "| | صور | مواضع |",
        "|---|---:|---:|",
        f"| يقرؤها الموزِّعُ حرفًا (حروفُ المعاني) فيُحجب جذرُها عن الحكم | {m['harf']:,} | "
        f"{m['harf_pos']:,} |",
        f"| منها للجذع عليها قراءةٌ (حُجبت ولم تُحذف) | {m['harf_jidh']:,} | {m['harf_jidh_pos']:,} |",
        f"| منها قراءةٌ بجذرٍ مشهودٍ في المقاييس | {m['harf_att']:,} | {m['harf_att_pos']:,} |",
        f"| ردّت سابقتُها الموصولةُ أصلًا فقرأه الجذعُ على جذرٍ مشهود | {m['gain']:,} | "
        f"{m['gain_pos']:,} |",
        f"| منها لم يكن لها جذرٌ مشهودٌ على الصورة | {m['new']:,} | {m['new_pos']:,} |",
        "",
        f"الصورُ ذاتُ سابقةٍ موصولةٍ مردودة (غيرَ أل): {m.get('lifted', 0):,}؛ وقراءاتُ الأصل المردود "
        f"{m['restored_readings']:,}. أبوابُ المشهود منها: {kinds}.",
        "",
        "## (٢) على قسمة MASAQ المحجوبة",
        "",
        f"من {mq.get('harf', 0):,} كلمةً يقرؤها الموزِّعُ حرفًا: بلا جهةٍ عند المرجع (حرفٌ أو ضميرٌ أو "
        f"موصول) {mq.get('with', 0):,} ({pct(mq.get('with', 0), mq.get('harf', 0))})، "
        "واسمٌ أو فعلٌ أو "
        f"وصفٌ عنده {mq.get('against', 0):,} ({pct(mq.get('against', 0), mq.get('harf', 0))}) — حجبٌ "
        "على غير المرجع، وقراءةُ الجذع فيها باقيةٌ لم تُحذف.",
        "",
        f"أكثرُها: {against or '—'}.",
        "",
        "## ما ليس هنا — باسمه",
        "",
        "- الحجبُ عن الحكم لا الحذف: الكتابةُ الواحدة في الخانات قد تكون حرفًا وفعلًا (عَلَى/عَلَا، خَلَا)، "
        "والفصلُ بينهما للقرينة لا للموزِّع.",
        "- قراءةُ الأصل المردود تُحصى ولا تُحسم: إن قرأ الجذعُ الصورةَ والأصلَ معًا بقيتا قراءتين.",
        "- أل الموصولةُ لا تُردّ هنا: الجذعُ يقرؤها أصلًا (`Al.silent`).",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    text = render()
    if "--check" in sys.argv[1:]:
        if TARGET.read_text(encoding="utf-8") != text:
            print("QIRAA_INDEX.md قديم: شغّل python tools/gen_qiraa_index.py")
            return 1
        print("QIRAA_INDEX.md مطابق")
        return 0
    TARGET.write_text(text, encoding="utf-8")
    print("كُتب QIRAA_INDEX.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
