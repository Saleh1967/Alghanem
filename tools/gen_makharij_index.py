"""فهرسُ المخارج (MAKHARIJ_INDEX.md): مخارجُ سيبويه وصفاتُه كما نُقلت، مقابلةً بالصفات المعلَنة
(`phonology`)، ثمّ توزيعُ ذرّات المصحف على المخارج والصفات.

(١) الأصولُ بترتيب سيبويه، والمخارجُ الخمسةَ عشر المعدودة (المنطوقُ ستّةَ عشر؛ الساقطُ اللام)، والصفاتُ
قسماتٍ تامّة. (٢) المقابلةُ بالمعلَن: الجهرُ/الهمس حرفًا حرفًا (الفرقُ: الصاد)، وموضعُ الحلق/الشفتين.
(٣) على `corpus-certificates.json.gz`: 99,130 ذرّةً — كم منها في كلّ مخرجٍ وكم مجهورٌ ومهموس وشديدٌ ورخوٌ
ومطبَق؛ الرقمُ يُنشر كما هو. (٤) الفروعُ الأربعةَ عشر أسماءً كما وردت (لا خاناتٍ لها).
"""

from __future__ import annotations

import gzip
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from slge.makharij import BAYN, FURU_BAD, FURU_GOOD, MAKHARIJ, MISSING, ORDER, SIFAT, STATED_COUNT
from slge.phonology import MAHRAJ, PAIRS

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "MAKHARIJ_INDEX.md"
DATA = ROOT / "tests" / "data"


def corpus_atoms() -> tuple[Counter[str], int]:
    """ذرّاتُ المصحف بحواملها، وعددُ النون الساكنة وحدَها (خانةُ الخفيفة/التنوين)."""

    with gzip.open(DATA / "corpus-certificates.json.gz", "rt", encoding="utf-8") as f:
        d: dict[str, Any] = json.load(f)
    cells = [tuple(c) for x in d["forms"] for c in x["cells"]]
    return Counter(a for a, _ in cells), sum(1 for c in cells if c == ("ن", "سكون"))


def measure() -> dict[str, Any]:
    atoms, nun_sukun = corpus_atoms()
    total = sum(atoms.values())
    by_makhraj = [nun_sukun if light else sum(atoms[c] for c in cs) for _, cs, light in MAKHARIJ]
    declared_hams = set(next(pos for name, _, pos, _ in PAIRS if name == "همس"))
    sib_hams = set(SIFAT["mahmusa"][1])
    jahr_agree = sum(1 for c in ORDER if (c in declared_hams) == (c in sib_hams))
    throat_sib = {c for m in MAKHARIJ[:3] for c in m[1]}
    throat_decl = {c for c, (place, _) in MAHRAJ.items() if place == "الحلق"}
    lips_sib = set(MAKHARIJ[12][1]) | set(MAKHARIJ[13][1])
    lips_decl = {c for c, (place, _) in MAHRAJ.items() if place == "الشفتان"}
    counts = {key: sum(atoms[c] for c in cs) for key, (_, cs) in SIFAT.items()}
    counts["bayn"] = sum(atoms[c] for c in BAYN)
    return {"order": "".join(ORDER), "makharij": len(MAKHARIJ), "stated": STATED_COUNT,
            "missing": "".join(MISSING), "atoms": total, "by_makhraj": by_makhraj,
            "sifat_atoms": counts, "jahr_agree": jahr_agree,
            "hams_diff": "".join(sorted(sib_hams - declared_hams)),
            "throat_sib": "".join(sorted(throat_sib)), "throat_decl": "".join(sorted(throat_decl)),
            "lips_agree": lips_sib == lips_decl, "furu": len(FURU_GOOD) + len(FURU_BAD),
            "lam_atoms": atoms["ل"]}


def render() -> str:
    m = measure()
    pct = lambda n: f"{100 * n / m['atoms']:.1f}%"  # noqa: E731
    lines = [
        "# فهرسُ المخارج — مخارجُ سيبويه وصفاتُه خاناتٍ، والمعلَنُ مقابَلًا بالمختوم",
        "",
        "مولَّدٌ بـ`python tools/gen_makharij_index.py` من `src/slge/makharij.py`؛ لا يُحرَّر باليد. "
        "البرهانُ "
        "`formal/Slge/Makharij.lean`؛ الجدولُ `formal/Slge/MakharijTable.lean` مولَّدٌ من المختوم "
        "`tests/data/openiti-sibawayh-kitab.txt.gz` (`tools/deposit_makharij.py --check`): "
        "«باب عدد الحروف العربية ومخارجها ومهموسها ومجهورها».",
        "",
        "## الأصولُ والمخارج كما نُقلت", "",
        f"الأصولُ التسعةُ والعشرون بترتيب سيبويه: `{m['order']}` — تبديلٌ للحوامل التسعة "
        "والعشرين "
        "(`order_is_the_alphabet`)، فالصفةُ تقع على الحامل نفسه الذي تقع عليه الحالةُ في الخانة.",
        "",
        f"المخارجُ: المنطوقُ في النصّ **{m['stated']}** والمعدودُ في النشرة **{m['makharij']}**؛ "
        "الساقطُ "
        f"مخرجُ **{m['missing']}** وحدَه (في نشرتي jk وShamela معًا) — نقصٌ مسمًّى لا يُرمَّم من الذاكرة "
        "(`lacuna_is_lam`). النونُ وحدَها في مخرجين: طرفُ اللسان والخياشيمُ للخفيفة (`nun_twice`).",
        "",
        "| # | الحروف | الموضع كما ورد | ذرّاتُ المصحف |", "|---|---|---|---|",
    ]
    for i, ((desc, cs, light), n) in enumerate(zip(MAKHARIJ, m["by_makhraj"], strict=True)):
        tag = " (الخفيفة: خانةُ النون الساكنة)" if light else ""
        lines.append(f"| {i + 1} | {''.join(cs)}{tag} | {desc} | {n:,} ({pct(n)}) |")
    sa = m["sifat_atoms"]
    lines += [
        "",
        "## الصفاتُ قسماتٍ تامّة (مبرهَنة)", "",
        "| الصفة | الحروف | العدد | ذرّاتُ المصحف |", "|---|---|---|---|",
        *(f"| {SIFAT[k][0]} | {''.join(SIFAT[k][1])} | {len(SIFAT[k][1])} | {sa[k]:,} "
          f"({pct(sa[k])}) |" for k in ("majhura", "mahmusa", "shadida", "rikhwa")),
        f"| بينَ بين (العين، المنحرف، الغنّة، المكرّر، اللينتان، الهاوي) | {''.join(BAYN)} | 8 | "
        f"{sa['bayn']:,} ({pct(sa['bayn'])}) |",
        f"| المطبقة | {''.join(SIFAT['mutbaqa'][1])} | 4 | {sa['mutbaqa']:,} "
        f"({pct(sa['mutbaqa'])}) |",
        f"| المنفتحة | {''.join(SIFAT['munfatiha'][1])} | 25 | {sa['munfatiha']:,} "
        f"({pct(sa['munfatiha'])}) |",
        "",
        "الجهرُ والهمس 19 + 10، والشدّةُ والرخاوةُ وما بينهما 8 + 13 + 8، والإطباقُ والانفتاح 4 + 25 — "
        "كلٌّ قسمةٌ تامّة للتسعة والعشرين بلا تداخل (`jahr_partition`، `shidda_partition`، "
        "`itbaq_partition`). الأعدادُ 19 و10 كما نطقها النصّ.",
        "",
        "## المعلَنُ (`phonology`) مقابَلًا بالمختوم", "",
        f"- الجهرُ/الهمس: يوافق المعلَنُ سيبويه في {m['jahr_agree']} حرفًا من 29؛ الفرقُ "
        f"**{m['hams_diff']}** "
        "— مهموسةٌ عند سيبويه (العاشرة) وليست في «فحثهشخسكت» المعلَنة. لا يُصحَّح المعلَنُ من الذاكرة؛ "
        "الصحيحُ الآن هو المختوم، والمعلَنُ يبقى باسمه حتى يُستبدل به (دينٌ في ADR ١٩).",
        f"- الحلق: سيبويه `{m['throat_sib']}` والمعلَنُ `{m['throat_decl']}` — الألفُ عند سيبويه من "
        "أقصى الحلق مع الهمزة والهاء، وعند المعلَن في «الجوف» (اصطلاحُ المتأخّرين).",
        f"- الشفتان: {'موافق' if m['lips_agree'] else 'مخالف'} (ف، ب، م، و).",
        "",
        "## على مودَع المصحف", "",
        f"{m['atoms']:,} ذرّةً في 18,179 صورة: توزيعُها على المخارج والصفات في الجدولين أعلاه؛ "
        f"اللامُ — التي لا مخرجَ لها في النشرة — {m['lam_atoms']:,} ذرّةً ({pct(m['lam_atoms'])}) "
        "خارجَ جدول المخارج وداخلَ جداول الصفات كلِّها.",
        "",
        "## الفروع", "",
        f"{m['furu']} فرعًا أسماءً كما وردت — لا خاناتٍ لها: المستحسنةُ الستّ: {'، '.join(FURU_GOOD)}؛ "
        f"وغيرُ المستحسنة الثماني: {'، '.join(FURU_BAD)}. النونُ الخفيفة منها خانتُها خانةُ النون "
        "الساكنة "
        "(`Zawaid.khafifa_is_tanwin`)، والباقي أداءٌ أو طبعةٌ لا خانة.",
        "",
        "## ما ليس هنا — باسمه", "",
        "- مخرجُ اللام ساقطٌ من التعداد في النشرتين؛ يُستكمل من نشرةٍ ثالثة مختومة إن أُذن، لا من "
        "الذاكرة.",
        "- الصفاتُ هنا وصفٌ على الحامل لا عمليّة؛ ما يُبنى عليها (الإدغامُ وأحكامُه في بقيّة الباب) لم "
        "يُقرأ.",
        "- الفروعُ لا تدخل الـ116 لأنّها ليست حواملَ؛ الهمزةُ بين بين والإمالةُ أداءٌ لا رسم.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    text = render()
    if "--check" in sys.argv:
        if TARGET.read_text(encoding="utf-8") != text:
            sys.stderr.write("MAKHARIJ_INDEX.md غيرُ مطابق؛ شغّل tools/gen_makharij_index.py\n")
            return 1
        sys.stdout.write("MAKHARIJ_INDEX.md مطابق\n")
        return 0
    TARGET.write_text(text, encoding="utf-8")
    sys.stdout.write("كُتب MAKHARIJ_INDEX.md\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
