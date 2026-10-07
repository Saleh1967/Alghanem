"""إيداعُ أبنية سيبويه هياكلَ حواملَ في SLGE من المصدر المختوم `tests/data/sibawayh-abniya.tsv`.

`python tools/deposit_abniya.py` يكتب من المصدر (749 صفًّا، 158 هيكلًا) جدولَ Lean
`formal/Slge/AbniyaTable.lean` والمرآةَ `src/slge/abniya_table.py`؛ وبـ`--check` يقارنهما بما يولَّد
الآن. الهيكلُ حروفٌ بلا حركات: ف ع ل أصولٌ، وما سواها زوائدُ بحواملها (ء ا ت س ن م و ي ه)؛ الرمزُ
فهرسُ الحامل في الأبجديّة. التاءُ المربوطة ليست في الهياكل (اصطلاحُ المصدر)، فهياكلُ الجدول تُسقط
التاءَ الأخيرة.
"""

from __future__ import annotations

import csv
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "tests" / "data" / "sibawayh-abniya.tsv"
LEAN = ROOT / "formal" / "Slge" / "AbniyaTable.lean"
PY = ROOT / "src" / "slge" / "abniya_table.py"
SHA = "678ca5144698b571a42804b19b8d1680766df7f2339cf6c9c53d84994051fdd9"
ALPHABET = "ءابتثجحخدذرزسشصضطظعغفقكلمنهوي"


def skeletons() -> tuple[str, list[tuple[int, ...]], dict[str, int]]:
    raw = SRC.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    if sha != SHA:
        raise SystemExit(f"SOURCE_SHA_MISMATCH {sha}")
    rows = list(csv.DictReader(raw.decode("utf-8").splitlines(), delimiter="\t"))
    codes = sorted({tuple(ALPHABET.index(ch) for ch in r["skeleton"]) for r in rows})
    tiers: dict[str, int] = {}
    for r in rows:
        tiers[r["tier"]] = tiers.get(r["tier"], 0) + 1
    return sha, codes, {"rows": len(rows), **tiers}


def render_lean(sha: str, codes: list[tuple[int, ...]], meta: dict[str, int]) -> str:
    lines = [
        "import Slge.Bridge", "",
        "/-! أبنيةُ سيبويه هياكلَ حواملَ: مولَّدٌ من `tests/data/sibawayh-abniya.tsv`",
        f"(SHA-256 `{sha}`؛ {meta['rows']} صفًّا: اسمٌ {meta['N']}، فعلٌ {meta['V']}، "
        f"جزئيّ {meta['P']})؛ لا يُحرَّر باليد.",
        "الهيكلُ حروفٌ بلا حركات: ف(20) ع(18) ل(23) أصولٌ وما سواها زوائدُ بحواملها. -/",
        "", "namespace Slge.Abniya", "",
        f"/-- {len(codes)} هيكلًا متمايزًا. -/",
        "def abniya : List (List Nat) := [",
    ]
    for i, c in enumerate(codes):
        tail = "," if i + 1 < len(codes) else ""
        lines.append("  [" + ", ".join(str(x) for x in c) + "]" + tail)
    lines += ["]", "", f"theorem abniya_length : abniya.length = {len(codes)} := by rfl", "",
              "end Slge.Abniya", ""]
    return "\n".join(lines)


def render_py(sha: str, codes: list[tuple[int, ...]], meta: dict[str, int]) -> str:
    lines = [
        '"""أبنيةُ سيبويه هياكلَ حواملَ — مولَّدٌ من المودَع `tests/data/sibawayh-abniya.tsv`؛ '
        "لا يُحرَّر باليد.",
        f"{meta['rows']} صفًّا (اسمٌ {meta['N']}، فعلٌ {meta['V']}، جزئيّ {meta['P']})، "
        f"{len(codes)} هيكلًا؛ الرمزُ فهرسُ الحامل في الأبجديّة.",
        f'SHA-256 {sha}."""',
        "", "from __future__ import annotations", "", "from typing import Final", "",
        f'SHA256: Final = "{sha}"',
        "SKELETONS: Final[tuple[tuple[int, ...], ...]] = (",
    ]
    lines += ["    (" + ", ".join(str(x) for x in c) + ")," for c in codes]
    lines += [")", ""]
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    sha, codes, meta = skeletons()
    lean, py = render_lean(sha, codes, meta), render_py(sha, codes, meta)
    if "--check" in argv:
        ok = LEAN.read_text(encoding="utf-8") == lean and PY.read_text(encoding="utf-8") == py
        sys.stdout.write("جدولا الأبنية مطابقان للمودَع\n" if ok else "جدولا الأبنية غيرُ مطابقين\n")
        return 0 if ok else 1
    LEAN.write_text(lean, encoding="utf-8")
    PY.write_text(py, encoding="utf-8")
    sys.stdout.write(f"{meta['rows']} صفًّا، {len(codes)} هيكلًا\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
