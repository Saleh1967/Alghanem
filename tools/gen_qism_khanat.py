"""قسمُ الكلمة من الخانات بعلامات سيبويه والألفيّة، والسقف (ADR ١٠٦) — القياسُ المسجَّلُ مسبقًا.

ينفّذ `docs/qism-khanat/PREREG.md` بعينه:
* المجتمع: رموزُ المصحف المختوم المقابلةُ لكلمةٍ واحدةٍ من QAC 0.4 (`gen_qac.groups`).
* المرجع: قسمُ جذعها بقسمة `gen_fractal_tarkib.code`.
* القسمة: A السورُ الفردية للاختيار، وB الزوجية للقياس.
* العلاماتُ العشر ثابتة، والاختيارُ على A بخطأٍ ≤ 1٪.
* القارئان K (العلامات) وM (الحافظ)، والسقفان على B.

والمبرهناتُ العامّة التي يُتحقّق منها هنا عددًا في `A116/QismKhanat.lean`:
* خطأُ المعيَّن لا يزيد على مجموع أخطاء العلامات.
* لا دالّةَ في الذرّات تزيد على السقف.

`python tools/gen_qism_khanat.py` يكتب `docs/qism-khanat/result.json`، و`--check` يُسقط البناءَ
بـ`QISM_KHANAT_RESULT_DRIFTED` إن لم يكن المودَعُ ما يحسبه الآن. معفاةٌ في الحارس لأنّها أداةُ قياس.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import sys
from collections import Counter, defaultdict
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import gate  # noqa: E402
from gate import Refusal  # noqa: E402

PREREG = ROOT / "docs" / "qism-khanat" / "PREREG.md"
RESULT = ROOT / "docs" / "qism-khanat" / "result.json"

F, D, K, S = "َ", "ُ", "ِ", "ْ"
VOWELS = (F, D, K)
ISM, FIL, HARF = 0, 1, 2
ALL = (ISM, FIL, HARF)
MUDARI = frozenset(h + m for h in "ءتين" for m in (F, D))


def _load(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


FT = _load("gen_fractal_tarkib", ROOT / "tools" / "gen_fractal_tarkib.py")
Q = FT.Q

Atoms = tuple[str, ...]
Pattern = Callable[[Atoms, Atoms | None], bool]


def vowelled(c: str) -> bool:
    return c[1:] in VOWELS


def _al(w: Atoms, _p: Atoms | None) -> bool:
    for i in (0, 1):
        if i == 1 and (not w or w[0] not in {"وَ", "فَ", "بِ", "كَ", "لِ"}):
            break
        r = w[i:]
        if (r[:2] == ("ءَ", "لْ") and len(r) > 2) or (r[:1] == ("لْ",) and len(r) > 1):
            return True
    return False


def _tanwin(w: Atoms, _p: Atoms | None) -> bool:
    return len(w) >= 2 and w[-1] == "نْ" and vowelled(w[-2])


def _ta_sakina(w: Atoms, _p: Atoms | None) -> bool:
    return len(w) >= 2 and w[-1] == "تْ" and w[-2][1:] == F


def _ta_fail(w: Atoms, _p: Atoms | None) -> bool:
    return (len(w) >= 2 and w[-1] in {"تُ", "تَ", "تِ"} and w[-2][1:] == S
            and w[-2][0] not in "اوي")


def _ya_faila(w: Atoms, _p: Atoms | None) -> bool:
    return (len(w) >= 4 and w[0] in {"تَ", "تُ"} and w[-1] == "نَ" and w[-2] == "يْ"
            and w[-3][1:] == K)


def _nun_tawkid(w: Atoms, _p: Atoms | None) -> bool:
    if len(w) < 4 or w[0] != "لَ" or w[1] not in MUDARI:
        return False
    return any(w[i] == "نْ" and w[i + 1] == "نَ" for i in range(2, len(w) - 1))


def _sa(w: Atoms, _p: Atoms | None) -> bool:
    for i in (0, 1):
        if i == 1 and (not w or w[0] not in {"وَ", "فَ"}):
            break
        r = w[i:]
        if len(r) >= 4 and r[0] == "سَ" and r[1] in MUDARI:
            return True
    return False


def _bad_lam(_w: Atoms, p: Atoms | None) -> bool:
    return p in {("لَ", "مْ"), ("لَ", "نْ"), ("سَ", "وْ", "فَ")}


def _bad_fi(_w: Atoms, p: Atoms | None) -> bool:
    return p == ("فِ", "يْ")


HARF_LAFZ = frozenset({("ثُ", "مْ", "مَ"), ("سَ", "وْ", "فَ"), ("هَ", "لْ"), ("فِ", "يْ"), ("لَ", "مْ")})


def _harf(w: Atoms, _p: Atoms | None) -> bool:
    return w in HARF_LAFZ


SIGNS: dict[str, tuple[Pattern, frozenset[int]]] = {
    "AL": (_al, frozenset({ISM})),
    "TANWIN": (_tanwin, frozenset({ISM})),
    "TA_SAKINA": (_ta_sakina, frozenset({FIL})),
    "TA_FAIL": (_ta_fail, frozenset({FIL})),
    "YA_FAILA": (_ya_faila, frozenset({FIL})),
    "NUN_TAWKID": (_nun_tawkid, frozenset({FIL})),
    "SA": (_sa, frozenset({FIL})),
    "BAD_LAM_LAN_SAWFA": (_bad_lam, frozenset({FIL})),
    "BAD_FI": (_bad_fi, frozenset({ISM})),
    "HARF_LAFZ": (_harf, frozenset({HARF})),
}


Row = tuple[int, Atoms, Atoms | None, int, int]
"""(السورة، الذرّات، ذرّاتُ السابق، عددُ الشهادة، القسم)."""


def stems(data: bytes) -> dict[tuple[int, int, int], tuple[str, str] | None]:
    out: dict[tuple[int, int, int], tuple[str, str] | None] = {}
    for ln in data.decode("utf-8").splitlines():
        if not ln.startswith("("):
            continue
        loc, form, tag, feats = ln.split("\t")
        s, v, w, _g = (int(x) for x in loc.strip("()").split(":"))
        out.setdefault((s, v, w), None)
        if "STEM" in feats.split("|"):
            out[(s, v, w)] = (tag, form)
    return out


def population(rec: bool = False) -> tuple[list[Any], Counter[str]]:
    data = Q.source()
    st = stems(data)
    words = Q.qac_words(data)
    keys = sorted(words)
    lines = Q.CORPUS.read_text(encoding="utf-8").splitlines()
    assert len(keys) == len(lines), "QAC_VERSE_COUNT"
    rows: list[Row] = []
    names = ("ALIGN_RESIDUAL", "YA_JOINED", "REFUSED", "NO_STEM")
    excl: Counter[str] = Counter({k: 0 for k in names})
    for (s, v), line in zip(keys, lines, strict=True):
        raw = line.split(" ")
        gs, _ = Q.groups(s, v, raw)
        if len(gs) != len(words[(s, v)]):
            excl["ALIGN_RESIDUAL"] += 1
            continue
        certs: dict[int, Any] = {}
        for j, t in enumerate(raw):
            c = gate.enter(t.encode("utf-8"))
            certs[j] = None if isinstance(c, Refusal) else c
        for g, (w, _f) in zip(gs, words[(s, v)], strict=True):
            if len(g) != 1:
                excl["YA_JOINED"] += 1
                continue
            j = g[0]
            c = certs[j]
            if c is None:
                excl["REFUSED"] += 1
                continue
            stem = st[(s, v, w)]
            if stem is None:
                excl["NO_STEM"] += 1
                continue
            prev = certs.get(j - 1) if j > 0 else None
            p = tuple(prev.atoms) if prev is not None else None
            row = (s, tuple(c.atoms), p, int(c.integer), FT.code(*stem))
            if rec:
                row = (*row, bool(gate.recover(c, peel=True)[1]))
            rows.append(row)
    return rows, excl


def fires(name: str, r: Row) -> bool:
    return SIGNS[name][0](r[1], r[2])


def misfire(name: str, r: Row) -> bool:
    return fires(name, r) and r[4] not in SIGNS[name][1]


def cands(kept: Sequence[str], r: Row) -> tuple[int, ...]:
    return tuple(q for q in ALL if all(q in SIGNS[n][1] for n in kept if fires(n, r)))


def wilson(k: int, n: int) -> list[float]:
    if n == 0:
        return [0.0, 0.0]
    z = 1.959963984540054
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [round(c - h, 6), round(c + h, 6)]


def ceiling(rows: Sequence[Row], key: Callable[[Row], Any]) -> int:
    cnt: dict[Any, Counter[int]] = defaultdict(Counter)
    for r in rows:
        cnt[key(r)][r[4]] += 1
    return sum(max(c.values()) for c in cnt.values())


def compute() -> dict[str, Any]:
    rows, excl = population()
    a = [r for r in rows if r[0] % 2 == 1]
    b = [r for r in rows if r[0] % 2 == 0]
    sel: dict[str, dict[str, int | bool]] = {}
    kept: list[str] = []
    for name in SIGNS:
        f = sum(fires(name, r) for r in a)
        m = sum(misfire(name, r) for r in a)
        keep = f >= 1 and m * 100 <= f
        sel[name] = {"fires_A": f, "misfires_A": m, "kept": keep}
        if keep:
            kept.append(name)
    muayyan = sahih = muhtamal = la = 0
    for r in b:
        c = cands(kept, r)
        if len(c) == 1:
            muayyan += 1
            sahih += c[0] == r[4]
        elif c:
            muhtamal += 1
        else:
            la += 1
    misB = {n: sum(misfire(n, r) for r in b) for n in kept}
    learn: dict[Atoms, Counter[int]] = defaultdict(Counter)
    for r in a:
        learn[r[1]][r[4]] += 1
    m_hakim = m_sahih = 0
    for r in b:
        if r[1] in learn:
            c = learn[r[1]]
            best = max(ALL, key=lambda q: (c[q], -q))
            m_hakim += 1
            m_sahih += best == r[4]
    forms: dict[Atoms, set[int]] = defaultdict(set)
    for r in b:
        forms[r[1]].add(r[4])
    amb = sum(len(forms[r[1]]) > 1 for r in b)
    n = len(b)
    cc = ceiling(b, lambda r: r[1])
    cn = ceiling(b, lambda r: r[3])
    return {
        "prereg_sha256": hashlib.sha256(PREREG.read_bytes()).hexdigest(),
        "excluded": dict(sorted(excl.items())),
        "n_A": len(a),
        "n_B": n,
        "selection": sel,
        "kept": kept,
        "K": {"muayyan": muayyan, "muayyan_share": round(muayyan / n, 6),
              "sahih": sahih, "precision": round(sahih / muayyan, 6) if muayyan else None,
              "precision_wilson": wilson(sahih, muayyan),
              "muhtamal": muhtamal, "la_hukm": la,
              "wrong": muayyan - sahih, "misfires_B": misB,
              "wrong_le_sum_misfires": muayyan - sahih <= sum(misB.values())},
        "M": {"hakim": m_hakim, "sahih": m_sahih,
              "precision": round(m_sahih / m_hakim, 6) if m_hakim else None,
              "precision_wilson": wilson(m_sahih, m_hakim)},
        "ceiling_atoms": cc, "ceiling_atoms_share": round(cc / n, 6),
        "ceiling_atoms_wilson": wilson(cc, n),
        "ceiling_integer": cn, "ceiling_integer_share": round(cn / n, 6),
        "ambiguous_share": round(amb / n, 6),
        "H1_precision_ge_99": bool(muayyan) and sahih * 100 >= 99 * muayyan,
        "H2_integer_above_atoms": cn > cc,
        "H3_ceiling_below_100": cc < n,
    }


def render(res: dict[str, Any]) -> str:
    return json.dumps(res, ensure_ascii=False, indent=1, sort_keys=True) + "\n"


# ═══ التسجيلُ الثاني (`docs/qism-khanat/PREREG-2.md`، ADR ١٠٧) ═══

PREREG2 = ROOT / "docs" / "qism-khanat" / "PREREG-2.md"
RESULT2 = ROOT / "docs" / "qism-khanat" / "result-2.json"
AMR = ROOT / "formal" / "a116" / "amr.csv"
AWAMIL = ROOT / "corpora" / "awamil" / "awamil.tsv"
SKELETONS = ROOT / "corpora" / "hadith" / "maqayis-skeletons.tsv"

Row2 = tuple[int, Atoms, Atoms | None, int, int, bool]
"""(السورة، الذرّات، ذرّاتُ السابق، عددُ الشهادة، القسم، أقرأها `gate.recover`)."""

Slot = tuple[str, str]
"""(«R1»/«R2»/«R3»/«P» أو حرفٌ، والحركة أو «*» حرّة)."""


def roots() -> frozenset[str]:
    out = set()
    for ln in SKELETONS.read_text(encoding="utf-8").splitlines():
        out.add(ln.split("\t")[1])
    return frozenset(out)


def mudari_templates() -> list[list[Slot]]:
    """صفوفُ المضارع المرفوع للجذر «صبر» (رقمه 10) في `amr.csv`.

    ص ب ر ← R1 R2 R3، والأوّلُ حرفُ مضارعة."""
    out = []
    for ln in AMR.read_text(encoding="utf-8").splitlines():
        cols = ln.split(",")
        if cols[0] != "10":
            continue
        cells = cols[3].split(" ")
        slots: list[Slot] = [("P", cells[0][1:])]
        for c in cells[1:]:
            slots.append(({"ص": "R1", "ب": "R2", "ر": "R3"}.get(c[0], c[0]), c[1:]))
        slots[-1] = (slots[-1][0], "*")
        out.append(slots)
    return out


FAIL: list[Slot] = [("R1", F), ("ا", S), ("R2", K), ("R3", "*")]
MAFUL: list[Slot] = [("م", F), ("R1", S), ("R2", D), ("و", S), ("R3", "*")]


def fit(slots: Sequence[Slot], w: Atoms, rs: frozenset[str]) -> bool:
    if len(slots) != len(w):
        return False
    r: dict[str, str] = {}
    for (k, h), c in zip(slots, w, strict=True):
        if k == "P":
            if c not in MUDARI or c[1:] != h:
                return False
            continue
        if h != "*" and c[1:] != h:
            return False
        if k in ("R1", "R2", "R3"):
            if r.setdefault(k, c[0]) != c[0]:
                return False
        elif c[0] != k:
            return False
    return r["R1"] + r["R2"] + r["R3"] in rs


SUBJ = [(), ("وْ", "نَ"), ("يْ", "نَ"), ("اْ", "نِ"), ("وْ", "اْ"), ("وْ",), ("اْ",), ("يْ",)]


def heads(w: Atoms, first: frozenset[str], second: frozenset[str]) -> list[Atoms]:
    out = []
    for a in (0, 1):
        if a and (not w or w[0] not in first):
            continue
        for b in (0, 1):
            if b and (len(w) <= a or w[a] not in second):
                continue
            out.append(w[a + b:])
    return out


def mudari_wazn(w: Atoms, ts: list[list[Slot]], rs: frozenset[str]) -> bool:
    for body in heads(w, frozenset({"وَ", "فَ"}), frozenset({"لِ", "لَ", "سَ"})):
        for suf in SUBJ:
            if suf and body[-len(suf):] != suf:
                continue
            core = body[:len(body) - len(suf)]
            if any(fit(t, core, rs) for t in ts):
                return True
    return False


def articles(w: Atoms) -> list[Atoms]:
    out = [w]
    if w[:2] == ("ءَ", "لْ"):
        out.append(w[2:])
    if w[:1] == ("لْ",):
        out.append(w[1:])
    if len(w) >= 3 and w[0] == "ءَ" and w[1][1:] == S and w[2][0] == w[1][0]:
        out.append(w[2:])
    if len(w) >= 2 and w[0][1:] == S and w[1][0] == w[0][0]:
        out.append(w[1:])
    return out


ISM_TAILS = [(), ("نْ",), ("وْ", "نَ"), ("يْ", "نَ")] + [(t,) for t in ("تَ", "تُ", "تِ")] + [
    (t, "نْ") for t in ("تَ", "تُ", "تِ")]


def ism_wazn(w: Atoms, rs: frozenset[str]) -> bool:
    for body in heads(w, frozenset({"وَ", "فَ", "بِ", "كَ", "لِ"}), frozenset()):
        for core0 in articles(body):
            for suf in ISM_TAILS:
                if suf and core0[-len(suf):] != suf:
                    continue
                core = core0[:len(core0) - len(suf)]
                if fit(FAIL, core, rs) or fit(MAFUL, core, rs):
                    return True
    return False


HAMZA = frozenset("أإآءؤئ")
MARKS = {"َ": F, "ُ": D, "ِ": K, "ْ": S}
SHADDA = "ّ"

OWN: dict[str, int | None] = {"NASB_RAF": HARF, "RAF_NASB": FIL, "NASB_NASB": FIL, "RAF_TAWIL": FIL,
                              "JARR": HARF, "TABI": HARF, "NIDA": HARF, "JAZM_FIL": HARF,
                              "NASB_FIL": HARF, "JARR_OR_NASB": None, "JARR_OR_NASB_FIL": None}
NONE_OWN: dict[str, int] = {"لو": HARF, "هل": HARF, "مَن": ISM, "ما": ISM, "ماذا": ISM, "أيّ": ISM,
                            "كم": ISM, "كيف": ISM, "أين": ISM, "متى": ISM}
TARGET: dict[str, int | None] = {"NASB_RAF": ISM, "RAF_NASB": ISM, "NASB_NASB": ISM,
                                 "RAF_TAWIL": ISM, "JARR": ISM, "JARR_OR_NASB": ISM,
                                 "JARR_OR_NASB_FIL": ISM, "NIDA": ISM,
                                 "JAZM_FIL": FIL, "NASB_FIL": FIL, "JAZM_FILAYN": FIL,
                                 "TABI": None, "NONE": None}
"""`A116.Awamil.target` بعينه (الاختبارُ يطابقه بنصّ Lean)."""

Spec = list[tuple[str, frozenset[str] | None]]
"""لكلّ حرفٍ: الحرفُ، والحالاتُ المسموحة (None حرّة)."""


def amil_spec(name: str) -> Spec | None:
    name = name.split(" (")[0]
    if " " in name or name.startswith("ال"):
        return None
    out: Spec = []
    for i, ch in enumerate(name):
        if ch in MARKS:
            out[-1] = (out[-1][0], frozenset({MARKS[ch]}))
        elif ch == SHADDA:
            letter, h = out[-1]
            out[-1] = (letter, frozenset({S}))
            out.append((letter, h))
        else:
            letter = "ء" if ch in HAMZA else {"ى": "ا", "ة": "ت"}.get(ch, ch)
            h = None
            if i == 0 and ch == "إ":
                h = frozenset({K})
            elif i == 0 and ch == "أ":
                h = frozenset({F, D})
            out.append((letter, h))
    return out


def awamil() -> list[tuple[str, str, Spec]]:
    rows = []
    for ln in AWAMIL.read_text(encoding="utf-8").splitlines()[1:]:
        cols = ln.split("\t")
        spec = amil_spec(cols[0])
        if spec is not None:
            rows.append((cols[0].split(" (")[0], cols[3], spec))
    return rows


def matches(spec: Spec, w: Atoms) -> bool:
    if len(spec) != len(w):
        return False
    return all(c[0] == letter and (h is None or c[1:] in h)
               for (letter, h), c in zip(spec, w, strict=True))


def own_of(name: str, athar: str) -> int | None:
    if athar == "JAZM_FILAYN":
        return HARF if name == "إنْ" else ISM
    if athar == "NONE":
        return NONE_OWN.get(name)
    return OWN.get(athar)


def amil_own(athar: str, w: Atoms, rows: list[tuple[str, str, Spec]]) -> int | None:
    for body in heads(w, frozenset({"وَ", "فَ"}), frozenset()):
        hit = [(n, a) for n, a, sp in rows if matches(sp, body)]
        if any(a == athar for _n, a in hit):
            qs = {own_of(n, a) for n, a in hit}
            if len(qs) == 1 and None not in qs:
                return qs.pop()
    return None


def amil_next(athar: str, p: Atoms | None, rows: list[tuple[str, str, Spec]]) -> int | None:
    if p is None:
        return None
    hit = [a for _n, a, sp in rows if matches(sp, p)]
    if athar not in hit:
        return None
    qs = {TARGET[a] for a in hit}
    return qs.pop() if len(qs) == 1 and None not in qs else None


Sign2 = tuple[Callable[[Row2], bool], frozenset[int]]


def signs2() -> dict[str, Sign2]:
    rs = roots()
    ts = mudari_templates()
    rows = awamil()
    out: dict[str, Sign2] = {
        "VERB_RECOVER": (lambda r: r[5], frozenset({FIL})),
        "MUDARI_WAZN": (lambda r: mudari_wazn(r[1], ts, rs), frozenset({FIL})),
        "ISM_WAZN": (lambda r: ism_wazn(r[1], rs), frozenset({ISM})),
    }
    athars = sorted({a for _n, a, _s in rows})
    for a in athars:
        for q in ALL:
            out[f"AMIL_OWN_{a}_{q}"] = (
                lambda r, a=a, q=q: amil_own(a, r[1], rows) == q, frozenset({q}))
            out[f"AMIL_NEXT_{a}_{q}"] = (
                lambda r, a=a, q=q: amil_next(a, r[2], rows) == q, frozenset({q}))
    return out


FAMILY = {"VERB_RECOVER": "A", "MUDARI_WAZN": "A", "ISM_WAZN": "B"}


def population2() -> list[Row2]:
    return population(rec=True)[0]


def compute2() -> dict[str, Any]:
    rows = population2()
    a = [r for r in rows if r[0] % 2 == 1]
    b = [r for r in rows if r[0] % 2 == 0]
    old_kept = json.loads(RESULT.read_text(encoding="utf-8"))["kept"]
    sg: dict[str, Sign2] = {n: ((lambda r, n=n: SIGNS[n][0](r[1], r[2])), SIGNS[n][1])
                            for n in old_kept}
    new = signs2()
    sel: dict[str, dict[str, int | bool]] = {}
    kept_new: list[str] = []
    for name, (fn, keep) in new.items():
        f = m = 0
        for r in a:
            if fn(r):
                f += 1
                m += r[4] not in keep
        k = f >= 1 and m * 100 <= f
        if f:
            sel[name] = {"fires_A": f, "misfires_A": m, "kept": k}
        if k:
            kept_new.append(name)

    def family(n: str) -> str:
        return FAMILY.get(n, "C")

    def run(names: Sequence[str]) -> dict[str, Any]:
        allsg = {**sg, **{n: new[n] for n in names}}
        mu = sa = mh = la = 0
        mis = dict.fromkeys(allsg, 0)
        for r in b:
            fired = [(n, keep) for n, (fn, keep) in allsg.items() if fn(r)]
            for n, keep in fired:
                mis[n] += r[4] not in keep
            c = tuple(q for q in ALL if all(q in keep for _n, keep in fired))
            if len(c) == 1:
                mu += 1
                sa += c[0] == r[4]
            elif c:
                mh += 1
            else:
                la += 1
        return {"muayyan": mu, "muayyan_share": round(mu / len(b), 6), "sahih": sa,
                "precision": round(sa / mu, 6) if mu else None, "precision_wilson": wilson(sa, mu),
                "muhtamal": mh, "la_hukm": la, "wrong": mu - sa,
                "sum_misfires_B": sum(mis.values()),
                "wrong_le_sum_misfires": mu - sa <= sum(mis.values())}

    k2 = run(kept_new)
    contrib = {fam: run([n for n in kept_new if family(n) == fam])["muayyan"]
               for fam in ("A", "B", "C")}
    n = len(b)
    cc = ceiling(b, lambda r: r[1])  # type: ignore[arg-type,return-value]
    cp = ceiling(b, lambda r: (r[2], r[1]))  # type: ignore[arg-type,return-value]
    k_old = json.loads(RESULT.read_text(encoding="utf-8"))["K"]["muayyan"]
    return {
        "prereg_sha256": hashlib.sha256(PREREG2.read_bytes()).hexdigest(),
        "n_A": len(a), "n_B": n,
        "selection": sel, "kept_new": kept_new,
        "K2": k2, "muayyan_by_family_with_K": contrib,
        "ceiling_atoms": cc, "ceiling_atoms_share": round(cc / n, 6),
        "ceiling_prev_atoms": cp, "ceiling_prev_atoms_share": round(cp / n, 6),
        "H1_precision_ge_99": bool(k2["muayyan"]) and k2["sahih"] * 100 >= 99 * k2["muayyan"],
        "H2_more_than_K": k2["muayyan"] > k_old,
        "H3_prev_ceiling_above": cp > cc,
    }


def main(argv: list[str]) -> int:
    out = render(compute())
    out2 = render(compute2())
    if "--check" in argv:
        if RESULT.read_text(encoding="utf-8") != out:
            sys.stderr.write("QISM_KHANAT_RESULT_DRIFTED\n")
            return 1
        if not RESULT2.exists() or RESULT2.read_text(encoding="utf-8") != out2:
            sys.stderr.write("QISM_KHANAT_RESULT_2_DRIFTED\n")
            return 1
        sys.stdout.write("قياسا القسم من الخانات مطابقان\n")
        return 0
    RESULT.write_text(out, encoding="utf-8")
    RESULT2.write_text(out2, encoding="utf-8")
    sys.stdout.write(out2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
