"""فهرسُ النعت والمطابقة الرباعيّة على درجات الترخيص التدريجيّ (NAAT_INDEX.md) من `slge.naat` وMASAQ.

القياسُ على `masaq-tawabi.json` بشهادات البوّابة: أزواجُ (التابع، المتبوع) الموسومةُ «نعت»؛ خاناتُ كلٍّ
من الجذع مع أل (det) والتنوين كما وسمتهما MASAQ. يُقاس: (١) قارئُ المطابقة الرباعيّة `naat_ok` على
أزواج النعت (كم زوجًا يقرؤه نعتًا)؛ (٢) الإعرابُ والتعريفُ من الخانة يوافقان وسمَ MASAQ (case، det)؛
(٣) الطفرة: أزواجُ العطف والبدل والتوكيد لا تُقرأ نعتًا بالضرورة (إحصاء).
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from slge.marifa import al, has_al
from slge.naat import naat_ok, vec
from slge.nawasikh import tanwin
from slge.nida import has_tanwin

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "NAAT_INDEX.md"
DATA = ROOT / "tests" / "data"
Word = tuple[tuple[str, str], ...]
CASE: dict[str, str] = {"مرفوع": "رفع", "منصوب": "نصب", "مجرور": "جرّ"}


def _cells(side: dict[str, Any]) -> Word:
    stem: Word = tuple((a, b) for a, b in side["stem"])
    if side.get("det"):
        stem = al(stem)
    if side.get("tanwin") and not has_tanwin(stem):  # بعضُ جذوع MASAQ تحمل نونَ التنوين
        stem = tanwin(stem)
    return stem


def pairs() -> list[tuple[str, Word, Word, str, str, bool, bool]]:
    """(الدور، التابع، المتبوع، حالتاهما، تعريفاهما) عند MASAQ؛ الحالةُ الفارغة «—»."""

    rows = json.loads((DATA / "masaq-tawabi.json").read_text(encoding="utf-8"))
    out: list[tuple[str, Word, Word, str, str, bool, bool]] = []
    for r in rows:
        t, m = r["tabi"], r["matbu"]
        ct = str(t["case"]).split()[0] if str(t["case"]).strip() else "—"
        cm = str(m["case"]).split()[0] if str(m["case"]).strip() else "—"
        out.append((str(t["role"]), _cells(t), _cells(m), ct, cm, bool(t.get("det")),
                    bool(m.get("det"))))
    return out


def measure() -> dict[str, object]:
    ps = pairs()
    read: Counter[tuple[str, bool]] = Counter()
    case_ok: Counter[str] = Counter()
    def_ok: Counter[str] = Counter()
    coords: Counter[str] = Counter()
    for role, t, m, ct, cm, dt, dm in ps:
        ok = naat_ok(m, t)
        read[(role, ok)] += 1
        if role != "نعت":
            continue
        vt, vm = vec(t), vec(m)
        for v, c, d in ((vt, ct, dt), (vm, cm, dm)):
            c_read = v[0].replace("نصب/جرّ", "نصب" if c == "منصوب" else "جرّ")
            agree = "وافق" if CASE.get(c) == c_read else "خالف"
            verdict = "لم يُقرأ" if v[0] == "لا تقرؤه الخانة" else agree
            case_ok[verdict] += 1
            def_ok["وافق" if has_al(t if v is vt else m) == d else "خالف"] += 1
        if not ok:
            if not (vt[0] != "لا تقرؤه الخانة" and vm[0] != "لا تقرؤه الخانة"):
                coords["الإعرابُ لا يُقرأ"] += 1
            elif vt[1] != vm[1]:
                coords["التعريف"] += 1
            elif vt[2] != vm[2]:
                coords["الجنس"] += 1
            elif vt[3] != vm[3]:
                coords["العدد"] += 1
            else:
                coords["الإعراب"] += 1
    return {"n": len(ps), "read": read, "case": case_ok, "def": def_ok, "coords": coords}


def render() -> str:
    m = measure()
    read: Counter[tuple[str, bool]] = m["read"]  # type: ignore[assignment]
    case_ok: Counter[str] = m["case"]  # type: ignore[assignment]
    def_ok: Counter[str] = m["def"]  # type: ignore[assignment]
    coords: Counter[str] = m["coords"]  # type: ignore[assignment]
    naat_n = read[("نعت", True)] + read[("نعت", False)]
    lines = [
        "# فهرسُ النعت والمطابقة الرباعيّة على درجات الترخيص التدريجيّ",
        "",
        "مولَّدٌ بـ`python tools/gen_naat_index.py` من `src/slge/naat.py`؛ لا يُحرَّر باليد. "
        "البرهانُ: "
        "`formal/Slge/Naat.lean`.",
        "",
        "## د٤ الخانة — المتّجهُ الرباعيّ مقروء", "",
        "الإعرابُ (`Tawabi.caseClass`)، والتعريفُ (نفيُ `Jumla.nakira`: تنوينٌ بلا أل)، والجنسُ "
        "والعددُ تحت "
        "التنوين (`Jumla.gender`، `Jumla.number`) — أربعةٌ تُقرأ من الخانات لا تُكتب باليد "
        "(`vec`).",
        "",
        "## د٨ الحدّ — النعتُ مطابقةٌ في الأربعة", "",
        "النعتُ الحقيقيّ تبعٌ في الإعراب وتعريفٌ واحد وجنسٌ وعددٌ موافقان (`naatOk`): انعكاسيٌّ "
        "على المقروء "
        "وتناظريّ (`naatOk_refl`، `naatOk_symm`)، ومنه الإعرابُ والتعريفُ والموافقة "
        "(`naatOk_case`، "
        "`naatOk_definite`، `naatOk_agree`). **المخالفُ إعرابًا ممنوع** لكلّ جذعين: مرفوعٌ لا "
        "يُنعَت بمنصوب "
        "ولا منصوبٌ بمجرور (`non_matching_case_blocked`)، **والمخالفُ تعريفًا ممنوع** "
        "(`non_matching_definite_blocked`). وعامًّا: المنوَّنُ المرفوعُ بلا أل على مثله مطابقٌ في "
        "الإعراب "
        "والتعريف لكلّ جذعين (`nakira_pair_two_coordinates`؛ `hasAl_setLast_tanwin`)؛ والجنسُ "
        "والعددُ "
        "بعمليّاتهما في `Jumla.agree_ops`.",
        "",
        "## الحملُ واحدٌ والفرقُ التعريف", "",
        "النعتُ والخبرُ على معرفةٍ مرفوعةٍ يتّفقان إعرابًا وجنسًا وعددًا ويفترقان في التعريف "
        "وحده: الرَّجُلُ "
        "الطَّوِيلُ نعتٌ والرَّجُلُ طَوِيلٌ خبرٌ (`hamlKind`؛ `khabar_not_naat`). والجملةُ بعد "
        "النكرة نعتٌ "
        "وبعد المعرفة حال (`jumlaMahall`): الحالُ تشترط صاحبًا معرفةً لكلّ كلمة "
        "(`hal_requires_marifa`)، "
        "والجملةُ بعد النكرة المنوَّنة المنصوبة نعتٌ لكلّ جذعٍ لا تشابه صورتُه فعلًا "
        "(`naat_after_nakira`). "
        "العمليّةُ `naat m k` تجعل الجذعَ على إعراب المنعوت وتعريفه (`naat_witnesses`: الرَّجُلُ "
        "الطَّوِيلُ، "
        "رَجُلٌ طَوِيلٌ، رَجُلًا طَوِيلًا، الرَّجُلِ الطَّوِيلِ، مَدْرَسَةٌ كَبِيرَةٌ).",
        "",
        "## القياس على MASAQ", "",
        f"على {m['n']:,} زوجَ (تابع، متبوع) من الشريحة المودَعة بشهادات البوّابة، "
        f"منها {naat_n:,} نعتًا:",
        "",
        f"- قارئُ المطابقة الرباعيّة يقرأ زوجَ النعت نعتًا في {read[('نعت', True)]:,} من {naat_n:,}.",
        "- ما لم يُقرأ نعتًا، بأوّل مخالفةٍ: "
        + "، ".join(f"{k} {v:,}" for k, v in coords.most_common()) + ".",
        f"- الإعرابُ من الخانة على طرفَي النعت ({sum(case_ok.values()):,}): وافق وسمَ MASAQ "
        f"{case_ok['وافق']:,}، خالف {case_ok['خالف']:,}، لم يُقرأ {case_ok['لم يُقرأ']:,}.",
        f"- أل من الخانة على طرفَي النعت (وسمُ det): وافق {def_ok['وافق']:,}، "
        f"خالف {def_ok['خالف']:,}.",
        "",
        "| دورُ التابع عند MASAQ | يُقرأ نعتًا | العدد |", "|---|---|---|",
        *[f"| {r} | {'نعم' if ok else 'لا'} | {v:,} |" for (r, ok), v in read.most_common()],
        "",
        "## ما لا تقرؤه الخانة — باسمه", "",
        "- المنعوتُ المضافُ (بلا أل ولا تنوين) معرفةٌ بالإضافة والقارئُ يراه بلا تنوين: التعريفُ "
        "موافقٌ "
        "اتّفاقًا؛ والعلمُ المنوَّن نكرةٌ بالخانة — المعجم.",
        "- الجنسُ والعددُ من اللاحقة والقالب: المؤنّثُ بلا تاء (شَمْس) والجمعُ غيرُ المقيس على "
        "غير قالب — "
        "الخانةُ لا تفصل؛ وجمعُ غير العاقل مع المفرد المؤنّث (`Jumla.agreeLoose`) معلَنٌ هنا لا "
        "مقروء.",
        "- النعتُ السببيّ (رَجُلٌ كَرِيمٌ أَبُوهُ) يُطابق في اثنين لا أربعة: خارج هذا الحصر.",
        "- المعطوفُ والبدلُ يُقرآن نعتًا متى طابقا في الأربعة: الفرقُ بينها معنًى وأداة، لا خانة.",
        "- الحصرُ المُرسَل: متّجهاتُه مكتوبةٌ باليد، وفحصُ إجهاده يفحص ما بناه — لم يُدخَل منه "
        "شيء.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    text = render()
    if "--check" in sys.argv:
        if TARGET.read_text(encoding="utf-8") != text:
            sys.stderr.write("NAAT_INDEX.md غيرُ مطابق؛ شغّل tools/gen_naat_index.py\n")
            return 1
        sys.stdout.write("NAAT_INDEX.md مطابق\n")
        return 0
    TARGET.write_text(text, encoding="utf-8")
    sys.stdout.write("كُتب NAAT_INDEX.md\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
