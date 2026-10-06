"""ولّد `MAJRURAT_INDEX.md`: فهرسُ المجرورات على درجات الترخيص التدريجيّ من `slge.majrurat`، وقياسُ
العلامات الثلاث وأسباب الجرّ على شريحة MASAQ المجمَّدة (مجرورٌ ومضافٌ بشهادات البوّابة)؛ ‎--check‎."""

from __future__ import annotations

import gzip
import json
import sys
from collections import Counter
from pathlib import Path

from slge.adad import uqud_case
from slge.cells import STATES, index
from slge.majrurat import GATE, HARFS, PROCLITIC
from slge.mansubat import derived
from slge.nida import has_tanwin
from slge.rawabit import cells_of
from slge.tawabi import case_class, compatible

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "MAJRURAT_INDEX.md"
SLICE = ROOT / "tests" / "data" / "masaq-majrurat.json.gz"
_ST = dict(zip("0123", STATES, strict=True))
TABI = ("نعت", "اسم معطوف", "بدل", "توكيد")


def load() -> list[dict[str, object]]:
    with gzip.open(SLICE, "rt", encoding="utf-8") as f:
        return json.load(f)  # type: ignore[no-any-return]


def cells(s: str) -> tuple[tuple[str, str], ...]:
    return tuple((s[i], _ST[s[i + 1]]) for i in range(0, len(s), 2))


def measure() -> dict[str, object]:
    rows = load()
    marker: Counter[tuple[str, str]] = Counter()
    sabab: Counter[tuple[str, str]] = Counter()
    harf: Counter[str] = Counter()
    mudaf_tanwin: Counter[tuple[str, bool]] = Counter()
    nun: Counter[bool] = Counter()
    lafzi: Counter[tuple[str, bool]] = Counter()
    mabni = 0
    for r in rows:
        stem = cells(str(r["s"]))
        if r["c"] == "مجرور":
            if r["e"] != "معرب":
                mabni += 1
            else:
                cc = case_class(stem)
                read = "جرّ" if compatible(cc, "جرّ") else cc
                m = str(r["m"]).replace("الفتحة (ممنوع من الصرف)", "الفتحة")
                marker[(m, read)] += 1
                role = str(r["r"])
                sabab[("التبعيّة" if role in TABI else "الإضافة" if role == "مضاف إليه" else
                       "الحرف" if role == "اسم مجرور" else "غيره", read)] += 1
                if role == "اسم مجرور":
                    harf[str(r["h"] or "—")] += 1
        if r["u"] and r["e"] == "معرب":
            dual_end = stem[-2:] == (("ي", STATES[3]), ("ن", STATES[1]))
            kind = "جمعٌ أو مثنًّى" if (uqud_case(stem) is not None or dual_end) else "مفرد"
            mudaf_tanwin[(kind, bool(r["t"]) or has_tanwin(stem))] += 1
            if stem and stem[-1] in (("و", STATES[3]), ("ي", STATES[3])) and len(stem) >= 2 \
                    and stem[-2][1] in (STATES[2], STATES[1], STATES[0]) and not r["n"]:
                nun[True] += 1  # مضافٌ آخرُه المدُّ بلا نون: مُهَنْدِسُو
            lafzi[("مشتقّ" if derived(stem) else "غيره", True)] += 1
    return {"marker": marker, "sabab": sabab, "harf": harf, "mudaf_tanwin": mudaf_tanwin,
            "nun": nun, "lafzi": lafzi, "n": len(rows), "mabni": mabni}


def _cells(w: str) -> str:
    return "-".join(str(index(c)) for c in cells_of(w))


def render() -> str:
    m = measure()
    marker: Counter[tuple[str, str]] = m["marker"]  # type: ignore[assignment]
    sabab: Counter[tuple[str, str]] = m["sabab"]  # type: ignore[assignment]
    harf: Counter[str] = m["harf"]  # type: ignore[assignment]
    mt: Counter[tuple[str, bool]] = m["mudaf_tanwin"]  # type: ignore[assignment]
    nun: Counter[bool] = m["nun"]  # type: ignore[assignment]
    lafzi: Counter[tuple[str, bool]] = m["lafzi"]  # type: ignore[assignment]
    lines = [
        "# فهرسُ المجرورات على درجات الترخيص التدريجيّ",
        "",
        "مولَّدٌ بـ`python tools/gen_majrurat_index.py` من `src/slge/majrurat.py`؛ لا يُحرَّر باليد. "
        "البرهانُ: `formal/Slge/Majrurat.lean`. الشاهدُ بلا علامةٍ بشهادة البوّابة؛ و° مودَعٌ على "
        "طريقتها.",
        "",
        "## د٤ الخانة — الجرُّ عمليّةٌ واحدة وعلاماتُه ثلاث", "",
        "| العلامة | العمليّة | المبرهَن |", "|---|---|---|",
        "| الكسرة | `jarr = setLast · 1` (وللنكرة `tanwin`) | تُقرأ جرًّا لكلّ جذعٍ آخرُه غيرُ نونٍ وتاء "
        "(`caseClass_jarr`)، ومنوَّنةً لكلّ جذع (`caseClass_jarr_tanwin`)؛ تحفظ الترخيص "
        "(`jarr_licensed`)؛ يحكم عليها جدولُ الأدوات (`govern_jarr`) |",
        "| الياء | `Adad.uqud _ false`، `dual` | نصبٌ أو جرّ — الخانةُ لا تفصلهما "
        "(`uqud_jarr_compatible`، `dual_jarr_compatible`)؛ والخمسةُ `Khamsa.form _ .jarr` لا "
        "يقرؤها القارئُ العامّ (`khamsa_jarr_unread`: الياءُ بعد كسرٍ مشتركةٌ مع المنقوص) |",
        "| الفتحة | `Sarf.mamnuJarr` | تُقرأ نصبًا (`mamnu_jarr_reads_nasb`): الجرُّ من جدول العلل؛ "
        "وبأل كسرٌ (`masajid_witness`: مَسَاجِدَ/الْمَسَاجِدِ) |",
        "",
        "## د٨ الحدّ — سببُ الجرّ", "",
        "- **الحرف**: " + ", ".join(f"{h}{'' if h in GATE else '°'} `{_cells(h)}`" for h in HARFS)
        + f" (`harfs_licensed`، {len(HARFS)} من العشرين المعلَنة)؛ المتّصلةُ الخمسةُ لا تُفسد ما بعدها "
        "(`proclitic_jarr_licensed`)؛ ثمانيةٌ في جدول أدوات الربط جارّةً (`harfs_in_rawabit`). "
        "رُبَّ للنكرة: النكرةُ المجرورةُ تحمل التنوين (`rubba_nakira`). تَاللَّهِ خارج الترخيص "
        "الثنائيّ (مدٌّ فلامٌ مشدّدة) كحَاجَّ، ووَاللَّهِ مرخَّصة (`qasam_witness`).",
        "- **الإضافة**: إسقاطُ التنوين (`mudaf_no_tanwin`)، وإسقاطُ نون الجمع والمثنّى "
        "(`mudaf_drops_nun`؛ مُهَنْدِسُو `muhandisu_witness`)؛ اللفظيّةُ يقرؤها القالب: صَانِعُ مشتقّ، "
        "كِتَابُ جامد (`lafziyya_by_template`)؛ والمضافُ إلى ضميرٍ معرفة (`mudaf_marifa`).",
        "- **التبعيّة**: توافقٌ في الحالة (`tabi_jarr_follows`؛ بِرَجُلٍ صَالِحٍ `rajul_salih`).",
        "",
        "## القياس على MASAQ", "",
        f"على {m['n']} مجرورٍ ومضافٍ بشهادات البوّابة ({m['mabni']} مبنيٌّ: صورٌ مودَعة):", "",
        "### علامةُ MASAQ مقابلَ قراءة الخانة", "",
        "| علامةُ MASAQ | قراءةُ الخانة | العدد |", "|---|---|---|",
        *[f"| {a} | {b} | {v} |" for (a, b), v in marker.most_common(12)],
        "",
        "الكسرةُ جرٌّ؛ الياءُ نصبٌ/جرّ (جمعٌ ومثنًّى) أو لا تقرؤها الخانة (الخمسةُ والمنقوص)؛ الفتحةُ "
        "نصبٌ (الممنوع) — كما بُرهن. والكسرةُ التي تُقرأ رفعًا: المفردُ المختومُ بألفٍ ونون (إِيمَانِ، "
        "شَيْطَانِ) خانتُه خانةُ المثنّى المرفوع (`an_kasra_shared`) — المعجمُ يفصل. والسكونُ: المضافُ إلى "
        "ياء المتكلّم والمقصورُ: مقدَّر.",
        "",
        "### سببُ الجرّ", "",
        "| السبب | قراءةُ الخانة | العدد |", "|---|---|---|",
        *[f"| {a} | {b} | {v} |" for (a, b), v in sabab.most_common(12)],
        "",
        "### الحرفُ الجارّ (اسمٌ مجرور)", "",
        "| الحرف | العدد |", "|---|---|",
        *[f"| {h} | {v} |" for h, v in harf.most_common(12)],
        "",
        "### قانونُ حسم المضاف", "",
        "| المضاف | منوَّن | العدد |", "|---|---|---|",
        *[f"| {k} | {'نعم' if t else 'لا'} | {v} |" for (k, t), v in sorted(mt.items())],
        "",
        f"- مضافٌ آخرُه مدٌّ بلا نون (مُهَنْدِسُو، أَبُو): {nun[True]}. والمفردُ المضافُ المنوَّن: تنوينُ "
        "العوض (كُلٍّ، يَوْمَئِذٍ) — استثناءٌ مسمًّى في `Marifa`.",
        "- الإضافةُ اللفظيّة (المضافُ على قالب وصف): "
        + "، ".join(f"{k} {v}" for (k, _), v in sorted(lafzi.items())) + ".",
        "",
        "## ما لا تقرؤه الخانة — باسمه", "",
        "- معاني الإضافة (اللام، مِنْ، فِي) والتعريفُ والتخصيصُ بها: معلَن/تيار.",
        "- اختصاصُ التاء بلفظ الجلالة، ورُبَّ بالنكرة، ومُذْ ومُنْذُ بالزمان: تيار.",
        "- الخمسةُ بالياء والمنقوصُ والمقصورُ: المعجم.",
        f"- شريحةُ MASAQ: الأدواتُ المتّصلة {len(PROCLITIC)} تُعدّ من السابقة لا من الخانة.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    text = render()
    if "--check" in sys.argv:
        if TARGET.read_text(encoding="utf-8") != text:
            sys.stderr.write("MAJRURAT_INDEX.md غيرُ مطابق؛ شغّل tools/gen_majrurat_index.py\n")
            return 1
        sys.stdout.write("MAJRURAT_INDEX.md مطابق\n")
        return 0
    TARGET.write_text(text, encoding="utf-8")
    sys.stdout.write("كُتب MAJRURAT_INDEX.md\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
