"""فهرسُ المقام على درجات الترخيص التدريجيّ (MAQAM_INDEX.md) من `slge.maqam` وشريحة MASAQ.

القياسُ على `masaq-filiyya.json.gz` بشهادات البوّابة: كلُّ فعلٍ (الصدرُ والجذعُ واللواحق): (١) شخصُه المقروء
يُقاس على وسوم MASAQ الحاملة للشخص (IV1S/IV1P/IV2MP/IV3MS/IV3MP/IV3FS، PVSUFF_SUBJ:*، CVSUFF_SUBJ:*)؛
(٢) ظهورُه المتّصل يُقاس على وسوم لاحقة الفاعل (SUBJ_PRON، *SUFF_SUBJ)؛ (٣) الفاعلُ الظاهر (وسمُ MASAQ
«فاعل» بعد الفعل مباشرة) لا يقع بعد فعلِ متكلّمٍ أو مخاطب — `zahir_only_ghaib` مقيسًا.
"""

from __future__ import annotations

import gzip
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from slge.filiyya import has_subject
from slge.maqam import PRESENT_TEMPLATES, same, shakhs, with_prefix
from slge.wazn import AWZAN, mizan

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "MAQAM_INDEX.md"
DATA = ROOT / "tests" / "data"
Word = tuple[tuple[str, str], ...]
PRE_TAGS = ("IMPERF_PREF", "CV_PREF", "IV1S", "IV1P", "IV2MP", "IV3MS", "IV3MP", "IV3FS")
PERSON_OF: dict[str, str] = {
    "IV1S": "متكلم", "IV1P": "متكلم", "IV2MP": "مخاطب", "IV3MS": "غائب", "IV3MP": "غائب",
    "IV3FS": "مخاطب/غائبة", "PVSUFF_SUBJ:1S": "متكلم", "PVSUFF_SUBJ:1P": "متكلم",
    "PVSUFF_SUBJ:2MP": "مخاطب", "PVSUFF_SUBJ:3MP": "غائب", "PVSUFF_SUBJ:3FS": "غائب",
    "CVSUFF_SUBJ:2MP": "مخاطب",
}
SUBJ_TAGS = ("SUBJ_PRON", "PVSUFF_SUBJ", "IVSUFF_SUBJ", "CVSUFF_SUBJ")


def _load() -> list[dict[str, Any]]:
    with gzip.open(DATA / "masaq-filiyya.json.gz", "rt", encoding="utf-8") as f:
        rows: list[dict[str, Any]] = json.load(f)["rows"]
    return rows


def _cells(r: dict[str, Any], keep: tuple[str, ...], suffix: bool = True) -> Word:
    pre = [(a, b) for t, cs in r["pre"] for a, b in cs if t in keep]
    suf = [(a, b) for _, cs in r["suf"] for a, b in cs] if suffix else []
    return (*pre, *((a, b) for a, b in r["stem"]), *suf)


def verbs() -> list[tuple[Word, str | None, bool, bool]]:
    """(الفعلُ، شخصُ MASAQ إن وُسم، لاحقةُ فاعلٍ عند MASAQ، فاعلٌ ظاهرٌ بعده عند MASAQ)."""

    by: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for r in _load():
        by[str(r["ref"])].append(r)
    out: list[tuple[Word, str | None, bool, bool]] = []
    for verse in by.values():
        verse.sort(key=lambda r: int(str(r["pos"])))
        for i, r in enumerate(verse):
            if not str(r["role"]).startswith("فعل"):
                continue
            tags = [t for t, _ in r["pre"]] + [t for t, _ in r["suf"]]
            person = next((PERSON_OF[t] for t in tags if t in PERSON_OF), None)
            attached = any(t.startswith(SUBJ_TAGS) for t in tags)
            nxt = verse[i + 1] if i + 1 < len(verse) else None
            zahir = (nxt is not None and nxt["role"] == "فاعل"
                     and int(str(nxt["pos"])) == int(str(r["pos"])) + 1)
            out.append((_cells(r, PRE_TAGS), person, attached, zahir))
    return out


def measure() -> dict[str, object]:
    vs = verbs()
    person: Counter[str] = Counter()
    attach: Counter[str] = Counter()
    zahir: Counter[str] = Counter()
    read: Counter[str] = Counter()
    for v, p, att, zh in vs:
        s = shakhs(v)
        read[s or "—"] += 1
        if p is not None:
            verdict = "لم يُقرأ" if s is None else ("وافق" if same(s, p) else "خالف")
            person[verdict] += 1
        attach["وافق" if has_subject(v) == att else "خالف"] += 1
        if zh:
            who = "لم يُقرأ" if s is None else ("غائب" if s in ("غائب", "مخاطب/غائبة") else "حاضر")
            zahir[who] += 1
    return {"n": len(vs), "person": person, "attach": attach, "zahir": zahir, "read": read}


def render() -> str:
    m = measure()
    person: Counter[str] = m["person"]  # type: ignore[assignment]
    attach: Counter[str] = m["attach"]  # type: ignore[assignment]
    zahir: Counter[str] = m["zahir"]  # type: ignore[assignment]
    read: Counter[str] = m["read"]  # type: ignore[assignment]
    pt = sum(person.values())
    at = sum(attach.values())
    zt = sum(zahir.values())
    table = [(k, [str(shakhs(with_prefix(p, mizan(AWZAN[k].template)))) for p in "ءنتي"])
             for k in PRESENT_TEMPLATES]
    lines = [
        "# فهرسُ المقام على درجات الترخيص التدريجيّ",
        "",
        "مولَّدٌ بـ`python tools/gen_maqam_index.py` من `src/slge/maqam.py`؛ لا يُحرَّر باليد. "
        "البرهانُ: "
        "`formal/Slge/Maqam.lean`.",
        "",
        "## د٤ الخانة — الشخصُ من صدر المضارع ولاحقة الماضي", "",
        "صدرُ المضارع يقرأ الشخصَ لكلّ قالبِ مضارعٍ (13) ولكلّ جذرٍ لا ألفَ فيه "
        "(`shakhsPresent`): همزةٌ ونونٌ متكلّم، ياءٌ غائب، تاءٌ "
        "مخاطبٌ أو غائبة — الخانةُ لا تفصل (`present_prefix_reads_person`، عامٌّ على الجذور لا "
        "شاهد). "
        "ولاحقةُ الفاعل على جذعِ فعلٍ تقرؤه من جدول `Filiyya.subjectSuffixes` بشخصٍ لكلّ لاحقة "
        "(`suffixShakhs_covers`)، وفي المضارع بلاحقةٍ (تَفْعَلُونَ/يَفْعَلُونَ) الصدرُ يفصل؛ "
        "والماضي بلا "
        "لاحقةٍ غائب، والأمرُ مخاطب (`shakhs`؛ `shakhs_witnesses`). الألفُ ليست أصلًا "
        "(`onTemplateRoot`).",
        "",
        "| القالب | ء | ن | ت | ي |", "|---|---|---|---|---|",
        *[f"| {AWZAN[k].name} | {a} | {b} | {c} | {d} |" for k, (a, b, c, d) in table],
        "",
        "## د٨ الحدّ — المستترُ لا خانةَ له، والظاهرُ للغائب", "",
        "الفاعلُ المستترُ غيابُ لاحقةٍ لا حضورُها: أَدْرُسُ ودَرَسَ ويَدْرُسُ بلا لاحقةِ فاعلٍ "
        "وشخصُها مقروء، "
        "وضَرَبْتُ لاحقتُه خانة (`mustatir_has_no_cell`). حكمُه وجوبًا للحاضر وجوازًا للغائب "
        "(`hadir_wujub`، "
        "`ghaib_jawaz`) — فالغائبُ يستتر لكن جوازًا؛ وما في الحصر المُرسَل من «حظر استتار الغائب» "
        "خلافُ "
        "النحو (هُوَ مستترٌ جوازًا في فَعَلَ ويَفْعَلُ) ولم يُدخَل. الاسمُ الظاهرُ فاعلًا للغائب "
        "وحده "
        "(`zahir_only_ghaib`؛ `zahir_not_hadir`: لا بعد متكلّمٍ ولا مخاطب)، والمتّصلُ والمستترُ "
        "لكلّ شخص "
        "(`valid`)؛ والظهورُ يُقرأ من الفعل والكلمة التالية (`zuhur_witnesses`).",
        "",
        "## التوكيدُ اللفظيّ وعودُ الغائب", "",
        "المنفصلُ بعد الفعل توكيدٌ إذا طابق شخصَه (`tawkid`): ضَرَبْتُ أَنَا وأَدْرُسُ أَنَا "
        "ودَرَسَ هُوَ "
        "وتَدْرُسُ أَنْتَ/هِيَ؛ وضَرَبْتُ أَنْتَ وأَدْرُسُ هُوَ لا (`tawkid_witnesses`). لكلّ "
        "منفصلٍ في الجدول "
        "شخصٌ (`detached_all_read`)، ولا توكيدَ إلّا بمنفصلٍ من الجدول وفعلٍ قُرئ شخصُه "
        "(`tawkid_needs_both`). "
        "والضميرُ العائدُ في الفاعل يفرض تقديمَ المفعول (`aid_forces_maful_first`): الغائبُ يحتاج "
        "ما يعود "
        "عليه لفظًا ورتبة.",
        "",
        "## القياس على MASAQ", "",
        f"على {m['n']:,} فعلًا من الشريحة المودَعة بشهادات البوّابة:",
        "",
        f"- الشخصُ حيث وسمته MASAQ ({pt:,}): وافق {person['وافق']:,}، خالف {person['خالف']:,}، "
        f"لم يُقرأ {person['لم يُقرأ']:,}.",
        f"- لاحقةُ الفاعل (المتّصل) على كلّ فعل ({at:,}): وافق {attach['وافق']:,}، خالف "
        f"{attach['خالف']:,}.",
        f"- الفاعلُ الظاهر بعد الفعل مباشرة ({zt:,}): بعد غائبٍ أو تاءٍ {zahir['غائب']:,}، بعد "
        f"حاضرٍ {zahir['حاضر']:,} (الطفرةُ المقيسة لـ`zahir_only_ghaib`)، "
        f"لم يُقرأ {zahir['لم يُقرأ']:,}.",
        "",
        "| الشخصُ المقروء | العدد |", "|---|---|",
        *[f"| {k} | {v:,} |" for k, v in read.most_common()],
        "",
        "## ما لا تقرؤه الخانة — باسمه", "",
        "- تاءُ المضارع (تَفْعَلُ): مخاطبٌ أو غائبة — الخانةُ لا تفصل، والتوكيدُ يقبل الاثنين.",
        "- المعتلُّ والمزيدُ بإدغامٍ على غير قالب، والمبدَلُ همزتُه ألفًا (آمَنُوا)، والمضارعُ "
        "بلاحقةٍ غيرِ "
        "مجدوَلة (نونُ التوكيد، نونُ الوقاية)، ولاحقةُ مفعولٍ بعد لاحقة الفاعل (آتَيْنَاهُمْ): لا "
        "يُقرأ شخصُه "
        "أو لا تُقرأ لاحقتُه — بقيّةٌ مسمّاة تعود إلى `Filiyya.hasSubject` وقوالب `wazn`.",
        "- الناقصُ (يَهْدِي، تَجْرِي): ياؤُه تُقرأ لاحقةَ مخاطبة بالخانة، والمنصوبُ من المثال "
        "بثلاث خانات "
        "(تَجِدَ) يُقرأ ماضيًا — الخانةُ لا تفصل.",
        "- وسومُ MASAQ الحاملةُ للشخص قليلةٌ (SUBJ_PRON بلا شخص) وبعضُها مخالفٌ للصورة (IV3FS على "
        "تَقُولُونَ): القياسُ على ما وُسم.",
        "- الحضورُ والشهودُ وعودُ الغائب على مذكورٍ سابق: معنًى ومقام؛ ما بُرهن الخانةُ والرتبة.",
        "- الحصرُ المُرسَل: أنواعُه مكتوبةٌ باليد، وفحصُ إجهاده يقارن الدالّةَ بنفسها — لم يُدخَل "
        "منه شيء.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    text = render()
    if "--check" in sys.argv:
        if TARGET.read_text(encoding="utf-8") != text:
            sys.stderr.write("MAQAM_INDEX.md غيرُ مطابق؛ شغّل tools/gen_maqam_index.py\n")
            return 1
        sys.stdout.write("MAQAM_INDEX.md مطابق\n")
        return 0
    TARGET.write_text(text, encoding="utf-8")
    sys.stdout.write("كُتب MAQAM_INDEX.md\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
