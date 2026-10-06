"""ولّد `ZAMAN_INDEX.md`: فهرسُ ظروف الزمان على درجات الترخيص التدريجيّ من `slge.zaman`، وقياسُ
التصرُّف (عددُ الحالات في الخانة الأخيرة) على شريحة MASAQ المجمَّدة؛ ‎--check‎ يفشل إن كان قديمًا."""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

from slge.cells import index
from slge.zaman import CONSTANTS, STEMS, forms_of, hukm

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "ZAMAN_INDEX.md"
SLICE = ROOT / "tests" / "data" / "masaq-zaman.json"
MUTASARRIF = {"يوم", "شهر", "سنة", "عام", "قرن", "ليل", "نهار", "صباح", "مساء", "ساعة", "حين",
              "وقت", "غد", "أبد", "لحظة", "زمان", "ضحى", "بكرة", "عشي"}
MABNI = {"إذ", "إذا", "أمس", "آن", "مذ", "منذ", "قط", "عوض", "متى", "أيان"}
VERB_TAGS = ("PV", "IV", "CV")


def states() -> tuple[dict[str, Counter[str]], dict[str, Counter[str]], int]:
    """لكلّ جذع: توزيعُ الحالة الأخيرة (مع وسم التنوين)؛ والأدوارُ عند الفتح."""

    rows = json.loads(SLICE.read_text(encoding="utf-8"))
    by_stem: dict[str, Counter[str]] = defaultdict(Counter)
    roles_at_fath: dict[str, Counter[str]] = defaultdict(Counter)
    used = 0
    for row in rows:
        if row["tag"].startswith(VERB_TAGS) or row["seg"] not in MUTASARRIF | MABNI:
            continue
        stem = tuple((c[0], c[1]) for c in row["stem"])
        if not stem:
            continue
        used += 1
        st = "تنوين " + stem[-2][1] if row["tanwin"] and len(stem) >= 2 else stem[-1][1]
        by_stem[row["seg"]][st] += 1
        if st == "فتح":
            roles_at_fath[row["seg"]][row["role"]] += 1
    return by_stem, roles_at_fath, used


def render() -> str:
    by_stem, roles_at_fath, used = states()
    mut = {s: c for s, c in by_stem.items() if s in MUTASARRIF}
    mab = {s: c for s, c in by_stem.items() if s in MABNI}
    mut_multi = sum(1 for c in mut.values() if len(c) >= 2)
    mab_single = sum(1 for c in mab.values() if len(c) == 1)
    fath_total = sum(sum(r.values()) for r in roles_at_fath.values())
    fath_zarf = sum(r.get("ظرف زمان", 0) + r.get("ظرف مكان", 0) for r in roles_at_fath.values())
    lines = [
        "# فهرسُ ظروف الزمان على درجات الترخيص التدريجيّ",
        "",
        "مولَّدٌ بـ`python tools/gen_zaman_index.py` من `src/slge/zaman.py`؛ لا يُحرَّر باليد. "
        "البرهانُ: `formal/Slge/Zaman.lean`.",
        "",
        "التصرُّفُ **عددُ الحالات** في الخانة الأخيرة: المتصرّفُ خمسُ صورٍ (مضاف، مجرور، مقطوع، "
        "مرفوعٌ منوَّن، "
        "منصوبٌ منوَّن)، والمبنيُّ صورةٌ واحدة. والخانةُ تفرّق الضمَّ المنوَّن من الضمّ العاري "
        "(`tanwin_vs_qat`، `hukm_rafTanwin`)؛ ولا تفرّق الظرفَ من المفعول به: كلاهما فتح.",
        "",
        "## د١٦ الإعراب من الخانة — المتصرّفة (40 صورة = 8 × 5)", "",
        "| الجذع | مضاف | مجرور | مقطوع | مرفوع منوَّن | منصوب منوَّن |", "|---|---|---|---|---|---|",
    ]
    for name, stem in STEMS.items():
        keys = ["-".join(str(index(c)) for c in f) for f in forms_of(stem)]
        lines.append(f"| {name} | " + " | ".join(f"`{k}`" for k in keys) + " |")
    lines += [
        "", "## د٤ الخانة — المبنيّة الثمانية (صورةٌ واحدة بحالةٍ ثابتة)", "",
        "| الظرف | الخانات | الحالةُ الأخيرة (معلن ومطابَق) | ما تقرؤه الخانة |", "|---|---|---|---|",
        *[f"| {n} | `{'-'.join(str(index(c)) for c in w)}` | {st} | {hukm(w)} |"
          for n, (w, st) in CONSTANTS.items()],
        "",
        "أَمْسِ بأل العهديّة معربٌ: الْأَمْسُ = ال ++ (أَمْس بالضمّ) (`al_amsu`).", "",
        "## القياس على MASAQ — التصرُّفُ عددُ الحالات", "",
        f"على {used} موضعًا بشهادات البوّابة (الجذعُ قبل الضمير وبعد السابقة، بلا الأفعال):", "",
        f"- المتصرّفةُ الواردة: **{mut_multi}/{len(mut)}** جذعًا بحالتين فأكثر.",
        f"- المبنيّةُ الواردة: **{mab_single}/{len(mab)}** بحالةٍ واحدة؛ والاثنان: إِذِ (كسرةُ التقاء "
        "الساكنين في الوصل — بقيّةُ حدٍّ لا حالة) وآنٍ (تصادفُ رسمٍ مع اسم الفاعل، لا الْآنَ).",
        f"- عند الفتح: **{fath_zarf}/{fath_total}** ظرفٌ، والباقي مفعولٌ به وبدلٌ ومعطوف — "
        "فالظرفيّةُ لا تُقرأ من الخانة.", "",
        "| الجذع | توزيعُ الحالة الأخيرة |", "|---|---|",
        *[f"| {s} | {'، '.join(f'{k}: {v}' for k, v in c.most_common())} |"
          for s, c in sorted(by_stem.items(), key=lambda kv: -sum(kv[1].values()))],
        "",
        "## خارج الخانة — باسمه", "",
        "- الظرفيّةُ (معنى «في») مقابل المفعول به: من النظم.",
        "- زمانٌ أم مكان في قَبْل/بَعْد/بَيْن/عِنْد: من المضاف إليه.",
        "- أَبَدًا وحِينًا وغَدًا: نكراتٌ منوَّنة منصوبة — صورةٌ من صور المتصرّف لا بابٌ مستقلّ.", "",
    ]
    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    text = render()
    if "--check" in argv:
        if not TARGET.exists() or TARGET.read_text(encoding="utf-8") != text:
            print("ZAMAN_INDEX.md قديم: شغّل python tools/gen_zaman_index.py", file=sys.stderr)
            return 1
        print("ZAMAN_INDEX.md مطابق")
        return 0
    TARGET.write_text(text, encoding="utf-8")
    print(f"كُتب {TARGET.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
