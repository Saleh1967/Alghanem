"""إيداعُ التحييد (ADR ٥٩): الحاويتان ← البابُ ← النصُّ المختوم ← الصورةُ القانونيّة، كلُّ حلقةٍ ببصمتها.

1. **الحاوية** (`tests/data/nabhani-shakhsiyya-{1,3}.docx`): بصمتُها بايتاتُها، وهي مدخلا السجلّ
   f0024 وf0025 في الغانم.
2. **الباب** (`door`): كلُّ فقرةٍ `w:p` من `word/document.xml` بترتيبها، نصوصُ `w:t` فيها موصولة،
   والفقراتُ بسطر، بلا تطبيع؛ ومعها علامةُ الاستثناء البنيويّ: الفقرةُ داخل جدولٍ (`w:tbl`) أو صندوقِ
   نصّ (`w:txbxContent`) أو حاملةٌ له.
   والشرط: البابُ يعيد النصَّ المختوم بايتًا بايتًا، وإلّا `DOOR_DOES_NOT_REPRODUCE_SEAL`.
3. **الصورةُ القانونيّة** (`slge.tahyid.canon`، مرآةُ `Slge.Tahyid.canon`): تُكتب
   `tests/data/nabhani-shakhsiyya-{1,3}.canonical.txt.gz`، وتُطابَق بصمتُها بعد فكّ الضغط.
4. **السجلّ** (`docs/tahyid/result.json`): ما حذفته كلُّ قاعدة، وأزواجُ الالتقاء (الأسطرُ التي يغيّر
   الترتيبُ ناتجَها)، وثباتُ علامات الشكل، واستقرارُ الصورة (القانونيّةُ من القانونيّة هي هي).

وبـ`--check` يعيد السلسلةَ كلَّها ويقارن، ولا يكتب.
"""

from __future__ import annotations

import gzip
import hashlib
import io
import json
import sys
import unicodedata
import zipfile
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

from slge.tahyid import canon, order_matters

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "tests" / "data"
OUT = ROOT / "docs" / "tahyid" / "result.json"
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

BOOKS: dict[str, tuple[str, str, str]] = {
    "shakhsiyya-1": ("nabhani-shakhsiyya-1",
                     "5e327aa2563af094962833951972b7537a872119a58bbfce5f2a813d20c88e17",
                     "b474d56021427070e2e3852b78bb774383f37bf87e2310d39dcdbaecf33aed63"),
    "shakhsiyya-3": ("nabhani-shakhsiyya-3",
                     "360f7653df4e3396d18153d0ea31e607523d33e0cb552b419340400b2211d5bd",
                     "359bb5532ecee8156f266522bb5388a1711e46e136004c3ac22e43f2ce656cb4"),
}
"""(الاسم، بصمةُ الحاوية، بصمةُ النصّ المختوم)."""


def door(raw: bytes) -> list[tuple[bool, str]]:
    root = ET.fromstring(zipfile.ZipFile(io.BytesIO(raw)).read("word/document.xml"))
    parent = {c: p for p in root.iter() for c in p}
    rows: list[tuple[bool, str]] = []
    for para in root.iter(W + "p"):
        text = "".join(t.text or "" for t in para.iter(W + "t"))
        node, inside = para, False
        while node in parent:
            node = parent[node]
            if node.tag in (W + "tbl", W + "txbxContent"):
                inside = True
                break
        holds = any(True for _ in para.iter(W + "txbxContent"))
        rows.append((inside or holds, text))
    return rows


def _marks(lines: list[str]) -> int:
    return sum(1 for ln in lines for ch in ln if unicodedata.category(ch) == "Mn")


def build(name: str) -> tuple[bytes, dict[str, Any]]:
    stem, c_sha, t_sha = BOOKS[name]
    raw = (DATA / f"{stem}.docx").read_bytes()
    if hashlib.sha256(raw).hexdigest() != c_sha:
        raise SystemExit(f"CONTAINER_SHA_MISMATCH:{stem}")
    rows = door(raw)
    text = "\n".join(t for _, t in rows).encode("utf-8")
    sealed = gzip.decompress((DATA / f"{stem}.txt.gz").read_bytes())
    if text != sealed or hashlib.sha256(text).hexdigest() != t_sha:
        raise SystemExit(f"DOOR_DOES_NOT_REPRODUCE_SEAL:{stem}")
    kept = [t for x, t in rows if not x]
    out = canon(rows)
    data = "\n".join(out).encode("utf-8")
    again = canon((False, ln) for ln in out)
    record = {
        "container_sha256": c_sha, "sealed_sha256": t_sha,
        "canonical_sha256": hashlib.sha256(data).hexdigest(),
        "paragraphs": len(rows), "canonical_lines": len(out),
        "excluded_structural": [i + 1 for i, (x, _) in enumerate(rows) if x],
        "tabs_removed": sum(t.count("\t") for t in kept),
        "spaces_removed": sum(len(t.replace("\t", "")) - len(t.replace("\t", "").strip(" "))
                              for t in kept),
        "blank_removed": sum(1 for t in kept if not t.replace("\t", "").strip(" ")),
        "order_critical_lines": sum(1 for t in kept if order_matters(t)),
        "marks_kept": _marks(kept), "marks_canonical": _marks(out),
        "canon_is_stable": again == out,
    }
    return data, record


def main(argv: list[str]) -> int:
    results: dict[str, Any] = {}
    ok = True
    for name, (stem, _, _) in BOOKS.items():
        data, rec = build(name)
        results[name] = rec
        path = DATA / f"{stem}.canonical.txt.gz"
        if "--check" in argv:
            ok &= path.exists() and gzip.decompress(path.read_bytes()) == data
        else:
            if not path.exists() or gzip.decompress(path.read_bytes()) != data:
                path.write_bytes(gzip.compress(data, mtime=0))
    text = json.dumps(results, ensure_ascii=False, indent=1, sort_keys=True) + "\n"
    if "--check" in argv:
        ok &= OUT.read_text(encoding="utf-8") == text
        sys.stdout.write("سلسلةُ التحييد مطابقة\n" if ok else "سلسلةُ التحييد غيرُ مطابقة\n")
        return 0 if ok else 1
    OUT.write_text(text, encoding="utf-8")
    for name, rec in results.items():
        sys.stdout.write(f"{name}\t{rec['canonical_sha256']}\t{rec['canonical_lines']}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
