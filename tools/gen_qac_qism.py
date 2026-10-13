"""الفرزُ يحسّن قراءة الإعراب: القياسُ على QAC (ADR ٥٤، `docs/qism/PREREG.md`).

المجتمعُ كلماتُ QAC المحاذاة: أسماءٌ بحالة بلا لاحقة، ومضارعٌ معرب بلا لاحقةٍ إلّا ضميرَ فاعله. المرجعُ حالةُ
Dukes. والقرّاء: الساذج، وبلا فرز، وبفرز الاسم من الفعل، وبالصنف بقواعد الألفيّة (`klass`). والنتيجةُ
`docs/qism/result.json`.

`--check` يُسقط البناءَ باسمه `QISM_RESULT_DRIFTED`. الأداةُ معفاةٌ في الحارس لأنّها أداةُ قياس.
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

RESULT = ROOT / "docs" / "qism" / "result.json"
NOUN_TAGS = frozenset({"N", "ADJ", "PN"})
CASE = {"NOM": "raf", "ACC": "nasb", "GEN": "jarr"}
SITTA = frozenset({">abN", ">ax", "*uw", "*aA", "Ham", "fuw"})
DUAL = frozenset({"MD", "FD", "D"})
PLURAL_M = frozenset({"MP", "P"})
PERSONS = ("1S", "1P", "2MS", "2FS", "2D", "2MD", "2FD", "2MP", "2FP", "3MS", "3FS", "3D", "3MD",
           "3FD", "3MP", "3FP")


def feats_of(segs: list[str]) -> dict[str, str]:
    stem = next((f for f in segs if f.startswith("STEM")), "")
    parts = stem.split("|")
    out = {"pos": Q.field([stem], "POS"), "lem": Q.field([stem], "LEM"),
           "root": Q.field([stem], "ROOT")}
    out["case"] = next((p for p in parts if p in CASE), "")
    numbers = ("M", "F", "MS", "FS", "MD", "FD", "MP", "FP", "D", "P")
    out["num"] = next((p for p in parts if p in numbers), "")
    out["person"] = next((p for p in parts if p in PERSONS), "")
    out["aspect"] = next((p for p in parts if p in ("PERF", "IMPF", "IMPV")), "")
    out["mood"] = next((p for p in parts if p.startswith("MOOD:")), "")
    sufs = [f for f in segs if f.startswith("SUFFIX")]
    out["emph"] = "1" if any("EMPH" in f for f in sufs) else ""
    out["subj_only"] = "1" if all(f == f"SUFFIX|PRON:{out['person']}" for f in sufs) else ""
    out["nosuf"] = "" if sufs else "1"
    return out


def klass(f: dict[str, str], e: str | None, word: str) -> str:
    """الصنفُ بقواعد التسجيل §٤ بترتيبها."""

    from gate.qism import clusters

    if f["pos"] in NOUN_TAGS:
        letters = "".join(c for c, _ in clusters(word))
        if f["num"] in DUAL and e in ("ani", "ayni"):
            return "iMuthanna"
        if f["num"] in PLURAL_M and e in ("una", "ina"):
            return "iJamM"
        if f["num"] == "FP" and letters.endswith("ات"):
            return "iJamF"
        if f["lem"] in SITTA and e in ("waw", "alif", "ya"):
            return "iSitta"
        if e == "alif":
            return "iMaqsur"
        if e == "ya":
            return "iManqus"
        return "iSahih"
    p = f["person"]
    if p in ("3MP", "2MP"):
        return "fKhamsaW"
    if "D" in p:
        return "fKhamsaA"
    if p == "2FS":
        return "fKhamsaY"
    if f["root"][-1:] not in ("w", "y"):
        return "fSahih"
    if e in ("alif",):
        return "fMutalAlif"
    if e in ("waw", "damma"):
        return "fMutalW"
    if e in ("ya", "kasra"):
        return "fMutalY"
    if e == "fatha":
        last = clusters(word)[-1][0]
        return {"و": "fMutalW", "ي": "fMutalY"}.get(last, "fMutalAlif")
    return "fSahih"


def population() -> tuple[list[dict[str, str]], Counter[str]]:
    from gate import Refusal, enter, exit
    from gate.qism import ending_of

    data = Q.source()
    words = Q.qac_words(data)
    lines = Q.CORPUS.read_text(encoding="utf-8").splitlines()
    keys = sorted(words)
    out: list[dict[str, str]] = []
    tally: Counter[str] = Counter()
    for i, (s, v) in enumerate(keys):
        raw = lines[i].split(" ")
        gs, _ = Q.groups(s, v, raw)
        if len(gs) != len(words[(s, v)]):
            tally["ALIGN_RESIDUAL"] += 1
            continue
        for g, (_w, segs) in zip(gs, words[(s, v)], strict=True):
            f = feats_of(segs)
            if f["pos"] in NOUN_TAGS and f["case"] and f["nosuf"]:
                gold = CASE[f["case"]]
            elif f["pos"] == "V" and f["aspect"] == "IMPF":
                if f["person"] in ("3FP", "2FP"):
                    tally["MABNI_INATH"] += 1
                    continue
                if f["emph"]:
                    sep = f["person"] in ("3MP", "2MP", "2FS") or "D" in f["person"]
                    tally["TAWKID_" + ("MAFSUL" if sep else "MUBASHIR")] += 1
                    continue
                if not f["subj_only"]:
                    continue
                gold = {"MOOD:SUBJ": "nasb", "MOOD:JUS": "jazm"}.get(f["mood"], "raf")
            else:
                continue
            cert = enter(raw[g[-1]].encode("utf-8"))
            if isinstance(cert, Refusal):
                tally["REFUSED_" + cert.status] += 1
                continue
            word = exit(cert).decode("utf-8")
            e = ending_of(word)
            out.append({"word": word, "noun": "1" if f["pos"] in NOUN_TAGS else "", "gold": gold,
                        "ending": e or "", "class": klass(f, e, word)})
    return out, tally


def readers(p: dict[str, str]) -> dict[str, str | None]:
    from gate import qism
    from gate.qism import naive, read

    e = p["ending"]
    if not e:
        return {"R0": None, "R1": None, "R2": None, "R3": None}
    return {"R0": naive(e), "R1": read(qism.blind_view, (), e),
            "R2": read(qism.qism_view, bool(p["noun"]), e),
            "R3": read(qism.class_view, p["class"], e)}


def tally(pop: list[dict[str, str]]) -> dict[str, object]:
    n = len(pop)
    out: dict[str, object] = {"n": n}
    reads = [readers(p) for p in pop]
    for r in ("R0", "R1", "R2", "R3"):
        dec = sum(1 for x in reads if x[r] is not None)
        ok = sum(1 for x, p in zip(reads, pop, strict=True) if x[r] == p["gold"])
        out[r] = {"decided": dec, "correct": ok, "accuracy_on_decided": Q.wilson(ok, dec),
                  "correct_over_n": Q.wilson(ok, n)}
    return out


def measure() -> dict[str, object]:
    pop, counts = population()
    nouns = [p for p in pop if p["noun"]]
    verbs = [p for p in pop if not p["noun"]]
    mamnu = sum(1 for p in nouns if p["gold"] == "jarr" and p["ending"] == "fatha")
    return {
        "prereg": "docs/qism/PREREG.md",
        "reference_sha256": Q.QAC_SHA256,
        "all": tally(pop), "nouns": tally(nouns), "verbs": tally(verbs),
        "class_counts": dict(sorted(Counter(p["class"] for p in pop).items())),
        "excluded": dict(sorted(counts.items())),
        "jarr_with_fatha_ending": mamnu,
    }


def main(argv: list[str]) -> int:
    if "--check" in argv:
        ok = not RESULT.exists() or RESULT.read_text(encoding="utf-8") == Q.dump(measure())
        state = "مطابقة" if RESULT.exists() else "لم تُقس بعد"
        print(f"الفرزُ على QAC: النتيجة {state}" if ok else "QISM_RESULT_DRIFTED")
        return 0 if ok else 1
    if argv[:1] == ["measure"]:
        RESULT.write_text(Q.dump(measure()), encoding="utf-8")
        print(f"كُتب {RESULT.relative_to(ROOT)}")
        return 0
    print("الاستعمال: measure | --check")
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
