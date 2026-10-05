"""الإملاء: ذهابٌ وإيابٌ استقصاءً، وقوانينُ الابتداء والوصل والوقف."""

from __future__ import annotations

import pytest

from conftest import licensed_words
from slge.cells import SUKUN, licensed, rho_admits
from slge.orthography import begin, join, pause, to_atoms, to_rasm


def test_roundtrip_exhaustive_upto_2() -> None:
    for n in (1, 2):
        for w in licensed_words(n):
            assert tuple(to_atoms(to_rasm(w))) == w, (w, to_rasm(w))


@pytest.mark.slow
def test_roundtrip_exhaustive_3() -> None:
    bad = [w for w in licensed_words(3) if tuple(to_atoms(to_rasm(w))) != w]
    assert bad == []


def test_regressions_from_the_original() -> None:
    fi = [("ف", "كسر"), ("ي", SUKUN)]
    assert to_rasm(fi) == "فِي" and to_atoms("فِي") == fi
    assert to_atoms(to_rasm([("ب", "فتح"), ("ء", SUKUN)])) == [("ب", "فتح"), ("ء", SUKUN)]
    assert to_rasm([("م", "كسر"), ("ن", SUKUN), ("ب", "فتح")]).startswith("مِنْ")


def test_begin_respects_rho() -> None:
    for n in (1, 2):
        for tail in licensed_words(n):
            if not all(rho_admits(c) for c in tail):
                continue
            out = begin([("ا", SUKUN), *tail])
            assert all(rho_admits(c) for c in out)
            assert out[0][1] != SUKUN


def test_join_bismillah() -> None:
    bismi = to_atoms("بِسْمِ")
    joined, ok = join(bismi, to_atoms("ٱللَّهِ"))
    assert ok and licensed([*bismi, *joined]) and joined[0] == ("ل", SUKUN)


def test_pause_tanwin() -> None:
    kitaban = to_atoms("كِتَابًا")
    assert pause(kitaban)[-1] == ("ب", SUKUN)
    assert pause([]) == []
