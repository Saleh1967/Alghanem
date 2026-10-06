"""المنح: لا اسمَ قبل قبضته — التوقّعاتُ من قانون الجسر لا من شيفرته، مطعَّمةٌ بالطفرة."""

from __future__ import annotations

import dataclasses

from slge.cells import ALPHABET, STATES, SUKUN
from slge.grant import DECLARED, LADDER, MURSAM, Bridge, Granted, Refusal, climb, grant

FATHA = STATES[0]

QALA = ((ALPHABET[21], FATHA), (ALPHABET[1], SUKUN), (ALPHABET[23], FATHA))
BAD_HEAD = ((ALPHABET[2], SUKUN), (ALPHABET[1], FATHA))
BAD_ADJ = ((ALPHABET[2], FATHA), (ALPHABET[1], SUKUN), (ALPHABET[3], SUKUN))


def test_mursam_grants_licensed_only() -> None:
    g = grant(MURSAM, QALA)
    assert isinstance(g, Granted) and g.grants == "مرسوم" and g.cells == QALA
    for bad in (BAD_HEAD, BAD_ADJ):
        r = grant(MURSAM, bad)
        assert isinstance(r, Refusal) and r.code == "CHECK-REFUSED" and r.bridge == "b-mursam"


def test_verdict_cannot_be_forged() -> None:
    """الطفرة التي قبلها `tarkib/bridge.py`: لا حقلَ حكمٍ هنا يُملأ؛ الفحصُ يجري كلَّ مرّة."""

    assert "check_verdict" not in {f.name for f in dataclasses.fields(Bridge)}
    always_no = dataclasses.replace(MURSAM, check=lambda _c: False)
    assert isinstance(grant(always_no, QALA), Refusal)


def test_grant_requires_check_to_run() -> None:
    calls: list[int] = []

    def counting(c: object) -> bool:
        calls.append(1)
        return True

    grant(Bridge("x", "y", counting), QALA)
    assert calls == [1]


def test_ladder_stops_at_first_refusal() -> None:
    reject = Bridge("b-stop", "لا", lambda _c: False)
    above = Bridge("b-above", "فوق", lambda _c: True)
    assert [g.via for g in climb(QALA, (MURSAM, reject, above))] == ["b-mursam"]
    assert climb(BAD_HEAD, (MURSAM, above)) == ()
    assert climb(QALA, ()) == ()


def test_only_one_rung_has_a_working_check() -> None:
    assert LADDER == (MURSAM,)
    assert set(DECLARED) == {
        "b-R-TN", "b-mustarajac", "b-sinf", "b-irab-wazifa", "b-jumla", "b-ifada",
    }
