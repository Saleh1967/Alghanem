"""عيّنةُ الصحيحين المحجوبة — إطارٌ يملؤه المالكُ بيده ثمّ يوقَّع (ADR ٧ تتمّة، 2026-10-10).

لا مرجعَ بشريًّا للصحيحين يقيس الاشتقاقَ والاسترجاعَ وحركةَ الوصل (طبعةُ Open-Hadith-Data ألفُ وصلها
مجرّدةٌ أبدًا، وعمودُها الثالث شرحٌ). فالمرجعُ يُصنع لا يُنسخ: هذه الأداةُ تسحب من المدوّنة المختومة
(`sahihain-lines.txt.gz`) عيّنةَ مواقع ببذرةٍ معلَنة (`SEED`) وحجمٍ معلَن (`SIZE`) — موقعًا موقعًا بسطره
وسياقه — وتكتب `corpora/hadith/sample-frame.tsv` بأعمدةٍ ثابتةٍ من المدوّنة وأعمدةٍ **فارغة** يملؤها
المالك: الجذرُ، القسمةُ (سوابق|جذع|لواحق)، حركةُ همزة الوصل إن كانت، وملاحظة. العيّنةُ عمياء: لا قراءةَ
للبوّابة فيها كي لا يرى المالكُ ما ستُقاس عليه.

`--check` يعيد السحبَ ويطابق الأعمدةَ الثابتة وحدَها، فتبقى الأعمدةُ المملوءةُ على حالها؛ ما يُملأ يصير
مرجعًا محجوبًا حين يوقَّع (`owner-reference.json`)، ولا رقمَ عليه قبل ذلك. الأداةُ معفاةٌ في الحارس لأنّها
أداةُ إيداع.
"""

from __future__ import annotations

import csv
import gzip
import hashlib
import io
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HADITH = ROOT / "corpora" / "hadith"
LINES = HADITH / "sahihain-lines.txt.gz"
FRAME = HADITH / "sample-frame.tsv"
SEED = 20261010
SIZE = 500
BUKHARI_LINES = 7008  # صفوفُ البخاريّ تسبق صفوفَ مسلم في السطور (gen_hadith_lines.HADITH_SOURCES)
FIXED = ("id", "book", "line", "pos", "left", "word", "right")
"""الأعمدةُ الثابتة من المدوّنة؛ ما بعدها يملؤه المالك."""
OWNER = ("root", "segmentation", "wasl_vowel", "note")


def _is_marker(w: str) -> bool:
    return w.startswith("<") and w.endswith(">")


def draw() -> list[dict[str, str]]:
    """المواقعُ المعيَّنة ببذرتها: (السطر، الموقع) من كلّ المواقع غير الرموز، بلا تكرار، مرتّبةً
    بالموضع."""

    with gzip.open(LINES, "rb") as f:
        text = f.read().decode("utf-8")
    lines = [ln.split(" ") for ln in text.splitlines()]
    positions = [(i, j) for i, toks in enumerate(lines) for j, t in enumerate(toks)
                 if t and not _is_marker(t)]
    chosen = sorted(random.Random(SEED).sample(positions, SIZE))
    out: list[dict[str, str]] = []
    for n, (i, j) in enumerate(chosen, 1):
        toks = lines[i]
        words = [(k, t) for k, t in enumerate(toks) if t and not _is_marker(t)]
        idx = next(m for m, (k, _) in enumerate(words) if k == j)
        left = words[idx - 1][1] if idx > 0 else ""
        right = words[idx + 1][1] if idx + 1 < len(words) else ""
        out.append({"id": str(n), "book": "bukhari" if i < BUKHARI_LINES else "muslim",
                    "line": str(i + 1), "pos": str(j + 1), "left": left, "word": toks[j],
                    "right": right})
    return out


def render(rows: list[dict[str, str]], filled: dict[str, dict[str, str]] | None = None) -> str:
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=[*FIXED, *OWNER], delimiter="\t", lineterminator="\n")
    w.writeheader()
    for r in rows:
        extra = (filled or {}).get(r["id"], {})
        w.writerow({**r, **{k: extra.get(k, "") for k in OWNER}})
    return buf.getvalue()


def read_frame() -> list[dict[str, str]]:
    with FRAME.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def main(argv: list[str]) -> int:
    rows = draw()
    if "--check" in argv:
        current = read_frame()
        fixed_now = [{k: r[k] for k in FIXED} for r in rows]
        fixed_file = [{k: r.get(k, "") for k in FIXED} for r in current]
        if fixed_now != fixed_file:
            sys.stderr.write("SAMPLE_FRAME_DRIFTED: الأعمدةُ الثابتة لا تطابق السحبَ ببذرته\n")
            return 1
        filled = sum(1 for r in current if any(r.get(k) for k in OWNER))
        sys.stdout.write(f"إطارُ العيّنة مطابق: {len(current)} موقعًا (بذرة {SEED})، "
                         f"مملوءٌ منها {filled}\n")
        return 0
    filled = {r["id"]: r for r in read_frame()} if FRAME.exists() else {}
    blob = render(rows, filled)
    FRAME.write_text(blob, encoding="utf-8")
    sys.stdout.write(f"كُتب {FRAME.name}: {len(rows)} موقعًا، بصمةُ الإطار "
                     f"{hashlib.sha256(blob.encode('utf-8')).hexdigest()}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
