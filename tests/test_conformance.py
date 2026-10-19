"""مطابقةُ البوّابة بما يطبعه Lean: الترتيبُ والترقيمُ والاقترانُ والقبول.

الجداولُ في `formal/a116/*.csv` يطبعها `lake exe a116-table` ويُعيد CI توليدَها ويقابلها
بالمودَع؛ فالاختبارُ هنا يقابل البايثون بما طبعه Lean لا بقيمٍ مكتوبة.
"""

from __future__ import annotations

from conftest import ROOT

from gate.bridge import A116
from gate.contextual import fold_atoms, pair, unfold_atoms, unpair

LEAN = ROOT / "formal" / "a116"
# ترتيبُ `Cells.lean`: الثمانيةُ والعشرون من «ا» إلى «ي»، ثمّ «ء» في الموضع 28 (م١).
LEAN_CARRIERS = (*"ابتثجحخدذرزسشصضطظعغفقكلمنهوي", "ء")
LEAN_HARAKAT = ("َ", "ُ", "ِ", "ْ")


def _rows(name: str) -> list[list[str]]:
    return [r.split(",") for r in (LEAN / name).read_text(encoding="utf-8").splitlines() if r]


def test_bridge_order_matches_lean() -> None:
    rows = _rows("order.csv")
    assert len(rows) == 116
    for k, carrier, haraka in rows:
        assert A116[int(k)] == LEAN_CARRIERS[int(carrier)] + LEAN_HARAKAT[int(haraka)]


def test_numbering_matches_lean_on_all_strings_upto_2() -> None:
    rows = _rows("numbers.csv")
    assert len(rows) == 1 + 116 + 116 * 116
    for row in rows:
        value = row[-1]
        atoms = tuple(A116[int(i)] for i in row[0].split()) if row[0] else ()
        assert fold_atoms(atoms) == int(value)
        assert unfold_atoms(int(value)) == atoms


def test_cantor_pairing_matches_lean() -> None:
    rows = _rows("pairs.csv")
    assert len(rows) == 64 * 64
    for u, r, z in rows:
        assert pair(int(u), int(r)) == int(z)
        assert unpair(int(z)) == (int(u), int(r))


def test_python_ternary_parse_matches_lean_syllables_table() -> None:
    """`gate.licence.parse/continue/pause/binary_ok` = `Stages.parse`/`Ternary.*B`
    على كلّ سلسلةِ أصنافٍ بطول 1…11 (265,719 سطرًا من `lake exe a116-table syllables`)."""

    from gate.licence import binary_ok, continue_licensed, parse, pause_licensed

    rows = 0
    with (ROOT / "formal" / "a116" / "syllables.csv").open(encoding="utf-8") as fh:
        for line in fh:
            key, shape, b, c, p = line.rstrip("\n").split(",")
            k = [x.lower() for x in key.split("-")]
            got = parse(k)
            if got is None:
                mine = "none"
            else:
                lead, ss = got
                mine = "-".join(([] if lead == "none" else [lead + "|"]) + list(ss))
            assert mine == shape, key
            assert (binary_ok(k), continue_licensed(k), pause_licensed(k)) == (
                b == "true", c == "true", p == "true"
            ), key
            rows += 1
    assert rows == 265719


def test_utf8_codec_matches_lean_on_the_surface_alphabet() -> None:
    """`A116.Unicode.utf8Encode` = ترميزُ بايثون على أبجديّة الرسم (53 نقطة)، وكلُّ العربيّ بايتان."""

    rows = 0
    with (ROOT / "formal" / "a116" / "utf8.csv").open(encoding="utf-8") as fh:
        for line in fh:
            cp, bytes_ = line.rstrip("\n").split(",")
            lean = bytes(int(b) for b in bytes_.split())
            assert lean == chr(int(cp)).encode("utf-8"), cp
            if 0x600 <= int(cp) <= 0x6FF:
                assert len(lean) == 2
            rows += 1
    assert rows == 53
