"""المراكبُ الثلاثة (`A116.Marakib`، `gate.marakib`، ADR ٩٩).

التوقّعاتُ مستقلّةٌ عن `gate.marakib`:
١. مركبُ الجسر حواملُ `gate.bridge.ALPHABET` بعينها، وحواملُ `alghanem-constitution`
   المنقولة في `corpora/marakib/marakib.tsv`.
٢. مركبُ الخانات: رقمُ كلّ خانةٍ من جدول Lean المولَّد `formal/a116/order.csv`
   (رقمُ الجسر، حاملُ Cells، الحالة) ‎4·الحامل + الحالة‎؛ وحروفُه الثمانيةُ والعشرون
   `letters28` في `Field112.lean` وحروفُ hamil المنقولة.
٣. مركبُ المخارج: رقمُ كلّ خانةٍ عمودُ `k` في جدول Lean المولَّد `formal/a116/huruf.csv`.
٤. على كلماتٍ من المصحف عبر `gate.enter`: الإحداثيُّ الأوّل من عدد الشهادة عددُ الجسر،
   والترجمةُ تذهب وتعود.
الطفرات: `MUTANT_SWAP_IGNORED`، `MUTANT_MAKHARIJ_REVERSED`، `MUTANT_WAHDA_UNTAGGED`.
"""

from __future__ import annotations

import csv
import re

from conftest import ROOT

from gate import Refusal, enter
from gate import marakib as M
from gate.bridge import ALPHABET
from gate.contextual import unpair

A = ROOT / "formal" / "a116"
HARAKA = {"fatha": "َ", "damma": "ُ", "kasra": "ِ", "sukun": "ْ"}
LEAN_NAMES = ("tabadil", "cellAt_index", "index_cellAt", "index_injective", "index_jisr",
              "naql_id", "naql_comp", "naql_inv", "naql_khana", "F_jisr", "F_injective",
              "F_surjective", "tarjim_spec", "tarjim_id", "tarjim_comp", "wahda_injective",
              "khalt_shahid", "makharij_order", "hamil_khanat", "kataba")


def deposit() -> dict[str, str]:
    path = ROOT / "corpora" / "marakib" / "marakib.tsv"
    rows = path.read_text(encoding="utf-8").splitlines()[1:]
    return {r.split("\t")[0]: r.split("\t")[5] for r in rows}


def lean_letters28() -> str:
    src = (A / "A116" / "Field112.lean").read_text(encoding="utf-8")
    m = re.search(r'def letters28 : List Char := "([^"]+)"', src)
    assert m is not None
    return m.group(1)


def khanat_expected(carriers: tuple[str, ...] | None = None) -> dict[str, int]:
    """من `order.csv`: رقمُ الجسر ← حاملُ Cells والحالة؛ والخانةُ حرفًا من `ALPHABET`."""
    out = {}
    for b, c, h in csv.reader((A / "order.csv").read_text(encoding="utf-8").splitlines()):
        atom = ALPHABET[int(b) // 4] + list(HARAKA.values())[int(b) % 4]
        out[atom] = 4 * int(c) + int(h)
    return out


def makharij_expected() -> dict[str, int]:
    rows = list(csv.DictReader((A / "huruf.csv").read_text(encoding="utf-8").splitlines()))
    return {r["harf"] + HARAKA[r["haraka"]]: int(r["k"]) for r in rows}


def words() -> list[tuple[str, ...]]:
    text = (ROOT / "corpora" / "quran-simple-enhanced.txt").read_text(encoding="utf-8").splitlines()
    out = []
    for line in text[:200]:
        for w in line.split("|")[-1].split():
            c = enter(w.encode())
            if not isinstance(c, Refusal):
                out.append((c.atoms, c.integer))
    return out


def test_jisr_is_gate_and_constitution() -> None:
    assert M.CARRIERS["jisr"] == tuple(ALPHABET)
    assert "".join(ALPHABET) == deposit()["jisr"]


def test_khanat_from_lean_table_and_hamil() -> None:
    exp = khanat_expected()
    assert len(exp) == 116 and all(M.index("khanat", a) == k for a, k in exp.items())
    assert "".join(M.CARRIERS["khanat"][:28]) == lean_letters28() == deposit()["khanat"]


def test_makharij_from_lean_table() -> None:
    exp = makharij_expected()
    assert len(exp) == 116 and all(M.index("makharij", a) == k for a, k in exp.items())


def test_gate_certificates_and_tarjim() -> None:
    ws = words()
    assert len(ws) > 500
    for atoms, n in ws:
        f = unpair(n)[0]
        assert f == M.number("jisr", atoms)
        for dst in M.MARAKIB:
            t = M.tarjim(f, "jisr", dst)
            assert M.atoms_of(dst, t) == atoms and M.tarjim(t, dst, "jisr") == f
            assert M.wahda_of(M.wahda(dst, atoms)) == (dst, atoms)


def test_khalt_and_lean_names() -> None:
    assert M.number("khanat", ["اَ"]) == M.number("jisr", ["ءَ"])  # khalt_shahid
    assert M.wahda("khanat", ["اَ"]) != M.wahda("jisr", ["ءَ"])
    kataba = [M.index(m, a) for m in M.MARAKIB for a in ("كَ", "تَ", "بَ")]
    assert kataba == [84, 8, 4, 84, 8, 4, 32, 72, 104]
    src = (A / "A116" / "Marakib.lean").read_text(encoding="utf-8")
    assert all(f"theorem {n}" in src for n in LEAN_NAMES)


def test_mutants_rejected() -> None:
    exp = khanat_expected()
    jisr = M.CARRIERS["jisr"]
    # MUTANT_SWAP_IGNORED: مركبُ الخانات بحوامل الجسر
    assert not all(4 * jisr.index(a[0]) + M.HARAKAT.index(a[1]) == k for a, k in exp.items())
    # MUTANT_MAKHARIJ_REVERSED
    rev = tuple(reversed(M.CARRIERS["makharij"]))
    mk = makharij_expected().items()
    assert not all(4 * rev.index(a[0]) + M.HARAKAT.index(a[1]) == k for a, k in mk)
    # MUTANT_WAHDA_UNTAGGED: الوحدةُ بلا مركبها تخلط «اَ» بـ«ءَ»
    assert M.number("khanat", ["اَ"]) == M.number("jisr", ["ءَ"])
