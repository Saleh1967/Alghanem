"""ولّد `NIDA_INDEX.md`: فهرسُ النداء على درجات الترخيص التدريجيّ من `slge.nida`، وقياسُ قانون المنادى
على شريحة MASAQ المجمَّدة (شهاداتُ البوّابة بأحكام MASAQ)؛ ‎--check‎ يفشل إن كان قديمًا."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

from slge.cells import index
from slge.nida import PARTICLES, hukm

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "NIDA_INDEX.md"
SLICE = ROOT / "tests" / "data" / "masaq-munada.json"


def measure() -> tuple[Counter[tuple[str, str, str]], int]:
    """(الحكمُ المقروء، حكمُ MASAQ، مضاف؟) → العدد؛ على جذع المنادى قبل الضمير المتّصل."""

    rows = json.loads(SLICE.read_text(encoding="utf-8"))
    out: Counter[tuple[str, str, str]] = Counter()
    for row in rows:
        cells = tuple((c[0], c[1]) for c in row["cells"])
        k = row["suffix_len"]
        stem = cells[:-k] if k else cells
        if row["tanwin"]:
            stem = (*stem[:-1], (stem[-1][0], stem[-1][1])) if stem else stem
        read = hukm(stem) if not row["tanwin"] else "نكرة غير مقصودة (منصوب)"
        masaq = "مبني" if row["masaq"][1] == "مبني" else "معرب"
        out[(read, masaq, row["masaq"][2])] += 1
    return out, len(rows)


def render() -> str:
    table, total = measure()
    damm = sum(v for (r, m, _), v in table.items() if r == "مبني على الضم")
    damm_ok = sum(v for (r, m, _), v in table.items() if r == "مبني على الضم" and m == "مبني")
    mansub = sum(v for (r, m, _), v in table.items() if r in ("معرب منصوب", "مضاف إلى ياء محذوفة"))
    mansub_ok = sum(v for (r, m, _), v in table.items()
                    if r in ("معرب منصوب", "مضاف إلى ياء محذوفة") and m == "معرب")
    unread = sum(v for (r, _, _), v in table.items() if r == "لا تقرؤه الخانة")
    lines = [
        "# فهرسُ النداء على درجات الترخيص التدريجيّ",
        "",
        "مولَّدٌ بـ`python tools/gen_nida_index.py` من `src/slge/nida.py`؛ لا يُحرَّر باليد. "
        "البرهانُ: `formal/Slge/Nida.lean`.",
        "",
        "لا «أسماءَ نداء»: الأدواتُ حروفٌ، والمنادى اسمٌ يُقرأ حكمُه من خانته الأخيرة. "
        "المسافةُ (قريب/بعيد) من الحصر المُرسَل **معلن**.",
        "",
        "## د٨ الحدّ — الأدواتُ الستّ (حروفٌ لا محلَّ لها)", "",
        "خاناتُها مرخَّصةٌ متباينة (`particles_licensed`)؛ الهمزةُ حرفٌ متّصل لا يُفسد ما بعده، "
        "ويَا تنتهي بألفٍ ساكنة فوصلُها بكلّ مرخَّصٍ مرخَّص (`ya_junction`).", "",
        "| الأداة | الخانات | المسافة (معلن) | الشاهد |", "|---|---|---|---|",
    ]
    for p in PARTICLES:
        key = "-".join(str(index(c)) for c in p.cells)
        lines.append(f"| {p.name} | `{key}` | {p.masafa} | "
                     f"{'شهادة' if p.witnessed else 'بالقانون'} |")
    lines += [
        "",
        "## د١٦ الإعراب من الخانة — قانونُ المنادى (مبرهَن، ومقيس)", "",
        "| الخانةُ الأخيرة للجذع | الحكم | المبرهَن |", "|---|---|---|",
        "| ضمٌّ بلا تنوين | مبنيٌّ على الضمّ في محلّ نصب (علم / نكرة مقصودة) | `damm_is_bina` |",
        "| فتحٌ بلا تنوين | معربٌ منصوب (مضاف / شبيه بالمضاف) | `hukm` |",
        "| فتحٌ بتنوين | نكرةٌ غيرُ مقصودة، منصوبة — والتنوينُ لا يجامع البناء | `tanwin_never_bina` |",
        "| كسرٌ | مضافٌ إلى ياء المتكلّم المحذوفة (يَا قَوْمِ) | `hukm` |",
        "| واوٌ/ألفٌ فنون | مبنيٌّ على الواو/الألف | `hukm` |",
        "| ألفٌ أو ياءٌ ساكنة (مُوسَى، بَنِي) | لا تقرؤه الخانة | — |",
        "",
        f"**القياس على MASAQ** ({total} منادًى بشهادات البوّابة، الجذعُ قبل الضمير المتّصل): "
        f"الضمُّ ⇒ مبنيّ **{damm_ok}/{damm}**؛ الفتحُ والكسرُ ⇒ معربٌ منصوب **{mansub_ok}/{mansub}** "
        f"(والباقي خلافُ وسمٍ في MASAQ: أَهْلَ الكتاب، مَعْشَرَ، بَنِي موسومةً «مبني»)؛ "
        f"لا تقرؤه الخانة: **{unread}**.", "",
        "| المقروء | وسم MASAQ | مضاف؟ | العدد |", "|---|---|---|---|",
        *[f"| {r} | {m} | {p} | {v} |" for (r, m, p), v in table.most_common()],
        "",
        "## خارج الثنائيّ — باسمه", "",
        "- **الندبة** (وَا حَسْرَتَاهْ): ألفٌ فهاءُ سكتٍ ساكنتان — غيرُ مرخَّصةٍ ثنائيًّا لكلّ جذع "
        "(`nudba_not_binary_licensed`)؛ صورةُ وقفٍ يرخّصها الثلاثيُّ في الغانم (`A116.Ternary`).",
        "- اللَّهُمَّ: نداءٌ بالميم المشدّدة عوضًا عن يا — صورةٌ واحدة، لا قانونَ عامّ منها.",
        "- النكرةُ المقصودة والعلم: خانةٌ واحدة (ضمّ)؛ الفصلُ من المعجم لا من الخانة.", "",
    ]
    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    text = render()
    if "--check" in argv:
        if not TARGET.exists() or TARGET.read_text(encoding="utf-8") != text:
            print("NIDA_INDEX.md قديم: شغّل python tools/gen_nida_index.py", file=sys.stderr)
            return 1
        print("NIDA_INDEX.md مطابق")
        return 0
    TARGET.write_text(text, encoding="utf-8")
    print(f"كُتب {TARGET.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
