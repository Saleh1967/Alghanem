"""شهاداتُ المصحف مودَعًا لـSLGE (`tools/gen_certificates.py`): الأعدادُ ثابتةٌ بتوقّعاتٍ مستقلّة،
والانحرافُ عن المودَع يُرفض باسمه (`DEPOSIT_DRIFTED_FROM_GATE`) بأوّل موضعٍ مختلف."""

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
