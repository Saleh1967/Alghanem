"""فهرسُ الأسلوب (الخبرُ والإنشاء) على درجات الترخيص التدريجيّ (USLUB_INDEX.md) من `slge.uslub` وMASAQ.

القياسُ على `masaq-shibh.json.gz` بشهادات البوّابة: (١) لَا الناهيةُ (وسمُ MASAQ «حرف جزم») ولَا النافيةُ
(«حرف غير عامل») مرجعٌ محجوبٌ لقانون الخانة — القارئُ يفصلهما بخانة آخر الفعل التالي؛ (٢) فعلُ الأمر
(وسمُ «فعل أمر») يُقرأ أمرًا (إنشاءً)؛ (٣) ما بعد حرف الاستفهام يُقرأ استفهامًا. ويُعدّ الصدقُ والكذبُ
(الخبرُ) على كلّ ما قُرئ.
"""

from __future__ import annotations

import gzip
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from slge.uslub import LA, TOOLS, truth_apt, uslub

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "USLUB_INDEX.md"
DATA = ROOT / "tests" / "data"
Word = tuple[tuple[str, str], ...]
PRE_TAGS = ("IMPERF_PREF", "CV_PREF", "IV1S", "IV1P", "IV2MP", "IV3MS", "IV3MP", "IV3FS", "DET")
SUBJ_TAGS = ("SUBJ_PRON", "PVSUFF_SUBJ", "IVSUFF_SUBJ", "CVSUFF_SUBJ", "OBJ_PRON", "PVSUFF_DO",
             "IVSUFF_DO", "EMPHATIC_NUN", "PROTECT_NUN")


def _cells(r: dict[str, Any]) -> Word:
    pre = [(a, b) for t, cs in r["pre"] for a, b in cs if t in PRE_TAGS]
    return (*pre, *((a, b) for a, b in r["stem"]))


def _bare(r: dict[str, Any]) -> bool:
    return not any(t.startswith(SUBJ_TAGS) for t, _ in r["suf"])


def contexts() -> list[tuple[str, str, Word, Word, Word | None]]:
    """(الباب، وسمُ MASAQ، السابق، الكلمة، التالي): ما بعد لَا، وفعلُ الأمر، وما بعد حرف الاستفهام."""

    with gzip.open(DATA / "masaq-shibh.json.gz", "rt", encoding="utf-8") as f:
        rows: list[dict[str, Any]] = json.load(f)["rows"]
    by: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for r in rows:
        by[str(r["ref"])].append(r)
    out: list[tuple[str, str, Word, Word, Word | None]] = []
    for verse in by.values():
        verse.sort(key=lambda r: int(str(r["pos"])))
        for i, r in enumerate(verse):
            nxt = verse[i + 1] if i + 1 < len(verse) else None
            adjacent = nxt is not None and int(str(nxt["pos"])) == int(str(r["pos"])) + 1
            role = str(r["role"])
            if role == "فعل أمر" and _bare(r):
                out.append(("أمر", "إنشاء", (), _cells(r), None))
            if not adjacent or nxt is None:
                continue
            after = verse[i + 2] if i + 2 < len(verse) else None
            after_cells = _cells(after) if after else None
            is_la = r["stem"] == [["ل", "فتح"], ["ا", "سكون"]]
            if is_la and str(nxt["tag"]) == "IV" and _bare(nxt):
                tag = {"حرف جزم": "نهي (إنشاء)", "حرف غير عامل": "نفي (خبر)"}.get(role)
                if tag:
                    out.append(("لَا", tag, LA, _cells(nxt), after_cells))
            elif role == "حرف استفهام":
                out.append(("استفهام", "إنشاء", tuple((a, b) for a, b in r["stem"]), _cells(nxt),
                            after_cells))
    return out


def measure() -> dict[str, object]:
    cs = contexts()
    read: Counter[tuple[str, str, str]] = Counter()
    truth: Counter[tuple[str, bool]] = Counter()
    for bab, tag, prev, w, nxt in cs:
        u = uslub(prev, w, nxt)
        read[(bab, tag, u)] += 1
        truth[(tag, truth_apt(u))] += 1
    return {"n": len(cs), "read": read, "truth": truth}


def _w(w: Word) -> str:
    return "".join(a for a, _ in w)


def render() -> str:
    m = measure()
    read: Counter[tuple[str, str, str]] = m["read"]  # type: ignore[assignment]
    la_ok = read[("لَا", "نهي (إنشاء)", "نهي")] + read[("لَا", "نفي (خبر)", "خبر")]
    la_all = sum(v for (b, _, _), v in read.items() if b == "لَا")
    la_wrong = read[("لَا", "نهي (إنشاء)", "خبر")] + read[("لَا", "نفي (خبر)", "نهي")]
    amr_ok = read[("أمر", "إنشاء", "أمر")]
    amr_all = sum(v for (b, _, _), v in read.items() if b == "أمر")
    ist_ok = read[("استفهام", "إنشاء", "استفهام")]
    ist_all = sum(v for (b, _, _), v in read.items() if b == "استفهام")
    lines = [
        "# فهرسُ الأسلوب — الخبرُ والإنشاء — على درجات الترخيص التدريجيّ",
        "",
        "مولَّدٌ بـ`python tools/gen_uslub_index.py` من `src/slge/uslub.py`؛ لا يُحرَّر باليد. "
        "البرهانُ: "
        "`formal/Slge/Uslub.lean`.",
        "",
        "## د٤ الخانة — الأسلوبُ مقروءٌ لا مكتوب", "",
        "الإنشاءُ طلبيٌّ: أمرٌ بصيغته، نهيٌ بلَا والجزم، استفهامٌ بأداته (أَ، هَلْ) أو اسمه (جدول "
        "`Istifham`)، نداءٌ بأداته (جدول `Nida`)، تمنٍّ بلَيْتَ، ترجٍّ بلَعَلَّ؛ وغيرُ طلبيّ: "
        "تعجّبٌ بمَا أَفْعَلَ "
        "ومنصوبٍ بعده، مدحٌ وذمٌّ بنِعْمَ وبِئْسَ. وما سواه من فعلٍ أو مبتدأٍ خبرٌ (`uslub`). "
        "الأدواتُ جدولٌ "
        f"حاصرٌ ({len(TOOLS)}) مرخَّصٌ (`tools_licensed`) من جدول الربط بعمله (`tools_in_rawabit`).",
        "",
        "| الأداة | الخانات | الأسلوب |", "|---|---|---|",
        *[f"| {n} | `{_w(cs)}` | {u} |" for n, cs, u in TOOLS],
        "",
        "## د٨ الحدّ — الصدقُ والكذبُ للخبر وحده، والفرقُ خانة", "",
        "`truthApt u = true ↔ u = khabar` (`truth_iff_khabar`): الإنشاءُ كلُّه محرومٌ من الصدق "
        "والكذب "
        "بالتعريف — وما بُرهن أنّ القراءةَ من الخانة: الأمرُ إنشاءٌ لكلّ قالبِ أمرٍ ولكلّ جذرٍ "
        "مهما كان ما "
        "قبله وما بعده (`amr_is_insha`)؛ ولَا تفصل النهيَ (إنشاء) عن النفي (خبر) **بخانة آخر "
        "الفعل وحدها** "
        "لكلّ قالبِ مضارعٍ وصدرٍ وجذر: لَا تَكْذِبْ إنشاءٌ ولَا تَكْذِبُ خبرٌ "
        "(`la_splits_by_last_state`؛ "
        "المجزومُ ليس على قالب ماضٍ `sukun_present_not_past`، والنهيُ لا يقع إلّا على مضارع "
        "`nahy_only_present`)؛ ومَا أَفْعَلَ تعجّبٌ إن نُصب ما بعده وخبرٌ (نفيٌ) إن رُفع، لكلّ "
        "جذرٍ ولكلّ اسم "
        "(`ma_afala_splits_by_next_case`). الشواهدُ: `uslub_witnesses`.",
        "",
        "## القياس على MASAQ", "",
        f"على {m['n']:,} سياقًا من شريحة شبه الجملة بشهادات البوّابة:",
        "",
        f"- لَا + مضارعٍ بلا لاحقة ({la_all}): وسمُ MASAQ (حرف جزم = نهي، حرف غير عامل = نفي) "
        "مرجعٌ محجوب؛ "
        f"القارئُ يوافقه بخانة الآخر في {la_ok}، ويخالفه في {la_wrong}، والباقي لا يُقرأ.",
        f"- فعلُ الأمر بلا لاحقة ({amr_all}): يُقرأ أمرًا (إنشاءً) في {amr_ok}.",
        f"- ما بعد حرف الاستفهام ({ist_all}): يُقرأ استفهامًا في {ist_ok} (الهمزةُ المتّصلةُ بما بعدها "
        "تُقرأ من جذع الكلمة التالية لا من حرفٍ منفصل — باسمها).",
        "",
        "| الباب | وسمُ MASAQ | القارئ | العدد |", "|---|---|---|---|",
        *[f"| {b} | {t} | {u} | {v:,} |" for (b, t, u), v in read.most_common()],
        "",
        "## ما لا تقرؤه الخانة — باسمه", "",
        "- المعتلُّ المجزومُ بحذف الآخر (لَا تَدْعُ) والأجوفُ (كُنْ، لَا تَكُنْ) والمجزومُ بحذف "
        "النون "
        "(لَا تَفْعَلُوا): على غير قالبٍ — دَينُ الإعلال واللواحق؛ وأمرُ أَفْعَلَ (أَعْرِضْ) غيرُ "
        "مودَعٍ فيُقرأ "
        "بحالة الآخر مضارعًا خبرًا.",
        "- الهمزةُ المتّصلةُ (أَتَكْتُبُ) جذعٌ واحدٌ في MASAQ: تُقرأ بصدر الكلمة لا بأداةٍ قبلها.",
        "- القسمُ وصيغُ العقود والعرضُ والتحضيض: معجمٌ ومقام؛ والخبرُ الذي يُراد به الإنشاء "
        "(غَفَرَ اللهُ لك) "
        "معنًى لا خانة.",
        "- الحصرُ المُرسَل في هذه الرسالة جملةٌ فعليّةٌ بأجناسٍ مكتوبةٍ باليد (`Genus`) وإجهادٌ "
        "يقارن الدالّةَ "
        "بنفسها — لم يُدخَل منه شيء؛ والمطلوبُ (الخبرُ والإنشاء) دخل على الخانات.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    text = render()
    if "--check" in sys.argv:
        if TARGET.read_text(encoding="utf-8") != text:
            sys.stderr.write("USLUB_INDEX.md غيرُ مطابق؛ شغّل tools/gen_uslub_index.py\n")
            return 1
        sys.stdout.write("USLUB_INDEX.md مطابق\n")
        return 0
    TARGET.write_text(text, encoding="utf-8")
    sys.stdout.write("كُتب USLUB_INDEX.md\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
