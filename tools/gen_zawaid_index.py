"""فهرسُ الزوائد (ZAWAID_INDEX.md): حروفُ سيبويه العشرة على الخانات، ونونُ التوكيد وتاءُ التأنيث قراءةً
على مودَع المصحف أوّلًا ثمّ على MASAQ، وشواهدُ القرآن من الباب بالرسم.

(١) الجدولُ كما نُقل: الحرفُ، مواضعُه، أمثلتُه، وكم خانةً من الـ116 يشغل. (٢) على
`corpus-certificates.json.gz`:
الصورُ التي آخرُها ثقيلةٌ `ـنَّ` أو تاءٌ ساكنة `ـتْ`، وكم منها يقرؤها الجذعُ لاحقةً على فعل (جهتُها فعل)،
وكم بلا قراءةٍ فعليّة — الرقمُ يُنشر كما هو. (٣) على `masaq-zawaid.json` (مرجعٌ محجوب: EMPHATIC_NUN،
SUFF_FEM_TA، PROTECT_NUN): كم كلمةً يوافق القارئُ وسمَها (نونٌ ثقيلة/تاءٌ ساكنة لاحقةً على فعل؛ ونونُ
الوقاية ضمنَ `ـنِي`). (٤) شواهدُ أبواب النون: كلماتُها رسمًا، وكم منها له صورةٌ في المصحف بالرسم
تُقرأ بالنون.
"""

from __future__ import annotations

import gzip
import json
import sys
from pathlib import Path
from typing import Any

from slge.cells import Cell
from slge.jidh import jidh
from slge.wujud import FIL, ont_of_reading
from slge.zawaid import CELLS, LETTERS, TA_TANITH, THAQILA, WITNESSES
from slge.zawaid_table import TABLE

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "ZAWAID_INDEX.md"
DATA = ROOT / "tests" / "data"
Word = tuple[Cell, ...]
NI: Word = (("ن", "كسر"), ("ي", "سكون"))


def corpus_forms() -> list[Word]:
    with gzip.open(DATA / "corpus-certificates.json.gz", "rt", encoding="utf-8") as f:
        d: dict[str, Any] = json.load(f)
    return [tuple((a, b) for a, b in x["cells"]) for x in d["forms"]]


def masaq() -> list[dict[str, Any]]:
    with (DATA / "masaq-zawaid.json").open(encoding="utf-8") as f:
        rows: list[dict[str, Any]] = json.load(f)
    return rows


def rasm(w: Word) -> str:
    """رسمُ الخانات: الحواملُ مع طيّ المثلين (الشدّة) — للربط بشواهد الباب غير المشكولة."""

    out: list[str] = []
    for i, (k, s) in enumerate(w):
        if i and s != "سكون" and w[i - 1] == (k, "سكون"):
            continue  # الثاني من المثلين
        out.append(k)
    return "".join(out)


def reads_as_verb_with(w: Word, suf: Word) -> bool:
    return any(rd.suf == suf and ont_of_reading(rd) == FIL for rd in jidh(w))


def measure() -> dict[str, Any]:
    forms = corpus_forms()
    end_nn = [w for w in forms if w[-2:] == THAQILA]
    end_t = [w for w in forms if w[-1:] == TA_TANITH]
    nn_verb = sum(reads_as_verb_with(w, THAQILA) for w in end_nn)
    t_verb = sum(reads_as_verb_with(w, TA_TANITH) for w in end_t)
    ref = masaq()
    by_tag: dict[str, dict[str, int]] = {}
    for r in ref:
        d = by_tag.setdefault(r["t"], {"n": 0, "cells": 0, "agree": 0})
        d["n"] += 1
        if r["cells"] is None:
            continue
        d["cells"] += 1
        w = tuple((a, b) for a, b in r["cells"])
        if r["t"] == "EMPHATIC_NUN":
            ok = any(rd.suf[:2] == THAQILA and ont_of_reading(rd) == FIL for rd in jidh(w))
        elif r["t"] == "SUFF_FEM_TA":
            ok = any(rd.suf[:1] == TA_TANITH and ont_of_reading(rd) == FIL for rd in jidh(w))
        else:  # PROTECT_NUN: نونُ الوقاية ضمنَ ـنِي أو ـنِ
            ok = any(rd.suf[:2] == NI or rd.suf[:1] == (("ن", "كسر"),) for rd in jidh(w))
        d["agree"] += int(ok)
    by_rasm: dict[str, Word] = {}
    for w in forms:
        by_rasm.setdefault(rasm(w), w)
    witness_words = [x for _, ws in WITNESSES for x in ws]
    linked = [x for x in witness_words if _rasm_of(x) in by_rasm]
    read_nn = [x for x in linked if by_rasm[_rasm_of(x)][-2:] == THAQILA
               and reads_as_verb_with(by_rasm[_rasm_of(x)], THAQILA)]
    return {"letters": list(LETTERS), "cells": len(CELLS),
            "table": [(n, k, list(p), len(ex)) for n, k, p, ex, _ in TABLE],
            "end_thaqila": len(end_nn), "thaqila_verb": nn_verb,
            "end_ta": len(end_t), "ta_verb": t_verb, "masaq": by_tag,
            "witness_words": len(witness_words), "witness_linked": len(linked),
            "witness_read": len(read_nn), "witness_read_words": read_nn}


def _rasm_of(x: str) -> str:
    table = {"أ": "ء", "إ": "ء", "ؤ": "ء", "ئ": "ء", "آ": "ءا", "ة": "ت", "ى": "ا"}
    return "".join(table.get(ch, ch) for ch in x)


def render() -> str:
    m = measure()
    lines = [
        "# فهرسُ الزوائد — حروفُ سيبويه العشرة خاناتٍ، ونونُ التوكيد وتاءُ التأنيث قراءةً",
        "",
        "مولَّدٌ بـ`python tools/gen_zawaid_index.py` من `src/slge/zawaid.py`؛ لا يُحرَّر باليد. البرهانُ "
        "`formal/Slge/Zawaid.lean`؛ الجدولُ `formal/Slge/ZawaidTable.lean` مولَّدٌ من المختوم "
        "`tests/data/openiti-sibawayh-kitab.txt.gz` (`tools/deposit_zawaid.py --check`؛ الكتابُ "
        "لسيبويه، OpenITI JK006989، CC BY-NC-SA 4.0): «باب علم حروف الزوائد» و«باب النون الثقيلة "
        "والخفيفة».",
        "",
        "## الحروفُ العشرة كما نُقلت", "",
        "| الحرف | الحامل | المواضع كما وردت | الأمثلة |", "|---|---|---|---|",
    ]
    for n, k, p, cnt in m["table"]:
        lines.append(f"| {n} | {k} | {', '.join(str(x) for x in p) or '—'} | {cnt} |")
    lines += [
        "",
        f"عشرةُ حواملَ متمايزة (`letters_ten`، `letters_nodup`) تشغل **{m['cells']} خانةً من الـ116** "
        "(`cells_forty`): الزائدُ خانةٌ كسائر الخانات لا «فردٌ» جديد. حروفُ المضارعة الأربعة منها "
        "(`mudaraa_are_zawaid`) وإلصاقُها يحفظ الترخيص (`mudaraa_licensed`). المواضعُ أعدادٌ ترتيبيّة "
        "كما وردت في الباب بلا تأويل.",
        "",
        "## نونُ التوكيد وتاءُ التأنيث على مودَع المصحف", "",
        f"صورٌ آخرُها الثقيلةُ `ـنَّ`: **{m['end_thaqila']:,}**؛ يقرؤها الجذعُ لاحقةً على فعلٍ: "
        f"**{m['thaqila_verb']:,}** ({100 * m['thaqila_verb'] / m['end_thaqila']:.1f}%) — الباقي "
        "إنَّ/أنَّ/هُنَّ وأخواتُها (اسمٌ أو حرف) لا فعل.",
        f"صورٌ آخرُها التاءُ الساكنة `ـتْ`: **{m['end_ta']:,}**؛ يقرؤها الجذعُ لاحقةً على فعلٍ: "
        f"**{m['ta_verb']:,}** ({100 * m['ta_verb'] / m['end_ta']:.1f}%).",
        "",
        "الإلصاقُ مبرهَنٌ حافظًا للترخيص (`tawkid_licensed`، `anith_licensed`)، والقطعُ عكسُه عبر "
        "`Jidh.enclitics` (`in_enclitics`، `thaqila_read`، `taTanith_read`). والخفيفةُ `ـنْ` خانتُها "
        "خانةُ التنوين (`khafifa_is_tanwin`) — فالقارئُ يردّها تنوينًا على الاسم ونونًا على الفعل "
        "بالجهة لا بالخانة.",
        "",
        "## على MASAQ (مرجعٌ محجوب)", "",
        "| الوسم | الكلمات | لها شهادة | يوافق القارئ |", "|---|---|---|---|",
    ]
    for t, d in sorted(m["masaq"].items()):
        pct = f"{100 * d['agree'] / d['cells']:.1f}%" if d["cells"] else "—"
        lines.append(f"| `{t}` | {d['n']} | {d['cells']} | {d['agree']} ({pct}) |")
    lines += [
        "",
        "`EMPHATIC_NUN`: قراءةٌ لاحقتُها الثقيلةُ (أو تبدأ بها قبل ضمير) على فعل؛ `SUFF_FEM_TA`: "
        "التاءُ الساكنة على فعل؛ `PROTECT_NUN`: نونُ الوقاية ضمنَ `ـنِي`/`ـنِ` — ليست زائدةً "
        "مستقلّةً في الخانات.",
        "",
        "## شواهدُ أبواب النون من الباب نفسه", "",
        f"كلماتُ الاقتباسات القرآنيّة في الأبواب: {m['witness_words']}؛ لها صورةٌ في المصحف بالرسم: "
        f"{m['witness_linked']}؛ منها ما آخرُه الثقيلةُ ويُقرأ فعلًا بها: {m['witness_read']} "
        f"({'، '.join(m['witness_read_words']) or '—'}).",
        "",
        "## ما ليس هنا — باسمه", "",
        "- الخفيفةُ لا تُعدّ على المصحف لأنّ خانتَها خانةُ التنوين؛ عدُّها يحتاج قرينةَ الجهة (الفعل) "
        "وهي في القارئ لا في الخانة.",
        "- صورتا النون في المثنّى والنسوة (تَفْعَلَانِّ، يَفْعَلْنَانِّ — «باب النون في فعل الاثنين وفعل "
        "جميع النساء») لم تُنفَّذ عمليّةً بعد.",
        "- أمثلةُ الباب غيرُ مشكولة فلا تدخل البوّابة؛ ربطُها بالحوامل «مطابَقٌ بالرسم» لا ترخيص.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    text = render()
    if "--check" in sys.argv:
        if TARGET.read_text(encoding="utf-8") != text:
            sys.stderr.write("ZAWAID_INDEX.md غيرُ مطابق؛ شغّل tools/gen_zawaid_index.py\n")
            return 1
        sys.stdout.write("ZAWAID_INDEX.md مطابق\n")
        return 0
    TARGET.write_text(text, encoding="utf-8")
    sys.stdout.write("كُتب ZAWAID_INDEX.md\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
