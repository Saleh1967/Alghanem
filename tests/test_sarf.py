"""الممنوعُ من الصرف: جرُّه نصبُه، شرطا الصرف يردّان الكسرة، عللُ الصيغة تُقرأ، والقياسُ على MASAQ."""

from __future__ import annotations

from slge.cells import STATES, licensed
from slge.marifa import has_al
from slge.nida import has_tanwin
from slge.sarf import (
    al_jarr,
    idafa_jarr,
    illa,
    mamduda,
    mamnu_jarr,
    maqsura,
    on_template,
    sarf_jarr,
    sarf_nasb,
)

_A, _I, _U, SUKUN = STATES
MASAJID = (("م", _A), ("س", _A), ("ا", SUKUN), ("ج", _I), ("د", _A))
MASABIH = (("م", _A), ("ص", _A), ("ا", SUKUN), ("ب", _I), ("ي", SUKUN), ("ح", _A))
SHUFAA = (("ش", _U), ("ف", _A), ("ع", _A), ("ا", SUKUN), ("ء", _A))
KUBRA = (("ك", _U), ("ب", SUKUN), ("ر", _A), ("ا", SUKUN))
ADAM = (("ء", _A), ("ا", SUKUN), ("د", _A), ("م", _A))
IBRAHIM = (("ء", _I), ("ب", SUKUN), ("ر", _A), ("ا", SUKUN), ("ه", _I), ("ي", SUKUN), ("م", _A))


def test_decisive_law_jarr_is_nasb() -> None:
    assert mamnu_jarr(MASAJID) == MASAJID and not has_tanwin(mamnu_jarr(MASAJID))
    assert sarf_jarr(MASAJID) != sarf_nasb(MASAJID)
    assert sarf_jarr(MASAJID)[-2][1] == _I and sarf_nasb(MASAJID)[-2][1] == _A
    assert all(licensed(w) for w in (sarf_jarr(MASAJID), sarf_nasb(MASAJID), mamnu_jarr(MASAJID)))


def test_two_conditions_restore_kasra() -> None:
    w = al_jarr(MASAJID)
    assert has_al(w) and w[-1][1] == _I and licensed(w)
    w2 = idafa_jarr(MASAJID, (("ه", _U), ("م", SUKUN)))
    assert w2[len(MASAJID) - 1][1] == _I and not has_tanwin(w2) and licensed(w2)


def test_illa_readers_on_gate_witnesses() -> None:
    assert illa(MASAJID) == "صيغة منتهى الجموع" and illa(MASABIH) == "صيغة منتهى الجموع"
    assert illa(SHUFAA) == "ألف التأنيث الممدودة" and mamduda(SHUFAA)
    assert illa(KUBRA) == "ألف التأنيث المقصورة" and maqsura(KUBRA)
    assert illa(ADAM) == "وزن أَفْعَل/فَعْلَان (صفةٌ أو علم)"
    assert illa(IBRAHIM) == "معجم"
    assert on_template(101, (*MASAJID[:-1], ("د", _U))) and not on_template(101, IBRAHIM)
    assert not maqsura((("ف", _A), ("ت", _A), ("ا", SUKUN)))  # ثلاثيّ: فَتَى ليس ألفَ تأنيث


def test_masaq_measurement_and_index() -> None:
    import importlib.util
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parent.parent
    tool = root / "tools" / "gen_sarf_index.py"
    spec = importlib.util.spec_from_file_location("gen_sarf_index", tool)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["gen_sarf_index"] = mod
    spec.loader.exec_module(mod)
    table, ilal, _, total = mod.measure()
    assert total == 754
    assert table[("بأل", "كسر")] == 255 and table[("مضاف", "كسر")] == 120
    assert table[("مجرّد", "تنوين كسر")] == 251 and table[("مجرّد", "فتح")] == 44
    assert table[("بأل", "فتح")] == 1 and table[("مضاف", "فتح")] == 0
    assert sum(ilal.values()) == 44 and ilal["صيغة منتهى الجموع"] == 6
    assert mod.render() == (root / "SARF_INDEX.md").read_text(encoding="utf-8")
