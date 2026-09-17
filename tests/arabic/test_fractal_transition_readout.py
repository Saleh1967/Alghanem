"""اختبارُ القراءة: الختمُ يُفحَص، والضابطُ السالبُ يقلب الحكم، والنتيجةُ تُعاد."""

from __future__ import annotations

import pytest

from alghanem.arabic.fractal_transition_hypothesis import FractalVerdict
from alghanem.arabic.fractal_transition_readout import (
    FIELD_EXTRACTORS,
    FieldReading,
    FractalTransitionReadoutError,
    FractalTransitionReadoutGate,
    PairReadingStatus,
    SealedPreregistration,
    StructureSignature,
    read_signature,
    seal_preregistration,
)


def test_a_seal_cannot_be_built_by_hand() -> None:
    with pytest.raises(FractalTransitionReadoutError):
        SealedPreregistration(
            hypothesis_digest="0" * 64,
            preregistration_digest="0" * 64,
            _token=object(),
        )


def test_a_readout_on_a_drifted_seal_is_refused() -> None:
    sealed = seal_preregistration()
    drifted = SealedPreregistration.__new__(SealedPreregistration)
    object.__setattr__(drifted, "hypothesis_digest", "1" * 64)
    object.__setattr__(drifted, "preregistration_digest", sealed.preregistration_digest)
    object.__setattr__(drifted, "_token", object())
    with pytest.raises(FractalTransitionReadoutError):
        FractalTransitionReadoutGate.read_pair(drifted, "syllable-to-word")


def test_an_unmeasurable_jurisdiction_has_no_signature() -> None:
    with pytest.raises(FractalTransitionReadoutError):
        read_signature("compound-layer", "كَتَبَ")


def test_the_two_measurable_layers_read_six_fields_each() -> None:
    for jurisdiction in ("syllable-segmentation", "word-structure-dictionary"):
        signature = read_signature(jurisdiction, "كَتَبَ")
        assert len(signature.readings) == 6
        assert all(reading.named_reason.strip() for reading in signature.readings)


def test_the_comparison_is_not_vacuous() -> None:
    """يقرأ مقياسُ المطابقة كذبًا على مدخلٍ حقيقيّ، فليس شرطًا لا يُفنّده شيء."""

    lower = read_signature("syllable-segmentation", "كتب")
    upper = read_signature("word-structure-dictionary", "كتب")
    assert any(
        lower.holds(field) != upper.holds(field)
        for field in ("Carrier", "Gate", "Identity", "Residual")
    )


def test_the_first_run_verdict_is_reproduced() -> None:
    sealed = seal_preregistration()
    first = FractalTransitionReadoutGate.read_hypothesis(sealed)
    second = FractalTransitionReadoutGate.read_hypothesis(seal_preregistration())
    assert first.verdict is second.verdict
    assert first.verdict is FractalVerdict.WEAKER_MODEL_RECONSTRUCTS
    readouts = {item.pair_id: item for item in first.pairs}
    assert (
        readouts["syllable-to-word"].status
        is PairReadingStatus.WEAKER_MODEL_RECONSTRUCTS
    )
    assert readouts["syllable-to-word"].reconstruct_weaker_model == 28
    assert readouts["syllable-to-word"].reconstruct_structure == 24
    assert readouts["word-to-compound"].status is PairReadingStatus.UNDERPOWERED
    assert readouts["compound-to-sentence"].status is PairReadingStatus.UNDERPOWERED


def test_no_pair_reads_supported_today() -> None:
    first = FractalTransitionReadoutGate.read_hypothesis(seal_preregistration())
    assert first.verdict is not FractalVerdict.SUPPORTED
    assert all(not item.is_holdout_pair for item in first.pairs)


def test_the_negative_control_does_not_read_a_match(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """طبقةٌ عليا مقلوبةُ المحمولات لا تُقرأ تطابقًا؛ فالمعيار يقيس بنيةً لا اسمًا."""

    original = FIELD_EXTRACTORS["word-structure-dictionary"]

    def inverted(surface: str) -> StructureSignature:
        signature = original(surface)
        return StructureSignature(
            jurisdiction=signature.jurisdiction,
            surface=signature.surface,
            readings=tuple(
                FieldReading(
                    field=reading.field,
                    holds=not reading.holds,
                    named_reason=f"ضابطٌ سالب: قُلِب محمولُ {reading.field}",
                )
                for reading in signature.readings
            ),
        )

    monkeypatch.setitem(FIELD_EXTRACTORS, "word-structure-dictionary", inverted)
    readout = FractalTransitionReadoutGate.read_pair(
        seal_preregistration(), "syllable-to-word"
    )
    assert readout.status is not PairReadingStatus.MATCH_HOLDS


def test_a_renamed_layer_is_not_a_structure(monkeypatch: pytest.MonkeyPatch) -> None:
    """طبقتان بالأسماء نفسها ومحمولاتٍ ثابتةٍ صادقة يبتلعهما النموذجُ الأضعف."""

    def always_true(surface: str) -> StructureSignature:
        return StructureSignature(
            jurisdiction="word-structure-dictionary",
            surface=surface,
            readings=tuple(
                FieldReading(
                    field=field,
                    holds=True,
                    named_reason="ضابطٌ سالب: محمولٌ صادقٌ بلا قراءة",
                )
                for field in (
                    "Carrier",
                    "Gate",
                    "Identity",
                    "Trace",
                    "Residual",
                    "Closure",
                )
            ),
        )

    monkeypatch.setitem(FIELD_EXTRACTORS, "word-structure-dictionary", always_true)
    readout = FractalTransitionReadoutGate.read_pair(
        seal_preregistration(), "syllable-to-word"
    )
    assert readout.status is PairReadingStatus.WEAKER_MODEL_RECONSTRUCTS
