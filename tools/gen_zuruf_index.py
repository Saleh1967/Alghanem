"""ولّد `ZURUF_INDEX.md`: فهرسُ ظروف المكان على درجات الترخيص التدريجيّ من `slge.zuruf`، وقياسُ
قانون الخانة الأخيرة على شريحة MASAQ المجمَّدة؛ ‎--check‎ يفشل إن كان قديمًا."""

from __future__ import annotations

import json
import sys
from collections import Counter
from collections.abc import Callable
from pathlib import Path

from slge.cells import index
from slge.zuruf import CONSTANTS, STEMS, hukm, jarr, mudaf, qat

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "ZURUF_INDEX.md"
SLICE = ROOT / "tests" / "data" / "masaq-zuruf.json"
JARR_PREFIX = {"ب", "ل", "ك"}


def measure() -> tuple[Counter[tuple[str, str, str]], int]:
    """(الحالةُ الأخيرة للجذع، أبعد جارّ؟، مضاف؟ حسب MASAQ) → العدد."""

    rows = json.loads(SLICE.read_text(encoding="utf-8"))
    out: Counter[tuple[str, str, str]] = Counter()
    for row in rows:
        stem = tuple((c[0], c[1]) for c in row["stem"])
        st = "تنوين" if row["tanwin"] else (stem[-1][1] if stem else "؟")
        after_jarr = row["prefix"] in JARR_PREFIX or row["prev_tag"] == "PREP"
        mudaf_ = "مضاف إلى ضمير" if row["suffix"] else row["mudaf"]
        out[(st, "بعد جارّ" if after_jarr else "—", mudaf_)] += 1
    return out, len(rows)


def render() -> str:
    table, total = measure()

    def n(pred: Callable[[tuple[str, str, str]], bool]) -> int:
        return sum(v for k, v in table.items() if pred(k))

    damm = n(lambda k: k[0] == "ضم")
    damm_cut = n(lambda k: k[0] == "ضم" and k[2] == "غير مضاف")
    fath = n(lambda k: k[0] == "فتح" and k[1] == "—")
    fath_mudaf = n(lambda k: k[0] == "فتح" and k[1] == "—" and k[2] != "غير مضاف")
    kasr = n(lambda k: k[0] == "كسر")
    kasr_ok = n(lambda k: k[0] == "كسر" and (k[1] == "بعد جارّ" or k[2] == "مضاف إلى ضمير"))
    lines = [
        "# فهرسُ ظروف المكان على درجات الترخيص التدريجيّ",
        "",
        "مولَّدٌ بـ`python tools/gen_zuruf_index.py` من `src/slge/zuruf.py`؛ لا يُحرَّر باليد. "
        "البرهانُ: `formal/Slge/Zuruf.lean`.",
        "",
        "الظرفُ المعربُ جذعٌ وخانةُ إعراب: الإضافةُ (فتح) والجرُّ (كسر) والقطعُ (ضمّ) ثلاثُ عمليّاتٍ على "
        "الخانة الأخيرة تحفظ الترخيصَ (`setLast_licensed`) ويقرؤها الحكم (`hukm_mudaf`، "
        "`hukm_jarr`، "
        "`hukm_qat`). البابُ (الجهات، المقادير…) من الحصر المُرسَل **معلن**.",
        "",
        "## د١٦ الإعراب من الخانة — المعربة (51 صورة = 17 جذعًا × 3)", "",
        "| الجذع | الباب (معلن) | مضاف (فتح) | مجرور (كسر) | مقطوع (ضمّ) | شواهد البوّابة |",
        "|---|---|---|---|---|---|",
    ]
    for z in STEMS:
        keys = ["-".join(str(index(c)) for c in op(z.stem)) for op in (mudaf, jarr, qat)]
        lines.append(f"| {z.name} | {z.bab} | `{keys[0]}` | `{keys[1]}` | `{keys[2]}` | "
                     f"{'، '.join(z.witnessed) or 'بالقانون'} |")
    lines += [
        "",
        "## د٤ الخانة — الثوابتُ المبنيّة (صورةٌ واحدة)", "",
        "| الثابت | الخانات | ما تقرؤه الخانة |", "|---|---|---|",
        *[f"| {name} | `{'-'.join(str(index(c)) for c in w)}` | {hukm(w)} |"
          for name, w in CONSTANTS.items()],
        "",
        "حَيْثُ ضمٌّ لازم: مقطوعةٌ أبدًا بالقانون نفسه (`haythu_always_cut`)؛ لَدُنْ ولَدَى وثَمَّ وهُنَا لا "
        "تقرأ لها الخانةُ حالةً.", "",
        "## القياس على MASAQ — مقيسٌ لا مبرهَن", "",
        f"على {total} ظرفًا (مكانٍ وزمان، بشهادات البوّابة، الجذعُ قبل الضمير وبعد السابقة):", "",
        f"- **الضمُّ ⇒ مقطوعٌ عن الإضافة: {damm_cut}/{damm}** — والباقي حَيْثُ (ضمٌّ لازم موسومٌ «مضاف» "
        "إلى جملة) وموضعان من خطأ قطع اللاحقة.",
        f"- **الفتحُ (بلا جارّ) ⇒ مضاف: {fath_mudaf}/{fath}** — والباقي ثَمَّ ودُونَ.",
        f"- **الكسرُ ⇒ بعد جارٍّ أو ياءِ المتكلّم: {kasr_ok}/{kasr}**.", "",
        "| الحالة الأخيرة | الجارّ | مضاف؟ (MASAQ) | العدد |", "|---|---|---|---|",
        *[f"| {a} | {b} | {c} | {v} |" for (a, b, c), v in table.most_common()],
        "",
        "## خارج الخانة — باسمه", "",
        "- المختصُّ (المسجد، البيت): ليس ظرفًا — قيدٌ معجميّ.",
        "- المقاديرُ (مِيل، فَرْسَخ) والمصوغُ من المصدر (مَجْلِسَ): يُعرب كالمعرب نفسِه؛ لا شاهدَ في المدوّنة.",
        "- ظرفُ الزمان: يتبع القانونَ نفسَه في القياس (قَبْلُ، بَعْدُ)؛ حصرُه معلَّقٌ حتى يُرسَل.", "",
    ]
    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    text = render()
    if "--check" in argv:
        if not TARGET.exists() or TARGET.read_text(encoding="utf-8") != text:
            print("ZURUF_INDEX.md قديم: شغّل python tools/gen_zuruf_index.py", file=sys.stderr)
            return 1
        print("ZURUF_INDEX.md مطابق")
        return 0
    TARGET.write_text(text, encoding="utf-8")
    print(f"كُتب {TARGET.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
