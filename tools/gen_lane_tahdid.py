"""التعيين: حلٌّ رياضيٌّ لديون ADR ٤٠ (ADR ٤٣، تسجيلٌ رابع `docs/lane/PREREG-4.md`).

القياساتُ الثلاثة السابقة (`gen_lane.py`، `gen_lane_hasr.py`، `gen_lane_shahid.py`) تبقى كما سُجّلت؛
وهذا تحليلٌ رابع يستعمل أدواتها ولا يغيّرها.

1. `TRANSITIVITY_WITNESS_SPARSE` — حلّان:
   (أ) **شاهدُ المضارع**: ‎يَفْعَلُهُ، تَفْعَلُهُ، نَفْعَلُهُ، يَفْعَلُوهُ، يَفْعَلُونَهُ‎ (حرفُ المضارعة مفتوحٌ ثمّ الفاءُ ساكنة
       ثمّ مفعولٌ هاءٌ أو كاف — `imperfect_witness`). حركةُ عين المضارع لا تعيّن بابَ الماضي فتُحمل على ما
       يوافقها (`COMPAT`)، ولا يُسند الشاهدُ إلى مدخلٍ إلّا إن كان للجذر عند لين مدخلُ فعلٍ مجرّدٍ **واحد**
       (التعيينُ بالتفرّد). والهمزةُ حرفَ مضارعةٍ مستبعَدة: تلتبس بأفعل التفضيل (أَكْرَمُهُ).
   (ب) **العيّنةُ تعيّن ما لا يشهده شاهد**: ما بقي مجهولًا (`U`، مدخلٌ تتوقّف إصابتُه على التعدية) يُسحب منه
       إطارٌ ببذرةٍ معلَنة (`FRAME`) يملؤه المالك من لين بيده؛ فالمنقولُ تقديرٌ بفاصل:
       ‎1 − (أدنى + |U|·q̂)/n‎ و‎q̂‎ نسبةُ الإصابة في العيّنة (Wilson). لا رقمَ قبل الملء.
2. `A_OBJ` — **يُفحص على لين نفسِه**: نسبةُ الشاهد في أفعالٍ علّمها لين متعدّيةً («هُ») وفي أفعالٍ وصفها
   لازمةً («intrans.» أو حدُّها «He was, or became»)؛ فإن انفصل فاصلاهما فالفرضُ غيرُ منقوض.
3. `FUULA_RULE_UNDECIDED` — **التعيينُ بالتمايز** (`A116.Hasr.pin_unique`): البيتُ في الألفية بندان
   مسمّيان ‎«وفُعَلٌ جمعًا لفُعْلةٍ عُرِف … ولفِعْلةٍ فِعَل»‎ بأمثلةٍ متفرّقة (قربة، غرفة | كسرة)؛ مرشَّحو كلّ بندٍ تشكيلاتُ
   لين لأمثلته (التقاطع)، والبندان لا يتّحدان، فإن تعيّن الثاني تعيّن الأوّل بحذفه. وشاهدٌ نصّيٌّ ثانٍ
   مستقلّ في الشرح المختوم نفسِه يصف الحركات بأسمائها (`FUULA_SOURCE`).
4. `A_OVER_TOO_WIDE` — **المحقِّقُ الأماميّ**: مرآةُ `A116.Neutral.realizeN` المطابَقة لجدول Lean
   (`tests/test_neutral.py::realize`) تُحقّق كلَّ مرشَّحٍ على الجذر؛ ويبقى ما يعيد الخاناتِ بأعيانها
   (`A116.Hasr.hasr_refine`) — بفرضٍ معلَن `A_FWD` تُقاس تغطيتُه على مفاتيح الأفعال المعتلّة.
5. `LANE_DEPOSIT_NOT_CONSUMED` — ليس مسألةً رياضيّة: قرارُ استهلاكٍ في SLGE (ADR ٤٣، مقترَحٌ للمالك).

`python tools/gen_lane_tahdid.py measure` يكتب `docs/lane/tahdid.json` والإطار؛ و`--check` يُسقط
البناءَ بـ`LANE_TAHDID_RESULT_DRIFTED` أو `LANE_FRAME_DRIFTED`. معفاةٌ في الحارس لأنّها أداةُ إيداع.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import re
import sys
from collections import Counter, defaultdict
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


L: Any = _load("gen_lane", ROOT / "tools" / "gen_lane.py")
H: Any = _load("gen_lane_hasr", ROOT / "tools" / "gen_lane_hasr.py")
S: Any = _load("gen_lane_shahid", ROOT / "tools" / "gen_lane_shahid.py")
NM: Any = _load("neutral_mirror", ROOT / "tests" / "test_neutral.py")

RESULT_V4 = ROOT / "docs" / "lane" / "tahdid.json"
FRAME = L.LANE / "transitivity-frame.tsv"
FRAME_HEADER = ["file", "entry", "root", "verb", "transitive"]
SEED = "ADR-43-lane-transitivity"
TARGET = 0.03
"""نصفُ عرض الفاصل المطلوب على المنقول: ‎m = ⌈(1.96 · 0.5 · |U|/n ÷ TARGET)²⌉‎ بحدٍّ أعلى |U|."""
FA, KA, DA, SU = "َ", "ِ", "ُ", "ْ"
VOWELS = (FA, KA, DA)

# --- ١أ. شاهدُ المضارع -----------------------------------------------------------------------------

PREFIX = frozenset("يتن")
COMPAT: dict[str, frozenset[str]] = {DA: frozenset(FA), KA: frozenset(FA + KA),
                                     FA: frozenset(FA + KA)}
"""حركةُ عين المضارع ← أبوابُ الماضي المتعدّي الموافقة: يَفْعُلُ من فَعَلَ (فَعُلَ لا يتعدّى بنفسه)، ويَفْعِلُ من
فَعَلَ أو فَعِلَ، ويَفْعَلُ من فَعَلَ أو فَعِلَ."""


def imperfect_witness(atoms: tuple[str, ...], rad: str) -> set[str]:
    """حركاتُ عين المضارع المشهودِ بها التعدّي: ‎P َ r1ْ r2X r3·‎ ثمّ مفعولٌ (هاء/كاف)، أو ‎r3ُ وْ‎ ثمّ مفعول،
    أو ‎r3ُ وْ نَ‎ ثمّ مفعول؛ و‎P‎ من ي ت ن."""

    out: set[str] = set()
    r1, r2, r3 = rad[0], rad[1], rad[2]
    for i in range(len(atoms) - 4):
        p, a, b, c = atoms[i], atoms[i + 1], atoms[i + 2], atoms[i + 3]
        if not (p and p[0] in PREFIX and p[1:] == FA and S._is(a, r1, SU) and b and b[0] == r2
                and b[1:] in VOWELS and c and c[0] == r3):
            continue
        rest = atoms[i + 4:]
        if c[1:] in (DA, FA, SU) and rest and S._obj(rest[0]):
            out.add(b[1:])
        elif c[1:] == DA and rest[:1] == ("وْ",) and len(rest) > 1 and S._obj(rest[1]):
            out.add(b[1:])
        elif (c[1:] == DA and rest[:2] == ("وْ", "نَ") and len(rest) > 2
              and S._obj(rest[2])):
            out.add(b[1:])
    return out


def compat_babs(impf: set[str]) -> set[str]:
    out: set[str] = set()
    for v in impf:
        out |= COMPAT[v]
    return out


IMPF_LETTERS = re.compile(r"(?:ون|و)?[هك]")


def corpus_witnesses(rads: set[str]) -> dict[str, dict[str, dict[str, set[str]]]]:
    """لكلّ مجالٍ مختوم ولكلّ جذر: أبوابُ التعدّي والفكّ من الماضي (`gen_lane_shahid.witness_forms`)
    وحركاتُ المضارع المتعدّي (`imperfect_witness`). الترشيحُ بالحروف ثمّ البوّابةُ على مجالها."""

    from gate.api import CORPUS, HADITH_CORPUS, LANE_CORPUS, Gate, Refusal, sealed_forms

    out: dict[str, dict[str, dict[str, set[str]]]] = {}
    for label, corpus in (("quran", CORPUS), ("sahihain", HADITH_CORPUS), ("lane", LANE_CORPUS)):
        cand: dict[str, set[str]] = defaultdict(set)
        for f in sealed_forms(corpus):
            lt = H.norm(L.letters(f))
            for i in range(len(lt) - 2):
                tri = lt[i:i + 3]
                if tri not in rads:
                    continue
                if (S.SUFFIX_LETTERS.match(lt, i + 3)
                        or (tri[1] == tri[2] and S.FAKK_LETTERS.match(lt, i + 3))
                        or (i > 0 and lt[i - 1] in PREFIX and IMPF_LETTERS.match(lt, i + 3))):
                    cand[f].add(tri)
        gate = Gate(corpus=corpus, domain=set(cand))
        per: dict[str, dict[str, set[str]]] = defaultdict(
            lambda: {"trans": set(), "fakk": set(), "impf": set()})
        for f, rs in cand.items():
            c = gate.enter(f.encode("utf-8"))
            if isinstance(c, Refusal):
                continue
            atoms = tuple(H.norm(a[0]) + a[1:] for a in c.atoms)
            for r in rs:
                t, k = S.witness_forms(atoms, r)
                per[r]["trans"] |= t
                per[r]["fakk"] |= k
                per[r]["impf"] |= imperfect_witness(atoms, r)
        out[label] = per
    return out


# --- ٢. فحصُ A_OBJ على لين ----------------------------------------------------------------------

NEG_LABEL = re.compile(r"\bintrans\.")
POS_LABEL = re.compile(r"\btrans\.")
STATIVE = re.compile(r"\b(?:He|She|It|They),? (?:was|were),? or (?:became|become)\b")
GLOSS = 600
"""حدُّ «أوّل الحدّ»: أوّلُ 600 حرفٍ من نصّ المدخل الإنجليزيّ."""


def lane_pass(ids: set[tuple[str, str]]) -> tuple[Counter[str], dict[tuple[str, str], str]]:
    """عددُ مداخل الفعل المجرّد (`itype` 1) لكلّ رأس جذر في لين كلِّه، ونصُّ المداخل المطلوبة."""

    form1: Counter[str] = Counter()
    texts: dict[tuple[str, str], str] = {}
    for name in sorted(L.LANE_SOURCES):
        for head, d in L.roots(name):
            for e in d.iter("entryFree"):
                it = e.find("form/itype")
                if it is None or (it.text or "").strip() != "1":
                    continue
                form1[head] += 1
                k = (name, e.get("id") or "")
                if k in ids:
                    texts[k] = "".join(t for kind, t in L.stream(e) if kind == "t")
    return form1, texts


def lane_label(text: str) -> str | None:
    """«neg_label»: لازمٌ بنصّ لين (intrans. بلا trans.)؛ «neg_stative»: أوّلُ حدّه
    «He was, or became»؛ وإلّا لا شيء."""

    if NEG_LABEL.search(text) and not POS_LABEL.search(text):
        return "neg_label"
    if STATIVE.search(text[:GLOSS]):
        return "neg_stative"
    return None


# --- ٣. التعيينُ بالتمايز -----------------------------------------------------------------------

CLAUSE_A = (("قربة", "قرب"), ("غرفة", "غرف"))
CLAUSE_B = (("كسرة", "كسر"),)
FUULA_SOURCE = {
    "file": "0769IbnCaqilBahaDinMisri.SharhCalaAlfiyya.Shamela0009904-ara1",
    "sha256_prefix": "661e43ea265eca8c",
    "verse_lines": [8407, 8409],
    "verse": "وفعل جمعا لفعلة عرف … ونحو كبرى ولفعلة فعل",
    "examples_lines": [8418, 8421],
    "clause_a_examples": "فالأول كقربة وقرب وغرفة وغرف",
    "clause_b_examples": "على فعلة نحو كسرة وكسر وحجة وحجج ومرية ومرى",
    "named_vowels_lines": [8222, 8224],
    "named_vowels": ("جمع فعلة بكسر الفاء يكون على فعل بكسر الأول وفتح الثاني وجمع فعلة بضم الفاء "
                     "يكون على فعل بضم الأول وفتح الثاني"),
}
"""منقولٌ من شرح ابن عقيل كما ختمه `gen_lane.py` (OpenITI 0775AH@61b0c789) — معلَن: الملفُّ
خارج الشجرة."""


def pin(pc: dict[tuple[str, str], list[tuple[str, str]]],
        cands: Any) -> dict[str, object]:
    """مرشَّحو كلّ بندٍ تقاطعُ تشكيلات لين لأمثلته (وزنُ المفرد ← وزنُ الجمع)؛ ثمّ `pin_unique`."""

    def cset(ex: tuple[str, str]) -> set[tuple[str, str]]:
        out: set[tuple[str, str]] = set()
        root = ex[0][:3]
        for key, w in pc.get(ex, []):
            sp, pp = cands(key, root), cands(w, root)
            if sp and pp and len(sp) == 1 and len(pp) == 1:
                out.add((next(iter(sp)), next(iter(pp))))
        return out

    per = {"/".join(ex): sorted(cset(ex)) for ex in CLAUSE_A + CLAUSE_B}
    ca = set.intersection(*(cset(ex) for ex in CLAUSE_A))
    cb = set.intersection(*(cset(ex) for ex in CLAUSE_B))
    pinned = None
    if len(cb) == 1:
        rest = sorted(ca - cb)
        if len(rest) == 1:
            pinned = rest[0]
    return {"per_example": {k: [list(x) for x in v] for k, v in per.items()},
            "clause_a": sorted(list(x) for x in ca), "clause_b": sorted(list(x) for x in cb),
            "pinned": list(pinned) if pinned else None, "source": FUULA_SOURCE}


# --- ٤. المحقِّقُ الأماميّ ------------------------------------------------------------------------

LIT_ATOM = {"ة": "ت"}


def realizations(pattern: str, rad: str) -> list[list[str]]:
    """صورُ الوزن على الجذر بمرآة `realizeN`: الجسمُ إلى آخر أصل، وحركةُ ذلك الأصل إن حُذفت (إعرابٌ)
    تُعدَّد، ثمّ ما بعده من حروفٍ زائدة كما هي."""

    toks = pattern.split()
    j = max((i for i, t in enumerate(toks) if t[0] in "123"), default=-1)
    if j < 0:
        return []
    body: list[tuple[str, str, str]] = [("slot", t[0], t[1:]) if t[0] in "123"
                                        else ("lit", t[0], t[1:]) for t in toks[:j]]
    last = int(toks[j][0]) - 1
    tail = [LIT_ATOM.get(t[0], t[0]) + t[1:] for t in toks[j + 1:]]
    hs = [toks[j][1:]] if toks[j][1:] else [FA, KA, DA, SU]
    return [NM.realize((False, last, body), rad, False, h) + tail for h in hs]


def same(real: list[str], surf: tuple[str, ...]) -> bool:
    """تطابقٌ بالخانات إلّا حركةَ الأخير (إعرابٌ أو وقف)."""

    return (len(real) == len(surf) and real[:-1] == list(surf[:-1])
            and bool(real) and real[-1][0] == surf[-1][0])


def surface(atoms: tuple[str, ...], word: str) -> tuple[str, ...]:
    if word and word[-1] in L.TANWIN and atoms and atoms[-1] == "نْ":
        return atoms[:-1]
    return atoms


def refine(cs: set[str] | None, rad: str, atoms: tuple[str, ...], word: str
           ) -> tuple[set[str] | None, str]:
    """(المرشَّحون بعد التحقيق، الحال): `UNBOUNDED` (لا قائمة)، `NO_REALIZATION` (لا مرشَّحَ يعيد
    الخانات — تبقى القائمةُ كما هي)، `REFINED`."""

    if cs is None:
        return None, "UNBOUNDED"
    surf = surface(atoms, word)
    keep = {p for p in cs if any(same(r, surf) for r in realizations(p, rad))}
    if not keep:
        return cs, "NO_REALIZATION"
    return keep, "REFINED"


# --- ٥. القياس ------------------------------------------------------------------------------------


def frame_size(u: int, n: int) -> int:
    if n == 0 or u == 0:
        return 0
    return min(u, math.ceil((1.959963984540054 * 0.5 * u / n / TARGET) ** 2))


def frame_order(file: str, entry: str) -> str:
    return hashlib.sha256(f"{SEED}\t{file}\t{entry}".encode()).hexdigest()


def estimate(rows: list[list[str]], hit: dict[tuple[str, str], dict[str, bool]],
             lo: int, u: int, n: int) -> dict[str, object] | None:
    """التقديرُ من الإطار المملوء: لكلّ مدخلٍ إصابتُه بقيمة المالك (1، 0، أو 01 فيُحصر)؛ ولا شيء
    قبل ملء الكلّ."""

    vals = [r[4].strip() for r in rows]
    if not rows or any(v not in ("1", "0", "01") for v in vals):
        return None
    qlo = qhi = 0
    for r, v in zip(rows, vals):
        hs = [hit[(r[0], r[1])][t] for t in v]
        qlo += min(hs)
        qhi += max(hs)
    m = len(rows)

    def t(q: float) -> float:
        return round(1 - (lo + u * q) / n, 4)

    wl, wh = L.wilson(qlo, m), L.wilson(qhi, m)
    return {"m": m, "q_low": round(qlo / m, 4), "q_high": round(qhi / m, 4),
            "transmitted": [t(qhi / m), t(qlo / m)], "ci95": [t(wh[1]), t(wl[0])]}


def measure() -> dict[str, object]:
    from gate.api import LANE_CORPUS, Gate, Refusal, sealed_forms
    from gate.residue import repair

    masdar = L.read_tsv(H.MASDAR_V2)
    plural = L.read_tsv(H.PLURAL_V2)
    weak_m, weak_p = S.weak_records()
    _, pc = S.relaxed_list_candidates()
    words: set[str] = set()
    for r in masdar + weak_m:
        words.add(r[5])
        words.update(r[7].split())
    for r in plural + weak_p:
        words.add(r[5])
        words.update(r[6].split())
    for v in pc.values():
        for a, b in v:
            words.update((a, b))
    gate = Gate(corpus=LANE_CORPUS,
                domain={repair(w)[0] for w in words} & sealed_forms(LANE_CORPUS))
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

    def cands(w: str, rad: str, fwd: bool = False) -> set[str] | None:
        a = atoms(w)
        if a is None:
            return None
        cs = S.over(a, rad, w)
        return refine(cs, rad, a, w)[0] if fwd else cs

    def verb_atoms(key: str) -> tuple[str, ...] | None:
        a = atoms(key)
        if a is None:
            return None
        if key.endswith(L.PRONOUN) and a and a[-1] == "هُ":
            a = a[:-1]
        return a

    def verb_cands(key: str, rad: str, fwd: bool = False) -> set[str] | None:
        a = verb_atoms(key)
        if a is None:
            return None
        cs = S.over(a, rad, "")
        return refine(cs, rad, a, "")[0] if fwd else cs

    v1 = json.loads(L.RESULT.read_text(encoding="utf-8"))
    strict_m = {k: set(v) for k, v in v1["masdar"]["rules"].items()}
    strict_p = {k: set(v) for k, v in v1["plural"]["rules"].items()}

    # ٣. التعيينُ بالتمايز
    fuula = pin(pc, lambda w, r: cands(w, r))
    pinned_p = {k: set(v) for k, v in strict_p.items()}
    if fuula["pinned"]:
        sp, pp = fuula["pinned"]  # type: ignore[misc]
        pinned_p.setdefault(sp, set()).add(pp)

    # ١أ. الشواهد
    rads = {r[4] for r in masdar + weak_m}
    wit = corpus_witnesses(rads)
    example_roots = ({r for _, r, _ in L.MASDAR_RULES} | {s[:3] for s, _ in L.PLURAL_RULES})

    def in_scope(r: list[str]) -> bool:
        return r[1] not in L.DEV_FILES and r[3] not in example_roots

    ids = {(r[1], r[2]) for r in masdar + weak_m if in_scope(r)}
    form1, texts = lane_pass(ids)

    def union(rad: str, key: str) -> set[str]:
        return set().union(*(wit[lab].get(rad, {}).get(key, set()) for lab in wit))

    # المصدر
    m_out: dict[str, object] = {}
    m_counts: dict[str, Counter[str]] = defaultdict(Counter)
    a_obj: dict[str, list[int]] = {g: [0, 0, 0, 0] for g in ("pos", "neg_label", "neg_stative")}
    u_rows: list[list[str]] = []
    u_hit: dict[tuple[str, str], dict[str, bool]] = {}
    sound_lo = sound_n = 0
    for st in ("sound", "hamzated", "doubled", "weak", "pooled"):
        acc: dict[str, list[int]] = {k: [0, 0] for k in ("strict_wit3", "strict_wit4")}
        if st == "weak":
            acc["strict_wit4_fwd"] = [0, 0]
        n = 0
        n_fwd = 0
        for r in masdar + weak_m:
            if not in_scope(r) or (st != "pooled" and r[0] != st):
                continue
            rad = r[4]
            vcand = verb_cands(r[5], rad)
            if vcand is None:
                continue
            babs = {p.split()[1][1:] for p in vcand if S._facala(p)}
            assimilated = any(S._assimilated(p) for p in vcand)
            fakk, trans_p, impf = union(rad, "fakk"), union(rad, "trans"), union(rad, "impf")
            if not babs and assimilated:
                babs = (fakk | trans_p) or {FA, KA, DA}
            if not babs:
                continue
            ms = [cands(w, rad) for w in r[7].split()]
            if not any(ms):
                continue
            n += 1
            unique = form1[r[3]] == 1
            w3 = bool(babs & trans_p)
            w_impf = unique and bool(babs & compat_babs(impf))
            w4 = w3 or w_impf
            t3 = {"1"} if (r[6] == "1" or w3) else {"0", "1"}
            t4 = {"1"} if (r[6] == "1" or w4) else {"0", "1"}
            if st != "pooled":
                m_counts[st]["UNIQUE_FORM1" if unique else "SHARED_FORM1"] += 1
                if r[6] == "0":
                    m_counts[st]["UNMARKED_" + ("WITNESSED_PAST" if w3 else
                                                "WITNESSED_IMPERFECT_ONLY" if w4 else
                                                "UNWITNESSED")] += 1
            if st == "sound":
                g = "pos" if r[6] == "1" else lane_label(texts.get((r[1], r[2]), ""))
                if g:
                    a_obj[g][0] += 1
                    a_obj[g][1] += w3
                    a_obj[g][2] += w_impf
                    a_obj[g][3] += w4
            for key, tset in (("strict_wit3", t3), ("strict_wit4", t4)):
                lo, hi = S.hit_bounds(S.classes(babs, tset), ms, strict_m)
                acc[key][0] += lo
                acc[key][1] += hi
                if st == "sound" and key == "strict_wit4":
                    sound_lo += lo
                    if lo != hi:
                        u_rows.append([r[1], r[2], r[4], r[5], ""])
                        u_hit[(r[1], r[2])] = {
                            t: S.hit_bounds(S.classes(babs, {t}), ms, strict_m)[0]
                            for t in ("0", "1")}
            if st == "weak":
                vf = verb_cands(r[5], rad, fwd=True) or set()
                babs_f = {p.split()[1][1:] for p in vf if S._facala(p)} or babs
                msf = [cands(w, rad, fwd=True) for w in r[7].split()]
                t4f = {"1"} if (r[6] == "1" or bool(babs_f & trans_p)
                                or (unique and bool(babs_f & compat_babs(impf)))) else {"0", "1"}
                lo, hi = S.hit_bounds(S.classes(babs_f, t4f), msf, strict_m)
                acc["strict_wit4_fwd"][0] += lo
                acc["strict_wit4_fwd"][1] += hi
                n_fwd += 1
        if st == "sound":
            sound_n = n
        m_out[st] = {k: H.bounds(v[0], v[1], n) for k, v in acc.items()}

    # ١ب. الإطار
    u_rows.sort(key=lambda r: frame_order(r[0], r[1]))
    m = frame_size(len(u_rows), sound_n)
    frame = u_rows[:m]
    filled = read_frame()
    if filled and [r[:4] for r in filled] == [r[:4] for r in frame]:
        frame = filled
    est = estimate(frame, u_hit, sound_lo, len(u_rows), sound_n)

    # الجمع
    p_out: dict[str, object] = {}
    for st in ("sound", "hamzated", "doubled", "weak", "pooled"):
        accp = {k: [0, 0] for k in ("strict", "pinned")}
        if st == "weak":
            accp["pinned_fwd"] = [0, 0]
        n = 0
        for r in plural + weak_p:
            if not in_scope(r) or (st != "pooled" and r[0] != st):
                continue
            sc = cands(r[5], r[4])
            if not sc:
                continue
            ps = [cands(w, r[4]) for w in r[6].split()]
            if not any(ps):
                continue
            n += 1
            for key, rules in (("strict", strict_p), ("pinned", pinned_p)):
                lo, hi = S.hit_bounds(sc, ps, rules)
                accp[key][0] += lo
                accp[key][1] += hi
            if st == "weak":
                scf = cands(r[5], r[4], fwd=True) or sc
                psf = [cands(w, r[4], fwd=True) for w in r[6].split()]
                lo, hi = S.hit_bounds(scf, psf, pinned_p)
                accp["pinned_fwd"][0] += lo
                accp["pinned_fwd"][1] += hi
        p_out[st] = {k: H.bounds(v[0], v[1], n) for k, v in accp.items()}

    return {
        "lines_sha256": L.sha(L.render(L.lines())),
        "witness_roots": {lab: {k: sum(1 for v in per.values() if v[k])
                                for k in ("trans", "fakk", "impf")}
                          for lab, per in sorted(wit.items())},
        "a_obj": {g: {"n": v[0], "past": v[1], "imperfect": v[2], "any": v[3],
                      "rate_any": round(v[3] / v[0], 4) if v[0] else None,
                      "ci95_any": L.wilson(v[3], v[0])} for g, v in a_obj.items()},
        "a_fwd": a_fwd(masdar, plural, weak_m, atoms, verb_atoms, in_scope),
        "fuula": fuula,
        "masdar": {"strata": m_out,
                   "counts": {k: dict(sorted(v.items())) for k, v in sorted(m_counts.items())}},
        "plural": {"strata": p_out},
        "frame": {"seed": SEED, "target_half_width": TARGET, "n": sound_n,
                  "hits_low": sound_lo, "unresolved": len(u_rows), "m": m,
                  "filled": sum(1 for r in frame if r[4].strip()), "estimate": est},
        "refusals": dict(sorted(refusals.items())),
        "_frame_rows": frame,
    }


def a_fwd(masdar: list[list[str]], plural: list[list[str]], weak_m: list[list[str]],
          atoms: Any, verb_atoms: Any, in_scope: Any) -> dict[str, object]:
    """تغطيةُ `A_FWD`: (أ) على الصحيح — المحقِّقُ يعيد وزنَ الكلمة على جذرها (هويّة)؛ (ب) على مفاتيح
    الأفعال المعتلّة — أحالُها `REFINED` وفيها فَعَلَ بأبوابه؟"""

    ident = Counter[str]()
    for r in masdar:
        if not in_scope(r) or r[0] != "sound":
            continue
        for w in r[7].split():
            a = atoms(w)
            cs = S.over(a, r[4], w) if a is not None else None
            if not cs or len(cs) != 1:
                continue
            ident["masdar_n"] += 1
            ident["masdar_ok"] += refine(cs, r[4], a, w)[1] == "REFINED"
    for r in plural:
        if not in_scope(r) or r[0] != "sound":
            continue
        for w in [r[5], *r[6].split()]:
            a = atoms(w)
            cs = S.over(a, r[4], w) if a is not None else None
            if not cs or len(cs) != 1:
                continue
            ident["plural_n"] += 1
            ident["plural_ok"] += refine(cs, r[4], a, w)[1] == "REFINED"
    verbs: Counter[str] = Counter()
    for r in weak_m:
        if not in_scope(r):
            continue
        a = verb_atoms(r[5])
        if a is None:
            continue
        cs, status = refine(S.over(a, r[4], ""), r[4], a, "")
        verbs[status] += 1
        if status == "REFINED":
            verbs["REFINED_FACALA"] += any(S._facala(p) for p in cs or set())
            verbs["REFINED_SIZE_1"] += len(cs or set()) == 1
    ref = verbs["REFINED"]
    return {"sound_identity": {"masdar": [ident["masdar_ok"], ident["masdar_n"]],
                               "plural": [ident["plural_ok"], ident["plural_n"]]},
            "weak_verbs": dict(sorted(verbs.items())),
            "weak_verbs_facala_rate": round(verbs["REFINED_FACALA"] / ref, 4) if ref else None,
            "weak_verbs_facala_ci95": L.wilson(verbs["REFINED_FACALA"], ref)}


def read_frame() -> list[list[str]]:
    if not FRAME.exists():
        return []
    rows = [r.split("\t") for r in FRAME.read_text(encoding="utf-8").splitlines()]
    return [r + [""] * (5 - len(r)) for r in rows[1:]]


def frame_bytes(rows: list[list[str]]) -> bytes:
    return L.tsv(FRAME_HEADER, rows)


def main(argv: list[str]) -> int:
    if "--check" in argv:
        res = measure()
        rows = res.pop("_frame_rows")
        if FRAME.exists() and [r[:4] for r in read_frame()] != [r[:4] for r in rows]:
            sys.stderr.write("LANE_FRAME_DRIFTED\n")
            return 1
        if RESULT_V4.exists() and RESULT_V4.read_bytes() != L.dump(res):
            sys.stderr.write("LANE_TAHDID_RESULT_DRIFTED\n")
            return 1
        sys.stdout.write("تعيينُ لين مطابق\n")
        return 0
    if "measure" in argv:
        res = measure()
        rows = res.pop("_frame_rows")
        if not FRAME.exists():
            FRAME.write_bytes(frame_bytes(rows))
        RESULT_V4.write_bytes(L.dump(res))
        sys.stdout.write(f"كُتب {RESULT_V4.relative_to(ROOT)}\n")
        return 0
    sys.stdout.write("measure | --check\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
