"""أدواتُ الربط: الخاناتُ كما تُخرجها البوّابة، العملُ على الخانة الأخيرة، والفهرسةُ مولَّدة."""

from __future__ import annotations

import pytest

from slge.afal import STEMS, form
from slge.cells import STATES, licensed
from slge.rawabit import BABS, COMPOUND, PARTICLES, Particle, cells_of, govern, tier

BY = {p.name: p for p in PARTICLES}
SUKUN = STATES[3]


def test_cells_follow_the_gate_law() -> None:
    assert cells_of("ثُمَّ") == (("ث", STATES[2]), ("م", SUKUN), ("م", STATES[0]))  # الشدّة خانتان
    assert cells_of("إِذًا") == (("ء", STATES[1]), ("ذ", STATES[0]), ("ن", SUKUN))  # ءِذَنْ
    assert cells_of("مَتَى") == (("م", STATES[0]), ("ت", STATES[0]), ("ا", SUKUN))  # مَتَاْ
    assert cells_of("إِلَى")[0] == ("ء", STATES[1])
    with pytest.raises(ValueError):
        cells_of("ثم")


def test_every_particle_licensed_and_witness_counts() -> None:
    assert len(PARTICLES) == 90 and all(licensed(p.cells) for p in PARTICLES)
    assert sum(p.witness == "شهادة" for p in PARTICLES) == 45
    assert {p.bab for p in PARTICLES} <= set(BABS) and set(COMPOUND) <= set(BABS)


def test_govern_reads_the_last_cell_and_the_five_verbs() -> None:
    yaktub = (("ي", STATES[0]), ("ك", SUKUN), ("ت", STATES[2]), ("ب", SUKUN))
    assert govern("جزم", yaktub) and not govern("نصب", yaktub) and not govern("جرّ", yaktub)
    assert govern("", yaktub)
    s = STEMS[0]
    assert govern("جزم", form(s, "الجماعة", "جزم")) and not govern("جزم", form(s, "الجماعة", "رفع"))
    assert govern("نصب", form(s, "الجماعة", "نصب"))
    assert govern("جرّ", (("ب", STATES[0]), ("ي", SUKUN), ("ت", STATES[1])))
    assert not govern("جزم", ())


def test_tiers_and_mutation() -> None:
    assert tier(BY["لَمْ"]) == "د١٦ العمل" and tier(BY["وَ"]) == "د٨ الحدّ"
    assert tier(BY["قَدْ"]) == "د٤ الخانة"
    assert tier(Particle("قَدْ", 2, "", "شهادة", True)) == "د٨ الحدّ"
    assert all(len(p.cells) == 1 and p.cells[0][1] != SUKUN for p in PARTICLES if p.proclitic)


def test_index_is_current() -> None:
    import importlib.util
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parent.parent
    tool = root / "tools" / "gen_rawabit_index.py"
    spec = importlib.util.spec_from_file_location("gen_rawabit_index", tool)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["gen_rawabit_index"] = mod
    spec.loader.exec_module(mod)
    assert mod.render() == (root / "RAWABIT_INDEX.md").read_text(encoding="utf-8")
