"""شواهدُ ترميز الوقعات وإسنادها: استرجاعٌ مفحوص، وضرورةٌ مُشغَّلة، وإرجاءٌ محفوظ."""

from __future__ import annotations

import pytest

from alghanem.arabic.occurrence_attribution_encoding import (
    OCCURRENCE_ATTRIBUTION_NAMED_RESIDUALS,
    THE_TWO_MIMS,
    UNRESOLVED_STATE,
    AttributionFieldNecessity,
    BirthBlocker,
    EncodedCorpus,
    LinguisticAndPhoneticBirth,
    OccurrenceAttributionError,
    OccurrenceRecord,
    SeparatedData,
    assess_attribution_field,
    assess_linguistic_and_phonetic_birth,
    decode_corpus,
    encode_corpus,
    occurrences_of,
    separate,
)
from alghanem.arabic.reference_articulation_layer import read_the_deposited_ayah


def measured() -> tuple[OccurrenceRecord, ...]:
    """وقعاتُ النصّ المُودَع، مقروءةً بالقاعدة المُعلَنة لا مكتوبةً هنا."""

    return occurrences_of(read_the_deposited_ayah())


def test_the_measured_occurrences_survive_a_round_trip() -> None:
    """فكُّ الترميز يُعيد كلَّ وقعةٍ في محلّها، وهو الهدفُ المُعلَن."""

    records = measured()
    encoded = encode_corpus(records)
    assert decode_corpus(encoded) == records
    assert encoded.bit_length == len(encoded.bits)
    assert set(encoded.bits) <= {"0", "1"}


def test_distinct_pairs_never_collide_in_the_registers() -> None:
    """زوجان مختلفان لا يشتركان في رمزٍ واحد؛ والتمايزُ مفحوصٌ بالتشغيل."""

    records = measured()
    encoded = encode_corpus(records)
    codes = {
        (
            encoded.registers.carrier_code(one.carrier),
            encoded.registers.state_code(one.state),
        )
        for one in records
    }
    assert len(codes) == len({one.pair for one in records})
    assert len(encoded.registers.carriers) == len(set(encoded.registers.carriers))
    assert len(encoded.registers.states) == len(set(encoded.registers.states))


def test_an_unassigned_code_is_refused_not_rounded_to_a_neighbour() -> None:
    """رمزٌ لا مدخلَ له في السجلّ يُرَدّ، ولا يُردّ عنه أقربُ مدخل."""

    records = measured()
    encoded = encode_corpus(records)
    registers = encoded.registers
    assert len(registers.carriers) < (1 << registers.carrier_width)
    head = 32 + registers.length_width
    unassigned = format(len(registers.carriers), f"0{registers.carrier_width}b")
    tampered = EncodedCorpus(
        registers=registers,
        bits=encoded.bits[:head]
        + unassigned
        + encoded.bits[head + registers.carrier_width :],
        word_count=encoded.word_count,
    )
    with pytest.raises(OccurrenceAttributionError):
        decode_corpus(tampered)


def test_word_boundaries_are_preserved_through_the_round_trip() -> None:
    """حدودُ الكلمات تُسترجَع كما دخلت؛ فالطولُ مُصرَّحٌ به قبل كلّ كلمة."""

    records = measured()
    encoded = encode_corpus(records)
    decoded = decode_corpus(encoded)
    assert encoded.word_count == len({one.word_index for one in records})
    assert [one.word_index for one in decoded] == [one.word_index for one in records]


def test_a_truncated_or_padded_stream_is_refused() -> None:
    """بايتاتٌ ناقصةٌ لا تُكمَّل بأصفار، وزائدةٌ لا تُهمَل."""

    encoded = encode_corpus(measured())
    with pytest.raises(OccurrenceAttributionError):
        decode_corpus(
            EncodedCorpus(
                registers=encoded.registers,
                bits=encoded.bits[:-3],
                word_count=encoded.word_count,
            )
        )
    with pytest.raises(OccurrenceAttributionError):
        decode_corpus(
            EncodedCorpus(
                registers=encoded.registers,
                bits=encoded.bits + "0000",
                word_count=encoded.word_count,
            )
        )


def test_the_two_mims_lose_their_attribution_once_separated() -> None:
    """مثالُ الميمين: حاملٌ واحدٌ وحالان، فالفصلُ يُضيع موضعَ الإسناد."""

    assert len({one.carrier for one in THE_TWO_MIMS}) == 1
    assert len({one.state for one in THE_TWO_MIMS}) == 2
    separated = separate(THE_TWO_MIMS)
    assert separated.attribution_is_lost is True
    assert len(separated.consistent_reassemblies) == 2
    assert tuple(one.pair for one in THE_TWO_MIMS) in separated.consistent_reassemblies


def test_a_swap_of_the_two_states_also_survives_the_separation() -> None:
    """تجربةُ تبديل الإسناد: المبدَّلُ متّسقٌ مع المفصول كاتّساق الأصل."""

    swapped = (
        OccurrenceRecord(word_index=0, carrier="م", state="متحرّكة"),
        OccurrenceRecord(word_index=0, carrier="م", state="ساكنة"),
    )
    separated = separate(THE_TWO_MIMS)
    assert tuple(one.pair for one in swapped) in separated.consistent_reassemblies
    assert separate(swapped).consistent_reassemblies == (
        separated.consistent_reassemblies
    )
    assert decode_corpus(encode_corpus(swapped)) == swapped
    assert decode_corpus(encode_corpus(THE_TWO_MIMS)) != swapped


def test_a_separation_of_identical_states_loses_nothing() -> None:
    """ضابطٌ سالب: إن اتّحدت الحالاتُ فلا موضعَ يضيع، فالبوّابةُ ليست خاوية."""

    identical = (
        OccurrenceRecord(word_index=0, carrier="م", state="ساكنة"),
        OccurrenceRecord(word_index=0, carrier="ب", state="ساكنة"),
    )
    separated = separate(identical)
    assert separated.attribution_is_lost is False
    assert len(separated.consistent_reassemblies) == 1


def test_a_separation_that_drops_a_member_is_refused() -> None:
    """مجموعتان مختلفتا الكثرة ليستا فصلًا لهذه الوقعات."""

    with pytest.raises(OccurrenceAttributionError):
        SeparatedData(carriers=("م", "م"), states=("ساكنة",))


def test_the_extra_attribution_field_costs_bits_and_adds_nothing() -> None:
    """الحقلُ الثالثُ يزيد بتّاتٍ ولا يزيد استرجاعًا للهدف المُعلَن."""

    decision = assess_attribution_field(measured())
    assert decision.necessity is (
        AttributionFieldNecessity.NOT_NECESSARY_FOR_THE_DECLARED_TARGET
    )
    assert decision.both_retrieve_the_same is True
    assert decision.added_bits > 0
    assert decision.augmented_bits == decision.plain_bits + decision.added_bits


def test_an_unresolved_occurrence_is_encoded_as_unresolved() -> None:
    """الامتناعُ عن التعيين يُرمَّز ويُسترجَع امتناعًا، ولا يُخمَّن له حال."""

    records = measured()
    assert any(one.state == UNRESOLVED_STATE for one in records)
    decoded = decode_corpus(encode_corpus(records))
    assert [one.state for one in decoded] == [one.state for one in records]


def test_a_malformed_record_or_register_is_refused_at_construction() -> None:
    """حارسُ البناء يرفض الناقصَ والمكرَّر، ولا يُصحَّح المُدخَلُ ضمنًا."""

    with pytest.raises(OccurrenceAttributionError):
        OccurrenceRecord(word_index=-1, carrier="م", state="ساكنة")
    with pytest.raises(OccurrenceAttributionError):
        OccurrenceRecord(word_index=0, carrier="", state="ساكنة")
    with pytest.raises(OccurrenceAttributionError):
        encode_corpus(())


def test_the_verdict_separates_what_passed_from_what_is_deferred() -> None:
    """الاسترجاعُ قائمٌ والعلاقةُ ضروريّة، والشهادةُ مُرجأةٌ بموانعها الثلاثة."""

    verdict = assess_linguistic_and_phonetic_birth()
    assert verdict.retrieval_holds_in_the_measured_scope is True
    assert verdict.attribution_relation_is_necessary is True
    assert verdict.attribution_field is (
        AttributionFieldNecessity.NOT_NECESSARY_FOR_THE_DECLARED_TARGET
    )
    assert verdict.linguistic_and_phonetic is LinguisticAndPhoneticBirth.DEFER
    assert set(verdict.blockers) == set(BirthBlocker)
    assert len(LinguisticAndPhoneticBirth) == 1
    assert verdict.a_three_field_triple_is_born is False
    assert verdict.a_complete_linguistic_fiber_law_is_born is False


def test_the_named_residuals_are_deposited_with_their_own_names() -> None:
    """كلُّ بقيّةٍ تحمل اسمَها في نصّها، فلا يُبدَّل الاسمُ دون النصّ."""

    assert len(OCCURRENCE_ATTRIBUTION_NAMED_RESIDUALS) == 8
    for name, text in OCCURRENCE_ATTRIBUTION_NAMED_RESIDUALS.items():
        assert text.startswith(f"{name}: ")
    assert "NO_LINGUISTIC_FIBER_LAW_IS_BORN_HERE" in (
        OCCURRENCE_ATTRIBUTION_NAMED_RESIDUALS
    )
