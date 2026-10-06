"""فهرسُ الطلب (صورُ الأمر) على درجات الترخيص التدريجيّ (TALAB_INDEX.md) من `slge.talab` وMASAQ.

القياسُ بشهادات البوّابة: (١) فعلُ الأمر (وسمُ «فعل أمر») واسمُ فعل الأمر في `masaq-shibh.json.gz`: ما
يقرؤه `talab` صيغةً أو اسمَ فعل؛ (٢) لامُ الأمر في `masaq-jazm.json` (الأداةُ «ل حرف جزم»): علامةُ الجزم
عند MASAQ على كلّ موضع — `lam_amr_jazm` مقيسًا — وسوابقُ اللام (الواو والفاء) التي تُسكِّنها.
"""

from __future__ import annotations

import gzip
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from slge.talab import ISM_FIL, talab

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "TALAB_INDEX.md"
DATA = ROOT / "tests" / "data"
Word = tuple[tuple[str, str], ...]
PRE_TAGS = ("CV_PREF", "IMPERF_PREF")
SUBJ_TAGS = ("SUBJ_PRON", "PVSUFF_SUBJ", "IVSUFF_SUBJ", "CVSUFF_SUBJ", "OBJ_PRON", "PVSUFF_DO",
             "IVSUFF_DO", "EMPHATIC_NUN", "PROTECT_NUN")


def _cells(r: dict[str, Any]) -> Word:
    pre = [(a, b) for t, cs in r["pre"] for a, b in cs if t in PRE_TAGS]
    return (*pre, *((a, b) for a, b in r["stem"]))


def amr_rows() -> list[tuple[str, Word]]:
    """(الدورُ عند MASAQ، الخانات) لأفعال الأمر بلا لاحقة وأسماء فعل الأمر."""

    with gzip.open(DATA / "masaq-shibh.json.gz", "rt", encoding="utf-8") as f:
        rows: list[dict[str, Any]] = json.load(f)["rows"]
    out: list[tuple[str, Word]] = []
    for r in rows:
        role = str(r["role"])
        bare = not any(t.startswith(SUBJ_TAGS) for t, _ in r["suf"])
        if role == "فعل أمر" and bare:
            out.append((role, _cells(r)))
        elif role == "اسم فعل أمر":
            out.append((role, tuple((a, b) for a, b in r["stem"])))
    return out


def lam_rows() -> list[tuple[str, tuple[str, ...]]]:
    """(علامةُ الإعراب عند MASAQ، السوابق) لكلّ موضعٍ أداتُه لامُ الأمر."""

    rows = json.loads((DATA / "masaq-jazm.json").read_text(encoding="utf-8"))
    return [(str(r["marker"]), tuple(r["prefixes"])) for r in rows if r["tool"] == ["ل", "حرف جزم"]]


def measure() -> dict[str, object]:
    read: Counter[tuple[str, str]] = Counter()
    for role, w in amr_rows():
        read[(role, talab((), w) or "—")] += 1
    markers: Counter[str] = Counter()
    before: Counter[str] = Counter()
    for marker, pre in lam_rows():
        markers[marker] += 1
        before["بعد الواو أو الفاء" if pre and pre[0] in ("و", "ف") else "في الصدر"] += 1
    return {"read": read, "markers": markers, "before": before, "lam_n": len(lam_rows())}


def render() -> str:
    m = measure()
    read: Counter[tuple[str, str]] = m["read"]  # type: ignore[assignment]
    markers: Counter[str] = m["markers"]  # type: ignore[assignment]
    before: Counter[str] = m["before"]  # type: ignore[assignment]
    amr_all = sum(v for (r, _), v in read.items() if r == "فعل أمر")
    lines = [
        "# فهرسُ الطلب — صورُ الأمر — على درجات الترخيص التدريجيّ",
        "",
        "مولَّدٌ بـ`python tools/gen_talab_index.py` من `src/slge/talab.py`؛ لا يُحرَّر باليد. "
        "البرهانُ: "
        "`formal/Slge/Talab.lean`.",
        "",
        "## د٤ الخانة — صورُ الأمر الأربع مقروءة", "",
        "الصيغةُ (قالبُ الأمر)، ولامُ الأمر على المضارع المجزوم (لِيَكْتُبْ؛ وبعد الواو والفاء "
        "تسكن: "
        "وَلْيَكْتُبْ)، والمصدرُ النائب (ضَرْبًا في الصدر)، واسمُ الفعل من جدوله الحاصر "
        f"({len(ISM_FIL)}: `ismFil_licensed`) — يقرؤها `talab` (`four_forms_witnesses`).",
        "",
        "| اسمُ الفعل | الخانات |", "|---|---|",
        *[f"| {n} | `{''.join(a for a, _ in cs)}` |" for n, cs in ISM_FIL],
        "",
        "## د٨ الحدّ — الصيغةُ للمخاطب واللامُ لكلّ شخص، والأمرُ ليس نهيًا", "",
        "لامُ الأمر على المضارع بصدوره تصل الغائبَ والمتكلّم لكلّ قالبِ مضارعٍ ولكلّ جذرٍ لا ألفَ "
        "فيه، وتُقرأ "
        "لامًا (`lam_reaches_every_person`)، وتجزم: آخرُها ساكنٌ أبدًا (`lam_amr_jazm`)، وتحفظ "
        "الترخيص "
        "(`lam_amr_licensed`)؛ والصيغةُ للمخاطب وحده (`Jiha.amr_is_mukhatab`). **الأمرُ بالشيء "
        "ليس نهيًا عن "
        "ضدّه على الخانة**: لَا قبل صيغة الأمر لا تقلبها نهيًا لكلّ قالبٍ ولكلّ جذر "
        "(`la_before_amr_stays_amr`)، "
        "والنهيُ لا يُقرأ إلّا بلَا قبل مضارع (`nahy_requires_la`)، وصيغةُ الأمر لا تُقرأ نهيًا "
        "مهما كان ما "
        "قبلها وما بعدها (`amr_never_reads_nahy`) — فالتحويلُ عمليّتان: إدخالُ لَا وتغييرُ "
        "القالب؛ والضدُّ معنًى.",
        "",
        "## الإلزامُ ليس في الخانة — معلَن", "",
        "صيغةُ الأمر من الجذر الواحد قائمةُ خاناتٍ واحدةٌ لكلّ حكم (وجوبٍ أو ندبٍ أو إباحة)، فلا "
        "دالّةَ من الخانة "
        "تفصل الأحكام: الجزمُ والإلزامُ من القرائن لا من اللفظ المجرّد — بديهيّةٌ لا تُسمّى "
        "برهانًا.",
        "",
        "## القياس على MASAQ", "",
        f"- فعلُ الأمر بلا لاحقة ({amr_all}) واسمُ فعل الأمر: ما يقرؤه `talab` في الجدول أدناه.",
        f"- لامُ الأمر ({m['lam_n']} موضعًا في شريحة الجزم): علامةُ MASAQ "
        + "، ".join(f"{k} {v}" for k, v in markers.most_common())
        + " — `lam_amr_jazm` مقيسًا (الجزمُ بالسكون أو بالحذف: كلُّها جزم)؛ وموضعُ اللام: "
        + "، ".join(f"{k} {v}" for k, v in before.most_common()) + ".",
        "",
        "| دورُ MASAQ | القارئ | العدد |", "|---|---|---|",
        *[f"| {r} | {s} | {v:,} |" for (r, s), v in read.most_common()],
        "",
        "## ما لا تقرؤه الخانة — باسمه", "",
        "- أمرُ أَفْعَلَ (أَعْرِضْ) غيرُ مودَعٍ، والأجوفُ (قُلْ، كُنْ) والناقصُ (اُدْعُ) على غير "
        "قالب: دَينُ "
        "القوالب والإعلال.",
        "- المصدرُ النائبُ عن الأمر لا يفرّقه القارئُ عن المفعول المطلق إلّا بالصدر (لا فعلَ "
        "قبله): معنًى "
        "ومقام.",
        "- أسماءُ الفعل بمعنى الأمر من الظروف والجارّ (عَلَيْكَ، إِلَيْكَ، مَكَانَكَ): معجم.",
        "- الحصرُ المُرسَل في هذه الرسالة عمومٌ وخصوصٌ بأنواعٍ مكتوبةٍ باليد وإجهادٌ يقارن "
        "الدالّةَ بنفسها — "
        "لم يُدخَل منه شيء؛ والمطلوبُ (الطلب) دخل على الخانات.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    text = render()
    if "--check" in sys.argv:
        if TARGET.read_text(encoding="utf-8") != text:
            sys.stderr.write("TALAB_INDEX.md غيرُ مطابق؛ شغّل tools/gen_talab_index.py\n")
            return 1
        sys.stdout.write("TALAB_INDEX.md مطابق\n")
        return 0
    TARGET.write_text(text, encoding="utf-8")
    sys.stdout.write("كُتب TALAB_INDEX.md\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
