"""فهرسُ الصنف المغلق (MUGHLAQ_INDEX.md) — الوسمُ الذي يفصل المبنيّات عن الاسم والفعل (ADR ٥٣)،
بتسجيلٍ مسبق
`docs/mughlaq/PREREG.md` (أُودعت الأداةُ معه قبل أيّ قياسٍ على QAC).

نظامان يُقاسان على المودَع نفسِه بالقاعدة نفسِها للوسم (مغلقٌ إن قُرئ بنواةٍ ليست ظرفًا):

* `S0` — **قبل الإغلاق**: الموزِّع كما كان قبل ADR ٥٣ (`before`، منسوخًا هنا بعينه ليُقاس عليه):
الجدولُ بالفعلين،
  والمتّصلةُ السبعُ حواملُ، وكلُّ مبنيٍّ يحمل اللاحقة، والتعديلاتُ الخمسة الأولى وحدَها. شاهدُ
  أمانة النسخ: يعيد أرقامَ
  `TAWZI_INDEX.md` السابقة بعينها (854؛ 13,151 / 655 / 507 — `tests/test_mughlaq_index.py`).
* `S1` — **بعد الإغلاق**: `slge.mughlaq.qism`.

القياسُ بترتيب قانون القارئ: (١) على مودَع شهادات المصحف كاملًا (الصورُ والمواقعُ بوسمها)؛ (٢) على
**QAC 0.4**
(`qac-pos.tsv.gz`، مرجعٌ بشريٌّ محجوب لقسم الجذع: مفتوحٌ ‎N PN ADJ IMPN V‎، ظرفٌ ‎T LOC‎، وما
سواهما مغلق) — الدقّةُ
والاستدعاءُ بفاصل Wilson وحكمُ التسجيل؛ (٣) على MASAQ مقاييسَ الموزِّع (قسمةُ المرجع/غيرُها/لا
يُقرأ) — **مفحوصٌ لا مقيس**،
لأنّ قواعدَ الإغلاق صُمّمت بعد رؤية ما لا يُقرأ عليه (PREREG §٥).
"""

from __future__ import annotations

import gzip
import json
import math
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from slge.jidh import OBJECT_SUFFIXES, PROCLITICS
from slge.mughlaq import ZARF_CELLS, qism
from slge.pipeline import GOLD_JIHA
from slge.rawabit import PARTICLES, cells_of
from slge.tawzi import TABLE, alif_to_ya, junction, tawzi

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "MUGHLAQ_INDEX.md"
DATA = ROOT / "tests" / "data"
Word = tuple[tuple[str, str], ...]
MARKS = {"فتح": "َ", "كسر": "ِ", "ضم": "ُ", "سكون": "ْ"}
OPEN = frozenset({"N", "PN", "ADJ", "IMPN", "V"})
ZARF = frozenset({"T", "LOC"})
PRE_IN_STEM = ("IMPERF_PREF", "CV_PREF", "IV1S", "IV1P", "IV2MP", "IV3MS", "IV3MP", "IV3FS")

# — S0: الموزِّع قبل ADR ٥٣ بعينه —
_NEW_RAWABIT = sum(1 for k, n, _ in TABLE if k == "حرف" and any(p.name == n for p in PARTICLES))
_OLD_CORES: dict[Word, tuple[str, str]] = {}
for _k, _n, _w in (*(("حرف", p.name, cells_of(p.name)) for p in PARTICLES if not p.proclitic),
                   *TABLE[_NEW_RAWABIT:]):
    _OLD_CORES.setdefault(_w, (_k, _n))  # الجدولُ القديم: أدواتُ الربط بفعليها في مواضعهما ثمّ الباقي
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


def measure() -> dict[str, Any]:
    forms, stream = certificates()
    q0 = [qism0(w) for w in forms]
    q1 = [qism(w) for w in forms]
    deposit: dict[str, Any] = {
        name: {"forms": dict(Counter(q)),
               "positions": dict(Counter(q[i] for i in stream if i >= 0))}
        for name, q in (("S0", q0), ("S1", q1))}
    deposit["changed_forms"] = sum(a != b for a, b in zip(q0, q1, strict=True))
    rows = qac_rows()
    refused = sum(1 for t, _, _ in rows if stream[t] < 0)
    kept = [(stream[t], segs, gold_class(stem)) for t, segs, stem in rows if stream[t] >= 0]
    qac = {name: confusion([(g, q[i]) for i, _, g in kept]) for name, q in (("S0", q0), ("S1", q1))}
    fn: Counter[tuple[str, str]] = Counter()
    fp: Counter[tuple[str, str]] = Counter()
    for i, segs, g in kept:
        if g == "مغلق" and q1[i] != "مغلق":
            fn[(vowelled(forms[i]), segs)] += 1
        if g == "مفتوح" and q1[i] == "مغلق":
            fp[(vowelled(forms[i]), segs)] += 1
    mrows = masaq_rows()
    m0 = tawzi_split(mrows, lambda w: [(pre, suf) for pre, _, suf, _ in before(w)])
    m1 = tawzi_split(mrows, lambda w: [(m.pre, m.suf) for m in tawzi(w)])
    return {"prereg": "docs/mughlaq/PREREG.md", "reference": "QAC 0.4 (Dukes) — قسمُ الجذع",
            "deposit": deposit,
            "qac": {"rows": len(rows), "refused_by_gate": refused, "measured": len(kept), **qac,
                    "verdict": verdict(qac["S0"], qac["S1"]),
                    "fn_top": [[w, s, n] for (w, s), n in fn.most_common(15)],
                    "fp_top": [[w, s, n] for (w, s), n in fp.most_common(15)]},
            "masaq_checked_not_measured": {"S0": m0, "S1": m1, "adr52_rule": adr52_rule(m0, m1)}}


def _pct(r: dict[str, Any]) -> str:
    lo, hi = r["wilson95"]
    return f"{100 * (r['p'] or 0):.2f}٪ [{100 * lo:.2f}، {100 * hi:.2f}] (n = {r['n']:,})"


def render(m: dict[str, Any] | None = None) -> str:
    m = m or measure()
    d, q, ms = m["deposit"], m["qac"], m["masaq_checked_not_measured"]

    def qs(c: dict[str, int]) -> str:
        return "، ".join(f"{k} {c.get(k, 0):,}" for k in ("مغلق", "ظرف", "مفتوح"))

    lines = [
        "# فهرسُ الصنف المغلق — وسمٌ يفصل المبنيّات عن الاسم والفعل",
        "",
        "مولَّدٌ بـ`python tools/gen_mughlaq_index.py` من `src/slge/mughlaq.py` "
        "و`src/slge/tawzi.py`؛ لا يُحرَّر باليد. "
        "البرهانُ `formal/Slge/Mughlaq.lean` (القسمةُ `maftuh_iff`، `mughlaq_iff`؛ إغلاقُ المعنى "
        "`closed_has_src`) و"
        "`formal/Slge/Tawzi.lean` (اللاحقةُ لا يحملها إلّا حاملُها `tawzi_suf_host`؛ شواهدُ "
        "القواعد المسمّاة)؛ "
        "والقياسُ بتسجيلٍ مسبق `docs/mughlaq/PREREG.md`. S0 الموزِّعُ قبل ADR ٥٣، وS1 بعده.",
        "",
        "## على مودَع المصحف أوّلًا (قانونُ القارئ)", "",
        "| النظام | الصور (18,179) | المواقع |", "|---|---|---|",
        *(f"| {k} | {qs(d[k]['forms'])} | {qs(d[k]['positions'])} |" for k in ("S0", "S1")),
        "",
        f"تغيّر وسمُ {d['changed_forms']:,} صورة.",
        "",
        "## على QAC 0.4 (مرجعٌ بشريٌّ محجوب لقسم الجذع)", "",
        f"{q['rows']:,} كلمةً محاذاة؛ ترفض البوّابةُ {q['refused_by_gate']:,}، فالمقيس "
        f"{q['measured']:,} موقعًا. "
        "الذهبيُّ: مفتوحٌ ‎N PN ADJ IMPN V‎، ظرفٌ ‎T LOC‎، وما سواهما مغلق؛ الدقّةُ والاستدعاءُ "
        "على الذهبيّ مغلقًا أو "
        "مفتوحًا، والظرفُ يُعدّ في المصفوفة وحدَها.",
        "",
        "| النظام | الدقّة | الاستدعاء | المفتوحُ موسومًا مغلقًا |", "|---|---|---|---|",
        *(f"| {k} | {_pct(q[k]['precision'])} | {_pct(q[k]['recall'])} | "
          f"{_pct(q[k]['open_leak'])} |"
          for k in ("S0", "S1")),
        "",
        f"**الحكمُ المسجَّل: `{q['verdict']}`.**",
        "",
        "| الذهبيّ→المتنبَّأ | S0 | S1 |", "|---|---|---|",
        *(f"| {k} | {q['S0']['matrix'].get(k, 0):,} | {q['S1']['matrix'].get(k, 0):,} |"
          for k in sorted(set(q["S0"]["matrix"]) | set(q["S1"]["matrix"]))),
        "",
        "### ما يفوت S1 (مغلقٌ عند المرجع، غيرُ مغلقٍ هنا) — بصوره وقطعه", "",
        "| الصورة | قطعُ QAC | العدد |", "|---|---|---|",
        *(f"| {w} | `{s}` | {n:,} |" for w, s, n in q["fn_top"]),
        "",
        "### ما يزيد S1 (مفتوحٌ عند المرجع، مغلقٌ هنا)", "",
        "| الصورة | قطعُ QAC | العدد |", "|---|---|---|",
        *(f"| {w} | `{s}` | {n:,} |" for w, s, n in q["fp_top"]),
        "",
        "## على MASAQ — مفحوصٌ لا مقيس", "",
        "قواعدُ الإغلاق صُمّمت بعد رؤية ما لا يقرؤه الموزِّعُ على MASAQ (PREREG §٥)، فهذه الأرقامُ "
        "فحصٌ لا قياس. على "
        "الكلمات التي لا جهةَ لها عند المرجع:",
        "",
        "| النظام | بقسمة المرجع | بغيرها | لا يُقرأ | المفتوحُ يقرؤه الموزِّع (ADR ٥٢) |",
        "|---|---|---|---|---|",
        *(f"| {k} | {ms[k]['gold']:,} | {ms[k]['wrong']:,} | {ms[k]['none']:,} | "
          f"{ms[k]['open_read']:,} من {ms[k]['open_population']:,} |" for k in ("S0", "S1")),
        "",
        f"وقاعدةُ القرار المسجَّلة في ADR ٥٢ على النظام كلّه (لا على قواعده الخمس وحدَها): "
        f"`{ms['adr52_rule']}`.",
        "",
        "## ما ليس هنا — باسمه", "",
        "- `HUKM_INPUT_CHANGED_BY_CLOSURE`: المغلقُ لا جذرَ يُحكم عليه (`Qiraa.mughlaq_no_hukm`)، "
        "فتغيّر مدخلُ الحكم "
        "على الصور التي تغيّر وسمُها؛ فقياسُ ADR ٥٠ على المخصَّص أُعيد بالنظام الجديد، والفرقُ في ADR ٥٣.",
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

