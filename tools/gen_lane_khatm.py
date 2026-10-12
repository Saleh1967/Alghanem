"""قفلُ مرحلة لين (ADR ٤٥، تسجيلٌ خامس `docs/lane/PREREG-5.md`): ما بقي من ديون ADR ٤٣ بتفويض المالك
(«انت اوجد حلول وانا موافق على المصادر وعلى التوقيع تصرف»، 2026-10-12).

1. `FUULA_DEFINITION_DECISION` — **الحركاتُ المسمّاة في الشرح المختوم**: شرحُ ابن عقيل مختومٌ هنا
   ببصمته (`corpora/ibn-aqil/`)، وتُطابَق منه سطورٌ بأعيانها (البيت، الأمثلة، والجملةُ التي تسمّي
   الحركات). القاعدةُ تُقرأ من الجملة المسمّية (`named_rules`) وتُقبل إن شكّل لين مثالًا من أمثلة
   بندها بها (`admit`) — فالوزنُ من نصّ الشارح والشاهدُ من لين، ولا حركةَ من الذاكرة.
2. `A_OBJ_NEG_LABEL_SPARSE` — **دقّةُ الشاهد مباشرةً**: كلُّ مدخلٍ صحيحٍ غيرِ معلَّم شُهد تعدّيه
   (`witness_rows`) إطارٌ ثانٍ (`corpora/lane/witness-frame.tsv`) يُملأ مع إطار التعدية خليطًا
   أعمى؛ والدقّةُ نسبةُ ما وُجد متعدّيًا.
3. `TRANSITIVITY_FRAME_UNFILLED` — يُملأ الإطاران بملء وكيلٍ بتفويض المالك من نصّ لين المختوم
   نفسِه بشاهدٍ منقولٍ لكلّ صفّ (`corpora/lane/agent-fill.json`)؛ فالقياسُ عليهما **مفحوصٌ لا
   مقيس**.

`python tools/gen_lane_khatm.py frame` يكتب إطارَ الشاهد (مرّةً)؛ و`measure` يكتب
`docs/lane/khatm.json`؛ و`--check` يُسقط البناءَ بـ`IBN_AQIL_SEAL_BROKEN` أو
`IBN_AQIL_LINE_DRIFTED` أو `LANE_WITNESS_FRAME_DRIFTED` أو `LANE_KHATM_RESULT_DRIFTED`. معفاةٌ في
الحارس لأنّها أداةُ إيداع.
"""

from __future__ import annotations

import gzip
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def _load(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules.setdefault(name, mod)
    spec.loader.exec_module(mod)
    return mod


T: Any = _load("gen_lane_tahdid", ROOT / "tools" / "gen_lane_tahdid.py")
L, H, S = T.L, T.H, T.S
FA, KA, DA, SU = T.FA, T.KA, T.DA, T.SU

IBN_AQIL = ROOT / "corpora" / "ibn-aqil" / "sharh-alfiyya.txt.gz"
IBN_AQIL_SHA = "661e43ea265eca8c72b9e4ab7a46cd9182b34e834105b595241bc7787b471f09"
QUOTES: tuple[tuple[int, int, str], ...] = (
    (8407, 8407, "وفعل جمعا لفعلة عرف"),
    (8409, 8409, "ونحو كبرى ولفعلة فعل"),
    (8418, 8419, "ومن أمثلة جمع الكثرة فعل وهو جمع لاسم علي فعلة أو على فعلى أنثى الأفعل "
                 "فالأول كقربة وقرب وغرفة وغرف"),
    (8222, 8225, "جمع فعلة بكسر الفاء يكون على فعل بكسر الأول وفتح الثاني وجمع فعلة بضم الفاء "
                 "يكون على فعل بضم الأول وفتح الثاني"),
)
"""(أوّلُ سطر، آخرُه، نصٌّ) — يُطابَق في السطور المضمومة بعد حذف علامات OpenITI (`#`، `~~`)."""
NAMED_LINES = QUOTES[3]
VOWEL_NAMES = {"ضم": DA, "كسر": KA, "فتح": FA}
NAMED_RE = re.compile(r"جمع فعلة ب(ضم|كسر|فتح) الفاء يكون على فعل ب(ضم|كسر|فتح) الأول "
                      r"و(ضم|كسر|فتح) الثاني")
CLAUSE_A = T.CLAUSE_A
WITNESS_FRAME = L.LANE / "witness-frame.tsv"
WITNESS_HEADER = ["file", "entry", "root", "verb", "transitive", "witness"]
AGENT_FILL = L.LANE / "agent-fill.json"
RESULT_V5 = ROOT / "docs" / "lane" / "khatm.json"


# --- ١. الشرحُ المختوم ----------------------------------------------------------------------------


def sealed_lines() -> list[str]:
    raw = gzip.decompress(IBN_AQIL.read_bytes())
    if hashlib.sha256(raw).hexdigest() != IBN_AQIL_SHA:
        raise ValueError("IBN_AQIL_SEAL_BROKEN")
    return raw.decode("utf-8").splitlines()


def span(lines: list[str], a: int, b: int) -> str:
    """السطورُ ‎a..b‎ (من 1) مضمومةً بمسافة بعد حذف علامات OpenITI في أوّلها."""

    parts = [re.sub(r"^(?:#\s*|~~)", "", lines[i - 1]).strip() for i in range(a, b + 1)]
    return re.sub(r"\s+", " ", " ".join(parts).replace("...", " "))


def quotes_hold(lines: list[str]) -> list[str]:
    """أسماءُ ما لم يُطابَق من `QUOTES` (فارغةٌ إن طابق كلُّها)."""

    return [f"{a}-{b}" for a, b, q in QUOTES if q not in span(lines, a, b)]


def named_rules(text: str) -> list[tuple[str, str]]:
    """القواعدُ من الجملة المسمّية: «جمع فعلة بـX الفاء يكون على فعل بـY الأول وZ الثاني» ← ‎1X 2ْ 3َ ة →
    1Y 2Z 3‎. ما لم يُسمَّ من حركات المفرد وزنُ «فَعْلة» نفسِه: العينُ ساكنةٌ وما قبل التاء مفتوح (فرضٌ معلَن
    `A_NAMED`)."""

    out: list[tuple[str, str]] = []
    for x, y, z in NAMED_RE.findall(text):
        out.append((f"1{VOWEL_NAMES[x]} 2{SU} 3{FA} ة", f"1{VOWEL_NAMES[y]} 2{VOWEL_NAMES[z]} 3"))
    return out


def admit(named: list[tuple[str, str]], per_example: dict[str, list[list[str]]]
          ) -> list[tuple[str, str]]:
    """تُقبل القاعدةُ المسمّاة إن شكّل لين بها مثالًا واحدًا على الأقلّ من أمثلة البند أ."""

    seen = {tuple(p) for k in ("/".join(ex) for ex in CLAUSE_A) for p in per_example.get(k, [])}
    return [r for r in named if r in seen]


# --- ٢. إطارُ الشاهد ---------------------------------------------------------------------------


def witness_rows() -> list[list[str]]:
    """كلُّ مدخلٍ صحيحٍ في القياس غيرِ معلَّم «هُ» شُهد تعدّيه (ماضيًا أو مضارعًا بالتفرّد) — بقواعد ADR ٤٣
    نفسِها، مرتّبًا بالملف والمدخل."""

    from gate.api import LANE_CORPUS, Gate, Refusal, sealed_forms
    from gate.residue import repair

    masdar = [r for r in L.read_tsv(H.MASDAR_V2) if r[0] == "sound"]
    example_roots = ({r for _, r, _ in L.MASDAR_RULES} | {s[:3] for s, _ in L.PLURAL_RULES})
    masdar = [r for r in masdar if r[1] not in L.DEV_FILES and r[3] not in example_roots]
    words = {r[5] for r in masdar} | {w for r in masdar for w in r[7].split()}
    gate = Gate(corpus=LANE_CORPUS,
                domain={repair(w)[0] for w in words} & sealed_forms(LANE_CORPUS))

    def atoms(w: str) -> tuple[str, ...] | None:
        c = gate.enter(w.encode("utf-8"))
        return None if isinstance(c, Refusal) else tuple(H.norm(a[0]) + a[1:] for a in c.atoms)

    wit = T.corpus_witnesses({r[4] for r in masdar})
    form1, _ = T.lane_pass(set())

    def union(rad: str, key: str) -> set[str]:
        return set().union(*(wit[lab].get(rad, {}).get(key, set()) for lab in wit))

    out: list[list[str]] = []
    for r in masdar:
        if r[6] != "0":
            continue
        a = atoms(r[5])
        if a is None:
            continue
        vc = S.over(a, r[4], "") or set()
        babs = {p.split()[1][1:] for p in vc if S._facala(p)}
        if not babs:
            continue
        ms = [S.over(x, r[4], w) if (x := atoms(w)) is not None else None for w in r[7].split()]
        if not any(ms):
            continue
        past = bool(babs & union(r[4], "trans"))
        impf = form1[r[3]] == 1 and bool(babs & T.compat_babs(union(r[4], "impf")))
        if past or impf:
            out.append([r[1], r[2], r[4], r[5], "", "past" if past else "imperfect"])
    return sorted(out, key=lambda r: (r[0], r[1]))


def read_rows(path: Path, width: int) -> list[list[str]]:
    if not path.exists():
        return []
    rows = [r.split("\t") for r in path.read_text(encoding="utf-8").splitlines()][1:]
    return [r + [""] * (width - len(r)) for r in rows]


def precision(rows: list[list[str]]) -> dict[str, object] | None:
    """دقّةُ الشاهد: ‎1‎ متعدٍّ (إصابة)، ‎0‎ لازم (خطأ)، ‎01‎ الوجهان (يُحصر)؛ ولا شيء قبل ملء الكلّ."""

    vals = [r[4].strip() for r in rows]
    if not rows or any(v not in ("1", "0", "01") for v in vals):
        return None
    lo = sum(v == "1" for v in vals)
    hi = sum(v in ("1", "01") for v in vals)
    n = len(vals)
    return {"n": n, "transitive": lo, "both": hi - lo, "intransitive": n - hi,
            "precision": [round(lo / n, 4), round(hi / n, 4)],
            "ci95": [L.wilson(lo, n)[0], L.wilson(hi, n)[1]]}


# --- ٣. القياس ------------------------------------------------------------------------------------


def measure() -> dict[str, object]:
    from gate.api import LANE_CORPUS, Gate, Refusal, sealed_forms
    from gate.residue import repair

    lines = sealed_lines()
    text = span(lines, NAMED_LINES[0], NAMED_LINES[1])
    named = named_rules(text)
    tahdid = json.loads(T.RESULT_V4.read_text(encoding="utf-8"))
    admitted = admit(named, tahdid["fuula"]["per_example"])

    plural = L.read_tsv(H.PLURAL_V2)
    _, weak_p = S.weak_records()
    words = {w for r in plural + weak_p for w in [r[5], *r[6].split()]}
    gate = Gate(corpus=LANE_CORPUS,
                domain={repair(w)[0] for w in words} & sealed_forms(LANE_CORPUS))
    cache: dict[str, tuple[str, ...] | None] = {}

    def cands(w: str, rad: str, fwd: bool = False) -> set[str] | None:
        if w not in cache:
            c = gate.enter(w.encode("utf-8"))
            cache[w] = (None if isinstance(c, Refusal)
                        else tuple(H.norm(a[0]) + a[1:] for a in c.atoms))
        a = cache[w]
        if a is None:
            return None
        cs = S.over(a, rad, w)
        return T.refine(cs, rad, a, w)[0] if fwd else cs

    v1 = json.loads(L.RESULT.read_text(encoding="utf-8"))
    strict_p = {k: set(v) for k, v in v1["plural"]["rules"].items()}
    named_p = {k: set(v) for k, v in strict_p.items()}
    for sp, pp in admitted:
        named_p.setdefault(sp, set()).add(pp)
    example_roots = ({r for _, r, _ in L.MASDAR_RULES} | {s[:3] for s, _ in L.PLURAL_RULES})
    p_out: dict[str, object] = {}
    for st in ("sound", "hamzated", "doubled", "weak", "pooled"):
        acc = {k: [0, 0] for k in ("strict", "named")}
        if st == "weak":
            acc["named_fwd"] = [0, 0]
        n = 0
        for r in plural + weak_p:
            if (r[1] in L.DEV_FILES or r[3] in example_roots
                    or (st != "pooled" and r[0] != st)):
                continue
            sc = cands(r[5], r[4])
            if not sc:
                continue
            ps = [cands(w, r[4]) for w in r[6].split()]
            if not any(ps):
                continue
            n += 1
            for key, rules in (("strict", strict_p), ("named", named_p)):
                lo, hi = S.hit_bounds(sc, ps, rules)
                acc[key][0] += lo
                acc[key][1] += hi
            if st == "weak":
                scf = cands(r[5], r[4], fwd=True) or sc
                psf = [cands(w, r[4], fwd=True) for w in r[6].split()]
                lo, hi = S.hit_bounds(scf, psf, named_p)
                acc["named_fwd"][0] += lo
                acc["named_fwd"][1] += hi
        p_out[st] = {k: H.bounds(v[0], v[1], n) for k, v in acc.items()}

    wrows = read_rows(WITNESS_FRAME, 6)
    return {
        "ibn_aqil": {"sha256": IBN_AQIL_SHA, "quotes": [f"{a}-{b}" for a, b, _ in QUOTES],
                     "named_rules": [list(x) for x in named],
                     "admitted": [list(x) for x in admitted]},
        "plural": {"strata": p_out},
        "witness_precision": {"all": precision(wrows),
                              "past": precision([r for r in wrows if r[5] == "past"]),
                              "imperfect": precision([r for r in wrows if r[5] == "imperfect"])},
        "transitivity_estimate": tahdid["frame"]["estimate"],
    }


def main(argv: list[str]) -> int:
    lines = sealed_lines()
    bad = quotes_hold(lines)
    if bad:
        sys.stderr.write("IBN_AQIL_LINE_DRIFTED: " + ", ".join(bad) + "\n")
        return 1
    if "frame" in argv:
        if not WITNESS_FRAME.exists():
            WITNESS_FRAME.write_bytes(L.tsv(WITNESS_HEADER, witness_rows()))
        sys.stdout.write(f"إطارُ الشاهد: {len(read_rows(WITNESS_FRAME, 6)):,} مدخلًا\n")
        return 0
    if "--check" in argv:
        if WITNESS_FRAME.exists() and ([r[:4] + r[5:6] for r in read_rows(WITNESS_FRAME, 6)]
                                       != [r[:4] + r[5:6] for r in witness_rows()]):
            sys.stderr.write("LANE_WITNESS_FRAME_DRIFTED\n")
            return 1
        if RESULT_V5.exists() and RESULT_V5.read_bytes() != L.dump(measure()):
            sys.stderr.write("LANE_KHATM_RESULT_DRIFTED\n")
            return 1
        sys.stdout.write("قفلُ لين مطابق\n")
        return 0
    if "measure" in argv:
        RESULT_V5.write_bytes(L.dump(measure()))
        sys.stdout.write(f"كُتب {RESULT_V5.relative_to(ROOT)}\n")
        return 0
    sys.stdout.write("frame | measure | --check\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
