"""ولّد `MANSUBAT_INDEX.md`: فهرسُ بقيّة المنصوبات (الحال، التمييز، الاستثناء) على درجات الترخيص
التدريجيّ من `slge.mansubat`، وقياسُها على شريحة MASAQ المجمَّدة بشهادات البوّابة؛ ‎--check‎."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

from slge.adad import uqud_case
from slge.cells import index
from slge.mansubat import GATE, TOOLS, derived
from slge.nida import has_tanwin
from slge.rawabit import cells_of
from slge.tawabi import case_class, compatible

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "MANSUBAT_INDEX.md"
SLICE = ROOT / "tests" / "data" / "masaq-mansubat.json"

DERIVED_TAGS = ("NOUN_ACTIVE_PART", "NOUN_PASSIVE_PART", "ADJ")
JAMID_TAGS = ("GERUND", "NOUN_ABSTRACT", "NOUN_CONCRETE")
POSITION = ("فاعل", "مفعول به", "خبر", "مبتدأ", "اسم مجرور", "نائب فاعل", "مبتدأ مؤخر",
            "خبر حرف ناسخ", "اسم حرف ناسخ", "اسم فعل ناسخ", "خبر فعل ناسخ", "مضاف إليه", "حال",
            "ظرف زمان", "ظرف مكان", "مفعول مطلق", "مفعول لأجله", "تمييز", "اسم معطوف", "نعت")


def measure() -> dict[str, object]:
    data = json.loads(SLICE.read_text(encoding="utf-8"))
    case: Counter[tuple[str, str]] = Counter()
    nakira: Counter[tuple[str, bool]] = Counter()
    sort: Counter[tuple[str, str]] = Counter()
    templ: Counter[tuple[str, bool]] = Counter()
    mabni = 0
    for row in data["cells"]:
        role = row["role"]
        stem = tuple((c[0], c[1]) for c in row["stem"])
        if row["declinable"] != "معرب":
            mabni += 1
            continue
        cc = case_class(stem)
        case[(role, "موافق" if compatible(cc, "نصب") else cc)] += 1
        if role in ("حال", "تمييز"):
            plural = uqud_case(stem) is not None  # ِينَ: النونُ عوضُ التنوين
            nakira[(role, not row["det"] and (has_tanwin(stem) or row["tanwin"] or plural))] += 1
            kind = "مشتق" if row["tag"].startswith(DERIVED_TAGS) else (
                "جامد" if row["tag"].startswith(JAMID_TAGS) else "غيره")
            sort[(role, kind)] += 1
            base = stem[:-1] if has_tanwin(stem) else stem[:-2] if plural else stem
            templ[(role, derived(base))] += 1
    illa: Counter[tuple[str, str]] = Counter()
    for i in data["illa"]:
        nxt = i["next"][2] if i["next"] else "—"
        cls = "مستثنى" if nxt == "مستثنى" else "بدل" if nxt == "بدل" else (
            "حسب موقعه" if nxt in POSITION else "غير اسم")
        illa[("منفيّ" if i["neg"] else "مثبت", cls)] += 1
    return {"case": case, "nakira": nakira, "sort": sort, "templ": templ, "illa": illa,
            "n": len(data["cells"]), "mabni": mabni, "n_illa": len(data["illa"])}


def _cells(w: str) -> str:
    return "-".join(str(index(c)) for c in cells_of(w))


def render() -> str:
    m = measure()
    case: Counter[tuple[str, str]] = m["case"]  # type: ignore[assignment]
    nakira: Counter[tuple[str, bool]] = m["nakira"]  # type: ignore[assignment]
    sort: Counter[tuple[str, str]] = m["sort"]  # type: ignore[assignment]
    templ: Counter[tuple[str, bool]] = m["templ"]  # type: ignore[assignment]
    illa: Counter[tuple[str, str]] = m["illa"]  # type: ignore[assignment]
    lines = [
        "# فهرسُ بقيّة المنصوبات على درجات الترخيص التدريجيّ",
        "",
        "مولَّدٌ بـ`python tools/gen_mansubat_index.py` من `src/slge/mansubat.py`؛ لا يُحرَّر باليد. "
        "البرهانُ: `formal/Slge/Mansubat.lean`. الشاهدُ بلا علامةٍ بشهادة البوّابة؛ و° مودَعٌ على "
        "طريقتها.",
        "",
        "## د٤ الخانة — الحالُ والتمييزُ عمليّةٌ واحدة", "",
        "النكرةُ المنصوبة = فتحٌ فتنوين (`nakiraMansuba = tanwin ∘ nasb`)، و`tamyiz = hal` حرفيًّا "
        "(`tamyiz_eq_hal`). مبرهَن لكلّ جذع: تُقرأ نصبًا (`nakira_reads_nasb`)، وتحمل التنوين "
        "(`nakira_has_tanwin`)، وتحفظ الترخيص (`nakira_licensed`). الحالُ الممنوعةُ المقصورة "
        "(سُكَارَى) لا تنوينَ فيها وحركتُها مقدَّرةٌ لا تقرؤها الخانة (`sukara_hal`).",
        "",
        "**قانونُ الفرز** (الحالُ مشتقّ/التمييزُ جامد) يقرؤه القالبُ لا المعنى: `derived` = على "
        "قالبٍ من 26 قالبَ وصفٍ في `Wazn.awzan` (فَاعِل، مَفْعُول، مُفْعِل…، فَعْلَاء، فُعَلَاء؛ "
        "`derived_templates_wf`) بعد إسقاط اللاحقة (ـَة، ـَات، ـِين، ـَيْن؛ `stripSuffix`) وفكِّ الإدغام "
        "(صَافَّات؛ `fakk`) — دَينٌ سُدِّد (`derived_witnesses`، `derived_of_bare`): "
        "ضَاحِك ورَاكِض ومُفْسِد مشتقّة، ونَفْس وشَيْب على فَعْل جامدة — `sorting_by_template`. "
        "تمييزُ العدد 11–99 بالقانون نفسِه (`adad_tamyiz_is_nakira`). والمحوَّلُ عن فاعل عمليّاتٌ: "
        "اشْتَعَلَ شَيْبُ الرَّأْسِ ⇄ اشْتَعَلَ الرَّأْسُ شَيْبًا (`tahwil_witness`، بشهادتي البوّابة).",
        "",
        "## د٨ الحدّ — الاستثناء: ثلاثُ حالاتٍ ثلاثُ عمليّات", "",
        "| الحالة | البنية | عمليّةُ المستثنى | المبرهَن |", "|---|---|---|---|",
        "| تامّ مثبت | مستثنى منه + لا نفي | `nakiraMansuba` | `tamm_muthbat_reads_nasb` |",
        "| تامّ منفي | مستثنى منه + نفي | نصبٌ، أو عمليّةُ المستثنى منه (بدل) | `badal_follows`: "
        "التبعيّةُ في الحالة |",
        "| ناقص منفي (مفرَّغ) | لا مستثنى منه + نفي | عمليّةُ الموقع | `mufarragh_eq_role`: إِلَّا بلا "
        "أثرٍ على الخانة |",
        "",
        "- الأدواتُ مرخَّصة (`tools_licensed`): " + ", ".join(
            f"{w}{'' if w in GATE else '°'} `{_cells(w)}`" for w in TOOLS) + ".",
        "- إِلَّا في جدول أدوات الربط بلا عمل، وغَيْرُ جارّةٌ بالإضافة (`illa_ghayr_in_rawabit`).",
        "- غَيْر: ما بعدها مجرور (`ghayr_idafa_jarr`) وحكمُها حكمُ ما بعد إِلَّا (`ghayr_takes_hukm`).",
        "- خَلَا/عَدَا/حَاشَا: جرٌّ أو نصب، وبـ«مَا» نصبٌ (`ma_khala_nasb`).",
        "",
        "## القياس على MASAQ", "",
        f"على {m['n']} حالٍ وتمييزٍ ومستثنًى بشهادات البوّابة ({m['mabni']} مبنيٌّ: كَيْفَ والموصول — "
        "صورٌ مودَعة):", "",
        "| الدور | قراءةُ الخانة | العدد |", "|---|---|---|",
        *[f"| {r} | {cc} | {v} |" for (r, cc), v in sorted(case.items(), key=lambda kv: -kv[1])],
        "",
        "تمييزٌ يُقرأ جرًّا: تمييزُ كَمْ الخبريّة وكَأَيِّنْ (مِنْ قَرْيَةٍ) — مجرورٌ لفظًا بالإضافة أو بمِنْ: "
        "تيار. وما لا تقرؤه الخانة: المقصورُ (أُسَارَى، أَعْمَى) والمضافُ إلى ياء المتكلّم.", "",
        "| الدور | نكرةٌ (تنوينٌ أو نونُ الجمع، بلا أداة) | العدد |", "|---|---|---|",
        *[f"| {r} | {'نعم' if b else 'لا'} | {v} |" for (r, b), v in sorted(nakira.items())],
        "",
        "### قانونُ الفرز", "",
        "| الدور | وسمُ MASAQ | العدد |", "|---|---|---|",
        *[f"| {r} | {k} | {v} |" for (r, k), v in sorted(sort.items())],
        "",
        "| الدور | على قالبِ وصفٍ (`derived`) | العدد |", "|---|---|---|",
        *[f"| {r} | {'نعم' if b else 'لا'} | {v} |" for (r, b), v in sorted(templ.items())],
        "",
        f"### إِلَّا ({m['n_illa']} موضعًا): النفيُ قبلها وما بعدها", "",
        "| الجملة | ما بعد إِلَّا | العدد |", "|---|---|---|",
        *[f"| {n} | {k} | {v} |" for (n, k), v in sorted(illa.items(), key=lambda kv: -kv[1])],
        "",
        "المثبتُ أكثرُه مستثنًى منصوب، والمنفيُّ أكثرُه بدلٌ أو حسب الموقع (المفرَّغ) — كما في الحصر؛ "
        "و«حسب موقعه» في المثبت استثناءٌ منقطعٌ أو حصرٌ بعد استفهامٍ لم يُعدَّ نفيًا: تيار.",
        "",
        "والقالبُ يقرأ المشتقَّ في الحال دون التمييز (المهموزُ العين خَائِف/قَائِم يُقرأ على فَاعِل: "
        "الهمزةُ حاملٌ كسائر الحوامل)؛ وما وسمه MASAQ مشتقًّا ولم يقرأه القالبُ بعد الإسقاط والفكّ: "
        "فَعِل (فَرِح، فَكِه) وفَعِلَّة (أَذِلَّة) قالبان خارج `awzan`، والرباعيُّ (مُذَبْذَب، مُطْمَئِنّ)، "
        "والناقصُ (مَرْضِيَّة) — بقيّةٌ مسمّاة.",
        "",
        "## ما لا تقرؤه الخانة — باسمه", "",
        "- النفيُ والتمامُ (هل المستثنى منه مذكور): تيار.",
        "- الحالُ الجملةُ وشبهُ الجملة ورابطُها (الضمير، واو الحال): تيار.",
        "- المعنى (الهيئةُ، رفعُ الإبهام، الإخراج)، والمحوَّلُ عن فاعلٍ أو مفعولٍ أو مبتدأ: معلَن.",
        "- شريحةُ MASAQ: 516 صورةً رُفضت بالاسم (REJECT) لأنّ طبعتَها تكتب التنوينَ بعد الألف "
        "(ـَاً)؛ لا تخمينَ ولا تطبيع.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    text = render()
    if "--check" in sys.argv:
        if TARGET.read_text(encoding="utf-8") != text:
            sys.stderr.write("MANSUBAT_INDEX.md غيرُ مطابق؛ شغّل tools/gen_mansubat_index.py\n")
            return 1
        sys.stdout.write("MANSUBAT_INDEX.md مطابق\n")
        return 0
    TARGET.write_text(text, encoding="utf-8")
    sys.stdout.write("كُتب MANSUBAT_INDEX.md\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
