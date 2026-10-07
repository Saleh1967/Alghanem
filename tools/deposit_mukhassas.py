"""إيداعُ شجرة المخصّص لابن سيده **كما هي** وربطُ عناوينها بجذور المقاييس **بالرسم**:
المعلوماتُ السابقة
(الأجناسُ والقابليّات) جدولًا مولَّدًا من المختوم `tests/data/openiti-mukhassas.txt.gz` (وضع،
CC BY-NC-SA 4.0).

القاعدةُ المعلَنة (لا تخمين):
- **العقدة**: كلُّ سطرِ عنوانٍ في نسخة OpenITI (`# | <1|2|3> …`) عقدةٌ بمستواها؛ العنوانُ بحروفه بعد إزالة
  علامات الصفحات (`msNNNN`) وقوسَي OpenITI ورقمِ المستوى الذيليّ. الأبُ آخرُ عقدةٍ سابقة أدنى مستوًى
  (مستوى 1 لا أبَ له). لا إعادةَ تصنيفٍ ولا دمج: ما سمّاه المصدرُ كتابًا أو بابًا أو فصلًا
يبقى، وما شذّ من
  ترقيمه (كتبٌ نحويّةٌ على مستوى 1، علاماتُ الأسفار) يبقى باسمه.
- **الربطُ بالرسم**: كلماتُ العنوان بعد حذف السوابق (وال/بال/فال/كال/لل/ال/و) واللواحق
  (ات/ين/ون/ة)؛ ما بقي
  ثلاثةَ حروف، أو أربعةً فيها ألفٌ غيرُ أولى فتُحذف (فَعَال/فَاعِل)، فهو مرشَّحُ جذر؛ الألفُ والواوُ والياءُ معتلّة؛
  يُقبل إن كان في جدول المقاييس (`Maqayis.member` على الخانات) وإلّا «لا ربط». الرابطُ رسمٌ لا ترخيص
  (النصُّ غيرُ مشكول) — وسمُه «مطابَق بالرسم».

يكتب `formal/Slge/MukhassasTable.lean` (العقد: معرّف، مستوى، أب؛ والقابليّات: معرّف، رموزُ جذورٍ بترميز
جدول المقاييس) و`src/slge/mukhassas_table.py` (ومعهما العناوينُ بحروفها)؛ بـ`--check` يقارنهما بما
يولَّد الآن.
"""

from __future__ import annotations

import gzip
import hashlib
import re
import sys
from pathlib import Path
from typing import Any

from slge.cells import ALPHABET
from slge.maqayis import WEAK, decode, member
from slge.maqayis_table import ROOTS

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "tests" / "data" / "openiti-mukhassas.txt.gz"
LEAN = ROOT / "formal" / "Slge" / "MukhassasTable.lean"
PY = ROOT / "src" / "slge" / "mukhassas_table.py"
SHA = "8d8134c2bce16b70b07bddf974fa5e9c0f7cd80129d8452baf55cd87006b80ac"
HEAD = re.compile(r"^# \| ([123])\s*(.*?)\s*$")
PREFIXES = ("وال", "بال", "فال", "كال", "لل", "ال", "و")
STOP = frozenset({"كتاب", "الكتاب", "باب", "أبواب", "فصل", "هذا", "ذكر", "أسماء", "تسمية", "تسميتك",
                  "السفر", "المخصص", "من", "ما", "إلى", "في", "على", "عن", "وما", "مما", "ومن",
"ومما",
                  "ونحوه", "ونحوها", "وغيره", "وغيرها", "نعوت", "صفات", "ذكرك"})
"""ألفاظُ هيكل المصدر (كتاب/باب/فصل/ذكر/أسماء/تسمية…) لا تُربط جذورًا: قاعدةٌ معلَنة."""
SUFFIXES = ("ات", "ين", "ون", "ة")
_CODES = frozenset(decode(n) for n in ROOTS)


def _title(level: int, raw: str) -> str:
    t = re.sub(r"\bms\d+\b", " ", raw)
    t = re.sub(r"\s*\)\s*" + str(level) + r"\s*$", "", t).strip()
    if t.startswith("("):
        t = t[1:].strip()
    if t.endswith(")"):
        t = t[:-1].strip()
    return re.sub(r"\s+", " ", t).strip(" .:،")


def root_of_word(w: str) -> tuple[int, int, int] | None:
    """مرشَّحُ جذرٍ من رسم كلمةٍ غير مشكولة، أو لا شيء."""

    for p in PREFIXES:
        if w.startswith(p) and len(w) - len(p) >= 3:
            w = w[len(p):]
            break
    for s in SUFFIXES:
        if w.endswith(s) and len(w) - len(s) >= 3:
            w = w[: -len(s)]
            break
    if len(w) == 4 and "ا" in w[1:]:
        i = w.index("ا", 1)
        w = w[:i] + w[i + 1:]
    if len(w) != 3 or any(ch not in ALPHABET for ch in w):
        return None
    w = w.replace("ا", "و")
    if member((w[0], w[1], w[2])):
        return tuple(ALPHABET.index(ch) for ch in w)  # type: ignore[return-value]
    return None


def _code(r: tuple[int, int, int]) -> int:
    """رمزُ جدول المقاييس (900a + 30b + c) بعد ردّ المعتلّ إلى 29 كما في الجدول."""

    def k(x: int) -> int:
        return WEAK if x in (27, 28) else x
    cands = [c for c in _CODES if all(t == k(x) or (t == WEAK and x in (27, 28)) or t == x
                                       for t, x in zip(c, r, strict=True))]
    a, b, d = cands[0] if cands else (k(r[0]), k(r[1]), k(r[2]))
    return a * 900 + b * 30 + d


def nodes() -> tuple[str, list[dict[str, Any]]]:
    raw = gzip.decompress(SRC.read_bytes())
    sha = hashlib.sha256(raw).hexdigest()
    if sha != SHA:
        raise SystemExit(f"SOURCE_SHA_MISMATCH {sha}")
    body = raw.decode("utf-8").split("#META#Header#End#", 1)[1]
    out: list[dict[str, Any]] = []
    stack: list[tuple[int, int]] = []  # (level, id)
    for line in body.split("\n"):
        m = HEAD.match(line)
        if not m:
            continue
        level = int(m.group(1))
        title = _title(level, m.group(2))
        while stack and stack[-1][0] >= level:
            stack.pop()
        parent = stack[-1][1] if stack else -1
        if level > 1 and parent == -1:
            parent = 0  # عنوانٌ أدنى بلا أبٍ أعلى قبله: يُعلَّق على العقدة 0 (المقدّمة) باسمه
        nid = len(out)
        roots: list[int] = []
        for w in title.split():
            if w in STOP:
                continue
            r = root_of_word(w)
            if r is not None:
                c = _code(r)
                if c not in roots:
                    roots.append(c)
        book = nid if parent == -1 else int(out[parent]["book"])
        out.append({"id": nid, "level": level, "parent": parent, "title": title, "roots": roots,
                    "book": book})
        stack.append((level, nid))
    return sha, out


def books(ns: list[dict[str, Any]]) -> list[tuple[int, list[int]]]:
    """لكلّ عقدةٍ من المستوى الأوّل: اتّحادُ جذور عناوينها وعناوين ما تحتها (القابليّاتُ
الموروثة)."""

    out: dict[int, list[int]] = {}
    for n in ns:
        b = int(n["book"])
        acc = out.setdefault(b, [])
        for c in n["roots"]:
            if c not in acc:
                acc.append(c)
    return sorted(out.items())


def _chunked(name: str, typ: str, items: list[str], size: int, per_line: int) -> list[str]:
    """تعريفٌ مقطَّعًا: `name0 … nameK` ثمّ `name := name0 ++ …` — تجنّبًا لعمق الاستدعاء على
القوائم الكبيرة."""

    out: list[str] = []
    parts = [items[i:i + size] for i in range(0, len(items), size)]
    for k, part in enumerate(parts):
        out += ["set_option maxRecDepth 100000 in", f"def {name}{k} : {typ} := ["]
        for i in range(0, len(part), per_line):
            tail = "," if i + per_line < len(part) else ""
            out.append("  " + ", ".join(part[i:i + per_line]) + tail)
        out += ["]", ""]
    out += ["set_option maxRecDepth 100000 in",
            f"def {name} : {typ} := " + " ++ ".join(f"{name}{k}" for k in range(len(parts))), ""]
    return out


def render_lean(sha: str, ns: list[dict[str, Any]]) -> str:
    lines = [
        "import Slge.Bridge", "",
        "/-! شجرةُ المخصّص لابن سيده كما هي، وقابليّاتُ عناوينها جذورًا بالرسم: مولَّدٌ من المختوم",
        f"`tests/data/openiti-mukhassas.txt.gz` (SHA-256 `{sha}`) بـ`tools/deposit_mukhassas.py`؛",
        "لا يُحرَّر باليد. العقدةُ (معرّف، مستوى، أب، كتاب، جذورُ عنوانها بالرسم بترميز جدول المقاييس",
        "900a+30b+c والمعتلّ 29)؛ الأبُ -1 للمستوى الأوّل والكتابُ جذرُ سلسلة الآباء. -/", "",
        "namespace Slge.Mukhassas", "",
        f"/-! {len(ns)} عقدةً بترتيب المصدر. -/",
    ]
    rows = [f"({n['id']}, {n['level']}, {n['parent']}, {n['book']}, "
            f"[{', '.join(str(c) for c in n['roots'])}])" for n in ns]
    lines += _chunked("nodes", "List (Nat × Nat × Int × Nat × List Nat)", rows, 200, 3)
    lines += ["set_option maxRecDepth 100000 in",
              f"theorem nodes_length : nodes.length = {len(ns)} := by rfl", "",
              "end Slge.Mukhassas", ""]
    return "\n".join(lines)


def render_py(sha: str, ns: list[dict[str, Any]]) -> str:
    lines = [
        '"""شجرةُ المخصّص كما هي وقابليّاتُ عناوينها بالرسم — مولَّدٌ من المختوم',
        f'`tests/data/openiti-mukhassas.txt.gz` (SHA-256 {sha[:16]}…)',
        'بـ`tools/deposit_mukhassas.py`؛',
        'لا يُحرَّر باليد."""', "", "from __future__ import annotations", "",
        "from typing import Final", "",
        "NODES: Final[tuple[tuple[int, int, int, str, tuple[int, ...], int], ...]] = (",
    ]
    for n in ns:
        roots = ", ".join(str(c) for c in n["roots"])
        title = str(n["title"]).replace("\\", "\\\\").replace('"', '\\"')
        tup = f'({roots}{"," if roots else ""})'
        row = f'    ({n["id"]}, {n["level"]}, {n["parent"]}, "{title}", {tup}, {n["book"]}),'
        if len(row) > 100:  # عنوانٌ طويل: يُقسَّم سطرَين (سلسلةٌ متجاورة)
            row = (f'    ({n["id"]}, {n["level"]}, {n["parent"]},\n     "{title}",\n'
                   f'     ({roots}{"," if roots else ""}), {n["book"]}),')
        lines.append(row)
    lines += [")", "", "BOOKS: Final[dict[int, tuple[int, ...]]] = {"]
    for b, rs in books(ns):
        items = [str(c) for c in rs]
        lines.append(f"    {b}: (")
        for i in range(0, len(items), 12):
            lines.append("        " + ", ".join(items[i:i + 12]) + ",")
        lines.append("    ),")
    lines += ["}", ""]
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    sha, ns = nodes()
    lean, py = render_lean(sha, ns), render_py(sha, ns)
    if "--check" in argv:
        ok = LEAN.read_text(encoding="utf-8") == lean and PY.read_text(encoding="utf-8") == py
        sys.stdout.write("جدولا المخصّص مطابقان للمختوم\n" if ok else "جدولا المخصّص غيرُ مطابقين\n")
        return 0 if ok else 1
    LEAN.write_text(lean, encoding="utf-8")
    PY.write_text(py, encoding="utf-8")
    by = {lv: sum(1 for n in ns if n["level"] == lv) for lv in (1, 2, 3)}
    linked = sum(1 for n in ns if n["roots"])
    sys.stdout.write(f"{len(ns)} عقدة {by}؛ مربوطٌ بالرسم {linked}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
