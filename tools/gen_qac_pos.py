"""أقسامُ الكلم في QAC 0.4 مودَعًا لـSLGE — مرجعُ الصنف المغلق (ADR ٥١).

SLGE يفصل المبنيّات المغلقة (الحروف، الضمائر، الإشارة، الاستفهام، الموصول) عن الاسم والفعل بوسمٍ
خاصّ (SLGE ADR ٥٠). ومرجعُه المحجوب وسمُ Kais Dukes لقسم كلّ قطعةٍ في المصحف (QAC 0.4، GPL، المختومُ
هنا ببصمته `gen_qac.QAC_SHA256`، ADR ٤١) — لم يُستعمل في بناء شيءٍ من قارئ SLGE. وSLGE لا يقرأ نصًّا،
فالمودَعُ هناك **مواقعُ لا كلمات**: لكلّ كلمةٍ محاذاةٍ عددُ موقعها في تيّار شهادات المصحف
(`corpus-certificates.json.gz`: كلُّ رمزٍ في السطر سوى `<sel>` موقعٌ بالترتيب، كما في
`gen_certificates.generate`)، وقطعُها بأقسامها (`PREFIX:CONJ+STEM:PRON`)، وقسمُ الجذع.

المحاذاةُ محاذاةُ `gen_qac.align` بقاعدتيها المسمّاتين (`BASMALA`، `YA_JOINED`) وآياتها المتروكة
(`ALIGN_RESIDUAL`)، مع فرقٍ واحد: كلُّ كلمةٍ لا المجذورةُ وحدَها؛ وفي الضمّة (`YA_JOINED`) يُودَع الموقعُ
الأخير وحدَه بقطع الكلمة كلّها، والأوّلُ متروكٌ يُعدّ باسمه `YA_JOINED_FIRST`.

`python tools/gen_qac_pos.py OUT` يكتب `OUT` (TSV مضغوطًا بلا طابع زمن)؛ و`--check OUT` يُسقط البناءَ
بـ`QAC_POS_DEPOSIT_DRIFTED` إن لم يكن المودَعُ ما تطبعه هذه الأداةُ الآن (CI الخاصّ بـSLGE يشغّله
على الإيداع المثبَّت). معفاةٌ في الحارس لأنّها أداةُ إيداع.
"""

from __future__ import annotations

import gzip
import importlib.util
import io
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

_SPEC = importlib.util.spec_from_file_location("gen_qac", ROOT / "tools" / "gen_qac.py")
assert _SPEC and _SPEC.loader
Q: Any = importlib.util.module_from_spec(_SPEC)
sys.modules["gen_qac"] = Q
_SPEC.loader.exec_module(Q)

HEADER = ("tok", "loc", "segs", "stem")


def segments(data: bytes) -> dict[tuple[int, int], list[tuple[int, list[str]]]]:
    """‎(سورة، آية) ← [(رقمُ الكلمة، [نوعُ القطعة:قسمُها])]‎ بالترتيب."""

    out: dict[tuple[int, int], dict[int, list[str]]] = {}
    for ln in data.decode("utf-8").splitlines():
        if not ln.startswith("("):
            continue
        loc, _form, tag, feats = ln.split("\t")
        s, v, w, _seg = (int(x) for x in loc.strip("()").split(":"))
        out.setdefault((s, v), {}).setdefault(w, []).append(f"{feats.split('|')[0]}:{tag}")
    return {k: sorted(ws.items()) for k, ws in out.items()}


def rows(data: bytes, corpus: str) -> tuple[list[tuple[str, ...]], Counter[str]]:
    """صفوفُ المودَع (الموقع، الموضع، القطع، قسمُ الجذع) وعدّادُ القواعد."""

    words = segments(data)
    keys = sorted(words)
    lines = corpus.splitlines()
    assert len(keys) == len(lines), "QAC_VERSE_COUNT"
    out: list[tuple[str, ...]] = []
    rules: Counter[str] = Counter()
    base = 0
    for i, (s, v) in enumerate(keys):
        raw = lines[i].split(" ")
        tok = {j: base + k for k, j in enumerate(j for j, t in enumerate(raw) if t != "<sel>")}
        base += len(tok)
        gs, dropped = Q.groups(s, v, raw)
        rules["BASMALA"] += dropped
        if len(gs) != len(words[(s, v)]):
            rules["ALIGN_RESIDUAL"] += 1
            continue
        for g, (w, segs) in zip(gs, words[(s, v)], strict=True):
            rules["YA_JOINED_FIRST"] += len(g) - 1
            stem = next((x.split(":", 1)[1] for x in segs if x.startswith("STEM:")), "")
            out.append((str(tok[g[-1]]), f"{s}:{v}:{w}", "+".join(segs), stem))
    assert base == sum(1 for ln in lines for t in ln.split(" ") if t != "<sel>")
    return out, rules


def render(rs: list[tuple[str, ...]]) -> bytes:
    text = "\t".join(HEADER) + "\n" + "".join("\t".join(r) + "\n" for r in rs)
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode="wb", mtime=0, filename="") as f:
        f.write(text.encode("utf-8"))
    return buf.getvalue()


def generate() -> tuple[bytes, Counter[str], int]:
    data = Q.source()
    corpus = Q.CORPUS.read_text(encoding="utf-8")
    rs, rules = rows(data, corpus)
    return render(rs), rules, len(rs)


def main(argv: list[str]) -> int:
    if not argv or argv == ["--check"]:
        sys.stdout.write("OUT | --check OUT\n")
        return 2
    out = Path(argv[-1])
    blob, rules, n = generate()
    if "--check" in argv:
        if gzip.decompress(out.read_bytes()) != gzip.decompress(blob):
            sys.stderr.write("QAC_POS_DEPOSIT_DRIFTED\n")
            return 1
        sys.stdout.write(f"مودَعُ أقسام QAC مطابق: {n:,} كلمةً؛ {dict(sorted(rules.items()))}\n")
        return 0
    out.write_bytes(blob)
    sys.stdout.write(f"كُتب {out} ({n:,} كلمةً؛ {dict(sorted(rules.items()))})\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
