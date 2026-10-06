"""فهرسُ الجهة والزمن على درجات الترخيص التدريجيّ (JIHA_INDEX.md) من `slge.jiha` وشرائح MASAQ.

القياسُ بشهادات البوّابة: (١) قارئُ الصيغة `sigha` على كلّ فعلٍ في `masaq-filiyya.json.gz` يُقاس على
وسم MASAQ (PV ماضٍ، IV مضارع، CV أمر؛ والمبنيُّ للمجهول بصيغته)؛ (٢) السينُ (FUT_PART) لا تقع إلّا على
مضارع — `shift_only_present` مقيسًا؛ (٣) ما بعد لَمْ ولَنْ وسَوْفَ وكَانَ في `masaq-shibh.json.gz`: وسمُ
الفعل التالي.
"""

from __future__ import annotations

import gzip
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from slge.jiha import KANA, LAM, LAN, SAWFA, jiha, sigha
from slge.maqam import PRESENT_TEMPLATES
from slge.zuruf import set_last

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "JIHA_INDEX.md"
DATA = ROOT / "tests" / "data"
Word = tuple[tuple[str, str], ...]
PRE_TAGS = ("IMPERF_PREF", "CV_PREF", "IV1S", "IV1P", "IV2MP", "IV3MS", "IV3MP", "IV3FS")
FUT = ("FUT_PART", "FUTURE_PART")
TAG_SIGHA: dict[str, str] = {"PV": "ماضٍ", "PV_PASS": "ماضٍ", "IV": "مضارع", "IV_PASS": "مضارع",
                             "CV": "أمر"}
SUBJ_TAGS = ("SUBJ_PRON", "PVSUFF_SUBJ", "IVSUFF_SUBJ", "CVSUFF_SUBJ")
PARTICLES: dict[str, Word] = {"لَمْ": LAM, "لَنْ": LAN, "سَوْفَ": SAWFA, "كَانَ": KANA}


def _load(name: str) -> list[dict[str, Any]]:
    with gzip.open(DATA / name, "rt", encoding="utf-8") as f:
        rows: list[dict[str, Any]] = json.load(f)["rows"]
    return rows


def _cells(r: dict[str, Any], keep: tuple[str, ...]) -> Word:
    pre = [(a, b) for t, cs in r["pre"] for a, b in cs if t in keep]
    return (*pre, *((a, b) for a, b in r["stem"]))


def sigha_mood(v: Word) -> str | None:
    """الصيغةُ بأيّ حالةٍ للآخر: المضارعُ مرفوعًا ومنصوبًا ومجزومًا."""

    s = sigha(v)
    if s is not None:
        return s
    return "مضارع" if v and sigha(set_last(v, "ضم")) == "مضارع" else None


def verbs() -> list[tuple[Word, str, bool, bool]]:
    """(الفعلُ بلا لواحق، صيغةُ MASAQ، له لاحقةُ فاعل، عليه السين)."""

    out: list[tuple[Word, str, bool, bool]] = []
    for r in _load("masaq-filiyya.json.gz"):
        tag = str(r["tag"])
        if tag not in TAG_SIGHA:
            continue
        tags = [t for t, _ in r["pre"]] + [t for t, _ in r["suf"]]
        out.append((_cells(r, PRE_TAGS), TAG_SIGHA[tag], any(t.startswith(SUBJ_TAGS) for t in tags),
                    any(t in FUT for t in tags)))
    return out


def after_particles() -> Counter[tuple[str, str]]:
    """(الأداة، وسمُ الكلمة التالية) من شريحة شبه الجملة."""

    by: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for r in _load("masaq-shibh.json.gz"):
        by[str(r["ref"])].append(r)
    out: Counter[tuple[str, str]] = Counter()
    for verse in by.values():
        verse.sort(key=lambda r: int(str(r["pos"])))
        for i, r in enumerate(verse):
            w = str(r["word"])
            if w not in PARTICLES or i + 1 >= len(verse):
                continue
            nxt = verse[i + 1]
            if int(str(nxt["pos"])) == int(str(r["pos"])) + 1:
                out[(w, TAG_SIGHA.get(str(nxt["tag"]), str(nxt["tag"])))] += 1
    return out


def measure() -> dict[str, object]:
    vs = verbs()
    bare: Counter[tuple[str, str]] = Counter()
    fut: Counter[str] = Counter()
    read_fut: Counter[str] = Counter()
    for v, tag, suffixed, has_sa in vs:
        if not suffixed:
            bare[(tag, sigha_mood(v) or "—")] += 1
        if has_sa:
            fut[tag] += 1
            read_fut[jiha((), (("س", "فتح"), *v))] += 1
    return {"n": len(vs), "bare": bare, "fut": fut, "read_fut": read_fut,
            "after": after_particles()}


def render() -> str:
    m = measure()
    bare: Counter[tuple[str, str]] = m["bare"]  # type: ignore[assignment]
    fut: Counter[str] = m["fut"]  # type: ignore[assignment]
    read_fut: Counter[str] = m["read_fut"]  # type: ignore[assignment]
    after: Counter[tuple[str, str]] = m["after"]  # type: ignore[assignment]
    nb = sum(bare.values())
    agree = sum(v for (t, s), v in bare.items() if t == s)
    wrong = sum(v for (t, s), v in bare.items() if s not in (t, "—"))
    lines = [
        "# فهرسُ الجهة والزمن على درجات الترخيص التدريجيّ",
        "",
        "مولَّدٌ بـ`python tools/gen_jiha_index.py` من `src/slge/jiha.py`؛ لا يُحرَّر باليد. "
        "البرهانُ: "
        "`formal/Slge/Jiha.lean`.",
        "",
        "## د٤ الخانة — الصيغةُ دالّةٌ في الحالات", "",
        "ما على قالبٍ فحالاتُه حالاتُ قالبه (`states_of_onTemplate`)، وأصنافُ الصيغ الثلاثة — "
        f"{len(PRESENT_TEMPLATES)} مضارعًا و13 ماضيًا و10 أوامر — متباينةُ الحالات قالبًا قالبًا "
        "(`sigha_states_disjoint`). فقارئُ الصيغة `sigha` يقرأ لكلّ جذرٍ لا ألفَ فيه: كلَّ ماضٍ "
        "ماضيًا، "
        "وكلَّ أمرٍ أمرًا، وكلَّ مضارعٍ بصدوره الأربعة مضارعًا (`sigha_of_fill`، عامٌّ لا شاهد) — "
        "فلا يُقرأ "
        "ماضٍ مضارعًا ولا أمرٌ ماضيًا.",
        "",
        "## د٨ الحدّ — الأمرُ للمخاطب، والإزاحةُ على المضارع وحده", "",
        "صيغةُ الأمر مخاطبٌ أبدًا عند قارئ المقام: لكلّ قالبِ أمرٍ ولكلّ جذرٍ لا ألفَ فيه ولا "
        "تاءَ في آخره "
        "وبلا لاحقة (`amr_is_mukhatab`؛ آخرُه لامُ الكلمة ساكنةً: `amr_fill_last`)؛ ولا قالبَ "
        "أمرٍ للمتكلّم "
        "أو الغائب — أمرُهما باللام على المضارع (`ghaib_amr_by_lam`: لِيَكْتُبْ). أدواتُ الإزاحة "
        "— السينُ "
        "وسَوْفَ (مستقبل)، لَمْ (ماضٍ منفيٌّ بالجزم)، لَنْ (مستقبلٌ منفيٌّ بالنصب)، كَانَ (ماضٍ "
        "مستمرّ) — "
        "عمليّاتٌ لا تقبل إلّا المضارع (`shift_only_present`)، والماضي والأمرُ لا يُزاحان "
        "(`past_not_shifted`)؛ "
        "السينُ تحفظ الترخيص (`sa_licensed`) وتُردّ بعينها (`sa_restores`)، ولَمْ تُردّ "
        "(`lam_restores`)؛ "
        "والأدواتُ من جدول الربط بعملها وكَانَ أولى أخواتها (`shifts_in_rawabit`).",
        "",
        "## القارئ", "",
        "`jiha` يقرأ الجهةَ من الكلمة وما قبلها: ماضٍ، مضارع، مستقبلٌ بالسين وسَوْفَ، ماضٍ منفيٌّ "
        "بلَمْ، "
        "مستقبلٌ منفيٌّ بلَنْ، ماضٍ مستمرٌّ بكَانَ، أمر (`jiha_witnesses`). نقاطُ رايشنباخ (E، S، "
        "R) معنًى "
        "لا خانة — معلَن.",
        "",
        "## القياس على MASAQ", "",
        f"على {m['n']:,} فعلًا من شريحة الفعليّة بشهادات البوّابة:",
        "",
        f"- الصيغةُ على الأفعال بلا لاحقةِ فاعل ({nb:,}): وافق وسمَ MASAQ {agree:,}، خالف {wrong:,}، "
        f"لم يُقرأ {nb - agree - wrong:,}.",
        f"- السينُ (FUT_PART) على {sum(fut.values())} فعلًا: "
        + "، ".join(f"{t} {v}" for t, v in fut.most_common())
        + " — `shift_only_present` مقيسًا؛ والقارئُ يقرؤها مستقبلًا في "
        f"{read_fut['مستقبل']} (والباقي معتلٌّ أو بلاحقة: لا يُقرأ).",
        "- ما بعد الأدوات في شريحة شبه الجملة: "
        + "، ".join(f"{p} ← {t} {v}" for (p, t), v in after.most_common()) + ".",
        "",
        "| وسمُ MASAQ | القارئ | العدد |", "|---|---|---|",
        *[f"| {t} | {s} | {v:,} |" for (t, s), v in bare.most_common()],
        "",
        "## ما لا تقرؤه الخانة — باسمه", "",
        "- المعتلُّ (قَالَ، جَاءَ، يَشَاءُ، قُلْ) والمبدَلُ همزتُه ألفًا: على غير قالب — دَينُ "
        "الإعلال في "
        "`wazn.DEBTS`؛ والمبنيُّ للمجهول من المزيد (أُنْزِلَ) غيرُ مودَع، وهو بالخانة مضارعُ "
        "المتكلّم منصوبًا "
        "(أُنْزِلَ = أُنْزِلَ) — الخانةُ لا تفصل؛ وأمرُ أَفْعَلَ (أَعْرِضْ) غيرُ مودَع فيُقرأ "
        "بحالة الآخر مضارعًا؛ "
        "والمنصوبُ من المثال بثلاث خانات (تَجِدَ) يُقرأ ماضيًا.",
        "- الزمنُ المعنويّ (قَدْ، إِذَا الشرطيّة، المضارعُ بمعنى الماضي في الحكاية): معنًى ومقام؛ "
        "ما بُرهن "
        "الصيغةُ والإزاحةُ بالأداة على الخانة.",
        "- الحصرُ المُرسَل: أنواعُ الزمن والشخص مكتوبةٌ باليد، وفحصُ إجهاده يقارن الدالّةَ بنفسها "
        "— لم يُدخَل "
        "منه شيء.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    text = render()
    if "--check" in sys.argv:
        if TARGET.read_text(encoding="utf-8") != text:
            sys.stderr.write("JIHA_INDEX.md غيرُ مطابق؛ شغّل tools/gen_jiha_index.py\n")
            return 1
        sys.stdout.write("JIHA_INDEX.md مطابق\n")
        return 0
    TARGET.write_text(text, encoding="utf-8")
    sys.stdout.write("كُتب JIHA_INDEX.md\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
