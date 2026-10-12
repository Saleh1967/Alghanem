"""جذورُ الصحيحين من «مقاييس اللغة» — نقلُ حكم ابن فارس إلى المواضع بالهيكل (ADR ٤٧، قرارُ المالك
2026-10-13).

**الواقع.** جدولُ «مقاييس اللغة» المختوم (`maqayis_by_root_csv_999.csv`، بصمتُه
`MAQAYIS_SHA256`): لكلّ جذرٍ نصُّ ابن فارس (`body_text`) وفيه الألفاظُ التي وضعها هو تحت ذلك
الجذر. فالحكمُ «اللفظُ من الجذر R» حكمُه هو، لا حكمُ البوّابة ولا الوكيل.

**القاعدة** (`RULE_B`، معلنةٌ في `docs/hadith-roots/PREREG.md` قبل القياس):

* الجذرُ من الجدول بطيّ الكراسيّ همزةً والمقصورةِ ياءً و«آ» = «ءا»، ثلاثةُ أصولٍ من الثمانية
  والعشرين (قاعدةُ `tests/test_maqayis.py` نفسُها).
* كلُّ لفظٍ عربيٍّ في نصّ الجذر يُطوى هيكلًا (بلا حركاتٍ ولا تطويل، وبالطيّ نفسه)، ويُعدّ من
  الجذر **إن وقعت أصولُه الثلاثة فيه بترتيبها** (حرفًا حرفًا، والضعيفُ كما كُتب في الجذر).
* المعجمُ: هيكلٌ ← جذوره؛ ويُنقل إلى موضع الصحيحين ما كان هيكلُه في المعجم بجذرٍ **واحد**
  (`unique`)، وما التبس يُعدّ ولا يُنقل.

`python tools/gen_hadith_roots.py` يكتب المعجمَ `corpora/hadith/maqayis-skeletons.tsv`؛
و`measure` يكتب `docs/hadith-roots/result.json`؛ و`--check` يُسقط البناءَ بأسمائها:
`MAQAYIS_SOURCE_DRIFTED`، `MAQAYIS_SKELETONS_DRIFTED`، `HADITH_ROOTS_RESULT_DRIFTED`. الأداةُ
معفاةٌ في الحارس لأنّها أداةُ إيداع.
"""

from __future__ import annotations

import csv
import gzip
import hashlib
import importlib.util
import io
import re
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

MAQAYIS = ROOT / "maqayis_by_root_csv_999.csv"
MAQAYIS_SHA256 = "2c6000bd47797e183294b89da77df4ddfd27921ea595c6071ba52299c382ccb0"
LINES = ROOT / "corpora" / "hadith" / "sahihain-lines.txt.gz"
SEEN_FRAME = ROOT / "corpora" / "hadith" / "sample-frame.tsv"
SKELETONS = ROOT / "corpora" / "hadith" / "maqayis-skeletons.tsv"
RESULT = ROOT / "docs" / "hadith-roots" / "result.json"

RADICALS = frozenset("بتثجحخدذرزسشصضطظعغفقكلمنهويء")
FOLD = {"أ": "ء", "إ": "ء", "ؤ": "ء", "ئ": "ء", "ى": "ي"}
MARKS = re.compile(r"[ً-ْٰـ]")
WORD = re.compile(r"[ء-يً-ْٰ]+")
LETTER = re.compile(r"[ء-يٱ]")


def fold(s: str) -> str:
    return "".join(FOLD.get(c, c) for c in s.replace("آ", "ءا"))


def skeleton(token: str) -> str:
    return fold(MARKS.sub("", token))


def in_order(sk: str, root: str) -> bool:
    i = 0
    for c in root:
        k = sk.find(c, i)
        if k < 0:
            return False
        i = k + 1
    return True


def maqayis_rows() -> list[dict[str, str]]:
    data = MAQAYIS.read_bytes()
    assert hashlib.sha256(data).hexdigest() == MAQAYIS_SHA256, "MAQAYIS_SOURCE_DRIFTED"
    return list(csv.DictReader(data.decode("utf-8").splitlines()))


def skeletons() -> dict[str, set[str]]:
    """`RULE_B`: هيكلٌ ← الجذورُ التي وضعه ابنُ فارس تحتها وأصولُها فيه بترتيبها."""

    out: dict[str, set[str]] = {}
    for row in maqayis_rows():
        root = fold(row["root_full"])
        if len(root) != 3 or not set(root) <= RADICALS:
            continue
        for tok in WORD.findall(row["body_text"]):
            sk = skeleton(tok)
            if in_order(sk, root):
                out.setdefault(sk, set()).add(root)
    return out


def render(d: dict[str, set[str]]) -> str:
    buf = io.StringIO()
    for sk in sorted(d):
        buf.write(f"{sk}\t{' '.join(sorted(d[sk]))}\n")
    return buf.getvalue()


def read_skeletons() -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for ln in SKELETONS.read_text(encoding="utf-8").splitlines():
        sk, roots = ln.split("\t")
        out[sk] = roots.split(" ")
    return out


def positions() -> list[tuple[int, int, str]]:
    """‎(السطر، الرمز، الكلمة)‎ لكلّ موضع — عدّاهما من 1 كإطار العيّنة، والرموزُ ليست مواقع."""

    from gate.api import is_marker

    with gzip.open(LINES, "rb") as f:
        text = f.read().decode("utf-8")
    return [(i + 1, j + 1, t) for i, ln in enumerate(text.splitlines())
            for j, t in enumerate(ln.split(" ")) if t and not is_marker(t) and LETTER.search(t)]


def seen() -> set[tuple[int, int]]:
    with SEEN_FRAME.open(encoding="utf-8", newline="") as f:
        return {(int(r["line"]), int(r["pos"])) for r in csv.DictReader(f, delimiter="\t")}


def wy(root: str) -> str:
    """الصنفُ الضعيف (`WEAK_RADICAL_CLASS`): الواوُ والياءُ أصلًا واحدًا في الموازنة."""

    return root.replace("ي", "و")


def judge(word: str, ref: str, gate_obj: Any) -> str:
    from gate import Refusal, recover

    if isinstance(gate_obj.enter(word.encode("utf-8")), Refusal):
        return "refused"
    roots = {r[0] for r in recover(word, peel=True)[1]}
    if not roots:
        return "no_reading"
    if ref in roots:
        return "agree_exact"
    if wy(ref) in {wy(r) for r in roots}:
        return "agree_weak_class"
    return "disagree"


def reference_quality(d: dict[str, list[str]]) -> dict[str, object]:
    """اتّفاقُ المرجعين البشريّين حيث يقع كلاهما: نقلُ ابن فارس هنا، ونقلُ Dukes بالهيكل من QAC."""

    qac: dict[str, set[str]] = {}
    for r in Q.read_reference():
        qac.setdefault(skeleton(r["word"]), set()).add(r["root"])
    both = exact = weak = 0
    for _, _, w in positions():
        sk = skeleton(w)
        if sk in d and len(d[sk]) == 1 and len(qac.get(sk, ())) == 1:
            a, b = d[sk][0], next(iter(qac[sk]))
            both += 1
            exact += a == b
            weak += wy(a) == wy(b)
    return {"n": both, "exact_rate": round(exact / both, 6),
            "weak_class_rate": round(weak / both, 6), "weak_class_wilson95": Q.wilson(weak, both)}


def measure() -> dict[str, object]:
    from gate.api import HADITH_CORPUS, Gate

    g = Gate(corpus=HADITH_CORPUS)
    d = read_skeletons()
    skip = seen()
    rows: list[tuple[str, str]] = []
    status: Counter[str] = Counter()
    for line, pos, w in positions():
        if (line, pos) in skip:
            status["excluded_seen"] += 1
            continue
        roots = d.get(skeleton(w))
        if roots is None:
            status["no_reference"] += 1
        elif len(roots) > 1:
            status["ambiguous_reference"] += 1
        else:
            status["unique_reference"] += 1
            rows.append((w, roots[0]))
    c: Counter[str] = Counter(judge(w, ref, g) for w, ref in rows)
    n = len(rows)
    read = n - c["refused"] - c["no_reading"]
    hit_w = c["agree_exact"] + c["agree_weak_class"]
    return {
        "prereg": "docs/hadith-roots/PREREG.md",
        "maqayis_sha256": MAQAYIS_SHA256,
        "system": "gate.recover(word, peel=True)",
        "positions": dict(sorted(status.items())),
        "outcomes": dict(sorted(c.items())),
        "n": n, "read": read,
        "primary_agree_weak_class_among_read": round(hit_w / read, 6) if read else 0.0,
        "primary_wilson95": Q.wilson(hit_w, read),
        "agree_exact_among_read": round(c["agree_exact"] / read, 6) if read else 0.0,
        "coverage_read": round(read / n, 6) if n else 0.0,
        "agree_weak_class_over_all": round(hit_w / n, 6) if n else 0.0,
        "reference_quality_vs_qac": reference_quality(d),
    }


def main(argv: list[str]) -> int:
    if "--check" in argv:
        bad: list[str] = []
        if SKELETONS.read_text(encoding="utf-8") != render(skeletons()):
            bad.append("MAQAYIS_SKELETONS_DRIFTED")
        if RESULT.exists() and RESULT.read_text(encoding="utf-8") != Q.dump(measure()):
            bad.append("HADITH_ROOTS_RESULT_DRIFTED")
        state = "مطابقة" if RESULT.exists() else "لم تُقس بعد"
        ok = f"معجمُ هياكل المقاييس مطابق: {len(read_skeletons()):,} هيكلًا؛ النتيجة {state}"
        print(", ".join(bad) if bad else ok)
        return 1 if bad else 0
    if argv[:1] == ["measure"]:
        RESULT.parent.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(Q.dump(measure()), encoding="utf-8")
        print(f"كُتب {RESULT.relative_to(ROOT)}")
        return 0
    SKELETONS.write_text(render(skeletons()), encoding="utf-8")
    print(f"كُتب {SKELETONS.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
