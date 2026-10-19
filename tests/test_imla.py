"""الإملاءُ بجسر يونيكود (`A116.Imla`، ADR ٨٤): جدولُ Lean وذرّاتُ البوّابة على المصحف كلِّه.

التوقّعاتُ مستقلّةٌ عن Lean وعن شيفرة البوّابة:
١. نقاطُ `Imla.letterCp` أسماؤها في `unicodedata` أسماءُ الحروف المكتوبة هنا باليد بالترتيب.
٢. كلُّ ذرّةٍ في كلّ شهادةٍ جاهزةٍ من المصحف نقطتان: حرفٌ من الجدول وعلامةٌ من الأربع، وأربعةُ بايتات.
٣. **الإملاءُ = الصورةُ القانونيّة بمحو الكرسيّ**: كلُّ كلمةٍ حروفُها من الجدول وعلاماتُها
   الأربع وكراسي الهمزة
   ذرّاتُها هي الكلمةُ بكراسيها همزات؛ وكلُّ كلمةٍ فيها شدّةٌ ذرّاتُها مثلان أوّلُهما ساكن — `imla_radd`.
الطفرات: `MUTANT_CP_SWAP` (ت↔ث في الجدول)، `MUTANT_SEAT_KEPT` (الواوُ المهموزة لا تُمحى).
"""

from __future__ import annotations

import re
import unicodedata
from functools import cache
from pathlib import Path

import gate
import gate.api as api

LEAN = Path(__file__).resolve().parents[1] / "formal" / "a116" / "A116" / "Imla.lean"
NAMES = ["ALEF", "BEH", "TEH", "THEH", "JEEM", "HAH", "KHAH", "DAL", "THAL", "REH", "ZAIN", "SEEN",
         "SHEEN", "SAD", "DAD", "TAH", "ZAH", "AIN", "GHAIN", "FEH", "QAF", "KAF", "LAM", "MEEM",
         "NOON",
         "HEH", "WAW", "YEH", "HAMZA"]
MARKS = "َُِْ"
SHADDA = "ّ"
SEATS = "أإؤئ"


def table() -> list[int]:
    body = re.search(r"def letterCp : List Nat :=\s*\[([^\]]+)\]", LEAN.read_text(encoding="utf-8"))
    assert body
    return [int(x, 16) for x in re.findall(r"0x([0-9A-F]+)", body.group(1))]


def names_ok(cps: list[int]) -> bool:
    return [unicodedata.name(chr(c)) for c in cps] == [f"ARABIC LETTER {n}" for n in NAMES]


@cache
def ready() -> list[tuple[str, tuple[str, ...]]]:
    out = []
    for f in sorted(api.sealed_forms()):
        r = gate.enter(f.encode())
        if isinstance(r, gate.Certificate):
            out.append((f, r.atoms))
    return out


def expand(word: str, seats: str) -> str:
    s = ["ء" if ch in seats else ch for ch in word]
    out: list[str] = []
    i = 0
    while i < len(s):
        if i + 2 < len(s) and s[i + 1] == SHADDA and s[i + 2] in MARKS[:3]:
            out += [s[i], MARKS[3], s[i], s[i + 2]]
            i += 3
        elif i + 2 < len(s) and s[i + 2] == SHADDA and s[i + 1] in MARKS[:3]:
            out += [s[i], MARKS[3], s[i], s[i + 1]]
            i += 3
        else:
            out.append(s[i])
            i += 1
    return "".join(out)


def agreement(seats: str) -> tuple[int, int]:
    letters = {chr(c) for c in table()}
    n = ok = 0
    for f, atoms in ready():
        if all(ch in letters or ch in MARKS or ch in SEATS or ch == SHADDA for ch in f):
            n += 1
            ok += expand(f, seats) == "".join(atoms)
    return n, ok


def test_table_is_unicode_names() -> None:
    assert names_ok(table())


def test_atoms_are_canonical() -> None:
    letters = {chr(c) for c in table()}
    rs = ready()
    assert len(rs) > 17000
    for _f, atoms in rs:
        for a in atoms:
            assert len(a) == 2 and a[0] in letters and a[1] in MARKS and len(a.encode()) == 4


def test_imla_is_canonical_with_seats_erased() -> None:
    n, ok = agreement(SEATS)
    assert n > 11000 and ok == n


def test_mutants_rejected() -> None:
    t = table()
    t[2], t[3] = t[3], t[2]
    assert not names_ok(t)
    n, ok = agreement("أإئ")
    assert ok < n
