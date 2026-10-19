"""ألفُ التأنيث على QAC — الجذرُ على الشكل (ADR ٥٣، `docs/tanith/PREREG.md`).

المجتمعُ كلماتُ QAC المحاذاة (`gen_qac.align`) اسمًا أو صفةً بلا لاحقةٍ ولها جذر، تدخل البوّابةَ شهادةً
وآخرُها ألفيّ. المرجعُ `A116.Tanith` بجذر QAC البشريّ؛ والمتنبّئات: S0 الشكلُ وحدَه، وS1 بجذرٍ من معجم
هياكل «مقاييس اللغة» (ADR ٤٧) بعد `PEEL_NOMINAL`،
وS1′ بالرجوع إلى S0. والنتيجةُ `docs/tanith/result.json`.

`--check` يُسقط البناءَ باسمه `TANITH_RESULT_DRIFTED`. الأداةُ معفاةٌ في الحارس لأنّها أداةُ قياس.
"""

from __future__ import annotations

import importlib.util
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def _load(name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / f"{name}.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


Q: Any = _load("gen_qac")
H: Any = _load("gen_hadith_roots")

RESULT = ROOT / "docs" / "tanith" / "result.json"
TAGS = frozenset({"N", "ADJ"})
PEEL_NOMINAL = ("وال", "فال", "بال", "كال", "لل", "ال", "و", "ف", "ب", "ك", "ل")


GENDERS = ("M", "F", "MS", "FS", "MD", "FD", "MP", "FP")


def features() -> tuple[set[str], dict[str, str]]:
    """مواقعُ QAC التي فيها قطعةُ `SUFFIX`، وجنسُ الجذع لكلّ موقع (وصفًا لا قياسًا، PREREG §٣)."""

    suf: set[str] = set()
    gender: dict[str, str] = {}
    for (s, v), ws in Q.qac_words(Q.source()).items():
        for w, feats in ws:
            loc = f"{s}:{v}:{w}"
            if any(f.startswith("SUFFIX") for f in feats):
                suf.add(loc)
            stem = next((f for f in feats if f.startswith("STEM")), "")
            gender[loc] = next((g for g in stem.split("|") if g in GENDERS), "-")
    return suf, gender


def maqayis_roots(word: str, d: dict[str, list[str]]) -> list[str]:
    sk = H.skeleton(word)
    if sk in d:
        return d[sk]
    for p in PEEL_NOMINAL:
        if sk.startswith(p) and sk[len(p):] in d:
            return d[sk[len(p):]]
    return []


def s1(sk: str, roots: list[str]) -> str:
    from gate.tanith import tanith

    if not roots:
        return "NO_ROOT"
    labels = {tanith(sk, r) or "none" for r in roots}
    return labels.pop() if len(labels) == 1 else "UNDECIDED"


def population() -> tuple[list[dict[str, str]], Counter[str]]:
    from gate import Refusal, enter, exit
    from gate.tanith import final_alif, skeleton, tanith

    rows, _rules, _res = Q.align(Q.source(), Q.CORPUS.read_text(encoding="utf-8"))
    suf, gender = features()
    d = H.read_skeletons()
    out: list[dict[str, str]] = []
    dropped: Counter[str] = Counter()
    for r in rows:
        if r["tag"] not in TAGS or r["loc"] in suf:
            continue
        cert = enter(r["word"].encode("utf-8"))
        if isinstance(cert, Refusal):
            dropped[cert.status] += 1
            continue
        sk = skeleton(cert.atoms)
        f = final_alif(sk)
        if f is None:
            continue
        out.append({
            "word": r["word"], "kind": f[0], "gold": tanith(sk, r["root"]) or "none",
            "s1": s1(sk, maqayis_roots(exit(cert).decode("utf-8"), d)),
            "gender": gender.get(r["loc"], "-"),
        })
    return out, dropped


def tally(pop: list[dict[str, str]]) -> dict[str, object]:
    n = len(pop)
    pos = sum(1 for p in pop if p["gold"] != "none")
    covered = [p for p in pop if p["s1"] not in ("NO_ROOT", "UNDECIDED")]
    m2 = sum(1 for p in covered if p["s1"] == p["gold"])
    m3 = sum(1 for p in pop if (p["s1"] if p in covered else p["kind"]) == p["gold"])
    conf = Counter(f"{p['gold']}|{p['s1']}" for p in pop)
    return {
        "n": n, "types": len({p["word"] for p in pop}), "gold_positive": pos,
        "M1_shape_precision": [pos, n, Q.wilson(pos, n)],
        "M2_s1_on_covered": [m2, len(covered), Q.wilson(m2, len(covered))],
        "coverage": [len(covered), n],
        "M3_s1_fallback": [m3, n, Q.wilson(m3, n)],
        "confusion_gold_s1": dict(sorted(conf.items())),
    }


def measure() -> dict[str, object]:
    pop, dropped = population()
    radical = Counter(p["word"] for p in pop if p["gold"] == "none")
    top = sorted(radical.items(), key=lambda x: (-x[1], x[0]))[:15]
    gen = Counter(p["gender"] for p in pop if p["gold"] != "none")
    return {
        "prereg": "docs/tanith/PREREG.md",
        "reference_sha256": Q.QAC_SHA256,
        "all": tally(pop),
        "by_kind": {k: tally([p for p in pop if p["kind"] == k]) for k in ("maqsura", "mamduda")},
        "refused_by_gate": dict(sorted(dropped.items())),
        "gold_positive_gender": dict(sorted(gen.items())),
        "gold_radical_top": [[w, c] for w, c in top],
    }


def main(argv: list[str]) -> int:
    if "--check" in argv:
        ok = not RESULT.exists() or RESULT.read_text(encoding="utf-8") == Q.dump(measure())
        state = "مطابقة" if RESULT.exists() else "لم تُقس بعد"
        print(f"ألفُ التأنيث على QAC: النتيجة {state}" if ok else "TANITH_RESULT_DRIFTED")
        return 0 if ok else 1
    if argv[:1] == ["measure"]:
        RESULT.write_text(Q.dump(measure()), encoding="utf-8")
        print(f"كُتب {RESULT.relative_to(ROOT)}")
        return 0
    print("الاستعمال: measure | --check")
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
