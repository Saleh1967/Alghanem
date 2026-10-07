"""فهرسُ الإعلال والإبدال على المودَع (ILAL_INDEX.md): ما يقرؤه النزولُ بالقواعد ممّا لم تقرأه القوالبُ
مباشرةً.

القياسُ على `tests/data/corpus-certificates.json.gz` (18,179 صورةً مشهودةً من المصحف): لكلّ صورةٍ قراءاتُ
`jidh` التي سلسلتُها غيرُ خالية (أصلٌ يصعد بالإعلال إلى الجذع)، وعدُّ الصور التي لا تُقرأ إلّا بالإعلال،
وتوزيعُ
القواعد وأطوال السلاسل. ثمّ على `masaq-shibh.json.gz`: هل القسمةُ المحجوبة بين قراءات الإعلال؟
"""

from __future__ import annotations

import gzip
import json
import sys
from collections import Counter
from itertools import pairwise
from pathlib import Path
from typing import Any

from slge.ilal import RULES, ascend
from slge.jidh import jidh

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "ILAL_INDEX.md"
DATA = ROOT / "tests" / "data"
Word = tuple[tuple[str, str], ...]
NAMES = {
    "QALB_AYN": "قلبُ عين الأجوف ألفًا", "HADHF_AYN_U": "حذفُ العين وضمُّ الفاء",
    "HADHF_AYN_I": "حذفُ العين وكسرُ الفاء", "NAQL": "نقلُ حركة العين",
    "QALB_LAM": "قلبُ لام الناقص ألفًا", "HADHF_LAM": "حذفُ اللام قبل واو الجماعة",
    "HADHF_WAW": "حذفُ واو المثال", "HAMZA_MADD": "الهمزةُ مدًّا",
    "TA_TTA": "تاءُ الافتعال طاءً", "TA_DAL": "تاءُ الافتعال دالًا", "FA_TA": "فاءُ الافتعال تاءً",
    "WAW_YA": "الواوُ ياءً بعد كسرة", "YA_WAW": "الياءُ واوًا بعد ضمّة",
}


def corpus_forms() -> list[Word]:
    with gzip.open(DATA / "corpus-certificates.json.gz", "rt", encoding="utf-8") as f:
        d: dict[str, Any] = json.load(f)
    return [tuple((a, b) for a, b in x["cells"]) for x in d["forms"]]


def ibdal_law(forms: list[Word]) -> dict[str, Any]:
    """قانونُ الإبدال على المودَع: ما بعد حرف الإطباق الساكن (ص ض ط ظ) وما بعد د/ذ/ز الساكنة، تاءً أو
    بدلَها، وما بعد و/ي الساكنة تاءً — عدًّا لا حكمًا؛ والصورُ التي بقيت فيها التاءُ مسمّاة."""

    n: Counter[str] = Counter()
    kept: set[str] = set()
    for w in forms:
        for (a, sa), (b, _) in pairwise(w):
            if sa != "سكون":
                continue
            if a in "صضطظ":
                n["itbaq_ta" if b == "ت" else "itbaq_tta" if b == "ط" else "itbaq_other"] += 1
            elif a in "دذز":
                n["dzz_ta" if b == "ت" else "dzz_dal" if b == "د" else "dzz_other"] += 1
            elif a in "وي":
                n["wy_ta" if b == "ت" else "wy_other"] += 1
            if a in "صضطظدذز" and b == "ت":
                kept.add("".join(ch for ch, _ in w))
    return {**n, "kept": sorted(kept)}


def measure() -> dict[str, Any]:
    forms = corpus_forms()
    only_ilal = with_ilal = 0
    rules: Counter[str] = Counter()
    lengths: Counter[int] = Counter()
    checked = 0
    for w in forms:
        rs = jidh(w)
        il = [r for r in rs if r.ilal]
        if il:
            with_ilal += 1
            if len(il) == len(rs):
                only_ilal += 1
        for r in il:
            lengths[len(r.ilal)] += 1
            for rule, _ in r.ilal:
                rules[rule] += 1
            assert ascend(r.ilal, (*r.asl, *r.suf)) == (*r.stem, *r.suf)  # jidh_ascends على المودَع
            checked += 1
    with gzip.open(DATA / "masaq-shibh.json.gz", "rt", encoding="utf-8") as f:
        rows: list[dict[str, Any]] = json.load(f)["rows"]
    m_total = m_hit = 0
    for row in rows:
        allpre = tuple((a, b) for _, cs in row["pre"] for a, b in cs)
        stem = tuple((a, b) for a, b in row["stem"])
        suf = tuple((a, b) for _, cs in row["suf"] for a, b in cs)
        if not stem:
            continue
        rs = jidh(allpre + stem + suf)
        il = [r for r in rs if r.ilal]
        if not il or len(il) != len(rs):
            continue
        m_total += 1
        if any(r.suf == suf for r in il):
            m_hit += 1
    return {"forms": len(forms), "with": with_ilal, "only": only_ilal, "rules": rules,
            "lengths": lengths, "checked": checked, "m_total": m_total, "m_hit": m_hit,
            "law": ibdal_law(forms)}


def render() -> str:
    m = measure()
    n, law = m["forms"], m["law"]
    lines = [
        "# فهرسُ الإعلال والإبدال على المودَع",
        "",
        "مولَّدٌ بـ`python tools/gen_ilal_index.py` من `src/slge/ilal.py` و`src/slge/jidh.py`؛ لا "
        "يُحرَّر "
        "باليد. البرهانُ: `formal/Slge/Ilal.lean` (هندسةٌ عكسيّةٌ لـ`A116.Ilal` في الغانم).",
        "",
        "## الجبرُ المغلق صعودًا ونزولًا", "",
        "القاعدةُ صعودٌ `up` من الأصل إلى الصورة في نافذة، ونزولٌ `down` من الصورة إلى الأصول التي "
        "يصعد "
        "كلٌّ منها إلى الصورة بعينها: مبرهَنٌ أنّ النزولَ عكسُ الصعود (`undo_sound`) ولا أصلَ يفوت "
        "(`undo_complete`)، وأنّ القلبَ والنقلَ والحذفَ والإبدالَ تحفظ الترخيصَ عبر الجسر إلى أدوات "
        "الغانم "
        "بعينها (`qalbAyn_closed`، `naql_closed`، `hadhfWaw_closed`، `ibdal_closed`، "
        "`qalbLam_closed`، "
        "`hadhfLam_closed`)، وأنّ أصلَ حذف العين غيرُ مرخَّصٍ فالحذفُ ملزَم (`hadhfAyn_forced`). والقارئُ "
        "ينزل حتى خطوتين وكلُّ ما ينزل إليه يصعد بسلسلته (`descend_ascends`، `jidh_ascends`)، وما "
        "صعد "
        "بخطوةٍ في موضعه ينزل (`descend_complete`، `jidh_complete_ilal`).",
        "",
        "## الرقمُ على المودَع نفسه", "",
        f"{n:,} صورةً مشهودةً من المصحف: صورٌ لها قراءةٌ بالإعلال {m['with']:,} "
        f"({100 * m['with'] / n:.1f}%)، منها لا تُقرأ إلّا بالإعلال {m['only']:,} "
        f"({100 * m['only'] / n:.1f}%). كلُّ قراءةٍ منها ({m['checked']:,}) صعد أصلُها بسلسلتها إلى "
        "جذعها بعينه (فُحص على المودَع كما هو مبرهَن).",
        "",
        "| القاعدة | ظهورُها في القراءات |", "|---|---|",
    ]
    for rule in RULES:
        lines.append(f"| {NAMES[rule]} (`{rule}`) | {m['rules'][rule]:,} |")
    lines += [
        "",
        f"أطوالُ السلاسل: خطوةٌ {m['lengths'][1]:,}، خطوتان {m['lengths'][2]:,}.",
        "",
        "## قانونُ الإبدال على المودَع — عدًّا لا حكمًا", "",
        "الردُّ بسجلّ الغانم بعينه مبرهَنٌ (`apply_roundtrip`، `apply_roundtrip_a116`: سجلُّ SLGE هو "
        "سجلُّ الغانم عبر الجسر)، وإبدالُ تاء الافتعال وفائه لا يغيّر الترخيصَ الثلاثيَّ "
        f"(`ibdal_ternary`). وعلى {n:,} صورةً: بعد حرف الإطباق الساكن تاءٌ "
        f"{law.get('itbaq_ta', 0):,} وطاءٌ {law.get('itbaq_tta', 0):,}؛ بعد د/ذ/ز الساكنة تاءٌ "
        f"{law.get('dzz_ta', 0):,} ودالٌ {law.get('dzz_dal', 0):,}؛ بعد و/ي الساكنة تاءٌ "
        f"{law.get('wy_ta', 0):,} (من {law.get('wy_other', 0) + law.get('wy_ta', 0):,}). "
        "«لا تبقى التاءُ بعد الإطباق» رقمٌ هنا لا بديهيّة؛ والتاءُ الباقيةُ بعد المطبَق والدال وأخواتها "
        f"في المودَع تاءُ فاعلٍ أو خطابٍ بعد لام الكلمة لا تاءُ افتعال ({len(law['kept'])} رسمًا: "
        + "، ".join(law["kept"]) + ") — فالقانونُ على تاء الافتعال وحدَها، وبهذا الشرط المعلَن "
        "لا نقضَ له في المودَع.",
        "",
        "## القياس على قسمة MASAQ المحجوبة", "",
        f"على {m['m_total']:,} كلمةً لا تُقرأ إلّا بالإعلال: لاحقةُ المرجع بين قراءاتها {m['m_hit']:,} "
        f"({100 * m['m_hit'] / max(m['m_total'], 1):.1f}%).",
        "",
        "## ما لا يُقرأ بعدُ — باسمه", "",
        "- المبنيُّ للمجهول من الأجوف (قِيلَ ← قُوِلَ) والمجزومُ منه (يَقُلْ ← يَقُوْلْ) ليسا من القواعد الاثنتي "
        "عشرة.",
        "- الإعلالُ بثلاث خطواتٍ فأكثر، والإدغامُ الرسميُّ بعد إبدال فاء الافتعال (اتَّصَلَ).",
        "- الأصلُ الواويُّ واليائيُّ قراءتان على الخانة (قَوَلَ/قَيَلَ): القرينةُ المعجميّةُ تفصل ولا تُحشر "
        "هنا.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    text = render()
    if "--check" in sys.argv:
        if TARGET.read_text(encoding="utf-8") != text:
            sys.stderr.write("ILAL_INDEX.md غيرُ مطابق؛ شغّل tools/gen_ilal_index.py\n")
            return 1
        sys.stdout.write("ILAL_INDEX.md مطابق\n")
        return 0
    TARGET.write_text(text, encoding="utf-8")
    sys.stdout.write("كُتب ILAL_INDEX.md\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
