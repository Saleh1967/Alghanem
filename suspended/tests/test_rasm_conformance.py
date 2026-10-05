"""معلَّق: `to_rasm`/`to_atoms` بايثونًا مقابل `Slge.Rasm` في Lean.

نُقل من `tests/test_conformance.py` مع تعليق `orthography.py`؛ البرهانُ `Slge.Rasm.*` باقٍ،
والمرآةُ البايثونيّة معلَّقةٌ حتى تعود عبر بوّابة الغانم (`gate.enter`).
"""

from __future__ import annotations

from conftest import licensed_words  # noqa: F401


def test_rasm_matches_lean() -> None:
    """`to_rasm` هو `Rasm.write` رمزًا رمزًا، و`to_atoms` يعيد الخانات، على كلّ سلسلةٍ بطول ‎≤ 2‎."""

    from itertools import product

    from slge.orthography import to_atoms, to_rasm

    vowel = {"َ": 0, "ِ": 1, "ُ": 2, "ْ": 3}
    tanwin = {"ً": 0, "ٍ": 1, "ٌ": 2}
    seat = {"أ": {"َ": "H0", "ُ": "H2", "ً": "HT0", "ٌ": "HT2"}, "إ": {"ِ": "H1", "ٍ": "HT1"}}

    def glyphs(rasm: str) -> list[str]:
        out: list[str] = []
        i = 0
        while i < len(rasm):
            ch = rasm[i]
            nxt = rasm[i + 1] if i + 1 < len(rasm) else ""
            if ch == "آ":
                out.append("MADDA")
            elif ch == "ء":
                assert nxt == "ْ"
                out.append("H3")
                i += 1
            elif ch in seat:
                out.append(seat[ch][nxt])
                i += 1
            else:
                out.append(f"L{ALPHABET.index(ch)}")
                if nxt in vowel:
                    out.append(f"M{vowel[nxt]}")
                    i += 1
                elif nxt in tanwin:
                    out.append(f"T{tanwin[nxt]}")
                    i += 1
            i += 1
        return out

    lean = {row[0]: row[1] for row in _rows("rasm.csv")}
    assert len(lean) == 1 + 116 + 116 * 116
    for n in (0, 1, 2):
        for w in product(CELLS, repeat=n):
            key = "-".join(str(index(c)) for c in w)
            rasm = to_rasm(w)
            assert " ".join(glyphs(rasm)) == lean[key], (w, rasm)
            assert tuple(to_atoms(rasm)) == w, (w, rasm)
