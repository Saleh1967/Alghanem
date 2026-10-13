"""الكلمةُ بعينها أوّلًا: قراءةُ المعجم قبل التقشير (ADR ٥٠، تسجيلٌ مسبق
`docs/lane-lexical/PREREG.md`).

ADR ٤٩ عيّن علاجين للاسترجاع بأسمائهما: **تقشيرٌ يأخذ الأصل** (وَجْه ← جهو) و**اسمٌ لا يُقرأ**
(الاسترجاعُ للفعل وحدَه). وكلاهما يُعالَج بترتيبٍ واحد يمدّ ما برهنه `A116.Sawabiq`
(`candidates_head`: الكلمةُ بعينها أوّلُ المرشَّحات): **الكلمةُ بعينها تُقرأ بكلّ قارئٍ لها قبل أن
تُقشَّر** — قراءةُ الفعل المباشرة، ثمّ قراءةُ معجم لين للكلمة بعينها (`RULE_L`، ADR ٤٩)، ثمّ
المرشَّحاتُ المقشّرة. والنظامُ هنا تركيبٌ يُقاس لا تعديلٌ للبوّابة: `gate.recover` كما هو.

الأنظمةُ المقيسة على QAC (وسمُ Dukes البشريّ للموضع، لم يُستعمل في بناء شيءٍ منها):

- `S0` — `gate.recover(word, peel=True)` (ADR ٤٦).
- `S1` — النظامُ أوّلًا: `S0`، فإن لم يقرأ فمعجمُ لين.
- `S2` — المعجمُ أوّلًا: معجمُ لين، فإن لم يكن فـ`S0`.
- `S3` (الرئيس) — الكلمةُ بعينها أوّلًا: `recover(word)` بلا تقشير، ثمّ معجمُ لين، ثمّ
  `recover(word, peel=True)`.

`python tools/gen_lane_lexical.py measure` يكتب `docs/lane-lexical/result.json`؛ و`--check` يُسقط
البناءَ بـ`LANE_LEXICAL_RESULT_DRIFTED`. معفاةٌ في الحارس لأنّها أداةُ إيداع.
"""

from __future__ import annotations

import importlib.util
import sys
from collections import Counter
from collections.abc import Callable
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def _load(name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / f"{name}.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules.setdefault(name, mod)
    spec.loader.exec_module(mod)
    return mod


R: Any = _load("gen_lane_roots")
Q = R.Q
RESULT = ROOT / "docs" / "lane-lexical" / "result.json"
SYSTEMS = ("S0", "S1", "S2", "S3")
Reader = Callable[[str], "set[str]"]


def compose(direct: Reader, lexical: Reader, peeled: Reader) -> dict[str, Reader]:
    """الأنظمةُ الأربعة من ثلاثة قرّاء: المباشر (بلا تقشير)، والمعجم (للكلمة بعينها)، والمقشِّر
    (`peel=True`)."""

    def first(*readers: Reader) -> Reader:
        def run(w: str) -> set[str]:
            for r in readers:
                got = r(w)
                if got:
                    return got
            return set()
        return run

    return {"S0": peeled, "S1": first(peeled, lexical), "S2": first(lexical, peeled),
            "S3": first(direct, lexical, peeled)}


def tally(rows: list[tuple[str, str]], system: Reader) -> dict[str, object]:
    """(الكلمة، جذرُ Dukes) ← المغطّى، والاتّفاقُ على الكلّ وعلى المغطّى (حرفًا، وبالصنف الضعيف)."""

    c: Counter[str] = Counter()
    for w, gold in rows:
        rs = system(w)
        if not rs:
            c["no_reading"] += 1
        elif gold in rs:
            c["agree"] += 1
        elif any(R.same(gold, r) for r in rs):
            c["agree_weak_class"] += 1
        else:
            c["disagree"] += 1
    n = len(rows)
    covered = n - c["no_reading"]
    return {"n": n, "outcomes": dict(sorted(c.items())),
            "agree_over_all": R.rate(c["agree"], n),
            "agree_among_covered": R.rate(c["agree"], covered),
            "agree_weak_class_over_all": R.rate(c["agree"] + c["agree_weak_class"], n),
            "coverage": round(covered / n, 6) if n else None}


def verdict(s0: dict[str, Any], s3: dict[str, Any]) -> str:
    """قاعدةُ التسجيل: `S3` أفضلُ إن جاوز حدُّه الأدنى للاتّفاق على الكلّ حدَّ `S0` الأعلى، ولم
    ينزل حدُّه الأدنى على
    المغطّى عن حدّ `S0` الأدنى بأكثرَ من نقطة."""

    up = s3["agree_over_all"]["wilson95"][0] > s0["agree_over_all"]["wilson95"][1]
    keep = (s3["agree_among_covered"]["wilson95"][0]
            >= s0["agree_among_covered"]["wilson95"][0] - 0.01)
    return "S3_BETTER" if up and keep else ("S3_NOT_BETTER" if not up else "S3_LOSES_PRECISION")


def measure() -> dict[str, object]:
    from gate import recover
    from gate.api import Gate, Refusal

    d = R.read_keys()
    g = Gate()
    rows_all = [r for r in Q.read_reference() if (r["line"], r["pos"]) not in Q.seen()]
    cache: dict[tuple[str, str], set[str]] = {}

    def memo(tag: str, f: Reader) -> Reader:
        def run(w: str) -> set[str]:
            if (tag, w) not in cache:
                cache[(tag, w)] = f(w)
            return cache[(tag, w)]
        return run

    def atoms(w: str) -> tuple[str, ...] | None:
        c = g.enter(w.encode("utf-8"))
        return None if isinstance(c, Refusal) else tuple(R.H.norm(x[0]) + x[1:] for x in c.atoms)

    def lexical(w: str) -> set[str]:
        r = R.ref_of(d, atoms(w), w)
        return {r} if r else set()

    systems = compose(memo("direct", lambda w: {x[0] for x in recover(w)[1]}),
                      memo("lexical", lexical),
                      memo("peeled", lambda w: {x[0] for x in recover(w, peel=True)[1]}))
    rows = [(r["word"], r["root"]) for r in rows_all]
    verbs = [(r["word"], r["root"]) for r in rows_all
             if r["tag"] == "V" and r["aspect"] in Q.MABNI]
    nouns = [(r["word"], r["root"]) for r in rows_all if r["tag"] != "V"]
    out = {name: {"all_rooted": tally(rows, f), "mabni_verbs": tally(verbs, f),
                  "non_verbs": tally(nouns, f)} for name, f in systems.items()}
    return {"prereg": "docs/lane-lexical/PREREG.md", "reference": "QAC 0.4 (Dukes)",
            "systems": out,
            "verdict_all_rooted": verdict(out["S0"]["all_rooted"], out["S3"]["all_rooted"]),
            "verdict_mabni_verbs": verdict(out["S0"]["mabni_verbs"], out["S3"]["mabni_verbs"])}


def main(argv: list[str]) -> int:
    if "--check" in argv:
        if RESULT.exists() and RESULT.read_text(encoding="utf-8") != Q.dump(measure()):
            sys.stderr.write("LANE_LEXICAL_RESULT_DRIFTED\n")
            return 1
        state = "مطابقة" if RESULT.exists() else "لم تُقس بعد"
        sys.stdout.write(f"قراءةُ المعجم: النتيجة {state}\n")
        return 0
    if argv[:1] == ["measure"]:
        RESULT.parent.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(Q.dump(measure()), encoding="utf-8")
        sys.stdout.write(f"كُتب {RESULT.relative_to(ROOT)}\n")
        return 0
    sys.stdout.write("measure | --check\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
