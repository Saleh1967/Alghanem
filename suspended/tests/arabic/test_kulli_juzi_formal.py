"""البرهان الصوري الشامل على تقسيم الاسم إلى كلّي وجزئي، على نطاق شواهد مُثبَتة.

تُثبِّت هذه الاختبارات خمسة أمور: المجال الصوري مجمَّد وحالاته ثمانٍ بالضبط،
ودالة القرار كلّية على تلك الثماني وترفض ما عداها بدل أن تحمله على أقربها،
ومحورا الكلّي مستقلّان فلا يُقرأ إثباتُ شاهدٍ في أحدهما إثباتًا في الآخر،
والبرهان الشامل ينجح على الشواهد كلها بلا استثناء، والوحدة خاملة سلطويًّا لا
تحرّك بوّابةً ولا تغيّر تدقيقًا خارجيًّا.
"""

import json
from dataclasses import replace
from pathlib import Path

import pytest

from alghanem.arabic.external_audit import audit_card
from alghanem.arabic.kulli_juzi_formal import (
    ATTESTED_NAME_WITNESSES,
    FROZEN_KULLI_JUZI_DOMAIN,
    JINS_IS_NOT_A_PROVED_SYNONYM_NOTE,
    KULLI_ADMISSIBLE_STATES,
    KULLI_AXIS_INDEPENDENCE_NOTE,
    KULLI_FIRST_QUESTION,
    KULLI_NOT_APPLICABLE_TEXT,
    KULLI_SECOND_QUESTION,
    KULLI_SOURCE,
    KULLI_SUCCESS_TITLE,
    AttestedNameWitness,
    FrozenKulliJuziDomain,
    KulliJuziClass,
    KulliJuziFormalError,
    SharingCarrier,
    SubOutcome,
    SubPartition,
    SubPartitionCarrier,
    Universality,
    canonical_sub_outcome,
    canonical_sub_partition,
    canonical_universality,
    classify_kulli_juzi,
    is_sub_partition_askable,
    prove_kulli_juzi_over_attested_corpus,
    universality_of_sub_partition,
)

_EXAMPLES = Path(__file__).resolve().parents[2] / "examples" / "external_audit"

_CARDS = (
    "man_2_255.yaml",
    "maa_2_197.yaml",
    "imran_3_33.yaml",
    "hadhan_20_63.yaml",
)


def _witness(classification: KulliJuziClass) -> AttestedNameWitness:
    found = tuple(
        witness
        for witness in ATTESTED_NAME_WITNESSES
        if witness.attested_class is classification
    )
    assert found
    return found[0]


def test_the_closed_vocabularies_are_exactly_the_declared_values() -> None:
    assert tuple(value.value for value in Universality) == ("كلّي", "جزئي")
    assert tuple(value.value for value in SubPartition) == (
        "التواطؤ_والتشكيك",
        "الجنس_والاشتقاق",
        "العلم_والضمير",
        "لا_محور_مُثبَت",
    )
    assert tuple(value.value for value in SubOutcome) == (
        "متواطئ",
        "مشكِّك",
        "جنس",
        "مشتق",
        "علَم",
        "ضمير",
        "غير_مطروح",
    )
    assert tuple(value.value for value in KulliJuziClass) == (
        "كلّي",
        "كلّي_متواطئ",
        "كلّي_مشكِّك",
        "كلّي_جنس",
        "كلّي_مشتق",
        "جزئي",
        "جزئي_علَم",
        "جزئي_ضمير",
    )


def test_the_frozen_domain_states_its_questions_and_source() -> None:
    assert FROZEN_KULLI_JUZI_DOMAIN.source == KULLI_SOURCE
    assert FROZEN_KULLI_JUZI_DOMAIN.first_question == KULLI_FIRST_QUESTION
    assert FROZEN_KULLI_JUZI_DOMAIN.second_question == KULLI_SECOND_QUESTION
    assert "محورٍ مُثبَت" in FROZEN_KULLI_JUZI_DOMAIN.second_question_condition
    assert FROZEN_KULLI_JUZI_DOMAIN.axis_independence_note == (
        KULLI_AXIS_INDEPENDENCE_NOTE
    )


def test_the_domain_has_exactly_eight_admissible_states() -> None:
    assert FROZEN_KULLI_JUZI_DOMAIN.cardinality == 8
    assert len(set(KULLI_ADMISSIBLE_STATES)) == 8
    assert KULLI_ADMISSIBLE_STATES == (
        (Universality.KULLI, SubPartition.NONE_ATTESTED, SubOutcome.NOT_ASKED),
        (Universality.KULLI, SubPartition.TAWATU_TASHKIK, SubOutcome.MUTAWATI),
        (Universality.KULLI, SubPartition.TAWATU_TASHKIK, SubOutcome.MUSHAKKIK),
        (Universality.KULLI, SubPartition.JINS_ISHTIQAQ, SubOutcome.JINS),
        (Universality.KULLI, SubPartition.JINS_ISHTIQAQ, SubOutcome.MUSHTAQQ),
        (Universality.JUZI, SubPartition.NONE_ATTESTED, SubOutcome.NOT_ASKED),
        (Universality.JUZI, SubPartition.ALAM_DAMIR, SubOutcome.ALAM),
        (Universality.JUZI, SubPartition.ALAM_DAMIR, SubOutcome.DAMIR),
    )


def test_the_domain_refuses_any_other_state_set() -> None:
    with pytest.raises(KulliJuziFormalError):
        FrozenKulliJuziDomain(admissible_states=KULLI_ADMISSIBLE_STATES[:4])
    with pytest.raises(KulliJuziFormalError):
        FrozenKulliJuziDomain(source="  ")


def test_the_decision_function_is_total_on_the_eight_states() -> None:
    derived = tuple(classify_kulli_juzi(*state) for state in KULLI_ADMISSIBLE_STATES)
    assert set(derived) == set(KulliJuziClass)
    assert len(set(derived)) == 8


def test_a_kulli_axis_is_not_asked_of_a_juzi_name() -> None:
    assert universality_of_sub_partition(SubPartition.TAWATU_TASHKIK) is (
        Universality.KULLI
    )
    assert universality_of_sub_partition(SubPartition.ALAM_DAMIR) is Universality.JUZI
    assert universality_of_sub_partition(SubPartition.NONE_ATTESTED) is None
    assert not is_sub_partition_askable(Universality.JUZI, SubPartition.JINS_ISHTIQAQ)
    assert not is_sub_partition_askable(Universality.KULLI, SubPartition.ALAM_DAMIR)
    assert is_sub_partition_askable(Universality.JUZI, SubPartition.NONE_ATTESTED)
    with pytest.raises(KulliJuziFormalError):
        classify_kulli_juzi(
            Universality.JUZI, SubPartition.JINS_ISHTIQAQ, SubOutcome.JINS
        )
    with pytest.raises(KulliJuziFormalError):
        classify_kulli_juzi(
            Universality.KULLI, SubPartition.ALAM_DAMIR, SubOutcome.ALAM
        )


def test_a_declared_axis_without_an_outcome_is_refused_and_the_reverse() -> None:
    with pytest.raises(KulliJuziFormalError):
        classify_kulli_juzi(
            Universality.KULLI, SubPartition.TAWATU_TASHKIK, SubOutcome.NOT_ASKED
        )
    with pytest.raises(KulliJuziFormalError):
        classify_kulli_juzi(
            Universality.KULLI, SubPartition.NONE_ATTESTED, SubOutcome.MUTAWATI
        )


def test_an_outcome_that_does_not_belong_to_its_axis_is_refused() -> None:
    with pytest.raises(KulliJuziFormalError):
        classify_kulli_juzi(
            Universality.KULLI, SubPartition.TAWATU_TASHKIK, SubOutcome.JINS
        )
    with pytest.raises(KulliJuziFormalError):
        classify_kulli_juzi(
            Universality.JUZI, SubPartition.ALAM_DAMIR, SubOutcome.MUSHAKKIK
        )


def test_the_decision_function_refuses_values_outside_the_vocabulary() -> None:
    with pytest.raises(KulliJuziFormalError):
        classify_kulli_juzi(
            "كلّي",  # type: ignore[arg-type]
            SubPartition.NONE_ATTESTED,
            SubOutcome.NOT_ASKED,
        )
    with pytest.raises(KulliJuziFormalError):
        classify_kulli_juzi(
            Universality.KULLI,
            "جنس",  # type: ignore[arg-type]
            SubOutcome.JINS,
        )


def test_the_canonical_readers_refuse_what_they_do_not_name() -> None:
    assert canonical_universality("كلي") is Universality.KULLI
    assert canonical_sub_partition("لا_محور_مُثبَت") is SubPartition.NONE_ATTESTED
    assert canonical_sub_outcome("مشكك") is SubOutcome.MUSHAKKIK
    for reader in (
        canonical_universality,
        canonical_sub_partition,
        canonical_sub_outcome,
    ):
        with pytest.raises(KulliJuziFormalError):
            reader("  ")
        with pytest.raises(KulliJuziFormalError):
            reader("لفظ لا تسمّيه المفردة")


def test_every_declared_class_has_at_least_one_attested_witness() -> None:
    attested = {witness.attested_class for witness in ATTESTED_NAME_WITNESSES}
    assert attested == set(KulliJuziClass)


def test_the_witness_identity_is_its_lexeme_with_its_tested_axis() -> None:
    keys = tuple(witness.witness_key for witness in ATTESTED_NAME_WITNESSES)
    assert len(set(keys)) == len(keys)


def test_an_answer_that_contradicts_its_carrier_is_refused() -> None:
    mutawati = _witness(KulliJuziClass.KULLI_MUTAWATI)
    with pytest.raises(KulliJuziFormalError):
        replace(mutawati, first_answer=Universality.JUZI)
    with pytest.raises(KulliJuziFormalError):
        replace(mutawati, sub_outcome=SubOutcome.MUSHAKKIK)
    with pytest.raises(KulliJuziFormalError):
        replace(mutawati, declared_sub_partition=SubPartition.JINS_ISHTIQAQ)


def test_flipping_the_sub_partition_carrier_flips_the_derived_class() -> None:
    mutawati = _witness(KulliJuziClass.KULLI_MUTAWATI)
    flipped = replace(
        mutawati,
        sub_partition_carrier=SubPartitionCarrier.UNEQUAL_IN_INSTANCES,
        sub_outcome=SubOutcome.MUSHAKKIK,
    )
    assert flipped.derived_class is KulliJuziClass.KULLI_MUSHAKKIK

    jins = _witness(KulliJuziClass.KULLI_JINS)
    flipped_jins = replace(
        jins,
        sub_partition_carrier=SubPartitionCarrier.DETERMINED_ATTRIBUTE,
        sub_outcome=SubOutcome.MUSHTAQQ,
    )
    assert flipped_jins.derived_class is KulliJuziClass.KULLI_MUSHTAQQ


def test_flipping_the_sharing_carrier_refuses_a_now_foreign_axis() -> None:
    alam = _witness(KulliJuziClass.JUZI_ALAM)
    with pytest.raises(KulliJuziFormalError):
        replace(
            alam,
            sharing_carrier=SharingCarrier.SHARING_NOT_PRECLUDED,
            first_answer=Universality.KULLI,
        ).derived_class


def test_a_kulli_axis_witness_must_declare_the_axes_are_independent() -> None:
    for classification in (
        KulliJuziClass.KULLI_MUTAWATI,
        KulliJuziClass.KULLI_MUSHAKKIK,
        KulliJuziClass.KULLI_JINS,
        KulliJuziClass.KULLI_MUSHTAQQ,
    ):
        witness = _witness(classification)
        assert witness.axis_independence_note == KULLI_AXIS_INDEPENDENCE_NOTE
        with pytest.raises(KulliJuziFormalError):
            replace(witness, axis_independence_note=KULLI_NOT_APPLICABLE_TEXT)


def test_every_other_witness_leaves_the_independence_note_not_applicable() -> None:
    for classification in (
        KulliJuziClass.KULLI_ALONE,
        KulliJuziClass.JUZI_ALONE,
        KulliJuziClass.JUZI_ALAM,
        KulliJuziClass.JUZI_DAMIR,
    ):
        witness = _witness(classification)
        assert witness.axis_independence_note == KULLI_NOT_APPLICABLE_TEXT
        with pytest.raises(KulliJuziFormalError):
            replace(witness, axis_independence_note=KULLI_AXIS_INDEPENDENCE_NOTE)


def test_no_witness_is_attested_on_both_kulli_axes_at_once() -> None:
    for witness in ATTESTED_NAME_WITNESSES:
        assert witness.declared_sub_partition in set(SubPartition)
        state = (
            witness.first_answer,
            witness.declared_sub_partition,
            witness.sub_outcome,
        )
        assert state in KULLI_ADMISSIBLE_STATES


def test_the_jins_synonym_claim_is_recorded_as_unproved() -> None:
    assert "الجامد" in JINS_IS_NOT_A_PROVED_SYNONYM_NOTE
    assert "لم يُقَم عليها دليلٌ هنا" in JINS_IS_NOT_A_PROVED_SYNONYM_NOTE
    assert JINS_IS_NOT_A_PROVED_SYNONYM_NOTE not in {
        witness.axis_independence_note for witness in ATTESTED_NAME_WITNESSES
    }


def test_the_blank_and_wrong_typed_fields_are_refused() -> None:
    witness = _witness(KulliJuziClass.KULLI_ALONE)
    with pytest.raises(KulliJuziFormalError):
        replace(witness, lexeme="   ")
    with pytest.raises(KulliJuziFormalError):
        replace(witness, first_evidence="")
    with pytest.raises(KulliJuziFormalError):
        replace(witness, sharing_carrier="لا_يمنع")  # type: ignore[arg-type]
    with pytest.raises(KulliJuziFormalError):
        replace(witness, attested_class="كلّي")  # type: ignore[arg-type]


def test_the_complete_proof_succeeds_on_every_attested_witness() -> None:
    report = prove_kulli_juzi_over_attested_corpus()

    assert len(report.rows) == len(ATTESTED_NAME_WITNESSES)
    assert report.is_complete_success is True
    assert report.unmatched == ()
    assert report.title == KULLI_SUCCESS_TITLE
    assert report.source == KULLI_SOURCE
    assert report.domain is FROZEN_KULLI_JUZI_DOMAIN
    assert all(row.derived_class is row.attested_class for row in report.rows)


def test_a_misreported_witness_is_reported_without_aborting_the_run() -> None:
    jins = _witness(KulliJuziClass.KULLI_JINS)
    misreported = replace(jins, attested_class=KulliJuziClass.KULLI_MUSHTAQQ)

    report = prove_kulli_juzi_over_attested_corpus(
        ATTESTED_NAME_WITNESSES + (misreported,)
    )

    assert len(report.rows) == len(ATTESTED_NAME_WITNESSES) + 1
    assert report.is_complete_success is False
    assert report.title is None
    assert len(report.unmatched) == 1
    assert report.unmatched[0].derived_class is KulliJuziClass.KULLI_JINS
    assert report.unmatched[0].attested_class is KulliJuziClass.KULLI_MUSHTAQQ


def test_the_proof_refuses_an_empty_corpus_and_non_attested_items() -> None:
    with pytest.raises(KulliJuziFormalError):
        prove_kulli_juzi_over_attested_corpus(())
    with pytest.raises(KulliJuziFormalError):
        prove_kulli_juzi_over_attested_corpus(("الحيوان",))  # type: ignore[arg-type]


def test_the_module_reads_no_kernel_authority() -> None:
    source = (
        Path(__file__).resolve().parents[2]
        / "src"
        / "alghanem"
        / "arabic"
        / "kulli_juzi_formal.py"
    ).read_text(encoding="utf-8")

    imports = tuple(
        line for line in source.splitlines() if line.startswith(("import ", "from "))
    )

    assert imports
    assert not any("kernel" in line for line in imports)


@pytest.mark.parametrize("card", _CARDS)
def test_the_classification_changes_no_external_audit_field(card: str) -> None:
    before = json.dumps(
        audit_card(_EXAMPLES / card).to_dict(), ensure_ascii=False, sort_keys=True
    )

    prove_kulli_juzi_over_attested_corpus()

    after = json.dumps(
        audit_card(_EXAMPLES / card).to_dict(), ensure_ascii=False, sort_keys=True
    )
    assert before == after
