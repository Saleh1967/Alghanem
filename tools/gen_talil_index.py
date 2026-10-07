"""فهرسُ التعليل والسببيّة على درجات الترخيص التدريجيّ (TALIL_INDEX.md) من `slge.talil` وشرائح MASAQ.

القياسُ على الشرائح المودَعة (`masaq-filiyya.json.gz`، `masaq-shibh.json.gz`) بشهادات البوّابة: كلُّ
كلمةٍ موسومةٍ «مفعول لأجله» مع ما قبلها، وكلُّ «مفعول به» و«مفعول مطلق» بعد فعلٍ (لفحص الفصل)، وكلُّ
«اسم مجرور» بسابقة لِ/بِ (إحصاءٌ لا مرجعَ له: MASAQ لا تسم التعليل بالحرف). ويُقاس أنّ العلّة لا تُرفَع:
حالةُ MASAQ لكلّ مفعولٍ لأجله.
"""

from __future__ import annotations

import gzip
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from slge.cells import index
from slge.talil import TOOLS, derives, talil
from slge.wazn import AWZAN

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "TALIL_INDEX.md"
DATA = ROOT / "tests" / "data"
Word = tuple[tuple[str, str], ...]
VERBS = ("فعل ماضٍ", "فعل مضارع", "فعل أمر")


def _load(name: str) -> list[dict[str, Any]]:
    with gzip.open(DATA / name, "rt", encoding="utf-8") as f:
        rows: list[dict[str, Any]] = json.load(f)["rows"]
    return rows


def _cells(r: dict[str, Any], keep: tuple[str, ...] = ("DET", "PREP"), suffix: bool = True) -> Word:
    pre = [(a, b) for t, cs in r["pre"] for a, b in cs if t in keep]
    suf = [(a, b) for _, cs in r["suf"] for a, b in cs] if suffix else []
    return (*pre, *((a, b) for a, b in r["stem"]), *suf)


def pairs() -> list[tuple[str, str, Word, Word]]:
    """(وسمُ MASAQ، حالتُها، الكلمةُ السابقة، الكلمة) — بلا تكرارٍ بين الشريحتين."""

    seen: set[tuple[str, int]] = set()
    out: list[tuple[str, str, Word, Word]] = []
    for name in ("masaq-filiyya.json.gz", "masaq-shibh.json.gz"):
        by: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for r in _load(name):
            by[str(r["ref"])].append(r)
        for verse in by.values():
            verse.sort(key=lambda r: int(str(r["pos"])))
            for i, r in enumerate(verse):
                key = (str(r["ref"]), int(str(r["pos"])))
                role = str(r["role"])
                adjacent = i > 0 and int(str(verse[i - 1]["pos"])) == key[1] - 1
                prv = verse[i - 1] if adjacent else None
                if role == "مفعول لأجله" or (role in ("مفعول به", "مفعول مطلق") and prv
                                              and prv["role"] in VERBS):
                    tag = role
                elif role == "اسم مجرور" and any(t == "PREP" and cs[0][0] in ("ل", "ب")
                                                   for t, cs in r["pre"]):
                    tag = "اسم مجرور بـ لِ/بِ"
                else:
                    continue
                if key in seen:
                    continue
                seen.add(key)
                pv = _cells(prv, ("IMPERF_PREF", "IV3MP", "IV3MS")) if prv else ()
                out.append((tag, str(r["case"]).split()[0] if r["case"] else "—", pv, _cells(r)))
    return out


def measure() -> dict[str, object]:
    ps = pairs()
    read: Counter[tuple[str, str]] = Counter()
    cases: Counter[str] = Counter()
    for tag, case, a, b in ps:
        read[(tag, talil(a, b))] += 1
        if tag == "مفعول لأجله":
            cases[case] += 1
    n = len(AWZAN)
    pairs_d = sum(derives(a, b) for a in range(n) for b in range(n))
    return {"pairs": len(ps), "read": read, "cases": cases, "derives": pairs_d}


def _w(w: Word) -> str:
    return "-".join(str(index(c)) for c in w)


def render() -> str:
    m = measure()
    read: Counter[tuple[str, str]] = m["read"]  # type: ignore[assignment]
    cases: Counter[str] = m["cases"]  # type: ignore[assignment]
    liajlih = sum(v for (t, _), v in read.items() if t == "مفعول لأجله")
    hit = read[("مفعول لأجله", "مفعول لأجله")]
    false_bih = read[("مفعول به", "مفعول لأجله")]
    bih = sum(v for (t, _), v in read.items() if t == "مفعول به")
    harf = read[("اسم مجرور بـ لِ/بِ", "تعليل بالحرف")]
    harf_all = sum(v for (t, _), v in read.items() if t == "اسم مجرور بـ لِ/بِ")
    lines = [
        "# فهرسُ التعليل والسببيّة على درجات الترخيص التدريجيّ",
        "",
        "مولَّدٌ بـ`python tools/gen_talil_index.py` من `src/slge/talil.py`؛ لا يُحرَّر باليد. "
        "البرهانُ: "
        "`formal/Slge/Talil.lean`.",
        "",
        "## د٨ الحدّ — العلّةُ فضلةٌ لا تُرفَع", "",
        "المفعولُ لأجله مصدرٌ منصوبٌ يُقرأ نصبًا لكلّ جذع (`liajlih_reads_nasb`)، وفرزُه عن "
        "المطلق بالجذر "
        "لا بالمعنى: مصدرٌ بغير جذر الفعل لأجله، وبجذره مطلق (`Filiyya.sortFadla`؛ "
        "`fadla_witnesses`: "
        "دَرَسَ حَذَرَ / دَرَسَ دَرْسَ). صورتا التعليل — نصبُ المصدر وجرُّه بالحرف — كلمةٌ "
        "بعينها: الحوامِلُ وما "
        "قبل الآخر والطولُ واحد، والفرقُ خانةُ الآخر وحدَها (`two_forms_same_word`). أدواتُ "
        "التعليل جدولٌ "
        "حاصرٌ على الخانات (`tools`، 6): لِ وبِ ومِنْ أَجْلِ جرُّ الاسم، ولِأَنَّ عملُ إِنَّ بعينه "
        "(`li_anna_eq_inna`)، وكَيْ ولِ نصبُ المضارع؛ مرخَّصةٌ كلُّها (`tools_licensed`) ومفردُها "
        "في جدول "
        "أدوات الربط بعمله (`tools_in_rawabit`). **وليس فيها ما يرفع معمولَه** "
        "(`talil_never_raf`): الجرُّ "
        "جرٌّ، واسمُ لِأَنَّ نصبٌ، والمضارعُ نصب — فالعلّةُ فضلةٌ أبدًا، والرفعُ للمسند إليه وحدَه "
        "(`Nisab.isnad_one_operation`).",
        "",
        "| الأداة | الخانات | العمل |", "|---|---|---|",
        *[f"| {n} | `{_w(cs)}` | {a} |" for n, cs, a in TOOLS],
        "",
        "## د١٦ — السببيّةُ الاشتقاقيّة ترتيبٌ جزئيٌّ صارم", "",
        "المصدرُ علّةُ المشتقّ عند البصريّين، فالعلّيّةُ على الأوزان الـ125 هي السلفيّةُ في الشبكة "
        "(`derives a b`: `b` سلفُ `a` في `Nisab.chain`). وهي ترتيبٌ جزئيٌّ صارم: لا شيءَ علّةُ "
        "نفسه "
        "(`derives_irrefl`)، وعلّةُ العلّة علّةٌ (`derives_trans`)، ولا دورَ (`derives_asymm`) — "
        "من ثلاثة "
        "جداول مقرَّرةٍ بـ`decide` على 125 و125×125 (`derives_irrefl_all`، `derives_trans_all`، "
        "`derives_dist_all`)، لا من نوعٍ مُعرَّفٍ باليد ولا من مصفوفة أحداثٍ مكتوبة. والبعدُ عن "
        "الجذر يتناقص "
        "على كلّ سبب (`derives_dist`) فلا لانهاية؛ والجذرُ (فَعْلٌ) علّةُ كلّ وزنٍ سواه ولا علّةَ "
        "له "
        "(`root_causes_all`).",
        "",
        f"أزواجُ السببيّة: {m['derives']} زوجًا (وزن، علّة) على 125 وزنًا.",
        "",
        "## د٨ — التنازعُ والتقديم", "",
        "فعلان على معمولٍ واحد: إعمالُ الثاني لقربه (البصريّون) — المتنازَعُ فيه معمولُ الأقرب "
        "وخانتُه "
        "مستقلّةٌ عن الفعل الأوّل (`nearer_works`)، والأوّلُ يُعمَل في ضميره متّصلًا حافظًا "
        "للترخيص "
        "(`first_takes_pronoun`؛ `tanazu_witness`: عَلِمْتُهُ وَعَمِلْتُ الْخَيْرَ). إعمالُ "
        "الأوّل (الكوفيّون) "
        "معلَن لا مودَع. المفعولُ المتّصلُ يتقدّم على الفاعل الظاهر حتمًا "
        "(`Filiyya.attached_object_first`)؛ "
        "والمفعولُ لأجله حرٌّ في الموضع: نصبُه قبل الفعل وبعده واحد (`fronting_keeps_nasb`).",
        "",
        "## القارئ", "",
        "`talil` يقرأ التعليلَ بين كلمتين من خانتيهما: لِأَنَّ بعينها؛ مصدرٌ منصوبٌ بلا «ال» بغير "
        "جذر الفعل "
        "قبله ⇒ مفعولٌ لأجله؛ لِ/بِ على مصدرٍ مجرور ⇒ تعليلٌ بالحرف (احتمالٌ: اللامُ والباءُ "
        "تُفيدان غيرَه)؛ "
        "وما سواه لا يُقرأ (`talil_witnesses`).",
        "",
        "## القياس على MASAQ", "",
        f"على {m['pairs']:,} كلمةً من الشريحتين المودَعتين بشهادات البوّابة: المفعولُ لأجله يُقرأ "
        f"لأجله في "
        f"{hit} من {liajlih}؛ والمفعولُ به بعد الفعل يُقرأ لأجله خطأً في {false_bih} من {bih:,} "
        f"(مصدرٌ نكرةٌ مفعولًا به — باسمه)؛ والمجرورُ بـلِ/بِ يُقرأ تعليلًا بالحرف في {harf} من "
        f"{harf_all:,} "
        "(إحصاءٌ: لا وسمَ في MASAQ للتعليل بالحرف).",
        "",
        "| وسمُ MASAQ | القارئ | العدد |", "|---|---|---|",
        *[f"| {t} | {n} | {v} |" for (t, n), v in read.most_common()],
        "",
        "حالةُ MASAQ لكلّ مفعولٍ لأجله (`talil_never_raf` مقيسًا): "
        + "، ".join(f"{c} {v}" for c, v in cases.most_common()) + ".",
        "",
        "## ما لا تقرؤه الخانة — باسمه", "",
        "- شرطُ المفعول لأجله (مصدرٌ قلبيٌّ متّحدٌ مع الفعل فاعلًا وزمانًا): معنًى؛ ما بُرهن "
        "الصورةُ والفرزُ "
        "بالجذر.",
        "- المصدرُ المعرَّف أو المضافُ مفعولًا لأجله (حَذَرَ الْمَوْتِ) يُقرأ متى خلا من «ال»؛ "
        "والمعرَّفُ بأل "
        "لا يُقرأ — والمضافُ المنصوبُ لا يفرّقه القارئُ عن مفعولٍ به مضاف.",
        "- ما لم يُقرأ من المفعول لأجله: مصدرٌ على قالبٍ غيرِ مودَع — فَعَالٌ (جَزَاءً)، "
        "مَفْعِلَةٌ وتَفْعِلَةٌ "
        "(مَوْعِظَةً، تَذْكِرَةً) — والأجوفُ (مَتَاعَ) والمقصورُ (ذِكْرَى): دَينُ القوالب في "
        "`wazn.DEBTS`؛ "
        "والمطلقُ المقروءُ لأجله: جذرُ فعلٍ معتلٍّ لم يُستردّ.",
        "- اللامُ والباءُ لغير التعليل (الاختصاص، الاستعانة…): القارئُ يُعلّم الاحتمالَ لا القطع.",
        "- السببيّةُ بين الأحداث (التعليمُ علّةُ العلم): معنًى؛ ما بُرهن السببيّةُ الاشتقاقيّة "
        "على الأوزان.",
        "- الحصرُ المُرسَل أحال على ملفّ `causality_operators_proofs.lean` لم يُرفَق؛ ومصفوفةُ "
        "أحداثه "
        "مكتوبةٌ باليد، وفحصُ إجهاده يعدّ صحيحًا ما بناه (100% بالبناء) — لم يُدخَل منه شيء.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    text = render()
    if "--check" in sys.argv:
        if TARGET.read_text(encoding="utf-8") != text:
            sys.stderr.write("TALIL_INDEX.md غيرُ مطابق؛ شغّل tools/gen_talil_index.py\n")
            return 1
        sys.stdout.write("TALIL_INDEX.md مطابق\n")
        return 0
    TARGET.write_text(text, encoding="utf-8")
    sys.stdout.write("كُتب TALIL_INDEX.md\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
