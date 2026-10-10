"""فهرسُ الحكم (HUKM_INDEX.md): دالّةُ الحكم على مودَع المصحف كاملًا، وعلى مرجع الأحكام المحجوب (ADR ٣٤).

يقرأ `corpus-certificates.json.gz` (صورُ المصحف وتكرارُها مواقعَ) ويمرّر كلَّ صورةٍ على
`hukm.hukm_of_form`: جذورُ قراءات الجذع ثمّ حكمُ الجنس (الركن 4) وحكمُ القابليّة (الركن 7) لكلّ جذر من
مودَع المعلومات السابقة (`ajnas-qabiliyyat.json.gz`) — فيعدّ: الصورَ بلا جذرٍ (**لا حكم**)، والصورَ ذاتَ
الحكم ومنها ما فيه «مفهومٌ» بشاهد (جنسًا أو قابليّةً) وما كلُّه «معلومة»، والمواقعَ كذلك بالتكرار؛ ويذكر
أكثرَ الأجناس والعقد شهادةً.
ثمّ **المرجعُ المحجوب** (`hukm-reference.tsv`، إطارٌ من 300 موقعٍ من المصحف ببذرةٍ معلَنة — الغانم ADR ٩):
ما ملأه المالكُ من أعمدته (الجذر، الجنس، القابليّة) يُقاس عليه الحكمُ موقعًا موقعًا؛ وما لم يُملأ فلا رقم —
الفهرسُ يكتب «لا رقم» ولا يخمّن. يكتب أيضًا `formal/Slge/HukmTable.lean` و`src/slge/hukm_table.py`
(الأعدادُ، ويبرهن Lean قسمتَها). لا نصَّ هنا إلّا عناوينُ المخصّص من جدوله لمطابقة ما كتبه المالك بالرسم.
"""

from __future__ import annotations

import csv
import gzip
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from slge.cells import ALPHABET, Cell
from slge.hukm import JINS, QABILIYYA, hukm_of_form, roots_of_form
from slge.maqayis import decode
from slge.mukhassas import code_of_root, title_of
from slge.salsala import ROWS as SALSALA

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "HUKM_INDEX.md"
LEAN = ROOT / "formal" / "Slge" / "HukmTable.lean"
PY = ROOT / "src" / "slge" / "hukm_table.py"
DATA = ROOT / "tests" / "data"
REFERENCE = DATA / "hukm-reference.tsv"
AJNAS = DATA / "ajnas-qabiliyyat.json.gz"
"""مودَعُ المعلومات السابقة الذي تقرؤه الدالّةُ عبر `ajnas_table` (مسجَّلٌ هنا للسجلّ)."""
OWNER = ("root", "jins", "qabiliyya")
Word = tuple[Cell, ...]
MARKS = {"فتح": "َ", "كسر": "ِ", "ضم": "ُ", "سكون": "ْ"}


def _load(name: str) -> dict[str, Any]:
    with gzip.open(DATA / name, "rt", encoding="utf-8") as f:
        d: dict[str, Any] = json.load(f)
    return d


def _forms(d: dict[str, Any]) -> list[Word]:
    return [tuple((a, b) for a, b in x["cells"]) for x in d["forms"]]


def vowelled(w: Word) -> str:
    return "".join(k + MARKS[s] for k, s in w)


def _root_name(code: int) -> str:
    return " ".join(ALPHABET[i] if i < 29 else "ـ" for i in decode(code))


def _owner_root_code(text: str) -> int | None:
    """جذرُ المالك حروفًا مفصولةً بمسافة ← رمزُ جدول المقاييس، أو لا شيء إن لم يكن فيه."""

    letters = tuple(text.split())
    if len(letters) != 3 or any(x not in ALPHABET for x in letters):
        return None
    return code_of_root(letters)


def _reference(forms: list[Word], stream: list[int], line_lengths: list[int]) -> dict[str, Any]:
    """المرجعُ المحجوب: المملوءُ من الإطار يُقاس عليه موقعًا موقعًا؛ ولا رقمَ إن لم يُملأ شيء."""

    with REFERENCE.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    offsets = [0]
    for n in line_lengths:
        offsets.append(offsets[-1] + n)
    filled = [r for r in rows if any(r.get(k, "").strip() for k in OWNER)]
    root_ok = jins_ok = qab_ok = unresolved = 0
    for r in filled:
        token = offsets[int(r["line"]) - 1] + int(r["pos"]) - 1
        fi = stream[token]
        if fi < 0:
            unresolved += 1
            continue
        w = forms[fi]
        roots = roots_of_form(w)
        code = _owner_root_code(r.get("root", "").strip())
        if code is not None and code in roots:
            root_ok += 1
        h = hukm_of_form(w) or []
        by_root = {x[0]: x for x in h}
        for key, rukn, ok_field in (("jins", JINS, "jins"), ("qabiliyya", QABILIYYA, "qab")):
            want = r.get(key, "").strip()
            if not want:
                continue
            j = None
            if code in by_root:
                j = by_root[code][1] if rukn == JINS else by_root[code][2]
            got = "-" if j is None or j.witness is None else title_of(j.witness)
            if got == want:
                if ok_field == "jins":
                    jins_ok += 1
                else:
                    qab_ok += 1
    return {"size": len(rows), "filled": len(filled), "unresolved": unresolved,
            "root_agree": root_ok, "jins_agree": jins_ok, "qabiliyya_agree": qab_ok}


def measure() -> dict[str, Any]:
    start, ctx = _load("corpus-certificates.json.gz"), _load("context-certificates.json.gz")
    assert start["corpus_sha256"] == ctx["corpus_sha256"]
    forms = _forms(start)
    stream: list[int] = list(start["stream"])
    freq: Counter[int] = Counter(i for i in stream if i >= 0)
    la_hukm = any_mafhum = both_malumah = single = multi = 0
    la_hukm_tok = any_mafhum_tok = both_malumah_tok = 0
    jins_forms = qab_forms = 0
    books: Counter[int] = Counter()
    nodes: Counter[int] = Counter()
    for i, w in enumerate(forms):
        h = hukm_of_form(w)
        if h is None:
            la_hukm += 1
            la_hukm_tok += freq[i]
            continue
        if len(h) == 1:
            single += 1
        else:
            multi += 1
        j_ok = any(x[1].witness is not None for x in h)
        q_ok = any(x[2].witness is not None for x in h)
        jins_forms += j_ok
        qab_forms += q_ok
        if j_ok or q_ok:
            any_mafhum += 1
            any_mafhum_tok += freq[i]
            for x in h:
                if x[1].witness is not None:
                    books[x[1].witness] += 1
                if x[2].witness is not None:
                    nodes[x[2].witness] += 1
        else:
            both_malumah += 1
            both_malumah_tok += freq[i]
    return {
        "forms": len(forms), "tokens": sum(freq.values()),
        "la_hukm": la_hukm, "ahkam": len(forms) - la_hukm, "single_root": single,
        "multi_root": multi, "any_mafhum": any_mafhum, "both_malumah": both_malumah,
        "jins_mafhum": jins_forms, "qabiliyya_mafhum": qab_forms,
        "tokens_la_hukm": la_hukm_tok, "tokens_any_mafhum": any_mafhum_tok,
        "tokens_both_malumah": both_malumah_tok,
        "top_books": [(title_of(b), n) for b, n in books.most_common(10)],
        "top_nodes": [(title_of(w), n) for w, n in nodes.most_common(10)],
        "reference": _reference(forms, stream, list(ctx["line_lengths"])),
    }


def render_tables(m: dict[str, Any]) -> tuple[str, str]:
    r = m["reference"]
    lean = "\n".join([
        "/-! الحكمُ على مودَع المصحف — مولَّدٌ بـ`tools/gen_hukm_index.py`؛ لا يُحرَّر باليد.",
        "الأعدادُ صورًا: بلا جذرٍ (لا حكم)، وذاتُ الحكم ومنها ما فيه مفهومٌ بشاهد وما كلُّه معلومة؛",
        "والمرجعُ المحجوب: حجمُه وما مُلئ منه (ولا رقمَ قبل الملء). -/", "",
        "namespace Slge.HukmTable", "",
        f"def forms : Nat := {m['forms']}",
        f"def laHukm : Nat := {m['la_hukm']}",
        f"def ahkam : Nat := {m['ahkam']}",
        f"def anyMafhum : Nat := {m['any_mafhum']}",
        f"def bothMalumah : Nat := {m['both_malumah']}",
        f"def singleRoot : Nat := {m['single_root']}",
        f"def multiRoot : Nat := {m['multi_root']}",
        f"def referenceSize : Nat := {r['size']}",
        f"def referenceFilled : Nat := {r['filled']}", "",
        "/-- القسمةُ تامّة: لا حكم + ذاتُ الحكم = الصور؛ وذاتُ الحكم مفهومٌ بشاهد أو معلومةٌ كلُّه؛",
        "وبجذرٍ أو بجذور؛ والمملوءُ من المرجع لا يتجاوز حجمَه. -/",
        "theorem partition :",
        "    laHukm + ahkam = forms ∧ anyMafhum + bothMalumah = ahkam ∧",
        "      singleRoot + multiRoot = ahkam ∧ referenceFilled ≤ referenceSize := by decide", "",
        "end Slge.HukmTable", "",
    ])
    py = "\n".join([
        '"""الحكمُ على مودَع المصحف — مولَّدٌ بـ`tools/gen_hukm_index.py`؛ لا يُحرَّر باليد."""', "",
        "from __future__ import annotations", "", "from typing import Final", "",
        f"FORMS: Final[int] = {m['forms']}",
        f"LA_HUKM: Final[int] = {m['la_hukm']}",
        f"AHKAM: Final[int] = {m['ahkam']}",
        f"ANY_MAFHUM: Final[int] = {m['any_mafhum']}",
        f"BOTH_MALUMAH: Final[int] = {m['both_malumah']}",
        f"SINGLE_ROOT: Final[int] = {m['single_root']}",
        f"MULTI_ROOT: Final[int] = {m['multi_root']}",
        f"REFERENCE_SIZE: Final[int] = {r['size']}",
        f"REFERENCE_FILLED: Final[int] = {r['filled']}", "",
    ])
    return lean, py


def _pct(a: int, b: int) -> str:
    return f"{a:,} من {b:,} ({100 * a / b:.1f}%)" if b else "—"


def render(m: dict[str, Any]) -> str:
    r = m["reference"]
    jins_name, qab_name = SALSALA[JINS][2], SALSALA[QABILIYYA][2]
    lines = [
        "# فهرسُ الحكم — من جذور الشهادة إلى ركنٍ من السلسلة بشاهدٍ من المودَع، أو «لا حكم»",
        "",
        "مولَّدٌ بـ`python tools/gen_hukm_index.py` من مودَع شهادات المصحف "
        "(`corpus-certificates.json.gz`) "
        "ومودَع المعلومات السابقة (`ajnas-qabiliyyat.json.gz`) ومرجع الأحكام المحجوب "
        "(`hukm-reference.tsv`)؛ لا يُحرَّر باليد. الدالّةُ `Slge.Hukm.hukm` (مرآتُها `slge.hukm`): لكلّ "
        f"جذرٍ من قراءات الجذع حكمان — **{jins_name}** (الركن {JINS}: الجذرُ اسمُ كتابٍ في المخصّص، "
        f"شاهدُه الكتاب) و**{qab_name}** (الركن {QABILIYYA}: الجذرُ في عنوان عقدةٍ تحت كتاب، شاهدُه "
        "العقدة) — «مفهومٌ» بشاهدٍ من المودَع أو «معلومةٌ» بلا شاهد؛ ولا جذرَ فـ«لا حكم». المبرهَن: لا "
        "إسقاطَ ولا زيادة (`hukm_length`، `hukm_mem`)، لا «مفهوم» بلا شاهدٍ عقدةٍ من الشجرة "
        "(`qabiliyya_witness_in_tree`)، والحكمُ لا يمسّ الشهادة (`shahada_untouched`).",
        "",
        "## على مودَع المصحف كاملًا (مقيسٌ على المودَع، لا على مرجع)",
        "",
        "| | صورًا | مواقعَ |",
        "|---|---|---|",
        f"| لا حكم (لا جذرَ للجذع) | {_pct(m['la_hukm'], m['forms'])} | "
        f"{_pct(m['tokens_la_hukm'], m['tokens'])} |",
        f"| ذاتُ حكمٍ فيه مفهومٌ بشاهد | {_pct(m['any_mafhum'], m['forms'])} | "
        f"{_pct(m['tokens_any_mafhum'], m['tokens'])} |",
        f"| ذاتُ حكمٍ كلُّه معلومة | {_pct(m['both_malumah'], m['forms'])} | "
        f"{_pct(m['tokens_both_malumah'], m['tokens'])} |",
        "",
        f"من ذوات الحكم ({m['ahkam']:,} صورة): بجذرٍ واحد {m['single_root']:,}، بجذورٍ متعدّدة "
        f"{m['multi_root']:,} (التعدّدُ يُرتَّب ولا يُحسم: `mem_rank`)؛ فيها مفهومُ جنسٍ "
        f"{m['jins_mafhum']:,}، ومفهومُ قابليّةٍ {m['qabiliyya_mafhum']:,}.",
        "",
        "### أكثرُ الأجناس شهادةً (الكتاب في المخصّص: كم صورةً جذرُها اسمُه)",
        "",
        "| الكتاب | الصور |", "|---|---|",
        *(f"| {t} | {n:,} |" for t, n in m["top_books"]),
        "",
        "### أكثرُ العقد شهادةً للقابليّة",
        "",
        "| العقدة | الصور |", "|---|---|",
        *(f"| {t} | {n:,} |" for t, n in m["top_nodes"]),
        "",
        "## على مرجع الأحكام المحجوب",
        "",
        f"الإطارُ {r['size']} موقعًا من المصحف ببذرةٍ معلَنة (الغانم `tools/gen_hukm_sample.py`، "
        "ADR ٩)، "
        f"يملؤه المالكُ بيده: الجذرُ، الجنسُ (عنوانُ الكتاب بلفظه أو «-»)، القابليّةُ (عنوانُ العقدة "
        "بلفظه أو «-»).",
        "",
    ]
    if r["filled"] == 0:
        lines += ["**لا رقم:** المرجعُ لم يُملأ بعد (0 من "
                  f"{r['size']})؛ فكلُّ ما فوق «مقيسٌ على المودَع» لا على مرجعٍ محجوب، والحكمُ "
                  "«مفحوصٌ/مبرهنُ البناء» حتى يُملأ ويُوقَّع.", ""]
    else:
        lines += [f"المملوءُ {r['filled']} من {r['size']} (منها {r['unresolved']} موقعًا رفضته "
                  "البوّابة):",
                  "", "| | موافقةُ الحكم للمالك |", "|---|---|",
                  f"| الجذر | {_pct(r['root_agree'], r['filled'])} |",
                  f"| الجنس | {_pct(r['jins_agree'], r['filled'])} |",
                  f"| القابليّة | {_pct(r['qabiliyya_agree'], r['filled'])} |", ""]
    lines += ["**ما بقي باسمه:** الحكمُ هنا على ركنَين من اثنين وعشرين؛ وما ليس من جذور المقاييس "
              "لا حكمَ له باسمه؛ والمرتبةُ من جدول السلسلة (ظنٌّ للركنين) لا من المودَع.", ""]
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    m = measure()
    lean, py = render_tables(m)
    text = render(m)
    if "--check" in argv:
        ok = (TARGET.read_text(encoding="utf-8") == text
              and LEAN.read_text(encoding="utf-8") == lean
              and PY.read_text(encoding="utf-8") == py)
        sys.stdout.write("HUKM_INDEX.md مطابق\n" if ok else "HUKM_INDEX.md غيرُ مطابق\n")
        return 0 if ok else 1
    LEAN.write_text(lean, encoding="utf-8")
    PY.write_text(py, encoding="utf-8")
    TARGET.write_text(text, encoding="utf-8")
    sys.stdout.write("كُتب HUKM_INDEX.md وجدولا الحكم\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
