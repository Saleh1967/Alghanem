"""عيّنةُ الأحكام المحجوبة — إطارٌ من المصحف يملؤه المالكُ بيده فيصير مرجعَ الأحكام (ADR ٩، 2026-10-10).

لا مرجعَ بشريًّا للحكم على مطابقة الجذر لجنسه وقابليّاته (المادّة ١٢: «المعلوماتُ السابقة لا تُقاس إلّا على
مرجع أحكامٍ محجوب»). فالمرجعُ يُصنع لا يُنسخ: هذه الأداةُ تسحب من المدوّنة المختومة (`CORPUS`) عيّنةَ مواقع
ببذرةٍ معلَنة (`SEED`) وحجمٍ معلَن (`SIZE`) — موقعًا موقعًا بسطره (الآية) وجاريه — وتكتب
`corpora/hukm-sample-frame.tsv` بأعمدةٍ ثابتةٍ من المدوّنة وأعمدةٍ **فارغة** يملؤها المالك: الجذرُ (حروفُه
مفصولةً بمسافة)، الجنسُ (عنوانُ الكتاب في المخصّص بلفظه أو «-»)، القابليّةُ (عنوانُ العقدة بلفظه أو «-»)،
وملاحظة. العيّنةُ عمياء: لا حكمَ للسُّلَّم فيها كي لا يرى المالكُ ما ستُقاس عليه.

المرجعُ يُقاس عليه في SLGE (`tools/gen_hukm_index.py`، المودَعُ `tests/data/hukm-reference.tsv` من نوع
«مرجع محجوب»)، ولا رقمَ عليه قبل الملء. `--check` يعيد السحبَ ويطابق الأعمدةَ الثابتة وحدَها فتبقى
المملوءةُ على حالها. الأداةُ معفاةٌ في الحارس لأنّها أداةُ إيداع.
"""

from __future__ import annotations

import csv
import hashlib
import io
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORPUS = ROOT / "corpora" / "quran-simple-enhanced.txt"
FRAME = ROOT / "corpora" / "hukm-sample-frame.tsv"
SEED = 20261010
SIZE = 300
FIXED = ("id", "line", "pos", "left", "word", "right")
"""الأعمدةُ الثابتة من المدوّنة؛ ما بعدها يملؤه المالك."""
OWNER = ("root", "jins", "qabiliyya", "note")


def draw() -> list[dict[str, str]]:
    """المواقعُ المعيَّنة ببذرتها: (السطر، الموقع) من كلّ مواقع المصحف، بلا تكرار، مرتّبةً بالموضع."""

    lines = [ln.split(" ") for ln in CORPUS.read_text(encoding="utf-8").splitlines()]
    positions = [(i, j) for i, toks in enumerate(lines) for j, t in enumerate(toks) if t]
    chosen = sorted(random.Random(SEED).sample(positions, SIZE))
    out: list[dict[str, str]] = []
    for n, (i, j) in enumerate(chosen, 1):
        toks = lines[i]
        out.append({"id": str(n), "line": str(i + 1), "pos": str(j + 1),
                    "left": toks[j - 1] if j > 0 else "", "word": toks[j],
                    "right": toks[j + 1] if j + 1 < len(toks) else ""})
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
        sys.stdout.write(f"إطارُ عيّنة الأحكام مطابق: {len(current)} موقعًا (بذرة {SEED})، "
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
