"""إيداعُ الأعلام ولفظِ الجلالة من المودَع الموقَّع `tests/data/owner-alam.json` (بتوقيع المالك):
لفظٌ منفردٌ بلا قياس — لا قالبَ ولا قياسَ عليه. يكتب `formal/Slge/AlamTable.lean`
و`src/slge/alam_table.py` ويفحصهما بـ`--check`؛ ولا يقرأ هذه الأداةَ غيرُ الحارس المعفى.

الصفُّ: (الرسمُ، خاناتُ الاسم بلا حالةِ الآخر، البابُ، الصرفُ). الصرفُ أربعة: ممنوع (جرُّه بالفتح)، منصرف
(بالتنوين)، مقصور (آخرُه ألفٌ لا تُقرأ حالتُه)، غيرُ مشهود الجرّ (لم تُشهد له صورةُ جرّ؛ يُقرأ على الوجهين).
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from slge.cells import ALPHABET

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "tests" / "data" / "owner-alam.json"
LEAN = ROOT / "formal" / "Slge" / "AlamTable.lean"
PY = ROOT / "src" / "slge" / "alam_table.py"
SHA = "09290ebbc0203a407531a74dd528581108f7403931c7bd4dd80a9b0d5fb59a86"
STATES = {"فتح": 0, "كسر": 1, "ضم": 2, "سكون": 3}
SARF = {"ممنوع": 0, "منصرف": 1, "مقصور": 2, "غير مشهود الجرّ": 3}
KIND = {"عربي": 0, "أعجمي": 1}


def _read() -> tuple[str, dict[str, Any]]:
    raw = SRC.read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    if sha != SHA:
        raise SystemExit(f"SOURCE_SHA_MISMATCH {sha}")
    d: dict[str, Any] = json.loads(raw.decode("utf-8"))
    return sha, d


def _lean_cells(cells: list[list[Any]]) -> str:
    return "[" + ", ".join(f"c {ALPHABET.index(k)} {STATES[s]}" for k, s in cells) + "]"


def render_lean(sha: str, d: dict[str, Any]) -> str:
    j = d["jalala"]
    base = j["base"][:-1]
    rows = []
    for it in d["alam"]:
        stem = it["stem"]
        head, last = stem[:-1], stem[-1]
        last_state = STATES[last[1]] if last[1] else 4  # 4 = حالةٌ مفتوحة تُقرأ من الكلمة
        rows.append(f"  ({_lean_cells(head)}, {ALPHABET.index(last[0])}, {last_state}, "
                    f"{KIND[it['kind']]}, {SARF[it['sarf']]})")
    return "\n".join([
        "import Slge.Categories", "",
        "/-! الأعلامُ ولفظُ الجلالة — لفظٌ منفردٌ بلا قياس، من المودَع الموقَّع",
        "`tests/data/owner-alam.json`",
        f"(SHA-256 `{sha}`) بـ`tools/deposit_alam.py`؛ لا يُحرَّر باليد.",
        "الصفُّ: (الخاناتُ قبل الآخر، حاملُ الآخر، حالتُه إن ثبتت وإلّا 4، البابُ 0 عربي/1 أعجمي،",
        "الصرفُ 0 ممنوع/1 منصرف/2 مقصور/3 غيرُ مشهود الجرّ). -/", "",
        "namespace Slge.AlamTable", "", "open Slge.Categories (c)", "",
        "/-- لفظُ الجلالة: لْلَ + الهاء بحالةٍ تُقرأ من الكلمة. -/",
        f"def jalalaHead : List SCell := {_lean_cells(base)}", "",
        f"def jalalaLast : Nat := {ALPHABET.index(j['base'][-1][0])}", "",
        f"def jalalaInitial : List SCell := {_lean_cells(j['initial'])}", "",
        f"def jalalaMadd : List SCell := {_lean_cells(j['madd'])}", "",
        f"def lahumma : List SCell := {_lean_cells(j['lahumma'])}", "",
        "def table : List (List SCell × Nat × Nat × Nat × Nat) := [",
        ",\n".join(rows), "]", "",
        f"theorem table_length : table.length = {len(d['alam'])} := by rfl", "",
        "end Slge.AlamTable", "",
    ])


def render_py(sha: str, d: dict[str, Any]) -> str:
    j = d["jalala"]
    lines = [
        '"""الأعلامُ ولفظُ الجلالة — لفظٌ منفردٌ بلا قياس، من المودَع الموقَّع',
        '`tests/data/owner-alam.json`',
        f'(SHA-256 {sha[:16]}…) بـ`tools/deposit_alam.py`؛ لا يُحرَّر باليد."""', "",
        "from __future__ import annotations", "", "from typing import Final", "",
        "Cell = tuple[str, str]", "",
        f"SIGNED_BY: Final[str] = {d['signed_by']!r}",
        f"JALALA_HEAD: Final[tuple[Cell, ...]] = {tuple((k, s) for k, s in j['base'][:-1])!r}",
        f"JALALA_LAST: Final[str] = {j['base'][-1][0]!r}",
        f"JALALA_CASES: Final[tuple[str, ...]] = {tuple(j['cases'])!r}",
        f"JALALA_INITIAL: Final[tuple[Cell, ...]] = {tuple((k, s) for k, s in j['initial'])!r}",
        f"JALALA_MADD: Final[tuple[Cell, ...]] = {tuple((k, s) for k, s in j['madd'])!r}",
        "LAHUMMA: Final[tuple[Cell, ...]] = (",
        "    " + ", ".join(repr((k, s)) for k, s in j["lahumma"]) + ")", "",
        "Row = tuple[str, tuple[Cell, ...], str, str | None, str, str]",
        '"""(الرسم، الخاناتُ قبل الآخر، حاملُ الآخر، حالتُه إن ثبتت، الباب، الصرف)."""', "",
        "ALAM: Final[tuple[Row, ...]] = (",
    ]
    for it in d["alam"]:
        stem = it["stem"]
        head = ", ".join(repr((k, s)) for k, s in stem[:-1])
        lines.append(f"    ({it['rasm']!r},")
        lines.append(f"     ({head},),")
        lines.append(f"     {stem[-1][0]!r}, {stem[-1][1]!r}, {it['kind']!r}, {it['sarf']!r}),")
    lines += [")", ""]
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    sha, d = _read()
    lean, py = render_lean(sha, d), render_py(sha, d)
    if "--check" in argv:
        ok = LEAN.read_text(encoding="utf-8") == lean and PY.read_text(encoding="utf-8") == py
        sys.stdout.write("جدولا الأعلام مطابقان للموقَّع\n" if ok else "جدولا الأعلام غيرُ مطابقين\n")
        return 0 if ok else 1
    LEAN.write_text(lean, encoding="utf-8")
    PY.write_text(py, encoding="utf-8")
    sys.stdout.write(f"كُتب جدولا الأعلام: {len(d['alam'])} علمًا ولفظُ الجلالة\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
