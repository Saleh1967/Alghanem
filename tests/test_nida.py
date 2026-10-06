"""النداء: الأدوات، قانونُ المنادى على الخانة، الندبةُ خارج الثنائيّ، والقياسُ على MASAQ."""

from __future__ import annotations

import pytest

from slge.cells import STATES, licensed
from slge.nida import PARTICLES, YA, has_tanwin, hukm, is_bina, nudba, ya_junction

_A, _I, _U, SUKUN = STATES
ADAM = (("ء", _A), ("ا", SUKUN), ("د", _A), ("م", _U))
QAWM = (("ق", _A), ("و", SUKUN), ("م", _I))
MASHAR = (("م", _A), ("ع", SUKUN), ("ش", _A), ("ر", _A))
RAJULAN = (("ر", _A), ("ج", _U), ("ل", _A), ("ن", SUKUN))
MUSA = (("م", _U), ("و", SUKUN), ("س", _A), ("ا", SUKUN))


def test_hukm_reads_the_last_cell() -> None:
    assert hukm(ADAM) == "مبني على الضم" and is_bina(hukm(ADAM))
    assert hukm(QAWM) == "مضاف إلى ياء محذوفة"
    assert hukm(MASHAR) == "معرب منصوب"
    assert hukm(RAJULAN) == "نكرة غير مقصودة (منصوب)" and has_tanwin(RAJULAN)
    assert hukm(MUSA) == "لا تقرؤه الخانة"
    muhammadun = (("م", _U), ("ح", _A), ("م", SUKUN), ("م", _A), ("د", _U), ("و", SUKUN), ("ن", _A))
    assert hukm(muhammadun) == "مبني على الواو"
    assert hukm((("ز", _A), ("ي", SUKUN), ("د", _A), ("ا", SUKUN), ("ن", _I))) == "مبني على الألف"


def test_tanwin_never_bina_mutation() -> None:
    for stem in (ADAM, MASHAR):
        assert not is_bina(hukm((*stem[:-1], (stem[-1][0], _A), ("ن", SUKUN))))
    damm_tanwin = (*ADAM, ("ن", SUKUN))  # آدمٌ: تنوينٌ بعد ضمّ — ليس منادًى مبنيًّا
    assert not is_bina(hukm(damm_tanwin))


def test_particles_and_junction() -> None:
    assert len(PARTICLES) == 6 and all(licensed(p.cells) for p in PARTICLES)
    assert len({p.cells for p in PARTICLES}) == 6
    assert ya_junction(ADAM) == (*YA, *ADAM) and licensed(ya_junction(ADAM))
    with pytest.raises(ValueError):
        ya_junction((("ب", SUKUN),))


def test_nudba_is_outside_binary_licence() -> None:
    assert not licensed(nudba((("ح", _A), ("س", SUKUN), ("ر", _A), ("ت", _A))))
    assert not licensed(nudba(ADAM))


def test_masaq_measurement_and_index() -> None:
    import importlib.util
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parent.parent
    tool = root / "tools" / "gen_nida_index.py"
    spec = importlib.util.spec_from_file_location("gen_nida_index", tool)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["gen_nida_index"] = mod
    spec.loader.exec_module(mod)
    table, total = mod.measure()
    assert total == 489
    damm = {m for (r, m, _) in table if r == "مبني على الضم"}
    assert damm == {"مبني"}  # الضمُّ ⇒ مبنيّ بلا استثناء
    assert sum(v for (r, _, _), v in table.items() if r == "مبني على الضم") == 188
    assert mod.render() == (root / "NIDA_INDEX.md").read_text(encoding="utf-8")
