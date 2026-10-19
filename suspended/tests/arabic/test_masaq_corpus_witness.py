"""اختباراتُ إيداعِ شاهد MASAQ ومَوانعِ إيداعه وقراءةِ صفوفه بربطٍ مُصرَّحٍ به.

والصفوفُ المكتوبةُ هنا **مُصطنَعةٌ مُصرَّحٌ بجنسها**، لا مقتطعةٌ من المدوَّنة:
بايتاتُها ليست في هذه الشجرة ولم تُفتَح فيها، وبنيةُ الصفّ وحدَها هي المُحاكاة.
وأسماءُ الأعمدة هنا **أسماءُ الاختبار** لا أسماءَ الملفّ الحقيقيّ؛ فربطُ
الأعمدة قرارٌ يُسَنُّ عند حائز البايتات لا يُخمَّن هنا.
"""

from __future__ import annotations

import hashlib

import pytest

from alghanem.arabic.masaq_corpus_witness import (
    MASAQ_ARRIVING_SHA256,
    MASAQ_COLUMN_BINDING,
    MASAQ_CORPUS_WITNESS,
    MASAQ_DEPOSIT_BARRIERS,
    MASAQ_WITNESS_NAMED_RESIDUALS,
    DepositStanding,
    MasaqColumnBinding,
    MasaqWitnessError,
    binding_digest,
    deposit_masaq_witness,
    masdar_rows,
    open_barriers,
    parse_masaq_rows,
    verified_masaq_bytes,
)

BINDING = MasaqColumnBinding(
    declared_by="اختبارٌ مُصطنَع؛ لا حائزَ بايتاتٍ أعلن هذه الأسماء",
    what_it_assumes="أسماءُ الأعمدة مكتوبةٌ في الاختبار لا مقروءةٌ من ملفّ",
    location_column="location",
    form_column="form",
    morphological_tag_column="tag",
    root_column="root",
    lemma_column="lemma",
    verb_form_column="verb_form",
    masdar_tag_values=("GERUND",),
    meemi_masdar_tag_values=("GERUND_MEEM",),
)

SYNTHETIC_CSV = (
    "location,form,tag,root,lemma,verb_form\n"
    "(2:3:2:1),qiyAm,GERUND,qwm,qiyAm,\n"
    "(2:43:2:1),<iqAmp,GERUND,qwm,<iqAmp,IV\n"
    "(4:103:5:1),tqwym,GERUND,qwm,taqwiym,II\n"
    "(2:125:4:1),mqAm,GERUND_MEEM,qwm,maqAm,\n"
    "(1:2:1:1),qAm,V,qwm,qAma,\n"
)


def test_no_witness_is_deposited_and_the_barriers_say_why() -> None:
    assert MASAQ_CORPUS_WITNESS is None
    assert MASAQ_COLUMN_BINDING is None
    assert len(open_barriers()) == len(MASAQ_DEPOSIT_BARRIERS)
    for barrier in MASAQ_DEPOSIT_BARRIERS:
        assert barrier.standing is DepositStanding.OPEN
        assert barrier.what_lifts_it.strip()


def test_the_named_residuals_include_the_two_corpora_note() -> None:
    assert "TwoCorporaAreNotOneCorpus" in MASAQ_WITNESS_NAMED_RESIDUALS
    assert "ADigestAloneIsNotADeposit" in MASAQ_WITNESS_NAMED_RESIDUALS
    assert "AColumnBindingIsLegislatedNotRead" in MASAQ_WITNESS_NAMED_RESIDUALS


def _deposit(byte_length: int = 64, sha256: str = MASAQ_ARRIVING_SHA256):  # type: ignore[no-untyped-def]
    return deposit_masaq_witness(
        version="3",
        upstream="upstream مُصطنَع",
        measured_mirror="مرآةٌ مُصطنَعة",
        measured_path="MASAQ.csv",
        byte_length=byte_length,
        licenses=("رخصةٌ مُصطنَعةٌ للاختبار",),
        required_attribution_links=("https://example.invalid/cite",),
        attribution_requirement="إسنادٌ مشروط",
        annotation_note="صفٌّ لكلِّ مقطع",
        sha256=sha256,
    )


def test_a_deposit_refuses_any_digest_but_the_arriving_one() -> None:
    with pytest.raises(MasaqWitnessError):
        _deposit(sha256="0" * 64)


def test_a_deposit_carries_the_two_corpora_note_in_its_annotation() -> None:
    witness = _deposit()
    assert "TwoCorporaAreNotOneCorpus" in witness.annotation_note
    assert "AttributionIsAConditionNotACourtesy" in witness.attribution_requirement
    assert witness.sha256 == MASAQ_ARRIVING_SHA256


def test_bytes_are_refused_when_length_or_digest_differ(tmp_path) -> None:  # type: ignore[no-untyped-def]
    path = tmp_path / "MASAQ.csv"
    path.write_bytes(b"x" * 64)
    with pytest.raises(MasaqWitnessError):
        verified_masaq_bytes(path, _deposit(byte_length=63))
    with pytest.raises(MasaqWitnessError):
        verified_masaq_bytes(path, _deposit(byte_length=64))
    assert hashlib.sha256(b"x" * 64).hexdigest() != MASAQ_ARRIVING_SHA256


def test_rows_are_read_by_declared_names_not_by_position() -> None:
    rows = parse_masaq_rows(SYNTHETIC_CSV, BINDING)
    assert len(rows) == 5
    assert rows[0].location == "(2:3:2:1)"
    assert rows[0].morphological_tag == "GERUND"
    assert [row.verb_form for row in rows] == ["", "IV", "II", "", ""]


def test_a_missing_declared_column_stops_the_reading() -> None:
    without_root = SYNTHETIC_CSV.replace(",root,", ",jidhr,")
    with pytest.raises(MasaqWitnessError):
        parse_masaq_rows(without_root, BINDING)


def test_only_the_declared_masdar_tags_are_masdar() -> None:
    rows = parse_masaq_rows(SYNTHETIC_CSV, BINDING)
    tagged = masdar_rows(rows, BINDING)
    assert len(tagged) == 4
    assert all(row.morphological_tag != "V" for row in tagged)


def test_a_binding_refuses_a_tag_shared_between_the_two_masdar_doors() -> None:
    with pytest.raises(MasaqWitnessError):
        MasaqColumnBinding(
            declared_by="اختبار",
            what_it_assumes="اختبار",
            location_column="a",
            form_column="b",
            morphological_tag_column="c",
            root_column="d",
            lemma_column="e",
            verb_form_column="f",
            masdar_tag_values=("GERUND",),
            meemi_masdar_tag_values=("GERUND",),
        )


def test_a_binding_refuses_one_column_bound_twice() -> None:
    with pytest.raises(MasaqWitnessError):
        MasaqColumnBinding(
            declared_by="اختبار",
            what_it_assumes="اختبار",
            location_column="a",
            form_column="a",
            morphological_tag_column="c",
            root_column="d",
            lemma_column="e",
            verb_form_column="f",
            masdar_tag_values=("GERUND",),
            meemi_masdar_tag_values=("GERUND_MEEM",),
        )


def test_the_binding_digest_moves_when_a_column_moves() -> None:
    other = MasaqColumnBinding(
        declared_by=BINDING.declared_by,
        what_it_assumes=BINDING.what_it_assumes,
        location_column="position",
        form_column=BINDING.form_column,
        morphological_tag_column=BINDING.morphological_tag_column,
        root_column=BINDING.root_column,
        lemma_column=BINDING.lemma_column,
        verb_form_column=BINDING.verb_form_column,
        masdar_tag_values=BINDING.masdar_tag_values,
        meemi_masdar_tag_values=BINDING.meemi_masdar_tag_values,
    )
    assert binding_digest(other) != binding_digest(BINDING)
