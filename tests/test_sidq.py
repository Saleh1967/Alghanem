"""الصدقُ عند السيرافيّ وصفوفُ القابليّة الثلاثيّة (`A116.SidqSirafi`، ADR ٨٩).

التوقّعاتُ مستقلّةٌ عن Lean وعن `tools/gen_sidq.py`:
١. بصمةُ شرح السيرافيّ مكتوبةٌ هنا باليد، وكلُّ مرساةٍ في سطرها (1-based)، وكلُّ صفٍّ
   فعلُه ومفعولُه في سطر شاهده أو ما يليه.
٢. مرساةُ المصحف المختوم (س5337) فيها «وَحُمِلَتِ» و«الْجِبَالُ».
٣. التوقيعُ بقاعدةٍ مكتوبةٍ هنا: موقَّعٌ ⟺ `signed_by` غيرُ فارغ وبصمةُ الصفوف كما سُجّلت.
٤. الحكمُ بقاعدةٍ مكتوبةٍ هنا: لا حكمَ في غير الخبر، والمحالُ في الخبر كذب، ثمّ الصفُّ
   الثلاثيّ، وإلّا «لا حكم». شواهدُ السيرافيّ الثلاثة: صفرٌ قبل التوقيع، وثلاثةٌ بالمسوّدة.
الطفرات: `MUTANT_AKHFASH`، `MUTANT_UNARY`، `MUTANT_FORGED_SIGNATURE`، `MUTANT_LINE_SHIFTED`.
"""

from __future__ import annotations

import gzip
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SIRAFI = (ROOT / "corpora" / "kitab"
          / "0368AbuSacidSirafi.SharhKitabSibawayhi.Sham19Y0017726-ara1.gz")
SIRAFI_SHA = "d53137fd4151028c5dee8ab9ff3e42275ecf0c39089e15fbf50bf0eefaa1603a"
DIR = ROOT / "corpora" / "sidq"
SHAWAHID = [("الإنسان", "حمل", "الجبل"), ("الإنسان", "شرب", "ماء البحر"),
            ("الإنسان", "صعد", "السماء")]
SURFACE = {"حمل": "حملت", "شرب": "شربت", "صعد": "صعدت"}


def sirafi() -> list[str]:
    raw = gzip.decompress(SIRAFI.read_bytes())
    assert hashlib.sha256(raw).hexdigest() == SIRAFI_SHA
    return raw.decode("utf-8").splitlines()


def tsv(name: str) -> list[dict[str, str]]:
    lines = (DIR / name).read_text(encoding="utf-8").splitlines()
    keys = lines[0].split("\t")
    return [dict(zip(keys, ln.split("\t"), strict=True)) for ln in lines[1:]]


def is_signed(sign: dict[str, object], rows_bytes: bytes) -> bool:
    sha = hashlib.sha256(rows_bytes).hexdigest()
    return bool(sign.get("signed_by")) and sign.get("rows_sha256") == sha


def rows_tuples() -> list[tuple[str, str, str, bool]]:
    return [(r["fail"], r["fil"], r["mafool"], r["ijab"] == "+") for r in tsv("qabiliyya3.tsv")]


def judge(rows: list[tuple[str, str, str, bool]], khabar: bool, muhal: bool,
          n: tuple[str, str, str] | None, unary: bool = False, akhfash: bool = False) -> str:
    if not khabar:
        return "laHukm"
    if muhal:
        return "laHukm" if akhfash else "kadhib"
    if n is not None:
        for f, v, m, ijab in rows:
            if (unary or f == n[0]) and v == n[1] and m == n[2]:
                return "sadiq" if ijab else "kadhib"
    return "laHukm"


def count(rows: list[tuple[str, str, str, bool]]) -> int:
    return sum(judge(rows, True, False, s) == "kadhib" for s in SHAWAHID)


def test_anchors_and_rows_in_sealed_sirafi() -> None:
    ls = sirafi()
    an = tsv("sirafi-anchors.tsv")
    assert len(an) == 18 and all(r["iqtibas"] in ls[int(r["satr"]) - 1] for r in an)
    for r in tsv("qabiliyya3.tsv"):
        n = int(r["shahid_satr"])
        span = (ls[n - 1] + " " + ls[n]).replace("~~", "")
        assert SURFACE[r["fil"]] in span and r["mafool"].split()[0] in span, r


def test_mushaf_anchor() -> None:
    mushaf = (ROOT / "corpora" / "quran-simple-enhanced.txt").read_text(encoding="utf-8")
    line = mushaf.splitlines()[5336]
    assert "وَحُمِلَتِ" in line and "الْجِبَالُ" in line


def test_signature_rule() -> None:
    sign = json.loads((DIR / "owner-qabiliyya.json").read_text(encoding="utf-8"))
    signed = is_signed(sign, (DIR / "qabiliyya3.tsv").read_bytes())
    src = (ROOT / "formal" / "a116" / "A116" / "SidqData.lean").read_text(encoding="utf-8")
    assert f"def signed : Bool := {'true' if signed else 'false'}" in src


def test_judgement_by_independent_rule() -> None:
    sign = json.loads((DIR / "owner-qabiliyya.json").read_text(encoding="utf-8"))
    signed = is_signed(sign, (DIR / "qabiliyya3.tsv").read_bytes())
    assert count(rows_tuples() if signed else []) == (3 if signed else 0)
    assert count(rows_tuples()) == 3
    assert judge(rows_tuples(), False, True, None) == "laHukm"          # قم أمس
    assert judge(rows_tuples(), True, True, None) == "kadhib"           # أتيتك غدا (س5122)
    # وَحُمِلَتِ الْجِبَالُ
    assert judge(rows_tuples(), True, False, ("", "حمل", "الجبل")) == "laHukm"
    assert judge(rows_tuples(), True, False, ("الإنسان", "لقي", "زيد")) == "laHukm"


def test_mutants_rejected() -> None:
    assert judge(rows_tuples(), True, True, None, akhfash=True) != "kadhib"
    jibal = ("", "حمل", "الجبل")
    assert judge(rows_tuples(), True, False, jibal, unary=True) != "laHukm"
    forged = {"signed_by": "x", "rows_sha256": "0" * 64}
    assert not is_signed(forged, (DIR / "qabiliyya3.tsv").read_bytes())
    ls = sirafi()
    assert not all(r["iqtibas"] in ls[int(r["satr"])] for r in tsv("sirafi-anchors.tsv"))
