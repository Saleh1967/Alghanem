"""إيداعُ أبواب الإعلال من الكتاب لسيبويه: لكلّ قاعدةٍ من قواعد `Slge.Ilal` الثلاثَ عشرةَ بابُها بسطره
وشاهدُه بعينه في نصّ الباب، ثمّ صورةٌ من مودَع المصحف تقرؤها القاعدةُ نفسُها — مولَّدٌ من المختوم
`tests/data/openiti-sibawayh-kitab.txt.gz` (JK006989، CC BY-NC-SA 4.0) ومن
`corpus-certificates.json.gz`.

القواعدُ معلَنة:
- `ANCHORS`: (القاعدة، عنوانُ الباب كما في النصّ، كلمةُ الشاهد رسمًا). الأداةُ تثبت أنّ العنوانَ موجودٌ وأنّ
  الكلمةَ واردةٌ في نصّ ذلك الباب بعينه (بسابقة و/ف/ال أو بدونها)؛ ما لم يوجد خطأٌ مسمًّى لا يُتجاوز.
- شاهدُ المصحف: أوّلُ صورةٍ في المودَع رسمُها الخشن رسمُ كلمة الباب (الهمزةُ بصورها والألفُ واحدة،
  ة→ت، ى→ا، طيُّ المثلين، وسابقةُ و/ف/ال)
  **وتقرؤها القاعدةُ** (`undo` غيرُ فارغ في موضعٍ ما)؛ فإن لم توجد سُجّل الشاهدُ رسمًا بلا خانات
  (`none`) ولا يُشكَّل من الذاكرة.
- ما يذكره سيبويه بابًا ولا قاعدةَ له عندنا يُسجَّل في `DEBTS` بعنوانه وسطره: غائبٌ باسمه.

يكتب `formal/Slge/IlalBabTable.lean` و`src/slge/ilal_bab_table.py`؛ وبـ`--check` يقارنهما بما يولَّد
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
from slge.ilal import RULES, undo

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "tests" / "data" / "openiti-sibawayh-kitab.txt.gz"
CORPUS = ROOT / "tests" / "data" / "corpus-certificates.json.gz"
LEAN = ROOT / "formal" / "Slge" / "IlalBabTable.lean"
PY = ROOT / "src" / "slge" / "ilal_bab_table.py"
SHA = "a160f940bb194e6fe7e6655d2c7f28e41f1fc648c4c5e340cc4e42306d5cb625"
PREFIXES: tuple[str, ...] = ("", "و", "ف", "ال", "وال")
"""سوابقُ الشاهد المقبولة في نصّ الباب وفي رسم المصحف: العطفُ والتعريف."""
RASM: dict[str, str] = {"أ": "ء", "إ": "ء", "ؤ": "ء", "ئ": "ء", "آ": "ءا", "ة": "ت", "ى": "ا"}

AYN = "هذا باب ما الياء والواو فيه ثانية وهما في موضع العين منه"
LAM = "هذا باب ما كانت الياء والواو في لامات"
BADAL = "هذا باب حروف البدل"
ANCHORS: tuple[tuple[str, str, str], ...] = (
    ("QALB_AYN", AYN, "خاف"),
    ("HADHF_AYN_U", AYN, "قلت"),
    ("HADHF_AYN_I", AYN, "خفت"),
    ("NAQL", AYN, "يقول"),
    ("QALB_LAM", LAM, "رمى"),
    ("HADHF_LAM", "هذا باب ما يخرج على الأصل إذا لم يكن حرف إعراب", "غزوا"),
    ("HADHF_WAW", "هذا باب ما كانت الواو فيه أولا وكانت فاء", "يعد"),
    ("HAMZA_MADD", "هذا باب الهمز", "آدم"),
    ("TA_TTA", BADAL, "اصطبر"),
    ("TA_DAL", BADAL, "ازدجر"),
    ("FA_TA", "هذا باب ما يلزمه بدل التاء من هذه الواوات التي تكون في موضع الفاء", "اتعد"),
    ("WAW_YA", "هذا باب ما تقلب فيه الواو ياء وذلك إذا سكنت وقبلها كسرة", "ميزان"),
    ("YA_WAW", "هذا باب تقلب فيه الياء واوا", "موقن"),
)
DEBTS: tuple[str, ...] = (
    "هذا باب ما تمال فيه الألفات",
    "هذا باب التضعيف في بنات الياء وذلك نحو عييت وحييت وأحييت",
    "هذا باب التضعيف في بنات الواو",
    "هذا باب ما الهمزة فيه في موضع اللام من بنات الياء والواو",
    "هذا باب ما إذا التقت فيه الهمزة والياء قلبت الهمزة ياء والياء ألفا",
    "هذا باب الإدغام في الحرفين اللذين تضع لسانك لهما موضعا واحدا لا",
    "هذا باب ما شذ من المعتل على الأصل",
)
"""أبوابٌ عند سيبويه لا قاعدةَ لها في `Slge.Ilal`: الإمالة، التضعيفُ في المعتلّ، همزةُ اللام،
التقاءُ الهمزة والياء، الإدغامُ، الشاذُّ على الأصل — تُسجَّل بأسطرها غائبةً باسمها."""


def _read() -> tuple[str, list[str]]:
    raw = gzip.decompress(SRC.read_bytes())
    sha = hashlib.sha256(raw).hexdigest()
    if sha != SHA:
        raise SystemExit(f"SOURCE_SHA_MISMATCH {sha}")
    return sha, raw.decode("utf-8").split("\n")


def _find_chapter(lines: list[str], title: str) -> int:
    """سطرُ العنوان (1-based) الذي يبدأ بـ`# | ( <title>`؛ عنوانٌ لا يوجد خطأٌ مسمًّى."""

    for i, ln in enumerate(lines):
        if ln.startswith("# | ( " + title):
            return i + 1
    raise SystemExit(f"CHAPTER_NOT_FOUND:{title}")


def _chapter_text(lines: list[str], start: int) -> str:
    body: list[str] = []
    k = start  # الأسطرُ بعد العنوان حتى العنوان التالي
    while k < len(lines) and not lines[k].startswith("# | ("):
        body.append(lines[k][2:] if lines[k].startswith("~~") else lines[k].lstrip("# "))
        k += 1
    return re.sub(r"\s+", " ", re.sub(r"PageV\d+P\d+|ms\d+", " ", " ".join(body)))


def rasm_of_word(w: str) -> str:
    """رسمٌ خشن: الهمزةُ بصورها والألفُ واحدةٌ (همزةُ الوصل ألفٌ في الرسم وهمزةٌ في الخانات)."""

    return "".join(RASM.get(ch, ch) for ch in w).replace("ء", "ا")


def rasm_of_cells(cells: tuple[Cell, ...]) -> str:
    out: list[str] = []
    for i, (k, s) in enumerate(cells):
        if i and s != "سكون" and cells[i - 1] == (k, "سكون"):
            continue
        out.append(k)
    return "".join(out).replace("ء", "ا")


def reads(rule: str, w: tuple[Cell, ...]) -> int | None:
    """أوّلُ موضعٍ تقرأ فيه القاعدةُ الصورةَ (`undo` غيرُ فارغ)، أو لا شيء."""

    for i in range(len(w)):
        if undo(rule, w, i):
            return i
    return None


def corpus_forms() -> list[tuple[Cell, ...]]:
    with gzip.open(CORPUS, "rt", encoding="utf-8") as f:
        d: dict[str, Any] = json.load(f)
    return [tuple((a, b) for a, b in x["cells"]) for x in d["forms"]]


def rows(lines: list[str], forms: list[tuple[Cell, ...]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    by_rasm: dict[str, list[tuple[Cell, ...]]] = {}
    for w in forms:
        by_rasm.setdefault(rasm_of_cells(w), []).append(w)
    for rule, title, word in ANCHORS:
        assert rule in RULES, rule
        line = _find_chapter(lines, title)
        text = _chapter_text(lines, line)
        toks = set(text.split())
        if not any(p + word in toks for p in PREFIXES):
            raise SystemExit(f"WITNESS_NOT_IN_CHAPTER:{rule}:{word}@{line}")
        cells: tuple[Cell, ...] | None = None
        at: int | None = None
        source = "none"
        for p in PREFIXES:
            for w in by_rasm.get(rasm_of_word(p + word), []):
                at = reads(rule, w)
                if at is not None:
                    cells, source = w, "chapter"
                    break
            if cells is not None:
                break
        out.append({"rule": rule, "title": title, "line": line, "word": word,
                    "cells": cells, "at": at, "source": source})
    return out


def debts(lines: list[str]) -> list[tuple[str, int]]:
    return [(t, _find_chapter(lines, t)) for t in DEBTS]


def render_lean(sha: str, rs: list[dict[str, Any]], ds: list[tuple[str, int]]) -> str:
    idx = {ch: i for i, ch in enumerate(ALPHABET)}
    st = {"فتح": 0, "كسر": 1, "ضم": 2, "سكون": 3}
    lines = [
        "import Slge.Categories", "",
        "/-! أبوابُ الإعلال عند سيبويه: لكلّ قاعدةٍ بابُها بسطره وشاهدُه حواملَ بالرسم، وصورةٌ من مودَع",
        "المصحف تقرؤها القاعدة — مولَّدٌ من المختوم `tests/data/openiti-sibawayh-kitab.txt.gz`",
        f"(SHA-256 `{sha}`) ومن `corpus-certificates.json.gz` بـ`tools/deposit_ilal_bab.py`؛",
        "لا يُحرَّر باليد. الصفُّ: (رقمُ القاعدة في `Rule.all`، سطرُ الباب، شاهدُ الباب حواملَ،",
        "صورةُ المصحف خاناتٍ، موضعُ القراءة). -/", "",
        "namespace Slge.IlalBab", "", "open Slge.Categories (c)", "",
        "def table : List (Nat × Nat × List Nat × List SCell × Nat) := [",
    ]
    rows_l = []
    for r in rs:
        word = "[" + ", ".join(str(idx[c]) for c in rasm_of_word(r["word"]) if c in idx) + "]"
        cells = "[" + ", ".join(f"c {idx[k]} {st[s]}" for k, s in (r["cells"] or ())) + "]"
        rows_l.append(f"  ({RULES.index(r['rule'])}, {r['line']}, {word}, {cells}, {r['at'] or 0})")
    lines += [",\n".join(rows_l), "]", "",
              f"theorem table_length : table.length = {len(rs)} := by rfl", "",
              "/-- أبوابٌ عند سيبويه لا قاعدةَ لها هنا — بأسطرها، غائبةٌ باسمها. -/",
              "def debts : List Nat := [" + ", ".join(str(n) for _, n in ds) + "]", "",
              "end Slge.IlalBab", ""]
    return "\n".join(lines)


def render_py(sha: str, rs: list[dict[str, Any]], ds: list[tuple[str, int]]) -> str:
    lines = [
        '"""أبوابُ الإعلال عند سيبويه بشواهدها وصور المصحف التي تقرؤها القواعد — مولَّدٌ من المختوم',
        f'`tests/data/openiti-sibawayh-kitab.txt.gz` (SHA-256 {sha[:16]}…) ومن مودَع المصحف',
        'بـ`tools/deposit_ilal_bab.py`؛ لا يُحرَّر باليد."""', "",
        "from __future__ import annotations", "", "from typing import Final", "",
        "Cell = tuple[str, str]", "",
        "Row = tuple[str, str, int, str, tuple[Cell, ...] | None, int | None, str]", "",
        "TABLE: Final[tuple[Row, ...]] = (",
    ]
    for r in rs:
        lines.append(f'    ("{r["rule"]}", "{r["title"]}", {r["line"]}, "{r["word"]}",')
        if r["cells"] is None:
            lines.append(f'     None, None, "{r["source"]}"),')
        else:
            lines.append("     (")
            lines += [f'         ("{k}", "{s}"),' for k, s in r["cells"]]
            lines.append(f'     ), {r["at"]}, "{r["source"]}"),')
    lines += [")", "", "DEBTS: Final[tuple[tuple[str, int], ...]] = ("]
    for t, n in ds:
        lines.append(f'    ("{t}", {n}),')
    lines += [")", ""]
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    sha, lines = _read()
    rs, ds = rows(lines, corpus_forms()), debts(lines)
    lean, py = render_lean(sha, rs, ds), render_py(sha, rs, ds)
    if "--check" in argv:
        ok = LEAN.read_text(encoding="utf-8") == lean and PY.read_text(encoding="utf-8") == py
        sys.stdout.write("جدولا أبواب الإعلال مطابقان للمختوم\n" if ok
                         else "جدولا أبواب الإعلال غيرُ مطابقين\n")
        return 0 if ok else 1
    LEAN.write_text(lean, encoding="utf-8")
    PY.write_text(py, encoding="utf-8")
    for r in rs:
        marks = {"فتح": "َ", "كسر": "ِ", "ضم": "ُ", "سكون": "ْ"}
        cs = "".join(k + marks[s] for k, s in (r["cells"] or ()))
        sys.stdout.write(f"{r['rule']}: {r['line']} {r['word']} ← {cs or '—'} @{r['at']} "
                         f"({r['source']})\n")
    sys.stdout.write(f"الديون: {len(ds)} بابًا\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
