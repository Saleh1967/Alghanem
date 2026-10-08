"""فهرسُ أبواب الإعلال (ILAL_BAB_INDEX.md): لكلّ قاعدةٍ من `Slge.Ilal` بابُها في الكتاب المختوم بسطره
وشاهدُه من نصّ الباب، وصورةُ المصحف التي تقرؤها، ثمّ كم صورةً من المودَع تقرؤها القاعدةُ في موضعٍ ما،
والأبوابُ التي لا قاعدةَ لها ديونًا بأسطرها.

(١) الجدولُ كما أُودع: 13 صفًّا بترتيب `Rule.all`؛ ثمانيةٌ لها صورةٌ مقروءة وخمسةٌ رسمٌ بلا خانات.
(٢) على `corpus-certificates.json.gz`: عددُ الصور التي يكون فيها `undo` غيرَ فارغ لكلّ قاعدة (قراءةٌ
مباشرة لا عبر `jidh`؛ فالرقمُ أعلى من عدّ `ILAL_INDEX` الذي يشترط جذرًا). (٣) الديونُ السبعة.
"""

from __future__ import annotations

import gzip
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from slge.ilal import RULES, undo
from slge.ilal_bab import DEBTS, TABLE, reads, unwitnessed, witnessed

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "ILAL_BAB_INDEX.md"
DATA = ROOT / "tests" / "data"
MARKS = {"فتح": "َ", "كسر": "ِ", "ضم": "ُ", "سكون": "ْ"}


def corpus_forms() -> list[tuple[tuple[str, str], ...]]:
    with gzip.open(DATA / "corpus-certificates.json.gz", "rt", encoding="utf-8") as f:
        d: dict[str, Any] = json.load(f)
    return [tuple((a, b) for a, b in x["cells"]) for x in d["forms"]]


def measure() -> dict[str, Any]:
    forms = corpus_forms()
    read: Counter[str] = Counter()
    for w in forms:
        for rule in RULES:
            if any(undo(rule, w, i) for i in range(len(w))):
                read[rule] += 1
    return {"rows": len(TABLE), "witnessed": len(witnessed()), "unwitnessed": list(unwitnessed()),
            "all_read": all(reads(r) for r in witnessed()), "debts": len(DEBTS),
            "forms": len(forms), "read": {rule: read[rule] for rule in RULES},
            "chapters": len({r[2] for r in TABLE})}


def vowelled(cells: tuple[tuple[str, str], ...] | None) -> str:
    return "".join(k + MARKS[s] for k, s in cells) if cells else "—"


def render() -> str:
    m = measure()
    lines = [
        "# فهرسُ أبواب الإعلال — كلُّ قاعدةٍ ببابها في الكتاب وشاهدِها وصورتِها المقروءة",
        "",
        "مولَّدٌ بـ`python tools/gen_ilal_bab_index.py` من `src/slge/ilal_bab.py`؛ لا يُحرَّر باليد. "
        "البرهانُ `formal/Slge/IlalBab.lean`؛ الجدولُ `formal/Slge/IlalBabTable.lean` مولَّدٌ من "
        "المختوم "
        "`tests/data/openiti-sibawayh-kitab.txt.gz` ومن `corpus-certificates.json.gz` "
        "(`tools/deposit_ilal_bab.py --check`).",
        "",
        "## الجدولُ كما أُودع", "",
        f"{m['rows']} صفًّا بترتيب `Rule.all` في {m['chapters']} أبواب — لكلّ قاعدةٍ صفٌّ واحد "
        "(`every_rule_once`). الشاهدُ كلمةٌ واردةٌ في نصّ الباب بعينه (رسمًا؛ النصُّ غيرُ مشكول)؛ "
        "وصورةُ المصحف أوّلُ صورةٍ في المودَع رسمُها رسمُ الشاهد **وتقرؤها القاعدةُ** (`undo` غيرُ فارغ): "
        f"{m['witnessed']} قواعد لها ذلك (`witnesses_read`)، و{len(m['unwitnessed'])} شاهدُها رسمٌ "
        "بلا خانات لم يُشكَّل من الذاكرة (`unwitnessed`).",
        "",
        "| # | القاعدة | الباب (سطرُه) | شاهدُ الباب | صورةُ المصحف | الموضع | تقرؤها | "
        "صورٌ تقرؤها القاعدة |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for i, r in enumerate(TABLE):
        rule, title, line, word, cells, at, _ = r
        lines.append(f"| {i} | `{rule}` | {title} ({line:,}) | {word} | {vowelled(cells)} | "
                     f"{'—' if at is None else at} | {'نعم' if reads(r) else 'لا'} | "
                     f"{m['read'][rule]:,} |")
    lines += [
        "",
        f"العمودُ الأخير على {m['forms']:,} صورةً من المودَع: كم صورةً يكون فيها `undo` غيرَ فارغ في "
        "موضعٍ ما — قراءةٌ مباشرة بلا شرطِ الجذر، فهي أعلى من عدّ `ILAL_INDEX.md` الذي يعدّ ما صعد "
        "إلى جذرٍ مودَع.",
        "",
        "## الخمسُ بلا صورةٍ مقروءة — باسمها", "",
        *(f"- `{r[0]}` ({r[3]})" for r in TABLE if r[4] is None),
        "",
        "السببُ واحدٌ للخمس (مفحوصٌ في `tools/deposit_ilal_bab.py`): لا صورةَ في مودَع المصحف رسمُها "
        "الخشن رسمُ شاهد الباب بسابقةٍ أو بدونها. لا يُشكَّل شاهدٌ من الذاكرة؛ تعود هذه بخاناتٍ حين "
        "توجد في مودَعٍ مختومٍ مشكول.",
        "",
        "## الديونُ: أبوابٌ عند سيبويه لا قاعدةَ لها هنا", "",
        f"{m['debts']} أبوابٍ بأسطرها (`debts_named`): لا تداخلَ مع أسطر الأبواب المودَعة.", "",
        *(f"- {t} ({n:,})" for t, n in DEBTS),
        "",
        "## ما ليس هنا — باسمه", "",
        "- الشاهدُ رسمٌ لا خانات لأنّ النصَّ المختوم غيرُ مشكول؛ الخاناتُ من مودَع المصحف وحدَه.",
        "- الباب يُثبت أنّ الشاهدَ **واردٌ** فيه، لا أنّ سيبويه يسوقه لهذه القاعدة بعينها؛ "
        "تلك قراءةٌ لم تُودَع.",
        "- قواعدُ الإدغام والإمالة والتضعيف وهمزةِ اللام ليست في `Slge.Ilal`؛ أبوابُها ديونٌ أعلاه.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    text = render()
    if "--check" in sys.argv:
        if TARGET.read_text(encoding="utf-8") != text:
            sys.stderr.write("ILAL_BAB_INDEX.md غيرُ مطابق؛ شغّل tools/gen_ilal_bab_index.py\n")
            return 1
        sys.stdout.write("ILAL_BAB_INDEX.md مطابق\n")
        return 0
    TARGET.write_text(text, encoding="utf-8")
    sys.stdout.write("كُتب ILAL_BAB_INDEX.md\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
