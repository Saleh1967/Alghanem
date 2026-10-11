"""شهاداتُ المصحف مودَعًا لـSLGE (`tools/gen_certificates.py`): الأعدادُ ثابتةٌ بتوقّعاتٍ مستقلّة،
والانحرافُ عن المودَع يُرفض باسمه (`DEPOSIT_DRIFTED_FROM_GATE`) بأوّل موضعٍ مختلف؛ والـn يُحمل كاملًا:
رتبةُ الليف وعددُ الشهادة (`A116.Certificate`) — «عَلَى» و«عَلَا» خاناتٌ واحدة وعددان."""

from __future__ import annotations

import copy
import importlib.util
import sys

from conftest import ROOT

SPEC = importlib.util.spec_from_file_location("gen_certificates",
                                              ROOT / "tools" / "gen_certificates.py")
assert SPEC and SPEC.loader
MOD = importlib.util.module_from_spec(SPEC)
sys.modules["gen_certificates"] = MOD
SPEC.loader.exec_module(MOD)
FRESH = MOD.generate()


def test_the_whole_mushaf_as_cells_and_numbers() -> None:
    assert len(FRESH["forms"]) == 18179 and FRESH["tokens"] == 78245
    assert FRESH["refusals"] == {"DEFER:UNVOCALIZED_WORD_IS_NEVER_GUESSED": 30,
                                 "REJECT:TANWIN_WITH_ANOTHER_HARAKA": 4,
                                 "REJECT:INITIAL_SUKUN_WITHOUT_REPAIR": 3,
                                 "REJECT:NOT_CONTINUE_LICENSED_AFTER_REPAIR": 1}
    assert FRESH["stream"].count(-1) == 38 and max(FRESH["stream"]) == 18178
    assert FRESH["forms"][0]["cells"] == [["ب", "كسر"], ["س", "سكون"], ["م", "كسر"]]
    assert all(f["residue_edits"] >= 0 and f["fiber_size"] >= 1 for f in FRESH["forms"])
    assert not any("ب" in c[0] and len(c[0]) != 1 for f in FRESH["forms"] for c in f["cells"])


def test_drift_is_named_at_its_first_position() -> None:
    assert MOD.drift(FRESH, FRESH) is None
    mutant = copy.deepcopy(FRESH)
    mutant["forms"][100]["fiber_size"] += 1
    assert MOD.drift(FRESH, mutant).startswith("forms[100]:")
    mutant = copy.deepcopy(FRESH)
    mutant["stream"][5] = -1
    assert MOD.drift(FRESH, mutant).startswith("stream[5]:")
    mutant = copy.deepcopy(FRESH)
    mutant["codebook_digest"] = "0" * 64
    assert MOD.drift(FRESH, mutant).startswith("codebook_digest:")
    mutant = copy.deepcopy(FRESH)
    del mutant["forms"][-1]
    assert "الطولُ" in MOD.drift(FRESH, mutant)


def _ala() -> tuple[dict[str, object], dict[str, object]]:
    """صورتا عَلَا (بالقائمة) وعَلَى (بالمقصورة) من المودَع بعددَيهما كما تطبعهما البوّابة."""

    from gate import enter

    by_n = {f["integer"]: f for f in FRESH["forms"]}
    alaa, ala = enter("عَلَا".encode()), enter("عَلَى".encode())
    return by_n[alaa.integer], by_n[ala.integer]  # type: ignore[union-attr]


def test_the_number_n_is_carried_whole() -> None:
    # كلُّ صورة: الرتبةُ دون حجم الليف، والعددُ ‎P(F, rank)‎ بالصيغة المغلقة (`Numbering.pair_closed`)
    from gate.contextual import fold_atoms

    atom = {"فتح": "َ", "كسر": "ِ", "ضم": "ُ", "سكون": "ْ"}
    for f in FRESH["forms"]:
        assert 0 <= f["ordinal"] < f["fiber_size"]
        u = fold_atoms(tuple(c + atom[s] for c, s in f["cells"]))
        assert f["integer"] == (u + f["ordinal"]) * (u + f["ordinal"] + 1) // 2 + f["ordinal"]
    # الـn للكلمة لا للرسم: 18,179 صورةً رسمًا على 17,551 عددًا؛ وما تشارك عددًا يفترق ببقيّة الرسم وحدَها
    ns = [f["integer"] for f in FRESH["forms"]]
    assert len(set(ns)) == 17551
    keyed = {(f["integer"], tuple(map(tuple, f["residue"]))) for f in FRESH["forms"]}
    assert len(keyed) == len(FRESH["forms"])
    # الطفرة: من يُسقط البقيّةَ يجعل رَبِّ ورَّبِّ صورةً واحدة (وهي كذلك كلمةً)، ومن يُسقط العددَ يُسقط الرتبة
    assert len({f["integer"] for f in FRESH["forms"]}) < len(FRESH["forms"])
    # الخاناتُ تُسقط الرتبة: كلماتٌ (أعدادٌ) متمايزة تصير بالخانات وحدَها أقلّ، والفرقُ هو الأعدادُ
    # التي رتبتُها في ليفها فوق الصفر — لا غير
    cells = {tuple(map(tuple, f["cells"])) for f in FRESH["forms"]}
    lost = {f["integer"] for f in FRESH["forms"] if f["ordinal"] > 0}
    assert len(set(ns)) - len(cells) == len(lost) == 18


def test_ala_and_alaa_one_cells_two_numbers() -> None:
    alaa, ala = _ala()
    assert alaa["cells"] == ala["cells"] == [["ع", "فتح"], ["ل", "فتح"], ["ا", "سكون"]]
    # بترتيب UTF-8 في الليف: ا (U+0627) قبل ى (U+0649)
    assert (alaa["ordinal"], ala["ordinal"]) == (0, 1) and ala["fiber_size"] == 2
    # ‎P(u, 1) − P(u, 0) = u + 2‎ (`A116.Certificate.pair_rank_one`) وu رقمُ الذرّات عَ لَ اْ
    assert ala["integer"] - alaa["integer"] == 938904 + 2
    # الطفرة: من يقرأ الخاناتِ وحدَها يجعلهما صورةً واحدة
    assert ala["cells"] == alaa["cells"] and ala["integer"] != alaa["integer"]
