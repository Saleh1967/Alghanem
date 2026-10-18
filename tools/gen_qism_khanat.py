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


def population() -> tuple[list[Row], Counter[str]]:
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
            rows.append((s, tuple(c.atoms), p, int(c.integer), FT.code(*stem)))
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


def main(argv: list[str]) -> int:
    out = render(compute())
    if "--check" in argv:
        if RESULT.read_text(encoding="utf-8") != out:
            sys.stderr.write("QISM_KHANAT_RESULT_DRIFTED\n")
            return 1
        sys.stdout.write("قياسُ القسم من الخانات مطابق\n")
        return 0
    RESULT.write_text(out, encoding="utf-8")
    sys.stdout.write(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
