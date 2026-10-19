"""قراءةُ المدلول من الكلمة (ADR ١٠٥، `A116/QiraaMadlul.lean`).

* صفوفُ المعجم الشاهد في Lean من مودَعاتٍ مختومة: هياكلُ ابن فارس، وأجناسُ المخصَّص.
* المراسي أسطرٌ بأعيانها في شرح ابن عقيل المختوم.
* القوالبُ صفوفُ جدول الأوزان المودَع بأعيانها.
* ومرآةُ بايثون لقارئ الماضي: قوالبُ الماضي الستّة وحدَها، مشتقّةً من صفوف `wazn.csv`،
  بلا اسم فاعلٍ ولا مفعولٍ ولا جنس. تُقارَن بـ`gate.recover` على صور المصحف المتمايزة،
  كلُّ صورةٍ معزولةٌ بلا سياق، وعلى جذور ابن فارس كلِّها. هذا فحصٌ للمرآة لا لـLean.
"""

from __future__ import annotations

import gzip
import re
from pathlib import Path

import gate
from gate import Refusal

ROOT = Path(__file__).resolve().parents[1]
LEAN = (ROOT / "formal/a116/A116/QiraaMadlul.lean").read_text(encoding="utf-8")
F, D, K, S = "َ", "ُ", "ِ", "ْ"

# صفوفُ `wazn.csv` التي يأخذها Lean، بأجسامها كما يتوقّعها هذا الاختبار (باليد)، ونوعُ كلٍّ منها.
WAZN_ROWS = {"0": "1َ 2َ 3َ", "1": "1َ 2ِ 3َ", "2": "1َ 2ُ 3َ", "4": "1َ اْ 2َ 3َ",
             "11": "1ُ 2ِ 3َ", "13": "1ُ وْ 2ِ 3َ"}
NAW = {"0": "filMaloom", "1": "filMaloom", "2": "filMaloom", "4": "filMaloom",
       "11": "filMajhul", "13": "filMajhul"}
# قوالبُ المرآة مشتقّةٌ من الصفوف نفسها، فلا تفترق عنها.
QAWALIB = [(NAW[i], body.split()) for i, body in WAZN_ROWS.items()]


def skeletons() -> dict[str, set[str]]:
    out: dict[str, set[str]] = {}
    path = ROOT / "corpora/hadith/maqayis-skeletons.tsv"
    for ln in path.read_text(encoding="utf-8").splitlines():
        sk, root = ln.split("\t")
        out.setdefault(sk, set()).add(root)
    return out


def lean_pairs(field: str) -> list[tuple[str, str]]:
    m = re.search(field + r" := \[(.*?)\]\n", LEAN, re.S)
    assert m, field
    rows = re.findall(r'\("([^"]+)", \[?"([^"\]]+)"\]?\)', m.group(1))
    assert len(rows) == m.group(1).count("("), (field, "ROW_NOT_PARSED")
    return rows


def read(atoms: tuple[str, ...], roots: set[str], free_last: bool = False) -> set[tuple[str, str]]:
    out = set()
    for naw, t in QAWALIB:
        if len(t) != len(atoms):
            continue
        r: dict[str, str] = {}
        ok = True
        for i, (p, a) in enumerate(zip(t, atoms)):
            last = i == len(t) - 1
            if p[0] in "123":
                if a[1:] != p[1:] and not (free_last and last):
                    ok = False
                    break
                r[p[0]] = a[0]
            elif a != p:
                ok = False
                break
        if ok and r["1"] + r["2"] + r["3"] in roots:
            out.add((r["1"] + r["2"] + r["3"], naw))
    return out


def test_deposit_rows() -> None:
    sk = skeletons()
    roots = set().union(*sk.values())
    hayakil = lean_pairs("hayakil")
    assert len(hayakil) == 4
    for key, root in hayakil:
        assert sk.get(key) == {root}, (key, sk.get(key))
    ajnas = (ROOT / "corpora/mukhassas/ajnas.tsv").read_text(encoding="utf-8").splitlines()
    genera = {ln.split("\t")[0] for ln in ajnas[1:]}
    for root, g in lean_pairs("ajnas"):
        assert g in genera, g
        bare = g.removeprefix("ال").replace("إ", "ء")
        assert root in sk.get(bare, set()) | sk.get("ال" + bare, set()), (g, root)
    judhur = re.search(r"judhur := \[(.*?)\]", LEAN).group(1)  # type: ignore[union-attr]
    for r in re.findall(r'"([^"]+)"', judhur):
        assert r in roots, r
    # جدولُ المصدر: جذورُه من المقاييس، ومصادرُه من مصادر `Khawass`.
    khawass = (ROOT / "formal/a116/A116/Khawass.lean").read_text(encoding="utf-8")
    masadir = re.search(r"inductive Masdar \| (.*)\n", khawass).group(1).split(" | ")  # type: ignore[union-attr]
    rows = re.findall(r'\| "([^"]+)" => some \.(\w+)', LEAN)
    assert len(rows) == 3
    for r, m in rows:
        assert r in roots and m in masadir, (r, m)


def test_anchors() -> None:
    lines = gzip.decompress((ROOT / "corpora/ibn-aqil/sharh-alfiyya.txt.gz").read_bytes()).decode(
        "utf-8").splitlines()
    assert "الماضي وهو مبني على الفتح" in lines[368 - 1]
    assert "فأول الفعل اضممن" in lines[3329 - 1]
    assert "كفاعل صغ اسم فاعل" in lines[5653 - 1]
    assert "زنة مفعول" in lines[5691 - 1]
    for n in ("س368", "س3329", "س5653", "س5691"):
        assert n in LEAN


def test_templates_from_wazn() -> None:
    rows = {ln.split(",")[0]: ln.split(",")[1]
            for ln in (ROOT / "formal/a116/wazn.csv").read_text(encoding="utf-8").splitlines()}
    for i, body in WAZN_ROWS.items():
        assert rows[i] == body, (i, rows[i])
    assert "[0, 1, 2, 4]" in LEAN and "[11, 13]" in LEAN


def gate_vs_reader(free_last: bool = False) -> tuple[int, int, int, int]:
    roots = set().union(*skeletons().values())
    words: set[str] = set()
    for ln in (ROOT / "corpora/quran-simple-enhanced.txt").read_text(encoding="utf-8").splitlines():
        words.update(ln.split())
    covered = missed = contradicted = extra = 0
    for w in sorted(words):
        cert = gate.enter(w.encode("utf-8"))
        if isinstance(cert, Refusal):
            continue
        _, readings = gate.recover(cert)
        mine = read(tuple(cert.atoms), roots, free_last)
        g = {(r, "filMaloom" if k == "PAST" else "filMajhul") for r, k, f, p in readings
             if p == "3MS" and (k, f) in {("PAST", "I-a"), ("PAST", "I-i"), ("PAST", "I-u"),
                                          ("PAST", "III"), ("PASSIVE", "I"), ("PASSIVE", "III")}
             and not set(r) & set("ويءا") and r[1] != r[2]}
        if g:
            if g <= mine:
                covered += 1
            else:
                missed += 1
        gate_any = {r for r, k, f, p in readings if k in ("PAST", "PASSIVE")}
        if mine and gate_any and not {r for r, _ in mine} & gate_any:
            contradicted += 1
        if mine and not gate_any:
            extra += 1
    return covered, missed, contradicted, extra


def test_reader_vs_gate() -> None:
    # (يقرؤه الطرفان، يقرؤه gate ويفوت المرآة، بجذرٍ مخالف، تقرؤه المرآةُ فعلًا ولا ماضيَ له في gate)
    base = gate_vs_reader()
    assert base == (128, 0, 0, 11)
    # MUTANT_VERB_LAST_FREE: آخرُ الماضي غيرُ مطابَق فيُقرأ «آدَمُ» وأمثالُه أفعالًا.
    assert gate_vs_reader(free_last=True) != base
