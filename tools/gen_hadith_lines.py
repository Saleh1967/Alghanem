"""المدوّنةُ المختومةُ الثانية — الصحيحان (Open-Hadith-Data، ODbL 1.0): من الملفّين المختومين إلى سطور.

المصدرُ ملفّان مضغوطان في `corpora/hadith/` (بايتاتُهما بعد فكّ الضغط ببصمتهما `HADITH_SOURCES`؛
الأصلُ mhashim6/Open-Hadith-Data عند الإيداع `1515f6cb`، 2022-07-30؛ الرخصةُ `LICENSE.ODbL`).
العمودُ الثاني في كلّ صفٍّ متنُ الحديث بإسناده مشكولًا؛ هذه الأداةُ تجعله **سطورًا** (الحديثُ سطرٌ،
كالآية) في `corpora/hadith/sahihain-lines.txt.gz` — مدوّنةً مختومةً ببصمتها
(`gate.api.SEALED_CORPORA`) تدخل البوّابةَ بالقانون نفسِه. التحويلُ **بلا تطبيع**: كلُّ ما ليس كلمةً
يُسمّى رمزًا بين قوسين ويبقى في موضعه، فيُردّ العمودُ بعينه (`restore_column`، يفحصه `--check` على كلّ
صفّ):

* `‏` (U+200F، علامةُ اتّجاه الطبعة) منفردةً → `<rlm>`؛ ملتصقةً بأوّل كلمةٍ → `<rlm+>` قبل الكلمة.
* `{` و`}` (أقواسُ المقتبَس القرآنيّ في الطبعة) → `<q>` و`</q>`.
* حرفٌ عربيٌّ مفردٌ بلا علامة (ح: تحويلُ الإسناد؛ و: واوُ العطف بين الإسنادين غيرَ مشكولة؛ ق، ص: رموز)
  → `<ltr:ح>`… — ليست كلماتٍ مشكولة فلا تدخل البوّابةَ ولا تُشكَّل تخمينًا.
* ما سوى ذلك كلماتٌ كما هي بايتًا بايتًا.

لا قراءةَ لنصٍّ هنا بغير هذا؛ الأداةُ معفاةٌ في الحارس لأنّها أداةُ إيداع.
"""

from __future__ import annotations

import csv
import gzip
import hashlib
import io
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HADITH = ROOT / "corpora" / "hadith"
TARGET = HADITH / "sahihain-lines.txt.gz"
RLM = "‏"
HADITH_SOURCES: dict[str, str] = {
    "sahih_al-bukhari_ahadith_mushakkala_mufassala.utf8.csv":
        "b03f661876fc4089520800b9231b57a1564baff734344ea8914494b86e2eb708",
    "sahih_muslim_ahadith_mushakkala_mufassala.utf8.csv":
        "79232c8d7c27fef161d8f33ca169f9754741cfe14957dde2ac76893374998943",
}
"""بصمةُ كلّ ملفٍّ مصدرٍ بعد فكّ الضغط — الختم."""


def _arabic_letter(ch: str) -> bool:
    return "ء" <= ch <= "ي"


def tokens_of(column: str) -> list[str]:
    """عمودُ الحديث ← رموزٌ وكلمات؛ عكسُه `restore_column`."""

    out: list[str] = []
    for tok in column.split(" "):
        if tok == "":
            out.append("<sp>")  # فراغان متتاليان في الطبعة: يُحفظان
            continue
        if tok == RLM:
            out.append("<rlm>")
            continue
        if tok.startswith(RLM):
            out.append("<rlm+>")
            tok = tok[1:]
        if tok == "{":
            out.append("<q>")
        elif tok == "}":
            out.append("</q>")
        elif len(tok) == 1 and _arabic_letter(tok):
            out.append(f"<ltr:{tok}>")
        else:
            if RLM in tok or "<" in tok or ">" in tok or "{" in tok or "}" in tok:
                raise ValueError(f"UNNAMED_EDITION_GLYPH:{tok!r}")
            out.append(tok)
    return out


def restore_column(tokens: list[str]) -> str:
    """الرموزُ والكلمات ← عمودُ الحديث بعينه."""

    parts: list[str] = []
    glue = False
    for t in tokens:
        if t == "<rlm+>":
            parts.append(RLM)
            glue = True
            continue
        if t == "<sp>":
            word = ""
        elif t == "<rlm>":
            word = RLM
        elif t == "<q>":
            word = "{"
        elif t == "</q>":
            word = "}"
        elif t.startswith("<ltr:"):
            word = t[5:-1]
        else:
            word = t
        if glue:
            parts[-1] += word
            glue = False
        else:
            parts.append(word)
    return " ".join(parts)


def sources() -> list[tuple[str, list[str]]]:
    """(الملفّ، أعمدةُ الحديث صفًّا صفًّا) بعد فحص الختم."""

    csv.field_size_limit(1 << 30)
    out: list[tuple[str, list[str]]] = []
    for name, sha in HADITH_SOURCES.items():
        with gzip.open(HADITH / (name + ".gz"), "rb") as f:
            raw = f.read()
        digest = hashlib.sha256(raw).hexdigest()
        if digest != sha:
            raise SystemExit(f"WRONG_SEALED_CORPUS:{name}:{digest}")
        rows = list(csv.reader(io.StringIO(raw.decode("utf-8"), newline="")))
        if any(len(r) != 3 for r in rows):
            raise SystemExit(f"UNEXPECTED_ROW_SHAPE:{name}")
        out.append((name, [r[1] for r in rows]))
    return out


def lines() -> tuple[list[str], dict[str, int]]:
    text: list[str] = []
    per_book: dict[str, int] = {}
    for name, cols in sources():
        per_book[name] = len(cols)
        for col in cols:
            toks = tokens_of(col)
            if restore_column(toks) != col:
                raise SystemExit("LOSSY_LINE")
            text.append(" ".join(toks))
    return text, per_book


def stats() -> dict[str, int | dict[str, int]]:
    """أرقامُ المدوّنة الثانية لسجلّ الأرقام (`gen_claims`): الأحاديثُ بكتابيها والكلماتُ والرموز."""

    text, per_book = lines()
    toks = [t for ln in text for t in ln.split()]
    return {"lines": len(text), "per_book": per_book,
            "words": sum(1 for t in toks if not t.startswith("<")),
            "markers": sum(1 for t in toks if t.startswith("<"))}


def render(text: list[str]) -> bytes:
    return ("\n".join(text) + "\n").encode("utf-8")


def main(argv: list[str]) -> int:
    text, per_book = lines()
    blob = render(text)
    digest = hashlib.sha256(blob).hexdigest()
    words = sum(1 for ln in text for t in ln.split() if not t.startswith("<"))
    markers = sum(1 for ln in text for t in ln.split() if t.startswith("<"))
    books = ", ".join(f"{k.split('_')[1]} {v:,}" for k, v in per_book.items())
    summary = (f"{len(text):,} حديثًا ({books})، {words:,} كلمة، {markers:,} رمزَ طبعة؛ "
               f"بصمةُ السطور {digest}")
    if "--check" in argv:
        with gzip.open(TARGET, "rb") as f:
            current = f.read()
        if current != blob:
            sys.stderr.write("sahihain-lines.txt.gz غيرُ مطابق؛ شغّل tools/gen_hadith_lines.py\n")
            return 1
        sys.stdout.write(f"سطورُ الصحيحين مطابقة: {summary}\n")
        return 0
    with TARGET.open("wb") as raw_f, gzip.GzipFile(fileobj=raw_f, mode="wb", compresslevel=9,
                                                     mtime=0) as f:
        f.write(blob)  # بلا طابع زمنٍ في رأس gzip: بايتاتُ الملفّ دالّةٌ في محتواه وحدَه
    sys.stdout.write(f"كُتب {TARGET.name}: {summary}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
