"""الصوت (`A116.Sawt`، ADR ٨٤): المراسي في النصوص المختومة، والصوتُ على المصحف كلِّه.

التوقّعاتُ مستقلّةٌ عن Lean وعن البوّابة:
١. كلُّ مرساةٍ في `Sawt.marasi` نصٌّ في سطرها بعينه (العدُّ من 1) من ملفّها في `corpora/kitab/`
   ببصمته في `MANIFEST.tsv`.
٢. صوتُ كلّ شهادةٍ جاهزةٍ من المصحف (صوامتُ وصوائتُ، والحركةُ مع حرف مدّها صائتٌ طويل) يُردّ إلى
   ذرّاتها بأعيانها.
٣. أحكامُ المدّ على المصحف: كلُّ مدٍّ لازمٍ داخلَ كلمةٍ جاهزة ساكنُه أوّلُ مثلين أو هو مدُّ الفرق —
   `lazim_mudgham`؛
   والأقسامُ كلُّها واقعة.
الطفرات: `MUTANT_LINE_SHIFTED`، `MUTANT_FATHA_BAAD_YA` (الفتحةُ بعضُ الياء يكسر الردّ).
"""

from __future__ import annotations

import gzip
import hashlib
import re
from collections import Counter
from functools import cache
from pathlib import Path

import gate
import gate.api as api

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "formal" / "a116" / "A116" / "Sawt.lean"
KITAB = ROOT / "corpora" / "kitab"
SUK = "ْ"
MADD = {"َ": "ا", "ُ": "و", "ِ": "ي"}


def marasi() -> list[tuple[str, int, str]]:
    text = LEAN.read_text(encoding="utf-8")
    return [(f, int(n), q) for f, n, q in re.findall(r'\("([^"]+)", (\d+), "([^"]+)"\)', text)]


@cache
def sealed(name: str) -> list[str]:
    sha = {r.split("\t")[0]: r.split("\t")[3]
           for r in (KITAB / "MANIFEST.tsv").read_text(encoding="utf-8").splitlines()[1:]}
    raw = gzip.decompress((KITAB / f"{name}.gz").read_bytes())
    assert hashlib.sha256(raw).hexdigest() == sha[f"{name}.gz"]
    return raw.decode("utf-8").splitlines()


def anchored(ms: list[tuple[str, int, str]]) -> bool:
    return all(q in sealed(f)[n - 1] for f, n, q in ms)


@cache
def ready() -> list[tuple[str, ...]]:
    out = []
    for f in sorted(api.sealed_forms()):
        r = gate.enter(f.encode())
        if isinstance(r, gate.Certificate):
            out.append(r.atoms)
    return out


def sawt(atoms: tuple[str, ...], madd: dict[str, str]) -> list[tuple[str, str, bool]]:
    out: list[tuple[str, str, bool]] = []
    i = 0
    while i < len(atoms):
        k, h = atoms[i]
        if h != SUK and i + 1 < len(atoms) and atoms[i + 1] == madd.get(h, "") + SUK:
            out.append((k, h, True))
            i += 2
        else:
            out.append((k, h, False))
            i += 1
    return out


def un(segs: list[tuple[str, str, bool]], madd: dict[str, str]) -> tuple[str, ...]:
    out: list[str] = []
    for k, h, tawil in segs:
        out.append(k + h)
        if tawil:
            out.append(madd[h] + SUK)
    return tuple(out)


def test_marasi_in_sealed_texts() -> None:
    ms = marasi()
    assert len(ms) == 8 and anchored(ms)


def test_sawt_radd_on_mushaf() -> None:
    rs = ready()
    assert all(un(sawt(a, MADD), MADD) == a for a in rs)
    assert sum(t for a in rs for _k, _h, t in sawt(a, MADD)) > 10000


def test_lazim_is_mudgham_on_mushaf() -> None:
    c: Counter[str] = Counter()
    for at in ready():
        for i in range(1, len(at)):
            if at[i][1] == SUK and MADD.get(at[i - 1][1]) == at[i][0]:
                nxt = at[i + 1] if i + 1 < len(at) else None
                if nxt is None:
                    c["taraf"] += 1
                elif nxt[0] == "ء":
                    c["muttasil"] += 1
                elif nxt[1] == SUK:
                    gem = i + 2 < len(at) and at[i + 2][0] == nxt[0]
                    farq = i == 1 and at[0] == "ءَ" and nxt[0] == "ل"
                    c["lazim_ok" if gem or farq else "lazim_bad"] += 1
                else:
                    c["tabii"] += 1
    assert c["lazim_bad"] == 0 and all(c[k] > 0 for k in ("taraf", "muttasil", "lazim_ok", "tabii"))


def test_mutants_rejected() -> None:
    assert not anchored([(f, n + 1, q) for f, n, q in marasi()])
    bad = dict(MADD, **{"َ": "ي"})
    assert any(un(sawt(a, MADD), bad) != a for a in ready())
