"""ختمُ ابن هشام النهائيّ (ADR ١١٥؛ إذنُ المالك 2026-10-19 02:40 بتوقيت عمّان:
«موافق اختم البيب ختم نهائي وحمل قطر الندى واختمه»).

البصماتُ مكتوبةٌ هنا باليد كما حُسبت على نسخة OpenITI/0775AH@61b0c789 في الجلسة، لا من الأداة:
«مغني اللبيب» (Shamela0006972، مرقًّى من الختم التجريبيّ ببصمته نفسِها) و«متن قطر الندى»
(Shamela0011376).

* `MUTANT_ONE_BYTE`: بايتٌ واحدٌ يُقلب فتسقط البصمة.
* `MUTANT_STILL_TRIAL`: «مغني اللبيب» في بيان الختم التجريبيّ يُرفض.
"""

from __future__ import annotations

import gzip
import hashlib
from pathlib import Path

from conftest import ROOT

DIR = ROOT / "corpora" / "kitab"
HAND = {
    "0761JamalDinIbnHisham.MughniLabib.Shamela0006972-ara1":
        ("f37ac2bb4b273f59169053dd0ac2abf50a52846a7e87ddf689ee5c0b87f77e7d", 1486890),
    "0761JamalDinIbnHisham.MatnQatrNada.Shamela0011376-ara1":
        ("2d9241beca1b138187ace8f6782d5eed68f3864f402ec1d5fc90fdeb306ceb9d", 40168),
}


def _raw(name: str, d: Path = DIR) -> bytes:
    return gzip.decompress((d / f"{name}.gz").read_bytes())


def sealed(name: str, d: Path = DIR) -> bool:
    """الفحصُ المستقلّ: البصمةُ والحجمُ المكتوبان باليد على الملفّ في المجلّد."""
    raw = _raw(name, d)
    sha, size = HAND[name]
    return hashlib.sha256(raw).hexdigest() == sha and len(raw) == size


def test_seals_by_hand() -> None:
    for name in HAND:
        assert sealed(name), name
        assert _raw(name).decode("utf-8").startswith("######OpenITI#"), name


def finals_in_trial(trial: str) -> list[str]:
    return [n for n in HAND if n in trial]


def test_final_not_trial() -> None:
    kitab = (DIR / "MANIFEST.tsv").read_text(encoding="utf-8")
    trial = (ROOT / "corpora" / "trial" / "MANIFEST.tsv").read_text(encoding="utf-8")
    for name in HAND:
        rows = [ln.split("\t") for ln in kitab.splitlines() if ln.startswith(name)]
        assert len(rows) == 1 and rows[0][5] == "مختوم", name
    assert finals_in_trial(trial) == []
    assert not (ROOT / "corpora" / "trial" / f"{next(iter(HAND))}.gz").exists()


def test_mutant_one_byte_rejected(tmp_path: Path) -> None:
    """مودَعٌ مطفَّر ببايتٍ واحد في مجلّدٍ مؤقّت يُسقطه الفحصُ نفسُه."""
    for name in HAND:
        raw = bytearray(_raw(name))
        raw[len(raw) // 2] ^= 1
        (tmp_path / f"{name}.gz").write_bytes(gzip.compress(bytes(raw), mtime=0))
        assert not sealed(name, tmp_path), name


def test_mutant_still_trial_rejected() -> None:
    trial = (ROOT / "corpora" / "trial" / "MANIFEST.tsv").read_text(encoding="utf-8")
    planted = trial + f"{next(iter(HAND))}.gz\tx\tx\tx\t0\tتجريبي\tx\n"
    assert finals_in_trial(planted) != []
