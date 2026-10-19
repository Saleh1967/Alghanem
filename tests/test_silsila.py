"""السلسلةُ كلمةً كلمة (ADR ١١٤): مرآةُ `tools/gen_silsila.py` مطابَقةٌ لجدول Lean `silsila.csv`،
وحالاتٌ باليد، وطفرات.

* المطابقة: كلُّ سطرٍ من `lake exe a116-table silsila` (المودَع `formal/a116/silsila.csv`) هو مخرجُ
  المرآة على القرّاء نفسِهم مكتوبين هنا باليد.
* الحالاتُ باليد: السقوطُ يسري، وطبقةٌ بلا قارئ «لا حكم»، وخارجُ المجال غيرُ «لا قارئ».
* الطفرات (`MUTANT_*`): مرآةٌ مُفسَدة تُرقَّع فيسقط شرطُ المطابقة.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[1]
TABLE = ROOT / "formal" / "a116" / "silsila.csv"
_spec = importlib.util.spec_from_file_location("gen_silsila", ROOT / "tools" / "gen_silsila.py")
assert _spec and _spec.loader
S = importlib.util.module_from_spec(_spec)
sys.modules["gen_silsila"] = S
_spec.loader.exec_module(S)

DUNS: list[Any] = [("m", "d"), ("p", ("d", "e")), ("l", "rafd:R"), ("l", "dunaha"), ("l", "laQari"),
             ("l", "kharij")]
QURRA: dict[str, Any] = {
    "none": None,
    "m": lambda _w, _d: ("m", "v"),
    "p": lambda _w, _d: ("p", ("v", "u")),
    "l": lambda _w, _d: ("l", "rafd:Q"),
    "k": lambda _w, _d: ("l", "kharij"),
    "echo": lambda _w, d: d,
    "word": lambda w, _d: ("m", w) if w == "x" else ("l", "rafd:R"),
}
MANQUL = S.manqul()
SHAHID: list[Any] = [
    lambda w, _d: ("m", w) if w == "كَتَبَ" else ("l", "rafd:REJECT"),
    lambda _w, _d: ("p", ("فعل", "اسم")),
    None,
]


DUN_BY_RAMZ = {S.ramz(d): d for d in DUNS}
"""مفتاحُ الأحكام بالمرآة السليمة، فطفرةُ `ramz` تُقتل بالمخرج لا بانهيار المفتاح."""


# المعجمُ الشاهد في `SilsilaQurra` (`hyMithal`، `ajMithal`، `wadMithal`) والكلماتُ ذرّاتٍ، مكتوبةً باليد.
HY = {"كلب": ["كلب"], "شمس": ["شمس"], "عين": ["عين", "عون"]}
AJ = [("كلب", "كتاب السباع"), ("شمس", "كتاب السماء"), ("عين", "كتاب خلق الإنسان"),
      ("عين", "كتاب المياه")]
WAD = [("كَ لْ ب", "كلب"), ("صَ لَ اْ ت", "صلو"), ("عَ يْ ن", "عين")]
ATOMS = {
    "ءَلْكَلْبُ": ("ءَ", "لْ", "كَ", "لْ", "بُ"), "ءَشْشَمْسُ": ("ءَ", "شْ", "شَ", "مْ", "سُ"),
    "لْكَلْبُ": ("لْ", "كَ", "لْ", "بُ"), "كَلْبُ": ("كَ", "لْ", "بُ"), "عَيْنُ": ("عَ", "يْ", "نُ"),
    "ءَلْعَيْنُ": ("ءَ", "لْ", "عَ", "يْ", "نُ"), "كَتَبَ": ("كَ", "تَ", "بَ"),
    "ءَلْلَيْلُ": ("ءَ", "لْ", "لَ", "يْ", "لُ"),
    "ءَيْيَاْمِ": ("ءَ", "يْ", "يَ", "اْ", "مِ"), "شْشَمْسُ": ("شْ", "شَ", "مْ", "سُ"),
}


def rows() -> list[list[str]]:
    return [ln.split(",") for ln in TABLE.read_text(encoding="utf-8").splitlines()]


def mismatches() -> list[str]:
    bad = []
    duns = DUN_BY_RAMZ
    for r in rows():
        if r[0] == "khutwa":
            got = S.ramz(S.khutwa(r[1], duns[r[2]], QURRA[r[3]]))
            want = r[4]
        elif r[0] == "jins":
            a = ATOMS[r[1]]
            rs = S.judhur_of(HY, a)
            got = ",".join([S.haykal(S.tajrid(a)), "|".join(rs),
                            "|".join(f"{x}:{y}" for x, y in S.ajnas_of(AJ, rs))])
            want = ",".join(r[2:5])
        elif r[0] == "haml":
            rs = r[3].split("|") if r[3] else []
            got = "|".join(f"{x}:{y}" for x, y in S.haml_of(MANQUL, WAD, r[1], r[2], rs))
            want = r[4]
        else:
            got = S.ramz(S.ahkam(r[1], ("m", r[1]), SHAHID)[int(r[2])])
            want = r[3]
        if got != want:
            bad.append(f"{','.join(r)} ≠ {got}")
    return bad


def test_table_shape() -> None:
    kinds = [r[0] for r in rows()]
    assert tuple(kinds.count(k) for k in ("khutwa", "silsila", "jins", "haml")) == (84, 6, 10, 7)


def test_mirror_matches_lean() -> None:
    assert mismatches() == []


def test_by_hand() -> None:
    assert S.ahkam("كتب", ("m", "كتب"), SHAHID) == [
        ("l", "rafd:REJECT"), ("l", "dunaha"), ("l", "dunaha")]
    assert S.ahkam("كَتَبَ", ("m", "كَتَبَ"), SHAHID) == [
        ("m", "كَتَبَ"), ("p", ("فعل", "اسم")), ("l", "laQari")]
    assert S.khutwa("x", ("l", "rafd:R"), lambda _w, _d: ("m", "v")) == ("l", "dunaha")
    assert S.khutwa("x", ("m", "d"), None) == ("l", "laQari")
    assert S.rafd("REJECT") == ("l", "rafd:REJECT")


def test_d32_signs_are_the_deposited_sixteen() -> None:
    """أسماءُ علامات D3₂ من النتائج المودَعة بأعيانها (6 + 1 + 8 + 1)، لا اختيارَ في الأداة."""
    qk = S._load("gen_qism_khanat", ROOT / "tools" / "gen_qism_khanat.py")
    sg = S.d32_signs(qk, lambda _t: None)
    r5 = json.loads((ROOT / "docs" / "qism-khanat" / "result-5.json").read_text(encoding="utf-8"))
    assert len(sg) == r5["D3"]["signs"] == 16
    assert {"TA_SAKINA", "HARF_LAFZ", "ISM_WAZN", "LAMMA_MADI_ISM", "AMIL_NEXT_N_JARR_0"} <= set(sg)
    assert not any(n.startswith("AMIL_") and "_N_" not in n for n in sg)


def test_manqul_rows_from_lean() -> None:
    """صفوفُ `Haqaiq.naql` تُقرأ من نصّ Lean: تسعةٌ، أربعٌ شرعيّة (س417)."""
    m = S.manqul()
    assert len(m) == 9 and m["الصلاة"] == "shariyya" and m["الدابة"] == "urfiyya_amma"
    assert sum(v == "shariyya" for v in m.values()) == 4


def test_wad_key_and_lexicon_conventions() -> None:
    assert S.wad_key(("كَ", "لْ", "بُ"), "كَلْبُ") == "كَ لْ ب"
    assert S.wad_key(("رَ", "حْ", "مَ", "تَ", "نْ"), "رَحْمَةً") == "رَ حْ مَ ت"
    assert S.sk_norm("رحمة") == "رحمت" and S.lane_root("اوب") == "ءوب"
    assert S.lexicon_forms("والكتاب", "كتب") == ["والكتاب", "الكتاب", "كتاب"]
    assert S.lexicon_forms("ولد", "ولد") == ["ولد"]
    assert S.lexicon_forms("الرحمة", "رحم") == ["الرحمت", "رحمت"]
    assert S.tajrid(("ءَ", "لْ", "حَ", "مْ", "دُ")) == ("حَ", "مْ", "دُ")
    assert S.tajrid(("ءَ", "يْ", "يَ", "اْ", "مِ")) == ("ءَ", "يْ", "يَ", "اْ", "مِ")


def test_lisan_in_noun_lexicon() -> None:
    """بأمر المالك: هياكلُ «لسان العرب» في معجم جذر الاسم.

    «رحمن» و«رحيم» تحت «رحم» فيه (`shuhud.tsv.gz`)، لا في هياكل ابن فارس."""
    faris = {ln.split("\t")[0] for ln in S.SKELETONS.read_text(encoding="utf-8").splitlines()}
    assert "رحمن" not in faris and "الرحمن" not in faris
    hy = S.hayakil()
    assert hy["رحمن"] == ["رحم"] and hy["رحيم"] == ["رحم"]
    assert ("رحم", "الرحمن") in S.lisan_hayakil()


Fake = Callable[..., Any]

MUTANTS: dict[str, tuple[str, Callable[[Fake], Fake]]] = {
    "MUTANT_STRIPAL_NO_GEMINATE": ("tajrid", lambda o: lambda a: tuple(a)
                                   if len(a) > 1 and tuple(a)[0][1:] == "ْ" and tuple(a)[0] != "لْ"
                                   and tuple(a)[0][0] == tuple(a)[1][0] else o(a)),
    "MUTANT_SHAMSI_ANY_LETTER": ("SHAMSI", lambda o: frozenset("ءابتثجحخدذرزسشصضطظعغفقكلمنهوي")),
    "MUTANT_NO_SHAMSI": ("tajrid", lambda o: lambda a: tuple(a) if tuple(a)[:1] == ("ءَ",)
                         and tuple(a)[1:2] != ("لْ",) else o(a)),
    "MUTANT_AJNAS_IGNORE_QAYD": ("ajnas_of", lambda o: lambda aj, rs: list(dict.fromkeys(aj))
                                 if rs else o(aj, rs)),
    "MUTANT_NAW_ALWAYS_LUGHAWI": ("naw_of", lambda o: lambda m, lafz: "lughawiyya"),
    "MUTANT_HAML_IGNORE_QAYD": ("haml_of", lambda o: lambda m, w, lafz, k, rs:
                                o(m, w, lafz, k, [r for _k, r in w])),
    "MUTANT_KHARIJ_AS_LAQARI": ("ramz", lambda o: lambda h: "l:laQari" if h == ("l", "kharij")
                                else o(h)),
    "MUTANT_NO_PROPAGATION": ("saqit", lambda o: lambda h: False),
    "MUTANT_LAQARI_PASSES_DUN": ("khutwa", lambda o: lambda w, d, q:
                                 d if q is None else o(w, d, q)),
    "MUTANT_DUNAHA_KEEPS_SABAB": ("khutwa", lambda o: lambda w, d, q:
                                  d if d[0] == "l" else o(w, d, q)),
    "MUTANT_RAMZ_DROPS_SABAB": ("ramz", lambda o: lambda h: "l:" if h[0] == "l" else o(h)),
}


@pytest.mark.parametrize("name", sorted(MUTANTS))
def test_mutant_killed(name: str, monkeypatch: pytest.MonkeyPatch) -> None:
    attr, make = MUTANTS[name]
    monkeypatch.setattr(S, attr, make(getattr(S, attr)))
    assert mismatches() != []
