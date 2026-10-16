"""ختمُ نصوص النبهانيّ ومودَعُ المعلومات السابقة (ADR ٨٧).

التوقّعاتُ مستقلّةٌ عن Lean وعن `tools/gen_nabhani.py`:
١. البصماتُ والأحجامُ مكتوبةٌ هنا باليد، وتُحسب من الملفّات المضغوطة.
٢. كلُّ اقتباسٍ في `malumat.tsv` و`tarifat.tsv` نصٌّ في سطره بعينه (1-based).
٣. المرتبةُ في كلّ صفٍّ هي قاعدةُ «التفكير» س28 مكتوبةً هنا: الوجودُ قطعيّ؛ والحقيقةُ والصفةُ والخاصّةُ
   والقابليّةُ ظنّيّة؛ وما سواها بلا مرتبة. وسطرُ التمييز ينصّ على أنّه «ليس فكراً».
الطفرات: `MUTANT_LINE_SHIFTED`، `MUTANT_MARTABA_FLIPPED`، `MUTANT_SEAL_FORGED`.
"""

from __future__ import annotations

import gzip
import hashlib
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "corpora" / "nabhani"
SEALS = {
    "tafkir": ("tafkir.txt.gz",
               "f7fcc683237681e8d24dfeb59afb5e9b2e8536822a925eab010e9bed05f5d83c", 339129),
    "j1": ("shakhsiyya_j1.txt.gz",
           "77d80c69c80cdb967152702458956553a79d89d5ca220926e2b1b01cc24525ab", 870941),
    "j3": ("shakhsiyya_j3.txt.gz",
           "dd57e74bec43534ceec90797ad050cb104a16925b6d0bf0304796d42e70c425e", 1242143),
}
SHARH = ("sharh-alfiyya.txt.gz", "661e43ea265eca8c72b9e4ab7a46cd9182b34e834105b595241bc7787b471f09")
QATI = {"wujud"}
ZANNI = {"haqiqa", "sifa", "khassa", "qabiliyya"}


def sealed(seals: dict[str, tuple[str, str, int]]) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for k, (f, sha, n) in seals.items():
        raw = gzip.decompress((DIR / f).read_bytes())
        assert hashlib.sha256(raw).hexdigest() == sha and len(raw) == n, f
        out[k] = raw.decode("utf-8").splitlines()
    raw = gzip.decompress((ROOT / "corpora" / "ibn-aqil" / SHARH[0]).read_bytes())
    assert hashlib.sha256(raw).hexdigest() == SHARH[1]
    out["sharh"] = raw.decode("utf-8").splitlines()
    return out


def tsv(name: str) -> list[dict[str, str]]:
    lines = (DIR / name).read_text(encoding="utf-8").splitlines()
    keys = lines[0].split("\t")
    return [dict(zip(keys, ln.split("\t"), strict=True)) for ln in lines[1:]]


def anchored(rows: list[dict[str, str]], ts: dict[str, list[str]], shift: int = 0) -> bool:
    return all(r["iqtibas"] in ts[r["nass"]][int(r["satr"]) - 1 + shift] for r in rows)


def rule(naw: str) -> str:
    return "qati" if naw in QATI else "zanni" if naw in ZANNI else "-"


def test_seals_by_hand() -> None:
    sealed(SEALS)


def test_quotes_in_sealed_lines() -> None:
    ts = sealed(SEALS)
    assert anchored(tsv("malumat.tsv"), ts) and anchored(tsv("tarifat.tsv"), ts)


def test_martaba_is_the_tafkir_rule() -> None:
    rows = tsv("malumat.tsv")
    assert all(r["martaba"] == rule(r["naw"]) for r in rows)
    assert {rule(r["naw"]) for r in rows} == {"qati", "zanni", "-"}
    tamyiz = [t for t in tsv("tarifat.tsv") if t["ism"] == "tamyiz"][0]
    assert "ليس فكراً" in sealed(SEALS)[tamyiz["nass"]][int(tamyiz["satr"]) - 1]


def test_generator_in_sync() -> None:
    r = subprocess.run([sys.executable, str(ROOT / "tools" / "gen_nabhani.py"), "--check"],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stderr


def test_mutants_rejected() -> None:
    ts = sealed(SEALS)
    assert not anchored(tsv("malumat.tsv"), ts, shift=1)
    flipped = [dict(r, martaba="qati" if r["martaba"] == "zanni" else r["martaba"])
               for r in tsv("malumat.tsv")]
    assert not all(r["martaba"] == rule(r["naw"]) for r in flipped)
    forged = dict(SEALS, tafkir=("tafkir.txt.gz", "0" * 64, 339129))
    try:
        sealed(forged)
    except AssertionError:
        pass
    else:
        raise AssertionError("MUTANT_SEAL_FORGED accepted")
