"""البوّابة: كلُّ جاهزٍ يعود بايتًا ببايت، ويقبله النموذجُ المبرهَن، وذرّاتُه مشتقّةٌ من رسمه."""

from __future__ import annotations

import pytest

from gate import Refusal, enter, exit, gate, recover
from gate.licence import binary_ok, continue_licensed, kind_of, pause_licensed
from gate.rasm_consistency import consistent


def test_licence_matches_lean_witnesses() -> None:
    """الشواهدُ المسمّاةُ في `Ternary.lean`: hajja، bahr، tamm."""

    hajja, bahr, tamm = ["cv", "v", "c", "cv"], ["cv", "c", "c"], ["cv", "v", "c", "c"]
    assert continue_licensed(hajja) and not binary_ok(hajja)
    assert pause_licensed(bahr) and not continue_licensed(bahr)
    assert pause_licensed(tamm) and not continue_licensed(tamm)
    assert kind_of(("حَ", "اْ", "جْ", "جَ")) == hajja
    assert kind_of(("مَ", "اْ")) == ["cv", "v"] and kind_of(("مِ", "نْ")) == ["cv", "c"]


def test_corpus_is_the_sealed_one() -> None:
    assert gate().book.payload["bridge_protocol"] == "A116-CANONICAL-TXT-1.1"
    assert len(gate().book.domain) == 18200


def test_every_ready_word_round_trips_and_is_admissible() -> None:
    g = gate()
    ready = madd = 0
    for surface in g.book.domain:
        cert = g.enter(surface.encode("utf-8"))
        if isinstance(cert, Refusal):
            assert cert.status in ("DEFER", "REJECT") and cert.reasons
            continue
        ready += 1
        assert g.exit(cert) == surface.encode("utf-8")
        k = kind_of(cert.atoms)
        assert continue_licensed(k), surface
        if not binary_ok(k):
            madd += 1
        assert consistent(surface, cert.atoms), surface
        assert g.book.decode_integer(cert.integer) == surface
    assert ready == 8532
    assert madd == 22  # ما يراه الثلاثيُّ ويعمى عنه الثنائيّ (مدٌّ ثمّ مشدَّد)


def test_refusals_are_named_and_never_guessed() -> None:
    assert enter("حاسوب".encode()).status == "DEFER"
    assert enter("يَعْلَمُونَ".encode()).reasons == ("HARAKA_IS_ABSENT_AND_IS_NEVER_GUESSED",)
    with pytest.raises(ValueError):
        exit(enter("كَتَبَ".encode())._replace(ordinal=5) if False else _tampered())


def _tampered():
    from dataclasses import replace

    return replace(enter("كَتَبَ".encode()), ordinal=5)


def test_generation_and_recovery_agree() -> None:
    cert = enter("كَتَبَ".encode())
    assert not isinstance(cert, Refusal)
    outcome, found = recover(cert)
    assert outcome == "RECOVERED" and ("كتب", "PAST", "I-a", "3MS") in found


@pytest.mark.slow
def test_recovery_on_masaq_verbs_is_at_least_97_percent() -> None:
    from gate.mabni_bridge import verb_readings

    r = verb_readings()
    total = sum(r["outcomes"].values()) if "outcomes" in r else None
    assert total, r.keys()
    assert r["outcomes"]["RECOVERED"] / total >= 0.97
