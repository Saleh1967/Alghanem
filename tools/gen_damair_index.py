"""ولّد `DAMAIR_INDEX.md`: فهرسُ الضمائر على درجات الترخيص التدريجيّ من `slge.damair`؛ ‎--check‎."""

from __future__ import annotations

import sys
from pathlib import Path

from slge.cells import index
from slge.damair import ATTACHED_NASB, ATTACHED_RAF, DETACHED_NASB, DETACHED_RAF, tier

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "DAMAIR_INDEX.md"
TIERS = ("د١٦ الإعراب من الخانة", "د٨ الحدّ (إلحاق)", "د٤ الخانة")
WHAT = {
    "د١٦ الإعراب من الخانة": "الدورُ يُقرأ من الخانة التي قبل الضمير: نا (سكونُ صحيحٍ ⇒ رفع، حركةٌ أو "
                          "مدٌّ ⇒ نصب/جرّ؛ `na_raf_reads_sukun`، `na_nasb_reads_vowel`، "
                          "`na_after_madd_not_raf`)، والتاءُ (الشخصُ في حالتها؛ `ta_person`).",
    "د٨ الحدّ (إلحاق)": "يُلحَق بالحامل ويحفظ الترخيصَ (`attach_licensed`)؛ ودورُه من الحامل "
                        "لا من الخانة.",
    "د٤ الخانة": "خاناتُه مرخَّصةٌ متباينة (`damair_licensed`، `damair_nodup`)؛ ونصبُه المنفصل = "
                "إِيَّا + المتّصل (`iyya_is_carrier_plus_suffix`).",
}


def render() -> str:
    allp = DETACHED_RAF + DETACHED_NASB + ATTACHED_RAF + ATTACHED_NASB
    lines = [
        "# فهرسُ الضمائر على درجات الترخيص التدريجيّ",
        "",
        "مولَّدٌ بـ`python tools/gen_damair_index.py` من `src/slge/damair.py`؛ لا يُحرَّر باليد. "
        "البرهانُ: `formal/Slge/Damair.lean`.",
        "",
        f"**{len(DETACHED_RAF) + len(DETACHED_NASB)} منفصلًا "
        f"و{len(ATTACHED_RAF) + len(ATTACHED_NASB)} صورةً متّصلة** (التسعةُ بأشخاصها). "
        "الدورُ الإعرابيُّ الثابت من الحصر المُرسَل **معلن**؛ "
        "ما تقرؤه الخانةُ مبرهَن. المستترُ ليس خانةً: خارج الفهرس باسمه.",
        "",
    ]
    for t in TIERS:
        ps = [p for p in allp if tier(p) == t]
        lines += [f"## {t} — {len(ps)}", "", WHAT[t], "",
                  "| الضمير | المجموعة | الخانات | الدور (معلن) | ما يقرؤه الحرف |",
                  "|---|---|---|---|---|"]
        for p in ps:
            key = "-".join(str(index(c)) for c in p.cells)
            lines.append(f"| {p.name} | {p.group} | `{key}` | {p.role} | {p.law or '—'} |")
        lines.append("")
    lines += ["## ما لا يفصله الحرف — باسمه", "",
              "- الياءُ الساكنة بعد كسر: مخاطبةٌ (رفع) أو متكلّمٌ (نصب/جرّ) — من الحامل "
              "(`ya_ambiguous`).",
              "- نصبٌ أم جرٌّ بعد المتحرّك: من الحامل (فعل/حرف مشبّه ⇒ نصب؛ اسم/حرف جرّ ⇒ جرّ).",
              "- الضميرُ المستتر: لا خانةَ له، فلا يدخل البوّابة؛ يُستدلّ عليه في النظم لا هنا.", ""]
    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    text = render()
    if "--check" in argv:
        if not TARGET.exists() or TARGET.read_text(encoding="utf-8") != text:
            print("DAMAIR_INDEX.md قديم: شغّل python tools/gen_damair_index.py", file=sys.stderr)
            return 1
        print("DAMAIR_INDEX.md مطابق")
        return 0
    TARGET.write_text(text, encoding="utf-8")
    print(f"كُتب {TARGET.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
