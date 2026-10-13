"""فهرسُ الصنف المغلق (MUGHLAQ_INDEX.md) — الوسمُ الذي يفصل المبنيّات عن الاسم والفعل (ADR ٥٣،
٥٤)، بتسجيلين مسبقين: `docs/mughlaq/PREREG.md` و`docs/mughlaq/PREREG-2.md`.

ثلاثةُ أنظمةٍ بقاعدةٍ واحدة للوسم (مغلقٌ إن قُرئ بنواةٍ ليست ظرفًا):

* `S0` — الموزِّعُ قبل ADR ٥٣ منسوخًا بعينه (`before`): يعيد أرقامَ `TAWZI_INDEX.md` السابقة
  (854؛ 13,151 / 655 / 507) ورقمَي ADR ٥٢ (20,498، 70) — `tests/test_mughlaq_index.py`.
* `S1` — بعد ADR ٥٣ (`389d86a`)؛ نظامُه لم يعد في الشجرة فأرقامُه المطبوعة ثابتةٌ هنا (`RECORDED_S1`).
* `S2` — بعد سداد الديون (ADR ٥٤): `slge.mughlaq.qism` الآن.

القياسُ بترتيب قانون القارئ: (١) مودَعُ شهادات المصحف كاملًا؛ (٢) QAC 0.4 (`qac-pos.tsv.gz`): الدقّةُ
والاستدعاءُ بفاصل Wilson، وحكما التسجيلين، وتفكيكُ خطأ S2 إلى حدٍّ أدنى لا تفصله الخانات وخلافِ تعريفٍ
وقابلٍ للإصلاح (`Mughlaq.const_errors_ge_min`)، وصدقُ المعنى بالصنف؛ (٣) MASAQ — مفحوصٌ لا مقيس.
"""

from __future__ import annotations

import gzip
import json
import math
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from slge.categories import PRONOUNS
from slge.categories import PRONOUNS as _PRONOUNS
from slge.damair import DETACHED_NASB
from slge.huruf import TABLE as HURUF
from slge.ishara import FORMS as ISHARA
from slge.istifham import FORMS as ISTIFHAM
from slge.jidh import OBJECT_SUFFIXES, PROCLITICS
from slge.marifa import MAWSUL
from slge.mughlaq import ZARF_CELLS, closed, qism
from slge.pipeline import GOLD_JIHA
from slge.rawabit import PARTICLES, cells_of
from slge.tawzi import COMPOUNDS, alif_to_ya, junction, tawzi
from slge.zaman import CONSTANTS as ZAMAN_CONSTANTS
from slge.zaman import STEMS as ZAMAN
from slge.zaman import forms_of
from slge.zuruf import CONSTANTS, STEMS, jarr, mudaf, qat

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "MUGHLAQ_INDEX.md"
DATA = ROOT / "tests" / "data"
Word = tuple[tuple[str, str], ...]
MARKS = {"فتح": "َ", "كسر": "ِ", "ضم": "ُ", "سكون": "ْ"}
OPEN = frozenset({"N", "PN", "ADJ", "IMPN", "V"})
ZARF = frozenset({"T", "LOC"})
PRE_IN_STEM = ("IMPERF_PREF", "CV_PREF", "IV1S", "IV1P", "IV2MP", "IV3MS", "IV3MP", "IV3FS")

HURUF_CELLS = frozenset(h.cells for h in HURUF)
COMPOUND_CELLS = frozenset(w for _, _, w in COMPOUNDS)
DAMIR_CELLS = frozenset((*_PRONOUNS, *(p.cells for p in DETACHED_NASB)))

# — S0: الموزِّع قبل ADR ٥٣ بعينه (جدولُه كما بناه `_table` يومئذٍ: الفعلان وذُو فيه) —
def _old_table() -> tuple[tuple[str, str, Word], ...]:
    rows: list[tuple[str, str, Word]] = []
    rows += [("حرف", p.name, cells_of(p.name)) for p in PARTICLES if not p.proclitic]
    rows += [("ضمير", "", w) for w in PRONOUNS]
    rows += [("ضمير", p.name, p.cells) for p in DETACHED_NASB]
    rows += [("إشارة", f.name, f.cells) for f in ISHARA]
    rows += [("استفهام", f.name, f.cells) for f in ISTIFHAM]
    rows += [("موصول", n, w) for n, w in MAWSUL.items()]
    rows += [("ظرف", z.name, form(z.stem)) for z in STEMS for form in (mudaf, jarr, qat)]
    rows += [("ظرف", n, w) for n, w in CONSTANTS.items()]
    rows += [("ظرف", n, f) for n, st in ZAMAN.items() for f in forms_of(st)]
    rows += [("ظرف", n, w) for n, (w, _) in ZAMAN_CONSTANTS.items()]
    return tuple(rows)


_OLD_CORES: dict[Word, tuple[str, str]] = {}
for _k, _n, _w in _old_table():
    if _w:
        _OLD_CORES.setdefault(_w, (_k, _n))
_OLD_HOSTS: dict[Word, tuple[str, str]] = {
    cells_of(p.name): ("حرف", p.name) for p in PARTICLES if p.proclitic}
_LI: Word = (("ل", "كسر"),)
_PRES: tuple[tuple[Word, ...], ...] = (
    (), *((p,) for p in PROCLITICS), *((p, q) for p in PROCLITICS for q in PROCLITICS))


def _old_variants(core: Word, suf: Word) -> tuple[Word, ...]:
    if suf:
        return core, alif_to_ya(core), ((("ل", "فتح"),) if core == _LI else core)
    k, f = junction(core)
    return core, k, f


def before(w: Word) -> tuple[tuple[tuple[Word, ...], Word, Word, str], ...]:
    """قراءاتُ الموزِّع قبل الإغلاق: (السوابق، النواة، اللاحقة، الباب) بترتيبها القديم."""

    out: list[tuple[tuple[Word, ...], Word, Word, str]] = []
    for pre in _PRES:
        flat = tuple(c for p in pre for c in p)
        if w[: len(flat)] != flat:
            continue
        rest = w[len(flat):]
        for suf in ((), *OBJECT_SUFFIXES):
            if suf and rest[len(rest) - len(suf):] != suf:
                continue
            surface = rest[: len(rest) - len(suf)] if suf else rest
            if not surface:
                continue
            cores = {**_OLD_CORES, **_OLD_HOSTS} if suf else _OLD_CORES
            for core, (kind, _name) in cores.items():
                if surface in _old_variants(core, suf):
                    out.append((pre, core, suf, kind))
    return tuple(out)


def qism0(w: Word) -> str:
    rs = before(w)
    if any(core not in ZARF_CELLS for _, core, _, _ in rs):
        return "مغلق"
    return "ظرف" if rs else "مفتوح"


# — المودَعات —

def certificates() -> tuple[list[Word], list[int]]:
    with gzip.open(DATA / "corpus-certificates.json.gz", "rt", encoding="utf-8") as f:
        d: dict[str, Any] = json.load(f)
    return [tuple((a, b) for a, b in x["cells"]) for x in d["forms"]], list(d["stream"])


def qac_rows() -> list[tuple[int, str, str]]:
    """(الموقع، القطع، قسمُ الجذع) من `qac-pos.tsv.gz`."""

    raw = gzip.decompress((DATA / "qac-pos.tsv.gz").read_bytes()).decode("utf-8").splitlines()
    out = []
    for r in raw[1:]:
        tok, _loc, segs, stem = r.split("\t")
        out.append((int(tok), segs, stem))
    return out


def masaq_rows() -> list[dict[str, Any]]:
    with gzip.open(DATA / "masaq-shibh.json.gz", "rt", encoding="utf-8") as f:
        rows: list[dict[str, Any]] = json.load(f)["rows"]
    return rows


def vowelled(w: Word) -> str:
    return "".join(k + MARKS[s] for k, s in w)


def gold_class(stem: str) -> str:
    return "مفتوح" if stem in OPEN else "ظرف" if stem in ZARF else "مغلق"


def wilson(k: int, n: int, z: float = 1.959964) -> list[float]:
    if n == 0:
        return [0.0, 0.0]
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [round(c - h, 6), round(c + h, 6)]


def rate(k: int, n: int) -> dict[str, Any]:
    return {"k": k, "n": n, "p": round(k / n, 6) if n else None, "wilson95": wilson(k, n)}


def confusion(pairs: list[tuple[str, str]]) -> dict[str, Any]:
    """(الذهبيّ، المتنبَّأ) ← المصفوفة، والدقّةُ والاستدعاءُ على الذهبيّ مغلقًا أو مفتوحًا."""

    m = Counter(pairs)
    core = [(g, p) for g, p in pairs if g != "ظرف"]
    tp = sum(1 for g, p in core if g == p == "مغلق")
    pred = sum(1 for _, p in core if p == "مغلق")
    gold = sum(1 for g, _ in core if g == "مغلق")
    opened = sum(1 for g, _ in core if g == "مفتوح")
    leak = sum(1 for g, p in core if g == "مفتوح" and p == "مغلق")
    return {"matrix": {f"{g}→{p}": n for (g, p), n in sorted(m.items())},
            "precision": rate(tp, pred), "recall": rate(tp, gold), "open_leak": rate(leak, opened)}


def verdict(s0: dict[str, Any], s1: dict[str, Any]) -> str:
    """قاعدةُ التسجيل (PREREG §٤): `CLOSURE_BETTER` إن جاوز حدُّ S1 الأدنى للاستدعاء حدَّ S0
    الأعلى، ولم ينزل حدُّ
    S1 الأدنى للدقّة عن حدّ S0 الأدنى بأكثرَ من نقطة."""

    up = s1["recall"]["wilson95"][0] > s0["recall"]["wilson95"][1]
    keep = s1["precision"]["wilson95"][0] >= s0["precision"]["wilson95"][0] - 0.01
    return "CLOSURE_BETTER" if up and keep else (
        "CLOSURE_NOT_BETTER" if not up else "CLOSURE_LOSES_PRECISION")


def tawzi_split(rows: list[dict[str, Any]], reader: Any) -> dict[str, int]:
    """مقاييسُ فهرس الموزِّع على MASAQ: قسمةُ المرجع، وغيرُها، ولا يُقرأ."""

    gold = wrong = none = 0
    sep_n = sep = 0
    for r in rows:
        w: Word = (*((a, b) for _, cs in r["pre"] for a, b in cs), *((a, b) for a, b in r["stem"]),
                   *((a, b) for _, cs in r["suf"] for a, b in cs))
        if r["tag"] in GOLD_JIHA:  # الفصلُ الخاطئ بتعريف ADR ٥٢: المفتوحُ عند المرجع يقرؤه الموزِّع
            if r["tag"] not in ("ADV", "NOUN_ABSTRACT"):
                sep_n += 1
                sep += bool(reader(w))
            continue
        ms = reader(w)
        if not ms:
            none += 1
            continue
        pre = tuple((a, b) for t, cs in r["pre"] for a, b in cs
                    if t not in PRE_IN_STEM and t != "DET")
        suf = tuple((a, b) for _, cs in r["suf"] for a, b in cs)
        p0, s0 = ms[0]
        gold += tuple(c for p in p0 for c in p) == pre and s0 == suf
        wrong += not (tuple(c for p in p0 for c in p) == pre and s0 == suf)
    return {"gold": gold, "wrong": wrong, "none": none, "open_population": sep_n,
            "open_read": sep}


def adr52_rule(s0: dict[str, int], s1: dict[str, int]) -> str:
    """قاعدةُ القرار المسجَّلة في ADR ٥٢ (الجلسةُ الأخرى) على النظام كلّه: نقص «لا يُقرأ» وزاد «بقسمة
    المرجع» وزيادةُ الفصل الخاطئ أقلُّ من نصف زيادة «بقسمة المرجع»."""

    dg = s1["gold"] - s0["gold"]
    ok = s1["none"] < s0["none"] and dg > 0 and 2 * (s1["open_read"] - s0["open_read"]) < dg
    return "ADR52_ACCEPTED" if ok else "ADR52_REJECTED"


# — الجولةُ الأولى مسجَّلةً (ADR ٥٣، `389d86a`): نظامُها لم يعد في الشجرة، فأرقامُها ثابتةٌ هنا كما طُبعت —
RECORDED_S1: dict[str, Any] = {
    "matrix": {"ظرف→ظرف": 1314, "ظرف→مغلق": 188, "ظرف→مفتوح": 332, "مغلق→ظرف": 20,
               "مغلق→مغلق": 24877, "مغلق→مفتوح": 293, "مفتوح→ظرف": 921, "مفتوح→مغلق": 245,
               "مفتوح→مفتوح": 49173},
    "forms": {"مغلق": 729, "ظرف": 208, "مفتوح": 17242},
    "positions": {"مغلق": 25319, "ظرف": 2256, "مفتوح": 50632},
    "masaq": {"gold": 13562, "wrong": 617, "none": 134, "open_population": 20498, "open_read": 65},
}


def confusion_from_matrix(matrix: dict[str, int]) -> dict[str, Any]:
    """المصفوفةُ ← الدقّةُ والاستدعاءُ والتسرّب بتعريف `confusion` نفسِه."""

    pairs = [tuple(k.split("→")) for k, n in matrix.items() for _ in range(n)]
    return confusion([(g, p) for g, p in pairs])


def verdict2(s1: dict[str, Any], s2: dict[str, Any]) -> str:
    """قاعدةُ التسجيل الثاني (PREREG-2 §٤): `DEBTS_BETTER` إن جاوز حدُّ S2 الأدنى للاستدعاء حدَّ S1
    الأعلى
    ولم ينزل حدُّ S2 الأدنى للدقّة عن حدّ S1 الأدنى بأكثرَ من نقطة."""

    up = s2["recall"]["wilson95"][0] > s1["recall"]["wilson95"][1]
    keep = s2["precision"]["wilson95"][0] >= s1["precision"]["wilson95"][0] - 0.01
    return "DEBTS_BETTER" if up and keep else (
        "DEBTS_NOT_BETTER" if not up else "DEBTS_LOSE_PRECISION")


def floor(rows: list[tuple[int, str]], pred: list[str]) -> dict[str, Any]:
    """تفكيكُ خطأ الوسم على الذهبيّ مغلقًا أو مفتوحًا (PREREG-2 §٣): الوسمُ دالّةٌ في الخانات، فكلُّ صورةٍ
    بوسمٍ واحد، وخطؤها لا ينزل عن أقلِّ صنفَيها (`Mughlaq.const_errors_ge_min`). فالخطأُ = **الحدُّ
    الأدنى**
    (Σ الأقلّ: متجانساتُ الخانات) + **خلافُ التعريف** (صورٌ صنفُها عند المرجع واحدٌ ووسمُنا غيرُه) +
    **القابلُ
    للإصلاح** (صورٌ مختلطةٌ أخذنا فيها الأقلّ)."""

    by: dict[int, Counter[str]] = {}
    for i, g in rows:
        if g != "ظرف":
            by.setdefault(i, Counter())[g] += 1
    out = {"errors": 0, "floor": 0, "definitional": 0, "reducible": 0}
    top: dict[str, Counter[int]] = {"floor": Counter(), "definitional": Counter(),
                                    "reducible": Counter()}
    for i, c in by.items():
        closed, opened = c["مغلق"], c["مفتوح"]
        err = opened if pred[i] == "مغلق" else closed
        low = min(closed, opened)
        out["errors"] += err
        out["floor"] += low
        top["floor"][i] += low
        if low == 0:
            out["definitional"] += err
            top["definitional"][i] += err
        else:
            out["reducible"] += err - low
            top["reducible"][i] += err - low
    assert out["errors"] == out["floor"] + out["definitional"] + out["reducible"]
    return {**out, "top": {k: [[i, n] for i, n in v.most_common(10) if n] for k, v in top.items()}}


GOLD_MEANING: dict[str, str] = {"PRON": "ضمير", "DEM": "إشارة", "REL": "موصول", "INTG": "استفهام"}
"""صنفُ المعنى عند المرجع (PREREG-2 §٣، معلن): قسمُ الجذع ضميرًا أو إشارةً أو موصولًا أو استفهامًا، وما
سواه
من أقسام المغلق حرف."""


def meaning_classes(core: Word) -> frozenset[str]:
    """أصنافُ المعنى التي تجعلها مصادرُنا للنواة — كلُّها لا أوّلُها (`mughlaq.src` يأخذ الأوّل)."""

    out: set[str] = set()
    if (core in HURUF_CELLS or core in COMPOUND_CELLS
            or any(cells_of(p.name) == core for p in PARTICLES)):
        out.add("حرف")
    if core in DAMIR_CELLS:
        out.add("ضمير")
    if any(f.cells == core for f in ISHARA):
        out.add("إشارة")
    if any(f.cells == core for f in ISTIFHAM):
        out.add("استفهام")
    if core in MAWSUL.values():
        out.add("موصول")
    return frozenset(out)


def meaning(kept: list[tuple[int, str, str]], forms: list[Word], pred: list[str]) -> dict[str, Any]:
    """صدقُ المعنى بالصنف (PREREG-2 §٣): على ما هو مغلقٌ عند المرجع وعندنا معًا، هل صنفُ معنى المرجع في
    أصناف
    مصادرنا لنوى القراءات المغلقة؟ ومعه متوسّطُ حجم المجموعة لئلّا يُخفي الاتّساعُ الخطأ."""

    hit = n = size = 0
    miss: Counter[tuple[str, str, str]] = Counter()
    for i, _segs, stem in kept:
        if gold_class(stem) != "مغلق" or pred[i] != "مغلق":
            continue
        ours = frozenset().union(*(meaning_classes(m.core) for m in closed(forms[i])))
        g = GOLD_MEANING.get(stem, "حرف")
        n += 1
        size += len(ours)
        if g in ours:
            hit += 1
        else:
            miss[(vowelled(forms[i]), stem, "، ".join(sorted(ours)))] += 1
    return {"agree": rate(hit, n), "mean_set_size": round(size / n, 4) if n else None,
            "miss_top": [[w, t, o, k] for (w, t, o), k in miss.most_common(12)]}


def measure() -> dict[str, Any]:
    forms, stream = certificates()
    q0 = [qism0(w) for w in forms]
    q2 = [qism(w) for w in forms]
    deposit: dict[str, Any] = {
        name: {"forms": dict(Counter(q)),
               "positions": dict(Counter(q[i] for i in stream if i >= 0))}
        for name, q in (("S0", q0), ("S2", q2))}
    deposit["S1"] = {"forms": RECORDED_S1["forms"], "positions": RECORDED_S1["positions"]}
    rows = qac_rows()
    refused = sum(1 for t, _, _ in rows if stream[t] < 0)
    kept = [(stream[t], segs, stem) for t, segs, stem in rows if stream[t] >= 0]
    gold = [(i, gold_class(stem)) for i, _, stem in kept]
    qac = {"S0": confusion([(g, q0[i]) for i, g in gold]),
           "S1": confusion_from_matrix(RECORDED_S1["matrix"]),
           "S2": confusion([(g, q2[i]) for i, g in gold])}
    fl = floor(gold, q2)
    fl["top"] = {k: [[vowelled(forms[i]), n] for i, n in v] for k, v in fl["top"].items()}
    mrows = masaq_rows()
    m0 = tawzi_split(mrows, lambda w: [(pre, suf) for pre, _, suf, _ in before(w)])
    m2 = tawzi_split(mrows, lambda w: [(m.pre, m.suf) for m in tawzi(w)])
    return {"prereg": ["docs/mughlaq/PREREG.md", "docs/mughlaq/PREREG-2.md"],
            "reference": "QAC 0.4 (Dukes) — قسمُ الجذع",
            "deposit": deposit,
            "qac": {"rows": len(rows), "refused_by_gate": refused, "measured": len(kept), **qac,
                    "verdict": verdict(qac["S0"], qac["S1"]),
                    "verdict2": verdict2(qac["S1"], qac["S2"]),
                    "floor_S2": fl, "meaning_S2": meaning(kept, forms, q2)},
            "masaq_checked_not_measured": {"S0": m0, "S1": RECORDED_S1["masaq"], "S2": m2,
                                           "adr52_rule": adr52_rule(m0, m2)}}


def _pct(r: dict[str, Any]) -> str:
    lo, hi = r["wilson95"]
    return f"{100 * (r['p'] or 0):.2f}٪ [{100 * lo:.2f}، {100 * hi:.2f}] (n = {r['n']:,})"


def render(m: dict[str, Any] | None = None) -> str:
    m = m or measure()
    d, q, ms = m["deposit"], m["qac"], m["masaq_checked_not_measured"]
    fl, mn = q["floor_S2"], q["meaning_S2"]
    sys3 = ("S0", "S1", "S2")

    def qs(c: dict[str, int]) -> str:
        return "، ".join(f"{k} {c.get(k, 0):,}" for k in ("مغلق", "ظرف", "مفتوح"))

    lines = [
        "# فهرسُ الصنف المغلق — وسمٌ يفصل المبنيّات عن الاسم والفعل",
        "",
        "مولَّدٌ بـ`python tools/gen_mughlaq_index.py` من `src/slge/mughlaq.py` و`src/slge/tawzi.py`؛ "
        "لا يُحرَّر باليد. البرهانُ `formal/Slge/Mughlaq.lean` (القسمةُ `maftuh_iff`، `mughlaq_iff`؛ "
        "إغلاقُ المعنى `closed_has_src`؛ حدُّ الخطأ `const_errors_ge_min`) و`formal/Slge/Tawzi.lean` "
        "(اللاحقةُ لا يحملها إلّا حاملُها `tawzi_suf_host`؛ شواهدُ القواعد والديون). S0 الموزِّعُ قبل "
        "ADR ٥٣، وS1 بعده مسجَّلًا (`389d86a`، أرقامُه ثابتة)، وS2 بعد سداد الديون (ADR ٥٤).",
        "",
        "## على مودَع المصحف أوّلًا (قانونُ القارئ)", "",
        "| النظام | الصور (18,179) | المواقع |", "|---|---|---|",
        *(f"| {k} | {qs(d[k]['forms'])} | {qs(d[k]['positions'])} |" for k in sys3),
        "",
        "## على QAC 0.4 (مرجعٌ بشريٌّ لقسم الجذع)", "",
        f"{q['rows']:,} كلمةً محاذاة؛ ترفض البوّابةُ {q['refused_by_gate']:,}، فالمقيس "
        f"{q['measured']:,} موقعًا. الذهبيُّ: مفتوحٌ ‎N PN ADJ IMPN V‎، ظرفٌ ‎T LOC‎، وما سواهما "
        "مغلق؛ الدقّةُ والاستدعاءُ على الذهبيّ مغلقًا أو مفتوحًا، والظرفُ يُعدّ في المصفوفة وحدَها.",
        "",
        "| النظام | الدقّة | الاستدعاء | المفتوحُ موسومًا مغلقًا |", "|---|---|---|---|",
        *(f"| {k} | {_pct(q[k]['precision'])} | {_pct(q[k]['recall'])} | "
          f"{_pct(q[k]['open_leak'])} |" for k in sys3),
        "",
        f"**حكمُ التسجيل الأوّل (S0 ← S1، مقيس): `{q['verdict']}`. وحكمُ التسجيل الثاني (S1 ← S2): "
        f"`{q['verdict2']}`** — مفحوصٌ لا مقيس: الديونُ عُرفت من هذا المرجع (PREREG-2 §٥).",
        "",
        "| الذهبيّ→المتنبَّأ | S0 | S1 | S2 |", "|---|---|---|---|",
        *(f"| {k} | " + " | ".join(f"{q[s]['matrix'].get(k, 0):,}" for s in sys3) + " |"
          for k in sorted(set(q["S0"]["matrix"]) | set(q["S2"]["matrix"]))),
        "",
        "## تفكيكُ الخطأ الباقي (S2) — ما تفصله الخاناتُ وما لا تفصله", "",
        "الوسمُ دالّةٌ في الخانات، فالصورةُ الواحدة بوسمٍ واحد، وخطؤها لا ينزل عن أقلّ صنفَيها عند المرجع "
        "(`Mughlaq.const_errors_ge_min`).",
        "",
        "| الخطأ | المواقع |", "|---|---|",
        f"| الكلّ (مفتوحٌ موسومٌ مغلقًا + مغلقٌ غيرُ موسوم) | {fl['errors']:,} |",
        f"| الحدُّ الأدنى: متجانساتُ الخانات — لا تفصلها دالّةٌ في الخانات | {fl['floor']:,} |",
        f"| خلافُ التعريف: صورٌ صنفُها عند المرجع واحدٌ ووسمُنا غيرُه | {fl['definitional']:,} |",
        f"| القابلُ للإصلاح في الخانات: صورٌ مختلطةٌ أخذنا فيها الأقلّ | {fl['reducible']:,} |",
        "",
        *(f"- **{name}**: " + "، ".join(f"{w} {n:,}" for w, n in fl["top"][k]) + "."
          for k, name in (("floor", "الحدُّ الأدنى"), ("definitional", "خلافُ التعريف"),
                          ("reducible", "القابلُ للإصلاح")) if fl["top"][k]),
        "",
        "## صدقُ المعنى بالصنف (S2)", "",
        "على ما هو مغلقٌ عند المرجع وعندنا معًا: صنفُ معنى المرجع "
        "(ضمير/إشارة/موصول/استفهام/حرف من قسم "
        f"الجذع) في أصناف مصادرنا: **{_pct(mn['agree'])}**، ومتوسّطُ حجم المجموعة "
        f"{mn['mean_set_size']}.",
        "",
        "| الصورة | قسمُ QAC | أصنافُنا | العدد |", "|---|---|---|---|",
        *(f"| {w} | `{t}` | {o} | {k:,} |" for w, t, o, k in mn["miss_top"]),
        "",
        "## على MASAQ — مفحوصٌ لا مقيس", "",
        "قواعدُ الإغلاق صُمّمت بعد رؤية ما لا يقرؤه الموزِّعُ على MASAQ (PREREG §٥)، فهذه الأرقامُ "
        "فحصٌ لا قياس. على الكلمات التي لا جهةَ لها عند المرجع:",
        "",
        "| النظام | بقسمة المرجع | بغيرها | لا يُقرأ | المفتوحُ يقرؤه الموزِّع (ADR ٥٢) |",
        "|---|---|---|---|---|",
        *(f"| {k} | {ms[k]['gold']:,} | {ms[k]['wrong']:,} | {ms[k]['none']:,} | "
          f"{ms[k]['open_read']:,} من {ms[k]['open_population']:,} |" for k in sys3),
        "",
        f"وقاعدةُ القرار المسجَّلة في ADR ٥٢ على النظام كلّه (S0 ← S2): `{ms['adr52_rule']}`.",
        "",
        "## ما ليس هنا — باسمه", "",
        "- `HUKM_INPUT_CHANGED_BY_CLOSURE`: المغلقُ لا جذرَ يُحكم عليه (`Qiraa.mughlaq_no_hukm`)، "
        "فقياسُ ADR ٥٠ على المخصَّص يُعاد بكلّ نظامٍ جديد، والفرقُ في ADR ٥٣ و٥٤.",
        "- الظرفُ وسمٌ ثالث لا مغلق: عِنْدَ وقَبْلَ وإِذَا وحَيْثُ تُقرأ من جداولها ولا يُعدّ "
        "ظرفُها أداةً.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    text = render()
    if "--check" in sys.argv:
        if TARGET.read_text(encoding="utf-8") != text:
            sys.stderr.write("MUGHLAQ_INDEX.md غيرُ مطابق؛ شغّل tools/gen_mughlaq_index.py\n")
            return 1
        sys.stdout.write("MUGHLAQ_INDEX.md مطابق\n")
        return 0
    TARGET.write_text(text, encoding="utf-8")
    sys.stdout.write("كُتب MUGHLAQ_INDEX.md\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

