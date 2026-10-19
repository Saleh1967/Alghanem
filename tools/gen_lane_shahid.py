"""الشاهدُ يضيّق الحصر: حلٌّ رياضيٌّ لديون ADR ٣٧ الأربعة (ADR ٤٠، تسجيلٌ ثالث
`docs/lane/PREREG-3.md`).

القياسان السابقان (`gen_lane.py`، `gen_lane_hasr.py`) يبقيان كما سُجّلا. وهذا تعميمٌ واحد: لكلّ
مدخلٍ **قائمةُ مرشَّحين** للحقّ (صنفُ الفعل × وزنُ كلّ مذكور)، والحقُّ أحدُها؛ فالإصابةُ محصورةٌ بين
«كلُّ المرشَّحين يصيب» و«أحدُهم يصيب» (`A116.Hasr.hasr_list`)، والشاهدُ يُسقط مرشَّحين فيضيّق ولا
يوسّع (`A116.Hasr.hasr_refine`).

1. `TRANSITIVITY_WITNESS_NEEDED` — **شاهدُ التعدية**: صيغُ الماضي المجرّد التي لا تكون إلّا فعلًا
   متعدّيًا بنفسه — فاعلٌ متّصلٌ ثمّ مفعولٌ متّصل: فَعَلْتُهُ، فَعَلْنَاهُ، فَعَلُوهُ، فَعَلَتْهُ،
   فَعَلْتُمُوهُ (والمفعولُ هاءٌ أو كاف) — على الخانات بأعيانها (`witness_forms`)، في المجالات
   المختومة الثلاثة: المصحف والصحيحين ولين. وحركةُ العين فيها بابُ الفعل. لا يُعدّ «فَعَلَهُ»
   شاهدًا: يلتبس باسمٍ منصوبٍ مضاف (عَمَلَهُ)؛ ولا المبنيُّ للمجهول: يكون للمتعدّي بحرف (غُضِبَ
   عَلَيْهِمْ).
2. `RELAXED_RULE_OVERREACH` — **الإرخاءُ في قوائم لين وحدَها**: مرشَّحُ المثال كلُّ وسمٍ في **أيّ**
   قائمة «inf. n.» أو «pl.» في مدخل المثال (`spans_after_all`)، لا كلُّ وسمٍ في المدخل؛ فلا يدخل
   «ضَرَبٌ» إلّا إن سمّاه لين مصدرًا.
3. `DOUBLED_INTRANSITIVE_BAB_HIDDEN` — **الفكُّ شاهدُ الباب**: الماضي المضعّف مع ضمير الرفع المتحرّك
   يُفكّ (فَرِرْتُ، ظَلِلْتُ) فتظهر حركةُ العين؛ وما لم يُشهد بابُه فمرشَّحوه الأبوابُ الثلاثة.
4. `WEAK_STRATUM_NOT_PATTERNABLE` — **العكسُ قائمةٌ لا دالّة**: الخاناتُ تنسى حرفَ العلّة
   (`Neutral.neutral_forgets_weak`) فلا دالّةَ من الشهادة إلى الوزن؛ لكنّ لها **علاقةً**: `over`
   يولّد كلَّ وزنٍ تحتيٍّ يمكن أن يصير إلى هذه الخانات بقلب العلّة (تبقى حركتُها)، أو صيرورتها ألفًا
   أو حذفها (حركتُها مجهولةٌ فتُعدَّد)، مع نقل الحركة إلى ما قبلها. فإن كان الوزنُ الحقّ فيها (فرضٌ
   معلَن `A_OVER`، تُقاس تغطيتُه على مفاتيح الأفعال المعتلّة نفسِها) صحّ الحصر.
5. `LANE_DEPOSIT_NOT_CONSUMED` — ليس مسألةً رياضيّة: لا يُحلّ هنا.

`python tools/gen_lane_shahid.py measure` يكتب `docs/lane/shahid.json`؛ و`--check` يُسقط البناءَ بـ
`LANE_SHAHID_RESULT_DRIFTED`. معفاةٌ في الحارس لأنّها أداةُ إيداع.
"""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from collections import Counter, defaultdict
from collections.abc import Iterable
from itertools import product
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
RESULT_V3 = ROOT / "docs" / "lane" / "shahid.json"
FA, KA, DA, SU = "َ", "ِ", "ُ", "ْ"
VOWELS = (FA, KA, DA)
WEAK_R = frozenset("وي")
CAP = 256
"""حدُّ قائمة المرشَّحين لكلمة؛ ما جاوزه يُعدّ «لا يُحصر» (الأدنى لا يصيب، والأعلى يصيب)."""


# --- ١. شاهدُ التعدية والباب على الخانات -------------------------------------------------------


def _is(atom: str, carrier: str, mark: str | None = None) -> bool:
    return bool(atom) and atom[0] == carrier and (mark is None or atom[1:] == mark)


def _obj(atom: str) -> bool:
    return bool(atom) and atom[0] in "هك"


SUFFIXES: tuple[tuple[str, tuple[str, ...]], ...] = (
    (SU, ("تُ",)), (SU, ("تَ",)), (SU, ("تِ",)), (SU, ("نَ", "اْ")),
    (DA, ("وْ",)), (FA, ("تْ",)), (SU, ("تُ", "مُ", "وْ")),
)
"""(حركةُ اللام، ذرّاتُ ضمير الرفع) في فَعَلْتُ، فَعَلْتَ، فَعَلْتِ، فَعَلْنَا، فَعَلُوا، فَعَلَتْ، فَعَلْتُمُو."""


def witness_forms(atoms: tuple[str, ...], rad: str) -> tuple[set[str], set[str]]:
    """(أبوابٌ شُهد بها التعدّي، أبوابٌ شُهد بها الفكّ) من ذرّات كلمة؛ الجذرُ ثلاثةُ أصولٍ بترتيبها.

    التعدّي: ‎r1َ r2X r3·‎ ثمّ ضميرُ رفعٍ من `SUFFIXES` ثمّ مفعولٌ هاءٌ أو كاف. والفكُّ (للمضعّف): ‎r1َ r2X r2ْ‎
    ثمّ ضميرُ رفعٍ متحرّكٌ ساكنُ اللام (تُ، تَ، تِ، نَا) — بلا مفعولٍ لازم."""

    trans: set[str] = set()
    fakk: set[str] = set()
    r1, r2, r3 = rad[0], rad[1], rad[2]
    for i in range(len(atoms) - 2):
        a, b, c = atoms[i], atoms[i + 1], atoms[i + 2]
        if not (_is(a, r1, FA) and b and b[0] == r2 and b[1:] in VOWELS and c and c[0] == r3):
            continue
        x = b[1:]
        for lam, subj in SUFFIXES:
            if c[1:] != lam:
                continue
            j = i + 3
            if tuple(atoms[j:j + len(subj)]) != subj:
                continue
            if j + len(subj) < len(atoms) and _obj(atoms[j + len(subj)]):
                trans.add(x)
            if r2 == r3 and lam == SU and subj in (("تُ",), ("تَ",), ("تِ",), ("نَ", "اْ")):
                fakk.add(x)
    return trans, fakk


# --- ٢. العكسُ قائمةً: كلُّ وزنٍ تحتيٍّ ممكن -------------------------------------------------------


def over(atoms: tuple[str, ...], rad: str, surface: str) -> set[str] | None:
    """الأوزانُ التحتيّة الممكنة لهذه الذرّات على هذا الجذر (`A_OVER`)؛ ولا شيء إن جاوزت `CAP`.

    الأصلُ الصحيح يطابق حاملَه بحركته. والمعتلُّ (و، ي): (أ) قلبٌ إلى و أو ي تبقى حركتُه؛ (ب) ألفٌ
    ساكنة أو (ج) حذف — حركتُه مجهولةٌ فتُعدَّد الأربع، ومع (ب) و(ج) تُعدَّد حركةُ الأصل الذي قبله (نقلُ
    الحركة). والزائدُ يُنقل كما هو. ثمّ نونُ التنوين وحركةُ الإعراب الأخيرة تُحذفان كما في
    `gen_lane.pattern`."""

    seq = list(atoms)
    if surface and surface[-1] in L.TANWIN and seq and seq[-1] == "نْ":
        seq = seq[:-1]
    if not seq:
        return set()
    out: set[tuple[str, ...]] = set()
    marks = (FA, KA, DA, SU)

    def go(i: int, k: int, acc: tuple[str, ...]) -> None:
        if len(out) > CAP:
            return
        if i == len(seq):
            if k == 3:
                out.add(acc)
            elif k < 3 and rad[k] in WEAK_R:  # حذفُ الأصل الأخير المعتلّ
                for m in marks:
                    go(i, k + 1, acc + (f"{k + 1}{m}",))
            return
        a = seq[i]
        ch, mk = a[0], a[1:]
        if k < 3:
            r = rad[k]
            if ch == r:
                go(i + 1, k + 1, acc + (f"{k + 1}{mk}",))
            if r in WEAK_R:
                if ch in WEAK_R and ch != r:  # قلب
                    go(i + 1, k + 1, acc + (f"{k + 1}{mk}",))
                for m in marks:
                    for prev in _naql(acc):
                        if ch == "ا":  # صيرورةٌ ألفًا
                            go(i + 1, k + 1, prev + (f"{k + 1}{m}",))
                        go(i, k + 1, prev + (f"{k + 1}{m}",))  # حذف
        go(i + 1, k, acc + (a,))

    go(0, 0, ())
    if len(out) > CAP:
        return None
    res: set[str] = set()
    for t in out:
        last = t[-1].rstrip("".join(L.HARAKAT))
        if L.letters(surface).endswith("ة") and last == "ت":
            last = "ة"
        res.add(" ".join(t[:-1] + (last,)))
    return res


def _naql(acc: tuple[str, ...]) -> list[tuple[str, ...]]:
    """الأصلُ السابق (إن كان آخرَ ما أُخذ) بحركاته الأربع؛ وإلّا كما هو."""

    if acc and acc[-1][:1].isdigit():
        base = acc[-1][0]
        return [acc] + [acc[:-1] + (base + m,) for m in (FA, KA, DA, SU) if base + m != acc[-1]]
    return [acc]


# --- ٣. القياس ------------------------------------------------------------------------------------


def spans_after_all(tokens: list[tuple[str, str]], marker: re.Pattern[str]) -> list[str]:
    """اتّحادُ القوائم بعد **كلّ** علامةٍ في المدخل (بشروط `gen_lane.spans_after` نفسِها لكلّ قائمة)."""

    out: list[str] = []
    for i, (kind, text) in enumerate(tokens):
        if kind != "t":
            continue
        for m in marker.finditer(text):
            sep = text[m.end():]
            for k2, t2 in tokens[i + 1:]:
                if k2 == "t":
                    sep += t2
                    continue
                if k2 != "ar" or not L.SEP.match(sep):
                    break
                out.append(t2)
                sep = ""
    return out


def relaxed_list_candidates() -> tuple[dict[tuple[str, str], list[tuple[str, str]]],
                                       dict[tuple[str, str], list[tuple[str, str]]]]:
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
                toks = L.stream(e)
                it = e.find("form/itype")
                if head in mroots and it is not None and (it.text or "").strip() == "1":
                    spans = [s.strip() for s in spans_after_all(toks, L.INF) if L.cited_noun(s)]
                    for cls, root, ml in L.MASDAR_RULES:
                        if root == head:
                            mc[(cls, root)] += [(key, s) for s in spans if L.letters(s) == ml]
                if head in proots and it is None:
                    spans = [s.strip() for s in spans_after_all(toks, L.PL) if L.cited_noun(s)]
                    for sing, pl in L.PLURAL_RULES:
                        if sing[:3] == head and L.letters(key) == sing:
                            pc[(sing, pl)] += [(key, s) for s in spans if L.letters(s) == pl]
    return mc, pc


SUFFIX_LETTERS = re.compile(r"(?:تمو|نا|و|ت)[هك]")
FAKK_LETTERS = re.compile(r"(?:ت|نا)")


def corpus_witnesses(rads: set[str]) -> dict[str, dict[str, dict[str, set[str]]]]:
    """لكلّ مجالٍ مختوم ولكلّ جذر: الأبوابُ المشهودُ بها التعدّي والفكّ. تُرشَّح الكلماتُ بحروفها أوّلًا
    (الأصولُ ثمّ حروفُ الضمائر)، ثمّ تدخل البوّابةَ على مجالها والشاهدُ يُقرأ من ذرّاتها وحدَها."""

    from gate.api import CORPUS, HADITH_CORPUS, LANE_CORPUS, Gate, Refusal, sealed_forms

    out: dict[str, dict[str, dict[str, set[str]]]] = {}
    for label, corpus in (("quran", CORPUS), ("sahihain", HADITH_CORPUS), ("lane", LANE_CORPUS)):
        forms = sealed_forms(corpus)
        cand: dict[str, set[str]] = defaultdict(set)
        for f in forms:
            lt = H.norm(L.letters(f))
            for i in range(len(lt) - 2):
                tri = lt[i:i + 3]
                if tri in rads and (SUFFIX_LETTERS.match(lt, i + 3)
                                    or (tri[1] == tri[2] and FAKK_LETTERS.match(lt, i + 3))):
                    cand[f].add(tri)
        gate = Gate(corpus=corpus, domain=set(cand))
        per: dict[str, dict[str, set[str]]] = defaultdict(lambda: {"trans": set(), "fakk": set()})
        for f, rs in cand.items():
            c = gate.enter(f.encode("utf-8"))
            if isinstance(c, Refusal):
                continue
            atoms = tuple(H.norm(a[0]) + a[1:] for a in c.atoms)
            for r in rs:
                t, k = witness_forms(atoms, r)
                per[r]["trans"] |= t
                per[r]["fakk"] |= k
        out[label] = per
    return out


def classes(babs: Iterable[str], trans: set[str]) -> set[str]:
    """صنفُ المتنبّئ لكلّ (باب، تعدية)؛ و`trans` مجموعةُ قيم التعدية الممكنة {"1"، "0"}."""

    res: set[str] = set()
    for b in babs:
        for t in trans:
            if b == DA:
                res.add("u")
            elif t == "1":
                res.add("transitive")
            else:
                res.add({KA: "intransitive_i", FA: "intransitive_a"}[b])
    return res


def measure() -> dict[str, object]:
    from gate.api import LANE_CORPUS, Gate, Refusal, sealed_forms
    from gate.residue import repair

    masdar = L.read_tsv(H.MASDAR_V2)
    plural = L.read_tsv(H.PLURAL_V2)
    weak_m, weak_p = weak_records()
    mc, pc = relaxed_list_candidates()
    words: set[str] = set()
    for r in masdar + weak_m:
        words.add(r[5])
        words.update(r[7].split())
    for r in plural + weak_p:
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
                cache[w] = tuple(H.norm(a[0]) + a[1:] for a in c.atoms)
        return cache[w]

    def cands(w: str, rad: str) -> set[str] | None:
        a = atoms(w)
        return None if a is None else over(a, rad, w)

    def verb_cands(key: str, rad: str) -> set[str] | None:
        a = atoms(key)
        if a is None:
            return None
        if key.endswith(L.PRONOUN) and a and a[-1] == "هُ":
            a = a[:-1]
        return over(a, rad, "")

    # القواعد: الصارمةُ من result.json، والمُرخاةُ بقوائم لين وحدَها
    v1 = json.loads(L.RESULT.read_text(encoding="utf-8"))
    strict_m = {k: set(v) for k, v in v1["masdar"]["rules"].items()}
    strict_p = {k: set(v) for k, v in v1["plural"]["rules"].items()}
    relax_m = {k: set(v) for k, v in strict_m.items()}
    relax_p = {k: set(v) for k, v in strict_p.items()}
    added_m: list[dict[str, str]] = []
    added_p: list[dict[str, str]] = []
    for (cls, root), cs in sorted(mc.items()):
        for key, w in cs:
            vc = verb_cands(key, root) or set()
            trans = "1" if key.endswith(L.PRONOUN) else "0"
            babs = {p.split()[1][1:] for p in vc if _facala(p)}
            if len(babs) != 1 or classes(babs, {trans}) != {cls}:
                continue
            mp = cands(w, root)
            if mp and len(mp) == 1:
                (p,) = tuple(mp)
                if p not in relax_m.setdefault(cls, set()):
                    relax_m[cls].add(p)
                    added_m.append({"class": cls, "root": root, "masdar": w, "pattern": p})
    for (sing, pl), cs in sorted(pc.items()):
        root = sing[:3]
        for key, w in cs:
            sp, pp = cands(key, root), cands(w, root)
            if sp and pp and len(sp) == 1 and len(pp) == 1:
                (s1,), (p1,) = tuple(sp), tuple(pp)
                if p1 not in relax_p.setdefault(s1, set()):
                    relax_p[s1].add(p1)
                    added_p.append({"singular": key, "plural": w, "from": s1, "to": p1})

    rads = {r[4] for r in masdar + weak_m}
    wit = corpus_witnesses(rads)

    example_roots = ({r for _, r, _ in L.MASDAR_RULES} | {s[:3] for s, _ in L.PLURAL_RULES})

    def in_scope(r: list[str]) -> bool:
        return r[1] not in L.DEV_FILES and r[3] not in example_roots

    # المصدر
    m_out: dict[str, object] = {}
    m_excl: dict[str, Counter[str]] = defaultdict(Counter)
    m_wit: dict[str, Counter[str]] = defaultdict(Counter)
    for st in ("sound", "hamzated", "doubled", "weak", "pooled"):
        acc: dict[str, list[int]] = {k: [0, 0] for k in
                                     ("strict_nowit", "strict_wit", "relax_wit")}
        n = 0
        for r in masdar + weak_m:
            if not in_scope(r) or (st != "pooled" and r[0] != st):
                continue
            rad = r[4]
            vcand = verb_cands(r[5], rad)
            if vcand is None:
                m_excl[st]["VERB_NO_CERTIFICATE"] += 1 if st != "pooled" else 0
                continue
            babs = {p.split()[1][1:] for p in vcand if _facala(p)}
            assimilated = any(_assimilated(p) for p in vcand)
            ws = {lab: wit[lab].get(rad, {"trans": set(), "fakk": set()}) for lab in wit}
            fakk = set().union(*(w["fakk"] for w in ws.values()))
            trans_w = set().union(*(w["trans"] for w in ws.values()))
            if not babs and assimilated:
                babs = (fakk | trans_w) or {FA, KA, DA}
                if st != "pooled":
                    m_wit[st]["DOUBLED_BAB_" + ("WITNESSED" if fakk | trans_w else "HIDDEN")] += 1
            if not babs:
                m_excl[st]["VERB_NOT_FACALA"] += 1 if st != "pooled" else 0
                continue
            ms = [cands(w, rad) for w in r[7].split()]
            if not any(ms):
                m_excl[st]["NO_MASDAR_CERTIFICATE"] += 1 if st != "pooled" else 0
                continue
            n += 1
            t_nowit = {"1"} if r[6] == "1" else {"0", "1"}
            witnessed = bool(babs & trans_w)
            t_wit = {"1"} if (r[6] == "1" or witnessed) else {"0", "1"}
            if st != "pooled" and r[6] == "0":
                m_wit[st]["UNMARKED_" + ("WITNESSED" if witnessed else "UNWITNESSED")] += 1
            for key, rules, tset in (("strict_nowit", strict_m, t_nowit),
                                     ("strict_wit", strict_m, t_wit),
                                     ("relax_wit", relax_m, t_wit)):
                cl = classes(babs, tset)
                lo, hi = hit_bounds(cl, ms, rules)
                acc[key][0] += lo
                acc[key][1] += hi
        m_out[st] = {k: H.bounds(v[0], v[1], n) for k, v in acc.items()}

    # الجمع
    p_out: dict[str, object] = {}
    p_excl: dict[str, Counter[str]] = defaultdict(Counter)
    for st in ("sound", "hamzated", "doubled", "weak", "pooled"):
        accp = {k: [0, 0] for k in ("strict", "relax")}
        n = 0
        for r in plural + weak_p:
            if not in_scope(r) or (st != "pooled" and r[0] != st):
                continue
            sc = cands(r[5], r[4])
            if not sc:
                p_excl[st]["SINGULAR_NO_CANDIDATE"] += 1 if st != "pooled" else 0
                continue
            ps = [cands(w, r[4]) for w in r[6].split()]
            if not any(ps):
                p_excl[st]["NO_PLURAL_CANDIDATE"] += 1 if st != "pooled" else 0
                continue
            n += 1
            for key, rules in (("strict", strict_p), ("relax", relax_p)):
                lo, hi = hit_bounds(sc, ps, rules)
                accp[key][0] += lo
                accp[key][1] += hi
        p_out[st] = {k: H.bounds(v[0], v[1], n) for k, v in accp.items()}

    return {
        "lines_sha256": L.sha(L.render(L.lines())),
        "a_over_coverage": a_over_coverage(weak_m, verb_cands),
        "masdar": {"strata": m_out, "witness_counts": {k: dict(sorted(v.items()))
                                                       for k, v in sorted(m_wit.items())},
                   "excluded": {k: dict(sorted(v.items())) for k, v in sorted(m_excl.items())},
                   "relaxed_rules_added": added_m},
        "plural": {"strata": p_out,
                   "excluded": {k: dict(sorted(v.items())) for k, v in sorted(p_excl.items())},
                   "relaxed_rules_added": added_p},
        "witness_roots": {lab: sum(1 for v in per.values() if v["trans"] or v["fakk"])
                          for lab, per in sorted(wit.items())},
        "refusals": dict(sorted(refusals.items())),
    }


def _facala(p: str) -> bool:
    parts = p.split()
    return len(parts) == 3 and parts[0] == "1" + FA and parts[2] == "3" and parts[1][1:] in VOWELS


def _assimilated(p: str) -> bool:
    return p.split() == ["1" + FA, "2" + SU, "3"]


def hit_bounds(cls: set[str], words: list[set[str] | None], rules: dict[str, set[str]]
               ) -> tuple[bool, bool]:
    """(الأدنى، الأعلى) لإصابة مدخل: الحقُّ صنفٌ من `cls` ووزنٌ لكلّ مذكورٍ من قائمته (`None` = لا
    يُحصر). الأدنى: لكلّ صنفٍ مذكورٌ كلُّ أوزانه متوقَّعة؛ الأعلى: صنفٌ ومذكورٌ ووزنٌ متوقَّع — `hasr_list`
    على حاصل الضرب."""

    def certain(c: str) -> bool:
        pred = rules.get(c, set())
        return any(w is not None and w and w <= pred for w in words)

    def possible(c: str) -> bool:
        pred = rules.get(c, set())
        return any(w is None or bool(w & pred) for w in words)

    if not cls:
        return False, False
    return all(certain(c) for c in cls), any(possible(c) for c in cls)


def weak_records() -> tuple[list[list[str]], list[list[str]]]:
    """سجلّا الطبقة المعتلّة بإطار `gen_lane_hasr.records_v2` نفسِه (هناك تُعدّ ولا تُكتب)."""

    masdar: list[list[str]] = []
    plural: list[list[str]] = []
    for name in sorted(L.LANE_SOURCES):
        for head, d in L.roots(name):
            st = H.stratum(head)
            if st is None or st[0] != "weak":
                continue
            rad = st[1]
            if "ا" in rad or "ى" in rad or "ٱ" in rad:
                continue
            hn = H.norm(head)
            for e in d.iter("entryFree"):
                key = (e.get("key") or "").strip()
                if not key or any(c.isspace() for c in key):
                    continue
                it = e.find("form/itype")
                toks = L.stream(e)
                if it is not None and (it.text or "").strip() == "1":
                    trans = key.endswith(L.PRONOUN)
                    verb = key[: -len(L.PRONOUN)] if trans else key
                    if not _weak_letters_ok(H.norm(L.letters(verb)), hn):
                        continue
                    ms = [s.strip() for s in L.spans_after(toks, L.INF) if L.cited_noun(s)]
                    if ms:
                        masdar.append(["weak", name, e.get("id") or "", head, rad, key,
                                       "1" if trans else "0", " ".join(ms)])
                elif it is None:
                    lk = H.norm(L.letters(key))
                    if not (_weak_letters_ok(lk, hn) or _weak_letters_ok(lk[:-1], hn)
                            and lk.endswith("ة")):
                        continue
                    ps = [s.strip() for s in L.spans_after(toks, L.PL) if L.cited_noun(s)]
                    if ps:
                        plural.append(["weak", name, e.get("id") or "", head, rad, key,
                                       " ".join(ps)])
    return masdar, plural


def _weak_letters_ok(lt: str, head: str) -> bool:
    """حروفُ المفتاح حروفُ الجذر بعد قلب العلّة ألفًا أو ياءً أو واوًا أو حذفِها — مطابقةٌ بالحروف وحدَها
    لاختيار المدخل؛ والوزنُ بعدُ من الذرّات."""

    alts = [{c} | ({"ا", "و", "ي", "ى", ""} if c in WEAK_R else set()) for c in head]
    return any("".join(p) == lt for p in product(*alts))


def a_over_coverage(weak_m: list[list[str]], verb_cands: Any) -> dict[str, object]:
    """تغطيةُ `A_OVER` على مفاتيح الأفعال المعتلّة: أيقع وزنٌ ‎1َ 2X 3‎ (فَعَلَ بأبوابه) في قائمة الماضي؟"""

    hit = n = 0
    for r in weak_m:
        vc = verb_cands(r[5], r[4])
        if vc is None:
            continue
        n += 1
        hit += any(_facala(p) for p in vc)
    return {"verbs": n, "covered": hit, "rate": round(hit / n, 4) if n else None}


def main(argv: list[str]) -> int:
    if "--check" in argv:
        if RESULT_V3.exists() and RESULT_V3.read_bytes() != L.dump(measure()):
            sys.stderr.write("LANE_SHAHID_RESULT_DRIFTED\n")
            return 1
        sys.stdout.write("شاهدُ لين مطابق\n")
        return 0
    if "measure" in argv:
        RESULT_V3.write_bytes(L.dump(measure()))
        sys.stdout.write(f"كُتب {RESULT_V3.relative_to(ROOT)}\n")
        return 0
    m, p = weak_records()
    sys.stdout.write(f"الطبقة المعتلّة: مصدر {len(m):,}، جمع {len(p):,}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
