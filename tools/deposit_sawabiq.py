"""إيداعُ أبواب السوابق الحرفيّة من الكتاب لسيبويه: باءُ الجرّ ولامُ الجرّ ولامُ الأمر ولامُ كي وألُ
التعريف وهمزةُ الوصل — لكلّ بابٍ سطرُه وشاهدُه بعينه في نصّ الباب، ثمّ صورةٌ من مودَع المصحف يقرؤها
`slge.sawabiq` بالباب نفسه — مولَّدٌ من المختوم `tests/data/openiti-sibawayh-kitab.txt.gz`
(JK006989، CC BY-NC-SA 4.0) ومن `corpus-certificates.json.gz`.

القواعدُ معلَنة:
- `ANCHORS`: (البابُ، عنوانُ الباب كما في النصّ، كلمةُ الشاهد رسمًا، صورةُ المصحف المطلوبة بالتشكيل،
  سوابقُها، أموصولةٌ). الأداةُ تثبت أنّ العنوانَ موجودٌ وأنّ كلمةَ الشاهد واردةٌ في نصّ ذلك الباب بعينه،
  وأنّ صورةَ المصحف موجودةٌ في المودَع **ويقرؤها القارئُ** بذلك الباب وتلك السوابق؛ ما لم يوجد خطأٌ مسمًّى.
- الموصولُ (سقوطُ الهمزة أو كسرة اللام في الوصل) شاهدُه في الكتاب عباراتٌ عبر كلمتين (يا زيد اضرب، من
  الله)؛ فشاهدُ الباب فيه كلمةُ الأصل، وصورةُ المصحف هي الموصولةُ داخل الكلمة الواحدة.

يكتب `formal/Slge/SawabiqTable.lean` و`src/slge/sawabiq_table.py`؛ وبـ`--check` يقارنهما بما يولَّد
الآن.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

from slge.cells import ALPHABET, Cell
from slge.rawabit import cells_of
from slge.sawabiq import KINDS, sawabiq

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "tests" / "data" / "openiti-sibawayh-kitab.txt.gz"
CORPUS = ROOT / "tests" / "data" / "corpus-certificates.json.gz"
LEAN = ROOT / "formal" / "Slge" / "SawabiqTable.lean"
PY = ROOT / "src" / "slge" / "sawabiq_table.py"
SHA = "a160f940bb194e6fe7e6655d2c7f28e41f1fc648c4c5e340cc4e42306d5cb625"
RASM: dict[str, str] = {"أ": "ء", "إ": "ء", "ؤ": "ء", "ئ": "ء", "آ": "ءا", "ة": "ت", "ى": "ا"}
PREFIXES: tuple[str, ...] = ("", "و", "ف")
"""سوابقُ الشاهد المقبولة في نصّ الباب: العطفُ (وابنم واسم واست)."""

KALIM = "هذا باب عدة ما يكون عليه الكلم"
JAZM = "هذا باب ما يعمل في الأفعال فيجزمها"
AN = "هذا باب الحروف التي تضمر فيها أن"
WASL = "هذا باب ما يتقدم أول الحروف وهي زائدة قدمت لإسكان أول الحروف"
ASMA = "هذا باب كينونتها في الأسماء"
ANCHORS: tuple[tuple[str, str, str, str, str, bool], ...] = (
    ("BA_JARR", KALIM, "بزيد", "بِرَبِّ", "بِ", False),
    ("LAM_JARR", KALIM, "لك", "لِرَبِّ", "لِ", False),
    ("LAM_AMR", JAZM, "ليفعل", "لِيُنْفِقْ", "لِ", False),
    ("LAM_AMR", ASMA, "فلينظر", "فَلْيَنْظُرْ", "فَ", True),
    ("LAM_KAY", AN, "لتفعل", "لِيَحْكُمَ", "لِ", False),
    ("AL", WASL, "الرجل", "اَلْحَمْدُ", "", False),
    ("AL", WASL, "بذل", "بِلْحَقِّ", "بِ", True),
    ("WASL_FIL", WASL, "اضرب", "اُسْكُنْ", "", False),
    ("WASL_FIL", WASL, "اضرب", "وَسْتَغْفِرْ", "وَ", True),
    ("WASL_ISM", ASMA, "ابن", "اِبْنَ", "", False),
    ("WASL_ISM", ASMA, "اسم", "بِسْمِ", "بِ", True),
)
"""الأبوابُ بشواهدها: «بزيد» (خرجت بزيد — باء الجر للإلزاق)، «لك» (الغلام لك — لام الإضافة الملك)،
«ليفعل» (اللام التي في الأمر)، «فلينظر» (لام الأمر مع الفاء والواو مسكَّنة)، «لتفعل» (جئتك لتفعل — أن
مضمرة)، «الرجل» (الحرف الذي تعرف به الأسماء)، «بذل» (بالشحم … بذل: أل موصولةً بعد الباء)، «اضرب» (ألف
الوصل في الأمر)، «ابن» و«اسم» (الأسماء التي أُسكنت أوائلها)."""


def _read() -> tuple[str, list[str]]:
    raw = gzip.decompress(SRC.read_bytes())
    sha = hashlib.sha256(raw).hexdigest()
    if sha != SHA:
        raise SystemExit(f"SOURCE_SHA_MISMATCH {sha}")
    return sha, raw.decode("utf-8").split("\n")


def _find_chapter(lines: list[str], title: str) -> int:
    """سطرُ العنوان (1-based) الذي يبدأ بـ`# | ( <title>` أو `# | <title>`؛ عنوانٌ لا يوجد خطأٌ
    مسمًّى."""

    for i, ln in enumerate(lines):
        if ln.startswith("# | ( " + title) or ln.startswith("# | " + title):
            return i + 1
    raise SystemExit(f"CHAPTER_NOT_FOUND:{title}")


def _chapter_text(lines: list[str], start: int) -> str:
    body: list[str] = []
    k = start
    while k < len(lines) and not (lines[k].startswith("# | ( هذا باب")
                                  or lines[k].startswith("# | هذا باب")):
        body.append(lines[k][2:] if lines[k].startswith("~~") else lines[k].lstrip("# "))
        k += 1
    return re.sub(r"\s+", " ", re.sub(r"PageV\d+P\d+|ms\d+", " ", " ".join(body)))


def rasm_of_word(w: str) -> str:
    return "".join(RASM.get(ch, ch) for ch in w).replace("ء", "ا")


def corpus_forms() -> set[tuple[Cell, ...]]:
    with gzip.open(CORPUS, "rt", encoding="utf-8") as f:
        d: dict[str, Any] = json.load(f)
    return {tuple((a, b) for a, b in x["cells"]) for x in d["forms"]}


def rows(lines: list[str], forms: set[tuple[Cell, ...]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for kind, title, word, form, pre, joined in ANCHORS:
        assert kind in KINDS, kind
        line = _find_chapter(lines, title)
        toks = set(_chapter_text(lines, line).split())
        if not any(p + word in toks for p in PREFIXES):
            raise SystemExit(f"WITNESS_NOT_IN_CHAPTER:{kind}:{word}@{line}")
        cells = cells_of(form)
        if cells not in forms:
            raise SystemExit(f"FORM_NOT_IN_CORPUS:{kind}:{form}")
        pre_cells = cells_of(pre) if pre else ()
        if not any(m.kind == kind and m.pre == pre_cells and m.joined == joined
                   for m in sawabiq(cells)):
            raise SystemExit(f"FORM_NOT_READ:{kind}:{form}")
        out.append({"kind": kind, "title": title, "line": line, "word": word, "form": form,
                    "cells": cells, "pre": pre_cells, "joined": joined})
    return out


def render_lean(sha: str, rs: list[dict[str, Any]]) -> str:
    idx = {ch: i for i, ch in enumerate(ALPHABET)}
    st = {"فتح": 0, "كسر": 1, "ضم": 2, "سكون": 3}

    def cl(cs: tuple[Cell, ...]) -> str:
        return "[" + ", ".join(f"c {idx[k]} {st[s]}" for k, s in cs) + "]"

    lines = [
        "import Slge.Categories", "",
        "/-! أبوابُ السوابق الحرفيّة عند سيبويه: لكلّ بابٍ سطرُه وشاهدُه حواملَ بالرسم، وصورةٌ من مودَع",
        "المصحف يقرؤها `Sawabiq.sawabiq` بالباب نفسه — مولَّدٌ من المختوم",
        "`tests/data/openiti-sibawayh-kitab.txt.gz`",
        f"(SHA-256 `{sha}`) ومن `corpus-certificates.json.gz`",
        "بـ`tools/deposit_sawabiq.py`؛ لا يُحرَّر باليد. الصفُّ: (رقمُ الباب في `Kind.idx`، سطرُ الباب،",
        "شاهدُ الباب حواملَ، صورةُ المصحف خاناتٍ، سوابقُها، أموصولةٌ). -/", "",
        "namespace Slge.SawabiqTable", "", "open Slge.Categories (c)", "",
        "def table : List (Nat × Nat × List Nat × List SCell × List SCell × Bool) := [",
    ]
    rows_l = []
    for r in rs:
        word = "[" + ", ".join(str(idx[ch]) for ch in rasm_of_word(r["word"]) if ch in idx) + "]"
        rows_l.append(f"  ({KINDS.index(r['kind'])}, {r['line']}, {word}, {cl(r['cells'])}, "
                      f"{cl(r['pre'])}, {'true' if r['joined'] else 'false'})")
    lines += [",\n".join(rows_l), "]", "",
              f"theorem table_length : table.length = {len(rs)} := by rfl", "",
              "end Slge.SawabiqTable", ""]
    return "\n".join(lines)


def render_py(sha: str, rs: list[dict[str, Any]]) -> str:
    lines = [
        '"""أبوابُ السوابق الحرفيّة عند سيبويه بشواهدها وصور المصحف التي يقرؤها القارئ — مولَّدٌ من',
        f'المختوم `tests/data/openiti-sibawayh-kitab.txt.gz` (SHA-256 {sha[:16]}…) ومن مودَع المصحف',
        'بـ`tools/deposit_sawabiq.py`؛ لا يُحرَّر باليد."""', "",
        "from __future__ import annotations", "", "from typing import Final", "",
        "Cell = tuple[str, str]", "",
        "Row = tuple[str, str, int, str, tuple[Cell, ...], tuple[Cell, ...], bool]",
        '"""(الباب، عنوانُ الباب، سطرُه، شاهدُه، صورةُ المصحف، سوابقُها، أموصولة)."""', "",
        "TABLE: Final[tuple[Row, ...]] = (",
    ]
    for r in rs:
        lines.append(f'    ("{r["kind"]}", "{r["title"]}", {r["line"]}, "{r["word"]}",')
        lines.append("     (" + ", ".join(f'("{k}", "{s}")' for k, s in r["cells"]) + "),")
        pre = ", ".join(f'("{k}", "{s}")' for k, s in r["pre"])
        lines.append(f"     ({pre}{',' if len(r['pre']) == 1 else ''}), {r['joined']}),")
    lines += [")", ""]
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    sha, lines = _read()
    rs = rows(lines, corpus_forms())
    lean, py = render_lean(sha, rs), render_py(sha, rs)
    if "--check" in argv:
        ok = LEAN.read_text(encoding="utf-8") == lean and PY.read_text(encoding="utf-8") == py
        sys.stdout.write("جدولا السوابق مطابقان للمختوم\n" if ok else "جدولا السوابق غيرُ مطابقين\n")
        return 0 if ok else 1
    LEAN.write_text(lean, encoding="utf-8")
    PY.write_text(py, encoding="utf-8")
    for r in rs:
        sys.stdout.write(f"{r['kind']}: {r['line']} {r['word']} ← {r['form']}"
                         f"{' (موصول)' if r['joined'] else ''}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
