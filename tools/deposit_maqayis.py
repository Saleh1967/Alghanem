"""إيداعُ جذور مقاييس اللغة حواملَ (خاناتٍ بلا حالة) في SLGE من المصدر المختوم.

`python tools/deposit_maqayis.py <maqayis_by_root_csv_999.csv>` يكتب ثلاثةً معًا من مصدرٍ واحد:
`tests/data/maqayis-roots.json.gz` (المودَع)، `formal/Slge/MaqayisTable.lean` (جدولُ Lean مقطَّعًا لحدّ
التعمّق)، `src/slge/maqayis_table.py` (المرآة). المصدرُ يُرفض إن خالف بصمتَه. وبـ`--check` يقارن
الثلاثةَ بالمودَع نفسه (لا يحتاج المصدر): الجدولان مولَّدان من المودَع لا يُحرَّران باليد.
التعيين: أ/ئ/ء → همزة (0)؛ ى وا في موضع أصلٍ → 29 (عينٌ أو لامٌ معتلّة: واوٌ أو ياء، مجهولةُ العين)؛
الرمزُ a·900 + b·30 + c. الرباعيُّ يُسقط باسمه.
"""

from __future__ import annotations

import csv
import gzip
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
DEPOSIT = ROOT / "tests" / "data" / "maqayis-roots.json.gz"
LEAN = ROOT / "formal" / "Slge" / "MaqayisTable.lean"
PY = ROOT / "src" / "slge" / "maqayis_table.py"
SHA = "2c6000bd47797e183294b89da77df4ddfd27921ea595c6071ba52299c382ccb0"
ALPHABET = "ءابتثجحخدذرزسشصضطظعغفقكلمنهوي"
WEAK = 29
CHUNK = 400


def carrier(ch: str) -> int:
    if ch in "أئء":
        return 0
    if ch in "ىا":
        return WEAK
    return ALPHABET.index(ch)


def deposit(src: Path) -> dict[str, Any]:
    raw = src.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    if sha != SHA:
        raise SystemExit(f"SOURCE_SHA_MISMATCH {sha}")
    rows = list(csv.DictReader(raw.decode("utf-8").splitlines()))
    roots = sorted({r["root_full"] for r in rows})
    tri = [r for r in roots if len(r) == 3]
    codes = sorted({carrier(r[0]) * 900 + carrier(r[1]) * 30 + carrier(r[2]) for r in tri})
    return {"source": src.name, "sha256": sha, "rows": len(rows), "distinct_roots": len(roots),
            "triliteral": len(tri), "skipped_quadriliteral": [r for r in roots if len(r) != 3],
            "alphabet": ALPHABET, "weak_code": WEAK,
            "mapping": "أ/ئ/ء→ء(0)؛ ى وا في موضع أصلٍ→29 (و أو ي، مجهولةُ العين)؛ "
                       "code = a*900+b*30+c",
            "codes": codes}


def render_lean(dep: dict[str, Any]) -> str:
    codes: list[int] = dep["codes"]
    chunks = [codes[i:i + CHUNK] for i in range(0, len(codes), CHUNK)]
    lines = [
        "import Slge.Bridge", "",
        "/-! جدولُ جذور مقاييس اللغة (ابن فارس) حواملَ: مولَّدٌ من `maqayis_by_root_csv_999.csv`",
        f"(SHA-256 `{dep['sha256']}`)؛ لا يُحرَّر باليد. الرمزُ ‎a·900 + b·30 + c‎ على 29 حاملًا "
        "و29 = عينٌ/لامٌ معتلّة",
        "(ا/ى في الطبعة: واوٌ أو ياء). الهمزةُ بصورها (أ ئ ء) حاملُ الهمزة. القطعُ أجزاءً لحدّ "
        "التعمّق في المحرّر. -/",
        "", "namespace Slge.Maqayis", "",
    ]
    for j, ch in enumerate(chunks):
        lines.append(f"def t{j} : List Nat := [")
        for i in range(0, len(ch), 12):
            tail = "," if i + 12 < len(ch) else ""
            lines.append("  " + ", ".join(str(c) for c in ch[i:i + 12]) + tail)
        lines += ["]", ""]
    lines += [f"/-- {len(codes)} جذرًا ثلاثيًّا (الرباعيُّ المكرَّر الثلاثةُ غيرُ مودَعة). -/",
              "def table : List Nat := " + " ++ ".join(f"t{j}" for j in range(len(chunks))),
              "", "/-- عددُ الجدول بعينه — القطعُ لم يُسقط رمزًا. -/",
              f"theorem table_length : table.length = {len(codes)} := by decide +kernel",
              "", "end Slge.Maqayis", ""]
    return "\n".join(lines)


def render_py(dep: dict[str, Any]) -> str:
    codes: list[int] = dep["codes"]
    lines = [
        '"""جدولُ جذور مقاييس اللغة حواملَ — مولَّدٌ من المودَع `tests/data/maqayis-roots.json.gz`؛ '
        "لا يُحرَّر باليد.",
        "المصدرُ `maqayis_by_root_csv_999.csv`، الرمزُ a*900+b*30+c، و29 عينٌ/لامٌ معتلّة.",
        f'SHA-256 {dep["sha256"]}."""',
        "", "from __future__ import annotations", "", "from typing import Final", "",
        f'SHA256: Final = "{dep["sha256"]}"', f"WEAK: Final = {WEAK}",
        "ROOTS: Final[tuple[int, ...]] = (",
    ]
    for i in range(0, len(codes), 12):
        lines.append("    " + ", ".join(str(c) for c in codes[i:i + 12]) + ",")
    lines += [")", ""]
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    if "--check" in argv:
        with gzip.open(DEPOSIT, "rt", encoding="utf-8") as f:
            dep = json.load(f)
        ok = (LEAN.read_text(encoding="utf-8") == render_lean(dep)
              and PY.read_text(encoding="utf-8") == render_py(dep))
        sys.stdout.write("جدولا المقاييس مطابقان للمودَع\n" if ok else "غيرُ مطابقين للمودَع\n")
        return 0 if ok else 1
    if len(argv) != 1:
        sys.stderr.write("الاستعمال: deposit_maqayis.py <csv> | --check\n")
        return 2
    dep = deposit(Path(argv[0]))
    with gzip.open(DEPOSIT, "wt", encoding="utf-8") as f:
        json.dump(dep, f, ensure_ascii=False)
    LEAN.write_text(render_lean(dep), encoding="utf-8")
    PY.write_text(render_py(dep), encoding="utf-8")
    n = len(dep["codes"])
    sys.stdout.write(f"{dep['rows']} صفًّا، {dep['distinct_roots']} جذرًا، {n} رمزًا\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
