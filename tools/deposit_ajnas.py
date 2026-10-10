"""إيداعُ **المعلومات السابقة** الأوّل: الأجناسُ والقابليّاتُ من شجرة المخصّص جدولًا مولَّدًا بنوعه
(المادّة ١٢؛ إذنُ المالك «نفذ وفق أفضل الممارسات SLGE والبرهان»، 2026-10-10؛ ADR ٣٤).

المخصّصُ مختومٌ «وضعًا» (روايةُ الوضع)، وجدولُه `mukhassas_table.NODES` مولَّدٌ منه بـ`deposit_mukhassas.py
--check`. يُشتقّ هنا منه مودَعٌ من النوع الثالث — **معلوماتٌ سابقة** — يستهلكه الحكمُ (`Slge.Hukm`) لا
سُلَّمُ الترخيص: لكلّ كتابٍ (عقدةٌ من المستوى الأوّل، 73) **جنسٌ** جذورُ عنوانه بالرسم، و**قابليّاتُه** كلُّ
جذرٍ في عنوانِ عقدةٍ تحته (المستوى الثاني فأعلى) مع **شاهده** أوّلَ عقدةٍ تحمله — فالقابليّةُ لا تُسجَّل إلّا
بعقدةٍ من الشجرة تشهد لها، ولا تُسجَّل جذورُ الكتاب نفسِه قابليّاتٍ (هي اسمُ الجنس). الشجرةُ منقولةٌ بلا
إعادة تصنيف.

يكتب `tests/data/ajnas-qabiliyyat.json.gz` (المودَع، ببصمته في `manifest.DEPOSITS`)
و`formal/Slge/AjnasTable.lean` و`src/slge/ajnas_table.py`؛ وبـ`--check` يقارن الثلاثةَ بما يولَّد الآن.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import sys
from pathlib import Path

from slge.mukhassas_table import NODES

ROOT = Path(__file__).resolve().parent.parent
DEPOSIT = ROOT / "tests" / "data" / "ajnas-qabiliyyat.json.gz"
LEAN = ROOT / "formal" / "Slge" / "AjnasTable.lean"
PY = ROOT / "src" / "slge" / "ajnas_table.py"
SOURCE = "openiti-mukhassas.txt.gz"
SOURCE_SHA = "8d8134c2bce16b70b07bddf974fa5e9c0f7cd80129d8452baf55cd87006b80ac"
KIND = "معلومات سابقة"

Genus = tuple[int, str, tuple[int, ...], tuple[tuple[int, int], ...]]
"""(الكتاب، عنوانه، جذورُ الجنس، القابليّاتُ (الجذر، العقدةُ الشاهدة) مرتّبةً بالجذر)."""


def genera() -> list[Genus]:
    out: list[Genus] = []
    for b, level, _, title, roots, _ in NODES:
        if level != 1:
            continue
        caps: dict[int, int] = {}
        for n, lv, _, _, rs, book in NODES:
            if book != b or lv < 2:
                continue
            for r in rs:
                caps.setdefault(r, n)
        out.append((b, title, tuple(roots), tuple(sorted(caps.items()))))
    return out


def verify(gs: list[Genus]) -> None:
    """الأجناسُ هي عقدُ المستوى الأوّل كلُّها بترتيبها؛ كلُّ شاهدٍ عقدةٌ في الكتاب نفسِه من مستوًى ثانٍ فأعلى
    يحمل عنوانُها الجذر؛ ولا جذرَ مكرَّرًا في قابليّات الجنس."""

    if [g[0] for g in gs] != [n[0] for n in NODES if n[1] == 1]:
        raise SystemExit("GENERA_ARE_NOT_THE_BOOKS")
    for b, _, _, caps in gs:
        if len({r for r, _ in caps}) != len(caps):
            raise SystemExit(f"CAP_REPEATED:{b}")
        for r, w in caps:
            n = NODES[w]
            if n[0] != w or n[5] != b or n[1] < 2 or r not in n[4]:
                raise SystemExit(f"CAP_WITHOUT_WITNESS:{b}:{r}:{w}")


def render_json(gs: list[Genus]) -> bytes:
    """المودَعُ بصورته القانونيّة (مفاتيحُ مرتّبة بلا فراغ) قبل الضغط؛ البصمةُ عليها لا على الضغط، لأنّ
    بايتاتِ gzip تختلف باختلاف zlib."""

    doc = {"version": 1, "kind": KIND, "source": SOURCE, "source_sha256": SOURCE_SHA,
           "note": "الأجناسُ والقابليّاتُ من شجرة المخصّص بشاهدها؛ لا نصَّ يُقرأ هنا",
           "genera": [{"book": b, "title": t, "roots": list(rs), "caps": [list(c) for c in caps]}
                      for b, t, rs, caps in gs]}
    blob = json.dumps(doc, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return blob.encode("utf-8")


def render_lean(gs: list[Genus], sha: str) -> str:
    out = [
        "import Slge.Bridge", "",
        "/-! الأجناسُ والقابليّاتُ من شجرة المخصّص — مودَعُ **المعلومات السابقة** الأوّل",
        f"(`tests/data/ajnas-qabiliyyat.json.gz`، SHA-256 `{sha}`)؛",
        "مولَّدٌ بـ`tools/deposit_ajnas.py`",
        f"من `MukhassasTable` (المختومُ `{SOURCE}` `{SOURCE_SHA}`)، لا يُحرَّر باليد.",
        "الجنسُ: (الكتاب، جذورُ عنوانه، القابليّاتُ (الجذر، العقدةُ الشاهدة)). -/", "",
        "namespace Slge.AjnasTable", "",
        "structure Genus where",
        "  book : Nat",
        "  roots : List Nat",
        "  caps : List (Nat × Nat)",
        "  deriving DecidableEq, Repr", "",
        "set_option maxRecDepth 100000 in",
        "def genera : List Genus := [",
    ]
    rows = []
    for b, _, rs, caps in gs:
        r = "[" + ", ".join(str(x) for x in rs) + "]"
        c = "[" + ", ".join(f"({x}, {w})" for x, w in caps) + "]"
        rows.append(f"  ⟨{b}, {r}, {c}⟩")
    out += [",\n".join(rows), "]", "",
            f"theorem genera_length : genera.length = {len(gs)} := by rfl", "",
            "end Slge.AjnasTable", ""]
    return "\n".join(out)


def render_py(gs: list[Genus], sha: str) -> str:
    out = [
        '"""الأجناسُ والقابليّاتُ من شجرة المخصّص — مودَعُ المعلومات السابقة الأوّل',
        f"(`tests/data/ajnas-qabiliyyat.json.gz`، SHA-256 {sha[:16]}…)؛",
        "مولَّدٌ بـ`tools/deposit_ajnas.py`",
        'من جدول المخصّص؛ لا يُحرَّر باليد."""', "",
        "from __future__ import annotations", "", "from typing import Final", "",
        f"KIND: Final[str] = {KIND!r}",
        f"SOURCE: Final[str] = {SOURCE!r}",
        "Genus = tuple[int, str, tuple[int, ...], tuple[tuple[int, int], ...]]",
        '"""(الكتاب، عنوانه، جذورُ الجنس، القابليّاتُ (الجذر، العقدةُ الشاهدة))."""', "",
        "GENERA: Final[tuple[Genus, ...]] = (",
    ]
    for b, t, rs, caps in gs:
        out.append(f"    ({b}, {t!r},")
        out.append(f"     {rs!r},")
        out.append("     (")
        for i in range(0, len(caps), 6):
            out.append("         " + " ".join(f"{c!r}," for c in caps[i:i + 6]))
        out.append("     )),")
    out += [")", ""]
    return "\n".join(out)


def main(argv: list[str]) -> int:
    gs = genera()
    verify(gs)
    blob = render_json(gs)
    sha = hashlib.sha256(blob).hexdigest()
    lean, py = render_lean(gs, sha), render_py(gs, sha)
    if "--check" in argv:
        ok = (gzip.decompress(DEPOSIT.read_bytes()) == blob
              and LEAN.read_text(encoding="utf-8") == lean and PY.read_text(encoding="utf-8") == py)
        sys.stdout.write("مودَعُ الأجناس والقابليّات وجدولاه مطابقة للمخصّص\n" if ok
                         else "مودَعُ الأجناس غيرُ مطابق\n")
        return 0 if ok else 1
    DEPOSIT.write_bytes(gzip.compress(blob, mtime=0))
    LEAN.write_text(lean, encoding="utf-8")
    PY.write_text(py, encoding="utf-8")
    caps = sum(len(g[3]) for g in gs)
    sys.stdout.write(f"كُتب مودَعُ الأجناس: {len(gs)} جنسًا، {caps} قابليّةً بشاهدها؛ SHA-256 {sha}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
