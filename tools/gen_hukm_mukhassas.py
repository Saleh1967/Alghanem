"""قياسُ حكم القابليّة في SLGE على «المخصَّص» مرجعًا آليًّا، بالتسجيل المسبق
`docs/hukm/PREREG-mukhassas.md`.

لكلّ صورةٍ من `corpus-certificates.json.gz` يُستخرج كلُّ زوجٍ (جذر، عقدة) حكم عليه
`slge.hukm.hukm_of_form` بالقابليّة «مفهومًا». ثمّ يُقابَل عنوانُ العقدة بعناوين المرجع بالتطبيع N،
ويُقابَل الجذرُ بجذور المرجع، ويُحكم بالصدق بعضويّة المتن. يكتب `docs/hukm/mukhassas-result.json`،
وبـ`--check` يعيد الحساب ويقارن. لا يُحرَّر الناتجُ باليد.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from slge.cells import ALPHABET, Cell
from slge.hukm import hukm_of_form
from slge.maqayis import decode
from slge.mukhassas import title_of

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "tests" / "data"
OUT = ROOT / "docs" / "hukm" / "mukhassas-result.json"
NODES = DATA / "mukhassas-ref-nodes.tsv"
MEMBERSHIP = DATA / "mukhassas-ref-membership.tsv"
NODES_SHA = "0cfd449b23c933e716add5d923bff914ffd94714f83daaa4fcd86d043736d718"
MEMBERSHIP_SHA = "96c22bbea3cc13421e613a2334f43249fbe62c5d69ba3851ab55ebcfee8179db"
WEAK = 29
Word = tuple[Cell, ...]

DROP = re.compile(r"[ً-ْٰـ0-9٠-٩«»()\[\]{}.,:;،؛؟!\"'\-–—*]")
FOLD = {"أ": "ا", "إ": "ا", "آ": "ا", "ى": "ي"}


def norm(t: str) -> str:
    """التطبيعُ N (التسجيل §٣.١)."""

    t = "".join(FOLD.get(c, c) for c in DROP.sub("", t))
    return " ".join(t.split())


def _read(path: Path, sha: str) -> str:
    raw = path.read_bytes()
    got = hashlib.sha256(raw).hexdigest()
    if got != sha:
        raise SystemExit(f"REFERENCE_SHA_MISMATCH:{path.name}:{got}")
    return raw.decode("utf-8")


def reference() -> tuple[dict[str, list[int]], dict[str, set[int]], int]:
    """(العنوانُ مطبَّعًا ← عُقَدُ المرجع، الجذرُ ← عُقَدُه، عددُ العُقَد)."""

    by_title: dict[str, list[int]] = {}
    lines = _read(NODES, NODES_SHA).splitlines()[1:]
    for ln in lines:
        nid, _, _, _, title = ln.split("\t")
        by_title.setdefault(norm(title), []).append(int(nid))
    members: dict[str, set[int]] = {}
    for ln in _read(MEMBERSHIP, MEMBERSHIP_SHA).splitlines():
        root, ids = ln.split("\t")
        members[root] = {int(x) for x in ids.split()}
    return by_title, members, len(lines)


def root_matches(code: int, rho: str) -> bool:
    """مقابلةُ الجذر (التسجيل §٣.٣): الموضعُ المعتلّ يطابق «و» أو «ي»."""

    if len(rho) != 3:
        return False
    return all((rho[k] in "وي") if i == WEAK else ALPHABET[i] == rho[k]
               for k, i in enumerate(decode(code)))


def nodes_of(code: int, members: dict[str, set[int]]) -> set[int]:
    out: set[int] = set()
    for rho, ids in members.items():
        if root_matches(code, rho):
            out |= ids
    return out


def wilson(k: int, n: int, z: float = 1.959963984540054) -> tuple[float, float]:
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (c - h, c + h)


def chance(n: int, k: int, m: int) -> float:
    """‎1 − C(N−k, m)/C(N, m)‎: أن تقع m عقدةً عشوائيّةً مميَّزة على إحدى عُقَد الجذر الـk."""

    if k == 0:
        return 0.0
    return 1 - math.comb(n - k, m) / math.comb(n, m)


def _forms() -> tuple[list[Word], Counter[int]]:
    with gzip.open(DATA / "corpus-certificates.json.gz", "rt", encoding="utf-8") as f:
        d: dict[str, Any] = json.load(f)
    forms = [tuple((a, b) for a, b in x["cells"]) for x in d["forms"]]
    return forms, Counter(i for i in d["stream"] if i >= 0)


def measure() -> dict[str, Any]:
    forms, freq = _forms()
    pairs: Counter[tuple[int, int]] = Counter()
    for i, w in enumerate(forms):
        h = hukm_of_form(w)
        if h is None:
            continue
        for r, _, q in h:
            if q.witness is not None:
                pairs[(r, q.witness)] += freq[i]
    by_title, members, n_nodes = reference()
    cache: dict[int, set[int]] = {}
    matched = true = unmatched = 0
    tok_matched = tok_true = 0
    base: list[float] = []
    witness_nodes = {nd for _, nd in pairs}
    ambiguous = {nd for nd in witness_nodes if len(by_title.get(norm(title_of(nd)), [])) > 1}
    unmatched_nodes = {nd for nd in witness_nodes if not by_title.get(norm(title_of(nd)))}
    for (r, nd), tok in sorted(pairs.items()):
        m = by_title.get(norm(title_of(nd)), [])
        if not m:
            unmatched += 1
            continue
        if r not in cache:
            cache[r] = nodes_of(r, members)
        ok = bool(cache[r] & set(m))
        matched += 1
        true += ok
        tok_matched += tok
        tok_true += tok * ok
        base.append(chance(n_nodes, len(cache[r]), len(m)))
    lo, hi = wilson(true, matched)
    rate = true / matched if matched else 0.0
    mean_base = sum(base) / len(base) if base else 0.0
    return {
        "prereg": "docs/hukm/PREREG-mukhassas.md",
        "reference": {"nodes_sha256": NODES_SHA, "membership_sha256": MEMBERSHIP_SHA,
                      "nodes": n_nodes, "alghanem": "556d95c"},
        "jins": "JINS_NOT_JUDGED_UNSIGNED",
        "pairs": {"all": len(pairs), "matched": matched, "node_unmatched": unmatched,
                  "true": true, "rate": round(true / matched, 4) if matched else None,
                  "wilson95": [round(lo, 4), round(hi, 4)]},
        "positions": {"matched": tok_matched, "true": tok_true,
                      "rate": round(tok_true / tok_matched, 4) if tok_matched else None},
        "baseline": {"mean_chance": round(mean_base, 4),
                     "lift_points": round(100 * (rate - mean_base), 2)},
        "witness_nodes": {"distinct": len(witness_nodes),
                          "matched": len(witness_nodes) - len(unmatched_nodes),
                          "ambiguous": len(ambiguous)},
    }


def render(m: dict[str, Any]) -> str:
    return json.dumps(m, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def main(argv: list[str]) -> int:
    text = render(measure())
    if "--check" in argv:
        ok = OUT.exists() and OUT.read_text(encoding="utf-8") == text
        sys.stdout.write("نتيجةُ قياس القابليّة على المخصَّص مطابقة\n" if ok
                         else "نتيجةُ قياس القابليّة على المخصَّص غيرُ مطابقة\n")
        return 0 if ok else 1
    OUT.write_text(text, encoding="utf-8")
    sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
