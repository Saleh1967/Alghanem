"""تسجيلٌ ثانٍ على جذور QAC — الاسترجاعُ بتقشير السوابق (ADR ٤٦، `docs/qac/PREREG-2.md`).

القياسُ الأوّل (`tools/gen_qac.py`، `docs/qac/result.json`) يبقى كما سُجّل. وهذا هو نفسُه — المرجعُ
`corpora/qac/qac-roots.tsv` والمجتمعُ والحكمُ والمقاييس — والفرقُ الوحيد أنّ النظامَ المقيس
`gate.recover(word, peel=True)`: مرشَّحاتُ `A116.Sawabiq` بترتيبها بعد القراءة المباشرة. والنتيجةُ
`docs/qac/result-2.json`.

`--check` يُسقط البناءَ باسمه `QAC_PEEL_RESULT_DRIFTED`. الأداةُ معفاةٌ في الحارس لأنّها أداةُ إيداع.
"""

from __future__ import annotations

import importlib.util
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

RESULT = ROOT / "docs" / "qac" / "result-2.json"


def judge(word: str, root: str, gate_obj: Any) -> str:
    from gate import Refusal, recover

    if isinstance(gate_obj.enter(word.encode("utf-8")), Refusal):
        return "refused"
    roots = {r[0] for r in recover(word, peel=True)[1]}
    if not roots:
        return "no_reading"
    if roots == {root}:
        return "agree_unique"
    if root in roots:
        return "agree_among"
    if Q.wy(root) in {Q.wy(r) for r in roots}:
        return "disagree_waw_ya"
    return "disagree"


def tally(rows: list[dict[str, str]], gate_obj: Any) -> dict[str, object]:
    c: Counter[str] = Counter(judge(r["word"], r["root"], gate_obj) for r in rows)
    n = len(rows)
    hit = c["agree_unique"] + c["agree_among"]
    covered = n - c["refused"] - c["no_reading"]
    return {
        "n": n, "outcomes": dict(sorted(c.items())),
        "agree_any": hit, "agree_any_rate": round(hit / n, 6) if n else 0.0,
        "agree_any_wilson95": Q.wilson(hit, n),
        "agree_unique_rate": round(c["agree_unique"] / n, 6) if n else 0.0,
        "agree_mod_waw_ya_rate": round((hit + c["disagree_waw_ya"]) / n, 6) if n else 0.0,
        "covered": covered, "agree_among_covered_rate": round(hit / covered, 6) if covered else 0.0,
    }


def measure() -> dict[str, object]:
    from gate.api import Gate

    g = Gate()
    rows = Q.read_reference()
    skip = Q.seen()
    pool = [r for r in rows if (r["line"], r["pos"]) not in skip]
    verbs = [r for r in pool if r["tag"] == "V" and r["aspect"] in Q.MABNI]
    return {
        "prereg": "docs/qac/PREREG-2.md",
        "reference_sha256": Q.QAC_SHA256,
        "system": "gate.recover(word, peel=True)",
        "primary_mabni_verbs": tally(verbs, g),
        "primary_by_prefix": {
            p: tally([r for r in verbs if r["prefix"] == p], g) for p in ("0", "1")},
        "secondary_all_rooted": tally(pool, g),
    }


def main(argv: list[str]) -> int:
    if "--check" in argv:
        ok = not RESULT.exists() or RESULT.read_text(encoding="utf-8") == Q.dump(measure())
        state = "مطابقة" if RESULT.exists() else "لم تُقس بعد"
        print(f"التسجيلُ الثاني على QAC: النتيجة {state}" if ok else "QAC_PEEL_RESULT_DRIFTED")
        return 0 if ok else 1
    if argv[:1] == ["measure"]:
        RESULT.write_text(Q.dump(measure()), encoding="utf-8")
        print(f"كُتب {RESULT.relative_to(ROOT)}")
        return 0
    print("الاستعمال: measure | --check")
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
