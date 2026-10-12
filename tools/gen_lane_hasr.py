"""الحصرُ على معجم لين: حلولٌ رياضيّةٌ لديون القياس المسمّاة (ADR ٣٧، تسجيلٌ ثانٍ
`docs/lane/PREREG-2.md`).

القياسُ الأوّل (`tools/gen_lane.py`، ADR ٣٣) يبقى كما سُجّل لا يُمسّ؛ وهذه الأداةُ **تحليلُ حساسيّةٍ
مسجَّلٌ بعد رؤية نتيجته**، يحلّ كلَّ دَينٍ مسمًّى بأداةٍ رياضيّة لا بتخمين:

1. `LANE_DOMAIN_MISS_UNEXPLAINED` — **سببُه** (لا رياضة): الفعلُ المتعدّي كان يُنزع منه «هُ» نصًّا
   فيصير صورةً ليست في المجال المختوم (نَطَبَهُ ← نَطَبَ) فيُرفض فيُستبعد؛ فالمتعدّي كان منقوصًا من
   المجتمع. **العلاج على الخانات**: تدخل الكلمةُ كما كُتبت (`key_surface`) وتُنزع ذرّةُ «هُ» من آخر
   الشهادة.
2. `LANE_TRANSITIVITY_IS_HEADWORD_MARK` — **الحصرُ الجزئيّ** (`A116.Hasr.hasr`): ما لم يُعلَّم «هُ»
   مجهولُ التعدية؛ فلكلّ مدخلٍ إصابتان (لازمًا ومتعدّيًا)، والعددُ لكلّ تعيينٍ ممكن بين «كلتاهما»
   و«إحداهما» — والحدّان يُبلَغان (`hasr_tight_low`، `hasr_tight_high`).
3. `EXAMPLE_VOCALIZATION_AMBIGUOUS` — **الاطّراد** (`A116.Hasr.countP_mono`، `hasr_mono`): القواعدُ
   من الاستخراج الصارم (القياس الأوّل) حدٌّ أدنى، ومن المُرخى (كلُّ وسمٍ في مدخل المثال حروفُه حروفُ
   المثال، بكلّ تشكيلٍ عند لين) حدٌّ أعلى؛ فالإصابةُ بأيّ اختيارٍ بينهما محصورةٌ بين عدّيهما.
4. `LANE_ONLY_SOUND_TRILITERAL` — **الطبقات**: المهموزُ (الهمزةُ حاملٌ واحد `ء` في الشهادة،
   `A116.Hamza`) والمضعّفُ (الشدّةُ ذرّتان في الشهادة، فالجذرُ ف ع ع يُطابَق بترتيبه) يُقاسان كلٌّ
   في طبقته؛ والمعتلُّ **لا وزنَ له من الخانات مع الجذر وحدَه** —
   `A116.Neutral.neutral_forgets_weak` و`A116.Dal.no_cell_function_recovers_root` يبرهنان أنّ
   الخانات تنسى الحرفَ المعتلّ — فيُعدّ ولا يُقاس (`WEAK_STRATUM_NOT_PATTERNABLE`).
5. `HARAKA_SHARE_NOT_MEASURED` — **التفكيك**: دقّةُ أفضلِ جدول بحثٍ (الأغلبيّة) تحت **ترك واحدٍ
   خارجًا** (LOO، فلا يُقاس الجدولُ على ما بُني منه) بثلاث معلومات متداخلة: لا شيء ⊂ الهيكل (حروفُ
   الوزن بلا حركات) ⊂ الوزنُ كاملًا؛ فنصيبُ «القوانين بلا حركة» = الثاني − الأوّل، ونصيبُ الحركة =
   الثالث − الثاني (نقاطًا مئويّة)؛ ومعه المعلومةُ المتبادلة بالبِت: ‎H(P) − H(P|هيكل)‎ و‎H(P|هيكل)
   − H(P|وزن)‎ (تقديرٌ مباشرٌ متحيّزٌ إلى الأعلى، معلَن).

`python tools/gen_lane_hasr.py` يكتب `corpora/lane/lane-masdar-v2.tsv` و`lane-plural-v2.tsv`؛
`measure` يكتب `docs/lane/hasr.json`؛ و`--check` يُسقط البناءَ بـ`LANE_HASR_RECORDS_DRIFTED`
و`LANE_HASR_RESULT_DRIFTED`. معفاةٌ في الحارس لأنّها أداةُ إيداع.
"""

from __future__ import annotations

import importlib.util
import math
import sys
from collections import Counter, defaultdict
from collections.abc import Iterable
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
_SPEC = importlib.util.spec_from_file_location("gen_lane", ROOT / "tools" / "gen_lane.py")
assert _SPEC and _SPEC.loader
L: Any = importlib.util.module_from_spec(_SPEC)
sys.modules.setdefault("gen_lane", L)
_SPEC.loader.exec_module(L)

MASDAR_V2 = L.LANE / "lane-masdar-v2.tsv"
PLURAL_V2 = L.LANE / "lane-plural-v2.tsv"
RESULT_V2 = ROOT / "docs" / "lane" / "hasr.json"
HAMZA = frozenset("أإؤئآء")
WEAKS = frozenset("اويىٱ")
MASDAR_V2_HEADER = ["stratum", "file", "entry", "head", "radicals", "key", "transitive", "masadir"]
PLURAL_V2_HEADER = ["stratum", "file", "entry", "head", "radicals", "singular", "plurals"]


def norm(s: str) -> str:
    """صورُ الهمزة كلُّها حاملٌ واحد `ء` — كما في ذرّات الشهادة."""

    return "".join("ء" if c in HAMZA else c for c in s)


def stratum(head: str) -> tuple[str, str] | None:
    """(الطبقة، الأصولُ الثلاثة) من رأس الجذر عند لين؛ ولا شيء لغير الثلاثيّ."""

    h = norm(head)
    if len(h) == 3 and len(set(h)) == 3:
        rad = h
    elif len(h) == 2 and h[0] != h[1]:
        rad = h + h[1]
    else:
        return None
    if set(rad) & WEAKS:
        return ("weak", rad)
    if len(h) == 2:
        return ("doubled", rad)
    if "ء" in rad:
        return ("hamzated", rad)
    return ("sound", rad)


def records_v2() -> tuple[list[list[str]], list[list[str]], Counter[str]]:
    masdar: list[list[str]] = []
    plural: list[list[str]] = []
    weak: Counter[str] = Counter()
    for name in sorted(L.LANE_SOURCES):
        for head, d in L.roots(name):
            st = stratum(head)
            if st is None:
                continue
            kind, rad = st
            hn = norm(head)
            for e in d.iter("entryFree"):
                key = (e.get("key") or "").strip()
                if not key or any(c.isspace() for c in key):
                    continue
                it = e.find("form/itype")
                toks = L.stream(e)
                if it is not None and (it.text or "").strip() == "1":
                    trans = key.endswith(L.PRONOUN)
                    verb = key[: -len(L.PRONOUN)] if trans else key
                    if norm(L.letters(verb)) != hn:
                        continue
                    ms = [s.strip() for s in L.spans_after(toks, L.INF) if L.cited_noun(s)]
                    if not ms:
                        continue
                    if kind == "weak":
                        weak["masdar"] += 1
                        continue
                    masdar.append([kind, name, e.get("id") or "", head, rad, key,
                                   "1" if trans else "0", " ".join(ms)])
                elif it is None:
                    if norm(L.letters(key)) not in (hn, hn + "ة"):
                        continue
                    ps = [s.strip() for s in L.spans_after(toks, L.PL) if L.cited_noun(s)]
                    if not ps:
                        continue
                    if kind == "weak":
                        weak["plural"] += 1
                        continue
                    plural.append([kind, name, e.get("id") or "", head, rad, key, " ".join(ps)])
    return masdar, plural, weak


def relaxed_candidates() -> tuple[dict[tuple[str, str], list[tuple[str, str]]],
                                  dict[tuple[str, str], list[tuple[str, str]]]]:
    """الاستخراجُ المُرخى لأمثلة القواعد: كلُّ وسمٍ عربيٍّ مذكورٍ اسمًا في مدخل المثال حروفُه حروفُ
    المثال."""

    mroots = {r for _, r, _ in L.MASDAR_RULES}
    proots = {s[:3] for s, _ in L.PLURAL_RULES}
    mc: dict[tuple[str, str], list[tuple[str, str]]] = defaultdict(list)
    pc: dict[tuple[str, str], list[tuple[str, str]]] = defaultdict(list)
    for name in sorted(L.LANE_SOURCES):
        for head, d in L.roots(name):
            if head not in mroots and head not in proots:
                continue
            for e in d.iter("entryFree"):
                key = (e.get("key") or "").strip()
                if not key or any(c.isspace() for c in key):
                    continue
                spans = [t for k, t in L.stream(e) if k == "ar" and L.cited_noun(t)]
                it = e.find("form/itype")
                if head in mroots and it is not None and (it.text or "").strip() == "1":
                    for cls, root, ml in L.MASDAR_RULES:
                        if root == head:
                            mc[(cls, root)] += [(key, s.strip()) for s in spans
                                                if L.letters(s.strip()) == ml]
                if head in proots and it is None:
                    for sing, pl in L.PLURAL_RULES:
                        if sing[:3] == head and L.letters(key) == sing:
                            pc[(sing, pl)] += [(key, s.strip()) for s in spans
                                               if L.letters(s.strip()) == pl]
    return mc, pc


def loo_majority(rows: Iterable[tuple[Any, str]]) -> tuple[int, int]:
    """دقّةُ جدول الأغلبيّة بترك واحدٍ خارجًا: لكلّ صفٍّ، الأغلبُ في صفوف خانته الأخرى، والتعادلُ
    بالأصغر ترتيبًا؛ والصفُّ وحيدُ خانته لا يُصيب."""

    rows = list(rows)
    by: dict[Any, Counter[str]] = defaultdict(Counter)
    for f, y in rows:
        by[f][y] += 1
    hit = 0
    for f, y in rows:
        c = by[f].copy()
        c[y] -= 1
        best = sorted(((-n, k) for k, n in c.items() if n > 0))
        if best and best[0][1] == y:
            hit += 1
    return hit, len(rows)


def cond_entropy(rows: Iterable[tuple[Any, str]]) -> float:
    rows = list(rows)
    by: dict[Any, Counter[str]] = defaultdict(Counter)
    for f, y in rows:
        by[f][y] += 1
    n = len(rows)
    h = 0.0
    for c in by.values():
        m = sum(c.values())
        for k in c.values():
            h -= (k / n) * math.log2(k / m)
    return h


def skeleton(p: str) -> str:
    return " ".join("".join(ch for ch in a if ch not in L.HARAKAT) for a in p.split())


def share(h: int, n: int) -> dict[str, object]:
    return {"hits": h, "n": n, "rate": round(h / n, 4) if n else None,
            "ci95": L.wilson(h, n), "transmitted": round(1 - h / n, 4) if n else None}


def bounds(lo: int, hi: int, n: int) -> dict[str, object]:
    """حصرُ المنقول: [1 − الأعلى، 1 − الأدنى]، وفاصلا Wilson للطرفين."""

    return {"n": n, "hits_low": lo, "hits_high": hi,
            "transmitted_low": round(1 - hi / n, 4) if n else None,
            "transmitted_high": round(1 - lo / n, 4) if n else None,
            "ci95_low_end": L.wilson(hi, n), "ci95_high_end": L.wilson(lo, n)}


def measure() -> dict[str, object]:
    from gate.api import LANE_CORPUS, Gate, Refusal, sealed_forms
    from gate.residue import repair

    masdar = L.read_tsv(MASDAR_V2)
    plural = L.read_tsv(PLURAL_V2)
    mc, pc = relaxed_candidates()
    words: set[str] = set()
    for r in masdar:
        words.add(r[5])
        words.update(r[7].split())
    for r in plural:
        words.add(r[5])
        words.update(r[6].split())
    for v in list(mc.values()) + list(pc.values()):
        for a, b in v:
            words.update((a, b))
    sealed = sealed_forms(LANE_CORPUS)
    gate = Gate(corpus=LANE_CORPUS, domain={repair(w)[0] for w in words} & sealed)
    refusals: Counter[str] = Counter()
    cache: dict[str, tuple[str, ...] | None] = {}

    def atoms(w: str) -> tuple[str, ...] | None:
        if w not in cache:
            c = gate.enter(w.encode("utf-8"))
            if isinstance(c, Refusal):
                refusals[c.status + ":" + ",".join(c.reasons)] += 1
                cache[w] = None
            else:
                cache[w] = tuple(c.atoms)
        return cache[w]

    def pat(w: str, rad: str) -> str | None:
        a = atoms(w)
        return None if a is None else L.pattern(a, rad, w)

    def verb_pat(key: str, rad: str) -> str | None:
        """الفعلُ من شهادة مفتاحه كما كُتب؛ وذرّةُ «هُ» الأخيرة تُنزع على الخانات."""

        a = atoms(key)
        if a is None:
            return None
        if key.endswith(L.PRONOUN) and a and a[-1] == "هُ":
            a = a[:-1]
        out: str | None = L.pattern(a, rad, "")
        return out

    # ١. القواعد: الصارمةُ (القياسُ الأوّل بعينه) والمُرخاة (اتّحادُها بكلّ مرشَّح)
    m1 = L.read_tsv(L.MASDAR_TSV)
    p1 = L.read_tsv(L.PLURAL_TSV)
    strict_m, _, strict_p, _ = L.rules(m1, p1, lambda w, r: pat(w, r))
    relax_m: dict[str, set[str]] = {k: set(v) for k, v in strict_m.items()}
    relax_p: dict[str, set[str]] = {k: set(v) for k, v in strict_p.items()}
    added_m: list[dict[str, str]] = []
    added_p: list[dict[str, str]] = []
    for (cls, root), cands in sorted(mc.items()):
        for key, w in cands:
            trans = "1" if key.endswith(L.PRONOUN) else "0"
            if L.verb_class(verb_pat(key, root), trans) != cls:
                continue
            mp = pat(w, root)
            if mp and mp not in relax_m.setdefault(cls, set()):
                relax_m[cls].add(mp)
                added_m.append({"class": cls, "root": root, "masdar": w, "pattern": mp})
    for (sing, pl), cands in sorted(pc.items()):
        root = sing[:3]
        for key, w in cands:
            sp, pp = pat(key, root), pat(w, root)
            if sp and pp and pp not in relax_p.setdefault(sp, set()):
                relax_p[sp].add(pp)
                added_p.append({"singular": key, "plural": w, "from": sp, "to": pp})

    example_roots = ({r for _, r, _ in L.MASDAR_RULES} | {s[:3] for s, _ in L.PLURAL_RULES})

    def in_scope(r: list[str]) -> bool:
        return r[1] not in L.DEV_FILES and r[3] not in example_roots

    # ٢. المصدر بالطبقات: نقطةُ التقدير (علامةُ لين، القواعدُ الصارمة) والحصرُ (التعديةُ × القواعد)
    def hit(ps: list[str], rules: dict[str, set[str]], cls: str) -> bool:
        return any(p in rules.get(cls, set()) for p in ps)

    m_out: dict[str, object] = {}
    m_excl: dict[str, Counter[str]] = defaultdict(Counter)
    m_feat: list[tuple[Any, Any, str]] = []
    for st in ("sound", "hamzated", "doubled", "pooled"):
        n = point = lo = hi = 0
        for r in masdar:
            if not in_scope(r) or (st != "pooled" and r[0] != st):
                continue
            vp = verb_pat(r[5], r[4])
            cls = L.verb_class(vp, r[6])
            if cls is None:
                if st != "pooled":
                    m_excl[st]["VERB_NOT_FACALA_OR_NO_CERTIFICATE"] += 1
                continue
            ps = [p for p in (pat(w, r[4]) for w in r[7].split()) if p]
            if not ps:
                if st != "pooled":
                    m_excl[st]["NO_MASDAR_PATTERN"] += 1
                continue
            n += 1
            point += hit(ps, strict_m, cls)
            if r[6] == "0" and cls in ("intransitive_a", "intransitive_i"):
                a0, b0 = hit(ps, strict_m, cls), hit(ps, strict_m, "transitive")
                a1, b1 = hit(ps, relax_m, cls), hit(ps, relax_m, "transitive")
                lo += a0 and b0
                hi += a1 or b1
            else:
                lo += hit(ps, strict_m, cls)
                hi += hit(ps, relax_m, cls)
            if st == "sound":
                assert vp is not None
                bab = vp.split()[1][1:]
                m_feat.append((r[6], (bab, r[6]), ps[0]))
        m_out[st] = {"point": share(point, n), "hasr": bounds(lo, hi, n)}

    # ٣. الجمع بالطبقات
    p_out: dict[str, object] = {}
    p_excl: dict[str, Counter[str]] = defaultdict(Counter)
    p_feat: list[tuple[str, str, str]] = []
    for st in ("sound", "hamzated", "doubled", "pooled"):
        n = point = hi = 0
        for r in plural:
            if not in_scope(r) or (st != "pooled" and r[0] != st):
                continue
            sp = pat(r[5], r[4])
            if sp is None:
                if st != "pooled":
                    p_excl[st]["SINGULAR_NO_CERTIFICATE_OR_PATTERN"] += 1
                continue
            ps = [p for p in (pat(w, r[4]) for w in r[6].split()) if p]
            if not ps:
                if st != "pooled":
                    p_excl[st]["NO_PLURAL_PATTERN"] += 1
                continue
            n += 1
            point += any(p in strict_p.get(sp, set()) for p in ps)
            hi += any(p in relax_p.get(sp, set()) for p in ps)
            if st == "sound":
                p_feat.append((skeleton(sp), sp, ps[0]))
        p_out[st] = {"point": share(point, n), "hasr": bounds(point, hi, n)}

    # ٤. التفكيك: لا شيء ⊂ الهيكل ⊂ الوزن (LOO) والمعلومةُ المتبادلة (بت)
    def decompose(rows: list[tuple[Any, Any, str]], names: tuple[str, str]) -> dict[str, object]:
        a0 = loo_majority((0, y) for _, _, y in rows)
        a1 = loo_majority((f, y) for f, _, y in rows)
        a2 = loo_majority((g, y) for _, g, y in rows)
        h0 = cond_entropy((0, y) for _, _, y in rows)
        h1 = cond_entropy((f, y) for f, _, y in rows)
        h2 = cond_entropy((g, y) for _, g, y in rows)
        n = len(rows)
        return {
            "n": n,
            "loo_accuracy": {"none": share(*a0), names[0]: share(*a1), names[1]: share(*a2)},
            "points": {names[0]: round(100 * (a1[0] - a0[0]) / n, 2) if n else None,
                       names[1]: round(100 * (a2[0] - a1[0]) / n, 2) if n else None},
            "bits": {"H": round(h0, 4), names[0]: round(h0 - h1, 4), names[1]: round(h1 - h2, 4)},
        }

    return {
        "lines_sha256": L.sha(L.render(L.lines())),
        "masdar": {"strata": m_out, "excluded": {k: dict(sorted(v.items()))
                                                 for k, v in sorted(m_excl.items())},
                   "relaxed_rules_added": added_m,
                   "decomposition": decompose(m_feat, ("transitivity_mark", "bab_and_mark"))},
        "plural": {"strata": p_out, "excluded": {k: dict(sorted(v.items()))
                                                 for k, v in sorted(p_excl.items())},
                   "relaxed_rules_added": added_p,
                   "decomposition": decompose(p_feat, ("skeleton", "haraka"))},
        "refusals": dict(sorted(refusals.items())),
    }


def counts(m: list[list[str]], p: list[list[str]], weak: Counter[str]) -> str:
    cm = Counter(r[0] for r in m)
    cp = Counter(r[0] for r in p)
    return (f"المصدر {dict(cm)}، الجمع {dict(cp)}، المعتلّ (يُعدّ ولا يُقاس) {dict(weak)}")


def main(argv: list[str]) -> int:
    m, p, weak = records_v2()
    mt, pt = L.tsv(MASDAR_V2_HEADER, m), L.tsv(PLURAL_V2_HEADER, p)
    if "--check" in argv:
        if MASDAR_V2.read_bytes() != mt or PLURAL_V2.read_bytes() != pt:
            sys.stderr.write("LANE_HASR_RECORDS_DRIFTED\n")
            return 1
        if RESULT_V2.exists() and RESULT_V2.read_bytes() != L.dump(measure()):
            sys.stderr.write("LANE_HASR_RESULT_DRIFTED\n")
            return 1
        sys.stdout.write(f"حصرُ لين مطابق: {counts(m, p, weak)}\n")
        return 0
    if "measure" in argv:
        RESULT_V2.write_bytes(L.dump(measure()))
        sys.stdout.write(f"كُتب {RESULT_V2.relative_to(ROOT)}\n")
        return 0
    MASDAR_V2.write_bytes(mt)
    PLURAL_V2.write_bytes(pt)
    sys.stdout.write(f"كُتب سجلّا الطبقات: {counts(m, p, weak)}\n")
    return 0



if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
