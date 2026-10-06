"""ولّد `FIL_INDEX.md`: فهرسُ الفعل (الأبواب، المزيد، الإعلال، الإبدال) على درجات الترخيص التدريجيّ من
`slge.fil`، وقياسُه على شريحة MASAQ المجمَّدة (أفعالُ المصحف بشهادات البوّابة)؛ ‎--check‎."""

from __future__ import annotations

import gzip
import json
import sys
from collections import Counter
from pathlib import Path

from slge.cells import STATES
from slge.fil import ABWAB, DHZ, ITBAQ, MAZID, MISSING, added, read_doubled, read_hollow
from slge.wazn import AWZAN, fill, root_of

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "FIL_INDEX.md"
SLICE = ROOT / "tests" / "data" / "masaq-fil.json.gz"
_ST = dict(zip("0123", STATES, strict=True))
_SYM = {STATES[0]: "فتح", STATES[1]: "كسر", STATES[2]: "ضم", STATES[3]: "سكون"}


def cells(s: str) -> tuple[tuple[str, str], ...]:
    return tuple((s[i], _ST[s[i + 1]]) for i in range(0, len(s), 2))


def _on(k: int, w: tuple[tuple[str, str], ...]) -> bool:
    t = AWZAN[k].template
    r = root_of(t, w)
    return r is not None and "ا" not in r and fill(t, r) == w


def measure() -> dict[str, object]:
    with gzip.open(SLICE, "rt", encoding="utf-8") as f:
        rows = json.load(f)
    past_ayn: Counter[str] = Counter()
    pres_ayn: Counter[str] = Counter()
    templ: Counter[str] = Counter()
    ibdal: Counter[str] = Counter()
    n_pv = n_iv = 0
    for r in rows:
        stem = cells(str(r["s"]))
        tag = str(r["g"])
        madd = any(c[0] in "اوي" and c[1] == STATES[3] for c in stem)
        if tag == "PV" and len(stem) == 3 and stem[-1][1] == STATES[0] and not madd \
                and stem[1][1] != STATES[3]:  # السالمُ المجرّد: فَعَلَ/فَعِلَ/فَعُلَ (المضعَّفُ خارج)
            n_pv += 1
            past_ayn[_SYM[stem[1][1]]] += 1
        if tag == "IV" and len(stem) == 3 and stem[0][1] == STATES[3] and not madd \
                and stem[1][1] != STATES[3]:  # حرفُ المضارعة سابقةٌ في MASAQ: الجذعُ فْعَلُ
            n_iv += 1
            pres_ayn[_SYM[stem[1][1]]] += 1
        if tag in ("PV", "PV_PASS") and not r["n"]:
            hit = next((k for k in (0, 1, 2, *MAZID) if _on(k, stem)), None)
            mudgham = len(stem) >= 5 and stem[:2] == (("ء", STATES[1]), ("ت", STATES[3])) \
                and stem[2][0] == "ت" and _on(17, (stem[0], ("و", STATES[3]), *stem[2:]))
            if mudgham:  # القالبُ يقبله بفاءٍ تاء؛ والفاءُ الأصلُ (و/ي/ء) بعد الإبدال معجم
                templ["اِفْتَعَلَ (مدغمٌ بعد الإبدال)"] += 1
            elif hit is not None:
                templ[AWZAN[hit].name] += 1
            elif read_hollow(stem) is not None:
                templ["فَعَلَ (أجوف بعد القلب)"] += 1
            elif read_doubled(stem) is not None:
                templ["فَعَلَ (مضعَّف بعد الإدغام)"] += 1
            else:
                templ["—"] += 1
            iftaal_shape = (len(stem) >= 3 and stem[0] == ("ء", STATES[1])
                            and stem[1][1] == STATES[3])
            if iftaal_shape:
                fa, ta = stem[1][0], stem[2][0]
                if fa in ITBAQ and ta == "ط":
                    ibdal["تاءٌ ⇒ طاء (" + fa + ")"] += 1
                elif fa in DHZ and ta == "د":
                    ibdal["تاءٌ ⇒ دال (" + fa + ")"] += 1
                elif fa == "ت" and ta == "ت":
                    ibdal["فاءٌ ⇒ تاء مدغمة"] += 1
    return {"past": past_ayn, "pres": pres_ayn, "templ": templ, "ibdal": ibdal, "n": len(rows),
            "n_pv": n_pv, "n_iv": n_iv}


def render() -> str:
    m = measure()
    past: Counter[str] = m["past"]  # type: ignore[assignment]
    pres: Counter[str] = m["pres"]  # type: ignore[assignment]
    templ: Counter[str] = m["templ"]  # type: ignore[assignment]
    ibd: Counter[str] = m["ibdal"]  # type: ignore[assignment]
    lines = [
        "# فهرسُ الفعل على درجات الترخيص التدريجيّ",
        "",
        "مولَّدٌ بـ`python tools/gen_fil_index.py` من `src/slge/fil.py`؛ لا يُحرَّر باليد. البرهانُ: "
        "`formal/Slge/Fil.lean`؛ وردُّ الإعلال مبرهَنٌ في الغانم (`A116.Ilal`). النواسخُ في "
        "`NAWASIKH_INDEX.md`.",
        "",
        "## د٤ الخانة — الأبوابُ أزواجُ حالات", "",
        "(عينُ الماضي، عينُ المضارع) من تسعةٍ ممكنة ستّةٌ (`abwab_six`): "
        + "، ".join(f"{_SYM[p]}–{_SYM[q]}" for p, q in ABWAB)
        + "؛ والساقطةُ " + "، ".join(f"{_SYM[p]}–{_SYM[q]}" for p, q in MISSING) + " ثقلٌ معلَن. "
        "القوالبُ سليمة (`bab_wf`)، وصورُها مرخَّصةٌ لكلّ جذر (`bab_licensed`)، وتُقرأ من الخانتين "
        "(`bab_read`)؛ شرطُ باب فَتَحَ (حلقيّةُ العين أو اللام) يقرؤه `halqi` (`bab_witnesses`: "
        "ضَرَبَ–يَضْرِبُ، فَتَحَ–يَفْتَحُ، فَرِحَ–يَفْرَحُ بشهادات البوّابة).",
        "",
        "## د٨ الحدّ — الزيادةُ طولُ قالب", "",
        "أحرفُ الزيادة = طولُ القالب − 3 (`added`)؛ التسعةُ في `Wazn.awzan` (`mazid_counts`): "
        + "، ".join(f"{AWZAN[k].name} ({added(k)})" for k in MAZID)
        + " — ثلاثةٌ بحرف، خمسةٌ بحرفين، واحدٌ بثلاثة كما في الحصر. لا فعلَ خماسيَّ الأصول: جذرُ `Wazn` "
        "ثلاثيٌّ بالبناء (`root_is_ternary`)؛ والرباعيُّ (دَحْرَجَ، زَلْزَلَ، تَدَحْرَجَ، اِطْمَأَنَّ) أشكالُ "
        "حالاتٍ مرخَّصة (`rubai_shapes`). معاني الصيغ معلَنة.",
        "",
        "## د١٦ — الإعلالُ ثلاثُ عمليّات والإبدالُ ثلاثُ قواعد", "",
        "- **القلب** `qalb`: و/ي متحرّكةٌ بعد فتحٍ ⇒ ألفٌ ساكنة (قَوَلَ ← قَالَ `qalb_witness`؛ يحفظ "
        "الترخيص `qalb_licensed`).",
        "- **النقل** `naql`: حركةُ المعتلّ إلى الساكن قبله (يَقْوُلُ ← يَقُولُ `naql_witness` بشهادة "
        "البوّابة؛ `naql_licensed`).",
        "- **الحذف**: السكونُ بعد المدّ غيرُ مرخَّصٍ فيُحذف المعتلّ (يَقُولُ ← يَقُلْ `hadhf_witness`؛ "
        "`Jazm.hollow_forced`).",
        "- **الإبدال** `ibdal` على اِفْتَعَلَ: تاءٌ ⇒ طاءٌ بعد الإطباق، تاءٌ ⇒ دالٌ بعد د/ذ/ز، فاءٌ و/ي/ء "
        "⇒ تاءٌ مدغمة — لا يغيّر نمطَ السكون فيحفظ الترخيص (`ibdal_licensed`)؛ اِصْطَبَرَ اِزْدَهَرَ اِتَّصَلَ "
        "اِتَّخَذَ (`ibdal_witnesses`)، واصْطَفَى وازْدَادُوا واتَّخَذَ بشهادة البوّابة.",
        "",
        "## القياس على MASAQ", "",
        f"على {m['n']} فعلًا بشهادات البوّابة (الجذعُ بعد السابقة وقبل اللاحقة):", "",
        f"### عينُ الماضي المجرّد السالم ({m['n_pv']}) وعينُ مضارعه ({m['n_iv']})", "",
        "| عينُ الماضي | العدد |", "|---|---|",
        *[f"| {k} | {v} |" for k, v in past.most_common()],
        "",
        "| عينُ المضارع | العدد |", "|---|---|",
        *[f"| {k} | {v} |" for k, v in pres.most_common()],
        "",
        "الماضي ثلاثُ حركاتٍ والمضارعُ ثلاثٌ — والزوجُ (البابُ) قانونُ معجمٍ يجمع الصورتين: الخانةُ تقرأ كلَّ "
        "صورةٍ وحدَها.",
        "",
        "### الماضي على القوالب (بلا لاحقة)", "",
        "| القالب | العدد |", "|---|---|",
        *[f"| {k} | {v} |" for k, v in templ.most_common(14)],
        "",
        "ما بعد القالب يُقرأ بالعمليّة (دَينٌ سُدِّد): الأجوفُ [ف، ا، ل] بعد القلب (`qalb_pastT`؛ "
        "`read_hollow`: قَالَ، جَاءَ)، والمضعَّفُ [ف، عْ، ع] بعد الإدغام (`idgham_pastT`؛ `read_doubled`: "
        "رَدَّ)، واِفْتَعَلَ المدغمُ بعد الإبدال (اِتَّخَذَ: القالبُ يقبله بفاءٍ تاء، والفاءُ الأصلُ و/ي/ء "
        "معجم — `ibdal`). "
        "وما بقي (—): ناقصٌ ومثالٌ ولفيفٌ وأجوفٌ على المزيد — إعلالٌ بعد القالب، بقيّةٌ مسمّاة.",
        "",
        "### الإبدالُ في اِفْتَعَلَ", "",
        "| القاعدة | العدد |", "|---|---|",
        *[f"| {k} | {v} |" for k, v in ibd.most_common()],
        "",
        "## ما لا تقرؤه الخانة — باسمه", "",
        "- معاني صيغ الزيادة (التعدية، المشاركة، المطاوعة، الطلب): معلَن.",
        "- اختيارُ الباب لجذرٍ بعينه (نَصَرَ–يَنْصُرُ لا يَنْصِرُ): معجم.",
        "- أمرُ المزيد: قوالبُ 113–120 من مضارعه بقاعدة أمر المجرّد (`amr_of_pres`)؛ أَفْعِلْ يفرّقه القطعُ "
        "المفتوح، وأمرُ اِفْعَلَّ بالقاعدة ساكنان غيرُ مرخَّصين (`amr_ifalla_unlicensed`) — فكُّ الإدغام "
        "بقيّةٌ مسمّاة.",
        "- شريحةُ MASAQ: 374 صورةً مستبعَدة (فارغٌ بعد السابقة 316، مرفوضٌ بالاسم 58).",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    text = render()
    if "--check" in sys.argv:
        if TARGET.read_text(encoding="utf-8") != text:
            sys.stderr.write("FIL_INDEX.md غيرُ مطابق؛ شغّل tools/gen_fil_index.py\n")
            return 1
        sys.stdout.write("FIL_INDEX.md مطابق\n")
        return 0
    TARGET.write_text(text, encoding="utf-8")
    sys.stdout.write("كُتب FIL_INDEX.md\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
