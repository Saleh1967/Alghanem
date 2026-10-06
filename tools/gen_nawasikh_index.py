"""ولّد `NAWASIKH_INDEX.md`: فهرسُ النواسخ على درجات الترخيص التدريجيّ من `slge.nawasikh`، وقياسُ
العمليّتين على شريحة MASAQ المجمَّدة (أسماءُ النواسخ وأخبارُها بشهادات البوّابة)؛ ‎--check‎."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

from slge.cells import index
from slge.marifa import has_al
from slge.nawasikh import GATE, INNA, KADA, KANA, LA, ZANNA, kaffa
from slge.nida import has_tanwin
from slge.rawabit import cells_of
from slge.tawabi import case_class, compatible

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "NAWASIKH_INDEX.md"
SLICE = ROOT / "tests" / "data" / "masaq-nawasikh.json"

EXPECT = {"اسم فعل ناسخ": "رفع", "خبر فعل ناسخ": "نصب", "اسم حرف ناسخ": "نصب",
          "خبر حرف ناسخ": "رفع", "اسم لا النافية للجنس": "نصب"}


def measure() -> dict[str, object]:
    """لكلّ دور: (موافقٌ | مخالفٌ | لا تقرؤه الخانة) بقارئ الحالة؛ واسمُ لا: بلا تنوينٍ ولا أداة؛
    وكاد: هل يليها أَنْ؛ وإنّما: ما بعدها."""

    data = json.loads(SLICE.read_text(encoding="utf-8"))
    table: Counter[tuple[str, str]] = Counter()
    detail: Counter[tuple[str, str]] = Counter()
    la_ok = 0
    mabni = 0
    ba = 0
    for row in data["cells"]:
        stem = tuple((c[0], c[1]) for c in row["stem"])
        role = row["role"]
        if row["declinable"] != "معرب" and not role.startswith("اسم لا"):
            mabni += 1  # ضميرٌ وموصولٌ وإشارة: صورٌ مودَعةٌ لا حالةَ تُقرأ من آخرها
            continue
        if role.startswith("خبر") and "ب" in row["prefixes"]:
            ba += 1  # الباءُ الزائدة في خبر ليس وما: جرٌّ لفظيّ
            continue
        cc = case_class(stem)
        if cc.startswith("لا تقرؤه"):
            table[(role, "لا تقرؤه الخانة")] += 1
        elif compatible(cc, EXPECT[role]):
            table[(role, "موافق")] += 1
        else:
            table[(role, "مخالف")] += 1
            detail[(role, cc)] += 1
        if role == "اسم لا النافية للجنس" and not has_tanwin(stem) and not has_al(stem) \
                and not row["det"] and not row["tanwin"]:
            la_ok += 1
    kada: Counter[tuple[str, bool]] = Counter()
    for k in data["kada"]:
        verb = {"كد": "كاد", "عسي": "عسى"}.get(k["verb"], k["verb"])
        kada[(verb, any(n[0] == "أن" for n in k["next"]))] += 1
    innama: Counter[tuple[str, str]] = Counter()
    for i in data["innama"]:
        innama[(i["seg"], i["next"][0][2] if i["next"] else "—")] += 1
    lemmas: Counter[str] = Counter()
    for role, seg, n in data["lemmas"]:
        if "فعل" in role or "حرف ناسخ" in role or role.startswith("لا") or role.startswith("ما"):
            lemmas[seg] += n
    return {"table": table, "detail": detail, "la_ok": la_ok, "kada": kada, "innama": innama,
            "lemmas": lemmas, "n": len(data["cells"]), "mabni": mabni, "ba": ba,
            "n_la": sum(1 for r in data["cells"] if r["role"].startswith("اسم لا"))}


def _cells(w: str) -> str:
    return "-".join(str(index(c)) for c in cells_of(w))


def _deposit(name: str, words: tuple[str, ...]) -> str:
    items = ", ".join(f"{w}{'' if w in GATE else '°'} `{_cells(w)}`" for w in words)
    return f"- **{name}** ({len(words)}): {items}"


def render() -> str:
    m = measure()
    table: Counter[tuple[str, str]] = m["table"]  # type: ignore[assignment]
    detail: Counter[tuple[str, str]] = m["detail"]  # type: ignore[assignment]
    kada: Counter[tuple[str, bool]] = m["kada"]  # type: ignore[assignment]
    innama: Counter[tuple[str, str]] = m["innama"]  # type: ignore[assignment]
    lemmas: Counter[str] = m["lemmas"]  # type: ignore[assignment]
    lines = [
        "# فهرسُ النواسخ على درجات الترخيص التدريجيّ",
        "",
        "مولَّدٌ بـ`python tools/gen_nawasikh_index.py` من `src/slge/nawasikh.py`؛ لا يُحرَّر باليد. "
        "البرهانُ: `formal/Slge/Nawasikh.lean`. الشاهدُ بلا علامةٍ بشهادة البوّابة (في المصحف)؛ "
        "و° مودَعٌ على طريقتها.",
        "",
        "## د٤ الخانة — أربعةُ أبوابٍ عمليّتان", "",
        "على الخانات عمليّتان لا غير: `raf` (ضمٌّ في الآخر) و`nasb` (فتحٌ في الآخر)؛ والتنوينُ "
        "عمليّةٌ ثالثةٌ منفصلة `tanwin` (الحركةُ وحدَها لا تنوينَ معها: `raf_no_tanwin`، "
        "`nasb_no_tanwin`). العمليّتان تحفظان الترخيص (`raf_licensed`، `nasb_licensed`).", "",
        "| الباب | الاسم | الخبر | المبرهَن |", "|---|---|---|---|",
        "| كان وأخواتها | رفع | نصب | `kana` |",
        "| كاد وأخواتها | رفع | نصب | `kada_eq_kana` — عملُ كان بعينه |",
        "| إنّ وأخواتها | نصب | رفع | `inna_eq_swap_kana` — عكسُ كان |",
        "| لا النافية للجنس | نصب | رفع | `laJins_eq_inna` |",
        "| ظنّ وأخواتها | نصب | نصب (مفعولان) | `zanna_both_nasb` |",
        "",
        "### المودَعات (مرخَّصةٌ ثنائيًّا: `kana_licensed`، `kada_licensed`، `inna_licensed`، "
        "`zanna_licensed`)", "",
        _deposit("كان وأخواتها", KANA),
        _deposit("كاد وأخواتها", KADA),
        _deposit("إنّ وأخواتها", INNA) + f"؛ ولا النافيةُ للجنس {LA} `{_cells(LA)}`",
        _deposit("ظنّ وأخواتها", ZANNA),
        "",
        "الحصرُ يعدّ كاد «11» ويسمّي 12، ويعدّ ظنّ 16 وجَعَلَ فيها مرّتان: الخانةُ واحدةٌ "
        "(`jaala_shared`: جَعَلَ في بابَي كاد وظنّ) والمعنى (الشروع/الرجحان/التحويل) معجم.",
        "",
        "## د٨ الحدّ — الكفُّ وخبرُ كاد", "",
        "- **الكفّ**: `kaffa` تُلحق «مَا» (`kaffa_licensed`)؛ والصورُ الستّ هي العمليّةُ على الستّة "
        "(`kaffa_forms`): "
        + "، ".join(f"{w}مَا `{'-'.join(str(index(c)) for c in kaffa(cells_of(w)))}`" for w in INNA)
        + ". وجدولُ أدوات الربط يسجّل إِنَّ ناصبةً "
        "للاسم وإِنَّمَا بلا عمل (`innama_kaffa_in_rawabit`)؛ ولَيْتَمَا خانتُها خانةُ الباقي "
        "(`laytama_cells`): جوازُ الإعمال قرارُ تيار.",
        "- **خبرُ كاد مضارع**: صورةٌ من الأفعال الخمسة مرفوعةٌ (`kada_khabar_raf`)، وبأَنْ منصوبةٌ "
        "(`an_khabar_nasb`)؛ وأَنْ مرخَّصةٌ لكنّها ليست في جدول أدوات الربط (`an_not_in_rawabit`) "
        "— دَينٌ مسمًّى.",
        "- أربعةٌ من أخوات إنّ في جدول أدوات الربط بعملها (`inna_in_rawabit`)؛ وكَأَنَّ ولَيْتَ ليستا "
        "فيه. ولَيْسَ ولَا ومَا فيه بلا عملٍ مسجَّل (`laysa_la_ma_in_rawabit`).",
        "",
        "## د١٦ الإعراب من الخانة — ما رُفع يُقرأ رفعًا وما نُصب نصبًا", "",
        "- `caseClass_raf`: لكلّ جذعٍ غيرِ فارغ، ما ضُمّ آخرُه يُقرأ رفعًا (ومع التنوين "
        "`caseClass_raf_tanwin`، ومع أل `caseClass_al_raf`).",
        "- `caseClass_nasb`: ما فُتح آخرُه يُقرأ نصبًا إن لم يكن آخرُه نونًا (نونُ ُونَ/ِينَ قانونُها "
        "قانونُ العقود: `uqud_nasb_compatible`)؛ ومع التنوين لكلّ جذع `caseClass_nasb_tanwin`.",
        "- اسمُ لا النافية للجنس: فتحٌ بلا تنوينٍ ولا أداة، يُقرأ نصبًا (`laJins_ism_no_tanwin`).",
        "- شاهدان: كَانَ اللَّهُ غَفُورًا / إِنَّ اللَّهَ غَفُورٌ (`kana_inna_witness`)، "
        "لَا رَيْبَ (`la_rayb_witness`).",
        "",
        "## القياس على MASAQ — العمليّتان في المصحف", "",
        f"على {m['n']} اسمٍ وخبرٍ للنواسخ بشهادات البوّابة (الجذعُ قبل الضمير وبعد السابقة): "
        f"{m['mabni']} مبنيٌّ (ضميرٌ وموصولٌ وإشارة: صورٌ مودَعةٌ لا حالةَ في آخرها)، و{m['ba']} خبرٌ "
        "بالباء الزائدة (ليس/ما: جرٌّ لفظيّ)؛ والباقي بقارئ الحالة `caseClass`:", "",
        "| الدور | المتوقَّع | موافق | مخالف | لا تقرؤه الخانة | نسبةُ الموافقة فيما تقرؤه |",
        "|---|---|---|---|---|---|",
    ]
    for role, exp in EXPECT.items():
        ok, bad = table[(role, "موافق")], table[(role, "مخالف")]
        un = table[(role, "لا تقرؤه الخانة")]
        pct = f"{100 * ok // (ok + bad)}%" if ok + bad else "—"
        lines.append(f"| {role} | {exp} | {ok} | {bad} | {un} | {pct} |")
    lines += [
        "",
        f"- اسمُ لا النافية للجنس: {m['la_ok']}/{m['n_la']} بلا تنوينٍ ولا أداة (نكرةٌ مفتوحة).",
        "- المخالفُ (حالةُ القارئ): "
        + "؛ ".join(f"{r}: {cc} {v}" for (r, cc), v in detail.most_common(8))
        + " — جهتان مسمّاتان: المضافُ إلى ياء المتكلّم (مقدَّر: رَبِّي)، والمنقوصُ (نَاجٍ) — "
        "دُيونٌ على القارئ لا على العمليّتين (وجمعُ المؤنّث السالم صار يقرؤه القارئ: "
        "`Tawabi.caseClass_jam_muannath`).",
        "",
        "### اقترانُ خبر كاد وأخواتها بأَنْ (الحصر: يقلّ مع كاد، يكثر مع عسى، يمتنع في الشروع)", "",
        "| الفعل | بأَنْ | بلا أَنْ |", "|---|---|---|",
    ]
    for verb in ("كاد", "عسى", "طفق"):
        lines.append(f"| {verb} | {kada[(verb, True)]} | {kada[(verb, False)]} |")
    lines += [
        "",
        "### إنّما الكافّة: ما بعدها", "",
        "| الحرف | ما بعده | العدد |", "|---|---|---|",
        *[f"| {seg} | {nxt} | {v} |" for (seg, nxt), v in innama.most_common()],
        "",
        "لا «اسمَ حرفٍ ناسخ» بعد إنّما في المصحف: الكفُّ مقيس.",
        "",
        "### ألفاظُ النواسخ في المصحف (الصورةُ المقطَّعة في MASAQ)", "",
        "| اللفظ | العدد |", "|---|---|",
        *[f"| {seg} | {v} |" for seg, v in lemmas.most_common(14)],
        "",
        "## ما لا تقرؤه الخانة — باسمه", "",
        "- الجامدُ (لَيْسَ، دَامَ) والمتصرّف، والتمامُ (كان بمعنى وُجد): معجمٌ وتيار.",
        "- شرطُ النفي قبل زَالَ وأخواتها، و«ما» المصدريّة قبل دَامَ، وشرطُ الفعليّة في خبر كاد: تيار.",
        "- التعليقُ والإلغاءُ في ظنّ، وجوازُ إعمال لَيْتَمَا: تيار.",
        "- عللُ المعنى (الرجحان/اليقين/التحويل؛ المقاربة/الرجاء/الشروع): معجم.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    text = render()
    if "--check" in sys.argv:
        if TARGET.read_text(encoding="utf-8") != text:
            sys.stderr.write("NAWASIKH_INDEX.md غيرُ مطابق؛ شغّل tools/gen_nawasikh_index.py\n")
            return 1
        sys.stdout.write("NAWASIKH_INDEX.md مطابق\n")
        return 0
    TARGET.write_text(text, encoding="utf-8")
    sys.stdout.write("كُتب NAWASIKH_INDEX.md\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
