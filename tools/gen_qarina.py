"""القرينةُ من «المخصَّص» مودَعةً للمشترك (ADR ٥٩): «استعمال اللفظ المشترك في أحد معانيه دون غيره …
يحتاج إلى قرينة مبينة تعيِّن المعنى المراد» (الشخصيّة ج3 ف423).

**الواقع.** مودَعان قائمان لا يُحرَّران هنا:

* `corpora/wad/wad.tsv` (ADR ٥٦، `tools/gen_wad.py --check`): علاقةُ الوضع؛ والمشتركُ لفظٌ له فيها
  جذران فأكثر.
* `corpora/mukhassas/membership.tsv` (ADR ٤٨، `tools/gen_mukhassas.py --check`): الجذرُ ← عُقَدُ
  «المخصَّص» التي ورد في نصّها لفظٌ بجذره (`RULE_M`). فالعقدةُ حقلُ معنًى وضعه ابنُ سيده،
  والجذرُ فيها بحكم ابن فارس.

**القاعدة** (`RULE_Q`):

* **حقلُ المعنى** `F(m)`: عُقَدُ جذر لين m في العضويّة، بعد ردّ ألف لين في الجذر همزةً (اوب = ءوب)
  وطيّ الهمزات، كما في `gen_wad.lane_root_as_ibn_faris`.
* **القرينةُ المبيِّنة** لمعنًى m من معاني لفظٍ: عقدةٌ في `F(m)` ليست في حقل معنًى آخر لذلك اللفظ
  (`A116.Qarina.Mub`). والحكمُ عليها في Lean لا هنا.

و`python tools/gen_qarina.py measure` يقيس قاعدةَ الاختيار على QAC بالتسجيل المسبق
`docs/qarina/PREREG.md` ويكتب `docs/qarina/result.json` (`QARINA_RESULT_DRIFTED` في `--check`).

يكتب `corpora/wad/qarina.tsv` (لكلّ جذرٍ من جذور المشترك: جذرُ لين، وصورتُه عند ابن فارس، وعُقَدُه) و
`formal/a116/A116/QarinaData.lean`؛ و`--check` يُسقط البناءَ بـ`QARINA_DEPOSIT_DRIFTED` أو
`QARINA_LEAN_DRIFTED`. معفاةٌ في الحارس لأنّها أداةُ إيداع.
"""

from __future__ import annotations

import importlib.util
import sys
from collections import Counter
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
WAD = ROOT / "corpora" / "wad" / "wad.tsv"
MEMBERSHIP = ROOT / "corpora" / "mukhassas" / "membership.tsv"
OUT = ROOT / "corpora" / "wad" / "qarina.tsv"
LEAN = ROOT / "formal" / "a116" / "A116" / "QarinaData.lean"
CORPUS = ROOT / "corpora" / "quran-simple-enhanced.txt"
RESULT = ROOT / "docs" / "qarina" / "result.json"

FOLD = {"أ": "ء", "إ": "ء", "ؤ": "ء", "ئ": "ء", "ى": "ي"}


def fold(s: str) -> str:
    return "".join(FOLD.get(c, c) for c in s.replace("آ", "ءا"))


def as_ibn_faris(root: str) -> str:
    """ألفُ لين في الجذر همزةٌ، والهمزاتُ مطويّة (`gen_wad.lane_root_as_ibn_faris` بعينها)."""

    return fold(root.replace("ا", "ء"))


def mushtarak() -> dict[str, list[str]]:
    """اللفظ ← جذورُه بترتيب المودَع، لما له جذران فأكثر."""

    by: dict[str, list[str]] = {}
    for ln in WAD.read_text(encoding="utf-8").splitlines():
        key, root, _ = ln.split("\t")
        by.setdefault(key, []).append(root)
    return {k: v for k, v in by.items() if len(v) >= 2}


def membership() -> dict[str, list[int]]:
    out: dict[str, list[int]] = {}
    for ln in MEMBERSHIP.read_text(encoding="utf-8").splitlines():
        r, ns = ln.split("\t")
        out[r] = [int(x) for x in ns.split(" ")]
    return out


def fields() -> list[tuple[str, str, list[int]]]:
    """(جذرُ لين، صورتُه عند ابن فارس، عُقَدُه) لكلّ جذرٍ من جذور المشترك، مرتّبًا."""

    mem = membership()
    roots = sorted({r for rs in mushtarak().values() for r in rs})
    return [(r, as_ibn_faris(r), mem.get(as_ibn_faris(r), [])) for r in roots]


def render_tsv(fs: list[tuple[str, str, list[int]]]) -> str:
    return "".join(f"{r}\t{f}\t{' '.join(map(str, ns))}\n" for r, f, ns in fs)


CHUNK = 16
"""صفوفٌ في كلّ قطعة: القائمةُ الواحدةُ الطويلة تتجاوز عمقَ المُعرِب."""


def rows(fs: list[tuple[str, str, list[int]]]) -> list[tuple[str, list[tuple[str, list[int]]]]]:
    """(اللفظ، [(الجذر، حقلُه)]) لكلّ لفظٍ مشترك، بترتيب المودَع."""

    f = {r: ns for r, _, ns in fs}
    mu = mushtarak()
    return [(k, [(r, f[r]) for r in mu[k]]) for k in sorted(mu)]


def render_lean(fs: list[tuple[str, str, list[int]]]) -> str:
    lines = [
        "/-! حقولُ المعنى لمعاني المشترك من «المخصَّص» — مولَّدٌ بـ`tools/gen_qarina.py` من",
        "`corpora/wad/wad.tsv` و`corpora/mukhassas/membership.tsv`،",
        "ويطابقه `tests/test_qarina.py`؛",
        "لا يُحرَّر باليد (ADR ٥٩). -/",
        "",
        "set_option autoImplicit false",
        "set_option maxRecDepth 100000",
        "",
        "namespace A116.QarinaData",
        "",
    ]
    rs = rows(fs)
    names = []
    for c in range(0, len(rs), CHUNK):
        name = f"chunk{c // CHUNK}"
        names.append(name)
        body = []
        for k, ms in rs[c:c + CHUNK]:
            assert '"' not in k and "\\" not in k
            inner = ", ".join(f'("{r}", [{", ".join(map(str, ns))}])' for r, ns in ms)
            body.append(f'  ("{k}", [{inner}])')
        lines += [f"def {name} : List (String × List (String × List Nat)) := [", ",\n".join(body),
                  "]", ""]
    lines += ["/-- (اللفظ المشترك، [(جذرُ لين، عُقَدُ «المخصَّص» التي ورد فيها جذرُه)])",
              "بترتيب `WadData`. -/",
              f"def rows : List (String × List (String × List Nat)) := {' ++ '.join(names)}",
              "", "end A116.QarinaData", ""]
    return "\n".join(lines)


# --- المرآة: `A116.Qarina` ---

Field = Callable[[str], Sequence[int]]


def mub(ms: Sequence[str], f: Field, q: int, m: str) -> bool:
    """`Qarina.Mub`: q في حقل m من معاني ms، ولا في حقل معنًى غيرِه منها."""

    return m in ms and q in f(m) and all(m2 == m or q not in f(m2) for m2 in ms)


def hits(ms: Sequence[str], f: Field, ctx: Sequence[int]) -> list[str]:
    """`Qarina.hits`: المعاني التي تبيّنها قرينةٌ حاضرة، بترتيب المعاني."""

    cs = set(ctx)
    return [m for m in ms if any(q in cs and mub(ms, f, q, m) for q in f(m))]


def choose(ms: Sequence[str], f: Field, ctx: Sequence[int]) -> str | None:
    """`Qarina.choose`: معنًى واحدٌ تبيّنه القرائنُ الحاضرة، وإلّا لا شيء."""

    hs = hits(ms, f, ctx)
    return hs[0] if hs and all(x == hs[0] for x in hs) else None


# --- القياس (التسجيلُ المسبق `docs/qarina/PREREG.md`) ---


def _load(name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, ROOT / "tools" / f"{name}.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules.setdefault(name, mod)
    spec.loader.exec_module(mod)
    return mod


def wy(root: str) -> str:
    """لامُ الناقص بلا تمييزٍ بين واوٍ وياء (الصنفُ الضعيف، `gen_qac.wy`)."""

    return root[:-1] + "ي" if root.endswith("و") else root


def agree(lane_root: str, gold: str) -> bool:
    """جذرُ لين يوافق جذرَ Dukes: بعد ردّ ألف لين همزةً وطيّ الهمزات، وبالصنف الضعيف."""

    return wy(as_ibn_faris(lane_root)) == wy(fold(gold))


def decide_row(ms: Sequence[str], f: Field, ctx: Sequence[int]) -> tuple[str, str | None]:
    """(الحكم، المعنى): `DECIDED` بمعنًى، أو `NO_QARINA`، أو `QARINA_CONFLICT`."""

    hs = hits(ms, f, ctx)
    if not hs:
        return "NO_QARINA", None
    m = choose(ms, f, ctx)
    return ("DECIDED", m) if m is not None else ("QARINA_CONFLICT", None)


def by_count(ms: Sequence[str], f: Field, ctx: Sequence[int]) -> str | None:
    """الثانويّ (وصفٌ لا حكم): المعنى الأكثرُ قرائنَ مبيِّنةً حاضرة، والتعادلُ لا شيء."""

    cs = set(ctx)
    score = {m: sum(1 for q in f(m) if q in cs and mub(ms, f, q, m)) for m in ms}
    best = max(score.values(), default=0)
    top = [m for m in ms if score[m] == best]
    return top[0] if best > 0 and len(top) == 1 else None


def by_field_size(ms: Sequence[str], f: Field) -> str | None:
    """الأساس: المعنى الأوسعُ حقلًا في «المخصَّص» بلا سياق، والتعادلُ لا شيء."""

    size = {m: len(f(m)) for m in ms}
    best = max(size.values(), default=0)
    top = [m for m in ms if size[m] == best]
    return top[0] if len(top) == 1 else None


def verdict(prec: list[float], chance: float, base: list[float], n_decided: int) -> str:
    if n_decided < 30:
        return "QARINA_TOO_FEW"
    bar = max(chance, base[1])
    if prec[0] > bar:
        return "QARINA_INFORMATIVE"
    if prec[1] <= bar:
        return "QARINA_NOT_INFORMATIVE"
    return "QARINA_UNDECIDED"


def measure() -> dict[str, object]:
    from gate import recover
    from gate.api import Gate, Refusal

    R: Any = _load("gen_lane_roots")
    Q = R.Q
    d = R.read_keys()
    g = Gate()
    mem = membership()

    def f(m: str) -> list[int]:
        return mem.get(as_ibn_faris(m), [])

    atoms_cache: dict[str, tuple[str, ...] | None] = {}

    def atoms(w: str) -> tuple[str, ...] | None:
        if w not in atoms_cache:
            c = g.enter(w.encode("utf-8"))
            atoms_cache[w] = (None if isinstance(c, Refusal)
                              else tuple(R.H.norm(x[0]) + x[1:] for x in c.atoms))
        return atoms_cache[w]

    def meanings(w: str) -> list[str]:
        a = atoms(w)
        return [] if a is None else list(d.get(R.key(a, w), []))

    nodes_cache: dict[str, frozenset[int]] = {}

    def nodes_of(w: str) -> frozenset[int]:
        """عُقَدُ جذور الكلمة بقراءة النظام `S3` (ADR ٥٠): المباشر، ثمّ معجمُ لين، ثمّ المقشِّر."""

        if w not in nodes_cache:
            rs = {x[0] for x in recover(w)[1]}
            if not rs:
                ms = meanings(w)
                rs = set(ms) if len(ms) == 1 else set()
            if not rs:
                rs = {x[0] for x in recover(w, peel=True)[1]}
            nodes_cache[w] = frozenset(q for r in rs for q in f(r))
        return nodes_cache[w]

    lines = CORPUS.read_text(encoding="utf-8").splitlines()
    seen = Q.seen()
    c: Counter[str] = Counter()
    k_base = k_count = n_count = 0
    chance = 0.0
    for r in Q.read_reference():
        if (r["line"], r["pos"]) in seen:
            continue
        w, gold = r["word"], r["root"]
        ms = meanings(w)
        if len(ms) < 2:
            continue
        c["population"] += 1
        if not any(agree(m, gold) for m in ms):
            c["GOLD_OUTSIDE_RELATION"] += 1
            continue
        c["in_relation"] += 1
        words = lines[int(r["line"]) - 1].split(" ")
        pos = int(r["pos"]) - 1
        assert words[pos] == w, (r["line"], r["pos"])
        ctx = sorted(set().union(*[nodes_of(x) for i, x in enumerate(words) if i != pos]))
        state, m = decide_row(ms, f, ctx)
        c[state] += 1
        mc = by_count(ms, f, ctx)
        if mc is not None:
            n_count += 1
            k_count += agree(mc, gold)
        if state == "DECIDED":
            assert m is not None
            c["correct" if agree(m, gold) else "wrong"] += 1
            mb = by_field_size(ms, f)
            k_base += mb is not None and agree(mb, gold)
            chance += 1 / len(ms)
    n_dec = c["DECIDED"]
    prec = Q.wilson(c["correct"], n_dec)
    base = Q.wilson(k_base, n_dec)
    ch = round(chance / n_dec, 6) if n_dec else 0.0
    return {
        "prereg": "docs/qarina/PREREG.md", "reference": "QAC 0.4 (Dukes)",
        "outcomes": dict(sorted(c.items())),
        "precision": {"k": c["correct"], "n": n_dec,
                      "rate": round(c["correct"] / n_dec, 6) if n_dec else None, "wilson95": prec},
        "coverage": {"k": n_dec, "n": c["in_relation"],
                     "rate": round(n_dec / c["in_relation"], 6) if c["in_relation"] else None,
                     "wilson95": Q.wilson(n_dec, c["in_relation"])},
        "baseline_field_size_on_decided": {"k": k_base, "n": n_dec, "wilson95": base},
        "baseline_chance_on_decided": ch,
        "secondary_by_count": {"k": k_count, "n": n_count, "wilson95": Q.wilson(k_count, n_count),
                               "coverage_over_in_relation": round(n_count / c["in_relation"], 6)
                               if c["in_relation"] else None},
        "verdict": verdict(prec, ch, base, n_dec),
    }


def dump(obj: object) -> str:
    import json

    return json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=True) + "\n"



def main(argv: list[str]) -> int:
    fs = fields()
    tsv, lean = render_tsv(fs), render_lean(fs)
    if "--check" in argv:
        bad = 0
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != tsv:
            sys.stderr.write("QARINA_DEPOSIT_DRIFTED: شغّل python tools/gen_qarina.py\n")
            bad = 1
        if not LEAN.exists() or LEAN.read_text(encoding="utf-8") != lean:
            sys.stderr.write("QARINA_LEAN_DRIFTED: شغّل python tools/gen_qarina.py\n")
            bad = 1
        if not bad and RESULT.exists() and RESULT.read_text(encoding="utf-8") != dump(measure()):
            sys.stderr.write("QARINA_RESULT_DRIFTED\n")
            bad = 1
        if not bad:
            state = "مطابقة" if RESULT.exists() else "لم تُقس بعد"
            sys.stdout.write(f"القرينة مطابقة: {len(fs)} جذرًا من جذور المشترك؛ النتيجة {state}\n")
        return bad
    if argv[:1] == ["measure"]:
        RESULT.parent.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(dump(measure()), encoding="utf-8")
        sys.stdout.write(f"كُتب {RESULT.relative_to(ROOT)}\n")
        return 0
    OUT.write_text(tsv, encoding="utf-8")
    LEAN.write_text(lean, encoding="utf-8")
    sys.stdout.write(f"كُتب {OUT.name} و{LEAN.name} ({len(fs)} جذرًا)\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
