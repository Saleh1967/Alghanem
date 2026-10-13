"""جذورُ لين مرجعًا بالحركات: فصلُ خطأ النظام عن خطأ المرجع (ADR ٤٩، تسجيلٌ مسبق
`docs/lane-roots/PREREG.md`).

**المشكلة** (ADR ٤٧، `REFERENCE_HOMOGRAPH`): مرجعُ الجذر في الصحيحين نقلُ حكم ابن فارس
**بالهيكل**، والهيكلُ لا يفرّق المتجانسين (قالوا ← قلو)؛ فالفرقُ بين 87.24٪ على الصحيحين و95.58٪
على المصحف يجمع خطأَ `gate.recover` وخطأَ المرجع ولا يفصلهما. **والحلّ**: مرجعٌ بشريٌّ ثانٍ مستقلّ
يحكم **بالحركات** لا بالهيكل — معجمُ لين المختوم (ADR ٣٣): كلُّ صيغةٍ وضعها لين رأسًا (`orth`) أو
مفتاحَ مدخلٍ تحت جذر، تدخل البوّابةَ على مجاله فتصير **خاناتٍ بحركاتها**؛ ويُنقل جذرُها إلى موضعٍ
في المصحف أو الصحيحين خاناتُه خاناتُها (إلّا حركةَ الإعراب الأخيرة والتنوين) **بجذرٍ واحد**
(`RULE_L`).

القياساتُ (معلنةٌ في التسجيل):

1. **جودةُ المرجع** على المصحف مقابلَ QAC (وسمُ Dukes البشريّ للموضع) حيث يقعان — ومرجعُ ابن فارس
   على المواضع نفسِها للمقارنة.
2. **النظامُ على الصحيحين** مقابلَ مرجع لين: اتّفاقُ `gate.recover(word, peel=True)` على ما يُقرأ.
3. **التفكيك**: حيث للموضع مرجعا لين وابن فارس ويقرؤه النظام — إن خالف النظامُ ابنَ فارس، أيوافق
   لينُ النظامَ (خطأُ مرجعٍ بالهيكل) أم ابنَ فارس (خطأُ نظام)؟
4. **المعايرة**: النظامُ على المصحف مقابلَ مرجع لين.

`python tools/gen_lane_roots.py` يكتب المعجمَ `corpora/lane/lane-root-keys.tsv`؛ و`measure` يكتب
`docs/lane-roots/result.json`؛ و`--check` يُسقط البناءَ بـ`LANE_ROOT_KEYS_DRIFTED` أو
`LANE_ROOTS_RESULT_DRIFTED`. معفاةٌ في الحارس لأنّها أداةُ إيداع.
"""

from __future__ import annotations

import importlib.util
import sys
from collections import Counter, defaultdict
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


L: Any = _load("gen_lane")
H: Any = _load("gen_lane_hasr")
HR: Any = _load("gen_hadith_roots")
Q = HR.Q

KEYS = L.LANE / "lane-root-keys.tsv"
RESULT = ROOT / "docs" / "lane-roots" / "result.json"
WEAK = frozenset("وي")
WEAK_SURFACE = frozenset("ويا")


# --- ١. المفتاحُ والقاعدة -------------------------------------------------------------------------


def key(atoms: tuple[str, ...], word: str) -> tuple[str, ...]:
    """خاناتُ الكلمة بلا نون التنوين (إن خُتم الرسمُ بتنوين) وبلا حركة الخانة الأخيرة (إعرابٌ أو
    وقف)."""

    a = atoms
    if word and word[-1] in L.TANWIN and a and a[-1] == "نْ":
        a = a[:-1]
    if not a:
        return ()
    return a[:-1] + (a[-1][0],)


def radicals_in(carriers: str, rad: str) -> bool:
    """`RULE_L`: أصولُ الجذر في حوامل الكلمة بترتيبها؛ والأصلُ المعتلّ (و، ي) قد يظهر واوًا أو
    ياءً أو ألفًا أو يسقط.
    حارسٌ يُسقط ما ليس من الجذر في المدخل (كلماتُ الشواهد)، لا حكمٌ بالجذر: الحكمُ وضعُ لين للصيغة
    تحت جذرها."""

    def go(i: int, k: int) -> bool:
        if k == len(rad):
            return True
        r = rad[k]
        if r in WEAK and go(i, k + 1):
            return True
        for j in range(i, len(carriers)):
            c = carriers[j]
            if c == r or (r in WEAK and c in WEAK_SURFACE):
                if go(j + 1, k + 1):
                    return True
        return False

    return go(0, 0)


# --- ٢. المعجم -----------------------------------------------------------------------------------


def lane_forms() -> list[tuple[str, str]]:
    """(الجذرُ بأصوله، الصيغة) لكلّ رأسٍ (`orth`) ومفتاحِ مدخلٍ في جذرٍ ثلاثيٍّ من لين؛ والمفتاحُ
    المختومُ بـ«هُ» يدخل
    بلا الضمير أيضًا."""

    out: list[tuple[str, str]] = []
    for name in sorted(L.LANE_SOURCES):
        for head, d in L.roots(name):
            st = H.stratum(head)
            if st is None:
                continue
            rad = st[1]
            for e in d.iter("entryFree"):
                k = (e.get("key") or "").strip()
                if k and not any(c.isspace() for c in k):
                    out.append((rad, k))
                    if k.endswith(L.PRONOUN) and len(k) > len(L.PRONOUN):
                        out.append((rad, k[: -len(L.PRONOUN)]))
            for o in d.iter("orth"):
                if o.get("lang") != "ar":
                    continue
                w = "".join(o.itertext()).strip()
                if w and not any(c.isspace() for c in w):
                    out.append((rad, w))
    return out


def lexicon() -> dict[tuple[str, ...], set[str]]:
    """مفتاحُ الخانات ← جذورُ لين التي وضع صيغتَه تحتها (بحارس `RULE_L`)."""

    from gate.api import LANE_CORPUS, Gate, Refusal, sealed_forms
    from gate.residue import repair

    pairs = lane_forms()
    sealed = sealed_forms(LANE_CORPUS)
    gate = Gate(corpus=LANE_CORPUS, domain={repair(w)[0] for _, w in pairs} & sealed)
    cache: dict[str, tuple[str, ...] | None] = {}
    out: dict[tuple[str, ...], set[str]] = defaultdict(set)
    for rad, w in pairs:
        if w not in cache:
            c = gate.enter(w.encode("utf-8"))
            cache[w] = (None if isinstance(c, Refusal)
                        else tuple(H.norm(x[0]) + x[1:] for x in c.atoms))
        a = cache[w]
        if a is None:
            continue
        k = key(a, w)
        if k and radicals_in("".join(x[0] for x in a), rad):
            out[k].add(rad)
    return dict(out)


def render(d: dict[tuple[str, ...], set[str]]) -> str:
    return "".join(f"{' '.join(k)}\t{' '.join(sorted(v))}\n" for k, v in sorted(d.items()))


def read_keys() -> dict[tuple[str, ...], list[str]]:
    out: dict[tuple[str, ...], list[str]] = {}
    for ln in KEYS.read_text(encoding="utf-8").splitlines():
        k, roots = ln.split("\t")
        out[tuple(k.split(" "))] = roots.split(" ")
    return out


# --- ٣. القياس ------------------------------------------------------------------------------------


def ref_of(d: dict[tuple[str, ...], list[str]], atoms: tuple[str, ...] | None, word: str
           ) -> str | None:
    """جذرُ لين للموضع إن كان لخاناته جذرٌ واحد؛ وإلّا لا شيء."""

    if atoms is None:
        return None
    roots = d.get(key(atoms, word))
    return roots[0] if roots and len(roots) == 1 else None


def system_roots(word: str) -> set[str]:
    from gate import recover

    return {r[0] for r in recover(word, peel=True)[1]}


def same(a: str, b: str) -> bool:
    return HR.wy(a) == HR.wy(b)


def rate(k: int, n: int) -> dict[str, object]:
    return {"k": k, "n": n, "rate": round(k / n, 6) if n else None, "wilson95": Q.wilson(k, n)}


def judge_all(items: list[tuple[str, str]], gate_obj: Any) -> dict[str, object]:
    """(الكلمة، الجذرُ المرجع) ← حصيلةُ النظام: اتّفاقٌ حرفًا / بالصنف الضعيف / خلاف / بلا قراءة /
    مرفوض."""

    from gate import Refusal

    c: Counter[str] = Counter()
    for w, ref in items:
        if isinstance(gate_obj.enter(w.encode("utf-8")), Refusal):
            c["refused"] += 1
            continue
        rs = system_roots(w)
        if not rs:
            c["no_reading"] += 1
        elif ref in rs:
            c["agree_exact"] += 1
        elif any(same(ref, r) for r in rs):
            c["agree_weak_class"] += 1
        else:
            c["disagree"] += 1
    read = c["agree_exact"] + c["agree_weak_class"] + c["disagree"]
    return {"n": len(items), "outcomes": dict(sorted(c.items())),
            "primary_agree_weak_class_among_read":
                rate(c["agree_exact"] + c["agree_weak_class"], read),
            "agree_exact_among_read": rate(c["agree_exact"], read),
            "coverage_read": round(read / len(items), 6) if items else None}


def measure() -> dict[str, object]:
    from gate.api import HADITH_CORPUS, Gate, Refusal

    d = read_keys()
    sk = HR.read_skeletons()

    def maq(w: str) -> str | None:
        roots = sk.get(HR.skeleton(w))
        return roots[0] if roots and len(roots) == 1 else None

    # ١، ٤: المصحف
    gq = Gate()
    qrows = [r for r in Q.read_reference() if (r["line"], r["pos"]) not in Q.seen()]
    q_atoms: dict[str, tuple[str, ...] | None] = {}

    def atoms_q(w: str) -> tuple[str, ...] | None:
        if w not in q_atoms:
            c = gq.enter(w.encode("utf-8"))
            q_atoms[w] = (None if isinstance(c, Refusal)
                          else tuple(H.norm(x[0]) + x[1:] for x in c.atoms))
        return q_atoms[w]

    qual_lane = Counter[str]()
    qual_maq = Counter[str]()
    q_items: list[tuple[str, str]] = []
    for r in qrows:
        w, gold = r["word"], r["root"]
        lr = ref_of(d, atoms_q(w), w)
        if lr is not None:
            q_items.append((w, lr))
            qual_lane["n"] += 1
            qual_lane["exact"] += lr == gold
            qual_lane["weak"] += same(lr, gold)
            mr = maq(w)
            if mr is not None:
                qual_maq["n"] += 1
                qual_maq["exact"] += mr == gold
                qual_maq["weak"] += same(mr, gold)
                qual_maq["lane_weak_same_positions"] += same(lr, gold)

    # ٢، ٣: الصحيحان
    gh = Gate(corpus=HADITH_CORPUS)
    skip = HR.seen()
    h_atoms: dict[str, tuple[str, ...] | None] = {}
    h_items: list[tuple[str, str]] = []
    status: Counter[str] = Counter()
    both: list[tuple[str, str, str]] = []
    for line, pos, w in HR.positions():
        if (line, pos) in skip:
            status["excluded_seen"] += 1
            continue
        if w not in h_atoms:
            c = gh.enter(w.encode("utf-8"))
            h_atoms[w] = (None if isinstance(c, Refusal)
                          else tuple(H.norm(x[0]) + x[1:] for x in c.atoms))
        lr = ref_of(d, h_atoms[w], w)
        if lr is None:
            status["no_lane_reference"] += 1
            continue
        status["lane_reference"] += 1
        h_items.append((w, lr))
        mr = maq(w)
        if mr is not None:
            both.append((w, lr, mr))

    sys_cache: dict[str, set[str]] = {}

    def sysr(w: str) -> set[str]:
        if w not in sys_cache:
            sys_cache[w] = system_roots(w)
        return sys_cache[w]

    dec: Counter[str] = Counter()
    against: Counter[tuple[str, str, str]] = Counter()
    for w, lr, mr in both:
        rs = sysr(w)
        if not rs:
            continue
        s_m = any(same(mr, r) for r in rs)
        s_l = any(same(lr, r) for r in rs)
        dec["read"] += 1
        dec["refs_agree"] += same(lr, mr)
        if s_m:
            dec["system_agrees_maqayis"] += 1
            continue
        dec["system_disagrees_maqayis"] += 1
        if s_l:
            dec["lane_sides_with_system"] += 1      # خطأُ المرجع بالهيكل
        elif same(lr, mr):
            dec["lane_sides_with_maqayis"] += 1     # خطأُ النظام
            against[(w, mr, " ".join(sorted(rs)))] += 1
        else:
            dec["three_way"] += 1
    wrong = dec["system_disagrees_maqayis"]
    return {
        "prereg": "docs/lane-roots/PREREG.md",
        "lane_lines_sha256": L.sha(L.render(L.lines())),
        "lexicon": {"keys": len(d), "unique": sum(1 for v in d.values() if len(v) == 1)},
        "reference_quality_vs_qac": {
            "lane": {"exact": rate(qual_lane["exact"], qual_lane["n"]),
                     "weak_class": rate(qual_lane["weak"], qual_lane["n"])},
            "maqayis_same_positions": {
                "exact": rate(qual_maq["exact"], qual_maq["n"]),
                "weak_class": rate(qual_maq["weak"], qual_maq["n"]),
                "lane_weak_class_on_these": rate(qual_maq["lane_weak_same_positions"],
                                                 qual_maq["n"])}},
        "quran_system_vs_lane": judge_all(q_items, gq),
        "sahihain_positions": dict(sorted(status.items())),
        "sahihain_system_vs_lane": judge_all(h_items, gh),
        "decomposition": {
            "counts": dict(sorted(dec.items())),
            "share_reference_error": rate(dec["lane_sides_with_system"], wrong),
            "share_system_error": rate(dec["lane_sides_with_maqayis"], wrong),
            "share_three_way": rate(dec["three_way"], wrong)},
        # بعد التسجيل (ADR ٤٩): وصفُ ما اتّفق فيه المرجعان على خلاف النظام — الصورُ الأكثرُ تكرارًا
        "post_registration_refs_agree_against_system": {
            "distinct_words": len(against),
            "top": [{"word": w, "reference": mr, "system": rs, "count": c}
                    for (w, mr, rs), c in sorted(against.items(),
                                                 key=lambda x: (-x[1], x[0]))[:15]]},
    }


def main(argv: list[str]) -> int:
    if "--check" in argv:
        bad: list[str] = []
        if KEYS.read_text(encoding="utf-8") != render(lexicon()):
            bad.append("LANE_ROOT_KEYS_DRIFTED")
        if RESULT.exists() and RESULT.read_text(encoding="utf-8") != Q.dump(measure()):
            bad.append("LANE_ROOTS_RESULT_DRIFTED")
        if bad:
            sys.stderr.write(", ".join(bad) + "\n")
            return 1
        sys.stdout.write(f"معجمُ جذور لين مطابق: {len(read_keys()):,} مفتاحًا؛ النتيجة "
                         f"{'مطابقة' if RESULT.exists() else 'لم تُقس بعد'}\n")
        return 0
    if argv[:1] == ["measure"]:
        RESULT.parent.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(Q.dump(measure()), encoding="utf-8")
        sys.stdout.write(f"كُتب {RESULT.relative_to(ROOT)}\n")
        return 0
    KEYS.write_text(render(lexicon()), encoding="utf-8")
    sys.stdout.write(f"كُتب {KEYS.relative_to(ROOT)}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
