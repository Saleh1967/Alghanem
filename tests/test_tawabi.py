"""التوابع: الحالةُ لا العلامة — قارئٌ موحِّد، وتوافقٌ، وعطفُ النسق والتوكيد، والقياسُ على MASAQ."""

from __future__ import annotations

from slge.cells import STATES, licensed
from slge.khamsa import KHAMSA, form
from slge.rawabit import PARTICLES
from slge.tawabi import NASAQ, TAWKID, case_class, compatible, follows, tawkid

_A, _I, _U, SUKUN = STATES
ALIMU = (("ء", _A), ("ل", SUKUN), ("ع", _A), ("ا", SUKUN), ("ل", _I), ("م", _U))
MUSLIMUNA = (("م", _U), ("س", SUKUN), ("ل", _I), ("م", _U), ("و", SUKUN), ("ن", _A))
RAJULANI = (("ر", _A), ("ج", _U), ("ل", _A), ("ا", SUKUN), ("ن", _I))
RAJULUN = (("ر", _A), ("ج", _U), ("ل", _U), ("ن", SUKUN))
AKHU = (("ء", _A), ("خ", _U), ("و", SUKUN))


def test_four_markers_one_case() -> None:
    for w in (ALIMU, MUSLIMUNA, RAJULANI, RAJULUN, AKHU):
        assert case_class(w) == "رفع", w
    assert follows(ALIMU, AKHU) and follows(RAJULANI, MUSLIMUNA)
    muslimina = (("م", _U), ("س", SUKUN), ("ل", _I), ("م", _I), ("ي", SUKUN), ("ن", _A))
    assert case_class(muslimina) == "نصب/جرّ"
    assert case_class((("ر", _A), ("ج", _U), ("ل", _I))) == "جرّ"


def test_khamsa_raf_read_nasb_unread() -> None:
    ab = KHAMSA[0]
    assert case_class(form(ab, "رفع")) == "رفع"
    assert case_class(form(ab, "نصب")).startswith("لا تقرؤه")  # الألفُ مشتركةٌ مع المقصور
    assert case_class((("م", _U), ("و", SUKUN), ("س", _A), ("ا", SUKUN))).startswith("لا تقرؤه")


def test_compatible_is_symmetric_and_reflexive_when_read() -> None:
    kinds = ("رفع", "نصب", "جرّ", "نصب/جرّ", "لا تقرؤه الخانة")
    for a in kinds:
        for b in kinds:
            assert compatible(a, b) == compatible(b, a)
        assert compatible(a, a) == (not a.startswith("لا تقرؤه"))
    assert compatible("نصب/جرّ", "جرّ") and not compatible("رفع", "جرّ")


def test_nasaq_and_tawkid() -> None:
    names = {p.name for p in PARTICLES}
    assert all(n in names for n in NASAQ) and len(NASAQ) == 9
    assert all(licensed(w) for w in TAWKID.values()) and len(TAWKID) == 6
    kulluhum = tawkid("كُلّ", (("ه", _U), ("م", SUKUN)))
    assert licensed(kulluhum) and case_class(kulluhum[:3]) == "رفع"


def test_masaq_measurement_and_index() -> None:
    import importlib.util
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parent.parent
    tool = root / "tools" / "gen_tawabi_index.py"
    spec = importlib.util.spec_from_file_location("gen_tawabi_index", tool)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["gen_tawabi_index"] = mod
    spec.loader.exec_module(mod)
    table, _, total = mod.measure()
    assert total == 3179
    assert table[("نعت", "موافق")] == 873 and table[("نعت", "مخالف")] == 206
    assert mod.render() == (root / "TAWABI_INDEX.md").read_text(encoding="utf-8")
