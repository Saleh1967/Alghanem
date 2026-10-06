"""ولّد `ISM_INDEX.md`: فهرسُ الاسم (المجرّد، التصغير، النسب، البناءُ العارض) على درجات الترخيص
التدريجيّ من `slge.ism`، وقياسُ أشكاله على شريحة MASAQ المجمَّدة (أسماءُ المصحف بشهادات البوّابة)؛
‎--check‎."""

from __future__ import annotations

import gzip
import json
import sys
from collections import Counter
from pathlib import Path

from slge.cells import STATES, index
from slge.ism import DROPPED, KHUMASI, NAMES, RUBAI, TEN, is_nisba, is_tasghir, read_thulathi, shape
from slge.rawabit import cells_of

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "ISM_INDEX.md"
SLICE = ROOT / "tests" / "data" / "masaq-ism.json.gz"
_ST = dict(zip("0123", STATES, strict=True))
_SYM = {STATES[0]: "َ", STATES[1]: "ِ", STATES[2]: "ُ", STATES[3]: "ْ"}


def cells(s: str) -> tuple[tuple[str, str], ...]:
    return tuple((s[i], _ST[s[i + 1]]) for i in range(0, len(s), 2))


def measure() -> dict[str, object]:
    with gzip.open(SLICE, "rt", encoding="utf-8") as f:
        rows = json.load(f)
    thul: Counter[tuple[str, str]] = Counter()
    rub: Counter[tuple[str, ...]] = Counter()
    tas: Counter[str] = Counter()
    nis: Counter[str] = Counter()
    n3 = n4 = 0
    for r in rows:
        stem = cells(str(r["s"]))
        if stem and stem[-1] == ("ن", STATES[3]) and len(stem) >= 2 and stem[-2][1] != STATES[3]:
            stem = stem[:-1]  # التنوين
        if any(c[0] in "اوي" and c[1] == STATES[3] for c in stem[:-1]):
            if is_tasghir(stem):
                tas[str(r["w"])] += 1
            if is_nisba(stem):
                nis[str(r["w"])] += 1
            continue  # المدُّ زائدٌ لا أصل: خارج المجرّد الثلاثيّ والرباعيّ
        if is_nisba(stem):
            nis[str(r["w"])] += 1
        if is_tasghir(stem):
            tas[str(r["w"])] += 1
        if len(stem) == 3:
            n3 += 1
            p = read_thulathi(stem)
            if p is not None and p[0] != STATES[3]:
                thul[p] += 1  # ما فاؤه ساكنةٌ (بعد سابقةٍ أو همزةٍ ساقطة) خارج القراءة
        elif len(stem) == 4:
            n4 += 1
            rub[shape(stem)] += 1
    return {"thul": thul, "rub": rub, "tas": tas, "nis": nis, "n": len(rows), "n3": n3, "n4": n4}


def _cells(w: str) -> str:
    return "-".join(str(index(c)) for c in cells_of(w))


def _shape_name(sh: tuple[str, ...]) -> str:
    return "ف" + _SYM[sh[0]] + "ع" + _SYM[sh[1]] + "ل" + _SYM[sh[2]] + "ل"


def render() -> str:
    m = measure()
    thul: Counter[tuple[str, str]] = m["thul"]  # type: ignore[assignment]
    rub: Counter[tuple[str, ...]] = m["rub"]  # type: ignore[assignment]
    tas: Counter[str] = m["tas"]  # type: ignore[assignment]
    nis: Counter[str] = m["nis"]  # type: ignore[assignment]
    ten_total = sum(v for p, v in thul.items() if p in TEN)
    dropped_total = sum(v for p, v in thul.items() if p in DROPPED)
    lines = [
        "# فهرسُ الاسم على درجات الترخيص التدريجيّ",
        "",
        "مولَّدٌ بـ`python tools/gen_ism_index.py` من `src/slge/ism.py`؛ لا يُحرَّر باليد. البرهانُ: "
        "`formal/Slge/Ism.lean`.",
        "",
        "## د٤ الخانة — المجرّدُ الثلاثيُّ عشرةٌ = 3 × 4 − 2", "",
        "حركةُ الفاء (فتح/ضم/كسر) في حالة العين (فتح/ضم/كسر/سكون) اثنا عشرَ قالبًا (`twelve`)، يسقط "
        "فُعُل وفِعُل (`dropped`) فتبقى عشرة (`thulathi_ten`)، كلُّها سليمةُ البناء (`thulathi_wf`) "
        "ومرخَّصةٌ لكلّ جذر (`thulathi_licensed`)، وتُقرأ من الخانتين الأُوليين (`thulathi_read`؛ "
        "الشواهدُ `witnesses_read`، ورَجُل بشهادة البوّابة). الحصرُ يسمّي «فُعِل» في الساقطين ثمّ يعدّها في "
        "العشرة بدُئِل: الجدولُ يفصل — الساقطان فُعُل وفِعُل.",
        "",
        "الرباعيُّ والخماسيُّ أشكالُ حالاتٍ (`shape`) لا قوالبُ `Wazn` (ثلاثيّةُ الجذر): الحصرُ يعدّ الرباعيَّ "
        "ستّةً ويسمّي فَعْلَل مرّتين (جَعْفَر، طَحْلَب) — الأشكالُ خمسة (`rubai_shapes`)؛ والخماسيُّ أربعة "
        "(`khumasi_shapes`): " + ", ".join(f"{w} `{_cells(w)}`" for w in RUBAI + KHUMASI) + ".",
        "",
        "## د٨ الحدّ — التصغيرُ والنسبُ عمليّات", "",
        "- **التصغير** ثلاثُ عمليّات: فُعَيْل `saghir3`، فُعَيْعِل `saghir4`، فُعَيْعِيل `saghir5` — تحفظ "
        "الترخيصَ لكلّ جذر (`tasghir_licensed`) ويقرؤها القارئُ من ضمٍّ ففتحٍ فياءٍ ساكنة "
        "(`tasghir_read`)؛ "
        "رُجَيْل ودُرَيْهِم وعُصَيْفِير (`tasghir_witnesses`)، وبُنَيَّ بشهادة البوّابة.",
        "- **النسب** عمليّةٌ واحدة `nisba` (كسرٌ فياءٌ مشدّدة) بعد تهيئةٍ مسمّاة `prepare` (حذفُ التاء، "
        "المقصورُ الثالثُ واوًا والرابعُ حذفًا، المنقوصُ الثالثُ واوًا بفتح ما قبله والرابعُ حذفًا)؛ تحفظ "
        "الترخيص (`nisba_licensed`) وتُقرأ (`nisba_read`)؛ مِصْرِيّ مَكِّيّ عَصَوِيّ مُصْطَفِيّ عَمَوِيّ قَاضِيّ "
        "(`nisba_witnesses`)، وعَرَبِيٌّ بشهادة البوّابة.",
        "",
        "## د١٦ الإعراب من الخانة — البناءُ العارض", "",
        "الأربعةُ في الحصر عمليّاتٌ على الآخر بحالةٍ ثابتة، كلٌّ في بابه (`arid_bina`): ضمُّ المنادى "
        "(`Nida.damm_is_bina`)، فتحُ اسم لا (`Nawasikh.laJins`)، ضمُّ الظرف المقطوع "
        "(`Zuruf.hukm_qat`)، "
        "فتحُ العدد المركّب (`Adad.compound_both_fatha`). واللازمُ جداولُ صورٍ مودَعة: 71 صورةً "
        "(الضمائر، الإشارة، الاستفهام، الشرط) لا عمليّةَ على آخرها (`lazim_deposited`).",
        "",
        "## القياس على MASAQ", "",
        f"على {m['n']} اسمًا معربًا بشهادات البوّابة (الجذعُ بعد السابقة وقبل الضمير، بلا تنوين؛ "
        "وما فيه مدٌّ زائدٌ خارج المجرّد):", "",
        f"### الثلاثيّ ({m['n3']}): حركةُ الفاء وحالةُ العين", "",
        "| القالب | العدد |", "|---|---|",
        *[f"| {NAMES[p]}{' (ساقط)' if p in DROPPED else ''} | {v} |"
          for p, v in thul.most_common()],
        "",
        f"العشرةُ {ten_total}، والساقطان {dropped_total} — وكلُّ ما على فُعُل جمعٌ (رُسُل، كُتُب، سُبُل: "
        "قالبُ الجمع `Wazn.awzan[88]`) لا مفردٌ مجرّد؛ فالحصرُ عن المفرد مقيس، وفِعُل معدومة.",
        "",
        f"### الرباعيّ ({m['n4']}): أشكالُ الحالات", "",
        "| الشكل | العدد |", "|---|---|",
        *[f"| {_shape_name(sh)} | {v} |" for sh, v in rub.most_common(10)],
        "",
        "فَعْلَل وفِعْلَل وفُعْلُل من أشكال الحصر؛ وفَعَلَل (نحو عَرَفَات قبل التاء) وفَعِلَل (كَلِمَت) أشكالُ "
        "المزيد بتاء التأنيث والجمع لا المجرّد — المعجمُ يفصل.",
        "",
        "### التصغيرُ والنسبُ في المصحف (بالقارئ)", "",
        f"- تصغير ({sum(tas.values())}): "
        + "، ".join(f"{w} {v}" for w, v in tas.most_common(8)) + ".",
        f"- نسب ({sum(nis.values())}): "
        + "، ".join(f"{w} {v}" for w, v in nis.most_common(10)) + ".",
        "",
        "## ما لا تقرؤه الخانة — باسمه", "",
        "- الماهيةُ (الجوهرُ الثابت) والتعليمُ الأوّل: معلَن.",
        "- عملُ اسم الفاعل في مفعولين ومسألةُ الكحل: تيار.",
        "- فُعَيْل الأعلامُ (كُلَيْب) والتصغيرُ: خانةٌ واحدة — المعجم.",
        "- شريحةُ MASAQ: 1,824 صورةً مرفوضةٌ بالاسم (REJECT 1,751: التنوينُ بعد الألف؛ OUTSIDE 73).",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    text = render()
    if "--check" in sys.argv:
        if TARGET.read_text(encoding="utf-8") != text:
            sys.stderr.write("ISM_INDEX.md غيرُ مطابق؛ شغّل tools/gen_ism_index.py\n")
            return 1
        sys.stdout.write("ISM_INDEX.md مطابق\n")
        return 0
    TARGET.write_text(text, encoding="utf-8")
    sys.stdout.write("كُتب ISM_INDEX.md\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
