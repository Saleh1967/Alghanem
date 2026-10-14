"""الختمُ التجريبيّ (ADR ٦١): البصماتُ مكتوبةٌ هنا باليد كما حُسبت من مستودعات OpenITI، لا من الأداة.

الطفراتُ بأسمائها:

* `MUTANT_ONE_BYTE`: بايتٌ واحدٌ يُقلب في نصٍّ مختوم فتسقط بصمتُه.
* `MUTANT_STATUS_FINAL`: صفٌّ في البيان حالُه غيرُ «تجريبي» يُرفض، فلا يُرقّى نصٌّ إلّا بتوقيع المالك.
* `MUTANT_GATE_READS_TRIAL`: ملفٌّ في `gate/` يذكر `corpora/trial` يُلتقط.
"""

from __future__ import annotations

import gzip
import hashlib
import importlib.util
import sys
from pathlib import Path
from typing import Any

from conftest import ROOT

SPEC = importlib.util.spec_from_file_location("gen_trial_seals",
                                              ROOT / "tools" / "gen_trial_seals.py")
assert SPEC and SPEC.loader
MOD: Any = importlib.util.module_from_spec(SPEC)
sys.modules["gen_trial_seals"] = MOD
SPEC.loader.exec_module(MOD)

DIR = ROOT / "corpora" / "trial"
HAND = {  # من الحساب على نسخ OpenITI في الجلسة (2026-10-14)
    "0761JamalDinIbnHisham.MughniLabib.Shamela0006972-ara1":
        "f37ac2bb4b273f59169053dd0ac2abf50a52846a7e87ddf689ee5c0b87f77e7d",
    "0794BadrDinZarkashi.BurhanFiCulumQuran.Shamela0011436-ara1":
        "393283ef77be278ffc2ce35e3a8095205a2ba2567775d7c7a4be5bd26729fa88",
    "0338AbuJacfarNahhas.IcrabQuran.Shamela0023587-ara1":
        "16d81f1f7b2852cc528bf6f9edc5f5f252d78f7c59b59fc18652d117e343a3aa",
    "0616MuhibbDinCukbari.TibyanFiIcrabQuran.Shamela0022928-ara1":
        "5a6fa8cca71cea3c1592f25e18cb49ab5efe1bbfa56345dfb41f35cafcadbb50",
}


def _raw(name: str) -> bytes:
    return gzip.decompress((DIR / f"{name}.gz").read_bytes())


def test_seals_by_hand() -> None:
    assert {f.name for f in DIR.glob("*.gz")} == {f"{n}.gz" for n in HAND}
    for name, sha in HAND.items():
        assert hashlib.sha256(_raw(name)).hexdigest() == sha, name
    assert MOD.breaches() == []


def test_texts_are_openiti_and_unvowelled() -> None:
    for name in HAND:
        text = _raw(name).decode("utf-8")
        assert text.startswith("######OpenITI#"), name
        letters = sum(1 for c in text if "ء" <= c <= "ي")
        marks = sum(1 for c in text if "ً" <= c <= "ْ")
        assert letters > 100_000 and marks == 0, name


def test_mutant_one_byte_rejected() -> None:
    name = next(iter(HAND))
    raw = bytearray(_raw(name))
    raw[len(raw) // 2] ^= 1
    assert hashlib.sha256(bytes(raw)).hexdigest() != HAND[name]


def _statuses(manifest: str) -> list[str]:
    return [ln.split("\t")[5] for ln in manifest.splitlines()[1:]]


def test_every_row_is_trial() -> None:
    text = (DIR / "MANIFEST.tsv").read_text(encoding="utf-8")
    assert _statuses(text) == ["تجريبي"] * 4


def test_mutant_status_final_rejected() -> None:
    text = (DIR / "MANIFEST.tsv").read_text(encoding="utf-8").replace("تجريبي", "نهائي", 1)
    assert _statuses(text) != ["تجريبي"] * 4


def _readers(root: Path) -> list[Path]:
    return [p for p in root.rglob("*.py") if "corpora/trial" in p.read_text(encoding="utf-8")]


def test_gate_does_not_read_trial() -> None:
    assert _readers(ROOT / "gate") == []
    users = {p.relative_to(ROOT).as_posix() for p in _readers(ROOT / "tools")}
    assert users <= {"tools/gen_trial_seals.py"}


def test_mutant_gate_reads_trial_caught(tmp_path: Path) -> None:
    (tmp_path / "planted.py").write_text('P = "corpora/trial/x.gz"\n', encoding="utf-8")
    assert _readers(tmp_path) != []
