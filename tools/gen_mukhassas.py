"""المجالُ المعلَنُ السادس — «المخصَّص» لابن سيده مرجعًا محجوبًا للجنس والقابليّة (ADR ٤٨، قرارُ
المالك).

**الواقع.** نصُّ OpenITI `0458IbnSidaMursi.Mukhassas.Shamela0003590-ara1` (CC BY-NC-SA 4.0،
للقياس وحدَه)، منسوخًا بعينه إلى `corpora/mukhassas/` وبصمتُه `MUKHASSAS_SHA256` — الختم.
عناوينُه مرقومةٌ في الطبعة (`### |` و`### $`)، فالشجرةُ من رقم المحرّر لا من تقطيعي.

**العُقَد** (`nodes` → `corpora/mukhassas/nodes.tsv`): كلُّ سطر عنوانٍ يبدأ عقدةً تمتدّ إلى
العنوان التالي؛ ونصُّ العنوان بلفظه بعد نزع الرقم (`$ 3 -`) والقوسين. و**الكتاب** (الجنس) آخرُ
عنوانٍ قبلها يبدأ نصُّه بـ«كتاب »، أو العنوانُ المسمّى `BOOK_HEADING_MISTYPED` («الكتاب الغنم»
مرقومٌ `$` في الطبعة)؛ وما قبل أوّل كتاب «-».

**العضويّة** (`RULE_M` → `corpora/mukhassas/membership.tsv`): الجذرُ R في العقدة N إن ورد في
نصّها لفظٌ هيكلُه في معجم هياكل ابن فارس (`corpora/hadith/maqayis-skeletons.tsv`، ADR ٤٧) بجذرٍ
واحدٍ هو R. فهو حكمُ ابن سيده (الموضع) وحكمُ ابن فارس (الجذر) معًا، بقاعدةٍ معلنة لا تمرّ
بالبوّابة.

`--check` يُسقط البناءَ بأسمائها: `MUKHASSAS_SOURCE_DRIFTED`، `MUKHASSAS_NODES_DRIFTED`،
`MUKHASSAS_MEMBERSHIP_DRIFTED`. الأداةُ معفاةٌ في الحارس لأنّها أداةُ إيداع.
"""

from __future__ import annotations

import gzip
import hashlib
import io
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "corpora" / "mukhassas" / "0458IbnSidaMursi.Mukhassas.Shamela0003590-ara1.gz"
MUKHASSAS_SHA256 = "936c68e0c2c62ddbfb881c573487c7b37650ef69117bca364c219b6d1bf8e76c"
SKELETONS = ROOT / "corpora" / "hadith" / "maqayis-skeletons.tsv"
NODES = ROOT / "corpora" / "mukhassas" / "nodes.tsv"
MEMBERSHIP = ROOT / "corpora" / "mukhassas" / "membership.tsv"

HEADING = re.compile(r"^### ([|$]+)\s*(.*)$")
NUMBER = re.compile(r"^\d+\s*-\s*")
MISTYPED_BOOKS = frozenset({"الكتاب الغنم"})
"""`BOOK_HEADING_MISTYPED`: عنوانُ كتابٍ مرقومٌ في الطبعة عقدةً (`### $ 1 - الكتاب الغنم`)."""
MARKS = re.compile(r"[ً-ْٰـ]")
WORD = re.compile(r"[ء-ي]+")
FOLD = {"أ": "ء", "إ": "ء", "ؤ": "ء", "ئ": "ء", "ى": "ي"}


def fold(s: str) -> str:
    return "".join(FOLD.get(c, c) for c in s.replace("آ", "ءا"))


def source() -> str:
    data = gzip.decompress(SOURCE.read_bytes())
    assert hashlib.sha256(data).hexdigest() == MUKHASSAS_SHA256, "MUKHASSAS_SOURCE_DRIFTED"
    return data.decode("utf-8")


def title(raw: str) -> str:
    t = NUMBER.sub("", raw.strip())
    return t.strip().strip("()").strip()


def is_book(t: str) -> bool:
    return t.startswith("كتاب ") or t in MISTYPED_BOOKS


def nodes(text: str) -> list[dict[str, object]]:
    """العُقَدُ بترتيبها: رقم، سطرُ العنوان، علامتُه، العنوان، الكتاب، ونصُّها إلى العنوان التالي."""

    out: list[dict[str, object]] = []
    book = "-"
    for n, ln in enumerate(text.splitlines(), 1):
        m = HEADING.match(ln)
        if m:
            t = title(m.group(2))
            if is_book(t):
                book = t
            out.append({"id": len(out) + 1, "line": n, "mark": m.group(1), "title": t, "book": book,
                        "body": []})
        elif out and not ln.startswith("# Page") and not ln.startswith("#META#"):
            body = out[-1]["body"]
            assert isinstance(body, list)
            body.append(ln)
    return out


def read_skeletons() -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for ln in SKELETONS.read_text(encoding="utf-8").splitlines():
        sk, roots = ln.split("\t")
        out[sk] = roots.split(" ")
    return out


def membership(ns: list[dict[str, object]], d: dict[str, list[str]]) -> dict[str, list[int]]:
    """`RULE_M`: جذرٌ ← العُقَدُ التي ورد في نصّها لفظٌ هيكلُه بجذرٍ واحدٍ عند ابن فارس."""

    out: dict[str, set[int]] = {}
    for nd in ns:
        body = nd["body"]
        assert isinstance(body, list)
        for tok in WORD.findall(MARKS.sub("", " ".join(body))):
            roots = d.get(fold(tok))
            if roots is not None and len(roots) == 1:
                nid = nd["id"]
                assert isinstance(nid, int)
                out.setdefault(roots[0], set()).add(nid)
    return {r: sorted(v) for r, v in out.items()}


def render_nodes(ns: list[dict[str, object]]) -> str:
    buf = io.StringIO()
    buf.write("id\tline\tmark\tbook\ttitle\n")
    for nd in ns:
        buf.write(f"{nd['id']}\t{nd['line']}\t{nd['mark']}\t{nd['book']}\t{nd['title']}\n")
    return buf.getvalue()


def render_membership(m: dict[str, list[int]]) -> str:
    return "".join(f"{r}\t{' '.join(map(str, m[r]))}\n" for r in sorted(m))


def build() -> tuple[str, str]:
    ns = nodes(source())
    return render_nodes(ns), render_membership(membership(ns, read_skeletons()))


def main(argv: list[str]) -> int:
    a, b = build()
    if "--check" in argv:
        bad = [name for name, path, want in (("MUKHASSAS_NODES_DRIFTED", NODES, a),
                                              ("MUKHASSAS_MEMBERSHIP_DRIFTED", MEMBERSHIP, b))
               if not path.exists() or path.read_text(encoding="utf-8") != want]
        ok = f"المخصَّص مطابق: {a.count(chr(10)) - 1:,} عقدةً، {b.count(chr(10)):,} جذرًا في العضويّة"
        print(", ".join(bad) if bad else ok)
        return 1 if bad else 0
    NODES.write_text(a, encoding="utf-8")
    MEMBERSHIP.write_text(b, encoding="utf-8")
    print(f"كُتب {NODES.relative_to(ROOT)} و{MEMBERSHIP.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
