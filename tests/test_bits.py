"""البتّاتُ على السُّلَّم: شهاداتُ المدوّنة المختومة (مودَعةً خاناتٍ وأعدادًا) تمرّ بكلّ درجةٍ بلا ضياع، وكلُّ
عددٍ تحت حدّه المبرهَن.

التوقّعاتُ مستقلّةٌ عن `gen_bits_index`: تُعاد هنا من الدوالّ الأصليّة مباشرة، والطفرةُ (خانةٌ تُبدَّل، عددٌ فوق
U(n)، بتٌّ يُقلب في التيار) تُرفَض.
"""

from __future__ import annotations

import contextlib
import gzip
import json
from functools import cache
from pathlib import Path

import pytest

from slge.cells import count, fold, licensed, unfold
from slge.entry import from_atoms, to_atoms
from slge.grant import climb
from slge.stream import cost, decode, decode_word, encode, encode_word

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA = ROOT_DIR / "tests" / "data" / "corpus-certificates.json.gz"


@cache
def _deposit() -> dict[str, object]:
    with gzip.open(DATA, "rt", encoding="utf-8") as f:
        d: dict[str, object] = json.load(f)
    return d


def _forms(d: dict[str, object]) -> list[tuple[tuple[str, str], ...]]:
    forms = d["forms"]
    assert isinstance(forms, list)
    return [tuple((a, b) for a, b in f["cells"]) for f in forms]


def test_deposit_is_the_sealed_corpus_as_cells_and_numbers() -> None:
    deposit = _deposit()
    sha = "37633090743d403886b334d12dd911d1994e49767faa9f2be0f01fd48b466c5a"
    assert deposit["corpus_sha256"] == sha
    assert deposit["bridge_protocol"] == "A116-CANONICAL-TXT-1.1" and deposit["tokens"] == 78245
    forms = _forms(deposit)
    stream = deposit["stream"]
    assert isinstance(stream, list)
    assert len(forms) == 18179 and sum(i >= 0 for i in stream) == 78207
    assert sum(len(w) for w in forms) == 99130
    assert all(from_atoms(to_atoms(w)) == w for w in forms)  # الخاناتُ ذرّاتٌ بعينها
    refusals = deposit["refusals"]
    assert isinstance(refusals, dict) and sum(refusals.values()) == 78245 - 78207
    assert all(k.split(":")[0] in ("DEFER", "REJECT", "OUTSIDE_DECLARED_DOMAIN") for k in refusals)


def test_fold_under_its_proven_bound_and_back() -> None:
    deposit = _deposit()
    forms = _forms(deposit)
    lic = [w for w in forms if licensed(w)]
    assert len(lic) == 18114 and len(forms) - len(lic) == 65
    bits = 0
    for w in lic:
        z = fold(w)
        assert z < count(len(w)) and tuple(unfold(len(w), z)) == w
        bits += z.bit_length()
    assert bits == 658873
    assert bits <= sum(count(len(w)).bit_length() for w in lic)
    # الطفرة: عددٌ فوق U(n) لا يُفكّ، وخانةٌ مبدَّلة تغيّر العدد
    w = lic[0]
    with pytest.raises(ValueError):
        unfold(len(w), count(len(w)))
    mutated = (*w[:-1], ("ء" if w[-1][0] != "ء" else "ب", w[-1][1]))
    assert not licensed(mutated) or fold(mutated) != fold(w)
    assert sum(len(climb(w)) for w in forms) == 18114  # المنحُ = الترخيصُ بالضبط


def test_certificate_integer_doubles_the_atoms_number() -> None:
    deposit = _deposit()
    forms = deposit["forms"]
    assert isinstance(forms, list)
    cert = sum(f["integer_bits"] for f in forms)
    atoms = sum(f["atoms_number_bits"] for f in forms)
    # كانا 1,276,753 و651,981 قبل تصحيح همزة الأسماء الموصولة كسرًا (الغانم ADR ٧): خمسُ صورٍ بتًّا أطول
    assert cert == 1276759 and atoms == 651986 and 1.9 < cert / atoms < 2.0  # 1,276,758 قبل ADR ٨
    assert sum(f["residual_bits"] for f in forms) == 38 == sum(f["fiber_size"] > 1 for f in forms)


def test_whole_mushaf_as_one_stream() -> None:
    deposit = _deposit()
    forms = _forms(deposit)
    idx = deposit["stream"]
    assert isinstance(idx, list)
    stream = [forms[i] for i in idx if i >= 0 and licensed(forms[i])]
    bits = encode(stream)
    assert len(stream) == 78100 and len(bits) == 2792533 == sum(cost(len(w)) for w in stream)
    assert all(decode_word(encode_word(w)) == (w, []) for w in stream)
    head = stream[:2000]
    assert decode(encode(head)) == head
    # الطفرة: بتٌّ مقلوبٌ في رأس التيار لا يعيد الكلمةَ الأولى (عددٌ خارج U(n) يُرفض باسمه)
    flipped = encode(head[:5])
    flipped[0] = not flipped[0]
    with contextlib.suppress(ValueError):
        assert decode(flipped)[:1] != head[:1]


def test_index_is_current() -> None:
    import subprocess
    import sys

    gen = str(ROOT_DIR / "tools" / "gen_bits_index.py")
    res = subprocess.run([sys.executable, gen, "--check"], capture_output=True, text=True,
                         cwd=ROOT_DIR)
    assert res.returncode == 0, res.stderr
