"""ولّد `WASL_INDEX.md`: فهرسُ همزتي الوصل والقطع على درجات الترخيص التدريجيّ من `slge.wasl`، وقياسُ
القارئ على شريحة MASAQ المجمَّدة (الصورُ المبدوءةُ بهمزة بشهادات البوّابة وبقايا رسمها)؛ ‎--check‎."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

from slge.cells import STATES, index
from slge.rawabit import cells_of
from slge.wasl import QAT_TEMPLATES, TEN, WASL_TEMPLATES, kind
from slge.wazn import AWZAN

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "WASL_INDEX.md"
SLICE = ROOT / "tests" / "data" / "masaq-hamza.json"
_ST = dict(zip("0123", STATES, strict=True))
TEN_SEGS = ("اسم", "ابن", "ابنة", "امرؤ", "امرأة", "اثنان", "اثنتان", "ابنم", "ايم", "ايمن")


def cells(s: str) -> tuple[tuple[str, str], ...]:
    return tuple((s[i], _ST[s[i + 1]]) for i in range(0, len(s), 2))


def measure() -> dict[str, object]:
    rows = json.loads(SLICE.read_text(encoding="utf-8"))
    kinds: Counter[str] = Counter()
    reader: Counter[tuple[str, str, str]] = Counter()
    ten: Counter[tuple[str, str]] = Counter()
    for r in rows:
        kinds[r["k"]] += 1
        if r["k"] not in ("وصل", "قطع") or not r["s"]:
            continue
        stem = cells(r["s"])
        tag = r["g"]
        group = ("فعل ماضٍ" if tag.startswith("PV") else "فعل أمر" if tag.startswith("CV") else
                 "مضارع" if tag.startswith("IV") else "مصدر" if tag.startswith("GERUND") else
                 "اسم" if tag.startswith(("NOUN", "ADJ")) else "حرف/ضمير/موصول")
        reader[(r["k"], group, kind(stem))] += 1
        seg = r["seg"]
        if seg in TEN_SEGS:
            ten[(seg, r["k"])] += 1
    read = sum(v for (_, _, k), v in reader.items() if k != "لا يُقرأ")
    agree = sum(v for (cert, _, k), v in reader.items()
                if (cert == "وصل" and k == "وصل") or (cert == "قطع" and k.startswith("قطع")))
    return {"kinds": kinds, "reader": reader, "ten": ten, "n": len(rows), "read": read,
            "agree": agree}


def _cells(w: str) -> str:
    return "-".join(str(index(c)) for c in cells_of(w))


def render() -> str:
    m = measure()
    kinds: Counter[str] = m["kinds"]  # type: ignore[assignment]
    reader: Counter[tuple[str, str, str]] = m["reader"]  # type: ignore[assignment]
    ten: Counter[tuple[str, str]] = m["ten"]  # type: ignore[assignment]
    lines = [
        "# فهرسُ همزتي الوصل والقطع على درجات الترخيص التدريجيّ",
        "",
        "مولَّدٌ بـ`python tools/gen_wasl_index.py` من `src/slge/wasl.py`؛ لا يُحرَّر باليد. البرهانُ: "
        "`formal/Slge/Wasl.lean`؛ وحدُّ الابتداء والوصل مبرهَنٌ في الغانم (`A116.Boundary`) "
        "وبقيّةُ الرسم `WASL`/`WASL_SILENT` في شهادته.",
        "",
        "## د٤ الخانة — خانةٌ واحدة في الابتداء", "",
        "اِنْطِلَاق وإِكْرَام: همزةٌ مكسورةٌ فساكن (`wasl_qat_cells_shared`) — الخانةُ لا تفرّق الوصلَ من "
        "القطع؛ الفرقُ في الحدّ وفي القالب وفي بقيّة الرسم.",
        "",
        "## د٨ الحدّ — الوصلُ يسقط والقطعُ يبقى", "",
        "- لا ابتداءَ بساكن (`no_initial_sukun`)، وهمزةُ الوصل تُرخِّصه (`wasl_licenses`).",
        "- في الوصل تسقط فيتّصل الساكنُ بمتحرّكٍ قبله (`wasl_drops`)؛ وبعد ساكنٍ لا تُقبل "
        "(`wasl_after_sukun`): كسرةُ التقاء الساكنين قانونُ `Context` في الغانم.",
        "- القطعُ يبقى بعد أيّ آخر (`qat_stays`).",
        "- **الاختبارُ السريع** بشهادتي البوّابة (`quick_test`): وَ + اِنْطَلَقَ ⇒ وَنْطَلَقَ "
        "(الهمزةُ ساقطة، `WASL_SILENT`)، وَ + أَكْرَمَ ⇒ وَأَكْرَمَ (باقية).",
        "- الحذفُ الإملائيّ عمليّاتُ حدّ: بِسْمِ = بِ + جذعُ اِسْم بلا همزة (`bism_witness`)؛ آلْآنَ = "
        "ءَاْ + ما بعد همزة أل (`istifham_al_witness`؛ مدٌّ فساكن: خارج الثنائيّ كحَاجَّ)؛ "
        "أَسْتَخْرَجْتَ: تسقط الوصلُ وتبقى الاستفهام (`istifhamVerb_licensed`).",
        "",
        "## الحصرُ الصرفيّ — تقسيمُ القوالب", "",
        "القوالبُ المبدوءةُ بهمزة في `Wazn.awzan` أربعةٌ وعشرون، تنقسم بالضبط "
        "(`templates_partition`):", "",
        "- **وصل** (" + ", ".join(f"{AWZAN[k].name} [{k}]" for k in WASL_TEMPLATES) + ")",
        "- **قطع** (" + ", ".join(f"{AWZAN[k].name} [{k}]" for k in QAT_TEMPLATES) + ")",
        "",
        "القارئُ `kind`: وصلٌ أو قطعٌ من القالب، قطعٌ أصليٌّ من الجذر (أَخَذَ، أَرْض: `radicalHamza`)، "
        "وما سواه لا يُقرأ (`kind_witnesses`). أَكْتُبُ يُقرأ قطعًا من قالب أَفْعُل (خانةٌ مشتركةٌ مع جمع "
        "القلّة، والحكمُ واحد). والقالبُ يقرأ ما لا تقرؤه الخانة "
        "(`template_reads_what_cells_cannot`). أمرُ الخماسيّ والسداسيّ (اِنْطَلِقْ، اِسْتَغْفِرْ) وصلٌ وأمرُ "
        "الرباعيّ (أَكْرِمْ) قطعٌ: قوالبُ 113 و118–120 (دَينٌ سُدِّد؛ `Fil.amr_of_pres`).",
        "",
        "- الأسماءُ العشرة (`tenNouns`): " + ", ".join(f"{w} `{_cells(w)}`" for w in TEN)
        + "؛ كلُّها همزةٌ متحرّكةٌ فساكن (`ten_shape`)، وجمعُها قطعٌ على أَفْعَال (`plural_qat`).",
        "",
        "## القياس على MASAQ", "",
        f"على {m['n']} صورةً مبدوءةً بهمزة بشهادات البوّابة؛ الصنفُ من بقيّة الرسم في الشهادة:", "",
        "| الصنف (الشهادة) | العدد |", "|---|---|",
        *[f"| {k} | {v} |" for k, v in kinds.most_common()],
        "",
        "الوصلُ ساقطٌ بعد السابقة (وَ، فَ، بِ، لِ) كما بُرهن؛ والمحذوفُ رسمًا: أل بعد اللام (لِلَّذِي) "
        "وبِسْمِ.",
        "",
        "### القارئُ (القالب) مقابلَ الشهادة — الصورُ بلا سابقة", "",
        f"فيما يقرؤه القالبُ ({m['read']}): موافقٌ للشهادة {m['agree']}، مخالفٌ "
        f"{int(str(m['read'])) - int(str(m['agree']))} (أُولُو على اُفْعُلْ، وإِمَّا وإِحْدَى: قوالبُ "
        "تقبل والمعجمُ يردّ).", "",
        "| الشهادة | الصنفُ الصرفيّ | قراءةُ القالب | العدد |", "|---|---|---|---|",
        *[f"| {a} | {b} | {c} | {v} |" for (a, b, c), v in reader.most_common(24)],
        "",
        "ما لا يقرؤه القالب: المهموزُ المعتلّ (آمَنَ، أَتَى)، وأفعالٌ على قوالبَ خارج `awzan` "
        "(اِتَّخَذَ بالإدغام: `Fil.ibdal` يُخرجه ولا يقرؤه القالبُ المجرّد)، والحروفُ والضمائرُ والموصولاتُ "
        "(مودَعاتٌ لا قوالب) — "
        "دُيونٌ مسمّاة لا أخطاء.",
        "",
        "### الأسماءُ العشرة في المصحف", "",
        "| الاسم | الشهادة | العدد |", "|---|---|---|",
        *[f"| {s} | {k} | {v} |" for (s, k), v in sorted(ten.items(), key=lambda kv: -kv[1])],
        "",
        "## ما لا تقرؤه الخانة — باسمه", "",
        "- الوصلُ من القطع في الابتداء: القالبُ أو الشهادةُ، لا الخانة.",
        "- حذفُ همزة ابن بين علمين، وتمامُ البسملة: تيار.",
        "- شريحةُ MASAQ: 555 صورةً رُفضت بالاسم (REJECT 336، OUTSIDE 206، DEFER 13).",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    text = render()
    if "--check" in sys.argv:
        if TARGET.read_text(encoding="utf-8") != text:
            sys.stderr.write("WASL_INDEX.md غيرُ مطابق؛ شغّل tools/gen_wasl_index.py\n")
            return 1
        sys.stdout.write("WASL_INDEX.md مطابق\n")
        return 0
    TARGET.write_text(text, encoding="utf-8")
    sys.stdout.write("كُتب WASL_INDEX.md\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
