"""فهرسُ المخصّص (MUKHASSAS_INDEX.md): الشجرةُ كما هي، والربطُ بالرسم، والقابليّاتُ الموروثة، "
"والحكمُ على
شواهد، ثمّ قياسٌ على مودَع المصحف.

(١) الشجرة: الأعدادُ بالمستوى، وكم عقدةً رُبط عنوانُها بجذرٍ في المقاييس بالرسم، وكم جذرًا
متمايزًا. (٢) الكتبُ
(المستوى الأوّل) وحجمُ قابليّاتها الموروثة. (٣) الشواهد: مشي/جري على أبواب المشي وكتاب خلق
الإنسان وكتاب
النخل. (٤) على `corpus-certificates.json.gz`: جذورُ القراءات الفعليّة الأولى (جهتُها فعل)
— كم جذرًا متمايزًا
يشهد له كتابٌ واحدٌ على الأقلّ في المخصّص (قابليّةٌ لجنسٍ ما)، وكم لا يشهد له شيء؛ الرقمُ يُنشر كما هو.
"""

from __future__ import annotations

import gzip
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from slge.jidh import jidh
from slge.maqayis import rank as rank_maqayis
from slge.maqayis import roots_of
from slge.mukhassas import BOOKS, NODES, code_of_root, judge_in, title_of
from slge.wujud import FIL, ont_of_reading

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "MUKHASSAS_INDEX.md"
DATA = ROOT / "tests" / "data"
WITNESSES: tuple[tuple[int, tuple[str, str, str], str], ...] = (
    (163, ("م", "ش", "ي"), "أبواب المشي ← مشي"),
    (1, ("م", "ش", "ي"), "كتاب خلق الإنسان ← مشي"),
    (979, ("ج", "ر", "ي"), "كتاب النخل ← جري"),
    (617, ("م", "ش", "ي"), "كتاب السباع ← مشي"),
    (664, ("ج", "ر", "ي"), "كتاب الحشرات ← جري"),
)


def corpus_forms() -> list[tuple[tuple[str, str], ...]]:
    with gzip.open(DATA / "corpus-certificates.json.gz", "rt", encoding="utf-8") as f:
        d: dict[str, Any] = json.load(f)
    return [tuple((a, b) for a, b in x["cells"]) for x in d["forms"]]


def measure() -> dict[str, Any]:
    by_level = Counter(n[1] for n in NODES)
    linked = sum(1 for n in NODES if n[4])
    distinct = {c for n in NODES for c in n[4]}
    books = sorted(((b, len(rs)) for b, rs in BOOKS.items()), key=lambda x: -x[1])
    verb_roots: Counter[int] = Counter()
    unlinked = 0
    for w in corpus_forms():
        rs = rank_maqayis(jidh(w))
        if not rs or ont_of_reading(rs[0]) != FIL:
            continue
        codes = [c for r in roots_of(rs[0]) if (c := code_of_root(r)) is not None]
        if not codes:
            unlinked += 1
            continue
        verb_roots[codes[0]] += 1
    attested = {c for c in verb_roots if any(c in rs for rs in BOOKS.values())}
    return {"by_level": by_level, "linked": linked, "distinct": len(distinct), "books": books,
            "verb_roots": verb_roots, "attested": attested, "unlinked": unlinked}


def render() -> str:
    m = measure()
    bl = m["by_level"]
    vr: Counter[int] = m["verb_roots"]
    att = m["attested"]
    tok_all = sum(vr.values())
    tok_att = sum(n for c, n in vr.items() if c in att)
    lines = [
        "# فهرسُ المخصّص — الأجناسُ والقابليّاتُ معلوماتٍ سابقةً، والحكمُ بشاهد",
        "",
        "مولَّدٌ بـ`python tools/gen_mukhassas_index.py` من `src/slge/mukhassas.py`؛ لا "
        "يُحرَّر باليد. البرهانُ: "
        "`formal/Slge/Mukhassas.lean`؛ الجدولُ `formal/Slge/MukhassasTable.lean` مولَّدٌ من "
        "المختوم "
        "`tests/data/openiti-mukhassas.txt.gz` (`tools/deposit_mukhassas.py --check`؛ المخصّص "
        "لابن سيده، "
        "OpenITI، CC BY-NC-SA 4.0). أوّلُ وحدةٍ في طبقة «الحكم» فوق سُلَّم الترخيص.",
        "",
        "## الشجرة كما هي", "",
        f"{len(NODES):,} عقدةً بترتيب المصدر: المستوى الأوّل {bl[1]}، الثاني {bl[2]}، الثالث "
        f"{bl[3]:,} — "
        "بلا إعادة تصنيف (كتبٌ نحويّةٌ وعلاماتُ أسفارٍ على المستوى الأوّل تبقى باسمها). "
        "مبرهَن: المعرّفاتُ مواضع، "
        "الأبُ أسبقُ وأدنى مستوًى وكتابُ الابن كتابُ أبيه، المستوى الأوّل وحدَه بلا أب، كتابُ "
        "كلّ عقدةٍ من المستوى "
        "الأوّل (`ids_are_positions`، `parent_lt`، `parent_level_lt`، `level_one_iff_no_parent`، "
        "`book_is_level_one`، `level_counts`).",
        "",
        "## الربطُ بالرسم (معلَن)", "",
        f"رُبط عنوانُ {m['linked']:,} عقدةً من {len(NODES):,} بجذرٍ واحدٍ فأكثر في جدول "
        f"المقاييس — {m['distinct']} "
        "جذرًا متمايزًا. القاعدة: حذفُ السوابق واللواحق، ثلاثةُ حروفٍ أو أربعةٌ بألفٍ غيرِ "
        "أولى، الألفُ والواوُ والياءُ "
        "معتلّة، ألفاظُ الهيكل (كتاب/باب/فصل/ذكر/أسماء…) لا تُربط؛ النصُّ غيرُ مشكول فالرابطُ "
        "رسمٌ لا ترخيص.",
        "",
        "## الكتبُ وقابليّاتُها الموروثة", "",
        "| # | الكتاب | القابليّات |", "|---|---|---|",
    ]
    for b, n in m["books"][:25]:
        lines.append(f"| {b} | {title_of(b)} | {n} |")
    lines += [
        "",
        f"الكتبُ {len(BOOKS)}؛ القابليّةُ الموروثة للكتاب اتّحادُ جذور عناوين ما تحته "
        f"**بالتعريف** (`capsUnder`) — "
        "لا قابليّةَ بلا عنوانٍ شاهد، ولا تُستنتج من غياب.",
        "",
        "## الحكمُ على شواهد (`judgeIn`، مبرهَن على الشواهد الثلاثة الأولى)", "",
        "| الكتاب ← الجذر | الحكم | الشاهد |", "|---|---|---|",
    ]
    for b, r, label in WITNESSES:
        code = code_of_root(r)
        assert code is not None
        g, w = judge_in(b, code)
        lines.append(f"| {label} | {g} | {title_of(w) if w is not None else '—'} |")
    lines += [
        "",
        "«معلومة» لا «ممتنع»: الغيابُ ليس امتناعًا (المادّة ١٦). المشيُ عند ابن سيده كتابٌ "
        "قائمٌ (أبواب المشي) لا بابٌ "
        "تحت الإنسان ولا السباع؛ فنسبةُ المشي إلى الإنسان أو السبع لا شاهدَ لها **في هذه "
        "الشجرة بالرسم** حتى "
        "تُربط الكتبُ بعضُها ببعض — دينٌ باسمه.",
        "",
        "## على مودَع المصحف", "",
        f"القراءاتُ الفعليّة الأولى (جهتُها فعل) ذاتُ جذرٍ في المقاييس: {tok_all:,} صورةً على "
        f"{len(vr):,} جذرًا "
        f"متمايزًا ({m['unlinked']:,} صورةً فعليّة بلا جذرٍ في الجدول). يشهد لجذرها كتابٌ واحدٌ "
        f"على الأقلّ في "
        f"المخصّص: **{len(att):,} من {len(vr):,} جذرًا** ({100 * len(att) / len(vr):.1f}%)، "
        f"{tok_att:,} من {tok_all:,} صورة ({100 * tok_att / tok_all:.1f}%).",
        "",
        "## ما ليس هنا — باسمه", "",
        "- الشهادةُ هنا لـ(كتاب، جذر) لا لـ(مسنَدٍ إليه، مسنَد): ربطُ المسنَد إليه في النصّ "
        "بعقدةٍ في الشجرة يحتاج "
        "جذرَه بالرسم من العنوان (لم يُنفَّذ)، والمسنَدُ جذرَ الفعل (موجود).",
        "- شاهدٌ سالبٌ (الامتناع) لا مصدرَ له إلّا مجاز القرآن المختوم — لم يُقرأ بعد.",
        "- أسماءُ الكتب غيرُ المشكولة لا تدخل البوّابة؛ الربطُ بالرسم «مطابَقٌ بالرسم» لا "
        "«مرخَّص».",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    text = render()
    if "--check" in sys.argv:
        if TARGET.read_text(encoding="utf-8") != text:
            sys.stderr.write("MUKHASSAS_INDEX.md غيرُ مطابق؛ شغّل tools/gen_mukhassas_index.py\n")
            return 1
        sys.stdout.write("MUKHASSAS_INDEX.md مطابق\n")
        return 0
    TARGET.write_text(text, encoding="utf-8")
    sys.stdout.write("كُتب MUKHASSAS_INDEX.md\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
