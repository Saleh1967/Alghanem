"""الهمزة: قاعدةُ الكرسيّ = جدولُ Lean (384 سياقًا)، ومقيسةٌ على كراسي المصحف (4,214)، والمخالفُ مسمًّى."""

from __future__ import annotations

from collections import Counter

from conftest import ROOT

from gate import Refusal, enter
from gate.hamza import SEATS, predict_seat, seat_of
from gate.residue import clusters, repair

_POS = {"A116.Hamza.Pos.initial": "initial", "A116.Hamza.Pos.medial": "medial",
        "A116.Hamza.Pos.final": "final"}
_H = {"A116.Haraka.fatha": "fatha", "A116.Haraka.damma": "damma", "A116.Haraka.kasra": "kasra",
      "A116.Haraka.sukun": "sukun"}
_SEAT = {"A116.Hamza.Seat.alif": "أ", "A116.Hamza.Seat.alifBelow": "إ", "A116.Hamza.Seat.waw": "ؤ",
         "A116.Hamza.Seat.ya": "ئ", "A116.Hamza.Seat.line": "ء"}


def test_seat_rule_matches_lean_table() -> None:
    rows = 0
    with (ROOT / "formal" / "a116" / "hamza.csv").open(encoding="utf-8") as fh:
        for line in fh:
            p, own, prev, pl, py, nw, seat = line.rstrip("\n").split(",")
            ctx = (_POS[p], _H[own], _H[prev], pl == "true", py == "true", nw == "true")
            assert seat_of(ctx) == _SEAT[seat], line
            rows += 1
    assert rows == 384


def test_seat_rule_on_the_sealed_corpus() -> None:
    """4,112 من 4,213 كرسيًّا في الشهادات بالقاعدة (97.60%)؛ والمخالفُ 101 في أجناسٍ مسمّاة (رسمُ
    المصحف: مِائَة، لُؤْلُؤ، نَبَإٍ، لَئِن؛ ولواصقُ مركّبة وَالْإِحْسَان؛ وفِئَة بلا لاصقة) — بقيّةٌ لا تخمين."""

    text = (ROOT / "corpora" / "quran-simple-enhanced.txt").read_text(encoding="utf-8")
    surfaces = {w for w in text.split() if w != "<sel>" and any("ء" <= c <= "ي" for c in w)}
    total, agree, miss = 0, 0, Counter()
    for s in sorted(surfaces):
        if isinstance(enter(s.encode("utf-8")), Refusal):
            continue
        canonical, _ = repair(s)
        cl = clusters(canonical)
        for i, c in enumerate(cl):
            if c[0] in SEATS:
                total += 1
                if predict_seat(canonical, i) == c[0]:
                    agree += 1
                else:
                    miss[c[0]] += 1
    assert total == 4213 and agree == 4112
    assert dict(miss) == {"أ": 16, "إ": 30, "ئ": 46, "ؤ": 7, "ء": 2}
